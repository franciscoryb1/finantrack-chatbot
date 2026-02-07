from pathlib import Path

# Base del proyecto
BASE_DIR = Path(__file__).resolve().parents[2]

# Versionado del modelo
MODEL_VERSION = "v1"

MODEL_DIR = BASE_DIR / "app" / "training" / MODEL_VERSION / "models"

MODEL_PATH = MODEL_DIR / "nlu_model_v1.pt"
LABELS_PATH = MODEL_DIR / "label_mappings.json"

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
