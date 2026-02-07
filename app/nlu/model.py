import json
import torch
from transformers import AutoTokenizer

from app.nlu.nn_model import NLUMultiHeadModel
from app.nlu.softmax import softmax_confidence
from app.nlu.config import (
    MODEL_NAME,
    MODEL_PATH,
    LABELS_PATH,
)

_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
_model = None
_mappings = None


def _load():
    global _model, _mappings

    if _model is not None:
        return

    # Cargar labels
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        _mappings = json.load(f)

    # Instanciar modelo
    _model = NLUMultiHeadModel(
        model_name=MODEL_NAME,
        num_intents=len(_mappings["intent"]),
        num_periods=len(_mappings["period_type"]),
        num_categories=len(_mappings["category_hint"]),
    )

    # Cargar pesos
    state = torch.load(MODEL_PATH, map_location=_device)
    _model.load_state_dict(state)

    _model.to(_device)
    _model.eval()


def run_nlu(text: str) -> dict:
    _load()

    encoding = _tokenizer(
        text.strip().lower(),
        truncation=True,
        padding="max_length",
        max_length=64,
        return_tensors="pt",
    )

    encoding = {k: v.to(_device) for k, v in encoding.items()}

    with torch.no_grad():
        outputs = _model(
            input_ids=encoding["input_ids"],
            attention_mask=encoding["attention_mask"],
        )

    ip, ic = softmax_confidence(outputs["intent_logits"])
    pp, pc = softmax_confidence(outputs["period_logits"])
    cp, cc = softmax_confidence(outputs["category_logits"])

    return {
        "intent": _mappings["intent"][ip[0]],
        "intent_confidence": float(ic[0]),

        "period_type": _mappings["period_type"][pp[0]],
        "period_confidence": float(pc[0]),

        "category_hint": _mappings["category_hint"][cp[0]],
        "category_confidence": float(cc[0]),
    }
