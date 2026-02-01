from fastapi import APIRouter
from pydantic import BaseModel

from app.nlu.nlu_service import NLUService
from app.conversation.resolver import ConversationResolver
from app.conversation.store import get_state
from app.actions.dispatcher import ActionDispatcher

router = APIRouter()

# Core services
nlu = NLUService()
resolver = ConversationResolver(nlu)
dispatcher = ActionDispatcher()


class ChatRequest(BaseModel):
    userId: str
    text: str


class ChatResponse(BaseModel):
    replyText: str
    intent: str | None = None
    entities: dict | None = None
    needsClarification: bool = False


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # 1️⃣ Obtener estado conversacional
    state = get_state(req.userId)

    # 2️⃣ Resolver NLU + contexto
    result = resolver.resolve(req.text, state)

    # 3️⃣ Si falta info → preguntar
    if result.needs_clarification:
        return ChatResponse(
            replyText=_build_clarification_message(result),
            intent=result.intent,
            entities=result.entities,
            needsClarification=True,
        )

    # 4️⃣ Ejecutar action
    action_result = dispatcher.dispatch(result)

    return ChatResponse(
        replyText=action_result.reply_text,
        intent=result.intent,
        entities=result.entities,
        needsClarification=False,
    )


def _build_clarification_message(result) -> str:
    missing = result.missing_slots or []

    if "period" in missing:
        return (
            "¿De qué período querés la información? "
            "Por ejemplo: hoy, este mes, el mes pasado, enero 2024."
        )

    if "category" in missing:
        return (
            "¿De qué categoría? "
            "Por ejemplo: comida, transporte, servicios."
        )

    return "Me falta un dato para ayudarte."
