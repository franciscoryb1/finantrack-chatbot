import httpx
from typing import Optional

from app.clients.base import BaseAPIClient
from app.clients.movements.schemas import PaginatedMovements


class MovementsClient:
    def __init__(self, base_url: str, api_key: str):
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
            },
        )

    async def list_movements(
        self,
        *,
        user_phone: str,
        from_date: str | None = None,
        to_date: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ):
        params = {
            "page": page,
            "pageSize": page_size,
        }
        if from_date:
            params["fromDate"] = from_date
            
        if to_date:
            params["toDate"] = to_date
            
        headers = {
            "X-User-Phone": user_phone,
        }

        res = await self._client.get(
            "/chatbot/movements",
            params=params,
            headers=headers,
        )

        res.raise_for_status()
        return res.json()
