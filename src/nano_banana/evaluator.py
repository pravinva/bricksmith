"""Manual evaluation interface for Nano Banana Pro."""

import json
import subprocess
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt, Prompt

from .mlflow_tracker import MLflowTracker
from .models import EvaluationScores


console = Console()


class Evaluator:
    """Manual evaluation interface with rubric-based scoring."""

    def __init__(self, mlflow_tracker: MLflowTracker):
        """Initialize evaluator.

        Args:
            mlflow_tracker: MLflow tracker instance
        """
        self.mlflow_tracker = mlflow_tracker

    def evaluate_run(
        self,
        run_id: str,
        interactive: bool = True,
        eval_file: Optional[Path] = None,
    ) -> EvaluationScores:
        """Evaluate a specific run.

        Args:
            run_id: MLflow run ID to evaluate
            interactive: If True, prompt user for scores
            eval_file: Optional path to pre-written evaluation JSON

        Returns:
            EvaluationScores object

        Raises:
            FileNotFoundError: If eval_file specified but doesn't exist
        """
        # Get run info
        try:
            run_info = self.mlflow_tracker.get_run_info(run_id)
        except Exception as e:
            raise ValueError(f"Failed to get run info: {e}")

        console.print(f"\n[bold]Evaluating Run: {run_id}[/bold]")
        console.print(f"Run Name: {run_info.get('run_name', 'N/A')}")
        console.print(f"Status: {run_info['status']}")

        # Get output image path
        artifact_uri = run_info["artifact_uri"]
        image_path = Path(artifact_uri.replace("file://", "")) / "outputs"

        # Find the image file
        image_files = []
        if image_path.exists():
            image_files = list(image_path.glob("*.png")) + list(image_path.glob("*.jpg"))

        if image_files:
            console.print(f"\n[bold green]Generated Image:[/bold green] {image_files[0]}")
            self.display_image(image_files[0])
        else:
            console.print("\n[yellow]Warning: No output image found[/yellow]")

        # Get scores
        if eval_file:
            scores = self.load_evaluation_from_file(eval_file)
        elif interactive:
            scores = self.interactive_evaluation(image_files[0] if image_files else None)
        else:
            raise ValueError("Must specify either interactive=True or provide eval_file")

        # Log evaluation to MLflow
        self.mlflow_tracker.log_evaluation(scores)
        console.print("\n[bold green]✓ Evaluation logged to MLflow[/bold green]")

        return scores

    def interactive_evaluation(self, image_path: Optional[Path] = None) -> EvaluationScores:
        """Interactive CLI evaluation with score prompts.

        Args:
            image_path: Optional path to image being evaluated

        Returns:
            EvaluationScores object
        """
        console.print("\n" + "=" * 70)
        console.print("[bold]EVALUATION RUBRIC[/bold]")
        console.print("=" * 70)
        self.display_rubric()

        console.print("\n[bold]Please provide scores (0-5) for each dimension:[/bold]\n")

        # Prompt for each score
        logo_fidelity = IntPrompt.ask(
            "Logo Fidelity Score (0-5)",
            default=3,
            show_default=True,
        )
        if logo_fidelity < 0 or logo_fidelity > 5:
            console.print("[red]Score must be between 0 and 5. Using 3.[/red]")
            logo_fidelity = 3

        layout_clarity = IntPrompt.ask(
            "Layout Clarity Score (0-5)",
            default=3,
            show_default=True,
        )
        if layout_clarity < 0 or layout_clarity > 5:
            console.print("[red]Score must be between 0 and 5. Using 3.[/red]")
            layout_clarity = 3

        text_legibility = IntPrompt.ask(
            "Text Legibility Score (0-5)",
            default=3,
            show_default=True,
        )
        if text_legibility < 0 or text_legibility > 5:
            console.print("[red]Score must be between 0 and 5. Using 3.[/red]")
            text_legibility = 3

        constraint_compliance = IntPrompt.ask(
            "Constraint Compliance Score (0-5)",
            default=3,
            show_default=True,
        )
        if constraint_compliance < 0 or constraint_compliance > 5:
            console.print("[red]Score must be between 0 and 5. Using 3.[/red]")
            constraint_compliance = 3

        notes = Prompt.ask(
            "\nEvaluation Notes (optional)",
            default="",
        )

        scores = EvaluationScores(
            logo_fidelity_score=logo_fidelity,
            layout_clarity_score=layout_clarity,
            text_legibility_score=text_legibility,
            constraint_compliance_score=constraint_compliance,
            notes=notes,
        )

        # Display summary
        console.print("\n[bold]Evaluation Summary:[/bold]")
        console.print(f"  Logo Fidelity: {scores.logo_fidelity_score}/5")
        console.print(f"  Layout Clarity: {scores.layout_clarity_score}/5")
        console.print(f"  Text Legibility: {scores.text_legibility_score}/5")
        console.print(f"  Constraint Compliance: {scores.constraint_compliance_score}/5")
        console.print(f"  [bold]Overall Score: {scores.overall_score:.2f}/5[/bold]")

        if scores.notes:
            console.print(f"\n  Notes: {scores.notes}")

        return scores

    def load_evaluation_from_file(self, eval_file: Path) -> EvaluationScores:
        """Load pre-written evaluation from JSON file.

        Args:
            eval_file: Path to JSON evaluation file

        Returns:
            EvaluationScores object

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If JSON is invalid
        """
        if not eval_file.exists():
            raise FileNotFoundError(f"Evaluation file not found: {eval_file}")

        with open(eval_file, "r") as f:
            data = json.load(f)

        return EvaluationScores(**data)

    def display_rubric(self) -> None:
        """Display evaluation rubric as formatted table."""
        table = Table(title="Evaluation Criteria", show_header=True, header_style="bold magenta")
        table.add_column("Dimension", style="cyan", width=20)
        table.add_column("Score", style="yellow", width=8)
        table.add_column("Description", style="white")

        # Logo Fidelity
        table.add_row(
            "Logo Fidelity",
            "5",
            "All logos reused exactly, perfect scaling, no alterations",
        )
        table.add_row("", "3", "Minor logo alterations or scaling issues")
        table.add_row("", "1", "Logos significantly altered or incorrectly used")
        table.add_row("", "0", "Logos not used, completely wrong, or filenames visible")

        # Layout Clarity
        table.add_row(
            "Layout Clarity",
            "5",
            "Crystal clear flow, excellent spacing, easy to understand",
        )
        table.add_row("", "3", "Adequate layout with minor spacing or flow issues")
        table.add_row("", "1", "Confusing layout, poor spacing")
        table.add_row("", "0", "Completely unclear or unusable layout")

        # Text Legibility
        table.add_row(
            "Text Legibility",
            "5",
            "All text clear, properly sized, and well-formatted",
        )
        table.add_row("", "3", "Most text readable with minor formatting issues")
        table.add_row("", "1", "Significant readability issues")
        table.add_row("", "0", "Text unreadable or missing")

        # Constraint Compliance
        table.add_row(
            "Constraint Compliance",
            "5",
            "All constraints followed perfectly",
        )
        table.add_row("", "3", "Most constraints followed with minor deviations")
        table.add_row("", "1", "Several constraint violations")
        table.add_row("", "0", "Major constraint violations or requirements ignored")

        console.print(table)

        # Critical notes
        console.print("\n[bold red]CRITICAL REQUIREMENTS:[/bold red]")
        console.print("  • NO filenames may appear in output (automatic -2 penalty)")
        console.print("  • Logos must be reused EXACTLY as provided")
        console.print("  • All logos must be scaled uniformly")

    def display_image(self, image_path: Path) -> None:
        """Display image path and attempt to open.

        Args:
            image_path: Path to image file
        """
        console.print(f"\n[bold]Image Location:[/bold] {image_path}")

        # Try to open image with default viewer
        try:
            if image_path.exists():
                # macOS
                subprocess.run(["open", str(image_path)], check=False)
                console.print("[green]Attempting to open image in default viewer...[/green]")
        except Exception:
            console.print("[yellow]Could not automatically open image. Please view manually.[/yellow]")
