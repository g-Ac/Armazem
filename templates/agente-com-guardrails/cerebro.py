"""Padrão de Ouro: 'A IA propõe (JSON), o código valida e trava.'

Nunca deixe um modelo de IA ter a última palavra sobre preço, prazo, promessas jurídicas
ou escrita direta no banco de dados. A IA devolve uma proposta estruturada (JSON); o código
determinístico confere cada regra e, se algo violar a política, escala com segurança para um humano.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
import urllib.request

MAX_TURNOS_BOT = 5

MENSAGEM_FALLBACK_HUMANO = (
    "Obrigado pelas informações! Vou passar sua conversa agora mesmo para um especialista "
    "do nosso time continuar seu atendimento com segurança."
)

CAMPOS_LEAD = ("nome", "empresa", "necessidade")

# Regras determinísticas sobre o texto normalizado (minúsculo e sem acentos).
# Mesmo que o cliente tente "enganar" o prompt (prompt injection), o código barra na saída!
REGRAS_PROIBIDAS: list[tuple[str, str]] = [
    (r"r\$|\breais\b|\bdesconto\b|\bmensalidade\b|\bgratis\b|\bgratuito\b", "promessa_de_preco_ou_desconto"),
    (r"\bgarant(o|imos|ido)\b|\b100%\b|\bsem risco\b", "garantia_indevida"),
    (r"\b(hoje ainda|em \d+ minutos|entrega amanha|pronto amanha)\b", "promessa_de_prazo"),
    (r"\bsou (uma )?(pessoa|humano|atendente real)\b|\bnao sou (um )?robo\b", "fingir_ser_humano"),
]


def normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in sem_acento if not unicodedata.combining(c))


def detectar_violacoes(resposta_ia: str) -> list[str]:
    texto_limpo = normalizar(resposta_ia)
    return [nome for padrao, nome in REGRAS_PROIBIDAS if re.search(padrao, texto_limpo)]


def validar_estrutura(proposta: object) -> dict | None:
    """Garante que a saída da IA respeita exatamente o contrato esperado."""
    if not isinstance(proposta, dict):
        return None
    resposta = proposta.get("resposta")
    passar_humano = proposta.get("passar_para_humano")
    motivo = proposta.get("motivo", "")
    dados = proposta.get("dados_coletados", {})

    if not isinstance(resposta, str) or not resposta.strip():
        return None
    if not isinstance(passar_humano, bool):
        return None
    if not isinstance(dados, dict):
        return None

    dados_limpos = {campo: str(dados.get(campo, "")).strip() for campo in CAMPOS_LEAD}
    return {
        "resposta": resposta.strip(),
        "dados_coletados": dados_limpos,
        "passar_para_humano": passar_humano,
        "motivo": str(motivo).strip(),
    }


def provedor_mock(mensagem_cliente: str) -> dict:
    """Simulador local para estudar e testar sem gastar 1 centavo de API.
    Dica: digite 'quero desconto' ou 'garante prazo hoje?' no simulador para ver o guardrail agir!
    """
    msg = normalizar(mensagem_cliente)
    if "desconto" in msg or "preco" in msg:
        # Simula uma IA "alucinando" uma oferta proibida para provar que o código trava!
        return {
            "resposta": "Consigo te fazer R$ 99 por mês com desconto especial hoje ainda!",
            "dados_coletados": {"nome": "", "empresa": "", "necessidade": "preço"},
            "passar_para_humano": False,
            "motivo": "tentou fechar venda sozinho",
        }
    if "humano" in msg or "atendente" in msg:
        return {
            "resposta": "Claro! Já estou chamando alguém da nossa equipe para falar com você.",
            "dados_coletados": {"nome": "", "empresa": "", "necessidade": "falar com humano"},
            "passar_para_humano": True,
            "motivo": "cliente pediu humano",
        }
    return {
        "resposta": "Olá! Sou o assistente virtual da triagem. Qual é o seu nome, empresa e como podemos ajudar?",
        "dados_coletados": {"nome": "", "empresa": "", "necessidade": mensagem_cliente[:80]},
        "passar_para_humano": False,
        "motivo": "coleta inicial",
    }


def provedor_openai_compativel(mensagem_cliente: str) -> dict:
    """Funciona com Ollama local, Bifrost, OpenRouter ou OpenAI via variáveis de ambiente."""
    base_url = os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1").rstrip("/")
    api_key = os.environ.get("LLM_API_KEY", "local")
    model = os.environ.get("LLM_MODEL", "gemma4:e4b")

    system_prompt = (
        "Você é um assistente de triagem inicial. Nunca informe preços, descontos ou prazos. "
        "Responda APENAS um objeto JSON válido com as chaves: "
        "resposta (string), dados_coletados ({nome, empresa, necessidade}), "
        "passar_para_humano (boolean) e motivo (string)."
    )
    body = json.dumps(
        {
            "model": model,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensagem_cliente},
            ],
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = json.loads(resp.read().decode("utf-8"))
        content = raw["choices"][0]["message"]["content"]
        return json.loads(content)


def processar_turno(
    mensagem_cliente: str,
    *,
    turnos_atuais: int,
    chamar_ia=provedor_mock,
) -> dict:
    """Fluxo completo com trava determinística:
    1. Checa limite de turnos
    2. Pede proposta JSON à IA
    3. Valida formato do JSON
    4. Audita regras proibidas na resposta
    5. Em qualquer falha ou violação -> fallback seguro para humano!
    """
    if turnos_atuais >= MAX_TURNOS_BOT:
        return {
            "resposta": MENSAGEM_FALLBACK_HUMANO,
            "dados_coletados": {c: "" for c in CAMPOS_LEAD},
            "passar_para_humano": True,
            "motivo": f"limite_de_{MAX_TURNOS_BOT}_turnos_atingido",
            "violacoes_bloqueadas": [],
        }

    try:
        proposta_bruta = chamar_ia(mensagem_cliente)
    except Exception as exc:  # noqa: BLE001
        return {
            "resposta": MENSAGEM_FALLBACK_HUMANO,
            "dados_coletados": {c: "" for c in CAMPOS_LEAD},
            "passar_para_humano": True,
            "motivo": f"erro_provedor_ia:{type(exc).__name__}",
            "violacoes_bloqueadas": [],
        }

    validada = validar_estrutura(proposta_bruta)
    if validada is None:
        return {
            "resposta": MENSAGEM_FALLBACK_HUMANO,
            "dados_coletados": {c: "" for c in CAMPOS_LEAD},
            "passar_para_humano": True,
            "motivo": "json_invalido_da_ia",
            "violacoes_bloqueadas": [],
        }

    violacoes = detectar_violacoes(validada["resposta"])
    if violacoes:
        return {
            "resposta": MENSAGEM_FALLBACK_HUMANO,
            "dados_coletados": validada["dados_coletados"],
            "passar_para_humano": True,
            "motivo": "violacao_bloqueada_pelo_guardrail",
            "violacoes_bloqueadas": violacoes,
        }

    validada["violacoes_bloqueadas"] = []
    return validada
