# Sprint SELAS - worklog Naomie V1

Date d'ouverture : 2026-06-02

## Objet

Ce fichier suit l'avancement operationnel de Naomie sur le sprint SELAS.

Il applique :

- `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` ;
- `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md` ;
- `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md` ;
- `docs/sprints/SPRINT_SELAS_V1.md`.

Il ne remplace pas le journal NotebookLM
`docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`. Le journal NotebookLM contient
les reponses de la base de connaissance ; ce worklog contient le suivi de ce que
Naomie a fait, ce qui manque et ce que Gad peut superviser.

## Identite

| Champ | Valeur |
| --- | --- |
| Projet | SYDEL document engine |
| Superviseur | Gad |
| Pilote accompagnee | Naomie |
| Sprint | SPRINT-SELAS-V1 |
| Type d'entreprise | SELAS |
| Branche cible | `codex/naomie-selas-sprint` |
| Phase courante | Phase 3 - NOTEBOOKLM |
| Statut courant | `NO-GO dev` |
| Ticket actif | `SELAS-SOURCES-NOTEBOOKLM-001` |
| Dernier rapport Gad | 2026-06-02 - rapport applique dans chat courant sans delta Naomi trace |
| Lecture branche | Branche distante visible via connecteur GitHub ; fetch local bloque par permissions/identifiants |
| Fiabilite suivi | `STALE` : worklog Naomi incomplet face a l'etat reel SELAS du repo |
| Backfill retroactif | Realise selon `docs/project/PROJECT_AGENT_ORG_CHART_V1.md` ; rapport `docs/review/selas_naomie_backfill_001_report_v1.md` |

## Etat courant

| Point | Statut |
| --- | --- |
| Identification Naomie | A confirmer dans la session Naomie |
| Branche Naomie | Existe cote GitHub ; lecture a faire via connecteur si `git fetch` local echoue |
| Prompt NotebookLM 01 donne | A faire dans la session Naomie |
| Reponse brute NotebookLM 01 recue | Non |
| Reponse structuree dans journal NotebookLM | Non |
| Audit reutilisation | Bloque |
| Matrice documentaire | Bloquee |
| GO dev | Manquant |

## Etat reel SELAS hors worklog

Le worklog ne doit pas etre lu comme la preuve que SELAS est vierge.

Preuves repo deja presentes au 2026-06-02 :

- sources SELAS dans `project/source_documents/`, notamment :
  - `project/source_documents/lot_02/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx` ;
  - `project/source_documents/lot_04/Statuts_SELAS_medecin.docx` ;
  - `project/source_documents/lot_05/Courrier SDE - SELAS.docx` ;
  - `project/source_documents/lot_05/PV AGE cession part SCM - SELAS.docx` ;
  - `project/source_truth/modele Statuts SELAS avec MH.docx`.
- catalogue SELAS deja existant dans `src/sydel_doc_engine/domain/case_catalog.py`
  avec documents SELAS communs, statuts medecin, regime communautaire, SCM,
  cession et derogations ;
- `DOC-018` deja defini comme `Statuts SELAS medecin` dans
  `src/sydel_doc_engine/registry/catalog.py` ;
- generateur `StatutsSelasMedecinGenerator` deja branche dans
  `src/sydel_doc_engine/orchestrator/service.py` ;
- conditions UI SELAS deja presentes dans
  `src/sydel_doc_engine/app/business_wizard.py` ;
- tests et exemples SELAS deja presents.

Conclusion : le rapport Gad ne doit pas dire `SELAS est au debut` ou `Naomi est
au demarrage NotebookLM` sans nuance. Il doit dire :

```text
Aucune action Naomi n'est tracee depuis le dernier rapport, mais le repo contient deja une matiere SELAS preexistante. Le suivi Naomi est stale/incomplet tant qu'il ne relie pas ces preuves a l'avancement operationnel.
```

## Derniere action Naomi tracee

Aucune action Naomi personnelle n'est tracee dans ce worklog a date.

Les protocoles indiquent encore que la prochaine action Naomi, si Naomi reprend
le sprint, doit etre : consolider l'etat SELAS reel, puis reprendre la boucle
NotebookLM a l'endroit utile. Le Prompt 01 ne doit plus etre donne comme si le
projet etait vierge sans audit de fraicheur prealable.

## Blocages

- Aucune reponse brute NotebookLM SELAS n'est encore tracee.
- Le sous-sprint NotebookLM n'est pas suffisant dans les fichiers de suivi,
  mais le repo contient deja des sources, specs, code et tests SELAS.
- Le suivi Naomi est defaillant/stale : les rapports Gad ont confondu absence
  de trace Naomi et absence d'avancee SELAS.
- L'audit de reutilisation et la matrice documentaire restent interdits.
- Aucun `GO dev` Gad n'a ete donne.
- `git fetch` peut echouer depuis ce worktree avec `FETCH_HEAD Permission
  denied` et/ou identifiants Git absents ; dans ce cas, Codex doit utiliser le
  connecteur GitHub avant de conclure que la branche est inaccessible.

## Prochaine action Naomi

```text
Reprendre apres audit de fraicheur : verifier l'etat reel SELAS existant, puis demander seulement la reponse NotebookLM qui manque encore.
```

## Prochaine action Codex

```text
Relancer la boucle NotebookLM sur les trous reels, en s'appuyant sur le backfill SELAS deja produit.
```

## Backfill retroactif

Objectif : reconstruire ce qui etait deja fait avant que le worklog Naomi existe
ou avant qu'il soit correctement tenu.

Agent responsable : `Backfill Agent`, defini dans
`docs/project/PROJECT_AGENT_ORG_CHART_V1.md`.

Regle : ne pas attribuer a Naomi une action qui n'est pas explicitement tracee.
Le backfill doit separer :

- actions Naomi tracees ;
- faits projet/code/sources non attribuables ;
- actions Codex ;
- traces de threads ;
- commits branche Naomi ;
- trous de suivi.

Sortie attendue :

```text
docs/review/selas_naomie_backfill_001_report_v1.md
```

Statut : realise le 2026-06-02 dans
`docs/review/selas_naomie_backfill_001_report_v1.md`.

Conclusion : aucune action personnelle de Naomi n'est prouvee dans les traces
accessibles, mais SELAS n'est pas vierge. Le repo contient deja sources, code,
catalogue, `DOC-018`, generateur, conditions UI et tests SELAS. Le suivi doit
donc reprendre depuis les trous reels, notamment la reponse NotebookLM brute.

## Questions pedagogiques posees

Aucune question pedagogique Naomi tracee dans ce worklog a date.

## Rapports Gad

Regle : quand Gad demande `ou en est Naomi ?`, Codex produit un rapport
differentiel depuis le dernier rapport inscrit ici. Si aucun rapport n'existe,
le rapport couvre toute la periode tracee depuis l'ouverture du worklog.

| Date | Demande Gad | Periode couverte | Sources lues | Synthese donnee | Action suivante | Curseur |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-02 | Gad demande : "ou en est Naomi ?" | Depuis l'ouverture du worklog 2026-06-02 jusqu'au 2026-06-02 | `PROJECT_CONTROL_TOWER_V1.md`, `04_LAST_STATE.md`, `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `SPRINT_SELAS_V1.md`, `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, tentative `git log/show origin/codex/naomie-selas-sprint` bloquee car ref absente localement, tentative `git fetch origin codex/naomie-selas-sprint --prune` bloquee par `FETCH_HEAD` permission denied, correction ulterieure : branche distante confirmee via connecteur GitHub | Naomi est toujours au demarrage du sprint SELAS : phase 3 NotebookLM, `NO-GO dev`, aucune action Naomi ni reponse NotebookLM tracee ; prompt 01 reste a donner dans la session Naomi. Diagnostic branche corrige : branche OK via connecteur GitHub, fetch local bloque | Naomi doit coller le Prompt NotebookLM 01 dans NotebookLM puis donner la reponse brute ; Codex structurera ensuite le journal | Dernier rapport Gad = 2026-06-02 premier rapport supervision Naomi |
| 2026-06-02 | Gad demande : "C'est gad, ou en est Naomi ?" | Depuis le premier rapport supervision Naomi 2026-06-02 jusqu'au 2026-06-02 | `PROJECT_CONTROL_TOWER_V1.md`, `04_LAST_STATE.md`, `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `SPRINT_SELAS_V1.md`, `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, `git status --short --branch`, `git remote -v`, `git branch --show-current`, `git show-ref refs/remotes/origin/codex/naomie-selas-sprint`, connecteur GitHub branche/fichiers | Aucun delta Naomi trace depuis le premier rapport : toujours Phase 3 NotebookLM, `NO-GO dev`, aucune reponse NotebookLM importee, Prompt 01 encore a donner dans la session Naomi. Branche distante confirmee via connecteur GitHub ; ref locale absente dans ce worktree | Naomi doit coller le Prompt NotebookLM 01 dans NotebookLM puis donner la reponse brute ; Codex structurera ensuite le journal | Dernier rapport Gad = 2026-06-02 deuxieme rapport supervision Naomi |
| 2026-06-02 | Gad signale que le rapport test est faux et demande ou la chaine casse | Depuis le deuxieme rapport supervision Naomi 2026-06-02 jusqu'au 2026-06-02 | worklog, journal NotebookLM local et distant, commits `codex/naomie-selas-sprint`, threads Codex recents, scan repo `rg SELAS`, catalogue, orchestrateur, sources, tests et exemples SELAS | Diagnostic corrige : aucune action Naomi personnelle n'est tracee, mais le projet SELAS n'est pas au debut. Le point de rupture est `PROJECT_STATE_IGNORED` + `WORKLOG_STALE` : les rapports ont pris le worklog vide comme verite unique et n'ont pas audite l'etat reel SELAS du repo | Backfiller le worklog depuis les preuves repo et imposer l'audit de fraicheur avant chaque rapport Gad | Dernier rapport Gad = 2026-06-02 audit fraicheur rapports Naomi |
| 2026-06-02 | Gad demande : "C'est gad, ou en est Naomi ?" | Depuis l'audit fraicheur rapports Naomi 2026-06-02 jusqu'au 2026-06-02 | `PROJECT_CONTROL_TOWER_V1.md`, `04_LAST_STATE.md`, `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `SPRINT_SELAS_V1.md`, `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, `git rev-parse --show-toplevel`, `git branch --show-current`, `git remote -v`, tentative `git log origin/codex/naomie-selas-sprint` bloquee par ref locale absente, connecteur GitHub branche/worklog, scan `rg SELAS` sur sources/catalogue/generateurs/tests/docs | Aucun delta Naomi personnel trace depuis le dernier curseur : aucune reponse NotebookLM importee, aucune action Naomi nouvelle, aucun message Gad en attente. Suivi Naomi defaillant/stale maintenu : le worklog ne prouve pas que SELAS est au debut ; le repo contient deja sources, specs, catalogue, generateur `DOC-018`, conditions UI, tests et exemples SELAS | Backfiller le suivi SELAS depuis les preuves repo/branche, puis reprendre NotebookLM uniquement sur les trous reels avec Naomi ; rester en `NO-GO dev` | Dernier rapport Gad = 2026-06-02 rapport Gad sans delta Naomi trace |
| 2026-06-02 | Gad demande d'appliquer le processus dans ce chat et de repondre comme a "ou en est Naomi ?" | Depuis le rapport Gad sans delta Naomi trace 2026-06-02 jusqu'au 2026-06-02 | `PROJECT_CONTROL_TOWER_V1.md`, `04_LAST_STATE.md`, `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `SPRINT_SELAS_V1.md`, `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, branche GitHub `codex/naomie-selas-sprint` HEAD `59bf703`, threads recents `Suivre statut Naomi`, `Saluer`, `Saluer l'utilisateur`, `Bonjour`, scan `rg SELAS` sur repo | Aucun delta Naomi personnel trace depuis le dernier curseur : aucun thread productif Naomi trouve, aucune reponse NotebookLM importee, aucune action Naomi nouvelle, aucun message Gad en attente. Etat reel SELAS toujours non vierge : sources SELAS, catalogue, `DOC-018`, generateur `StatutsSelasMedecinGenerator`, conditions UI, tests et exemples. Fiabilite du suivi : `STALE`, car le backfill operationnel n'est pas encore fait | Backfiller le suivi SELAS depuis les preuves repo/branche/threads, puis reprendre NotebookLM avec Naomi uniquement sur les trous reels ; rester en `NO-GO dev` | Dernier rapport Gad = 2026-06-02 rapport applique dans chat courant sans delta Naomi trace |

## Messages Gad a transmettre a Naomi

Regle : Gad peut laisser un message a transmettre a Naomi au prochain echange.
Codex doit citer le message de Gad entre guillemets, puis marquer la ligne
comme `transmis`.

| Date | Auteur | Message exact | Contexte | Statut | Date transmission | Note |
| --- | --- | --- | --- | --- | --- | --- |
| - | - | Aucun message en attente | - | - | - | - |

## Decisions Gad

- 2026-06-02 : le suivi Naomi doit etre generique, supervise par traces, et non
  limite a un protocole SELAS.
- 2026-06-02 : Gad doit pouvoir demander `ou en est Naomi ?` sans que Codex
  demande a Naomi un statut oral ; Codex doit lire la branche, la tour de
  controle, le fichier de sprint et ce worklog.
- 2026-06-02 : les rapports Naomi demandes par Gad doivent etre differentiels
  depuis le dernier rapport note dans ce worklog.
- 2026-06-02 : Gad peut laisser un message a transmettre a Naomi ; Codex le
  garde dans ce worklog et le citera au prochain echange avec elle.
- 2026-06-02 : si `git fetch` local echoue, Codex doit tenter la lecture via
  connecteur GitHub avant d'ecrire que la branche est inaccessible.
- 2026-06-02 : un rapport Gad ne doit plus assimiler worklog vide et projet au
  debut. Codex doit toujours distinguer `aucune action Naomi tracee` de `etat
  reel SELAS du repo`.
- 2026-06-02 : Gad demande une pyramide d'agents et un chemin de backfill
  retroactif. Decision : `PROJECT_AGENT_ORG_CHART_V1.md` devient le registre
  central des agents ; le backfill SELAS produit
  `docs/review/selas_naomie_backfill_001_report_v1.md`.

## Historique

| Date | Acteur | Trace | Impact |
| --- | --- | --- | --- |
| 2026-06-02 | Gad | Demande de formaliser un suivi Naomi generique et supervisable | Creation du protocole orchestrateur Naomi et de ce worklog SELAS |
| 2026-06-02 | Gad | Demande de rapports differentiels et de messages Gad en attente pour Naomi | Ajout des sections `Rapports Gad` et `Messages Gad a transmettre a Naomi` |
| 2026-06-02 | Gad | Capture montrant une branche declaree inaccessible apres `FETCH_HEAD Permission denied` | Correction du diagnostic : branche distante confirmee via connecteur GitHub ; fetch local bloque seulement |
| 2026-06-02 | Gad | Capture d'un rapport disant que Naomi est encore au demarrage NotebookLM alors que le repo contient deja de la matiere SELAS | Diagnostic : chaine de suivi stale ; ajout obligatoire d'un audit de fraicheur et d'un etat reel SELAS hors worklog |
| 2026-06-02 | Gad | Demande d'un organigramme pyramidal des agents et d'un agent retroactif pour retrouver ce qui a ete fait avant le suivi | Creation du registre `PROJECT_AGENT_ORG_CHART_V1.md`; backfill SELAS produit avant reprise NotebookLM |
| 2026-06-02 | Codex | Backfill retroactif SELAS execute depuis repo, GitHub, threads recents, worklog et journal NotebookLM | Rapport `docs/review/selas_naomie_backfill_001_report_v1.md` cree ; aucune action Naomi personnelle prouvee, mais etat SELAS repo non vierge |
