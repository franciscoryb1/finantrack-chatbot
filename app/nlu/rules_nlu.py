from app.core.interpretation import Interpretation


class RulesNLU:
    """
    NLU determinístico: rápido y confiable para casos obvios.
    Devuelve Interpretation con confidence alta cuando aplica.
    """

    def interpret(self, text: str) -> Interpretation:
        t = text.lower().strip()

        # HELP muy obvio
        if t in {"help", "ayuda", "?", "ayúdame"}:
            return Interpretation(intent="help", confidence=1.0)

        # Si detectamos meses y "gast", podemos inferir algo sin ML
        if "gast" in t and "enero" in t:
            return Interpretation(
                intent="get_expenses_total",
                confidence=0.95,
                entities={"period": {"type": "month", "value": "2026-01"}},
            )

        # Si vemos "gast" pero no periodo -> pedir aclaración (regla útil)
        if "gast" in t and not self._contains_month(t):
            return Interpretation(
                intent="get_expenses_total",
                confidence=0.6,
                needs_clarification=True,
                missing_slots=["period"],
                clarification_question="¿De qué mes querés el total de gastos? Por ejemplo: enero 2026",
            )

        # Si no aplica regla, devolvemos unknown con baja confianza
        return Interpretation(intent="unknown", confidence=0.0)

    def _contains_month(self, text: str) -> bool:
        months = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
        ]
        return any(m in text for m in months)
