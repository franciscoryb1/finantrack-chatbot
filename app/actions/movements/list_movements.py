from app.actions.models import ActionResult
from app.nlu.nlu_service import Interpretation
from app.infra.user_session_resolver import UserSessionResolver
from app.infra.finance_api_client import FinanceApiClient


class ListMovementsAction:
    def __init__(
        self,
        session_resolver: UserSessionResolver,
        finance_client: FinanceApiClient,
    ):
        self.session_resolver = session_resolver
        self.finance_client = finance_client

    def execute(self, interpretation: Interpretation, phone_number: str) -> ActionResult:
        jwt = self.session_resolver.get_jwt_for_user(phone_number)

        params = {}

        if "from_date" in interpretation.entities:
            params["fromDate"] = interpretation.entities["from_date"]

        if "to_date" in interpretation.entities:
            params["toDate"] = interpretation.entities["to_date"]

        data = self.finance_client.list_movements(jwt, params)

        movements = data.get("items", [])

        if not movements:
            return ActionResult(
                reply_text="No tenés movimientos registrados.",
                data={"movements": []},
            )

        lines = []
        for m in movements[:5]:
            lines.append(
                f"- {m.get('description', 'Movimiento')} ${m['amountCents'] / 100:.2f}"
            )

        return ActionResult(
            reply_text="Estos son tus últimos movimientos:\n" + "\n".join(lines),
            data={"movements": movements},
        )
