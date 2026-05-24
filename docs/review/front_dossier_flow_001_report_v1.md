# Rapport FRONT-DOSSIER-FLOW-001

Date : 2026-05-24

## 1. Perimetre

Ce ticket ajoute la fondation du flow dossier du futur front global dans la couche
`front_data`. Il ne modifie ni l'UI visible, ni Streamlit, ni les generateurs, ni
le moteur DOCX/PDF/ZIP.

Le flow reste une couche metier/data : il decrit les etapes, les blocs activables,
les dependances, les pre-requis, les reutilisations possibles et les raisons de
blocage ou de warning pour la future UI.

## 2. Sources utilisees

- `docs/review/front_data_layer_001_report_v1.md`
- `docs/review/front_role_model_001_report_v1.md`
- `docs/review/front_address_model_001_report_v1.md`
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`
- `docs/project/GLOBAL_FRONT_RULES_V1.md`
- `docs/project/GLOBAL_FRONT_SCREEN_STRATEGY_V1.md`
- `docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv`
- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`
- `src/sydel_doc_engine/front_data/models.py`
- `src/sydel_doc_engine/front_data/canonical_mapping.py`
- `src/sydel_doc_engine/front_data/validation.py`
- `src/sydel_doc_engine/front_data/role_model.py`
- `src/sydel_doc_engine/front_data/address_model.py`
- `tests/unit/test_front_data_layer.py`
- `tests/unit/test_front_role_model.py`
- `tests/unit/test_front_address_model.py`

ADR applicables : ADR-0001 source de verite documentaire et ADR-0005 mode de
travail Codex/repo-first.

## 3. Objets et modules crees

Module cree :

- `src/sydel_doc_engine/front_data/dossier_flow.py`

Objets principaux :

- `DossierStep`
- `DossierBlock`
- `BlockActivationRule`
- `FlowDependency`
- `FlowStatus`
- `FlowValidationResult`
- `DossierFlow`

Helpers exposes :

- `build_dossier_flow(...)`
- `build_sentinel_dossier_flow(...)`
- `validate_dossier_flow(...)`
- `active_reuse_rules_for_flow(...)`

Les exports publics sont ajoutes a `src/sydel_doc_engine/front_data/__init__.py`.

## 4. Etapes du flow retenues

Le flow global retient 10 etapes ordonnees :

1. Qualification / type d'operation
2. Fiche client / personnes
3. Fiche societe
4. Roles et parties
5. Adresses
6. Capital / titres / apports
7. Ordre / inscription / pieces ordinales
8. Cession / apport / SCM / bail / financement
9. Documents attendus
10. Generation

Chaque etape porte ses dependances. Par exemple les roles dependent des fiches
personnes et societes, les operations consomment roles et adresses, et la
generation depend des documents attendus.

## 5. Blocs retenus

Blocs transverses :

- qualification dossier ;
- personnes physiques ;
- personnes morales ;
- assignments de roles ;
- adresses typees ;
- reutilisations d'adresses ;
- documents attendus ;
- readiness generation.

Blocs metier specialises :

- associes et repartitions ;
- capital et titres ;
- apports ;
- ordre et identifiants ordinaux ;
- mandataire / derogation ordre ;
- pieces ordinales ;
- cession cabinet ;
- prix de cession ;
- origine de propriete ;
- exercices financiers ;
- bail et locaux loues ;
- financement et banque ;
- SCM et cession de parts ;
- associes SCM et apports ;
- SPFPL et societe cible ;
- apport de titres.

Chaque bloc sait quels documents le concernent, quels roles/adresses/champs
canoniques il consomme, quelles reutilisations peuvent etre proposees, et quelles
ambiguities doivent rester visibles.

## 6. Cas orange mieux structures

| Document | Structuration ajoutee | Reste orange volontaire |
|---|---|---|
| `DOC-034` | Blocs `ordre_identifiants`, `ordre_mandataire`, `ordre_pieces` ; separation inscrit / societe inscrite / conseil de l'ordre / mandataire. | Parametrage ordre par inscrit, mandataire configurable, derogation manuelle. |
| `DOC-017` | Blocs capital associes, capital titres, ordre, financement/banque. | Pluralite d'associes, seuils de gerance, parametrage banque. |
| `DOC-009` | Blocs cession cabinet, prix, origine, exercices, bail, financement. | Origine de propriete libre, collection d'exercices, absence de deduction bailleur/locataire. |
| `DOC-041` | Blocs SPFPL, societe cible, apport de titres, commissaire/evaluateur. | Source evaluateur/commissaire, libelle commissaire, champs SPFPL encore incertains. |
| `DOC-025` | Blocs SCM, associes SCM, apports, banque et capital. | Alias legacy `personne_2.nb_parts`, cardinalite associes SCM, parts/apports par ligne. |

Les blocs localisent les zones orange sans inventer de raccourci metier. Les
warnings restent portes par `unresolved_ambiguity_keys`.

## 7. Documents attendus et validations

Le flow sait rattacher les documents sentinelles aux blocs qui les concernent.
Il peut indiquer :

- les documents concernes par bloc ;
- les roles requis ;
- les adresses typees requises ;
- les champs canoniques requis ;
- les reutilisations explicitement permises ;
- les valeurs manquantes bloquantes ;
- les ambiguities non resolues en warning.

La validation du flow reutilise les objets existants sans creer de donnees :
aucun role, aucune adresse et aucune regle de reutilisation ne sont inventes par
le flow.

## 8. Ce qui reste volontairement pour les tickets suivants

- Couche de statuts documentaires : generable, manuel, reserve, non pret,
  contexte incomplet et document-lot.
- Regles detaillees de readiness document par document.
- Mode document unitaire comme diagnostic separe.
- Prefills de test du nouveau front global.
- Calculs et ecrans fins capital/titres/apports.
- Parametrage ordre par profession/departement et pieces ordinales.
- Detail des clauses cession cabinet / bail / financement.

## 9. Prototype actuel

- Garde : bac a sable et outil de diagnostic.
- Jette : modele de navigation et `session_state` comme fondation produit.
- Migre : enseignements de diagnostic, separation dossier complet / document
  unitaire, besoin de prefill deterministe.
- Diagnostic seul : Streamlit actuel reste hors cible de ce ticket.

## 10. Tests

Tests ajoutes :

- `tests/unit/test_front_dossier_flow.py`

Validation cible executee pendant le ticket :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_dossier_flow.py`
  : OK, 11 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check src/sydel_doc_engine/front_data/dossier_flow.py tests/unit/test_front_dossier_flow.py src/sydel_doc_engine/front_data/__init__.py`
  : OK.

Validation finale :

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 324 tests passes.

## 11. Prochaine etape recommandee

Lancer `FRONT-DOCUMENT-STATUS-LAYER-001`.

Cette prochaine couche doit utiliser le flow dossier pour declarer les statuts
documentaires front : document attendu, manuel, reserve, non pret, generable,
document-lot et raisons precises de blocage, sans coder l'UI visible.
