import re
from typing import Optional


_AMOUNT_REGEX = re.compile(
    r"(?P<amount>\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?)"
)


def normalize_amount(text: str) -> Optional[float]:
    """
    Extrae el primer monto numérico del texto.
    Ej:
    - 'gasté 2500 en supermercado' -> 2500.0
    - 'pagué $1.200,50' -> 1200.50
    """
    match = _AMOUNT_REGEX.search(text)
    if not match:
        return None

    raw = match.group("amount")

    # Normalizar separadores
    normalized = raw.replace(".", "").replace(",", ".")
    try:
        return float(normalized)
    except ValueError:
        return None
