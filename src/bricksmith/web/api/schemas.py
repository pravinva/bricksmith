"""Pydantic request/response schemas for the web API."""

from typing import Any, Optional, Literal

from pydantic import BaseModel, Field


# Component and Connection schemas (mirrors models.py)
class ComponentSchema(BaseModel):
    """A component in the architecture."""

    id: str
    label: str
    type: str = Field(
        default="service",
        description="Component type: service, storage, external, compute, network",
    )
    logo_name: Optional[str] = None


class ConnectionSchema(BaseModel):
    """A connection between components."""

    from_id: str
    to_id: str
    label: Optional[str] = None
    style: str = Field(default="solid", description="Line style: solid, dashed, dotted")


class ArchitectureState(BaseModel):
    """Current state of the architecture being designed."""

    components: list[ComponentSchema] = Field(default_factory=list)
    connections: list[ConnectionSchema] = Field(default_factory=list)
    title: Optional[str] = None
    subtitle: Optional[str] = None


# MCP enrichment options for session creation
class MCPEnrichmentOptions(BaseModel):
    """MCP enrichment configuration for a session."""

    enabled: bool = False
    sources: list[str] = Field(default_factory=lambda: ["glean", "confluence"])


# Session schemas
class CreateSessionRequest(BaseModel):
    """Request to create a new architect session."""

    initial_problem: str = Field(
        ..., description="Description of the architecture problem to solve"
    )
    custom_context: Optional[str] = Field(None, description="Additional context or requirements")
    logo_dir: Optional[str] = Field(
        None, description="Path to logo directory (defaults to logos/default)"
    )
    image_provider: Optional[Literal["gemini", "openai"]] = Field(
        None,
        description="Optional image provider override for this session",
    )
    openai_api_key: Optional[str] = Field(
        None,
        description="Optional OpenAI API key for this session",
    )
    vertex_api_key: Optional[str] = Field(
        None,
        description="Optional Gemini/Vertex API key for this session",
    )
    reference_prompt: Optional[str] = Field(
        None, description="Existing prompt text to use as reference"
    )
    reference_prompt_path: Optional[str] = Field(
        None, description="Path to a prompt file to load as reference"
    )
    reference_image_base64: Optional[str] = Field(
        None, description="Base64-encoded reference architecture image (PNG, JPG, GIF, WebP)"
    )
    reference_image_filename: Optional[str] = Field(
        None, description="Original filename for MIME type detection"
    )
    mcp_enrichment: Optional[MCPEnrichmentOptions] = Field(
        None, description="MCP enrichment configuration"
    )


class SessionResponse(BaseModel):
    """Response containing session details."""

    session_id: str
    initial_problem: str
    status: str = Field(description="Session status: active, completed")
    created_at: str
    turn_count: int
    current_architecture: Optional[ArchitectureState] = None


class SessionListResponse(BaseModel):
    """Response containing a list of sessions."""

    sessions: list[SessionResponse]
    total: int


# Chat/message schemas
class SendMessageRequest(BaseModel):
    """Request to send a message in a session."""

    message: str = Field(..., description="User message or command")


class MessageResponse(BaseModel):
    """Response from sending a message."""

    response: str = Field(description="Architect's response")
    ready_for_output: bool = Field(
        default=False, description="Whether architecture is ready for diagram generation"
    )
    architecture: ArchitectureState = Field(
        default_factory=ArchitectureState,
        description="Current architecture state",
    )
    turn_number: int


class StatusResponse(BaseModel):
    """Response containing current architecture status."""

    session_id: str
    status: str
    turn_count: int
    ready_for_output: bool
    architecture: ArchitectureState
    available_logos: list[str] = Field(default_factory=list)
    image_provider: Literal["gemini", "openai"] = Field(
        default="gemini",
        description="Active image provider for this session",
    )
    credential_mode: Literal["environment", "custom_key"] = Field(
        default="environment",
        description="Whether session uses environment credentials or user-supplied key",
    )


class GenerateOutputRequest(BaseModel):
    """Request to generate the final diagram prompt."""

    output_dir: Optional[str] = Field(
        None, description="Directory to save output files (defaults to outputs/)"
    )


class GenerateOutputResponse(BaseModel):
    """Response from generating output."""

    success: bool
    output_dir: Optional[str] = None
    prompt_file: Optional[str] = None
    architecture_file: Optional[str] = None
    error: Optional[str] = None


# Preview generation schemas
class GeneratePreviewResponse(BaseModel):
    """Response from generating a diagram preview image."""

    success: bool
    image_url: Optional[str] = Field(None, description="URL to access the generated image")
    image_urls: list[str] = Field(default_factory=list, description="URLs for all variants")
    run_id: Optional[str] = Field(None, description="Identifier for this generation run")
    error: Optional[str] = None


# Turn history schemas
class TurnSchema(BaseModel):
    """A single conversation turn."""

    turn_number: int
    user_input: str
    architect_response: str
    architecture_snapshot: Optional[dict] = None
    created_at: Optional[str] = None


class TurnsResponse(BaseModel):
    """Response containing conversation turns for a session."""

    turns: list[TurnSchema]


# Error response
class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str
    error_code: Optional[str] = None


# CLI mirror schemas
class CLICommandSpec(BaseModel):
    """Metadata for a supported CLI command."""

    name: str
    description: str
    examples: list[str] = Field(default_factory=list)
    supports_stdin: bool = False


class CLICommandsResponse(BaseModel):
    """Response containing supported CLI commands."""

    commands: list[CLICommandSpec]


class StartCliJobRequest(BaseModel):
    """Request to execute a CLI command."""

    command: str = Field(..., description="CLI subcommand name")
    args: list[str] = Field(
        default_factory=list,
        description="Arguments to pass to the command (one array item per argument)",
    )
    stdin_text: Optional[str] = Field(
        default=None,
        description="Optional stdin content for interactive commands",
    )
    timeout_seconds: int = Field(
        default=1800,
        ge=1,
        le=7200,
        description="Timeout in seconds before command is terminated",
    )


class CliJobResponse(BaseModel):
    """Response describing the state/result of a CLI job."""

    job_id: str
    status: Literal["queued", "running", "succeeded", "failed", "cancelled", "timeout"]
    command: str
    args: list[str]
    started_at: str
    ended_at: Optional[str] = None
    exit_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    timeout_seconds: int


class StartCliJobResponse(BaseModel):
    """Response when submitting a CLI job."""

    job: CliJobResponse


# Best results explorer schemas
class BestResultItem(BaseModel):
    """One ranked architecture+prompt result."""

    result_id: str
    source: Literal["chat", "generate_raw", "refine", "unknown"]
    title: str
    image_path: Optional[str] = None
    image_url: Optional[str] = None
    prompt_path: Optional[str] = None
    prompt_preview: str = ""
    full_prompt: Optional[str] = None
    run_id: Optional[str] = None
    run_group: Optional[str] = None
    score: Optional[float] = None
    score_source: Optional[str] = None
    created_at: Optional[str] = None
    relative_output_dir: str
    notes: Optional[str] = None


class UpdateResultRequest(BaseModel):
    """Request to update a result's metadata."""

    run_group: Optional[str] = Field(None, description="Run group tag")


class BestResultsResponse(BaseModel):
    """Response containing ranked architecture results."""

    results: list[BestResultItem]
    total: int


# Prompt file browser schemas
class PromptFileItem(BaseModel):
    """A prompt file discovered in the outputs directory."""

    path: str
    relative_path: str
    preview: str = Field(default="", description="First 300 chars of the file")
    size: int = 0
    modified_at: Optional[str] = None


class PromptFilesResponse(BaseModel):
    """Response containing discovered prompt files."""

    files: list[PromptFileItem]
    total: int


# Prompt generation from document schemas
class GenerateFromDocRequest(BaseModel):
    """Request to generate a bricksmith diagram prompt from an architecture document."""

    document_text: str = Field(..., description="Full text of the architecture document")
    filename: Optional[str] = Field(None, description="Original filename for context")


class GenerateFromDocResponse(BaseModel):
    """Response containing the generated bricksmith diagram prompt."""

    prompt: str = Field(..., description="Generated bricksmith diagram prompt")


# Refinement loop schemas
class EvaluationScores(BaseModel):
    """LLM Judge evaluation scores for a generated diagram."""

    information_hierarchy: int
    technical_accuracy: int
    logo_fidelity: int
    visual_clarity: int
    data_flow_legibility: int
    text_readability: int


class RefinementIterationSchema(BaseModel):
    """A single iteration of the refinement loop."""

    iteration: int
    prompt_used: str
    image_url: str
    image_urls: list[str] = Field(default_factory=list)
    overall_score: Optional[int] = None
    scores: Optional[EvaluationScores] = None
    strengths: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)
    feedback_for_refinement: str = ""
    user_feedback: Optional[str] = None
    refinement_reasoning: Optional[str] = None
    settings_used: Optional["GenerationSettingsRequest"] = None
    created_at: str


class RefinementStateResponse(BaseModel):
    """Current state of a refinement loop for a session."""

    session_id: str
    status: str = Field(description="Status: idle, generating, evaluating, refining")
    original_prompt: str
    current_prompt: str
    current_image_url: Optional[str] = None
    iterations: list[RefinementIterationSchema] = Field(default_factory=list)
    iteration_count: int = 0


class RefinementIterationResponse(BaseModel):
    """Response from a generate-and-evaluate step."""

    success: bool
    iteration: Optional[RefinementIterationSchema] = None
    error: Optional[str] = None


class RefineRequest(BaseModel):
    """Request to refine the current prompt with user feedback."""

    user_feedback: str


class RefineResponse(BaseModel):
    """Response from a prompt refinement step."""

    success: bool
    refined_prompt: Optional[str] = None
    reasoning: Optional[str] = None
    expected_improvement: Optional[str] = None
    error: Optional[str] = None


# Generation settings schemas


class GenerationSettingsRequest(BaseModel):
    """Per-run generation settings for image generation."""

    preset: Optional[str] = Field(
        None, description="Preset: deterministic, conservative, balanced, creative, wild"
    )
    image_size: Optional[str] = Field(None, description="1K, 2K, or 4K")
    aspect_ratio: Optional[str] = Field(None, description="16:9, 1:1, 4:3, 9:16, 3:4, 21:9")
    num_variants: Optional[int] = Field(None, ge=1, le=8)

    def to_generation_kwargs(self) -> dict[str, Any]:
        """Resolve preset + overrides into kwargs for generate_image()."""
        from ...conversation import GENERATION_PRESETS

        kwargs: dict[str, Any] = {}

        if self.preset and self.preset in GENERATION_PRESETS:
            settings = GENERATION_PRESETS[self.preset]
            kwargs["temperature"] = settings.temperature
            kwargs["top_p"] = settings.top_p
            kwargs["top_k"] = settings.top_k
            kwargs["presence_penalty"] = settings.presence_penalty
            kwargs["frequency_penalty"] = settings.frequency_penalty
            kwargs["image_size"] = settings.image_size
            kwargs["aspect_ratio"] = settings.aspect_ratio

        # Explicit overrides take precedence over preset
        if self.image_size is not None:
            kwargs["image_size"] = self.image_size
        if self.aspect_ratio is not None:
            kwargs["aspect_ratio"] = self.aspect_ratio

        return kwargs


class GeneratePreviewRequest(BaseModel):
    """Request body for generate-preview endpoint."""

    settings: Optional[GenerationSettingsRequest] = None


class GenerateAndEvaluateRequest(BaseModel):
    """Request body for refinement generate-and-evaluate endpoint."""

    settings: Optional[GenerationSettingsRequest] = None


class StartStandaloneRefinementRequest(BaseModel):
    """Request to start a standalone refinement loop from a raw prompt."""

    prompt: str = Field(..., description="Raw diagram prompt text")
    image_provider: Optional[Literal["gemini", "openai"]] = None
    openai_api_key: Optional[str] = None
    vertex_api_key: Optional[str] = None
