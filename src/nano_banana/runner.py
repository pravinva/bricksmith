"""Workflow orchestration for Nano Banana Pro."""

import time
from pathlib import Path
from typing import Optional

import mlflow.gemini
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import AppConfig
from .gemini_client import GeminiClient
from .logos import LogoKitHandler
from .mlflow_tracker import MLflowTracker
from .models import DiagramSpec, GenerationResult
from .prompts import PromptBuilder


console = Console()


class DiagramRunner:
    """Orchestrates the complete diagram generation workflow."""

    def __init__(
        self,
        config: AppConfig,
        logo_handler: LogoKitHandler,
        prompt_builder: PromptBuilder,
        gemini_client: GeminiClient,
        mlflow_tracker: MLflowTracker,
    ):
        """Initialize diagram runner.

        Args:
            config: Application configuration
            logo_handler: Logo kit handler
            prompt_builder: Prompt builder
            gemini_client: Google AI (Gemini) client
            mlflow_tracker: MLflow tracker
        """
        self.config = config
        self.logo_handler = logo_handler
        self.prompt_builder = prompt_builder
        self.gemini_client = gemini_client
        self.mlflow_tracker = mlflow_tracker

        # Create outputs directory
        self.outputs_dir = Path("outputs")
        self.outputs_dir.mkdir(exist_ok=True)

    def run_experiment(
        self,
        diagram_spec: DiagramSpec,
        prompt_template_id: str,
        run_name: Optional[str] = None,
        tags: Optional[dict[str, str]] = None,
    ) -> GenerationResult:
        """Run a complete diagram generation experiment.

        This orchestrates the full workflow:
        1. Start MLflow run
        2. Load logo kit
        3. Build prompt
        4. Generate image via Vertex AI
        5. Log everything to MLflow
        6. Return results

        Args:
            diagram_spec: Diagram specification
            prompt_template_id: Prompt template identifier
            run_name: Optional run name
            tags: Optional tags dictionary

        Returns:
            GenerationResult object
        """
        start_time = time.time()
        run_id = None

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                # Step 1: Start MLflow run
                task = progress.add_task("Starting MLflow run...", total=None)
                run_id = self.mlflow_tracker.start_run(run_name, tags)
                progress.update(task, description=f"[green]✓ Started run: {run_id[:8]}")

                # Enable Gemini autologging for automatic tracing
                mlflow.gemini.autolog(log_traces=True, silent=True)

                # Step 2: Load logo kit
                task = progress.add_task("Loading logo kit...", total=None)
                logo_kit = self.logo_handler.load_logo_kit()
                progress.update(
                    task, description=f"[green]✓ Loaded {len(logo_kit)} logos"
                )

                # Step 3: Load template and build prompt
                task = progress.add_task("Building prompt...", total=None)
                template = self.prompt_builder.load_template(prompt_template_id)
                prompt = self.prompt_builder.build_prompt(
                    template, diagram_spec, logo_kit
                )
                progress.update(
                    task, description=f"[green]✓ Built prompt ({len(prompt)} chars)"
                )

                # Step 4: Convert logos to image parts
                task = progress.add_task("Converting logos...", total=None)
                logo_parts = [
                    self.logo_handler.to_image_part(logo) for logo in logo_kit
                ]
                progress.update(
                    task, description=f"[green]✓ Converted {len(logo_parts)} logos"
                )

                # Step 5: Log parameters to MLflow
                task = progress.add_task("Logging parameters...", total=None)
                model_info = self.gemini_client.get_model_info()
                parameters = {
                    "model": model_info["model"],
                    "temperature": 0.8,  # Optimized for architecture diagrams with good logo inclusion
                    "top_p": 0.95,
                    "top_k": 50,  # Higher value helps with logo inclusion
                    "presence_penalty": 0.1,
                    "frequency_penalty": 0.1,
                    "max_output_tokens": 32768,
                    "aspect_ratio": "16:9",  # Presentation format
                    "image_size": "2K",  # Higher quality
                    "prompt_template_id": prompt_template_id,
                    "diagram_spec_id": diagram_spec.name,
                }
                self.mlflow_tracker.log_parameters(parameters)

                # Log logo hashes
                logo_hashes = {logo.name: logo.sha256_hash for logo in logo_kit}
                self.mlflow_tracker.log_parameters({"logo_hashes": logo_hashes})

                progress.update(task, description="[green]✓ Logged parameters")

                # Step 6: Log artifacts
                task = progress.add_task("Logging artifacts...", total=None)
                self.mlflow_tracker.log_prompt(prompt)
                self.mlflow_tracker.log_diagram_spec(diagram_spec)
                self.mlflow_tracker.log_generation_config(model_info)
                progress.update(task, description="[green]✓ Logged artifacts")

                # Step 7: Generate image via Google AI (Gemini)
                task = progress.add_task("Generating image...", total=None)
                image_bytes, response_text, metadata = self.gemini_client.generate_image(
                    prompt=prompt,
                    logo_parts=logo_parts,
                    temperature=parameters["temperature"],
                    top_p=parameters["top_p"],
                    top_k=parameters["top_k"],
                    presence_penalty=parameters["presence_penalty"],
                    frequency_penalty=parameters["frequency_penalty"],
                    max_output_tokens=parameters["max_output_tokens"],
                    aspect_ratio=parameters["aspect_ratio"],
                    image_size=parameters["image_size"],
                )
                progress.update(task, description="[green]✓ Generated image")

                # Step 8: Save output
                task = progress.add_task("Saving output...", total=None)
                output_path = self._save_output(run_id, image_bytes, run_name)
                self.mlflow_tracker.log_output_image(output_path)
                progress.update(
                    task, description=f"[green]✓ Saved to {output_path.name}"
                )

                # Step 9: Log generation time
                generation_time = time.time() - start_time
                self.mlflow_tracker.log_metrics(
                    {"generation_time_seconds": generation_time}
                )

                # Step 10: End run successfully
                self.mlflow_tracker.end_run(status="FINISHED")

                console.print(f"\n[bold green]✓ Generation completed successfully![/bold green]")
                console.print(f"  Run ID: {run_id}")
                console.print(f"  Output: {output_path}")
                console.print(f"  Time: {generation_time:.2f}s")

                return GenerationResult(
                    run_id=run_id,
                    output_path=output_path,
                    prompt_text=prompt,
                    parameters=parameters,
                    generation_time_seconds=generation_time,
                    success=True,
                )

        except Exception as e:
            # Log error and end run with FAILED status
            error_msg = str(e)
            console.print(f"\n[bold red]✗ Generation failed: {error_msg}[/bold red]")

            if run_id:
                try:
                    self.mlflow_tracker.end_run(status="FAILED")
                except:
                    pass

            generation_time = time.time() - start_time

            return GenerationResult(
                run_id=run_id or "unknown",
                output_path=Path(""),
                prompt_text="",
                parameters={},
                generation_time_seconds=generation_time,
                success=False,
                error_message=error_msg,
            )

    def _save_output(self, run_id: str, image_bytes: bytes, run_name: Optional[str] = None) -> Path:
        """Save output image to disk in organized date-based folders.

        Args:
            run_id: MLflow run ID
            image_bytes: Image data
            run_name: Optional run name for folder organization

        Returns:
            Path to saved image
        """
        from datetime import datetime

        # Create date-based output folder: outputs/YYYY-MM-DD/{run_name}/
        now = datetime.now()
        date_folder = now.strftime("%Y-%m-%d")
        time_stamp = now.strftime("%H%M%S")

        # Use run_name or fallback to run_id for folder name
        folder_name = run_name or f"run-{run_id[:8]}"
        run_dir = self.outputs_dir / date_folder / folder_name
        run_dir.mkdir(parents=True, exist_ok=True)

        # Create filename with timestamp
        output_filename = f"diagram_{time_stamp}.png"
        output_path = run_dir / output_filename

        # Write image bytes
        with open(output_path, "wb") as f:
            f.write(image_bytes)

        return output_path

    def verify_setup(self) -> bool:
        """Verify that all components are properly configured.

        Returns:
            True if setup is valid, False otherwise
        """
        console.print("[bold]Verifying setup...[/bold]\n")

        all_good = True

        # Check Vertex AI auth
        console.print("Checking Vertex AI authentication...", end=" ")
        try:
            if self.vertex_client.verify_auth():
                console.print("[green]✓[/green]")
            else:
                console.print("[red]✗ Not authenticated[/red]")
                all_good = False
        except Exception as e:
            console.print(f"[red]✗ {e}[/red]")
            all_good = False

        # Check MLflow
        console.print("Checking MLflow configuration...", end=" ")
        try:
            self.mlflow_tracker.initialize()
            console.print("[green]✓[/green]")
        except Exception as e:
            console.print(f"[red]✗ {e}[/red]")
            all_good = False

        # Check logo directory
        console.print("Checking logo directory...", end=" ")
        if self.config.logo_kit.logo_dir.exists():
            logo_count = len(
                [
                    f
                    for f in self.config.logo_kit.logo_dir.iterdir()
                    if f.suffix.lower() in self.config.logo_kit.allowed_extensions
                ]
            )
            console.print(f"[green]✓ ({logo_count} logos)[/green]")
        else:
            console.print(f"[red]✗ Not found: {self.config.logo_kit.logo_dir}[/red]")
            all_good = False

        # Check template directory
        console.print("Checking template directory...", end=" ")
        template_dir = self.prompt_builder.template_dir
        if template_dir.exists():
            template_count = len(list(template_dir.glob("*.txt")))
            console.print(f"[green]✓ ({template_count} templates)[/green]")
        else:
            console.print(f"[red]✗ Not found: {template_dir}[/red]")
            all_good = False

        console.print()
        if all_good:
            console.print("[bold green]✓ All checks passed![/bold green]")
        else:
            console.print("[bold red]✗ Setup incomplete. Please fix errors above.[/bold red]")

        return all_good
