# CLAUDE.md — instruções pra IA neste projeto Python

Você (IA) está trabalhando num projeto de automação/bot 24/7 em Python.

## Stack e princípios
- **Python 3.10+** enxuto: prefira biblioteca padrão (`sqlite3`, `urllib`, `pathlib`, `dataclasses`) sempre que resolver bem sem peso extra.
- **SQLite em modo WAL** (`src/db.py`) para histórico e trilha de auditoria (`audit_log`).
- **Isolamento de runtime**: bancos `.db` e logs ficam em `runtime/` (ignorado pelo Git).
- **Segredos só em `.env`**: nunca coloque tokens do Telegram ou chaves de API no código.
- **Resiliência 24/7**: falhas de rede/HTTP nunca devem derrubar o processo principal — capture, registre no banco e alerte.
- **Aprovação humana**: ações destrutivas ou de restart em produção devem sempre registrar quem aprovou no `audit_log`.

## Onde fica cada coisa
- `src/config.py` — leitura do `.env` e configurações tipadas (`Settings`)
- `src/db.py` — conexão SQLite WAL, gravação de checagens e auditoria
- `src/monitor.py` — checagens de saúde e regras puras de alerta
- `src/bot.py` — CLI (`--demo`, `--once`, `--status`), envio ao Telegram e loop contínuo
- `deploy/automacao.service` — arquivo do `systemd` para rodar 24/7 no Linux
- `tests/` — testes automáticos com `pytest`

## Antes de dizer "pronto"
1. Escreva ou atualize testes em `tests/` para qualquer regra nova.
2. Rode `pytest -q` e confirme que todos os testes passam.
3. Teste no terminal com `python3 -m src.bot --demo` ou `python3 -m src.bot --once`.
