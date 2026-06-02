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
  +-- Orchestrateur Naomie / supervision Gad
  |     Source : docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md
  |     Worklog : docs/sprints/SPRINT_[TYPE]_NAOMIE_WORKLOG_V1.md
  |     Sortie : rapport differentiel Gad + curseur mis a jour
  |
  +-- Runtime Naomie / agent operationnel accompagne
  |     Source : docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md
  |     Sortie : action unique pour Naomie + point pedagogie
  |
  +-- Professeur Naomie
  |     Source : docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md
  |     Sortie : explication pedagogique, jamais GO dev
  |
  +-- Reuse Auditor
  |     Source : docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md
  |     Sortie : matrice identique / reuse-check / adapter / no-go
  |
  +-- Agents specialistes
        Source/Juridique, NotebookLM, Front, Moteur, QA, Revue humaine,
        Git/branche, Backfill retroactif
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
| 4 | Orchestrateur Naomie | `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` | Ou en est Naomi ? | rapport Gad + worklog mis a jour |
| 4 | Runtime Naomie | `NAOMIE_RUNTIME_PROTOCOL_V1.md` | Que dire a Naomi maintenant ? | action unique + point pedagogie |
| 4 | Professeur Naomie | `NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md` | Comment expliquer sans coder ? | explication pedagogique |
| 4 | Reuse Auditor | `REUSE_AUDIT_AGENT_PROTOCOL_V1.md` | Que reutiliser sans risque ? | matrice reuse |
| 5 | NotebookLM Agent | prompt/log du sprint | Quelles infos la base donne ? | reponse structuree dans journal |
| 5 | Source/Juridique Agent | source truth, DOCX, specs, retours | Quelle source fait foi ? | ecarts, reserves, non trouve |
| 5 | Front Agent | front contracts, `src/.../front*` | Quel parcours utilisateur ? | contrat, UX, blocages |
| 5 | Motor Agent | catalogue, orchestrateur, generateurs | Que sait produire le moteur ? | code/tests ou blocage |
| 5 | QA Agent | tests, smoke, pack | Est-ce verifie ? | rapport de validation |
| 5 | Human Review Agent | brief, pack actif, retours | Que dit l'humain ? | retours classes |
| 5 | Git/Branch Agent | remote, branche, commits | Quelle branche/fichier distant ? | etat local/distant |
| 5 | Backfill Agent | repo, commits, threads, docs | Qu'a-t-on fait avant le suivi ? | ledger retroactif |

## Chaine standard pour "ou en est Naomi ?"

Quand Gad demande `ou en est Naomi ?`, la chaine obligatoire est :

1. Routeur identite confirme que l'interlocuteur est Gad.
2. Big Orchestrateur lit la tour de controle.
3. Orchestrateur Naomie lit :
   - `04_LAST_STATE.md` ;
   - `SPRINT_SELAS_V1.md` ou le sprint actif ;
   - `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` ;
   - `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` ;
   - branche Naomi via Git local ou GitHub ;
   - threads Codex accessibles ;
   - etat reel du repo : sources, specs, catalogue, generateurs, tests,
     exemples, rapports.
4. Si tout concorde, rapport `fiabilite : tracee`.
5. Si le worklog est vide ou stale mais que le repo contient des preuves,
   activer le Backfill Agent.
6. Produire un rapport differentiel depuis le dernier curseur Gad.
7. Mettre a jour le worklog avec le nouveau curseur.

## Backfill Agent

Le Backfill Agent reconstruit retroactivement ce qui a ete fait avant que les
processus de suivi existent.

Il doit distinguer deux choses :

- `action Naomi tracee` : action explicitement attribuable a Naomi dans un
  thread, un message, un worklog, un commit ou un rapport ;
- `etat projet existant` : sources, code, tests, specs ou rapports presents,
  mais non attribuables directement a Naomi.

Le Backfill Agent ne doit jamais transformer une preuve projet en action Naomi
sans preuve d'attribution.

### Sources du backfill

Le Backfill Agent fouille dans cet ordre :

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

### Sortie du backfill

Le Backfill Agent produit une table :

| Date | Source | Fait trouve | Attribution | Fiabilite | Impact sprint | Action |
| --- | --- | --- | --- | --- | --- | --- |
| date | fichier/commit/thread | fait | Naomi / Codex / Projet / inconnu | tracee / probable / non attribuable | effet | backfill / ignorer / demander |

Cette table doit etre ecrite dans le worklog du sprint ou dans un rapport dedie
`docs/review/[type]_naomie_backfill_001_report_v1.md`.

## Etat actuel des trous

| Sujet | Etat | Trou | Correction |
| --- | --- | --- | --- |
| Big orchestrateur | OK | Aucun registre pyramidal unique avant ce fichier | Ce document devient le registre |
| Routage Gad/Naomi | OK | A surveiller dans nouveaux chats | `AGENTS.md` + tour de controle |
| Suivi Naomi | PARTIAL | Backfill SELAS 001 produit, mais aucune action Naomi personnelle prouvee | reprendre NotebookLM sur les trous reels |
| Rapport Gad | OK/PARTIAL | Delta possible, mais seulement apres curseur fiable | rapport differentiel + audit fraicheur |
| Etat reel SELAS | OK | Non attribuable automatiquement a Naomi | distinguer projet vs action Naomi |
| NotebookLM SELAS | INCOMPLET | aucune reponse brute structuree | reprendre uniquement sur trous reels |
| Reuse audit SELAS | BLOQUE | NotebookLM/backfill pas assez propres | attendre sortie backfill + NotebookLM |
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
