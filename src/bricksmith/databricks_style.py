"""Databricks brand style guide for diagram generation.

This module provides official Databricks brand colors, typography, and styling
guidelines to ensure generated diagrams match corporate brand standards.
"""

# Typography
FONT_FAMILY = "DM Sans"
FONT_MONO = "DM Mono"
TYPE_SCALE_PX = [12, 16, 20, 24, 32, 40, 56, 64]

# Grid
GRID_COLUMNS = 12

# Primary Brand Colors
COLORS = {
    # Primary
    "primary_orange": "#FF3621",
    "primary_orange_alt": "#FF5F46",
    "navy": "#1B3139",

    # Neutrals
    "warm_gray": "#A0ACBE",
    "gray_light": "#C4CCD6",
    "white": "#FFFFFF",

    # Accent Colors
    "yellow": "#FCBA33",
    "teal": "#42BA91",
    "amber": "#FFAB00",
    "green": "#00875C",
    "green_bright": "#00A972",

    # Deep/Dark Accents
    "red_deep": "#BD2B26",
    "gold_bronze": "#BD802B",
    "maroon": "#730D21",
    "crimson": "#98102A",
    "blue_slate": "#143D4A",
    "blue_steel": "#1B5162",
    "burgundy_dark": "#4A121A",
    "brown_olive": "#7D5319",
    "green_forest": "#095A35",

    # Light/Pastel Accents
    "pink_mauve": "#D69EA8",
    "rose": "#BF7080",
    "mint": "#9ED6C4",
    "seafoam": "#70C4AB",
    "butter": "#FFDB96",
    "gold": "#FFCC66",
    "blush_light": "#FABFBA",
    "coral_light": "#FF9E94",
    "blue_gray": "#618794",
}

# Background defaults
BACKGROUND_DEFAULT = COLORS["warm_gray"]
BACKGROUND_WHITE = COLORS["white"]

# Chart styling
CHART_BACKGROUND = "none"
CHART_BORDER = "none"


def get_style_prompt() -> str:
    """Generate a style instruction block for Databricks-branded diagrams.

    Returns:
        A formatted string with Databricks brand guidelines for the model.
    """
    return f"""
=== DATABRICKS BRAND STYLE GUIDE ===

TYPOGRAPHY:
- Primary font: {FONT_FAMILY} (clean, modern sans-serif)
- Monospace font: {FONT_MONO} (for code/technical text)
- Use clear hierarchy with sizes: {', '.join(str(s) + 'px' for s in TYPE_SCALE_PX)}

COLOR PALETTE (use these exact hex values):
- Primary Orange: {COLORS['primary_orange']} (main accent, CTAs, highlights)
- Primary Orange Alt: {COLORS['primary_orange_alt']} (hover states, secondary accent)
- Navy: {COLORS['navy']} (headers, dark backgrounds, text)
- Warm Gray: {COLORS['warm_gray']} (backgrounds, borders)
- Light Gray: {COLORS['gray_light']} (subtle backgrounds)
- White: {COLORS['white']} (backgrounds, contrast)

ACCENT COLORS (for data visualization and highlights):
- Teal: {COLORS['teal']} (success, positive)
- Green: {COLORS['green']} (success states)
- Yellow: {COLORS['yellow']} (warnings, attention)
- Amber: {COLORS['amber']} (warnings)
- Blue Slate: {COLORS['blue_slate']} (secondary headers)
- Blue Steel: {COLORS['blue_steel']} (borders, accents)

VISUAL STYLE:
- Clean, professional, modern aesthetic
- White or light gray backgrounds preferred
- Use orange sparingly for emphasis and key elements
- Navy for text and structural elements
- Flat 2D vector graphics, no 3D effects
- Clear visual hierarchy with consistent spacing
- 12-column grid alignment when possible

DO NOT USE:
- Bright saturated colors outside the palette
- Gradients (unless subtle)
- Drop shadows (keep minimal if used)
- Decorative elements not in the prompt
- NUMBERED CIRCLES or step indicators (1, 2, 3 in circles) - NEVER add these unless explicitly requested
- Numbered labels or annotations on logos
- Callout bubbles with numbers
- Any numeric sequence markers
"""


def get_color(name: str) -> str:
    """Get a Databricks brand color by name.

    Args:
        name: Color name (e.g., 'primary_orange', 'navy')

    Returns:
        Hex color code

    Raises:
        KeyError: If color name not found
    """
    return COLORS[name]
