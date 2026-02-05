# app/api/chat.py

from fastapi import APIRouter
from pydantic import BaseModel

from app.orchestrator.chat_orchestrator import ChatOrchestrator

router = APIRouter()


class ChatRequest(BaseModel):
    phone_number: str
    text: str


@router.post("/chat")
async def chat(req: ChatRequest):
    """
    Endpoint único de chat.

    No contiene lógica de negocio.
    Delegá todo al ChatOrchestrator.
    """
    orchestrator = ChatOrchestrator()

    response = await orchestrator.handle(
        phone_number=req.phone_number,
        text=req.text,
    )

    return {
        "replyText": response.replyText,
        "traceId": response.traceId,
    }

