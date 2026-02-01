CATEGORIES = {
    "comida": ["comida", "restaurant", "restaurante", "bar", "super", "supermercado"],
    "transporte": ["transporte", "uber", "taxi", "colectivo", "sube"],
    "alquiler": ["alquiler", "renta"],
    "servicios": ["luz", "agua", "gas", "internet"],
}


def normalize_category(text: str) -> str | None:
    t = text.lower()

    for canonical, keywords in CATEGORIES.items():
        if any(k in t for k in keywords):
            return canonical

    return None
