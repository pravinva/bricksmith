"""API endpoints for browsing best generated architectures and prompts."""

from typing import Optional

from fastapi import APIRouter

from .schemas import BestResultsResponse
from ..services.results_service import get_results_service

router = APIRouter()


@router.get("/best", response_model=BestResultsResponse)
async def list_best_results(
    limit: int = 30,
    query: Optional[str] = None,
    min_score: Optional[float] = None,
    include_prompt: bool = False,
) -> BestResultsResponse:
    """Return ranked architecture outputs with their associated prompts."""
    service = get_results_service()
    results = service.list_best_results(
        limit=limit,
        query=query,
        min_score=min_score,
        include_prompt=include_prompt,
    )
    return BestResultsResponse(results=results, total=len(results))
