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
- `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` pour le suivi
  de Naomie demande par Gad ;
- `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md` pour le workflow Gad / Naomie / Codex multi-projets ;
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

## Routage interlocuteur au debut d'un chat

Dans un nouveau chat, le premier gate est l'identite de l'interlocuteur.

Si le message est un simple accueil sans identite explicite (`bonjour`, `salut`,
`ca va`, `on reprend`), Codex doit demander :

```text
Bonjour, tu es Gad ou Naomi ?
Je te route ensuite sur le bon protocole projet.
```

Codex ne doit pas declencher NotebookLM, changer de branche, demander une tache
ou choisir un sprint tant que l'interlocuteur n'est pas identifie.

Si l'interlocuteur est Gad :

- Gad est le superviseur produit et decisionnaire ;
- Codex applique la tour de controle et donne l'etat utile du projet ;
- mentionner Naomi ou SELAS dans une question de Gad ne suffit pas a declencher
  le protocole runtime Naomi ;
- si Gad demande ou en est Naomi, Codex applique l'orchestrateur Naomie et lit
  les traces disponibles avant de repondre ;
- avant de repondre a Gad sur Naomi, Codex doit aussi auditer la fraicheur des
  traces : worklog, journal specialise, branche, threads accessibles et etat
  reel du type dans le repo ;
- Codex ne doit jamais assimiler `aucune action Naomi tracee` a `projet au
  debut` sans avoir verifie l'etat reel du type ;
- chaque rapport Naomi demande par Gad doit etre inscrit dans le worklog et le
  rapport suivant doit etre differentiel depuis ce curseur ;
- si Gad laisse un message pour Naomi, Codex l'inscrit dans le worklog et le
  transmet au prochain echange avec elle ;
- Codex peut auditer, corriger ou preparer le protocole Naomi si Gad le demande.

Si l'interlocutrice est Naomi/Naomie :

- Codex applique `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md` ;
- le sprint SELAS actif reste en phase NotebookLM / `NO-GO dev` ;
- Codex donne la prochaine action simple a Naomi, avec un point pedagogie.

## Niveaux de pilotage

| Niveau | Source de verite | Role |
| --- | --- | --- |
| Projet global | `PROJECT_CONTROL_TOWER_V1.md` + `04_LAST_STATE.md` | Savoir ou en est le projet entier |
| Sprint type entreprise | `docs/sprints/SPRINT_[TYPE]_V1.md` | Suivre un type d'entreprise de bout en bout |
| Suivi Naomie | `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` + worklog sprint | Repondre a Gad sur l'avancee de Naomie depuis les traces |
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
| 11 | Audit fidelite / trois sources | Source + QA sous Codex PM | pack actif + audit source/reference/NotebookLM/humain | questions inutiles eliminees, pack transmissible |
| 12 | Revue associe | Associe via Gad/Naomie | retour humain classe | retours compris |
| 13 | Corrections | Codex PM + dev | tickets correction | retours traites ou reportes |
| 14 | Cloture sprint | Codex PM | statut canonique final | sprint reprenable et auditable |

Regle : aucune etape ne saute par-dessus la precedente. Si une etape est
incomplete, Codex doit dire `NO-GO dev` et donner l'action exacte suivante.

## Regle issue de la cloture SELARL

Avant toute revue finale ou cloture d'un type d'entreprise, Codex doit verifier
les trois familles de preuves :

1. document de reference / source de verite ;
2. NotebookLM ou retours modele journalises ;
3. retour humain deja disponible, puis retour final de l'associe.

Codex ne doit pas poser de questions abstraites si ces preuves repondent deja.
Il doit transmettre a l'associe un pack actif et demander des ecarts concrets.
Si un pack est corrige, l'ancien pack est remplace et ne doit plus etre utilise.

## Registre courant des sprints

| Type | Sprint | Pilote metier | Branche | Phase courante | Statut | Action autorisee maintenant |
| --- | --- | --- | --- | --- | --- | --- |
| SELARL | `SPRINT-SELARL-CLOSING-V1` | Gad | `track-b/clean-rebuild` | Validation finale pack corrige | IN_PROGRESS | transmettre le pack 004 et le brief `SELARL-FINAL-ASSOCIE-VALIDATION-001`, attendre validation ou ecarts concrets |
| SELAS | `SPRINT-SELAS-V1` | Naomie | `codex/naomie-selas-sprint` | Sous-sprint NotebookLM + backfill suivi | `NO-GO dev` | auditer la fraicheur, backfiller l'etat SELAS reel, puis reprendre NotebookLM sur les trous reels |

## Etat courant SELARL

La SELARL est le modele de methode et le premier pack de production partielle.

Etat utile :

- creation simple medecin / chirurgien-dentiste generable ;
- regime communautaire traite avec `DOC-005` et `DOC-006` actifs ;
- multi-associes limite disponible sur certains sous-cas ;
- pack de revue corrige regenere dans `artifacts/selarl_closing_pack_004/` ;
- brief de validation associe pret dans
  `docs/review/selarl_final_validation_001_brief_v1.md` ;
- cession, SCM, derogations, site distinct, plusieurs gerants et statuts
  multi-associes complets restent a cadrer ;
- fin de sprint ecrite dans `docs/sprints/SPRINT_SELARL_CLOSING_V1.md` ;
- action courante : transmettre le pack 004 a l'associe / juriste et attendre
  une validation finale ou des ecarts concrets.

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
- worklog Naomie : `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` ;
- dernier rapport Gad : voir section `Rapports Gad` du worklog ;
- messages Gad a transmettre : voir section `Messages Gad a transmettre a
  Naomi` du worklog ;
- prompt source : `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md` ;
- etat reel SELAS : matiere preexistante dans le repo, dont sources SELAS,
  `DOC-018`, generateur statuts SELAS, selection catalogue, conditions UI, tests
  et exemples ;
- action courante : auditer la fraicheur, backfiller le suivi SELAS reel, puis
  reprendre NotebookLM sur les trous reels.
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

Si l'interlocutrice active est Naomie/Naomi, Codex doit repondre en format
sprint :

```text
Statut sprint : [phase] / [statut]
Action maintenant : [une seule action]
Point pedagogie : [explication courte]
Prochaine etape : [suite immediate]
```

Si la demande est un simple `bonjour` sans identite explicite, Codex demande
d'abord si l'interlocuteur est Gad ou Naomi. Si la personne repond ensuite
Naomi/Naomie, Codex donne le Prompt NotebookLM 01 complet. Il ne doit pas
attendre que Naomie choisisse une tache.

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
