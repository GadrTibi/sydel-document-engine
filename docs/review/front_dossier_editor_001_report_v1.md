# Rapport FRONT-DOSSIER-EDITOR-001

Date : 2026-05-24

## 1. Perimetre

Ce ticket ajoute la premiere tranche visible de l'editeur dossier du nouveau front
global. Il ne modifie ni les generateurs, ni le moteur DOCX/PDF/ZIP, ni le
wording juridique, et ne reconstruit pas le wizard historique.

Le prototype Streamlit reste disponible dans `Prototype / outils de test`.

## 2. Sources utilisees

- `docs/review/front_ui_shell_001_report_v1.md`
- `docs/review/front_data_layer_001_report_v1.md`
- `docs/review/front_role_model_001_report_v1.md`
- `docs/review/front_address_model_001_report_v1.md`
- `docs/review/front_dossier_flow_001_report_v1.md`
- `docs/review/front_document_status_layer_001_report_v1.md`
- `docs/review/front_unit_document_mode_001_report_v1.md`
- `docs/review/front_test_prefill_001_report_v1.md`
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`
- `docs/project/GLOBAL_FRONT_RULES_V1.md`
- `docs/project/GLOBAL_FRONT_SCREEN_STRATEGY_V1.md`
- `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `src/sydel_doc_engine/app/front_shell.py`
- `src/sydel_doc_engine/front_data/models.py`
- `src/sydel_doc_engine/front_data/dossier_flow.py`
- `src/sydel_doc_engine/front_data/document_status.py`
- `src/sydel_doc_engine/front_data/unit_document_mode.py`

ADR applicables : ADR-0001 source de verite documentaire, ADR-0002 moteur par
document canonique et ADR-0005 mode de travail Codex/repo-first.

## 3. Ce qui a ete implemente visiblement

Nouveau module :

- `src/sydel_doc_engine/app/front_dossier_editor.py`

La zone `Nouveau front global > Dossier` affiche maintenant :

- un selecteur `Type de dossier / structure de base` ;
- une synthese du dossier selectionne ;
- les etapes du flow dossier ;
- les blocs actifs ;
- les exigences principales par document ;
- les documents attendus et leurs statuts ;
- le statut de lot avec la legende `ready`, `partial`, `blocked`.

Profils V1 exposes :

- `SELARL creation simple`
- `SELARL ordre / inscription`
- `SELARL cession cabinet + bail + financement`
- `SCM cession de parts`
- `SPFPL apport de titres`

Ces profils sont prudents : ils servent a afficher les zones du futur editeur et
les blocages data-layer, pas a inventer une saisie complete.

## 4. Ce qui reste placeholder

- Pas de saisie effective des personnes, societes, roles, adresses ou valeurs
  canoniques dans le nouveau front.
- Pas d'activation d'overrides depuis l'UI.
- Pas de generation DOCX/PDF/ZIP depuis le nouveau front.
- Pas de migration massive du vieux `session_state`.
- Pas de reconstruction du wizard SELARL historique.

La vue est volontairement une premiere tranche de pilotage : elle rend visibles
les manques avant de construire les composants de saisie.

## 5. Consommation des fondations

`front_dossier_editor.py` construit un `DossierRecord` minimal par profil, ajoute
les `OperationContext` et `DocumentRequirementRecord`, puis consomme :

- `DossierRecord` pour representer l'enveloppe dossier ;
- `build_dossier_flow(...)` pour les etapes, blocs, dependances et validations ;
- `build_document_status_summary(...)` pour les statuts documentaires et le lot ;
- `unit_document_requirement(...)` pour reutiliser les exigences unitaires et
  sentinelles deja stabilisees.

Streamlit ne porte pas la logique metier : il affiche les lignes preparees par le
module d'adaptation.

## 6. Impact prototype

- `Assistant metier prototype` reste dans la zone secondaire.
- `Document unitaire` reste un outil de test separe.
- `Technique / diagnostic` reste accessible.
- Aucun prefill, generateur ou backend documentaire n'a ete modifie.

## 7. Tests

Tests ajoutes :

- `tests/unit/test_front_dossier_editor.py`

Couverture :

- construction d'un `DossierRecord` minimal depuis un profil ;
- exposition des etapes et blocs actifs ;
- exposition des exigences, statuts documents et statuts de lot ;
- absence de dependance Streamlit dans le module d'adaptation ;
- rendu AppTest de la zone `Dossier` ;
- non-regression de la zone prototype.

Validation cible executee pendant le ticket :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_dossier_editor.py tests/unit/test_front_ui_shell.py -q`
  : OK, 12 tests passes.

Validation finale :

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 364 tests passes.

## 8. Points ouverts

- L'editeur ne saisit pas encore les valeurs : il expose les exigences et les
  blocages.
- Le panneau `Documents attendus` du shell reste a extraire en composant cible
  complet.
- Les profils ne remplacent pas les futurs parcours de saisie.
- Les cas orange restent volontairement localises, pas resolus artificiellement.

## 9. Prochaine etape recommandee

Lancer `FRONT-DOCUMENTS-PANEL-001`.

Ce prochain ticket doit transformer la vue read-only des documents attendus en un
panneau operationnel du nouveau front : statuts, raisons de blocage, reserves,
documents manuels, lot documentaire et actions preparatoires, toujours sans
toucher aux generateurs ni au moteur DOCX/PDF/ZIP.
