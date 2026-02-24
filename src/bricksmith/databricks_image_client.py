"""Databricks Model Serving image generation client using the OpenAI Responses API.

Routes through a Databricks serving endpoint (e.g. databricks-gpt-5-2) to
gpt-image-1.5 for image generation. Uses existing DATABRICKS_HOST and
DATABRICKS_TOKEN credentials - no separate OpenAI API key required.

Only available on AWS US Databricks workspaces.
"""

import base64
import os
from io import BytesIO
from typing import Any, Optional

from openai import OpenAI
from PIL import Image as PILImage

# Map aspect ratio to OpenAI size (same as openai_image_client.py)
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


def _compress_for_upload(image_data: bytes, max_side: int = 2048, quality: int = 95) -> str:
    """Compress raw image bytes to a JPEG base64 string for API upload."""
    img = PILImage.open(BytesIO(image_data))
    if max(img.size) > max_side:
        ratio = max_side / max(img.size)
        img = img.resize((int(img.width * ratio), int(img.height * ratio)))
    buf = BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


class DatabricksImageClient:
    """Databricks Model Serving image client using the OpenAI Responses API.

    Implements the same generate_image contract as GeminiClient/OpenAIImageClient
    so callers can switch provider via config.

    Uses client.responses.create() with the image_generation tool, which is
    fundamentally different from the standard OpenAI images.generate/edit APIs.
    """

    def __init__(
        self,
        model: str = "databricks-gpt-5-2",
        image_model: str = "gpt-image-1.5",
        host: Optional[str] = None,
        token: Optional[str] = None,
    ):
        """Initialize Databricks image client.

        Args:
            model: Databricks serving endpoint for routing (e.g. databricks-gpt-5-2).
            image_model: Underlying image generation model (e.g. gpt-image-1.5).
            host: Databricks workspace URL. Falls back to DATABRICKS_HOST env.
            token: Databricks PAT token. Falls back to DATABRICKS_TOKEN env.
        """
        resolved_host = host or os.getenv("DATABRICKS_HOST", "")
        resolved_token = token or os.getenv("DATABRICKS_TOKEN", "")

        if not resolved_host:
            raise ValueError(
                "Databricks host required. Set DATABRICKS_HOST environment variable "
                "or pass host parameter."
            )
        if not resolved_token:
            raise ValueError(
                "Databricks token required. Set DATABRICKS_TOKEN environment variable "
                "or pass token parameter."
            )

        self.client = OpenAI(
            api_key=resolved_token,
            base_url=f"{resolved_host.rstrip('/')}/serving-endpoints",
        )
        self.model = model
        self.image_model = image_model

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
        """Generate diagram image via Databricks Model Serving Responses API.

        Uses responses.create() with image_generation tool. When logo_parts are
        empty, sends a plain text prompt. When logos are provided, sends a
        multi-part input with compressed JPEG data URIs.
        """
        size = ASPECT_RATIO_TO_SIZE.get(aspect_ratio, "1536x1024")
        quality = IMAGE_SIZE_TO_QUALITY.get(image_size, "medium")

        tools = [
            {
                "type": "image_generation",
                "model": self.image_model,
                "quality": quality,
                "size": size,
                "output_format": "png",
            }
        ]

        if not logo_parts:
            # Text-to-image: simple string input
            api_input: Any = prompt
        else:
            # Edit mode: compress logos to JPEG data URIs
            content: list[dict[str, Any]] = [{"type": "input_text", "text": prompt}]
            for part in logo_parts:
                b64 = _compress_for_upload(part["data"])
                content.append(
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{b64}",
                    }
                )
            api_input = [{"role": "user", "content": content}]

        response = self.client.responses.create(
            model=self.model,
            input=api_input,
            tools=tools,
        )

        # Extract image from response output items
        image_bytes: Optional[bytes] = None
        for item in response.output:
            if item.type == "image_generation_call":
                image_bytes = base64.b64decode(item.result)
                break

        if image_bytes is None:
            raise ValueError(
                "No image_generation_call found in Databricks response. "
                "Check that the endpoint supports the image_generation tool."
            )

        metadata: dict[str, Any] = {
            "model": self.model,
            "image_model": self.image_model,
            "provider": "databricks",
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
