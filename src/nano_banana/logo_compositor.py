"""Logo compositor for overlaying exact logos onto generated diagrams."""

from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger(__name__)


class LogoCompositor:
    """Composites exact logo images onto generated diagrams."""

    def __init__(self, logo_dir: Path):
        """Initialize compositor.

        Args:
            logo_dir: Directory containing logo files
        """
        self.logo_dir = logo_dir
        self._logo_cache: dict[str, Image.Image] = {}

    def load_logo(self, logo_name: str) -> Optional[Image.Image]:
        """Load a logo image file.

        Args:
            logo_name: Name of logo file (with or without extension)

        Returns:
            PIL Image or None if not found
        """
        if logo_name in self._logo_cache:
            return self._logo_cache[logo_name]

        # Try different extensions
        extensions = ['.jpg', '.jpeg', '.png', '.svg']

        for ext in extensions:
            # Try exact match
            logo_path = self.logo_dir / f"{logo_name}{ext}"
            if logo_path.exists():
                try:
                    img = Image.open(logo_path).convert('RGBA')
                    self._logo_cache[logo_name] = img
                    return img
                except Exception as e:
                    logger.warning(f"Failed to load {logo_path}: {e}")
                    continue

            # Try without extension if name already has one
            if '.' in logo_name:
                logo_path = self.logo_dir / logo_name
                if logo_path.exists():
                    try:
                        img = Image.open(logo_path).convert('RGBA')
                        self._logo_cache[logo_name] = img
                        return img
                    except Exception as e:
                        logger.warning(f"Failed to load {logo_path}: {e}")
                        continue

        logger.error(f"Logo not found: {logo_name}")
        return None

    def composite_logo(
        self,
        base_image: Image.Image,
        logo_name: str,
        position: Tuple[int, int],
        max_size: Optional[Tuple[int, int]] = None,
        scale: float = 1.0,
    ) -> Image.Image:
        """Overlay a logo onto the base image.

        Args:
            base_image: Base diagram image
            logo_name: Name of logo to overlay
            position: (x, y) position for logo center
            max_size: Optional (width, height) maximum size
            scale: Scale factor (1.0 = original size)

        Returns:
            Image with logo composited
        """
        logo = self.load_logo(logo_name)
        if logo is None:
            logger.warning(f"Skipping logo: {logo_name}")
            return base_image

        # Create a copy to avoid modifying original
        result = base_image.copy()

        # Scale logo
        if scale != 1.0 or max_size is not None:
            width, height = logo.size

            if max_size:
                # Fit within max_size while preserving aspect ratio
                aspect = width / height
                max_w, max_h = max_size

                if width > max_w:
                    width = max_w
                    height = int(width / aspect)

                if height > max_h:
                    height = max_h
                    width = int(height * aspect)

            # Apply scale
            width = int(width * scale)
            height = int(height * scale)

            logo = logo.resize((width, height), Image.Resampling.LANCZOS)

        # Calculate top-left position from center
        logo_width, logo_height = logo.size
        x = position[0] - logo_width // 2
        y = position[1] - logo_height // 2

        # Composite logo
        if logo.mode == 'RGBA':
            result.paste(logo, (x, y), logo)  # Use alpha channel as mask
        else:
            result.paste(logo, (x, y))

        return result

    def composite_diagram_logos(
        self,
        base_image_path: Path,
        output_path: Path,
        logo_positions: dict[str, dict],
    ) -> Path:
        """Composite multiple logos onto a diagram.

        Args:
            base_image_path: Path to generated diagram
            output_path: Path to save composited diagram
            logo_positions: Dictionary mapping logo names to position info:
                {
                    'kaluza_logo_black': {
                        'position': (x, y),  # center position in pixels
                        'max_size': (width, height),  # optional max size
                        'scale': 1.0,  # optional scale factor
                    },
                    ...
                }

        Returns:
            Path to composited image
        """
        # Load base image
        base = Image.open(base_image_path).convert('RGBA')

        # Composite each logo
        for logo_name, config in logo_positions.items():
            position = config['position']
            max_size = config.get('max_size')
            scale = config.get('scale', 1.0)

            logger.info(f"Compositing {logo_name} at {position}")
            base = self.composite_logo(base, logo_name, position, max_size, scale)

        # Save result
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert back to RGB for JPEG
        if output_path.suffix.lower() in ['.jpg', '.jpeg']:
            base = base.convert('RGB')

        base.save(output_path, quality=95)
        logger.info(f"Saved composited diagram: {output_path}")

        return output_path


def find_logo_positions_interactive(
    image_path: Path,
) -> dict[str, dict]:
    """Helper to interactively find logo positions.

    Opens the image and prints click coordinates to help determine positions.

    Args:
        image_path: Path to diagram image

    Returns:
        Dictionary of logo positions (empty, for manual editing)
    """
    from PIL import Image
    import matplotlib.pyplot as plt

    img = Image.open(image_path)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(img)
    ax.set_title("Click to find logo positions (coordinates will be printed)")

    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            x, y = int(event.xdata), int(event.ydata)
            print(f"Position: ({x}, {y})")
            ax.plot(x, y, 'ro', markersize=10)
            fig.canvas.draw()

    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    return {}
