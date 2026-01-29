from typing import Dict, Any, List

from app.integrations.finance_api_client import FinanceApiClient
from app.core.interpretation import Interpretation


class FinanceActions:
    """
    Acciones de dominio financiero usadas por el chatbot.
    """

    def __init__(self, api_client: FinanceApiClient | None = None):
        self._api = api_client or FinanceApiClient()

    async def get_movements(self, user_id: int, interpretation: Interpretation) -> str:
        """
        Ejecuta la acción get_movements y devuelve texto para el bot.
        """

        # Por ahora: solo gastos, primera página
        filters: Dict[str, Any] = {
            "type": "EXPENSE",
        }

        response = await self._api.list_movements(
            user_id=user_id,
            filters=filters,
            page=1,
            page_size=5,
        )

        items: List[Dict[str, Any]] = response.get("items", [])
        total: int = response.get("total", 0)

        if not items:
            return "No encontré gastos registrados."

        # Resumen corto (UX)
        lines = []
        for m in items[:3]:
            desc = m.get("description") or "Sin descripción"
            amount = m.get("amount")
            category = m.get("category", {}).get("name", "Sin categoría")
            lines.append(f"- {desc} (${amount}) [{category}]")

        summary = "\n".join(lines)

        return (
            f"Encontré {total} gastos en total. "
            f"Los últimos fueron:\n{summary}"
        )
