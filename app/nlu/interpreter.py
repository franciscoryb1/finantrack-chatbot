from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from app.core.interpretation import Interpretation
from app.nlu.rules import detect_intent, extract_date_range


class NLUInterpreter:
    """
    NLU v1 (rules-only), orientado a tools.
    - Detecta intent SHOW_MOVEMENTS
    - Extrae entidades (from_date, to_date, page, page_size)
    - No ejecuta tools, no usa LLM
    """

    def __init__(self, locale: str = "es_AR"):
        self.locale = locale

    def interpret(
        self,
        text: str,
        *,
        now: Optional[datetime] = None,
    ) -> Interpretation:
        intent, conf, intent_reason = detect_intent(text)
        
        print('Detected intent:', intent, 'with confidence:', conf)

        entities: Dict[str, Any] = {}

        # Solo extraemos entidades si el intent es SHOW_MOVEMENTS
        if intent == "SHOW_MOVEMENTS":
            dr = extract_date_range(text, now=now)
            if dr.from_date:
                entities["from_date"] = dr.from_date
            if dr.to_date:
                entities["to_date"] = dr.to_date

            # v1: paginación por default (podés elegir no setearlos)
            entities["page"] = 1
            entities["page_size"] = 20

            # Guardamos razones internas útiles para logs/debug
            # (si no querés ensuciar entities, podés moverlo a logging)
            entities["_debug"] = {
                "intent_reason": intent_reason,
                "date_reason": dr.reason,
            }

        return Interpretation(
            intent=intent,
            confidence=float(conf),
            entities=entities,
            needs_clarification=False,
            missing_slots=[],
            clarification_question=None,
        )
