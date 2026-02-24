"""Chat/conversation API endpoints."""

import logging

from fastapi import APIRouter, HTTPException

from .schemas import (
    SendMessageRequest,
    MessageResponse,
    StatusResponse,
    GenerateOutputRequest,
    GenerateOutputResponse,
    GenerateAndEvaluateRequest,
    GeneratePreviewRequest,
    GeneratePreviewResponse,
    TurnSchema,
    TurnsResponse,
    RefineRequest,
    RefineResponse,
    RefinementIterationResponse,
    RefinementStateResponse,
)
from ..services.architect_service import get_architect_service
from ..services.refinement_service import get_refinement_service
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
            image_base64=request.image_base64,
            image_filename=request.image_filename,
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
async def generate_preview(
    session_id: str,
    request: GeneratePreviewRequest = None,
) -> GeneratePreviewResponse:
    """Generate a diagram preview image from the current architecture state.

    This endpoint uses GeminiClient to generate an actual diagram image based on
    the current architecture components and connections.

    Args:
        session_id: Session ID
        request: Optional generation settings

    Returns:
        GeneratePreviewResponse with image URL and run ID

    Raises:
        HTTPException: If session not found
    """
    service = get_architect_service()
    settings_req = request.settings if request else None
    response = await service.generate_preview(session_id, settings_req=settings_req)

    if response.error == "Session not found":
        raise HTTPException(status_code=404, detail="Session not found")

    return response


# --- Refinement loop endpoints ---


@router.post("/{session_id}/refinement/start", response_model=RefinementStateResponse)
async def start_refinement(session_id: str) -> RefinementStateResponse:
    """Start a refinement loop from the current architect session state.

    Initializes the refinement service with the diagram prompt built from the
    session's current architecture.
    """
    service = get_refinement_service()
    try:
        return await service.start_refinement(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Error starting refinement for %s: %s", session_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/refinement/generate", response_model=RefinementIterationResponse)
async def generate_and_evaluate(
    session_id: str,
    request: GenerateAndEvaluateRequest = None,
) -> RefinementIterationResponse:
    """Generate a diagram image and evaluate it with the LLM Judge.

    This generates the image from the current prompt, then runs evaluation
    to produce scores, strengths, issues, and improvement suggestions.
    """
    service = get_refinement_service()
    try:
        settings_req = request.settings if request else None
        return await service.generate_and_evaluate(session_id, settings_req=settings_req)
    except Exception as e:
        logger.error("Error in generate_and_evaluate for %s: %s", session_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/refinement/refine", response_model=RefineResponse)
async def refine_prompt(session_id: str, request: RefineRequest) -> RefineResponse:
    """Refine the current prompt using DSPy with optional user feedback.

    Takes user feedback and uses ConversationalRefiner to produce an improved
    prompt for the next generation cycle.
    """
    service = get_refinement_service()
    try:
        return await service.refine_prompt(session_id, request.user_feedback)
    except Exception as e:
        logger.error("Error in refine_prompt for %s: %s", session_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/refinement/state", response_model=RefinementStateResponse)
async def get_refinement_state(session_id: str) -> RefinementStateResponse:
    """Get the current refinement state for a session."""
    service = get_refinement_service()
    state = service.get_state(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="No refinement in progress for this session")
    return state
