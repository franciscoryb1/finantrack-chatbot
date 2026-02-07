from dataclasses import dataclass
from typing import Optional


@dataclass
class Interpretation:
    # Intent
    intent: str
    intent_confidence: float

    # Slots semánticos (NO normalizados)
    period_type: Optional[str]
    period_confidence: float

    category_hint: Optional[str]
    category_confidence: float

    # Control de diálogo
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
