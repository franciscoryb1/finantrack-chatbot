import httpx
from typing import Optional

from app.clients.base import BaseAPIClient
from app.clients.movements.schemas import PaginatedMovements


class MovementsClient(BaseAPIClient):
    async def list_movements(
        self,
        user_phone: str,
        *,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedMovements:

        params = {
            "fromDate": from_date,
            "toDate": to_date,
            "page": page,
            "pageSize": page_size,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            res = await client.get(
                f"{self.base_url}/movements",
                headers=self._headers(user_phone),
                params={k: v for k, v in params.items() if v is not None},
            )

        res.raise_for_status()
        return PaginatedMovements.model_validate(res.json())
