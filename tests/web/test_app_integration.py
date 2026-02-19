"""Integration tests for the Bricksmith web app."""

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from bricksmith.web.main import create_app
from bricksmith.web.services import architect_service as architect_service_module
from bricksmith.web.services import results_service as results_service_module
from bricksmith.web.services import session_store as session_store_module
from bricksmith.web.db.sqlite import SQLiteSessionStore


@pytest.fixture()
def isolated_sqlite_store(tmp_path: Path):
    """Use a temporary SQLite session store for each test."""
    session_store_module.reset_session_store()
    architect_service_module._architect_service = None

    store = SQLiteSessionStore(db_path=str(tmp_path / "sessions.db"))
    session_store_module._session_store = store

    yield store

    session_store_module.reset_session_store()
    architect_service_module._architect_service = None


def test_list_sessions_handles_malformed_architecture(isolated_sqlite_store: SQLiteSessionStore):
    """`/api/sessions` should not 500 if one stored row has malformed architecture JSON."""
    app = create_app()
    with TestClient(app) as client:
        conn = sqlite3.connect(isolated_sqlite_store.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        now = datetime.now(timezone.utc).isoformat()
        cursor.execute(
            """
            INSERT INTO sessions
                (session_id, initial_problem, current_architecture, status, created_at, updated_at)
            VALUES
                (?, ?, ?, ?, ?, ?)
            """,
            (
                "badarch01",
                "Broken architecture row",
                '{"components":"not-a-list","connections":[]}',
                "active",
                now,
                now,
            ),
        )
        conn.commit()
        conn.close()

        response = client.get("/api/sessions")
        assert response.status_code == 200

        payload = response.json()
        assert payload["total"] == 1
        assert payload["sessions"][0]["session_id"] == "badarch01"
        assert payload["sessions"][0]["current_architecture"] is None


def test_root_serves_existing_built_assets():
    """Production index should only reference assets that can be served."""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "frontend" / "dist" / "index.html"
    if not index_path.exists():
        pytest.skip("frontend/dist/index.html not present")

    app = create_app()
    with TestClient(app) as client:
        index_response = client.get("/")
        assert index_response.status_code == 200

        html = index_response.text
        asset_paths = re.findall(r'(?:src|href)="(/assets/[^"]+)"', html)
        assert asset_paths, "Expected built asset references in index.html"

        for asset_path in asset_paths:
            asset_response = client.get(asset_path)
            assert asset_response.status_code == 200, f"Missing built asset: {asset_path}"


def test_best_results_reads_chat_prompt_file_fallback(tmp_path: Path, monkeypatch):
    """Best-results API should fallback to prompt file when prompt_used is empty."""
    monkeypatch.chdir(tmp_path)
    results_service_module._results_service = None

    outputs_dir = tmp_path / "outputs" / "2026-02-10" / "chat-prompt"
    outputs_dir.mkdir(parents=True)

    prompt_text = "Design a medallion architecture with Unity Catalog governance."
    (outputs_dir / "iteration_9_prompt.txt").write_text(prompt_text)
    (outputs_dir / "iteration_9.png").write_bytes(b"png-bytes")
    (outputs_dir / "session.json").write_text(
        json.dumps(
            {
                "turns": [
                    {
                        "iteration": 9,
                        "image_path": str(outputs_dir / "iteration_9.png"),
                        "prompt_used": "",
                        "timestamp": "2026-02-10T12:00:00",
                    }
                ]
            }
        )
    )

    app = create_app()
    with TestClient(app) as client:
        response = client.get("/api/results/best?include_prompt=true")
        assert response.status_code == 200
        payload = response.json()
        assert payload["total"] == 1
        result = payload["results"][0]
        assert result["prompt_path"].endswith("iteration_9_prompt.txt")
        assert result["prompt_preview"].startswith("Design a medallion architecture")
        assert result["full_prompt"] == prompt_text
