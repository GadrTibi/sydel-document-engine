# SELAS-DOC005-DOC006-REGIME-COMMUNAUTAIRE-001

Date : 2026-06-02

## Objet

Brancher le batch conditionnel regime communautaire SELAS pour `DOC-005` et
`DOC-006`, sans activer le pack SELAS complet.

## Sources lues

- `docs/sprints/SPRINT_SELAS_SPEC_REGIME_COMMUNAUTAIRE_001.md`
- `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md`
- `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`
- generateurs existants Lot 02 regime communautaire
- tests existants regime communautaire

## Decision

`DOC-005` et `DOC-006` forment un batch conditionnel unique pour SELAS.

- Si `regime_communautaire = false`, aucun des deux documents ne doit apparaitre
  comme candidat SELAS.
- Si `regime_communautaire = true`, les deux documents deviennent candidats
  avec un statut `CONTEXT_INCOMPLETE`, car les donnees conjoint/apport/societe
  doivent etre completes avant generation.
- `DOC-006` sort de la reserve SELAS dans le schema front/data. Il ne devient
  visible que par le declencheur regime communautaire.

## Changements realises

- `src/sydel_doc_engine/front_data/selas_schema.py`
  - ajout de `DOC-006` comme candidat conditionnel avec `DOC-005` ;
  - suppression de `DOC-006` des documents reserves SELAS ;
  - ajout d'une liste de champs canoniques commune au batch regime communautaire.
- `tests/unit/test_selas_front_schema.py`
  - verification que le parcours simple n'expose pas `DOC-005` / `DOC-006` ;
  - verification que le parcours regime communautaire expose les deux documents ;
  - verification des roles, statuts et champs requis.
- `tests/unit/test_regime_communautaire.py`
  - renforcement des controles anti-regression SELAS : actionnaire, SELAS,
    absence de `SELARL`, `parts sociales` et `Directeur General`.

## Validations

- `compileall` OK sur les fichiers modifies.
- Smoke manuel schema SELAS OK :
  - parcours simple sans `DOC-005` / `DOC-006` ;
  - parcours regime communautaire avec `DOC-005` / `DOC-006` candidats ;
  - `DOC-006` absent des reserves.
- Smoke manuel DOCX OK avec generation reelle des deux lettres :
  - renonciation contient `personnellement actionnaire de cette société` ;
  - avertissement contient `à la SELAS RC SANTE` ;
  - aucune trace interdite `SELARL`, `parts sociales`, `Directeur General`,
    crochets de placeholder.

## Limites

- `pytest` et `ruff` sont indisponibles dans l'environnement local et dans le
  runtime embarque ; ils devront etre relances dans un environnement equipe.
- Le ticket n'active pas le pack DOCX/PDF/ZIP SELAS.
- Aucun wording juridique source n'a ete modifie.

## Prochaine etape recommandee

`SELAS-DOC018-STATUTS-MEDECIN-AU-001`
