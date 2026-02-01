from langchain_groq import ChatGroq
from app.core.config import settings


def build_groq_llm(
    *,
    model: str = "llama-3.1-8b-instant",
    temperature: float = 0.0,
):
    return ChatGroq(
        model=model,
        temperature=temperature,
        api_key=settings.GROQ_API_KEY,  # 👈 CLAVE
    )
