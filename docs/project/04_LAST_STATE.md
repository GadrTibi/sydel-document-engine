# Dernier état projet

## Date de mise à jour
2026-05-12

## Dernier ticket terminé
DOC-001 : implémenter la déclaration sur l'honneur de non-condamnation.

## État courant du repo
- DOC-001 dispose maintenant d'un générateur dédié :
  - `src/sydel_doc_engine/generators/lot_01/declaration_non_condamnation.py`
  - génération DOCX from-scratch ;
  - sortie déterministe `declaration_non_condamnation.docx` ;
  - création du répertoire de sortie si nécessaire.
- Les helpers existants sont utilisés pour :
  - accords de genre : `sydel_doc_engine.utils.grammar` ;
  - assemblage d'adresse personnelle : `sydel_doc_engine.utils.addresses`.
- Des tests unitaires ciblés couvrent :
  - création du fichier DOCX ;
  - présence des textes essentiels ;
  - accords féminins ;
  - assemblage de l'adresse personnelle dans l'ordre source, sans rendu `cp ville`.
- DOC-002, DOC-003, l'orchestrateur, Streamlit, PDF et ZIP n'ont pas été modifiés dans ce ticket.
- Aucun commit, push ou PR n'a été fait.

## Décisions métier/techniques appliquées dans ce ticket
- Génération DOCX from-scratch pour DOC-001.
- Pas de PDF ni ZIP dans ce ticket.
- Adresse personnelle DOC-001 rendue au format source `num voie + voie, ville cp`.
- Dates rendues au format `DD/MM/YYYY`.
- Accords obligatoires appliqués :
  - `Je soussigné` / `Je soussignée` ;
  - `Né le` / `Née le` ;
  - `fils de Monsieur` / `fille de Monsieur`.
- Si `signature.image_optionnelle` est fournie, l'image est insérée ; sinon une zone de signature vide est laissée.
- Le texte juridique source a été conservé autant que possible ; aucune réécriture juridique volontaire n'a été introduite.

## Prochain ticket à lancer
DOC-003 : implémenter la procuration.

## Points ouverts
- Aucun point bloquant identifié pour DOC-003.
- DOC-002 doit toujours respecter la décision V1 : `domiciliation.adresse_locaux_affichee` est un champ libre.
- Toute ambiguïté de wording juridique doit bloquer l'implémentation concernée et être documentée.

## Validations connues
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 12 tests passés.

## Recommandation immédiate suivante
Lancer DOC-003 avec lecture préalable de :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/delivery/lot_01_analysis_and_specs_v1.md`
- ADR-0001, ADR-0002, ADR-0004 et ADR-0005
