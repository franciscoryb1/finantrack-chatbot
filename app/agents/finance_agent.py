from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI

from app.agents.prompts import SYSTEM_PROMPT
from app.agents.memory import build_memory

class FinanceAgent:
    def __init__(self, tools: list):
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4o-mini"
        )
        self.tools = tools

    def run(self, user_id: str, text: str) -> dict:
        memory = build_memory(user_id)

        agent = create_openai_tools_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=SYSTEM_PROMPT
        )

        executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=memory,
            verbose=True
        )

        result = executor.invoke({"input": text})

        # result["output"] es texto final del agent
        return {
            "reply_text": result.get("output", ""),
            "data": None
        }
