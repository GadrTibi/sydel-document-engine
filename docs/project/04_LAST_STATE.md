# Dernier état projet

## Date de mise à jour
2026-05-13

## Dernier ticket terminé
SMOKE-001 : smoke test réel du Lot 1 via l'orchestrateur.

## État courant du repo
- DOC-001, DOC-002 et DOC-003 disposent chacun d'un générateur dédié déjà terminé.
- L'orchestrateur dossier expose :
  - un registre minimal des générateurs Lot 1 ;
  - `select_documents(structure)` selon le catalogue ;
  - `generate_documents(ctx, output_dir) -> list[Path]`.
- `examples/contexts/lot_01_example.yaml` a été corrigé au minimum strict pour utiliser le champ V1 attendu `domiciliation.adresse_domiciliation_affichee`.
- Un smoke test réel a généré les trois DOCX du Lot 1 dans `artifacts/lot_01_smoke_test/`.
- Fichiers générés :
  - `artifacts/lot_01_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_01_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_01_smoke_test/procuration.docx`
- Streamlit, PDF, ZIP et `rendering/bundle.py` n'ont pas été modifiés dans ce ticket.
- Aucun commit, push ou PR n'a été fait.

## Décisions métier/techniques appliquées dans ce ticket
- Le smoke test utilise le catalogue moteur existant via `DocumentOrchestrator(build_seed_catalog())`.
- Le contexte d'exemple reste un contexte SELARL exploitable pour les trois documents universels du Lot 1.
- La correction du YAML ne change aucun wording juridique : elle aligne seulement le nom du champ de domiciliation sur la spec V1 et le modèle Pydantic.
- Aucun autre lot n'a été touché.

## Prochain ticket à lancer
UI-001 : brancher Streamlit V0 Lot 1 sur l'orchestrateur dossier.

## Points ouverts
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Le smoke test confirme la production de trois fichiers DOCX, mais ne remplace pas une revue humaine du rendu visuel ni une validation juridique fine du contenu généré.
- PDF et ZIP restent à intégrer dans des tickets ultérieurs.
- Toute ambiguïté de wording juridique doit bloquer l'implémentation concernée et être documentée.

## Validations connues
- Smoke test Lot 1 réel : OK, 3 DOCX produits dans `artifacts/lot_01_smoke_test/`.
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 31 tests passés.

## Recommandation immédiate suivante
Lancer UI-001 avec lecture préalable de :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/delivery/lot_01_analysis_and_specs_v1.md`
- l'orchestrateur `src/sydel_doc_engine/orchestrator/service.py`
- l'interface `src/sydel_doc_engine/app/streamlit_app.py`
