"""Vertex AI client with OAuth authentication for Nano Banana Pro."""

from typing import Any, Optional

import google.auth
from google.auth.transport import requests as google_requests

from .config import VertexAIConfig


class VertexAIClient:
    """Vertex AI client with OAuth authentication.

    Uses Application Default Credentials (ADC) for authentication.
    No API keys are used.
    """

    def __init__(self, config: VertexAIConfig):
        """Initialize Vertex AI client.

        Args:
            config: Vertex AI configuration
        """
        self.config = config
        self._credentials = None
        self._client = None

    def authenticate(self) -> None:
        """Authenticate using OAuth (Application Default Credentials).

        Raises:
            google.auth.exceptions.DefaultCredentialsError: If ADC not configured
        """
        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        # Refresh credentials if needed
        if not credentials.valid:
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(google_requests.Request())

        self._credentials = credentials

        # Initialize client
        try:
            from google import genai
            from google.genai import types

            self._client = genai.Client(
                vertexai=True,
                project=self.config.project_id,
                location=self.config.location,
                credentials=credentials,
            )
            self._types = types
        except ImportError:
            raise ImportError(
                "google-genai library not found. Install with: uv pip install google-genai"
            )

    def verify_auth(self) -> bool:
        """Verify OAuth credentials are valid.

        Returns:
            True if authenticated, False otherwise
        """
        try:
            if self._credentials is None:
                self.authenticate()

            return self._credentials.valid
        except Exception as e:
            print(f"Authentication verification failed: {e}")
            return False

    def generate_image(
        self,
        prompt: str,
        logo_parts: list[dict[str, Any]],
        generation_config: Optional[dict[str, Any]] = None,
    ) -> tuple[bytes, dict[str, Any]]:
        """Generate diagram image.

        Args:
            prompt: Text prompt
            logo_parts: List of logo image parts
            generation_config: Optional generation configuration override

        Returns:
            Tuple of (image_bytes, metadata)

        Raises:
            ValueError: If not authenticated
            Exception: For API errors
        """
        if self._client is None:
            raise ValueError("Client not authenticated. Call authenticate() first.")

        # Build content parts (text + images)
        content_parts = self._build_content_parts(prompt, logo_parts)

        # Build generation config
        gen_config = self._build_generation_config(generation_config)

        try:
            # Generate image using Vertex AI
            response = self._client.models.generate_content(
                model=self.config.model_id,
                contents=content_parts,
                config=gen_config,
            )

            # Extract image from response
            if not response.candidates:
                raise ValueError("No candidates in response")

            candidate = response.candidates[0]
            if not candidate.content.parts:
                raise ValueError("No parts in response content")

            # Get image part
            image_part = candidate.content.parts[0]
            if not hasattr(image_part, "inline_data"):
                raise ValueError("Response does not contain image data")

            image_bytes = image_part.inline_data.data

            # Build metadata
            metadata = {
                "model": self.config.model_id,
                "finish_reason": str(candidate.finish_reason),
                "safety_ratings": [
                    {
                        "category": str(rating.category),
                        "probability": str(rating.probability),
                    }
                    for rating in candidate.safety_ratings
                ]
                if candidate.safety_ratings
                else [],
            }

            return image_bytes, metadata

        except Exception as e:
            raise Exception(f"Image generation failed: {e}")

    def _build_content_parts(
        self,
        prompt: str,
        logo_parts: list[dict[str, Any]],
    ) -> list[Any]:
        """Build content parts for multi-modal input.

        Args:
            prompt: Text prompt
            logo_parts: List of logo image parts

        Returns:
            List of content parts
        """
        parts = []

        # Add all logo images first
        for logo_part in logo_parts:
            parts.append(
                self._types.Part.from_bytes(
                    data=logo_part["data"],
                    mime_type=logo_part["mime_type"],
                )
            )

        # Add text prompt last
        parts.append(self._types.Part.from_text(text=prompt))

        return parts

    def _build_generation_config(
        self, override_config: Optional[dict[str, Any]] = None
    ) -> Any:
        """Build generation configuration.

        Args:
            override_config: Optional config overrides

        Returns:
            GenerationConfig object
        """
        config_dict = {
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "max_output_tokens": self.config.max_output_tokens,
        }

        if self.config.seed is not None:
            config_dict["seed"] = self.config.seed

        # Apply overrides
        if override_config:
            config_dict.update(override_config)

        return self._types.GenerateContentConfig(**config_dict)

    def get_model_info(self) -> dict[str, Any]:
        """Get information about the configured model.

        Returns:
            Model information dictionary
        """
        return {
            "model_id": self.config.model_id,
            "project_id": self.config.project_id,
            "location": self.config.location,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "max_output_tokens": self.config.max_output_tokens,
            "seed": self.config.seed,
        }
