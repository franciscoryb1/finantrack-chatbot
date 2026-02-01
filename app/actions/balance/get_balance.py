from app.actions.models import ActionResult
from app.nlu.nlu_service import Interpretation


def get_balance(interpretation: Interpretation) -> ActionResult:
    return ActionResult(
        reply_text="Tu saldo actual es $120.000",
        data={"balance": 120000},
    )
