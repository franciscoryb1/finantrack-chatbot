from langchain_core.tools import tool
from app.infra.finance_api_client import FinanceApiClient

@tool(
    name_or_callable="get_movements",
    description=(
        "Devuelve los movimientos financieros reales del usuario autenticado. "
        "Usar SIEMPRE que el usuario pida ver movimientos, transacciones, "
        "consumos, gastos recientes o actividad financiera."
    ),
)
def get_movements(jwt: str) -> str:
    client = FinanceApiClient()
    data = client.list_movements(jwt=jwt)

    return (
        "Últimos movimientos:\n"
        + "\n".join(
            f"- {m['date']}: {m['description']} ({m['amount']})"
            for m in data.get("items", [])
        )
    )