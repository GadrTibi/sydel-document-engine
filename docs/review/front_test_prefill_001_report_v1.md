# Rapport FRONT-TEST-PREFILL-001

Date : 2026-05-24

## 1. Perimetre

Ce ticket realigne le pre-remplissage de test du mode `Assistant metier` sur la
nouvelle couche `front_data`, sans modifier les generateurs, le moteur
DOCX/PDF/ZIP, le wording juridique, le mode `Technique / diagnostic` ni le mode
`Document unitaire`.

L'objectif n'est pas de creer un second systeme de prefill : l'adaptateur
Streamlit existant est conserve et devient testable contre les objets data.

## 2. Sources utilisees

- `docs/review/front_data_layer_001_report_v1.md`
- `docs/review/front_role_model_001_report_v1.md`
- `docs/review/front_address_model_001_report_v1.md`
- `docs/review/front_dossier_flow_001_report_v1.md`
- `docs/review/front_document_status_layer_001_report_v1.md`
- `docs/review/front_unit_document_mode_001_report_v1.md`
- `src/sydel_doc_engine/front_data/models.py`
- `src/sydel_doc_engine/front_data/canonical_mapping.py`
- `src/sydel_doc_engine/front_data/validation.py`
- `src/sydel_doc_engine/front_data/dossier_flow.py`
- `src/sydel_doc_engine/front_data/document_status.py`
- `src/sydel_doc_engine/front_data/unit_document_mode.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `src/sydel_doc_engine/app/test_prefill_presets.py`
- tests existants `test_business_wizard.py` et `test_front_unit_document_mode.py`

ADR applicables : ADR-0001 source de verite documentaire, ADR-0002 moteur par
document canonique et ADR-0005 mode de travail Codex/repo-first.

## 3. Audit de l'existant

Deja present :

- module `src/sydel_doc_engine/app/test_prefill_presets.py` ;
- selecteur `Scenario de test` dans `Assistant metier` ;
- boutons `Preremplir` et `Reinitialiser` ;
- message visible `Mode test - donnees fictives preremplies` ;
- quatre scenarios deterministes ;
- synchronisation UI des champs derives SELARL par le rendu Streamlit :
  dossier unipersonnel, associe unique, gerant/signataire et domiciliation.

Encore prototype avant ce ticket :

- les presets etaient des valeurs de widgets Streamlit ;
- aucune structure front_data ne decrivait les attentes de scenario ;
- les tests validaient surtout le comportement visible et le wizard historique ;
- la conversion `session_state -> BusinessWizardInput -> front_data` n'etait pas
  exposee comme chemin reutilisable.

## 4. Ce qui est conserve

- Les quatre scenarios et leurs donnees fictives.
- L'emplacement UI dans `Assistant metier`.
- Les boutons existants.
- Le mecanisme de remplissage du `session_state`.
- La separation avec `Technique / diagnostic`.
- Le mode `Document unitaire`, non complique dans ce ticket.

## 5. Ce qui est refactore

Ajouts cote `front_data` :

- `src/sydel_doc_engine/front_data/test_prefill_presets.py`
- `FrontDataTestPrefillProfile`
- profils de scenarios avec roles, adresses typees, operations, documents
  generables, reserves, manuels et orange.

Ajouts cote adaptateur Assistant :

- conversion pure d'un scenario vers `BusinessWizardInput` ;
- construction d'un `DossierRecord` front_data depuis le scenario ;
- synthese `DocumentStatusSummary` par document, isolee pour eviter qu'un
  document orange contamine les statuts de `DOC-001` a `DOC-004` ;
- liste de reset elargie aux widgets derives des associes SELARL.

## 6. Scenarios disponibles

| Scenario | Usage |
|---|---|
| `SELARL medecin unipersonnelle simple` | Cas heureux. `DOC-001` a `DOC-004` sont generables dans le wizard et dans la synthese front_data. |
| `SELARL chirurgien-dentiste + regime communautaire + site distinct` | Active regime communautaire, site distinct et derogation ; `DOC-006` garde sa reserve et `DOC-013` / `DOC-014` restent manuels. |
| `SELARL medecin + cession cabinet medical + bail + financement` | Active les blocs cession, bail, banque, financement et emprunt. `DOC-009` reste orange/non generable dans front_data, sans resolution artificielle. |
| `SCI simple` | Non-regression du parcours historique SCI. Le wizard genere `DOC-001` a `DOC-004`; la couche front_data signale que `DOC-002` garde une exigence unit/Selarl de role `praticien`. |

Toutes les donnees restent fictives et deterministes.

## 7. Synchronisation session_state

Le bouton `Preremplir` conserve le comportement existant :

- purge de l'etat Assistant ;
- pose du type de dossier ;
- injection des valeurs de widgets du scenario ;
- activation du flag `business_prefill_loaded` ;
- affichage du message de mode test.

Le rendu Assistant continue de deriver les champs verrouilles au prochain run :

- associe unique depuis le praticien ;
- gerant et signataire depuis le praticien en dossier unipersonnel ;
- domiciliation depuis le siege social si l'option explicite est active.

La liste des cles a purger couvre maintenant aussi les champs derives
`selarl_associe_*` afin d'eviter les residus apres `Reinitialiser`.

## 8. Limites connues

- Le prefill ne devient pas une source metier ; il reste un outil de test.
- `DOC-009` est volontairement non resolu completement : il localise les blocs
  cession/bail/financement mais ne tranche pas les points orange de rebuild.
- Le scenario SCI reste compatible avec l'ancien Assistant ; son alignement
  front_data complet demandera un modele futur hors SELARL pour `DOC-002`.
- Le mode `Document unitaire` pourra reutiliser ces profils plus tard, mais il
  n'est pas modifie ici.

## 9. Tests

Tests ajoutes :

- `tests/unit/test_front_prefill_mode.py`

Validations cible executees pendant le ticket :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_prefill_mode.py -q`
  : OK, 8 tests passes.
- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_business_wizard.py tests/unit/test_front_unit_document_mode.py -q`
  : OK, 52 tests passes.

Validation finale :

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 352 tests passes.

## 10. Prochaine etape recommandee

Lancer `FRONT-REVIEW-001`.

Le prefill de test etant consolide, le modele front global peut passer en revue
produit/juriste avant tout rebuild visible plus large.
