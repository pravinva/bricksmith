"""Service for running bricksmith CLI commands from the web app."""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from ..api.schemas import CLICommandSpec, CliJobResponse


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CliJob:
    """In-memory representation of an async CLI execution."""

    job_id: str
    command: str
    args: list[str]
    timeout_seconds: int
    status: str = "queued"
    started_at: str = field(default_factory=_utc_now_iso)
    ended_at: Optional[str] = None
    exit_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    process: Optional[asyncio.subprocess.Process] = None

    def to_response(self) -> CliJobResponse:
        return CliJobResponse(
            job_id=self.job_id,
            status=self.status,
            command=self.command,
            args=self.args,
            started_at=self.started_at,
            ended_at=self.ended_at,
            exit_code=self.exit_code,
            stdout=self.stdout,
            stderr=self.stderr,
            timeout_seconds=self.timeout_seconds,
        )


class CliRunnerService:
    """Runs CLI commands in background jobs and tracks output."""

    REPO_ROOT = Path(__file__).resolve().parents[4]
    MAX_JOB_HISTORY = 100
    SUPPORTED_COMMANDS: list[CLICommandSpec] = [
        CLICommandSpec(
            name="evaluate",
            description="Evaluate a generated diagram run",
            examples=[
                "evaluate <run_id> --eval-file evaluations/example.json",
            ],
        ),
        CLICommandSpec(
            name="list-runs",
            description="List MLflow runs",
            examples=["list-runs --max-results 20"],
        ),
        CLICommandSpec(
            name="show-run",
            description="Show run details",
            examples=["show-run <run_id>"],
        ),
        CLICommandSpec(
            name="generate-raw",
            description="Generate diagram(s) from prompt file",
            examples=[
                "generate-raw --prompt-file prompts/example.txt --logo-dir logos/default",
            ],
        ),
        CLICommandSpec(
            name="validate-logos",
            description="Validate a logo kit directory",
            examples=["validate-logos --logo-dir logos/default"],
        ),
        CLICommandSpec(
            name="refine",
            description="Regenerate a prior run with feedback",
            examples=["refine <run_id> --feedback 'logos too small'"],
        ),
        CLICommandSpec(
            name="refine-prompt",
            description="Analyze and improve a prompt",
            examples=["refine-prompt --run-id <run_id> --feedback 'clearer flow needed'"],
        ),
        CLICommandSpec(
            name="chat",
            description="Run iterative chat workflow",
            examples=["chat --prompt-file prompts/example.txt --auto-refine --target-score 8"],
            supports_stdin=True,
        ),
        CLICommandSpec(
            name="architect",
            description="Run architecture design workflow",
            examples=["architect --problem 'Design lakehouse for retail analytics'"],
            supports_stdin=True,
        ),
        CLICommandSpec(
            name="web",
            description="Start web server command (generally not needed here)",
            examples=["web --port 8080"],
        ),
    ]

    def __init__(self) -> None:
        self._jobs: dict[str, CliJob] = {}
        self._lock = asyncio.Lock()

    def list_supported_commands(self) -> list[CLICommandSpec]:
        return self.SUPPORTED_COMMANDS

    async def list_jobs(self) -> list[CliJobResponse]:
        async with self._lock:
            jobs = list(self._jobs.values())
        jobs.sort(key=lambda j: j.started_at, reverse=True)
        return [job.to_response() for job in jobs]

    async def get_job(self, job_id: str) -> Optional[CliJobResponse]:
        async with self._lock:
            job = self._jobs.get(job_id)
        return job.to_response() if job else None

    async def cancel_job(self, job_id: str) -> Optional[CliJobResponse]:
        async with self._lock:
            job = self._jobs.get(job_id)

        if not job:
            return None

        if job.process and job.status in {"queued", "running"}:
            job.process.terminate()
            job.status = "cancelled"
            job.ended_at = _utc_now_iso()
        return job.to_response()

    async def start_job(
        self,
        command: str,
        args: list[str],
        stdin_text: Optional[str] = None,
        timeout_seconds: int = 1800,
    ) -> CliJobResponse:
        supported = {spec.name for spec in self.SUPPORTED_COMMANDS}
        if command not in supported:
            raise ValueError(f"Unsupported command '{command}'")

        job_id = str(uuid.uuid4())[:8]
        job = CliJob(
            job_id=job_id,
            command=command,
            args=args,
            timeout_seconds=timeout_seconds,
        )

        async with self._lock:
            self._jobs[job_id] = job
            self._trim_job_history_locked()

        asyncio.create_task(self._run_job(job_id, stdin_text))
        return job.to_response()

    def _trim_job_history_locked(self) -> None:
        if len(self._jobs) <= self.MAX_JOB_HISTORY:
            return
        sorted_jobs = sorted(self._jobs.values(), key=lambda j: j.started_at, reverse=True)
        keep_ids = {j.job_id for j in sorted_jobs[: self.MAX_JOB_HISTORY]}
        self._jobs = {job_id: job for job_id, job in self._jobs.items() if job_id in keep_ids}

    async def _run_job(self, job_id: str, stdin_text: Optional[str]) -> None:
        async with self._lock:
            job = self._jobs.get(job_id)
        if not job:
            return

        job.status = "running"
        cmd = ["uv", "run", "bricksmith", job.command, *job.args]

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(self.REPO_ROOT),
                stdin=asyncio.subprocess.PIPE if stdin_text is not None else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            job.process = process

            input_bytes = stdin_text.encode("utf-8") if stdin_text is not None else None
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(input=input_bytes),
                    timeout=job.timeout_seconds,
                )
                job.stdout = stdout.decode("utf-8", errors="replace")
                job.stderr = stderr.decode("utf-8", errors="replace")
                job.exit_code = process.returncode
                job.status = "succeeded" if process.returncode == 0 else "failed"
            except TimeoutError:
                process.kill()
                await process.wait()
                job.exit_code = process.returncode
                job.status = "timeout"
                job.stderr = (
                    f"Command exceeded timeout ({job.timeout_seconds}s) and was terminated.\n"
                )
        except Exception as exc:
            job.status = "failed"
            job.stderr = str(exc)
        finally:
            job.process = None
            job.ended_at = _utc_now_iso()


_cli_runner_service: Optional[CliRunnerService] = None


def get_cli_runner_service() -> CliRunnerService:
    """Return singleton CLI runner service."""
    global _cli_runner_service
    if _cli_runner_service is None:
        _cli_runner_service = CliRunnerService()
    return _cli_runner_service
