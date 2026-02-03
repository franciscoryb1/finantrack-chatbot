# app/infra/container.py
from app.infra.chatbot_auth_client import ChatbotAuthClient
from app.infra.user_session_resolver import UserSessionResolver

chatbot_auth_client = ChatbotAuthClient()

user_session_resolver = UserSessionResolver(
    auth_client=chatbot_auth_client
)
