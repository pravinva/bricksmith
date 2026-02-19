"""Configuration management for Bricksmith."""

import os
from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class VertexAIConfig(BaseModel):
    """Vertex AI model configuration."""

    project_id: str = Field(..., description="GCP project ID")
    location: str = Field(default="us-central1", description="GCP region")
    model_id: str = Field(
        default="gemini-3-pro-image-preview",
        description="Vertex AI model identifier",
    )
    temperature: float = Field(default=0.4, ge=0.0, le=2.0)
    top_p: float = Field(default=0.95, ge=0.0, le=1.0)
    max_output_tokens: int = Field(default=8192, ge=1)
    image_size: str = Field(default="1024x1024", description="Output image size")
    aspect_ratio: Optional[str] = Field(default=None, description="Image aspect ratio")
    seed: Optional[int] = Field(default=42, description="Random seed for reproducibility")


class MLflowConfig(BaseModel):
    """MLflow tracking configuration."""

    tracking_uri: str = Field(
        default="file:./mlruns", description="MLflow tracking server URI"
    )
    experiment_name: str = Field(
        default="bricksmith-arch-diagrams",
        description="MLflow experiment name",
    )
    artifact_location: Optional[str] = Field(
        default=None, description="Custom artifact storage location"
    )


class ImageProviderConfig(BaseModel):
    """Image generation provider (Gemini or OpenAI gpt-image)."""

    provider: Literal["gemini", "openai"] = Field(
        default="gemini",
        description="Backend for diagram image generation: gemini or openai (gpt-image-1.5)",
    )
    openai_model: str = Field(
        default="gpt-image-1.5",
        description="OpenAI model when provider is openai (e.g. gpt-image-1.5, gpt-image-1)",
    )


class LogoKitConfig(BaseModel):
    """Logo kit configuration."""

    logo_dir: Path = Field(
        default=Path("./logos/default"), description="Directory containing logos"
    )
    max_logo_size_mb: float = Field(default=5.0, description="Maximum logo file size in MB")
    allowed_extensions: list[str] = Field(
        default=[".jpg", ".jpeg", ".png"], description="Allowed logo file extensions"
    )


class AppConfig(BaseSettings):
    """Main application configuration.

    Can be loaded from:
    1. YAML file (configs/default.yaml by default)
    2. Environment variables with BRICKSMITH_ prefix
    3. Direct initialization
    """

    model_config = SettingsConfigDict(
        env_prefix="BRICKSMITH_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    vertex: VertexAIConfig = Field(default_factory=VertexAIConfig)
    mlflow: MLflowConfig = Field(default_factory=MLflowConfig)
    image_provider: ImageProviderConfig = Field(
        default_factory=ImageProviderConfig,
        description="Image generation backend (gemini or openai)",
    )
    logo_kit: LogoKitConfig = Field(default_factory=LogoKitConfig)

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "AppConfig":
        """Load configuration from YAML file.

        Supports environment variable substitution using ${VAR_NAME} syntax.

        Args:
            yaml_path: Path to YAML configuration file

        Returns:
            AppConfig instance
        """
        with open(yaml_path, "r") as f:
            content = f.read()

        # Substitute environment variables
        content = os.path.expandvars(content)

        data = yaml.safe_load(content)

        # Parse nested structures
        config_dict = {}
        if "vertex" in data:
            config_dict["vertex"] = VertexAIConfig(**data["vertex"])
        if "mlflow" in data:
            config_dict["mlflow"] = MLflowConfig(**data["mlflow"])
        if "image_provider" in data:
            config_dict["image_provider"] = ImageProviderConfig(**data["image_provider"])
        if "logo_kit" in data:
            # Convert logo_dir string to Path
            logo_data = data["logo_kit"].copy()
            if "logo_dir" in logo_data:
                logo_data["logo_dir"] = Path(logo_data["logo_dir"])
            config_dict["logo_kit"] = LogoKitConfig(**logo_data)

        return cls(**config_dict)

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "AppConfig":
        """Load configuration from file or use defaults.

        Args:
            config_path: Optional path to config file. If not provided,
                        tries configs/default.yaml, then uses defaults.

        Returns:
            AppConfig instance
        """
        if config_path and config_path.exists():
            return cls.from_yaml(config_path)

        default_path = Path("configs/default.yaml")
        if default_path.exists():
            return cls.from_yaml(default_path)

        # Use defaults
        return cls()


def load_config(config_path: Optional[Path] = None) -> AppConfig:
    """Convenience function to load application configuration.

    Args:
        config_path: Optional path to configuration file

    Returns:
        AppConfig instance
    """
    return AppConfig.load(config_path)
