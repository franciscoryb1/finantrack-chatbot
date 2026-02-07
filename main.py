from fastapi import FastAPI
from app.core.config import settings
from app.api.chat import router as chat_router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.include_router(chat_router)

print('docs: http://localhost:8010/docs')

from app.nlu.model import run_nlu

# print(run_nlu("gasté 2500 en supermercado ayer"))



@app.get("/health", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "env": settings.app_env,
    }
