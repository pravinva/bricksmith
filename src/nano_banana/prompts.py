"""Prompt template management and building for Nano Banana Pro."""

import re
from pathlib import Path
from typing import Any, Optional

from .logos import LogoKitHandler
from .models import LogoInfo, PromptTemplate


class PromptBuilder:
    """Builds prompts from templates with variable substitution."""

    def __init__(self, template_dir: Optional[Path] = None, logo_handler: Optional[LogoKitHandler] = None):
        """Initialize prompt builder.

        Args:
            template_dir: Directory containing prompt templates
            logo_handler: Optional LogoKitHandler for accessing logo hints
        """
        self.template_dir = template_dir or Path("prompts/prompt_templates")
        self._templates: dict[str, PromptTemplate] = {}
        self.logo_handler = logo_handler

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

    def _build_logo_hints_section(self, logo_kit: list[LogoInfo]) -> str:
        """Build logo-specific hints section for logos that need special instructions.

        Args:
            logo_kit: List of logos

        Returns:
            Formatted hints text (empty if no hints apply)
        """
        if not self.logo_handler:
            return ""

        hints_blocks = []
        
        for logo in logo_kit:
            hint = self.logo_handler.get_logo_hint(logo.name)
            if hint:
                formatted_hint = self.logo_handler.format_logo_hint(hint)
                hints_blocks.append(formatted_hint)
        
        return "\n".join(hints_blocks) if hints_blocks else ""

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
