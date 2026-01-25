import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from joblib import dump
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "intents_dataset.csv"
OUTPUT_DIR = BASE_DIR / "model"

OUTPUT_DIR.mkdir(exist_ok=True)


def main():
    # 1. Cargar dataset
    df = pd.read_csv(DATASET_PATH)

    texts = df["text"]
    intents = df["intent"]

    # 2. Pipeline: TF-IDF + Logistic Regression
    pipeline = Pipeline(
        steps=[
            (
                "vectorizer",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    max_features=5000,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    solver="lbfgs",
                    multi_class="auto",
                ),
            ),
        ]
    )

    # 3. Entrenar
    pipeline.fit(texts, intents)

    # 4. Guardar pipeline completo
    model_path = OUTPUT_DIR / "intent_classifier.joblib"
    dump(pipeline, model_path)

    print("✅ Modelo entrenado y guardado en:")
    print(model_path)


if __name__ == "__main__":
    main()
