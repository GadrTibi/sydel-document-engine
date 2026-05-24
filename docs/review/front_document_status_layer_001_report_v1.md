# Rapport FRONT-DOCUMENT-STATUS-LAYER-001

Date : 2026-05-24

## 1. Perimetre

Ce ticket ajoute la couche de statuts documentaires du futur front global dans
`front_data`. Elle reste independante de Streamlit et ne modifie ni l'UI visible,
ni les generateurs, ni le moteur DOCX/PDF/ZIP.

La couche consomme les `DocumentRequirementRecord`, les validations data-layer, le
flow dossier et les metadonnees utiles du catalogue existant.

## 2. Sources utilisees

- `docs/review/front_data_layer_001_report_v1.md`
- `docs/review/front_role_model_001_report_v1.md`
- `docs/review/front_address_model_001_report_v1.md`
- `docs/review/front_dossier_flow_001_report_v1.md`
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`
- `docs/project/GLOBAL_FRONT_RULES_V1.md`
- `docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv`
- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`
- `src/sydel_doc_engine/front_data/models.py`
- `src/sydel_doc_engine/front_data/canonical_mapping.py`
- `src/sydel_doc_engine/front_data/validation.py`
- `src/sydel_doc_engine/front_data/role_model.py`
- `src/sydel_doc_engine/front_data/address_model.py`
- `src/sydel_doc_engine/front_data/dossier_flow.py`
- `src/sydel_doc_engine/domain/case_catalog.py`
- `tests/unit/test_front_data_layer.py`
- `tests/unit/test_front_role_model.py`
- `tests/unit/test_front_address_model.py`
- `tests/unit/test_front_dossier_flow.py`

ADR applicables : ADR-0001 source de verite documentaire et ADR-0005 mode de
travail Codex/repo-first.

## 3. Objets crees

Module cree :

- `src/sydel_doc_engine/front_data/document_status.py`

Objets principaux :

- `DocumentStatusRecord`
- `DocumentLotStatusRecord`
- `DocumentStatusReason`
- `DocumentStatusSummary`

Enums ajoutes :

- `DocumentStatus`
- `DocumentLotStatus`
- `DocumentStatusReasonType`
- `DocumentStatusReasonSource`

Helpers exposes :

- `build_document_status(...)`
- `build_document_status_for_code(...)`
- `build_document_status_summary(...)`
- `build_document_lot_status(...)`
- helpers de diagnostic : raisons bloquantes, roles manquants, adresses
  manquantes, champs canoniques manquants, ambiguities non resolues.

## 4. Statuts documentaires retenus

Statuts documentaires :

- `expected`
- `generable`
- `manual_only`
- `not_implemented`
- `context_incomplete`
- `blocked_missing_data`
- `blocked_unresolved_ambiguity`
- `generable_with_reserve`

Regle de synthese :

- un document manuel reste visible mais n'est jamais pret a generer ;
- un document non implemente ou sans contexte exploitable est distingue d'un
  document manuel ;
- les donnees manquantes bloquent avant les ambiguities ;
- les ambiguities non resolues bloquent sauf quand elles sont explicitement
  classees non bloquantes, par exemple l'alias documentaire legacy de `DOC-002` ;
- une reserve documentaire n'empeche pas la generation technique, mais produit
  `generable_with_reserve`.

## 5. Statuts de lot retenus

Statuts de lot :

- `ready` : tous les documents du lot sont `generable` ;
- `partial` : au moins un document est manuel, reserve ou incomplet, sans blocage
  critique ;
- `blocked` : au moins un document critique est bloque par donnees manquantes ou
  ambiguite bloquante. Les documents incomplets, reserves, manuels ou non
  implementes rendent le lot `partial` tant qu'ils ne sont pas declares critiques.

Ce modele prepare l'ecran futur "Documents attendus" sans appeler les generateurs.

## 6. Calcul des raisons de blocage

Les raisons sont tracees par `DocumentStatusReason` avec :

- type de raison ;
- severite ;
- source (`document_requirement`, `validation`, `dossier_flow`, `catalog`,
  `reserve`) ;
- document ;
- bloc dossier si la raison vient du flow ;
- role, adresse, champ canonique ou ambiguity concernes ;
- action recommandee quand elle existe.

Sources de calcul :

- `validate_document_requirement(...)` pour roles, adresses, champs et ambiguities ;
- `validate_role_assignments(...)`, `validate_address_records(...)` et
  `validate_reuse_rules(...)` pour les incoherences pertinentes ;
- `build_dossier_flow(...)` pour rattacher les blocages aux blocs metier ;
- `case_catalog.py` pour `manual_only`, `not_implemented`, notes et reserves.

## 7. Couverture des sentinelles

| Document | Couverture status layer |
|---|---|
| `DOC-002` | Peut devenir `generable` quand siege, domiciliation, roles et champs sont presents ; l'alias legacy reste non bloquant. |
| `DOC-034` | Les blocages mandataire, ordre, adresse ordre, champs et pieces ordinales sont rattaches aux blocs ordre du flow. |
| `DOC-017` | Les dependances capital, associes, ordre et banque sont portees par raisons roles/champs/blocs. |
| `DOC-033` | Les dependances cedant, cessionnaire, SCM cedee, prix et adresses restent tracees. |
| `DOC-009` | Les raisons de blocage sont structurees par cession cabinet, bail, financement, origine et exercices. |
| `DOC-041` | Les dependances apport titres, societe cible, commissaire et evaluateur sont portees par blocs et ambiguities. |
| `DOC-025` | Les dependances SCM, associes, representant personne morale, banque et apports restent detectables. |

## 8. DOC-006 / DOC-013 / DOC-014

- `DOC-006` est modelisable en `generable_with_reserve` : generation technique
  possible, reserve source V2 conservee.
- `DOC-013` est `manual_only` via le catalogue.
- `DOC-014` est `manual_only` via le catalogue.
- Les documents manuels restent visibles mais ne sont jamais consideres prets pour
  generation.

## 9. Points encore ORANGE

- Les statuts s'appuient sur les exigences sentinelles et les metadonnees catalogue,
  mais pas encore sur un mapping exhaustif des 43 documents.
- Les statuts de lot restent simples : ils ne gerent pas encore les priorites
  metier fines, les documents-lots complexes ni les pieces justificatives.
- Le statut `blocked_unresolved_ambiguity` localise l'ambiguite ; il ne tranche pas
  les decisions produit/juridiques.
- Le mode document unitaire doit encore etre separe proprement du parcours dossier.

## 10. Prototype actuel

- Garde : references utiles de statut (`manual_only`, `context_incomplete`,
  reserves, documents visibles hors generation).
- Jette : logique de statut liee a l'UI ou au `session_state`.
- Migre : la distinction documents generables / manuels / reserves / incomplets.
- Diagnostic seul : le prototype Streamlit reste un bac a sable.

## 11. Tests

Tests ajoutes :

- `tests/unit/test_front_document_status_layer.py`

Validation cible executee pendant le ticket :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_document_status_layer.py`
  : OK, 9 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check src/sydel_doc_engine/front_data/document_status.py src/sydel_doc_engine/front_data/__init__.py tests/unit/test_front_document_status_layer.py`
  : OK.

Validation finale :

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 333 tests passes.

## 12. Prochaine etape recommandee

Lancer `FRONT-UNIT-DOCUMENT-MODE-001`.

Cette prochaine couche doit reconcevoir le mode document unitaire comme diagnostic
separe du parcours dossier complet, en s'appuyant sur les statuts documentaires
et sans coder le rebuild UI visible.
