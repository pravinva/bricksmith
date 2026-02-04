"""SQLite implementation of the session store."""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..api.schemas import SessionResponse, ArchitectureState
from ..services.session_store import SessionStore


class SQLiteSessionStore(SessionStore):
    """SQLite-based session storage for local development."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize the SQLite store.

        Args:
            db_path: Path to the SQLite database file.
                     Defaults to ~/.nano_banana/sessions.db
        """
        if db_path is None:
            db_dir = Path.home() / ".nano_banana"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(db_dir / "sessions.db")

        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    def _get_connection(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    async def initialize(self) -> None:
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                initial_problem TEXT NOT NULL,
                current_architecture TEXT,
                available_logos TEXT,
                custom_context TEXT,
                status TEXT DEFAULT 'active',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
        """)

        # Create turns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                turn_number INTEGER NOT NULL,
                user_input TEXT NOT NULL,
                architect_response TEXT NOT NULL,
                architecture_snapshot TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
                UNIQUE(session_id, turn_number)
            )
        """)

        # Create index for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_turns_session_id ON turns(session_id)
        """)

        conn.commit()

    async def close(self) -> None:
        """Close database connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    async def create_session(
        self,
        session_id: str,
        initial_problem: str,
        custom_context: Optional[str] = None,
        available_logos: Optional[list[str]] = None,
    ) -> SessionResponse:
        """Create a new session."""
        conn = self._get_connection()
        cursor = conn.cursor()

        now = datetime.utcnow().isoformat()
        logos_json = json.dumps(available_logos) if available_logos else None

        cursor.execute(
            """
            INSERT INTO sessions (session_id, initial_problem, custom_context, available_logos, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (session_id, initial_problem, custom_context, logos_json, now, now),
        )
        conn.commit()

        return SessionResponse(
            session_id=session_id,
            initial_problem=initial_problem,
            status="active",
            created_at=now,
            turn_count=0,
            current_architecture=None,
        )

    async def get_session(self, session_id: str) -> Optional[SessionResponse]:
        """Get a session by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM sessions WHERE session_id = ?",
            (session_id,),
        )
        row = cursor.fetchone()

        if row is None:
            return None

        # Get turn count
        cursor.execute(
            "SELECT COUNT(*) as count FROM turns WHERE session_id = ?",
            (session_id,),
        )
        turn_count = cursor.fetchone()["count"]

        # Parse architecture
        architecture = None
        if row["current_architecture"]:
            arch_data = json.loads(row["current_architecture"])
            architecture = ArchitectureState(**arch_data)

        return SessionResponse(
            session_id=row["session_id"],
            initial_problem=row["initial_problem"],
            status=row["status"],
            created_at=row["created_at"],
            turn_count=turn_count,
            current_architecture=architecture,
        )

    async def list_sessions(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[SessionResponse], int]:
        """List sessions with pagination."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Get total count
        cursor.execute("SELECT COUNT(*) as count FROM sessions")
        total = cursor.fetchone()["count"]

        # Get sessions
        cursor.execute(
            """
            SELECT s.*,
                   (SELECT COUNT(*) FROM turns t WHERE t.session_id = s.session_id) as turn_count
            FROM sessions s
            ORDER BY s.created_at DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        rows = cursor.fetchall()

        sessions = []
        for row in rows:
            architecture = None
            if row["current_architecture"]:
                arch_data = json.loads(row["current_architecture"])
                architecture = ArchitectureState(**arch_data)

            sessions.append(
                SessionResponse(
                    session_id=row["session_id"],
                    initial_problem=row["initial_problem"],
                    status=row["status"],
                    created_at=row["created_at"],
                    turn_count=row["turn_count"],
                    current_architecture=architecture,
                )
            )

        return sessions, total

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Delete turns first (foreign key)
        cursor.execute("DELETE FROM turns WHERE session_id = ?", (session_id,))

        # Delete session
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        conn.commit()

        return cursor.rowcount > 0

    async def update_session(
        self,
        session_id: str,
        architecture: Optional[dict] = None,
        status: Optional[str] = None,
    ) -> Optional[SessionResponse]:
        """Update session data."""
        conn = self._get_connection()
        cursor = conn.cursor()

        updates = []
        params = []

        if architecture is not None:
            updates.append("current_architecture = ?")
            params.append(json.dumps(architecture))

        if status is not None:
            updates.append("status = ?")
            params.append(status)

        if not updates:
            return await self.get_session(session_id)

        updates.append("updated_at = ?")
        params.append(datetime.utcnow().isoformat())
        params.append(session_id)

        cursor.execute(
            f"UPDATE sessions SET {', '.join(updates)} WHERE session_id = ?",
            params,
        )
        conn.commit()

        return await self.get_session(session_id)

    async def add_turn(
        self,
        session_id: str,
        turn_number: int,
        user_input: str,
        architect_response: str,
        architecture_snapshot: Optional[dict] = None,
    ) -> bool:
        """Add a conversation turn to a session."""
        conn = self._get_connection()
        cursor = conn.cursor()

        snapshot_json = json.dumps(architecture_snapshot) if architecture_snapshot else None

        try:
            cursor.execute(
                """
                INSERT INTO turns (session_id, turn_number, user_input, architect_response, architecture_snapshot)
                VALUES (?, ?, ?, ?, ?)
                """,
                (session_id, turn_number, user_input, architect_response, snapshot_json),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    async def get_turns(self, session_id: str) -> list[dict]:
        """Get all turns for a session."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT turn_number, user_input, architect_response, architecture_snapshot, created_at
            FROM turns
            WHERE session_id = ?
            ORDER BY turn_number
            """,
            (session_id,),
        )
        rows = cursor.fetchall()

        turns = []
        for row in rows:
            snapshot = None
            if row["architecture_snapshot"]:
                snapshot = json.loads(row["architecture_snapshot"])

            turns.append(
                {
                    "turn_number": row["turn_number"],
                    "user_input": row["user_input"],
                    "architect_response": row["architect_response"],
                    "architecture_snapshot": snapshot,
                    "created_at": row["created_at"],
                }
            )

        return turns

    async def get_full_session_data(self, session_id: str) -> Optional[dict]:
        """Get complete session data including turns and architecture."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM sessions WHERE session_id = ?",
            (session_id,),
        )
        row = cursor.fetchone()

        if row is None:
            return None

        turns = await self.get_turns(session_id)

        # Parse JSON fields
        architecture = None
        if row["current_architecture"]:
            architecture = json.loads(row["current_architecture"])

        available_logos = None
        if row["available_logos"]:
            available_logos = json.loads(row["available_logos"])

        return {
            "session_id": row["session_id"],
            "initial_problem": row["initial_problem"],
            "current_architecture": architecture,
            "available_logos": available_logos,
            "custom_context": row["custom_context"],
            "status": row["status"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "turns": turns,
        }
