from fastapi import APIRouter
from pydantic import BaseModel

from app.nlu.nlu_service import NLUService
from app.conversation.resolver import ConversationResolver
from app.conversation.store import get_state

from app.actions.dispatcher import ActionDispatcher
from app.actions.models import ActionResult

# Acciones concretas
from app.actions.movements.list_movements import ListMovementsAction

# Infra
from app.infra.chatbot_auth_client import ChatbotAuthClient
from app.infra.finance_api_client import FinanceApiClient
from app.infra.jwt_cache import JwtCache
from app.infra.user_session_resolver import UserSessionResolver

router = APIRouter()

# -------------------------
# Infra wiring (manual DI)
# -------------------------

jwt_cache = JwtCache()

auth_client = ChatbotAuthClient()
session_resolver = UserSessionResolver(
    auth_client=auth_client,
    cache=jwt_cache,
)

finance_client = FinanceApiClient()

# -------------------------
# Actions registry
# -------------------------

actions = {
    "get_movements": ListMovementsAction(
        session_resolver=session_resolver,
        finance_client=finance_client,
    ),
}

dispatcher = ActionDispatcher(actions)

# -------------------------
# NLU + Conversation
# -------------------------

nlu = NLUService()
resolver = ConversationResolver(nlu)


class ChatRequest(BaseModel):
    userId: str   # phone_number / wa_id
    text: str


@router.post("/chat")
def chat(req: ChatRequest):
    """
    Orquestador principal del chatbot
    """
    # 1) Estado conversacional
    state = get_state(req.userId)

    # 2) Resolver intención + slots
    interpretation = resolver.resolve(req.text, state)

    # 3) Ejecutar acción
    action_result: ActionResult = dispatcher.dispatch(
        interpretation=interpretation,
        user_id=req.userId,
    )

    # 4) Respuesta unificada
    return {
        "intent": interpretation.intent,
        "needs_clarification": interpretation.needs_clarification,
        "reply_text": action_result.reply_text,
        "data": action_result.data,
    }
