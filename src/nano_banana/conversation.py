"""Conversational diagram refinement chatbot orchestration.

Enables iterative refinement of architecture diagrams through a
generate -> evaluate -> feedback -> refine loop.
"""

import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

from .config import AppConfig
from .conversation_dspy import ConversationalRefiner
from .gemini_client import GeminiClient
from .logos import LogoKitHandler
from .mlflow_tracker import MLflowTracker
from .models import (
    ConversationConfig,
    ConversationSession,
    ConversationStatus,
    ConversationTurn,
    DiagramSpec,
)
from .prompts import PromptBuilder

console = Console()


class ConversationChatbot:
    """Interactive chatbot for iterative diagram refinement.

    Workflow:
    1. User provides initial prompt or diagram spec
    2. System generates diagram
    3. User scores result (1-5)
    4. User provides feedback
    5. DSPy refines prompt based on conversation history
    6. Repeat until satisfied
    """

    def __init__(
        self,
        config: AppConfig,
        conv_config: Optional[ConversationConfig] = None,
        dspy_model: Optional[str] = None,
    ):
        """Initialize the chatbot.

        Args:
            config: Application configuration
            conv_config: Conversation configuration (uses defaults if not provided)
            dspy_model: Optional Databricks model endpoint for DSPy refinement
        """
        self.config = config
        self.conv_config = conv_config or ConversationConfig()

        # Initialize components
        self.logo_handler = LogoKitHandler(config.logo_kit)
        self.prompt_builder = PromptBuilder()
        self.gemini_client = GeminiClient()
        self.mlflow_tracker = MLflowTracker(config.mlflow)

        # Initialize DSPy refiner (deferred to allow for lazy loading)
        self._refiner: Optional[ConversationalRefiner] = None
        self._dspy_model = dspy_model

        # Session state
        self._session: Optional[ConversationSession] = None
        self._logos: list = []
        self._logo_parts: list = []

    @property
    def refiner(self) -> ConversationalRefiner:
        """Lazy-load the DSPy refiner."""
        if self._refiner is None:
            console.print("[dim]Initializing DSPy refiner with Databricks...[/dim]")
            self._refiner = ConversationalRefiner(model=self._dspy_model)
        return self._refiner

    def start_session(
        self,
        initial_prompt: Optional[str] = None,
        diagram_spec: Optional[DiagramSpec] = None,
        template_id: Optional[str] = None,
        diagram_spec_path: Optional[Path] = None,
    ) -> ConversationSession:
        """Start a new conversation session.

        Args:
            initial_prompt: Direct prompt text (mutually exclusive with diagram_spec)
            diagram_spec: Diagram specification (builds prompt from spec)
            template_id: Template ID to use with diagram_spec
            diagram_spec_path: Path to diagram spec for tracking

        Returns:
            New ConversationSession

        Raises:
            ValueError: If neither prompt nor spec provided
        """
        if not initial_prompt and not diagram_spec:
            raise ValueError("Must provide either initial_prompt or diagram_spec")

        # Load logos
        logo_dir = self.conv_config.logo_dir or self.config.logo_kit.logo_dir
        console.print(f"[bold]Loading logos from {logo_dir}...[/bold]")
        self._logos = self.logo_handler.load_logo_kit(logo_dir)
        console.print(f"  Loaded {len(self._logos)} logos")

        # Convert logos to image parts for generation
        self._logo_parts = [
            self.logo_handler.to_image_part(logo) for logo in self._logos
        ]

        # Build initial prompt
        if diagram_spec:
            template = self.prompt_builder.load_template(template_id or "baseline")
            initial_prompt = self.prompt_builder.build_prompt(
                template, diagram_spec, self._logos
            )
        else:
            # For raw prompts, prepend logo section
            logo_section = self.prompt_builder._build_logo_section(self._logos)
            initial_prompt = f"{logo_section}\n\n{initial_prompt}"

        # Create session
        session_id = str(uuid.uuid4())[:8]
        self._session = ConversationSession(
            session_id=session_id,
            initial_prompt=initial_prompt,
            created_at=datetime.now().isoformat(),
            diagram_spec_path=diagram_spec_path,
            template_id=template_id,
        )

        console.print(f"\n[bold green]Session started: {session_id}[/bold green]")
        return self._session

    def run_iteration(self, prompt: str) -> ConversationTurn:
        """Run a single generation iteration.

        Args:
            prompt: The prompt to use for generation

        Returns:
            ConversationTurn with generation results
        """
        if not self._session:
            raise ValueError("No active session. Call start_session() first.")

        iteration = len(self._session.turns) + 1

        # Initialize MLflow
        self.mlflow_tracker.initialize()

        # Start MLflow run
        run_name = f"chat-{self._session.session_id}-iter-{iteration}"
        run_id = self.mlflow_tracker.start_run(run_name=run_name)

        try:
            # Log parameters
            self.mlflow_tracker.log_parameters({
                "session_id": self._session.session_id,
                "iteration": iteration,
                "prompt_template_id": self._session.template_id or "raw",
                "logo_count": len(self._logos),
                "temperature": self.conv_config.temperature,
            })

            # Log prompt
            self.mlflow_tracker.log_prompt(prompt, "prompt.txt")

            console.print(f"\n[bold cyan]Iteration {iteration}[/bold cyan]")
            console.print("[yellow]Generating diagram...[/yellow]")

            # Generate image
            start_time = time.time()
            image_bytes, response_text, metadata = self.gemini_client.generate_image(
                prompt=prompt,
                logo_parts=self._logo_parts,
                temperature=self.conv_config.temperature,
            )
            generation_time = time.time() - start_time

            # Save image
            output_dir = Path("outputs") / datetime.now().strftime("%Y-%m-%d") / f"chat-{self._session.session_id}"
            output_dir.mkdir(parents=True, exist_ok=True)
            image_path = output_dir / f"iteration_{iteration}.png"
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            # Log to MLflow
            self.mlflow_tracker.log_output_image(image_path)
            self.mlflow_tracker.log_metrics({
                "generation_time_seconds": generation_time,
                "iteration": iteration,
            })

            console.print(f"[green]Generated in {generation_time:.1f}s[/green]")
            console.print(f"[dim]Image saved: {image_path}[/dim]")

            # Create turn
            turn = ConversationTurn(
                iteration=iteration,
                prompt_used=prompt,
                run_id=run_id,
                image_path=image_path,
                generation_time_seconds=generation_time,
            )

            # Auto-analyze if enabled
            if self.conv_config.auto_analyze:
                console.print("[dim]Analyzing image...[/dim]")
                try:
                    analysis = self.gemini_client.analyze_image(
                        str(image_path),
                        "Describe this architecture diagram in detail. "
                        "Note: logo placement, text legibility, layout clarity, "
                        "any visual issues, and overall quality."
                    )
                    turn.visual_analysis = analysis
                except Exception as e:
                    console.print(f"[yellow]Analysis failed: {e}[/yellow]")

            self.mlflow_tracker.end_run("FINISHED")
            return turn

        except Exception as e:
            self.mlflow_tracker.end_run("FAILED")
            raise

    def collect_feedback(self, turn: ConversationTurn) -> tuple[int, str]:
        """Collect user feedback for a turn.

        Args:
            turn: The turn to collect feedback for

        Returns:
            Tuple of (score, feedback_text)
        """
        console.print(f"\n[bold]Please review the image:[/bold]")
        console.print(f"  [cyan]{turn.image_path}[/cyan]")

        if turn.visual_analysis:
            console.print(f"\n[bold]AI Analysis:[/bold]")
            # Truncate long analysis
            analysis = turn.visual_analysis[:500]
            if len(turn.visual_analysis) > 500:
                analysis += "..."
            console.print(Panel(analysis, title="Visual Analysis", border_style="dim"))

        console.print()

        # Get score
        score = IntPrompt.ask(
            "[bold]Score (1-5)[/bold]",
            default=3,
            choices=["1", "2", "3", "4", "5"],
        )

        # Get feedback
        feedback = Prompt.ask(
            "[bold]Feedback[/bold] (what to improve, or 'done' if satisfied)",
            default="",
        )

        turn.score = score
        turn.feedback = feedback

        return score, feedback

    def refine_prompt(
        self,
        current_prompt: str,
        turn: ConversationTurn,
    ) -> str:
        """Refine the prompt based on feedback using DSPy.

        Args:
            current_prompt: The current prompt
            turn: The turn with feedback

        Returns:
            Refined prompt
        """
        console.print("\n[yellow]Refining prompt with DSPy...[/yellow]")

        # Get conversation history
        history = self._session.get_history_json() if self._session else "[]"

        # Run refinement
        refined_prompt, reasoning, expected = self.refiner.refine_with_context(
            session_history=history,
            original_prompt=self._session.initial_prompt if self._session else current_prompt,
            current_prompt=current_prompt,
            feedback=turn.feedback or "",
            score=turn.score or 3,
            visual_analysis=turn.visual_analysis or "",
        )

        # Store reasoning
        turn.refinement_reasoning = reasoning

        console.print(f"\n[bold]Refinement Reasoning:[/bold]")
        console.print(Panel(reasoning, border_style="cyan"))
        console.print(f"\n[bold]Expected Improvement:[/bold]")
        console.print(Panel(expected, border_style="green"))

        return refined_prompt

    def run_conversation(self) -> ConversationSession:
        """Run the full conversation loop.

        Returns:
            Completed ConversationSession
        """
        if not self._session:
            raise ValueError("No active session. Call start_session() first.")

        current_prompt = self._session.initial_prompt

        console.print(Panel(
            f"Starting conversation refinement loop\n"
            f"Target score: {self.conv_config.target_score}\n"
            f"Max iterations: {self.conv_config.max_iterations}\n"
            f"Type 'done' or score {self.conv_config.target_score} to finish",
            title="Conversation Session",
            border_style="cyan",
        ))

        while len(self._session.turns) < self.conv_config.max_iterations:
            # Generate
            turn = self.run_iteration(current_prompt)

            # Collect feedback
            score, feedback = self.collect_feedback(turn)

            # Add turn to session
            self._session.add_turn(turn)

            # Check if done
            if feedback.lower() == "done" or score >= self.conv_config.target_score:
                self._session.status = ConversationStatus.COMPLETED
                console.print("\n[bold green]Target reached! Conversation complete.[/bold green]")
                break

            # Refine prompt for next iteration
            current_prompt = self.refine_prompt(current_prompt, turn)

        else:
            # Max iterations reached
            console.print("\n[yellow]Max iterations reached.[/yellow]")
            self._session.status = ConversationStatus.COMPLETED

        # Show summary
        self._show_summary()

        return self._session

    def _show_summary(self) -> None:
        """Display conversation summary."""
        if not self._session:
            return

        console.print("\n[bold]Conversation Summary[/bold]")

        # Create summary table
        table = Table(show_header=True)
        table.add_column("Iter", style="cyan", width=4)
        table.add_column("Score", style="magenta", width=5)
        table.add_column("Time", style="yellow", width=6)
        table.add_column("Feedback", style="white")

        for turn in self._session.turns:
            table.add_row(
                str(turn.iteration),
                str(turn.score) if turn.score else "-",
                f"{turn.generation_time_seconds:.1f}s",
                (turn.feedback or "-")[:50],
            )

        console.print(table)

        # Show best result
        best = self._session.get_best_turn()
        if best:
            console.print(f"\n[bold green]Best result:[/bold green] Iteration {best.iteration} (Score: {best.score})")
            console.print(f"  Image: {best.image_path}")
            console.print(f"  Run ID: {best.run_id}")

        # Save session
        self._save_session()

    def _save_session(self) -> None:
        """Save session to JSON file."""
        if not self._session:
            return

        output_dir = Path("outputs") / datetime.now().strftime("%Y-%m-%d") / f"chat-{self._session.session_id}"
        output_dir.mkdir(parents=True, exist_ok=True)

        session_file = output_dir / "session.json"
        session_data = {
            "session_id": self._session.session_id,
            "status": self._session.status.value,
            "created_at": self._session.created_at,
            "diagram_spec_path": str(self._session.diagram_spec_path) if self._session.diagram_spec_path else None,
            "template_id": self._session.template_id,
            "turns": [
                {
                    "iteration": t.iteration,
                    "run_id": t.run_id,
                    "image_path": str(t.image_path),
                    "generation_time_seconds": t.generation_time_seconds,
                    "score": t.score,
                    "feedback": t.feedback,
                    "visual_analysis": t.visual_analysis,
                    "refinement_reasoning": t.refinement_reasoning,
                }
                for t in self._session.turns
            ],
        }

        with open(session_file, "w") as f:
            json.dump(session_data, f, indent=2)

        console.print(f"\n[dim]Session saved: {session_file}[/dim]")
