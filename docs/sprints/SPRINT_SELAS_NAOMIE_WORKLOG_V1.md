# Sprint SELAS - worklog Naomi V1

Date d'ouverture : 2026-06-02

## Objet

Ce fichier suit l'avancement operationnel du flux Naomi sur le sprint SELAS.

Il applique :

- `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` ;
- `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md` ;
- `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md` ;
- `docs/sprints/SPRINT_SELAS_V1.md`.

Il ne remplace pas le journal NotebookLM
`docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`. Le journal NotebookLM contient
les reponses de la base de connaissance ; ce worklog contient le suivi de ce que
le flux Naomi a produit, ce qui manque et ce que Gad peut superviser.

## Identite

| Champ | Valeur |
| --- | --- |
| Projet | SYDEL document engine |
| Superviseur | Gad |
| Pilote accompagnee | Naomi |
| Sprint | SPRINT-SELAS-V1 |
| Type d'entreprise | SELAS |
| Branche cible | `codex/naomie-selas-sprint` |
| Phase courante | Sync incident : avancee annoncee jusqu'a attente retour humain, non verifiee dans les traces publiees |
| Statut courant | `NO-GO dev` tant que commit pousse ou Sync packet absent |
| Ticket actif | `NAOMIE-SYNC-CHECKPOINT-001` |
| Dernier rapport Gad | 2026-06-02 - Gad annonce que le flux SELAS est termine jusqu'a attente retour humain, mais la branche publiee ne montre pas cette avancee |
| Lecture branche | Branche distante visible via connecteur GitHub ; fetch local bloque par permissions/identifiants |
| Fiabilite suivi | `SYNC_MANQUANTE` : avancee annoncee, commit/Sync packet absent |
| Rattrapage retroactif | Realise selon `docs/project/PROJECT_AGENT_ORG_CHART_V1.md` ; rapport `docs/review/selas_naomie_backfill_001_report_v1.md` |
| Agent de tracabilite | `docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` |
| Agent de synchronisation | `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md` |

## Etat courant

| Point | Statut |
| --- | --- |
| Identification Naomi | A confirmer dans la session Naomi |
| Branche Naomi | Existe cote GitHub ; lecture a faire via connecteur si `git fetch` local echoue |
| Prompt NotebookLM 01 donne | A faire dans la session Naomi |
| Reponse brute NotebookLM 01 recue | Non |
| Reponse structuree dans journal NotebookLM | Non |
| Avancee SELAS terminee jusqu'a retour humain | Annoncee par Gad, non verifiee dans branche/worklog |
| Audit reutilisation | Inconnu dans traces publiees |
| Matrice documentaire | Inconnue dans traces publiees |
| GO dev | Manquant dans traces publiees |

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
au demarrage NotebookLM` sans nuance. Il doit parler du flux Naomi SELAS :

```text
Le flux Naomi SELAS a deja de la matiere prouvee dans le repo. Le suivi etait stale/incomplet ; le rattrapage retroactif est fait. Le prochain trou reel est la reponse NotebookLM manquante.
```

## Dernier avancement du flux Naomi trace

Le flux Naomi SELAS contient deja des sources, du code, un catalogue, `DOC-018`,
un generateur, des conditions UI et des tests. Le rattrapage retroactif est
documente dans `docs/review/selas_naomie_backfill_001_report_v1.md`.

Les protocoles indiquent encore que la prochaine action Naomi, si Naomi reprend
le sprint, doit etre : reprendre la boucle NotebookLM sur le trou reel. Le
Prompt 01 ne doit plus etre donne comme si le projet etait vierge sans audit de
fraicheur prealable.

## Blocages

- Gad indique que Naomi a avance SELAS jusqu'a attente retour humain, mais
  cette avancee n'est pas visible sur la branche `codex/naomie-selas-sprint`
  publiee au moment du controle.
- Le point de rupture probable est la synchronisation : travail non pousse,
  mauvais thread, mauvais depot, mauvaise branche, ou Sync packet absent.
- Aucune reponse brute NotebookLM SELAS n'est encore tracee.
- Le sous-sprint NotebookLM n'est pas suffisant dans les fichiers de suivi,
  mais le repo contient deja des sources, specs, code et tests SELAS.
- Le suivi etait defaillant/stale : les rapports Gad ont confondu absence de
  trace tenue par l'agent et absence d'avancee du flux SELAS.
- L'audit de reutilisation et la matrice documentaire restent interdits.
- Aucun `GO dev` Gad n'a ete donne.
- `git fetch` peut echouer depuis ce worktree avec `FETCH_HEAD Permission
  denied` et/ou identifiants Git absents ; dans ce cas, Codex doit utiliser le
  connecteur GitHub avant de conclure que la branche est inaccessible.

## Prochaine action Naomi

```text
Faire un Sync checkpoint : verifier branche/HEAD/status, puis pousser le travail
termine ou produire un Sync packet complet si le push bloque.
```

## Prochaine action Codex

```text
Ne pas relancer NotebookLM tant que la sync n'est pas clarifiee. Lire le commit
pousse ou le Sync packet de Naomi, puis mettre a jour le statut reel SELAS.
```

## Rattrapage retroactif

Objectif : reconstruire ce qui etait deja fait avant que le worklog Naomi existe
ou avant qu'il soit correctement tenu.

Agent responsable : Agent de tracabilite de flux, defini dans
`docs/project/PROJECT_AGENT_ORG_CHART_V1.md`.

Regle : le rapport boss parle du flux Naomi SELAS. La separation fine reste
interne au rattrapage. Le rattrapage doit separer :

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

Conclusion : le flux Naomi SELAS n'est pas vierge. Le repo contient deja
sources, code, catalogue, `DOC-018`, generateur, conditions UI et tests SELAS.
Le rapport boss ne doit pas chercher une evaluation personnelle de Naomi ; il
doit reprendre depuis les trous reels, notamment la reponse NotebookLM brute.

## Questions pedagogiques posees

Aucune question pedagogique Naomi tracee dans ce worklog a date.

## Rapports Gad

Regle : quand Gad demande `ou en est Naomi ?`, Codex produit un rapport
differentiel depuis le dernier rapport inscrit ici. Si aucun rapport n'existe,
le rapport couvre toute la periode tracee depuis l'ouverture du worklog.

Format boss par defaut :

```text
Statut flux Naomi : SYDEL / SPRINT-SELAS-V1 / Phase 3 NotebookLM / NO-GO dev
Avancement depuis le dernier point : rattrapage retroactif fait ; SELAS contient deja sources, catalogue, DOC-018, generateur, conditions UI et tests ; journal NotebookLM toujours vide.
Prochaine etape : obtenir la reponse brute NotebookLM manquante, puis la structurer dans le journal.
Blocage / risque : NotebookLM pas encore couvert ; reuse audit, matrice et dev restent bloques.
Fiabilite : suivi rattrape partiellement, preuves repo OK, prochain suivi a tenir par l'Agent de tracabilite.
```

| Date | Demande Gad | Periode couverte | Sources lues | Synthese donnee | Action suivante | Curseur |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-02 | Gad informe que Naomi a avance SELAS jusqu'a attente retour humain, mais que le rapport ne le voit pas | Depuis le rapport boss court precedent jusqu'au 2026-06-02 | branche GitHub `codex/naomie-selas-sprint` HEAD `6a0382f`, commits visibles, liste branches GitHub, threads Codex recents accessibles, worklog local | Avancee annoncee par Gad, non verifiee dans les traces publiees. La branche distante ne montre pas de commit/livrable SELAS termine apres les commits de protocoles. Point de rupture probable : sync Git/thread manquante, mauvais thread, mauvais depot, mauvaise branche, ou push absent | Demander a Naomi un Sync checkpoint : commit/push si possible, sinon Sync packet complet ; ne pas relancer NotebookLM avant de clarifier la sync | Dernier rapport Gad = 2026-06-02 sync manquante flux SELAS |
| 2026-06-02 | Gad demande : "ou en est Naomi ?" | Depuis l'ouverture du worklog 2026-06-02 jusqu'au 2026-06-02 | `PROJECT_CONTROL_TOWER_V1.md`, `04_LAST_STATE.md`, `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `SPRINT_SELAS_V1.md`, `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, tentative `git log/show origin/codex/naomie-selas-sprint` bloquee car ref absente localement, tentative `git fetch origin codex/naomie-selas-sprint --prune` bloquee par `FETCH_HEAD` permission denied, correction ulterieure : branche distante confirmee via connecteur GitHub | Historique depasse : ce rapport confondait worklog vide et flux au demarrage. Le format actuel doit parler du flux Naomi SELAS et activer le rattrapage si les traces sont stale | Reprendre depuis le rapport boss par defaut et le rattrapage retroactif | Dernier rapport Gad = 2026-06-02 premier rapport supervision Naomi |
| 2026-06-02 | Gad demande : "C'est gad, ou en est Naomi ?" | Depuis le premier rapport supervision Naomi 2026-06-02 jusqu'au 2026-06-02 | `PROJECT_CONTROL_TOWER_V1.md`, `04_LAST_STATE.md`, `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `SPRINT_SELAS_V1.md`, `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, `git status --short --branch`, `git remote -v`, `git branch --show-current`, `git show-ref refs/remotes/origin/codex/naomie-selas-sprint`, connecteur GitHub branche/fichiers | Historique depasse : ce rapport cherchait un delta individuel au lieu de consolider l'avancement du flux. Branche distante confirmee via connecteur GitHub ; ref locale absente dans ce worktree | Reprendre depuis le rapport boss par defaut et le rattrapage retroactif | Dernier rapport Gad = 2026-06-02 deuxieme rapport supervision Naomi |
| 2026-06-02 | Gad signale que le rapport test est faux et demande ou la chaine casse | Depuis le deuxieme rapport supervision Naomi 2026-06-02 jusqu'au 2026-06-02 | worklog, journal NotebookLM local et distant, commits `codex/naomie-selas-sprint`, threads Codex recents, scan repo `rg SELAS`, catalogue, orchestrateur, sources, tests et exemples SELAS | Diagnostic corrige : aucune action humaine directe n'est tracee, mais le flux SELAS n'est pas au debut. Le point de rupture est `PROJECT_STATE_IGNORED` + `WORKLOG_STALE` : les rapports ont pris le worklog vide comme verite unique et n'ont pas audite l'etat reel SELAS du repo | Rattraper retroactivement le worklog depuis les preuves repo et imposer l'audit de fraicheur avant chaque rapport Gad | Dernier rapport Gad = 2026-06-02 audit fraicheur rapports Naomi |
| 2026-06-02 | Gad demande : "C'est gad, ou en est Naomi ?" | Depuis l'audit fraicheur rapports Naomi 2026-06-02 jusqu'au 2026-06-02 | `PROJECT_CONTROL_TOWER_V1.md`, `04_LAST_STATE.md`, `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `SPRINT_SELAS_V1.md`, `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, `git rev-parse --show-toplevel`, `git branch --show-current`, `git remote -v`, tentative `git log origin/codex/naomie-selas-sprint` bloquee par ref locale absente, connecteur GitHub branche/worklog, scan `rg SELAS` sur sources/catalogue/generateurs/tests/docs | Aucun delta de flux supplementaire trace depuis le dernier curseur : aucune reponse NotebookLM importee, aucun message Gad en attente. Suivi defaillant/stale maintenu : le worklog ne prouve pas que SELAS est au debut ; le repo contient deja sources, specs, catalogue, generateur `DOC-018`, conditions UI, tests et exemples SELAS | Rattraper retroactivement le suivi SELAS depuis les preuves repo/branche, puis reprendre NotebookLM uniquement sur les trous reels avec Naomi ; rester en `NO-GO dev` | Dernier rapport Gad = 2026-06-02 rapport Gad sans delta Naomi trace |
| 2026-06-02 | Gad demande d'appliquer le processus dans ce chat et de repondre comme a "ou en est Naomi ?" | Depuis le rapport Gad sans delta Naomi trace 2026-06-02 jusqu'au 2026-06-02 | `PROJECT_CONTROL_TOWER_V1.md`, `04_LAST_STATE.md`, `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `SPRINT_SELAS_V1.md`, `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, branche GitHub `codex/naomie-selas-sprint` HEAD `59bf703`, threads recents `Suivre statut Naomi`, `Saluer`, `Saluer l'utilisateur`, `Bonjour`, scan `rg SELAS` sur repo | Historique depasse par `WORKSTREAM-TRACE-BOSS-REPORT-001` : SELAS non vierge, suivi alors `STALE`, rattrapage a produire | Produire le rattrapage puis reprendre NotebookLM sur les trous reels ; rester en `NO-GO dev` | Dernier rapport Gad = 2026-06-02 rapport applique dans chat courant sans delta Naomi trace |
| 2026-06-02 | Gad demande : "C'est gad, ou en est Naomi ?" | Depuis le rapport applique dans chat courant sans delta de flux trace 2026-06-02 jusqu'au 2026-06-02 | `PROJECT_CONTROL_TOWER_V1.md`, `04_LAST_STATE.md`, `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `PROJECT_AGENT_ORG_CHART_V1.md`, `SPRINT_SELAS_V1.md`, `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, connecteur GitHub branche `codex/naomie-selas-sprint`, `docs/review/naomie_reporting_freshness_audit_001_report_v1.md`, `docs/review/selas_naomie_backfill_001_report_v1.md`, scan `rg SELAS` sur repo | Historique depasse par `WORKSTREAM-TRACE-BOSS-REPORT-001` : le rapport doit maintenant consolider le flux Naomi SELAS. Rattrapage disponible : SELAS n'est pas vierge, avec sources, catalogue, `DOC-018`, generateur `StatutsSelasMedecinGenerator`, conditions UI, tests et exemples | Reprendre NotebookLM avec Naomi sur les trous reels, tenir worklog + journal a chaque reponse, rester en `NO-GO dev` jusqu'a NotebookLM suffisant, reuse audit, matrice et GO Gad | Dernier rapport Gad = 2026-06-02 rapport Gad courant sans delta de flux trace |
| 2026-06-02 | Gad demande : "C'est gad, ou en est Naomi ?" | Depuis le rapport Gad courant sans delta de flux trace 2026-06-02 jusqu'au 2026-06-02 | `PROJECT_CONTROL_TOWER_V1.md`, `04_LAST_STATE.md`, `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `SPRINT_SELAS_V1.md`, `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, `docs/review/selas_naomie_backfill_001_report_v1.md`, `docs/review/naomie_reporting_freshness_audit_001_report_v1.md`, `git rev-parse --show-toplevel`, `git branch --show-current`, `git remote -v`, `git show-ref refs/remotes/origin/codex/naomie-selas-sprint`, connecteur GitHub branche `codex/naomie-selas-sprint`, scan `rg SELAS` | Aucun delta supplementaire trace depuis le dernier curseur : aucune reponse NotebookLM importee, aucun message Gad en attente, branche distante confirmee via GitHub mais ref locale absente. Le flux Naomi SELAS reste non vierge et rattrape partiellement : sources, catalogue, `DOC-018`, generateur, conditions UI, tests et exemples existent deja | Reprendre NotebookLM avec Naomi sur la reponse brute manquante, puis structurer le journal ; rester en `NO-GO dev` jusqu'a NotebookLM suffisant, reuse audit, matrice et GO Gad | Dernier rapport Gad = 2026-06-02 rapport Gad courant : aucun delta de flux trace depuis le rattrapage |

## Messages Gad a transmettre a Naomi

Regle : Gad peut laisser un message a transmettre a Naomi au prochain echange.
Codex doit citer le message de Gad entre guillemets, puis marquer la ligne
comme `transmis`.

| Date | Auteur | Message exact | Contexte | Statut | Date transmission | Note |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-02 | Gad | Naomi, pour SYDEL ouvre Codex dans `C:\Users\Gad\Desktop\Sydel\sydel-track-b`, pas dans `sydel-document-engine` ni `sydel-track-a`. Dis a Codex de verifier le dossier, la branche et le remote avant toute action ; tu ne fais aucune commande Git toi-meme. | Assainissement Git/worktrees apres confusion racine `sydel-document-engine` vs workspace retenu `sydel-track-b` | a transmettre | - | Message a citer au prochain echange avec Naomi, puis marquer transmis |

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
- 2026-06-02 : un rapport Gad ne doit plus assimiler worklog vide et flux au
  debut. Codex doit parler du flux Naomi SELAS en rapport boss court ; la
  distinction fine reste en preuve interne.
- 2026-06-02 : Gad demande une pyramide d'agents et un chemin de rattrapage
  retroactif. Decision : `PROJECT_AGENT_ORG_CHART_V1.md` devient le registre
  central des agents ; le rattrapage SELAS produit
  `docs/review/selas_naomie_backfill_001_report_v1.md`.
- 2026-06-02 : Gad precise qu'il ne veut pas une evaluation personnelle de
  Naomi. Decision : `WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` devient le
  protocole de tracabilite du flux ; ce n'est pas a Naomi de tenir le suivi.

## Historique

| Date | Acteur | Trace | Impact |
| --- | --- | --- | --- |
| 2026-06-02 | Gad | Demande de formaliser un suivi Naomi generique et supervisable | Creation du protocole orchestrateur Naomi et de ce worklog SELAS |
| 2026-06-02 | Gad | Demande de rapports differentiels et de messages Gad en attente pour Naomi | Ajout des sections `Rapports Gad` et `Messages Gad a transmettre a Naomi` |
| 2026-06-02 | Gad | Capture montrant une branche declaree inaccessible apres `FETCH_HEAD Permission denied` | Correction du diagnostic : branche distante confirmee via connecteur GitHub ; fetch local bloque seulement |
| 2026-06-02 | Gad | Capture d'un rapport disant que Naomi est encore au demarrage NotebookLM alors que le repo contient deja de la matiere SELAS | Diagnostic : chaine de suivi stale ; ajout obligatoire d'un audit de fraicheur et d'un etat reel SELAS hors worklog |
| 2026-06-02 | Gad | Demande d'un organigramme pyramidal des agents et d'un agent retroactif pour retrouver ce qui a ete fait avant le suivi | Creation du registre `PROJECT_AGENT_ORG_CHART_V1.md`; rattrapage SELAS produit avant reprise NotebookLM |
| 2026-06-02 | Codex | Rattrapage retroactif SELAS execute depuis repo, GitHub, threads recents, worklog et journal NotebookLM | Rapport `docs/review/selas_naomie_backfill_001_report_v1.md` cree ; flux Naomi SELAS non vierge |
| 2026-06-02 | Gad | Demande de rapport boss court sur le flux, sans evaluation personnelle de Naomi | Creation de `WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` ; le rapport par defaut devient statut/avancement/prochaine etape/blocage/fiabilite |
