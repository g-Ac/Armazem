# SPEC — [Nome do Sistema ou Automação]

**Data:** AAAA-MM-DD · **Status:** Rascunho / Aprovado

---

## 1. Qual dor real isso resolve?
_(Explique em 2 ou 3 frases simples: quem usa, o que hoje é manual/lento/confuso e o que muda quando estiver pronto.)_

## 2. O que o sistema FAZ na versão 1 (Escopo Mínimo)
- [ ] Funcionalidade essencial 1
- [ ] Funcionalidade essencial 2
- [ ] Funcionalidade essencial 3

## 3. O que FICA DE FORA agora (para não travar tentando fazer tudo)
- Não terá login multi-empresa complexo na v1
- Não terá aplicativo mobile nativo na v1

## 4. Como o usuário interage (Telas ou Comandos)
_(Se for Web: liste as páginas, ex: `/clientes`, `/novo-pedido`. Se for Bot no Telegram: liste os comandos/botões, ex: `/status`, `/resumo`.)_

## 5. Dados que precisam ser salvos (Tabelas)
- **Tabela 1 (`...`)**: quais campos guarda?
- **Tabela 2 (`...`)**: quais campos guarda?

## 6. Regras de segurança e limites
- Quem pode acessar ou disparar ações?
- Alguma ação exige aprovação humana antes de executar?
- Quais variáveis vão no `.env`?

## 7. Critério de Pronto (GO / NO-GO)
_(Como sabemos, sem sombra de dúvida, que a versão 1 funciona? Ex: "Consigo cadastrar um pedido na tela, recarregar a página, ver salvo no SQLite e `npm test` passa 100%".)_
