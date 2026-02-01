import time
from typing import Optional

class JwtCache:
    def __init__(self, ttl_seconds: int = 60 * 30):  # 30 min
        self.ttl = ttl_seconds
        self._store: dict[str, dict] = {}

    def get(self, key: str) -> Optional[str]:
        item = self._store.get(key)
        if not item:
            return None

        if time.time() > item["expires_at"]:
            del self._store[key]
            return None

        return item["token"]

    def set(self, key: str, token: str):
        self._store[key] = {
            "token": token,
            "expires_at": time.time() + self.ttl,
        }
