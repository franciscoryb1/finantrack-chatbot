from uuid import uuid4

from app.core.schemas import ChatRequest, ChatResponse
from app.core.interpretation import Interpretation
from app.nlu.nlu_service import NLUService


class ChatOrchestrator:
    """
    Orquesta el flujo del chatbot:
    - delega NLU
    - decide qué hacer con la interpretación
    - construye la respuesta
    """

    def __init__(self):
        self._nlu = NLUService()

    def handle(self, req: ChatRequest) -> ChatResponse:
        trace_id = str(uuid4())

        interpretation: Interpretation = self._nlu.interpret(req)

        # 1) Falta información → pedir aclaración
        if interpretation.needs_clarification:
            return ChatResponse(
                replyText=interpretation.clarification_question
                or "¿Podés darme un poco más de detalle?",
                traceId=trace_id,
            )

        # 2) Intent: gastos totales
        if interpretation.intent == "get_expenses_total":
            period = interpretation.entities.get("period", {}).get("value")
            return ChatResponse(
                replyText=(
                    f"[stub] Ok. Voy a buscar tu gasto total del período {period}."
                ),
                traceId=trace_id,
            )

        # 3) Intent: help
        if interpretation.intent == "help":
            return ChatResponse(
                replyText=(
                    "Podés preguntarme cosas como: " "'Cuánto gasté en enero 2026?'"
                ),
                traceId=trace_id,
            )

        # 4) Fallback
        return ChatResponse(
            replyText=(
                "No terminé de entenderte. " "Probá con: 'Cuánto gasté en enero 2026?'"
            ),
            traceId=trace_id,
        )
