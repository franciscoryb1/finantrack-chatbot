from fastapi import APIRouter

from app.orchestrator.chat_orchestrator import ChatOrchestrator
from app.core.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

_orchestrator = ChatOrchestrator()


@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    return await _orchestrator.handle(request)
