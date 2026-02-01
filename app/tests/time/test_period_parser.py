from datetime import date

from app.time.period_parser import parse_period


TODAY = date(2025, 2, 10)


def test_parse_hoy():
    res = parse_period("cuanto gaste hoy", TODAY)
    assert res.from_date == TODAY
    assert res.to_date == TODAY
    assert res.granularity == "day"


def test_parse_ayer():
    res = parse_period("ayer gaste mucho", TODAY)
    assert res.from_date == date(2025, 2, 9)
    assert res.to_date == date(2025, 2, 9)


def test_parse_este_mes():
    res = parse_period("este mes", TODAY)
    assert res.from_date == date(2025, 2, 1)
    assert res.to_date == date(2025, 2, 28)


def test_parse_mes_pasado():
    res = parse_period("mes pasado", TODAY)
    assert res.from_date == date(2025, 1, 1)
    assert res.to_date == date(2025, 1, 31)


def test_parse_mes_explicito_sin_anio():
    res = parse_period("enero", TODAY)
    assert res.from_date == date(2025, 1, 1)
    assert res.to_date == date(2025, 1, 31)


def test_parse_mes_explicito_con_anio():
    res = parse_period("enero 2024", TODAY)
    assert res.from_date == date(2024, 1, 1)
    assert res.to_date == date(2024, 1, 31)


def test_parse_ultimos_dias():
    res = parse_period("últimos 7 días", TODAY)
    assert res.from_date == date(2025, 2, 3)
    assert res.to_date == TODAY


def test_parse_none():
    res = parse_period("cuanto gaste", TODAY)
    assert res is None
