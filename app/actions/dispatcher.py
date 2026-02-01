from typing import Dict

from app.actions.base import Action
from app.actions.models import ActionResult
from app.nlu.nlu_service import Interpretation


class ActionDispatcher:
    def __init__(self, actions: Dict[str, Action]):
        """
        actions: dict intent -> Action
        """
        self.actions = actions

    def dispatch(
        self,
        interpretation: Interpretation,
        user_id: str,  # phone_number / wa_id / external id
    ) -> ActionResult:
        action = self.actions.get(interpretation.intent)

        if not action:
            return ActionResult(
                reply_text="No entendí qué querés hacer. ¿Podés reformular?",
            )

        return action.execute(interpretation, user_id)
