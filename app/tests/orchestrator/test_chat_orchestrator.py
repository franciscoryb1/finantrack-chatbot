import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from app.orchestrator.chat_orchestrator import ChatOrchestrator
from app.core.access_gate import AccessLevel


@pytest.mark.asyncio
async def test_chat_free_flow():
    """
    Caso:
    - El Gate dice NO_REAL_DATA
    - Se usa FinanceAgent
    - NO se ejecuta ninguna tool
    """

    orchestrator = ChatOrchestrator()

    with patch(
        "app.orchestrator.chat_orchestrator.user_session_resolver.resolve",
        return_value=SimpleNamespace(phone_number="+5491111111111"),
    ), patch(
        "app.orchestrator.chat_orchestrator.decide_access",
        return_value=SimpleNamespace(access_level=AccessLevel.NO_REAL_DATA),
    ), patch(
        "app.orchestrator.chat_orchestrator.FinanceAgent.run",
        new=AsyncMock(return_value={"reply_text": "Hola!"}),
    ) as mock_agent_run, patch(
        "app.orchestrator.chat_orchestrator.get_movements",
        new=AsyncMock(),
    ) as mock_tool:

        response = await orchestrator.handle(
            phone_number="+5491111111111",
            text="hola",
        )

        assert response.replyText == "Hola!"
        assert response.traceId is not None

        mock_agent_run.assert_awaited_once()
        mock_tool.assert_not_awaited()


@pytest.mark.asyncio
async def test_financial_flow_executes_tool():
    """
    Caso:
    - El Gate dice REAL_DATA_REQUIRED
    - El NLU detecta SHOW_MOVEMENTS
    - Se ejecuta get_movements
    - El LLM solo explica
    """

    orchestrator = ChatOrchestrator()

    fake_tool_data = {
        "items": [{"id": 1, "amount": 100}],
        "pagination": {"page": 1},
    }

    with patch(
        "app.orchestrator.chat_orchestrator.user_session_resolver.resolve",
        return_value=SimpleNamespace(phone_number="+5492222222222"),
    ), patch(
        "app.orchestrator.chat_orchestrator.decide_access",
        return_value=SimpleNamespace(access_level=AccessLevel.REAL_DATA_REQUIRED),
    ), patch(
        "app.orchestrator.chat_orchestrator.get_movements",
        new=AsyncMock(return_value=fake_tool_data),
    ) as mock_tool, patch(
        "app.orchestrator.chat_orchestrator.FinanceAgent.run",
        new=AsyncMock(return_value={"reply_text": "Estos son tus movimientos"}),
    ) as mock_agent_run:

        response = await orchestrator.handle(
            phone_number="+5492222222222",
            text="mostrame mis movimientos",
        )

        assert "movimientos" in response.replyText.lower()
        assert response.traceId is not None

        mock_tool.assert_awaited_once()
        mock_agent_run.assert_awaited_once()


@pytest.mark.asyncio
async def test_financial_flow_unknown_intent():
    """
    Caso:
    - Gate permite datos reales
    - NLU NO reconoce intent
    - NO se ejecuta tool
    """

    orchestrator = ChatOrchestrator()

    with patch(
        "app.orchestrator.chat_orchestrator.user_session_resolver.resolve",
        return_value=SimpleNamespace(phone_number="+5493333333333"),
    ), patch(
        "app.orchestrator.chat_orchestrator.decide_access",
        return_value=SimpleNamespace(access_level=AccessLevel.REAL_DATA_REQUIRED),
    ), patch(
        "app.orchestrator.chat_orchestrator.NLUInterpreter.interpret",
        return_value=SimpleNamespace(intent="UNKNOWN", entities={}),
    ), patch(
        "app.orchestrator.chat_orchestrator.get_movements",
        new=AsyncMock(),
    ) as mock_tool:

        response = await orchestrator.handle(
            phone_number="+5493333333333",
            text="algo raro que no se entiende",
        )

        assert "no terminé de entender" in response.replyText.lower()
        assert response.traceId is not None

        mock_tool.assert_not_awaited()
