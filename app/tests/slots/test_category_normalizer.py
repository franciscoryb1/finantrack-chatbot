from app.slots.category_normalizer import normalize_category


def test_category_comida():
    assert normalize_category("gastos de comida") == "comida"
    assert normalize_category("fui al restaurante") == "comida"


def test_category_transporte():
    assert normalize_category("uber") == "transporte"


def test_none():
    assert normalize_category("balance general") is None
