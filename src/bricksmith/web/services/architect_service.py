"""Service layer wrapping ArchitectChatbot for web use."""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from ...architect import ArchitectChatbot
from ...config import AppConfig, load_config
from ...gemini_client import GeminiClient
from ...image_generator import ImageGenerator
from ...models import ArchitectConfig, ArchitectSession, ArchitectTurn, ConversationStatus
from ...openai_image_client import OpenAIImageClient
from ..api.schemas import (
    ArchitectureState,
    ComponentSchema,
    ConnectionSchema,
    MessageResponse,
    SessionResponse,
    StatusResponse,
    GenerateOutputResponse,
    GeneratePreviewResponse,
)
from .session_store import get_session_store


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

    @property
    def config(self) -> AppConfig:
        """Lazy-load application config."""
        if self._config is None:
            self._config = load_config()
        return self._config

    @property
    def _image_generator(self) -> ImageGenerator:
        """Image generator from config (Gemini or OpenAI), cached per service."""
        if self._image_generator_instance is None:
            prov = self.config.image_provider
            if prov.provider == "openai":
                self._image_generator_instance = OpenAIImageClient(model=prov.openai_model)
            else:
                self._image_generator_instance = GeminiClient()
        return self._image_generator_instance

    async def create_session(
        self,
        initial_problem: str,
        custom_context: Optional[str] = None,
        logo_dir: Optional[str] = None,
    ) -> SessionResponse:
        """Create a new architect session.

        Args:
            initial_problem: Description of the architecture problem
            custom_context: Optional additional context
            logo_dir: Optional path to logo directory

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
        logo_path = logo_dir or str(self.config.logo_kit.logo_dir)
        logos = chatbot.logo_handler.load_logo_kit(logo_path)
        chatbot.logo_handler.load_logo_hints(logo_path)
        available_logos = [logo.name for logo in logos]

        # Store in session store
        store = get_session_store()
        session_response = await store.create_session(
            session_id=session_id,
            initial_problem=initial_problem,
            custom_context=custom_context,
            available_logos=available_logos,
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

        # Cache chatbot instance
        self._chatbots[session_id] = chatbot

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
        logo_path = str(self.config.logo_kit.logo_dir)

        logos = chatbot.logo_handler.load_logo_kit(logo_path)
        chatbot.logo_handler.load_logo_hints(logo_path)
        chatbot._logos = logos
        chatbot._logo_names = [logo.name for logo in logos]
        chatbot._custom_context = session_data.get("custom_context") or ""

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
    ) -> Optional[MessageResponse]:
        """Send a message in a session and get the response.

        Args:
            session_id: Session ID
            message: User's message

        Returns:
            MessageResponse with AI response and updated state
        """
        chatbot = await self._get_or_restore_chatbot(session_id)
        if chatbot is None:
            return None

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

    async def generate_preview(self, session_id: str) -> GeneratePreviewResponse:
        """Generate a diagram preview image from the current architecture.

        Args:
            session_id: Session ID

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
                        # Logo not found, skip it
                        pass

            # Generate image using configured provider (Gemini or OpenAI)
            image_bytes, response_text, metadata = self._image_generator.generate_image(
                prompt=prompt,
                logo_parts=logo_parts,
            )

            # Create output directory and save image
            run_id = f"preview-{session_id}-{datetime.now().strftime('%H%M%S')}"
            output_dir = Path("outputs") / datetime.now().strftime("%Y-%m-%d") / run_id
            output_dir.mkdir(parents=True, exist_ok=True)

            image_path = output_dir / "diagram.png"
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            # Return URL for serving the image
            image_url = f"/api/images/{datetime.now().strftime('%Y-%m-%d')}/{run_id}/diagram.png"

            return GeneratePreviewResponse(
                success=True,
                image_url=image_url,
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
