from fastapi import APIRouter
from pydantic import BaseModel

from app.core.schemas import ChatRequest, ChatResponse

from app.orchestrator.chat_orchestrator import ChatOrchestrator

router = APIRouter(prefix="/chat", tags=["chat"])


_orchestrator = ChatOrchestrator()


@router.post("", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    return _orchestrator.handle(request)
