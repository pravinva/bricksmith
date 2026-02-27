"""Databricks brand style guide for diagram generation."""

# Typography
FONT_FAMILY = "DM Sans"
FONT_MONO = "DM Mono"
TYPE_SCALE_PX = [12, 16, 20, 24, 32, 40, 56, 64]

# Grid
GRID_COLUMNS = 12

# Core Brand Colors
COLORS = {
    # Core
    "primary_orange": "#FF3621",
    "cyan": "#00A8E1",
    "navy": "#1B3139",

    # Neutrals
    "warm_gray": "#A0ACBE",
    "gray_light": "#C4CCD6",
    "white": "#FFFFFF",
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
- Databricks Lava: {COLORS['primary_orange']} (primary emphasis)
- Databricks Cyan: {COLORS['cyan']} (flows, links, secondary emphasis)
- Databricks Navy: {COLORS['navy']} (titles, structure, primary text)
- Light Gray: {COLORS['gray_light']} (subtle borders and soft container fills)
- White: {COLORS['white']} (background)

VISUAL STYLE:
- Clean, professional, modern aesthetic
- White background with subtle grouped containers
- Use Lava sparingly for emphasis and key platform elements
- Use Cyan for flow arrows and accents
- Use Navy for text and structural elements
- Flat 2D vector graphics, no 3D effects
- Clear visual hierarchy with consistent spacing
- 12-column grid alignment when possible
- Treat this section as hidden guidance only; do NOT render any of this guide text.
- Never render color names or hex codes as visible labels in the diagram.

DO NOT USE:
- Any saturated colors outside the core palette
- Gradients (unless subtle)
- Drop shadows (keep minimal if used)
- Decorative elements not in the prompt
- NUMBERED CIRCLES or step indicators (1, 2, 3 in circles) - NEVER add these unless explicitly requested
- Numbered labels or annotations on logos
- Callout bubbles with numbers
- Any numeric sequence markers
- Any style-guide words or palette labels in diagram text (e.g., "Databricks Navy", "Databricks Cyan", "Databricks Lava")
- Any hex color values like #1B3139, #00A8E1, #FF3621 shown as visible text
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
