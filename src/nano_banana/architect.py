"""Collaborative architecture design conversation orchestration.

Enables users to have a back-and-forth conversation with an AI solutions
architect about a complex problem, which eventually produces a diagram
prompt suitable for generate-raw.
"""

import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from .architect_dspy import ArchitectRefiner
from .config import AppConfig
from .logos import LogoKitHandler
from .models import (
    ArchitectConfig,
    ArchitectSession,
    ArchitectTurn,
    ConversationStatus,
)

console = Console()


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
    ):
        """Initialize the architect chatbot.

        Args:
            config: Application configuration
            arch_config: Architect configuration (uses defaults if not provided)
            dspy_model: Optional Databricks model endpoint for DSPy
        """
        self.config = config
        self.arch_config = arch_config or ArchitectConfig()

        # Initialize components
        self.logo_handler = LogoKitHandler(config.logo_kit)

        # Initialize DSPy refiner (deferred to allow for lazy loading)
        self._refiner: Optional[ArchitectRefiner] = None
        self._dspy_model = dspy_model

        # Session state
        self._session: Optional[ArchitectSession] = None
        self._logos: list = []
        self._logo_names: list[str] = []

        # Custom context and reference prompt
        self._custom_context: str = ""
        self._reference_prompt: str = ""

    @property
    def refiner(self) -> ArchitectRefiner:
        """Lazy-load the DSPy refiner."""
        if self._refiner is None:
            console.print("[dim]Initializing DSPy architect with Databricks...[/dim]")
            self._refiner = ArchitectRefiner(model=self._dspy_model)
        return self._refiner

    def start_session(
        self,
        initial_problem: str,
        context_file: Optional[Path] = None,
        reference_prompt: Optional[Path] = None,
    ) -> ArchitectSession:
        """Start a new architect session.

        Args:
            initial_problem: Description of the architecture problem
            context_file: Optional file with domain/customer context
            reference_prompt: Optional existing diagram prompt to use as reference

        Returns:
            New ArchitectSession
        """
        # Load logos
        logo_dir = self.arch_config.logo_dir or self.config.logo_kit.logo_dir
        console.print(f"[bold]Loading logos from {logo_dir}...[/bold]")
        self._logos = self.logo_handler.load_logo_kit(logo_dir)
        self._logo_names = [logo.name for logo in self._logos]
        console.print(f"  Loaded {len(self._logos)} logos: {', '.join(self._logo_names[:5])}...")

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
            console.print(f"[bold]Loading reference prompt from {self.arch_config.reference_prompt}...[/bold]")
            self._reference_prompt = self.arch_config.reference_prompt.read_text()

        # Create session ID from name or generate random
        if self.arch_config.session_name:
            safe_name = re.sub(r'[^\w\-_]', '_', self.arch_config.session_name)
            session_id = safe_name[:50]
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

        # Process through DSPy
        response, updated_arch, ready = self.refiner.process_turn(
            user_message=user_input,
            conversation_history=self._session.get_history_json(),
            available_logos=", ".join(self._logo_names),
            current_architecture=self._session.get_architecture_json(),
            custom_context=self._custom_context,
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

        return response, False

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
                logo = f" ({comp.get('logo_name', 'no logo')})" if comp.get('logo_name') else ""
                lines.append(f"  - {comp.get('label', comp.get('id', 'unknown'))}{logo}")

        if connections:
            lines.append(f"\n**Connections:** {len(connections)}")
            for conn in connections:
                lines.append(f"  - {conn.get('from_id')} → {conn.get('to_id')}: {conn.get('label', '')}")

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

        # Generate conversation summary
        summary_parts = [f"Problem: {self._session.initial_problem}"]
        for turn in self._session.turns[-5:]:  # Last 5 turns for context
            summary_parts.append(f"User: {turn.user_input[:100]}...")
            summary_parts.append(f"Architect: {turn.architect_response[:100]}...")
        conversation_summary = "\n".join(summary_parts)

        # Use DSPy to generate the prompt
        console.print("\n[yellow]Generating diagram prompt...[/yellow]")

        try:
            prompt, rationale = self.refiner.create_diagram_prompt(
                conversation_summary=conversation_summary,
                architecture_json=json.dumps(arch, indent=2),
                available_logos=", ".join(self._logo_names),
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

        # Create output directory
        output_dir = Path("outputs") / datetime.now().strftime("%Y-%m-%d") / f"architect-{self._session.session_id}"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save session JSON
        session_data = {
            "session_id": self._session.session_id,
            "initial_problem": self._session.initial_problem,
            "status": self._session.status.value,
            "created_at": self._session.created_at,
            "available_logos": self._session.available_logos,
            "custom_context": self._session.custom_context,
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
            "final_architecture": self._session.current_architecture,
        }

        (output_dir / "session.json").write_text(json.dumps(session_data, indent=2))

        # Save prompt
        (output_dir / "prompt.txt").write_text(prompt)

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

    def run_conversation(self) -> ArchitectSession:
        """Run the full conversation loop.

        Returns:
            Completed ArchitectSession
        """
        if not self._session:
            raise ValueError("No active session. Call start_session() first.")

        # Show initial prompt
        console.print(Panel(
            f"[bold]Problem:[/bold] {self._session.initial_problem}\n\n"
            f"[dim]Available logos: {', '.join(self._logo_names[:8])}...[/dim]\n\n"
            "Commands:\n"
            "  • Natural text - continue discussing architecture\n"
            "  • 'output' or 'generate' - generate the diagram prompt\n"
            "  • 'status' - show current architecture state\n"
            "  • 'done' - save and exit",
            title="Architect Session",
            border_style="cyan",
        ))

        # Process the initial problem
        response, _ = self.process_user_input(self._session.initial_problem)
        console.print("\n[bold blue]Architect:[/bold blue]")
        console.print(Panel(response, border_style="blue"))

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
                break

            # Process input
            response, should_exit = self.process_user_input(user_input)

            # Display response
            console.print("\n[bold blue]Architect:[/bold blue]")
            console.print(Panel(response, border_style="blue"))

            if should_exit:
                self._session.status = ConversationStatus.COMPLETED
                break

        else:
            console.print("\n[yellow]Max turns reached.[/yellow]")
            self._session.status = ConversationStatus.COMPLETED

        # Show summary
        self._show_summary()

        return self._session

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
