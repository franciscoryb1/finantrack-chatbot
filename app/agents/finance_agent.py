from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from app.agents.llm.factory import build_llm
from app.agents.tools import build_tools


class AgentState(TypedDict):
    messages: List[BaseMessage]
    phone_number: str


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

    async def _llm_step(self, state: AgentState):
        messages = state["messages"]
        response = await self.llm.ainvoke(messages)

        return {
            "messages": messages + [response],
            "phone_number": state["phone_number"],
        }

    def _should_use_tools(self, state: AgentState) -> str:
        last = state["messages"][-1]

        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"

        return "end"

    async def run(self, *, phone_number: str, text: str) -> str:
        system = SystemMessage(
            content=(
                "Sos un asistente financiero personal conectado a un sistema real.\n\n"
                "IMPORTANTE:\n"
                "No sos un chatbot genérico. Tenés acceso a herramientas que devuelven "
                "INFORMACIÓN REAL del usuario.\n\n"
                "PROTOCOLO DE USO DE HERRAMIENTAS:\n"
                "1. Si el mensaje del usuario solicita información financiera personal "
                "(movimientos, transacciones, gastos, consumos, balance, cuentas, saldos), "
                "DEBÉS llamar inmediatamente a la herramienta adecuada.\n"
                "2. En esos casos, NO respondas texto primero.\n"
                "3. NO expliques limitaciones ni políticas.\n"
                "4. NO inventes datos.\n"
                "5. Primero ejecutá la herramienta. Luego, cuando el sistema te devuelva datos, "
                "podrás ayudar a interpretarlos.\n\n"
                "REGLA ABSOLUTA:\n"
                "- Ante pedidos financieros personales, tu PRIMERA respuesta debe ser "
                "una llamada a una herramienta.\n\n"
                "Si el pedido NO requiere datos financieros reales, podés responder normalmente."
            )
        )

        result = await self.graph.ainvoke(
            {
                "messages": [system, HumanMessage(content=text)],
                "phone_number": phone_number,
            },
            config={"configurable": {"thread_id": phone_number}},
        )

        messages = result.get("messages", [])
        last = messages[-1] if messages else None

        return {
            "reply_text": getattr(last, "content", "") if last else "",
            "data": None,
        }
