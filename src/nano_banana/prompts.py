"""Prompt template management and building for Nano Banana Pro."""

import re
from pathlib import Path
from typing import Any, Optional

from .models import DiagramSpec, LogoInfo, PromptTemplate


class PromptBuilder:
    """Builds prompts from templates with variable substitution."""

    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize prompt builder.

        Args:
            template_dir: Directory containing prompt templates
        """
        self.template_dir = template_dir or Path("examples/prompt_templates")
        self._templates: dict[str, PromptTemplate] = {}

    def load_template(self, template_id: str) -> PromptTemplate:
        """Load a prompt template by ID.

        Args:
            template_id: Template identifier (filename without extension)

        Returns:
            PromptTemplate object

        Raises:
            FileNotFoundError: If template file not found
        """
        # Check cache first
        if template_id in self._templates:
            return self._templates[template_id]

        # Try to load from file
        template_path = self.template_dir / f"{template_id}.txt"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        template = PromptTemplate.from_file(template_path, template_id)
        self._templates[template_id] = template
        return template

    def build_prompt(
        self,
        template: PromptTemplate,
        diagram_spec: DiagramSpec,
        logo_kit: list[LogoInfo],
        variables: Optional[dict[str, Any]] = None,
    ) -> str:
        """Build complete prompt with all sections.

        Logo constraints are ALWAYS included in the final prompt, either via
        template placeholders or automatically prepended if missing.

        Args:
            template: Prompt template
            diagram_spec: Diagram specification
            logo_kit: List of available logos
            variables: Optional additional variables for substitution

        Returns:
            Complete prompt text with logo constraints guaranteed
        """
        # Start with template
        prompt = template.template

        # Build sections (pass logo_kit to diagram section for index mapping)
        logo_section = self._build_logo_section(logo_kit)
        diagram_section = self._build_diagram_section(diagram_spec, logo_kit)

        # Prepare variables for substitution
        all_variables = {
            "logo_section": logo_section,
            "diagram_section": diagram_section,
            **(template.variables or {}),
            **(variables or {}),
        }

        # Substitute variables
        prompt = self.substitute_variables(prompt, all_variables)

        # CRITICAL: Ensure logo section is ALWAYS included
        # If template didn't include {logo_section}, prepend it
        if "{logo_section}" not in template.template and logo_section not in prompt:
            prompt = f"{logo_section}\n\n{prompt}"

        # CRITICAL: Ensure diagram section is ALWAYS included
        # If template didn't include {diagram_section}, append it
        if "{diagram_section}" not in template.template and "Diagram:" not in prompt:
            prompt = f"{prompt}\n\n{diagram_section}"

        # CRITICAL: Ensure logo constraints are ALWAYS present
        # Double-check the critical constraint text appears
        critical_constraints = [
            "Reuse uploaded logos EXACTLY",
            "Scale all logos uniformly",
            "NO filenames"
        ]

        has_constraints = all(
            constraint.lower() in prompt.lower()
            for constraint in critical_constraints
        )

        if not has_constraints:
            # Force-inject constraints at the top
            constraint_block = """
CRITICAL LOGO REQUIREMENTS (MANDATORY):
- Reuse uploaded logos EXACTLY as provided
- Scale all logos uniformly
- NO filenames or file labels may appear in the output

"""
            prompt = constraint_block + prompt

        return prompt

    def _build_logo_section(self, logo_kit: list[LogoInfo]) -> str:
        """Build the logo kit reference section.

        This section lists all available logos with descriptions and includes
        the critical constraint: "Reuse uploaded logos EXACTLY. Scale uniformly. No filenames."

        Args:
            logo_kit: List of logos

        Returns:
            Logo section text
        """
        lines = ["LOGO KIT (uploaded as image attachments):"]
        lines.append("Use these EXACT logos - do NOT recreate or substitute.")
        lines.append("Do NOT add numbered labels or circles to the diagram.")
        lines.append("")

        for logo in logo_kit:
            logo_name = logo.name.replace('-', ' ').replace('_', ' ').title()
            description = logo.description

            if description and description != f"{logo.name} logo":
                lines.append(f"- {logo_name}: {description}")
            else:
                lines.append(f"- {logo_name}")
            
        lines.append("")
        lines.append("LOGO RULES:")
        lines.append("- Use EXACT uploaded images - do NOT redraw or recreate")
        lines.append("- Only use logos mentioned in the prompt")
        lines.append("- Do NOT add numbered circles or labels to logos")
        lines.append("- Scale logos uniformly")
        lines.append("- NO filenames in output")

        return "\n".join(lines)

    def _build_diagram_section(
        self,
        diagram_spec: DiagramSpec,
        logo_kit: Optional[list[LogoInfo]] = None
    ) -> str:
        """Build the diagram specification section.

        Args:
            diagram_spec: Diagram specification
            logo_kit: Optional logo kit for index-based references

        Returns:
            Diagram section text
        """
        # Create logo name to index mapping if logo_kit provided
        logo_index_map = {}
        if logo_kit:
            for idx, logo in enumerate(logo_kit, 1):
                logo_name = logo.name.lower()
                # Map exact name
                logo_index_map[logo_name] = idx
                # Map with/without underscores and hyphens
                logo_index_map[logo_name.replace('_', '-')] = idx
                logo_index_map[logo_name.replace('-', '_')] = idx
                # Map base name without -logo/-logo suffix
                base_name = logo_name.replace('-logo', '').replace('_logo', '').replace('.svg', '')
                logo_index_map[base_name] = idx
                logo_index_map[base_name.replace('_', '-')] = idx
                logo_index_map[base_name.replace('-', '_')] = idx
                # Map first part before underscore/hyphen (e.g., "kaluza" from "kaluza_logo_black")
                first_part = logo_name.split('_')[0].split('-')[0]
                if first_part and first_part not in logo_index_map:
                    logo_index_map[first_part] = idx

        lines = [f"Diagram: {diagram_spec.name}"]
        lines.append(f"Description: {diagram_spec.description}")
        lines.append("")

        # Components
        lines.append("Components:")
        for comp in diagram_spec.components:
            comp_line = f"- {comp.id}: {comp.label} (type: {comp.type})"
            if comp.logo_name:
                logo_ref = f" [use {comp.logo_name} logo"
                # Add index if available
                if logo_kit and comp.logo_name in logo_index_map:
                    idx = logo_index_map[comp.logo_name]
                    logo_ref += f" = Image {idx}"
                logo_ref += " - USE EXACT UPLOADED IMAGE]"
                comp_line += logo_ref
            lines.append(comp_line)

        lines.append("")

        # Connections
        lines.append("Connections:")
        for conn in diagram_spec.connections:
            conn_line = f"- {conn.from_id} → {conn.to_id}"
            if conn.label:
                conn_line += f' "{conn.label}"'
            if conn.style != "solid":
                conn_line += f" ({conn.style})"
            lines.append(conn_line)

        lines.append("")

        # Constraints
        lines.append("Layout Constraints:")
        lines.append(f"- Layout: {diagram_spec.constraints.layout}")
        lines.append(f"- Background: {diagram_spec.constraints.background}")
        lines.append(f"- Label style: {diagram_spec.constraints.label_style}")
        lines.append(f"- Spacing: {diagram_spec.constraints.spacing}")
        if diagram_spec.constraints.show_grid:
            lines.append("- Show grid lines")

        return "\n".join(lines)

    def substitute_variables(self, template: str, variables: dict[str, Any]) -> str:
        """Replace {variable} placeholders with values.

        Args:
            template: Template string with {variable} placeholders
            variables: Dictionary of variable names to values

        Returns:
            String with variables substituted
        """
        result = template

        # Find all {variable} patterns
        pattern = re.compile(r"\{(\w+)\}")

        def replacer(match: re.Match) -> str:
            var_name = match.group(1)
            if var_name in variables:
                return str(variables[var_name])
            # Leave unmatched variables as-is
            return match.group(0)

        result = pattern.sub(replacer, result)
        return result

    def list_templates(self) -> list[str]:
        """List available template IDs.

        Returns:
            List of template identifiers
        """
        if not self.template_dir.exists():
            return []

        templates = []
        for path in self.template_dir.glob("*.txt"):
            templates.append(path.stem)

        return sorted(templates)

    def validate_template(self, template: PromptTemplate) -> list[str]:
        """Validate that a template has recommended placeholders.

        Note: Logo constraints are automatically injected if missing,
        but templates SHOULD include {logo_section} for best results.

        Args:
            template: Template to validate

        Returns:
            List of missing recommended placeholders (empty if valid)
        """
        recommended = ["logo_section", "diagram_section"]
        missing = []

        for req in recommended:
            if f"{{{req}}}" not in template.template:
                missing.append(req)

        return missing

    def validate_final_prompt(self, prompt: str) -> dict[str, bool]:
        """Validate that a final prompt has all critical elements.

        Args:
            prompt: Final prompt text to validate

        Returns:
            Dictionary with validation results
        """
        return {
            "has_logo_section": "logo kit provided" in prompt.lower() or "logo" in prompt.lower(),
            "has_reuse_constraint": "reuse" in prompt.lower() and "exactly" in prompt.lower(),
            "has_scale_constraint": "scale" in prompt.lower() and "uniformly" in prompt.lower(),
            "has_no_filename_constraint": "no filename" in prompt.lower() or "no file" in prompt.lower(),
            "has_diagram_info": "diagram:" in prompt.lower() or "components:" in prompt.lower(),
        }
