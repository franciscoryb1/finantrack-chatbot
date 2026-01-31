from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

import httpx

from app.core.config import settings


@dataclass
class LLMSuggestion:
    intent: str
    confidence: float
    needs_clarification: bool = False
    clarification_question: Optional[str] = None


class GeminiLLMFallbackService:
    """
    Gemini LLM fallback: sugiere intent en JSON estricto.
    - No ejecuta acciones
    - No inventa intents (se valida aguas abajo también)
    """

    ALLOWED_INTENTS = {
        "help",
        "get_movements",
        "get_expenses_total",
        "get_expenses_by_category",
        "get_balance",
        "unknown",
    }

    def __init__(
        self,
        api_key: str,
        model: str,
        timeout_seconds: float = 5.0,
    ):
        self._api_key = api_key
        self._model = model
        self._timeout = timeout_seconds

        # Endpoint oficial (Generative Language API)
        self._base_url = "https://generativelanguage.googleapis.com"

    def _system_prompt(self) -> str:
        return (
            "You are an intent classification assistant for a personal finance chatbot.\n\n"
            "Your task is to analyze the user's message and return ONLY a valid JSON object.\n\n"
            "Rules:\n"
            "- You MUST return ONLY JSON.\n"
            "- Do NOT add explanations, text, or markdown.\n"
            "- Do NOT invent intents.\n"
            "- Use ONLY one of the allowed intents.\n"
            "- Confidence must be a number between 0 and 1.\n\n"
            "Allowed intents:\n"
            "- help\n"
            "- get_movements\n"
            "- get_expenses_total\n"
            "- get_expenses_by_category\n"
            "- get_balance\n"
            "- unknown\n\n"
            "If you are not confident, return:\n"
            '{\n'
            '  "intent": "unknown",\n'
            '  "confidence": 0.0,\n'
            '  "needs_clarification": false,\n'
            '  "clarification_question": null\n'
            '}\n'
        )

    def _user_prompt(self, user_text: str) -> str:
        return f'User message:\n"{user_text}"\n\nReturn the JSON now.'

    async def suggest(self, text: str) -> LLMSuggestion:
        """
        Devuelve LLMSuggestion o lanza excepción (que el caller captura).
        """
        url = f"{self._base_url}/v1beta/models/{self._model}:generateContent"

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": self._system_prompt()},
                        {"text": self._user_prompt(text)},
                    ],
                }
            ],
            # bajamos creatividad
            "generationConfig": {
                "temperature": 0.0,
                "topP": 0.1,
                "maxOutputTokens": 200,
            },
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(
                url,
                params={"key": self._api_key},
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()

        # Extraer texto del candidato
        raw_text = self._extract_text(data)

        # Parse JSON estricto (tolerante a basura alrededor)
        obj = self._parse_json_object(raw_text)

        return self._validate(obj)

    def _extract_text(self, data: dict) -> str:
        """
        Gemini típicamente devuelve:
        candidates[0].content.parts[0].text
        """
        candidates = data.get("candidates") or []
        if not candidates:
            raise ValueError("Gemini returned no candidates")

        content = (candidates[0].get("content") or {})
        parts = content.get("parts") or []
        if not parts:
            raise ValueError("Gemini returned no parts")

        txt = parts[0].get("text")
        if not isinstance(txt, str) or not txt.strip():
            raise ValueError("Gemini returned empty text")

        return txt.strip()

    def _parse_json_object(self, raw: str) -> dict:
        """
        Queremos JSON-only, pero por seguridad toleramos:
        - backticks
        - texto antes/después
        Entonces extraemos el primer {...} válido.
        """
        cleaned = raw.strip().strip("`").strip()

        # intento directo
        try:
            obj = json.loads(cleaned)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass

        # extracción por primer bloque { ... }
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No JSON object found in Gemini response")

        snippet = cleaned[start : end + 1]
        obj = json.loads(snippet)
        if not isinstance(obj, dict):
            raise ValueError("Parsed JSON is not an object")
        return obj

    def _validate(self, obj: dict) -> LLMSuggestion:
        intent = obj.get("intent")
        confidence = obj.get("confidence")
        needs_clarification = obj.get("needs_clarification", False)
        clarification_question = obj.get("clarification_question", None)

        if not isinstance(intent, str) or intent not in self.ALLOWED_INTENTS:
            # devolvemos unknown seguro
            return LLMSuggestion(intent="unknown", confidence=0.0)

        try:
            conf = float(confidence)
        except Exception:
            conf = 0.0

        if conf < 0.0:
            conf = 0.0
        if conf > 1.0:
            conf = 1.0

        if not isinstance(needs_clarification, bool):
            needs_clarification = False

        if clarification_question is not None and not isinstance(clarification_question, str):
            clarification_question = None

        return LLMSuggestion(
            intent=intent,
            confidence=conf,
            needs_clarification=needs_clarification,
            clarification_question=clarification_question,
        )


def build_gemini_llm_fallback() -> GeminiLLMFallbackService | None:
    """
    Factory: respeta feature flag y presencia de API key.
    """
    if not settings.ENABLE_LLM_FALLBACK:
        return None

    if not settings.GEMINI_API_KEY:
        return None

    return GeminiLLMFallbackService(
        api_key=settings.GEMINI_API_KEY,
        model=settings.GEMINI_MODEL,
        timeout_seconds=settings.GEMINI_TIMEOUT_SECONDS,
    )
