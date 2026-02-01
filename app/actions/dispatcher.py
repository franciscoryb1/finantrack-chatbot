from app.actions.models import ActionResult
from app.nlu.nlu_service import Interpretation

from app.actions.balance.get_balance import get_balance
from app.actions.movements.list_movements import get_movements
from app.actions.expenses.get_total import get_expenses_total
from app.actions.expenses.get_by_category import get_expenses_by_category


class ActionDispatcher:

    def dispatch(self, interpretation: Interpretation) -> ActionResult:
        intent = interpretation.intent

        if intent == "get_balance":
            return get_balance(interpretation)

        if intent == "get_movements":
            return get_movements(interpretation)

        if intent == "get_expenses_total":
            return get_expenses_total(interpretation)

        if intent == "get_expenses_by_category":
            return get_expenses_by_category(interpretation)

        return ActionResult(
            reply_text="No entendí qué querés hacer. ¿Podés reformular?",
        )
