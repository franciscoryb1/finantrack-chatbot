from typing import Optional


def normalize_category(
    *,
    category_hint: str,
    user_categories: list[str],
) -> Optional[str]:
    """
    Devuelve el nombre (o id) de la categoría real del usuario
    que mejor coincide con el hint del NLU.
    """
    if not category_hint:
        return None

    hint = category_hint.lower()

    for cat in user_categories:
        if hint in cat.lower():
            return cat

    return None
