# Semaine 5 : l'interface Streamlit

## Les essais (T29 à T33)

| Contrôle | Essai | Résultat |
|---|---|---|
| T29 | Ouvrir la page | « API prête : tfidf-logreg (TP2, models/sentiment.joblib) » |
| T30 | Avis positif | Avis positif, 78 % |
| T30 | Avis négatif | Avis négatif, 75 % |
| T31 | Texte inventé `xqzvb wlktpr grombu` | « Je ne sais pas : à faire vérifier par un humain », 52 %, encadré sur le seuil d'abstention |
| T32 | Trois espaces | « Texte refusé : vide, fait d'espaces, ou de plus de 2000 caractères » (422) |
| T32 | API arrêtée | « API injoignable : lancez d'abord uvicorn api.main:app » |
| T33 | Fichier `avis_exemple.csv` | Tableau de 6 avis, résumé `{INDETERMINE: 1, NEGATIVE: 2, POSITIVE: 3}`, téléchargement de `resultats.csv` |

## Question 1 — Pourquoi l'interface n'importe-t-elle jamais le modèle ?

L'interface est un client de l'API : elle envoie `POST /predict` et lit la réponse JSON, mais elle ne charge jamais `models/sentiment.joblib` ni `api/`. C'est la troisième règle d'architecture du guide : un modèle réentraîné, une API déplacée sur un autre serveur, ou un changement de modèle (TF-IDF → CamemBERT) ne demandent aucune modification de la page. L'interface reste stable, l'API évolue.

## Question 2 — Que montre-t-elle quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Quand la confiance est sous le seuil d'abstention (0.60), la page affiche « Je ne sais pas : à faire vérifier par un humain » avec un encadré bleu qui explique « La confiance est sous le seuil d'abstention : un humain doit trancher. » C'est mieux qu'un verdict forcé, car un faux POSITIVE sur un avis mitigé peut faire passer un client mécontent pour un client satisfait : l'abstention prévient l'erreur au lieu de la commettre.

## Question 3 — Que voit l'utilisateur quand l'API tombe ?

La page affiche un encadré rouge en haut : « API injoignable : lancez d'abord uvicorn api.main:app ». L'utilisateur n'a pas besoin de lire un code HTTP (503, 500, 422) : le client Python (`ui/client.py`) traduit chaque cas en message clair. La page ne fait que l'afficher.