"""Session CRUD API endpoints."""

from fastapi import APIRouter, HTTPException

from .schemas import (
    CreateSessionRequest,
    SessionResponse,
    SessionListResponse,
)
from ..services.architect_service import get_architect_service

router = APIRouter()


@router.post("", response_model=SessionResponse)
async def create_session(request: CreateSessionRequest) -> SessionResponse:
    """Create a new architect session.

    Args:
        request: Session creation request with problem description

    Returns:
        Created session details
    """
    service = get_architect_service()
    session = await service.create_session(
        initial_problem=request.initial_problem,
        custom_context=request.custom_context,
        logo_dir=request.logo_dir,
    )
    return session


@router.get("", response_model=SessionListResponse)
async def list_sessions(
    limit: int = 50,
    offset: int = 0,
) -> SessionListResponse:
    """List all sessions with pagination.

    Args:
        limit: Maximum number of sessions to return
        offset: Number of sessions to skip

    Returns:
        List of sessions and total count
    """
    service = get_architect_service()
    sessions, total = await service.list_sessions(limit=limit, offset=offset)
    return SessionListResponse(sessions=sessions, total=total)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str) -> SessionResponse:
    """Get a session by ID.

    Args:
        session_id: Session ID

    Returns:
        Session details

    Raises:
        HTTPException: If session not found
    """
    service = get_architect_service()
    session = await service.get_session(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.delete("/{session_id}")
async def delete_session(session_id: str) -> dict:
    """Delete a session.

    Args:
        session_id: Session ID

    Returns:
        Success confirmation

    Raises:
        HTTPException: If session not found
    """
    service = get_architect_service()
    deleted = await service.delete_session(session_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"status": "deleted", "session_id": session_id}
