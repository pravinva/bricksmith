"""Google AI (Gemini) client with API key authentication for gemini-3-pro-image-preview.

NOTE: This uses API key authentication (Google AI Studio) instead of OAuth (Vertex AI)
because gemini-3-pro-image-preview is only available via Google AI Studio.
"""

import os
from typing import Any, Optional

from google import genai
from google.genai import types


# Default system instruction for architecture diagram generation
DEFAULT_ARCHITECTURE_SYSTEM_INSTRUCTION = """
You are a world-class Solutions Architect for Databricks, specializing in creating professional architecture diagrams for executive presentations and technical documentation.

CRITICAL LOGO REQUIREMENTS (MANDATORY):
- Use ONLY the uploaded logo images exactly as provided - NEVER recreate, redraw, or substitute logos
- Only include logos that are explicitly mentioned in the prompt - do not add logos that aren't referenced
- Do NOT add numbered circles, labels, annotations, or any text overlays to logos
- Scale all logos uniformly - maintain consistent size relationships between all logos
- Unity Catalog logo has pink squares, yellow triangles, navy hexagon - use the uploaded image exactly
- NO filenames, file paths, or image references may appear anywhere in the diagram

VISUAL STYLE & LAYOUT:
- Clean, professional executive presentation style suitable for C-level audiences
- Use white or very light neutral background (avoid dark backgrounds)
- Organize components logically with clear visual hierarchy
- Maintain consistent spacing between components (avoid crowding or excessive gaps)
- Align components on a grid or clear flow pattern (left-to-right, top-to-bottom, or circular as specified)
- Use consistent component sizing - similar components should be similar sizes

DATA FLOW & CONNECTIONS:
- Show clear data flow direction with well-placed arrows
- Use arrow styles consistently (solid for primary flows, dashed for optional/secondary flows)
- Ensure arrows don't overlap unnecessarily or create visual clutter
- Label connections clearly when specified in the prompt
- Use arrow colors that contrast well with background (typically dark arrows on light background)

TEXT & TYPOGRAPHY:
- Use clear, legible fonts - ensure all text is readable at presentation size
- Maintain consistent text sizing throughout the diagram
- Use high contrast between text and background (dark text on light background)
- Keep component labels concise and professional
- Ensure text doesn't overlap with logos or other visual elements
- Use appropriate font weights (bold for component names, regular for descriptions)

COLOR & DESIGN:
- Use professional color palette - avoid overly bright or clashing colors
- Maintain brand consistency when using logos (logos should appear in their original colors)
- Use subtle shadows or borders to define component boundaries if needed
- Avoid decorative elements, icons, or graphics not specified in the prompt
- Keep the design minimal and focused - every element should serve a purpose

CONSTRAINT COMPLIANCE:
- Follow all layout constraints specified in the prompt (layout direction, background color, spacing)
- Respect component types and relationships as described
- Include only components and connections explicitly mentioned
- Do not add elements, annotations, or features not requested
- Ensure the diagram matches the specified aspect ratio and composition

QUALITY STANDARDS:
- The diagram should be presentation-ready and suitable for printing or projection
- All elements should be crisp and clear (no blurry or pixelated elements)
- The overall composition should be balanced and visually appealing
- The diagram should effectively communicate the architecture at a glance
"""


class GeminiClient:
    """Google AI (Gemini) client with API key authentication.

    This client is specifically for gemini-3-pro-image-preview model which is only
    available via Google AI Studio, not Vertex AI.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client.

        Args:
            api_key: Google AI API key. If not provided, will look for
                    GEMINI_API_KEY or GOOGLE_CLOUD_API_KEY in environment.

        Raises:
            ValueError: If API key not found
        """
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_CLOUD_API_KEY")

        if not self.api_key:
            raise ValueError(
                "API key required. Set GEMINI_API_KEY or GOOGLE_CLOUD_API_KEY "
                "environment variable, or pass api_key parameter."
            )

        # Initialize client
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-3-pro-image-preview"

    def generate_image(
        self,
        prompt: str,
        logo_parts: list[dict[str, Any]],
        temperature: float = 0.8,  # Balanced for architecture diagrams with good logo inclusion
        top_p: float = 0.95,  # Higher for better logo inclusion
        top_k: Optional[int] = 50,  # Higher value helps with logo inclusion
        max_output_tokens: int = 32768,
        presence_penalty: float = 0.1,  # Reduce element repetition
        frequency_penalty: float = 0.1,  # Reduce repeated patterns
        aspect_ratio: str = "16:9",  # Changed default to 16:9 for presentations
        image_size: str = "2K",  # Increased default for better quality
        system_instruction: Optional[str] = None,  # Optional system-level guidance
    ) -> tuple[bytes, str, dict[str, Any]]:
        """Generate diagram image.

        Args:
            prompt: Text prompt for diagram generation
            logo_parts: List of logo image parts (each with 'data' and 'mime_type')
            temperature: Sampling temperature (0.0 to 2.0). Lower values (0.6-0.8)
                        produce more consistent, deterministic outputs ideal for
                        architecture diagrams.
            top_p: Nucleus sampling parameter (0.0 to 1.0). Lower values (0.85-0.9)
                   provide more focused generation.
            top_k: Top-k sampling. Limits token choices for more consistent outputs.
                   Recommended: 40-50 for architecture diagrams.
            max_output_tokens: Maximum tokens to generate
            presence_penalty: Penalty for repeating elements (0.0 to 1.0).
                            Helps avoid duplicate components in diagrams.
            frequency_penalty: Penalty for frequent patterns (0.0 to 1.0).
                             Reduces repetitive visual elements.
            aspect_ratio: Image aspect ratio (e.g., "1:1", "16:9", "4:3")
            image_size: Image size ("1K", "2K", "4K")
            system_instruction: Optional system-level instruction to guide model
                               behavior. Useful for enforcing diagram style constraints.

        Returns:
            Tuple of (image_bytes, response_text, metadata)

        Raises:
            Exception: For API errors
        """
        # Build content parts: logos first, then prompt
        content_parts = []

        # Add logo images
        for logo_part in logo_parts:
            content_parts.append(
                types.Part.from_bytes(
                    data=logo_part["data"],
                    mime_type=logo_part["mime_type"],
                )
            )

        # Add text prompt
        content_parts.append(types.Part.from_text(text=prompt))

        # Create content
        contents = [
            types.Content(
                role="user",
                parts=content_parts
            )
        ]

        # Build generation config with architecture diagram optimizations
        config_kwargs = {
            "temperature": temperature,
            "top_p": top_p,
            "max_output_tokens": max_output_tokens,
            "response_modalities": ["TEXT", "IMAGE"],
            "safety_settings": [
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
            ],
            "image_config": types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=image_size,
            ),
        }
        
        # Add optional parameters if provided
        if top_k is not None:
            config_kwargs["top_k"] = top_k
        
        # Note: presence_penalty and frequency_penalty may not be available in all SDK versions
        # Uncomment if your SDK version supports them:
        # if presence_penalty is not None:
        #     config_kwargs["presence_penalty"] = presence_penalty
        # if frequency_penalty is not None:
        #     config_kwargs["frequency_penalty"] = frequency_penalty
        
        # Use provided system instruction or default architecture instruction
        effective_system_instruction = system_instruction if system_instruction is not None else DEFAULT_ARCHITECTURE_SYSTEM_INSTRUCTION
        if effective_system_instruction:
            config_kwargs["system_instruction"] = effective_system_instruction
        
        generate_content_config = types.GenerateContentConfig(**config_kwargs)

        # Call the model
        response_text = []
        image_data = None

        try:
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                # Check if chunk has the expected structure
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue

                # Extract image data
                if (chunk.candidates[0].content.parts[0].inline_data
                    and chunk.candidates[0].content.parts[0].inline_data.data):
                    image_data = chunk.candidates[0].content.parts[0].inline_data.data
                elif chunk.text:
                    response_text.append(chunk.text)

            if not image_data:
                raise ValueError("No image data received in response")

            # Build metadata
            metadata = {
                "model": self.model,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "max_output_tokens": max_output_tokens,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty,
                "aspect_ratio": aspect_ratio,
                "image_size": image_size,
                "prompt_length": len(prompt),
                "logo_count": len(logo_parts),
                "has_system_instruction": effective_system_instruction is not None,
            }

            return image_data, "".join(response_text), metadata

        except Exception as e:
            raise Exception(f"Image generation failed: {e}")

    def analyze_image(
        self,
        image_path: str,
        prompt: str,
        temperature: float = 0.2,
        max_output_tokens: int = 2048,
    ) -> str:
        """Analyze an image and return text description/analysis.

        Args:
            image_path: Path to image file to analyze
            prompt: Analysis prompt (what to analyze about the image)
            temperature: Sampling temperature (lower for more factual analysis)
            max_output_tokens: Maximum tokens to generate

        Returns:
            Analysis text

        Raises:
            Exception: For API errors
        """
        from pathlib import Path

        # Read image file
        image_file = Path(image_path)
        with open(image_file, "rb") as f:
            image_data = f.read()

        # Determine MIME type
        suffix = image_file.suffix.lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        mime_type = mime_types.get(suffix, "image/jpeg")

        # Build content with image and prompt
        content_parts = [
            types.Part.from_bytes(data=image_data, mime_type=mime_type),
            types.Part.from_text(text=prompt),
        ]

        contents = [types.Content(role="user", parts=content_parts)]

        # Generate analysis
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            response_modalities=["TEXT"],
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config,
            )

            return response.text

        except Exception as e:
            raise Exception(f"Image analysis failed: {e}")

    def analyze_images(
        self,
        image_paths: list[str],
        prompt: str,
        temperature: float = 0.2,
        max_output_tokens: int = 2048,
    ) -> str:
        """Analyze multiple images and return comparative analysis.

        Args:
            image_paths: List of paths to image files to analyze
            prompt: Analysis prompt (what to analyze about the images)
            temperature: Sampling temperature (lower for more factual analysis)
            max_output_tokens: Maximum tokens to generate

        Returns:
            Analysis text

        Raises:
            Exception: For API errors
        """
        from pathlib import Path

        # Build content parts with all images
        content_parts = []

        for i, image_path in enumerate(image_paths, 1):
            image_file = Path(image_path)
            with open(image_file, "rb") as f:
                image_data = f.read()

            # Determine MIME type
            suffix = image_file.suffix.lower()
            mime_types = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
            }
            mime_type = mime_types.get(suffix, "image/jpeg")

            content_parts.append(
                types.Part.from_bytes(data=image_data, mime_type=mime_type)
            )

        # Add analysis prompt
        content_parts.append(types.Part.from_text(text=prompt))

        contents = [types.Content(role="user", parts=content_parts)]

        # Generate analysis
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            response_modalities=["TEXT"],
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config,
            )

            return response.text

        except Exception as e:
            raise Exception(f"Image analysis failed: {e}")

    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.4,
        max_output_tokens: int = 2048,
    ) -> str:
        """Generate text response (no images).

        Args:
            prompt: Text prompt
            temperature: Sampling temperature
            max_output_tokens: Maximum tokens to generate

        Returns:
            Generated text

        Raises:
            Exception: For API errors
        """
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            response_modalities=["TEXT"],
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config,
            )

            return response.text

        except Exception as e:
            raise Exception(f"Text generation failed: {e}")

    def get_model_info(self) -> dict[str, Any]:
        """Get information about the model.

        Returns:
            Model information dictionary
        """
        return {
            "model": self.model,
            "provider": "Google AI Studio",
            "authentication": "API Key",
            "capabilities": [
                "text-to-image",
                "multimodal-input",
                "logo-integration",
                "image-analysis",
                "visual-comparison",
            ],
        }
