# tests/nlu/test_nlu_movements.py

from datetime import datetime

import pytest

from app.nlu import NLUInterpreter


@pytest.fixture()
def nlu():
    return NLUInterpreter()


def test_intent_show_movements_simple(nlu):
    out = nlu.interpret("Mostrame mis movimientos")
    assert out.intent == "SHOW_MOVEMENTS"
    assert out.needs_clarification is False


def test_intent_unknown(nlu):
    out = nlu.interpret("Hola, cómo estás?")
    assert out.intent == "UNKNOWN"
    assert out.entities == {}


def test_date_this_month(nlu):
    now = datetime(2026, 2, 4, 12, 0, 0)
    out = nlu.interpret("gastos de este mes", now=now)
    assert out.intent == "SHOW_MOVEMENTS"
    assert out.entities["from_date"] == "2026-02-01"
    assert out.entities["to_date"] == "2026-02-04"


def test_date_last_month(nlu):
    now = datetime(2026, 2, 4, 12, 0, 0)
    out = nlu.interpret("movimientos del mes pasado", now=now)
    assert out.entities["from_date"] == "2026-01-01"
    assert out.entities["to_date"] == "2026-01-31"


def test_date_month_name_with_year(nlu):
    now = datetime(2026, 2, 4, 12, 0, 0)
    out = nlu.interpret("transacciones de enero 2025", now=now)
    assert out.entities["from_date"] == "2025-01-01"
    assert out.entities["to_date"] == "2025-01-31"


def test_date_today(nlu):
    now = datetime(2026, 2, 4, 9, 30, 0)
    out = nlu.interpret("movimientos de hoy", now=now)
    assert out.entities["from_date"] == "2026-02-04"
    assert out.entities["to_date"] == "2026-02-04"


def test_date_yesterday(nlu):
    now = datetime(2026, 2, 4, 9, 30, 0)
    out = nlu.interpret("gastos de ayer", now=now)
    assert out.entities["from_date"] == "2026-02-03"
    assert out.entities["to_date"] == "2026-02-03"
