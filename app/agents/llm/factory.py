from app.core.config import settings
from app.agents.llm.groq import build_groq_llm
from app.agents.llm.openai import build_openai_llm


def build_llm():
    provider = settings.LLM_PROVIDER.lower()

    if provider == "groq":
        return build_groq_llm()

    if provider == "openai":
        return build_openai_llm()

    raise RuntimeError(f"Unsupported LLM provider: {provider}")
