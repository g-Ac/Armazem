---
name: audit
description: Faz uma revisão completa de qualidade, testes, erros e segurança do projeto atual
---

Faça uma auditoria completa do projeto atual verificando:

1. **Testes e tipagem**: rode a suíte de testes e o linter/typecheck do projeto e reporte o resultado real.
2. **Bugs e riscos**: revise os arquivos principais procurando exceções engolidas, falhas de borda ou código morto.
3. **Segurança**: confirme se `.env` e bancos locais estão protegidos no `.gitignore` e se não há credenciais hardcoded.
4. **Próximos passos**: consolide tudo num relatório curto, priorizado por impacto (Crítico -> Importante -> Melhoria).
