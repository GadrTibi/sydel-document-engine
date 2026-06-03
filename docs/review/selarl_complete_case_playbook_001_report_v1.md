# Rapport SELARL-COMPLETE-CASE-PLAYBOOK-001

Date : 2026-05-25

## Verdict

Le cas SELARL ne doit plus etre traite comme un test a quatre documents.
Le moteur contient deja la plupart des generateurs utiles, mais le nouveau
front global reste limite volontairement a `DOC-001`, `DOC-002`, `DOC-003` et
`DOC-004`.

Le prochain travail utile n'est donc pas de modifier les generateurs. Il faut
d'abord brancher un adaptateur de contexte SELARL complet cote front.

## Etat reel actuel

### Generable depuis le nouveau front

Depuis la surface principale actuelle :

- `DOC-001` declaration non-condamnation ;
- `DOC-002` autorisation domiciliation ;
- `DOC-003` procuration ;
- `DOC-004` PV nomination gerant.

Les actions DOCX et ZIP sont branchees sur ce perimetre. Le PDF reste
conditionne par le backend local.

### Disponible cote moteur, mais non branche en generation front SELARL

- `DOC-005` lettre de renonciation associe ;
- `DOC-006` lettre avertissement conjoint, avec reserve source SELARL ;
- `DOC-007` avenant contrat de bail ;
- `DOC-008` appel de fonds SEL ;
- `DOC-009` acte de cession cabinet medical ;
- `DOC-010` compromis de cession cabinet medical ;
- `DOC-011` acte de cession cabinet dentaire ;
- `DOC-012` compromis de cession cabinet dentaire ;
- `DOC-016` statuts SELARL chirurgien-dentiste ;
- `DOC-017` statuts SELARL medecin ;
- `DOC-031` PV AGE cession part SCM ;
- `DOC-032` courrier SDE cession SCM ;
- `DOC-033` acte de cession parts SCM vers SELARL ;
- `DOC-034` demande inscription ordre.

### A maintenir hors generation automatique SELARL

- formulaire site distinct CD94 sans code moteur ;
- `DOC-013` formulaire multi-sites SEL ;
- derogation SEL BNC sans code moteur ;
- `DOC-014` demande derogation cumul SELARL BNC.

`DOC-013` et `DOC-014` existent cote moteur, mais la source SELARL verifiee les
classe comme manuels pour le pilote SELARL. Ils ne doivent donc pas etre
reactives par simple opportunisme technique.

## Cause de l'ecart utilisateur

Le front a trois plafonds explicites :

- `FRONT_GENERATION_SUPPORTED_DOC_CODES` limite a `DOC-001` a `DOC-004` ;
- `UNIT_DOCUMENT_V1_SUPPORTED_CODES` limite a `DOC-001` a `DOC-004` ;
- `BUSINESS_WIZARD_CONTEXT_READY_DOCUMENT_IDS` limite a `DOC-001` a `DOC-004`.

Cela explique le ressenti : le produit affiche une SELARL de test, pas encore
une SELARL complete.

## Livrable cree

- `docs/project/SELARL_COMPLETE_CASE_PLAYBOOK_V1.md`

Le document contient :

- definition de la SELARL complete ;
- matrice des documents SELARL ;
- garde-fous documentaires ;
- cible UX minimale ;
- prochain ticket unique ;
- mode d'emploi reproductible pour les autres cas.

## Prochain ticket recommande

`SELARL-COMPLETE-CONTEXT-ADAPTER-001`

Objectif : brancher dans le nouveau front une selection documentaire SELARL
conditionnelle et un `DocumentGenerationContext` complet pour les documents
deja autorises et generables, sans toucher aux generateurs ni au moteur
DOCX/PDF/ZIP.

Ce ticket doit produire les tests de selection/readiness/contexte avant toute
modification visuelle ambitieuse.

## Tests

Aucun test Python lance : ce ticket ne modifie que la documentation et le
pilotage.

