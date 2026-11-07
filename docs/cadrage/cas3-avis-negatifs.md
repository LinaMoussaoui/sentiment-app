# Fiche de cadrage : Avis clients négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Détecter automatiquement les avis clients négatifs (mécontents, produits défectueux, service défaillant) pour les remonter à l'équipe qualité sous 24 heures.

## Utilisateur final (obligatoire)

L'équipe qualité produit, qui reçoit une liste triée des avis les plus urgents au lieu de parcourir des milliers de commentaires.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) Les avis sont naturellement étiquetés par leur note (1 ou 2 étoiles = négatif), ce qui fournit un jeu d'entraînement abondant et gratuit. (c) Le volume atteint plusieurs milliers d'avis par jour : un classifieur léger reste très bon marché, un appel LLM par avis exploserait le budget. (d) La conséquence d'une erreur est modérée : un avis raté est rattrapé par le tri manuel hebdomadaire.

## Données nécessaires et leur origine (obligatoire)

Avis publics collectés sur Trustpilot et Google Reviews, avec la note associée, plus un export interne des avis du site e-commerce.

## Métrique de succès et seuil d'acceptation (obligatoire)

F1 macro ≥ 0,88 sur un jeu de test tenu à l'écart ; rappel ≥ 0,90 sur la classe « négatif », pour ne pas laisser passer les signaux faibles.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un avis mal classé est signalé par l'utilisateur ou rattrapé par la revue hebdomadaire ; l'équipe qualité peut corriger manuellement la prédiction.

## Risques éthiques ou de confidentialité (obligatoire)

Les avis publics restent pseudonymes : ne pas tenter de ré-identifier les auteurs, et ne pas exposer les noms d'utilisateurs dans les tableaux de bord internes.

## Approche écartée et pourquoi (facultatif)

Règles basées sur la note seule : insuffisantes car un avis à 5 étoiles peut contenir une critique (« 5 étoiles mais livraison en retard »).
