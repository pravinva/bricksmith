"""Logo kit handling for Nano Banana Pro."""

import base64
import hashlib
import mimetypes
from pathlib import Path
from typing import Any, Optional

from PIL import Image

from .config import LogoKitConfig
from .models import LogoInfo


# Logo name to description mapping (for prompt injection)
DEFAULT_LOGO_DESCRIPTIONS = {
    "databricks": "red/orange stacked bars icon with 'databricks' text",
    "databricks-logo": "red/orange stacked bars icon with 'databricks' text",
    "delta-lake": "teal triangle icon",
    "delta-lake-logo": "teal triangle icon",
    "uc": "pink squares, yellow triangles, navy hexagon in center - USE THIS for Unity Catalog",
    "uc-logo": "pink squares, yellow triangles, navy hexagon in center - USE THIS for Unity Catalog",
    "unity-catalog": "pink squares, yellow triangles, navy hexagon in center - USE THIS for Unity Catalog",
    "unity-catalog-logo": "pink squares, yellow triangles, navy hexagon in center - USE THIS for Unity Catalog",
    "00-unity-catalog-logo": "pink squares, yellow triangles, navy hexagon in center - USE THIS for Unity Catalog",
    "00-governance-catalog-logo": "pink squares, yellow triangles, navy hexagon in center - USE THIS for Unity Catalog/Governance",
    "governance-catalog": "pink squares, yellow triangles, navy hexagon in center - USE THIS for Unity Catalog/Governance",
    "kaluza": "three BLACK hexagons in triangular pattern",
    "kaluza_logo_black": "three BLACK hexagons in triangular pattern",
    "kaluza-logo": "three BLACK hexagons in triangular pattern",
    "agl": "AGL Energy logo - cyan/teal rays with 'agl' text",
    "agl-logo": "AGL Energy logo - cyan/teal rays with 'agl' text",
    "agl_energy": "AGL Energy logo - cyan/teal rays with 'agl' text",
    "aws": "grey 'AWS' text with orange smile underneath",
    "aws-logo": "grey 'AWS' text with orange smile underneath",
    "azure": "blue Microsoft Azure symbol",
    "azure-logo": "blue Microsoft Azure symbol",
}


class LogoKitHandler:
    """Handles logo loading, validation, hashing, and conversion."""

    def __init__(self, config: LogoKitConfig):
        """Initialize logo kit handler.

        Args:
            config: Logo kit configuration
        """
        self.config = config
        self._logo_cache: dict[str, LogoInfo] = {}

    def load_logo_kit(self, logo_dir: Optional[Path] = None) -> list[LogoInfo]:
        """Load all logos from directory.

        Args:
            logo_dir: Optional logo directory (uses config default if not provided)

        Returns:
            List of LogoInfo objects

        Raises:
            FileNotFoundError: If logo directory doesn't exist
            ValueError: If no valid logos found
        """
        if logo_dir is None:
            logo_dir = self.config.logo_dir

        if not logo_dir.exists():
            raise FileNotFoundError(f"Logo directory not found: {logo_dir}")

        logos = []
        for file_path in sorted(logo_dir.iterdir()):
            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in self.config.allowed_extensions:
                continue

            try:
                logo = self._load_single_logo(file_path)
                logos.append(logo)
                self._logo_cache[logo.name] = logo
            except Exception as e:
                print(f"Warning: Failed to load {file_path}: {e}")
                continue

        if not logos:
            raise ValueError(f"No valid logos found in {logo_dir}")

        return logos

    def _load_single_logo(self, file_path: Path) -> LogoInfo:
        """Load a single logo file.

        Args:
            file_path: Path to logo file

        Returns:
            LogoInfo object

        Raises:
            ValueError: If logo is invalid
        """
        # Validate logo
        self.validate_logo(file_path)

        # Extract name from filename (without extension)
        # Remove common prefixes like "00-" that are used for sorting
        name = file_path.stem.lower()
        if name.startswith("00-"):
            name = name[3:]  # Remove "00-" prefix

        # Get description
        description = self._get_logo_description(name)

        # Compute hash
        sha256_hash = self.compute_hash(file_path)

        # Get MIME type
        content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

        # Get size
        size_bytes = file_path.stat().st_size

        return LogoInfo(
            name=name,
            description=description,
            file_path=file_path,
            sha256_hash=sha256_hash,
            content_type=content_type,
            size_bytes=size_bytes,
        )

    def _get_logo_description(self, name: str) -> str:
        """Get description for a logo name.

        Args:
            name: Logo name

        Returns:
            Description string
        """
        # Try exact match
        if name in DEFAULT_LOGO_DESCRIPTIONS:
            return DEFAULT_LOGO_DESCRIPTIONS[name]

        # Try partial match
        for key, desc in DEFAULT_LOGO_DESCRIPTIONS.items():
            if key in name or name in key:
                return desc

        # Default generic description
        return f"{name} logo"

    def get_logo(self, name: str) -> LogoInfo:
        """Get a specific logo by name.

        Args:
            name: Logo name

        Returns:
            LogoInfo object

        Raises:
            KeyError: If logo not found in cache
        """
        name_lower = name.lower()
        if name_lower not in self._logo_cache:
            raise KeyError(f"Logo '{name}' not found in cache. Load logo kit first.")
        return self._logo_cache[name_lower]

    def compute_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of file.

        Args:
            file_path: Path to file

        Returns:
            Hexadecimal hash string
        """
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def to_image_part(self, logo: LogoInfo) -> dict[str, Any]:
        """Convert logo to Vertex AI image part format.

        Args:
            logo: LogoInfo object

        Returns:
            Dictionary in google-genai image part format with raw bytes
        """
        # Read file as raw bytes (not base64 encoded)
        with open(logo.file_path, "rb") as f:
            image_bytes = f.read()

        # Return in google-genai format (raw bytes, not base64)
        return {
            "mime_type": logo.content_type,
            "data": image_bytes,
        }

    def validate_logo(self, file_path: Path) -> None:
        """Validate logo file.

        Args:
            file_path: Path to logo file

        Raises:
            ValueError: If logo is invalid
        """
        if not file_path.exists():
            raise ValueError(f"Logo file not found: {file_path}")

        # Check file size
        size_mb = file_path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_logo_size_mb:
            raise ValueError(
                f"Logo {file_path.name} is too large: "
                f"{size_mb:.2f}MB > {self.config.max_logo_size_mb}MB"
            )

        # Check extension
        if file_path.suffix.lower() not in self.config.allowed_extensions:
            raise ValueError(
                f"Logo {file_path.name} has invalid extension. "
                f"Allowed: {self.config.allowed_extensions}"
            )

        # Try to open as image
        try:
            with Image.open(file_path) as img:
                img.verify()
        except Exception as e:
            raise ValueError(f"Logo {file_path.name} is not a valid image: {e}")

    def list_loaded_logos(self) -> list[str]:
        """Get list of loaded logo names.

        Returns:
            List of logo names
        """
        return sorted(self._logo_cache.keys())

    def clear_cache(self) -> None:
        """Clear logo cache."""
        self._logo_cache.clear()
