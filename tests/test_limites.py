"""Tests aux limites du contrat d'entrée (TP4, étape B)."""
import json
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient

    from api.main import app
    with TestClient(app) as c:
        yield c


def en_json(valeur: object) -> bytes:
    return json.dumps(valeur).encode("utf-8")


CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "   "}), 422, id="espaces-seuls"),
    pytest.param(en_json({"text": "a"}), 200, id="un-seul-caractere"),
    pytest.param(en_json({"text": "a" * 2000}), 200, id="2000-caracteres"),
    pytest.param(en_json({"text": "a" * 2001}), 422, id="2001-caracteres"),
    pytest.param(en_json({}), 422, id="champ-absent"),
    pytest.param(en_json({"text": 42}), 422, id="champ-type-invalide"),
    pytest.param(b"pas du json", 422, id="corps-non-json"),
]


@pytest.mark.parametrize("corps, code_attendu", CAS)
def test_frontieres_du_contrat(client, corps, code_attendu):
    reponse = client.post("/predict", content=corps, headers={"Content-Type": "application/json"})
    assert reponse.status_code == code_attendu
    if code_attendu == 422:
        detail = reponse.json()["detail"]
        assert isinstance(detail, list), f"detail attendu en liste, reçu : {type(detail)}"
        assert detail, "detail ne doit pas être une liste vide"
        for erreur in detail:
            assert "loc" in erreur
            assert "msg" in erreur
            assert "type" in erreur


@given(st.text(min_size=1, max_size=2000).filter(lambda t: t.strip()))
@settings(deadline=None, max_examples=50)
def test_texte_valide_recoit_200(client, texte):
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 200, f"texte={texte!r} -> {reponse.status_code}"
    body = reponse.json()
    assert body["label"] in {"POSITIVE", "NEGATIVE", "INDETERMINE"}
    assert 0.0 <= body["score"] <= 1.0


@given(st.text(alphabet=" \t\n\r\u0085", min_size=1, max_size=100))
@settings(deadline=None, max_examples=50)
def test_texte_blancs_recoit_422(client, texte):
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 422, f"texte={texte!r} -> {reponse.status_code}"
    detail = reponse.json()["detail"]
    assert isinstance(detail, list), f"detail attendu en liste, reçu : {type(detail)}"
