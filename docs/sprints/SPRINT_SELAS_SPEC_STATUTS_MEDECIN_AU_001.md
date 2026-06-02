# SELAS-SPEC-STATUTS-MEDECIN-AU-001

Date : 2026-06-02

Statut : `DONE - specification V1`

Decision sprint : `GO spec` mais `NO-GO pack SELAS`

## Objet

Specifier le perimetre V1 des statuts :

```text
SELAS medecin, actionnaire unique, President unique, creation simple.
```

Ce ticket ne code rien. Il verrouille seulement :

- la source documentaire exploitable ;
- le document canonique cible ;
- les conditions d'automatisation V1 ;
- les donnees minimales ;
- les cas a bloquer ;
- les criteres de recette du futur ticket de code.

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
- `docs/sprints/SPRINT_SELAS_SPEC_DECISION_PRESIDENT_001.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`
- `project/source_documents/lot_04/Statuts_SELAS_medecin.docx`
- `src/sydel_doc_engine/generators/lot_04/statuts_selas_medecin.py`
- `src/sydel_doc_engine/generators/lot_04/statuts_sel_exercice_common.py`
- `src/sydel_doc_engine/generators/lot_04/statuts_sel_exercice_templates.py`
- `tests/unit/test_lot_04_statuts_sel_exercice.py`
- `tests/unit/test_selas_front_schema.py`

ADR applicables :

- ADR-0001 : source de verite documentaire.
- ADR-0002 : moteur par document canonique.
- ADR-0004 : generation DOCX propre from-scratch.
- ADR-0005 : travail Codex repo-first et petits tickets.

## Decision principale

Le document canonique cible est :

```text
DOC-018 - Statuts SELAS medecin
```

Decision V1 :

- le modele source `Statuts_SELAS_medecin.docx` est recu ;
- le document est deja rattache a l'overlay `selas_medecin` ;
- les statuts SELAS medecin sont codables uniquement pour le cas actionnaire
  unique / President unique / creation simple ;
- le futur ticket de code doit rester borne a `DOC-018` ;
- aucun pack SELAS complet ne doit etre active par ce seul ticket ;
- aucune formulation SELARL ne doit etre substituee automatiquement dans ces
  statuts ;
- le wording source est conserve strictement, sauf note de validation explicite.

## Lien avec la decision President

Le ticket `SELAS-SPEC-DECISION-PRESIDENT-001` avait laisse ouvert le choix :

```text
President nomme dans les statuts
ou
President nomme dans un acte separe
```

Lecture de la source statuts SELAS medecin :

- les statuts contiennent une mention d'acceptation des fonctions de
  `[fonction_dirigeant]` ;
- le generateur existant consomme `ctx.dirigeant_nomine` ;
- la source Lot 4 indique que l'overlay SELAS medecin contient `president`,
  `directeurs generaux` et `duree de mandat`.

Decision V1 :

- pour le parcours simple, la nomination / acceptation du President est portee
  par les statuts `DOC-018` ;
- le document de travail `SELAS-DECISION-PRESIDENT` reste reserve / conditionnel ;
- aucun acte separe de nomination du President n'est genere en V1 tant qu'une
  source texte distincte n'est pas verrouillee.

## Directeur General

Point sensible :

- les reponses NotebookLM V1 ne donnent pas de role operationnel de Directeur
  General a automatiser ;
- la source des statuts SELAS medecin contient des clauses generales sur les
  directeurs generaux.

Decision V1 :

- les clauses generales presentes dans la source statuts peuvent rester dans
  `DOC-018` parce qu'elles appartiennent au wording source ;
- aucune nomination effective d'un Directeur General n'est automatisee ;
- aucun role `DIRECTEUR_GENERAL` ne doit etre requis par le schema SELAS V1 ;
- tout dossier demandant de renseigner ou nommer un Directeur General reste
  bloque hors V1.

## Conditions d'apparition V1

`DOC-018` peut etre candidat seulement si toutes les conditions suivantes sont
vraies :

- dossier `SELAS` ;
- profession `medecin` ;
- overlay statuts `selas_medecin` ;
- un seul actionnaire ;
- actionnaire personne physique ;
- President personne physique ;
- President identique a l'actionnaire unique ou deja signataire comme associe ;
- pas de Directeur General nomme ;
- pas de droits de vote ou financiers derogatoires ;
- pas d'actions de preference ;
- pas de demembrement ;
- pas de micro-holding / personne morale associee ;
- second lieu absent ou completement renseigne ;
- source wording conservee.

## Roles canoniques

| Role | Statut V1 | Regle |
| --- | --- | --- |
| `ACTIONNAIRE` | obligatoire | Actionnaire unique qui detient les actions |
| `PRESIDENT` | obligatoire | Dirigeant SELAS, fonction affichee fournie et validee |
| `SIGNATAIRE` | obligatoire | En V1, meme personne que l'actionnaire unique |
| `SOCIETE_PRINCIPALE` | obligatoire | SELAS en formation |
| `ORDRE` | obligatoire | Ordre des medecins pour inscription et mentions statutaires |
| `BANQUE` | obligatoire | Banque de depot des fonds |
| `GERANT` | interdit | Role incompatible avec SELAS |
| `DIRECTEUR_GENERAL` | bloque | Pas de nomination DG automatisee V1 |

Regle de reutilisation :

- le praticien peut alimenter `ACTIONNAIRE`, `PRESIDENT` et `SIGNATAIRE` dans le
  cas actionnaire unique ;
- cette reutilisation doit rester explicite cote front/data ;
- hors actionnaire unique, aucun raccourci de role n'est autorise.

## Donnees minimales attendues

### Societe

- `societe.societe_principale.denomination`
- `societe.societe_principale.forme_sociale` = `SELAS`
- `societe.societe_principale.forme_sociale_complete`
- `societe.societe_principale.forme_sociale_abregee`
- `societe.societe_principale.capital_social`
- `societe.societe_principale.capital_social_lettres`
- `societe.societe_principale.duree`
- `societe.societe_principale.siege.adresse`

### Actionnaire unique / praticien

- `personne.actionnaire.genre`
- `personne.actionnaire.civilite_affichage`
- `personne.actionnaire.prenom`
- `personne.actionnaire.nom`
- `personne.actionnaire.profession`
- `personne.actionnaire.profession_reglementee`
- `personne.actionnaire.profession_reglementee_pluriel`
- `personne.actionnaire.titre_professionnel`
- `personne.actionnaire.qualification_principale`
- `personne.actionnaire.date_naissance`
- `personne.actionnaire.ville_naissance`
- `personne.actionnaire.departement_naissance`
- `personne.actionnaire.nationalite`
- `personne.actionnaire.adresse_personnelle`
- `personne.actionnaire.situation_maritale`
- `personne.actionnaire.regime_matrimonial`
- `personne.actionnaire.qualite`
- `personne.actionnaire.numero_rpps`
- `personne.actionnaire.numero_ordre`

### Conjoint

La source actuelle consomme un bloc conjoint dans la comparution.

Donnees requises si le wording source reste tel quel :

- `personne.actionnaire.conjoint.civilite_affichage`
- `personne.actionnaire.conjoint.prenom`
- `personne.actionnaire.conjoint.nom`

Point ouvert :

- si le parcours doit couvrir un praticien non marie ou sans conjoint affiche
  dans les statuts, il faut un ticket separe pour valider le wording de
  comparution alternatif.

### Capital / actions

- `capital.montant`
- `capital.montant_lettres`
- `capital.actions.nombre_total`
- `capital.actions.nombre_total_lettres`
- `capital.actions.valeur_nominale`
- `capital.actions.valeur_nominale_lettres`
- `capital.actions.repartition_actionnaires`
- `capital.apport_numeraire`
- `capital.apport_numeraire_lettres`

Regles V1 :

- le capital est divise en actions ;
- la somme des actions attribuees doit correspondre au nombre total d'actions ;
- la valeur nominale multipliee par le nombre d'actions doit correspondre au
  capital social ;
- la numerotation complexe des actions reste hors V1 tant que le ticket
  `SELAS-SPEC-CAPITAL-ACTIONS-001` n'est pas tranche.

### Banque

- `banque_depot.nom`
- `banque_depot.adresse`

### Exercice / lieux

- `exercice.lieux[0].adresse_affichee`
- `exercice.debut_exercice`
- `exercice.fin_exercice`
- `exercice.date_cloture_premier_exercice`

Second lieu :

- `exercice.lieux[1].nom`
- `exercice.lieux[1].adresse_affichee`

Regle :

- si un seul champ du second lieu est fourni, la generation doit bloquer ;
- si aucun second lieu n'est fourni, la ligne source du second lieu est omise.

### President

- `personne.president.prenom`
- `personne.president.nom`
- `personne.president.adresse_personnelle`
- `personne.president.fonction_affichage` = `President`
- `personne.president.duree_mandat`

Regle :

- `fonction_affichage` est une donnee validee ;
- le generateur ne deduit pas automatiquement `Presidente` depuis le genre.

### Signature

- `signature.lieu`
- `signature.date`
- `signature.prestataire_signature_electronique`

## Blocages obligatoires

Le futur code `DOC-018` doit bloquer si :

- le dossier n'est pas `SELAS` ;
- l'overlay n'est pas `selas_medecin` ;
- il y a plusieurs actionnaires ;
- l'actionnaire est une personne morale ;
- le President n'est pas l'actionnaire unique ou requiert une signature separee ;
- un Directeur General est demande ou doit etre nomme ;
- une action de preference est demandee ;
- les droits de vote ou financiers divergent de la repartition du capital ;
- il existe un demembrement ;
- la numerotation des actions est complexe ou non tranchee ;
- le second lieu est partiellement renseigne ;
- un bloc conjoint est necessaire mais incomplet ;
- la sortie attendue serait une SELAS dentiste ;
- la source demande une correction de wording non documentee.

Cas reserves hors V1 :

- multi-actionnaires ;
- President non associe ;
- Directeur General ;
- actions de preference ;
- droits derogatoires ;
- demembrement ;
- micro-holding ;
- cession de fonds liberal ;
- SCM ;
- site distinct avec demande de derogation ;
- statuts SELAS dentiste.

## Wording sensible

Termes attendus dans le futur rendu SELAS :

- `Société d'exercice libéral par actions simplifiée` ou graphie source ;
- `SELAS` ;
- `actions` ;
- `President` / graphie source ;
- `associe unique` si la source le prevoit.

Termes interdits comme fonction ou forme sociale cible :

- `Gerant`
- `gerant`
- `SELARL`
- `parts sociales`

Nuance :

- le mot `president` peut exister dans certaines expressions legales generiques
  hors fonction de dirigeant ; les tests devront cibler les erreurs de role et
  de forme sociale, pas corriger le wording source.
- les clauses generales sur les directeurs generaux restent source-validees,
  mais ne creent aucun role DG a collecter.

## Reutilisation technique

Reutilisable :

- l'architecture `statuts_sel_exercice` ;
- le document `DOC-018` existant ;
- l'overlay `selas_medecin` ;
- les helpers communs de statuts SEL ;
- le verrou second lieu deja arbitre ;
- la logique de blocage multi-associes V1 ;
- le schema front SELAS comme point d'entree, sous reserve d'ajouter les champs
  statutaires manquants.

Non reutilisable tel quel :

- `DOC-004 - PV nomination gerant` comme document de nomination President ;
- les statuts SELARL medecin ;
- les statuts SELARL dentiste ;
- une transformation automatique `parts -> actions` ou `gerant -> President`
  sur un texte SELARL.

## Tests attendus pour le futur ticket code

Le futur ticket `SELAS-DOC018-STATUTS-MEDECIN-AU-001` devra au minimum verifier :

1. `DOC-018` est selectionne seulement pour `SELAS` + `selas_medecin` ;
2. le rendu contient la forme SELAS et les actions ;
3. le rendu ne transforme pas une source SELARL ;
4. le rendu ne contient pas `SELARL` comme forme cible ;
5. le rendu ne contient pas `parts sociales` dans le capital ;
6. la fonction dirigeante fournie est reprise telle quelle ;
7. le cas multi-actionnaires bloque ;
8. le President non associe avec signature separee bloque ;
9. le Directeur General nomme bloque ;
10. le second lieu absent est accepte ;
11. le second lieu complet est rendu ;
12. le second lieu partiel bloque ;
13. le capital bloque si nombre d'actions, valeur nominale et montant ne
    correspondent pas ;
14. la generation du pack SELAS reste inactive sans gate separe ;
15. le document `SELAS-DECISION-PRESIDENT` reste non genere si la nomination est
    absorbee par les statuts.

## Decision finale

`DOC-018 - Statuts SELAS medecin` est le bon candidat de statuts pour le sprint
SELAS V1.

Le futur developpement est possible seulement sur un ticket borne :

```text
SELAS-DOC018-STATUTS-MEDECIN-AU-001
```

Mais il reste prudent de traiter avant lui le ticket :

```text
SELAS-SPEC-CAPITAL-ACTIONS-001
```

Raison : le capital en actions, le nombre d'actions, la valeur nominale et la
numerotation sont les variables les plus sensibles des statuts SELAS.
