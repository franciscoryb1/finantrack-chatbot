from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class Interpretation(BaseModel):
    """
    Representa la interpretación estructurada de un mensaje del usuario.
    Es producido por NLU y consumido por el Orchestrator.
    """

    intent: str
    confidence: float

    entities: Dict[str, Any] = {}

    needs_clarification: bool = False
    missing_slots: List[str] = []

    clarification_question: Optional[str] = None
