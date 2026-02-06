"""Data models for Nano Banana Pro."""

from enum import Enum
from pathlib import Path
from typing import Any, Optional

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


# =============================================================================
# Conversation Models for Interactive Diagram Refinement
# =============================================================================


class ConversationStatus(str, Enum):
    """Status of a conversation session."""

    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class EvaluationPersona(str, Enum):
    """Persona lens for diagram evaluation.

    Different personas emphasize different aspects of architecture diagrams.
    """

    # Architecture-first (default) - focuses on universal best practices
    ARCHITECT = "architect"

    # Executive/CTO lens - strategic, cost, risk focused
    EXECUTIVE = "executive"

    # Developer/Engineer lens - implementation details, APIs, tech stack
    DEVELOPER = "developer"

    # Auto-detect based on diagram complexity
    AUTO = "auto"


class ConversationTurn(BaseModel):
    """A single turn in the conversation (generate → evaluate → feedback cycle)."""

    iteration: int = Field(..., description="Turn number (1-based)")
    prompt_used: str = Field(..., description="The prompt used for this generation")
    run_id: str = Field(..., description="MLflow run ID for this iteration")
    image_path: Path = Field(..., description="Path to generated image")
    generation_time_seconds: float = Field(..., description="Time taken to generate")
    score: Optional[int] = Field(default=None, ge=1, le=5, description="User score (1-5)")
    feedback: Optional[str] = Field(default=None, description="User feedback text")
    visual_analysis: Optional[str] = Field(
        default=None, description="AI visual analysis of the generated image"
    )
    refinement_reasoning: Optional[str] = Field(
        default=None, description="DSPy reasoning for prompt refinement"
    )


class ConversationSession(BaseModel):
    """A complete conversation session for iterative diagram refinement."""

    session_id: str = Field(..., description="Unique session identifier")
    initial_prompt: str = Field(..., description="The starting prompt")
    turns: list[ConversationTurn] = Field(
        default_factory=list, description="List of conversation turns"
    )
    status: ConversationStatus = Field(
        default=ConversationStatus.ACTIVE, description="Session status"
    )
    created_at: str = Field(default="", description="Session creation timestamp")
    diagram_spec_path: Optional[Path] = Field(
        default=None, description="Path to diagram spec if used"
    )
    template_id: Optional[str] = Field(
        default=None, description="Template ID if used"
    )

    def add_turn(self, turn: ConversationTurn) -> None:
        """Add a turn to the session.

        Args:
            turn: ConversationTurn to add
        """
        self.turns.append(turn)

    def get_history_json(self) -> str:
        """Get conversation history as JSON for DSPy context.

        Returns:
            JSON string of conversation history
        """
        import json

        history = []
        for turn in self.turns:
            history.append({
                "iteration": turn.iteration,
                "score": turn.score,
                "feedback": turn.feedback,
                "visual_analysis": turn.visual_analysis,
                "refinement_reasoning": turn.refinement_reasoning,
            })
        return json.dumps(history, indent=2)

    def is_satisfied(self, target_score: int = 5) -> bool:
        """Check if the latest score meets the target.

        Args:
            target_score: Target score to reach

        Returns:
            True if latest score >= target_score
        """
        if not self.turns:
            return False
        latest_turn = self.turns[-1]
        return latest_turn.score is not None and latest_turn.score >= target_score

    def get_latest_prompt(self) -> str:
        """Get the most recent prompt used.

        Returns:
            Latest prompt or initial prompt if no turns
        """
        if self.turns:
            return self.turns[-1].prompt_used
        return self.initial_prompt

    def get_best_turn(self) -> Optional[ConversationTurn]:
        """Get the turn with the highest score.

        Returns:
            Best scoring turn or None if no scored turns
        """
        scored_turns = [t for t in self.turns if t.score is not None]
        if not scored_turns:
            return None
        return max(scored_turns, key=lambda t: t.score)


class GenerationSettings(BaseModel):
    """Sampling settings for image generation."""

    temperature: float = Field(
        default=0.8, ge=0.0, le=2.0,
        description="Sampling temperature: 0=deterministic, 0.8=balanced, 2.0=creative"
    )
    top_p: float = Field(
        default=0.95, ge=0.0, le=1.0,
        description="Nucleus sampling: lower=focused, higher=diverse"
    )
    top_k: int = Field(
        default=50, ge=0,
        description="Top-k sampling: limits token choices (0 to disable)"
    )
    presence_penalty: float = Field(
        default=0.1, ge=0.0, le=2.0,
        description="Penalty for repeating elements"
    )
    frequency_penalty: float = Field(
        default=0.1, ge=0.0, le=2.0,
        description="Penalty for frequent patterns"
    )

    def summary(self) -> str:
        """Return a short summary of settings."""
        parts = [f"t={self.temperature}"]
        if self.top_p != 0.95:
            parts.append(f"p={self.top_p}")
        if self.top_k != 50:
            parts.append(f"k={self.top_k}")
        return " ".join(parts)


class ConversationConfig(BaseModel):
    """Configuration for conversation sessions."""

    max_iterations: int = Field(
        default=10, ge=1, le=50, description="Maximum number of iterations"
    )
    target_score: int = Field(
        default=5, ge=1, le=5, description="Target score to stop refinement"
    )
    auto_analyze: bool = Field(
        default=True, description="Automatically analyze images with AI"
    )
    auto_refine: bool = Field(
        default=False,
        description="Automatically refine based on design principles (no manual feedback)"
    )
    reference_image: Optional[Path] = Field(
        default=None,
        description="Reference image to match style and design patterns"
    )
    session_name: Optional[str] = Field(
        default=None,
        description="Name for the session (used in output directory)"
    )
    temperature: float = Field(
        default=0.8, ge=0.0, le=2.0, description="Generation temperature"
    )
    top_p: float = Field(
        default=0.95, ge=0.0, le=1.0, description="Nucleus sampling"
    )
    top_k: int = Field(
        default=50, ge=0, description="Top-k sampling (0 to disable)"
    )
    presence_penalty: float = Field(
        default=0.1, ge=0.0, le=2.0, description="Presence penalty"
    )
    frequency_penalty: float = Field(
        default=0.1, ge=0.0, le=2.0, description="Frequency penalty"
    )
    logo_dir: Optional[Path] = Field(
        default=None, description="Logo directory override"
    )
    evaluation_persona: EvaluationPersona = Field(
        default=EvaluationPersona.ARCHITECT,
        description="Persona lens for LLM Judge evaluation (architect, executive, developer, auto)"
    )

    def get_generation_settings(self) -> GenerationSettings:
        """Get current generation settings."""
        return GenerationSettings(
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
        )


# =============================================================================
# Architect Models for Collaborative Architecture Design
# =============================================================================


class ArchitectTurn(BaseModel):
    """A single turn in the architect conversation."""

    turn_number: int = Field(..., description="Turn number (1-based)")
    user_input: str = Field(..., description="User's message in this turn")
    architect_response: str = Field(..., description="AI architect's response")
    architecture_snapshot: Optional[dict] = Field(
        default=None,
        description="Components and connections at this point in the conversation"
    )
    timestamp: str = Field(default="", description="Turn timestamp")


class ArchitectSession(BaseModel):
    """A complete architect conversation session."""

    session_id: str = Field(..., description="Unique session identifier")
    initial_problem: str = Field(..., description="The initial problem description")
    turns: list[ArchitectTurn] = Field(
        default_factory=list, description="List of conversation turns"
    )
    current_architecture: dict = Field(
        default_factory=lambda: {"components": [], "connections": []},
        description="Evolving architecture state"
    )
    available_logos: list[str] = Field(
        default_factory=list, description="Logo names available for the diagram"
    )
    custom_context: Optional[str] = Field(
        default=None, description="Custom domain/customer context"
    )
    created_at: str = Field(default="", description="Session creation timestamp")
    status: ConversationStatus = Field(
        default=ConversationStatus.ACTIVE, description="Session status"
    )

    def add_turn(self, turn: ArchitectTurn) -> None:
        """Add a turn to the session.

        Args:
            turn: ArchitectTurn to add
        """
        self.turns.append(turn)

    def get_history_json(self) -> str:
        """Get conversation history as JSON for DSPy context.

        Returns:
            JSON string of conversation history
        """
        import json

        history = []
        for turn in self.turns:
            history.append({
                "turn_number": turn.turn_number,
                "user_input": turn.user_input,
                "architect_response": turn.architect_response,
                "architecture_snapshot": turn.architecture_snapshot,
            })
        return json.dumps(history, indent=2)

    def get_architecture_json(self) -> str:
        """Get current architecture as JSON.

        Returns:
            JSON string of current architecture
        """
        import json
        return json.dumps(self.current_architecture, indent=2)


class MCPEnrichmentConfig(BaseModel):
    """Configuration for MCP-based context enrichment.

    When enabled and invoked from Claude Code with an mcp_callback,
    the architect chatbot will automatically search internal knowledge
    sources for relevant context before processing user input.
    """

    enabled: bool = Field(
        default=False,
        description="Enable MCP-based context enrichment (requires Claude Code callback)",
    )

    sources: list[str] = Field(
        default_factory=lambda: ["glean", "confluence"],
        description="MCP sources to query: glean, slack, jira, confluence",
    )

    max_results_per_source: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum results to retrieve per source",
    )

    max_context_chars: int = Field(
        default=2000,
        ge=100,
        le=10000,
        description="Maximum characters for enriched context",
    )


class ArchitectConfig(BaseModel):
    """Configuration for architect sessions."""

    max_turns: int = Field(
        default=20, ge=1, le=100, description="Maximum conversation turns"
    )
    context_file: Optional[Path] = Field(
        default=None, description="Custom context file with domain knowledge"
    )
    reference_prompt: Optional[Path] = Field(
        default=None,
        description="Existing diagram prompt to use as reference/starting point"
    )
    output_format: str = Field(
        default="prompt",
        description="Output format: 'prompt' for generate-raw or 'spec' for YAML"
    )
    session_name: Optional[str] = Field(
        default=None, description="Session name for output directory"
    )
    logo_dir: Optional[Path] = Field(
        default=None, description="Logo directory override"
    )
    mcp_enrichment: MCPEnrichmentConfig = Field(
        default_factory=MCPEnrichmentConfig,
        description="MCP context enrichment configuration",
    )
