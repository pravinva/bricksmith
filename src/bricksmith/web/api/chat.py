"""Chat/conversation API endpoints."""

import logging

from fastapi import APIRouter, HTTPException

from .schemas import (
    SendMessageRequest,
    MessageResponse,
    StatusResponse,
    GenerateOutputRequest,
    GenerateOutputResponse,
    GeneratePreviewResponse,
    TurnSchema,
    TurnsResponse,
)
from ..services.architect_service import get_architect_service
from ..services.session_store import get_session_store

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/{session_id}/message", response_model=MessageResponse)
async def send_message(
    session_id: str,
    request: SendMessageRequest,
) -> MessageResponse:
    """Send a message in a session and get the AI response.

    Args:
        session_id: Session ID
        request: Message request containing user message

    Returns:
        AI response with updated architecture state

    Raises:
        HTTPException: If session not found
    """
    service = get_architect_service()
    try:
        response = await service.send_message(
            session_id=session_id,
            message=request.message,
        )
    except Exception as e:
        logger.error("Error in send_message for %s: %s", session_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    if response is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return response


@router.get("/{session_id}/status", response_model=StatusResponse)
async def get_status(session_id: str) -> StatusResponse:
    """Get the current architecture status for a session.

    Args:
        session_id: Session ID

    Returns:
        Current architecture status and state

    Raises:
        HTTPException: If session not found
    """
    service = get_architect_service()
    status = await service.get_status(session_id)

    if status is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return status


@router.get("/{session_id}/turns", response_model=TurnsResponse)
async def get_turns(session_id: str) -> TurnsResponse:
    """Get all conversation turns for a session.

    Args:
        session_id: Session ID

    Returns:
        List of conversation turns

    Raises:
        HTTPException: If session not found
    """
    store = get_session_store()
    session = await store.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    turns_data = await store.get_turns(session_id)
    turns = [TurnSchema(**turn) for turn in turns_data]
    return TurnsResponse(turns=turns)


@router.post("/{session_id}/output", response_model=GenerateOutputResponse)
async def generate_output(
    session_id: str,
    request: GenerateOutputRequest = None,
) -> GenerateOutputResponse:
    """Generate the final diagram prompt for a session.

    This finalizes the architecture design and saves:
    - session.json: Full session history
    - prompt.txt: Diagram prompt for generate-raw
    - architecture.json: Final architecture definition
    - rationale.txt: AI's reasoning for the design

    Args:
        session_id: Session ID
        request: Optional output configuration

    Returns:
        Output generation result with file paths

    Raises:
        HTTPException: If session not found
    """
    service = get_architect_service()

    output_dir = None
    if request and request.output_dir:
        output_dir = request.output_dir

    response = await service.generate_output(
        session_id=session_id,
        output_dir=output_dir,
    )

    if response.error == "Session not found":
        raise HTTPException(status_code=404, detail="Session not found")

    return response


@router.post("/{session_id}/generate-preview", response_model=GeneratePreviewResponse)
async def generate_preview(session_id: str) -> GeneratePreviewResponse:
    """Generate a diagram preview image from the current architecture state.

    This endpoint uses GeminiClient to generate an actual diagram image based on
    the current architecture components and connections.

    Args:
        session_id: Session ID

    Returns:
        GeneratePreviewResponse with image URL and run ID

    Raises:
        HTTPException: If session not found
    """
    service = get_architect_service()
    response = await service.generate_preview(session_id)

    if response.error == "Session not found":
        raise HTTPException(status_code=404, detail="Session not found")

    return response
