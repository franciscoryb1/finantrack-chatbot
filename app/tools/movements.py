from typing import Optional
from pydantic import BaseModel, Field
from langchain.tools import tool

from app.tools.base import ToolResult
from app.actions.dispatcher import ActionDispatcher
from app.slots.type_normalizer import normalize_type  # si aplica
from app.slots.category_normalizer import normalize_category  # si aplica

class GetMovementsInput(BaseModel):
    period: Optional[str] = Field(
        default=None,
        description="Periodo de tiempo, por ejemplo: 'hoy', 'este mes', 'mes pasado'"
    )

@tool(args_schema=GetMovementsInput)
def get_movements(period: Optional[str] = None) -> ToolResult:
    """
    Obtiene los movimientos financieros del usuario.
    """

    # 1️⃣ Normalización (determinística)
    entities = {}
    if period:
        entities["period"] = period  # si luego tenés normalizador de period, va acá

    # 2️⃣ Dispatch a Action real
    dispatcher = ActionDispatcher()

    action_result = dispatcher.dispatch(
        intent="get_movements",
        entities=entities
    )

    # 3️⃣ Contrato de retorno estándar
    return {
        "reply_text": action_result.reply_text,
        "data": action_result.data,
    }
