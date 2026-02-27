"""Collaborative architecture design conversation orchestration.

Enables users to have a back-and-forth conversation with an AI solutions
architect about a complex problem, which eventually produces a diagram
prompt suitable for generate-raw.

Sessions are automatically saved after each turn for crash recovery.
Use --resume to continue a previous session.
"""

import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from .architect_dspy import ArchitectRefiner
from .config import AppConfig
from .gemini_client import GeminiClient
from .logos import LogoKitHandler
from .mcp_context_enricher import MCPContextEnricher, MCPQuery
from .databricks_style import get_style_prompt
from .models import (
    ArchitectConfig,
    ArchitectSession,
    ArchitectTurn,
    ConversationStatus,
)

console = Console()
DEFAULT_BRANDING_FILE = Path("prompts/branding/databricks_default.txt")


# Prompt template for generating high-quality diagram prompts
DIAGRAM_PROMPT_TEMPLATE = """LOGO KIT (uploaded as image attachments):
Use these EXACT logos - do NOT recreate or substitute.
Do NOT add numbered labels or circles to the diagram.

{logo_descriptions}

LOGO RULES:
- Use EXACT uploaded images - do NOT redraw or recreate
- Only use logos mentioned in the prompt
- Do NOT add numbered circles or labels to logos
- Scale logos uniformly
- NO filenames in output

# {title}
## {subtitle}

---

## DESIGN PHILOSOPHY

**Target Audience:** {audience}
**Visual Style:** {visual_style}
**Aesthetic:** Consulting-firm quality (McKinsey/Deloitte style)
**Key Message:** {key_message}

---

## CANVAS & TYPOGRAPHY

**Canvas:** 1920px × 1080px (16:9 landscape)
**Background:** Pure white (#FFFFFF)
**Font Family:** Inter or Helvetica Neue (clean, professional sans-serif)
**Title:** "{title}" - 24px, navy (#1B3139), top-left, subtle
**No decorative elements, no gradients, no drop shadows**

**CRITICAL: Do NOT render any layout instructions, section headers, or canvas percentages as visible text in the diagram. Only render the actual content labels and descriptions specified below.**

---

## ALIGNMENT REQUIREMENTS

**ALL BOXES MUST BE PERFECTLY ALIGNED:**
- Boxes in the same row must have identical top edges
- Boxes in the same column must have identical left edges
- Use consistent spacing (20px gaps between adjacent boxes)
- All containers must have consistent padding (16px internal)

---

## DIAGRAM CONTENT (LEFT TO RIGHT)

{diagram_content}

---

## VISUAL RULES

✅ DO:
- Use uploaded logos exactly as provided
- PERFECTLY ALIGN all boxes
- Use consistent spacing throughout
- Show clear data flow direction
- Use professional color palette

❌ DO NOT:
- Render any section headers like "ZONE 1:" as visible text
- Display canvas percentage instructions as visible text
- Have jumbled or overlapping boxes
- Have any boxes slightly misaligned
- Modify or recreate logos
- Add numbered circles or step indicators
"""


# Prompt for analyzing a reference architecture image
ARCHITECT_REFERENCE_IMAGE_PROMPT = """Analyze this architecture diagram image in detail. Extract:

1. **Components**: List every distinct component, service, or system shown. For each, note:
   - Name/label
   - Type (database, compute, API, storage, network, external service, etc.)
   - Any technology or product indicated (e.g. Databricks, Azure, Kafka)

2. **Connections & Data Flows**: Describe how components connect:
   - Source and destination
   - Direction (unidirectional, bidirectional)
   - Labels on arrows or connections
   - Flow type (data, control, API call, event, etc.)

3. **Groupings & Zones**: Identify any visual groupings:
   - Named zones, layers, or sections
   - Cloud provider boundaries
   - Network boundaries (VPC, subnet, etc.)
   - Logical tiers (ingestion, processing, serving, etc.)

4. **Layout Pattern**: Describe the overall layout:
   - Flow direction (left-to-right, top-to-bottom, hub-and-spoke, etc.)
   - Number of distinct layers or tiers
   - How the visual hierarchy is organized

5. **Technologies & Logos**: List any specific products or technologies visible:
   - Cloud services (AWS, Azure, GCP specific services)
   - Data platforms (Databricks, Snowflake, etc.)
   - Tools and frameworks

Provide a structured, detailed description that could be used to recreate or evolve this architecture."""


class ArchitectChatbot:
    """Interactive chatbot for collaborative architecture design.

    Workflow:
    1. User describes their problem/requirements
    2. AI asks clarifying questions and proposes architecture
    3. User refines through back-and-forth conversation
    4. AI generates diagram prompt when ready
    """

    def __init__(
        self,
        config: AppConfig,
        arch_config: Optional[ArchitectConfig] = None,
        dspy_model: Optional[str] = None,
        mcp_callback: Optional[Callable[[MCPQuery], Any]] = None,
    ):
        """Initialize the architect chatbot.

        Args:
            config: Application configuration
            arch_config: Architect configuration (uses defaults if not provided)
            dspy_model: Optional Databricks model endpoint for DSPy
            mcp_callback: Optional callback for executing MCP queries.
                         When provided, enables context enrichment from
                         internal knowledge sources (Glean, Slack, etc.)
        """
        self.config = config
        self.arch_config = arch_config or ArchitectConfig()

        # Initialize components
        self.logo_handler = LogoKitHandler(config.logo_kit)

        # Initialize DSPy refiner (deferred to allow for lazy loading)
        self._refiner: Optional[ArchitectRefiner] = None
        self._dspy_model = dspy_model

        # Initialize MCP enricher if callback provided and enrichment enabled
        self._mcp_enricher: Optional[MCPContextEnricher] = None
        if mcp_callback and self.arch_config.mcp_enrichment.enabled:
            self._mcp_enricher = MCPContextEnricher(
                config=self.arch_config.mcp_enrichment,
                mcp_callback=mcp_callback,
            )
            console.print("[dim]MCP context enrichment enabled[/dim]")
        elif self.arch_config.mcp_enrichment.enabled and not mcp_callback:
            console.print(
                "[yellow]Warning: MCP enrichment enabled but no callback provided. "
                "Enrichment requires Claude Code context.[/yellow]"
            )

        # Session state
        self._session: Optional[ArchitectSession] = None
        self._logos: list = []
        self._logo_names: list[str] = []

        # Custom context and reference prompt
        self._custom_context: str = ""
        self._reference_prompt: str = ""
        self._reference_image_analysis: str = ""

    @property
    def refiner(self) -> ArchitectRefiner:
        """Lazy-load the DSPy refiner."""
        if self._refiner is None:
            console.print("[dim]Initializing DSPy architect with Databricks...[/dim]")
            self._refiner = ArchitectRefiner(model=self._dspy_model)
        return self._refiner

    def analyze_reference_image(self, image_path: Path) -> str:
        """Analyze a reference architecture image and append the result.

        Multiple images can be analyzed - each analysis is appended with a
        numbered header. Works for both session-start and mid-chat images.

        Args:
            image_path: Path to the reference image file

        Returns:
            Analysis text describing the architecture in the image
        """
        console.print(f"[bold]Analyzing reference image: {image_path.name}...[/bold]")
        client = GeminiClient()
        analysis = client.analyze_image(
            str(image_path), ARCHITECT_REFERENCE_IMAGE_PROMPT, temperature=0.2
        )
        # Count existing analyses by counting the header markers
        count = self._reference_image_analysis.count("[IMAGE ")
        header = f"[IMAGE {count + 1}: {image_path.name}]"
        separator = "\n\n" if self._reference_image_analysis else ""
        self._reference_image_analysis += f"{separator}{header}\n{analysis}"
        console.print(f"  [green]Analysis complete ({len(analysis)} chars)[/green]")
        return analysis

    def start_session(
        self,
        initial_problem: str,
        context_file: Optional[Path] = None,
        reference_prompt: Optional[Path] = None,
        reference_images: Optional[list[Path]] = None,
    ) -> ArchitectSession:
        """Start a new architect session.

        Args:
            initial_problem: Description of the architecture problem
            context_file: Optional file with domain/customer context
            reference_prompt: Optional existing diagram prompt to use as reference
            reference_images: Optional reference architecture image(s) to analyze

        Returns:
            New ArchitectSession
        """
        # Load logos and hints
        logo_dir = self.arch_config.logo_dir or self.config.logo_kit.logo_dir
        console.print(f"[bold]Loading logos from {logo_dir}...[/bold]")
        self._logos = self.logo_handler.load_logo_kit(logo_dir)
        logo_hints = self.logo_handler.load_logo_hints(logo_dir)
        self._logo_names = [logo.name for logo in self._logos]
        hints_msg = f" with {len(logo_hints)} hints" if logo_hints else ""
        console.print(
            f"  Loaded {len(self._logos)} logos{hints_msg}: {', '.join(self._logo_names[:5])}..."
        )

        # Load custom context if provided
        if context_file:
            console.print(f"[bold]Loading context from {context_file}...[/bold]")
            self._custom_context = context_file.read_text()
        elif self.arch_config.context_file:
            console.print(f"[bold]Loading context from {self.arch_config.context_file}...[/bold]")
            self._custom_context = self.arch_config.context_file.read_text()

        # Load reference prompt if provided
        if reference_prompt:
            console.print(f"[bold]Loading reference prompt from {reference_prompt}...[/bold]")
            self._reference_prompt = reference_prompt.read_text()
        elif self.arch_config.reference_prompt:
            console.print(
                f"[bold]Loading reference prompt from {self.arch_config.reference_prompt}...[/bold]"
            )
            self._reference_prompt = self.arch_config.reference_prompt.read_text()

        # Analyze reference image(s) if provided
        ref_images = reference_images or (
            self.arch_config.reference_images if self.arch_config.reference_images else []
        )
        for ref_image in ref_images:
            self.analyze_reference_image(ref_image)

        # Create session ID from name or generate random
        if self.arch_config.session_name:
            safe_name = re.sub(r"[^\w\-_]", "_", self.arch_config.session_name)
            session_id = safe_name[:50]

            # If directory already exists, append a short random suffix to avoid
            # collisions when multiple sessions share the same name.
            candidate_dir = (
                Path("outputs") / datetime.now().strftime("%Y-%m-%d") / f"architect-{session_id}"
            )
            if candidate_dir.exists():
                session_id = f"{session_id}-{str(uuid.uuid4())[:6]}"
        else:
            session_id = str(uuid.uuid4())[:8]

        self._session = ArchitectSession(
            session_id=session_id,
            initial_problem=initial_problem,
            available_logos=self._logo_names,
            custom_context=self._custom_context if self._custom_context else None,
            created_at=datetime.now().isoformat(),
        )

        console.print(f"\n[bold green]Session started: {session_id}[/bold green]")
        return self._session

    def process_user_input(self, user_input: str) -> tuple[str, bool]:
        """Process user input and get AI response.

        Args:
            user_input: User's message

        Returns:
            Tuple of (AI response, ready_for_output flag)
        """
        if not self._session:
            raise ValueError("No active session. Call start_session() first.")

        # Check for commands
        cmd = user_input.strip().lower()
        if cmd in ("output", "generate"):
            return self._generate_output(), True
        if cmd == "status":
            return self._show_status(), False
        if cmd == "done":
            return "Session ended. Use 'output' to generate the diagram prompt first.", True

        # Enrich context with MCP if available
        enriched_context = self._custom_context
        if self._mcp_enricher:
            mcp_context = self._mcp_enricher.enrich(
                user_input=user_input,
                conversation_history=self._session.get_history_json(),
            )
            if mcp_context:
                enriched_context = (
                    f"{self._custom_context}\n\n{mcp_context}"
                    if self._custom_context
                    else mcp_context
                )

        # Prepend reference image analysis if available
        if self._reference_image_analysis:
            image_context = (
                "[REFERENCE IMAGE ANALYSIS]\n"
                "The user provided an existing architecture diagram:\n\n"
                f"{self._reference_image_analysis}\n"
                "[END REFERENCE IMAGE ANALYSIS]\n\n"
            )
            enriched_context = (
                f"{image_context}{enriched_context}" if enriched_context else image_context
            )

        # Process through DSPy
        response, updated_arch, ready = self.refiner.process_turn(
            user_message=user_input,
            conversation_history=self._session.get_history_json(),
            available_logos=", ".join(self._logo_names),
            current_architecture=self._session.get_architecture_json(),
            custom_context=enriched_context,
            reference_prompt=self._reference_prompt,
        )

        # Update session state
        self._session.current_architecture = updated_arch

        # Create turn
        turn = ArchitectTurn(
            turn_number=len(self._session.turns) + 1,
            user_input=user_input,
            architect_response=response,
            architecture_snapshot=updated_arch.copy(),
            timestamp=datetime.now().isoformat(),
        )
        self._session.add_turn(turn)

        # Notify if ready for output
        if ready:
            response += "\n\n[dim]I believe we have enough information. Type 'output' to generate the diagram prompt, or continue discussing.[/dim]"

        return response, ready

    def _show_status(self) -> str:
        """Show current architecture status.

        Returns:
            Status summary string
        """
        if not self._session:
            return "No active session."

        arch = self._session.current_architecture
        components = arch.get("components", [])
        connections = arch.get("connections", [])

        lines = [
            f"**Session:** {self._session.session_id}",
            f"**Turns:** {len(self._session.turns)}",
            f"**Components:** {len(components)}",
        ]

        if components:
            lines.append("\n**Components:**")
            for comp in components:
                logo = f" ({comp.get('logo_name', 'no logo')})" if comp.get("logo_name") else ""
                lines.append(f"  - {comp.get('label', comp.get('id', 'unknown'))}{logo}")

        if connections:
            lines.append(f"\n**Connections:** {len(connections)}")
            for conn in connections:
                lines.append(
                    f"  - {conn.get('from_id')} → {conn.get('to_id')}: {conn.get('label', '')}"
                )

        return "\n".join(lines)

    def _generate_output(self) -> str:
        """Generate the diagram prompt.

        Returns:
            Generated prompt or error message
        """
        if not self._session:
            return "No active session."

        arch = self._session.current_architecture
        components = arch.get("components", [])

        if len(components) < 2:
            return "Not enough components defined yet. Please describe more of the architecture."

        # Generate conversation summary - use full text for recent turns
        summary_parts = [f"Problem: {self._session.initial_problem}"]
        for turn in self._session.turns[-5:]:  # Last 5 turns for context
            summary_parts.append(f"User: {turn.user_input[:500]}")
            summary_parts.append(f"Architect: {turn.architect_response[:500]}")
        conversation_summary = "\n".join(summary_parts)

        # Use DSPy to generate the prompt
        console.print("\n[yellow]Generating diagram prompt...[/yellow]")

        try:
            prompt, rationale = self.refiner.create_diagram_prompt(
                conversation_summary=conversation_summary,
                architecture_json=json.dumps(arch, indent=2),
                available_logos=", ".join(self._logo_names),
                reference_prompt=self._reference_prompt,
            )

            # Save outputs
            self._save_output(prompt, rationale)

            console.print("\n[bold]Prompt Rationale:[/bold]")
            console.print(Panel(rationale, border_style="cyan"))

            return "Diagram prompt generated and saved. See output directory for files."

        except Exception as e:
            return f"Error generating prompt: {e}"

    def _build_diagram_prompt(self, arch: dict) -> str:
        """Build a diagram prompt from the architecture.

        Args:
            arch: Architecture dictionary

        Returns:
            Complete diagram prompt
        """
        components = arch.get("components", [])
        connections = arch.get("connections", [])

        # Build logo descriptions
        logo_descriptions = []
        for logo in self._logos:
            logo_descriptions.append(f"- {logo.name}: {logo.description}")

        # Build diagram content from components
        content_lines = []
        for i, comp in enumerate(components):
            label = comp.get("label", comp.get("id", f"Component {i+1}"))
            comp_type = comp.get("type", "service")
            logo = comp.get("logo_name", "")

            content_lines.append(f"**{label}**")
            content_lines.append(f"- Type: {comp_type}")
            if logo:
                content_lines.append(f"- Use {logo} logo")
            content_lines.append("")

        # Add connections
        if connections:
            content_lines.append("\n**Data Flows:**")
            for conn in connections:
                from_id = conn.get("from_id", "source")
                to_id = conn.get("to_id", "target")
                label = conn.get("label", "connects to")
                content_lines.append(f"- {from_id} → {to_id}: {label}")

        return DIAGRAM_PROMPT_TEMPLATE.format(
            logo_descriptions="\n".join(logo_descriptions),
            title="Architecture Diagram",
            subtitle="Generated from Architect Conversation",
            audience="Technical stakeholders, architects",
            visual_style="Clean, professional enterprise architecture diagram",
            key_message="Show the system architecture and data flows",
            diagram_content="\n".join(content_lines),
        )

    def _save_output(self, prompt: str, rationale: str) -> Path:
        """Save session output to files.

        Args:
            prompt: Generated diagram prompt
            rationale: Prompt rationale

        Returns:
            Output directory path
        """
        if not self._session:
            raise ValueError("No active session.")

        # Use consistent session directory
        output_dir = self._get_session_dir()
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save session with full recovery information
        self._save_session()

        # Ensure generated prompt carries Databricks branding defaults.
        branded_prompt = prompt
        if "DATABRICKS BRAND STYLE GUIDE" not in branded_prompt:
            branding_section = ""
            if DEFAULT_BRANDING_FILE.exists():
                branding_section = DEFAULT_BRANDING_FILE.read_text().strip()
            branded_prompt = "\n\n".join(
                [s for s in [branding_section, get_style_prompt(), branded_prompt] if s]
            )

        # Save prompt
        (output_dir / "prompt.txt").write_text(branded_prompt)

        # Save architecture JSON
        (output_dir / "architecture.json").write_text(
            json.dumps(self._session.current_architecture, indent=2)
        )

        # Save rationale
        (output_dir / "rationale.txt").write_text(rationale)

        console.print(f"\n[bold green]Output saved to:[/bold green] {output_dir}")
        console.print("  ├── session.json")
        console.print("  ├── prompt.txt")
        console.print("  ├── architecture.json")
        console.print("  └── rationale.txt")

        return output_dir

    def _show_summary(self) -> None:
        """Display conversation summary."""
        if not self._session:
            return

        console.print("\n[bold]Session Summary[/bold]")

        # Show architecture
        arch = self._session.current_architecture
        components = arch.get("components", [])
        connections = arch.get("connections", [])

        table = Table(show_header=True, title="Final Architecture")
        table.add_column("Component", style="cyan")
        table.add_column("Type", style="yellow")
        table.add_column("Logo", style="green")

        for comp in components:
            table.add_row(
                comp.get("label", comp.get("id", "unknown")),
                comp.get("type", "service"),
                comp.get("logo_name", "-"),
            )

        console.print(table)

        console.print(f"\n[bold]Connections:[/bold] {len(connections)}")
        for conn in connections:
            console.print(f"  {conn.get('from_id')} → {conn.get('to_id')}: {conn.get('label', '')}")

        console.print(f"\n[bold]Turns:[/bold] {len(self._session.turns)}")
        console.print(f"[bold]Status:[/bold] {self._session.status.value}")

    def _get_session_dir(self) -> Path:
        """Get the session directory path.

        Creates a consistent directory for session files based on creation date
        and session ID.

        Returns:
            Path to session directory
        """
        if not self._session:
            raise ValueError("No active session.")

        # Use the session's creation date for consistent directory
        if self._session.created_at:
            try:
                created_dt = datetime.fromisoformat(self._session.created_at)
                date_str = created_dt.strftime("%Y-%m-%d")
            except ValueError:
                date_str = datetime.now().strftime("%Y-%m-%d")
        else:
            date_str = datetime.now().strftime("%Y-%m-%d")

        return Path("outputs") / date_str / f"architect-{self._session.session_id}"

    def _save_session(self) -> Path:
        """Save session state for crash recovery.

        Saves the full session state to disk after each turn so the
        conversation can be resumed if interrupted.

        Returns:
            Path to the saved session file
        """
        if not self._session:
            raise ValueError("No active session.")

        session_dir = self._get_session_dir()
        session_dir.mkdir(parents=True, exist_ok=True)

        # Build session data with all recovery information
        session_data = {
            "session_id": self._session.session_id,
            "initial_problem": self._session.initial_problem,
            "status": self._session.status.value,
            "created_at": self._session.created_at,
            "available_logos": self._session.available_logos,
            "custom_context": self._session.custom_context,
            "current_architecture": self._session.current_architecture,
            "turns": [
                {
                    "turn_number": t.turn_number,
                    "user_input": t.user_input,
                    "architect_response": t.architect_response,
                    "architecture_snapshot": t.architecture_snapshot,
                    "timestamp": t.timestamp,
                }
                for t in self._session.turns
            ],
            # Save config for restoration
            "_config": {
                "logo_dir": str(self.arch_config.logo_dir) if self.arch_config.logo_dir else None,
                "max_turns": self.arch_config.max_turns,
                "context_file": (
                    str(self.arch_config.context_file) if self.arch_config.context_file else None
                ),
                "reference_prompt": (
                    str(self.arch_config.reference_prompt)
                    if self.arch_config.reference_prompt
                    else None
                ),
                "output_format": self.arch_config.output_format,
            },
            "_custom_context": self._custom_context,
            "_reference_prompt": self._reference_prompt,
            "_reference_image_analysis": self._reference_image_analysis,
            "_last_saved": datetime.now().isoformat(),
        }

        session_file = session_dir / "session.json"
        session_file.write_text(json.dumps(session_data, indent=2))

        return session_file

    @classmethod
    def find_sessions(cls, base_dir: Path = Path("outputs")) -> list[dict]:
        """Find all saved architect sessions.

        Args:
            base_dir: Base directory to search (default: outputs/)

        Returns:
            List of session info dicts with path, session_id, problem, turns, status
        """
        sessions = []

        if not base_dir.exists():
            return sessions

        # Search for session.json files in architect-* directories
        for date_dir in sorted(base_dir.iterdir(), reverse=True):
            if not date_dir.is_dir():
                continue

            for session_dir in date_dir.iterdir():
                if not session_dir.is_dir() or not session_dir.name.startswith("architect-"):
                    continue

                session_file = session_dir / "session.json"
                if session_file.exists():
                    try:
                        data = json.loads(session_file.read_text())
                        sessions.append(
                            {
                                "path": session_file,
                                "session_id": data.get("session_id", "unknown"),
                                "problem": data.get("initial_problem", "")[:80],
                                "turns": len(data.get("turns", [])),
                                "status": data.get("status", "unknown"),
                                "created_at": data.get("created_at", ""),
                                "last_saved": data.get("_last_saved", ""),
                            }
                        )
                    except (json.JSONDecodeError, KeyError):
                        continue

        return sessions

    @classmethod
    def resume_session(
        cls,
        session_path: Path,
        config: AppConfig,
        dspy_model: Optional[str] = None,
        mcp_callback: Optional[Callable[[MCPQuery], Any]] = None,
    ) -> "ArchitectChatbot":
        """Resume a saved session from disk.

        Args:
            session_path: Path to session.json file or session directory
            config: Application configuration
            dspy_model: Optional Databricks model endpoint
            mcp_callback: Optional MCP callback for enrichment

        Returns:
            ArchitectChatbot instance with restored session
        """
        # Handle both file path and directory path
        if session_path.is_dir():
            session_file = session_path / "session.json"
        else:
            session_file = session_path

        if not session_file.exists():
            raise FileNotFoundError(f"Session file not found: {session_file}")

        # Load session data
        session_data = json.loads(session_file.read_text())

        # Restore arch_config from saved data
        saved_config = session_data.get("_config", {})
        from .models import ArchitectConfig

        arch_config = ArchitectConfig(
            max_turns=saved_config.get("max_turns", 20),
            context_file=(
                Path(saved_config["context_file"]) if saved_config.get("context_file") else None
            ),
            reference_prompt=(
                Path(saved_config["reference_prompt"])
                if saved_config.get("reference_prompt")
                else None
            ),
            output_format=saved_config.get("output_format", "prompt"),
            session_name=session_data.get("session_id"),
            logo_dir=Path(saved_config["logo_dir"]) if saved_config.get("logo_dir") else None,
        )

        # Create chatbot instance
        chatbot = cls(
            config=config,
            arch_config=arch_config,
            dspy_model=dspy_model,
            mcp_callback=mcp_callback,
        )

        # Load logos
        logo_dir = arch_config.logo_dir or config.logo_kit.logo_dir
        console.print(f"[bold]Loading logos from {logo_dir}...[/bold]")
        chatbot._logos = chatbot.logo_handler.load_logo_kit(logo_dir)
        chatbot._logo_names = [logo.name for logo in chatbot._logos]
        console.print(f"  Loaded {len(chatbot._logos)} logos")

        # Restore session state
        chatbot._session = ArchitectSession(
            session_id=session_data["session_id"],
            initial_problem=session_data["initial_problem"],
            available_logos=session_data.get("available_logos", chatbot._logo_names),
            custom_context=session_data.get("custom_context"),
            created_at=session_data.get("created_at", datetime.now().isoformat()),
            status=ConversationStatus(session_data.get("status", "active")),
            current_architecture=session_data.get(
                "current_architecture", {"components": [], "connections": []}
            ),
        )

        # Restore turns
        for turn_data in session_data.get("turns", []):
            turn = ArchitectTurn(
                turn_number=turn_data["turn_number"],
                user_input=turn_data["user_input"],
                architect_response=turn_data["architect_response"],
                architecture_snapshot=turn_data.get("architecture_snapshot"),
                timestamp=turn_data.get("timestamp", ""),
            )
            chatbot._session.turns.append(turn)

        # Restore custom context, reference prompt, and image analysis
        chatbot._custom_context = session_data.get("_custom_context", "")
        chatbot._reference_prompt = session_data.get("_reference_prompt", "")
        chatbot._reference_image_analysis = session_data.get("_reference_image_analysis", "")

        console.print(f"\n[bold green]Session restored: {chatbot._session.session_id}[/bold green]")
        console.print(f"  Turns: {len(chatbot._session.turns)}")
        console.print(f"  Status: {chatbot._session.status.value}")

        return chatbot

    def run_conversation(self, skip_initial: bool = False) -> ArchitectSession:
        """Run the full conversation loop.

        Args:
            skip_initial: If True, skip processing the initial problem
                         (used when resuming a session)

        Returns:
            Completed ArchitectSession
        """
        if not self._session:
            raise ValueError("No active session. Call start_session() first.")

        # Show session panel
        resume_note = " (Resumed)" if skip_initial else ""
        console.print(
            Panel(
                f"[bold]Problem:[/bold] {self._session.initial_problem}\n\n"
                f"[dim]Available logos: {', '.join(self._logo_names[:8])}...[/dim]\n\n"
                f"[dim]Session: {self._session.session_id}{resume_note}[/dim]\n\n"
                "Commands:\n"
                "  • Natural text - continue discussing architecture\n"
                "  • 'output' or 'generate' - generate the diagram prompt\n"
                "  • 'status' - show current architecture state\n"
                "  • 'done' - save and exit",
                title="Architect Session",
                border_style="cyan",
            )
        )

        # Process the initial problem (skip if resuming)
        if not skip_initial:
            response, _ = self.process_user_input(self._session.initial_problem)
            console.print("\n[bold blue]Architect:[/bold blue]")
            console.print(Panel(response, border_style="blue"))

            # Auto-save after initial turn
            session_file = self._save_session()
            console.print(f"[dim]Session auto-saved to {session_file.parent}[/dim]")
        else:
            # Show last response when resuming
            if self._session.turns:
                last_turn = self._session.turns[-1]
                console.print("\n[bold blue]Architect (last response):[/bold blue]")
                console.print(Panel(last_turn.architect_response, border_style="blue"))

        # Conversation loop
        while len(self._session.turns) < self.arch_config.max_turns:
            # Get user input
            console.print()
            user_input = Prompt.ask("[bold green]You[/bold green]")

            if not user_input.strip():
                continue

            # Check for exit
            if user_input.strip().lower() == "done":
                self._session.status = ConversationStatus.COMPLETED
                self._save_session()
                break

            # Process input
            response, should_exit = self.process_user_input(user_input)

            # Auto-save after each turn
            session_file = self._save_session()

            # Display response
            console.print("\n[bold blue]Architect:[/bold blue]")
            console.print(Panel(response, border_style="blue"))
            console.print(f"[dim]Session auto-saved ({len(self._session.turns)} turns)[/dim]")

            if should_exit:
                self._session.status = ConversationStatus.COMPLETED
                self._save_session()
                break

        else:
            console.print("\n[yellow]Max turns reached.[/yellow]")
            self._session.status = ConversationStatus.COMPLETED
            self._save_session()

        # Show summary
        self._show_summary()

        return self._session
