# Sprint SELAS V1

Date d'ouverture : 2026-06-01

## Identite sprint

| Champ | Valeur |
| --- | --- |
| sprint_id | SPRINT-SELAS-V1 |
| Type d'entreprise | SELAS |
| Pilote metier | Naomi |
| Superviseur | Gad |
| Pilote projet / technique | Codex |
| Tour de controle | `docs/project/PROJECT_CONTROL_TOWER_V1.md` |
| Branche cible | `codex/naomie-selas-sprint` |
| Dossier local attendu | Le nom peut etre `sydel-document-engine` chez Naomi ; verifier surtout remote + branche |
| Phase courante | Sync incident : avancee annoncee jusqu'a attente retour humain, non verifiee dans traces publiees |
| Statut courant | `NO-GO dev` tant que commit pousse ou Sync packet absent |
| Derniere action | Gad indique le 2026-06-02 que Naomi a avance SELAS jusqu'a attente retour humain ; branche publiee encore sans preuve correspondante |
| Prochaine action | Resoudre la sync manquante : obtenir commit pousse ou Sync packet de Naomi avant de requalifier l'etat SELAS |
| Worklog Naomi | `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` |
| Agent de tracabilite | `docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` |
| Agent de synchronisation | `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md` |

## Decisions d'ouverture

- La SELAS est le prochain type d'entreprise logique parce qu'elle est proche de
  la SELARL, tout en imposant des controles propres : actions, president,
  eventuels directeurs generaux, statuts SELAS et wording specifique.
- Le travail SELARL doit etre reutilise intelligemment : documents deja traites,
  variables globales, `front_data`, orchestrateur, tests et methode.
- Aucune reutilisation n'est validee par ressemblance seule.
- Naomi ne gere pas Git, les branches, les commandes, les tests, les commits ou
  les push. Codex s'en charge.
- Le sprint est ouvert en `NO-GO dev`.
- Aucun code, aucune generation nouvelle et aucune mise en production SELAS ne
  sont autorises avant les gates.
- Le repo n'est pas vierge cote SELAS : des sources, documents, mappings,
  generateurs, tests et exemples SELAS existent deja. Le flux Naomi doit
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
revanche que le rapport de supervision doit parler du flux Naomi SELAS :
avancement du flux, trous restants, blocages et prochaine etape. La separation
fine entre humain, Codex, repo et outil reste une preuve interne, disponible en
audit detaille seulement.

## Etat des gates

| Gate | Statut | Note |
| --- | --- | --- |
| Branche cible | PRETE A VERIFIER AU DEMARRAGE | `codex/naomie-selas-sprint` geree par Codex |
| Identification Naomi | A CONFIRMER | Si Naomi est l'interlocutrice active, appliquer le protocole runtime ; si Gad parle de Naomi, appliquer l'orchestrateur de suivi |
| Sources | PARTIEL | Sources SELAS deja presentes ; rattrapage et hierarchie a consolider |
| NotebookLM | INCONNU APRES SYNC INCIDENT | Journal NotebookLM SELAS vide cote branche publiee ; Gad annonce une avancee au-dela de cette trace |
| Worklog Naomi | PARTIAL | Worklog ouvert ; doit tracer le flux Naomi, pas seulement les actions humaines |
| Sync Naomi | BLOQUE | Gad annonce SELAS terminee jusqu'a attente retour humain, mais la branche publiee ne contient pas encore cette preuve |
| Rattrapage retroactif | FAIT | Rapport `docs/review/selas_naomie_backfill_001_report_v1.md` ; etat SELAS repo non vierge |
| Audit reutilisation | INCONNU | Peut avoir ete fait dans le thread Naomi, mais pas visible sans sync |
| Matrice documentaire | INCONNU | Peut avoir ete faite dans le thread Naomi, mais pas visible sans sync |
| Parcours metier | INCONNU | Peut avoir ete traite dans le thread Naomi, mais pas visible sans sync |
| Tickets sprint | INCONNU | A verifier via commit pousse ou Sync packet |
| Validation Gad | MANQUANTE DANS TRACES PUBLIEES | Aucun `GO dev` visible cote branche publiee |
| Revue associe | ATTENTE ANNONCEE NON VERIFIEE | Gad indique attente retour humain, a confirmer via sync |

## Reponse obligatoire quand Naomi arrive

Si Naomi est l'interlocutrice active deja identifiee et dit seulement
`Bonjour`, repondre :

```text
Statut sprint : Phase 3 - NOTEBOOKLM / NO-GO dev
Action maintenant : colle le Prompt NotebookLM 01 dans NotebookLM, puis donne-moi la reponse brute.
Point pedagogie : tu n'as pas a gerer Git ni les commandes ; Codex protege la branche, l'ordre du sprint et le passage par NotebookLM avant tout dev.
Prochaine etape : je structure ta reponse dans SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md et je choisis le prompt suivant selon les trous.
```

Puis donner le Prompt NotebookLM 01 complet depuis
`docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md`.

Si Naomi dit `Je suis Naomi. Je veux demarrer le sprint SELAS.`, ou une
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

Chaque reponse NotebookLM donnee par Naomi doit etre structuree dans
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
| 2 | SELAS-NAOMIE-TRACE-RECOVERY-001 | DONE | Reconstituer les traces du flux Naomi SELAS avant suivi complet | Rapport `docs/review/selas_naomie_backfill_001_report_v1.md` + worklog mis a jour |
| 3 | SELAS-REUSE-AUDIT-001 | BLOCKED | Auditer reutilisation SELARL/global | Debloque apres sources/NotebookLM et suivi de flux a jour |
| 4 | SELAS-MATRIX-001 | BLOCKED | Produire matrice documentaire SELAS | Debloque apres reuse audit |
| 5 | SELAS-FRONT-CONTRACT-001 | BLOCKED | Ecrire contrat metier-front | Debloque apres matrice |
| 6 | SELAS-GO-DEV-FIRST-TICKET-001 | BLOCKED | Obtenir GO dev borne | Debloque apres validation Gad |

## Blocages actuels

- Sync Naomi manquante : Gad annonce une avancee jusqu'a attente retour humain,
  mais la branche publiee ne montre pas encore le commit, le pack ou le rapport
  correspondant.
- NotebookLM/reuse/matrice/pack sont `INCONNU` dans les traces publiees, pas
  forcement non faits.
- Aucun `GO dev` donne par Gad n'est visible dans les traces publiees.
- Le rapport boss ne doit pas requalifier SELAS tant que le commit pousse ou le
  Sync packet n'a pas ete recu.

## Prochaine action concrete

1. Demander a Naomi un Sync checkpoint selon
   `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md`.
2. Si le travail est local et coherent, le pousser sur
   `codex/naomie-selas-sprint`.
3. Si le push bloque, produire un Sync packet complet.
4. Lire le commit pousse ou le Sync packet, puis requalifier les gates SELAS :
   NotebookLM, reuse, matrice, pack, retour humain.
5. Rester en `NO-GO dev` tant que la preuve de sync et les gates ne sont pas
   confirmes.

## Statut final

Non applicable. Sprint ouvert, non developpe.
