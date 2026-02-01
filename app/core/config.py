from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    app_name: str = "Finances Chatbot Service"
    app_env: str = "dev"

    ENABLE_LLM_FALLBACK: bool = Field(default=False)
    GEMINI_API_KEY: str | None = Field(default=None)
    GEMINI_MODEL: str = Field(default="gemini-1.5-flash")
    GEMINI_TIMEOUT_SECONDS: float = Field(default=5.0)

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
