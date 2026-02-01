from typing import TypedDict, List

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from app.agents.llm.factory import build_llm
from app.agents.models import AgentResult
from app.agents.tools import build_tools


class AgentState(TypedDict):
    messages: List


class FinanceAgent:
    def __init__(self):
        self.llm = build_llm()

    def _build_graph(self, tools):
        graph = StateGraph(AgentState)

        llm_with_tools = self.llm.bind_tools(tools)

        def llm_step(state: AgentState):
            response = llm_with_tools.invoke(state["messages"])
            return {"messages": state["messages"] + [response]}

        graph.add_node("llm", llm_step)
        graph.add_edge("llm", END)
        graph.set_entry_point("llm")

        return graph.compile()

    def run(self, user_id: str, text: str) -> AgentResult:
        tools = build_tools(user_id)
        graph = self._build_graph(tools)

        result = graph.invoke(
            {"messages": [HumanMessage(content=text)]}
        )

        last = result["messages"][-1]

        return AgentResult(
            reply_text=last.content,
            data=None,
        )


finance_agent = FinanceAgent()
