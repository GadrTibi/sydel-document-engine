# SELARL returns 006 conjoint letters 001 report V1

Date : 2026-06-02

Ticket : `SELARL-RETURNS-006-CONJOINT-LETTERS-001`

Sources :

- `docs/review/selarl_human_returns_006_raw_v1.md`
- `docs/review/selarl_human_returns_triage_006_report_v1.md`

## Verdict

Verdict : `DONE`.

Le ticket est reste borne au batch regime communautaire `DOC-005` / `DOC-006`.

## Corrections appliquees

| Retour | Decision appliquee |
| --- | --- |
| `DOC-006` forme juridique | Le bloc societe de la lettre d'avertissement rend une forme sociale redigee. Pour SELARL, il rend `Société d’exercice libéral à responsabilité limitée de {profession}` selon la profession disponible dans le contexte. |
| `DOC-006` adresse conjoint | L'adresse affichee pour le conjoint est derivee de l'adresse personnelle de l'associe/signataire quand elle existe. Une ancienne adresse conjoint separee ne pilote plus le document. |
| Front/readiness adresse conjoint | L'adresse conjoint n'est plus un champ canonique requis pour declarer `DOC-005` / `DOC-006` generables dans le front SELARL complet. |
| Formulaire simple | Le champ visible `Adresse conjoint` a ete retire du formulaire simple ; le champ technique reste tolere en entree de compatibilite, mais il n'est plus source metier. |
| `DOC-005` date sous la ville | La lettre de renonciation ne rend plus la ligne de date sous la ville avant l'objet ; l'espace avant l'objet est conserve. |

## Fichiers modifies

- `src/sydel_doc_engine/generators/lot_02/lettre_avertissement_conjoint.py`
- `src/sydel_doc_engine/generators/lot_02/lettre_renonciation_associe.py`
- `src/sydel_doc_engine/front_app/selarl_slice.py`
- `src/sydel_doc_engine/app/front_generation_actions.py`
- `src/sydel_doc_engine/app/front_dossier_entry.py`
- `src/sydel_doc_engine/app/front_selarl_complete.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `tests/unit/test_regime_communautaire.py`
- `tests/unit/test_clean_front_app.py`
- `tests/unit/test_front_generation_actions.py`

## Validations

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_regime_communautaire.py -q` : OK, 10 tests passes.
- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_regime_communautaire.py -q` : OK, 50 tests passes.
- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_lot_04_statuts_sel_exercice.py tests/unit/test_declaration_non_condamnation.py tests/unit/test_pv_nomination_gerant.py tests/unit/test_procuration.py tests/unit/test_regime_communautaire.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_single_document_mode.py tests/unit/test_business_wizard.py -q` : OK, 139 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check src/sydel_doc_engine/generators/lot_02/lettre_avertissement_conjoint.py src/sydel_doc_engine/generators/lot_02/lettre_renonciation_associe.py src/sydel_doc_engine/front_app/selarl_slice.py src/sydel_doc_engine/app/front_generation_actions.py src/sydel_doc_engine/app/front_dossier_entry.py src/sydel_doc_engine/app/front_selarl_complete.py src/sydel_doc_engine/app/streamlit_app.py tests/unit/test_regime_communautaire.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py` : OK.

## Suite

Prochain ticket recommande : `SELARL-RETURNS-006-ORDRE-001`.
