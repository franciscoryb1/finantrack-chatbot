from typing import Optional, List
from pydantic import BaseModel

from app.infra.finance_api_client import FinanceApiClient


class Movement(BaseModel):
    id: str
    description: str
    amount: float
    date: str


class GetMovementsResult(BaseModel):
    movements: List[Movement]


def get_movements(user_id: str) -> GetMovementsResult:
    """
    Tool: obtiene los últimos movimientos del usuario
    """

    client = FinanceApiClient(user_id=user_id)
    response = client.get_movements()

    return GetMovementsResult(
        movements=[
            Movement(
                id=m["id"],
                description=m["description"],
                amount=m["amount"],
                date=m["date"],
            )
            for m in response
        ]
    )
