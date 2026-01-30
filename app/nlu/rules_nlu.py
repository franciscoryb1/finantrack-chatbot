from app.core.interpretation import Interpretation


class RulesNLU:
    """
    Rules minimalistas: solo casos obvios y de alta confianza.
    No intentan cubrir lenguaje libre ni variaciones infinitas.
    """

    HELP_SET = {"help", "ayuda", "?", "ayúdame", "como funciona", "qué podés hacer"}

    BALANCE_KEYWORDS = {
        "saldo", "balance", "cuánta plata", "cuanta plata", "plata tengo"
    }

    MOVEMENTS_KEYWORDS = {
        "movimientos", "transacciones", "movs",
        "últimos movimientos", "ultimos movimientos"
    }

    CATEGORY_KEYWORDS = {
        "por categoría", "por categoria",
        "categorías", "categorias",
        "agrupado", "agrupados",
        "en qué gasté más", "en que gaste mas"
    }

    EXPENSES_TOTAL_KEYWORDS = {
        "cuánto gasté", "cuanto gaste",
        "total de gastos", "mis gastos totales"
    }

    def interpret(self, text: str) -> Interpretation:
        t = text.lower().strip()

        # HELP
        if t in self.HELP_SET:
            return Interpretation(intent="help", confidence=1.0)

        # BALANCE (muy explícito)
        if any(k in t for k in self.BALANCE_KEYWORDS):
            return Interpretation(intent="get_balance", confidence=0.95)

        # EXPENSES BY CATEGORY (muy explícito)
        if any(k in t for k in self.CATEGORY_KEYWORDS):
            return Interpretation(intent="get_expenses_by_category", confidence=0.9)

        # MOVEMENTS (muy explícito)
        if any(k in t for k in self.MOVEMENTS_KEYWORDS):
            return Interpretation(intent="get_movements", confidence=0.9)

        # EXPENSES TOTAL (caso de negocio clave)
        if any(k in t for k in self.EXPENSES_TOTAL_KEYWORDS):
            return Interpretation(intent="get_expenses_total", confidence=0.9)


        return Interpretation(intent="unknown", confidence=0.0)
