from app.core.interpretation import Interpretation
from app.core.schemas import ChatRequest
from app.nlu.rules_nlu import RulesNLU
from app.nlu.intent_classifier.classifier import IntentClassifierService


class NLUService:
    """
    NLU híbrido:
    1) Reglas (rápidas y determinísticas)
    2) Intent Classifier (ML) como fallback
    """

    RULES_MIN_CONFIDENCE = 0.85
    ML_MIN_CONFIDENCE = 0.65

    def __init__(self):
        self._rules = RulesNLU()
        self._classifier = IntentClassifierService()

    def interpret(self, req: ChatRequest) -> Interpretation:
        text = req.text.strip()

        # 1) Reglas primero
        rules_result = self._rules.interpret(text)
        if rules_result.confidence >= self.RULES_MIN_CONFIDENCE:
            return rules_result

        # Si reglas determinan que falta info, respetamos eso
        if rules_result.needs_clarification:
            return rules_result

        # 2) ML classifier fallback
        pred = self._classifier.predict(text)

        if pred.confidence < self.ML_MIN_CONFIDENCE:
            return Interpretation(intent="unknown", confidence=pred.confidence)

        return Interpretation(intent=pred.intent, confidence=pred.confidence)
