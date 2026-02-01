from app.actions.models import ActionResult
from app.nlu.nlu_service import Interpretation


def get_movements(interpretation: Interpretation) -> ActionResult:
    return ActionResult(
        reply_text=(
            "Estos son tus últimos movimientos:\n"
            "- Supermercado $12.500\n"
            "- Transporte $3.200"
        ),
        data={
            "movements": [
                {"desc": "Supermercado", "amount": 12500},
                {"desc": "Transporte", "amount": 3200},
            ]
        },
    )
