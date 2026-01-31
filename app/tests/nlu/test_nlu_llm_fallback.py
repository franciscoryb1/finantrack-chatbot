import pytest
from unittest.mock import AsyncMock, MagicMock

from app.nlu.nlu_service import NLUService
from app.core.schemas import ChatRequest
from app.core.interpretation import Interpretation


def make_req(text: str) -> ChatRequest:
    return ChatRequest(
        userId="test-user",
        text=text,
    )


@pytest.fixture
def nlu():
    llm_mock = MagicMock()
    llm_mock.suggest = AsyncMock()
    return NLUService(llm_fallback=llm_mock)


def test_llm_fallback_suggests_valid_intent(nlu):
    """
    Si rules + ML no detectan nada,
    el LLM puede sugerir un intent válido.
    """

    nlu._llm_fallback.suggest.return_value = Interpretation(
        intent="get_balance",
        confidence=0.8,
    )

    res = nlu.interpret(make_req("decime algo raro"))

    assert res.intent == "get_balance"
    assert res.confidence == 0.8
    assert not res.needs_clarification


def test_llm_fallback_invalid_intent_is_rejected(nlu):
    """
    El LLM no puede inventar intents.
    Si devuelve algo inválido, se responde unknown.
    """

    nlu._llm_fallback.suggest.return_value = Interpretation(
        intent="invented_intent",
        confidence=0.9,
    )

    res = nlu.interpret(make_req("algo totalmente raro"))

    assert res.intent == "unknown"


def test_llm_fallback_expenses_total_needs_period(nlu):
    """
    Si el LLM detecta get_expenses_total
    pero no provee período, se pide aclaración.
    """

    nlu._llm_fallback.suggest.return_value = Interpretation(
        intent="get_expenses_total",
        confidence=0.75,
        entities={},
    )

    res = nlu.interpret(make_req("cuanto gaste"))

    assert res.intent == "get_expenses_total"
    assert res.needs_clarification
    assert "period" in res.missing_slots
    assert res.clarification_question is not None


def test_llm_fallback_exception_returns_unknown(nlu):
    """
    Si el LLM falla (timeout, error, etc),
    el NLU debe responder unknown y no romper.
    """

    nlu._llm_fallback.suggest.side_effect = Exception("LLM down")

    res = nlu.interpret(make_req("texto cualquiera"))

    assert res.intent == "unknown"
