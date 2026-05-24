# Rapport FRONT-UNIT-DOCUMENT-MODE-001

Date : 2026-05-24

## 1. Perimetre

Ce ticket ajoute la fondation du mode de test "Document unitaire" sur la nouvelle
couche `front_data`, sans modifier les generateurs, le moteur DOCX/PDF/ZIP ni le
wording juridique.

Le mode existant dans Streamlit reste un adaptateur de test. Sa selection, ses
statuts et ses exigences s'appuient maintenant sur la couche data unitaire au lieu
de porter seuls la logique documentaire.

## 2. Sources utilisees

- `docs/review/front_data_layer_001_report_v1.md`
- `docs/review/front_role_model_001_report_v1.md`
- `docs/review/front_address_model_001_report_v1.md`
- `docs/review/front_dossier_flow_001_report_v1.md`
- `docs/review/front_document_status_layer_001_report_v1.md`
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_RULES_V1.md`
- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`
- `docs/delivery/lot_01_analysis_and_specs_v1.md`
- `src/sydel_doc_engine/front_data/models.py`
- `src/sydel_doc_engine/front_data/canonical_mapping.py`
- `src/sydel_doc_engine/front_data/validation.py`
- `src/sydel_doc_engine/front_data/dossier_flow.py`
- `src/sydel_doc_engine/front_data/document_status.py`
- `src/sydel_doc_engine/registry/catalog.py`
- `src/sydel_doc_engine/app/single_document_mode.py`
- `src/sydel_doc_engine/app/streamlit_app.py`

ADR applicables : ADR-0001 source de verite documentaire, ADR-0002 moteur par
document canonique, ADR-0005 mode de travail Codex/repo-first.

## 3. Perimetre V1 retenu

Documents supportes en generation unitaire V1 :

- `DOC-001` - Declaration sur l'honneur de non-condamnation
- `DOC-002` - Autorisation de domiciliation
- `DOC-003` - Procuration
- `DOC-004` - PV nomination gerant

Documents visibles mais non ouverts a la generation unitaire V1 :

- `DOC-006` - visible avec reserve documentaire V2 ;
- `DOC-013` - manuel uniquement ;
- `DOC-014` - manuel uniquement ;
- `DOC-033` - hors perimetre V1, car cession SCM encore trop structuree pour ce
  mode prudent ;
- `DOC-034` - hors perimetre V1, car ordre / mandataire / derogation / pieces
  ordinales restent orange.

`DOC-033` et `DOC-034` ne sont pas generalises depuis les checks sentinelles :
leur couverture data existe, mais le mode unitaire V1 ne doit pas inventer un
formulaire local incomplet.

## 4. Architecture retenue

Module cree :

- `src/sydel_doc_engine/front_data/unit_document_mode.py`

Objets principaux :

- `UnitDocumentScopeStatus`
- `UnitDocumentPlan`
- `UnitDocumentPreparation`

Le module expose :

- les codes supportes V1 ;
- les exigences `DocumentRequirementRecord` de `DOC-001` a `DOC-004` ;
- les exclusions explicites V1 ;
- le calcul d'un plan unitaire depuis `DocumentStatusRecord` ;
- les exigences lisibles : roles, adresses typees, champs canoniques ;
- la preparation de generation unitaire sans dependance Streamlit.

## 5. Reutilisation de la nouvelle couche data

La fondation reutilise :

- `DocumentRequirementRecord` pour decrire les exigences ;
- `DocumentStatusRecord` pour distinguer generable, manuel, reserve, incomplet et
  hors generation ;
- `DossierFlow` pour rattacher les validations aux blocs quand un dossier est
  fourni ;
- `validate_document_requirement` indirectement via la couche status ;
- les roles et adresses typees de `front_data.models` ;
- le catalogue metier pour `manual_only`, `not_implemented` et reserves.

Le module `app/single_document_mode.py` reste responsable de l'adaptation vers le
contexte moteur existant et la generation DOCX. Il construit aussi un
`DossierRecord` minimal pour verifier la readiness front_data avant d'activer la
generation.

## 6. Integration UI minimale

`src/sydel_doc_engine/app/streamlit_app.py` conserve les trois modes existants :

- Assistant metier ;
- Document unitaire ;
- Technique / diagnostic.

Le mode "Document unitaire" affiche maintenant les exigences data-layer du
document selectionne et bloque le bouton DOCX si la couche data ne considere pas
le document pret.

Il ne cree pas de parcours dossier global et ne modifie pas les modes Assistant
metier ou Technique / diagnostic.

## 7. Ce qui reste a faire

- Elargir le mode unitaire au-dela de `DOC-001` a `DOC-004` seulement apres
  couverture data document par document.
- Stabiliser une representation plus complete des inputs unitaires sans copier le
  futur rebuild UI.
- Ajouter des prefills de test determines par la nouvelle couche front, sans les
  confondre avec des donnees metier reelles.
- Traiter plus tard `DOC-033` et `DOC-034` dans des tickets dedies si le besoin
  de test unitaire est confirme.

## 8. Tests

Tests ajoutes :

- `tests/unit/test_front_unit_document_mode.py`

Validations cible executees pendant le ticket :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_unit_document_mode.py -q`
  : OK, 11 tests passes.
- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_unit_document_mode.py tests/unit/test_single_document_mode.py -q`
  : OK, 19 tests passes.
- Ruff cible : OK apres correction automatique d'ordre d'import.

Validation finale :

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 344 tests passes.

## 9. Prochaine etape recommandee

Lancer `FRONT-TEST-PREFILL-001`.

Ce ticket doit ajouter des scenarios fictifs et deterministes pour tester le futur
front global et le mode unitaire sans promouvoir les donnees du prototype comme
source metier.
