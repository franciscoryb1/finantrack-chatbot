from app.core.interpretation import Interpretation
from app.core.schemas import ChatRequest
from app.nlu.rules_nlu import RulesNLU
from app.nlu.intent_classifier.classifier import IntentClassifierService


class NLUService:
    RULES_MIN_CONFIDENCE = 0.85
    ML_MIN_CONFIDENCE = 0.65

    def __init__(self):
        self._rules = RulesNLU()
        self._classifier = IntentClassifierService()

    def interpret(self, req: ChatRequest) -> Interpretation:
        text = req.text.strip()
        t = text.lower().strip()

        # 1) Rules
        rules_result = self._rules.interpret(text)

        if rules_result.confidence >= self.RULES_MIN_CONFIDENCE:
            return self._finalize_with_slot_validation(rules_result, t)

        # 2) ML fallback
        pred = self._classifier.predict(text)

        if pred.confidence < self.ML_MIN_CONFIDENCE:
            return Interpretation(intent="unknown", confidence=pred.confidence)

        ml_result = Interpretation(intent=pred.intent, confidence=pred.confidence)
        return self._finalize_with_slot_validation(ml_result, t)

    def _finalize_with_slot_validation(
        self, result: Interpretation, text: str
    ) -> Interpretation:
        """
        Valida slots obligatorios antes de devolver el resultado final.
        """

        # get_expenses_total REQUIERE período
        if result.intent == "get_expenses_total":
            if not self._has_period(text):
                return Interpretation(
                    intent="get_expenses_total",
                    confidence=result.confidence,
                    needs_clarification=True,
                    missing_slots=["period"],
                    clarification_question=(
                        "¿De qué período querés el total de gastos? "
                        "Por ejemplo: enero 2026 o “este mes”."
                    ),
                )

        return result

    def _has_period(self, t: str) -> bool:
        months = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
        ]
        if any(m in t for m in months):
            return True

        if (
            "este mes" in t
            or "mes pasado" in t
            or "ayer" in t
            or "hoy" in t
            or "últimos" in t
            or "ultimos" in t
        ):
            return True

        return False
