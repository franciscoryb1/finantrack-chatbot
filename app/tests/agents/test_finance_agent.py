import pytest
from langchain_core.messages import AIMessage
from langchain_core.tools import tool

from app.agents.finance_agent import FinanceAgent


class FakeLLM:
    def __init__(self):
        self.called = False

    async def ainvoke(self, messages):
        # Primera vez → pide la tool
        if not self.called:
            self.called = True
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "id": "call-1",
                        "name": "get_movements",
                        "args": {
                            "phone_number": "+5493411111111",
                            "page": 1,
                            "page_size": 5,
                        },
                    }
                ],
            )

        # Segunda vez → respuesta FINAL (sin tool_calls)
        return AIMessage(
            content="Estos son tus últimos movimientos.",
        )


@tool
async def get_movements(phone_number: str, page: int = 1, page_size: int = 5):
    """
    Devuelve movimientos financieros del usuario.
    """
    return {
        "items": [
            {
                "id": 1,
                "description": "Supermercado",
                "amount": -12000,
            }
        ]
    }


@pytest.mark.asyncio
async def test_finance_agent_calls_tool_and_returns_response(mocker):
    # Mock LLM
    mocker.patch(
        "app.agents.finance_agent.build_llm",
        return_value=FakeLLM(),
    )

    # Mock tools
    mocker.patch(
        "app.agents.finance_agent.build_tools",
        return_value=[get_movements],
    )

    agent = FinanceAgent()

    result = await agent.run(
        text="Mostrame mis movimientos",
        phone_number="+5493411111111",
    )


    assert result["reply_text"] is not None
