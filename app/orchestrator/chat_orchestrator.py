from uuid import uuid4

from app.core.schemas import ChatRequest, ChatResponse
from app.core.interpretation import Interpretation
from app.nlu.nlu_service import NLUService


class ChatOrchestrator:
    def __init__(self):
        self._nlu = NLUService()

    async def handle(self, req: ChatRequest) -> ChatResponse:
        trace_id = str(uuid4())

        interpretation: Interpretation = self._nlu.interpret(req)

        if interpretation.needs_clarification:
            return ChatResponse(
                replyText=interpretation.clarification_question
                or "¿Podés darme un poco más de detalle?",
                traceId=trace_id,
            )

        # ⚠️ por ahora seguimos con stub
        if interpretation.intent == "get_movements":
            return ChatResponse(
                replyText="[stub] Voy a buscar tus movimientos.",
                traceId=trace_id,
            )

        if interpretation.intent == "help":
            return ChatResponse(
                replyText="Podés preguntarme por tus gastos, movimientos o saldo.",
                traceId=trace_id,
            )

        return ChatResponse(
            replyText="No terminé de entenderte. Probá con algo como 'mostrame mis gastos'.",
            traceId=trace_id,
        )
