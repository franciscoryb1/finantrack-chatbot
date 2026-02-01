import requests
from app.core.config import settings


class FinanceApiClient:
    def __init__(self):
        self.base_url = settings.FINANCE_API_BASE_URL

    def list_movements(self, jwt: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/movements"

        headers = {
            "Authorization": f"Bearer {jwt}",
            "Content-Type": "application/json",
        }

        resp = requests.get(
            url,
            headers=headers,
            params=params or {},
            timeout=5,
        )

        if resp.status_code != 200:
            raise RuntimeError(
                f"Finance API error ({resp.status_code}): {resp.text}"
            )

        return resp.json()
