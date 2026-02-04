"""Pydantic request/response schemas for the web API."""

from datetime import datetime
from typing import Optional

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


# Session schemas
class CreateSessionRequest(BaseModel):
    """Request to create a new architect session."""

    initial_problem: str = Field(
        ..., description="Description of the architecture problem to solve"
    )
    custom_context: Optional[str] = Field(
        None, description="Additional context or requirements"
    )
    logo_dir: Optional[str] = Field(
        None, description="Path to logo directory (defaults to logos/default)"
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
    run_id: Optional[str] = Field(None, description="Identifier for this generation run")
    error: Optional[str] = None


# Error response
class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str
    error_code: Optional[str] = None
