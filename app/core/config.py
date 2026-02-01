from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    app_name: str = "Finances Chatbot Service"
    app_env: str = "dev"

    USE_AGENT: bool = True

    # LLM
    LLM_PROVIDER: str = "groq"  # groq | openai

    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None

    # === Chatbot / Backend ===
    FINANCE_API_BASE_URL: str
    CHATBOT_API_KEY: str

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
