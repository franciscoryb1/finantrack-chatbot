from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.finance_agent import FinanceAgent
from app.infra.container import user_session_resolver

router = APIRouter()


class ChatRequest(BaseModel):
    phone_number: str
    text: str


@router.post("/chat")
async def chat(req: ChatRequest):
    # 1️⃣ Resolver sesión del usuario usando el phone_number
    session = user_session_resolver.resolve(req.phone_number)

    # 2️⃣ Crear el agente (stateless, el estado vive en LangGraph)
    agent = FinanceAgent()

    # 3️⃣ Ejecutar el agente
    reply_text = await agent.run(
        phone_number=session.phone_number,
        text=req.text,
    )

    # 4️⃣ Responder
    return {
        "reply_text": reply_text,
        "data": None,
    }
