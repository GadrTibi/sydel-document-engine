# Réunion 2026-06-09 — Rafael × Albane × David (boss Sydel) — extraction + routage

> Source : débrief IA de la réunion, transmis par Gad le 2026-06-09. Ce fichier = **lecture du
> Second** : extraction, classification (confirmé / direction / ouvert), et **routage** vers les docs
> canoniques. C'est la 1re **validation humaine** (Albane + David) du moteur.

## ✅ VALIDATION POSITIVE (milestone) → board
Albane + David **constatent que le moteur génère correctement** : documents, **logos**, variables,
**féminisation**, **pluralisation**, remplissage, personnalisation. Téléchargement **un par un** ET
**dossier ZIP** : déjà en place, confirmé. → C'est la 1re validation **fonctionnelle** humaine ;
la validation **juridique fine** reste en cours (clauses à revoir, ci-dessous).

## DÉCISIONS / DIRECTIONS (classées par niveau de confiance — règle 20)

| # | Point | Niveau | Routage |
| :- | :--- | :--- | :--- |
| 1 | **Multi-associés N (2/3/5+)** : listes dynamiques ; le générateur adapte statuts, procurations, PV, annexes. | **Confirmé** (étend mon flag « généraliser au-delà de 2 ») | board + roadmap dev |
| 2 | **Associé ≠ dirigeant** : distinguer **Associé / Président / DG / DG délégué** ; **case à cocher « dirigeant »** → champs complémentaires conditionnels (parents, DNC) **seulement si** dirigeant. | **Confirmé** (feature demandée) | board + roadmap dev |
| 3 | **Pas de mise à jour rétroactive** : produire les bons docs **à la création** ; ne pas re-modifier les dossiers historiques (réforme ordre 2025 = trop de formalités/coûts). | **Confirmé** (scope ; aligné V1=création) | journal décisions |
| 4 | **Professions réglementées** : socle commun + docs additionnels selon profession (médecin/dentiste : inscription ordre, autorisations). | **Confirmé** (déjà fait) | board (état) |
| 5 | **Architecture : modèle unique « intelligent »** (conditions + variables + arbres de décision) plutôt que N modèles séparés, pour la maintenance (1 loi change → 1 seul modèle). | **Direction / probable** (« l'équipe semble privilégier ») — partiellement notre approche (couche commune + conditionnels) | journal décisions (à confirmer) |
| 6 | **Base de données des personnes** : réutiliser les identités déjà saisies (éviter la sursaisie), PP + PM. | **Souhait / feature à scoper** | roadmap dev (change-intent) |

## JURIDIQUE À CORRIGER → paquet Rafael (en attente de ses cas concrets)
Le résumé est **vague** (« certaines formulations imprécises ») → **inactionnable sans les cas précis**.
Points cités, à faire remonter par Rafael avec exemples : **mentions d'intérêts de retard** · **clauses de
cession** · **désignation des dirigeants** · **informations parentales** (déclaration non-condamnation) ·
variables mal injectées. → Rafael doit fournir les **dossiers/cas concrets** (son action item).

## ACTIONS DÉCIDÉES
- **Rafael (métier)** : tester la génération **multi-associés**, créer des **cas concrets**, remonter les
  **erreurs juridiques** + clauses à corriger + variables problématiques.
- **Nous (dev)** : gestion **multi-associés N** ; **désignation dirigeants** (Président/DG/DG délégué) ;
  revoir les variables signalées ; poursuivre la logique **modèle unique dynamique** (conditions/arbres).

## MÉTHODO confirmée (alignée avec notre INTEL GATE)
« Les devs ne peuvent pas deviner les règles métier » → besoin : modèles + règles + cas + **arbres de
décision** des juristes. Logique : tronc commun → variantes → conditions/règles → génération
(« dominos »). → C'est exactement notre démarche (extract-from-models + canon + conditionnels). Les
arbres de décision vivent déjà dans `07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1`, `08_DICTIONNAIRE_VARIABLES`,
`09_TABLE_MAPPING_DOCUMENTS_VARIABLES`.

## NOTE GOUVERNANCE
Débrief = **résumé IA de 2e main** : les décisions « confirmé » sont fiables (direction claire) ; le
« modèle unique » est une **inclination** à confirmer ; le juridique est **ouvert** (attendre les cas
Rafael). Ne rien **construire à l'aveugle** sur le vague ; scoper dirigeants + multi-N (constructibles)
avant build.
