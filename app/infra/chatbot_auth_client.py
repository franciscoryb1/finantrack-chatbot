import requests
from app.core.config import settings


class ChatbotAuthClient:
    def __init__(self):
        self.base_url = settings.FINANCE_API_BASE_URL
        self.api_key = settings.CHATBOT_API_KEY

    def resolve_user(self, phone_number: str) -> dict:
        response = requests.post(
            f"{self.base_url}/auth/chatbot/resolve-user",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={"phoneNumber": phone_number},
            timeout=5,
        )

        if not (200 <= response.status_code < 300):
            raise RuntimeError(
                f"Chatbot auth failed ({response.status_code}): {response.text}"
            )

        return response.json()
