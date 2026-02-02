from contextvars import ContextVar
from typing import Optional

_user_jwt: ContextVar[Optional[str]] = ContextVar("user_jwt", default=None)
_user_phone: ContextVar[Optional[str]] = ContextVar("user_phone", default=None)

def set_request_context(*, user_jwt: str, user_phone: str):
    t1 = _user_jwt.set(user_jwt)
    t2 = _user_phone.set(user_phone)
    return (t1, t2)

def reset_request_context(tokens):
    t1, t2 = tokens
    _user_jwt.reset(t1)
    _user_phone.reset(t2)

def get_user_jwt() -> str:
    v = _user_jwt.get()
    if not v:
        raise RuntimeError("Missing user_jwt in request context")
    return v

def get_user_phone() -> str:
    v = _user_phone.get()
    if not v:
        raise RuntimeError("Missing user_phone in request context")
    return v
