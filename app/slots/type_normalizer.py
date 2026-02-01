def normalize_type(text: str) -> str | None:
    t = text.lower()

    expense_keywords = [
        "gasto", "gasté", "gaste", "pagos", "pagué", "pague",
        "compras", "comida", "alquiler"
    ]

    income_keywords = [
        "ingreso", "ingresos", "cobré", "cobre",
        "sueldo", "salario", "plata que entró", "me pagaron"
    ]

    if any(k in t for k in expense_keywords):
        return "EXPENSE"

    if any(k in t for k in income_keywords):
        return "INCOME"

    return None
