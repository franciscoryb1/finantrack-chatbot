from abc import ABC, abstractmethod
from app.nlu.nlu_service import Interpretation
from app.actions.models import ActionResult


class Action(ABC):

    @abstractmethod
    def execute(
        self,
        interpretation: Interpretation,
        user_id: str,
    ) -> ActionResult: ...
