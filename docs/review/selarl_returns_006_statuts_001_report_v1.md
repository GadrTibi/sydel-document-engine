# SELARL returns 006 statuts 001 report V1

Date : 2026-06-02

Ticket : `SELARL-RETURNS-006-STATUTS-001`

Source :

- `docs/review/selarl_human_returns_006_raw_v1.md`
- `docs/review/selarl_human_returns_triage_006_report_v1.md`

## Verdict

Verdict : `DONE`.

Le ticket est reste borne aux statuts SELARL `DOC-016` et `DOC-017`.

## Corrections appliquees

| Retour | Decision appliquee |
| --- | --- |
| Mention regime matrimonial communaute | Les statuts affichent `marie sous le regime de la communaute avec {civilite conjoint} {prenom conjoint} {nom conjoint}` apres l'identite ordinale. |
| Mention regime matrimonial separation de biens | Les statuts affichent `marie sous le regime de la separation de biens avec {civilite conjoint} {prenom conjoint} {nom conjoint}`. Aucun document additionnel n'est declenche dans ce ticket. |
| Article 8 | Le libelle `associe` est accorde en genre/nombre via un libelle derive : `associe unique`, `associee unique`, `associes`, `associees`. |
| Annexe | Les statuts SELARL placent l'annexe sur la page suivante. |
| Ligne `Ouverture...` | La ligne finale est rendue avec un tiret devant `Ouverture d'un compte bancaire`. |

## Fichiers modifies

- `src/sydel_doc_engine/generators/lot_04/statuts_sel_exercice_common.py`
- `src/sydel_doc_engine/generators/lot_04/statuts_sel_exercice_templates.py`
- `src/sydel_doc_engine/generators/lot_04/statuts_selarl_dentiste.py`
- `src/sydel_doc_engine/generators/lot_04/statuts_selarl_medecin.py`
- `tests/unit/test_lot_04_statuts_sel_exercice.py`

## Validations

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_lot_04_statuts_sel_exercice.py -q` : OK, 14 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check src/sydel_doc_engine/generators/lot_04/statuts_sel_exercice_common.py src/sydel_doc_engine/generators/lot_04/statuts_selarl_dentiste.py src/sydel_doc_engine/generators/lot_04/statuts_selarl_medecin.py tests/unit/test_lot_04_statuts_sel_exercice.py` : OK.
- `.\.venv\Scripts\python.exe -m ruff check src/sydel_doc_engine/generators/lot_04/statuts_sel_exercice_templates.py` : OK.

## Suite

Prochain ticket recommande : `SELARL-RETURNS-006-DNC-001`.
