"""API endpoints for browsing best generated architectures and prompts."""

import textwrap
from typing import Optional

from fastapi import APIRouter, HTTPException

from .schemas import (
    BestResultItem,
    BestResultsResponse,
    PromptFilesResponse,
    GenerateFromDocRequest,
    GenerateFromDocResponse,
    UpdateResultRequest,
)
from ..services.results_service import get_results_service

router = APIRouter()


@router.get("/prompt-files", response_model=PromptFilesResponse)
async def list_prompt_files(
    query: Optional[str] = None,
    limit: int = 100,
) -> PromptFilesResponse:
    """Return prompt files from the outputs directory."""
    service = get_results_service()
    files = service.list_prompt_files(query=query, limit=limit)
    return PromptFilesResponse(files=files, total=len(files))


_DOC_TO_PROMPT_SYSTEM = textwrap.dedent("""
    You are an expert at writing diagram prompts for Bricksmith, an AI-powered architecture
    diagram generation tool that uses Google Gemini to produce polished, executive-ready
    architecture diagrams.

    A Bricksmith prompt is a structured plain-text file that instructs Gemini exactly how to
    draw the diagram. Good prompts follow this pattern:

    1. PURPOSE — one paragraph: audience, key message, what the diagram communicates.
    2. LOGO KIT — which logos to place and exactly where (top-left, inside a zone, etc.).
       Only reference logos that would be in a customer or Databricks logo kit.
    3. BRAND COLORS — exact hex codes for each zone/element type.
    4. DESIGN PRINCIPLES — style (flat, landscape/portrait), canvas size, title bar content.
    5. LAYOUT — numbered ZONES or SWIM LANES (left-to-right or top-to-bottom) with:
       - Zone/lane header label
       - Components inside (boxes, sub-zones, bullet lists of items)
       - Visual cues (badges, callout boxes, annotations)
    6. DATA FLOW ARROWS — each arrow labeled, colored, with source→destination.
    7. CALLOUT BOXES — key insight panels placed near the relevant zones.
    8. RULES — explicit DO and DO NOT list.

    When writing the prompt:
    - Be specific enough that Gemini can draw it without guessing.
    - Use exact color hex codes, not vague words like "blue".
    - Name every component box, its label, and its sub-items.
    - Describe arrows with source, destination, label, color, and style (solid/dashed/dotted).
    - Reference the customer/vendor logo correctly (e.g. "AGL Energy logo: cyan/teal rays").
    - Keep it scannable with headers and bullet points.
    - The prompt should be complete enough to run `bricksmith generate-raw` or
      `bricksmith chat --prompt-file` with it directly.

    Output ONLY the prompt text. No preamble, no explanation, no markdown code fences.
""").strip()


@router.post("/from-document", response_model=GenerateFromDocResponse)
async def generate_prompt_from_doc(request: GenerateFromDocRequest) -> GenerateFromDocResponse:
    """Generate a Bricksmith diagram prompt from an architecture document.

    Takes any architecture, design, or requirements document and uses Gemini to
    produce a ready-to-use bricksmith diagram prompt in the expected format.
    """
    from ...gemini_client import GeminiClient
    from ...config import load_config

    try:
        config = load_config()
        client = GeminiClient(api_key=config.gemini_api_key or None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialise Gemini client: {e}")

    filename_hint = f"\nSource file: {request.filename}\n" if request.filename else ""
    full_prompt = f"""{_DOC_TO_PROMPT_SYSTEM}

---

Convert the following architecture document into a Bricksmith diagram prompt.
{filename_hint}
ARCHITECTURE DOCUMENT:
{request.document_text}

---

Write the Bricksmith diagram prompt now:"""

    try:
        generated = client.generate_text(full_prompt, temperature=0.3, max_output_tokens=4096)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gemini generation failed: {e}")

    return GenerateFromDocResponse(prompt=generated.strip())


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


@router.patch("/{result_id:path}", response_model=BestResultItem)
async def update_result(
    result_id: str,
    request: UpdateResultRequest,
) -> BestResultItem:
    """Update a result's metadata (e.g. run_group tag)."""
    service = get_results_service()
    updated = service.update_result(result_id, run_group=request.run_group)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Result not found: {result_id}")
    return updated
