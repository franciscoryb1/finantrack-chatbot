from langchain_core.tools import tool

from app.tools.movements import get_movements


def build_tools(user_id: str):
    @tool
    def get_movements_tool() -> dict:
        """
        Obtiene los movimientos financieros recientes del usuario.
        Usar cuando el usuario quiera ver gastos, pagos o movimientos.
        """
        result = get_movements(user_id)
        return result.model_dump()

    return [get_movements_tool]
