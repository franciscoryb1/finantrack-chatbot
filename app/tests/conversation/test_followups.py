from datetime import date
import pytest

from app.conversation.state import ConversationState
from app.conversation.resolver import ConversationResolver
from app.nlu.nlu_service import Interpretation


# Fake NLU para testear resolver sin ML real
class FakeNLU:
    def interpret(self, text: str) -> Interpretation:
        return Interpretation(
            intent="unknown",
            confidence=0.2,
            entities={},
        )

    def _finalize_with_slot_validation(
        self, result: Interpretation, normalized_text: str
    ) -> Interpretation:
        # Simula la validación real del NLU
        if result.intent == "get_expenses_total" and "period" not in result.entities:
            return Interpretation(
                intent="get_expenses_total",
                confidence=result.confidence,
                entities=result.entities,
                needs_clarification=True,
                missing_slots=["period"],
            )

        return result


@pytest.fixture
def today():
    return date(2025, 2, 15)


@pytest.fixture
def resolver(today):
    return ConversationResolver(FakeNLU(), today=today)


def test_followup_resolves_missing_period(resolver):
    state = ConversationState(
        last_intent="get_expenses_total",
        last_entities={},
        awaiting_slots={"period"},
    )

    result = resolver.resolve("este mes", state)

    assert result.intent == "get_expenses_total"
    assert "period" in result.entities
    assert result.needs_clarification is False

    # Como completó, el estado debería limpiarse
    assert state.last_intent is None
    assert state.last_entities == {}
    assert state.awaiting_slots == set()


def test_followup_replaces_period(resolver):
    state = ConversationState(
        last_intent="get_expenses_total",
        last_entities={"period": {"label": "este mes"}},
        awaiting_slots=set(),
    )

    result = resolver.resolve("y el mes pasado?", state)

    assert result.intent == "get_expenses_total"
    assert result.entities["period"]["label"] == "mes pasado"


def test_followup_adds_category(resolver):
    state = ConversationState(
        last_intent="get_expenses_total",
        last_entities={"period": {"label": "este mes"}},
        awaiting_slots=set(),
    )

    result = resolver.resolve("en comida", state)

    assert result.intent == "get_expenses_total"
    assert result.entities["category"] == "comida"
    assert result.entities["period"]["label"] == "este mes"


def test_followup_without_context_falls_back_to_nlu(resolver):
    state = ConversationState()

    result = resolver.resolve("este mes", state)

    # Sin contexto, cae al interpret() del NLU fake → unknown
    assert result.intent == "unknown"
