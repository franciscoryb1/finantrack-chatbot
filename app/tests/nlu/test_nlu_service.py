import pytest

from app.nlu.nlu_service import NLUService
from app.core.schemas import ChatRequest


@pytest.fixture
def nlu():
    return NLUService()


def make_req(text: str) -> ChatRequest:
    return ChatRequest(
        userId="test-user",
        text=text,
    )


# =========================
# HELP
# =========================

def test_help_intent(nlu):
    res = nlu.interpret("ayuda")
    assert res.intent == "help"
    assert res.confidence == 1.0
    assert not res.needs_clarification


# =========================
# BALANCE
# =========================

@pytest.mark.parametrize("text", [
    "saldo",
    "balance",
    "cuánta plata tengo",
    "cuanta plata tengo",
])
def test_get_balance(nlu, text):
    res = nlu.interpret(text)
    assert res.intent == "get_balance"
    assert res.confidence >= 0.9
    assert not res.needs_clarification


# =========================
# EXPENSES BY CATEGORY
# =========================

@pytest.mark.parametrize("text", [
    "gastos por categoría",
    "gastos por categoria",
    "en qué gasté más",
    "en que gaste mas",
    "gastos agrupados",
])
def test_get_expenses_by_category(nlu, text):
    res = nlu.interpret(text)
    assert res.intent == "get_expenses_by_category"
    assert res.confidence >= 0.85
    assert not res.needs_clarification


# =========================
# MOVEMENTS
# =========================

@pytest.mark.parametrize("text", [
    "movimientos",
    "últimos movimientos",
    "ultimos movimientos",
    "ver transacciones",
])
def test_get_movements(nlu, text):
    res = nlu.interpret(text)
    assert res.intent == "get_movements"
    assert res.confidence >= 0.85
    assert not res.needs_clarification


# =========================
# EXPENSES TOTAL — WITH PERIOD
# =========================

@pytest.mark.parametrize("text", [
    "cuánto gasté en enero",
    "cuanto gaste en enero",
    "cuánto gasté este mes",
    "total de gastos el mes pasado",
    "cuánto gasté ayer",
])
def test_get_expenses_total_with_period(nlu, text):
    res = nlu.interpret(text)
    assert res.intent == "get_expenses_total"
    assert not res.needs_clarification


# =========================
# EXPENSES TOTAL — WITHOUT PERIOD (CLARIFICATION REQUIRED)
# =========================

@pytest.mark.parametrize("text", [
    "cuánto gasté",
    "cuanto gaste",
    "total de gastos",
    "decime cuánto gasté",
])
def test_get_expenses_total_needs_period(nlu, text):
    res = nlu.interpret(text)
    assert res.intent == "get_expenses_total"
    assert res.needs_clarification
    assert res.missing_slots is not None
    assert "period" in res.missing_slots
    assert res.clarification_question is not None


# =========================
# UNKNOWN
# =========================

@pytest.mark.parametrize("text", [
    "hola",
    "buen día",
    "buen dia",
    "asdf",
    "qwerty",
])
def test_unknown_intent(nlu, text):
    res = nlu.interpret(text)
    assert res.intent == "unknown"
