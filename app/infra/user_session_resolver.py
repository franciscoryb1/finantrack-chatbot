from app.infra.chatbot_auth_client import ChatbotAuthClient
from app.infra.jwt_cache import JwtCache

class UserSessionResolver:
    def __init__(
        self,
        auth_client: ChatbotAuthClient,
        cache: JwtCache,
    ):
        self.auth_client = auth_client
        self.cache = cache

    def get_jwt_for_user(self, phone_number: str) -> str:
        cached = self.cache.get(phone_number)
        if cached:
            return cached

        data = self.auth_client.resolve_user(phone_number)
        token = data["access_token"]
        self.cache.set(phone_number, token)
        return token
