# SELAS-DOC018-STATUTS-MEDECIN-AU-001

Date : 2026-06-02

## Objet

Brancher et securiser `DOC-018 - Statuts SELAS medecin` pour le parcours V1 :
SELAS medecin, actionnaire unique, President unique, creation simple, capital en
numeraire divise en actions ordinaires.

## Sources lues

- `docs/sprints/SPRINT_SELAS_SPEC_STATUTS_MEDECIN_AU_001.md`
- `docs/sprints/SPRINT_SELAS_SPEC_CAPITAL_ACTIONS_001.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`
- `project/source_documents/lot_04/Statuts_SELAS_medecin.docx`

## Changements

- `DOC-018` conserve son generateur dedie `StatutsSelasMedecinGenerator`.
- Le generateur bloque les cas hors V1 : Directeur General nomme, actions de
  preference, categories d'actions, demembrement, personne morale actionnaire,
  micro-holding, droits de vote ou droits financiers derogatoires.
- Le capital SELAS est controle : `capital.type_titre == actions`, nombre
  d'actions positif, valeur nominale positive, montant du capital coherent avec
  `nombre_actions * valeur_nominale`, et apport de l'actionnaire unique coherent
  avec le capital.
- La numerotation manuelle est acceptee seulement si elle reste simple
  `1 a N`; sinon la generation est bloquee.
- L'orchestrateur ne selectionne pas `DOC-004 - PV nomination gerant` pour le
  contexte `SELAS` + `statuts_sel.overlay == selas_medecin`, car la nomination
  du President est absorbee par les statuts V1.
- Le catalogue documente les conditions SELAS specifiques de `DOC-018`.

## Validations locales

- `compileall` OK sur les fichiers modifies et les tests cibles.
- Smoke manuel orchestrateur OK : `DOC-018` selectionne, `DOC-004`, `DOC-016`
  et `DOC-017` non selectionnes.
- Smoke manuel DOCX OK avec le runtime documentaire : sortie
  `statuts_selas_medecin.docx`, presence `SELAS` / `President` / `actions`,
  absence `SELARL` / `parts sociales` / placeholders.
- Smokes negatifs OK : blocage `parts_sociales`, valeur nominale incoherente,
  apport incoherent, Directeur General, actions de preference et numerotation
  complexe.
- `git diff --check` OK.

## Limites

- `pytest` et `ruff` sont indisponibles dans le Python systeme et dans le
  runtime embarque ; les tests complets doivent etre relances dans un
  environnement equipe.
- Aucun pack SELAS complet n'est active.
- Aucun wording juridique source n'a ete modifie.

## Prochaine action

Lancer `SELAS-FRONT-READINESS-PACK-001` pour aligner le statut front/data du
pack SELAS V1 avant l'orchestration pack.
