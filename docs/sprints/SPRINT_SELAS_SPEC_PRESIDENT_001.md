# SELAS spec president 001

Date : 2026-06-01

Ticket : `SELAS-SPEC-PRESIDENT-001`

Statut : `DONE - spec metier`

Decision sprint : `NO-GO generation`

## Objet

Specifier le role `President` pour le parcours SELAS V1 avant tout document
juridique.

Ce livrable ne code rien, ne genere aucun DOCX/PDF/ZIP et ne valide aucun
wording juridique final. Il fixe le contrat metier minimal commun aux documents
candidats qui consomment le dirigeant SELAS.

## Sources et livrables lus

- `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`
- `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md`
- `docs/sprints/SPRINT_SELAS_MATRIX_001.md`
- `docs/sprints/SPRINT_SELAS_FRONT_CONTRACT_001.md`
- `docs/sprints/SPRINT_SELAS_TICKETS_001.md`
- `docs/delivery/lot_01_analysis_and_specs_v1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`
- `src/sydel_doc_engine/front_data/selas_schema.py`

## Perimetre V1

Inclus :

- structure : `SELAS` ;
- profession active du premier parcours : medecin ;
- creation simple ;
- actionnaire unique ;
- president unique ;
- president personne physique ;
- president rattache au praticien seulement par reuse explicite ;
- signataire principal pouvant etre le president ;
- mandataire formalites distinct.

Exclus :

- directeur general ;
- president personne morale ;
- plusieurs presidents ;
- plusieurs actionnaires ;
- micro-holding ou personne morale associee ;
- actions de preference ;
- cession fonds/cabinet ;
- SCM ;
- derogation/site distinct ;
- statuts SELAS dentiste.

## Decision metier centrale

Pour le parcours SELAS V1, le dirigeant documentaire est le `President`.

Le moteur/front ne doit pas convertir silencieusement un `gerant` SELARL en
`president` SELAS. La reutilisation est autorisee au niveau des donnees
personne, adresse, signature et roles explicites, pas au niveau du wording
juridique.

## Roles canoniques

| Role | Cible | Statut V1 | Notes |
| --- | --- | --- | --- |
| `praticien` | Personne physique | Reutilisable | Fiche pivot client |
| `actionnaire` | Personne physique ou morale | V1 personne physique uniquement | Detenteur des actions ; distinct du president meme si meme personne |
| `president` | Personne physique | Obligatoire | Dirigeant SELAS V1 |
| `signataire` | Personne physique | Obligatoire par document | Peut pointer vers le president via assignment explicite |
| `mandataire` | Personne ou societe | Obligatoire pour procuration/ordre | Ne jamais confondre avec signataire |
| `conjoint` | Personne physique | Conditionnel | Seulement si regime communautaire retenu |
| `directeur_general` | Non modelise | Bloque | Non trouve dans NotebookLM V1 pour le parcours simple |

## Reutilisations autorisees

Dans le parcours actionnaire unique / president unique uniquement :

- `praticien -> actionnaire` : autorise par regle explicite ;
- `praticien -> president` : autorise par regle explicite ;
- `praticien -> signataire` : autorise par regle explicite ;
- `president -> signataire` : autorise seulement par assignment document ou lot ;
- `president -> mandataire` : interdit par defaut ;
- `actionnaire -> president` : non automatique, meme si la meme personne porte
  les deux roles.

Cette separation est volontaire : elle evite qu'un meme nom dans l'interface
cree une confusion juridique dans les actes.

## Variables minimales President

Champs requis pour la fiche `president` :

- civilite d'affichage ;
- genre grammatical ;
- prenom ;
- nom ;
- date de naissance ;
- lieu de naissance ;
- nationalite ;
- adresse personnelle ;
- profession ;
- email de signature ;
- telephone portable de signature.

Champs a confirmer avant automatisation documentaire :

- filiation complete pour la DNC (`nom_pere`, `nom_mere`) ;
- fonction exacte a afficher au feminin, le cas echeant ;
- date de nomination si differente de la date de signature ;
- duree du mandat si elle n'est pas dans les statuts ;
- formule exacte d'acceptation des fonctions.

## Documents impactes

| Document | Code | Role president | Decision spec president |
| --- | --- | --- | --- |
| DNC president | `DOC-001` | Personne declarant la non-condamnation | `reuse-check`, mais filiation a arbitrer dans `SELAS-SPEC-DNC-PRESIDENT-001` |
| Procuration president | `DOC-003` | Signataire / dirigeant de la societe | `adapter`, spec wording obligatoire dans `SELAS-SPEC-PROCURATION-001` |
| Decision / PV nomination president | A definir | Personne nominee president | Nouveau cadrage requis dans `SELAS-SPEC-DECISION-PRESIDENT-001` |
| Statuts SELAS medecin | `DOC-018` | President nomme ou mentionne dans les statuts | `adapter`, source/statuts a verrouiller dans `SELAS-SPEC-STATUTS-MEDECIN-AU-001` |
| Demande d'inscription a l'Ordre | `DOC-034` | Signataire ou dirigeant selon modele | `reuse-check`, mandataire/ordre a confirmer dans `SELAS-SPEC-ORDRE-001` |
| Regime communautaire | `DOC-005` / `DOC-006` | Eventuelle fonction affichee | Hors present ticket ; arbitrage dedie requis |

## Regles par document

### DOC-001 - DNC president

Regles :

- le document reste centre sur une personne physique ;
- la personne est le president, pas un gerant ;
- la filiation complete est deja obligatoire dans la spec Lot 1 existante ;
- NotebookLM n'a pas confirme la filiation comme champ SELAS source.

Decision :

- ne pas supprimer la filiation du schema existant ;
- ne pas promettre une DNC SELAS complete avant arbitrage ;
- ouvrir `SELAS-SPEC-DNC-PRESIDENT-001`.

### DOC-003 - Procuration president

Regles :

- la procuration existante consomme `fonction_dirigeant` ;
- pour SELAS V1, la fonction attendue est `President` ;
- le mandataire reste distinct du signataire ;
- le bloc mandataire SYDEL reste une configuration a ne pas deduire du president.

Decision :

- ne pas faire de remplacement global `gerant -> president` ;
- utiliser un champ canonique de fonction dirigeant, resolu par structure ;
- ouvrir `SELAS-SPEC-PROCURATION-001` pour le texte exact.

### Decision / PV nomination president

Regles :

- le PV nomination gerant existant est une famille mutualisable, mais sa spec
  canonique fixe par defaut la fonction `gerant` ;
- SELAS exige une variante president ;
- en actionnaire unique, le formalisme cible est une decision de l'actionnaire
  unique plutot qu'un PV d'assemblee pluripersonnelle ;
- la pluralite d'actionnaires reste hors V1.

Decision :

- creer un document canonique SELAS a specifier, avec code a arbitrer ;
- ne pas reutiliser directement `DOC-004` sans spec textuelle SELAS ;
- ouvrir `SELAS-SPEC-DECISION-PRESIDENT-001`.

### DOC-018 - Statuts SELAS medecin

Regles :

- le president peut etre nomme dans les statuts ou dans une decision separee ;
- le sprint ne doit pas choisir implicitement entre ces deux voies ;
- toute mention `gerant` est incompatible avec le parcours SELAS ;
- le directeur general reste bloque.

Decision :

- le schema front peut collecter `president` ;
- la generation des statuts reste bloquee tant que la source/spec ne tranche pas
  la nomination du president ;
- ouvrir `SELAS-SPEC-STATUTS-MEDECIN-AU-001`.

### DOC-034 - Ordre

Regles :

- la spec ordre existante indique des variantes SELARL/SELAS proches ;
- le mandataire est configurable dans les variantes SELARL/SELAS ;
- le `President` dans l'appel ordinal peut aussi designer le president du
  conseil de l'Ordre, pas le president de la SELAS.

Decision :

- ne pas confondre `president` SELAS et `Monsieur le President` destinataire de
  l'Ordre ;
- garder `ordre_president_destinataire` hors du role `president` SELAS ;
- ouvrir `SELAS-SPEC-ORDRE-001`.

## Termes interdits / reserves

Interdits dans un parcours SELAS president V1 :

- `gerant` comme fonction du dirigeant SELAS ;
- `parts sociales` pour le capital SELAS ;
- `associe unique` comme libelle documentaire final si la source impose
  `actionnaire unique` ;
- `directeur general` sans source et ticket dedie.

Reserves :

- feminisation de `President` / `Presidente` : a valider dans les specs texte ;
- `associe` comme terme front transversal : tolere en UI historique seulement si
  le document final reste coherent ;
- nomination du president dans les statuts : a trancher avec la source statuts.

## Blocages V1

Le parcours doit bloquer si :

- plus d'un actionnaire est renseigne ;
- un directeur general est demande ;
- le president n'est pas une personne physique ;
- une personne morale ou micro-holding devient actionnaire ;
- les actions ont des droits derogatoires ;
- la nomination du president doit etre pluripersonnelle ;
- la source statuts SELAS medecin ne confirme pas la voie de nomination.

## Impacts sur le schema front/data

Le ticket `SELAS-FRONT-SCHEMA-001` a deja pose le socle compatible :

- `BusinessRole.ACTIONNAIRE` existe ;
- `BusinessRole.PRESIDENT` existe ;
- `PRATICIEN -> ACTIONNAIRE` est une reuse explicite ;
- `PRATICIEN -> PRESIDENT` est une reuse explicite ;
- les documents candidats gardent des ambiguites non resolues.

Cette spec confirme ce choix. Elle ne demande pas de changement de code
immediat.

## Criteres d'acceptation du present ticket

- le role president SELAS est distinct de gerant, actionnaire, signataire et
  mandataire ;
- le directeur general reste bloque ;
- les documents consommateurs du president sont listes ;
- les prochaines specs documentaires sont identifiees ;
- aucune generation documentaire n'est activee ;
- aucun wording juridique final n'est modifie.

## Prochain ticket recommande

`SELAS-SPEC-PROCURATION-001`

Raison : la procuration est le premier document ou le changement de fonction
`President` peut etre isole avec un risque faible, a condition de verifier le
texte et les tests anti-mentions `gerant` / `SELARL`.

## Decision de sortie

`SELAS-SPEC-PRESIDENT-001` est suffisant pour cadrer les tickets documentaires
suivants, mais il ne donne aucun `GO generation`.

Le sprint reste en `NO-GO generation`.
