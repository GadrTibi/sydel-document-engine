# Rapport SELARL-FLOW-REALIGN-001

## Objet

Réaligner l'ordre conceptuel du parcours SELARL sur les arbitrages associé, NotebookLM et la hiérarchie de sources corrigée, sans toucher aux générateurs ni au moteur DOCX/PDF/ZIP.

## Sources lues

- `project/source_truth/notebooklm_selarl_10_prompts_v1.md`
- `project/source_truth/Documents_a_generer_par_cas_V3.docx`
- `docs/project/SELARL_SOURCE_HIERARCHY_V2.md`
- `docs/review/selarl_notebooklm_reconciliation_001_report_v1.md`
- `docs/project/SELARL_REBUILD_BACKLOG_V2.md`
- `docs/review/selarl_wording_realign_001_report_v1.md`
- `src/sydel_doc_engine/app/selarl_form_schema.py`
- `src/sydel_doc_engine/app/business_wizard.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `tests/unit/test_selarl_form_schema.py`
- `tests/unit/test_business_wizard.py`

## Ordre ancien

Le cadrage technique issu du commit UI SELARL présentait encore cet ordre :

1. Qualification ;
2. Société ;
3. Fiche Client ;
4. Associés ;
5. Conditions spécifiques ;
6. Documents attendus ;
7. Génération.

L'écart principal était la société placée avant la personne cliente, alors que NotebookLM et l'arbitrage associé font de la Fiche Client / Praticien la source métier initiale.

## Ordre nouveau

Le schéma et les projections métier expriment maintenant l'ordre suivant :

1. Qualification ;
2. Fiche Client / Praticien ;
3. Fiche Société ;
4. Capital & Associés ;
5. Contexte & scénarios métier ;
6. Documents & génération.

## Ce qui a été modifié

- Ajout d'une notion `FormStep` dans `selarl_form_schema.py`.
- Ajout de `SELARL_FLOW_STEPS` pour rendre l'ordre SELARL explicite et testable.
- Réordonnancement des blocs machine-readable : Fiche Client / Ordre avant Fiche Société / Siège.
- Rattachement conceptuel des parts sociales au bloc `Capital & Associés`.
- Ajout de `selarl_blocks_by_step()` pour contrôler le regroupement des blocs.
- Ajout de `selarl_ui_flow_steps()` et `selarl_ui_visible_fields_by_step()` dans `business_wizard.py`.
- Mise à jour in-place des specs actives `SELARL_FORM_SCHEMA_V1.md` et `SELARL_UI_WIZARD_SPEC_V1.md`.

## Ce qui reste pour SELARL-REUSE-RULES-REALIGN-001

- Logique `Dossier unipersonnel`.
- Copie contrôlée Praticien = associé unique = gérant = signataire si option active.
- Distinction mandataire / signataire par défaut.
- Réutilisation explicite de la SELARL comme acquéreur ou cessionnaire.
- Réutilisation explicite du siège, du lieu d'exercice, du cabinet et de la domiciliation.
- Règles vendeur / locataire actuel.

## Impacts sur l'UI visible

`streamlit_app.py` n'a pas été modifié dans ce ticket. Le rendu Streamlit existant reste donc techniquement committé, mais il n'est pas validé produit et ne doit pas être poussé ou redéployé comme parcours SELARL cible.

Le réordonnancement visible complet reste volontairement réservé à `SELARL-UI-REALIGN-001`, après les règles de réutilisation.

## Impacts sur les tests

- Ajout de tests d'ordre des étapes SELARL dans `test_selarl_form_schema.py`.
- Ajout de tests de regroupement des blocs par étape.
- Ajout de tests de projection UI métier dans `test_business_wizard.py`.
- Les tests de documents attendus, documents manuels et mode Technique / diagnostic restent conservés.

## Validations

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_selarl_form_schema.py tests/unit/test_business_wizard.py` : OK, 41 tests passés.
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 245 tests passés.

## Garde-fous respectés

- Aucun générateur modifié.
- Aucun moteur DOCX/PDF/ZIP modifié.
- Aucun rendu juridique modifié.
- Aucun changement SCI.
- Aucun mode Projet ni filigrane ajouté.
- Aucun nouveau statut produit documentaire ajouté.

## Prochaine étape recommandée

Lancer `SELARL-REUSE-RULES-REALIGN-001` pour traiter `Dossier unipersonnel` et les réutilisations métier utiles avant le réalignement UI visible.
