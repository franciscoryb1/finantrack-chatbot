from datetime import date
from app.conversation.state import ConversationState
from app.conversation.entity_extractor import extract_entities_only
from app.nlu.nlu_service import Interpretation

class ConversationResolver:

    def __init__(self, nlu, *, today: date | None = None):
        self.nlu = nlu
        self.today = today

    def resolve(self, text: str, state: ConversationState) -> Interpretation:
        text = text.strip().lower()

        # 1️⃣ Sin contexto → NLU normal
        if not state.last_intent:
            result = self.nlu.interpret(text)
            result = self._ensure_interpretation(result)
            self._update_state_from_result(state, result)
            return result

        # 2️⃣ Extraer SOLO slots
        extracted_entities = extract_entities_only(text, today=self.today)

        # Si no hay slots útiles → NLU normal
        if not extracted_entities:
            result = self.nlu.interpret(text)
            result = self._ensure_interpretation(result)
            self._update_state_from_result(state, result)
            return result

        # 3️⃣ Heredar intent
        intent = state.last_intent

        # 4️⃣ Merge de entities (lo nuevo pisa)
        entities = {**state.last_entities, **extracted_entities}

        # 5️⃣ Revalidar con NLU
        result = Interpretation(
            intent=intent,
            confidence=1.0,
            entities=entities,
        )

        result = self.nlu._finalize_with_slot_validation(result, text)
        result = self._ensure_interpretation(result)

        # 6️⃣ Update state
        self._update_state_from_result(state, result)

        return result

    def _update_state_from_result(self, state: ConversationState, result):
        if result.needs_clarification:
            state.last_intent = result.intent
            state.last_entities = result.entities or {}
            state.awaiting_slots = set(result.missing_slots or [])
        else:
            state.clear()
            
    def _ensure_interpretation(self, result) -> Interpretation:
        if isinstance(result, Interpretation):
            return result
        return Interpretation(**result)

