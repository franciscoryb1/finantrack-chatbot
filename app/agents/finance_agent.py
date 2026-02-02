from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from app.agents.llm.factory import build_llm
from app.agents.tools import build_tools


class AgentState(TypedDict):
    messages: List[BaseMessage]
    jwt: str


class FinanceAgent:
    def __init__(self):
        self.llm = build_llm()
        self.tools = build_tools()
        self.checkpointer = MemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)

        tool_node = ToolNode(self.tools)

        graph.add_node("llm", self._llm_step)
        graph.add_node("tools", tool_node)

        graph.set_entry_point("llm")

        graph.add_conditional_edges(
            "llm",
            self._should_use_tools,
            {
                "tools": "tools",
                "end": END,
            },
        )

        graph.add_edge("tools", "llm")

        return graph.compile(checkpointer=self.checkpointer)

    def _llm_step(self, state: AgentState):
        messages = state["messages"]
        response = self.llm.invoke(messages)

        return {
            "messages": messages + [response],
            "jwt": state["jwt"],  # se propaga sin problema
        }

    def _should_use_tools(self, state: AgentState) -> str:
        last = state["messages"][-1]

        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"

        return "end"

    def run(self, *, user_id: str, text: str, jwt: str) -> dict:
        system = SystemMessage(
            content=(
                "Sos un asistente financiero personal.\n\n"

                "Tenés acceso a herramientas que devuelven INFORMACIÓN REAL "
                "del sistema financiero del usuario.\n\n"

                "REGLA OBLIGATORIA:\n"
                "- Si el usuario pide movimientos, transacciones, consumos, gastos, balance "
                "o información financiera personal, TENÉS QUE usar una herramienta.\n"
                "- NO respondas con texto explicativo sin usar una herramienta.\n"
                "- NO digas que no tenés acceso a la información.\n\n"

                "Si una herramienta está disponible y es relevante, usarla ES OBLIGATORIO."
            )
        )


        result = self.graph.invoke(
            {
                "messages": [system, HumanMessage(content=text)],
                "jwt": jwt,
            },
            config={"configurable": {"thread_id": user_id}},
        )

        messages = result.get("messages", [])
        last = messages[-1] if messages else None

        return {
            "reply_text": getattr(last, "content", "") if last else "",
            "data": None,
        }


finance_agent = FinanceAgent()
