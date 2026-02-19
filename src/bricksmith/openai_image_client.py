"""OpenAI Image API client for gpt-image-1.5 (and gpt-image-1) diagram generation.

Uses images.generate when there are no logos, and images.edit when logo_parts
are provided (reference images + prompt). Analysis (e.g. LLM Judge) remains on
Gemini; this module is for image generation only.
"""

import base64
import os
from io import BytesIO
from typing import Any, Optional

from openai import OpenAI


# Map aspect ratio to OpenAI size (landscape 1536x1024, portrait 1024x1536, square 1024x1024)
ASPECT_RATIO_TO_SIZE: dict[str, str] = {
    "1:1": "1024x1024",
    "4:3": "1536x1024",
    "16:9": "1536x1024",
    "21:9": "1536x1024",
    "9:16": "1024x1536",
    "3:4": "1024x1536",
}

# Map our image_size (1K, 2K, 4K) to OpenAI quality
IMAGE_SIZE_TO_QUALITY: dict[str, str] = {
    "1K": "low",
    "2K": "medium",
    "4K": "high",
}


class OpenAIImageClient:
    """OpenAI Images API client for gpt-image-1.5 / gpt-image-1.

    Implements the same generate_image contract as GeminiClient so callers
    can switch provider via config. Uses images.generate (text-only) when
    logo_parts is empty, and images.edit (image + prompt) when logos are provided.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-image-1.5",
    ):
        """Initialize OpenAI client.

        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env.
            model: Model name (gpt-image-1.5, gpt-image-1, or gpt-image-1-mini).
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

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
        """Generate diagram image via OpenAI Images API.

        Uses images.generate when logo_parts is empty, and images.edit when
        logos are provided (reference images + prompt). Other kwargs are
        accepted for API compatibility but OpenAI Image API does not support
        temperature/top_p/top_k; they are ignored and recorded in metadata.
        """
        size = ASPECT_RATIO_TO_SIZE.get(aspect_ratio, "1536x1024")
        quality = IMAGE_SIZE_TO_QUALITY.get(image_size, "medium")

        if not logo_parts:
            result = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                quality=quality,
                output_format="png",
            )
        else:
            # Edit API: provide reference images (logos) + prompt
            image_files = [
                BytesIO(part["data"]) for part in logo_parts
            ]
            result = self.client.images.edit(
                model=self.model,
                image=image_files,
                prompt=prompt,
                size=size,
                quality=quality,
                output_format="png",
            )

        b64 = result.data[0].b64_json
        if b64 is None:
            raise ValueError("No image data in OpenAI response")
        image_bytes = base64.b64decode(b64)

        metadata = {
            "model": self.model,
            "provider": "openai",
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "aspect_ratio": aspect_ratio,
            "image_size": image_size,
            "openai_size": size,
            "openai_quality": quality,
            "prompt_length": len(prompt),
            "logo_count": len(logo_parts),
            "has_system_instruction": system_instruction is not None,
        }
        return image_bytes, "", metadata
