import httpx
from typing import Optional


class BaseHttpClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        headers: Optional[dict] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers or {}

    def _client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers,
        )
