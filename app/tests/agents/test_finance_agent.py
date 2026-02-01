from app.agents.finance_agent import FinanceAgent
from app.tools.movements import get_movements
from app.tests.agents.fake_llm import FakeLLM


def test_finance_agent_calls_get_movements_tool():
    agent = FinanceAgent(
        tools=[get_movements],
        llm=FakeLLM(),
    )

    result = agent.run(
        user_id="+5491111111111",
        text="mostrame mis movimientos de este mes",
    )

    assert "reply_text" in result
    assert isinstance(result["reply_text"], str)
