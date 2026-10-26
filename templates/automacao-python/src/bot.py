"""Motor principal do bot de monitoramento e automação com registro de auditoria."""
from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request

from src.config import Settings, get_settings
from src.db import connect_db, get_summary, record_audit, record_check
from src.monitor import DiskStatus, HttpStatus, check_disk, check_http, evaluate_alerts


def send_telegram_message(token: str, chat_id: str, text: str) -> bool:
    """Envia mensagem via API oficial do Telegram usando apenas biblioteca padrão do Python."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return bool(data.get("ok"))
    except Exception as exc:  # noqa: BLE001
        print(f"[telegram] falha ao enviar alerta: {exc}")
        return False


def run_cycle(settings: Settings) -> list[str]:
    conn = connect_db(settings.db_path)
    try:
        disk = check_disk("/", warn_pct=settings.disk_warn_pct)
        http = check_http(settings.check_url)

        record_check(conn, target="disk:/", ok=disk.ok, latency_ms=0.0, detail=disk.detail)
        record_check(
            conn,
            target=f"http:{http.url}",
            ok=http.ok,
            latency_ms=http.latency_ms,
            detail=http.detail,
        )

        alerts = evaluate_alerts(disk, http)
        print(f"[check] {disk.detail} | {http.url} -> {http.detail}")

        if alerts:
            msg = "🔔 Automação detectou atenção:\n" + "\n".join(alerts)
            print(msg)
            if settings.telegram_enabled:
                sent = send_telegram_message(
                    settings.telegram_bot_token, settings.telegram_chat_id, msg
                )
                record_audit(
                    conn,
                    actor="bot",
                    action="notify_telegram",
                    status="ok" if sent else "failed",
                    note="; ".join(alerts),
                )
            else:
                record_audit(
                    conn,
                    actor="bot",
                    action="notify_console",
                    status="ok",
                    note="; ".join(alerts),
                )
        return alerts
    finally:
        conn.close()


def run_demo(settings: Settings) -> None:
    """Simula um incidente completo + aprovação humana (sem precisar de Telegram configurado)."""
    print("=== MODO DEMO: Simulando ciclo saudável + incidente com aprovação humana ===\n")
    conn = connect_db(settings.db_path)
    try:
        # 1. Ciclo normal
        ok_disk = DiskStatus(ok=True, used_pct=42.0, free_gb=25.0, detail="Disco em 42.0% (25.0 GB livres)")
        ok_http = HttpStatus(
            url="https://meu-sistema.local/health",
            ok=True,
            status_code=200,
            latency_ms=38.5,
            detail="HTTP 200 em 38.5 ms",
        )
        record_check(conn, target="demo:health", ok=True, latency_ms=38.5, detail=ok_http.detail)
        print(f"1) Ciclo saudável -> {ok_disk.detail} | {ok_http.detail}")

        # 2. Incidente simulado
        bad_http = HttpStatus(
            url="https://meu-sistema.local/health",
            ok=False,
            status_code=502,
            latency_ms=120.0,
            detail="Erro HTTP 502 em 120.0 ms",
        )
        record_check(conn, target="demo:health", ok=False, latency_ms=120.0, detail=bad_http.detail)
        alerts = evaluate_alerts(ok_disk, bad_http)
        print(f"2) Incidente detectado -> {alerts[0]}")

        # 3. Regra de ouro: o bot diagnostica e pede aprovação antes de reiniciar serviço crítico
        print("3) Pedido de aprovação enviado ao operador: 'Posso reiniciar meu-sistema? [APROVAR / IGNORAR]'")
        record_audit(
            conn,
            actor="operador_humano",
            action="restart_service:meu-sistema",
            status="approved_simulated",
            note="Aprovação simulada no modo --demo após HTTP 502",
        )
        print("4) Ação registrada no audit_log do SQLite!\n")

        summary = get_summary(conn)
        print("=== Resumo salvo no banco SQLite ===")
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    finally:
        conn.close()


def print_status(settings: Settings) -> None:
    conn = connect_db(settings.db_path)
    try:
        summary = get_summary(conn)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Automação de monitoramento 24/7 com SQLite + Telegram")
    parser.add_argument("--once", action="store_true", help="Roda apenas 1 ciclo e encerra")
    parser.add_argument("--demo", action="store_true", help="Simula incidente + aprovação humana no terminal")
    parser.add_argument("--status", action="store_true", help="Mostra métricas salvas no banco SQLite")
    args = parser.parse_args()

    settings = get_settings()

    if args.demo:
        run_demo(settings)
        return
    if args.status:
        print_status(settings)
        return
    if args.once:
        run_cycle(settings)
        return

    print(
        f"[start] Monitorando {settings.check_url} a cada {settings.check_interval_sec}s "
        f"(Telegram={'ativo' if settings.telegram_enabled else 'desativado'})"
    )
    while True:
        run_cycle(settings)
        time.sleep(settings.check_interval_sec)


if __name__ == "__main__":
    main()
