# Sprint SELAS V1

Date d'ouverture : 2026-06-01

## Identite sprint

| Champ | Valeur |
| --- | --- |
| sprint_id | SPRINT-SELAS-V1 |
| Type d'entreprise | SELAS |
| Pilote metier | Naomie |
| Superviseur | Gad |
| Pilote projet / technique | Codex |
| Tour de controle | `docs/project/PROJECT_CONTROL_TOWER_V1.md` |
| Branche cible | `codex/naomie-selas-sprint` |
| Dossier local attendu | Le nom peut etre `sydel-document-engine` chez Naomie ; verifier surtout remote + branche |
| Phase courante | 3 - NOTEBOOKLM |
| Statut courant | `NO-GO dev` |
| Derniere action | Audit de fraicheur 2026-06-02 : les rapports Naomi etaient stale car ils ignoraient l'etat SELAS deja present dans le repo |
| Prochaine action | Backfiller l'etat SELAS reel, puis reprendre NotebookLM uniquement sur les trous reels |
| Worklog Naomie | `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` |

## Decisions d'ouverture

- La SELAS est le prochain type d'entreprise logique parce qu'elle est proche de
  la SELARL, tout en imposant des controles propres : actions, president,
  eventuels directeurs generaux, statuts SELAS et wording specifique.
- Le travail SELARL doit etre reutilise intelligemment : documents deja traites,
  variables globales, `front_data`, orchestrateur, tests et methode.
- Aucune reutilisation n'est validee par ressemblance seule.
- Naomie ne gere pas Git, les branches, les commandes, les tests, les commits ou
  les push. Codex s'en charge.
- Le sprint est ouvert en `NO-GO dev`.
- Aucun code, aucune generation nouvelle et aucune mise en production SELAS ne
  sont autorises avant les gates.
- Le repo n'est pas vierge cote SELAS : des sources, documents, mappings,
  generateurs, tests et exemples SELAS existent deja. Le sprint Naomie doit
  consolider/auditer cette matiere, pas pretendre repartir de zero.

## Etat reel SELAS preexistant

Au 2026-06-02, un rapport Gad ne doit pas dire que SELAS est simplement "au
demarrage NotebookLM" sans nuance.

Preuves deja presentes dans le repo :

- sources SELAS :
  - `project/source_documents/lot_02/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx` ;
  - `project/source_documents/lot_04/Statuts_SELAS_medecin.docx` ;
  - `project/source_documents/lot_05/Courrier SDE - SELAS.docx` ;
  - `project/source_documents/lot_05/PV AGE cession part SCM - SELAS.docx` ;
  - `project/source_truth/modele Statuts SELAS avec MH.docx`.
- selection SELAS dans `src/sydel_doc_engine/domain/case_catalog.py` ;
- `DOC-018` `Statuts SELAS medecin` dans
  `src/sydel_doc_engine/registry/catalog.py` ;
- generateur `StatutsSelasMedecinGenerator` branche dans
  `src/sydel_doc_engine/orchestrator/service.py` ;
- conditions UI SELAS dans `src/sydel_doc_engine/app/business_wizard.py` ;
- tests et exemples SELAS.

Cette matiere ne vaut pas validation finale du sprint SELAS. Elle prouve en
revanche que le rapport de supervision doit separer :

- l'avancement personnel de Naomie trace dans le worklog ;
- l'etat reel SELAS deja existant dans le repo ;
- les trous NotebookLM/audit/reuse/matrice restant a combler.

## Etat des gates

| Gate | Statut | Note |
| --- | --- | --- |
| Branche cible | PRETE A VERIFIER AU DEMARRAGE | `codex/naomie-selas-sprint` geree par Codex |
| Identification Naomie | A CONFIRMER | Si Naomie est l'interlocutrice active, appliquer le protocole runtime ; si Gad parle de Naomie, appliquer l'orchestrateur de suivi |
| Sources | PARTIEL | Sources SELAS deja presentes ; backfill et hierarchie a consolider |
| NotebookLM | TRACE INCOMPLETE | Journal NotebookLM SELAS vide ; ne pas confondre avec absence d'etat SELAS repo |
| Worklog Naomie | STALE | Worklog ouvert mais incomplet ; doit distinguer action Naomi et etat reel SELAS |
| Backfill retroactif | FAIT / TRACE PARTIELLE | Rapport `docs/review/selas_naomie_backfill_001_report_v1.md` ; aucune action Naomi personnelle prouvee, etat SELAS repo non vierge |
| Audit reutilisation | BLOQUE | Interdit tant que le sous-sprint NotebookLM n'est pas suffisant |
| Matrice documentaire | BLOQUE | Interdite tant que NotebookLM et reuse audit ne sont pas faits |
| Parcours metier | A FAIRE | Definir saisie, roles, adresses, reutilisations |
| Tickets sprint | A FAIRE | Ecrire les tickets avant dev |
| Validation Gad | MANQUANTE | Aucun `GO dev` donne |
| Revue associe | NON APPLICABLE | Seulement en fin de sprint |

## Reponse obligatoire quand Naomie arrive

Si Naomie est l'interlocutrice active deja identifiee et dit seulement
`Bonjour`, repondre :

```text
Statut sprint : Phase 3 - NOTEBOOKLM / NO-GO dev
Action maintenant : colle le Prompt NotebookLM 01 dans NotebookLM, puis donne-moi la reponse brute.
Point pedagogie : tu n'as pas a gerer Git ni les commandes ; Codex protege la branche, l'ordre du sprint et le passage par NotebookLM avant tout dev.
Prochaine etape : je structure ta reponse dans SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md et je choisis le prompt suivant selon les trous.
```

Puis donner le Prompt NotebookLM 01 complet depuis
`docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md`.

Si Naomie dit `Je suis Naomie. Je veux demarrer le sprint SELAS.`, ou une
variante comme `je veux lancer/reprendre le sprint SELAS/CELAS`, Codex ne doit
pas partir en production, ni en generation, ni en audit, ni en matrice finale.
Il doit lancer uniquement le sous-sprint NotebookLM.

Reponse attendue :

```text
Statut sprint : Phase 3 - NOTEBOOKLM / NO-GO dev
Action maintenant : colle le Prompt NotebookLM 01 dans NotebookLM, puis donne-moi la reponse brute.
Point pedagogie : on collecte d'abord la matiere metier ; Codex la transforme ensuite en journal, puis en prompts de precision.
Prochaine etape : je structure ta reponse dans SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md et je choisis le prompt suivant selon les trous.
```

Puis donner le Prompt NotebookLM 01 complet depuis
`docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md`.

Si un nouveau chat dit seulement `Bonjour` sans identite explicite, ne pas
declencher ce bloc. Demander d'abord :

```text
Bonjour, tu es Gad ou Naomi ?
Je te route ensuite sur le bon protocole projet.
```

Reponse explicitement interdite :

```text
Bonjour Naomi ! Je suis pret. Tu veux qu'on attaque quoi dans le moteur documentaire ?
```

Cette reponse doit etre consideree comme un incident de workflow : elle ne
verifie pas la branche, ne rappelle pas le `NO-GO dev`, ne contient pas le point
pedagogie et risque de lancer du travail sans NotebookLM.

## Questions NotebookLM initiales

Ces questions sont a poser avant toute matrice finale. Codex peut en ajouter.
Pour respecter les limites de caracteres NotebookLM, elles ne doivent pas etre
envoyees toutes ensemble. Utiliser les prompts courts de
`docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md`.

Chaque reponse NotebookLM donnee par Naomie doit etre structuree dans
`docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` avant de passer au prompt
suivant.

1. Pour une SELAS, quels documents doivent etre generes a la creation ?
2. Quels documents SELAS sont identiques aux documents SELARL deja traites ?
3. Quels documents SELAS sont proches des documents SELARL mais exigent une
   verification de wording ou de conditions ?
4. Quels documents SELAS sont toujours attendus ?
5. Quels documents SELAS sont conditionnels ?
6. Quels documents SELAS doivent rester a remplir a la main ?
7. Quels documents SELAS sont reserves faute de source ou de decision humaine ?
8. Quelles differences entre SELARL et SELAS impactent les statuts ?
9. Quelles differences entre gerant SELARL et president SELAS impactent le PV ?
10. Faut-il prevoir un directeur general ou uniquement un president en V1 ?
11. Quelles variables SELARL peuvent etre reutilisees sans changement ?
12. Quelles variables ont le meme libelle mais un role different en SELAS ?
13. Les documents d'ordre professionnel couvrent-ils la SELAS dans les sources ?
14. Les documents de regime communautaire couvrent-ils la SELAS ?
15. Les documents de cession cabinet ou SCM sont-ils pertinents pour SELAS ?
16. Quels cas simples SELAS doivent etre couverts en premier ?
17. Quels cas SELAS complexes doivent rester bloques en V1 ?
18. Quels retours humains SELARL ne doivent pas etre transposes a SELAS ?
19. Quels scenarios de smoke SELAS sont indispensables ?
20. Qu'est-ce qui permettrait a l'associe de valider le sprint SELAS a 100 % ?

## Hypotheses de reutilisation a verifier

Ces lignes ne sont pas des validations. Elles guident l'audit `Reuse Auditor`.

| Element | Hypothese | Statut |
| --- | --- | --- |
| DOC-001 non-condamnation | Probable reutilisation forte | A verifier |
| DOC-002 domiciliation | Probable reutilisation forte | A verifier |
| DOC-003 procuration | Probable reutilisation forte | A verifier |
| DOC-004 PV nomination gerant | Non identique : SELAS implique president / gouvernance | A adapter ou no-go |
| DOC-005 regime communautaire | Peut couvrir SELAS selon source/spec | A verifier |
| DOC-006 avertissement conjoint | Reserve deja sensible | NO-GO sans source/decision |
| DOC-034 ordre | Spec semble couvrir SELAS | A verifier |
| Statuts SELAS | Source/spec existe cote statuts SEL | A analyser |
| Front SELARL | Methode reutilisable, pas copie directe | A adapter |
| Variables capital/parts/actions | Attention parts sociales vs actions | A verifier |

## Matrice documentaire

Statut : A FAIRE.

| Condition | Document | Code | Statut source | Statut moteur | Statut front | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| SELAS creation | A inventorier | A definir | A verifier | A verifier | A verifier | `NO-GO dev` |

## Audit reutilisation

Statut : A FAIRE.

| Element | Source existante | Conditions identiques ? | Variables identiques ? | Decision | Action |
| --- | --- | --- | --- | --- | --- |
| Socle SELARL | SELARL Track B | A verifier | A verifier | `reuse-check` | Lancer Reuse Auditor |

## Tickets du sprint

Statut : A FAIRE.

| Ordre | Ticket | Statut | Objet | Criteria |
| --- | --- | --- | --- | --- |
| 1 | SELAS-SOURCES-NOTEBOOKLM-001 | IN_PROGRESS | Piloter la boucle NotebookLM par prompts courts | Reponses structurees dans `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, contradictions listees |
| 2 | SELAS-NAOMIE-BACKFILL-001 | DONE | Reconstituer les traces SELAS/Naomie avant suivi complet | Rapport `docs/review/selas_naomie_backfill_001_report_v1.md` + worklog mis a jour, sans attribution Naomi non prouvee |
| 3 | SELAS-REUSE-AUDIT-001 | BLOCKED | Auditer reutilisation SELARL/global | Debloque apres sources/NotebookLM + backfill |
| 4 | SELAS-MATRIX-001 | BLOCKED | Produire matrice documentaire SELAS | Debloque apres reuse audit |
| 5 | SELAS-FRONT-CONTRACT-001 | BLOCKED | Ecrire contrat metier-front | Debloque apres matrice |
| 6 | SELAS-GO-DEV-FIRST-TICKET-001 | BLOCKED | Obtenir GO dev borne | Debloque apres validation Gad |

## Blocages actuels

- NotebookLM non interroge.
- Le suivi Naomi/worklog est backfille, mais aucune action Naomi personnelle n'est prouvee dans les traces accessibles.
- Audit de reutilisation non fait.
- Matrice documentaire non faite.
- Aucun `GO dev` donne par Gad.
- Aucune revue associe possible tant qu'aucun pack SELAS n'existe.

## Prochaine action concrete

1. Faire un audit de fraicheur avant tout nouveau rapport Gad : worklog,
   NotebookLM, branche, threads, sources, catalogue, generateurs, tests.
2. Backfiller le worklog avec l'etat SELAS reel deja present dans le repo.
3. Quand Naomie arrive, verifier la branche `codex/naomie-selas-sprint`.
4. Donner a Naomie la prochaine action NotebookLM seulement apres avoir indique
   que la mission consiste a consolider les trous reels, pas a repartir de zero.
5. Structurer chaque reponse dans le journal, mettre a jour le worklog Naomie,
   puis choisir le prompt suivant selon les trous.
6. Rester en `NO-GO dev` tant que NotebookLM/reuse/matrice/GO Gad ne sont pas
   passes.

## Statut final

Non applicable. Sprint ouvert, non developpe.
