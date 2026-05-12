# Dernier état projet

## Date de mise à jour
2026-05-12

## Dernier ticket terminé
DOC-003 : implémenter la procuration.

## État courant du repo
- DOC-001 dispose d'un générateur dédié déjà terminé et n'a pas été modifié dans ce ticket.
- DOC-003 dispose maintenant d'un générateur dédié :
  - `src/sydel_doc_engine/generators/lot_01/procuration.py` ;
  - génération DOCX from-scratch ;
  - sortie déterministe `procuration.docx` ;
  - création du répertoire de sortie si nécessaire.
- Des tests unitaires ciblés couvrent DOC-003 :
  - création du fichier DOCX ;
  - présence des textes essentiels ;
  - accord féminin `Je soussignée` ;
  - assemblage de l'adresse personnelle dans l'ordre source `num voie, ville cp` ;
  - assemblage de l'adresse du siège dans l'ordre source `num voie, ville cp` ;
  - présence du bloc SYDEL exact ;
  - absence de logique d'image de signature.
- DOC-002, l'orchestrateur, Streamlit, PDF et ZIP n'ont pas été modifiés dans ce ticket.
- Aucun commit, push ou PR n'a été fait.

## Décisions métier/techniques appliquées dans ce ticket
- Génération DOCX from-scratch pour DOC-003.
- Pas de PDF ni ZIP dans ce ticket.
- Accord de genre limité à `Je soussigné` / `Je soussignée`.
- Adresse personnelle rendue au format source `num voie + voie, ville cp`.
- Adresse du siège rendue au format source `num voie + voie, ville cp`.
- Bloc SYDEL fixe conservé :
  - `SYDEL`
  - `80 avenue Marceau, 75008 PARIS`
  - `RCS PARIS 788 531 432`
  - `0153814303`
- Aucune image de signature n'est insérée pour DOC-003.
- Les formulations de mandat ont été conservées, notamment la phrase :
  - `De pour moi et en mon nom faire tous dépôts...`

## Prochain ticket à lancer
DOC-002 : implémenter l'autorisation de domiciliation.

## Points ouverts
- Aucun point bloquant identifié après DOC-003.
- DOC-002 doit respecter la décision V1 : `domiciliation.adresse_locaux_affichee` est un champ libre.
- Toute ambiguïté de wording juridique doit bloquer l'implémentation concernée et être documentée.

## Validations connues
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 20 tests passés.

## Recommandation immédiate suivante
Lancer DOC-002 avec lecture préalable de :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/delivery/lot_01_analysis_and_specs_v1.md`
- ADR-0001, ADR-0002, ADR-0004 et ADR-0005
