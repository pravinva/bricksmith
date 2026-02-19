"""Regression tests for ArchitectService edge cases."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from bricksmith.web.api.schemas import SessionResponse
from bricksmith.web.services.architect_service import ArchitectService


class _FakeLogo:
    def __init__(self, name: str):
        self.name = name


class _FakeLogoHandler:
    def __init__(self):
        self.paths_seen: list[Path] = []

    def load_logo_kit(self, logo_dir: Path):
        assert isinstance(logo_dir, Path)
        self.paths_seen.append(logo_dir)
        return [_FakeLogo("databricks")]

    def load_logo_hints(self, logo_dir: Path):
        assert isinstance(logo_dir, Path)
        self.paths_seen.append(logo_dir)
        return {}


class _FakeChatbot:
    def __init__(self, config, arch_config):
        self.logo_handler = _FakeLogoHandler()
        self._session = None
        self._logos = []
        self._logo_names = []
        self._custom_context = ""


class _FakeStore:
    async def create_session(
        self,
        session_id: str,
        initial_problem: str,
        custom_context: str | None = None,
        available_logos: list[str] | None = None,
    ) -> SessionResponse:
        return SessionResponse(
            session_id=session_id,
            initial_problem=initial_problem,
            status="active",
            created_at="2026-01-01T00:00:00",
            turn_count=0,
            current_architecture=None,
        )


@pytest.mark.anyio
async def test_create_session_passes_path_to_logo_loader(monkeypatch):
    """create_session should pass Path objects to logo loading APIs."""
    fake_config = SimpleNamespace(
        logo_kit=SimpleNamespace(logo_dir=Path("logos/default")),
        image_provider=SimpleNamespace(provider="gemini", openai_model="gpt-image-1"),
    )

    monkeypatch.setattr(
        "bricksmith.web.services.architect_service.load_config",
        lambda: fake_config,
    )
    monkeypatch.setattr(
        "bricksmith.web.services.architect_service.ArchitectChatbot",
        _FakeChatbot,
    )
    monkeypatch.setattr(
        "bricksmith.web.services.architect_service.get_session_store",
        lambda: _FakeStore(),
    )

    service = ArchitectService()
    response = await service.create_session(initial_problem="Test problem")

    assert response.initial_problem == "Test problem"
