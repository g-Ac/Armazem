"""Persistência local em SQLite (modo WAL) para histórico e auditoria."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def connect_db(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    # WAL permite leitura e escrita simultâneas sem travar o banco em serviços 24/7
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            target TEXT NOT NULL,
            ok INTEGER NOT NULL,
            latency_ms REAL NOT NULL,
            detail TEXT NOT NULL
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            actor TEXT NOT NULL,
            action TEXT NOT NULL,
            status TEXT NOT NULL,
            note TEXT NOT NULL
        );
        """
    )
    conn.commit()
    return conn


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def record_check(
    conn: sqlite3.Connection,
    *,
    target: str,
    ok: bool,
    latency_ms: float,
    detail: str,
) -> None:
    conn.execute(
        "INSERT INTO checks (created_at, target, ok, latency_ms, detail) VALUES (?, ?, ?, ?, ?)",
        (_now_iso(), target, 1 if ok else 0, round(latency_ms, 2), detail),
    )
    conn.commit()


def record_audit(
    conn: sqlite3.Connection,
    *,
    actor: str,
    action: str,
    status: str,
    note: str = "",
) -> None:
    conn.execute(
        "INSERT INTO audit_log (created_at, actor, action, status, note) VALUES (?, ?, ?, ?, ?)",
        (_now_iso(), actor, action, status, note),
    )
    conn.commit()


def get_summary(conn: sqlite3.Connection) -> dict:
    row = conn.execute(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN ok = 1 THEN 1 ELSE 0 END) AS successes,
            ROUND(AVG(latency_ms), 1) AS avg_latency_ms
        FROM checks
        """
    ).fetchone()
    total = row["total"] or 0
    successes = row["successes"] or 0
    uptime_pct = round((successes / total) * 100, 1) if total > 0 else 0.0
    recent_audits = [
        dict(r)
        for r in conn.execute(
            "SELECT created_at, actor, action, status, note FROM audit_log ORDER BY id DESC LIMIT 5"
        ).fetchall()
    ]
    return {
        "total_checks": total,
        "uptime_pct": uptime_pct,
        "avg_latency_ms": row["avg_latency_ms"] or 0.0,
        "recent_audits": recent_audits,
    }
