from dataclasses import dataclass

@dataclass
class UserSession:
    user_id: str
    access_token: str
