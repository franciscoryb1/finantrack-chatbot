from app.actions.models import ActionResult
from app.nlu.nlu_service import Interpretation


def get_expenses_by_category(interpretation: Interpretation) -> ActionResult:
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
