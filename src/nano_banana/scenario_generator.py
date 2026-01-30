"""Generate diagram specifications from scenario descriptions.

This module uses Gemini to convert natural language scenario descriptions
into structured YAML diagram specifications.
"""

from pathlib import Path
from typing import Optional

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from .gemini_client import GeminiClient
from .logos import LogoKitHandler
from .models import DiagramSpec

console = Console()


class ScenarioGenerator:
    """Generates diagram specifications from scenario descriptions."""

    def __init__(self, logo_handler: Optional[LogoKitHandler] = None):
        """Initialize scenario generator.

        Args:
            logo_handler: Optional logo handler for available logos
        """
        self.client = GeminiClient()
        self.logo_handler = logo_handler

    def _build_generation_prompt(self, scenario: str, available_logos: list[str]) -> str:
        """Build prompt for generating diagram spec from scenario.

        Args:
            scenario: User's scenario description
            available_logos: List of available logo names

        Returns:
            Prompt for Gemini
        """
        logo_list = "\n".join([f"  - {logo}" for logo in available_logos])

        return f"""You are an expert at designing data and cloud architecture diagrams.

Given a scenario description, generate a YAML diagram specification that captures the architecture.

Available logos:
{logo_list}

Only use logos from the list above. Use `null` for components without logos.

**Scenario:**
{scenario}

**Instructions:**
1. Identify the key components in the architecture
2. Define logical connections between components
3. Use appropriate component types: "service", "storage", "external", "compute", "network"
4. Use connection styles: "solid" (data flow), "dashed" (governance/metadata), "dotted" (optional)
5. Set sensible constraints for layout

**Output a valid YAML diagram specification following this exact format:**

```yaml
name: "architecture-name"
description: "Brief description of the architecture"

components:
  - id: "component-id"
    label: "Display Name"
    type: "service"
    logo_name: "logo-name-or-null"

connections:
  - from_id: "source-id"
    to_id: "target-id"
    label: "Connection purpose"
    style: "solid"

constraints:
  layout: "left-to-right"
  background: "white"
  label_style: "sentence-case"
  show_grid: false
  spacing: "comfortable"
```

**Important:**
- Use snake-case for component IDs (e.g., "databricks-workspace", "s3-bucket")
- Use sentence case for labels (e.g., "Databricks Workspace", "S3 Bucket")
- Keep descriptions concise and clear
- Layout should be "left-to-right" or "top-to-bottom"
- Only output the YAML, no additional text or markdown code fences
"""

    def generate_spec_from_scenario(
        self,
        scenario: str,
        output_path: Optional[Path] = None,
    ) -> DiagramSpec:
        """Generate a diagram specification from a scenario description.

        Args:
            scenario: Natural language description of the architecture
            output_path: Optional path to save the generated spec

        Returns:
            DiagramSpec object

        Raises:
            ValueError: If generation fails or YAML is invalid
        """
        # Get available logos
        available_logos = ["null"]  # Always include null option
        if self.logo_handler:
            try:
                # Load logo kit to populate cache
                self.logo_handler.load_logo_kit()
                # Get list of loaded logo names
                available_logos.extend(sorted(self.logo_handler.list_loaded_logos()))
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load logos: {e}[/yellow]")
                console.print("[yellow]Proceeding with null logos only[/yellow]")

        console.print("\n[bold cyan]Generating diagram specification...[/bold cyan]")
        console.print(f"[dim]Available logos: {len(available_logos) - 1}[/dim]")

        # Generate spec using Gemini
        prompt = self._build_generation_prompt(scenario, available_logos)
        response = self.client.generate_text(prompt, temperature=0.4)

        # Clean up response (remove markdown code fences if present)
        yaml_content = response.strip()
        if yaml_content.startswith("```yaml"):
            yaml_content = yaml_content[7:]
        if yaml_content.startswith("```"):
            yaml_content = yaml_content[3:]
        if yaml_content.endswith("```"):
            yaml_content = yaml_content[:-3]
        yaml_content = yaml_content.strip()

        # Parse YAML
        try:
            spec_dict = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            console.print(f"[red]Error parsing generated YAML:[/red] {e}")
            console.print("[yellow]Generated content:[/yellow]")
            console.print(yaml_content)
            raise ValueError(f"Failed to parse generated YAML: {e}")

        # Validate structure
        if not isinstance(spec_dict, dict):
            raise ValueError("Generated YAML is not a dictionary")

        required_fields = ["name", "description", "components", "connections"]
        missing_fields = [f for f in required_fields if f not in spec_dict]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")

        # Create DiagramSpec object
        try:
            diagram_spec = DiagramSpec(**spec_dict)
        except Exception as e:
            console.print(f"[red]Error creating DiagramSpec:[/red] {e}")
            console.print("[yellow]Generated YAML:[/yellow]")
            syntax = Syntax(yaml_content, "yaml", theme="monokai", line_numbers=True)
            console.print(syntax)
            raise ValueError(f"Failed to create DiagramSpec: {e}")

        # Display generated spec
        console.print("\n[bold green]✓ Successfully generated diagram specification[/bold green]")
        console.print(Panel(
            Syntax(yaml_content, "yaml", theme="monokai", line_numbers=False),
            title="[bold]Generated Diagram Spec[/bold]",
            border_style="green"
        ))

        # Save if output path provided
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                yaml.dump(spec_dict, f, default_flow_style=False, sort_keys=False)
            console.print(f"\n[bold green]✓ Saved to:[/bold green] {output_path}")

        return diagram_spec

    def generate_and_create_diagram(
        self,
        scenario: str,
        template: str = "baseline",
        spec_output: Optional[Path] = None,
        run_name: Optional[str] = None,
    ) -> tuple[DiagramSpec, str]:
        """Generate spec from scenario and immediately create the diagram.

        Args:
            scenario: Natural language description
            template: Prompt template to use
            spec_output: Optional path to save the spec
            run_name: Optional run name for MLflow

        Returns:
            Tuple of (DiagramSpec, run_id)
        """
        # Import here to avoid circular dependency
        from .runner import DiagramRunner

        # Generate spec
        diagram_spec = self.generate_spec_from_scenario(scenario, spec_output)

        # Create runner and generate diagram
        console.print("\n[bold cyan]Generating diagram from specification...[/bold cyan]")
        runner = DiagramRunner()
        run_id = runner.generate_diagram(
            diagram_spec=diagram_spec,
            template_id=template,
            run_name=run_name or f"scenario-{diagram_spec.name}",
        )

        return diagram_spec, run_id
