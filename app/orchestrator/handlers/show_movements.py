from app.core.schemas import ChatResponse
from app.core.thresholds import SLOT_THRESHOLD
from app.normalizers.period_normalizer import normalize_period
from app.services.movements_service import fetch_movements
from app.agents.prompts import build_movements_explanation_prompt


async def handle_show_movements(
    *,
    session,
    text: str,
    interpretation,
    agent,
    trace_id: str,
) -> ChatResponse:

    # 1️⃣ Período (requerido)
    if interpretation.period_confidence < SLOT_THRESHOLD:
        return ChatResponse(
            replyText="¿Para qué período querés ver los movimientos?",
            traceId=trace_id,
        )

    from_date, to_date = normalize_period(interpretation.period_type)

    # 2️⃣ Categoría (opcional)
    category = None
    if interpretation.category_confidence >= SLOT_THRESHOLD:
        category = interpretation.category_hint

    # 3️⃣ Tool (fuente única de verdad)
    data = await fetch_movements(
        phone_number=session.phone_number,
        from_date=from_date,
        to_date=to_date,
        category=category,
        page=1,
        page_size=20,
    )

    # 4️⃣ Explicación
    prompt = build_movements_explanation_prompt(
        user_text=text,
        data=data,
    )

    explanation = await agent.run(
        phone_number=session.phone_number,
        text=prompt,
    )

    return ChatResponse(
        replyText=explanation["reply_text"],
        traceId=trace_id,
    )
