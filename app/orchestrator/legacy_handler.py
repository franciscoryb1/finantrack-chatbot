from app.core.schemas import ChatResponse


class LegacyChatHandler:
    """
    Handler legacy TEMPORAL.

    No usa NLU.
    No interpreta.
    No ejecuta acciones.

    Se elimina cuando USE_AGENT sea siempre true.
    """

    def handle(self, user_id: str, text: str, trace_id: str) -> ChatResponse:
        return ChatResponse(
            reply_text=(
                "El asistente está en mantenimiento en este momento. "
                "Probá de nuevo en unos minutos."
            ),
            trace_id=trace_id,
        )
