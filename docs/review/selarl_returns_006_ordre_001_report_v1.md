# SELARL returns 006 ordre 001 report V1

Date : 2026-06-02

Ticket : `SELARL-RETURNS-006-ORDRE-001`

Sources :

- `docs/review/selarl_human_returns_006_raw_v1.md`
- `docs/review/selarl_human_returns_triage_006_report_v1.md`

## Verdict

Verdict : `DONE`.

Le ticket est reste borne au `DOC-034` demande d'inscription a l'Ordre et aux
champs front necessaires.

## Correction appliquee

| Retour | Decision appliquee |
| --- | --- |
| Conseil departemental | Le document ne demande plus un libelle complet de conseil departemental comme source principale. Pour SELARL/SELAS, le libelle est compose sous la forme `Conseil departemental de l'Ordre des {Profession} de {departement d'inscription a l'Ordre}`. |
| Variable front | Le front SELARL conserve le departement d'inscription a l'Ordre comme donnee utile et ne bloque plus sur un champ visible de libelle complet. |
| Compatibilite | L'ancien libelle complet reste tolere en fallback technique quand le departement d'inscription n'est pas renseigne, afin de ne pas casser les contextes existants hors ticket. |

## Fichiers modifies

- `src/sydel_doc_engine/domain/models.py`
- `src/sydel_doc_engine/generators/lot_02/demande_inscription_ordre.py`
- `src/sydel_doc_engine/front_app/selarl_slice.py`
- `src/sydel_doc_engine/front_app/shell.py`
- `src/sydel_doc_engine/app/front_generation_actions.py`
- `src/sydel_doc_engine/app/front_dossier_entry.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `tests/unit/test_demande_inscription_ordre.py`
- `tests/unit/test_clean_front_app.py`
- `tests/unit/test_front_generation_actions.py`

## Validations

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_demande_inscription_ordre.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_front_dossier_data_entry.py -q` : OK, 57 tests passes.
- Regression SELARL large executee apres tous les tickets 006 restants : OK, 165 tests passes.
- Ruff cible execute apres tous les tickets 006 restants : OK.

## Questions humaines

Aucune question humaine n'etait necessaire : le retour 006 indiquait la forme
attendue et la variable utile.

## Suite

Ticket suivant traite : `SELARL-RETURNS-006-FRONT-VARIABLES-001`.
