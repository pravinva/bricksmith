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

# Design principles evaluation prompt for automatic refinement
REFERENCE_IMAGE_ANALYSIS_PROMPT = """Analyze this reference architecture diagram and extract its design patterns and style characteristics.

Identify and describe:
1. **Layout Pattern** - Flow direction, component arrangement, grouping strategy
2. **Visual Style** - Color palette, background, borders, shadows
3. **Typography** - Font styles, label positioning, text hierarchy
4. **Logo Treatment** - Size, placement, spacing around logos
5. **Connection Style** - Arrow types, line weights, connection routing
6. **Overall Composition** - Balance, whitespace usage, visual hierarchy

Provide a concise summary that can be used to guide generation of similar diagrams.
Format your response as a structured description that another AI can use as style guidance."""


REFERENCE_COMPARISON_PROMPT = """You are an expert architecture diagram reviewer. Compare the generated diagram against the reference image and evaluate how well it matches the reference style.

REFERENCE IMAGE STYLE:
{reference_style}

EVALUATION CRITERIA (score each 1-5 based on how well it matches the reference):

1. **Layout Match** - Does it follow the same flow direction and component arrangement?
   - 5: Excellent match to reference layout
   - 3: Partial match, some differences
   - 1: Completely different layout

2. **Visual Style Match** - Does it use similar colors, backgrounds, and styling?
   - 5: Consistent with reference style
   - 3: Some style elements match
   - 1: Very different visual style

3. **Typography Match** - Are labels and text styled similarly?
   - 5: Text treatment matches reference
   - 3: Partial match
   - 1: Very different text styling

4. **Logo Treatment** - Are logos sized and positioned similarly?
   - 5: Logo treatment matches reference
   - 3: Some differences in logo handling
   - 1: Very different logo treatment

5. **Overall Quality** - Is it professional and presentation-ready?
   - 5: Excellent quality, matches reference standard
   - 3: Acceptable quality
   - 1: Poor quality

RESPONSE FORMAT (use exactly this JSON structure):
```json
{{
  "scores": {{
    "layout_match": <1-5>,
    "visual_style_match": <1-5>,
    "typography_match": <1-5>,
    "logo_treatment": <1-5>,
    "overall_quality": <1-5>
  }},
  "overall_score": <1-5 weighted average>,
  "differences": [
    "specific difference from reference 1",
    "specific difference from reference 2"
  ],
  "improvements": [
    "how to better match the reference 1",
    "how to better match the reference 2"
  ],
  "feedback_for_refinement": "A single paragraph describing how to modify the diagram to better match the reference style. Be specific and actionable."
}}
```

Evaluate the generated diagram (second image) against the reference (first image) and respond with ONLY the JSON."""


DESIGN_PRINCIPLES_EVAL_PROMPT = """You are an expert architecture diagram reviewer. Evaluate this diagram against professional design principles and provide structured feedback.

EVALUATION CRITERIA (score each 1-5):

1. **Logo Fidelity** - Are logos used exactly as provided without modification?
   - 5: All logos crisp, unmodified, properly sized
   - 3: Minor logo issues (sizing inconsistencies)
   - 1: Logos modified, blurry, or missing

2. **Layout Clarity** - Is the diagram well-organized with clear visual hierarchy?
   - 5: Clear flow direction, logical grouping, balanced composition
   - 3: Acceptable layout with some crowding or unclear groupings
   - 1: Chaotic layout, no clear flow, overlapping elements

3. **Text Legibility** - Is all text readable and well-formatted?
   - 5: All text crisp, consistent sizing, proper contrast
   - 3: Some text hard to read or inconsistent
   - 1: Text illegible, overlapping, or poorly placed

4. **Visual Design** - Does it follow professional design standards?
   - 5: Clean, professional, presentation-ready
   - 3: Acceptable but needs polish
   - 1: Unprofessional appearance, cluttered

5. **Data Flow** - Are connections and relationships clear?
   - 5: Clear directional arrows, logical flow, well-labeled connections
   - 3: Flow mostly clear but some ambiguity
   - 1: Confusing connections, unclear relationships

RESPONSE FORMAT (use exactly this JSON structure):
```json
{
  "scores": {
    "logo_fidelity": <1-5>,
    "layout_clarity": <1-5>,
    "text_legibility": <1-5>,
    "visual_design": <1-5>,
    "data_flow": <1-5>
  },
  "overall_score": <1-5 weighted average>,
  "issues": [
    "specific issue 1",
    "specific issue 2"
  ],
  "improvements": [
    "specific actionable improvement 1",
    "specific actionable improvement 2"
  ],
  "feedback_for_refinement": "A single paragraph summarizing the most important changes needed to improve this diagram. Be specific and actionable."
}
```

Evaluate the diagram and respond with ONLY the JSON - no other text."""


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

        # Reference image state
        self._reference_style: Optional[str] = None

    def analyze_reference_image(self, reference_path: Path) -> str:
        """Analyze a reference image to extract design patterns.

        Args:
            reference_path: Path to the reference image

        Returns:
            Style description extracted from the reference
        """
        console.print(f"[bold]Analyzing reference image:[/bold] {reference_path}")

        try:
            style_description = self.gemini_client.analyze_image(
                str(reference_path),
                REFERENCE_IMAGE_ANALYSIS_PROMPT,
                temperature=0.2,
            )
            self._reference_style = style_description
            console.print("[green]Reference style extracted successfully[/green]")
            console.print(Panel(style_description[:500] + "..." if len(style_description) > 500 else style_description,
                               title="Reference Style", border_style="cyan"))
            return style_description
        except Exception as e:
            console.print(f"[yellow]Warning: Could not analyze reference image: {e}[/yellow]")
            return ""

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

            console.print(f"\n[bold cyan]═══ Iteration {iteration} ═══[/bold cyan]")
            console.print("[yellow]Generating diagram...[/yellow]")

            # Generate image
            start_time = time.time()
            image_bytes, response_text, metadata = self.gemini_client.generate_image(
                prompt=prompt,
                logo_parts=self._logo_parts,
                temperature=self.conv_config.temperature,
            )
            generation_time = time.time() - start_time

            # Save image and prompt
            output_dir = Path("outputs") / datetime.now().strftime("%Y-%m-%d") / f"chat-{self._session.session_id}"
            output_dir.mkdir(parents=True, exist_ok=True)
            image_path = output_dir / f"iteration_{iteration}.png"
            prompt_path = output_dir / f"iteration_{iteration}_prompt.txt"

            with open(image_path, "wb") as f:
                f.write(image_bytes)
            with open(prompt_path, "w") as f:
                f.write(prompt)

            # Log to MLflow
            self.mlflow_tracker.log_output_image(image_path)
            self.mlflow_tracker.log_metrics({
                "generation_time_seconds": generation_time,
                "iteration": iteration,
            })

            console.print(f"[green]Generated in {generation_time:.1f}s[/green]")
            console.print(f"[bold]Image:[/bold] {image_path}")
            console.print(f"[bold]Prompt:[/bold] {prompt_path}")

            # Create turn
            turn = ConversationTurn(
                iteration=iteration,
                prompt_used=prompt,
                run_id=run_id,
                image_path=image_path,
                generation_time_seconds=generation_time,
            )

            # Auto-analyze if enabled (skip if auto_refine - that does its own evaluation)
            if self.conv_config.auto_analyze and not self.conv_config.auto_refine:
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

            # Don't end MLflow run yet - will be ended after scoring
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

    def auto_evaluate(self, turn: ConversationTurn) -> tuple[int, str]:
        """Automatically evaluate diagram against design principles or reference image.

        Args:
            turn: The turn to evaluate

        Returns:
            Tuple of (score, feedback_text)
        """
        # Use reference comparison if we have a reference style
        if self._reference_style and self.conv_config.reference_image:
            return self._evaluate_against_reference(turn)

        console.print(f"\n[bold cyan]Auto-evaluating against design principles...[/bold cyan]")
        console.print(f"  [dim]{turn.image_path}[/dim]")

        try:
            # Get structured evaluation from Gemini
            eval_response = self.gemini_client.analyze_image(
                str(turn.image_path),
                DESIGN_PRINCIPLES_EVAL_PROMPT,
                temperature=0.2,  # Low temp for consistent evaluation
            )

            # Parse JSON response
            import re
            json_match = re.search(r'\{[\s\S]*\}', eval_response)
            if not json_match:
                raise ValueError("No JSON found in evaluation response")

            eval_data = json.loads(json_match.group())

            # Extract scores
            scores = eval_data.get("scores", {})
            overall_score = int(round(eval_data.get("overall_score", 3)))
            issues = eval_data.get("issues", [])
            improvements = eval_data.get("improvements", [])
            feedback = eval_data.get("feedback_for_refinement", "")

            # Display evaluation results
            score_table = Table(title="Design Principles Evaluation", show_header=True)
            score_table.add_column("Criterion", style="cyan")
            score_table.add_column("Score", style="magenta", justify="center")

            for criterion, score_val in scores.items():
                label = criterion.replace("_", " ").title()
                color = "green" if score_val >= 4 else "yellow" if score_val >= 3 else "red"
                score_table.add_row(label, f"[{color}]{score_val}/5[/{color}]")

            score_table.add_row("", "")
            overall_color = "green" if overall_score >= 4 else "yellow" if overall_score >= 3 else "red"
            score_table.add_row("[bold]Overall[/bold]", f"[bold {overall_color}]{overall_score}/5[/bold {overall_color}]")

            console.print(score_table)

            if issues:
                console.print("\n[bold red]Issues Found:[/bold red]")
                for issue in issues[:5]:  # Limit to top 5
                    console.print(f"  • {issue}")

            if improvements:
                console.print("\n[bold green]Suggested Improvements:[/bold green]")
                for improvement in improvements[:5]:  # Limit to top 5
                    console.print(f"  • {improvement}")

            # Store analysis details
            turn.visual_analysis = json.dumps(eval_data, indent=2)
            turn.score = overall_score
            turn.feedback = feedback

            console.print(f"\n[bold]Feedback for refinement:[/bold]")
            console.print(Panel(feedback, border_style="yellow"))

            return overall_score, feedback

        except Exception as e:
            console.print(f"[yellow]Auto-evaluation failed: {e}[/yellow]")
            console.print("[yellow]Falling back to manual feedback...[/yellow]")
            return self.collect_feedback(turn)

    def _evaluate_against_reference(self, turn: ConversationTurn) -> tuple[int, str]:
        """Evaluate diagram by comparing against reference image.

        Args:
            turn: The turn to evaluate

        Returns:
            Tuple of (score, feedback_text)
        """
        console.print(f"\n[bold cyan]Comparing against reference image...[/bold cyan]")
        console.print(f"  [dim]Generated: {turn.image_path}[/dim]")
        console.print(f"  [dim]Reference: {self.conv_config.reference_image}[/dim]")

        try:
            # Build the comparison prompt with the extracted style
            comparison_prompt = REFERENCE_COMPARISON_PROMPT.format(
                reference_style=self._reference_style
            )

            # Compare images (reference first, generated second)
            eval_response = self.gemini_client.analyze_images(
                [str(self.conv_config.reference_image), str(turn.image_path)],
                comparison_prompt,
                temperature=0.2,
            )

            # Parse JSON response
            import re
            json_match = re.search(r'\{[\s\S]*\}', eval_response)
            if not json_match:
                raise ValueError("No JSON found in evaluation response")

            eval_data = json.loads(json_match.group())

            # Extract scores
            scores = eval_data.get("scores", {})
            overall_score = int(round(eval_data.get("overall_score", 3)))
            differences = eval_data.get("differences", [])
            improvements = eval_data.get("improvements", [])
            feedback = eval_data.get("feedback_for_refinement", "")

            # Display evaluation results
            score_table = Table(title="Reference Comparison", show_header=True)
            score_table.add_column("Criterion", style="cyan")
            score_table.add_column("Score", style="magenta", justify="center")

            for criterion, score_val in scores.items():
                label = criterion.replace("_", " ").title()
                color = "green" if score_val >= 4 else "yellow" if score_val >= 3 else "red"
                score_table.add_row(label, f"[{color}]{score_val}/5[/{color}]")

            score_table.add_row("", "")
            overall_color = "green" if overall_score >= 4 else "yellow" if overall_score >= 3 else "red"
            score_table.add_row("[bold]Overall[/bold]", f"[bold {overall_color}]{overall_score}/5[/bold {overall_color}]")

            console.print(score_table)

            if differences:
                console.print("\n[bold red]Differences from Reference:[/bold red]")
                for diff in differences[:5]:
                    console.print(f"  • {diff}")

            if improvements:
                console.print("\n[bold green]How to Match Reference:[/bold green]")
                for improvement in improvements[:5]:
                    console.print(f"  • {improvement}")

            # Store analysis details
            turn.visual_analysis = json.dumps(eval_data, indent=2)
            turn.score = overall_score
            turn.feedback = feedback

            console.print(f"\n[bold]Feedback for refinement:[/bold]")
            console.print(Panel(feedback, border_style="yellow"))

            return overall_score, feedback

        except Exception as e:
            console.print(f"[yellow]Reference comparison failed: {e}[/yellow]")
            console.print("[yellow]Falling back to design principles evaluation...[/yellow]")
            # Fall back to standard evaluation
            self._reference_style = None
            return self.auto_evaluate(turn)

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
        mode = "Auto-refine" if self.conv_config.auto_refine else "Interactive"

        console.print(Panel(
            f"Starting conversation refinement loop\n"
            f"Mode: [bold]{mode}[/bold]\n"
            f"Target score: {self.conv_config.target_score}\n"
            f"Max iterations: {self.conv_config.max_iterations}\n"
            + ("" if self.conv_config.auto_refine else "Type 'done' or score target to finish"),
            title="Conversation Session",
            border_style="cyan",
        ))

        while len(self._session.turns) < self.conv_config.max_iterations:
            # Generate
            turn = self.run_iteration(current_prompt)

            # Collect feedback (auto or manual)
            if self.conv_config.auto_refine:
                score, feedback = self.auto_evaluate(turn)
            else:
                score, feedback = self.collect_feedback(turn)

            # Log score to MLflow and end the run
            try:
                self.mlflow_tracker.log_metrics({"score": score})
                if turn.feedback:
                    self.mlflow_tracker.log_prompt(turn.feedback, "feedback.txt")
                self.mlflow_tracker.end_run("FINISHED")
            except Exception:
                pass  # Run may already be ended

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
