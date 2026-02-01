from uuid import uuid4

from app.core.schemas import ChatRequest, ChatResponse
from app.agents import finance_agent


class ChatOrchestrator:
    """
    High-level orchestrator for chat messages.

    Responsibilities:
    - Generate trace_id
    - Delegate message handling to the Agent
    - Normalize API response
    """

    async def handle(self, req: ChatRequest) -> ChatResponse:
        trace_id = str(uuid4())

        result = finance_agent.run(
            user_id=req.userId,
            text=req.text,
        )

        return ChatResponse(
            replyText=result["reply_text"],
            traceId=trace_id,
        )
