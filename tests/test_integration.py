"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D)."""
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refuse_de_demarrer(tmp_path, monkeypatch):
    """D.2 : modèle absent, l'API refuse de démarrer (FileNotFoundError)."""
    from fastapi.testclient import TestClient

    from api.main import app
    from predict import charger_modele

    fake_modele = tmp_path / "absent.joblib"
    monkeypatch.setattr("predict.MODELE", fake_modele)
    charger_modele.cache_clear()

    with pytest.raises(FileNotFoundError):
        with TestClient(app):
            pass

    # Restaurer le cache pour les autres tests
    charger_modele.cache_clear()


def test_modele_retire_renvoie_503(monkeypatch):
    """D.3 : modèle retiré de app.state, 503 sur /health et /predict."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        old = app.state.classifier
        del app.state.classifier
        try:
            assert client.get("/health").status_code == 503
            assert client.post("/predict", json={"text": "un avis"}).status_code == 503
        finally:
            app.state.classifier = old


def test_modele_en_panne_renvoie_500(monkeypatch):
    """D.4 : predict lève RuntimeError, l'API renvoie 500 sans le message interne."""
    from fastapi.testclient import TestClient

    from api.main import app

    class BugClassifier:
        model_name = "bug"

        def predict(self, text: str) -> dict:
            raise RuntimeError("bug interne")

    with TestClient(app) as client:
        old = app.state.classifier
        app.state.classifier = BugClassifier()
        try:
            r = client.post("/predict", json={"text": "un avis"})
            assert r.status_code == 500
            assert "bug interne" not in r.text
        finally:
            app.state.classifier = old


def test_modele_etiquettes_inconnues_refuse_de_demarrer(monkeypatch):
    """D.5 : modèle aux étiquettes inconnues, l'API renvoie 500."""
    from fastapi.testclient import TestClient

    from api.main import app

    class BadClassifier:
        model_name = "bad"

        def predict(self, text: str) -> dict:
            return {"label": "MAUVAIS", "score": 0.9, "text": text}

    with TestClient(app) as client:
        old = app.state.classifier
        app.state.classifier = BadClassifier()
        try:
            r = client.post("/predict", json={"text": "un avis"})
            assert r.status_code == 500
        finally:
            app.state.classifier = old
