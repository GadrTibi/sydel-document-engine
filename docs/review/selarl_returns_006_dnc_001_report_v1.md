# SELARL returns 006 DNC 001 report V1

Date : 2026-06-02

Ticket : `SELARL-RETURNS-006-DNC-001`

Source :

- `docs/review/selarl_human_returns_006_raw_v1.md`
- `docs/review/selarl_human_returns_triage_006_report_v1.md`

## Verdict

Verdict : `DONE`.

Le ticket est reste borne a `DOC-001` Declaration de non condamnation et a la
donnee moteur/front necessaire pour choisir `a` ou `au` devant la ville de
naissance.

## Corrections appliquees

| Retour | Decision appliquee |
| --- | --- |
| Ajouter la ville de naissance apres `Ne le {date}` | La DNC rend maintenant `Ne le {date} a {ville}.` ou `Nee le {date} a {ville}.` selon le genre grammatical. |
| Ajouter une case `au` pour les villes comme `Bourget` | Le modele commun `Person` porte `ville_naissance_article_au`. Si la case est cochee, la DNC rend `au {ville}` ; sinon elle rend `a {ville}`. |
| Repercuter dans le moteur | La donnee est propagee dans le clean front SELARL, le front historique, le wizard metier et le mode document unitaire DOC-001. |
| Coherence des donnees de test | Le prefill aleatoire SELARL ne cree plus un statut `Marie(e)` sans conjoint quand le regime communautaire n'est pas actif. |

## Fichiers modifies

- `src/sydel_doc_engine/domain/models.py`
- `src/sydel_doc_engine/generators/lot_01/declaration_non_condamnation.py`
- `src/sydel_doc_engine/front_app/selarl_slice.py`
- `src/sydel_doc_engine/front_app/shell.py`
- `src/sydel_doc_engine/app/front_dossier_entry.py`
- `src/sydel_doc_engine/app/front_generation_actions.py`
- `src/sydel_doc_engine/app/business_wizard.py`
- `src/sydel_doc_engine/app/single_document_mode.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `src/sydel_doc_engine/app/test_prefill_presets.py`
- `tests/unit/test_declaration_non_condamnation.py`
- `tests/unit/test_clean_front_app.py`
- `tests/unit/test_front_generation_actions.py`
- `tests/unit/test_single_document_mode.py`
- `tests/unit/test_business_wizard.py`

## Validations

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_declaration_non_condamnation.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_single_document_mode.py tests/unit/test_business_wizard.py -q` : OK, 94 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check src/sydel_doc_engine/domain/models.py src/sydel_doc_engine/generators/lot_01/declaration_non_condamnation.py src/sydel_doc_engine/front_app/selarl_slice.py src/sydel_doc_engine/front_app/shell.py src/sydel_doc_engine/app/front_dossier_entry.py src/sydel_doc_engine/app/front_generation_actions.py src/sydel_doc_engine/app/business_wizard.py src/sydel_doc_engine/app/single_document_mode.py src/sydel_doc_engine/app/streamlit_app.py src/sydel_doc_engine/app/test_prefill_presets.py tests/unit/test_declaration_non_condamnation.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_single_document_mode.py tests/unit/test_business_wizard.py` : OK.

## Suite

Prochain ticket recommande : `SELARL-RETURNS-006-PV-001`.
