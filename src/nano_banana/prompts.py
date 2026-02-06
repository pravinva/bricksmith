"""Prompt building for Nano Banana Pro."""

from typing import Optional

from .logos import LogoKitHandler
from .models import LogoInfo


class PromptBuilder:
    """Builds prompts with logo constraints for architecture diagram generation."""

    def __init__(self, logo_handler: Optional[LogoKitHandler] = None):
        """Initialize prompt builder.

        Args:
            logo_handler: Optional LogoKitHandler for accessing logo hints
        """
        self.logo_handler = logo_handler

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

