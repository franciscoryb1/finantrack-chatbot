from __future__ import annotations

import re
import unicodedata
from typing import Tuple


INTENT_SHOW_MOVEMENTS = "SHOW_MOVEMENTS"
INTENT_UNKNOWN = "UNKNOWN"


# Palabras y frases típicas de consulta de movimientos/transacciones.
# Esto NO es el Gate (seguridad), esto es NLU (tool-intent).
_MOVEMENTS_PATTERNS = [
    r"\bmovimient(?:o|os)\b",
    r"\btransacci(?:o|ó)n(?:es)?\b",
    r"\bgast(?:o|os|e|é|aste|é)\b",
    r"\bconsum(?:o|os)\b",
    r"\bactividad\b",
    r"\bpag(?:o|os)\b",
    r"\bcompr(?:a|as|é)\b",
    r"\bgastos?\s+de\b",
    r"\bver\b.*\bmovimient",
    r"\bmostr(?:a|ame|ame)\b.*\bmovimient",
]


def _normalize(text: str) -> str:
    """
    Normaliza texto: lower + remueve tildes + espacios.
    """
    text = (text or "").strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"\s+", " ", text)
    return text


def detect_intent(text: str) -> Tuple[str, float, str | None]:
    """
    Devuelve: (intent, confidence, reason)

    - intent: SHOW_MOVEMENTS | UNKNOWN
    - confidence: score informativo (NO es decisorio)
    - reason: regla que matcheó (útil para logs)
    """
    t = _normalize(text)

    for pattern in _MOVEMENTS_PATTERNS:
        if re.search(pattern, t):
            return INTENT_SHOW_MOVEMENTS, 0.90, f"pattern:{pattern}"

    return INTENT_UNKNOWN, 0.20, "no_match"
