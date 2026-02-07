from dataclasses import dataclass


@dataclass
class NLUResult:
    intent: str
    intent_confidence: float

    period_type: str
    period_confidence: float

    category_hint: str
    category_confidence: float
