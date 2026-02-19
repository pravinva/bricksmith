"""API endpoints for mirroring CLI functionality."""

from fastapi import APIRouter, HTTPException

from .schemas import (
    CLICommandsResponse,
    CliJobResponse,
    StartCliJobRequest,
    StartCliJobResponse,
)
from ..services.cli_runner_service import get_cli_runner_service

router = APIRouter()


@router.get("/commands", response_model=CLICommandsResponse)
async def list_commands() -> CLICommandsResponse:
    """List CLI commands exposed by the web command runner."""
    service = get_cli_runner_service()
    return CLICommandsResponse(commands=service.list_supported_commands())


@router.post("/jobs", response_model=StartCliJobResponse)
async def start_job(request: StartCliJobRequest) -> StartCliJobResponse:
    """Start a CLI command in the background."""
    service = get_cli_runner_service()
    try:
        job = await service.start_job(
            command=request.command,
            args=request.args,
            stdin_text=request.stdin_text,
            timeout_seconds=request.timeout_seconds,
        )
        return StartCliJobResponse(job=job)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/jobs", response_model=list[CliJobResponse])
async def list_jobs() -> list[CliJobResponse]:
    """List recent CLI jobs."""
    service = get_cli_runner_service()
    return await service.list_jobs()


@router.get("/jobs/{job_id}", response_model=CliJobResponse)
async def get_job(job_id: str) -> CliJobResponse:
    """Get details for one CLI job."""
    service = get_cli_runner_service()
    job = await service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.delete("/jobs/{job_id}", response_model=CliJobResponse)
async def cancel_job(job_id: str) -> CliJobResponse:
    """Cancel a running CLI job."""
    service = get_cli_runner_service()
    job = await service.cancel_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
