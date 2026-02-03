# app/infra/user_session_resolver.py
from app.infra.chatbot_auth_client import ChatbotAuthClient
from app.infra.user_session import UserSession


class UserSessionResolver:
    def __init__(self, auth_client: ChatbotAuthClient):
        self.auth_client = auth_client

    def resolve(self, phone_number: str) -> UserSession:
        """
        Valida al chatbot contra el backend y verifica
        que el usuario exista para el phone_number dado.
        """
        data = self.auth_client.resolve_user(phone_number)

        return UserSession(
            phone_number=phone_number,
            user_id=str(data.get("user", {}).get("id")) if data.get("user") else None,
        )
