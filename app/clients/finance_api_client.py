import httpx
from typing import Optional
from app.clients.schemas import (
    PaginatedMovements,
    TotalAmount,
    ExpensesByCategory,
)


class FinanceApiClient:
    def __init__(
        self,
        base_url: str,
        service_token: str,
        timeout: float = 5.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.service_token = service_token
        self.timeout = timeout

    def _headers(self, user_phone: str) -> dict:
        return {
            "Authorization": f"Bearer {self.service_token}",
            "X-User-Phone": user_phone,
        }

    async def list_movements(
        self,
        user_phone: str,
        *,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        type: Optional[str] = None,
        category_id: Optional[int] = None,
        account_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedMovements:
        params = {
            "fromDate": from_date,
            "toDate": to_date,
            "type": type,
            "categoryId": category_id,
            "accountId": account_id,
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

    async def get_expenses_total(
        self,
        user_phone: str,
        *,
        from_date: str,
        to_date: str,
        category_id: Optional[int] = None,
        account_id: Optional[int] = None,
    ) -> TotalAmount:
        params = {
            "fromDate": from_date,
            "toDate": to_date,
            "categoryId": category_id,
            "accountId": account_id,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            res = await client.get(
                f"{self.base_url}/movements/total",
                headers=self._headers(user_phone),
                params={k: v for k, v in params.items() if v is not None},
            )

        res.raise_for_status()
        return TotalAmount.model_validate(res.json())

    async def get_expenses_by_category(
        self,
        user_phone: str,
        *,
        from_date: str,
        to_date: str,
        account_id: Optional[int] = None,
    ) -> ExpensesByCategory:
        params = {
            "fromDate": from_date,
            "toDate": to_date,
            "accountId": account_id,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            res = await client.get(
                f"{self.base_url}/movements/by-category",
                headers=self._headers(user_phone),
                params=params,
            )

        res.raise_for_status()
        return ExpensesByCategory.model_validate(res.json())
