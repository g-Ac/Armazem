# Módulo 03 — Sua Primeira Automação e Bot em Python

> **Tempo estimado:** 40 minutos
> **Pasta de trabalho:** [`templates/automacao-python/`](../templates/automacao-python/)
> **Meta prática:** rodar um robô em Python que vigia sistemas/APIs sozinho, salva histórico em SQLite, manda alertas no Telegram e registra auditoria de ações.

---

## 1. Quando usar Web vs Automação?

- **Sistema Web (`web-fullstack`)**: quando uma pessoa abre uma tela para cadastrar, consultar ou clicar em botões.
- **Automação / Bot (`automacao-python`)**: quando o trabalho precisa acontecer **sozinho em segundo plano** (de 1 em 1 minuto, toda manhã às 8h, ou reagindo a mensagens no Telegram/WhatsApp).

Os melhores projetos reais juntam os dois!

---

## 2. Anatomia de uma automação que não dá dor de cabeça

Olhe os 4 arquivos dentro de [`templates/automacao-python/src/`](../templates/automacao-python/src/):

1. **`config.py` (Configuração fora do código)**: lê URLs, limites e tokens do arquivo `.env`. Trocar de ambiente = mudar 1 linha no `.env`.
2. **`db.py` (Memória e Auditoria em SQLite WAL)**: toda checagem vira linha na tabela `checks`, e toda ação importante vira linha no `audit_log`. O modo **WAL** (*Write-Ahead Logging*) evita erro de "banco travado" (*database is locked*) quando dois processos leem e gravam ao mesmo tempo.
3. **`monitor.py` (Regras puras e resilientes)**: mede espaço em disco e testa sites/APIs. Se a internet cair, ele **não explode** — devolve `ok=False` com o motivo exato.
4. **`bot.py` (Orquestrador)**: junta tudo, envia alerta pro Telegram se houver problema e oferece modos fáceis de teste (`--demo`, `--once`, `--status`).

---

## 3. Rodando na prática agora

```bash
cd ~/projects/Armazem/templates/automacao-python

# 1. Ambiente virtual Python (mantém pacotes isolados deste projeto)
python3 -m venv .venv
source .venv/bin/activate

# 2. Instala pytest e roda os testes automáticos
pip install -r requirements.txt
pytest -q

# 3. Copia o .env de exemplo e roda a demonstração completa
cp .env.example .env
python -m src.bot --demo

# 4. Agora faz 1 checagem real na internet e consulta o banco SQLite
python -m src.bot --once
python -m src.bot --status
```

---

## 4. Exercício prático com a IA: Monitor de Preço / Cotação

Abra seu agente de IA dentro de `templates/automacao-python` e peça uma evolução real:

```text
Leia o CLAUDE.md.
Quero adicionar no monitor.py uma função check_btc_price(max_alert_usd: float) que consulta uma API pública gratuita (sem precisar de chave) ou recebe um JSON injetável nos testes, e gera alerta se passar do valor configurado no .env.
1. Escreva testes unitários em tests/ simulando resposta acima e abaixo do limite (sem depender de internet no pytest!).
2. Integre opcionalmente no bot.py quando BTC_ALERT_USD estiver preenchido no .env.
Me mostre o plano em 5 linhas antes de editar.
```

> 💡 **Reparou no detalhe de ouro?** Nos testes automáticos (`pytest`), simulamos a resposta da API para os testes rodarem em 0,2 segundo mesmo sem Wi-Fi!

---

## ✅ Entrega prática deste módulo

- [ ] `pytest -q` passando 100% verde.
- [ ] Você rodou `--demo`, `--once` e `--status` e viu os dados acumulados no SQLite.
- [ ] *(Bônus recomendado)* Criou seu bot gratuito no `@BotFather` do Telegram, colocou o token no `.env` e recebeu uma mensagem real no seu celular!

Próximo passo: aprender como colocar **Inteligência Artificial dentro de sistemas e bots** com segurança total no **[Módulo 04 — IA Dentro do Sistema (Guardrails)](04-ia-dentro-do-sistema.md)**!
