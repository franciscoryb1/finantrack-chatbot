from app.core.interpretation import Interpretation
from app.core.schemas import ChatRequest
from app.nlu.rules_nlu import RulesNLU
from app.nlu.intent_classifier.classifier import IntentClassifierService

from typing import Optional
import anyio


class NLUService:
    """
    NLU híbrido v2:
    1) Rules (determinístico, alta confianza)
    2) ML intent classifier
    3) LLM fallback (async encapsulado)
    """

    RULES_MIN_CONFIDENCE = 0.85
    ML_MIN_CONFIDENCE = 0.65
    
    ALLOWED_INTENTS = {
        "get_balance",
        "get_movements",
        "get_expenses_total",
        "get_expenses_by_category",
        "help",
        "unknown",
    }

    def __init__(self, llm_fallback: Optional[object] = None):
        self._rules = RulesNLU()
        self._classifier = IntentClassifierService()
        self._llm_fallback = llm_fallback

    def interpret(self, req: ChatRequest) -> Interpretation:
        text = req.text.strip()
        t = text.lower()

        # 1) RULES
        rules_result = self._rules.interpret(text)

        if rules_result.confidence >= self.RULES_MIN_CONFIDENCE:
            return self._finalize_with_slot_validation(rules_result, t)

        if rules_result.needs_clarification:
            return rules_result

        # 2) ML CLASSIFIER
        pred = self._classifier.predict(text)

        if pred.confidence >= self.ML_MIN_CONFIDENCE:
            ml_result = Interpretation(
                intent=pred.intent,
                confidence=pred.confidence,
            )
            return self._finalize_with_slot_validation(ml_result, t)

        # 3) LLM FALLBACK (ENCAPSULADO)
        llm_result = self._call_llm_fallback(text)

        if llm_result.intent in self.ALLOWED_INTENTS and llm_result.intent != "unknown":
            return self._finalize_with_slot_validation(llm_result, t)

        # 4) UNKNOWN
        return Interpretation(intent="unknown", confidence=0.0)

    def _call_llm_fallback(self, text: str) -> Interpretation:
        if not self._llm_fallback:
            return Interpretation(intent="unknown", confidence=0.0)

        try:
            return anyio.run(self._llm_fallback.suggest, text)
        except Exception:
            return Interpretation(intent="unknown", confidence=0.0)

    def _finalize_with_slot_validation(
        self, result: Interpretation, normalized_text: str
    ) -> Interpretation:
        """
        Validación simple de slots obligatorios.
        Esto mantiene la lógica consistente para rules / ML / LLM.
        """

        if result.intent == "get_expenses_total":
            # Heurística simple: si el texto menciona un período, no pedir aclaración
            period_keywords = [
                "enero", "febrero", "marzo", "abril", "mayo", "junio",
                "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
                "mes", "ayer", "hoy", "semana", "año", "pasado", "este"
            ]

            if not result.entities.get("period") and not any(
                kw in normalized_text for kw in period_keywords
            ):
                return Interpretation(
                    intent="get_expenses_total",
                    confidence=result.confidence,
                    needs_clarification=True,
                    missing_slots=["period"],
                    clarification_question=(
                        "¿De qué período querés el total de gastos? "
                        "Por ejemplo: enero, este mes, el mes pasado."
                    ),
                )


        return result
