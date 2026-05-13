# Dernier état projet

## Date de mise à jour
2026-05-13

## Dernier ticket terminé
PM-004 : intégrer l'arbre moteur document-centré V1 dans la mémoire projet.

## État courant du repo
- DOC-001, DOC-002 et DOC-003 disposent chacun d'un générateur dédié déjà terminé.
- L'orchestrateur dossier expose maintenant :
  - un registre minimal des générateurs Lot 1 ;
  - `select_documents(structure)` selon le catalogue ;
  - `generate_documents(ctx, output_dir) -> list[Path]`.
- `generate_documents` sélectionne les documents applicables via `ctx.structure`, conserve l'ordre du catalogue, crée les DOCX dans le répertoire de sortie et retourne les chemins produits.
- Si un document sélectionné n'a pas de générateur enregistré, l'orchestrateur lève une erreur explicite.
- La logique documentaire du moteur est désormais formalisée par l'arbre moteur document-centré V1 présent dans `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md.md`.
- Les tests unitaires d'orchestration couvrent :
  - la sélection SELARL des trois documents universels Lot 1 ;
  - la création de trois DOCX ;
  - l'ordre de sortie conforme au catalogue ;
  - l'erreur de générateur manquant.
- Streamlit, PDF, ZIP et `rendering/bundle.py` n'ont pas été modifiés dans ce ticket.
- Aucun commit, push ou PR n'a été fait.

## Décisions métier/techniques appliquées dans ce ticket
- L'arbre moteur document-centré V1 est intégré comme mémoire projet, sans réinvention ni réécriture de l'arbre.
- Le board signale que la logique documentaire du moteur est formalisée.
- Aucun code Python n'a été modifié.
- Aucun commit, push ou PR n'a été fait.
- Aucun wording juridique n'a été modifié.

## Prochain ticket à lancer
UI-001 : brancher Streamlit V0 Lot 1 sur l'orchestrateur dossier.

## Points ouverts
- Aucun point bloquant identifié après ORCH-001.
- Le chemin demandé `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md` n'existe pas encore : le fichier présent est `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md.md`.
- PDF et ZIP restent à intégrer dans des tickets ultérieurs.
- Toute ambiguïté de wording juridique doit bloquer l'implémentation concernée et être documentée.

## Validations connues
- Relecture du diff documentaire : OK.
- Vérification du scope : uniquement `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md` modifiés.
- Aucun test code lancé : tâche documentaire pure sans modification Python.

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
