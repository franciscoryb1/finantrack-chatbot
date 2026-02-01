from app.actions.models import ActionResult
from app.nlu.nlu_service import Interpretation


def get_expenses_total(interpretation: Interpretation) -> ActionResult:
    period = interpretation.entities.get("period", {}).get(
        "label", "el período elegido"
    )
    category = interpretation.entities.get("category")

    if category:
        text = f"En {category} gastaste $35.000 durante {period}."
        total = 35000
    else:
        text = f"En total gastaste $85.000 durante {period}."
        total = 85000

    return ActionResult(
        reply_text=text,
        data={
            "total": total,
            "period": period,
            "category": category,
        },
    )
