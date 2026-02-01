from app.actions.finance_actions import FinanceActions
from app.actions.models import ActionResult
from app.nlu.nlu_service import Interpretation


class ActionDispatcher:

    def __init__(self):
        self.actions = FinanceActions()

    def dispatch(self, interpretation: Interpretation) -> ActionResult:
        intent = interpretation.intent

        if intent == "get_balance":
            return self.actions.get_balance(interpretation)

        if intent == "get_movements":
            return self.actions.get_movements(interpretation)

        if intent == "get_expenses_total":
            return self.actions.get_expenses_total(interpretation)

        if intent == "get_expenses_by_category":
            return self.actions.get_expenses_by_category(interpretation)

        return ActionResult(
            reply_text="No entendí qué querés hacer. ¿Podés reformular?",
        )
