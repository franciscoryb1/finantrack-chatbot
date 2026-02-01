from typing import Dict
from app.conversation.state import ConversationState

_STATE_BY_USER: Dict[str, ConversationState] = {}

def get_state(user_id: str) -> ConversationState:
    if user_id not in _STATE_BY_USER:
        _STATE_BY_USER[user_id] = ConversationState()
    return _STATE_BY_USER[user_id]
