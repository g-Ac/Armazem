"""Carregamento simples e seguro de configurações via .env + variáveis de ambiente."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def load_dotenv_file(env_path: str | Path = ".env") -> None:
    """Lê pares CHAVE=VALOR de um arquivo .env sem sobrescrever variáveis já definidas no sistema."""
    path = Path(env_path)
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass(frozen=True)
class Settings:
    db_path: str
    check_url: str
    disk_warn_pct: float
    check_interval_sec: int
    telegram_bot_token: str
    telegram_chat_id: str

    @property
    def telegram_enabled(self) -> bool:
        return bool(self.telegram_bot_token and self.telegram_chat_id)


def get_settings(env_path: str | Path = ".env") -> Settings:
    load_dotenv_file(env_path)
    return Settings(
        db_path=os.environ.get("DB_PATH", "runtime/automacao.db"),
        check_url=os.environ.get("CHECK_URL", "https://example.com"),
        disk_warn_pct=float(os.environ.get("DISK_WARN_PCT", "85")),
        check_interval_sec=max(5, int(os.environ.get("CHECK_INTERVAL_SEC", "60"))),
        telegram_bot_token=os.environ.get("TELEGRAM_BOT_TOKEN", "").strip(),
        telegram_chat_id=os.environ.get("TELEGRAM_CHAT_ID", "").strip(),
    )
