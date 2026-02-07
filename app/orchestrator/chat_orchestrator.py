# app/orchestrator/chat_orchestrator.py

from uuid import uuid4

from app.core.schemas import ChatResponse
from app.core.thresholds import INTENT_THRESHOLD
from app.infra.container import user_session_resolver
from app.core.access_gate import decide_access, AccessLevel

from app.nlu import NLUInterpreter
from app.agents.finance_agent import FinanceAgent

from app.orchestrator.handlers.show_movements import handle_show_movements
from app.orchestrator.handlers.add_expense import handle_add_expense


class ChatOrchestrator:
    def __init__(self):
        self._nlu = NLUInterpreter()
        self._agent = FinanceAgent()

    async def handle(self, *, phone_number: str, text: str) -> ChatResponse:
        trace_id = str(uuid4())

        # 1️⃣ Sesión
        session = user_session_resolver.resolve(phone_number)

        # 2️⃣ Gate
        access = decide_access(text)

        if access.access_level == AccessLevel.NO_REAL_DATA:
            agent_result = await self._agent.run(
                phone_number=session.phone_number,
                text=text,
            )
            return ChatResponse(
                replyText=agent_result["reply_text"],
                traceId=trace_id,
            )

        # 3️⃣ NLU
        interpretation = self._nlu.interpret(text)

        if interpretation.intent_confidence < INTENT_THRESHOLD:
            return ChatResponse(
                replyText=(
                    "No terminé de entender qué querés hacer. "
                    "¿Podés reformular?"
                ),
                traceId=trace_id,
            )

        # 4️⃣ Dispatch por intent
        if interpretation.intent == "SHOW_MOVEMENTS":
            return await handle_show_movements(
                session=session,
                text=text,
                interpretation=interpretation,
                agent=self._agent,
                trace_id=trace_id,
            )

        if interpretation.intent == "ADD_EXPENSE":
            return await handle_add_expense(
                session=session,
                text=text,
                interpretation=interpretation,
                agent=self._agent,
                trace_id=trace_id,
            )


        return ChatResponse(
            replyText="Todavía no puedo manejar ese tipo de consulta.",
            traceId=trace_id,
        )
