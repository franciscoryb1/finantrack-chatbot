from typing import TypedDict, List

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage

from app.agents.llm.factory import build_llm


class AgentState(TypedDict):
    messages: List


class FinanceAgent:
    def __init__(self):
        self.llm = build_llm()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)

        graph.add_node("llm", self._llm_step)
        graph.add_edge("llm", END)

        graph.set_entry_point("llm")
        return graph.compile()

    def _llm_step(self, state: AgentState):
        messages = state["messages"]
        response = self.llm.invoke(messages)
        return {"messages": messages + [response]}

    def run(self, user_id: str, text: str) -> dict:
        result = self.graph.invoke(
            {"messages": [HumanMessage(content=text)]}
        )

        last = result["messages"][-1]

        return {
            "reply_text": last.content,
            "data": None,
        }
