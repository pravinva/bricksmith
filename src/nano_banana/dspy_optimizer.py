"""DSPy-inspired prompt optimizer for image generation.

This is NOT traditional DSPy (which works on text→text tasks).
Instead, it uses DSPy principles adapted for text→image:
- Systematic prompt variation
- Human-in-the-loop evaluation
- Iterative refinement
- MLflow tracking
"""

import json
from pathlib import Path
from typing import Any, Optional
import dspy
import mlflow

from .models import DiagramSpec


class ImagePromptSignature(dspy.Signature):
    """Signature for image generation prompt refinement."""

    # Inputs
    diagram_spec = dspy.InputField(desc="Diagram specification with components and layout")
    technical_context = dspy.InputField(desc="Technical context from Databricks docs")
    previous_prompt = dspy.InputField(desc="Previous prompt version (if any)")
    feedback = dspy.InputField(desc="Feedback on previous generation (if any)")

    # Output
    refined_prompt = dspy.OutputField(
        desc="Refined prompt for image generation that incorporates feedback "
        "and improves technical accuracy, visual clarity, and logo prominence"
    )


class ImagePromptRefiner(dspy.Module):
    """Refines image generation prompts based on feedback."""

    def __init__(self):
        super().__init__()
        self.refine = dspy.ChainOfThought(ImagePromptSignature)

    def forward(
        self,
        diagram_spec: str,
        technical_context: str,
        previous_prompt: str = "",
        feedback: str = "",
    ):
        """Refine prompt based on inputs and feedback."""
        return self.refine(
            diagram_spec=diagram_spec,
            technical_context=technical_context,
            previous_prompt=previous_prompt or "No previous version",
            feedback=feedback or "No feedback yet - this is the first iteration",
        )


class HumanEvaluator:
    """Human-in-the-loop evaluation for image quality."""

    @staticmethod
    def evaluate_image(image_path: Path) -> dict[str, Any]:
        """Prompt human to evaluate generated image.

        Args:
            image_path: Path to generated image

        Returns:
            Evaluation scores and feedback
        """
        from rich.console import Console
        from rich.prompt import Prompt, IntPrompt
        from rich.panel import Panel

        console = Console()

        console.print(f"\n[bold cyan]Evaluate Image: {image_path.name}[/bold cyan]")
        console.print(f"[dim]Open the image to review: {image_path}[/dim]\n")

        # Score different aspects
        scores = {}

        console.print("[bold]Rate each aspect (1-5, where 5 is excellent):[/bold]\n")

        scores["logo_visibility"] = IntPrompt.ask(
            "  Logo Visibility (all logos present & clear)", default=3
        )
        scores["technical_accuracy"] = IntPrompt.ask(
            "  Technical Accuracy (correct terms, layout)", default=3
        )
        scores["visual_quality"] = IntPrompt.ask(
            "  Visual Quality (colors, polish, readability)", default=3
        )
        scores["layout_clarity"] = IntPrompt.ask(
            "  Layout Clarity (easy to understand flow)", default=3
        )
        scores["presentation_ready"] = IntPrompt.ask(
            "  Presentation Ready (suitable for exec presentation)", default=3
        )

        # Overall
        scores["overall"] = sum(scores.values()) / len(scores)

        # Feedback
        console.print("\n[bold]Provide specific feedback:[/bold]")
        feedback = Prompt.ask(
            "  What needs improvement?",
            default="Good overall",
        )

        return {
            "scores": scores,
            "feedback": feedback,
            "would_use_in_production": scores["overall"] >= 4.0,
        }


class DSPyPromptOptimizer:
    """Optimizer for image generation prompts using DSPy + human feedback."""

    def __init__(
        self,
        lm_model: str = "databricks-meta-llama-3-1-70b-instruct",
        experiment_name: str = "nano-banana-dspy-optimization",
    ):
        """Initialize optimizer.

        Args:
            lm_model: LLM model for prompt refinement
            experiment_name: MLflow experiment name
        """
        # Configure DSPy with Databricks
        self.lm = dspy.Databricks(
            model=lm_model,
            max_tokens=3000,
            temperature=0.3,  # Moderate creativity for refinement
        )
        dspy.settings.configure(lm=self.lm)

        # Initialize refiner
        self.refiner = ImagePromptRefiner()

        # MLflow setup
        mlflow.set_tracking_uri("./mlruns")
        mlflow.set_experiment(experiment_name)

        # Track optimization history
        self.history: list[dict[str, Any]] = []

    def optimize_prompt(
        self,
        initial_prompt: str,
        diagram_spec: DiagramSpec,
        technical_context: str,
        max_iterations: int = 3,
        target_score: float = 4.5,
    ) -> tuple[str, list[dict[str, Any]]]:
        """Optimize prompt through iterative refinement.

        Args:
            initial_prompt: Starting prompt
            diagram_spec: Diagram specification
            technical_context: Technical context from docs
            max_iterations: Maximum refinement iterations
            target_score: Stop when overall score reaches this

        Returns:
            Tuple of (best_prompt, optimization_history)
        """
        from rich.console import Console

        console = Console()

        console.print("\n[bold cyan]Starting DSPy Prompt Optimization[/bold cyan]")
        console.print(f"Target score: {target_score}/5.0")
        console.print(f"Max iterations: {max_iterations}\n")

        current_prompt = initial_prompt
        best_prompt = initial_prompt
        best_score = 0.0

        # Convert diagram spec to string
        spec_str = json.dumps(
            {
                "name": diagram_spec.name,
                "description": diagram_spec.description,
                "components": [
                    {"id": c.id, "label": c.label, "type": c.type}
                    for c in diagram_spec.components
                ],
            },
            indent=2,
        )

        for iteration in range(max_iterations):
            console.print(f"[bold]Iteration {iteration + 1}/{max_iterations}[/bold]")

            with mlflow.start_run(run_name=f"optimization_iter_{iteration + 1}"):
                # Get feedback from previous iteration
                feedback = ""
                if iteration > 0:
                    prev_eval = self.history[-1]["evaluation"]
                    feedback = (
                        f"Previous score: {prev_eval['scores']['overall']:.1f}/5.0. "
                        f"Feedback: {prev_eval['feedback']}"
                    )

                # Refine prompt
                console.print("  [yellow]Refining prompt with DSPy...[/yellow]")

                refinement = self.refiner(
                    diagram_spec=spec_str,
                    technical_context=technical_context,
                    previous_prompt=current_prompt if iteration > 0 else "",
                    feedback=feedback,
                )

                refined_prompt = refinement.refined_prompt

                # Log to MLflow
                mlflow.log_param("iteration", iteration + 1)
                mlflow.log_param("prompt_length", len(refined_prompt))
                mlflow.log_text(refined_prompt, f"prompt_iter_{iteration + 1}.txt")

                console.print(f"  [green]✓ Refined prompt ({len(refined_prompt)} chars)[/green]")

                # At this point, you would:
                # 1. Generate image with refined prompt
                # 2. Have human evaluate it
                # For now, we'll simulate or prompt for manual evaluation

                console.print("\n  [yellow]→ Generate image with this prompt[/yellow]")
                console.print("  [yellow]→ Then evaluate the result[/yellow]\n")

                # Simulated evaluation (replace with actual generation + evaluation)
                evaluation = self._get_evaluation_placeholder(iteration)

                # Log evaluation
                mlflow.log_metrics(evaluation["scores"])
                mlflow.log_text(evaluation["feedback"], f"feedback_iter_{iteration + 1}.txt")

                # Track history
                self.history.append(
                    {
                        "iteration": iteration + 1,
                        "prompt": refined_prompt,
                        "evaluation": evaluation,
                    }
                )

                # Update best
                if evaluation["scores"]["overall"] > best_score:
                    best_score = evaluation["scores"]["overall"]
                    best_prompt = refined_prompt

                console.print(
                    f"  [cyan]Score: {evaluation['scores']['overall']:.1f}/5.0[/cyan]"
                )

                # Check if target reached
                if evaluation["scores"]["overall"] >= target_score:
                    console.print(f"\n[bold green]✓ Target score reached![/bold green]")
                    break

                current_prompt = refined_prompt

        console.print(f"\n[bold green]Optimization complete![/bold green]")
        console.print(f"Best score: {best_score:.1f}/5.0")
        console.print(f"Iterations: {len(self.history)}")

        return best_prompt, self.history

    def _get_evaluation_placeholder(self, iteration: int) -> dict[str, Any]:
        """Placeholder evaluation - replace with actual image generation + human eval."""
        # This would be replaced with:
        # 1. Generate image with refined prompt
        # 2. Call HumanEvaluator.evaluate_image()
        # 3. Return actual scores

        # Simulated improving scores
        base_score = 3.0 + (iteration * 0.5)
        return {
            "scores": {
                "logo_visibility": min(5.0, base_score),
                "technical_accuracy": min(5.0, base_score + 0.2),
                "visual_quality": min(5.0, base_score - 0.1),
                "layout_clarity": min(5.0, base_score + 0.1),
                "presentation_ready": min(5.0, base_score),
                "overall": min(5.0, base_score),
            },
            "feedback": f"Iteration {iteration + 1}: Making progress",
            "would_use_in_production": base_score >= 4.0,
        }
