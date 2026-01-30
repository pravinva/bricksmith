"""Data models for Nano Banana Pro."""

from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field


class LogoInfo(BaseModel):
    """Information about a single logo."""

    name: str = Field(..., description="Human-readable logo name (e.g., 'databricks')")
    description: str = Field(
        ..., description="Description for prompt (e.g., 'red icon')"
    )
    file_path: Path = Field(..., description="Path to logo file")
    sha256_hash: str = Field(..., description="SHA256 hash for tracking")
    content_type: str = Field(..., description="MIME type (e.g., 'image/jpeg')")
    size_bytes: int = Field(..., description="File size in bytes")


class Component(BaseModel):
    """A component in the architecture diagram."""

    id: str = Field(..., description="Unique component identifier")
    label: str = Field(..., description="Display label for the component")
    type: str = Field(..., description="Component type (service, storage, database, etc.)")
    logo_name: Optional[str] = Field(
        default=None, description="Logo name reference (from LogoInfo.name)"
    )


class Connection(BaseModel):
    """A connection between components."""

    from_id: str = Field(..., description="Source component ID")
    to_id: str = Field(..., description="Target component ID")
    label: Optional[str] = Field(default=None, description="Connection label")
    style: str = Field(default="solid", description="Line style: solid, dashed, or dotted")


class DiagramConstraints(BaseModel):
    """Layout and style constraints for the diagram."""

    layout: str = Field(
        default="left-to-right",
        description="Layout direction: left-to-right, top-to-bottom, or grid",
    )
    background: str = Field(default="white", description="Background color")
    label_style: str = Field(
        default="sentence-case", description="Label formatting style"
    )
    show_grid: bool = Field(default=False, description="Whether to show grid lines")
    spacing: str = Field(
        default="comfortable", description="Spacing: compact, comfortable, or spacious"
    )


class DiagramSpec(BaseModel):
    """Complete diagram specification."""

    name: str = Field(..., description="Diagram name/identifier")
    description: str = Field(..., description="Diagram description")
    components: list[Component] = Field(..., description="List of components")
    connections: list[Connection] = Field(..., description="List of connections")
    constraints: DiagramConstraints = Field(
        default_factory=DiagramConstraints, description="Layout and style constraints"
    )

    @classmethod
    def from_yaml(cls, path: Path) -> "DiagramSpec":
        """Load diagram specification from YAML file.

        Args:
            path: Path to YAML file

        Returns:
            DiagramSpec instance

        Raises:
            FileNotFoundError: If file doesn't exist
            yaml.YAMLError: If YAML is invalid
            ValidationError: If spec doesn't match schema
        """
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def to_yaml(self, path: Path) -> None:
        """Save diagram specification to YAML file.

        Args:
            path: Path to save YAML file
        """
        with open(path, "w") as f:
            yaml.safe_dump(self.model_dump(), f, default_flow_style=False, sort_keys=False)


class PromptTemplate(BaseModel):
    """A prompt template with variable substitution."""

    id: str = Field(..., description="Template identifier")
    name: str = Field(..., description="Human-readable template name")
    template: str = Field(..., description="Template text with {variable} placeholders")
    variables: dict[str, Any] = Field(
        default_factory=dict, description="Default variable values"
    )

    @classmethod
    def from_file(cls, path: Path, template_id: Optional[str] = None) -> "PromptTemplate":
        """Load prompt template from text file.

        Args:
            path: Path to template file
            template_id: Optional template ID (defaults to filename without extension)

        Returns:
            PromptTemplate instance
        """
        with open(path, "r") as f:
            content = f.read()

        if template_id is None:
            template_id = path.stem

        return cls(
            id=template_id,
            name=template_id.replace("_", " ").title(),
            template=content,
        )


class GenerationResult(BaseModel):
    """Result of a diagram generation."""

    run_id: str = Field(..., description="MLflow run ID")
    output_path: Path = Field(..., description="Path to generated image")
    prompt_text: str = Field(..., description="Complete prompt used for generation")
    parameters: dict[str, Any] = Field(..., description="Generation parameters")
    generation_time_seconds: float = Field(..., description="Time taken to generate")
    success: bool = Field(..., description="Whether generation succeeded")
    error_message: Optional[str] = Field(
        default=None, description="Error message if generation failed"
    )


class EvaluationScores(BaseModel):
    """Manual evaluation scores for a generated diagram."""

    logo_fidelity_score: int = Field(
        ..., ge=0, le=5, description="Logo reuse fidelity (0-5)"
    )
    layout_clarity_score: int = Field(..., ge=0, le=5, description="Layout clarity (0-5)")
    text_legibility_score: int = Field(
        ..., ge=0, le=5, description="Text legibility (0-5)"
    )
    constraint_compliance_score: int = Field(
        ..., ge=0, le=5, description="Constraint compliance (0-5)"
    )
    notes: str = Field(default="", description="Evaluation notes")

    @property
    def overall_score(self) -> float:
        """Calculate average score across all dimensions.

        Returns:
            Average score (0.0-5.0)
        """
        return (
            self.logo_fidelity_score
            + self.layout_clarity_score
            + self.text_legibility_score
            + self.constraint_compliance_score
        ) / 4.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary including calculated overall score.

        Returns:
            Dictionary with all scores and overall score
        """
        data = self.model_dump()
        data["overall_score"] = self.overall_score
        return data


class PromptRefinement(BaseModel):
    """Result of prompt refinement analysis."""

    original_prompt: str = Field(..., description="Original prompt text")
    refined_prompt: str = Field(..., description="Improved prompt text")
    changes: list[str] = Field(..., description="List of key changes made")
    expected_improvements: list[str] = Field(
        ..., description="Expected improvements from changes"
    )
    analysis: dict[str, Any] = Field(..., description="Visual analysis results")
    confidence_score: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Confidence in refinement (0-1)"
    )

    def save_template(self, output_path: Path) -> None:
        """Save refined prompt as a template file.

        Args:
            output_path: Path to save template
        """
        with open(output_path, "w") as f:
            f.write(self.refined_prompt)

    def summary(self) -> str:
        """Generate human-readable summary of refinement.

        Returns:
            Formatted summary string
        """
        summary = ["Prompt Refinement Summary", "=" * 50, ""]

        summary.append("Key Changes:")
        for i, change in enumerate(self.changes, 1):
            summary.append(f"  {i}. {change}")

        summary.append("")
        summary.append("Expected Improvements:")
        for i, improvement in enumerate(self.expected_improvements, 1):
            summary.append(f"  {i}. {improvement}")

        summary.append("")
        summary.append(f"Confidence: {self.confidence_score:.1%}")

        return "\n".join(summary)
