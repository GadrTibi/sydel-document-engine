# SELARL returns 006 address signature 001 report V1

Date : 2026-06-02

Ticket : `SELARL-RETURNS-006-ADDRESS-SIGNATURE-001`

Sources :

- `docs/review/selarl_human_returns_006_raw_v1.md`
- `docs/review/selarl_human_returns_triage_006_report_v1.md`

## Verdict

Verdict : `DONE`.

Le ticket est reste borne aux regles transversales explicites du retour humain
006 : ordre code postal / ville et suppression des encadres de signature.

## Corrections appliquees

| Retour | Decision appliquee |
| --- | --- |
| Code postal avant ville | Les adresses d'entree du front/moteur sont normalisees pour rendre `75010 Paris` plutot que `Paris 75010` quand une adresse affichee arrive dans le mauvais ordre. |
| Signature sans encadre | Les blocs de signature encadres restants dans le perimetre SELARL pack sont passes en blocs non encadres sur `DOC-001`, `DOC-002` et `DOC-003`. |

## Fichiers modifies

- `src/sydel_doc_engine/app/front_generation_actions.py`
- `src/sydel_doc_engine/generators/lot_01/declaration_non_condamnation.py`
- `src/sydel_doc_engine/generators/lot_01/autorisation_domiciliation.py`
- `src/sydel_doc_engine/generators/lot_01/procuration.py`
- `tests/unit/test_front_generation_actions.py`
- `tests/unit/test_declaration_non_condamnation.py`
- `tests/unit/test_autorisation_domiciliation.py`
- `tests/unit/test_procuration.py`

## Validations

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_declaration_non_condamnation.py tests/unit/test_autorisation_domiciliation.py tests/unit/test_procuration.py tests/unit/test_front_generation_actions.py -q` : OK, 37 tests passes.
- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_demande_inscription_ordre.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_front_dossier_data_entry.py tests/unit/test_business_wizard.py tests/unit/test_single_document_mode.py tests/unit/test_lot_04_statuts_sel_exercice.py tests/unit/test_pv_nomination_gerant.py tests/unit/test_declaration_non_condamnation.py tests/unit/test_autorisation_domiciliation.py tests/unit/test_procuration.py tests/unit/test_regime_communautaire.py -q` : OK, 165 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check src/sydel_doc_engine/app/front_generation_actions.py src/sydel_doc_engine/app/front_dossier_entry.py src/sydel_doc_engine/app/streamlit_app.py src/sydel_doc_engine/domain/models.py src/sydel_doc_engine/front_app/data_entry.py src/sydel_doc_engine/front_app/field_derivations.py src/sydel_doc_engine/front_app/selarl_slice.py src/sydel_doc_engine/front_app/shell.py src/sydel_doc_engine/generators/lot_01/declaration_non_condamnation.py src/sydel_doc_engine/generators/lot_01/autorisation_domiciliation.py src/sydel_doc_engine/generators/lot_01/procuration.py src/sydel_doc_engine/generators/lot_02/demande_inscription_ordre.py tests/unit/test_demande_inscription_ordre.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_front_dossier_data_entry.py tests/unit/test_business_wizard.py tests/unit/test_single_document_mode.py tests/unit/test_lot_04_statuts_sel_exercice.py tests/unit/test_pv_nomination_gerant.py tests/unit/test_declaration_non_condamnation.py tests/unit/test_autorisation_domiciliation.py tests/unit/test_procuration.py tests/unit/test_regime_communautaire.py` : OK.

## Questions humaines

Aucune question humaine n'etait necessaire : le retour 006 etait une regle
generale claire.

## Suite

Prochain ticket recommande : `SELARL-CLOSING-PACK-005`.
