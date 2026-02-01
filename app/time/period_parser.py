import re
from datetime import date, timedelta
from calendar import monthrange

from app.time.models import PeriodParseResult


MONTHS = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}


def parse_period(text: str, today: date) -> PeriodParseResult | None:
    t = text.lower()

    # ----------------
    # HOY / AYER
    # ----------------
    if "hoy" in t:
        return PeriodParseResult(
            from_date=today,
            to_date=today,
            granularity="day",
            label="hoy",
        )

    if "ayer" in t:
        d = today - timedelta(days=1)
        return PeriodParseResult(
            from_date=d,
            to_date=d,
            granularity="day",
            label="ayer",
        )

    # ----------------
    # ESTE MES / MES PASADO
    # ----------------
    if "este mes" in t:
        from_d = today.replace(day=1)
        last_day = monthrange(today.year, today.month)[1]
        to_d = today.replace(day=last_day)

        return PeriodParseResult(
            from_date=from_d,
            to_date=to_d,
            granularity="month",
            label="este mes",
        )

    if "mes pasado" in t:
        year = today.year
        month = today.month - 1
        if month == 0:
            month = 12
            year -= 1

        last_day = monthrange(year, month)[1]
        return PeriodParseResult(
            from_date=date(year, month, 1),
            to_date=date(year, month, last_day),
            granularity="month",
            label="mes pasado",
        )

    # ----------------
    # MESES EXPLÍCITOS (enero, enero 2025)
    # ----------------
    for name, month in MONTHS.items():
        if name in t:
            year = today.year
            match = re.search(rf"{name}\s+(\d{{4}})", t)
            if match:
                year = int(match.group(1))

            last_day = monthrange(year, month)[1]
            return PeriodParseResult(
                from_date=date(year, month, 1),
                to_date=date(year, month, last_day),
                granularity="month",
                label=f"{name} {year}",
            )

    # ----------------
    # ÚLTIMOS N DÍAS
    # ----------------
    match = re.search(r"últimos?\s+(\d+)\s+d[ií]as?", t)
    if match:
        days = int(match.group(1))
        return PeriodParseResult(
            from_date=today - timedelta(days=days),
            to_date=today,
            granularity="range",
            label=f"últimos {days} días",
        )

    return None
