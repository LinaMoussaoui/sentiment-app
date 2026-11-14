#!/usr/bin/env python
"""Prédiction unitaire : la fonction que l'API de la semaine 3 appellera.

Usage :
  python src/predict.py "Livraison rapide, très satisfait"
  >>> from predict import predict ; predict("texte")

Le modèle est cherché dans cet ordre :
  1. la variable d'environnement SENTIMENT_MODELE (chemin absolu ou relatif) ;
  2. models/sentiment.joblib à la racine du dépôt.
"""
import os
import sys
from functools import lru_cache
from pathlib import Path

import joblib

RACINE = Path(__file__).resolve().parents[1]
MODELE = RACINE / "models" / "sentiment.joblib"


def chemin_modele() -> Path:
    """Le chemin du modèle : SENTIMENT_MODELE s'il est défini, sinon models/sentiment.joblib."""
    env = os.environ.get("SENTIMENT_MODELE")
    if env:
        return Path(env)
    return MODELE


@lru_cache(maxsize=1)
def charger_modele():
    """Chargé une seule fois par processus, pas à chaque appel."""
    chemin = chemin_modele()
    if not chemin.exists():
        raise FileNotFoundError(
            f"{chemin} absent : définissez SENTIMENT_MODELE ou lancez python src/train.py"
        )
    return joblib.load(chemin)


def predict(texte: str) -> dict:
    """Renvoie {'label': 'positive'|'negative', 'score': float}."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    etiquette = pipeline.predict([texte])[0]
    score = float(pipeline.predict_proba([texte]).max())
    return {"label": etiquette, "score": round(score, 4)}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    resultat = predict(" ".join(sys.argv[1:]))
    print(f"{resultat['label']} (confiance {resultat['score']:.0%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
