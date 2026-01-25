from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Finances Chatbot Service"
    app_env: str = "dev"

    class Config:
        env_file = ".env"


settings = Settings()
