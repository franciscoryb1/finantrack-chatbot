from app.core.schemas import ChatResponse
from app.core.thresholds import SLOT_THRESHOLD
from app.normalizers.amount_normalizer import normalize_amount
from app.normalizers.period_normalizer import normalize_period
from app.normalizers.category_normalizer import normalize_category
from app.services.movements_service import create_expense


async def handle_add_expense(
    *,
    session,
    text: str,
    interpretation,
    agent,
    trace_id: str,
) -> ChatResponse:

    # 1️⃣ Monto (requerido)
    amount = normalize_amount(text)
    if amount is None:
        return ChatResponse(
            replyText="¿Cuál fue el monto del gasto?",
            traceId=trace_id,
        )

    # 2️⃣ Período (opcional → default hoy)
    if interpretation.period_confidence >= SLOT_THRESHOLD:
        from_date, _ = normalize_period(interpretation.period_type)
        date = from_date
    else:
        from datetime import date as _date
        date = _date.today()

    # 3️⃣ Categoría (opcional)
    category = None
    if interpretation.category_confidence >= SLOT_THRESHOLD:
        user_categories = session.categories  # asumimos disponibles
        category = normalize_category(
            category_hint=interpretation.category_hint,
            user_categories=user_categories,
        )

    # 4️⃣ Confirmación explícita
    confirmation_text = (
        f"Voy a registrar un gasto de ${amount:.2f}"
        f"{f' en la categoría {category}' if category else ''}"
        f" con fecha {date.isoformat()}. ¿Confirmás?"
    )

    confirmation = await agent.run(
        phone_number=session.phone_number,
        text=confirmation_text,
    )

    if "sí" not in confirmation["reply_text"].lower():
        return ChatResponse(
            replyText="Ok, no registré el gasto.",
            traceId=trace_id,
        )

    # 5️⃣ Ejecutar tool (fuente única de verdad)
    await create_expense(
        phone_number=session.phone_number,
        amount=amount,
        category=category,
        date=date,
        description=text,
    )

    return ChatResponse(
        replyText="Listo ✅ Ya registré el gasto.",
        traceId=trace_id,
    )
