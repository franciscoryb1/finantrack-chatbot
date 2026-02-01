from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.finance_agent import finance_agent

router = APIRouter()


class ChatRequest(BaseModel):
    userId: str
    text: str


@router.post("/chat")
def chat(req: ChatRequest):
    """
    Endpoint principal del chatbot.
    Usa exclusivamente el Agent.
    """

    result = finance_agent.run(
        user_id=req.userId,
        text=req.text,
    )

    # Contrato único del sistema (AgentResult)
    return {
        "reply_text": result.reply_text,
        "data": result.data,
    }
