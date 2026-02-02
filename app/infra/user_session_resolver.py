from dataclasses import dataclass
from app.infra.chatbot_auth_client import ChatbotAuthClient


@dataclass
class UserSession:
    user_id: str
    jwt: str
    email: str | None = None


class UserSessionResolver:
    def __init__(self, auth_client: ChatbotAuthClient):
        self.auth_client = auth_client

    def get_session(self, phone_number: str) -> UserSession:
        data = self.auth_client.resolve_user(phone_number)

        return UserSession(
            user_id=str(data["user"]["id"]),
            jwt=data["access_token"],
            email=data["user"].get("email"),
        )
