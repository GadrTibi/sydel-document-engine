# SELAS-SPEC-CAPITAL-ACTIONS-001

Date : 2026-06-02

Statut : `DONE - specification V1`

Decision sprint : `GO spec` mais `NO-GO pack SELAS`

## Objet

Specifier le bloc capital / actions pour le parcours :

```text
SELAS medecin, actionnaire unique, President unique, creation simple.
```

Ce ticket ne code rien. Il verrouille seulement :

- les donnees capital / actions a collecter ;
- les controles de coherence attendus ;
- la regle V1 de numerotation ;
- les cas complexes a bloquer ;
- l'impact sur `DOC-018 - Statuts SELAS medecin` ;
- les criteres de recette du futur ticket code.

## Sources et documents lus

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/PROJECT_CONTROL_TOWER_V1.md`
- `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`
- `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`
- `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`
- `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`
- `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`
- `docs/sprints/SPRINT_SELAS_V1.md`
- `docs/sprints/SPRINT_SELAS_TICKETS_001.md`
- `docs/sprints/SPRINT_SELAS_SPEC_STATUTS_MEDECIN_AU_001.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`
- `project/source_documents/lot_04/Statuts_SELAS_medecin.docx`
- `src/sydel_doc_engine/domain/models.py`
- `src/sydel_doc_engine/front_data/selas_schema.py`
- `src/sydel_doc_engine/generators/lot_04/statuts_sel_exercice_common.py`
- `src/sydel_doc_engine/generators/lot_04/statuts_selas_medecin.py`

ADR applicables :

- ADR-0001 : source de verite documentaire.
- ADR-0002 : moteur par document canonique.
- ADR-0004 : generation DOCX propre from-scratch.
- ADR-0005 : travail Codex repo-first et petits tickets.

## Decision principale

Le bloc capital / actions V1 est limite a :

```text
capital social en numeraire,
actions ordinaires,
actionnaire unique,
pleine propriete,
droits de vote et droits financiers proportionnels au capital.
```

Decision V1 :

- `capital.type_titre` doit etre `actions` pour SELAS ;
- l'actionnaire unique detient 100 % des actions ;
- le President est sans incidence sur la repartition du capital ;
- aucune action de preference n'est automatisee ;
- aucun droit financier ou droit de vote derogatoire n'est automatise ;
- aucun demembrement n'est automatise ;
- aucune personne morale actionnaire n'est automatisee ;
- aucune ligne multi-actionnaires n'est automatisee dans les statuts V1.

## Perimetre documentaire

Le bloc capital / actions impacte en premier :

- `DOC-018 - Statuts SELAS medecin` ;
- `SELAS-ATTESTATION-CAPITAL` reservee ;
- futurs actes de cession d'actions, reserves hors V1 simple.

Decision documentaire :

- la source `DOC-018` affiche le capital, le nombre d'actions et la valeur
  nominale ;
- la source `DOC-018` ne doit pas recevoir une ligne de numerotation inventee si
  elle ne la contient pas ;
- la numerotation peut etre calculee comme donnee interne pour controle et
  futurs documents, mais elle n'est affichee que dans un document dont la source
  l'exige.

## Donnees canoniques attendues

### Capital global

- `capital.type_titre` = `actions`
- `capital.montant`
- `capital.montant_lettres`
- `capital.nombre_titres_total`
- `capital.nombre_titres_total_lettres`
- `capital.valeur_nominale_titre`
- `capital.valeur_nominale_titre_lettres`
- `capital.liberation` = `entierement_libere`

Aliases front acceptes pour le parcours SELAS :

- `capital.actions.nombre_total` -> `capital.nombre_titres_total`
- `capital.actions.nombre_total_lettres` -> `capital.nombre_titres_total_lettres`
- `capital.actions.valeur_nominale` -> `capital.valeur_nominale_titre`
- `capital.actions.valeur_nominale_lettres` -> `capital.valeur_nominale_titre_lettres`

Regle :

- le front peut afficher `actions` ;
- le moteur conserve une structure generique `titres` quand elle existe deja,
  avec `type_titre = actions`.

### Actionnaire unique

- `personne.actionnaire.prenom`
- `personne.actionnaire.nom`
- `personne.actionnaire.nombre_actions`
- `personne.actionnaire.apport_numeraire`
- `personne.actionnaire.apport_numeraire_lettres`
- `personne.actionnaire.pourcentage_capital` = `100`
- `personne.actionnaire.pourcentage_droits_vote` = `100`
- `personne.actionnaire.pourcentage_droits_financiers` = `100`
- `personne.actionnaire.qualite` = valeur source validee, par exemple
  `associe unique`

Mapping moteur existant :

- `associes[0].nb_parts` peut rester le champ technique existant tant que le
  generateur commun l'utilise pour representer le nombre de titres ;
- pour SELAS, son sens documentaire est `nombre d'actions`, pas `parts
  sociales` ;
- un futur nettoyage peut renommer le champ technique, mais ce ticket ne le fait
  pas.

## Controles obligatoires

Le futur code doit verifier au minimum :

1. `capital.type_titre == actions` ;
2. `capital.nombre_titres_total` est un entier strictement positif ;
3. `capital.valeur_nominale_titre` est un montant strictement positif ;
4. `capital.montant` est un montant strictement positif ;
5. `capital.nombre_titres_total * capital.valeur_nominale_titre == capital.montant` ;
6. `associes[0].nombre_actions == capital.nombre_titres_total` ;
7. `associes[0].apport_numeraire == capital.montant` ;
8. les droits de vote sont proportionnels au capital ;
9. les droits financiers sont proportionnels au capital ;
10. aucune action de preference n'est presente ;
11. aucune classe ou categorie d'actions n'est presente ;
12. aucun demembrement n'est present ;
13. aucun actionnaire supplementaire n'est present ;
14. aucune personne morale actionnaire n'est presente ;
15. les libelles en lettres sont fournis quand la source les exige.

Les controles de montants doivent utiliser une logique numerique fiable, par
exemple `Decimal`, pas une comparaison de chaines affichees.

## Numerotation des actions

### Decision V1

Pour le cas actionnaire unique, la numerotation est deterministe :

```text
actions 1 a N
```

avec :

```text
N = capital.nombre_titres_total
```

Regle :

- la numerotation est calculee automatiquement pour le controle interne ;
- elle ne doit pas etre saisie manuellement dans le happy path ;
- elle ne doit pas etre affichee dans `DOC-018` si la source statuts ne contient
  pas de wording de numerotation ;
- si un document futur exige une plage d'actions, la plage V1 autorisee est
  seulement `1 a N` pour l'actionnaire unique.

### Cas a bloquer

Bloquer si :

- la numerotation est fournie manuellement et ne correspond pas a `1 a N` ;
- il y a plusieurs plages d'actions ;
- les actions ne sont pas consecutives ;
- une action est demembree ;
- il existe plusieurs categories d'actions ;
- il existe des actions de preference ;
- le dossier demande une repartition non proportionnelle des votes ou benefices.

## Wording autorise et interdit

Autorise / attendu pour SELAS :

- `actions`
- `action`
- `capital social`
- `valeur nominale`
- `associe unique` si la source statuts l'utilise
- `droits de vote` si la source statuts l'utilise

Interdit comme rendu cible du bloc capital SELAS :

- `parts sociales`
- `part sociale`
- `cession de parts`
- `associe porteur de parts` si le contexte vise les titres SELAS

Nuance :

- le mot `associe` peut rester si la source statuts SELAS le contient ;
- ce ticket ne remplace pas automatiquement `associe` par `actionnaire` dans le
  wording juridique ;
- le front peut afficher `Actionnaire` pour clarifier le role utilisateur.

## Blocages hors V1

Restent hors automatisation V1 :

- multi-actionnaires ;
- repartition inegale du capital ;
- droits de vote non proportionnels ;
- droits financiers non proportionnels ;
- actions de preference ;
- categories d'actions ;
- demembrement usufruit / nue-propriete ;
- indivision ;
- personne morale actionnaire ;
- micro-holding ;
- apport en nature ;
- apport de titres ;
- prime d'emission ;
- capital variable ;
- augmentation ou reduction de capital ;
- cession d'actions ;
- liste des souscripteurs integree aux statuts ;
- attestation de capital SELAS tant que son document canonique n'est pas
  specifie.

## Impact front / schema

Le schema front SELAS devra afficher ou exiger :

- montant du capital ;
- nombre d'actions ;
- valeur nominale ;
- repartition : actionnaire unique = 100 % ;
- droits de vote = capital ;
- droits financiers = capital ;
- blocage visible si l'utilisateur tente de saisir un cas complexe ;
- rappel que la numerotation est automatique en V1.

Message de blocage recommande :

```text
La V1 SELAS automatise uniquement les actions ordinaires detenues a 100 % par
l'actionnaire unique. Les actions de preference, droits derogatoires,
demembrements ou multi-actionnaires doivent etre traites manuellement.
```

## Impact moteur `DOC-018`

Le futur ticket `SELAS-DOC018-STATUTS-MEDECIN-AU-001` devra :

- conserver `capital.type_titre = actions` ;
- controler la coherence montant / nombre d'actions / valeur nominale ;
- controler que l'actionnaire unique recoit toutes les actions ;
- ne pas ajouter de wording de numerotation si la source `DOC-018` ne le
  contient pas ;
- bloquer les droits derogatoires et actions complexes ;
- verifier l'absence de `parts sociales` dans le bloc capital rendu.

## Tests attendus pour futur code

Le futur code devra au minimum tester :

1. cas heureux : 1 000 euros, 100 actions, 10 euros de valeur nominale ;
2. blocage si `type_titre != actions` ;
3. blocage si nombre d'actions absent ;
4. blocage si valeur nominale absente ;
5. blocage si capital absent ;
6. blocage si `nombre_actions * valeur_nominale != capital` ;
7. blocage si actionnaire unique ne recoit pas toutes les actions ;
8. blocage si droits de vote differents de 100 % ;
9. blocage si droits financiers differents de 100 % ;
10. blocage si une action de preference est declaree ;
11. blocage si une categorie d'actions est declaree ;
12. blocage si une numerotation manuelle ne correspond pas a `1 a N` ;
13. rendu `DOC-018` sans `parts sociales` dans le bloc capital ;
14. rendu `DOC-018` sans placeholder capital residuel ;
15. pack SELAS toujours inactif sans gate separe.

## Decision finale

Le capital / actions SELAS V1 est assez cadre pour permettre ensuite une spec
`DOC-018` plus proche du code, mais pas pour activer un pack.

Prochaine action recommandee :

```text
SELAS-SPEC-ORDRE-001
```

ou validation outillee des tickets deja codes si l'environnement dev est equipe.
