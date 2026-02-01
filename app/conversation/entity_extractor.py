from datetime import date
from dataclasses import asdict, is_dataclass

from app.time.period_parser import parse_period
from app.slots.type_normalizer import normalize_type
from app.slots.category_normalizer import normalize_category


def _to_plain_dict(obj):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj
    # pydantic v2
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    # pydantic v1
    if hasattr(obj, "dict"):
        return obj.dict()
    # dataclass
    if is_dataclass(obj):
        return asdict(obj)
    # fallback
    return obj.__dict__


def extract_entities_only(text: str, *, today: date | None = None) -> dict:
    entities = {}
    today = today or date.today()

    period = parse_period(text, today=today)
    if period:
        entities["period"] = _to_plain_dict(period)

    t = normalize_type(text)
    if t:
        entities["type"] = t

    c = normalize_category(text)
    if c:
        entities["category"] = c

    return entities
