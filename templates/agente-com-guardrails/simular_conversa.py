"""Simulador interativo no terminal para testar o padrão 'IA propõe JSON -> código trava'."""
from __future__ import annotations

import os
from cerebro import processar_turno, provedor_mock, provedor_openai_compativel


def main() -> None:
    usar_api = os.environ.get("PROVIDER", "mock").lower() == "api"
    provedor = provedor_openai_compativel if usar_api else provedor_mock

    print("==================================================================")
    print(" Simulador de Agente com Guardrails ('A IA propõe, o código trava')")
    print(f" Provedor ativo: {'API LLM Real' if usar_api else 'Mock Local (grátis/offline)'}")
    print(" Dica: digite 'quero desconto no preço' para ver a trava em ação!")
    print(" Digite 'sair' para encerrar.")
    print("==================================================================\n")

    turno = 0
    while True:
        try:
            msg = input(f"[Turno {turno + 1}] Cliente: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando simulador.")
            break

        if not msg or msg.lower() in {"sair", "exit", "quit"}:
            break

        resultado = processar_turno(msg, turnos_atuais=turno, chamar_ia=provedor)
        turno += 1

        print(f"🤖 Bot: {resultado['resposta']}")
        if resultado["violacoes_bloqueadas"]:
            print(f"🛡️ GUARDRAIL ATIVADO! Bloqueou: {resultado['violacoes_bloqueadas']}")
        print(
            f"   [status] passar_para_humano={resultado['passar_para_humano']} | motivo={resultado['motivo']}\n"
        )

        if resultado["passar_para_humano"]:
            print("➡️ Conversa transferida para fila humana. Fim do atendimento automático.")
            break


if __name__ == "__main__":
    main()
