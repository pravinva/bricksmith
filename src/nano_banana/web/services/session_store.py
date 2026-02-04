"""Abstract session store and factory for storage backend selection."""

import os
from abc import ABC, abstractmethod
from typing import Optional

from ..api.schemas import SessionResponse, ArchitectureState


class SessionStore(ABC):
    """Abstract base class for session storage backends."""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the storage backend (create tables, etc.)."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close connections and cleanup resources."""
        pass

    @abstractmethod
    async def create_session(
        self,
        session_id: str,
        initial_problem: str,
        custom_context: Optional[str] = None,
        available_logos: Optional[list[str]] = None,
    ) -> SessionResponse:
        """Create a new session."""
        pass

    @abstractmethod
    async def get_session(self, session_id: str) -> Optional[SessionResponse]:
        """Get a session by ID."""
        pass

    @abstractmethod
    async def list_sessions(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[SessionResponse], int]:
        """List sessions with pagination. Returns (sessions, total_count)."""
        pass

    @abstractmethod
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session by ID. Returns True if deleted."""
        pass

    @abstractmethod
    async def update_session(
        self,
        session_id: str,
        architecture: Optional[dict] = None,
        status: Optional[str] = None,
    ) -> Optional[SessionResponse]:
        """Update session data."""
        pass

    @abstractmethod
    async def add_turn(
        self,
        session_id: str,
        turn_number: int,
        user_input: str,
        architect_response: str,
        architecture_snapshot: Optional[dict] = None,
    ) -> bool:
        """Add a conversation turn to a session."""
        pass

    @abstractmethod
    async def get_turns(self, session_id: str) -> list[dict]:
        """Get all turns for a session."""
        pass

    @abstractmethod
    async def get_full_session_data(self, session_id: str) -> Optional[dict]:
        """Get complete session data including turns and architecture."""
        pass


# Singleton instance
_session_store: Optional[SessionStore] = None


def get_session_store() -> SessionStore:
    """Get or create the session store instance.

    Auto-detects environment:
    - If DATABRICKS_LAKEBASE_URL is set, uses PostgreSQL/Lakebase
    - Otherwise, uses SQLite
    """
    global _session_store

    if _session_store is None:
        if os.environ.get("DATABRICKS_LAKEBASE_URL"):
            from ..db.lakebase import LakebaseSessionStore

            _session_store = LakebaseSessionStore()
        else:
            from ..db.sqlite import SQLiteSessionStore

            _session_store = SQLiteSessionStore()

    return _session_store


def reset_session_store() -> None:
    """Reset the session store singleton (for testing)."""
    global _session_store
    _session_store = None
