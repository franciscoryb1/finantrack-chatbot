from datetime import date
from app.nlu.rules_nlu import Interpretation
from app.nlu.nlu_service import NLUService


def test_expenses_total_without_period_requests_clarification():
    nlu = NLUService()

    result = Interpretation(
        intent="get_expenses_total",
        confidence=0.9,
        entities={},
    )

    out = nlu._finalize_with_slot_validation(result, "cuánto gasté")

    assert out.needs_clarification is True
    assert out.missing_slots == ["period"]
    assert "período" in out.clarification_question.lower()


def test_expenses_total_with_explicit_period_is_resolved():
    nlu = NLUService()

    result = Interpretation(
        intent="get_expenses_total",
        confidence=0.9,
        entities={},
    )

    out = nlu._finalize_with_slot_validation(result, "cuánto gasté este mes")

    assert out.needs_clarification is False
    assert "period" in out.entities
    assert out.entities["period"]["label"] == "este mes"


def test_category_is_normalized_if_present():
    nlu = NLUService()

    result = Interpretation(
        intent="get_expenses_total",
        confidence=0.9,
        entities={},
    )

    out = nlu._finalize_with_slot_validation(
        result, "cuánto gasté en comida este mes"
    )

    assert out.entities["category"] == "comida"


def test_type_is_normalized_if_present():
    nlu = NLUService()

    result = Interpretation(
        intent="get_expenses_total",
        confidence=0.9,
        entities={},
    )

    out = nlu._finalize_with_slot_validation(
        result, "cuánto gasté"
    )

    assert out.entities.get("type") == "EXPENSE"


def test_existing_entities_are_not_overwritten():
    nlu = NLUService()

    result = Interpretation(
        intent="get_expenses_total",
        confidence=0.9,
        entities={
            "category": "transporte"
        },
    )

    out = nlu._finalize_with_slot_validation(
        result, "cuánto gasté en comida este mes"
    )

    assert out.entities["category"] == "transporte"
    assert "period" in out.entities
