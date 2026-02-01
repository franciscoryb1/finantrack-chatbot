from app.actions.models import ActionResult
from app.nlu.nlu_service import Interpretation


class FinanceActions:

    def get_balance(self, interpretation: Interpretation) -> ActionResult:
        return ActionResult(
            reply_text="Tu saldo actual es $120.000",
            data={"balance": 120000},
        )

    def get_movements(self, interpretation: Interpretation) -> ActionResult:
        return ActionResult(
            reply_text="Estos son tus últimos movimientos:\n- Supermercado $12.500\n- Transporte $3.200",
            data={
                "movements": [
                    {"desc": "Supermercado", "amount": 12500},
                    {"desc": "Transporte", "amount": 3200},
                ]
            },
        )

    def get_expenses_total(self, interpretation: Interpretation) -> ActionResult:
        period = interpretation.entities.get("period", {}).get("label", "el período elegido")
        category = interpretation.entities.get("category")

        if category:
            text = f"En {category} gastaste $35.000 durante {period}."
        else:
            text = f"En total gastaste $85.000 durante {period}."

        return ActionResult(
            reply_text=text,
            data={
                "total": 85000,
                "period": period,
                "category": category,
            },
        )

    def get_expenses_by_category(self, interpretation: Interpretation) -> ActionResult:
        return ActionResult(
            reply_text=(
                "Tus gastos por categoría:\n"
                "- Comida: $40.000\n"
                "- Transporte: $15.000\n"
                "- Otros: $30.000"
            ),
            data={
                "by_category": {
                    "comida": 40000,
                    "transporte": 15000,
                    "otros": 30000,
                }
            },
        )
