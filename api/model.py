"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de sentiment_app/predict.py, qui charge models/sentiment.joblib une seule fois.
"""
from sentiment_app.predict import charger_modele, predict as _predict

SEUIL_ABSTENTION = 0.60  # sous ce seuil, le modèle s'abstient : un humain doit trancher


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        charger_modele()  # échoue immédiatement si le joblib manque : on ne démarre pas sans modèle

    def predict(self, text: str) -> dict:
        """Renvoie {'label': 'POSITIVE'|'NEGATIVE'|'INDETERMINE', 'score': float, 'text': aperçu}."""
        r = _predict(text)  # lève ValueError si le texte est vide
        label = r["label"].upper()
        score = float(r["score"])
        if score < SEUIL_ABSTENTION:
            label = "INDETERMINE"
        return {"label": label, "score": score, "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans sentiment_app/predict.py)."""
    return SentimentClassifier()
