# app/infra/user_session.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserSession:
    phone_number: str
    user_id: Optional[str] = None
