from pydantic import BaseModel


class ChatRequest(BaseModel):
    userId: int | str
    text: str
    channel: str = "test"
    locale: str = "es-AR"


class ChatResponse(BaseModel):
    replyText: str
    traceId: str
