from typing import TypedDict, List

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, BaseMessage

from app.agents.llm.factory import build_llm
from app.agents.models import AgentResult


# -------------------------
# State del Agent
# -------------------------

class AgentState(TypedDict):
    messages: List[BaseMessage]


# -------------------------
# Finance Agent
# -------------------------

class FinanceAgent:
    """
    Agent conversacional financiero.

    Responsabilidades:
    - Recibir texto del usuario
    - Ejecutar razonamiento con LLM
    - (más adelante) decidir y llamar tools
    - Devolver un AgentResult (contrato explícito)

    NO:
    - Maneja HTTP
    - Maneja trace_id
    - Maneja autenticación
    """

    def __init__(self):
        self.llm = build_llm()
        self.graph = self._build_graph()

    # -------------------------
    # Graph
    # -------------------------

    def _build_graph(self):
        graph = StateGraph(AgentState)

        graph.add_node("llm", self._llm_step)
        graph.add_edge("llm", END)

        graph.set_entry_point("llm")
        return graph.compile()

    # -------------------------
    # Steps
    # -------------------------

    def _llm_step(self, state: AgentState) -> AgentState:
        messages = state["messages"]

        response = self.llm.invoke(messages)

        return {
            "messages": messages + [response],
        }

    # -------------------------
    # Public API
    # -------------------------

    def run(self, user_id: str, text: str) -> AgentResult:
        """
        Ejecuta el agent para un mensaje de usuario.

        - user_id: identificador del usuario (NO usado todavía)
        - text: mensaje del usuario
        """

        result = self.graph.invoke(
            {
                "messages": [HumanMessage(content=text)],
            }
        )

        last_message = result["messages"][-1]

        return AgentResult(
            reply_text=last_message.content,
            data=None,
        )


# -------------------------
# Singleton (uso global)
# -------------------------

finance_agent = FinanceAgent()
