"""Service for discovering and ranking best generated architectures."""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..api.schemas import BestResultItem, PromptFileItem


@dataclass
class _ResultCandidate:
    """Intermediate result representation before schema conversion."""

    source: str
    title: str
    image_path: Optional[Path]
    prompt_path: Optional[Path]
    prompt_text: str
    run_id: Optional[str]
    run_group: Optional[str]
    score: Optional[float]
    score_source: Optional[str]
    created_at: Optional[str]
    output_dir: Path
    notes: Optional[str]


class ResultsService:
    """Builds ranked list of generated architecture outputs."""

    OUTPUTS_DIR = Path("outputs")

    def list_prompt_files(
        self,
        query: Optional[str] = None,
        limit: int = 100,
    ) -> list[PromptFileItem]:
        """List prompt files from the outputs directory.

        Args:
            query: Optional search filter on filename or content preview
            limit: Maximum number of results

        Returns:
            List of PromptFileItem sorted by modification time descending
        """
        if not self.OUTPUTS_DIR.exists():
            return []

        candidates: list[PromptFileItem] = []
        for path in self.OUTPUTS_DIR.rglob("*prompt*.txt"):
            if not path.is_file():
                continue

            try:
                relative = path.relative_to(self.OUTPUTS_DIR).as_posix()
            except ValueError:
                relative = path.as_posix()

            preview = self._safe_read_text(path)[:300]
            stat = path.stat()

            candidates.append(
                PromptFileItem(
                    path=str(path),
                    relative_path=relative,
                    preview=preview.strip().replace("\n", " "),
                    size=stat.st_size,
                    modified_at=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                )
            )

        # Filter by query
        if query:
            needle = query.lower().strip()
            candidates = [
                c
                for c in candidates
                if needle in c.relative_path.lower() or needle in c.preview.lower()
            ]

        # Sort by modified_at descending
        candidates.sort(key=lambda c: c.modified_at or "", reverse=True)

        return candidates[:limit]

    def list_best_results(
        self,
        limit: int = 30,
        query: Optional[str] = None,
        min_score: Optional[float] = None,
        include_prompt: bool = False,
    ) -> list[BestResultItem]:
        candidates = self._collect_candidates()

        if query:
            needle = query.lower().strip()
            candidates = [
                c
                for c in candidates
                if needle in c.title.lower()
                or needle in c.prompt_text.lower()
                or (c.notes and needle in c.notes.lower())
                or (c.run_id and needle in c.run_id.lower())
                or (c.run_group and needle in c.run_group.lower())
            ]

        if min_score is not None:
            candidates = [c for c in candidates if c.score is not None and c.score >= min_score]

        candidates.sort(
            key=lambda c: (
                c.score is not None,
                c.score if c.score is not None else -1.0,
                c.created_at or "",
            ),
            reverse=True,
        )

        limited = candidates[:limit]
        return [self._to_item(c, include_prompt=include_prompt) for c in limited]

    def _collect_candidates(self) -> list[_ResultCandidate]:
        if not self.OUTPUTS_DIR.exists():
            return []

        candidates: list[_ResultCandidate] = []
        candidates.extend(self._collect_chat_candidates())
        candidates.extend(self._collect_metadata_candidates())
        return candidates

    def _collect_chat_candidates(self) -> list[_ResultCandidate]:
        candidates: list[_ResultCandidate] = []
        for session_file in self.OUTPUTS_DIR.rglob("session.json"):
            parent_name = session_file.parent.name
            if not parent_name.startswith("chat-"):
                continue

            data = self._read_json(session_file)
            if not data:
                continue

            turns = data.get("turns", [])
            for turn in turns:
                image_path_str = turn.get("image_path")
                if not image_path_str:
                    continue

                image_path = Path(image_path_str)
                prompt_text = str(turn.get("prompt_used") or "")
                score = self._to_float(turn.get("score"))
                iteration = turn.get("iteration")
                title = f"{parent_name} iteration {iteration}" if iteration else parent_name

                # Try to resolve prompt file if present
                prompt_path = None
                if iteration is not None:
                    candidate_prompt = session_file.parent / f"iteration_{iteration}_prompt.txt"
                    if candidate_prompt.exists():
                        prompt_path = candidate_prompt
                if prompt_path is None and (session_file.parent / "prompt.txt").exists():
                    prompt_path = session_file.parent / "prompt.txt"

                # Some historical chat sessions did not persist prompt_used in turn data.
                # Fall back to the iteration prompt file so the UI can still show prompt text.
                if not prompt_text and prompt_path and prompt_path.exists():
                    prompt_text = self._safe_read_text(prompt_path)

                candidates.append(
                    _ResultCandidate(
                        source="chat",
                        title=title,
                        image_path=image_path if image_path.exists() else None,
                        prompt_path=prompt_path,
                        prompt_text=prompt_text,
                        run_id=turn.get("run_id"),
                        run_group=None,
                        score=score,
                        score_source="chat_score" if score is not None else None,
                        created_at=turn.get("timestamp"),
                        output_dir=session_file.parent,
                        notes=turn.get("feedback"),
                    )
                )
        return candidates

    def _collect_metadata_candidates(self) -> list[_ResultCandidate]:
        candidates: list[_ResultCandidate] = []
        for metadata_file in self.OUTPUTS_DIR.rglob("metadata*.json"):
            data = self._read_json(metadata_file)
            if not data:
                continue

            output_dir = metadata_file.parent
            run_id = data.get("run_id")
            run_name = data.get("run_name") or output_dir.name
            run_group = data.get("run_group")
            if run_group is None and isinstance(data.get("tags"), dict):
                tags = data.get("tags") or {}
                run_group = tags.get("run_group") or tags.get("group")

            prompt_path = None
            prompt_file_field = data.get("prompt_file")
            if isinstance(prompt_file_field, str):
                prompt_candidate = Path(prompt_file_field)
                if prompt_candidate.exists():
                    prompt_path = prompt_candidate
            if prompt_path is None and (output_dir / "prompt.txt").exists():
                prompt_path = output_dir / "prompt.txt"

            prompt_text = ""
            if prompt_path and prompt_path.exists():
                prompt_text = self._safe_read_text(prompt_path)

            # Try to infer image from matching metadata naming convention
            image_path = self._resolve_image_for_metadata(metadata_file, output_dir)

            score = None
            score_source = None
            feedback_score, feedback_source = self._resolve_feedback_score(
                metadata_file, output_dir
            )
            if feedback_score is not None:
                score = feedback_score
                score_source = feedback_source

            source = "refine" if str(run_name).startswith("refine-") else "generate_raw"

            candidates.append(
                _ResultCandidate(
                    source=source,
                    title=str(run_name),
                    image_path=image_path,
                    prompt_path=prompt_path,
                    prompt_text=prompt_text,
                    run_id=run_id,
                    run_group=str(run_group) if run_group else None,
                    score=score,
                    score_source=score_source,
                    created_at=data.get("timestamp"),
                    output_dir=output_dir,
                    notes=None,
                )
            )
        return candidates

    def _resolve_image_for_metadata(self, metadata_file: Path, output_dir: Path) -> Optional[Path]:
        stem = metadata_file.stem.replace("metadata_", "")
        candidate = output_dir / f"diagram_{stem}.png"
        if candidate.exists():
            return candidate

        diagrams = sorted(output_dir.glob("diagram*.png"))
        return diagrams[-1] if diagrams else None

    def _resolve_feedback_score(
        self, metadata_file: Path, output_dir: Path
    ) -> tuple[Optional[float], Optional[str]]:
        stem = metadata_file.stem.replace("metadata_", "")
        parts = stem.split("_")
        if not parts:
            return None, None
        feedback_file = output_dir / f"feedback_{parts[0]}.json"
        if not feedback_file.exists():
            return None, None
        data = self._read_json(feedback_file)
        if not data:
            return None, None
        score = self._to_float(data.get("score"))
        if score is None:
            return None, None
        return score, "feedback_score"

    def _to_item(self, candidate: _ResultCandidate, include_prompt: bool) -> BestResultItem:
        prompt_preview = candidate.prompt_text.strip().replace("\n", " ")[:320]
        image_url = None
        if candidate.image_path:
            try:
                relative = candidate.image_path.relative_to(self.OUTPUTS_DIR)
                image_url = f"/api/images/{relative.as_posix()}"
            except ValueError:
                image_url = None

        prompt_path_str = str(candidate.prompt_path) if candidate.prompt_path else None
        image_path_str = str(candidate.image_path) if candidate.image_path else None

        try:
            rel_output_dir = candidate.output_dir.relative_to(self.OUTPUTS_DIR).as_posix()
        except ValueError:
            rel_output_dir = candidate.output_dir.as_posix()

        result_id = (
            f"{candidate.source}:{candidate.run_id or candidate.title}:{candidate.created_at or ''}"
        )

        return BestResultItem(
            result_id=result_id,
            source=(
                candidate.source
                if candidate.source in {"chat", "generate_raw", "refine"}
                else "unknown"
            ),
            title=candidate.title,
            image_path=image_path_str,
            image_url=image_url,
            prompt_path=prompt_path_str,
            prompt_preview=prompt_preview,
            full_prompt=candidate.prompt_text if include_prompt else None,
            run_id=candidate.run_id,
            run_group=candidate.run_group,
            score=candidate.score,
            score_source=candidate.score_source,
            created_at=candidate.created_at,
            relative_output_dir=rel_output_dir,
            notes=candidate.notes,
        )

    def _read_json(self, path: Path) -> Optional[dict]:
        try:
            return json.loads(path.read_text())
        except Exception:
            return None

    def _safe_read_text(self, path: Path) -> str:
        try:
            return path.read_text()
        except Exception:
            return ""

    def _to_float(self, value: object) -> Optional[float]:
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None


_results_service: Optional[ResultsService] = None


def get_results_service() -> ResultsService:
    """Return singleton results service."""
    global _results_service
    if _results_service is None:
        _results_service = ResultsService()
    return _results_service
