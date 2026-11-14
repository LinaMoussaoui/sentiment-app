# Semaine 4 : tests approfondis et qualité, notes du binôme

> Une à deux pages. Uniquement des chiffres issus de VOS exécutions.

## 1. Couverture

- Avant (étape A) : **91 %**, lignes jamais exécutées : **49, 77-79, 85-87** dans `api/main.py`.
- Comportements non testés :
  - ligne 49 : réponse 503 quand le modèle n'est pas chargé (retiré en cours de route)
  - lignes 77-79 : réponse 500 quand le modèle plante (RuntimeError, ValueError)
  - lignes 85-87 : lancement direct de l'API (bloc `__main__`, jamais exécuté sous pytest)
- Après (étape D) : à compléter après T26.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| à compléter | à compléter | à compléter |

## 3. Seuil d'abstention

- Deux ou trois points de la courbe (`python src/courbe_seuil.py`) : à compléter après T24.
- Seuil retenu : à compléter ; part des avis envoyés à un humain : à compléter.
- Justification : à compléter.

## 4. Jeu d'or

- Bilan (`python src/bilan_jeu_or.py`) : à compléter après T25.
- Ce que ces chiffres disent du modèle : à compléter.

## 5. Outils statiques

- Remarques au départ : ruff **11 erreurs** (B904 ×2, I001 ×2, F401 ×2, B905 ×2, E741 ×3), mypy **0 erreur** (`Success: no issues found in 4 source files`).
- Parmi les défauts de la partie 2, ruff et mypy en avaient signalé : **0**. Conclusion : les outils statiques ne remplacent pas les tests. Ils détectent la forme (style, imports, typage) mais pas la sémantique (contrat d'entrée, gestion d'erreurs, uniformité des 422). Ils sont utiles en complément, pas en substitut.