# SELARL returns 006 front variables 001 report V1

Date : 2026-06-02

Ticket : `SELARL-RETURNS-006-FRONT-VARIABLES-001`

Sources :

- `docs/review/selarl_human_returns_006_raw_v1.md`
- `docs/review/selarl_human_returns_triage_006_report_v1.md`

## Verdict

Verdict : `DONE`.

Le ticket est reste borne aux variables front/moteur citees dans les retours
humains 006.

## Corrections appliquees

| Retour | Decision appliquee |
| --- | --- |
| Duree sociale | La duree SELARL est forcee a `99 ans`; elle n'est plus demandee dans les surfaces SELARL corrigees. |
| Siege social identique adresse personnelle | Une option `identique a l'adresse personnelle` copie l'adresse personnelle vers le siege social dans le front. |
| Nationalite portugaise | `Portugaise` est ajoutee aux choix de nationalite. |
| Nombre d'exemplaires | Les variables visibles de nombre d'exemplaires sont retirees du parcours SELARL corrige ; la valeur moteur est forcee a quatre exemplaires. |
| Qualite renoncee | La qualite renoncee est forcee a `associe`. |
| Date courrier | La date courrier avertissement est derivee du jour, et non plus demandee a l'utilisateur. |

## Fichiers modifies

- `src/sydel_doc_engine/front_app/field_derivations.py`
- `src/sydel_doc_engine/front_app/data_entry.py`
- `src/sydel_doc_engine/front_app/selarl_slice.py`
- `src/sydel_doc_engine/front_app/shell.py`
- `src/sydel_doc_engine/app/front_dossier_entry.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `tests/unit/test_clean_front_app.py`
- `tests/unit/test_front_generation_actions.py`
- `tests/unit/test_business_wizard.py`

## Validations

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_front_dossier_data_entry.py tests/unit/test_business_wizard.py tests/unit/test_single_document_mode.py -q` : OK, 100 tests passes.
- Regression SELARL large executee apres tous les tickets 006 restants : OK, 165 tests passes.
- Ruff cible execute apres tous les tickets 006 restants : OK.

## Questions humaines

Aucune question humaine n'etait necessaire : les retours 006 donnaient les
constantes attendues et les variables a supprimer.

## Suite

Ticket suivant traite : `SELARL-RETURNS-006-ADDRESS-SIGNATURE-001`.
