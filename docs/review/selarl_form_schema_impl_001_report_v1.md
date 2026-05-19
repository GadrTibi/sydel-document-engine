# Rapport SELARL-FORM-SCHEMA-IMPL-001

## Source et périmètre

- Source V2 relue : `project/source_truth/Documents_a_generer_par_cas_V2.docx`.
- Hash V2 déjà vérifié dans le ticket précédent : `2E9843AA1EC05A01D82DF5FCE12516A8EF49EA2B3842547D186204218C90B23F`.
- Périmètre respecté : schéma de données SELARL côté Assistant métier, sans refonte Streamlit, sans modification des générateurs, du moteur DOCX/PDF/ZIP ni du mode Technique / diagnostic.

## Fichiers modifiés

- `src/sydel_doc_engine/domain/case_catalog.py`
- `src/sydel_doc_engine/app/selarl_form_schema.py`
- `tests/unit/test_case_catalog.py`
- `tests/unit/test_selarl_form_schema.py`
- `docs/review/selarl_source_verify_001_report_v1.md`
- `docs/review/selarl_form_schema_impl_001_report_v1.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/04_LAST_STATE.md`

## Corrections QA traitées

- `DOC-006` / `lettre_avertissement_conjoint` porte désormais une note catalogue exploitable par l'UI : la vraie V2 indique que le document ne figure pas parmi les sources fournies ; la génération moteur existante doit donc être affichée avec réserve dans le pilote SELARL.
- Le rapport `selarl_source_verify_001_report_v1.md` précise que la colonne `Statut actuel` décrit l'état avant correction et que `DOC-013` / `DOC-014` sont finaux `MANUAL_ONLY`, visibles mais exclus des codes générables SELARL.

## Structure schéma créée

Le nouveau module `src/sydel_doc_engine/app/selarl_form_schema.py` expose des dataclasses et constantes machine-readable :

- blocs métier ;
- champs UI, labels, variables alimentées, obligations et conditions ;
- règles de réutilisation ;
- documents SELARL attendus avec statut, condition, variables connues et notes de réserve ;
- fonctions de projection depuis le catalogue (`selarl_expected_documents`, `selarl_generable_document_codes`) ;
- couverture des variables V2 (`all_selarl_v2_variables`, `selarl_variable_coverage`) ;
- validation interne (`validate_selarl_schema`).

## Blocs métier

Blocs représentés : Qualification du dossier, Société, Siège social, Professionnel / gérant, Ordre professionnel, Associés, Mandataire / signataire, Régime matrimonial / conjoint, Cession de cabinet, Bail, SCM, Banque / financement, Signature.

## Règles de réutilisation

Règles implémentées : le signataire est le premier associé ; le gérant est le professionnel principal ; le signataire est le professionnel principal ; le mandataire est le signataire ; la SELARL en création est l'acquéreur ; la SELARL en création est la cessionnaire des parts SCM ; l'adresse de domiciliation est le siège social.

Chaque règle indique source, cible, effet attendu, champs alimentés/verrouillés et condition d'activation.

## Traitement DOC-006 / DOC-013 / DOC-014

- `DOC-006` reste `GENERATABLE` côté moteur/catalogue, mais avec réserve source V2 explicite.
- `DOC-013` est visible dans les documents attendus si `derogation = oui`, mais reste `MANUAL_ONLY` et absent des codes générables SELARL.
- `DOC-014` est visible dans les documents attendus si `derogation = oui`, mais reste `MANUAL_ONLY` et absent des codes générables SELARL.

## Couverture des variables V2

Le module conserve les variables brutes V2 par document dans `SELARL_V2_VARIABLES_BY_DOCUMENT`.

La fonction `selarl_variable_coverage()` garantit qu'une variable V2 du pilote SELARL est toujours :

- mappée à un champ UI ;
- ou dérivée par une règle de réutilisation ;
- ou explicitement marquée `to_arbitrate` pour éviter toute perte silencieuse avant le ticket document par document.

Les variables critiques d'adresse, d'identité, de société, d'ordre, de banque, de bail, de cession et de SCM sont testées comme mappées ou dérivées, pas seulement listées.

## Tests lancés

- `.\.venv\Scripts\python.exe -m ruff check .`
- `.\.venv\Scripts\python.exe -m pytest`

Résultats :

- Ruff : OK, `All checks passed!`
- Pytest : OK, 231 tests passés.

## Prochaine étape recommandée

Ouvrir `SELARL-UI-WIZARD-IMPL-001` pour brancher l'Assistant métier visible sur ce schéma SELARL, en conservant les documents manuels visibles mais exclus de la génération et en maintenant le mode SCI existant.
