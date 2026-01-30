"""Command-line interface for Nano Banana Pro."""

from pathlib import Path
from typing import Optional

import click
import mlflow
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from . import __version__

# Load environment variables from .env file
load_dotenv()
from .analyzer import PromptAnalyzer
from .config import AppConfig
from .evaluator import Evaluator
from .gemini_client import GeminiClient
from .logos import LogoKitHandler
from .mlflow_tracker import MLflowTracker
from .models import DiagramSpec
from .prompts import PromptBuilder
from .prompt_refiner import PromptRefiner
from .runner import DiagramRunner


console = Console()


class Context:
    """Shared context for CLI commands."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize context.

        Args:
            config_path: Optional path to config file
        """
        self.config = AppConfig.load(config_path)
        self.logo_handler = LogoKitHandler(self.config.logo_kit)
        self.prompt_builder = PromptBuilder()
        self.gemini_client = GeminiClient()  # Uses API key from environment
        self.mlflow_tracker = MLflowTracker(self.config.mlflow)
        self.evaluator = Evaluator(self.mlflow_tracker)
        self.analyzer = PromptAnalyzer(self.mlflow_tracker)
        self.runner = DiagramRunner(
            self.config,
            self.logo_handler,
            self.prompt_builder,
            self.gemini_client,
            self.mlflow_tracker,
        )
        self.prompt_refiner = PromptRefiner(
            self.gemini_client,
            self.mlflow_tracker,
            self.prompt_builder,
        )


@click.group()
@click.version_option(version=__version__, prog_name="nano-banana")
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),
    help="Path to config file (default: configs/default.yaml)",
)
@click.pass_context
def main(ctx: click.Context, config: Optional[Path]):
    """Nano Banana Pro - MLflow-tracked prompt engineering for architecture diagrams.

    Generate, track, and evaluate architecture diagrams using Vertex AI.
    """
    ctx.obj = Context(config)


@main.command()
@click.option(
    "--diagram-spec",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to diagram specification YAML file",
)
@click.option(
    "--template",
    required=True,
    help="Prompt template ID (e.g., 'baseline', 'detailed')",
)
@click.option("--run-name", help="Optional run name for MLflow")
@click.option(
    "--tag",
    multiple=True,
    help="Tags as key=value (can be specified multiple times)",
)
@click.pass_obj
def generate(
    ctx: Context,
    diagram_spec: Path,
    template: str,
    run_name: Optional[str],
    tag: tuple[str],
):
    """Generate a diagram from a specification.

    Example:

        nano-banana generate \\
            --diagram-spec examples/diagram_specs/example_basic.yaml \\
            --template baseline \\
            --run-name "test-run-1" \\
            --tag "experiment=baseline" \\
            --tag "version=1"
    """
    try:
        # Parse tags
        tags = {}
        for tag_str in tag:
            if "=" in tag_str:
                key, value = tag_str.split("=", 1)
                tags[key] = value
            else:
                console.print(f"[yellow]Warning: Ignoring invalid tag '{tag_str}'[/yellow]")

        # Initialize MLflow
        console.print("[bold]Initializing MLflow...[/bold]")
        ctx.mlflow_tracker.initialize()

        # Load diagram spec
        console.print(f"[bold]Loading diagram spec from {diagram_spec.name}...[/bold]")
        spec = DiagramSpec.from_yaml(diagram_spec)

        # Run experiment
        console.print(f"\n[bold]Generating diagram...[/bold]\n")
        result = ctx.runner.run_experiment(spec, template, run_name, tags)

        if result.success:
            console.print(f"\n[bold green]Success![/bold green]")
            console.print(f"\nTo evaluate: nano-banana evaluate {result.run_id}")
            console.print(f"To view runs: nano-banana list-runs")
        else:
            console.print(f"\n[bold red]Failed: {result.error_message}[/bold red]")
            raise click.Exit(1)

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise click.Exit(1)


@main.command()
@click.argument("run_id")
@click.option(
    "--eval-file",
    type=click.Path(exists=True, path_type=Path),
    help="Load evaluation from JSON file instead of interactive",
)
@click.pass_obj
def evaluate(ctx: Context, run_id: str, eval_file: Optional[Path]):
    """Evaluate a generated diagram.

    Provides interactive scoring interface or loads scores from file.

    Example:

        nano-banana evaluate abc123def456
    """
    try:
        # Initialize MLflow
        ctx.mlflow_tracker.initialize()

        # Run evaluation
        interactive = eval_file is None
        scores = ctx.evaluator.evaluate_run(run_id, interactive=interactive, eval_file=eval_file)

        console.print(f"\n[bold green]Evaluation complete![/bold green]")
        console.print(f"Overall score: {scores.overall_score:.2f}/5")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise click.Exit(1)


@main.command()
@click.option(
    "--filter",
    "filter_string",
    help="MLflow filter string (e.g., 'metrics.overall_score > 4.0')",
)
@click.option(
    "--max-results",
    default=10,
    type=int,
    help="Maximum number of runs to display",
)
@click.pass_obj
def list_runs(ctx: Context, filter_string: Optional[str], max_results: int):
    """List experiment runs.

    Example:

        nano-banana list-runs --max-results 20
        nano-banana list-runs --filter "metrics.overall_score > 4.0"
    """
    try:
        # Initialize MLflow
        ctx.mlflow_tracker.initialize()

        # Get runs
        runs = ctx.mlflow_tracker.list_runs(
            filter_string=filter_string, max_results=max_results
        )

        if not runs:
            console.print("[yellow]No runs found[/yellow]")
            return

        # Display table
        table = Table(title=f"Recent Runs ({len(runs)})", show_header=True)
        table.add_column("Run ID", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Status", style="yellow")
        table.add_column("Template", style="green")
        table.add_column("Overall Score", style="magenta")
        table.add_column("Time", style="blue")

        for run in runs:
            run_id = str(run.get("run_id", ""))[:8]
            run_name = str(run.get("tags.mlflow.runName", run.get("run_name", "N/A")))
            status = str(run.get("status", "UNKNOWN"))
            template = str(run.get("params.prompt_template_id", "N/A"))
            overall_score = run.get("metrics.overall_score", None)
            score_str = f"{overall_score:.2f}" if overall_score is not None else "N/A"
            gen_time = run.get("metrics.generation_time_seconds", None)
            time_str = f"{gen_time:.1f}s" if gen_time is not None else "N/A"

            table.add_row(run_id, run_name, status, template, score_str, time_str)

        console.print(table)
        console.print(f"\nTo view details: nano-banana show-run <run_id>")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise click.Exit(1)


@main.command()
@click.argument("run_id")
@click.pass_obj
def show_run(ctx: Context, run_id: str):
    """Show detailed information about a run.

    Example:

        nano-banana show-run abc123def456
    """
    try:
        # Initialize MLflow
        ctx.mlflow_tracker.initialize()

        # Get run info
        run_info = ctx.mlflow_tracker.get_run_info(run_id)

        console.print(f"\n[bold]Run Details: {run_id}[/bold]\n")
        console.print(f"Name: {run_info.get('run_name', 'N/A')}")
        console.print(f"Status: {run_info['status']}")
        console.print(f"Start: {run_info.get('start_time', 'N/A')}")
        console.print(f"End: {run_info.get('end_time', 'N/A')}")

        # Parameters
        console.print("\n[bold]Parameters:[/bold]")
        for key, value in sorted(run_info["parameters"].items()):
            console.print(f"  {key}: {value}")

        # Metrics
        console.print("\n[bold]Metrics:[/bold]")
        for key, value in sorted(run_info["metrics"].items()):
            console.print(f"  {key}: {value}")

        # Artifacts
        console.print(f"\n[bold]Artifacts:[/bold]")
        console.print(f"  Location: {run_info['artifact_uri']}")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise click.Exit(1)


@main.command()
@click.option(
    "--prompt-file",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to prompt file (.txt or .md)",
)
@click.option(
    "--logo-dir",
    type=click.Path(exists=True, path_type=Path),
    default="examples/logo_kit",
    help="Directory containing logo files (default: examples/logo_kit). Ignored if --logo is used.",
)
@click.option(
    "--logo",
    "logo_files",
    multiple=True,
    type=click.Path(exists=True, path_type=Path),
    help="Specific logo file(s) to include (can be specified multiple times). If provided, --logo-dir is ignored.",
)
@click.option(
    "--branding",
    type=click.Path(exists=True, path_type=Path),
    default="examples/branding/minimal.txt",
    help="Path to branding/style guide file (.txt or .md). Use minimal.txt for best logo fidelity.",
)
@click.option("--run-name", help="Optional run name for MLflow")
@click.option(
    "--tag",
    multiple=True,
    help="Tags as key=value (can be specified multiple times)",
)
@click.option(
    "--temperature",
    default=0.8,
    type=float,
    help="Sampling temperature: 0.0=deterministic, 0.8=balanced for diagrams, 2.0=creative (default: 0.8)",
)
@click.option(
    "--top-p",
    default=0.95,
    type=float,
    help="Nucleus sampling: lower=more focused, higher=more diverse (default: 0.95)",
)
@click.option(
    "--top-k",
    default=50,
    type=int,
    help="Top-k sampling: limits token choices for consistency (default: 50, set 0 to disable). Higher values help with logo inclusion.",
)
@click.option(
    "--presence-penalty",
    default=0.1,
    type=float,
    help="Penalty for repeating elements: 0.0=none, higher=less repetition (default: 0.1)",
)
@click.option(
    "--frequency-penalty",
    default=0.1,
    type=float,
    help="Penalty for frequent patterns: 0.0=none, higher=less repetition (default: 0.1)",
)
@click.option(
    "--system-instruction",
    default=None,
    type=str,
    help="System-level instruction to guide model behavior (default: uses architecture diagram defaults)",
)
@click.option(
    "--count",
    default=1,
    type=int,
    help="Number of images to generate (default: 1)",
)
@click.option(
    "--size",
    default="1K",
    type=click.Choice(["1K", "2K", "4K"]),
    help="Image size/resolution (default: 2K)",
)
@click.option(
    "--aspect-ratio",
    default="16:9",
    type=click.Choice(["1:1", "4:3", "16:9", "9:16", "3:4", "21:9"]),
    help="Image aspect ratio (default: 16:9). Use 21:9 for wide banners.",
)
@click.option(
    "--avoid",
    default=None,
    help="Things to avoid (simulates negative prompt), e.g. 'blurry, spelling errors, 3D'",
)
@click.option(
    "--feedback/--no-feedback",
    default=False,
    help="Prompt for quick 1-5 scoring after each generation",
)
@click.option(
    "--databricks-style/--no-databricks-style",
    default=False,
    help="Apply official Databricks brand style guide (colors, typography, visual style)",
)
@click.pass_obj
def generate_raw(
    ctx: Context,
    prompt_file: Path,
    logo_dir: Optional[Path],
    logo_files: tuple[Path],
    branding: Optional[Path],
    run_name: Optional[str],
    tag: tuple[str],
    temperature: float,
    top_p: float,
    top_k: int,
    presence_penalty: float,
    frequency_penalty: float,
    system_instruction: Optional[str],
    count: int,
    size: str,
    aspect_ratio: str,
    avoid: Optional[str],
    feedback: bool,
    databricks_style: bool,
):
    """Generate a diagram from a raw prompt file with logo kit attached.

    This command takes a plain text prompt and prepends the logo kit section
    with all critical constraints. No YAML diagram spec required.

    Examples:

        # Load all logos from directory
        nano-banana generate-raw \\
            --prompt-file examples/diagram_specs/agl_data_architecture.txt \\
            --logo-dir examples/logo_kit \\
            --run-name "agl-arch-v1"

        # Use specific logos only
        nano-banana generate-raw \\
            --prompt-file examples/diagram_specs/agl_data_architecture.txt \\
            --logo examples/logo_kit/databricks-logo.png \\
            --logo examples/logo_kit/azure-logo.png \\
            --run-name "minimal-diagram"
    """
    try:
        # Parse tags
        tags = {}
        for tag_str in tag:
            if "=" in tag_str:
                key, value = tag_str.split("=", 1)
                tags[key] = value
            else:
                console.print(f"[yellow]Warning: Ignoring invalid tag '{tag_str}'[/yellow]")

        # Initialize MLflow (use default experiment name from config)
        console.print("[bold]Initializing MLflow...[/bold]")
        ctx.mlflow_tracker.initialize()

        # Load logos - either specific files or from directory
        if logo_files:
            # Load specific logo files
            console.print(f"[bold]Loading {len(logo_files)} specific logo(s)...[/bold]")
            logos = []
            for logo_file in logo_files:
                try:
                    logo = ctx.logo_handler._load_single_logo(logo_file)
                    logos.append(logo)
                    console.print(f"  ✓ {logo_file.name}")
                except Exception as e:
                    console.print(f"  [red]✗ Failed to load {logo_file.name}: {e}[/red]")
            
            if not logos:
                raise click.ClickException("No valid logos loaded. Check logo file paths.")
            
            # Set logo_path for logging purposes (use directory of first logo file)
            logo_path = logo_files[0].parent if logo_files else (logo_dir or ctx.config.logo_kit.logo_dir)
        else:
            # Load all logos from directory
            logo_path = logo_dir or ctx.config.logo_kit.logo_dir
            console.print(f"[bold]Loading logos from {logo_path}...[/bold]")
            logos = ctx.logo_handler.load_logo_kit(logo_path)
            console.print(f"  Loaded {len(logos)} logos")

        # Read raw prompt
        console.print(f"[bold]Reading prompt from {prompt_file.name}...[/bold]")
        raw_prompt = prompt_file.read_text()

        # Read branding if provided
        branding_section = ""
        if branding:
            console.print(f"[bold]Loading branding from {branding.name}...[/bold]")
            branding_section = branding.read_text()

        # Skip best practices - too verbose, reduces logo fidelity
        # Use minimal branding instead for better results
        best_practices_section = ""

        # Build logo section
        logo_section = ctx.prompt_builder._build_logo_section(logos)

        # Combine: logo section + branding + best practices + raw prompt
        sections = [logo_section]
        if branding_section:
            sections.append(branding_section)
        if best_practices_section:
            sections.append(best_practices_section)

        # Add Databricks brand style guide if requested
        if databricks_style:
            from .databricks_style import get_style_prompt
            console.print("[bold]Applying Databricks brand style guide...[/bold]")
            sections.append(get_style_prompt())
        else:
            # Add generic visual styling enhancement section
            visual_style_section = """
=== VISUAL ENHANCEMENT GUIDELINES ===
- Make logos prominent and clearly visible - Unity Catalog logo should be as visible as other major logos
- Add visual interest with subtle professional styling: rounded corners, subtle shadows, color accents
- Use clear typography hierarchy - important text should stand out
- Make the diagram visually engaging while maintaining professional appearance
- Unity Catalog: When mentioned, display the Unity Catalog logo prominently - use the actual logo image, NOT a small generic grey icon
- Ensure Unity Catalog logo is clearly visible and recognizable, matching the prominence of Databricks, Azure, and Delta Lake logos
"""
            sections.append(visual_style_section)

        sections.append(raw_prompt)

        # Add negative prompt / avoid section (always include defaults)
        default_avoid = "blurry, low quality, distorted text, spelling errors, typos, 3D render, isometric, realistic photo, noise, grain, handwriting, sketch, messy, cluttered, tiny generic icons for Unity Catalog, numbered circles, step numbers in circles, numeric sequence markers, callout numbers"
        if avoid:
            full_avoid = f"{default_avoid}, {avoid}"
        else:
            full_avoid = default_avoid

        avoid_section = f"""
**AVOID (DO NOT include any of the following):**
{full_avoid}

Ensure the output does NOT contain any of the above qualities or elements. Double-check all text for spelling accuracy.
**SPECIFICALLY**:
- Do NOT create small generic grey icons for Unity Catalog - use the actual Unity Catalog logo image prominently.
- Do NOT add numbered circles (1, 2, 3) or step indicators unless explicitly requested in the prompt.
- Do NOT add numeric labels or annotations to logos or components.
"""
        sections.append(avoid_section)

        # Add explicit component-to-logo mapping section BEFORE building final prompt
        # Extract component names from prompt and map to logos
        component_logo_mapping = []
        prompt_lower = raw_prompt.lower()
        
        # Build mapping based on logo names found in prompt
        for idx, logo in enumerate(logos, 1):
            logo_name_variants = [
                logo.name.lower(),
                logo.name.replace('-', ' ').replace('_', ' ').lower(),
                logo.name.replace('-logo', '').replace('_logo', '').lower(),
                logo.name.replace('00-', '').replace('-logo', '').replace('_logo', '').lower(),
            ]
            
            # Special handling for Unity Catalog
            if "unity" in logo.name.lower() or "uc" in logo.name.lower() or "00-unity" in logo.name.lower():
                logo_name_variants.extend(["unity catalog", "unity-catalog", "uc", "governance", "catalog"])
            
            for variant in logo_name_variants:
                if variant in prompt_lower:
                    # Find context around the mention
                    logo_display = logo.name.replace('-', ' ').replace('_', ' ').replace('00-', '').title()
                    component_logo_mapping.append(f"- Components/text mentioning '{logo_display}' or related terms → Use Image {idx} ({logo_display} logo)")
                    break
        
        # Also add explicit mappings for common patterns
        if "azure" in prompt_lower:
            azure_logo = next((logo for logo in logos if "azure" in logo.name.lower()), None)
            if azure_logo:
                idx = logos.index(azure_logo) + 1
                component_logo_mapping.append(f"- Azure services/components (Azure Data Factory, Azure Synapse, etc.) → Use Image {idx} (Azure logo)")
        
        if "databricks" in prompt_lower:
            db_logo = next((logo for logo in logos if "databricks" in logo.name.lower()), None)
            if db_logo:
                idx = logos.index(db_logo) + 1
                component_logo_mapping.append(f"- Databricks components → Use Image {idx} (Databricks logo)")
        
        if "delta" in prompt_lower or "delta lake" in prompt_lower:
            delta_logo = next((logo for logo in logos if "delta" in logo.name.lower()), None)
            if delta_logo:
                idx = logos.index(delta_logo) + 1
                component_logo_mapping.append(f"- Delta Lake components → Use Image {idx} (Delta Lake logo)")
        
        # Keep logo mapping minimal to avoid confusing the model
        if component_logo_mapping:
            mapping_section = "Logo mapping: " + ", ".join(component_logo_mapping[:5])
            sections.insert(1, mapping_section)

        final_prompt = "\n\n".join(sections)

        # Ensure critical constraints are present
        critical_constraints = [
            "Reuse uploaded logos EXACTLY",
            "Scale all logos uniformly",
            "NO filenames"
        ]
        has_constraints = all(
            constraint.lower() in final_prompt.lower()
            for constraint in critical_constraints
        )
        # Add simple reminder - avoid verbose instructions that cause numbered circles
        if not has_constraints:
            final_prompt = "Use uploaded logos exactly. No numbered labels.\n\n" + final_prompt

        # Convert logos to image parts (once, reused for all generations)
        logo_parts = [
            ctx.logo_handler.to_image_part(logo) for logo in logos
        ]

        import time
        from datetime import datetime
        import json

        # Create date-based output folder: outputs/YYYY-MM-DD/{run_name}/
        # Files are timestamped: diagram_{HHMMSS}.png, metadata_{HHMMSS}.json
        now = datetime.now()
        date_folder = now.strftime("%Y-%m-%d")
        time_stamp = now.strftime("%H%M%S")
        batch_name = run_name or prompt_file.stem
        batch_dir = Path("outputs") / date_folder / batch_name
        batch_dir.mkdir(parents=True, exist_ok=True)

        # Save prompt once to batch folder (overwrite if exists)
        (batch_dir / "prompt.txt").write_text(final_prompt)

        output_images = []

        for i in range(count):
            iteration = f" ({i+1}/{count})" if count > 1 else ""
            console.print(f"\n[bold]Generating diagram{iteration}...[/bold]\n")

            # Start MLflow run
            run_name_final = batch_name if count == 1 else f"{batch_name}-{i+1}"
            run_id = ctx.mlflow_tracker.start_run(run_name=run_name_final)

            try:
                # Log parameters
                params = {
                    "prompt_file": prompt_file.name,
                    "prompt_template_id": "raw",
                    "logo_count": len(logos),
                    "logo_dir": str(logo_path),
                    "branding_file": branding.name if branding else "none",
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k if top_k > 0 else None,
                    "presence_penalty": presence_penalty,
                    "frequency_penalty": frequency_penalty,
                    "image_size": size,
                    "aspect_ratio": aspect_ratio,
                    "iteration": i + 1,
                    "batch_count": count,
                    "has_custom_system_instruction": system_instruction is not None,
                }
                ctx.mlflow_tracker.log_parameters(params)

                # Log tags
                for key, value in tags.items():
                    mlflow.set_tag(key, value)

                # Log prompt as artifact
                ctx.mlflow_tracker.log_prompt(final_prompt, "prompt.txt")

                # Generate image
                start_time = time.time()

                image_bytes, response_text, metadata = ctx.gemini_client.generate_image(
                    prompt=final_prompt,
                    logo_parts=logo_parts,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k if top_k > 0 else None,
                    presence_penalty=presence_penalty,
                    frequency_penalty=frequency_penalty,
                    system_instruction=system_instruction,
                    image_size=size,
                    aspect_ratio=aspect_ratio,
                )

                generation_time = time.time() - start_time
                ctx.mlflow_tracker.log_metrics({"generation_time_seconds": generation_time})

                # Save image to batch folder with timestamp and params
                # Get fresh timestamp for each generation
                gen_time = datetime.now().strftime("%H%M%S")
                # Format temperature for filename (0.8 -> t08, 1.0 -> t10)
                temp_str = f"t{int(temperature * 10):02d}"
                image_filename = f"diagram_{gen_time}_{temp_str}.png"
                image_path = batch_dir / image_filename
                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                # Save metadata for this generation with matching filename base
                meta_filename = f"metadata_{gen_time}_{temp_str}.json"
                run_metadata = {
                    "run_id": run_id,
                    "run_name": run_name_final,
                    "timestamp": now.isoformat(),
                    "iteration": i + 1,
                    "generation_time_seconds": generation_time,
                    "temperature": temperature,
                    "top_p": top_p,
                    "image_size": size,
                    "aspect_ratio": aspect_ratio,
                    "logo_count": len(logos),
                    "prompt_file": str(prompt_file),
                    "branding_file": str(branding) if branding else None,
                    **metadata,
                }
                (batch_dir / meta_filename).write_text(json.dumps(run_metadata, indent=2))

                ctx.mlflow_tracker.log_output_image(image_path)
                ctx.mlflow_tracker.log_metrics({"success": 1})

                output_images.append(image_filename)
                console.print(f"[green]✓ Saved: {image_filename}[/green]")

                # Collect quick feedback if enabled
                if feedback:
                    console.print(f"\n[bold]Quick feedback for {image_filename}:[/bold]")
                    console.print(f"  [dim]Image at: {image_path}[/dim]")

                    score_input = click.prompt(
                        "  Score (1-5, or Enter to skip)",
                        default="",
                        show_default=False,
                    )

                    user_score = None
                    if score_input.strip():
                        try:
                            user_score = int(score_input)
                            if user_score < 1 or user_score > 5:
                                console.print("  [yellow]Score out of range, skipping[/yellow]")
                                user_score = None
                        except ValueError:
                            console.print("  [yellow]Invalid score, skipping[/yellow]")

                    user_comment = ""
                    if user_score is not None:
                        user_comment = click.prompt(
                            "  Comment (optional, Enter to skip)",
                            default="",
                            show_default=False,
                        )

                    if user_score is not None:
                        ctx.mlflow_tracker.log_metrics({"user_score": user_score})
                        if user_comment:
                            mlflow.set_tag("user_comment", user_comment[:500])

                        # Save feedback to file with matching timestamp
                        feedback_data = {"score": user_score, "comment": user_comment}
                        (batch_dir / f"feedback_{gen_time}.json").write_text(json.dumps(feedback_data, indent=2))
                        console.print(f"  [green]✓ Feedback saved[/green]")

                ctx.mlflow_tracker.end_run("FINISHED")

            except Exception as e:
                ctx.mlflow_tracker.end_run("FAILED")
                console.print(f"[red]✗ Failed: {e}[/red]")

        console.print(f"\n[bold green]Done! Generated {len(output_images)} image(s)[/bold green]")
        console.print(f"  {batch_dir}/")
        console.print(f"    ├── prompt.txt")
        for img in output_images:
            meta = img.replace("diagram", "metadata").replace(".png", ".json")
            console.print(f"    ├── {img}")
            console.print(f"    ├── {meta}")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise SystemExit(1)


@main.command()
@click.option(
    "--logo-dir",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Directory containing logo files",
)
@click.pass_obj
def validate_logos(ctx: Context, logo_dir: Path):
    """Validate a logo kit directory.

    Checks all logos for size, format, and accessibility.

    Example:

        nano-banana validate-logos --logo-dir examples/logo_kit
    """
    try:
        console.print(f"[bold]Validating logos in {logo_dir}...[/bold]\n")

        # Load logos
        logos = ctx.logo_handler.load_logo_kit(logo_dir)

        # Display table
        table = Table(title=f"Logo Kit ({len(logos)} logos)", show_header=True)
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Size", style="yellow")
        table.add_column("Hash (first 8)", style="green")

        for logo in logos:
            size_kb = logo.size_bytes / 1024
            table.add_row(
                logo.name,
                logo.description,
                f"{size_kb:.1f} KB",
                logo.sha256_hash[:8],
            )

        console.print(table)
        console.print(f"\n[bold green]✓ All logos valid![/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise click.Exit(1)


@main.command()
@click.pass_obj
def check_auth(ctx: Context):
    """Verify Google Cloud OAuth authentication.

    Checks that Application Default Credentials are configured correctly.

    Example:

        nano-banana check-auth
    """
    try:
        console.print("[bold]Checking OAuth authentication...[/bold]\n")

        if ctx.vertex_client.verify_auth():
            console.print("[bold green]✓ Authentication successful![/bold green]")
            console.print(f"\nProject: {ctx.config.vertex.project_id}")
            console.print(f"Location: {ctx.config.vertex.location}")
            console.print(f"Model: {ctx.config.vertex.model_id}")
        else:
            console.print("[bold red]✗ Authentication failed[/bold red]")
            console.print("\nPlease run: gcloud auth application-default login")
            raise click.Exit(1)

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        console.print("\nPlease run: gcloud auth application-default login")
        raise click.Exit(1)


@main.command()
@click.pass_obj
def verify_setup(ctx: Context):
    """Verify complete system setup.

    Checks auth, MLflow, logos, and templates.

    Example:

        nano-banana verify-setup
    """
    try:
        # Authenticate
        ctx.vertex_client.authenticate()

        # Run verification
        if ctx.runner.verify_setup():
            console.print("\n[bold green]Ready to generate diagrams![/bold green]")
        else:
            raise click.Exit(1)

    except Exception as e:
        console.print(f"\n[bold red]Setup verification failed: {e}[/bold red]")
        raise click.Exit(1)


@main.command()
@click.option(
    "--min-score",
    default=4.0,
    type=float,
    help="Minimum overall score to consider (default: 4.0)",
)
@click.option(
    "--dimension",
    type=click.Choice(
        [
            "logo_fidelity_score",
            "layout_clarity_score",
            "text_legibility_score",
            "constraint_compliance_score",
        ]
    ),
    help="Focus on specific dimension instead of overall score",
)
@click.option(
    "--max-runs",
    default=50,
    type=int,
    help="Maximum number of runs to analyze",
)
@click.pass_obj
def analyze_prompts(
    ctx: Context,
    min_score: float,
    dimension: Optional[str],
    max_runs: int,
):
    """Analyze patterns in high-scoring prompts.

    Finds common patterns, phrases, and correlations in prompts
    from runs that scored above the threshold.

    Example:

        nano-banana analyze-prompts --min-score 4.5
        nano-banana analyze-prompts --dimension logo_fidelity_score --min-score 4.0
    """
    try:
        # Initialize MLflow
        ctx.mlflow_tracker.initialize()

        # Run analysis
        ctx.analyzer.analyze_high_scoring_runs(
            min_score=min_score,
            dimension=dimension,
            max_runs=max_runs,
        )

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise click.Exit(1)


@main.command()
@click.option(
    "--template",
    help="Template ID to analyze and suggest improvements for",
)
@click.option(
    "--min-score",
    default=4.0,
    type=float,
    help="Minimum score for reference runs (default: 4.0)",
)
@click.pass_obj
def suggest_improvements(
    ctx: Context,
    template: Optional[str],
    min_score: float,
):
    """Suggest prompt improvements based on successful runs.

    Analyzes high-scoring runs and suggests what to add or change
    in your prompts to improve results.

    Example:

        nano-banana suggest-improvements --template baseline --min-score 4.5
        nano-banana suggest-improvements --min-score 4.0
    """
    try:
        # Initialize MLflow
        ctx.mlflow_tracker.initialize()

        # Get current prompt if template specified
        current_prompt = None
        if template:
            try:
                template_obj = ctx.prompt_builder.load_template(template)
                current_prompt = template_obj.template
            except Exception:
                console.print(f"[yellow]Note: Could not load template '{template}'[/yellow]")

        # Get suggestions
        ctx.analyzer.suggest_improvements(
            template_id=template,
            current_prompt=current_prompt,
            min_score=min_score,
        )

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise click.Exit(1)


@main.command()
@click.pass_obj
def template_stats(ctx: Context):
    """Show performance statistics by template.

    Displays average scores, run counts, and score ranges
    for each prompt template.

    Example:

        nano-banana template-stats
    """
    try:
        # Initialize MLflow
        ctx.mlflow_tracker.initialize()

        # Get stats
        ctx.analyzer.template_performance()

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise click.Exit(1)


@main.command()
@click.option(
    "--template",
    help="Filter by specific template",
)
@click.pass_obj
def dimension_stats(ctx: Context, template: Optional[str]):
    """Show score statistics by evaluation dimension.

    Displays average scores for each evaluation dimension
    (logo fidelity, layout clarity, etc.).

    Example:

        nano-banana dimension-stats
        nano-banana dimension-stats --template baseline
    """
    try:
        # Initialize MLflow
        ctx.mlflow_tracker.initialize()

        # Get stats
        ctx.analyzer.dimension_analysis(template_id=template)

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise click.Exit(1)


@main.command()
@click.argument("run_id")
@click.option(
    "--feedback",
    required=True,
    help="Feedback on what to improve (e.g., 'logos not included, text is blurry')",
)
@click.option(
    "--temperature",
    default=0.8,
    type=float,
    help="Sampling temperature (default: 0.8)",
)
@click.option(
    "--top-p",
    default=0.95,
    type=float,
    help="Nucleus sampling (default: 0.95)",
)
@click.option(
    "--top-k",
    default=40,
    type=int,
    help="Top-k sampling (default: 40, set 0 to disable)",
)
@click.option(
    "--presence-penalty",
    default=0.1,
    type=float,
    help="Penalty for repeating elements (default: 0.1)",
)
@click.option(
    "--frequency-penalty",
    default=0.1,
    type=float,
    help="Penalty for frequent patterns (default: 0.1)",
)
@click.option(
    "--count",
    default=1,
    type=int,
    help="Number of refined images to generate (default: 1)",
)
@click.pass_obj
def refine(
    ctx: Context,
    run_id: str,
    feedback: str,
    temperature: float,
    top_p: float,
    top_k: int,
    presence_penalty: float,
    frequency_penalty: float,
    count: int,
):
    """Refine a previous generation based on feedback.

    Takes a run ID, retrieves the original prompt, appends your feedback
    as refinement instructions, and regenerates.

    Example:

        nano-banana refine abc123 --feedback "logos not used, text is blurry"
        nano-banana refine abc123 --feedback "need more spacing between layers" --count 3
    """
    import time

    try:
        # Initialize MLflow
        console.print("[bold]Initializing MLflow...[/bold]")
        ctx.mlflow_tracker.initialize()

        # Get original run info
        console.print(f"[bold]Loading run {run_id[:8]}...[/bold]")
        run_info = ctx.mlflow_tracker.get_run_info(run_id)

        # Get artifact URI and load original prompt
        artifact_uri = run_info["artifact_uri"]
        prompt_path = Path(artifact_uri.replace("file://", "").replace("dbfs:", "/dbfs")) / "prompts" / "prompt.txt"

        if not prompt_path.exists():
            # Try alternative path structures
            alt_paths = [
                Path(artifact_uri.replace("file://", "")) / "prompt.txt",
                Path(artifact_uri.replace("dbfs:", "/dbfs")) / "prompt.txt",
            ]
            for alt in alt_paths:
                if alt.exists():
                    prompt_path = alt
                    break

        if not prompt_path.exists():
            console.print(f"[red]Could not find original prompt at {prompt_path}[/red]")
            console.print("[yellow]Falling back to parameters...[/yellow]")
            # Try to reconstruct from parameters
            params = run_info["parameters"]
            raise click.ClickException(
                f"Original prompt not found. Check artifact_uri: {artifact_uri}"
            )

        original_prompt = prompt_path.read_text()
        console.print(f"  Loaded original prompt ({len(original_prompt)} chars)")

        # Build refinement section
        refinement_section = f"""

---
REFINEMENT INSTRUCTIONS (CRITICAL - MUST FOLLOW):
The previous generation had these issues that MUST be fixed:
{feedback}

Please regenerate addressing ALL of the above feedback.
---
"""

        refined_prompt = original_prompt + refinement_section
        console.print(f"  Added refinement instructions")

        # Get logo directory from original params
        params = run_info["parameters"]
        logo_dir = Path(params.get("logo_dir", "examples/logo_kit"))

        # Load logos
        console.print(f"[bold]Loading logos from {logo_dir}...[/bold]")
        logos = ctx.logo_handler.load_logo_kit(logo_dir)
        console.print(f"  Loaded {len(logos)} logos")

        # Convert logos to image parts
        logo_parts = [ctx.logo_handler.to_image_part(logo) for logo in logos]

        from datetime import datetime
        import json

        output_dirs = []
        original_run_name = run_info.get("run_name", "unknown")

        for i in range(count):
            iteration = f" ({i+1}/{count})" if count > 1 else ""
            console.print(f"\n[bold]Generating refined diagram{iteration}...[/bold]\n")

            # Start new MLflow run
            new_run_name = f"refine-{original_run_name}-{i+1}" if count > 1 else f"refine-{original_run_name}"
            new_run_id = ctx.mlflow_tracker.start_run(run_name=new_run_name)

            # Create date-based output folder: outputs/YYYY-MM-DD/{run_name}/
            # Files are timestamped: diagram_{HHMMSS}.png, metadata_{HHMMSS}.json
            now = datetime.now()
            date_folder = now.strftime("%Y-%m-%d")
            time_stamp = now.strftime("%H%M%S")
            run_dir = Path("outputs") / date_folder / new_run_name
            run_dir.mkdir(parents=True, exist_ok=True)

            try:
                # Log parameters
                ctx.mlflow_tracker.log_parameters({
                    "original_run_id": run_id,
                    "feedback": feedback[:500],  # Truncate if too long
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k if top_k > 0 else None,
                    "presence_penalty": presence_penalty,
                    "frequency_penalty": frequency_penalty,
                    "iteration": i + 1,
                    "prompt_template_id": "refined",
                    "logo_count": len(logos),
                })

                # Log refined prompt
                ctx.mlflow_tracker.log_prompt(refined_prompt, "prompt.txt")

                # Save prompt to run folder (overwrite if exists)
                (run_dir / "prompt.txt").write_text(refined_prompt)

                # Save feedback to run folder (overwrite if exists)
                (run_dir / "feedback.txt").write_text(feedback)

                # Generate
                start_time = time.time()
                image_bytes, response_text, metadata = ctx.gemini_client.generate_image(
                    prompt=refined_prompt,
                    logo_parts=logo_parts,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k if top_k > 0 else None,
                    presence_penalty=presence_penalty,
                    frequency_penalty=frequency_penalty,
                )
                generation_time = time.time() - start_time

                ctx.mlflow_tracker.log_metrics({"generation_time_seconds": generation_time})

                # Save image with timestamp and params
                gen_time = datetime.now().strftime("%H%M%S")
                temp_str = f"t{int(temperature * 10):02d}"
                image_path = run_dir / f"diagram_{gen_time}_{temp_str}.png"
                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                # Save metadata with matching filename base
                run_metadata = {
                    "run_id": new_run_id,
                    "run_name": new_run_name,
                    "original_run_id": run_id,
                    "original_run_name": original_run_name,
                    "timestamp": now.isoformat(),
                    "generation_time_seconds": generation_time,
                    "temperature": temperature,
                    "logo_count": len(logos),
                    "feedback": feedback,
                    **metadata,
                }
                (run_dir / f"metadata_{gen_time}_{temp_str}.json").write_text(json.dumps(run_metadata, indent=2))

                ctx.mlflow_tracker.log_output_image(image_path)
                ctx.mlflow_tracker.log_metrics({"success": 1})
                ctx.mlflow_tracker.end_run("FINISHED")

                output_dirs.append((run_dir, f"diagram_{gen_time}_{temp_str}.png", f"metadata_{gen_time}_{temp_str}.json"))
                console.print(f"[green]✓ Saved to: {run_dir}/diagram_{gen_time}_{temp_str}.png[/green]")

            except Exception as e:
                ctx.mlflow_tracker.end_run("FAILED")
                console.print(f"[red]✗ Failed: {e}[/red]")

        console.print(f"\n[bold green]Done! Generated {len(output_dirs)} refined run(s)[/bold green]")
        for d, img, meta in output_dirs:
            console.print(f"  {d}/")
            console.print(f"    ├── {img}")
            console.print(f"    ├── {meta}")
            console.print(f"    ├── prompt.txt")
            console.print(f"    └── feedback.txt")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
