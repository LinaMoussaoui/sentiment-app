# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Signaler automatiquement les ordonnances incomplètes (posologie absente, durée non précisée, médicament non adapté à l'âge) avant la délivrance.

## Utilisateur final (obligatoire)

Les pharmaciens et préparateurs en officine, qui saisissent l'ordonnance et doivent vérifier sa conformité avant de préparer les boîtes.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) Il existe très peu d'ordonnances annotées « incomplètes » en France, car les données de santé sont difficiles à obtenir : un modèle supervisé manquerait de matière. (b) Les règles de dispensation (posologies, contre-indications) sont publiées par l'ANSM et vérifiables une par une : un système RAG peut citer la source de chaque alerte. (d) Une erreur peut mettre un patient en danger, ce qui impose une validation humaine systématique.

## Données nécessaires et leur origine (obligatoire)

Base publique des interactions médicamenteuses (ANSM, Thésaurus des interactions) et référentiel des posologies pédiatriques, tous deux accessibles en open data.

## Métrique de succès et seuil d'acceptation (obligatoire)

Rappel ≥ 0,95 sur les ordonnances réellement incomplètes : on préfère dix fausses alertes à une seule ordonnance dangereuse manquée.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Toute alerte est relue par le pharmacien avant d'être communiquée au prescripteur ; le pharmacien peut marquer une alerte comme « non pertinente », ce qui alimente la base d'apprentissage.

## Risques éthiques ou de confidentialité (obligatoire)

Les ordonnances contiennent des données de santé sensibles (RGPD article 9) : hébergement interne certifié HDS, aucune requête vers un service tiers, journalisation des accès.

## Approche écartée et pourquoi (facultatif)

Règles par mots-clés seules : ne détectent pas les interactions entre deux médicaments prescrits ensemble, qui sont précisément la cause principale des erreurs.