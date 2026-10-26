"""Testes automáticos da automação: banco SQLite, regras de alerta e configuração."""
from __future__ import annotations

import os
from pathlib import Path

from src.config import get_settings
from src.db import connect_db, get_summary, record_audit, record_check
from src.monitor import DiskStatus, HttpStatus, evaluate_alerts


def test_evaluate_alerts_healthy():
    disk = DiskStatus(ok=True, used_pct=50.0, free_gb=20.0, detail="Disco OK")
    http = HttpStatus(url="https://example.com", ok=True, status_code=200, latency_ms=45.0, detail="HTTP 200")
    assert evaluate_alerts(disk, http) == []


def test_evaluate_alerts_detects_disk_and_http_failures():
    disk = DiskStatus(ok=False, used_pct=92.0, free_gb=1.5, detail="Disco em 92%")
    http = HttpStatus(url="https://api.local", ok=False, status_code=503, latency_ms=110.0, detail="Erro HTTP 503")
    alerts = evaluate_alerts(disk, http)
    assert len(alerts) == 2
    assert "DISCO" in alerts[0]
    assert "FORA DO AR" in alerts[1]


def test_sqlite_persistence_and_summary(tmp_path: Path):
    db_file = tmp_path / "test.db"
    conn = connect_db(db_file)
    try:
        mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
        assert mode.lower() == "wal"

        record_check(conn, target="http:site", ok=True, latency_ms=30.0, detail="OK")
        record_check(conn, target="http:site", ok=False, latency_ms=90.0, detail="Timeout")
        record_audit(conn, actor="operador", action="restart", status="approved", note="Teste")

        summary = get_summary(conn)
        assert summary["total_checks"] == 2
        assert summary["uptime_pct"] == 50.0
        assert summary["avg_latency_ms"] == 60.0
        assert len(summary["recent_audits"]) == 1
        assert summary["recent_audits"][0]["action"] == "restart"
    finally:
        conn.close()


def test_settings_loads_from_env_file(tmp_path: Path, monkeypatch):
    for key in ("DB_PATH", "CHECK_URL", "DISK_WARN_PCT", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
        monkeypatch.delenv(key, raising=False)

    env_file = tmp_path / ".env"
    env_file.write_text(
        "DB_PATH=runtime/custom.db\nCHECK_URL=https://meusite.com.br\nDISK_WARN_PCT=90\n",
        encoding="utf-8",
    )
    settings = get_settings(env_file)
    assert settings.db_path == "runtime/custom.db"
    assert settings.check_url == "https://meusite.com.br"
    assert settings.disk_warn_pct == 90.0
    assert settings.telegram_enabled is False
    # Limpa env criado durante o teste
    for key in ("DB_PATH", "CHECK_URL", "DISK_WARN_PCT"):
        os.environ.pop(key, None)
