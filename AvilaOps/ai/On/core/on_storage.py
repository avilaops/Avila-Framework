"""SQLite-backed persistence layer for the On platform."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterable, Iterator, Optional

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "registry" / "on_core.db"
_INITIALISED = False


@contextmanager
def _connect() -> Iterator[sqlite3.Connection]:
    """Yield a SQLite connection with foreign keys enabled."""
    DB_PATH.parent.mkdir(exist_ok=True, parents=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """Initialise the SQLite schema when the platform boots."""
    global _INITIALISED
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT,
                timestamp TEXT,
                message TEXT
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT,
                task TEXT,
                status TEXT,
                created_at TEXT,
                updated_at TEXT
            );
            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT,
                start_time TEXT,
                end_time TEXT,
                duration_min REAL,
                completed INTEGER
            );
            CREATE TABLE IF NOT EXISTS heartbeats (
                agent TEXT PRIMARY KEY,
                last_beat TEXT
            );
            """
        )
    _INITIALISED = True


def _ensure_schema() -> None:
    if not _INITIALISED:
        init_db()


def log(agent: str, message: str) -> None:
    """Persist a log line attributed to an agent."""
    _ensure_schema()
    with _connect() as conn:
        conn.execute(
            "INSERT INTO logs (agent, timestamp, message) VALUES (?,?,?)",
            (agent, datetime.utcnow().isoformat(), message),
        )


def add_task(agent: str, task: str) -> int:
    """Register a new task for an agent and return the task id."""
    _ensure_schema()
    created = datetime.utcnow().isoformat()
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (agent, task, status, created_at, updated_at) VALUES (?,?,?,?,?)",
            (agent, task, "Pendente", created, created),
        )
        return cur.lastrowid


def update_task(agent: str, task_id: int, status: str) -> None:
    """Update task status while tracking the timestamp change."""
    _ensure_schema()
    with _connect() as conn:
        conn.execute(
            "UPDATE tasks SET status=?, updated_at=? WHERE id=? AND agent=?",
            (status, datetime.utcnow().isoformat(), task_id, agent),
        )


def register_shift(agent: str, start: str, end: str, duration: float, completed: bool) -> None:
    """Record a completed or interrupted shift for an agent."""
    _ensure_schema()
    with _connect() as conn:
        conn.execute(
            "INSERT INTO shifts (agent, start_time, end_time, duration_min, completed) VALUES (?,?,?,?,?)",
            (agent, start, end, duration, int(completed)),
        )


def update_heartbeat(agent: str, timestamp: str) -> None:
    """Upsert the last known heartbeat timestamp for an agent."""
    _ensure_schema()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO heartbeats (agent, last_beat) VALUES (?, ?)
            ON CONFLICT(agent) DO UPDATE SET last_beat=excluded.last_beat
            """,
            (agent, timestamp),
        )


def get_logs(agent: Optional[str] = None, limit: int = 50) -> list[tuple[str, str, str]]:
    """Fetch recent logs optionally filtered by agent."""
    _ensure_schema()
    query = "SELECT agent, timestamp, message FROM logs"
    params: Iterable[object] = ()
    if agent:
        query += " WHERE agent=?"
        params = (agent,)
    query += " ORDER BY id DESC LIMIT ?"
    params = (*params, limit)
    with _connect() as conn:
        rows = conn.execute(query, params).fetchall()
    return rows


def get_tasks(agent: Optional[str] = None) -> list[tuple[int, str, str, str, str]]:
    """Return tasks for all agents or a single agent."""
    _ensure_schema()
    query = "SELECT id, agent, task, status, updated_at FROM tasks"
    params: Iterable[object] = ()
    if agent:
        query += " WHERE agent=?"
        params = (agent,)
    query += " ORDER BY id DESC"
    with _connect() as conn:
        rows = conn.execute(query, params).fetchall()
    return rows


def get_shifts(agent: Optional[str] = None) -> list[tuple[str, str, float, int]]:
    """Return shift history for all agents or a single agent."""
    _ensure_schema()
    query = "SELECT start_time, end_time, duration_min, completed FROM shifts"
    params: Iterable[object] = ()
    if agent:
        query += " WHERE agent=?"
        params = (agent,)
    query += " ORDER BY id DESC"
    with _connect() as conn:
        rows = conn.execute(query, params).fetchall()
    return rows
