# CLAUDE.md — instruções pra IA neste projeto

Você (IA: Claude Code / Codex / Cursor / Antigravity) deve seguir estes padrões ao gerar, revisar ou alterar código neste projeto.

## Papel do humano vs papel da IA
- **O dono do projeto decide o produto:** o que a tela faz, regras de negócio, prioridades e o que é aceitável.
- **Você (IA) cuida da técnica dentro desta stack:** proponha sempre o caminho mais simples, seguro e fácil de reverter. Se houver dúvida de regra de negócio, **pergunte em português simples** antes de sair codando.
- Ao explicar o que fez ou pedir uma decisão, traduza jargões técnicos na primeira vez que aparecerem.

## Stack (não troque sem perguntar)
- **React Router v8** (framework mode) — cada página é uma rota com `loader` / `action` / componente
- **React 19** + **Tailwind CSS v4** (estilo via classes utilitárias)
- **TypeScript** em modo `strict`
- **Prisma** + **SQLite** (`dev.db` local) — acesso a dados
- **Biome** — lint e formatação (NÃO adicione ESLint nem Prettier)
- **Vitest** — testes automáticos

## Onde fica cada coisa
- `app/routes/*.tsx` — uma rota = uma página. Exporta `loader` (ler dados), `action` (gravar dados) e o componente React.
- `app/routes.ts` — registra as rotas ativas.
- `app/db.server.ts` — cliente do Prisma. **Só use no servidor** (`loader` / `action`), nunca dentro do componente visual.
- `app/lib/*.ts` — regras de negócio e funções puras (sempre acompanhadas de `*.test.ts`).
- `prisma/schema.prisma` — tabelas do banco de dados.

> Arquivos `*.server.ts` rodam exclusivamente no servidor. Nunca importe `~/db.server` direto num componente de interface.

## Como adicionar uma funcionalidade (o padrão da casa)
1. Precisa guardar dado novo? Adicione um `model` em `prisma/schema.prisma`, rode `npx prisma migrate dev --name <nome>` e em seguida `npx prisma generate` (o client fica em `generated/prisma`).
2. Crie a rota em `app/routes/<nome>.tsx` com `loader` e `action` usando `db` de `~/db.server`.
3. Registre a rota em `app/routes.ts`.
4. Tem cálculo ou regra de negócio? Extraia para `app/lib/<regra>.ts` e crie o teste `app/lib/<regra>.test.ts`.
5. Use `app/routes/notes.tsx` como referência do padrão.

## Regras de qualidade antes de dizer "pronto"
- Faça **apenas a tarefa pedida**, um passo por vez.
- Escreva **teste** para toda lógica nova.
- Rode obrigatoriamente `npm run typecheck`, `npm test` e `npm run lint` e mostre que passaram.
- Segredos ficam no `.env` (nunca hardcoded no código). Atualize `.env.example` quando criar variável nova.
- Commits pequenos no padrão Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`).
