from uuid import uuid4
from typing import Any, Dict

from requests import session

from app.core.schemas import ChatResponse
from app.infra.container import user_session_resolver

# Gate (lo implementamos / conectamos después)
from app.core.access_gate import decide_access, AccessLevel

# NLU
from app.nlu import NLUInterpreter

# Tool
from app.tools.movements import get_movements

# Agent (solo para chat libre / explicación)
from app.agents.finance_agent import FinanceAgent

# Prompt para explicación de datos reales
from app.agents.prompts import build_movements_explanation_prompt


class ChatOrchestrator:
    """
    Orquestador principal del chatbot.

    Responsabilidades:
    - Resolver sesión de usuario
    - Decidir si el mensaje requiere datos reales
    - Ejecutar NLU + tools cuando corresponda
    - Delegar al LLM solo para:
        * chat libre
        * explicación de datos reales
    """

    def __init__(self):
        self._nlu = NLUInterpreter()
        self._agent = FinanceAgent()

    async def handle(self, *, phone_number: str, text: str) -> ChatResponse:
        trace_id = str(uuid4())

        # 1️⃣ Resolver sesión del usuario (auth real)
        session = user_session_resolver.resolve(phone_number)

        # 2️⃣ Gate de acceso a datos reales
        access_decision = decide_access(text)

        # ----------------------------------------
        # 🟢 CASO 1: NO requiere datos reales
        # ----------------------------------------
        if access_decision.access_level == AccessLevel.NO_REAL_DATA:
            agent_result = await self._agent.run(
                phone_number=session.phone_number,
                text=text,
            )

            return ChatResponse(
                replyText=agent_result["reply_text"],
                traceId=trace_id,
            )

        # ----------------------------------------
        # 🟢 CASO 2: Requiere datos reales
        # ----------------------------------------

        # 3️⃣ NLU (interpretación estructurada)
        interpretation = self._nlu.interpret(text)

        # Si el NLU no entiende qué hacer, no ejecutamos tools
        if interpretation.intent != "SHOW_MOVEMENTS":
            return ChatResponse(
                replyText=(
                    "No terminé de entender qué información financiera querés ver. "
                    "¿Podés reformular la consulta?"
                ),
                traceId=trace_id,
            )

        # 4️⃣ Ejecutar tool (fuente única de verdad)
        tool_data: Dict[str, Any] = await get_movements(
            phone_number=session.phone_number,
            from_date=interpretation.entities.get("from_date"),
            to_date=interpretation.entities.get("to_date"),
            page=interpretation.entities.get("page", 1),
            page_size=interpretation.entities.get("page_size", 20),
        )

        # 5️⃣ Explicación con LLM
        prompt = build_movements_explanation_prompt(
            user_text=text,
            data=tool_data,
        )

        explanation = await self._agent.run(
            phone_number=session.phone_number,
            text=prompt,
        )

        return ChatResponse(
            replyText=explanation["reply_text"],
            traceId=trace_id,
        )

