from __future__ import annotations
import re
import unicodedata
from enum import Enum
from dataclasses import dataclass
from typing import List


class AccessLevel(str, Enum):
    REAL_DATA_REQUIRED = "real_data_required"
    NO_REAL_DATA = "no_real_data"


@dataclass(frozen=True)
class AccessDecision:
    access_level: AccessLevel
    reasons: List[str]


# --------------------------------------------------
# Normalización
# --------------------------------------------------

def _normalize(text: str) -> str:
    """
    Normaliza texto para matching determinista:
    - lower
    - sin tildes
    - espacios simples
    """
    text = (text or "").strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"\s+", " ", text)
    return text


# --------------------------------------------------
# Reglas del Gate
# --------------------------------------------------

_FINANCIAL_KEYWORDS = [
    # núcleo financiero
    "gasto", "gastos", "gaste", "gaste", "gaste", "gaste",
    "movimiento", "movimientos",
    "transaccion", "transacciones",
    "consumo", "consumos",
    "saldo", "balance",
    "ingreso", "ingresos",
    "egreso", "egresos",
    "cuenta", "cuentas",
    "actividad",
]

_TEMPORAL_KEYWORDS = [
    "hoy",
    "ayer",
    "este mes",
    "mes pasado",
    "ultimo mes",
    "esta semana",
    "este año",
]

_QUANTIFIERS = [
    "cuanto",
    "cuanta",
    "cuantos",
    "total",
]

_EXPLICIT_NON_FINANCIAL = [
    "hola",
    "buen dia",
    "buenas",
    "gracias",
    "help",
    "ayuda",
    "que podes hacer",
    "como funcionas",
]


# --------------------------------------------------
# Decisión principal
# --------------------------------------------------

def decide_access(text: str) -> AccessDecision:
    """
    Decide si el mensaje puede requerir acceso a datos reales.
    """

    t = _normalize(text)
    reasons: List[str] = []

    # 1️⃣ Exclusiones explícitas (saludos, ayuda)
    for phrase in _EXPLICIT_NON_FINANCIAL:
        if phrase in t:
            return AccessDecision(
                access_level=AccessLevel.NO_REAL_DATA,
                reasons=[f"explicit_non_financial:{phrase}"],
            )

    # 2️⃣ Keywords financieros directos
    for kw in _FINANCIAL_KEYWORDS:
        if kw in t:
            reasons.append(f"financial_keyword:{kw}")

    # 3️⃣ Cuantificadores + temporal
    has_quantifier = any(q in t for q in _QUANTIFIERS)
    has_temporal = any(tmp in t for tmp in _TEMPORAL_KEYWORDS)

    if has_quantifier and has_temporal:
        reasons.append("quantifier+temporal")

    # 4️⃣ Decisión final
    if reasons:
        return AccessDecision(
            access_level=AccessLevel.REAL_DATA_REQUIRED,
            reasons=reasons,
        )

    return AccessDecision(
        access_level=AccessLevel.NO_REAL_DATA,
        reasons=["no_financial_signals"],
    )
