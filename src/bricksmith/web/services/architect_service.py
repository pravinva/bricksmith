"""Service layer wrapping ArchitectChatbot for web use."""

import base64
import logging
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Literal

from ...architect import ArchitectChatbot
from ...config import AppConfig, load_config
from ...gemini_client import GeminiClient
from ...image_generator import ImageGenerator
from ...mcp_config import MCPEnrichmentConfig
from ...mcp_context_enricher import MCPContextEnricher
from ...models import ArchitectConfig, ArchitectSession, ArchitectTurn, ConversationStatus
from ...databricks_image_client import DatabricksImageClient
from ...openai_image_client import OpenAIImageClient
from ..api.schemas import (
    ArchitectureState,
    ComponentSchema,
    ConnectionSchema,
    GenerationSettingsRequest,
    MCPEnrichmentOptions,
    MessageResponse,
    SessionResponse,
    StatusResponse,
    GenerateOutputResponse,
    GeneratePreviewResponse,
)
from .session_store import get_session_store

logger = logging.getLogger(__name__)


class ArchitectService:
    """Service for managing architect sessions via the web interface.

    This service wraps the ArchitectChatbot for stateless HTTP request handling,
    using the session store for persistence between requests.
    """

    def __init__(self):
        """Initialize the architect service."""
        self._config: Optional[AppConfig] = None
        self._image_generator_instance: Optional[ImageGenerator] = None
        self._chatbots: dict[str, ArchitectChatbot] = {}
        self._session_image_generators: dict[str, ImageGenerator] = {}
        self._session_provider_overrides: dict[str, Literal["gemini", "openai", "databricks"]] = {}
        self._session_mcp_config: dict[str, MCPEnrichmentOptions] = {}

    @property
    def config(self) -> AppConfig:
        """Lazy-load application config."""
        if self._config is None:
            self._config = load_config()
        return self._config

    @property
    def _image_generator(self) -> ImageGenerator:
        """Image generator from config (Gemini, OpenAI, or Databricks), cached per service."""
        if self._image_generator_instance is None:
            prov = self.config.image_provider
            if prov.provider == "openai":
                self._image_generator_instance = OpenAIImageClient(model=prov.openai_model)
            elif prov.provider == "databricks":
                self._image_generator_instance = DatabricksImageClient(
                    model=prov.databricks_model,
                    image_model=prov.databricks_image_model,
                )
            else:
                self._image_generator_instance = GeminiClient()
        return self._image_generator_instance

    async def create_session(
        self,
        initial_problem: str,
        custom_context: Optional[str] = None,
        logo_dir: Optional[str] = None,
        image_provider: Optional[Literal["gemini", "openai", "databricks"]] = None,
        openai_api_key: Optional[str] = None,
        vertex_api_key: Optional[str] = None,
        reference_prompt: Optional[str] = None,
        reference_prompt_path: Optional[str] = None,
        reference_image_base64: Optional[str] = None,
        reference_image_filename: Optional[str] = None,
        reference_images_base64: Optional[list[str]] = None,
        reference_images_filenames: Optional[list[str]] = None,
        mcp_enrichment: Optional[MCPEnrichmentOptions] = None,
    ) -> SessionResponse:
        """Create a new architect session.

        Args:
            initial_problem: Description of the architecture problem
            custom_context: Optional additional context
            logo_dir: Optional path to logo directory
            image_provider: Optional per-session image provider override
            openai_api_key: Optional per-session OpenAI key
            vertex_api_key: Optional per-session Gemini/Vertex key
            reference_prompt: Optional existing prompt text as reference
            reference_prompt_path: Optional path to prompt file to load as reference
            reference_image_base64: Optional base64-encoded reference image (single, backward compat)
            reference_image_filename: Optional original filename for MIME detection (single)
            reference_images_base64: Optional list of base64-encoded reference images
            reference_images_filenames: Optional filenames corresponding to reference_images_base64
            mcp_enrichment: Optional MCP enrichment configuration

        Returns:
            SessionResponse with new session details
        """
        session_id = str(uuid.uuid4())[:8]

        # Create architect config
        arch_config = ArchitectConfig(
            logo_dir=Path(logo_dir) if logo_dir else None,
        )

        # Create chatbot instance
        chatbot = ArchitectChatbot(
            config=self.config,
            arch_config=arch_config,
        )

        # Start session (this loads logos and initializes state)
        # We need to capture logo names before starting the session
        logo_path = Path(logo_dir) if logo_dir else self.config.logo_kit.logo_dir
        logos = chatbot.logo_handler.load_logo_kit(logo_path)
        chatbot.logo_handler.load_logo_hints(logo_path)
        available_logos = [logo.name for logo in logos]

        # Resolve reference prompt: explicit text takes priority, then load from path
        resolved_reference_prompt = reference_prompt or ""
        if not resolved_reference_prompt and reference_prompt_path:
            ref_path = Path(reference_prompt_path)
            if ref_path.exists():
                resolved_reference_prompt = ref_path.read_text()
            else:
                logger.warning("Reference prompt path not found: %s", reference_prompt_path)

        # Store in session store
        store = get_session_store()
        session_response = await store.create_session(
            session_id=session_id,
            initial_problem=initial_problem,
            custom_context=custom_context,
            available_logos=available_logos,
            reference_prompt=resolved_reference_prompt or None,
        )

        # Start the chatbot session
        chatbot._session = ArchitectSession(
            session_id=session_id,
            initial_problem=initial_problem,
            available_logos=available_logos,
            custom_context=custom_context,
            created_at=datetime.now().isoformat(),
        )
        chatbot._logos = logos
        chatbot._logo_names = available_logos
        chatbot._custom_context = custom_context or ""
        chatbot._reference_prompt = resolved_reference_prompt

        # Analyze reference image(s) if provided
        # Build list: multi-image field first, then fall back to single-image field
        images_to_analyze: list[tuple[str, Optional[str]]] = []
        if reference_images_base64:
            for i, img_b64 in enumerate(reference_images_base64):
                fname = (
                    reference_images_filenames[i]
                    if reference_images_filenames and i < len(reference_images_filenames)
                    else None
                )
                images_to_analyze.append((img_b64, fname))
        elif reference_image_base64:
            images_to_analyze.append((reference_image_base64, reference_image_filename))

        for img_b64, fname in images_to_analyze:
            try:
                image_data = base64.b64decode(img_b64)
                suffix = ".png"
                if fname:
                    ext = Path(fname).suffix.lower()
                    if ext in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
                        suffix = ext
                with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                    tmp.write(image_data)
                    tmp_path = Path(tmp.name)
                try:
                    chatbot.analyze_reference_image(tmp_path)
                    logger.info(
                        "Reference image analyzed for session %s (%d chars)",
                        session_id,
                        len(chatbot._reference_image_analysis),
                    )
                finally:
                    tmp_path.unlink(missing_ok=True)
            except Exception as e:
                logger.warning("Failed to analyze reference image: %s", e)

        # Set up MCP enrichment if requested
        if mcp_enrichment and mcp_enrichment.enabled:
            self._session_mcp_config[session_id] = mcp_enrichment
            try:
                mcp_config = MCPEnrichmentConfig(
                    enabled=True,
                    sources=mcp_enrichment.sources,
                )
                chatbot._mcp_enricher = MCPContextEnricher(
                    config=mcp_config,
                    use_native=True,
                )
                logger.info("MCP enrichment enabled for session %s", session_id)
            except Exception as e:
                logger.warning("Failed to initialize MCP enricher: %s", e)

        # Cache chatbot instance
        self._chatbots[session_id] = chatbot

        # Optional per-session image generator override from user-supplied keys.
        # Keys are kept in memory only for the current app process.
        selected_provider = image_provider or self.config.image_provider.provider
        if image_provider:
            self._session_provider_overrides[session_id] = image_provider
        if selected_provider == "openai":
            if openai_api_key:
                self._session_image_generators[session_id] = OpenAIImageClient(
                    api_key=openai_api_key,
                    model=self.config.image_provider.openai_model,
                )
        elif selected_provider == "databricks":
            self._session_image_generators[session_id] = DatabricksImageClient(
                model=self.config.image_provider.databricks_model,
                image_model=self.config.image_provider.databricks_image_model,
            )
        elif selected_provider == "gemini":
            if vertex_api_key:
                self._session_image_generators[session_id] = GeminiClient(
                    api_key=vertex_api_key,
                )

        return session_response

    async def get_session(self, session_id: str) -> Optional[SessionResponse]:
        """Get a session by ID."""
        store = get_session_store()
        return await store.get_session(session_id)

    async def list_sessions(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[SessionResponse], int]:
        """List sessions with pagination."""
        store = get_session_store()
        return await store.list_sessions(limit, offset)

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        # Remove from cache
        if session_id in self._chatbots:
            del self._chatbots[session_id]
        if session_id in self._session_image_generators:
            del self._session_image_generators[session_id]
        if session_id in self._session_provider_overrides:
            del self._session_provider_overrides[session_id]
        if session_id in self._session_mcp_config:
            del self._session_mcp_config[session_id]

        store = get_session_store()
        return await store.delete_session(session_id)

    async def _get_or_restore_chatbot(self, session_id: str) -> Optional[ArchitectChatbot]:
        """Get chatbot from cache or restore from database.

        Args:
            session_id: Session ID

        Returns:
            ArchitectChatbot instance or None if session not found
        """
        # Check cache first
        if session_id in self._chatbots:
            return self._chatbots[session_id]

        # Restore from database
        store = get_session_store()
        session_data = await store.get_full_session_data(session_id)

        if session_data is None:
            return None

        # Create architect config
        arch_config = ArchitectConfig()

        # Create chatbot instance
        chatbot = ArchitectChatbot(
            config=self.config,
            arch_config=arch_config,
        )

        # Restore session state
        available_logos = session_data.get("available_logos", [])
        logo_path = self.config.logo_kit.logo_dir

        logos = chatbot.logo_handler.load_logo_kit(logo_path)
        chatbot.logo_handler.load_logo_hints(logo_path)
        chatbot._logos = logos
        chatbot._logo_names = [logo.name for logo in logos]
        chatbot._custom_context = session_data.get("custom_context") or ""
        chatbot._reference_prompt = session_data.get("reference_prompt") or ""
        chatbot._reference_image_analysis = session_data.get("reference_image_analysis") or ""

        # Restore MCP enricher from stored config
        if session_id in self._session_mcp_config:
            mcp_opts = self._session_mcp_config[session_id]
            try:
                mcp_config = MCPEnrichmentConfig(
                    enabled=True,
                    sources=mcp_opts.sources,
                )
                chatbot._mcp_enricher = MCPContextEnricher(
                    config=mcp_config,
                    use_native=True,
                )
            except Exception as e:
                logger.warning("Failed to restore MCP enricher: %s", e)

        # Restore session
        chatbot._session = ArchitectSession(
            session_id=session_id,
            initial_problem=session_data["initial_problem"],
            available_logos=available_logos,
            custom_context=session_data.get("custom_context"),
            created_at=session_data["created_at"],
            status=ConversationStatus(session_data.get("status", "active")),
        )

        # Restore architecture
        if session_data.get("current_architecture"):
            chatbot._session.current_architecture = session_data["current_architecture"]

        # Restore turns
        for turn_data in session_data.get("turns", []):
            turn = ArchitectTurn(
                turn_number=turn_data["turn_number"],
                user_input=turn_data["user_input"],
                architect_response=turn_data["architect_response"],
                architecture_snapshot=turn_data.get("architecture_snapshot", {}),
                timestamp=turn_data.get("created_at", datetime.now().isoformat()),
            )
            chatbot._session.turns.append(turn)

        # Cache for future requests
        self._chatbots[session_id] = chatbot

        return chatbot

    async def send_message(
        self,
        session_id: str,
        message: str,
        image_base64: Optional[str] = None,
        image_filename: Optional[str] = None,
    ) -> Optional[MessageResponse]:
        """Send a message in a session and get the response.

        Args:
            session_id: Session ID
            message: User's message
            image_base64: Optional base64-encoded image to analyze as context
            image_filename: Optional original filename for MIME detection

        Returns:
            MessageResponse with AI response and updated state
        """
        chatbot = await self._get_or_restore_chatbot(session_id)
        if chatbot is None:
            return None

        # Analyze mid-chat image if provided
        if image_base64:
            try:
                image_data = base64.b64decode(image_base64)
                suffix = ".png"
                if image_filename:
                    ext = Path(image_filename).suffix.lower()
                    if ext in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
                        suffix = ext
                with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                    tmp.write(image_data)
                    tmp_path = Path(tmp.name)
                try:
                    chatbot.analyze_reference_image(tmp_path)
                    logger.info(
                        "Mid-chat image analyzed for session %s (%d chars)",
                        session_id,
                        len(chatbot._reference_image_analysis),
                    )
                finally:
                    tmp_path.unlink(missing_ok=True)
            except Exception as e:
                logger.warning("Failed to analyze mid-chat image: %s", e)

        # Process through chatbot
        response, ready_for_output = chatbot.process_user_input(message)

        # Get updated architecture state
        arch = chatbot._session.current_architecture if chatbot._session else {}
        architecture = self._convert_architecture(arch)

        # Get turn number
        turn_number = len(chatbot._session.turns) if chatbot._session else 0

        # Persist to database
        store = get_session_store()

        # Update session with new architecture
        await store.update_session(
            session_id=session_id,
            architecture=arch,
        )

        # Add turn if it was a normal message (not a command)
        if chatbot._session and chatbot._session.turns:
            latest_turn = chatbot._session.turns[-1]
            await store.add_turn(
                session_id=session_id,
                turn_number=latest_turn.turn_number,
                user_input=latest_turn.user_input,
                architect_response=latest_turn.architect_response,
                architecture_snapshot=latest_turn.architecture_snapshot,
            )

        return MessageResponse(
            response=response,
            ready_for_output=ready_for_output,
            architecture=architecture,
            turn_number=turn_number,
        )

    async def get_status(self, session_id: str) -> Optional[StatusResponse]:
        """Get current architecture status for a session.

        Args:
            session_id: Session ID

        Returns:
            StatusResponse with current state
        """
        chatbot = await self._get_or_restore_chatbot(session_id)
        if chatbot is None:
            return None

        session = chatbot._session
        if session is None:
            return None

        arch = session.current_architecture
        architecture = self._convert_architecture(arch)

        # Determine if ready for output
        components = arch.get("components", [])
        ready_for_output = len(components) >= 2

        return StatusResponse(
            session_id=session_id,
            status=session.status.value,
            turn_count=len(session.turns),
            ready_for_output=ready_for_output,
            architecture=architecture,
            available_logos=session.available_logos or [],
            image_provider=self._session_provider_overrides.get(
                session_id,
                self.config.image_provider.provider,
            ),
            credential_mode=(
                "custom_key" if session_id in self._session_image_generators else "environment"
            ),
        )

    async def generate_output(
        self,
        session_id: str,
        output_dir: Optional[str] = None,
    ) -> GenerateOutputResponse:
        """Generate the final diagram prompt.

        Args:
            session_id: Session ID
            output_dir: Optional output directory

        Returns:
            GenerateOutputResponse with file paths
        """
        chatbot = await self._get_or_restore_chatbot(session_id)
        if chatbot is None:
            return GenerateOutputResponse(
                success=False,
                error="Session not found",
            )

        try:
            # Use the chatbot's generate output method
            response, _ = chatbot.process_user_input("output")

            # Get the output directory
            session = chatbot._session
            if session:
                base_dir = Path(output_dir) if output_dir else Path("outputs")
                out_dir = base_dir / datetime.now().strftime("%Y-%m-%d") / f"architect-{session_id}"

                # Update session status
                store = get_session_store()
                await store.update_session(session_id, status="completed")

                return GenerateOutputResponse(
                    success=True,
                    output_dir=str(out_dir),
                    prompt_file=str(out_dir / "prompt.txt"),
                    architecture_file=str(out_dir / "architecture.json"),
                )
            else:
                return GenerateOutputResponse(
                    success=False,
                    error="No active session",
                )

        except Exception as e:
            return GenerateOutputResponse(
                success=False,
                error=str(e),
            )

    async def generate_preview(
        self,
        session_id: str,
        settings_req: Optional[GenerationSettingsRequest] = None,
    ) -> GeneratePreviewResponse:
        """Generate a diagram preview image from the current architecture.

        Args:
            session_id: Session ID
            settings_req: Optional generation settings (preset, size, ratio, variants)

        Returns:
            GeneratePreviewResponse with image URL and run ID
        """
        chatbot = await self._get_or_restore_chatbot(session_id)
        if chatbot is None:
            return GeneratePreviewResponse(
                success=False,
                error="Session not found",
            )

        try:
            session = chatbot._session
            if session is None:
                return GeneratePreviewResponse(
                    success=False,
                    error="No active session",
                )

            arch = session.current_architecture
            components = arch.get("components", [])

            if len(components) < 1:
                return GeneratePreviewResponse(
                    success=False,
                    error="No components defined in architecture",
                )

            # Resolve generation settings
            gen_kwargs: dict = {}
            num_variants = 1
            if settings_req:
                gen_kwargs = settings_req.to_generation_kwargs()
                num_variants = settings_req.num_variants or 1

            # Build prompt from architecture
            prompt = self._build_diagram_prompt(arch, session.initial_problem)

            # Load logos
            logo_parts = []
            logos_used = set()
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

            # Generate image using per-session override when provided, otherwise app default.
            image_generator = self._session_image_generators.get(session_id)
            if image_generator is None:
                provider_override = self._session_provider_overrides.get(session_id)
                if provider_override == "openai":
                    image_generator = OpenAIImageClient(
                        model=self.config.image_provider.openai_model
                    )
                elif provider_override == "databricks":
                    image_generator = DatabricksImageClient(
                        model=self.config.image_provider.databricks_model,
                        image_model=self.config.image_provider.databricks_image_model,
                    )
                elif provider_override == "gemini":
                    image_generator = GeminiClient()
                else:
                    image_generator = self._image_generator

            # Create output directory
            run_id = f"preview-{session_id}-{datetime.now().strftime('%H%M%S')}"
            date_str = datetime.now().strftime("%Y-%m-%d")
            output_dir = Path("outputs") / date_str / run_id
            output_dir.mkdir(parents=True, exist_ok=True)

            # Generate variant(s)
            image_urls: list[str] = []
            for v in range(num_variants):
                image_bytes, response_text, metadata = image_generator.generate_image(
                    prompt=prompt,
                    logo_parts=logo_parts,
                    **gen_kwargs,
                )
                filename = "diagram.png" if v == 0 else f"diagram_v{v + 1}.png"
                image_path = output_dir / filename
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                image_urls.append(f"/api/images/{date_str}/{run_id}/{filename}")

            return GeneratePreviewResponse(
                success=True,
                image_url=image_urls[0],
                image_urls=image_urls,
                run_id=run_id,
            )

        except Exception as e:
            return GeneratePreviewResponse(
                success=False,
                error=str(e),
            )

    def _build_diagram_prompt(self, arch: dict, initial_problem: str) -> str:
        """Build a diagram generation prompt from architecture state.

        Args:
            arch: Architecture dictionary
            initial_problem: Original problem description

        Returns:
            Prompt string for diagram generation
        """
        components = arch.get("components", [])
        connections = arch.get("connections", [])
        title = arch.get("title", "Architecture Diagram")
        subtitle = arch.get("subtitle", "")

        # Build component descriptions
        comp_lines = []
        for comp in components:
            label = comp.get("label", comp.get("id", ""))
            comp_type = comp.get("type", "service")
            logo = comp.get("logo_name", "")
            logo_desc = f" (use {logo} logo)" if logo else ""
            comp_lines.append(f"- {label}: {comp_type}{logo_desc}")

        # Build connection descriptions
        conn_lines = []
        comp_map = {c.get("id"): c.get("label", c.get("id")) for c in components}
        for conn in connections:
            from_label = comp_map.get(conn.get("from_id"), conn.get("from_id"))
            to_label = comp_map.get(conn.get("to_id"), conn.get("to_id"))
            conn_label = conn.get("label", "connects to")
            style = conn.get("style", "solid")
            conn_lines.append(f"- {from_label} {conn_label} {to_label} ({style} line)")

        prompt = f"""Create a professional architecture diagram for: {initial_problem}

Title: {title}
{f'Subtitle: {subtitle}' if subtitle else ''}

Components:
{chr(10).join(comp_lines)}

Connections/Data Flow:
{chr(10).join(conn_lines) if conn_lines else '- Show logical relationships between components'}

Requirements:
- Use the uploaded logos exactly as provided for each component
- Professional presentation style with clean layout
- Clear data flow arrows between connected components
- High contrast text labels
- White background
"""
        return prompt

    def _convert_architecture(self, arch: dict) -> ArchitectureState:
        """Convert architecture dict to schema.

        Args:
            arch: Architecture dictionary from chatbot

        Returns:
            ArchitectureState schema
        """
        components = []
        for comp in arch.get("components", []):
            components.append(
                ComponentSchema(
                    id=comp.get("id", ""),
                    label=comp.get("label", ""),
                    type=comp.get("type", "service"),
                    logo_name=comp.get("logo_name"),
                )
            )

        connections = []
        for conn in arch.get("connections", []):
            connections.append(
                ConnectionSchema(
                    from_id=conn.get("from_id", ""),
                    to_id=conn.get("to_id", ""),
                    label=conn.get("label"),
                    style=conn.get("style", "solid"),
                )
            )

        return ArchitectureState(
            components=components,
            connections=connections,
            title=arch.get("title"),
            subtitle=arch.get("subtitle"),
        )


# Singleton instance
_architect_service: Optional[ArchitectService] = None


def get_architect_service() -> ArchitectService:
    """Get the singleton architect service instance."""
    global _architect_service
    if _architect_service is None:
        _architect_service = ArchitectService()
    return _architect_service
