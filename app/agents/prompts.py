# app/agents/prompts.py

from typing import Dict, Any


def build_movements_explanation_prompt(
    *,
    user_text: str,
    data: Dict[str, Any],
    locale: str = "es-AR",
) -> str:
    """
    Prompt controlado para explicar movimientos financieros reales.

    Reglas:
    - NO inventar datos
    - NO llamar herramientas
    - NO asumir información no presente
    - Explicar de forma clara y breve
    """

    return (
        "Sos un asistente financiero personal.\n\n"
        "El usuario hizo la siguiente consulta:\n"
        f"\"{user_text}\"\n\n"
        "A continuación tenés DATOS FINANCIEROS REALES del sistema.\n"
        "Tu única tarea es EXPLICAR lo que muestran esos datos.\n\n"
        "REGLAS ABSOLUTAS:\n"
        "- No inventes información.\n"
        "- No supongas categorías, totales ni conclusiones no explícitas.\n"
        "- No llames herramientas ni menciones su uso.\n"
        "- Si los datos están vacíos, decilo claramente.\n\n"
        "DATOS:\n"
        f"{data}\n\n"
        "Explicá los resultados de forma clara, breve y fácil de entender."
    )
