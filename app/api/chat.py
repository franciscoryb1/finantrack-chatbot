from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.finance_agent import finance_agent
from app.infra.container import user_session_resolver

router = APIRouter()


class ChatRequest(BaseModel):
    userId: str
    text: str


@router.post("/chat")
def chat(req: ChatRequest):
    session = user_session_resolver.get_session(req.userId)

    result = finance_agent.run(
        user_id=session.user_id,
        text=req.text,
        jwt=session.jwt,
    )

    return {
        "reply_text": result["reply_text"],
        "data": result.get("data"),
    }
