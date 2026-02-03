# app/clients/base.py
class BaseAPIClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 5.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _headers(self, user_phone: str) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "X-User-Phone": user_phone,
        }
