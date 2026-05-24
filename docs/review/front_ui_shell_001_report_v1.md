# Rapport FRONT-UI-SHELL-001

Date : 2026-05-24

## 1. Perimetre

Ce ticket cree la premiere tranche visible du nouveau front global. Il ne modifie
ni les generateurs, ni le moteur DOCX/PDF/ZIP, ni le wording juridique, et ne code
pas encore l'editeur dossier complet.

Le prototype Streamlit reste present. Il est maintenant isole dans une zone
secondaire explicite : `Prototype / outils de test`.

## 2. Sources utilisees

- `docs/review/front_review_001_report_v1.md`
- `docs/project/FRONT_MIGRATION_MAP_V1.md`
- `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`
- `docs/review/front_data_layer_001_report_v1.md`
- `docs/review/front_role_model_001_report_v1.md`
- `docs/review/front_address_model_001_report_v1.md`
- `docs/review/front_dossier_flow_001_report_v1.md`
- `docs/review/front_document_status_layer_001_report_v1.md`
- `docs/review/front_unit_document_mode_001_report_v1.md`
- `docs/review/front_test_prefill_001_report_v1.md`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `src/sydel_doc_engine/app/business_wizard.py`
- `src/sydel_doc_engine/app/single_document_mode.py`
- `src/sydel_doc_engine/app/test_prefill_presets.py`
- `src/sydel_doc_engine/front_data/models.py`
- `src/sydel_doc_engine/front_data/dossier_flow.py`
- `src/sydel_doc_engine/front_data/document_status.py`
- `src/sydel_doc_engine/front_data/unit_document_mode.py`

## 3. Ce qui a ete cree visiblement

Le point d'entree Streamlit expose maintenant deux espaces :

- `Nouveau front global` : entree cible du rebuild UI.
- `Prototype / outils de test` : zone secondaire pour les parcours historiques et
  diagnostics.

Dans `Nouveau front global`, la navigation cible prepare quatre zones :

- `Accueil / selection`
- `Dossier`
- `Documents attendus`
- `Generation`

Ces zones sont volontairement read-only ou placeholder. Elles posent la structure
du futur front sans reconstruire le formulaire dossier.

## 4. Isolation du prototype

Les anciens parcours restent accessibles mais ne sont plus presentes comme front
final :

- `Assistant metier prototype` : bac a sable historique et smoke de comparaison.
- `Document unitaire` : outil de test separe du parcours dossier complet.
- `Technique / diagnostic` : outil de chargement YAML/JSON et verification moteur.

Le prefill de test, le mode unitaire et le diagnostic technique sont conserves.
Ils restent dans une zone secondaire, avec avertissement visible sur leur statut
de test/prototype.

## 5. Fondations exposees

Nouveau module :

- `src/sydel_doc_engine/app/front_shell.py`

Ce module fournit une couche de lecture UI pure, sans dependance Streamlit, pour :

- les items de navigation cible/prototype ;
- les etapes du `dossier_flow` ;
- les blocs actifs sur les documents sentinelles ;
- un apercu des statuts documentaires via `document_status`.

Le shell affiche notamment :

- les 10 etapes du flow dossier global ;
- les blocs actifs lisibles par etape ;
- un apercu documentaire sur `DOC-002`, `DOC-006`, `DOC-013`, `DOC-014` et
  `DOC-034` ;
- le statut de lot `partial` quand certains documents sont reserves ou manuels.

## 6. Ce qui n'est pas fait dans ce ticket

- Pas d'editeur dossier complet.
- Pas de nouvelle saisie de roles, adresses ou parties.
- Pas de reconstruction du wizard SELARL.
- Pas de branchement generation depuis le nouveau shell.
- Pas de suppression du prototype.
- Pas de modification des generateurs ou du moteur DOCX/PDF/ZIP.

## 7. Tests

Tests ajoutes ou adaptes :

- `tests/unit/test_front_ui_shell.py`
- `tests/unit/test_business_wizard.py`
- `tests/unit/test_single_document_mode.py`

Les tests couvrent :

- separation visible `Nouveau front global` / `Prototype / outils de test` ;
- presence des zones cible du shell ;
- presence de `Document unitaire` et `Technique / diagnostic` dans la zone test ;
- exposition des etapes `dossier_flow` ;
- exposition des statuts documentaires ;
- non-regression des prefills Assistant et du mode Document unitaire.

## 8. Points de vigilance

- `streamlit_app.py` reste volumineux : le shell isole l'entree produit, mais les
  anciennes fonctions prototype restent dans le meme fichier.
- Le panneau `Documents attendus` est encore un apercu read-only, pas la vue
  operationnelle finale.
- Le shell ne construit pas encore un `DossierRecord` depuis l'UI.
- La generation du nouveau front est volontairement non branchee tant que le
  panneau documents et l'editeur dossier ne sont pas disponibles.

## 9. Prochaine etape recommandee

Lancer `FRONT-DOSSIER-EDITOR-001`.

Ce prochain ticket doit construire un premier editeur dossier data-first adosse a
`DossierRecord`, `RoleAssignment`, `AddressRecord` et `dossier_flow`, sans
retomber dans les fusions implicites du prototype.
