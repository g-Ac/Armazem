---
name: fix
description: Diagnostica um erro ou falha nos testes, encontra a causa raiz e corrige com teste
---

Algo quebrou ou não está funcionando como esperado. Siga este roteiro sem chutar:

1. **Reproduza o erro**: rode os testes, cheque os logs recentes ou execute o comando que falha para ver a mensagem exata.
2. **Encontre a causa raiz**: leia o arquivo e a linha onde ocorre o problema (não coloque remendo superficial sem entender o motivo).
3. **Crie ou ajuste um teste** que pega exatamente esse bug.
4. **Aplique a menor correção segura** e rode todos os testes novamente para provar que resolveu sem quebrar o resto.
5. Explique em 3 linhas simples: o que causou, o que você mudou e como testou.
