# Desafios Práticos — Do Estudo para Sistemas Reais

Não tente decorar mais nada lendo. Escolha **um** desafio abaixo, crie um repositório próprio no seu GitHub, copie o `CLAUDE-BASE.md` + `SPEC-TEMPLATE.md` do [`kit-ia/`](../kit-ia/) e construa usando o método!

> **Regra para todos os desafios:**
> 1. Preencha o `SPEC.md` de 1 página **antes** de pedir código para a IA.
> 2. Trabalhe em fatias pequenas com testes automáticos (`Vitest` ou `pytest`).
> 3. Passe o checklist do agente `security-auditor` antes de dar `git push`.

---

## 🟢 Desafio 1 — Mini-CRM de Clientes e Orçamentos (Sistema Web)
**Base:** [`templates/web-fullstack/`](../templates/web-fullstack/)

**A dor real:** pequenos prestadores de serviço perdem orçamentos no meio do WhatsApp e esquecem de cobrar retorno (*follow-up*).
**O que construir:**
- Cadastro de clientes (nome, telefone, empresa, observação).
- Cadastro de orçamentos ligados ao cliente com status: `enviado`, `aprovado`, `perdido`.
- Tela inicial destacando em vermelho quem recebeu orçamento há mais de 3 dias e ainda está `enviado`.
- **Critério de pronto:** testes cobrindo a regra de atraso de 3 dias + filtro por status funcionando no navegador.

---

## 🟢 Desafio 2 — Vigia de Preços ou Vagas no Telegram (Automação 24/7)
**Base:** [`templates/automacao-python/`](../templates/automacao-python/)

**A dor real:** acompanhar manualmente todo dia se um produto baixou de preço, se uma API caiu ou se saiu um edital/vaga nova.
**O que construir:**
- Coletor em Python que consulta uma página ou API pública a cada X minutos.
- Tabela no SQLite para guardar itens já vistos (**idempotência**: nunca mandar o mesmo alerta repetido 10 vezes no seu Telegram!).
- Comando ou resumo diário dizendo quantos itens foram checados nas últimas 24h.
- **Critério de pronto:** rodar 2 vezes seguidas para o mesmo item e provar em teste `pytest` que o alerta só dispara na primeira vez!

---

## 🟡 Desafio 3 — Recepção Inteligente de Chamados com Trava (IA + Guardrails)
**Base:** [`templates/agente-com-guardrails/`](../templates/agente-com-guardrails/) + [`templates/web-fullstack/`](../templates/web-fullstack/)

**A dor real:** clientes mandam mensagens incompletas (*"meu sistema parou, socorro"*) e o suporte perde 20 minutos só perguntando quem é, qual tela e qual a urgência.
**O que construir:**
- Tela simulando o chat do cliente + tela interna `/atendente` mostrando a fila já organizada.
- O motor de IA coleta `nome`, `sistema_afetado` e `urgencia` em no máximo 4 perguntas.
- **Guardrail obrigatório:** o robô é proibido de prometer prazo de resolução (*"resolvemos em 10 minutos"*) ou pedir senha do cliente. Se violar, transfere imediatamente para a fila humana marcando o alerta.
- **Critério de pronto:** bateria de testes tentando enganar o bot + fila `/atendente` exibindo o dossiê mastigado.

---

## 🟠 Desafio 4 — Sistema Completo Conectado (Web + Bot no Mesmo Banco)
**Base:** Unir Web + Automação Python

**O que construir:**
- Um painel web onde você cadastra URLs/serviços que quer monitorar e vê o histórico de disponibilidade (*uptime*).
- O robô em Python lê essa lista de URLs, testa em segundo plano a cada minuto, grava os resultados e te avisa no Telegram quando algum cair ou voltar ao normal.
- **Aprendizado chave:** entender na pele por que o `PRAGMA journal_mode=WAL;` do SQLite permite o site ler e o bot gravar sem um travar o outro!

---

## 🔴 Desafio 5 — Operação Real 24/7 + Auditoria de Segurança
**Base:** Módulo 05 + inspiração no [`g-Ac/homelab`](https://github.com/g-Ac/homelab)

**O que fazer:**
- Subir seu projeto do Desafio 2 ou 4 num ambiente Linux (PC antigo, Raspberry Pi ou VPS) usando `systemd` ou `Docker Compose`.
- Simular uma queda de propósito (derrubar o alvo monitorado) e receber o alerta real no celular.
- Rodar `gitleaks` no seu repositório e documentar num arquivo `docs/decisoes/0001-arquitetura.md` (usando o template de decisão do `kit-ia`) como seu sistema funciona e como fazer backup do arquivo `.db`.
