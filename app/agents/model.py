from typing import Optional, Dict
from pydantic import BaseModel


class AgentResult(BaseModel):
    reply_text: str
    data: Optional[Dict] = None
