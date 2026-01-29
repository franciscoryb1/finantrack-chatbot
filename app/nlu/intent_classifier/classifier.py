from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from joblib import load


@dataclass(frozen=True)
class IntentPrediction:
    intent: str
    confidence: float


class IntentClassifierService:
    """
    Wrapper del modelo entrenado (Pipeline TF-IDF + LogisticRegression).
    Carga 1 vez el .joblib y expone predict(text) -> IntentPrediction.
    """

    def __init__(self, model_path: Optional[str] = None):
        self._model_path = Path(
            model_path
            or Path(__file__).resolve().parents[2]  # app/
            / "training"
            / "model"
            / "intent_classifier.joblib"
        )
        self._pipeline = None

    def _load_model(self):
        if self._pipeline is None:
            self._pipeline = load(self._model_path)

    def predict(self, text: str) -> IntentPrediction:
        self._load_model()

        probas = self._pipeline.predict_proba([text])[0]
        classes = self._pipeline.classes_

        best_idx = probas.argmax()
        return IntentPrediction(
            intent=str(classes[best_idx]),
            confidence=float(probas[best_idx]),
        )
