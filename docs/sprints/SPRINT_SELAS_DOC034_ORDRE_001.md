# SELAS DOC034 ordre 001

Date : 2026-06-02

Ticket : `SELAS-DOC034-ORDRE-001`

Statut : `DONE - partial QA`

Decision sprint : `NO-GO pack`

## Objet

Brancher de maniere bornee `DOC-034 - Demande d'inscription a l'Ordre` pour le
parcours SELAS V1.

Ce ticket reste limite a `DOC-034`. Il ne cree pas de nouveau document
canonique, ne modifie pas le wording juridique source, ne branche pas le pack
SELAS complet et ne genere aucun ZIP/PDF.

## Sources et specs lues

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/PROJECT_CONTROL_TOWER_V1.md`
- `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`
- `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`
- `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`
- `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`
- `docs/sprints/SPRINT_SELAS_SPEC_ORDRE_001.md`
- `docs/sprints/SPRINT_SELAS_ROADMAP_TO_COMPLETION_001.md`

ADR applicables :

- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : generation DOCX propre from-scratch ;
- ADR-0005 : mode Codex repo-first.

## Changements realises

### Schema SELAS

Fichier modifie :

- `src/sydel_doc_engine/front_data/selas_schema.py`

Changements :

- `DOC-034` conserve les roles directs attendus :
  - `SIGNATAIRE` ;
  - `MANDATAIRE` ;
  - `SOCIETE_PRINCIPALE` ;
  - `ORDRE_PROFESSIONNEL`.
- Les champs requis sont maintenant explicites pour SELAS :
  - signataire ;
  - societe ;
  - ordre ;
  - mandataire ;
  - signature ;
  - option derogation.
- L'ambiguite `mandataire_configurable` est levee cote schema SELAS, car la
  spec accepte soit `mandataire.libelle_affiche`, soit les champs mandataire
  detailles.
- L'ambiguite `selas_ordre_pieces_plans_devis` reste conservee comme reserve
  produit : plans/devis sont des pieces attendues, pas des DOCX generes.

### Tests

Fichiers modifies :

- `tests/unit/test_selas_front_schema.py`
- `tests/unit/test_demande_inscription_ordre.py`

Tests ajoutes :

- verification des roles, adresses, champs requis et ambiguites restantes de
  `DOC-034` dans le schema SELAS ;
- verification que `DOC-034` SELAS ne contient pas les termes interdits :
  `SELARL`, `gerant` / `gérant`, `parts sociales`, `Directeur General`,
  `Dérogation ?` ;
- verification que la derogation SELAS bloque sans mention manuelle.

## Validations realisees

Reussies :

```text
python3 -m compileall src/sydel_doc_engine/front_data/selas_schema.py tests/unit/test_demande_inscription_ordre.py tests/unit/test_selas_front_schema.py
PYTHONPATH=src python3 <smoke schema SELAS DOC-034>
PYTHONPATH=src <python runtime Codex> <smoke generateur DOC-034 SELAS>
```

Limites :

- `pytest` indisponible dans le Python systeme ;
- `ruff` indisponible dans le Python systeme ;
- `pytest` indisponible dans le runtime Python Codex ;
- `ruff` indisponible dans le runtime Python Codex.

## Verification trois sources

Le gate `SELAS-TRIPLE-SOURCE-CHECK-001` a ete ajoute a la roadmap.

Avant cloture SELAS V1, la premiere version totale devra etre comparee avec :

1. `project/source_truth/Documents_a_generer_par_cas.docx` ;
2. le journal NotebookLM SELAS ;
3. les retours humains Gad / associe / juriste sur la premiere version complete.

## Decision de sortie

`SELAS-DOC034-ORDRE-001` est termine en `DONE - partial QA`.

Le document `DOC-034` est SELAS-safe cote schema/front-data et generateur pour
le parcours SELAS medecin actionnaire unique President unique, sous reserve de
relancer `pytest` et `ruff` dans un environnement equipe.

Prochaine action recommandee selon roadmap :

```text
SELAS-DOC005-DOC006-REGIME-COMMUNAUTAIRE-001
```

Le pack SELAS complet reste bloque.
