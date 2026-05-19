# Rapport SELARL-WORDING-REALIGN-001

## Objet

Realigner le vocabulaire visible du pilote SELARL sur les arbitrages explicites de l'associe, sans modifier l'ordre du parcours, les regles de reutilisation, les generateurs ni le moteur DOCX/PDF/ZIP.

## Sources lues

- `project/source_truth/notebooklm_selarl_10_prompts_v1.md`
- `project/source_truth/Documents_a_generer_par_cas_V3.docx`
- `docs/project/SELARL_SOURCE_HIERARCHY_V2.md`
- `docs/review/selarl_notebooklm_reconciliation_001_report_v1.md`
- `docs/project/SELARL_REBUILD_BACKLOG_V2.md`
- `src/sydel_doc_engine/app/selarl_form_schema.py`
- `src/sydel_doc_engine/app/business_wizard.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `tests/unit/test_selarl_form_schema.py`
- `tests/unit/test_business_wizard.py`

## Corrections realisees

- L'ancien titre de l'ecran personne devient `Ecran 3 - Fiche Client`.
- L'ancien bloc schema personne devient `Fiche Client`.
- Les champs d'identite, naissance, filiation, fonction, adresse personnelle et identifiants ordinaux parlent maintenant du `Praticien`.
- Les aides et captions de reutilisation visibles disent `Le gerant est le Praticien`, `Le signataire est le Praticien`, `Copier depuis le Praticien`.
- Le role juridique `Gerant` reste affiche quand la fonction ou le mandat social est vise.
- Les roles `Associe`, `Signataire` et `Mandataire` restent conserves dans leurs contextes.
- Les specs actives SELARL ont ete mises a jour in-place, sans creer de version documentaire inutile.

## Elements volontairement inchanges

- Les cles internes `professionnel_gerant`, `gerant_is_professional` et `signataire_is_professional` restent stables pour eviter tout changement de logique.
- L'ordre actuel des ecrans n'a pas ete modifie ; le realignement de flow reste pour `SELARL-FLOW-REALIGN-001`.
- Les regles de reutilisation n'ont pas ete changees fonctionnellement.
- `Ordre professionnel`, `adresse professionnelle d'exercice` et `identifiants professionnels` restent inchanges car ils designent le contexte ordinal ou professionnel exact.
- Les generateurs, le moteur DOCX/PDF/ZIP et `case_catalog.py` n'ont pas ete modifies.

## Tests ajoutes ou adaptes

- Verification de l'absence de l'ancien libelle personne dans les textes visibles du schema SELARL.
- Verification de la presence de `Fiche Client`, `Praticien`, `Gerant`, `Associe`, `Signataire`, `Mandataire`.
- Verification de l'absence de la transcription erronee de SELARL hors source NotebookLM.
- Mise a jour du test Streamlit pour verifier `Ecran 3 - Fiche Client`.
- Mise a jour du test d'adresse SELARL vers `Adresse personnelle du Praticien`.

## Validations

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_selarl_form_schema.py tests/unit/test_business_wizard.py` : OK, 37 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 241 tests passes.

## Decision de suite

Le prochain ticket SELARL recommande est `SELARL-FLOW-REALIGN-001`.

L'UI SELARL actuelle reste non validee produit pour push ou redeploiement tant que le flow, les reutilisations et l'UI complete ne sont pas realignes.
