from typing import Optional, Dict, Any

import httpx

class FinanceApiClient:
    """
    Cliente HTTP async para comunicarse con la Finance API (NestJS backend).
    Pensado para FastAPI.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:3000",
        timeout_seconds: int = 5,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout_seconds

    async def list_movements(
        self,
        user_id: int,
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Dict[str, Any]:
        """
        Llama a GET /movements con filtros opcionales.
        """

        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
        }

        if filters:
            params.update(filters)

        headers = {
            # Simulación de auth por ahora
            "X-User-Id": str(user_id),
        }

        url = f"{self.base_url}/movements"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
