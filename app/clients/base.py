class BaseAPIClient:
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
