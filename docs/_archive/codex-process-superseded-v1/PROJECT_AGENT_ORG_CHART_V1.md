# Project agent org chart V1

Date : 2026-06-02

## Objet

Ce document est le registre pyramidal des agents du projet SYDEL.

Il repond a une question simple :

```text
Quand Gad demande ou en est le projet, quel agent faut-il interroger, dans quel
ordre, et ou se trouve la preuve ?
```

Il ne remplace pas les protocoles existants. Il les relie dans une chaine de
commandement lisible.

## Regle centrale

```text
Tout statut projet doit pouvoir remonter au big orchestrateur, puis redescendre
vers le bon agent, le bon journal, le bon worklog ou le bon rapport.
```

Si un niveau de la pyramide ne sait pas ou trouver la preuve, ce n'est pas un
etat fiable : c'est un trou de suivi a corriger.

## Pyramide de pilotage

```text
Gad
  |
  v
Big Orchestrateur Projet / Codex PM
  Source : docs/project/PROJECT_CONTROL_TOWER_V1.md
  Memoire : docs/project/04_LAST_STATE.md
  Tickets : docs/project/01_EXECUTION_BOARD.md
  |
  +-- Routeur d'identite / nouveau chat
  |     Sources : AGENTS.md, PROJECT_CONTROL_TOWER_V1.md
  |     Sortie : Gad / Naomi / autre + protocole actif
  |
  +-- Orchestrateur Produit / Gate metier
  |     Source : docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md
  |     Sortie : GO dev / NO-GO dev / cadrage requis
  |
  +-- Orchestrateur de sprint par type d'entreprise
  |     Source : docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md
  |     Methode : docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md
  |     Sortie : docs/sprints/SPRINT_[TYPE]_V1.md
  |
  +-- Orchestrateur Naomi / supervision Gad
  |     Source : docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md
  |     Tracabilite : docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md
  |     Sync : docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md
  |     Worklog : docs/sprints/SPRINT_[TYPE]_NAOMIE_WORKLOG_V1.md
  |     Sortie : rapport boss court + curseur mis a jour
  |
  +-- Runtime Naomi / agent operationnel accompagne
  |     Source : docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md
  |     Sortie : action unique pour Naomi + point pedagogie
  |
  +-- Professeur Naomi
  |     Source : docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md
  |     Sortie : explication pedagogique, jamais GO dev
  |
  +-- Reuse Auditor
  |     Source : docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md
  |     Sortie : matrice identique / reuse-check / adapter / no-go
  |
  +-- Front Information Dedup Agent
  |     Source : docs/project/FRONT_INFORMATION_DEDUP_AGENT_PROTOCOL_V1.md
  |     Sortie : champs source uniques / derives / reutilises / distincts
  |
  +-- Agents specialistes
        Tracabilite de flux, Source/Juridique, NotebookLM, Front, Moteur, QA,
        Revue humaine, Git/branche, rattrapage retroactif
        Sortie : rapport, matrice, tests, pack, ou blocage trace
```

## Niveaux et responsabilites

| Niveau | Agent | Fichier source | Question traitee | Sortie obligatoire |
| --- | --- | --- | --- | --- |
| 0 | Gad | message humain | Priorite, arbitrage, validation | decision, demande, GO/NO-GO |
| 1 | Big Orchestrateur Projet | `PROJECT_CONTROL_TOWER_V1.md` | Ou en est le projet entier ? | sprint actif, phase, action autorisee |
| 1 bis | Memoire de reprise | `04_LAST_STATE.md` | Que doit savoir un nouveau chat ? | dernier ticket, etat reprenable |
| 2 | Board / tickets | `01_EXECUTION_BOARD.md` | Quel ticket existe et quel statut ? | ticket DONE/IN_PROGRESS/BLOCKED/READY |
| 2 | Routeur identite | `AGENTS.md` | Qui parle ? | Gad / Naomi / autre |
| 2 | Gate produit | `PRODUCT_GUARDRAIL_PROTOCOL_V1.md` | Peut-on coder ? | `GO dev` ou `NO-GO dev` |
| 3 | Orchestrateur sprint | `SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` | Quelle phase de sprint ? | gate courant et prochaine action |
| 3 | Playbook type entreprise | `COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` | Quelle methode pour un type ? | sources, NotebookLM, reuse, matrice, pack |
| 3 | Fichier de sprint | `docs/sprints/SPRINT_[TYPE]_V1.md` | Etat exact d'un type | phase, gates, blocages |
| 4 | Orchestrateur Naomi | `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` | Ou en est Naomi ? | rapport Gad + worklog mis a jour |
| 4 | Agent de tracabilite de flux | `WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` | Ou en est le flux pilote ? | avancement du flux + preuves internes |
| 4 | Agent de synchronisation de flux | `NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md` | Pourquoi le travail annonce n'est pas visible ? | commit pousse ou Sync packet |
| 4 | Runtime Naomi | `NAOMIE_RUNTIME_PROTOCOL_V1.md` | Que dire a Naomi maintenant ? | action unique + point pedagogie |
| 4 | Professeur Naomi | `NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md` | Comment expliquer sans coder ? | explication pedagogique |
| 4 | Reuse Auditor | `REUSE_AUDIT_AGENT_PROTOCOL_V1.md` | Que reutiliser sans risque ? | matrice reuse |
| 4 | Front Information Dedup Agent | `FRONT_INFORMATION_DEDUP_AGENT_PROTOCOL_V1.md` | Est-ce qu'une meme information est redemandee dans le front ? | verdict dedup + tickets de suppression/reuse |
| 5 | NotebookLM Agent | prompt/log du sprint | Quelles infos la base donne ? | reponse structuree dans journal |
| 5 | Source/Juridique Agent | source truth, DOCX, specs, retours | Quelle source fait foi ? | ecarts, reserves, non trouve |
| 5 | Front Agent | front contracts, `src/.../front*` | Quel parcours utilisateur ? | contrat, UX, blocages |
| 5 | Motor Agent | catalogue, orchestrateur, generateurs | Que sait produire le moteur ? | code/tests ou blocage |
| 5 | QA Agent | tests, smoke, pack | Est-ce verifie ? | rapport de validation |
| 5 | Human Review Agent | brief, pack actif, retours | Que dit l'humain ? | retours classes |
| 5 | Git/Branch Agent | remote, branche, commits | Quelle branche/fichier distant ? | etat local/distant |
| 5 | Agent de rattrapage retroactif | repo, commits, threads, docs | Qu'est-ce qui n'a pas ete trace ? | ledger retroactif |
| 5 | Blocker / Question Agent | sources, specs, retours, code, tests | Qu'est-ce qui manque vraiment ? | question concrete a Gad ou decision sourcee |

## Chaine standard pour "ou en est Naomi ?"

Quand Gad demande `ou en est Naomi ?`, la chaine obligatoire est :

1. Routeur identite confirme que l'interlocuteur est Gad.
2. Big Orchestrateur lit la tour de controle.
3. Orchestrateur Naomi active l'Agent de tracabilite de flux, qui lit :
   - `04_LAST_STATE.md` ;
   - `SPRINT_SELAS_V1.md` ou le sprint actif ;
   - `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` ;
   - `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` ;
   - branche Naomi via Git local ou GitHub ;
   - threads Codex accessibles ;
   - etat reel du repo : sources, specs, catalogue, generateurs, tests,
     exemples, rapports.
4. Si tout concorde, rapport boss court.
5. Si le worklog est vide ou stale mais que le flux a avance, activer le
   rattrapage retroactif.
6. Si Gad annonce une avancee terminee mais qu'aucune trace publiee ne la
   montre, activer le protocole de synchronisation avant de repondre comme si le
   flux n'avait pas avance.
7. Produire un rapport differentiel depuis le dernier curseur Gad, en parlant
   du flux Naomi et non de performance personnelle.
8. Mettre a jour le worklog avec le nouveau curseur.

## Agent de tracabilite et rattrapage retroactif

L'Agent de tracabilite de flux est defini dans
`docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md`.

Son role est de tracer ce qui avance sur le flux, sans demander au pilote humain
de tenir le journal.

Le rattrapage retroactif est un mode de cet agent. Il reconstruit ce qui a ete
fait avant que les processus de suivi existent ou quand ils n'ont pas ete tenus.

Pour Gad, le rapport par defaut parle d'un seul niveau : le flux Naomi. Les
details `humain / Codex / repo / outil` restent des preuves internes et ne
sortent qu'en audit detaille.

### Sources du rattrapage

L'agent fouille dans cet ordre :

1. worklog Naomi du sprint ;
2. journaux NotebookLM ou base de connaissance ;
3. fichier de sprint actif ;
4. `04_LAST_STATE.md` ;
5. `01_EXECUTION_BOARD.md` ;
6. rapports `docs/review/` lies au type ;
7. specs `docs/delivery/` ;
8. source truth et sources DOCX ;
9. code : catalogue, case catalog, orchestrateur, generateurs, front, tests ;
10. commits de la branche Naomi ;
11. commits des branches proches si necessaire ;
12. threads Codex accessibles ;
13. artefacts ou packs actifs.

### Sortie du rattrapage

L'agent produit une table :

| Date | Source | Fait trouve | Attribution | Fiabilite | Impact sprint | Action |
| --- | --- | --- | --- | --- | --- | --- |
| date | fichier/commit/thread | fait | humain / Codex / Projet / outil / inconnu | tracee / probable / non attribuable | effet | rattraper / ignorer / demander |

Cette table doit etre ecrite dans le worklog du sprint ou dans un rapport dedie
`docs/review/[type]_trace_recovery_001_report_v1.md`. Si un ancien nom de
rapport existe deja, comme `naomie_backfill`, il reste utilisable comme alias
technique.

## Etat actuel des trous

| Sujet | Etat | Trou | Correction |
| --- | --- | --- | --- |
| Big orchestrateur | OK | Aucun registre pyramidal unique avant ce fichier | Ce document devient le registre |
| Routage Gad/Naomi | OK | A surveiller dans nouveaux chats | `AGENTS.md` + tour de controle |
| Suivi flux Naomi | PARTIAL | Rattrapage SELAS 001 produit ; le flux est suivi mais NotebookLM manque | reprendre NotebookLM sur les trous reels |
| Rapport Gad | OK V2 | Rapport boss court defini par `WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` | statut / avancement / prochaine etape / blocage / fiabilite |
| Etat reel SELAS | OK | Doit remonter comme avancement du flux Naomi SELAS | garder details en preuve interne |
| Sync inter-threads | A INSTALLER | Si Naomi avance dans un autre thread sans push, Gad ne voit rien | appliquer `NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md` |
| NotebookLM SELAS | INCOMPLET | aucune reponse brute structuree | reprendre uniquement sur trous reels |
| Reuse audit SELAS | BLOQUE | NotebookLM pas assez propre | attendre sortie NotebookLM |
| Front dedup | OK V1 | Agent dedie ajoute apres retour Gad 2026-06-02 | appliquer avant tout GO dev front |
| Matrice SELAS | BLOQUE | reuse audit absent | interdite avant gate |
| Dev SELAS | NO-GO | aucun GO Gad | interdit |
| Threads Codex | OUTIL-DEPENDANT | recherche possible mais pas source garantie | noter si l'outil est indisponible |
| Branche locale Naomi | BLOQUE LOCAL | ref absente/fetch bloque dans ce worktree | utiliser GitHub |

## Definition de coherence A-Z

Le systeme est coherent si chaque question de Gad peut suivre ce chemin :

```text
Question Gad
  -> Routeur identite
  -> Big Orchestrateur Projet
  -> Orchestrateur specialise
  -> Agent de preuve
  -> Journal/worklog/rapport
  -> Reponse Gad
  -> Memoire mise a jour
```

Si une etape manque, Codex doit dire quel niveau manque et creer ou mettre a
jour le fichier correspondant.

## Chaine standard quand un ticket bloque

Quand un agent specialise ne peut pas avancer, il doit appeler le
`Blocker / Question Agent` avant de solliciter Gad.

Le Blocker / Question Agent doit :

1. relire les sources, specs, retours NotebookLM/modele, retours humains, code
   et tests pertinents ;
2. classer le point en `reponse trouvee`, `contradiction`, `source manquante`,
   `arbitrage scope`, `donnee utilisateur manquante` ou `vrai blocage` ;
3. si la reponse est trouvee, renvoyer une decision sourcee et permettre au
   ticket d'avancer ;
4. si le blocage est reel, produire une question courte a Gad avec l'impact
   exact sur la cloture du sprint.

Un agent projet ne doit pas attendre silencieusement : tout blocage reel doit
etre visible dans le board, le dernier etat ou le fichier de sprint.

## Reponse attendue du big orchestrateur

Quand Gad demande `ou est-ce qu'on va ?` ou `qui doit gerer ca ?`, Codex doit
repondre :

```text
Big orchestrateur : PROJECT_CONTROL_TOWER_V1.md.
Sprint actif : [sprint].
Agent specialise a interroger : [agent].
Source de preuve : [worklog/journal/rapport/code/branch].
Trou eventuel : [aucun ou detail].
Action autorisee maintenant : [une seule action].
```

## Prochaine action pour Naomi / SELAS

Pour SELAS, l'action correcte n'est plus de faire comme si tout commençait.

Action autorisee :

1. lire `docs/review/selas_naomie_backfill_001_report_v1.md` ;
2. reprendre NotebookLM uniquement sur les trous reels ;
3. mettre a jour `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` a chaque session ;
4. rester en `NO-GO dev`.
