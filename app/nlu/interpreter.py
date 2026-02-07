from app.core.interpretation import Interpretation
from app.nlu.model import run_nlu  # wrapper del modelo entrenado


class NLUInterpreter:
    """
    NLU v2 (NN-based)

    Responsabilidades:
    - Ejecutar el modelo NLU
    - Devolver intent + slots semánticos + confidences
    - NO normaliza
    - NO ejecuta lógica de negocio
    """

    def interpret(self, text: str) -> Interpretation:
        result = run_nlu(text)
        print(f"NLU result: {result}")

        return Interpretation(
            intent=result["intent"],
            intent_confidence=float(result["intent_confidence"]),

            period_type=result.get("period_type"),
            period_confidence=float(result.get("period_confidence", 0.0)),

            category_hint=result.get("category_hint"),
            category_confidence=float(result.get("category_confidence", 0.0)),
        )
