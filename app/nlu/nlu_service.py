from app.core.interpretation import Interpretation
from app.core.schemas import ChatRequest


class NLUService:
    """
    Servicio de Natural Language Understanding (NLU).

    Responsabilidad:
    - analizar el texto del usuario
    - detectar intención
    - extraer entidades (slots)
    - devolver un Interpretation
    """

    def interpret(self, req: ChatRequest) -> Interpretation:
        text = req.text.lower().strip()

        # 1) HELP
        if text in {"help", "ayuda", "?", "ayúdame"}:
            return Interpretation(
                intent="help",
                confidence=1.0,
            )

        # 2) GASTOS SIN PERIODO
        if "gast" in text and not self._contains_month(text):
            return Interpretation(
                intent="get_expenses_total",
                confidence=0.6,
                needs_clarification=True,
                missing_slots=["period"],
                clarification_question=(
                    "¿De qué mes querés el total de gastos? " "Por ejemplo: enero 2026"
                ),
            )

        # 3) GASTOS CON ENERO (MVP)
        if "gast" in text and "enero" in text:
            return Interpretation(
                intent="get_expenses_total",
                confidence=0.9,
                entities={
                    "period": {
                        "type": "month",
                        "value": "2026-01",
                    }
                },
            )

        # 4) FALLBACK
        return Interpretation(
            intent="unknown",
            confidence=0.2,
        )

    def _contains_month(self, text: str) -> bool:
        months = [
            "enero",
            "febrero",
            "marzo",
            "abril",
            "mayo",
            "junio",
            "julio",
            "agosto",
            "septiembre",
            "octubre",
            "noviembre",
            "diciembre",
        ]
        return any(month in text for month in months)
