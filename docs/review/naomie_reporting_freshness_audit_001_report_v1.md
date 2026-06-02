# Naomie reporting freshness audit 001

Date : 2026-06-02

## Objet

Diagnostiquer pourquoi un rapport Gad `ou en est Naomi ?` a repondu que Naomi
etait toujours au demarrage NotebookLM, alors que l'etat reel SELAS du repo est
plus avance qu'un demarrage vierge.

## Sources lues

- `AGENTS.md`
- `docs/project/PROJECT_CONTROL_TOWER_V1.md`
- `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`
- `docs/sprints/SPRINT_SELAS_V1.md`
- `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`
- `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`
- branche GitHub `codex/naomie-selas-sprint`
- commits recents de la branche Naomi
- threads Codex recents du workspace
- scan repo `SELAS` sur docs, sources, code, tests et exemples

## Constat

Le rapport de test n'a pas invente une reponse NotebookLM : le worklog et le
journal NotebookLM etaient effectivement vides.

Mais il a fait un mauvais saut logique :

```text
worklog Naomi vide -> Naomi/projet au debut NotebookLM
```

Ce saut est faux.

La conclusion correcte est :

```text
aucune action personnelle Naomi n'est tracee dans le worklog depuis le curseur,
mais le repo contient deja une matiere SELAS preexistante et le suivi Naomi est
stale/incomplet.
```

## Preuves SELAS ignorees par le rapport

- sources SELAS deja presentes :
  - `project/source_documents/lot_02/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx`
  - `project/source_documents/lot_04/Statuts_SELAS_medecin.docx`
  - `project/source_documents/lot_05/Courrier SDE - SELAS.docx`
  - `project/source_documents/lot_05/PV AGE cession part SCM - SELAS.docx`
  - `project/source_truth/modele Statuts SELAS avec MH.docx`
- `DOC-018` `Statuts SELAS medecin` existe dans le registre.
- `StatutsSelasMedecinGenerator` est branche dans l'orchestrateur.
- Le catalogue metier contient deja des occurrences SELAS.
- Le front/business wizard expose deja des conditions SELAS.
- Des tests et exemples SELAS existent deja.

## Point de rupture

Verdict :

```text
PROJECT_STATE_IGNORED + WORKLOG_STALE
```

La chaine casse au niveau de l'orchestrateur de rapport :

- il lit le worklog et le journal ;
- il verifie la branche ;
- mais il ne compare pas ces traces avec l'etat reel du type SELAS dans le repo ;
- il transforme une absence de trace Naomi en affirmation d'avancement projet.

Il y a aussi un defaut de process :

- le worklog Naomi a ete ouvert apres une partie de la matiere SELAS deja
  presente ;
- il n'a pas ete backfille avec cet etat reel ;
- les rapports differentiels partent donc d'un curseur incomplet.

## Correction decidee

1. Ajouter dans l'orchestrateur Naomi un audit de fraicheur obligatoire.
2. Interdire explicitement la conclusion `worklog vide = projet au debut`.
3. Ajouter dans le worklog SELAS une section `Etat reel SELAS hors worklog`.
4. Mettre a jour le sprint SELAS : la prochaine action n'est plus de donner le
   Prompt 01 comme si le repo etait vierge, mais de backfiller l'etat reel puis
   reprendre NotebookLM sur les trous reels.
5. Dans les rapports Gad, ajouter `Fiabilite du suivi` et `Etat reel du
   projet/type`.

## Reponse attendue desormais

Un rapport Gad doit ressembler a :

```text
Statut Naomi : SYDEL / SPRINT-SELAS-V1 / NotebookLM + backfill suivi / NO-GO dev
Fiabilite du suivi : STALE
Ce que Naomi a fait depuis le dernier rapport : aucune action Naomi personnelle tracee.
Etat reel SELAS : sources, DOC-018, generateur statuts SELAS, catalogue, UI, tests et exemples deja presents.
Point de rupture : worklog non backfille et etat projet ignore.
Action maintenant : backfiller le suivi, puis reprendre NotebookLM sur les trous reels.
```

## Tests

Aucun test Python lance : correction documentaire/protocolaire uniquement.
