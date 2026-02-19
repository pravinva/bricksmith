"""Abstract image generation interface and factory for multi-provider support.

All image generation in the app goes through the ImageGenerator protocol so we can
swap Gemini for OpenAI (gpt-image-1.5) or other backends via config/CLI.
"""

from typing import Any, Optional, Protocol


class ImageGenerator(Protocol):
    """Protocol for diagram image generation (Gemini, OpenAI, etc.)."""

    def generate_image(
        self,
        prompt: str,
        logo_parts: list[dict[str, Any]],
        temperature: float = 0.8,
        top_p: float = 0.95,
        top_k: Optional[int] = 50,
        max_output_tokens: int = 32768,
        presence_penalty: float = 0.1,
        frequency_penalty: float = 0.1,
        aspect_ratio: str = "16:9",
        image_size: str = "2K",
        system_instruction: Optional[str] = None,
    ) -> tuple[bytes, str, dict[str, Any]]:
        """Generate a diagram image from prompt and optional logo images.

        Returns:
            Tuple of (image_bytes, response_text, metadata).
        """
        ...
