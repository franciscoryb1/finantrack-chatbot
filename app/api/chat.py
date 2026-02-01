from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

# 🧠 Agent (nuevo flujo)
from app.agents import finance_agent

# 🧓 Legacy (flujo viejo, mientras dure la migración)
from app.orchestrator.chat_orchestrator import ChatOrchestrator

router = APIRouter()


class ChatRequest(BaseModel):
    userId: str   # phone_number / wa_id
    text: str


@router.post("/chat")
def chat(req: ChatRequest):
    """
    Endpoint principal del chatbot.

    Usa LangChain Agent + tools si USE_AGENT=true.
    Caso contrario, ejecuta el flujo legacy.
    """

    # Agent + Tools
    if settings.USE_AGENT:
        result = finance_agent.run(
            user_id=req.userId,
            text=req.text,
        )

        # Contrato unificado
        return {
            "reply_text": result.get("reply_text", ""),
            "data": result.get("data"),
        }

    # FLUJO LEGACY (mientras se migra todo)
    orchestrator = ChatOrchestrator()
    legacy_result = orchestrator.handle(req.userId, req.text)

    return legacy_result
