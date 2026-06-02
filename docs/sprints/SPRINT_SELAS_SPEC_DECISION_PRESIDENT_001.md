# SELAS-SPEC-DECISION-PRESIDENT-001

Date : 2026-06-02

Statut : `DONE - specification V1`

Decision sprint : `NO-GO code` et `NO-GO pack SELAS`

## Objet

Specifier le document de nomination du President SELAS pour le parcours :

```text
SELAS medecin, actionnaire unique, President unique, creation simple.
```

Ce ticket ne code rien. Il verrouille seulement :

- le perimetre documentaire ;
- la reutilisation possible du `DOC-004` existant ;
- les roles et donnees minimales ;
- les blocages avant tout futur generateur ;
- les criteres de recette du futur ticket `SELAS-DECISION-PRESIDENT-001`.

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
- `docs/sprints/SPRINT_SELAS_MATRIX_001.md`
- `docs/sprints/SPRINT_SELAS_FRONT_CONTRACT_001.md`
- `docs/sprints/SPRINT_SELAS_TICKETS_001.md`
- `docs/sprints/SPRINT_SELAS_SPEC_PRESIDENT_001.md`
- `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`
- `src/sydel_doc_engine/front_data/selas_schema.py`
- `src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py`
- source DOCX Lot 2 `PV nomination gerant - transforme.docx`, lue via les
  specs Lot 2.

ADR applicables :

- ADR-0001 : source de verite documentaire.
- ADR-0002 : moteur par document canonique.
- ADR-0004 : generation DOCX propre from-scratch.
- ADR-0005 : travail Codex repo-first et petits tickets.

## Decision principale

Le document SELAS de nomination du President ne doit pas etre traite comme un
simple `DOC-004 - PV nomination gerant` renomme.

Decision V1 :

- le code front temporaire reste `SELAS-DECISION-PRESIDENT` ;
- `DOC-004` est seulement un patron structurel possible ;
- aucun generateur `DOC-004` existant ne doit etre branche sur SELAS pour ce
  document ;
- le futur code documentaire reste bloque tant qu'un texte SELAS President
  n'est pas verrouille par source/spec ;
- le Directeur General reste hors V1.

## Pourquoi `DOC-004` ne suffit pas

Le `DOC-004` existant est une famille `PV nomination gerant`.

La spec canonique Lot 2 dit explicitement que :

- la fonction par defaut de cette famille est `gerant` ;
- le modele source contient un formalisme d'assemblee ;
- il parle de parts, pas d'actions ;
- il a ete canonise autour des roles `associes[]` et `dirigeant_nomine`.

Pour SELAS, les reponses NotebookLM et la spec President indiquent :

- le dirigeant est le `President` ;
- le capital est divise en actions ;
- en actionnaire unique, le formalisme cible est une decision de l'actionnaire
  unique, pas un PV d'assemblee pluripersonnelle ;
- `Directeur General` est non trouve pour la V1 NotebookLM.

Conclusion : on peut reutiliser la methode du `DOC-004`, mais pas son wording
ni son generateur actuel.

## Nom et condition d'apparition

Nom de travail :

```text
Decision de nomination du President SELAS
```

Code de travail :

```text
SELAS-DECISION-PRESIDENT
```

Condition d'apparition V1 :

- dossier `SELAS` ;
- profession `medecin` ;
- actionnaire unique ;
- President unique ;
- pas de Directeur General ;
- pas de multi-actionnaires ;
- nomination du President non deja absorbee et verrouillee dans les statuts.

Point ouvert :

- si la spec statuts SELAS medecin confirme que le President est nomme
  directement dans les statuts, ce document peut devenir reserve ou
  conditionnel ;
- tant que ce choix n'est pas tranche, le document reste candidat mais non
  generable en pack.

## Roles canoniques

| Role | Statut V1 | Regle |
| --- | --- | --- |
| `ACTIONNAIRE` | obligatoire | Actionnaire unique qui prend la decision |
| `PRESIDENT` | obligatoire | Personne physique nommee President |
| `SIGNATAIRE` | obligatoire | En V1, l'actionnaire unique signe la decision |
| `SOCIETE_PRINCIPALE` | obligatoire | SELAS en cours de creation |
| `GERANT` | interdit | Role incompatible avec SELAS President |
| `DIRECTEUR_GENERAL` | bloque | Non trouve NotebookLM V1 ; source raw non qualifiee |
| `MANDATAIRE` | hors document | Ne pas confondre avec la procuration `DOC-003` |

Regle de reutilisation :

- en actionnaire unique seulement, le praticien peut alimenter explicitement
  `ACTIONNAIRE`, `PRESIDENT` et `SIGNATAIRE` ;
- cette reutilisation doit rester explicite dans le schema front/data ;
- hors actionnaire unique, aucun raccourci de role n'est autorise.

## Donnees minimales attendues

### Societe

- `societe.societe_principale.denomination`
- `societe.societe_principale.forme_sociale` = `SELAS`
- `societe.societe_principale.forme_sociale_longue`
- `societe.societe_principale.capital_social`
- `societe.societe_principale.siege.adresse.num_voie`
- `societe.societe_principale.siege.adresse.voie`
- `societe.societe_principale.siege.adresse.cp`
- `societe.societe_principale.siege.adresse.ville`

### Actionnaire unique

- `personne.actionnaire.genre`
- `personne.actionnaire.civilite_affichage`
- `personne.actionnaire.prenom`
- `personne.actionnaire.nom`
- `capital.actions.nombre_total`
- `capital.actions.repartition_actionnaires`

### President nomme

- `personne.president.genre`
- `personne.president.civilite_affichage`
- `personne.president.prenom`
- `personne.president.nom`
- `personne.president.date_naissance`
- `personne.president.lieu_naissance`
- `personne.president.nationalite`
- `personne.president.adresse_personnelle`
- `personne.president.fonction_affichage` = `President`

### Decision et signature

- `decision.date`
- `signature.lieu`
- `signature.date`

Champs non retenus comme obligatoires V1 sans source SELAS verrouillee :

- `signature.nombre_exemplaires`
- `reunion.heure`
- `reunion.date_lettres`
- quorum ;
- majorite ;
- droits de vote derogatoires.

## Blocages obligatoires

Le futur document doit rester bloque si :

- le dossier n'est pas `SELAS` ;
- il existe plus d'un actionnaire ;
- le President n'est pas renseigne ;
- le signataire n'est pas l'actionnaire unique en V1 ;
- le role `GERANT` est requis ou injecte ;
- un `DIRECTEUR_GENERAL` est demande ;
- la nomination du President est deja traitee dans les statuts sans besoin
  d'acte separe ;
- la source textuelle SELAS President n'est pas verrouillee.

Cas reserves hors V1 :

- multi-actionnaires ;
- actions de preference ;
- droits de vote ou financiers derogatoires ;
- Directeur General ;
- President personne morale ;
- micro-holding ;
- decision collective pluripersonnelle.

## Wording sensible

Termes obligatoires ou attendus pour un futur texte SELAS :

- `President`
- `actionnaire unique` si le document est bien unipersonnel ;
- `SELAS` ou forme longue SELAS si la source le demande.

Termes interdits dans le futur texte SELAS V1 :

- `gerant`
- `gerants`
- `SELARL`
- `parts sociales`
- toute mention de Directeur General.

Termes a manier avec source :

- `assemblee generale` ;
- `proces-verbal` ;
- `associe` au lieu de `actionnaire` ;
- `actions` et numerotation des actions.

Decision : ne pas inventer une formule juridique nouvelle. Si la source SELAS
utilise une formulation precise, elle devra etre reprise dans une spec texte
dediee avant code.

## Tests attendus pour le futur ticket code

Le futur ticket `SELAS-DECISION-PRESIDENT-001` devra au minimum verifier :

1. le schema exige `ACTIONNAIRE`, `PRESIDENT`, `SIGNATAIRE` et
   `SOCIETE_PRINCIPALE` ;
2. le document bloque si `GERANT` ou `DIRECTEUR_GENERAL` apparait ;
3. le document bloque si plusieurs actionnaires sont fournis ;
4. le document bloque si le choix statuts/decision separee est inconnu ;
5. le texte genere ne contient pas `SELARL`, `gerant`, `parts sociales` ;
6. le texte genere mentionne le President selon la source validee ;
7. le signataire est l'actionnaire unique dans le cas V1 ;
8. aucun pack DOCX/PDF/ZIP SELAS n'est active par ce ticket.

## Impact front/data

Le schema front SELAS contient deja un candidat :

```text
SELAS-DECISION-PRESIDENT
```

Cette spec confirme le code de travail, mais ne valide pas encore :

- un code moteur `DOC-XXX` final ;
- un generateur ;
- une sortie DOCX ;
- un branchement orchestrateur ;
- un pack SELAS.

Mise a jour recommandee au futur ticket front/data :

- remplacer l'ambiguite `selas_decision_president_canonical_code` par un blocage
  plus precis : `selas_decision_president_source_text_lock` ;
- ajouter le champ `decision.date` ;
- ajouter un champ ou une option `president.nomination_mode` avec au minimum :
  `statuts`, `decision_separee`, `inconnu`.

## Decision de sortie

`SELAS-SPEC-DECISION-PRESIDENT-001` est suffisant pour cadrer le document, mais
ne donne pas de `GO dev`.

Prochaine action recommandee :

```text
SELAS-SPEC-STATUTS-MEDECIN-AU-001
```

Raison : il faut savoir si la nomination du President est portee par les statuts
ou par une decision separee avant de coder ce document.
