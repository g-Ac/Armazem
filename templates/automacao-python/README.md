# automacao-python — Base de Bot e Automação 24/7

Esqueleto prático em Python para criar robôs que monitoram sistemas, coletam dados, mandam alertas no **Telegram** e rodam **24 horas por dia** num Linux, Raspberry Pi ou VPS barata.

**Por que essa estrutura funciona tão bem na vida real:**
- **Zero dependência pesada** para rodar (usa biblioteca padrão do Python + `SQLite` nativo).
- **Banco SQLite em modo WAL** (`runtime/automacao.db`) — guarda todo o histórico de checagens e um livro de auditoria (`audit_log`).
- **Nunca morre por queda de internet** — trata timeouts, grava a falha e segue vivo.
- **Pronto para `systemd`** (`deploy/automacao.service`) — se o servidor reiniciar ou faltar luz, o bot volta sozinho.

> 📖 Estudando pela trilha? Siga o guia passo a passo em [`../../trilha/03-primeira-automacao-bot.md`](../../trilha/03-primeira-automacao-bot.md).

## Rodar agora (leva 1 minuto)

Pré-requisito: **Python 3.10+**.

```bash
# 1. Criar ambiente virtual isolado e ativar
python3 -m venv .venv
source .venv/bin/activate   # No Windows (PowerShell): .venv\Scripts\Activate.ps1

# 2. Instalar o pytest para rodar os testes
pip install -r requirements.txt

# 3. Criar seu .env local a partir do exemplo
cp .env.example .env

# 4. Rodar a simulação completa (saudável + incidente + aprovação humana)
python -m src.bot --demo
```

## Comandos disponíveis

| Comando | O que faz |
|---|---|
| `python -m src.bot --demo` | Simula um incidente e mostra o histórico no SQLite (sem precisar de Telegram) |
| `python -m src.bot --once` | Faz **1 checagem real** (disco + URL do `.env`) e salva no banco |
| `python -m src.bot --status` | Mostra uptime %, latência média e últimas auditorias gravadas |
| `python -m src.bot` | Fica rodando em loop contínuo (modo usado pelo `systemd` 24/7) |
| `pytest -q` | Roda a bateria de testes automáticos |

## Ativando alertas reais no Telegram (opcional)

1. No Telegram, fale com o **[@BotFather](https://t.me/BotFather)**, mande `/newbot` e copie o **Token**.
2. Mande um "oi" para o seu bot novo e descubra seu `chat_id` acessando `https://api.telegram.org/botSEU_TOKEN/getUpdates` no navegador.
3. Preencha `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` no seu arquivo `.env` (que nunca sobe pro GitHub!).
4. Teste derrubando a URL no `.env` (ex: `CHECK_URL=http://localhost:9999`) e rode `python -m src.bot --once`. O alerta cai direto no seu celular!
