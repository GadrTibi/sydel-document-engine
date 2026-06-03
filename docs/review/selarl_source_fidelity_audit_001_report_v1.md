# SELARL-SOURCE-FIDELITY-AUDIT-001 - rapport V1

Date : 2026-06-01

## Decision

Le retour associe est traite comme un signal produit valide.

Conclusion : il ne fallait pas poser de nouvelles questions abstraites sur le
regime communautaire. La condition est deja determinee par les sources : quand
le regime communautaire est actif, il faut produire la lettre de renonciation
`DOC-005` et la lettre d'avertissement conjoint `DOC-006`.

## Cause racine

Le moteur contenait deja `DOC-006`, mais le front et plusieurs documents de
pilotage avaient conserve une ancienne reserve source.

Cette reserve etait devenue fausse pour le perimetre actuel :

- la source DOCX `DOC-006` existe dans `project/source_documents/lot_02/` ;
- le batch regime communautaire est specifie dans les specs Lot 2 ;
- l'orchestrateur et le catalogue savent deja generer `DOC-006` ;
- la source de verite liste les deux lettres pour le regime communautaire.

## Sources relues

- `project/source_truth/Documents_a_generer_par_cas.docx`
- `project/source_documents/lot_02/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx`
- `project/source_documents/lot_02/Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - transforme.docx`
- `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md`
- `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`
- `src/sydel_doc_engine/generators/lot_02/lettre_renonciation_associe.py`
- `src/sydel_doc_engine/generators/lot_02/lettre_avertissement_conjoint.py`
- `src/sydel_doc_engine/orchestrator/service.py`
- `src/sydel_doc_engine/registry/catalog.py`

## Correction faite

- `DOC-006` est selectionne avec `DOC-005` quand `regime_communautaire=True`.
- Le front demande l'adresse du conjoint uniquement dans ce contexte.
- Le contexte moteur fournit cette adresse au generateur `DOC-006`.
- Le panneau documents n'affiche plus `DOC-006` comme reserve quand le regime
  communautaire est actif.
- Les warnings produit disent maintenant que `DOC-005` et `DOC-006` seront
  generes.
- Les tests attendent 8 DOCX pour les scenarios regime communautaire.

## Fichiers code touches

- `src/sydel_doc_engine/front_app/selarl_slice.py`
- `src/sydel_doc_engine/front_app/shell.py`
- `tests/unit/test_clean_front_app.py`

## Documents projet alignes

- `docs/project/SELARL_CANONICAL_STATUS_V1.md`
- `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`
- `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md`
- `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md`
- `docs/project/SELARL_COMPLETE_CASE_PLAYBOOK_V1.md`
- `docs/project/SELARL_PROCESS_SPEC_V1.md`
- `docs/project/SELARL_UI_WIZARD_SPEC_V1.md`
- `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`
- `docs/project/PROJECT_CONTROL_TOWER_V1.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/04_LAST_STATE.md`

## Validation

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- Tests cibles SELARL/documents : 83 passes.
- `.\.venv\Scripts\python.exe -m pytest -q` : 415 passes.

## Decision de pilotage

Ne plus demander a Gad ou a l'associe une confirmation sur les regles deja
couvertes par les sources et les specs.

La prochaine revue humaine doit porter seulement sur des ecarts concrets :

- texte qui ne respecte pas la source ;
- document attendu absent ;
- variable mal injectee ;
- document en trop ;
- erreur de ZIP ou de scenario.
