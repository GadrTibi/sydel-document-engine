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
| Phase courante | 31 - HUMAN REVIEW PACK SELAS |
| Statut courant | `SELAS-HUMAN-REVIEW-PACK-001` realise ; pack pret pour revue humaine ; attente retour Gad / associe / juriste |
| Derniere action | Pack de revue humaine prepare avec DOCX happy path, DOCX regime communautaire, checklist, questions de revue, pre-check NotebookLM et ZIP |
| Prochaine action | Transmettre le pack de revue a Gad / associe / juriste ; apres retour, lancer `SELAS-HUMAN-FIXES-001` si corrections |

## Decisions d'ouverture

- La SELAS est le prochain type d'entreprise logique parce qu'elle est proche de
  la SELARL, tout en imposant des controles propres : actions, president,
  eventuels directeurs generaux, statuts SELAS et wording specifique.
- Le travail SELARL doit etre reutilise intelligemment : documents deja traites,
  variables globales, `front_data`, orchestrateur, tests et methode.
- Aucune reutilisation n'est validee par ressemblance seule.
- Naomie ne gere pas Git, les branches, les commandes, les tests, les commits ou
  les push. Codex s'en charge.
- Le sprint a recu un `GO dev` borne pour `SELAS-FRONT-SCHEMA-001`.
- Le sprint a recu un `GO dev` borne pour `SELAS-DOC003-PROCURATION-PRESIDENT-001`.
- Le sprint a recu un `GO dev` borne utilisateur pour `SELAS-DOC001-DNC-PRESIDENT-001`.
- Le sprint a recu un `GO dev` borne utilisateur pour `SELAS-DOC002-DOMICILIATION-001`.
- `DOC-003` est maintenant SELAS-safe pour le cas President unique, mais aucun
  pack SELAS complet, aucune mise en production SELAS et aucun autre wording
  juridique ne sont autorises avant les gates documentaires suivants.
- `DOC-001` DNC President est maintenant specifie en reutilisation canonique :
  la filiation reste obligatoire, l'ambiguite NotebookLM est documentee, et la
  generation reste bloquee sans donnees President/signataire completes.
- `DOC-002` Autorisation de domiciliation est maintenant specifie en
  reutilisation canonique : le document est neutre vis-a-vis SELARL/SELAS et
  President/Gerant, mais la generation SELAS V1 est autorisee seulement si la
  domiciliation correspond au siege/cabinet via une regle explicite.
- `SELAS-DECISION-PRESIDENT` est maintenant specifie comme document candidat
  separe : `DOC-004` peut inspirer la structure, mais son wording/generateur
  `PV nomination gerant` ne doit pas etre reutilise directement pour SELAS.
- `DOC-018` Statuts SELAS medecin est maintenant specifie pour le parcours
  actionnaire unique / President unique : la nomination President est absorbee
  par les statuts V1, tandis que Directeur General nomme, multi-actionnaires,
  droits derogatoires et actions complexes restent bloques.
- Le bloc capital / actions SELAS V1 est maintenant specifie : actions
  ordinaires, actionnaire unique a 100 %, droits proportionnels et numerotation
  simple derivee `1 a N`, sans insertion de wording non present dans la source.
- `DOC-034` Demande d'inscription a l'Ordre est maintenant specifie pour la
  SELAS V1 : reutilisation autorisee avec overlay SELARL/SELAS, sans confusion
  entre le president du Conseil de l'Ordre et le President SELAS, et avec
  plans/devis comme pieces attendues non generees.
- Le batch regime communautaire SELAS V1 est maintenant specifie : `DOC-005`
  et `DOC-006` sont conditionnels si le dossier est marie sous regime
  communautaire ; `DOC-006` est sorti de reserve dans le schema front/data,
  sans activation du pack SELAS complet.
- La roadmap A-Z SELAS V1 est maintenant produite : le prochain passage dev
  doit commencer par `DOC-034`, puis `DOC-005`/`DOC-006`, puis `DOC-018`, avant
  readiness front, orchestration pack, smoke tests, revue humaine et cloture.
- La roadmap A-Z est validee pour avancer, avec ajout d'un gate trois sources
  avant cloture : `Documents_a_generer_par_cas.docx`, NotebookLM SELAS et
  retours humains sur la premiere version complete.
- `DOC-034` Demande d'inscription a l'Ordre est maintenant SELAS-safe cote
  schema/front-data et generateur pour le parcours V1 simple, sous reserve de
  relancer `pytest` et `ruff` dans un environnement equipe.
- `DOC-005` et `DOC-006` Regime communautaire sont maintenant SELAS-safe cote
  schema/front-data pour le parcours conditionnel : le parcours simple ne les
  expose pas, et le parcours regime communautaire affiche les deux candidats
  ensemble.
- `DOC-018` Statuts SELAS medecin est maintenant SELAS-safe pour le parcours
  actionnaire unique / President unique : capital/actions coherents, cas
  complexes bloques, nomination President absorbee par les statuts, et
  `DOC-004` non selectionne dans ce contexte.
- La readiness front/data du pack SELAS V1 est maintenant alignee : le front
  distingue les documents prets, conditionnels et reserves, mais la generation
  de pack reste inactive jusqu'au ticket d'orchestration.
- L'orchestrateur sait maintenant selectionner le pack SELAS V1 via le contexte
  dossier sans activer les cas hors V1 ; le pack reste non valide final tant que
  les smokes, le checkpoint trois sources et la revue humaine ne sont pas faits.
- Le smoke happy path SELAS V1 est passe : le pack simple sans regime
  communautaire genere 5 DOCX attendus et n'active pas les documents
  conditionnels ou reserves.
- Le smoke regime communautaire SELAS V1 est passe : le pack conditionnel
  genere 7 DOCX attendus, ajoute `DOC-005` et `DOC-006`, et n'active pas les
  documents reserves ou complexes.
- L'anti-regression wording SELAS V1 est passe en strict : aucun `SELARL`,
  `Gerant` ou `parts sociales` dans les deux packs ; les occurrences
  `associe` / `associé` sont classees comme points a verifier au checkpoint
  trois sources.

## Etat des gates

| Gate | Statut | Note |
| --- | --- | --- |
| Branche cible | PRETE A VERIFIER AU DEMARRAGE | `codex/naomie-selas-sprint` geree par Codex |
| Identification Naomie | A CONFIRMER | Si le contexte ou le titre indique Naomie, appliquer quand meme le protocole runtime |
| Sources | PARTIAL | Sources NotebookLM nommees (`Texte colle`, `Besoins Sydel (juridique).pdf`, `Notre job - Sydel.pdf`) mais passages exacts encore a verifier |
| NotebookLM | SUFFISANT POUR PREPARER AUDIT | Prompts 01 a 07 + suivi sources journalises ; aucun `GO dev` |
| Audit reutilisation | REALISE V1 | `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md`; aucun `GO dev` |
| Matrice documentaire | REALISEE V1 | `docs/sprints/SPRINT_SELAS_MATRIX_001.md`; aucun `GO dev` |
| Parcours metier | REALISE V1 | `docs/sprints/SPRINT_SELAS_FRONT_CONTRACT_001.md`; aucun `GO dev` |
| Tickets sprint | REALISES V1 | `docs/sprints/SPRINT_SELAS_TICKETS_001.md`; ordre des tickets, dependances et reserves documentes |
| Validation Gad | GO DEV BORNE | Gad a repondu `ok go` apres la proposition de socle commun SELAS reutilisable |
| Dev limite | REALISE PARTIELLEMENT | `SELAS-FRONT-SCHEMA-001` code et verifie par compilation/import/tests manuels ; `pytest`/`ruff` indisponibles localement |
| Spec President | REALISEE V1 | `docs/sprints/SPRINT_SELAS_SPEC_PRESIDENT_001.md`; aucun wording juridique final valide |
| Spec Procuration | REALISEE V1 | `docs/sprints/SPRINT_SELAS_SPEC_PROCURATION_001.md`; autorise une demande de `GO dev` borne sur `DOC-003` |
| Dev DOC-003 Procuration | REALISE PARTIAL QA | Verrou SELAS/President code ; generation manuelle DOCX verifiee ; `pytest`/`ruff` indisponibles localement |
| Spec DNC President | REALISEE V1 | `docs/sprints/SPRINT_SELAS_SPEC_DNC_PRESIDENT_001.md`; `DOC-001` reutilisable avec President signataire et filiation obligatoire |
| Dev DOC-001 DNC President | REALISE PARTIAL QA | Schema SELAS DNC aligne, tests cibles ajoutes, smoke manuel DOCX verifie ; `pytest`/`ruff` indisponibles localement |
| Spec DOC-002 Domiciliation | REALISEE V1 | `docs/sprints/SPRINT_SELAS_SPEC_DOC002_DOMICILIATION_001.md`; `DOC-002` reutilisable comme document neutre seulement si domiciliation = siege/cabinet |
| Dev DOC-002 Domiciliation | REALISE PARTIAL QA | Schema SELAS DOC-002 aligne, regle reuse siege->domiciliation obligatoire, tests generateur/schema ajoutes, smoke manuel DOCX verifie ; `pytest`/`ruff` indisponibles localement |
| Spec Decision President | REALISEE V1 | `docs/sprints/SPRINT_SELAS_SPEC_DECISION_PRESIDENT_001.md`; `DOC-004` patron structurel seulement, acte separe reserve car la nomination President est absorbee par les statuts V1 |
| Spec Statuts SELAS medecin AU | REALISEE V1 | `docs/sprints/SPRINT_SELAS_SPEC_STATUTS_MEDECIN_AU_001.md`; `DOC-018` candidat V1, nomination President dans les statuts, cas complexes bloques |
| Spec Capital / Actions | REALISEE V1 | `docs/sprints/SPRINT_SELAS_SPEC_CAPITAL_ACTIONS_001.md`; actions ordinaires uniquement, coherence capital/actions/valeur nominale et numerotation simple `1 a N` |
| Spec Ordre | REALISEE V1 | `docs/sprints/SPRINT_SELAS_SPEC_ORDRE_001.md`; `DOC-034` reutilisable pour SELAS via overlay SELARL/SELAS, pieces plans/devis reservees comme pieces attendues |
| Spec Regime communautaire | REALISEE V1 | `docs/sprints/SPRINT_SELAS_SPEC_REGIME_COMMUNAUTAIRE_001.md`; `DOC-005` et `DOC-006` conditionnels si regime communautaire |
| Roadmap A-Z SELAS | VALIDEE POUR AVANCER | `docs/sprints/SPRINT_SELAS_ROADMAP_TO_COMPLETION_001.md`; ordre officiel propose jusqu'a cloture SELAS V1, avec gate trois sources avant cloture |
| Dev DOC-034 Ordre | REALISE PARTIAL QA | `docs/sprints/SPRINT_SELAS_DOC034_ORDRE_001.md`; schema SELAS aligne, tests cibles ajoutes, smoke manuel DOCX OK ; `pytest`/`ruff` indisponibles localement |
| Dev DOC-005/DOC-006 Regime communautaire | REALISE PARTIAL QA | `docs/sprints/SPRINT_SELAS_DOC005_DOC006_REGIME_COMMUNAUTAIRE_001.md`; batch conditionnel SELAS aligne, `DOC-006` sorti de reserve, smoke manuel DOCX OK ; `pytest`/`ruff` indisponibles localement |
| Dev DOC-018 Statuts SELAS medecin AU | REALISE PARTIAL QA | `docs/sprints/SPRINT_SELAS_DOC018_STATUTS_MEDECIN_AU_001.md`; verrous capital/actions et hors V1 ajoutes, `DOC-004` non selectionne, smoke manuel DOCX OK ; `pytest`/`ruff` indisponibles localement |
| Dev Front readiness pack SELAS | REALISE PARTIAL QA | `docs/sprints/SPRINT_SELAS_FRONT_READINESS_PACK_001.md`; pack simple/conditionnel/reserve aligne cote front/data, generation toujours inactive ; `pytest`/`ruff` indisponibles localement |
| Dev Orchestrator pack SELAS | REALISE PARTIAL QA | `docs/sprints/SPRINT_SELAS_ORCHESTRATOR_PACK_001.md`; selection explicite du pack simple/conditionnel, cas hors V1 bloques ; `pytest`/`ruff` indisponibles localement |
| Smoke Happy Path SELAS | REALISE PARTIAL QA | `docs/sprints/SPRINT_SELAS_SMOKE_HAPPY_PATH_001.md`; pack simple sans regime communautaire genere, controles terminologiques et documents parasites OK |
| Smoke Regime communautaire SELAS | REALISE PARTIAL QA | `docs/sprints/SPRINT_SELAS_SMOKE_REGIME_COMMUNAUTAIRE_001.md`; pack conditionnel genere avec `DOC-005`/`DOC-006`, controles terminologiques et documents parasites OK |
| Anti-regression wording SELAS | REALISE PARTIAL QA | `docs/sprints/SPRINT_SELAS_ANTI_REGRESSION_WORDING_001.md`; strict OK, occurrences `associe` a verifier au checkpoint trois sources |
| Triple source check SELAS | REALISE PARTIAL QA | `docs/sprints/SPRINT_SELAS_TRIPLE_SOURCE_CHECK_001.md`; source metier + NotebookLM alignes sur perimetre V1, retour humain pack encore absent |
| Revue associe | PACK PRET | `docs/sprints/SPRINT_SELAS_HUMAN_REVIEW_PACK_001.md`; ZIP et questions de revue prets, retour humain attendu |

## Reponse obligatoire quand Naomie arrive

Si Naomie dit seulement `Bonjour`, repondre :

```text
Statut sprint : Phase 31 - HUMAN REVIEW PACK SELAS / `SELAS-HUMAN-REVIEW-PACK-001` realise
Action maintenant : transmettre le ZIP et les questions a Gad / associe / juriste.
Point pedagogie : Codex a prepare le pack ; la validation juridique finale doit maintenant venir d'une relecture humaine.
Prochaine etape : classer le retour humain puis lancer `SELAS-HUMAN-FIXES-001` si corrections.
```

Si Naomie dit `Je suis Naomie. Je veux demarrer le sprint SELAS.`, ou une
variante comme `je veux lancer/reprendre le sprint SELAS/CELAS`, Codex doit lire
l'etat courant ci-dessus. Il ne relance pas le Prompt NotebookLM 01 par defaut :
il reprend l'action courante du sprint, sauf si une source precise manque et
necessite un nouveau prompt cible.

Reponse attendue :

```text
Statut sprint : Phase 31 - HUMAN REVIEW PACK SELAS / `SELAS-HUMAN-REVIEW-PACK-001` realise
Action maintenant : transmettre le ZIP et les questions a Gad / associe / juriste.
Point pedagogie : la methode SELARL est conservee ; apres les controles internes, la prochaine securite est la relecture humaine.
Prochaine etape : classer le retour humain puis lancer `SELAS-HUMAN-FIXES-001` si corrections.
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
| DOC-006 avertissement conjoint | Batch conditionnel regime communautaire | Specifie et code en QA partielle |
| DOC-034 ordre | Spec semble couvrir SELAS | A verifier |
| Statuts SELAS | Source/spec existe cote statuts SEL | A analyser |
| Front SELARL | Methode reutilisable, pas copie directe | A adapter |
| Variables capital/parts/actions | Attention parts sociales vs actions | A verifier |

## Matrice documentaire

Statut : REALISEE V1.

| Condition | Document | Code | Statut source | Statut moteur | Statut front | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| SELAS medecin actionnaire unique simple | Pack candidat : `DOC-001`, `DOC-002`, `DOC-003`, decision/PV president, `DOC-034`, `DOC-018`, `DOC-005`/`DOC-006` conditionnels | Voir `SPRINT_SELAS_MATRIX_001.md` | Partiel | Non generatif | Schema front/data code | `NO-GO generation` |

## Audit reutilisation

Statut : REALISE V1.

| Element | Source existante | Conditions identiques ? | Variables identiques ? | Decision | Action |
| --- | --- | --- | --- | --- | --- |
| Socle SELARL / global | `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md` | Variables et methode reutilisables, wording non reutilisable tel quel | A adapter selon roles SELAS | `reuse-check` / `adapter` / `no-go` selon document | Matrice, contrat front et tickets V1 produits |

## Tickets du sprint

Statut : REALISE V1, premier dev borne autorise.

| Ordre | Ticket | Statut | Objet | Criteria |
| --- | --- | --- | --- | --- |
| 1 | SELAS-SOURCES-NOTEBOOKLM-001 | DONE | Piloter la boucle NotebookLM par prompts courts | Prompts 01 a 07 + suivi sources structures dans `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` |
| 2 | SELAS-REUSE-AUDIT-001 | DONE | Auditer reutilisation SELARL/global | Audit lecture seule produit dans `SPRINT_SELAS_REUSE_AUDIT_001.md` |
| 3 | SELAS-MATRIX-001 | DONE | Produire matrice documentaire SELAS | Matrice lecture seule produite dans `SPRINT_SELAS_MATRIX_001.md` |
| 4 | SELAS-FRONT-CONTRACT-001 | DONE | Ecrire contrat metier-front | Contrat lecture seule produit dans `SPRINT_SELAS_FRONT_CONTRACT_001.md` |
| 5 | SELAS-TICKETS-001 | DONE | Preparer les tickets SELAS ordonnes | Backlog lecture seule produit dans `SPRINT_SELAS_TICKETS_001.md` |
| 6 | SELAS-GO-DEV-FIRST-TICKET-001 | DONE | Obtenir GO dev borne | Demande d'arbitrage Gad preparee dans `SPRINT_SELAS_GO_DEV_FIRST_TICKET_001.md`; aucun code avant validation |
| 7 | SELAS-GAD-FEEDBACK-001 | DONE | Repondre au retour Gad sur cas par cas et reutilisation | Reponse reformulee dans `SPRINT_SELAS_GAD_FEEDBACK_001.md`; aucun code |
| 8 | SELAS-FRONT-SCHEMA-001 | DONE_PARTIAL_QA | Premier ticket dev borne | Socle commun SELAS front/data code ; compilation/import/tests manuels OK ; `pytest`/`ruff` a relancer en environnement equipe |
| 9 | SELAS-SPEC-PRESIDENT-001 | DONE | Specifier le role President SELAS | Spec metier produite dans `SPRINT_SELAS_SPEC_PRESIDENT_001.md`; aucun DOCX/PDF/ZIP, aucun wording final valide |
| 10 | SELAS-SPEC-PROCURATION-001 | DONE | Verrouiller l'adaptation SELAS de `DOC-003` procuration | Spec documentaire produite dans `SPRINT_SELAS_SPEC_PROCURATION_001.md`; futur code borne possible sur `DOC-003` |
| 11 | SELAS-DOC003-PROCURATION-PRESIDENT-001 | DONE_PARTIAL_QA | Coder le verrou SELAS/President de `DOC-003` | `DOC-003` force `President` pour SELAS, bloque `Gerant` et `Directeur General`, tests cibles ajoutes ; compilation et smoke manuel OK ; `pytest`/`ruff` indisponibles localement |
| 12 | SELAS-SPEC-DNC-PRESIDENT-001 | DONE | Verrouiller la reutilisation SELAS de `DOC-001` DNC President | Spec documentaire produite dans `SPRINT_SELAS_SPEC_DNC_PRESIDENT_001.md`; filiation obligatoire, mapping President/signataire explicite, futur code borne possible sur `DOC-001` |
| 13 | SELAS-DOC001-DNC-PRESIDENT-001 | DONE_PARTIAL_QA | Coder l'adaptation bornee de `DOC-001` DNC President | Schema SELAS `DOC-001` exige President/Signataire, filiation et signature ; tests generateur/schema ajoutes ; compilation et smoke manuel OK ; `pytest`/`ruff` indisponibles localement |
| 14 | SELAS-SPEC-DOC002-DOMICILIATION-001 | DONE | Verrouiller la reutilisation SELAS de `DOC-002` Domiciliation | Spec documentaire produite dans `SPRINT_SELAS_SPEC_DOC002_DOMICILIATION_001.md`; reutilisation neutre autorisee seulement si domiciliation = siege/cabinet |
| 15 | SELAS-DOC002-DOMICILIATION-001 | DONE_PARTIAL_QA | Coder l'adaptation bornee de `DOC-002` Domiciliation pour SELAS President unique | Schema SELAS `DOC-002` exige President/Signataire/Societe, siege et reuse siege->domiciliation ; tests generateur/schema ajoutes ; compilation et smoke manuel OK ; `pytest`/`ruff` indisponibles localement |
| 16 | SELAS-SPEC-DECISION-PRESIDENT-001 | DONE | Verrouiller Decision/PV nomination President SELAS | Spec documentaire produite dans `SPRINT_SELAS_SPEC_DECISION_PRESIDENT_001.md`; `DOC-004` patron structurel seulement, futur code bloque sans source texte/statuts |
| 17 | SELAS-SPEC-STATUTS-MEDECIN-AU-001 | DONE | Verrouiller Statuts SELAS medecin actionnaire unique | Spec documentaire produite dans `SPRINT_SELAS_SPEC_STATUTS_MEDECIN_AU_001.md`; `DOC-018` candidat V1, President dans les statuts, DG nomme/multi-actionnaires/actions complexes bloques |
| 18 | SELAS-SPEC-CAPITAL-ACTIONS-001 | DONE | Verrouiller capital, actions, valeur nominale et numerotation V1 | Spec documentaire produite dans `SPRINT_SELAS_SPEC_CAPITAL_ACTIONS_001.md`; actions ordinaires, actionnaire unique 100 %, droits proportionnels et numerotation derivee `1 a N` |
| 19 | SELAS-SPEC-ORDRE-001 | DONE | Verrouiller la demande d'inscription a l'Ordre SELAS | Spec documentaire produite dans `SPRINT_SELAS_SPEC_ORDRE_001.md`; `DOC-034` reutilisable via overlay SELARL/SELAS, President ordinal distinct du President SELAS, plans/devis en pieces attendues |
| 20 | SELAS-SPEC-REGIME-COMMUNAUTAIRE-001 | DONE | Verrouiller le regime communautaire SELAS | Spec documentaire produite dans `SPRINT_SELAS_SPEC_REGIME_COMMUNAUTAIRE_001.md`; `DOC-005` et `DOC-006` conditionnels |
| 21 | SELAS-ROADMAP-TO-COMPLETION-001 | DONE | Ecrire l'ordre A-Z jusqu'a cloture SELAS V1 | Roadmap produite dans `SPRINT_SELAS_ROADMAP_TO_COMPLETION_001.md`; validee pour avancer, gate trois sources ajoute avant cloture |
| 22 | SELAS-DOC034-ORDRE-001 | DONE_PARTIAL_QA | Brancher `DOC-034` Demande d'inscription a l'Ordre pour SELAS | Schema SELAS DOC-034 aligne, tests cibles ajoutes, smoke manuel DOCX OK ; `pytest`/`ruff` indisponibles localement |
| 23 | SELAS-DOC005-DOC006-REGIME-COMMUNAUTAIRE-001 | DONE_PARTIAL_QA | Brancher le batch conditionnel regime communautaire SELAS | Schema SELAS DOC-005/DOC-006 aligne, `DOC-006` sorti de reserve, tests cibles ajoutes, smoke manuel DOCX OK ; `pytest`/`ruff` indisponibles localement |
| 24 | SELAS-DOC018-STATUTS-MEDECIN-AU-001 | DONE_PARTIAL_QA | Brancher `DOC-018` Statuts SELAS medecin actionnaire unique | Verrous capital/actions et cas hors V1 ajoutes ; `DOC-004` non selectionne si nomination President absorbee par les statuts ; smoke manuel DOCX OK ; `pytest`/`ruff` indisponibles localement |
| 25 | SELAS-FRONT-READINESS-PACK-001 | DONE_PARTIAL_QA | Aligner la readiness front/data du pack SELAS V1 | Pack simple, conditionnel et reserve expose cote schema ; generation toujours inactive ; prochain ticket `SELAS-ORCHESTRATOR-PACK-001` |
| 26 | SELAS-ORCHESTRATOR-PACK-001 | DONE_PARTIAL_QA | Brancher la selection orchestrateur du pack SELAS V1 | Selection simple/conditionnelle alignee sur readiness ; cas hors V1 bloques ; prochain ticket `SELAS-SMOKE-HAPPY-PATH-001` |
| 27 | SELAS-SMOKE-HAPPY-PATH-001 | DONE_PARTIAL_QA | Generer et verifier le pack SELAS simple sans regime communautaire | 5 DOCX generes : `DOC-001`, `DOC-002`, `DOC-003`, `DOC-034`, `DOC-018`; pas de `DOC-004`, pas de `DOC-005`/`DOC-006`, controles placeholders/SELARL/Gerant/parts sociales OK |
| 28 | SELAS-SMOKE-REGIME-COMMUNAUTAIRE-001 | DONE_PARTIAL_QA | Generer et verifier le pack SELAS avec regime communautaire | 7 DOCX generes : `DOC-001`, `DOC-002`, `DOC-003`, `DOC-034`, `DOC-018`, `DOC-005`, `DOC-006`; pas de `DOC-004`, cession, SCM, bail, derogations, controles placeholders/SELARL/Gerant/parts sociales OK |
| 29 | SELAS-ANTI-REGRESSION-WORDING-001 | DONE_PARTIAL_QA | Verifier les mots sensibles SELAS dans les deux packs smoke | Strict OK : aucun `SELARL`, `Gerant`, `parts sociales`; occurrences `associe` classees pour revue trois sources |
| 30 | SELAS-TRIPLE-SOURCE-CHECK-001 | DONE_PARTIAL_QA | Comparer le pack SELAS V1 aux trois reperes projet | Source metier + NotebookLM alignes sur le perimetre V1 ; retour Gad strategie pris en compte ; revue humaine pack absente donc `NO-GO cloture`, prochain `SELAS-HUMAN-REVIEW-PACK-001` |
| 31 | SELAS-HUMAN-REVIEW-PACK-001 | DONE_WAITING_HUMAN_REVIEW | Preparer le pack SELAS V1 pour revue Gad / associe / juriste | ZIP, inventaire, checklist, questions de revue et pre-check NotebookLM produits ; pack non valide final tant que le retour humain n'est pas classe |

## Blocages actuels

- Sources NotebookLM seulement partielles : documents nommes, passages/pages non extraits.
- Audit de reutilisation V1 fait, mais il ne vaut pas validation juridique.
- Matrice documentaire V1 faite, mais elle ne vaut pas validation juridique.
- Contrat metier-front SELAS V1 fait, mais il ne vaut pas validation juridique.
- Tickets de sprint SELAS prepares en V1.
- Demande d'arbitrage premier ticket preparee.
- Retour Gad sur reutilisation/cas par cas analyse.
- `GO dev SELAS-FRONT-SCHEMA-001` donne oralement par Gad via Naomie (`ok go`), borne au socle front/data sans generation.
- `SELAS-FRONT-SCHEMA-001` implemente ; validation complete limitee par absence locale de `pytest` et `ruff`.
- `SELAS-SPEC-PRESIDENT-001` realise ; il autorise les specs documentaires suivantes mais pas la generation.
- `SELAS-SPEC-PROCURATION-001` realise ; il autorise une demande de `GO dev` borne sur `DOC-003`, pas la generation du pack SELAS.
- `SELAS-DOC003-PROCURATION-PRESIDENT-001` code ; `DOC-003` est SELAS-safe pour President unique, mais aucun pack SELAS n'est active.
- `SELAS-SPEC-DNC-PRESIDENT-001` realise ; il autorise une demande de `GO dev` borne sur `DOC-001`, mais pas la generation du pack SELAS.
- `SELAS-DOC001-DNC-PRESIDENT-001` code ; `DOC-001` est SELAS-safe cote schema/front-data pour President signataire et filiation obligatoire, mais aucun pack SELAS n'est active.
- `SELAS-SPEC-DOC002-DOMICILIATION-001` realise ; il autorise une demande de `GO dev` borne sur `DOC-002`, mais seulement si la domiciliation est explicitement rattachee au siege/cabinet.
- `SELAS-DOC002-DOMICILIATION-001` code ; `DOC-002` est SELAS-safe cote schema/front-data pour President signataire et domiciliation rattachee au siege/cabinet, mais aucun pack SELAS n'est active.
- `SELAS-DOC005-DOC006-REGIME-COMMUNAUTAIRE-001` code ; `DOC-005` et
  `DOC-006` sont SELAS-safe cote schema/front-data comme batch conditionnel
  regime communautaire, mais aucun pack SELAS n'est active.
- `SELAS-SPEC-DECISION-PRESIDENT-001` realise ; il confirme que `DOC-004`
  n'est pas reutilisable directement et que la decision President reste
  reservee/conditionnelle apres arbitrage statuts V1.
- `SELAS-SPEC-STATUTS-MEDECIN-AU-001` realise ; il confirme `DOC-018` comme
  candidat V1 pour les statuts SELAS medecin actionnaire unique, avec nomination
  President absorbee par les statuts et blocage des cas complexes.
- `SELAS-SPEC-CAPITAL-ACTIONS-001` realise ; il confirme que le capital SELAS
  V1 reste limite aux actions ordinaires detenues a 100 % par l'actionnaire
  unique, avec droits proportionnels et numerotation simple derivee.
- `SELAS-SPEC-ORDRE-001` realise ; il confirme que `DOC-034` est reutilisable
  pour SELAS avec l'overlay SELARL/SELAS, sans confusion entre le President
  SELAS et le president du Conseil de l'Ordre, et avec les plans/devis traites
  comme pieces attendues non generees.
- `SELAS-SPEC-REGIME-COMMUNAUTAIRE-001` realise ; il confirme que `DOC-005`
  et `DOC-006` forment un batch conditionnel SELAS si regime communautaire,
  et la sortie de reserve de `DOC-006` a ete realisee dans le ticket dev borne.
- `SELAS-ROADMAP-TO-COMPLETION-001` realise ; il fixe l'ordre A-Z propose pour
  terminer la SELAS V1, sous validation Gad avant tout nouveau dev.
- `SELAS-DOC034-ORDRE-001` realise en QA partielle ; `DOC-034` est SELAS-safe
  cote schema/front-data et generateur pour le parcours V1 simple, mais
  `pytest`/`ruff` restent a relancer en environnement equipe.
- `SELAS-DOC005-DOC006-REGIME-COMMUNAUTAIRE-001` realise en QA partielle ;
  `DOC-005` et `DOC-006` sont SELAS-safe cote schema/front-data et smoke DOCX,
  mais `pytest`/`ruff` restent a relancer en environnement equipe.
- `SELAS-DOC018-STATUTS-MEDECIN-AU-001` realise en QA partielle ; `DOC-018`
  est SELAS-safe pour le parcours V1 simple, avec verrous capital/actions,
  blocage DG/actions complexes et non-selection de `DOC-004`, mais
  `pytest`/`ruff` restent a relancer en environnement equipe.
- `SELAS-FRONT-READINESS-PACK-001` realise en QA partielle ; le pack SELAS V1
  est aligne cote readiness front/data avec documents simples, conditionnels et
  reserves, mais la generation de pack reste inactive.
- `SELAS-ORCHESTRATOR-PACK-001` realise en QA partielle ; l'orchestrateur
  selectionne le pack SELAS V1 simple et le batch regime communautaire, tout en
  bloquant les cas hors V1.
- `SELAS-SMOKE-HAPPY-PATH-001` realise en QA partielle ; le pack simple sans
  regime communautaire genere les 5 DOCX attendus et n'active pas les documents
  conditionnels ou reserves.
- `SELAS-SMOKE-REGIME-COMMUNAUTAIRE-001` realise en QA partielle ; le pack avec
  regime communautaire genere les 7 DOCX attendus, ajoute `DOC-005` et
  `DOC-006`, et n'active pas les documents reserves ou complexes.
- `SELAS-ANTI-REGRESSION-WORDING-001` realise en QA partielle ; les deux packs
  passent le controle strict anti-SELARL/gerant/parts sociales, avec occurrences
  `associe` classees pour revue trois sources.
- `SELAS-TRIPLE-SOURCE-CHECK-001` realise en QA partielle ; source metier et
  NotebookLM confirment le perimetre V1, le retour Gad strategie est pris en
  compte, mais aucun retour humain pack complet n'est encore present.
- `SELAS-HUMAN-REVIEW-PACK-001` realise ; le pack de revue humaine est pret,
  avec ZIP, inventaire, checklist, questions de decision et pre-check
  NotebookLM, mais aucun retour humain n'est encore classe.
- La revue humaine devient possible sur les packs smoke generes, mais elle n'est
  pas encore realisee.

## Prochaine action concrete

1. Transmettre `artifacts/selas_human_review_pack_001/selas_human_review_pack_001_20260602_135708.zip` a Gad / associe / juriste.
2. Attendre le retour humain classe.
3. Si corrections : lancer `SELAS-HUMAN-FIXES-001`.
4. Si validation sans correction : lancer `SELAS-FINAL-SMOKE-ZIP-PDF-001`.
5. Relancer `pytest` et `ruff` dans un environnement avec dependances dev quand disponible.
6. Garder le pack SELAS debranche tant qu'aucun GO pack n'est donne.
7. Ne produire aucun pack DOCX/PDF/ZIP SELAS sans specs documentaires, tests et validation humaine.

## Statut final

`DOC-003` Procuration, `DOC-001` DNC President, `DOC-002` Domiciliation, `DOC-034` Demande d'inscription a l'Ordre, le batch conditionnel `DOC-005`/`DOC-006` Regime communautaire et `DOC-018` Statuts SELAS medecin actionnaire unique sont securises pour SELAS President unique ; la readiness front/data et l'orchestrateur savent selectionner les documents simples, conditionnels et reserves ; les smokes internes happy path et regime communautaire sont passes avec 5 puis 7 DOCX generes ; le controle anti-regression wording strict est passe ; le checkpoint trois sources confirme le perimetre V1 contre la source metier et NotebookLM ; le pack de revue humaine est pret dans `artifacts/selas_human_review_pack_001/20260602_135708/` et en ZIP, avec pre-check NotebookLM integre ; le bloc Capital / Actions V1 est borne aux actions ordinaires 100 % actionnaire unique ; la roadmap A-Z jusqu'a cloture SELAS V1 est validee pour avancer ; `SELAS-DECISION-PRESIDENT` reste reserve/conditionnel car la nomination President est absorbee par les statuts V1 ; pack SELAS non valide final tant que le retour humain n'est pas classe et que les corrections eventuelles ne sont pas faites.
