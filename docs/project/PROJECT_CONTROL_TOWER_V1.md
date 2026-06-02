# Tour de controle projet V1

Date : 2026-06-02

## Objet

Ce document est la tour de controle du projet SYDEL.

Il fixe le role de Codex comme chef de projet / chef de produit global. Codex ne
doit pas seulement executer le prochain message utilisateur : il doit savoir ou
en est le projet, quel sprint est actif, quelle etape est autorisee, quelle etape
est interdite, et quoi faire ensuite.

Ce document ne remplace pas :

- `docs/project/01_EXECUTION_BOARD.md` pour les tickets ;
- `docs/project/04_LAST_STATE.md` pour le dernier etat reprenable ;
- `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md` pour le protocole court Naomie ;
- `docs/sprints/SPRINT_[TYPE]_V1.md` pour l'etat detaille d'un sprint ;
- `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` pour la methode.

Il les coordonne.

## Regle centrale

```text
Codex est responsable de la continuite projet.
```

Avant toute reponse operationnelle, Codex doit identifier :

1. qui parle : Gad, Naomie, associe indirect, autre ;
2. le type d'entreprise concerne ;
3. le sprint actif ou a ouvrir ;
4. la phase courante ;
5. la seule action autorisee maintenant ;
6. les actions interdites tant que les gates ne sont pas passes.

Si Codex ne peut pas repondre a ces six points, il doit rester en cadrage et ne
pas developper.

## Niveaux de pilotage

| Niveau | Source de verite | Role |
| --- | --- | --- |
| Projet global | `PROJECT_CONTROL_TOWER_V1.md` + `04_LAST_STATE.md` | Savoir ou en est le projet entier |
| Sprint type entreprise | `docs/sprints/SPRINT_[TYPE]_V1.md` | Suivre un type d'entreprise de bout en bout |
| Sous-sprint | journal ou protocole dedie | Gerer une etape specialisee, ex. NotebookLM |
| Ticket | `01_EXECUTION_BOARD.md` | Encadrer une action bornee |
| Validation humaine | retour Gad / associe | Autoriser la suite ou les corrections |

## Cycle standard pour chaque type d'entreprise

Ce cycle est le meme pour SELARL, SELAS et tous les futurs types d'entreprise.

| Etape | Nom | Responsable pilote | Sortie obligatoire | Peut passer a la suite si |
| --- | --- | --- | --- | --- |
| 0 | Etat initial du type | Codex PM | statut courant du type | Codex sait ce qui existe/deja fait |
| 1 | Ouverture sprint | Codex PM + Gad/Naomie | fichier `SPRINT_[TYPE]_V1.md` | sprint en `NO-GO dev` |
| 2 | Sources de reference | Codex PM | sources listees et hierarchisees | sources et trous connus |
| 3 | Sous-sprint NotebookLM | Codex PM + Naomie si pilote | prompts + reponses structurees | couverture suffisante documentee |
| 4 | Audit reutilisation | Reuse Auditor sous Codex PM | matrice reuse | decisions `identique/reuse-check/adapter/no-go` |
| 5 | Matrice documentaire | Codex PM | documents classes par condition | manuels/reserves/bloques visibles |
| 6 | Parcours metier/front | Product + Front sous Codex PM | contrat metier-front | donnees, roles, blocages definis |
| 7 | Tickets sprint | Codex PM | tickets ordonnes + criteres | premier ticket borne |
| 8 | Validation Gad | Gad | `GO dev ticket X` ou `NO-GO dev` | accord explicite de Gad |
| 9 | Dev limite | Codex dev | code + tests du ticket | tests et scope respectes |
| 10 | Smoke interne | QA sous Codex PM | DOCX/ZIP/PDF si dispo + rapport | pas de regressions bloquantes |
| 11 | Revue associe | Associe via Gad/Naomie | retour humain classe | retours compris |
| 12 | Corrections | Codex PM + dev | tickets correction | retours traites ou reportes |
| 13 | Cloture sprint | Codex PM | statut canonique final | sprint reprenable et auditable |

Regle : aucune etape ne saute par-dessus la precedente. Si une etape est
incomplete, Codex doit dire `NO-GO dev` et donner l'action exacte suivante.

## Registre courant des sprints

| Type | Sprint | Pilote metier | Branche | Phase courante | Statut | Action autorisee maintenant |
| --- | --- | --- | --- | --- | --- | --- |
| SELARL | Sprint pilote historique / production partielle | Gad | `track-b/clean-rebuild` | Revue humaine / consolidation | PARTIAL | preparer revue associe/juriste ou choisir un sous-cas unique avec `GO dev` |
| SELAS | `SPRINT-SELAS-V1` | Naomie | `codex/naomie-selas-sprint` | Human review pack SELAS | `WAITING_HUMAN_REVIEW` | transmettre le pack de revue ; aucun pack SELAS final valide |

## Etat courant SELARL

La SELARL est le modele de methode et le premier pack de production partielle.

Etat utile :

- creation simple medecin / chirurgien-dentiste generable ;
- regime communautaire partiellement traite avec `DOC-005` actif et `DOC-006`
  reserve ;
- multi-associes limite disponible sur certains sous-cas ;
- cession, SCM, derogations, site distinct, plusieurs gerants et statuts
  multi-associes complets restent a cadrer ;
- prochaine action recommandee : revue humaine associe/juriste ou choix d'un
  seul sous-cas avec `GO dev`.

SELARL ne doit pas etre consideree terminee a 100 % tant que la revue humaine
finale et les corrections eventuelles ne sont pas bouclees.

## Etat courant SELAS

La SELAS est le sprint actif de Naomie.

Etat utile :

- branche cible : `codex/naomie-selas-sprint` ;
- sprint : `docs/sprints/SPRINT_SELAS_V1.md` ;
- dernier ticket : `SELAS-HUMAN-REVIEW-PACK-001` realise en `DONE_WAITING_HUMAN_REVIEW` ;
- dernier ticket code : `SELAS-ORCHESTRATOR-PACK-001` en `DONE_PARTIAL_QA` ;
- tickets codes precedents : `SELAS-DOC001-DNC-PRESIDENT-001` et `SELAS-DOC003-PROCURATION-PRESIDENT-001` en `DONE_PARTIAL_QA` ;
- spec President : `SELAS-SPEC-PRESIDENT-001` terminee ;
- spec Procuration : `SELAS-SPEC-PROCURATION-001` terminee ;
- spec DNC President : `SELAS-SPEC-DNC-PRESIDENT-001` terminee ; `DOC-001` reutilisable avec President signataire explicite et filiation obligatoire ;
- spec Domiciliation : `SELAS-SPEC-DOC002-DOMICILIATION-001` terminee ; `DOC-002` reutilisable comme document neutre seulement si domiciliation = siege/cabinet ;
- spec Decision President : `SELAS-SPEC-DECISION-PRESIDENT-001` terminee ; `DOC-004` est seulement un patron structurel et l'acte separe reste reserve car la nomination President est absorbee par les statuts V1 ;
- spec Statuts SELAS medecin AU : `SELAS-SPEC-STATUTS-MEDECIN-AU-001` terminee ; `DOC-018` est le candidat V1 pour actionnaire unique / President unique, nomination President absorbee par les statuts, DG nomme et cas complexes bloques ;
- spec Capital / Actions : `SELAS-SPEC-CAPITAL-ACTIONS-001` terminee ; actions ordinaires uniquement, actionnaire unique 100 %, droits proportionnels et numerotation simple derivee `1 a N` ;
- spec Ordre : `SELAS-SPEC-ORDRE-001` terminee ; `DOC-034` reutilisable via overlay SELARL/SELAS, `Monsieur le President` rattache au Conseil de l'Ordre et non au President SELAS, plans/devis traites comme pieces attendues non generees ;
- spec Regime communautaire : `SELAS-SPEC-REGIME-COMMUNAUTAIRE-001` terminee ; `DOC-005` et `DOC-006` sont conditionnels si regime communautaire ;
- ticket dev borne DOC-005/DOC-006 : `SELAS-DOC005-DOC006-REGIME-COMMUNAUTAIRE-001` code ; schema SELAS aligne, `DOC-006` sorti de reserve, tests cibles ajoutes, smoke manuel DOCX OK ;
- ticket dev borne DOC-018 : `SELAS-DOC018-STATUTS-MEDECIN-AU-001` code ; verrous capital/actions et cas hors V1 ajoutes, `DOC-004` non selectionne si nomination President absorbee par les statuts, smoke manuel DOCX OK ;
- ticket readiness pack : `SELAS-FRONT-READINESS-PACK-001` code ; pack simple/conditionnel/reserve expose cote front/data, generation pack toujours inactive, prochain ticket `SELAS-ORCHESTRATOR-PACK-001` ;
- ticket orchestration pack : `SELAS-ORCHESTRATOR-PACK-001` code ; selection explicite du pack SELAS V1, batch regime communautaire conditionnel et blocage des cas hors V1 ;
- ticket smoke happy path : `SELAS-SMOKE-HAPPY-PATH-001` realise ; pack simple sans regime communautaire genere en DOCX avec `DOC-001`, `DOC-002`, `DOC-003`, `DOC-034`, `DOC-018`, sans `DOC-004`, `DOC-005`, `DOC-006` ni documents complexes ;
- ticket smoke regime communautaire : `SELAS-SMOKE-REGIME-COMMUNAUTAIRE-001`
  realise ; pack conditionnel genere en DOCX avec `DOC-001`, `DOC-002`,
  `DOC-003`, `DOC-034`, `DOC-018`, `DOC-005`, `DOC-006`, sans `DOC-004`,
  cession, SCM, bail, derogations ni documents reserves ;
- ticket anti-regression wording : `SELAS-ANTI-REGRESSION-WORDING-001`
  realise ; controle strict OK sur les deux packs, sans `SELARL`, `Gerant` ni
  `parts sociales`, avec occurrences `associe` classees pour le checkpoint
  trois sources ;
- ticket triple source check : `SELAS-TRIPLE-SOURCE-CHECK-001` realise ;
  source metier et NotebookLM alignes sur le perimetre SELAS V1, retour Gad
  strategie pris en compte, retour humain pack complet encore absent ;
- ticket human review pack : `SELAS-HUMAN-REVIEW-PACK-001` realise ; pack de
  revue humaine, ZIP, inventaire, checklist, pre-check NotebookLM et questions
  de decision prets ; attente retour Gad / associe / juriste ;
- roadmap A-Z : `SELAS-ROADMAP-TO-COMPLETION-001` terminee ; ordre propose jusqu'a cloture SELAS V1, a envoyer a Gad pour validation avant tout nouveau dev ;
- gate trois sources : execute en QA partielle ; il autorise la preparation de
  revue humaine mais pas la cloture SELAS V1 ;
- ticket dev borne DOC-034 : `SELAS-DOC034-ORDRE-001` code ; schema SELAS aligne sur signataire/societe/ordre/mandataire/signature, tests cibles ajoutes, smoke manuel DOCX OK ;
- ticket dev borne DOC-001 : `SELAS-DOC001-DNC-PRESIDENT-001` code ; schema SELAS aligne sur President/Signataire/filiation/signature, tests cibles ajoutes, smoke manuel DOCX OK ;
- ticket dev borne DOC-002 : `SELAS-DOC002-DOMICILIATION-001` code ; schema SELAS aligne sur President/Signataire/Societe, capital, siege et reuse siege->domiciliation obligatoire, tests cibles ajoutes, smoke manuel DOCX OK ;
- socle front/data : `SELAS-FRONT-SCHEMA-001` implemente ;
- ticket dev borne : `SELAS-FRONT-SCHEMA-001`, valide oralement par Gad via `ok go` ;
- ticket dev borne DOC-003 : `SELAS-DOC003-PROCURATION-PRESIDENT-001` code ; `President` force pour SELAS, `Gerant` et `Directeur General` bloques ;
- sous-sprint NotebookLM : suffisant pour audit, journalise ;
- audit reutilisation : V1 realise dans `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md` ;
- matrice documentaire : V1 realisee dans `docs/sprints/SPRINT_SELAS_MATRIX_001.md` ;
- contrat metier-front : V1 realise dans `docs/sprints/SPRINT_SELAS_FRONT_CONTRACT_001.md` ;
- tickets SELAS : V1 realises dans `docs/sprints/SPRINT_SELAS_TICKETS_001.md` ;
- demande premier GO dev : preparee dans `docs/sprints/SPRINT_SELAS_GO_DEV_FIRST_TICKET_001.md` ;
- journal : `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` ;
- prompt source : `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md` ;
- action courante : transmettre le pack de revue humaine, puis attendre le retour humain classe.
- protocole court obligatoire : `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`.

Interdits actuels SELAS :

- production ;
- generation ;
- generation documentaire ;
- matrice finale generable ;
- push de fonctionnalite ;
- wording juridique non specifie.

Le code front/data borne est autorise uniquement pour le ticket deja valide.
Les actions ci-dessus restent interdites sans spec documentaire et validation
humaine.

## Fail-safe branche main

Si Naomie arrive dans un environnement qui indique la branche `main`, Codex doit
considerer que le contexte de sprint n'est pas encore correctement place.

Le nom du dossier local ne suffit pas a diagnostiquer. `sydel-track-b` est le
nom du worktree utilise par Gad ; `sydel-document-engine` peut etre le nom normal
d'un clone chez Naomie. Le diagnostic correct est :

- remote GitHub attendu : `https://github.com/GadrTibi/sydel-document-engine.git` ;
- branche attendue pour Naomie/SELAS : `codex/naomie-selas-sprint`.

Action obligatoire :

1. tenter de basculer sur `codex/naomie-selas-sprint` ;
2. si la bascule est impossible, bloquer en `NO-GO dev` ;
3. expliquer a Naomie qu'elle n'a pas a gerer Git, et que Codex doit recuperer ou
   ouvrir la branche de sprint ;
4. ne jamais lui demander de choisir une tache ou un ticket depuis `main`.

## Routine obligatoire au debut d'une reprise

Quand un nouveau chat ou une nouvelle demande arrive, Codex doit faire cette
lecture mentale avant d'agir :

```text
Projet : SYDEL document engine.
Tour de controle : PROJECT_CONTROL_TOWER_V1.md.
Sprint actif Naomie : SELAS.
Phase SELAS : Human review pack SELAS.
Action SELAS : transmettre le pack de revue humaine, puis garder les corrections humaines avant cloture.
Pack SELAS : interdit.
SELARL : production partielle, prochaine action revue humaine ou sous-cas borne.
```

Si la demande concerne Naomie, Codex doit repondre en format sprint :

```text
Statut sprint : [phase] / [statut]
Action maintenant : [une seule action]
Point pedagogie : [explication courte]
Prochaine etape : [suite immediate]
```

Si la demande est un simple `bonjour`, Codex doit reprendre la phase courante
du sprint SELAS et donner l'action exacte suivante. Il ne doit pas revenir au
Prompt NotebookLM 01 si cette phase est deja terminee.

## Reponse attendue si Naomie lance SELAS

Si Naomie dit :

```text
Bonjour, je suis Naomie.
Je veux lancer le sprint SELAS.
```

Codex doit repondre :

```text
Statut sprint : [phase courante dans SPRINT_SELAS_V1.md] / NO-GO dev
Action maintenant : [action courante dans SPRINT_SELAS_V1.md]
Point pedagogie : Codex protege l'ordre du sprint ; Naomie n'a pas a gerer Git, les commandes ou les gates juridiques.
Prochaine etape : [prochaine etape indiquee par le fichier de sprint]
```

Si la phase courante est encore NotebookLM, Codex donne le prompt NotebookLM
courant. Si la phase a avance, Codex ne relance pas le Prompt 01 par defaut.

## Mise a jour obligatoire

Codex doit mettre a jour cette tour de controle quand :

- un sprint change de phase ;
- un nouveau sprint de type d'entreprise est ouvert ;
- un sprint est cloture, reporte ou bloque ;
- le sprint actif de Naomie change ;
- Gad donne ou retire un `GO dev` ;
- l'associe donne un retour qui change le statut.

En fin de ticket, Codex doit aussi mettre a jour :

- `docs/project/01_EXECUTION_BOARD.md` ;
- `docs/project/04_LAST_STATE.md` ;
- le fichier de sprint actif.

## Definition de reprise correcte

Une reprise correcte est possible si un nouveau chat peut lire ce document et
repondre sans demander a Gad :

- quel sprint est actif ;
- qui le pilote ;
- quelle branche utiliser ;
- quelle etape est en cours ;
- quelle est la prochaine action exacte ;
- ce qui est interdit tant que le gate n'est pas passe.
