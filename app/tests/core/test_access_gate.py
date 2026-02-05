from app.core.access_gate import decide_access, AccessLevel


def test_financial_keyword():
    d = decide_access("mostrame mis gastos")
    assert d.access_level == AccessLevel.REAL_DATA_REQUIRED


def test_quantifier_and_temporal():
    d = decide_access("cuanto gaste este mes")
    assert d.access_level == AccessLevel.REAL_DATA_REQUIRED


def test_non_financial_greeting():
    d = decide_access("hola, como estas?")
    assert d.access_level == AccessLevel.NO_REAL_DATA


def test_ambiguous_but_conservative():
    d = decide_access("me preocupa la plata")
    assert d.access_level == AccessLevel.NO_REAL_DATA


def test_movements_without_quantifier():
    d = decide_access("movimientos")
    assert d.access_level == AccessLevel.REAL_DATA_REQUIRED
