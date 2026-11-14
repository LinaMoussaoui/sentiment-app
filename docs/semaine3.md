# Semaine 3 : l'API FastAPI

## Les quatre essais (T15 à T18)

| Contrôle | Requête | Réponse |
|---|---|---|
| T15 | `GET /health` | `200`, `"status": "OK"`, modèle `tfidf-logreg (TP2, models/sentiment.joblib)` |
| T16 | `POST /predict` `{"text": "Livraison rapide, produit conforme, très satisfait"}` | `200`, `POSITIVE`, `0.777` |
| T17 | `POST /predict` `{"text": "Produit cassé et service injoignable, à fuir"}` | `200`, `NEGATIVE`, `0.7465` |
| T18a | `POST /predict` `{"text": "   "}` (trois espaces) | `422`, `detail` = **chaîne** `"texte vide"` |
| T18b | `POST /predict` `{}` | `422`, `detail` = **liste** avec `type: missing` |
| T18c | `POST /predict` `{"text": 42}` | `422`, `detail` = **liste** avec `type: string_type` |

**Défaut constaté (que le TP4 corrigera)** : deux formes de 422 coexistent — une chaîne pour `{"text": "   "}` (refusé par `predict()`), une liste pour `{}` et `{"text": 42}` (refusés par Pydantic). Le TP4 uniformisera les deux formes.

## Question 1 — Pourquoi l'API refuse-t-elle de démarrer sans modèle, plutôt que de répondre 503 ?

Une API sans modèle ne pourra jamais répondre correctement : en refusant de démarrer, elle rend la panne visible tout de suite, au moment du déploiement, au lieu de paraître en marche et de répondre 503 à chaque client. Le code 503 sert aux indisponibilités passagères, quand le modèle a été retiré en cours de route.

## Question 2 — Un texte vide est refusé deux fois (par Pydantic puis par `predict()`), est-ce redondant ?

C'est une défense en profondeur : Pydantic valide le contrat au plus tôt, mais `predict()` peut être appelée directement (dans un test, ou depuis un autre script) sans passer par l'API. Les deux validations ne protègent pas la même porte d'entrée. En revanche, elles produisent **deux formes de 422 différentes** : une chaîne pour le refus par `predict()` (cas `{"text": "   "}`), une liste pour le refus par Pydantic (cas `{}` ou `{"text": 42}`). C'est un défaut à corriger (le TP4 le fera).
