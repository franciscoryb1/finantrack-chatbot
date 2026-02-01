from app.slots.type_normalizer import normalize_type


def test_expense_detection():
    assert normalize_type("cuanto gaste") == "EXPENSE"
    assert normalize_type("mis gastos del mes") == "EXPENSE"


def test_income_detection():
    assert normalize_type("cuanto cobre") == "INCOME"
    assert normalize_type("mis ingresos") == "INCOME"


def test_none():
    assert normalize_type("balance") is None
