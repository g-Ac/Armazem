# Memória de Engenharia (Obsidian + Git)

Conversas de chat com IA acabam e esquecem detalhes importantes. **Arquivos Markdown salvos no Git não esquecem nunca.**

Esta pasta é um modelo enxuto de "segundo cérebro" para seus projetos. Você pode abri-la gratuitamente no **[Obsidian](https://obsidian.md/)** ou direto no VS Code, e pedir para a IA ler ou registrar notas aqui.

## Estrutura sugerida

```text
meu-vault/
├── knowledge/          # Conhecimento permanente (como sua infra funciona, checklists, padrões)
├── context/
│   ├── decisoes/       # Por que escolhemos X em vez de Y (ADRs curtos)
│   ├── incidentes/     # O que quebrou, por que quebrou e como evitamos repetir
│   └── aprendizados/   # Descobertas práticas que economizam horas no futuro
└── templates/          # Modelos prontos de 15 linhas
    ├── decisao.md
    ├── incidente.md
    └── aprendizado.md
```

## Quando criar uma nota?
- **Decisão (`decisao.md`)**: trocou de banco? Escolheu uma biblioteca? Definiu uma regra de segurança? Anote em 5 minutos.
- **Incidente (`incidente.md`)**: um bot travou de madrugada ou um deploy deu erro? Anote a causa raiz antes de esquecer.
- **Aprendizado (`aprendizado.md`)**: descobriu uma pegadinha que tomou 2 horas? Registre para a IA nunca mais cair nela.
