from uuid import uuid4

from app.core.config import settings
from app.core.schemas import ChatRequest, ChatResponse

# Agent (nuevo flujo)
from app.agents import finance_agent

# Legacy (flujo viejo, temporal)
# ⚠️ cuando terminemos la migración, este import se borra
from app.orchestrator.legacy_handler import LegacyChatHandler


class ChatOrchestrator:
    """
    Orquestador de alto nivel.

    - Decide el flujo (agent vs legacy)
    - No contiene lógica de negocio
    - Devuelve siempre ChatResponse
    """

    def __init__(self):
        self._legacy = LegacyChatHandler()

    def handle(self, req: ChatRequest) -> ChatResponse:
        trace_id = str(uuid4())

        # ------------------------
        # NUEVO FLUJO (Agent)
        # ------------------------
        if settings.USE_AGENT:
            result = finance_agent.run(
                user_id=req.userId,
                text=req.text,
            )

            return ChatResponse(
                reply_text=result.reply_text,
                data=result.data,
                trace_id=trace_id,
            )

        # ------------------------
        # LEGACY (temporal)
        # ------------------------
        legacy_result = self._legacy.handle(
            user_id=req.userId,
            text=req.text,
            trace_id=trace_id,
        )

        return legacy_result
