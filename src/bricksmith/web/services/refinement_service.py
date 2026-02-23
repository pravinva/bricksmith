"""Service for managing the diagram refinement loop in web sessions.

Reuses existing components:
- conversation.build_evaluation_prompt() for LLM Judge evaluation
- GeminiClient.analyze_image() for image analysis
- ConversationalRefiner.refine_with_context() for DSPy prompt refinement
- ArchitectService for image generation resources (logos, image generator, prompts)
"""

import asyncio
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from ...conversation import build_evaluation_prompt
from ...conversation_dspy import ConversationalRefiner
from ...gemini_client import GeminiClient
from ..api.schemas import (
    EvaluationScores,
    RefineResponse,
    RefinementIterationResponse,
    RefinementIterationSchema,
    RefinementStateResponse,
)

logger = logging.getLogger(__name__)


class _RefinementState:
    """In-memory state for a single session's refinement loop."""

    def __init__(self, session_id: str, original_prompt: str):
        self.session_id = session_id
        self.original_prompt = original_prompt
        self.current_prompt = original_prompt
        self.current_image_url: Optional[str] = None
        self.status = "idle"  # idle, generating, evaluating, refining
        self.iterations: list[RefinementIterationSchema] = []

    def to_response(self) -> RefinementStateResponse:
        return RefinementStateResponse(
            session_id=self.session_id,
            status=self.status,
            original_prompt=self.original_prompt,
            current_prompt=self.current_prompt,
            current_image_url=self.current_image_url,
            iterations=self.iterations,
            iteration_count=len(self.iterations),
        )


class RefinementService:
    """Manages per-session refinement state and orchestrates the refinement loop.

    Gets image generation resources (logos, image generator, prompt builder) from
    ArchitectService to avoid duplication.
    """

    def __init__(self):
        self._states: dict[str, _RefinementState] = {}
        self._refiner: Optional[ConversationalRefiner] = None
        self._gemini_analyzer: Optional[GeminiClient] = None

    def _get_refiner(self) -> ConversationalRefiner:
        """Lazy-initialize DSPy refiner."""
        if self._refiner is None:
            self._refiner = ConversationalRefiner()
        return self._refiner

    def _get_analyzer(self) -> GeminiClient:
        """Lazy-initialize Gemini client for image analysis."""
        if self._gemini_analyzer is None:
            self._gemini_analyzer = GeminiClient()
        return self._gemini_analyzer

    async def start_refinement(self, session_id: str) -> RefinementStateResponse:
        """Start a refinement loop from the current architect session state.

        Gets the diagram prompt from ArchitectService and initializes state.
        """
        from .architect_service import get_architect_service

        service = get_architect_service()
        chatbot = await service._get_or_restore_chatbot(session_id)
        if chatbot is None:
            raise ValueError(f"Session {session_id} not found")

        session = chatbot._session
        if session is None:
            raise ValueError(f"No active session for {session_id}")

        arch = session.current_architecture
        prompt = service._build_diagram_prompt(arch, session.initial_problem)

        state = _RefinementState(session_id=session_id, original_prompt=prompt)
        self._states[session_id] = state

        return state.to_response()

    async def generate_and_evaluate(self, session_id: str) -> RefinementIterationResponse:
        """Generate an image from current prompt and evaluate it with LLM Judge.

        Returns a RefinementIterationResponse with the full iteration data.
        """
        from .architect_service import get_architect_service

        state = self._states.get(session_id)
        if state is None:
            return RefinementIterationResponse(
                success=False, error="No refinement in progress for this session"
            )

        service = get_architect_service()
        chatbot = await service._get_or_restore_chatbot(session_id)
        if chatbot is None:
            return RefinementIterationResponse(success=False, error="Session not found")

        try:
            # Phase 1: Generate image
            state.status = "generating"

            session = chatbot._session
            arch = session.current_architecture if session else {}
            components = arch.get("components", [])

            # Build logo parts (reuses architect_service pattern)
            logo_parts = []
            logos_used: set[str] = set()
            for comp in components:
                logo_name = comp.get("logo_name")
                if logo_name and logo_name not in logos_used:
                    try:
                        logo = chatbot.logo_handler.get_logo(logo_name)
                        logo_part = chatbot.logo_handler.to_image_part(logo)
                        logo_parts.append(logo_part)
                        logos_used.add(logo_name)
                    except KeyError:
                        pass

            # Get per-session image generator or default
            image_generator = service._session_image_generators.get(session_id)
            if image_generator is None:
                from ...openai_image_client import OpenAIImageClient

                provider_override = service._session_provider_overrides.get(session_id)
                if provider_override == "openai":
                    image_generator = OpenAIImageClient(
                        model=service.config.image_provider.openai_model
                    )
                elif provider_override == "gemini":
                    image_generator = GeminiClient()
                else:
                    image_generator = service._image_generator
            gen = image_generator

            image_bytes, response_text, metadata = await asyncio.to_thread(
                gen.generate_image,
                prompt=state.current_prompt,
                logo_parts=logo_parts,
            )

            # Save image
            iteration_num = len(state.iterations) + 1
            run_id = f"refine-{session_id}-{iteration_num}-" f"{datetime.now().strftime('%H%M%S')}"
            output_dir = Path("outputs") / datetime.now().strftime("%Y-%m-%d") / run_id
            output_dir.mkdir(parents=True, exist_ok=True)

            image_path = output_dir / "diagram.png"
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_url = f"/api/images/{datetime.now().strftime('%Y-%m-%d')}/{run_id}/diagram.png"
            state.current_image_url = image_url

            # Phase 2: Evaluate with LLM Judge
            state.status = "evaluating"
            eval_prompt = build_evaluation_prompt("architect")

            analyzer = self._get_analyzer()
            eval_response = await asyncio.to_thread(
                analyzer.analyze_image,
                str(image_path),
                eval_prompt,
                0.2,
            )

            # Parse evaluation JSON (same pattern as conversation.py auto_evaluate)
            json_match = re.search(r"\{[\s\S]*\}", eval_response)
            scores = None
            overall_score = None
            strengths: list[str] = []
            issues: list[str] = []
            improvements: list[str] = []
            feedback = ""

            if json_match:
                try:
                    eval_data = json.loads(json_match.group())
                    raw_scores = eval_data.get("scores", {})
                    overall_score = int(round(eval_data.get("overall_score", 0)))
                    strengths = eval_data.get("strengths", [])
                    issues = eval_data.get("issues", [])
                    improvements = eval_data.get("actionable_improvements", [])
                    feedback = eval_data.get("feedback_for_refinement", "")

                    scores = EvaluationScores(
                        information_hierarchy=raw_scores.get("information_hierarchy", 0),
                        technical_accuracy=raw_scores.get("technical_accuracy", 0),
                        logo_fidelity=raw_scores.get("logo_fidelity", 0),
                        visual_clarity=raw_scores.get("visual_clarity", 0),
                        data_flow_legibility=raw_scores.get("data_flow_legibility", 0),
                        text_readability=raw_scores.get("text_readability", 0),
                    )
                except (json.JSONDecodeError, ValueError) as e:
                    logger.warning("Failed to parse evaluation JSON: %s", e)

            iteration = RefinementIterationSchema(
                iteration=iteration_num,
                prompt_used=state.current_prompt,
                image_url=image_url,
                overall_score=overall_score,
                scores=scores,
                strengths=strengths,
                issues=issues,
                improvements=improvements,
                feedback_for_refinement=feedback,
                created_at=datetime.now().isoformat(),
            )

            state.iterations.append(iteration)
            state.status = "idle"

            return RefinementIterationResponse(success=True, iteration=iteration)

        except Exception as e:
            logger.error("Error in generate_and_evaluate for %s: %s", session_id, e, exc_info=True)
            state.status = "idle"
            return RefinementIterationResponse(success=False, error=str(e))

    async def refine_prompt(self, session_id: str, user_feedback: str) -> RefineResponse:
        """Refine the current prompt using DSPy with user feedback.

        Uses ConversationalRefiner.refine_with_context() to generate a new prompt.
        """
        state = self._states.get(session_id)
        if state is None:
            return RefineResponse(success=False, error="No refinement in progress for this session")

        if not state.iterations:
            return RefineResponse(
                success=False, error="No iterations yet - generate an image first"
            )

        try:
            state.status = "refining"

            latest = state.iterations[-1]

            # Store user feedback on the latest iteration
            latest.user_feedback = user_feedback

            # Build session history for DSPy context
            history = [
                {
                    "iteration": it.iteration,
                    "score": it.overall_score,
                    "feedback": it.user_feedback or it.feedback_for_refinement,
                }
                for it in state.iterations
            ]

            refiner = self._get_refiner()
            refined_prompt, reasoning, expected_improvement = await asyncio.to_thread(
                refiner.refine_with_context,
                session_history=json.dumps(history),
                original_prompt=state.original_prompt,
                current_prompt=state.current_prompt,
                feedback=user_feedback or latest.feedback_for_refinement,
                score=latest.overall_score or 5,
                visual_analysis="; ".join(latest.issues) if latest.issues else "",
            )

            state.current_prompt = refined_prompt
            latest.refinement_reasoning = reasoning
            state.status = "idle"

            return RefineResponse(
                success=True,
                refined_prompt=refined_prompt,
                reasoning=reasoning,
                expected_improvement=expected_improvement,
            )

        except Exception as e:
            logger.error("Error in refine_prompt for %s: %s", session_id, e, exc_info=True)
            state.status = "idle"
            return RefineResponse(success=False, error=str(e))

    def get_state(self, session_id: str) -> Optional[RefinementStateResponse]:
        """Get the current refinement state for a session."""
        state = self._states.get(session_id)
        if state is None:
            return None
        return state.to_response()


# Singleton instance
_refinement_service: Optional[RefinementService] = None


def get_refinement_service() -> RefinementService:
    """Get the singleton refinement service instance."""
    global _refinement_service
    if _refinement_service is None:
        _refinement_service = RefinementService()
    return _refinement_service
