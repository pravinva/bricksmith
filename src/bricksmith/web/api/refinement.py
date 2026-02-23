"""Standalone refinement loop API endpoints.

Provides a direct prompt -> generate -> evaluate -> refine workflow
without requiring an architect session.
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

from .schemas import (
    GenerateAndEvaluateRequest,
    RefineRequest,
    RefineResponse,
    RefinementIterationResponse,
    RefinementStateResponse,
    StartStandaloneRefinementRequest,
)
from ..services.refinement_service import get_refinement_service

router = APIRouter()


@router.post("/start", response_model=RefinementStateResponse)
async def start_standalone_refinement(
    request: StartStandaloneRefinementRequest,
) -> RefinementStateResponse:
    """Start a standalone refinement loop from a raw prompt."""
    service = get_refinement_service()
    try:
        return await service.start_standalone_refinement(
            prompt=request.prompt,
            image_provider=request.image_provider,
            openai_api_key=request.openai_api_key,
            vertex_api_key=request.vertex_api_key,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{session_id}/generate", response_model=RefinementIterationResponse)
async def generate_and_evaluate(
    session_id: str,
    request: Optional[GenerateAndEvaluateRequest] = None,
) -> RefinementIterationResponse:
    """Generate an image and evaluate it for a standalone refinement session."""
    service = get_refinement_service()
    settings = request.settings if request else None
    return await service.generate_and_evaluate(session_id, settings)


@router.post("/{session_id}/refine", response_model=RefineResponse)
async def refine_prompt(
    session_id: str,
    request: RefineRequest,
) -> RefineResponse:
    """Refine the current prompt with user feedback."""
    service = get_refinement_service()
    return await service.refine_prompt(session_id, request.user_feedback)


@router.get("/{session_id}/state", response_model=RefinementStateResponse)
async def get_state(session_id: str) -> RefinementStateResponse:
    """Get the current refinement state."""
    service = get_refinement_service()
    state = service.get_state(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Refinement session not found")
    return state
