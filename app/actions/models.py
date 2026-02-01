from typing import Optional, Dict, Any
from pydantic import BaseModel


class ActionResult(BaseModel):
    reply_text: str
    data: Optional[Dict[str, Any]] = None
