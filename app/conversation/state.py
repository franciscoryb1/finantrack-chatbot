from typing import Optional, Dict, Set
from pydantic import BaseModel, Field

class ConversationState(BaseModel):
    last_intent: Optional[str] = None
    last_entities: Dict = Field(default_factory=dict)
    awaiting_slots: Set[str] = Field(default_factory=set)

    def clear(self):
        self.last_intent = None
        self.last_entities = {}
        self.awaiting_slots = set()
