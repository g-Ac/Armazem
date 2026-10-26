# agente-com-guardrails — "A IA propõe, o código trava"

Exemplo prático, enxuto e 100% testável do padrão mais importante para colocar **IA em atendimento comercial, triagem de chamados ou sistemas internos** sem passar vergonha nem tomar prejuízo.

## O princípio em 1 frase

> **Prompt não é trava de segurança.** A IA pode errar ou ser induzida pelo usuário (*prompt injection*). Por isso, a IA devolve apenas um **JSON com uma proposta**, e o **código Python determinístico** confere formato, palavras proibidas e limite de turnos antes de qualquer mensagem sair para o cliente.

> 📖 Estudando pela trilha? Leia a explicação completa em [`../../trilha/04-ia-dentro-do-sistema.md`](../../trilha/04-ia-dentro-do-sistema.md).

## Testar na prática agora (offline e de graça)

```bash
# 1. Rodar o simulador interativo no terminal
python3 simular_conversa.py
```

Experimente digitar no simulador:
1. `Oi, preciso organizar os pedidos da minha loja` → passa limpo!
2. `Quero desconto no preço!` → o mock simula a IA tentando oferecer *"R$ 99 por mês hoje ainda"*, o **guardrail bloqueia na hora** e transfere com mensagem segura para um humano!

Para rodar os testes automáticos:

```bash
pytest -q
```

## Conectando numa IA real (Ollama local, Bifrost ou OpenAI)

Quando quiser testar com um modelo real em vez do mock:

```bash
PROVIDER=api \
LLM_BASE_URL=http://localhost:11434/v1 \
LLM_MODEL=gemma4:e4b \
LLM_API_KEY=local \
python3 simular_conversa.py
```
