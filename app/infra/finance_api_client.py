# app/infra/finance_api_client.py
import requests
from app.core.config import settings


class FinanceApiClient:
    def __init__(self, *, jwt: str):
        self.base_url = settings.FINANCE_API_BASE_URL
        self.jwt = jwt

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.jwt}",
            "Content-Type": "application/json",
        }

    def list_movements(self, params: dict | None = None) -> dict:
        url = f"{self.base_url}/movements"

        resp = requests.get(
            url,
            headers=self._headers(),
            params=params or {},
            timeout=5,
        )

        if not resp.ok:
            raise RuntimeError(
                f"Finance API error ({resp.status_code}): {resp.text}"
            )

        return resp.json()
