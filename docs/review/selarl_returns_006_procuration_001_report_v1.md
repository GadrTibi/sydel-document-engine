# SELARL returns 006 procuration 001 report V1

Date : 2026-06-02

Ticket : `SELARL-RETURNS-006-PROCURATION-001`

Sources :

- `docs/review/selarl_human_returns_006_raw_v1.md`
- `docs/review/selarl_human_returns_triage_006_report_v1.md`

## Verdict

Verdict : `DONE`.

Le ticket est reste borne au `DOC-003` procuration.

## Corrections appliquees

| Retour | Decision appliquee |
| --- | --- |
| Phrase introductive | La phrase rend maintenant `demeurant au ..., agissant en qualite...` sur la meme phrase, avec `agissant` en minuscule et une virgule apres l'adresse personnelle. |
| Denomination societe | La phrase rend `de la {designation societe}` pour coller au retour humain, tout en conservant la protection existante contre `SELARL SELARL ...`. |
| Siege social | La phrase rend `dont le siege est situe {adresse siege}` sans ajouter `au` avant l'adresse, conformement au retour. |
| Adresses dans cette procuration | Les adresses personnelles et siege rendent le code postal avant la ville : `{num voie} {voie}, {cp} {ville}`. |

## Fichiers modifies

- `src/sydel_doc_engine/generators/lot_01/procuration.py`
- `tests/unit/test_procuration.py`

## Validations

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_procuration.py -q` : OK, 9 tests passes.
- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_single_document_mode.py tests/unit/test_business_wizard.py tests/unit/test_procuration.py -q` : OK, 98 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check src/sydel_doc_engine/generators/lot_01/procuration.py tests/unit/test_procuration.py docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md docs/project/PROJECT_CONTROL_TOWER_V1.md docs/project/PROJECT_AGENT_ORG_CHART_V1.md docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md AGENTS.md` : OK.

## Suite

Prochain ticket recommande : `SELARL-RETURNS-006-CONJOINT-LETTERS-001`.
