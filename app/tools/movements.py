# app/tools/movements.py
from langchain_core.tools import tool
from app.clients.movements.client import MovementsClient
from app.core.config import settings


@tool
async def get_movements(
    phone_number: str,
    from_date: str | None = None,
    to_date: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """
    Obtiene los movimientos financieros reales del usuario.

    Debe usarse cuando el usuario pide ver movimientos, transacciones,
    gastos, consumos o actividad financiera.

    Devuelve datos crudos (dict). No genera texto narrativo.
    """

    client = MovementsClient(
        base_url=settings.FINANCE_API_BASE_URL,
        api_key=settings.CHATBOT_API_KEY,
    )

    result = await client.list_movements(
        user_phone=phone_number,
        from_date=from_date,
        to_date=to_date,
        page=page,
        page_size=page_size,
    )

    return result.model_dump()
