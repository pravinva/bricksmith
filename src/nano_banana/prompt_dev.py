"""Prompt development and iteration framework.

Tools for systematically developing and refining diagram generation prompts.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import mlflow
import mlflow.gemini
from rich.console import Console
from rich.table import Table

from .config import LogoKitConfig
from .gemini_client import GeminiClient
from .logos import LogoKitHandler
from .mcp_enricher import MCPEnricher
from .models import DiagramSpec
from .prompts import PromptBuilder

console = Console()


class PromptExperiment:
    """Represents a single prompt experiment."""

    def __init__(
        self,
        template_id: str,
        variant_name: str,
        use_mcp_enrichment: bool = False,
        modifications: Optional[dict[str, Any]] = None,
    ):
        """Initialize experiment.

        Args:
            template_id: Base template ID
            variant_name: Descriptive name for this variant
            use_mcp_enrichment: Whether to use MCP enrichment
            modifications: Optional modifications to apply
        """
        self.template_id = template_id
        self.variant_name = variant_name
        self.use_mcp_enrichment = use_mcp_enrichment
        self.modifications = modifications or {}
        self.run_id: Optional[str] = None
        self.output_path: Optional[Path] = None
        self.metrics: dict[str, float] = {}


class PromptDevelopmentLab:
    """Laboratory for developing and testing prompt variants."""

    def __init__(
        self,
        experiment_name: str = "nano-banana-prompt-development",
        output_dir: Path = Path("outputs/prompt_dev"),
    ):
        """Initialize prompt development lab.

        Args:
            experiment_name: MLflow experiment name
            output_dir: Directory for outputs
        """
        self.experiment_name = experiment_name
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.client = GeminiClient()
        self.logo_handler = LogoKitHandler(
            LogoKitConfig(
                logo_dir=Path("logos/default"),
                max_logo_size_mb=5.0,
                allowed_extensions=[".jpg", ".jpeg", ".png"],
            )
        )
        self.prompt_builder = PromptBuilder()
        self.mcp_enricher = MCPEnricher()

        # Initialize MLflow
        mlflow.set_tracking_uri("./mlruns")
        mlflow.set_experiment(self.experiment_name)

    def run_experiment(
        self,
        diagram_spec_path: Path,
        experiment: PromptExperiment,
        aspect_ratio: str = "16:9",
        image_size: str = "2K",
    ) -> PromptExperiment:
        """Run a single prompt experiment.

        Args:
            diagram_spec_path: Path to diagram spec
            experiment: Experiment configuration
            aspect_ratio: Image aspect ratio
            image_size: Image size

        Returns:
            Updated experiment with results
        """
        console.print(
            f"\n[bold cyan]Running experiment: {experiment.variant_name}[/bold cyan]"
        )

        try:
            with mlflow.start_run(run_name=experiment.variant_name) as run:
                experiment.run_id = run.info.run_id

                # Enable autologging
                mlflow.gemini.autolog(log_traces=True, silent=True)

                # Load components
                logo_kit = self.logo_handler.load_logo_kit()
                spec = DiagramSpec.from_yaml(diagram_spec_path)

                # Build prompt
                template = self.prompt_builder.load_template(experiment.template_id)
                prompt = self.prompt_builder.build_prompt(template, spec, logo_kit)

                # Optionally enrich with MCP
                if experiment.use_mcp_enrichment:
                    console.print("  [yellow]Enriching with Databricks docs...[/yellow]")
                    enriched_context = self.mcp_enricher.enrich_diagram_spec(spec)
                    if enriched_context:
                        context_section = (
                            self.mcp_enricher.build_enriched_prompt_section(
                                enriched_context
                            )
                        )
                        prompt = f"{prompt}\n\n{context_section}"
                        console.print(
                            f"  [green]✓ Added context for {len(enriched_context)} components[/green]"
                        )

                # Log parameters
                mlflow.log_params(
                    {
                        "template_id": experiment.template_id,
                        "variant_name": experiment.variant_name,
                        "use_mcp_enrichment": experiment.use_mcp_enrichment,
                        "aspect_ratio": aspect_ratio,
                        "image_size": image_size,
                        "prompt_length": len(prompt),
                        "logo_count": len(logo_kit),
                    }
                )

                # Convert logos
                logo_parts = [
                    self.logo_handler.to_image_part(logo) for logo in logo_kit
                ]

                # Generate
                console.print("  [yellow]Generating diagram...[/yellow]")
                start_time = time.time()

                image_bytes, response_text, metadata = self.client.generate_image(
                    prompt=prompt,
                    logo_parts=logo_parts,
                    aspect_ratio=aspect_ratio,
                    image_size=image_size,
                )

                generation_time = time.time() - start_time

                # Save output
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{experiment.variant_name}_{timestamp}.png"
                output_path = self.output_dir / filename

                with open(output_path, "wb") as f:
                    f.write(image_bytes)

                experiment.output_path = output_path

                # Log metrics
                experiment.metrics = {
                    "generation_time_seconds": generation_time,
                    "image_size_bytes": len(image_bytes),
                    "prompt_length": len(prompt),
                }
                mlflow.log_metrics(experiment.metrics)

                # Log artifacts
                mlflow.log_artifact(str(output_path), artifact_path="outputs")

                # Save prompt
                prompt_path = self.output_dir / f"{experiment.variant_name}_prompt.txt"
                prompt_path.write_text(prompt)
                mlflow.log_artifact(str(prompt_path), artifact_path="prompts")

                console.print(
                    f"  [green]✓ Generated in {generation_time:.1f}s[/green]"
                )
                console.print(f"  [green]✓ Saved to {output_path.name}[/green]")

        except Exception as e:
            console.print(f"  [red]✗ Failed: {e}[/red]")

        return experiment

    def run_comparison(
        self,
        diagram_spec_path: Path,
        experiments: list[PromptExperiment],
        aspect_ratio: str = "16:9",
        image_size: str = "2K",
    ) -> list[PromptExperiment]:
        """Run multiple experiments for comparison.

        Args:
            diagram_spec_path: Path to diagram spec
            experiments: List of experiments to run
            aspect_ratio: Image aspect ratio
            image_size: Image size

        Returns:
            List of completed experiments with results
        """
        console.print(
            f"\n[bold]Running {len(experiments)} prompt experiments[/bold]\n"
        )

        results = []
        for exp in experiments:
            result = self.run_experiment(
                diagram_spec_path, exp, aspect_ratio, image_size
            )
            results.append(result)
            time.sleep(1)  # Brief pause between experiments

        # Display comparison table
        self._display_comparison(results)

        return results

    def _display_comparison(self, experiments: list[PromptExperiment]) -> None:
        """Display comparison table of experiments.

        Args:
            experiments: List of completed experiments
        """
        console.print("\n[bold]Experiment Comparison[/bold]\n")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Variant")
        table.add_column("Template")
        table.add_column("MCP Enriched")
        table.add_column("Gen Time (s)")
        table.add_column("Image Size (MB)")
        table.add_column("Output")

        for exp in experiments:
            if exp.metrics:
                table.add_row(
                    exp.variant_name,
                    exp.template_id,
                    "✓" if exp.use_mcp_enrichment else "✗",
                    f"{exp.metrics.get('generation_time_seconds', 0):.1f}",
                    f"{exp.metrics.get('image_size_bytes', 0) / 1024 / 1024:.2f}",
                    exp.output_path.name if exp.output_path else "N/A",
                )

        console.print(table)

        console.print("\n[bold]Next Steps:[/bold]")
        console.print("1. Review generated diagrams in outputs/prompt_dev/")
        console.print("2. Compare quality and accuracy")
        console.print("3. Select best variant or iterate further")
        console.print("4. View detailed traces: mlflow ui --port 5000")
