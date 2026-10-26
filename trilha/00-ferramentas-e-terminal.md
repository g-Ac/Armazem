# Módulo 00 — Ferramentas, Terminal e Git sem Medo

> **Tempo estimado:** 30 a 45 minutos (uma única vez)
> **Meta prática:** sair deste módulo com o ambiente instalado, dominando os 10 comandos de terminal que resolvem 95% da vida real e com este repositório rodando na sua máquina.

---

## 1. O que você precisa instalar no PC

Você não precisa de um computador caro. Qualquer notebook ou PC comum dá conta tranquilamente:

1. **Terminal decente**:
   - **Windows**: instale o **WSL2 (Ubuntu)** (`wsl --install` no PowerShell como Administrador). Quase todo servidor do mundo roda Linux — usar o Ubuntu dentro do Windows já te treina pro mundo real desde o dia 1!
   - **Linux ou macOS**: o terminal nativo já está pronto.
2. **Editor de código**: [VS Code](https://code.visualstudio.com/) (leve, gratuito e abre pastas direto do terminal com `code .`).
3. **Node.js (versão 20 ou 22 LTS)**: usado para rodar sistemas web modernos ([nodejs.org](https://nodejs.org/)).
4. **Python (3.10+)**: usado para criar bots, automações, scripts e integrações de IA.
5. **Git + conta no GitHub**: sua "máquina do tempo" do código. Se algo quebrar, você volta ao estado anterior em 1 segundo.
6. **Seu Agente de Código com IA** (escolha um para trabalhar no terminal/editor):
   - **Claude Code** (`npm install -g @anthropic-ai/claude-code` -> comando `claude`)
   - **Codex CLI**, **Antigravity** ou **Cursor**.

### Conferindo se tudo está instalado

Abra o terminal e rode:

```bash
node -v        # deve mostrar v20.x ou v22.x+
npm -v         # gerenciador de pacotes do Node
python3 --version
git --version
```

---

## 2. Os 10 comandos de terminal que resolvem 95% do dia a dia

Esqueça decorar livros de Linux. No dia a dia você só usa isto aqui:

| Comando | Tradução prática | Exemplo |
|---|---|---|
| `pwd` | "Onde eu estou agora?" | Mostra `/home/seu-usuario/projects` |
| `ls -la` | "O que tem dentro desta pasta?" (inclusive arquivos ocultos como `.env`) | `ls -la` |
| `cd <pasta>` | Entra numa pasta (`cd ..` sobe um nível, `cd ~` volta pra sua pasta inicial) | `cd templates/web-fullstack` |
| `mkdir -p <pasta>` | Cria uma pasta nova | `mkdir -p ~/projects` |
| `cp <origem> <destino>` | Copia um arquivo | `cp .env.example .env` |
| `cat <arquivo>` | Mostra o conteúdo de um arquivo pequeno na tela | `cat README.md` |
| `Ctrl + C` | **Para imediatamente** o programa que está rodando no terminal | Segure `Ctrl` e aperte `C` |
| `grep -rn "texto" .` | Procura onde uma palavra aparece dentro de todos os arquivos | `grep -rn "DATABASE_URL" .` |
| `code .` | Abre a pasta atual no VS Code | `code .` |
| `clear` | Limpa a tela do terminal | `clear` |

---

## 3. Git em 5 comandos (sua rede de segurança)

Pense no Git como **checkpoints de videogame**. Nunca faça mudanças grandes sem salvar um checkpoint funcionando antes!

```bash
# 1. Baixar este repositório para sua pasta de projetos
mkdir -p ~/projects && cd ~/projects
git clone https://github.com/g-Ac/Armazem.git
cd Armazem

# 2. Ver o que você alterou desde o último checkpoint
git status

# 3. Ver exatamente quais linhas mudaram
git diff

# 4. Salvar um checkpoint local (commit)
git add .
git commit -m "feat: adiciona tela de cadastro de tarefas"

# 5. Enviar seus checkpoints para o seu GitHub
git push
```

> ⚠️ **Regra de sobrevivência nº 1:** Antes de dar `git add .`, sempre olhe o `git status` para garantir que nenhum arquivo `.env` (com senhas/chaves) ou banco `.db` está indo junto!

---

## ✅ Entrega prática deste módulo (Critério de Pronto)

Você concluiu o Módulo 00 quando conseguir executar isto no seu terminal sem erro:

```bash
cd ~/projects/Armazem
ls -la
python3 templates/agente-com-guardrails/simular_conversa.py
```

Digite `Oi` no simulador, veja o robô responder, digite `sair` e siga para o **[Módulo 01 — O Método para Construir com IA](01-metodo-com-ia.md)**!
