from app.actions.dispatcher import ActionDispatcher
from app.nlu.nlu_service import Interpretation


def test_dispatch_get_balance():
    dispatcher = ActionDispatcher()

    interpretation = Interpretation(
        intent="get_balance",
        confidence=0.9,
        entities={},
    )

    result = dispatcher.dispatch(interpretation)

    assert "saldo" in result.reply_text.lower()


def test_dispatch_get_movements():
    dispatcher = ActionDispatcher()

    interpretation = Interpretation(
        intent="get_movements",
        confidence=0.9,
        entities={},
    )

    result = dispatcher.dispatch(interpretation)

    assert "movimientos" in result.reply_text.lower()


def test_dispatch_get_expenses_total():
    dispatcher = ActionDispatcher()

    interpretation = Interpretation(
        intent="get_expenses_total",
        confidence=0.9,
        entities={
            "period": {"label": "este mes"},
        },
    )

    result = dispatcher.dispatch(interpretation)

    assert "gastaste" in result.reply_text.lower()


def test_dispatch_unknown_intent():
    dispatcher = ActionDispatcher()

    interpretation = Interpretation(
        intent="unknown",
        confidence=0.3,
        entities={},
    )

    result = dispatcher.dispatch(interpretation)

    assert "no entendí" in result.reply_text.lower()
