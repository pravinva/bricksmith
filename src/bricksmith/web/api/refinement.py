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
    UpdatePromptRequest,
    UpdatePromptResponse,
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
            prompt_file=request.prompt_file,
            image_provider=request.image_provider,
            gemini_model=request.gemini_model,
            openai_api_key=request.openai_api_key,
            vertex_api_key=request.vertex_api_key,
            persona=request.persona,
            aspect_ratio=request.aspect_ratio,
            image_size=request.image_size,
            folder=request.folder,
            num_variants=request.num_variants,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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
    return await service.refine_prompt(
        session_id, request.user_feedback, user_score=request.user_score
    )


@router.post("/{session_id}/update-prompt", response_model=UpdatePromptResponse)
async def update_prompt(
    session_id: str,
    request: UpdatePromptRequest,
) -> UpdatePromptResponse:
    """Directly update the current prompt without DSPy refinement."""
    service = get_refinement_service()
    success = await service.update_prompt(session_id, request.prompt)
    if not success:
        raise HTTPException(status_code=404, detail="Refinement session not found")
    state = service.get_state(session_id)
    return UpdatePromptResponse(
        success=True,
        current_prompt=state.current_prompt if state else "",
    )


@router.get("/{session_id}/state", response_model=RefinementStateResponse)
async def get_state(session_id: str) -> RefinementStateResponse:
    """Get the current refinement state."""
    service = get_refinement_service()
    state = service.get_state(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Refinement session not found")
    return state
