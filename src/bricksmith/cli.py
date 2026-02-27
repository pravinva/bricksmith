"""Command-line interface for Bricksmith."""

from datetime import datetime
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
from .config import AppConfig
from .evaluator import Evaluator
from .gemini_client import GeminiClient
from .image_generator import ImageGenerator
from .logos import LogoKitHandler
from .databricks_image_client import DatabricksImageClient
from .openai_image_client import OpenAIImageClient
from .mlflow_tracker import MLflowTracker
from .prompts import PromptBuilder
from .prompt_refiner import PromptRefiner
from .conversation import ConversationChatbot
from .models import ConversationConfig, ArchitectConfig

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
        self.prompt_builder = PromptBuilder(logo_handler=self.logo_handler)
        self.gemini_client = GeminiClient()  # For analysis (evaluate, refine, judge)
        self._image_generator: ImageGenerator | None = None
        self.mlflow_tracker = MLflowTracker(self.config.mlflow)
        self.evaluator = Evaluator(self.mlflow_tracker)
        self.prompt_refiner = PromptRefiner(
            self.gemini_client,
            self.mlflow_tracker,
            self.prompt_builder,
        )

    @property
    def image_generator(self) -> ImageGenerator:
        """Lazy-initialized image generator (Gemini, OpenAI, or Databricks) from config."""
        if self._image_generator is None:
            prov = self.config.image_provider
            if prov.provider == "openai":
                self._image_generator = OpenAIImageClient(model=prov.openai_model)
            elif prov.provider == "databricks":
                self._image_generator = DatabricksImageClient(
                    model=prov.databricks_model,
                    image_model=prov.databricks_image_model,
                )
            else:
                self._image_generator = self.gemini_client
        return self._image_generator

    def set_image_provider(self, provider: str) -> None:
        """Override image provider for this context (e.g. from CLI --image-provider)."""
        prov = self.config.image_provider
        if provider == "openai":
            self._image_generator = OpenAIImageClient(model=prov.openai_model)
        elif provider == "databricks":
            self._image_generator = DatabricksImageClient(
                model=prov.databricks_model,
                image_model=prov.databricks_image_model,
            )
        else:
            self._image_generator = self.gemini_client


@click.group()
@click.version_option(version=__version__, prog_name="bricksmith")
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),
    help="Path to config file (default: configs/default.yaml)",
)
@click.option(
    "--image-provider",
    type=click.Choice(["gemini", "openai", "databricks"]),
    default=None,
    help="Image generation backend: gemini (default), openai (gpt-image-1.5), or databricks (AWS US). Overrides config.",
)
@click.pass_context
def main(ctx: click.Context, config: Optional[Path], image_provider: Optional[str]):
    """Bricksmith - MLflow-tracked prompt engineering for architecture diagrams.

    Generate, track, and evaluate architecture diagrams using Vertex AI.
    """
    obj = Context(config)
    if image_provider is not None:
        obj.set_image_provider(image_provider)
    ctx.obj = obj


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

        bricksmith evaluate abc123def456
    """
    try:
        # Initialize MLflow
        ctx.mlflow_tracker.initialize()

        # Run evaluation
        interactive = eval_file is None
        scores = ctx.evaluator.evaluate_run(run_id, interactive=interactive, eval_file=eval_file)

        console.print("\n[bold green]Evaluation complete![/bold green]")
        console.print(f"Overall score: {scores.overall_score:.2f}/10")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise SystemExit(1)


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

        bricksmith list-runs --max-results 20
        bricksmith list-runs --filter "metrics.overall_score > 4.0"
    """
    try:
        # Initialize MLflow
        ctx.mlflow_tracker.initialize()

        # Get runs
        runs = ctx.mlflow_tracker.list_runs(filter_string=filter_string, max_results=max_results)

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
        console.print("\nTo view details: bricksmith show-run <run_id>")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise SystemExit(1)


@main.command()
@click.argument("run_id")
@click.pass_obj
def show_run(ctx: Context, run_id: str):
    """Show detailed information about a run.

    Example:

        bricksmith show-run abc123def456
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
        console.print("\n[bold]Artifacts:[/bold]")
        console.print(f"  Location: {run_info['artifact_uri']}")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise SystemExit(1)


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
    default="logos/default",
    help="Directory containing logo files (default: logos/default). Ignored if --logo is used.",
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
    default="prompts/branding/databricks_default.txt",
    help="Path to branding/style guide file (.txt or .md). Defaults to Databricks branding.",
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
    help="Prompt for quick 1-10 scoring after each generation",
)
@click.option(
    "--databricks-style/--no-databricks-style",
    default=True,
    help="Apply official Databricks brand style guide (enabled by default)",
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
        bricksmith generate-raw \\
            --prompt-file prompts/diagram_specs/agl_data_architecture.txt \\
            --logo-dir logos/default \\
            --run-name "agl-arch-v1"

        # Use specific logos only
        bricksmith generate-raw \\
            --prompt-file prompts/diagram_specs/agl_data_architecture.txt \\
            --logo logos/default/databricks-logo.png \\
            --logo logos/default/azure-logo.png \\
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
        run_group = tags.get("run_group") or tags.get("group")

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
            logo_path = (
                logo_files[0].parent if logo_files else (logo_dir or ctx.config.logo_kit.logo_dir)
            )
        else:
            # Load all logos from directory
            logo_path = logo_dir or ctx.config.logo_kit.logo_dir
            console.print(f"[bold]Loading logos from {logo_path}...[/bold]")
            logos = ctx.logo_handler.load_logo_kit(logo_path)
            logo_hints = ctx.logo_handler.load_logo_hints(logo_path)
            hints_msg = f" with {len(logo_hints)} hints" if logo_hints else ""
            console.print(f"  Loaded {len(logos)} logos{hints_msg}")

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
                logo.name.replace("-", " ").replace("_", " ").lower(),
                logo.name.replace("-logo", "").replace("_logo", "").lower(),
                logo.name.replace("00-", "").replace("-logo", "").replace("_logo", "").lower(),
            ]

            # Special handling for Unity Catalog
            if (
                "unity" in logo.name.lower()
                or "uc" in logo.name.lower()
                or "00-unity" in logo.name.lower()
            ):
                logo_name_variants.extend(
                    ["unity catalog", "unity-catalog", "uc", "governance", "catalog"]
                )

            for variant in logo_name_variants:
                if variant in prompt_lower:
                    # Find context around the mention
                    logo_display = (
                        logo.name.replace("-", " ").replace("_", " ").replace("00-", "").title()
                    )
                    component_logo_mapping.append(
                        f"- Components/text mentioning '{logo_display}' or related terms → Use Image {idx} ({logo_display} logo)"
                    )
                    break

        # Also add explicit mappings for common patterns
        if "azure" in prompt_lower:
            azure_logo = next((logo for logo in logos if "azure" in logo.name.lower()), None)
            if azure_logo:
                idx = logos.index(azure_logo) + 1
                component_logo_mapping.append(
                    f"- Azure services/components (Azure Data Factory, Azure Synapse, etc.) → Use Image {idx} (Azure logo)"
                )

        if "databricks" in prompt_lower:
            db_logo = next((logo for logo in logos if "databricks" in logo.name.lower()), None)
            if db_logo:
                idx = logos.index(db_logo) + 1
                component_logo_mapping.append(
                    f"- Databricks components → Use Image {idx} (Databricks logo)"
                )

        if "delta" in prompt_lower or "delta lake" in prompt_lower:
            delta_logo = next((logo for logo in logos if "delta" in logo.name.lower()), None)
            if delta_logo:
                idx = logos.index(delta_logo) + 1
                component_logo_mapping.append(
                    f"- Delta Lake components → Use Image {idx} (Delta Lake logo)"
                )

        # Keep logo mapping minimal to avoid confusing the model
        if component_logo_mapping:
            mapping_section = "Logo mapping: " + ", ".join(component_logo_mapping[:5])
            sections.insert(1, mapping_section)

        final_prompt = "\n\n".join(sections)

        # Ensure critical constraints are present
        critical_constraints = [
            "Reuse uploaded logos EXACTLY",
            "Scale all logos uniformly",
            "NO filenames",
        ]
        has_constraints = all(
            constraint.lower() in final_prompt.lower() for constraint in critical_constraints
        )
        # Add simple reminder - avoid verbose instructions that cause numbered circles
        if not has_constraints:
            final_prompt = "Use uploaded logos exactly. No numbered labels.\n\n" + final_prompt

        # Convert logos to image parts (once, reused for all generations)
        logo_parts = [ctx.logo_handler.to_image_part(logo) for logo in logos]

        import time
        from datetime import datetime
        import json

        # Create date-based output folder: outputs/YYYY-MM-DD/{run_name}/
        # Files are timestamped: diagram_{HHMMSS}.png, metadata_{HHMMSS}.json
        now = datetime.now()
        date_folder = now.strftime("%Y-%m-%d")
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

                image_bytes, response_text, metadata = ctx.image_generator.generate_image(
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
                    "run_group": run_group,
                    "tags": tags,
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
                        "  Score (1-10, or Enter to skip)",
                        default="",
                        show_default=False,
                    )

                    user_score = None
                    if score_input.strip():
                        try:
                            user_score = int(score_input)
                            if user_score < 1 or user_score > 10:
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
                        (batch_dir / f"feedback_{gen_time}.json").write_text(
                            json.dumps(feedback_data, indent=2)
                        )
                        console.print("  [green]✓ Feedback saved[/green]")

                ctx.mlflow_tracker.end_run("FINISHED")

            except Exception as e:
                ctx.mlflow_tracker.end_run("FAILED")
                console.print(f"[red]✗ Failed: {e}[/red]")

        console.print(f"\n[bold green]Done! Generated {len(output_images)} image(s)[/bold green]")
        console.print(f"  {batch_dir}/")
        console.print("    ├── prompt.txt")
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

        bricksmith validate-logos --logo-dir logos/default
    """
    try:
        console.print(f"[bold]Validating logos in {logo_dir}...[/bold]\n")

        # Load logos
        logos = ctx.logo_handler.load_logo_kit(logo_dir)
        ctx.logo_handler.load_logo_hints(logo_dir)

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
        console.print("\n[bold green]✓ All logos valid![/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise SystemExit(1)


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

        bricksmith refine abc123 --feedback "logos not used, text is blurry"
        bricksmith refine abc123 --feedback "need more spacing between layers" --count 3
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
        prompt_path = (
            Path(artifact_uri.replace("file://", "").replace("dbfs:", "/dbfs"))
            / "prompts"
            / "prompt.txt"
        )

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
        console.print("  Added refinement instructions")

        # Get logo directory from original params
        params = run_info["parameters"]
        logo_dir = Path(params.get("logo_dir", "logos/default"))

        # Load logos and hints
        console.print(f"[bold]Loading logos from {logo_dir}...[/bold]")
        logos = ctx.logo_handler.load_logo_kit(logo_dir)
        logo_hints = ctx.logo_handler.load_logo_hints(logo_dir)
        hints_msg = f" with {len(logo_hints)} hints" if logo_hints else ""
        console.print(f"  Loaded {len(logos)} logos{hints_msg}")

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
            new_run_name = (
                f"refine-{original_run_name}-{i+1}" if count > 1 else f"refine-{original_run_name}"
            )
            new_run_id = ctx.mlflow_tracker.start_run(run_name=new_run_name)

            # Create date-based output folder: outputs/YYYY-MM-DD/{run_name}/
            # Files are timestamped: diagram_{HHMMSS}.png, metadata_{HHMMSS}.json
            now = datetime.now()
            date_folder = now.strftime("%Y-%m-%d")
            run_dir = Path("outputs") / date_folder / new_run_name
            run_dir.mkdir(parents=True, exist_ok=True)

            try:
                # Log parameters
                ctx.mlflow_tracker.log_parameters(
                    {
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
                    }
                )

                # Log refined prompt
                ctx.mlflow_tracker.log_prompt(refined_prompt, "prompt.txt")

                # Save prompt to run folder (overwrite if exists)
                (run_dir / "prompt.txt").write_text(refined_prompt)

                # Save feedback to run folder (overwrite if exists)
                (run_dir / "feedback.txt").write_text(feedback)

                # Generate
                start_time = time.time()
                image_bytes, response_text, metadata = ctx.image_generator.generate_image(
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
                (run_dir / f"metadata_{gen_time}_{temp_str}.json").write_text(
                    json.dumps(run_metadata, indent=2)
                )

                ctx.mlflow_tracker.log_output_image(image_path)
                ctx.mlflow_tracker.log_metrics({"success": 1})
                ctx.mlflow_tracker.end_run("FINISHED")

                output_dirs.append(
                    (
                        run_dir,
                        f"diagram_{gen_time}_{temp_str}.png",
                        f"metadata_{gen_time}_{temp_str}.json",
                    )
                )
                console.print(
                    f"[green]✓ Saved to: {run_dir}/diagram_{gen_time}_{temp_str}.png[/green]"
                )

            except Exception as e:
                ctx.mlflow_tracker.end_run("FAILED")
                console.print(f"[red]✗ Failed: {e}[/red]")

        console.print(
            f"\n[bold green]Done! Generated {len(output_dirs)} refined run(s)[/bold green]"
        )
        for d, img, meta in output_dirs:
            console.print(f"  {d}/")
            console.print(f"    ├── {img}")
            console.print(f"    ├── {meta}")
            console.print("    ├── prompt.txt")
            console.print("    └── feedback.txt")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise SystemExit(1)


@main.command()
@click.option(
    "--run-id",
    help="MLflow run ID to analyze",
)
@click.option(
    "--reference-image",
    type=click.Path(exists=True, path_type=Path),
    help="Path to reference image (alternative to --run-id)",
)
@click.option(
    "--original-prompt",
    type=click.Path(exists=True, path_type=Path),
    help="Path to original prompt file (required with --reference-image)",
)
@click.option(
    "--feedback",
    help="User feedback about what to improve",
)
@click.option(
    "--output-template",
    type=click.Path(path_type=Path),
    help="Optional path to save refined prompt as template",
)
@click.pass_obj
def refine_prompt(
    ctx: Context,
    run_id: Optional[str],
    reference_image: Optional[Path],
    original_prompt: Optional[Path],
    feedback: Optional[str],
    output_template: Optional[Path],
):
    """Analyze diagram and suggest prompt improvements.

    Uses visual analysis to identify what worked and what didn't,
    then generates concrete suggestions for improving the prompt.

    Examples:
        # Analyze a previous run
        bricksmith refine-prompt --run-id abc123 --feedback "logos too small"

        # Analyze any image
        bricksmith refine-prompt \\
            --reference-image path/to/diagram.png \\
            --original-prompt path/to/prompt.txt \\
            --feedback "need more spacing"
    """
    try:
        console.print("\n[bold blue]🔍 Analyzing diagram for prompt improvements...[/bold blue]\n")

        # Get refinement based on input type
        if run_id:
            console.print(f"Loading run: {run_id}")
            refinement = ctx.prompt_refiner.refine_from_run(run_id, feedback)
        elif reference_image and original_prompt:
            console.print(f"Analyzing image: {reference_image}")
            with open(original_prompt) as f:
                prompt_text = f.read()
            refinement = ctx.prompt_refiner.suggest_improvements(
                reference_image, prompt_text, user_feedback=feedback
            )
        else:
            console.print(
                "[red]Error: Provide either --run-id or both --reference-image and --original-prompt[/red]"
            )
            raise SystemExit(1)

        # Display summary
        console.print("[bold green]✓ Analysis complete![/bold green]\n")
        console.print(refinement.summary())

        # Display refined prompt
        console.print("\n[bold]Refined Prompt:[/bold]")
        console.print("─" * 80)
        console.print(refinement.refined_prompt)
        console.print("─" * 80)

        # Save as template if requested
        if output_template:
            refinement.save_template(output_template)
            console.print(f"\n[green]✓ Saved refined prompt to: {output_template}[/green]")

        console.print("\n[dim]Tip: Use the refined prompt for your next generation[/dim]")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise SystemExit(1)


@main.command()
@click.option(
    "--prompt-file",
    required=False,
    type=click.Path(exists=True, path_type=Path),
    help="Initial prompt file (.txt) - required unless using --resume or --list-sessions",
)
@click.option(
    "--resume",
    type=click.Path(exists=True, path_type=Path),
    help="Resume a saved session from path (session.json file or session directory)",
)
@click.option(
    "--list-sessions",
    is_flag=True,
    help="List available sessions to resume and exit",
)
@click.option(
    "--logo-dir",
    type=click.Path(exists=True, path_type=Path),
    help="Logo directory (default: from config)",
)
@click.option(
    "--max-iterations",
    default=0,
    type=int,
    help="Maximum refinement iterations (0 = no limit, default: 0)",
)
@click.option(
    "--target-score",
    default=10,
    type=int,
    help="Target score to stop (1-10, default: 10)",
)
@click.option(
    "--temperature",
    default=0.8,
    type=float,
    help="Generation temperature (default: 0.8)",
)
@click.option(
    "--top-p",
    default=0.95,
    type=float,
    help="Nucleus sampling: lower=focused, higher=diverse (default: 0.95)",
)
@click.option(
    "--top-k",
    default=50,
    type=int,
    help="Top-k sampling: limits token choices (default: 50, 0 to disable)",
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
    "--no-auto-analyze",
    is_flag=True,
    help="Disable automatic image analysis",
)
@click.option(
    "--auto-refine",
    is_flag=True,
    help="Automatically refine based on design principles (no manual feedback needed)",
)
@click.option(
    "--reference-image",
    type=click.Path(exists=True, path_type=Path),
    help="Reference image to match style and design (implies --auto-refine)",
)
@click.option(
    "--name",
    type=str,
    default=None,
    help="Session name for output directory (defaults to prompt filename)",
)
@click.option(
    "--folder",
    type=str,
    default=None,
    help="Output folder name (outputs/YYYY-MM-DD/chat-<folder>). Same as --name.",
)
@click.option(
    "--dspy-model",
    type=str,
    default=None,
    help="Databricks model for DSPy refinement (default: databricks-claude-opus-4-5)",
)
@click.option(
    "--persona",
    type=click.Choice(["architect", "executive", "developer", "auto"], case_sensitive=False),
    default="architect",
    help="LLM Judge evaluation persona: architect (default), executive/CTO, or developer",
)
@click.option(
    "--size",
    default="2K",
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
    "--num-variants",
    default=1,
    type=int,
    help="Number of image variants to generate per iteration (1-8, default: 1). "
    "Generates multiple images from the same prompt to deal with non-determinism.",
)
@click.option(
    "--selected-dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Folder to copy selected/best images to (default: outputs/selected). "
    "Use 's' or 'best' in chat to copy current or best image.",
)
@click.pass_obj
def chat(
    ctx: Context,
    prompt_file: Optional[Path],
    resume: Optional[Path],
    list_sessions: bool,
    logo_dir: Optional[Path],
    max_iterations: int,
    target_score: int,
    temperature: float,
    top_p: float,
    top_k: int,
    presence_penalty: float,
    frequency_penalty: float,
    no_auto_analyze: bool,
    auto_refine: bool,
    reference_image: Optional[Path],
    name: Optional[str],
    folder: Optional[str],
    dspy_model: Optional[str],
    persona: str,
    size: str,
    aspect_ratio: str,
    num_variants: int,
    selected_dir: Optional[Path],
):
    """Start interactive diagram refinement conversation.

    This command creates a generate -> evaluate -> feedback -> refine loop
    that iteratively improves your diagram through conversation.

    Sessions are automatically saved after each turn for crash recovery.
    Use --resume to continue a previous session.

    Examples:

        # Start with a prompt file
        bricksmith chat --prompt-file prompts/my_prompt.txt

        # Name the output folder (runs go to outputs/YYYY-MM-DD/chat-my-architecture)
        bricksmith chat --prompt-file prompt.txt --folder my-architecture

        # Customize iteration settings
        bricksmith chat --prompt-file prompt.txt --max-iterations 5 --target-score 4

        # Auto-refine based on design principles (fully autonomous)
        bricksmith chat --prompt-file prompt.txt --auto-refine --target-score 4

        # Match style from a reference image
        bricksmith chat --prompt-file prompt.txt --reference-image examples/good_diagram.png

        # Use executive/CTO persona for evaluation (strategic, cost-focused feedback)
        bricksmith chat --prompt-file prompt.txt --auto-refine --persona executive

        # Use developer persona for evaluation (implementation-focused feedback)
        bricksmith chat --prompt-file prompt.txt --auto-refine --persona developer

        # Generate 3 variants per iteration to pick the best (handles non-determinism)
        bricksmith chat --prompt-file prompt.txt --num-variants 3

        # Use 4K resolution with 1:1 aspect ratio
        bricksmith chat --prompt-file prompt.txt --size 4K --aspect-ratio 1:1

        # Use a specific Databricks model for refinement
        bricksmith chat --prompt-file prompt.txt --dspy-model databricks-claude-sonnet-4

        # List available sessions to resume
        bricksmith chat --list-sessions

        # Resume a crashed or interrupted session
        bricksmith chat --resume outputs/2026-02-11/chat-my-session

        # Resume and use a different logo kit (e.g. AGL logos)
        bricksmith chat --resume outputs/2026-02-14/chat-prompt-455771 --logo-dir logos/agl

    During the conversation, type 'help' or '?' to see all commands. Quick reference:

        • Text feedback: Refines the prompt based on your feedback
        • 'r' or 'retry': Retry same prompt with slight temp variation
        • 'r 0.5': Retry with specific temperature (0.5)
        • 'r t=0.5 p=0.9': Retry with specific temp and top_p
        • 'r creative': Retry with a preset (deterministic/conservative/balanced/creative/wild)
        • 'r size=4K ar=1:1': Retry with different resolution/aspect ratio
        • Image path: Use as style reference for comparison
        • 'done': Finish session
        • 'help' or '?': Show all available commands
    """
    from .models import EvaluationPersona

    try:
        # Handle --list-sessions flag
        if list_sessions:
            sessions = ConversationChatbot.find_sessions()
            if not sessions:
                console.print("[yellow]No saved chat sessions found in outputs/[/yellow]")
                raise SystemExit(0)

            console.print(f"\n[bold]Found {len(sessions)} saved chat session(s):[/bold]\n")

            from rich.table import Table

            table = Table(show_header=True)
            table.add_column("Session", style="cyan")
            table.add_column("Turns", style="magenta", justify="right")
            table.add_column("Status", style="yellow")
            table.add_column("Created", style="green")
            table.add_column("Last Saved", style="dim")
            table.add_column("Path", style="dim")

            for s in sessions:
                status_color = (
                    "green"
                    if s["status"] == "completed"
                    else "yellow" if s["status"] == "active" else "red"
                )
                table.add_row(
                    s["session_id"],
                    str(s["turns"]),
                    f"[{status_color}]{s['status']}[/{status_color}]",
                    s["created_at"][:19] if s["created_at"] else "",
                    s["last_saved"][:19] if s["last_saved"] else "",
                    str(s["path"]),
                )

            console.print(table)
            console.print("\n[bold]To resume a session:[/bold]")
            console.print("  bricksmith chat --resume <path>")
            raise SystemExit(0)

        # Handle --resume option
        if resume:
            console.print(f"[bold]Resuming session from {resume}...[/bold]")
            if logo_dir:
                console.print(f"[dim]Using logo kit: {logo_dir}[/dim]")
            chatbot, current_prompt = ConversationChatbot.resume_session(
                session_path=resume,
                config=ctx.config,
                dspy_model=dspy_model,
                logo_dir_override=logo_dir,
            )

            # Run conversation from where it left off
            session = chatbot.run_conversation(resume_prompt=current_prompt)

            # Final output
            console.print("\n[bold green]Session complete![/bold green]")
            console.print(f"  Status: {session.status.value}")
            console.print(f"  Iterations: {len(session.turns)}")

            best = session.get_best_turn()
            if best:
                console.print(f"  Best score: {best.score}")
                console.print(f"  Best image: {best.image_path}")
                console.print("\n[bold]To evaluate the best run:[/bold]")
                console.print(f"  bricksmith evaluate {best.run_id}")

            return

        # Require --prompt-file for new sessions
        if not prompt_file:
            raise click.ClickException(
                "--prompt-file is required when starting a new session. "
                "Use --resume to continue an existing session, or --list-sessions to find one."
            )

        # Reference image implies auto-refine
        if reference_image and not auto_refine:
            console.print("[dim]Reference image provided - enabling auto-refine mode[/dim]")
            auto_refine = True

        # Output folder name: --folder or --name or prompt filename
        session_name = folder or name
        if not session_name:
            session_name = prompt_file.stem  # filename without extension

        # Create conversation config
        conv_config = ConversationConfig(
            max_iterations=max_iterations,
            target_score=target_score,
            auto_analyze=not no_auto_analyze,
            auto_refine=auto_refine,
            reference_image=reference_image,
            session_name=session_name,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            logo_dir=logo_dir,
            evaluation_persona=EvaluationPersona(persona.lower()),
            image_size=size,
            aspect_ratio=aspect_ratio,
            num_variants=num_variants,
            selected_output_dir=selected_dir,
        )

        # Create chatbot
        chatbot = ConversationChatbot(
            config=ctx.config,
            conv_config=conv_config,
            dspy_model=dspy_model,
            image_generator=ctx.image_generator,
            gemini_client=ctx.gemini_client,
        )

        # Analyze reference image if provided
        if reference_image:
            chatbot.analyze_reference_image(reference_image)

        # Load prompt
        console.print(f"[bold]Loading prompt: {prompt_file.name}[/bold]")
        initial_prompt = prompt_file.read_text()

        # Start session
        chatbot.start_session(
            initial_prompt=initial_prompt,
        )

        # Run conversation
        session = chatbot.run_conversation()

        # Final output
        console.print("\n[bold green]Session complete![/bold green]")
        console.print(f"  Status: {session.status.value}")
        console.print(f"  Iterations: {len(session.turns)}")

        best = session.get_best_turn()
        if best:
            console.print(f"  Best score: {best.score}")
            console.print(f"  Best image: {best.image_path}")
            console.print("\n[bold]To evaluate the best run:[/bold]")
            console.print(f"  bricksmith evaluate {best.run_id}")

    except KeyboardInterrupt:
        # run_conversation() handles interrupts inside the loop.
        # This catches interrupts during setup (logo loading, session start, etc.).
        console.print("\n[yellow]Conversation interrupted.[/yellow]")
        # Try to save session if one was started
        try:
            session_file = chatbot._save_session()  # noqa: F821
            chatbot._show_resume_banner(session_file)
        except (NameError, UnboundLocalError, Exception):
            pass
        raise SystemExit(0)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise SystemExit(1)


@main.command()
@click.option(
    "--problem",
    type=str,
    help="Initial problem description (or enter interactively)",
)
@click.option(
    "--logo-dir",
    type=click.Path(exists=True, path_type=Path),
    help="Logo directory (default: from config)",
)
@click.option(
    "--context",
    type=click.Path(exists=True, path_type=Path),
    help="Custom context file with domain knowledge",
)
@click.option(
    "--reference-prompt",
    type=click.Path(exists=True, path_type=Path),
    help="Existing diagram prompt to use as reference for style and structure",
)
@click.option(
    "--reference-image",
    type=click.Path(exists=True, path_type=Path),
    multiple=True,
    help="Reference architecture diagram image(s) to analyze. Can be specified multiple times.",
)
@click.option(
    "--output-format",
    type=click.Choice(["prompt"]),
    default="prompt",
    help="Output format: prompt for generate-raw (default: prompt)",
)
@click.option(
    "--output-file",
    type=click.Path(path_type=Path),
    help="Save output to specific file",
)
@click.option(
    "--max-turns",
    default=20,
    type=int,
    help="Maximum conversation turns (default: 20)",
)
@click.option(
    "--dspy-model",
    type=str,
    default=None,
    help="Databricks model for DSPy (default: databricks-claude-opus-4-5)",
)
@click.option(
    "--name",
    type=str,
    default=None,
    help="Session name for output directory",
)
@click.option(
    "--mcp-enrich/--no-mcp-enrich",
    default=True,
    help="Enable MCP context enrichment from Glean, Slack, JIRA, Confluence (uses Claude Code's MCP servers)",
)
@click.option(
    "--mcp-sources",
    type=str,
    default="glean,confluence",
    help="Comma-separated MCP sources to query (default: glean,confluence). Options: glean,slack,jira,confluence",
)
@click.option(
    "--resume",
    type=click.Path(exists=True, path_type=Path),
    help="Resume a saved session from path (session.json file or session directory)",
)
@click.option(
    "--list-sessions",
    is_flag=True,
    help="List available sessions to resume and exit",
)
@click.pass_obj
def architect(
    ctx: Context,
    problem: Optional[str],
    logo_dir: Optional[Path],
    context: Optional[Path],
    reference_prompt: Optional[Path],
    reference_image: tuple[Path, ...],
    output_format: str,
    output_file: Optional[Path],
    max_turns: int,
    dspy_model: Optional[str],
    name: Optional[str],
    mcp_enrich: bool,
    mcp_sources: str,
    resume: Optional[Path],
    list_sessions: bool,
):
    """Start a collaborative architecture design conversation.

    Have a back-and-forth conversation with an AI solutions architect
    about a complex problem. The AI will ask clarifying questions,
    propose architecture solutions, and help refine the design.

    When ready, type 'output' to generate a diagram prompt suitable
    for generate-raw.

    Sessions are automatically saved after each turn for crash recovery.
    Use --resume to continue a previous session.

    Examples:

        # Start interactively
        bricksmith architect

        # Start with a problem description
        bricksmith architect --problem "Coles needs to migrate from Snowflake..."

        # With custom context file
        bricksmith architect \\
            --problem "Real-time analytics pipeline" \\
            --context prompts/context/customer_background.md

        # Use an existing prompt as reference for style/structure
        bricksmith architect \\
            --problem "Similar diagram for ANZ Bank" \\
            --reference-prompt prompts/coles_semantic_fragmentation.md

        # Specify logo directory and session name
        bricksmith architect \\
            --problem "Data lakehouse on Azure" \\
            --logo-dir logos/azure \\
            --name azure-lakehouse

        # Enable MCP enrichment (when invoked from Claude Code)
        bricksmith architect \\
            --problem "Coles Unity Catalog governance" \\
            --mcp-enrich \\
            --mcp-sources glean,slack,confluence

        # List available sessions to resume
        bricksmith architect --list-sessions

        # Resume a crashed or interrupted session
        bricksmith architect --resume outputs/2026-02-05/architect-my-session

    During the conversation, you can use these commands:

        • Natural text - continue discussing architecture
        • 'output' or 'generate' - generate the diagram prompt
        • 'status' - show current architecture state
        • 'done' - save and exit

    MCP Enrichment:

        When --mcp-enrich is enabled (default), the chatbot automatically searches
        internal knowledge sources (Glean, Slack, JIRA, Confluence) for relevant
        context based on customer names and Databricks concepts in your input.
        Uses Claude Code's MCP server configuration from ~/.claude/settings.json.
    """
    from .architect import ArchitectChatbot
    from .models import MCPEnrichmentConfig

    try:
        # Handle --list-sessions flag
        if list_sessions:
            sessions = ArchitectChatbot.find_sessions()
            if not sessions:
                console.print("[yellow]No saved sessions found in outputs/[/yellow]")
                raise SystemExit(0)

            table = Table(title="Saved Architect Sessions", show_header=True)
            table.add_column("Session ID", style="cyan")
            table.add_column("Problem", style="white", max_width=50)
            table.add_column("Turns", style="yellow", justify="right")
            table.add_column("Status", style="green")
            table.add_column("Path", style="dim")

            for sess in sessions[:20]:  # Limit to 20 most recent
                table.add_row(
                    sess["session_id"],
                    sess["problem"][:50] + "..." if len(sess["problem"]) > 50 else sess["problem"],
                    str(sess["turns"]),
                    sess["status"],
                    str(sess["path"].parent),
                )

            console.print(table)
            console.print("\n[bold]To resume a session:[/bold]")
            console.print("  bricksmith architect --resume <path>")
            raise SystemExit(0)

        # Handle --resume option
        if resume:
            console.print(f"[bold]Resuming session from {resume}...[/bold]")
            chatbot = ArchitectChatbot.resume_session(
                session_path=resume,
                config=ctx.config,
                dspy_model=dspy_model,
                mcp_callback=None,
            )

            # Run conversation from where we left off
            session = chatbot.run_conversation(skip_initial=True)

        else:
            # Start new session
            # Get problem description
            if not problem:
                console.print("[bold cyan]Describe your architecture problem:[/bold cyan]")
                console.print(
                    "[dim]What system do you need to design? What are the requirements?[/dim]\n"
                )
                problem = click.prompt("Problem", default="")

                if not problem.strip():
                    console.print("[red]Error: Problem description is required[/red]")
                    raise SystemExit(1)

            # Parse MCP sources
            mcp_source_list = [s.strip().lower() for s in mcp_sources.split(",") if s.strip()]

            # Create MCP enrichment config
            mcp_config = MCPEnrichmentConfig(
                enabled=mcp_enrich,
                sources=mcp_source_list,
            )

            # Create config
            arch_config = ArchitectConfig(
                max_turns=max_turns,
                context_file=context,
                reference_prompt=reference_prompt,
                reference_images=list(reference_image) if reference_image else None,
                output_format=output_format,
                session_name=name,
                logo_dir=logo_dir,
                mcp_enrichment=mcp_config,
            )

            # MCP enrichment now uses native client - no callback needed
            chatbot = ArchitectChatbot(
                config=ctx.config,
                arch_config=arch_config,
                dspy_model=dspy_model,
                mcp_callback=None,  # Native MCP client used when None
            )

            # Start session
            chatbot.start_session(
                initial_problem=problem,
                context_file=context,
                reference_prompt=reference_prompt,
                reference_images=list(reference_image) if reference_image else None,
            )

            # Run conversation
            session = chatbot.run_conversation()

        # Final output
        console.print("\n[bold green]Session complete![/bold green]")
        console.print(f"  Status: {session.status.value}")
        console.print(f"  Turns: {len(session.turns)}")
        console.print(f"  Components: {len(session.current_architecture.get('components', []))}")

        # Show next steps
        output_dir = (
            Path("outputs")
            / datetime.now().strftime("%Y-%m-%d")
            / f"architect-{session.session_id}"
        )
        if (output_dir / "prompt.txt").exists():
            console.print("\n[bold]Next steps:[/bold]")
            console.print("  # Use the generated prompt")
            console.print(
                f"  bricksmith generate-raw --prompt-file {output_dir}/prompt.txt --logo-dir logos/default"
            )
            console.print("\n  # Or continue refining with chat")
            console.print(f"  bricksmith chat --prompt-file {output_dir}/prompt.txt")

    except KeyboardInterrupt:
        console.print("\n[yellow]Session interrupted.[/yellow]")
        raise SystemExit(0)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise SystemExit(1)


@main.command()
@click.option(
    "--host",
    default="0.0.0.0",
    help="Host to bind to (default: 0.0.0.0)",
)
@click.option(
    "--port",
    default=8080,
    type=int,
    help="Port to bind to (default: 8080)",
)
@click.option(
    "--reload",
    is_flag=True,
    help="Enable auto-reload for development",
)
@click.option(
    "--dev",
    is_flag=True,
    help="Run in development mode (starts both backend and frontend dev servers)",
)
@click.pass_obj
def web(ctx: Context, host: str, port: int, reload: bool, dev: bool):
    """Start the web interface for architect workflows.

    Launches a FastAPI server that provides a web-based interface
    for collaborative architecture design.

    Examples:

        # Start the web server
        bricksmith web

        # Start with auto-reload for development
        bricksmith web --reload

        # Run on a different port
        bricksmith web --port 3000

        # Development mode (starts both backend and frontend)
        bricksmith web --dev

    The web interface provides:

        - Session management (create, list, delete)
        - Real-time chat with the AI architect
        - Live architecture visualization (Mermaid diagrams)
        - Output generation when design is complete
    """
    import os
    import socket
    import subprocess

    try:
        import uvicorn
    except ImportError:
        console.print("[red]Error: uvicorn not installed.[/red]")
        console.print("Install web dependencies with: uv pip install -e '.[web]'")
        raise SystemExit(1)

    def _port_in_use(check_port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return sock.connect_ex(("127.0.0.1", check_port)) == 0

    def _find_available_port(preferred: int, max_tries: int = 100) -> int:
        if not _port_in_use(preferred):
            return preferred
        for candidate in range(preferred + 1, preferred + max_tries + 1):
            if not _port_in_use(candidate):
                return candidate
        raise click.ClickException(
            f"No available port found near {preferred} (checked {max_tries} ports)."
        )

    if dev:
        backend_port = _find_available_port(port)
        frontend_port = _find_available_port(5173)
        if backend_port != port:
            console.print(
                f"[yellow]Port {port} is in use; using backend port {backend_port} instead.[/yellow]"
            )
        if frontend_port != 5173:
            console.print(
                f"[yellow]Port 5173 is in use; using frontend port {frontend_port} instead.[/yellow]"
            )

        # Development mode: start both backend and frontend
        console.print("[bold]Starting development servers...[/bold]")
        console.print(f"  Backend: http://localhost:{backend_port}")
        console.print(f"  Frontend: http://localhost:{frontend_port}")
        console.print("\n[dim]Press Ctrl+C to stop both servers[/dim]\n")

        from pathlib import Path

        frontend_dir = Path(__file__).parent.parent.parent / "frontend"

        if not frontend_dir.exists():
            console.print(f"[red]Frontend directory not found: {frontend_dir}[/red]")
            raise SystemExit(1)

        # Check if node_modules exists
        if not (frontend_dir / "node_modules").exists():
            console.print("[yellow]Installing frontend dependencies...[/yellow]")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)

        # Start frontend dev server in background, pointing proxy at chosen backend.
        frontend_env = os.environ.copy()
        frontend_env["VITE_BACKEND_URL"] = f"http://localhost:{backend_port}"
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev", "--", "--port", str(frontend_port)],
            cwd=frontend_dir,
            env=frontend_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        try:
            # Start backend with reload
            uvicorn.run(
                "bricksmith.web.main:app",
                host=host,
                port=backend_port,
                reload=True,
            )
        finally:
            # Stop frontend when backend stops
            frontend_process.terminate()
            frontend_process.wait()

    else:
        # Production mode: serve built frontend from FastAPI
        console.print("[bold]Starting Bricksmith Architect web server...[/bold]")
        console.print(f"  URL: http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
        console.print("\n[dim]Press Ctrl+C to stop[/dim]\n")

        uvicorn.run(
            "bricksmith.web.main:app",
            host=host,
            port=port,
            reload=reload,
        )


if __name__ == "__main__":
    main()
