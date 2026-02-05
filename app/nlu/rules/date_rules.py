from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from typing import Optional, Tuple


@dataclass(frozen=True)
class DateRange:
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    reason: Optional[str] = None


_MONTHS = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "setiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}


def _normalize(text: str) -> str:
    text = (text or "").strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"\s+", " ", text)
    return text


def _fmt(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def _month_range(year: int, month: int) -> Tuple[date, date]:
    """
    Devuelve (first_day, last_day) del mes.
    """
    first = date(year, month, 1)
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    last = next_month - timedelta(days=1)
    return first, last


def extract_date_range(text: str, now: Optional[datetime] = None) -> DateRange:
    """
    Extrae rango de fechas desde texto.
    Devuelve strings YYYY-MM-DD compatibles con tool get_movements.
    """
    t = _normalize(text)
    now_dt = now or datetime.now()
    today = now_dt.date()

    # hoy
    if re.search(r"\bhoy\b", t):
        d = today
        return DateRange(_fmt(d), _fmt(d), "today")

    # ayer
    if re.search(r"\bayer\b", t):
        d = today - timedelta(days=1)
        return DateRange(_fmt(d), _fmt(d), "yesterday")

    # este mes
    if re.search(r"\beste mes\b", t):
        first = date(today.year, today.month, 1)
        return DateRange(_fmt(first), _fmt(today), "this_month")

    # mes pasado
    if re.search(r"\bmes pasado\b", t) or re.search(r"\bel mes pasado\b", t):
        year = today.year
        month = today.month - 1
        if month == 0:
            month = 12
            year -= 1
        first, last = _month_range(year, month)
        return DateRange(_fmt(first), _fmt(last), "last_month")

    # Mes por nombre: "enero" o "enero 2025"
    month_names = "|".join(map(re.escape, _MONTHS.keys()))
    m = re.search(rf"\b({month_names})\b(?:\s+(20\d{{2}}))?", t)
    if m:
        month_name = m.group(1)
        year_str = m.group(2)
        month = _MONTHS[month_name]
        year = int(year_str) if year_str else today.year
        first, last = _month_range(year, month)
        return DateRange(_fmt(first), _fmt(last), f"month_name:{month_name}:{year}")

    return DateRange(None, None, "no_date")
