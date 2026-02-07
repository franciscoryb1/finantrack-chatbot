from datetime import date, timedelta
import calendar


def normalize_period(period_type: str, reference_date: date | None = None):
    """
    Devuelve (from_date, to_date)
    """
    today = reference_date or date.today()

    if period_type == "TODAY":
        return today, today

    if period_type == "YESTERDAY":
        y = today - timedelta(days=1)
        return y, y

    if period_type == "THIS_MONTH":
        first = today.replace(day=1)
        last = first.replace(
            day=calendar.monthrange(first.year, first.month)[1]
        )
        return first, last

    if period_type == "LAST_MONTH":
        first_this = today.replace(day=1)
        last_prev = first_this - timedelta(days=1)
        first_prev = last_prev.replace(day=1)
        return first_prev, last_prev

    # Fallback seguro
    first = today.replace(day=1)
    last = today
    return first, last
