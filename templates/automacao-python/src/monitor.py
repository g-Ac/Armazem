"""Regras determinísticas de monitoramento (disco + endpoint HTTP)."""
from __future__ import annotations

import shutil
import time
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass(frozen=True)
class DiskStatus:
    ok: bool
    used_pct: float
    free_gb: float
    detail: str


@dataclass(frozen=True)
class HttpStatus:
    url: str
    ok: bool
    status_code: int
    latency_ms: float
    detail: str


def check_disk(path: str = "/", warn_pct: float = 85.0) -> DiskStatus:
    usage = shutil.disk_usage(path)
    used_pct = round((usage.used / usage.total) * 100, 1)
    free_gb = round(usage.free / (1024**3), 2)
    ok = used_pct < warn_pct
    detail = f"Disco em {used_pct}% ({free_gb} GB livres; limite {warn_pct}%)"
    return DiskStatus(ok=ok, used_pct=used_pct, free_gb=free_gb, detail=detail)


def check_http(url: str, timeout: float = 5.0) -> HttpStatus:
    started = time.perf_counter()
    req = urllib.request.Request(url, headers={"User-Agent": "ArmazemMonitor/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            latency_ms = round((time.perf_counter() - started) * 1000, 1)
            code = resp.getcode() or 200
            ok = 200 <= code < 400
            return HttpStatus(
                url=url,
                ok=ok,
                status_code=code,
                latency_ms=latency_ms,
                detail=f"HTTP {code} em {latency_ms} ms",
            )
    except urllib.error.HTTPError as exc:
        latency_ms = round((time.perf_counter() - started) * 1000, 1)
        return HttpStatus(
            url=url,
            ok=False,
            status_code=exc.code,
            latency_ms=latency_ms,
            detail=f"Erro HTTP {exc.code} em {latency_ms} ms",
        )
    except Exception as exc:  # noqa: BLE001 - automação 24/7 nunca deve cair por falha de rede
        latency_ms = round((time.perf_counter() - started) * 1000, 1)
        return HttpStatus(
            url=url,
            ok=False,
            status_code=0,
            latency_ms=latency_ms,
            detail=f"Falha de conexão: {type(exc).__name__} ({exc})",
        )


def evaluate_alerts(disk: DiskStatus, http: HttpStatus) -> list[str]:
    """Função pura: recebe leituras e devolve lista de alertas claros."""
    alerts: list[str] = []
    if not disk.ok:
        alerts.append(f"⚠️ ALERTA DE DISCO: {disk.detail}")
    if not http.ok:
        alerts.append(f"🚨 SERVIÇO FORA DO AR ({http.url}): {http.detail}")
    return alerts
