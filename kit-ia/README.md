# kit-ia — O Cérebro Operacional para Programar com IA

Aqui está o conjunto real de instruções, subagentes, comandos, hooks e templates de memória que transforma um agente de IA (Claude Code, Codex, Cursor, Antigravity) de um "gerador de código bagunçado" num **time de engenharia disciplinado**.

## O que tem nesta pasta

| Arquivo / Pasta | Para que serve | Onde colocar |
|---|---|---|
| [`CLAUDE-BASE.md`](CLAUDE-BASE.md) | Regras universais de trabalho entre você (dono do produto) e a IA | Copie para a raiz do seu projeto como `CLAUDE.md` (ou `AGENTS.md`) |
| [`SPEC-TEMPLATE.md`](SPEC-TEMPLATE.md) | Modelo de 1 página para planejar um sistema **antes** de pedir código | Copie para `SPEC.md` na raiz do projeto novo |
| [`settings.example.json`](settings.example.json) | Exemplo de Hook que roda os testes sozinho toda vez que a IA salva um arquivo | Base para o seu `~/.claude/settings.json` |
| [`agents/`](agents/) | 3 subagentes especialistas (`architect`, `bug-hunter`, `security-auditor`) | Copie para `~/.claude/agents/` |
| [`commands/`](commands/) | 3 atalhos rápidos (`/plan-feature`, `/audit`, `/fix`) | Copie para `~/.claude/commands/` |
| [`skills/conselho/`](skills/conselho/SKILL.md) | Protocolo multiagente para tomar decisões difíceis sem viés de confirmação | Copie para `~/.claude/skills/conselho/` |
| [`memoria-obsidian/`](memoria-obsidian/README.md) | Estrutura de notas em Markdown + Git para a IA nunca perder contexto entre conversas | Abra a pasta no [Obsidian](https://obsidian.md) ou mantenha em `~/vault/` |

## Instalação rápida no Claude Code (Linux / macOS / WSL)

```bash
mkdir -p ~/.claude/agents ~/.claude/commands ~/.claude/skills/conselho
cp kit-ia/agents/*.md ~/.claude/agents/
cp kit-ia/commands/*.md ~/.claude/commands/
cp kit-ia/skills/conselho/SKILL.md ~/.claude/skills/conselho/
```

Pronto! Nos seus projetos novos, basta copiar `kit-ia/CLAUDE-BASE.md` para `./CLAUDE.md` e ajustar a seção "Stack do Projeto".
