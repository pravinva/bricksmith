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

        # Filename suffixes that are conventions, not part of the logo identity.
        # These must never leak into the prompt or Gemini will render them as text.
        _FILENAME_SUFFIXES = [
            "-full", "-logo", "-solo", "-notext", "-icon",
            "-wordmark", "-black", "-final", "-white",
        ]

        for logo in logo_kit:
            # Strip filename-convention suffixes before building the display name.
            # Loop to handle chained suffixes (e.g. "mlflow-logo-final-black").
            clean_name = logo.name
            changed = True
            while changed:
                changed = False
                for suffix in _FILENAME_SUFFIXES:
                    if clean_name.endswith(suffix):
                        clean_name = clean_name[: -len(suffix)]
                        changed = True
                        break

            logo_name = clean_name.replace('-', ' ').replace('_', ' ').title()
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

