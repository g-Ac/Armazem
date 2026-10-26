# Como funciona este projeto

Mapa das pastas e arquivos principais — pra você saber onde mexer.

## Pastas
- **`app/`** — todo o código do site/app.
  - **`app/routes/`** — as páginas. Cada arquivo é uma página (ex: `notes.tsx` → página `/notes`).
  - **`app/routes.ts`** — a lista que registra quais rotas existem.
  - **`app/db.server.ts`** — a conexão com o banco (Prisma). Só roda no servidor.
  - **`app/lib/`** — funções utilitárias (com testes).
  - **`app/root.tsx`** — o "esqueleto" que envolve todas as páginas.
  - **`app/app.css`** — estilos globais (Tailwind).
- **`prisma/`** — o banco de dados.
  - **`prisma/schema.prisma`** — o modelo de dados (as tabelas).
  - **`prisma/migrations/`** — histórico de mudanças no banco.
- **`public/`** — arquivos estáticos (ícone, imagens).

## Arquivos de configuração
- **`package.json`** — dependências e os comandos (`scripts`).
- **`biome.json`** — regras de estilo/lint do código.
- **`tsconfig.json`** — config do TypeScript (modo `strict` ligado).
- **`vite.config.ts`** / **`react-router.config.ts`** — config da build e do roteador.
- **`.env`** — segredos (NÃO vai pro Git). **`.env.example`** mostra quais variáveis existem.

## O exemplo pronto
A página **`app/routes/notes.tsx`** é o exemplo do padrão da casa: lê notas do banco (`loader`), cria nota nova (`action`) e mostra a lista. **Copie esse padrão** pra novas telas.
