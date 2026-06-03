# SELARL returns 006 PV 001 report V1

Date : 2026-06-02

Ticket : `SELARL-RETURNS-006-PV-001`

Source :

- `docs/review/selarl_human_returns_006_raw_v1.md`
- `docs/review/selarl_human_returns_triage_006_report_v1.md`

## Verdict

Verdict : `DONE`.

Le ticket est reste borne au `DOC-004` PV nomination gerant.

## Corrections appliquees

| Retour | Decision appliquee |
| --- | --- |
| Forme juridique sous la denomination | Le header du PV utilise la forme redigee quand elle existe. Pour SELARL, le rendu derive `Société d’exercice libéral à responsabilité limitée de {profession}` depuis la profession portee par les associes du contexte. |
| Supprimer l'acronyme en header | Le header ne rend plus `SELARL à capital variable` dans le cas SELARL corrige. |
| Capital haut de page | La ligne `Au capital minimum et effectif de ...` est remplacee par `Au capital de {capital_social}` avec suffixe `euros` si la valeur ne le contient pas deja. |

## Fichiers modifies

- `src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py`
- `tests/unit/test_pv_nomination_gerant.py`

## Validations

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_pv_nomination_gerant.py -q` : OK, 10 tests passes.
- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_single_document_mode.py tests/unit/test_business_wizard.py tests/unit/test_pv_nomination_gerant.py -q` : OK, 99 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check AGENTS.md docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md docs/project/PROJECT_CONTROL_TOWER_V1.md docs/project/PROJECT_AGENT_ORG_CHART_V1.md docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py tests/unit/test_pv_nomination_gerant.py` : OK.

## Suite

Prochain ticket recommande : `SELARL-RETURNS-006-PROCURATION-001`.
