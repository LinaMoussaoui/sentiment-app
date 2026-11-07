# Fiche de cadrage : Litiges de règlement

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Classer automatiquement les réclamations clients liées au règlement (remboursement, échéancier, impayé) pour les router vers le bon service.

## Utilisateur final (obligatoire)

Les gestionnaires du service clientèle, qui traitent les réclamations et doivent les orienter en moins de deux heures.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) Le service client conserve deux ans de réclamations étiquetées par catégorie de litige, ce qui fournit un jeu d'entraînement solide. (b) Les décisions doivent être auditables pour la conformité, et un modèle de régression logistique permet de justifier chaque prédiction par les mots-clés détectés. (c) Le volume quotidien est de plusieurs milliers de réclamations : un classifieur coûte quelques microsecondes par requête, un LLM serait hors budget.

## Données nécessaires et leur origine (obligatoire)

Export anonymisé des tickets (texte de la réclamation et catégorie attribuée) sur deux ans, fourni par l'outil de ticketing interne après pseudonymisation.

## Métrique de succès et seuil d'acceptation (obligatoire)

F1 macro ≥ 0,85 sur un jeu de test tenu à l'écart ; rappel ≥ 0,90 sur la classe « impayé », car c'est la plus urgente à traiter.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

L'agent peut réassigner un ticket mal classé en un clic ; chaque réassignation est journalisée et alimente le prochain réentraînement.

## Risques éthiques ou de confidentialité (obligatoire)

Les réclamations contiennent des données financières personnelles : pseudonymisation avant stockage, chiffrement au repos, accès limité aux agents habilités.

## Approche écartée et pourquoi (facultatif)

Modèle génératif seul : coût par requête prohibitif au volume attendu, et difficile à auditer pour la conformité.
