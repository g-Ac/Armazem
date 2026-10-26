# CLAUDE.md — Instruções para a IA neste projeto

Você (IA: Claude Code / Codex / Cursor / Antigravity) deve seguir este protocolo ao planejar, escrever, revisar ou corrigir código aqui.

## 1. Divisão de responsabilidades (Humano vs IA)

- **Eu (dono do projeto) decido o produto:** comportamento visível, regras de negócio, prioridades, custo, privacidade, risco aceitável e quando exigir aprovação humana.
- **Você (IA) cuida da técnica:** organização interna, padrões limpos e escolhas reversíveis dentro da stack definida abaixo.
- **Não jogue escolhas técnicas abertas no meu colo** sem antes traduzir o impacto prático e dar sua recomendação.
- **Pare e pergunte** sempre que uma escolha mudar regra de negócio, segurança, dados existentes, custo ou for difícil de desfazer.
- **Push, deploy, exclusão de dados e mudanças em produção** exigem minha autorização explícita.

## 2. Como falar comigo antes de despejar detalhes técnicos

Toda proposta, revisão ou bloqueio deve começar com 5 linhas em português simples:
1. **O que está acontecendo** — qual tela, automação ou etapa estamos mexendo.
2. **Problema e impacto** — o que pode dar errado na prática e por que importa.
3. **Preciso decidir algo?** — `sim` ou `não`.
4. **Recomendação** — o menor próximo passo seguro.
5. **Estado da etapa** — pronta, pendente de ajuste ou bloqueada.

> Sempre traduza jargões técnicos (ex: *idempotência*, *migration*, *race condition*, *WAL*) em 1 frase prática na primeira vez que usar.

## 3. Fluxo de trabalho obrigatório

1. **Uma coisa por vez**: confirme o comportamento esperado e o critério de pronto antes de editar vários arquivos.
2. **Teste primeiro (RED → GREEN → REFACTOR)**: para toda regra verificável, escreva um teste que falha, faça passar com o código mais simples possível e limpe depois.
3. **Explique enquanto constrói**: ao entregar, explique em 2–3 linhas pelo menos 1 conceito útil ligado ao código que acabou de criar.
4. **Proibido dizer "pronto" no chute**: rode os testes, o linter e a checagem de tipos e mostre o resultado real.

## 4. Segurança inegociável

- **Zero segredos no código**: chaves, senhas e tokens ficam apenas em `.env` (que está no `.gitignore`). Mantenha `.env.example` atualizado com valores fictícios.
- **IA em produção**: se o sistema chamar um LLM para falar com usuários ou triar dados, **a IA só propõe JSON e o código determinístico valida** antes de gravar ou responder.

## 5. Stack deste projeto (preencha ao iniciar)

- **Linguagem / Runtime:** _(ex: TypeScript + Node 22 / Python 3.12)_
- **Banco de dados:** _(ex: SQLite via Prisma / SQLite modo WAL)_
- **Comando para rodar local:** _(ex: `npm run dev` / `python -m src.bot --once`)_
- **Comandos de validação:** _(ex: `npm test && npm run typecheck && npm run lint` / `pytest -q`)_
