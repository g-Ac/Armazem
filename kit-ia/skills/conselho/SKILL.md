---
name: conselho
description: "Use quando o usuário pedir para 'chamar o conselho' antes de uma decisão importante de arquitetura, produto, ferramenta ou negócio."
version: 1.0.0
---

# Conselho de Decisões

## Objetivo
Ajudar o dono do projeto a decidir sobre arquitetura, produto, automação ou operação com **evidência e contraponto real**, evitando que a IA apenas concorde com a primeira ideia (*viés de confirmação*). Responder em português simples.

## 1. Preparação (somente leitura)
1. Defina claramente: a decisão concreta, as opções (incluindo **não fazer nada agora**), as restrições e o critério de sucesso.
2. Separe **fatos verificados** (arquivos do projeto, documentação oficial, números medidos) de **hipóteses/estimativas**.
3. Se faltar uma informação decisiva (ex: orçamento, volume esperado ou prazo), pergunte antes de convocar os pareceres.

## 2. Pareceres independentes (via subagentes, se disponível)
Se a ferramenta possuir subagentes, envie o mesmo briefing neutro (sem revelar sua opção favorita) para 3 papéis independentes em modo **somente leitura**:
- **Negócio e Prioridade**: custo de oportunidade, tempo pra colocar no ar e opção de simplificar.
- **Especialista Técnico**: viabilidade, manutenção, segurança e aderência à stack atual.
- **Revisor Crítico**: caça premissas frágeis, riscos escondidos e qual seria a alternativa mais simples de todas.

*(Se o ambiente não suportar subagentes paralelos, avise com transparência e analise explicitamente sob as 3 lentes.)*

## 3. Formato da síntese final
Entregue direto ao ponto:
1. **Recomendação e por quê** (em linguagem simples).
2. **Fatos vs Hipóteses** que sustentam a escolha.
3. **Principal risco ou argumento contra**.
4. **Menor próximo passo reversível** (como testar rápido sem se comprometer por meses).
5. **O que mudaria essa decisão** (critério de revisão).

> Regra de ouro: o conselho apenas recomenda; **quem bate o martelo é o humano**. Nunca invente estatísticas, preços ou probabilidades sem fonte.
