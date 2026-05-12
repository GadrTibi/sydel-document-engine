# Dernier état projet

## Date de mise à jour
2026-05-12

## Dernier ticket terminé
DOC-002 : implémenter l'autorisation de domiciliation.

## État courant du repo
- DOC-001 dispose d'un générateur dédié déjà terminé et n'a pas été modifié dans ce ticket.
- DOC-003 dispose d'un générateur dédié déjà terminé et n'a pas été modifié dans ce ticket.
- DOC-002 dispose maintenant d'un générateur dédié :
  - `src/sydel_doc_engine/generators/lot_01/autorisation_domiciliation.py` ;
  - génération DOCX from-scratch ;
  - sortie déterministe `autorisation_domiciliation.docx` ;
  - création du répertoire de sortie si nécessaire.
- Le modèle `Domiciliation` porte le champ libre `adresse_domiciliation_affichee`.
- Des tests unitaires ciblés couvrent DOC-002 :
  - création du fichier DOCX ;
  - présence des textes essentiels ;
  - accord féminin `Je soussignée` ;
  - accord masculin `Je soussigné` ;
  - reprise stricte de `adresse_domiciliation_affichee` ;
  - absence de reconstruction automatique depuis l'adresse du siège ;
  - absence de logique d'image de signature.
- L'orchestrateur, Streamlit, PDF et ZIP n'ont pas été modifiés dans ce ticket.
- Aucun commit, push ou PR n'a été fait.

## Décisions métier/techniques appliquées dans ce ticket
- Génération DOCX from-scratch pour DOC-002.
- Pas de PDF ni ZIP dans ce ticket.
- Accord de genre limité à `Je soussigné` / `Je soussignée`.
- Le texte cible a été codé directement dans le générateur Python.
- L'adresse affichée est fournie par le champ libre `domiciliation.adresse_domiciliation_affichee`.
- L'anomalie source `[ville_siege] [cp_siege] [ville_siege]` n'est pas reproduite.
- Aucun mapping automatique depuis le siège social n'est appliqué.
- Aucune image de signature n'est insérée pour DOC-002.

## Prochain ticket à lancer
ORCH-001 : brancher les trois générateurs Lot 1 dans l'orchestrateur dossier.

## Points ouverts
- Aucun point bloquant identifié après DOC-002.
- La spec de livraison Lot 1 est alignée sur le champ `domiciliation.adresse_domiciliation_affichee`.
- Toute ambiguïté de wording juridique doit bloquer l'implémentation concernée et être documentée.

## Validations connues
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 27 tests passés.

## Recommandation immédiate suivante
Lancer ORCH-001 avec lecture préalable de :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/delivery/lot_01_analysis_and_specs_v1.md`
- ADR-0001, ADR-0002, ADR-0004 et ADR-0005
