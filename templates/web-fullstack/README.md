# web-fullstack — Esqueleto pronto de Sistema Web

Base pronta para criar sistemas web completos (telas + servidor + banco de dados num lugar só), sem perder dias configurando ferramenta.

**Stack incluída:**
- **React Router v8** (fullstack) + **React 19** + **Tailwind CSS v4**
- **TypeScript** (`strict`)
- **Prisma** + **SQLite** (banco de dados local num arquivo `dev.db`, zero instalação de servidor)
- **Biome** (formatação e lint rápidos) + **Vitest** (testes automáticos)

> 📖 Estudando pela trilha? Siga o guia passo a passo em [`../../trilha/02-primeiro-sistema-web.md`](../../trilha/02-primeiro-sistema-web.md).

## Rodar em 4 comandos

Pré-requisito: **Node.js 20+** instalado.

```bash
# 1. Copiar o arquivo de configuração de exemplo
cp .env.example .env

# 2. Instalar dependências (já gera o cliente do banco automaticamente)
npm install

# 3. Criar o banco de dados local (arquivo dev.db)
npx prisma migrate dev

# 4. Subir o servidor de desenvolvimento
npm run dev
```

Abra **http://localhost:5173** no navegador e teste a página de exemplo em **http://localhost:5173/notes**.

## Comandos do dia a dia

| Comando | O que faz |
|---|---|
| `npm run dev` | Roda local e atualiza a tela sozinho ao salvar |
| `npm test` | Roda os testes automáticos (Vitest) |
| `npm run typecheck` | Confere se os tipos do TypeScript batem |
| `npm run lint` | Confere estilo e possíveis erros (Biome) |
| `npm run format` | Formata o código automaticamente |
| `npx prisma migrate dev --name <nome>` | Atualiza o banco após mudar `prisma/schema.prisma` |
| `npx prisma generate` | Regenera o cliente TypeScript do banco |
| `npm run build` | Gera a versão de produção |

## Mapa rápido para não se perder

- **[`docs/COMO-FUNCIONA.md`](docs/COMO-FUNCIONA.md)** — o que cada pasta e arquivo faz
- **[`docs/GLOSSARIO.md`](docs/GLOSSARIO.md)** — tradução em 1 linha de cada termo técnico
- **[`CLAUDE.md`](CLAUDE.md)** — regras prontas que a IA lê antes de mexer no código
- **[`app/routes/notes.tsx`](app/routes/notes.tsx)** — exemplo real completo (lê do banco, grava pelo formulário e renderiza na tela)
