from langchain_openai import ChatOpenAI
from app.core.config import settings


def build_openai_llm(
    *,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
):
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=settings.OPENAI_API_KEY,
    )
