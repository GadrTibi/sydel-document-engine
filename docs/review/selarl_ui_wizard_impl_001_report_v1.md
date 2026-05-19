# Rapport SELARL-UI-WIZARD-IMPL-001

## Perimetre

Objectif traite : adapter le mode `Assistant metier` Streamlit pour proposer un parcours SELARL pilote lisible, base sur le schema machine-readable `src/sydel_doc_engine/app/selarl_form_schema.py`.

Garde-fous respectes :

- aucun generateur DOCX/PDF/ZIP modifie ;
- aucun moteur documentaire modifie ;
- mode `Technique / diagnostic` conserve ;
- mode SCI existant conserve ;
- pas de nouveau worktree ;
- pas de push automatique.

## Fichiers modifies

- `src/sydel_doc_engine/app/business_wizard.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `tests/unit/test_business_wizard.py`
- `docs/review/selarl_ui_wizard_impl_001_report_v1.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/04_LAST_STATE.md`

## Parcours UI SELARL implemente

Le mode `Assistant metier` conserve la selection de type de dossier et branche un parcours dedie lorsque le dossier est `SELARL`.

Parcours visible :

- Ecran 1 : qualification du dossier via les conditions SELARL du schema ;
- Ecran 2 : societe, capital, parts, siege social et domiciliation ;
- Ecran 3 : professionnel principal / gerant, ordre professionnel et regles de reutilisation ;
- Ecran 4 : associes, parts, gerant parmi associes et copie depuis professionnel principal ;
- Ecran 5 : blocs conditionnels regime/conjoint, SCM, cession, bail, banque/financement et derogation ;
- Ecran 6 : documents attendus avec synthese generables / manuels / reserves / exclus ;
- Ecran 7 : generation DOCX, ZIP et PDF optionnel, filtree par les documents prets.

Le libelle `Dirigeant / pharmacien` a ete retire du parcours Streamlit et remplace par un wording generique `Representant legal` hors SELARL ; le parcours SELARL utilise `Gerant / professionnel principal`.

## Consommation du schema SELARL

`business_wizard.py` expose des projections testables issues de `selarl_form_schema.py` :

- conditions de qualification SELARL ;
- visibilite des blocs metier ;
- champs visibles par bloc ;
- labels d'adresse qualifies ;
- regles de reutilisation ;
- specs documentaires SELARL.

`streamlit_app.py` consomme ces projections pour les labels, aides, conditions d'affichage, regles de reutilisation et synthese documentaire. La logique de statut documentaire reste calculee par `evaluate_business_wizard(...)` et `get_expected_documents(...)`.

## Documents generables, manuels et reserves

- Les documents manuels restent visibles dans le tableau des documents attendus.
- Les documents non prets restent visibles comme `Contexte incomplet pour generation V2`.
- La generation automatique utilise toujours `validation.generatable_document_codes`, donc seulement les documents attendus, generables, codes en `DOC-XXX` et prets.
- `DOC-006` reste visible avec sa reserve source V2 issue du catalogue.
- `DOC-013` reste visible si derogation active, mais `MANUAL_ONLY`.
- `DOC-014` reste visible si derogation active, mais `MANUAL_ONLY`.
- `DOC-013` et `DOC-014` sont exclus des codes envoyes a la generation automatique SELARL.
- Le PV d'autorisation d'emprunt n'apparait pas comme document autonome ; l'emprunt est une option du `DOC-004`.

## Limites connues

- Les blocs cession, bail, banque et SCM affichent les champs du schema, mais leur contexte moteur complet reste a brancher document par document lors du smoke generation SELARL.
- Les documents SELARL complexes restent honnetement marques `Contexte incomplet pour generation V2` tant que les mappings complets ne sont pas relies au runtime.
- Aucune validation visuelle Playwright/Streamlit n'a ete ajoutee dans ce ticket ; les tests restent unitaires et source-level.

## Tests lances

- `.\.venv\Scripts\python.exe -m ruff check .`
- `.\.venv\Scripts\python.exe -m pytest`

Resultats :

- Ruff : OK, `All checks passed!`
- Pytest : OK, 239 tests passes.

## Prochaine etape recommandee

Ouvrir `SELARL-DOCS-GENERATION-SMOKE-001` pour tester le parcours SELARL avec des donnees realistes, confirmer les documents produits, et documenter les champs qui restent `Contexte incomplet pour generation V2` avant revue juriste.
