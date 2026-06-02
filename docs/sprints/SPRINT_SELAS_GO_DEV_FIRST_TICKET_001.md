# SELAS GO dev first ticket 001

Date : 2026-06-01

Ticket : `SELAS-GO-DEV-FIRST-TICKET-001`

Statut : `DONE - demande d'arbitrage preparee`

Decision sprint : `NO-GO dev maintenu tant que Gad ne valide pas`

## Objet

Preparer la demande d'arbitrage Gad pour le premier ticket SELAS qui pourrait
recevoir un `GO dev` borne.

Ce livrable ne donne pas lui-meme le `GO dev`. Il formule la decision a obtenir.

## Recommandation Codex

Demander un `GO dev` uniquement pour :

```text
SELAS-FRONT-SCHEMA-001
```

Nature du ticket recommande :

- ticket front / schema de saisie uniquement ;
- aucun generateur documentaire ;
- aucun DOCX produit ;
- aucun PDF ;
- aucun ZIP ;
- aucune modification de wording juridique ;
- aucun branchement de documents SELAS en production.

Raison : le schema front peut afficher le parcours SELAS simple, les documents
candidats et les blocages sans prendre encore le risque de produire des actes
juridiques.

## Scope exact propose pour le premier dev

Le futur ticket `SELAS-FRONT-SCHEMA-001` devrait uniquement permettre de cadrer
visuellement et techniquement ce parcours :

```text
SELAS medecin, actionnaire unique, president unique, creation simple,
sans cession, sans SCM, sans derogation, sans site distinct,
sans directeur general, sans micro-holding, sans actions de preference,
hors multi-actionnaires.
```

## Ce que le `GO dev` autoriserait

Si Gad valide, le premier ticket dev pourra :

- ajouter le type dossier `SELAS` dans le schema front ou la couche de parcours ;
- limiter le parcours actif a `medecin` ;
- collecter les blocs de donnees definis dans
  `SPRINT_SELAS_FRONT_CONTRACT_001.md` ;
- modeliser les roles `praticien`, `actionnaire_unique`, `president`,
  `signataire`, `mandataire` et `conjoint` conditionnel ;
- afficher les documents candidats :
  - `DOC-001` DNC president ;
  - `DOC-002` domiciliation ;
  - `DOC-003` procuration president ;
  - Decision/PV president a specifier ;
  - `DOC-034` Ordre ;
  - `DOC-018` statuts SELAS medecin ;
  - `DOC-005` renonciation conjoint conditionnelle ;
- afficher les documents reserves ou bloques ;
- bloquer explicitement les cas hors V1 simple ;
- ajouter des tests sur la presence du parcours, des champs et des blocages.

## Ce que le `GO dev` n'autoriserait pas

Meme si Gad valide `SELAS-FRONT-SCHEMA-001`, il ne faut pas :

- generer un document SELAS ;
- adapter `DOC-001`, `DOC-002`, `DOC-003`, `DOC-005`, `DOC-018` ou `DOC-034` ;
- creer le document Decision/PV president ;
- modifier les sources DOCX ;
- modifier les textes juridiques ;
- promettre la SELAS chirurgien-dentiste ;
- ouvrir les cas multi-actionnaires ;
- traiter directeur general, cession, SCM, site distinct, derogation,
  micro-holding ou actions de preference ;
- rendre le pack SELAS exploitable juridiquement.

## Questions d'arbitrage a Gad

Decision principale :

```text
Gad valide-t-il un GO dev borne pour SELAS-FRONT-SCHEMA-001,
uniquement schema front SELAS simple, sans generation DOCX ?
```

Questions associees :

1. Le premier parcours est-il bien limite a `SELAS medecin actionnaire unique
   president unique` ?
2. L'interface doit-elle afficher `Actionnaire` pour SELAS, ou conserver
   `Associe` comme terme transversal hors documents ?
3. Les cas bloques doivent-ils etre visibles des le premier ticket ou seulement
   listes dans la documentation ?
4. Le bloc regime communautaire doit-il etre visible mais bloque/reserve tant
   que `DOC-005` et `DOC-006` ne sont pas arbitres ?
5. Les pieces Ordre plans/devis doivent-elles apparaitre comme pieces attendues
   des le schema front ?

## Decision attendue de Gad

Gad peut repondre par l'une des options suivantes :

| Option | Effet |
| --- | --- |
| `GO dev SELAS-FRONT-SCHEMA-001` | Codex peut ouvrir le premier ticket de dev front, sans generation DOCX |
| `GO cadrage supplementaire` | Codex reste en lecture seule et precise les specs demandees |
| `NO-GO dev` | Codex conserve le backlog et attend un arbitrage plus tard |
| `Changer premier ticket` | Codex reordonne le backlog selon la priorite donnee |

## Message pret a envoyer a Gad

```text
Gad, peut-on valider un GO dev strictement borne pour le ticket
SELAS-FRONT-SCHEMA-001 ?

Scope propose :
- SELAS medecin uniquement ;
- actionnaire unique ;
- president unique ;
- creation simple ;
- aucun DOCX, aucun PDF, aucun ZIP ;
- aucun wording juridique modifie ;
- aucun generateur SELAS branche ;
- uniquement schema front, champs, roles, documents candidats et blocages.

But : afficher le parcours SELAS simple et ses limites avant de coder les
documents.

Decision attendue :
1. GO dev SELAS-FRONT-SCHEMA-001 ;
2. GO cadrage supplementaire ;
3. NO-GO dev ;
4. Changer le premier ticket.
```

## Decision de sortie

`SELAS-GO-DEV-FIRST-TICKET-001` prepare la demande d'arbitrage.

Le sprint reste en `NO-GO dev`.

Prochaine etape : attendre la decision Gad. Si Gad donne explicitement
`GO dev SELAS-FRONT-SCHEMA-001`, Codex pourra lancer le ticket correspondant.
