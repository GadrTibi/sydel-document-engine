# Tour de controle projet V1

Date : 2026-06-01

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
| SELAS | `SPRINT-SELAS-V1` | Naomie | `codex/naomie-selas-sprint` | Sous-sprint NotebookLM | `NO-GO dev` | donner Prompt NotebookLM 01, attendre la reponse brute, structurer le journal |

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
- ticket actif : `SELAS-SOURCES-NOTEBOOKLM-001` ;
- sous-sprint actif : NotebookLM ;
- journal : `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` ;
- prompt source : `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md` ;
- action courante : donner Prompt 01, attendre la reponse brute, structurer,
  puis iterer.
- protocole court obligatoire : `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`.

Interdits actuels SELAS :

- production ;
- generation ;
- code ;
- matrice finale ;
- audit reutilisation ;
- push de fonctionnalite ;
- `GO dev`.

Ces actions restent interdites tant que le sous-sprint NotebookLM n'est pas
suffisant.

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
Phase SELAS : NotebookLM.
Action SELAS : prompt -> reponse -> journal -> prompt suivant.
Dev SELAS : interdit.
SELARL : production partielle, prochaine action revue humaine ou sous-cas borne.
```

Si la demande concerne Naomie, Codex doit repondre en format sprint :

```text
Statut sprint : [phase] / [statut]
Action maintenant : [une seule action]
Point pedagogie : [explication courte]
Prochaine etape : [suite immediate]
```

Si la demande est un simple `bonjour`, Codex doit quand meme donner le Prompt
NotebookLM 01 complet. Il ne doit pas attendre que Naomie choisisse une tache.

## Reponse attendue si Naomie lance SELAS

Si Naomie dit :

```text
Bonjour, je suis Naomie.
Je veux lancer le sprint SELAS.
```

Codex doit repondre :

```text
Statut sprint : Phase 3 - NOTEBOOKLM / NO-GO dev
Action maintenant : colle le Prompt NotebookLM 01 dans NotebookLM, puis donne-moi la reponse brute.
Point pedagogie : on demarre par la collecte metier. NotebookLM aide a extraire les regles, mais Codex decide ensuite quoi noter, quoi verifier et quoi demander.
Prochaine etape : je structure ta reponse dans le journal SELAS, puis je te donne le prompt suivant selon les trous.
```

Puis Codex donne le Prompt NotebookLM 01 complet.

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
