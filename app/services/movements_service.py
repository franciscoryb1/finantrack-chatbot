from typing import Dict, Any
from app.clients.movements.client import MovementsClient
from app.core.config import settings


from datetime import date
from typing import Optional


async def fetch_movements(
    *,
    phone_number: str,
    from_date: str | None = None,
    to_date: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> Dict[str, Any]:
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

    # result ya es dict
    return result


async def create_expense(
    *,
    phone_number: str,
    amount: float,
    date: date,
    category: Optional[str],
    description: str,
):
    """
    Registra un gasto real en el backend financiero.
    Esta es la ÚNICA fuente de verdad para ADD_EXPENSE.
    """
    client = MovementsClient(
        base_url=settings.FINANCE_API_BASE_URL,
        api_key=settings.CHATBOT_API_KEY,
    )
    payload = {
        "type": "EXPENSE",
        "amount": amount,
        "date": date.isoformat(),
        "description": description,
    }

    if category:
        payload["category"] = category

    return await client.create_expense(
        phone_number=phone_number,
        amount=amount,
        date=date,
        description=description,
        category=category,
    )
