"""PostgreSQL/Lakebase implementation of the session store.

Lakebase is Databricks' managed PostgreSQL service. This implementation
uses psycopg2 for async-compatible database operations.
"""

import json
import os
from datetime import datetime
from typing import Optional

from ..api.schemas import SessionResponse, ArchitectureState
from ..services.session_store import SessionStore


class LakebaseSessionStore(SessionStore):
    """Lakebase (PostgreSQL) based session storage for Databricks deployment."""

    def __init__(self, connection_url: Optional[str] = None):
        """Initialize the Lakebase store.

        Args:
            connection_url: PostgreSQL connection URL.
                           Defaults to DATABRICKS_LAKEBASE_URL env var.
        """
        self.connection_url = connection_url or os.environ.get("DATABRICKS_LAKEBASE_URL")
        if not self.connection_url:
            raise ValueError(
                "DATABRICKS_LAKEBASE_URL environment variable not set. "
                "Configure Lakebase in your Databricks App settings."
            )

        self._pool = None

    def _get_connection(self):
        """Get a database connection from the pool."""
        if self._pool is None:
            from psycopg2 import pool

            self._pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=self.connection_url,
            )

        return self._pool.getconn()

    def _put_connection(self, conn):
        """Return a connection to the pool."""
        if self._pool is not None:
            self._pool.putconn(conn)

    async def initialize(self) -> None:
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            # Create sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    initial_problem TEXT NOT NULL,
                    current_architecture JSONB,
                    available_logos JSONB,
                    custom_context TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create turns table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS turns (
                    id SERIAL PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
                    turn_number INTEGER NOT NULL,
                    user_input TEXT NOT NULL,
                    architect_response TEXT NOT NULL,
                    architecture_snapshot JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(session_id, turn_number)
                )
            """)

            # Create index for faster lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_turns_session_id ON turns(session_id)
            """)

            conn.commit()
        finally:
            self._put_connection(conn)

    async def close(self) -> None:
        """Close the connection pool."""
        if self._pool is not None:
            self._pool.closeall()
            self._pool = None

    async def create_session(
        self,
        session_id: str,
        initial_problem: str,
        custom_context: Optional[str] = None,
        available_logos: Optional[list[str]] = None,
    ) -> SessionResponse:
        """Create a new session."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            now = datetime.utcnow()
            logos_json = json.dumps(available_logos) if available_logos else None

            cursor.execute(
                """
                INSERT INTO sessions (session_id, initial_problem, custom_context, available_logos, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (session_id, initial_problem, custom_context, logos_json, now, now),
            )
            conn.commit()

            return SessionResponse(
                session_id=session_id,
                initial_problem=initial_problem,
                status="active",
                created_at=now.isoformat(),
                turn_count=0,
                current_architecture=None,
            )
        finally:
            self._put_connection(conn)

    async def get_session(self, session_id: str) -> Optional[SessionResponse]:
        """Get a session by ID."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM sessions WHERE session_id = %s",
                (session_id,),
            )
            row = cursor.fetchone()

            if row is None:
                return None

            # Get column names
            columns = [desc[0] for desc in cursor.description]
            row_dict = dict(zip(columns, row))

            # Get turn count
            cursor.execute(
                "SELECT COUNT(*) FROM turns WHERE session_id = %s",
                (session_id,),
            )
            turn_count = cursor.fetchone()[0]

            # Parse architecture
            architecture = None
            if row_dict["current_architecture"]:
                arch_data = row_dict["current_architecture"]
                if isinstance(arch_data, str):
                    arch_data = json.loads(arch_data)
                architecture = ArchitectureState(**arch_data)

            return SessionResponse(
                session_id=row_dict["session_id"],
                initial_problem=row_dict["initial_problem"],
                status=row_dict["status"],
                created_at=row_dict["created_at"].isoformat() if row_dict["created_at"] else "",
                turn_count=turn_count,
                current_architecture=architecture,
            )
        finally:
            self._put_connection(conn)

    async def list_sessions(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[SessionResponse], int]:
        """List sessions with pagination."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            # Get total count
            cursor.execute("SELECT COUNT(*) FROM sessions")
            total = cursor.fetchone()[0]

            # Get sessions with turn counts
            cursor.execute(
                """
                SELECT s.*,
                       (SELECT COUNT(*) FROM turns t WHERE t.session_id = s.session_id) as turn_count
                FROM sessions s
                ORDER BY s.created_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            sessions = []
            for row in rows:
                row_dict = dict(zip(columns, row))

                architecture = None
                if row_dict["current_architecture"]:
                    arch_data = row_dict["current_architecture"]
                    if isinstance(arch_data, str):
                        arch_data = json.loads(arch_data)
                    architecture = ArchitectureState(**arch_data)

                sessions.append(
                    SessionResponse(
                        session_id=row_dict["session_id"],
                        initial_problem=row_dict["initial_problem"],
                        status=row_dict["status"],
                        created_at=row_dict["created_at"].isoformat() if row_dict["created_at"] else "",
                        turn_count=row_dict["turn_count"],
                        current_architecture=architecture,
                    )
                )

            return sessions, total
        finally:
            self._put_connection(conn)

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session by ID."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            # Turns will be cascade deleted
            cursor.execute("DELETE FROM sessions WHERE session_id = %s", (session_id,))
            conn.commit()

            return cursor.rowcount > 0
        finally:
            self._put_connection(conn)

    async def update_session(
        self,
        session_id: str,
        architecture: Optional[dict] = None,
        status: Optional[str] = None,
    ) -> Optional[SessionResponse]:
        """Update session data."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            updates = []
            params = []

            if architecture is not None:
                updates.append("current_architecture = %s")
                params.append(json.dumps(architecture))

            if status is not None:
                updates.append("status = %s")
                params.append(status)

            if not updates:
                return await self.get_session(session_id)

            updates.append("updated_at = %s")
            params.append(datetime.utcnow())
            params.append(session_id)

            cursor.execute(
                f"UPDATE sessions SET {', '.join(updates)} WHERE session_id = %s",
                params,
            )
            conn.commit()

            return await self.get_session(session_id)
        finally:
            self._put_connection(conn)

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
        try:
            cursor = conn.cursor()

            snapshot_json = json.dumps(architecture_snapshot) if architecture_snapshot else None

            try:
                cursor.execute(
                    """
                    INSERT INTO turns (session_id, turn_number, user_input, architect_response, architecture_snapshot)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (session_id, turn_number, user_input, architect_response, snapshot_json),
                )
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False
        finally:
            self._put_connection(conn)

    async def get_turns(self, session_id: str) -> list[dict]:
        """Get all turns for a session."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT turn_number, user_input, architect_response, architecture_snapshot, created_at
                FROM turns
                WHERE session_id = %s
                ORDER BY turn_number
                """,
                (session_id,),
            )
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            turns = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                snapshot = row_dict["architecture_snapshot"]
                if isinstance(snapshot, str):
                    snapshot = json.loads(snapshot)

                turns.append(
                    {
                        "turn_number": row_dict["turn_number"],
                        "user_input": row_dict["user_input"],
                        "architect_response": row_dict["architect_response"],
                        "architecture_snapshot": snapshot,
                        "created_at": row_dict["created_at"].isoformat() if row_dict["created_at"] else "",
                    }
                )

            return turns
        finally:
            self._put_connection(conn)

    async def get_full_session_data(self, session_id: str) -> Optional[dict]:
        """Get complete session data including turns and architecture."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM sessions WHERE session_id = %s",
                (session_id,),
            )
            row = cursor.fetchone()

            if row is None:
                return None

            columns = [desc[0] for desc in cursor.description]
            row_dict = dict(zip(columns, row))

            turns = await self.get_turns(session_id)

            # Parse JSON fields
            architecture = row_dict["current_architecture"]
            if isinstance(architecture, str):
                architecture = json.loads(architecture)

            available_logos = row_dict["available_logos"]
            if isinstance(available_logos, str):
                available_logos = json.loads(available_logos)

            return {
                "session_id": row_dict["session_id"],
                "initial_problem": row_dict["initial_problem"],
                "current_architecture": architecture,
                "available_logos": available_logos,
                "custom_context": row_dict["custom_context"],
                "status": row_dict["status"],
                "created_at": row_dict["created_at"].isoformat() if row_dict["created_at"] else "",
                "updated_at": row_dict["updated_at"].isoformat() if row_dict["updated_at"] else "",
                "turns": turns,
            }
        finally:
            self._put_connection(conn)
