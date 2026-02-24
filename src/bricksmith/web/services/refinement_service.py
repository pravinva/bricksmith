"""Service for managing the diagram refinement loop in web sessions.

Wraps ConversationChatbot to reuse the exact same generate -> evaluate -> refine
loop as the CLI `bricksmith chat` command. This ensures prompts are properly built
with logo constraints, negative prompts, and all enhancement logic.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from ...config import AppConfig, load_config
from ...conversation import ConversationChatbot
from ...gemini_client import GeminiClient
from ...image_generator import ImageGenerator
from ...models import ConversationConfig, GenerationSettings
from ..api.schemas import (
    EvaluationScores,
    GenerationSettingsRequest,
    RefineResponse,
    RefinementIterationResponse,
    RefinementIterationSchema,
    RefinementStateResponse,
)

logger = logging.getLogger(__name__)


def _settings_from_request(
    settings_req: Optional[GenerationSettingsRequest],
) -> Optional[GenerationSettings]:
    """Convert a web GenerationSettingsRequest to the models.GenerationSettings used by the chatbot."""
    if settings_req is None:
        return None

    from ...conversation import GENERATION_PRESETS

    # Start from preset if provided, otherwise defaults
    if settings_req.preset and settings_req.preset in GENERATION_PRESETS:
        settings = GENERATION_PRESETS[settings_req.preset].model_copy()
    else:
        settings = GenerationSettings()

    # Explicit overrides
    if settings_req.image_size is not None:
        settings.image_size = settings_req.image_size
    if settings_req.aspect_ratio is not None:
        settings.aspect_ratio = settings_req.aspect_ratio

    return settings


def _image_url_from_path(image_path: Path) -> str:
    """Convert a local image path like outputs/2026-02-24/chat-xyz/iteration_1.png to an API URL."""
    parts = image_path.parts
    try:
        idx = parts.index("outputs")
        relative = "/".join(parts[idx + 1 :])
        return f"/api/images/{relative}"
    except ValueError:
        return f"/api/images/{image_path.name}"


def _resolve_image_generator(
    config: AppConfig,
    image_provider: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    vertex_api_key: Optional[str] = None,
) -> Optional[ImageGenerator]:
    """Create an image generator for the given provider, or None to use the default."""
    if image_provider == "openai":
        from ...openai_image_client import OpenAIImageClient

        return OpenAIImageClient(
            api_key=openai_api_key or None,
            model=config.image_provider.openai_model,
        )
    elif image_provider == "databricks":
        from ...databricks_image_client import DatabricksImageClient

        return DatabricksImageClient(
            model=config.image_provider.databricks_model,
            image_model=config.image_provider.databricks_image_model,
        )
    elif image_provider == "gemini" and vertex_api_key:
        return GeminiClient(api_key=vertex_api_key)
    return None


class RefinementService:
    """Manages per-session refinement using ConversationChatbot.

    Wraps the same chat loop as the CLI `bricksmith chat` command, ensuring
    prompts are built with logo constraints, evaluated with the LLM Judge,
    and refined with DSPy using full session context.
    """

    def __init__(self):
        self._chatbots: dict[str, ConversationChatbot] = {}
        # Track raw user prompt separately (chatbot prepends logo section)
        self._raw_prompts: dict[str, str] = {}
        # Track iteration schemas for API responses (richer than ConversationTurn)
        self._iterations: dict[str, list[RefinementIterationSchema]] = {}
        self._statuses: dict[str, str] = {}  # idle, generating, evaluating, refining

    async def start_refinement(self, session_id: str) -> RefinementStateResponse:
        """Start a refinement loop from the current architect session state.

        Gets the diagram prompt from ArchitectService and initializes a
        ConversationChatbot with that prompt.
        """
        from .architect_service import get_architect_service

        service = get_architect_service()
        arch_chatbot = await service._get_or_restore_chatbot(session_id)
        if arch_chatbot is None:
            raise ValueError(f"Session {session_id} not found")

        arch_session = arch_chatbot._session
        if arch_session is None:
            raise ValueError(f"No active session for {session_id}")

        arch = arch_session.current_architecture
        prompt = service._build_diagram_prompt(arch, arch_session.initial_problem)

        # Resolve image generator from architect service overrides
        image_gen = service._session_image_generators.get(session_id)
        if image_gen is None:
            provider_override = service._session_provider_overrides.get(session_id)
            image_gen = _resolve_image_generator(service.config, provider_override)

        return await self._init_chatbot(session_id, prompt, service.config, image_gen)

    async def start_standalone_refinement(
        self,
        prompt: str,
        image_provider: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        vertex_api_key: Optional[str] = None,
    ) -> RefinementStateResponse:
        """Start a standalone refinement loop from a raw prompt.

        Creates a ConversationChatbot that loads logos, builds the full prompt
        with logo constraints, and prepares for the generate/evaluate/refine loop.
        """
        import uuid

        session_id = f"standalone-{str(uuid.uuid4())[:8]}"
        config = load_config()

        image_gen = _resolve_image_generator(config, image_provider, openai_api_key, vertex_api_key)

        return await self._init_chatbot(session_id, prompt, config, image_gen)

    async def _init_chatbot(
        self,
        session_id: str,
        prompt: str,
        config: AppConfig,
        image_generator: Optional[ImageGenerator] = None,
    ) -> RefinementStateResponse:
        """Create and initialize a ConversationChatbot for the refinement loop."""
        conv_config = ConversationConfig(
            auto_refine=True,
            auto_analyze=True,
            session_name=session_id,
        )

        chatbot = ConversationChatbot(
            config=config,
            conv_config=conv_config,
            image_generator=image_generator,
        )

        # start_session loads logos, builds logo section, prepends to prompt
        await asyncio.to_thread(chatbot.start_session, prompt)

        self._chatbots[session_id] = chatbot
        self._raw_prompts[session_id] = prompt
        self._iterations[session_id] = []
        self._statuses[session_id] = "idle"

        return self._build_state_response(session_id)

    async def generate_and_evaluate(
        self,
        session_id: str,
        settings_req: Optional[GenerationSettingsRequest] = None,
    ) -> RefinementIterationResponse:
        """Generate an image and evaluate it with the LLM Judge.

        Uses ConversationChatbot.run_iteration() for generation (same as CLI)
        and ConversationChatbot.auto_evaluate() for scoring.
        """
        chatbot = self._chatbots.get(session_id)
        if chatbot is None or chatbot._session is None:
            return RefinementIterationResponse(
                success=False, error="No refinement in progress for this session"
            )

        try:
            self._statuses[session_id] = "generating"

            gen_settings = _settings_from_request(settings_req)
            num_variants = (
                settings_req.num_variants if settings_req and settings_req.num_variants else None
            )
            current_prompt = chatbot._session.get_latest_prompt()

            # Generate image(s) using the same logic as CLI `bricksmith chat`
            turn = await asyncio.to_thread(
                chatbot.run_iteration,
                prompt=current_prompt,
                settings=gen_settings,
                is_retry=len(chatbot._session.turns) > 0,
                num_variants_override=num_variants,
            )

            # Evaluate with LLM Judge (same as CLI auto-refine mode)
            self._statuses[session_id] = "evaluating"
            score, feedback = await asyncio.to_thread(chatbot.auto_evaluate, turn)

            # End MLflow run (run_iteration leaves it open for scoring)
            try:
                chatbot.mlflow_tracker.log_metrics({"score": score})
                chatbot.mlflow_tracker.end_run("FINISHED")
            except Exception:
                pass

            # Add turn to session
            chatbot._session.add_turn(turn)

            # Build image URLs from saved paths
            image_urls = [_image_url_from_path(p) for p in turn.variant_paths]
            if not image_urls:
                image_urls = [_image_url_from_path(turn.image_path)]
            image_url = _image_url_from_path(turn.image_path)

            # Parse evaluation scores from visual_analysis if available
            scores = None
            strengths: list[str] = []
            issues: list[str] = []
            improvements: list[str] = []

            if turn.visual_analysis:
                try:
                    eval_data = json.loads(turn.visual_analysis)
                    raw_scores = eval_data.get("scores", {})
                    strengths = eval_data.get("strengths", [])
                    issues = eval_data.get("issues", [])
                    improvements = eval_data.get("actionable_improvements", [])

                    scores = EvaluationScores(
                        information_hierarchy=raw_scores.get("information_hierarchy", 0),
                        technical_accuracy=raw_scores.get("technical_accuracy", 0),
                        logo_fidelity=raw_scores.get("logo_fidelity", 0),
                        visual_clarity=raw_scores.get("visual_clarity", 0),
                        data_flow_legibility=raw_scores.get("data_flow_legibility", 0),
                        text_readability=raw_scores.get("text_readability", 0),
                    )
                except (json.JSONDecodeError, ValueError):
                    pass

            iteration = RefinementIterationSchema(
                iteration=turn.iteration,
                prompt_used=turn.prompt_used,
                image_url=image_url,
                image_urls=image_urls,
                overall_score=score,
                scores=scores,
                strengths=strengths,
                issues=issues,
                improvements=improvements,
                feedback_for_refinement=feedback,
                settings_used=settings_req,
                created_at=datetime.now().isoformat(),
            )

            self._iterations.setdefault(session_id, []).append(iteration)
            self._statuses[session_id] = "idle"

            return RefinementIterationResponse(success=True, iteration=iteration)

        except Exception as e:
            logger.error("Error in generate_and_evaluate for %s: %s", session_id, e, exc_info=True)
            self._statuses[session_id] = "idle"
            # Try to end MLflow run on error
            try:
                chatbot.mlflow_tracker.end_run("FAILED")
            except Exception:
                pass
            return RefinementIterationResponse(success=False, error=str(e))

    async def refine_prompt(self, session_id: str, user_feedback: str) -> RefineResponse:
        """Refine the current prompt using DSPy with user feedback.

        Uses ConversationChatbot.refine_prompt() which passes full session history,
        original prompt (with logo constraints), and visual analysis to DSPy.
        """
        chatbot = self._chatbots.get(session_id)
        if chatbot is None or chatbot._session is None:
            return RefineResponse(success=False, error="No refinement in progress for this session")

        if not chatbot._session.turns:
            return RefineResponse(
                success=False, error="No iterations yet - generate an image first"
            )

        try:
            self._statuses[session_id] = "refining"

            latest_turn = chatbot._session.turns[-1]
            latest_turn.feedback = user_feedback

            # Store user feedback on the iteration schema too
            iterations = self._iterations.get(session_id, [])
            if iterations:
                iterations[-1].user_feedback = user_feedback

            current_prompt = chatbot._session.get_latest_prompt()

            # Refine using DSPy with full session context (same as CLI)
            refined_prompt = await asyncio.to_thread(
                chatbot.refine_prompt,
                current_prompt=current_prompt,
                turn=latest_turn,
            )

            # Store reasoning on iteration schema
            if iterations and latest_turn.refinement_reasoning:
                iterations[-1].refinement_reasoning = latest_turn.refinement_reasoning

            self._statuses[session_id] = "idle"

            return RefineResponse(
                success=True,
                refined_prompt=refined_prompt,
                reasoning=latest_turn.refinement_reasoning or "",
                expected_improvement="",
            )

        except Exception as e:
            logger.error("Error in refine_prompt for %s: %s", session_id, e, exc_info=True)
            self._statuses[session_id] = "idle"
            return RefineResponse(success=False, error=str(e))

    def get_state(self, session_id: str) -> Optional[RefinementStateResponse]:
        """Get the current refinement state for a session."""
        if session_id not in self._chatbots:
            return None
        return self._build_state_response(session_id)

    def _build_state_response(self, session_id: str) -> RefinementStateResponse:
        """Build a RefinementStateResponse from chatbot state."""
        chatbot = self._chatbots[session_id]
        session = chatbot._session
        iterations = self._iterations.get(session_id, [])
        status = self._statuses.get(session_id, "idle")

        current_image_url = None
        if iterations:
            current_image_url = iterations[-1].image_url

        return RefinementStateResponse(
            session_id=session_id,
            status=status,
            original_prompt=self._raw_prompts.get(session_id, ""),
            current_prompt=session.get_latest_prompt() if session else "",
            current_image_url=current_image_url,
            iterations=iterations,
            iteration_count=len(iterations),
        )


# Singleton instance
_refinement_service: Optional[RefinementService] = None


def get_refinement_service() -> RefinementService:
    """Get the singleton refinement service instance."""
    global _refinement_service
    if _refinement_service is None:
        _refinement_service = RefinementService()
    return _refinement_service
