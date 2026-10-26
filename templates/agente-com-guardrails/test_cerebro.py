"""Testes provando que nenhuma alucinação ou falha da IA vaza para o cliente final."""
from __future__ import annotations

from cerebro import (
    MAX_TURNOS_BOT,
    MENSAGEM_FALLBACK_HUMANO,
    detectar_violacoes,
    processar_turno,
)


def test_resposta_limpa_passa_normalmente():
    def ia_ok(_msg: str) -> dict:
        return {
            "resposta": "Olá! Qual é o nome da sua empresa?",
            "dados_coletados": {"nome": "João", "empresa": "", "necessidade": "sistema web"},
            "passar_para_humano": False,
            "motivo": "coletando empresa",
        }

    res = processar_turno("Oi, sou o João", turnos_atuais=0, chamar_ia=ia_ok)
    assert res["passar_para_humano"] is False
    assert res["violacoes_bloqueadas"] == []
    assert "empresa" in res["resposta"]


def test_guardrail_barra_promessa_de_preco_e_prazo():
    def ia_alucinada(_msg: str) -> dict:
        return {
            "resposta": "Faço por R$ 150 reais com desconto e fica pronto amanhã, eu garanto!",
            "dados_coletados": {"nome": "Maria", "empresa": "Padaria", "necessidade": "site"},
            "passar_para_humano": False,
            "motivo": "tentou vender",
        }

    res = processar_turno("Quanto custa?", turnos_atuais=1, chamar_ia=ia_alucinada)
    assert res["passar_para_humano"] is True
    assert res["resposta"] == MENSAGEM_FALLBACK_HUMANO
    assert "promessa_de_preco_ou_desconto" in res["violacoes_bloqueadas"]
    assert "garantia_indevida" in res["violacoes_bloqueadas"]
    assert "promessa_de_prazo" in res["violacoes_bloqueadas"]
    # Os dados úteis que a IA já tinha extraído continuam preservados para o atendente humano!
    assert res["dados_coletados"]["nome"] == "Maria"


def test_json_quebrado_ou_excecao_cai_em_fallback_seguro():
    def ia_quebrada(_msg: str):
        return "texto solto que não é dicionário JSON"

    res = processar_turno("Oi", turnos_atuais=0, chamar_ia=ia_quebrada)
    assert res["passar_para_humano"] is True
    assert res["motivo"] == "json_invalido_da_ia"
    assert res["resposta"] == MENSAGEM_FALLBACK_HUMANO


def test_limite_de_turnos_transfere_para_humano():
    res = processar_turno("Mais uma pergunta", turnos_atuais=MAX_TURNOS_BOT)
    assert res["passar_para_humano"] is True
    assert "limite" in res["motivo"]


def test_nao_permite_fingir_ser_humano():
    violacoes = detectar_violacoes("Fique tranquilo, não sou um robô, sou uma pessoa de verdade.")
    assert "fingir_ser_humano" in violacoes
