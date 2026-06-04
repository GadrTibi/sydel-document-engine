# Dernier état projet

## Date de mise à jour
2026-06-03

## Correction de cadrage projet 2026-06-02
PROJECT-CLARITY-AUDIT-001 : audit global demande par Gad apres confusion entre
catalogue/moteur historique et types d'entreprise reellement traites. Decision
verrouillee : seuls `SELARL` et `SELAS` sont en traitement metier. Les autres
types (`SPFPL cession`, `SPFPL apport`, `SCS`, `SCI`, `SCM`, `SAS`) existent
dans le catalogue, le moteur, les specs ou les tests, mais ne sont pas traites
comme sprints produit. Livrables : `docs/review/project_clarity_audit_001_report_v1.md`
et `docs/project/COMPANY_TYPE_STATUS_REGISTRY_V1.md`. La tour de controle et le
plan maitre pointent maintenant vers ce registre. Action de nettoyage terminee :
`PROJECT-COMPANY-TYPE-UI-STATUS-001` durcit l'Assistant metier pour que le front
et les rapports ne presentent jamais un type non sprinte comme generable produit
V1.

## Dernier ticket SELARL traite
SELARL-RETURNS-008-MAIN-AUDIT-FIX-001 : correction appliquee sur `main` apres audit Gad/associe du 2026-06-03. Vrai ecart nouveau confirme : le cas SELARL medecin marie sous separation de biens n'etait pas assez cadre cote front/contexte ; l'identite conjoint pouvait manquer et la generation des statuts pouvait echouer. Correction : le front actif affiche les champs civilite/prenom/nom conjoint des que le praticien est marie, la validation les exige pour les statuts, `Marie(e)` sans regime communautaire derive `separation de biens`, et le cas separation genere les statuts avec la phrase attendue sans produire `DOC-005`/`DOC-006`. Correctifs associes : libelles medecin accentues dans les documents, fonction mandataire `gerant` accentuee, nationalite francaise accentuee, capital visible formate `1 000`. Rapport : `docs/review/selarl_returns_008_main_audit_fix_report_v1.md`. Validations : `python -m ruff check .` OK, py_compile OK, generation reelle DOCX/ZIP 3 scenarios OK, audit retours associe par extraction DOCX OK avec 32 controles. Limite environnement : `pytest` avec `tmp_path` reste bloque par permissions Windows sur les repertoires temporaires, donc la preuve metier active est le script direct de generation/extraction DOCX. Prochaine action : deployer/tester `main` et demander a l'associe uniquement des ecarts concrets document par document.

SELARL-RETURNS-007-SIGNATURE-DNC-001 : nouveaux retours associe transmis par Gad le 2026-06-03. Critique : le retour signature est fonde ; la correction precedente supprimait les bordures imprimees mais gardait une table invisible, encore visible comme grille/carre Word. Correction appliquee : `add_simple_signature_block` rend maintenant des paragraphes alignes a droite, sans table. DNC ville naissance : retour non reproduit dans la version active ; le pack 005 regenere affiche `Ne le 12/04/1984 a Paris.` dans les quatre scenarios apres normalisation ASCII. Adresse conjoint : point positif confirme. Rapport : `docs/review/selarl_associe_returns_007_signature_dnc_report_v1.md`. Validations : tests Lot 1 signatures/DNC 23 passes, regression SELARL ciblee 187 passes, ruff cible OK, pack 005 regenere localement. Point de vigilance : les tables bordees restantes sont les titres encadres, pas les signatures ; si l'associe veut supprimer aussi les titres encadres, ouvrir un ticket de mise en forme global distinct.

SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001 : audit d'incident generalise demande par Gad apres nouveaux exemples associe. Verdict : l'ancien audit 006 etait trop confiant ; deux vrais manques ont ete confirmes dans la chaine recente. Le premier etait deja corrige (`adresse conjoint` encore visible dans des branches front/schema). Le second a ete trouve et corrige maintenant : `DOC-002` autorisation de domiciliation rendait encore `pour une duree indeterminee`; le generateur rend desormais `pour 99 ans`, le test DOC-002 est aligne, le pack 005 local est regenere et le manifest contient `doc002_duration_99_years=true` pour les 4 scenarios. Rapport : `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`. Validations : `pytest tests/unit/test_autorisation_domiciliation.py -q` OK, 8 passes ; smokes generation SELARL cibles OK, 10 passes ; regression SELARL ciblee OK, 187 passes ; `ruff check` cible OK. Point de vigilance : le texte `duree indeterminee` existe encore dans le PV nomination gerant pour la duree du mandat de gerant, ce n'est pas la domiciliation ni la duree sociale et ne doit pas etre modifie sans retour humain explicite. Prochaine action : faire tester cette version candidate par l'associe et demander uniquement des ecarts concrets document par document.

SELARL-RETURNS-006-CONJOINT-ADDRESS-FRONT-LOCK-001 : incident confirme par Gad/associe sur les retours humains 006. Le retour associe etait fonde sur ce point : la correction precedente avait verrouille le rendu `DOC-006`, mais pas toutes les branches front/schema. Corrections appliquees : suppression des cles `conjoint_adresse_*` du clean front et de son prefill, discard explicite des anciennes cles dans `build_clean_data_entry`, suppression de `conjoint_adresse` du formulaire simple historique, suppression de `adresse_conjoint` des exigences `DOC-006`, contrats front actifs alignes. Rapport : `docs/review/selarl_returns_006_conjoint_address_front_lock_001_report_v1.md`. Validations : tests anti-regression cibles OK, 6 passes ; `ruff check` cible OK. Limite : le paquet large cible affiche 107 tests passes puis 7 erreurs dues aux permissions Windows sur les dossiers temporaires `tmp_path`, pas des echecs d'assertion metier. Prochaine action : faire retester l'interface par l'associe sur la branche courante, puis relancer les smokes DOCX dans un environnement temporaire propre avant nouveau pack final.

SELARL-EXTERNAL-RECHECK-RETURNS-006-001 : reverification presque exterieure demandee par Gad sur les derniers retours humains 006. Methode : relire `selarl_human_returns_006_raw_v1.md`, extraire directement le texte et le XML des DOCX du pack 005, verifier les points non visibles via le front propre actif `front_app`, puis relancer les tests cibles. Verdict historique : controle depasse, car l'audit incident du 2026-06-03 a ensuite trouve puis corrige l'ecart `DOC-002` (`pour 99 ans`). Validations historiques : extraction DOCX/XML 4 scenarios, 0 failure ; `pytest tests/unit/test_clean_front_app.py tests/unit/test_lot_04_statuts_sel_exercice.py tests/unit/test_declaration_non_condamnation.py tests/unit/test_pv_nomination_gerant.py tests/unit/test_procuration.py tests/unit/test_regime_communautaire.py tests/unit/test_demande_inscription_ordre.py -q` OK, 84 tests passes. Reserve : les anciens ecrans legacy contiennent encore des variables historiques, mais ils sont explicitement hors nouveau front par `front_app/legacy_boundary.py` et le test anti-import legacy. Rapport historique : `docs/review/selarl_external_recheck_returns_006_pack_005_report_v1.md`. Rapport actif : `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`. Prochaine action officielle : `SELARL-FINAL-ASSOCIE-VALIDATION-001`.

FRONT-INFORMATION-DEDUP-AGENT-001 : agent dedie ajoute a la demande de Gad pour garantir qu'une information metier identique n'est demandee qu'une seule fois dans le front. Livrable : `docs/project/FRONT_INFORMATION_DEDUP_AGENT_PROTOCOL_V1.md`. Raccordements : `docs/project/PROJECT_AGENT_ORG_CHART_V1.md`, `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`, `AGENTS.md` et `docs/project/01_EXECUTION_BOARD.md`. Decision : tout ticket qui touche la saisie front ou les variables utilisateur doit activer cet agent avant `GO dev`.

SELARL-HUMAN-RETURNS-DEEP-AUDIT-006 : audit approfondi des retours humains 006 sur le pack 005. Verdict historique depasse : l'audit incident `SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001` a trouve puis corrige un ecart `DOC-002` (`pour une duree indeterminee` -> `pour 99 ans`). Sources verifiees : `docs/review/selarl_human_returns_006_raw_v1.md`, `docs/review/selarl_human_returns_triage_006_report_v1.md`, `artifacts/selarl_closing_pack_005/` et son manifest. Rapport historique : `docs/review/selarl_human_returns_deep_audit_006_report_v1.md`. Rapport actif incident : `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`. Prochaine action officielle : `SELARL-FINAL-ASSOCIE-VALIDATION-001`.

SELARL-CLOSING-PACK-005 : pack SELARL regenere apres retours humains 006 dans `artifacts/selarl_closing_pack_005/`. Manifest : `artifacts/selarl_closing_pack_005/manifest_selarl_closing_pack_005.json`. Scenarios : medecin simple 6 DOCX, dentiste simple 6 DOCX, medecin regime communautaire 8 DOCX, dentiste regime communautaire 8 DOCX, 0 echec manifest. Rapport : `docs/review/selarl_closing_pack_005_report_v1.md`. Deux ecarts detectes pendant l'audit du premier manifest 005 ont ete corriges avant cloture du ticket : `DOC-006` en quatre exemplaires et accord feminin `associee unique` dans les statuts dentiste. Amendement 2026-06-03 : `DOC-002` autorisation de domiciliation corrigee en `pour 99 ans`, pack 005 local regenere et manifest enrichi avec `doc002_duration_99_years=true`. Validations : tests statuts/regime 25 passes, regression SELARL large 166 passes, puis regression SELARL ciblee 187 passes apres amendement, ruff cible OK.

SELARL-RETURNS-006-ADDRESS-SIGNATURE-001 : correction transversale bornee selon retours humains 006. Corrections appliquees : les adresses front/moteur sont normalisees pour rendre le code postal avant la ville, y compris quand une adresse affichee arrive sous forme `Paris 75001`; les encadres de signature restants dans le perimetre pack SELARL sont supprimes sur `DOC-001`, `DOC-002` et `DOC-003`. Rapport : `docs/review/selarl_returns_006_address_signature_001_report_v1.md`. Validations : `pytest tests/unit/test_declaration_non_condamnation.py tests/unit/test_autorisation_domiciliation.py tests/unit/test_procuration.py tests/unit/test_front_generation_actions.py -q` OK, 37 tests passes ; regression SELARL large OK, 165 tests passes ; ruff cible OK. Prochaine action bornee : `SELARL-CLOSING-PACK-005`.

SELARL-RETURNS-006-FRONT-VARIABLES-001 : correction bornee des variables front/moteur SELARL selon retours humains 006. Corrections appliquees : duree sociale forcee a 99 ans, nombre d'exemplaires force a quatre, qualite renoncee forcee a associe, date courrier derivee du jour, nationalite portugaise ajoutee, option siege social identique adresse personnelle ajoutee. Rapport : `docs/review/selarl_returns_006_front_variables_001_report_v1.md`. Validations : tests front cibles OK, 100 tests passes ; regression SELARL large OK, 165 tests passes ; ruff cible OK. Prochaine action alors traitee : `SELARL-RETURNS-006-ADDRESS-SIGNATURE-001`.

SELARL-RETURNS-006-ORDRE-001 : correction bornee de la demande d'inscription a l'Ordre selon retours humains 006. Corrections appliquees sur `DOC-034` : le libelle `Conseil departemental de l'Ordre des {Profession} de {departement}` est compose depuis la profession et le departement d'inscription a l'Ordre ; le front SELARL ne demande plus le libelle complet visible comme source principale. Rapport : `docs/review/selarl_returns_006_ordre_001_report_v1.md`. Validations : tests ordre/front OK, 57 tests passes ; regression SELARL large OK, 165 tests passes ; ruff cible OK. Prochaine action alors traitee : `SELARL-RETURNS-006-FRONT-VARIABLES-001`.

SELARL-RETURNS-006-CONJOINT-LETTERS-001 : correction bornee du batch regime communautaire selon retours humains 006. Corrections appliquees sur `DOC-005`/`DOC-006` : forme juridique redigee dans la lettre d'avertissement, adresse conjoint derivee depuis l'adresse personnelle de l'associe/signataire, adresse conjoint retiree des exigences front/readiness et du formulaire simple visible, date sous la ville retiree de la lettre de renonciation. Rapport : `docs/review/selarl_returns_006_conjoint_letters_001_report_v1.md`. Validations : `pytest tests/unit/test_regime_communautaire.py -q` OK, 10 tests passes ; tests front/regime OK, 50 tests passes ; non-regression SELARL ciblee OK, 139 tests passes ; ruff cible OK. Prochaine action bornee : `SELARL-RETURNS-006-ORDRE-001`.

SELARL-RETURNS-006-PROCURATION-001 : correction bornee de la procuration selon retours humains 006. Corrections appliquees sur `DOC-003` : phrase introductive `demeurant au ..., agissant en qualite...` sur la meme phrase avec `agissant` en minuscule, `de la {designation societe}` sans duplication de forme sociale, siege rendu sans ajout de `au`, adresses personnelles et siege en ordre `CP Ville`. Rapport : `docs/review/selarl_returns_006_procuration_001_report_v1.md`. Validations : `pytest tests/unit/test_procuration.py -q` OK, 9 tests passes ; tests front cibles OK, 98 tests passes ; ruff cible OK. Prochaine action bornee : `SELARL-RETURNS-006-CONJOINT-LETTERS-001`.

SELARL-RETURNS-006-PV-001 : correction bornee du PV nomination gerant selon retours humains 006. Corrections appliquees sur `DOC-004` : header avec forme juridique redigee en dessous de la denomination sociale et au-dessus du capital, profession SEL derivee des associes pour rendre `Société d’exercice libéral à responsabilité limitée de médecin` en contexte SELARL medecin, remplacement de `Au capital minimum et effectif de ...` par `Au capital de ...`. Rapport : `docs/review/selarl_returns_006_pv_001_report_v1.md`. Validations : `pytest tests/unit/test_pv_nomination_gerant.py -q` OK, 10 tests passes ; tests front cibles OK, 99 tests passes ; ruff cible OK. Prochaine action bornee : `SELARL-RETURNS-006-PROCURATION-001`.

PROJECT-BLOCKER-QUESTION-PROTOCOL-001 : comportement projet ajoute a la demande de Gad 2026-06-02. Si un ticket bloque, Codex et les agents projet doivent verifier sources, specs, retours NotebookLM/modele, retours humains, code et tests avant de demander ; si le trou demeure, poser a Gad une question concrete avec sources deja verifiees, impact et action possible en attendant. Pointeurs mis a jour : `AGENTS.md`, `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `docs/project/PROJECT_CONTROL_TOWER_V1.md`, `docs/project/PROJECT_AGENT_ORG_CHART_V1.md`, `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`.

SELARL-RETURNS-006-DNC-001 : correction bornee de la declaration de non condamnation selon retours humains 006. Corrections appliquees sur `DOC-001` : ligne de naissance complete avec ville (`Ne/Nee le {date} a {ville}.`) et option moteur/front `au` via `ville_naissance_article_au` pour rendre `au {ville}`. Propagation dans `Person`, clean front SELARL, front historique, wizard metier et mode document unitaire DOC-001. Rapport : `docs/review/selarl_returns_006_dnc_001_report_v1.md`. Validations : `pytest tests/unit/test_declaration_non_condamnation.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_single_document_mode.py tests/unit/test_business_wizard.py -q` OK, 94 tests passes ; ruff cible OK. Ticket suivant alors traite : `SELARL-RETURNS-006-PV-001`.

SELARL-RETURNS-006-STATUTS-001 : correction bornee des statuts SELARL selon retours humains 006. Corrections appliquees sur `DOC-016` et `DOC-017` : clause matrimoniale communaute/separation de biens apres l'identite ordinale avec civilite/prenom/nom conjoint, accord du libelle `associe` a l'article 8, annexe placee a la page suivante, tiret devant `Ouverture d'un compte bancaire`. Rapport : `docs/review/selarl_returns_006_statuts_001_report_v1.md`. Validations : `pytest tests/unit/test_lot_04_statuts_sel_exercice.py -q` OK, 14 tests passes ; ruff cible OK. Prochaine action bornee : `SELARL-RETURNS-006-DNC-001`.

SELARL-HUMAN-RETURNS-006-TRIAGE-001 : nouveaux retours humains SELARL recus par message Gad 2026-06-02, enregistres en brut dans `docs/review/selarl_human_returns_006_raw_v1.md` et classes dans `docs/review/selarl_human_returns_triage_006_report_v1.md`. Decision : le pack 004 n'est plus a presenter comme final ; il devient le pack a corriger. Ouverture des tickets `SELARL-RETURNS-006-*` sur statuts, declaration de non condamnation, PV nomination gerant, procuration, lettres conjoint/renonciation, ordre, variables front, adresses et signatures. Prochaine action bornee : `SELARL-RETURNS-006-STATUTS-001`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie dans ce ticket de triage.

## Dernier ticket terminé
PROJECT-COMPANY-TYPE-UI-STATUS-001 : nettoyage produit/code borne apres audit de
clarte des types d'entreprise. Correction appliquee dans
`src/sydel_doc_engine/app/business_wizard.py` : `business_dossier_types()`
distingue maintenant `SELARL` comme seul type generable produit V1, `SELAS`
comme sprint actif `NO-GO dev`, et `SCI`, `SCM`, `SPFPL cession`,
`SPFPL apport`, `SCS`, `SAS` comme `INVENTAIRE_TECHNIQUE`. Les warnings du
wizard signalent aussi quand un type est seulement un inventaire technique ou
un sprint actif non generable. Test cible mis a jour :
`tests/unit/test_business_wizard.py`. Rapport :
`docs/review/company_type_ui_status_001_report_v1.md`. Validations :
`ruff check src/sydel_doc_engine/app/business_wizard.py tests/unit/test_business_wizard.py`
OK ; `pytest tests/unit/test_business_wizard.py -q` OK, 42 tests passes.
Agent Git/Branch utilise avant edition : Curie a confirme branche
`track-b/clean-rebuild`, remote GitHub, index clean, dirty state important et
risque de collision front ; les generateurs SELARL et rapports `selarl_*` ont
ete volontairement evites. Etat SELARL mis a jour ensuite : les corrections
006, le pack 005 et l'audit 006 sont termines ; prochaine action projet
recommandee : `SELARL-FINAL-ASSOCIE-VALIDATION-001`, ou attendre le Sync packet
Naomi pour requalifier SELAS.

NAOMIE-SYNC-CHECKPOINT-001 : ouvert apres retour Gad 2026-06-02. Gad indique que Naomi a avance SELAS jusqu'a tout terminer et attendre le retour humain, mais cette avancee n'est pas visible sur la branche publiee `codex/naomie-selas-sprint`, qui pointe sur `6a0382f` et contient les commits de protocoles/rapports, pas les livrables SELAS termines annonces. Diagnostic courant : `avancee annoncee, synchronisation manquante`. Decision : ne pas relancer NotebookLM ni conclure que SELAS est au debut ; demander au thread Naomi un Sync checkpoint selon `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md`. Preuve attendue : commit pousse sur `codex/naomie-selas-sprint` ou `Sync packet` complet. Tant que cette preuve manque, statut SELAS = non requalifie / `NO-GO dev` dans les traces publiees. Pointeurs mis a jour : `AGENTS.md`, `docs/project/PROJECT_CONTROL_TOWER_V1.md`, `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md`, `docs/project/PROJECT_AGENT_ORG_CHART_V1.md`, `docs/project/NAOMIE_GITHUB_ONBOARDING_V1.md`, `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md`, `docs/project/PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md`, `docs/sprints/SPRINT_SELAS_V1.md`, `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` et `docs/project/01_EXECUTION_BOARD.md`.

WORKSTREAM-TRACE-BOSS-REPORT-001 : correction du suivi Naomi apres retour Gad 2026-06-02. Diagnostic : le process cherchait trop une evaluation individuelle de Naomi et produisait un rapport trop audit/technique. Decision : Gad demande l'etat du `flux Naomi`, pas une evaluation individuelle. Si Codex, un sous-agent, GitHub, NotebookLM ou un outil avance dans le perimetre du sprint/branche Naomi, cela remonte comme avancement du flux Naomi. Naomi ne porte pas la charge de tracabilite : l'Agent de tracabilite de flux tient le worklog, les preuves, les curseurs et le rattrapage retroactif. Rapport boss par defaut : statut du flux, avancement depuis le dernier point, prochaine etape, blocage/risque, fiabilite. Livrable principal : `docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md`. Pointeurs mis a jour : `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/01_EXECUTION_BOARD.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`, `docs/project/PROJECT_CONTROL_TOWER_V1.md`, `docs/project/PROJECT_AGENT_ORG_CHART_V1.md`, `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `docs/sprints/SPRINT_SELAS_V1.md`, `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` et `docs/review/selas_naomie_backfill_001_report_v1.md`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

PROJECT-AGENT-ORG-CHART-001 : creation du registre pyramidal des agents du projet pour repondre a la demande Gad 2026-06-02. Diagnostic : les protocoles existaient par morceaux, mais il manquait une carte centrale indiquant quel agent interroger, dans quel ordre, et ou trouver la preuve. Livrable principal : `docs/project/PROJECT_AGENT_ORG_CHART_V1.md`. Rattrapage SELAS produit : `docs/review/selas_naomie_backfill_001_report_v1.md`. Decision : tout statut projet doit remonter au big orchestrateur (`PROJECT_CONTROL_TOWER_V1.md`), redescendre vers l'agent specialise, puis s'appuyer sur un journal, worklog, rapport, code, branche ou source precise. Pointeurs mis a jour : `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/01_EXECUTION_BOARD.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`, `docs/project/PROJECT_CONTROL_TOWER_V1.md`, `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `docs/sprints/SPRINT_SELAS_V1.md` et `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

NAOMIE-REPORT-FRESHNESS-AUDIT-001 : correction du faux rapport Gad indiquant que Naomi etait encore au demarrage NotebookLM. Diagnostic : le worklog Naomi et le journal NotebookLM etaient bien vides, mais le repo contient deja une matiere SELAS preexistante : sources SELAS, catalogue, `DOC-018`, generateur statuts SELAS, conditions UI, tests et exemples. Point de rupture : `PROJECT_STATE_IGNORED + WORKLOG_STALE`. Les rapports Gad ne doivent plus assimiler `aucune action Naomi tracee` a `projet/type au debut`. Livrables : `docs/review/naomie_reporting_freshness_audit_001_report_v1.md`, `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `docs/sprints/SPRINT_SELAS_V1.md`, `docs/project/PROJECT_CONTROL_TOWER_V1.md`, `AGENTS.md` et `docs/project/01_EXECUTION_BOARD.md`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

NAOMIE-BRANCH-READ-FALLBACK-001 : correction du diagnostic branche Naomi apres la capture Gad 2026-06-02. Constat : le rapport precedent ecrivait que la branche `codex/naomie-selas-sprint` etait inaccessible parce que `git fetch` local echouait sur `FETCH_HEAD Permission denied`. Diagnostic corrige : la branche distante existe et le connecteur GitHub la voit ; le probleme est local au worktree Git / identifiants Git, pas a l'existence de la branche. Decision : quand `git fetch`, `git ls-remote` ou `git show origin/[branche]` echoue pour raison locale, Codex doit tenter la lecture via connecteur GitHub avant de declarer une branche inaccessible. Livrables mis a jour : `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md`, `docs/project/PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md` et `docs/project/01_EXECUTION_BOARD.md`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

NAOMIE-REPORT-CURSOR-AND-MESSAGE-QUEUE-001 : ajout de deux fonctions au suivi Naomi. Decision : quand Gad demande un rapport Naomi, Codex doit lire le worklog et produire uniquement le delta depuis le dernier rapport Gad inscrit ; apres reponse, Codex note la date, la periode couverte, la synthese et le nouveau curseur dans le worklog. Decision complementaire : Gad peut laisser un message pour Naomi ; Codex l'inscrit dans `Messages Gad a transmettre a Naomi` avec statut `a transmettre`, le cite au prochain echange avec Naomi sous la forme `Message de Gad : "[message exact]"`, puis marque le message `transmis`. Livrables mis a jour : `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md`, `docs/project/PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md`, `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`, `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`, `docs/project/PROJECT_CONTROL_TOWER_V1.md` et `docs/project/01_EXECUTION_BOARD.md`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

NAOMIE-SUPERVISION-ORCHESTRATOR-001 : formalisation du suivi Naomi generique demande par Gad. Constat : le projet avait un runtime Naomi et un professeur Naomi, mais pas encore un orchestrateur de suivi capable de repondre a Gad `ou en est Naomi ?` depuis les traces sans demander a Naomi un statut oral. Decision : creer le role `Orchestrateur Naomi`, separe du professeur, applicable a tout projet/sprint et pas seulement SELAS. Quand Gad demande le statut de Naomi, Codex doit lire tour de controle, dernier etat, fichier de sprint, worklog Naomi, journal de base de connaissance, branche Naomi si accessible, puis repondre avec faits traces, blocages et prochaine action. Livrables : `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, mises a jour de `AGENTS.md`, `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md`, `docs/project/PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md`, `docs/project/PROJECT_CONTROL_TOWER_V1.md`, `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`, `docs/sprints/SPRINT_SELAS_V1.md`, `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` et `docs/project/01_EXECUTION_BOARD.md`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

GLOBAL-CHAT-IDENTITY-ROUTING-001 : correction du routage nouveau chat Gad / Naomi. Constat : les garde-fous etaient efficaces pour proteger Naomi une fois identifiee, mais trop agressifs quand Gad parlait de Naomi comme superviseur ; Codex pouvait declencher le Prompt NotebookLM alors que Gad posait une question de cadrage. Decision : un nouveau chat qui commence par `bonjour`, `salut`, `ca va` ou une reprise vague doit d'abord demander `Bonjour, tu es Gad ou Naomi ?`. Si l'interlocuteur est Gad, Codex applique le rail superviseur produit et ne declenche pas NotebookLM seulement parce que Gad parle de Naomi. Si l'interlocutrice est Naomi/Naomi, Codex applique `NAOMIE_RUNTIME_PROTOCOL_V1.md`, reste en SELAS NotebookLM / `NO-GO dev` et donne la prochaine action simple avec point pedagogie. Livrables mis a jour : `AGENTS.md`, `docs/project/PROJECT_CONTROL_TOWER_V1.md`, `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`, `docs/sprints/SPRINT_SELAS_V1.md`, `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md`, `docs/project/PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` et `docs/project/01_EXECUTION_BOARD.md`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

COMPANY-TYPE-SPRINT-PLAYBOOK-002 : completion du mode d'emploi reusable pour les prochains types d'entreprise, a partir de la cloture SELARL. Livrables mis a jour : `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`, `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`, `docs/project/PROJECT_CONTROL_TOWER_V1.md`, `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md`, `docs/project/PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md`, `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`, `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `docs/project/PROCESS_BUILD_PROTOCOL_V1.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` et `docs/project/01_EXECUTION_BOARD.md`. Decision : tout nouveau sprint doit trianguler document de reference, NotebookLM/modele et retours humains ; Codex ne doit poser des questions humaines que sur des trous reels ; l'associe doit recevoir le pack actif et annoter des ecarts concrets ; la cloture se fait en `DONE`, `PARTIAL` ou `BLOCKED`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

Reference SELARL active : `SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001` est la derniere preuve metier du pack actif `artifacts/selarl_closing_pack_005/` : incident adresse conjoint front/schema corrige, ecart `DOC-002` trouve puis corrige en `pour 99 ans`, manifest 0 echec apres regeneration locale, regression SELARL ciblee 187 tests OK ; rapport `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`. Le rapport `SELARL-HUMAN-RETURNS-DEEP-AUDIT-006` reste historique et doit etre lu avec cet amendement. Le pack 004 reste une reference historique remplacee.

## Ticket en cours
SELARL courant : `SELARL-FINAL-ASSOCIE-VALIDATION-001` est le prochain ticket autorise. Ne plus transmettre ni presenter `artifacts/selarl_closing_pack_004/` comme final ; le pack actif est `artifacts/selarl_closing_pack_005/`.

SELARL-FINAL-ASSOCIE-VALIDATION-001 : validation finale prete sur le pack 005. Le brief actif est `docs/review/selarl_final_validation_001_brief_v1.md`. Attendre le verdict de l'associe : `VALIDE`, corrections concretes, ou blocage documente. Sans ce retour humain, ne pas declarer la SELARL simple/regime a 100 %.

GLOBAL-NAOMIE-COLLABORATION-001 / SELARL-CLOSING-PLAN-001 : formalisation du workflow Gad / Naomi / Codex reutilisable sur tous les projets et ecriture de la fin de sprint SELARL. Livrables : `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md`, `docs/project/PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md` et `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`. Decision : Naomi ne doit jamais arriver dans un projet sans cadrage projet/remote/branche/phase/prochaine action, et chaque projet doit avoir un protocole local inspire du template. Pour la SELARL, statut courant alors = `PARTIAL - production simple avancee` ; prochaine action prevue a ce moment = `SELARL-CLOSING-PACK-001`, maintenant terminee, puis revue associe / juriste, triage, corrections, smoke final et cloture canonique. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

NAOMIE-RUNTIME-FAILSAFE-001 : auto-critique et correction de l'incident persistant d'accueil Naomi. Constat : le repo contenait deja des garde-fous, mais ils etaient trop disperses et coexistaient avec des formulations anciennes ; un nouveau chat pouvait encore repondre vaguement ou retomber sur l'ancien libelle `SELAS-NOTEBOOKLM-RECONCILIATION-001`. Correction : creation de `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`, ajout d'une regle prioritaire en tete de `AGENTS.md`, alignement de `SPRINT_SELAS_V1.md` sur la phase 3 NotebookLM, et declaration explicite que le ticket actif est `SELAS-SOURCES-NOTEBOOKLM-001`. Reponse attendue desormais apres un simple `bonjour` de Naomi : statut sprint, action NotebookLM, point pedagogie, prochaine etape, puis Prompt NotebookLM 01 complet. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

MAIN-NAOMIE-TRIGGER-001 : correction du probleme constate sur la capture 2026-06-01, ou un nouveau chat ouvert sur `main` repond genericement a `bonjour` puis `je suis naomi`. Cause : les garde-fous Naomi/SELAS et la tour de controle etaient publies sur `track-b/clean-rebuild` et `codex/naomie-selas-sprint`, mais pas visibles depuis un chat demarre sur `main`. Correction : ajout d'un fail-safe explicite dans `AGENTS.md` et `docs/project/PROJECT_CONTROL_TOWER_V1.md` : si Naomi/SELAS arrive sur `main`, Codex doit tenter de basculer sur `codex/naomie-selas-sprint`, ou bloquer en `NO-GO dev` en expliquant que Codex gere la branche ; il ne doit jamais demander une tache ou un ticket. Le kit de gouvernance doit etre pousse aussi sur `main`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

PROJECT-CONTROL-TOWER-001 : installation d'une vraie tour de controle chef de projet pour SYDEL. Livrable principal : `docs/project/PROJECT_CONTROL_TOWER_V1.md`. Decision : Codex doit toujours commencer par identifier qui parle, le type d'entreprise, le sprint actif, la branche, la phase courante, l'action autorisee et les actions interdites. La tour de controle fixe le cycle standard unique pour chaque type d'entreprise : etat initial, ouverture sprint, sources, sous-sprint NotebookLM, audit reutilisation, matrice documentaire, contrat metier-front, tickets, validation Gad, dev limite, smoke, revue associe, corrections, cloture. Etat courant inscrit : SELARL = production partielle / prochaine revue humaine ou sous-cas borne ; SELAS = sprint actif Naomi / sous-sprint NotebookLM / `NO-GO dev` / Prompt 01 a donner. Pointeurs mis a jour : `AGENTS.md`, `00_MASTER_PLAN.md`, `02_CODEX_WORKFLOW.md`, `03_HANDOFF_FOR_NEW_AGENT.md`, `PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`, `COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`, `SPRINT_SELAS_V1.md`, `01_EXECUTION_BOARD.md` et ce fichier. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

SELAS-NOTEBOOKLM-START-TRIGGER-001 : correction du cas ou Naomi dit qu'elle veut lancer/demarrer/reprendre le sprint SELAS/CELAS et que Codex part trop loin. Decision verrouillee : pour Naomi, `lancer le sprint` signifie uniquement lancer le sous-sprint NotebookLM. Codex doit donner le prompt NotebookLM courant a copier-coller, attendre la reponse brute de Naomi, la structurer dans `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, puis choisir le prompt suivant selon les trous. Interdits avant couverture NotebookLM suffisante : production, generation, code, matrice finale, audit de reutilisation et push de fonctionnalite. Livrables mis a jour : `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/01_EXECUTION_BOARD.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`, `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`, `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` et `docs/sprints/SPRINT_SELAS_V1.md`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

SELAS-NOTEBOOKLM-PROMPT-LOOP-001 : formalisation de la boucle NotebookLM SELAS pour Naomi. Correction de workflow : Codex ne doit pas seulement constater "il manque une source NotebookLM SELAS" ; il doit donner a Naomi un prompt court a copier dans NotebookLM, recevoir la reponse, la structurer dans `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, puis iterer avec le prompt suivant jusqu'a couverture suffisante. Livrables : `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md`, `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, mise a jour de `docs/sprints/SPRINT_SELAS_V1.md`, `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`, `docs/project/02_CODEX_WORKFLOW.md`, `AGENTS.md` et `docs/project/01_EXECUTION_BOARD.md`. Decision : le prochain message utile a Naomi doit contenir le Prompt NotebookLM 01, pas une demande vague de source. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

NAOMIE-HELLO-TRIGGER-001 : correction de l'incident d'accueil Naomi. Constat : la branche distante `codex/naomie-selas-sprint` existe bien et contient `docs/sprints/SPRINT_SELAS_V1.md`, donc le probleme n'etait pas un manque de push de branche ; le probleme etait un declencheur trop peu explicite dans le chemin de lecture immediat du nouvel agent. Correction : ajout d'un trigger haut niveau dans `AGENTS.md`, durcissement de `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`, de `docs/sprints/SPRINT_SELAS_V1.md` et de `docs/project/02_CODEX_WORKFLOW.md`. Regle nouvelle corrigee par `GLOBAL-CHAT-IDENTITY-ROUTING-001` : si Naomi/Naomi est l'interlocutrice active et que le message est seulement `Bonjour`, Codex doit verifier la branche `codex/naomie-selas-sprint`, repondre en phase 0 `ACCUEIL / NO-GO dev`, inclure un point pedagogie et preparer NotebookLM ; si l'identite est inconnue, demander d'abord Gad ou Naomi. La reponse generique "tu veux qu'on attaque quoi dans le moteur documentaire ?" est explicitement interdite. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

SPRINT-ORCHESTRATOR-PROTOCOL-001 / SPRINT-SELAS-V1-001 : installation du garde-fou manquant pour les sprints par type d'entreprise et ouverture du sprint SELAS pour Naomi. Livrables principaux : `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` et `docs/sprints/SPRINT_SELAS_V1.md`. Decision : sprint SELAS en phase 0 `ACCUEIL / INITIALISATION`, statut `NO-GO dev`. Le lancement d'un sprint ne vaut jamais autorisation de developper ; Codex doit lire le fichier de sprint, appliquer le playbook, poser NotebookLM, lancer l'audit reutilisation SELARL/global, produire la matrice documentaire, puis attendre un `GO dev` explicite de Gad sur un ticket borne. Pour Naomi, chaque reponse doit contenir un point pedagogie et rappeler que Codex gere Git, les branches, les commandes, les tests, les commits et les push. Branche cible : `codex/naomie-selas-sprint`, creee/poussee depuis le checkpoint documentaire Track B. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie dans ce ticket de gouvernance.

NAOMIE-LEARNING-MENTOR-001 : ajout de la surcouche pedagogique pour Naomi. Livrable principal : `docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md`. Decision : `GO pedagogie`, `NO-GO dev`. Le role `Professeur Naomi` explique le projet, Git, les branches, les sprints, le moteur documentaire, les matrices et les controles qualite ; il ne pilote pas le scope, ne lance pas de commandes, ne modifie aucun fichier, ne decide pas de `GO dev` et ne remplace pas Codex pilote. Le protocole rappelle que Naomi est stagiaire : elle doit pouvoir poser des questions et apprendre, sans porter le risque Git/technique. Pointeurs mis a jour : `docs/project/NAOMIE_GITHUB_ONBOARDING_V1.md`, `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`, `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/01_EXECUTION_BOARD.md` et ce fichier. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

NAOMIE-GITHUB-ONBOARDING-001 / REUSE-AUDIT-AGENT-PROTOCOL-001 : formalisation du mode d'emploi pour installer le projet GitHub sur le poste de Naomi, travailler sur une branche dediee et demarrer un sprint propre. Livrables principaux : `docs/project/NAOMIE_GITHUB_ONBOARDING_V1.md` et `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`. Regles fixees : `1 sprint = 1 branche = 1 type d'entreprise`, Naomi ne travaille pas sur `main` ni directement sur `track-b/clean-rebuild`, la branche cible sera `codex/naomie-[type-entreprise]-sprint`, et un audit de reutilisation SELARL/global est obligatoire avant le premier `GO dev` d'un nouveau type d'entreprise. Correction produit : Naomi ne gere pas GitHub, Git, les branches, les commandes, les tests, les commits ou les push ; Codex gere ces operations dans le terminal du projet, avec arbitrage de Gad pour les checkpoints et push. Un sous-agent Reuse Auditor a ete lance en lecture seule et sa synthese a ete integree au protocole : reutiliser `front_data`, registres globaux de variables, orchestrateur, tests et contrats comme socle ; ne jamais copier le wording ou les locks SELARL sans verification source/spec/retour humain. La creation effective de branche reste `BLOCKED` tant que le type d'entreprise n'est pas choisi et que le checkpoint documentaire courant n'est pas commite/pousse. Pointeurs mis a jour : `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/01_EXECUTION_BOARD.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`, `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `docs/project/GLOBAL_CODEX_PRODUCT_GUARDRAIL_V1.md`, `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` et ce fichier. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

COMPANY-TYPE-SPRINT-PLAYBOOK-001 : formalisation du mode d'emploi de sprint par type d'entreprise demande par l'utilisateur. Livrable principal : `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`. Regles fixees : `1 sprint = 1 type d'entreprise`, sprint ecrit et suivi avant dev, demarrage en `NO-GO dev`, lecture des references, interrogation large de NotebookLM ou import de ses reponses, identification obligatoire de Naomi si elle pilote, guidage etape par etape, test de l'associe en fin de sprint, boucle de corrections jusqu'a validation ou report explicite. La SELARL devient le modele de methode via `docs/project/SELARL_CANONICAL_STATUS_V1.md`, mais reste a valider humainement avant cloture juridique 100 %. Pointeurs mis a jour : `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/01_EXECUTION_BOARD.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`, `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `docs/project/SELARL_CANONICAL_STATUS_V1.md` et ce fichier. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

SELARL-CANONICAL-STATUS-001 : consolidation de l'etat SELARL canonique apres le grand tour projet demande par l'utilisateur. Livrable principal : `docs/project/SELARL_CANONICAL_STATUS_V1.md`, qui devient le point de reprise unique pour la SELARL. Decision actuelle : `NO-GO dev` pour toute extension complexe tant qu'un sous-cas unique n'est pas choisi et cadre sous gate produit ; `GO documentation / reprise projet` pour clarifier l'etat, preparer la revue humaine et capitaliser la methode pour les autres formes sociales. Pointeurs mis a jour : `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/01_EXECUTION_BOARD.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` et ce fichier. Prochaine etape courante apres pack : `SELARL-ASSOCIE-REVIEW-001` sur le pack simple medecin/dentiste et regime communautaire avant nouveau dev complexe. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

PM-PRODUCT-GUARDRAIL-001 : installation du gate produit / métier obligatoire demandé par l'utilisateur. Codex devient le pilote projet / produit principal du dépôt avant développement : reformulation métier, vérification sources/specs, décision `GO dev` ou `NO-GO dev`, possibilité d'utiliser des sous-agents spécialisés, et maintien d'une mémoire de reprise autonome pour les nouveaux chats. Livrables principaux : doctrine globale `docs/project/GLOBAL_CODEX_PRODUCT_GUARDRAIL_V1.md` et protocole local `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`. La doctrine globale est destinée à tous les projets pilotés avec Codex ; le protocole local en est l'application SYDEL. Références mises à jour : `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` et `docs/project/01_EXECUTION_BOARD.md`. Correction complémentaire : les passages obsolètes du master plan et du handoff indiquant que le Lot 1 n'était pas démarré ont été remplacés par l'état Track B courant et par un renvoi vers ce fichier. Aucun code Python, générateur, moteur DOCX/PDF/ZIP, source de vérité ou wording juridique n'a été modifié. Validation limitée à la relecture documentaire, au contrôle du diff et à la revue PM en lecture seule.

TRACK-B-PREVIEW-VALIDATION-AND-CHECKPOINT-009 : validation de la preview clean front Track B et preparation du checkpoint Git local. Le lancement Streamlit a ete fait sans `Start-Process`, via `.\.venv\Scripts\python.exe -m streamlit run src\sydel_doc_engine\front_app\app.py --server.port 8534 --server.headless true --browser.gatherUsageStats false`. Resultat : HTTP 200 confirme sur `http://127.0.0.1:8534`, logs sous `artifacts/track_b_preview_validation_checkpoint_009/`, process termine proprement et port 8534 libre apres arret. Le mode `SELARL dentiste multi-associes simple (PARTIAL statuts)` est present dans le clean front. Validations : `ruff check .` OK ; tests cibles clean front/statuts/PV OK, 46 passes ; smoke dedie dentiste multi-associes PARTIAL OK, 1 pass. Git : les changements Track B accumules depuis le dernier push sont classes pour checkpoint local, sans push ni merge. Aucun nouveau developpement fonctionnel n'a ete ajoute.

TRACK-B-SELARL-DENTIST-MULTI-ASSOCIES-STATUTS-PARTIAL-008 : implementation du sous-cas SELARL chirurgien-dentiste multi-associes simple en mode PARTIAL. Le clean front Track B expose le mode `SELARL dentiste multi-associes simple (PARTIAL statuts)` uniquement pour la profession chirurgien-dentiste, selectionne `DOC-004` et `DOC-016`, reutilise les donnees multi-associes simples du ticket 007, derive les apports par associe depuis les parts et la valeur nominale, choisit le president de seance parmi les associes existants, garde un gerant unique et bloque les parts incoherentes. `DOC-004` reste LOCKED sur ce sous-cas ; `DOC-016` devient PARTIAL avec apports/capital/repartition/signatures associes rendus, mais comparution plurielle et signature plurielle stricte restent OPEN GAP faute de source humaine ligne par ligne. Livrable : `docs/review/track_b_selarl_dentist_multi_associes_statuts_partial_008_report_v1.md`. Artifacts : `artifacts/track_b_selarl_dentist_multi_associes_statuts_partial_008/pv_nomination_gerant.docx`, `statuts_selarl_chirurgien_dentiste.docx` et `dossier_generation.zip`. Validations : tests cibles OK, 46 passes ; `ruff check .` OK ; smoke DOCX/ZIP OK ; controle placeholders/parasites OK ; preview HTTP non validee car le lancement Streamlit via `Start-Process` est reste bloque dans le shell local, ports 8532/8533 verifies libres apres interruption. Aucun push, aucun merge, aucun ticket suivant n'est suggere ici.

TRACK-B-SELARL-MULTI-ASSOCIES-DOC004-LIMITED-007 : implementation du sous-cas SELARL multi-associes simple limite a `DOC-004` uniquement. Le clean front Track B expose le mode `SELARL multi-associes simple (limite DOC-004)`, collecte les associes necessaires au PV, impose le president de seance parmi les associes existants, garde un gerant unique rattache au praticien/associe 1, selectionne uniquement `DOC-004` et affiche clairement les exclusions : statuts multi-associes, plusieurs gerants, cession, SCM, regime communautaire et votes non unanimes. Le contexte moteur construit `associes[]`, derive `reunion.president` depuis l'associe selectionne et bloque les repartitions de parts incoherentes. Livrable : `docs/review/track_b_selarl_multi_associes_doc004_limited_007_report_v1.md`. Artifacts : `artifacts/track_b_selarl_multi_associes_doc004_limited_007/pv_nomination_gerant.docx` et `dossier_generation.zip`. Validations : tests cibles OK, 30 passes ; `ruff check .` OK ; smoke DOCX/ZIP `DOC-004` OK ; clean front HTTP 200 sur `http://localhost:8531`, PID `23780` arrete proprement. Aucun push, aucun merge, aucun ticket suivant n'est suggere ici.

TRACK-B-SELARL-MULTI-ASSOCIES-SOURCE-CONTRACT-006 : contrat source produit pour la famille SELARL multi-associes / president de seance / plusieurs gerants, sans code, sans front et sans modification de wording juridique. Livrable : `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md`. Sources relues : backlog/factory SELARL, human reference lock, reports 003/004/005, retours humains, specs PV/statuts/cession/SCM, modeles domaine/front en verification. Decision : GO limite uniquement pour un futur sous-cas multi-associes simple sur `DOC-004` avec president choisi parmi les associes existants, un gerant unique et unanimite totale ; NO-GO pour statuts multi-associes, plusieurs gerants, president externe, cession medicale/dentaire et cession SCM dans ce contrat. Validations : revue documentaire et diff local, aucun test code ni preview lance car le ticket est documentaire et n'implemente rien. Aucun ticket suivant n'est suggere ici.

TRACK-B-SELARL-MEDECIN-REGIME-COMMUNAUTAIRE-005 : entree historique remplacee par `SELARL-DOC006-REGIME-FIX-001`. Le ticket 005 avait conserve `DOC-006` en reserve ; la correction du 2026-06-01 leve cette reserve et genere desormais `DOC-006` avec `DOC-005` quand `regime_communautaire=True`.

TRACK-B-SELARL-PRODUCTION-PACK-001 : premier pack de production SELARL Track B. Corrections moteur appliquees sur `DOC-001`, `DOC-002`, `DOC-004`, `DOC-005` et `DOC-016` selon les retours humains explicites : adresse personnelle `num voie, CP ville`, domiciliation dans les locaux du cabinet au siege, renonciation sans parasite RCS et avec `Fait pour servir et valoir ce que de droit.`, PV sans `RCS de ...`, sans `EXTRAORDINAIRE`, sans heure de reunion, avec president de seance rattache a l'associe unique et libelle singulier/pluriel de nomination, statuts chirurgien-dentiste avec `euros`, communaute et prestataire de signature electronique coherent. Livrables documentation : `docs/project/SELARL_PRODUCTION_FACTORY_V1.md` et `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md`. Validations : tests cibles OK, 55 passes ; `ruff check .` OK ; smoke DOCX/ZIP SELARL dentiste + regime communautaire OK dans `artifacts/track_b_selarl_production_pack_001/selarl-dentiste-regime` ; clean front lance sur `http://localhost:8513`, HTTP 200 confirme, PID `19756` arrete proprement. Prochaine etape recommandee : relecture humaine des DOCX SELARL produits par ce pack avant extension aux variantes restantes.

TRACK-B-SELARL-TEST-DATA-PREFILL-001 : ajout d'un bouton `Generer des donnees de test` immediatement sous `Type de dossier` dans le clean front SELARL V1. Le bouton pre-remplit un dossier SELARL aleatoire mais coherent pour accelerer les tests : profession medecin ou chirurgien-dentiste, dossier unipersonnel, hors scope V1 desactive, dates `JJ/MM/AAAA`, capital et parts coherents, ordre, banque, siege, praticien et conjoint si necessaire. Le test AppTest verifie que le pre-remplissage rend la generation possible et expose un bouton de telechargement ZIP. Validations : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py -q` OK, 14 tests passes ; clean front lance sur `http://localhost:8512`, HTTP 200 confirme, PID `35648` arrete proprement ; browser-use a refuse localhost et n'a pas ete contourne. Aucun generateur, moteur documentaire, wording juridique source, Track A, repo anchor ou merge n'a ete modifie.

TRACK-B-SELARL-DOWNLOAD-UX-001 : correction du retour testeur indiquant que le dossier genere ne se telechargeait pas localement. Le clean front conserve maintenant le dernier dossier genere en session Streamlit et affiche des boutons de telechargement natifs pour le ZIP et chaque DOCX. Les chemins serveur restent affiches en information, mais ne sont plus le seul moyen de recuperer les fichiers. Validations : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py -q` OK, 13 tests passes ; clean front lance sur `http://localhost:8511`, HTTP 200 confirme, PID `16648` arrete proprement ; browser-use a refuse localhost et n'a pas ete contourne. Aucun generateur, moteur documentaire, wording juridique source, Track A, repo anchor, push ou merge n'a ete modifie.

TRACK-B-SELARL-UX-FOLLOWUP-001 : corrections apres test local du clean front SELARL V1. Dates visibles passees en champs texte `JJ/MM/AAAA` sans borne Streamlit, bouton `Aujourd'hui` conserve, `Situation matrimoniale` en liste courte, doublon visible `Regime matrimonial` retire au profit de la case `Documents regime de la communaute`, valeur nominale calculee par capital / parts, champs ordre clarifies. Validations : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py -q` OK, 12 tests passes ; clean front lance sur `http://localhost:8510`, HTTP 200 confirme, PID `3480` arrete proprement. Aucun generateur, moteur documentaire, wording juridique source, Track A, repo anchor, push ou merge n'a ete modifie.

TRACK-B-SELARL-UX-DEDUP-RECONCILIATION-001 : reconciliation UX du clean front SELARL V1 apres retours associe / NotebookLM. Livrables : `src/sydel_doc_engine/front_app/field_derivations.py`, corrections ciblees dans `data_entry.py`, `shell.py`, `selarl_slice.py`, tests `tests/unit/test_clean_front_app.py` et pilotage mis a jour. Corrections appliquees : suppression des champs visibles de genre grammatical et titre d'affichage, derivation des accords depuis la civilite, suppression des champs en lettres derivables, capital/parts/valeur nominale en saisie numerique, boutons `Aujourd'hui` sur les dates visibles, lieu d'exercice masque par defaut derriere `Autre lieu d'exercice ?`, conjoint masque hors cas utile, date courrier avertissement visible seulement si regime communautaire, mandataire SYDEL pre-rempli hors parcours principal, seuils de gerance et prestataire Yousign fixes par defaut, repartition associe unique conservee a 100 %, nationalite remplacee par presets courts + `Autre`. Aucun generateur, moteur documentaire, wording juridique source, Track A, repo anchor, push ou merge n'a ete modifie. Validations : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py -q` OK, 11 tests passes ; clean front lance via `.\.venv\Scripts\python.exe -m streamlit run src/sydel_doc_engine/front_app/app.py --server.port 8508 --server.headless true --browser.gatherUsageStats false`, HTTP 200 confirme sur `http://localhost:8508`, PID `18436` arrete proprement. Aucun ticket suivant n'est suggere.

TRACK-B-SELARL-FIELD-DEDUP-AUDIT-001 : audit des champs utilisateur du parcours clean front SELARL V1. Livrable : `docs/review/track_b_selarl_field_dedup_audit_001_report_v1.md`. Resultat : PASS, aucune vraie duplication editable detectee sur les 72 champs de donnees recenses, hors bouton de generation. Les derivations Praticien -> associe/gerant/signataire, siege -> domiciliation, capital -> apport/depot et profession -> DOC-016/DOC-017 restent internes, sans double saisie. Points ambigus documentes : lieu d'exercice pouvant coincider avec le siege, bloc conjoint toujours visible, date courrier avertissement visible hors regime, seuils medecin exiges aussi en dentiste, mandataire `DOC-003` encore gere par constantes moteur. Aucun code Python, moteur, wording juridique, push ou merge n'a ete fait. Aucun ticket suivant n'est suggere.

TRACK-B-SELARL-VERTICAL-SLICE-IMPLEMENT-001 : implementation de la vertical slice SELARL V1 bornee dans le nouveau front propre Track B. Livrables : `src/sydel_doc_engine/front_app/selarl_slice.py`, realignement de `data_entry.py`, `dossier_selection.py`, `generation.py`, `shell.py`, tests `tests/unit/test_clean_front_app.py` et pilotage mis a jour. Perimetre implemente : creation SELARL medecin/chirurgien-dentiste, associe unique, generation DOCX/ZIP de `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-017` ou `DOC-016`, et `DOC-005` seulement si regime communautaire actif. Hors scope volontairement bloque ou signale : cession, SCM, derogations, site distinct, `DOC-006`, SELAS, micro-holding et statuts multi-associes. Aucun push, aucun merge, aucune modification du moteur documentaire ni du wording juridique source.

TRACK-B-SELARL-SOURCE-OF-TRUTH-CONTRACT-001 : gel du contrat metier-front SELARL V1 depuis les sources de verite Track B. Livrable : `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md`. Sources consolidees : reponse metier Albane, sources V2/V3, NotebookLM utilise uniquement en resolution/vocabulaire/flow, specs SELARL, lots ordre/PV/statuts, revues front/schema/flow et verification de coherence `front_data`/catalogue. Conclusion : GO pour une vertical slice SELARL V1 bornee a creation medecin/chirurgien-dentiste unipersonnelle avec `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016` ou `DOC-017`, et `DOC-005` conditionnel. Hors generation automatique V1 : cession, SCM, derogations, site distinct, `DOC-006` et statuts multi-associes. Aucun code, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

TRACK-B-FRONT-ARCHITECTURE-RESET-001 : refondation du chemin front Track B propre apres arbitrage produit. Livrables : nouveau package `src/sydel_doc_engine/front_app/` avec entrypoint `app.py`, shell minimal, routing, selection dossier, zone de saisie, zone generation placeholder, frontiere legacy, tests `tests/unit/test_clean_front_app.py`, rapport `docs/review/track_b_front_architecture_reset_001_report_v1.md`, commande de lancement documentee et mise a jour du pilotage. Constats : le moteur documentaire et `front_data/` restent conserves ; l'ancien `src/sydel_doc_engine/app/streamlit_app.py` reste reference historique mais n'est pas importe par le nouveau point d'entree ; Assistant metier prototype, Document unitaire, Technique / diagnostic, Debug interne et ecrans historiques ne sont pas exposes dans `front_app`. Limite volontaire : aucune vraie implementation metier SELARL n'est ajoutee ; la zone Generation affiche un slot non generable jusqu'au branchement d'une vertical slice propre. Aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

SELARL-COMPLETE-CONTEXT-ADAPTER-001 : entree historique remplacee sur le point `DOC-006` par `SELARL-DOC006-REGIME-FIX-001`. Le nouveau front genere les documents simples medecin/dentiste, et le regime communautaire ajoute desormais `DOC-005` et `DOC-006`. `DOC-013`, `DOC-014` et la derogation SEL BNC sans code restent manuels/exclus. Cession medicale/dentaire et cession SCM restent `context_incomplete` jusqu'a gate produit dedie.

SELARL-COMPLETE-CASE-PLAYBOOK-001 : entree historique ; la reserve `DOC-006` mentionnee alors est levee par `SELARL-DOC006-REGIME-FIX-001`. Le statut courant SELARL est dans `docs/project/SELARL_CANONICAL_STATUS_V1.md`.

FRONT-MINIMAL-SURFACE-CLEANUP-001 : application de la surface utilisateur minimale avant test. Livrables : coupe UI dans `src/sydel_doc_engine/app/streamlit_app.py`, tests AppTest adaptes, rapport `docs/review/front_minimal_surface_cleanup_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Constats : la vue normale affiche uniquement `Type de dossier`, `Donnees a saisir` et `Generation`, avec 0 radio, 0 table, 0 expander et aucun outil interne visible. Les outils internes restent accessibles seulement via mode equipe cache (`SYDEL_ENABLE_INTERNAL_TOOLS=1` ou flag de session interne). Le PDF est cache quand le backend local est indisponible ; les blocages data-layer/runtime sont affiches dans `Generation`. Aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie. Validations : tests cibles OK, 79 tests passes ; ruff OK ; pytest OK, 382 tests passes. Prochaine etape recommandee : test utilisateur local du pilote `SELARL creation simple`.

FRONT-REALITY-CHECK-001 : audit de realite du nouveau front global contre les debriefs recents. Livrables : `docs/review/front_reality_check_001_report_v1.md`, `docs/project/FRONT_MINIMAL_USER_SURFACE_V1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Constats : la vue normale est bien reduite techniquement a `Type de dossier`, `Donnees a saisir` et `Generation`, sans radio ni tableau par defaut, mais elle reste chargee par 3 expanders ouverts, 22 champs texte, la checkbox sidebar `Outils internes`, un bouton PDF visible meme lorsque le backend est indisponible et des blocages runtime non expliques. Generation reelle : DOCX et ZIP branches depuis le nouveau front pour `DOC-001` a `DOC-004`; PDF branche en code mais indisponible localement (`is_pdf_export_available() == False`). Aucun Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie. Prochaine etape recommandee : `FRONT-MINIMAL-SURFACE-CLEANUP-001`.

FRONT-STATE-AUDIT-001 : audit de reprise apres retour utilisateur sur le nouveau front. Livrables : `docs/review/front_state_audit_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Constats : le moteur reste disponible sur 43 documents moteurs (`DOC-001` a `DOC-043`) et le catalogue metier contient 46 documents attendus, mais la surface normale du nouveau front est volontairement limitee au pilote `SELARL creation simple` et a la generation `DOC-001` a `DOC-004`. Cause UX principale : la readiness data-layer peut declarer les quatre documents generables pendant que l'adaptateur moteur bloque ensuite sur un format de date, une adresse ou une ville RCS, sans exposer le detail dans la vue normale. Tests cibles OK : `test_front_generation_actions.py` 6 passes, `test_front_dossier_data_entry.py` 10 passes. Aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie. Prochaine etape recommandee : `FRONT-GENERATION-READINESS-UX-001`, puis `FRONT-DOCUMENTS-PANEL-001`.

FRONT-UX-HARD-CUT-001 : retrait complet du bruit non-user de la vue principale normale du nouveau front. Livrables : durcissement de `src/sydel_doc_engine/app/streamlit_app.py`, tests adaptes `tests/unit/test_front_ui_shell.py`, `tests/unit/test_front_dossier_editor.py`, `tests/unit/test_front_dossier_data_entry.py`, `tests/unit/test_front_generation_actions.py`, `tests/unit/test_business_wizard.py`, `tests/unit/test_single_document_mode.py`, rapport `docs/review/front_ux_hard_cut_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Decisions : la vue normale ne rend plus aucun radio de navigation, aucun tableau et aucun diagnostic ; elle affiche uniquement `Type de dossier`, `Donnees a saisir` et `Generation`. Les outils `Assistant metier prototype`, `Document unitaire`, `Technique / diagnostic` et `Debug interne` sont deplaces derriere la checkbox sidebar `Outils internes`. Ruff OK et pytest OK, 380 tests passes. Aucun generateur, moteur DOCX/PDF/ZIP, fondation `front_data` ou wording juridique n'a ete modifie. Prochaine etape recommandee : vrai test local utilisateur sur `SELARL creation simple`.

NAOMIE-RUNTIME-FAILSAFE-001 : auto-critique et correction de l'incident persistant d'accueil Naomi. Constat : le repo contenait deja des garde-fous, mais ils etaient trop disperses et coexistaient avec des formulations anciennes ; un nouveau chat pouvait encore repondre vaguement ou retomber sur l'ancien libelle `SELAS-NOTEBOOKLM-RECONCILIATION-001`. Correction : creation de `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`, ajout d'une regle prioritaire en tete de `AGENTS.md`, alignement de `SPRINT_SELAS_V1.md` sur la phase 3 NotebookLM, et declaration explicite que le ticket actif est `SELAS-SOURCES-NOTEBOOKLM-001`. Reponse attendue desormais apres un simple `bonjour` de Naomi : statut sprint, action NotebookLM, point pedagogie, prochaine etape, puis Prompt NotebookLM 01 complet. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

MAIN-NAOMIE-TRIGGER-001 : correction du probleme constate sur la capture 2026-06-01, ou un nouveau chat ouvert sur `main` repond genericement a `bonjour` puis `je suis naomi`. Cause : les garde-fous Naomi/SELAS et la tour de controle etaient publies sur `track-b/clean-rebuild` et `codex/naomie-selas-sprint`, mais pas visibles depuis un chat demarre sur `main`. Correction : ajout d'un fail-safe explicite dans `AGENTS.md` et `docs/project/PROJECT_CONTROL_TOWER_V1.md` : si Naomi/SELAS arrive sur `main`, Codex doit tenter de basculer sur `codex/naomie-selas-sprint`, ou bloquer en `NO-GO dev` en expliquant que Codex gere la branche ; il ne doit jamais demander une tache ou un ticket. Le kit de gouvernance doit etre pousse aussi sur `main`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

PROJECT-CONTROL-TOWER-001 : installation d'une vraie tour de controle chef de projet pour SYDEL. Livrable principal : `docs/project/PROJECT_CONTROL_TOWER_V1.md`. Decision : Codex doit toujours commencer par identifier qui parle, le type d'entreprise, le sprint actif, la branche, la phase courante, l'action autorisee et les actions interdites. La tour de controle fixe le cycle standard unique pour chaque type d'entreprise : etat initial, ouverture sprint, sources, sous-sprint NotebookLM, audit reutilisation, matrice documentaire, contrat metier-front, tickets, validation Gad, dev limite, smoke, revue associe, corrections, cloture. Etat courant inscrit : SELARL = production partielle / prochaine revue humaine ou sous-cas borne ; SELAS = sprint actif Naomi / sous-sprint NotebookLM / `NO-GO dev` / Prompt 01 a donner. Pointeurs mis a jour : `AGENTS.md`, `00_MASTER_PLAN.md`, `02_CODEX_WORKFLOW.md`, `03_HANDOFF_FOR_NEW_AGENT.md`, `PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`, `COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`, `SPRINT_SELAS_V1.md`, `01_EXECUTION_BOARD.md` et ce fichier. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

SELAS-NOTEBOOKLM-START-TRIGGER-001 : correction du cas ou Naomi dit qu'elle veut lancer/demarrer/reprendre le sprint SELAS/CELAS et que Codex part trop loin. Decision verrouillee : pour Naomi, `lancer le sprint` signifie uniquement lancer le sous-sprint NotebookLM. Codex doit donner le prompt NotebookLM courant a copier-coller, attendre la reponse brute de Naomi, la structurer dans `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, puis choisir le prompt suivant selon les trous. Interdits avant couverture NotebookLM suffisante : production, generation, code, matrice finale, audit de reutilisation et push de fonctionnalite. Livrables mis a jour : `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/01_EXECUTION_BOARD.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`, `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`, `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` et `docs/sprints/SPRINT_SELAS_V1.md`. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

SELAS-NOTEBOOKLM-PROMPT-LOOP-001 : formalisation de la boucle NotebookLM SELAS pour Naomi. Correction de workflow : Codex ne doit pas seulement constater "il manque une source NotebookLM SELAS" ; il doit donner a Naomi un prompt court a copier dans NotebookLM, recevoir la reponse, la structurer dans `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, puis iterer avec le prompt suivant jusqu'a couverture suffisante. Livrables : `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md`, `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, mise a jour de `docs/sprints/SPRINT_SELAS_V1.md`, `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`, `docs/project/02_CODEX_WORKFLOW.md`, `AGENTS.md` et `docs/project/01_EXECUTION_BOARD.md`. Decision : le prochain message utile a Naomi doit contenir le Prompt NotebookLM 01, pas une demande vague de source. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

NAOMIE-HELLO-TRIGGER-001 : correction de l'incident d'accueil Naomi. Constat : la branche distante `codex/naomie-selas-sprint` existe bien et contient `docs/sprints/SPRINT_SELAS_V1.md`, donc le probleme n'etait pas un manque de push de branche ; le probleme etait un declencheur trop peu explicite dans le chemin de lecture immediat du nouvel agent. Correction : ajout d'un trigger haut niveau dans `AGENTS.md`, durcissement de `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`, de `docs/sprints/SPRINT_SELAS_V1.md` et de `docs/project/02_CODEX_WORKFLOW.md`. Regle nouvelle : si le contexte indique Naomi/Naomi et que le message est seulement `Bonjour`, Codex doit verifier la branche `codex/naomie-selas-sprint`, repondre en phase 0 `ACCUEIL / NO-GO dev`, inclure un point pedagogie et preparer NotebookLM ; la reponse generique "tu veux qu'on attaque quoi dans le moteur documentaire ?" est explicitement interdite. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

FRONT-TEST-PREFILL-001 : entree historique ; les prefills restent utiles, mais la reserve `DOC-006` mentionnee alors est levee par `SELARL-DOC006-REGIME-FIX-001`.

FRONT-UNIT-DOCUMENT-MODE-001 : entree historique ; le mode document unitaire reste hors pilotage SELARL courant. `DOC-006` est desormais un document conditionnel du regime communautaire.

FRONT-DOCUMENT-STATUS-LAYER-001 : entree historique ; le statut courant de `DOC-006` est maintenant `generable` si regime communautaire actif. `DOC-013` et `DOC-014` restent `manual_only`.

COMPANY-TYPE-SPRINT-PLAYBOOK-001 : formalisation du mode d'emploi de sprint par type d'entreprise demande par l'utilisateur. Livrable principal : `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`. Regles fixees : `1 sprint = 1 type d'entreprise`, sprint ecrit et suivi avant dev, demarrage en `NO-GO dev`, lecture des references, interrogation large de NotebookLM ou import de ses reponses, identification obligatoire de Naomi si elle pilote, guidage etape par etape, test de l'associe en fin de sprint, boucle de corrections jusqu'a validation ou report explicite. La SELARL devient le modele de methode via `docs/project/SELARL_CANONICAL_STATUS_V1.md`, mais reste a valider humainement avant cloture juridique 100 %. Pointeurs mis a jour : `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/01_EXECUTION_BOARD.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`, `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `docs/project/SELARL_CANONICAL_STATUS_V1.md` et ce fichier. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

SELARL-CANONICAL-STATUS-001 : consolidation de l'etat SELARL canonique apres le grand tour projet demande par l'utilisateur. Livrable principal : `docs/project/SELARL_CANONICAL_STATUS_V1.md`, qui devient le point de reprise unique pour la SELARL. Decision actuelle : `NO-GO dev` pour toute extension complexe tant qu'un sous-cas unique n'est pas choisi et cadre sous gate produit ; `GO documentation / reprise projet` pour clarifier l'etat, preparer la revue humaine et capitaliser la methode pour les autres formes sociales. Pointeurs mis a jour : `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/01_EXECUTION_BOARD.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` et ce fichier. Prochaine etape recommandee : `SELARL-JURIST-REVIEW-001` sur le pack simple medecin/dentiste et regime communautaire avant nouveau dev complexe. Aucun code Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

PM-PRODUCT-GUARDRAIL-001 : installation du gate produit / métier obligatoire demandé par l'utilisateur. Codex devient le pilote projet / produit principal du dépôt avant développement : reformulation métier, vérification sources/specs, décision `GO dev` ou `NO-GO dev`, possibilité d'utiliser des sous-agents spécialisés, et maintien d'une mémoire de reprise autonome pour les nouveaux chats. Livrables principaux : doctrine globale `docs/project/GLOBAL_CODEX_PRODUCT_GUARDRAIL_V1.md` et protocole local `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`. La doctrine globale est destinée à tous les projets pilotés avec Codex ; le protocole local en est l'application SYDEL. Références mises à jour : `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` et `docs/project/01_EXECUTION_BOARD.md`. Correction complémentaire : les passages obsolètes du master plan et du handoff indiquant que le Lot 1 n'était pas démarré ont été remplacés par l'état Track B courant et par un renvoi vers ce fichier. Aucun code Python, générateur, moteur DOCX/PDF/ZIP, source de vérité ou wording juridique n'a été modifié. Validation limitée à la relecture documentaire, au contrôle du diff et à la revue PM en lecture seule.

TRACK-B-PREVIEW-VALIDATION-AND-CHECKPOINT-009 : validation de la preview clean front Track B et preparation du checkpoint Git local. Le lancement Streamlit a ete fait sans `Start-Process`, via `.\.venv\Scripts\python.exe -m streamlit run src\sydel_doc_engine\front_app\app.py --server.port 8534 --server.headless true --browser.gatherUsageStats false`. Resultat : HTTP 200 confirme sur `http://127.0.0.1:8534`, logs sous `artifacts/track_b_preview_validation_checkpoint_009/`, process termine proprement et port 8534 libre apres arret. Le mode `SELARL dentiste multi-associes simple (PARTIAL statuts)` est present dans le clean front. Validations : `ruff check .` OK ; tests cibles clean front/statuts/PV OK, 46 passes ; smoke dedie dentiste multi-associes PARTIAL OK, 1 pass. Git : les changements Track B accumules depuis le dernier push sont classes pour checkpoint local, sans push ni merge. Aucun nouveau developpement fonctionnel n'a ete ajoute.

TRACK-B-SELARL-DENTIST-MULTI-ASSOCIES-STATUTS-PARTIAL-008 : implementation du sous-cas SELARL chirurgien-dentiste multi-associes simple en mode PARTIAL. Le clean front Track B expose le mode `SELARL dentiste multi-associes simple (PARTIAL statuts)` uniquement pour la profession chirurgien-dentiste, selectionne `DOC-004` et `DOC-016`, reutilise les donnees multi-associes simples du ticket 007, derive les apports par associe depuis les parts et la valeur nominale, choisit le president de seance parmi les associes existants, garde un gerant unique et bloque les parts incoherentes. `DOC-004` reste LOCKED sur ce sous-cas ; `DOC-016` devient PARTIAL avec apports/capital/repartition/signatures associes rendus, mais comparution plurielle et signature plurielle stricte restent OPEN GAP faute de source humaine ligne par ligne. Livrable : `docs/review/track_b_selarl_dentist_multi_associes_statuts_partial_008_report_v1.md`. Artifacts : `artifacts/track_b_selarl_dentist_multi_associes_statuts_partial_008/pv_nomination_gerant.docx`, `statuts_selarl_chirurgien_dentiste.docx` et `dossier_generation.zip`. Validations : tests cibles OK, 46 passes ; `ruff check .` OK ; smoke DOCX/ZIP OK ; controle placeholders/parasites OK ; preview HTTP non validee car le lancement Streamlit via `Start-Process` est reste bloque dans le shell local, ports 8532/8533 verifies libres apres interruption. Aucun push, aucun merge, aucun ticket suivant n'est suggere ici.

TRACK-B-SELARL-MULTI-ASSOCIES-DOC004-LIMITED-007 : implementation du sous-cas SELARL multi-associes simple limite a `DOC-004` uniquement. Le clean front Track B expose le mode `SELARL multi-associes simple (limite DOC-004)`, collecte les associes necessaires au PV, impose le president de seance parmi les associes existants, garde un gerant unique rattache au praticien/associe 1, selectionne uniquement `DOC-004` et affiche clairement les exclusions : statuts multi-associes, plusieurs gerants, cession, SCM, regime communautaire et votes non unanimes. Le contexte moteur construit `associes[]`, derive `reunion.president` depuis l'associe selectionne et bloque les repartitions de parts incoherentes. Livrable : `docs/review/track_b_selarl_multi_associes_doc004_limited_007_report_v1.md`. Artifacts : `artifacts/track_b_selarl_multi_associes_doc004_limited_007/pv_nomination_gerant.docx` et `dossier_generation.zip`. Validations : tests cibles OK, 30 passes ; `ruff check .` OK ; smoke DOCX/ZIP `DOC-004` OK ; clean front HTTP 200 sur `http://localhost:8531`, PID `23780` arrete proprement. Aucun push, aucun merge, aucun ticket suivant n'est suggere ici.

TRACK-B-SELARL-MULTI-ASSOCIES-SOURCE-CONTRACT-006 : contrat source produit pour la famille SELARL multi-associes / president de seance / plusieurs gerants, sans code, sans front et sans modification de wording juridique. Livrable : `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md`. Sources relues : backlog/factory SELARL, human reference lock, reports 003/004/005, retours humains, specs PV/statuts/cession/SCM, modeles domaine/front en verification. Decision : GO limite uniquement pour un futur sous-cas multi-associes simple sur `DOC-004` avec president choisi parmi les associes existants, un gerant unique et unanimite totale ; NO-GO pour statuts multi-associes, plusieurs gerants, president externe, cession medicale/dentaire et cession SCM dans ce contrat. Validations : revue documentaire et diff local, aucun test code ni preview lance car le ticket est documentaire et n'implemente rien. Aucun ticket suivant n'est suggere ici.

TRACK-B-SELARL-MEDECIN-REGIME-COMMUNAUTAIRE-005 : industrialisation du cas SELARL medecin unipersonnelle avec regime communautaire. Le clean front Track B conserve `DOC-017` medecin, active `DOC-005` uniquement quand `regime_communautaire=True`, maintient `DOC-006` en reserve, exige le conjoint et la date du courrier d'avertissement seulement dans ce contexte, et laisse le cas medecin standard sans conjoint ni `DOC-005`. Livrables : rapport `docs/review/track_b_selarl_medecin_regime_communautaire_005_report_v1.md`, tests cibles ajoutes dans `tests/unit/test_clean_front_app.py`, backlog SELARL mis a jour, smoke DOCX/ZIP dans `artifacts/track_b_selarl_medecin_regime_communautaire_005`. Validations : tests cibles OK, 25 passes ; tests cibles + statuts OK, 36 passes ; `ruff check .` OK ; smoke DOCX/ZIP OK, 7 DOCX, ZIP, aucun placeholder, aucun parasite RCS/telephone, `DOC-005` present, `DOC-006` absent ; clean front HTTP 200 sur `http://localhost:8528`, process arrete et verification finale sans process Python/Streamlit restant. Aucun generateur ni wording juridique n'a ete modifie. Aucun ticket suivant n'est suggere ici.

TRACK-B-SELARL-PRODUCTION-PACK-001 : premier pack de production SELARL Track B. Corrections moteur appliquees sur `DOC-001`, `DOC-002`, `DOC-004`, `DOC-005` et `DOC-016` selon les retours humains explicites : adresse personnelle `num voie, CP ville`, domiciliation dans les locaux du cabinet au siege, renonciation sans parasite RCS et avec `Fait pour servir et valoir ce que de droit.`, PV sans `RCS de ...`, sans `EXTRAORDINAIRE`, sans heure de reunion, avec president de seance rattache a l'associe unique et libelle singulier/pluriel de nomination, statuts chirurgien-dentiste avec `euros`, communaute et prestataire de signature electronique coherent. Livrables documentation : `docs/project/SELARL_PRODUCTION_FACTORY_V1.md` et `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md`. Validations : tests cibles OK, 55 passes ; `ruff check .` OK ; smoke DOCX/ZIP SELARL dentiste + regime communautaire OK dans `artifacts/track_b_selarl_production_pack_001/selarl-dentiste-regime` ; clean front lance sur `http://localhost:8513`, HTTP 200 confirme, PID `19756` arrete proprement. Prochaine etape recommandee : relecture humaine des DOCX SELARL produits par ce pack avant extension aux variantes restantes.

TRACK-B-SELARL-TEST-DATA-PREFILL-001 : ajout d'un bouton `Generer des donnees de test` immediatement sous `Type de dossier` dans le clean front SELARL V1. Le bouton pre-remplit un dossier SELARL aleatoire mais coherent pour accelerer les tests : profession medecin ou chirurgien-dentiste, dossier unipersonnel, hors scope V1 desactive, dates `JJ/MM/AAAA`, capital et parts coherents, ordre, banque, siege, praticien et conjoint si necessaire. Le test AppTest verifie que le pre-remplissage rend la generation possible et expose un bouton de telechargement ZIP. Validations : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py -q` OK, 14 tests passes ; clean front lance sur `http://localhost:8512`, HTTP 200 confirme, PID `35648` arrete proprement ; browser-use a refuse localhost et n'a pas ete contourne. Aucun generateur, moteur documentaire, wording juridique source, Track A, repo anchor ou merge n'a ete modifie.

TRACK-B-SELARL-DOWNLOAD-UX-001 : correction du retour testeur indiquant que le dossier genere ne se telechargeait pas localement. Le clean front conserve maintenant le dernier dossier genere en session Streamlit et affiche des boutons de telechargement natifs pour le ZIP et chaque DOCX. Les chemins serveur restent affiches en information, mais ne sont plus le seul moyen de recuperer les fichiers. Validations : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py -q` OK, 13 tests passes ; clean front lance sur `http://localhost:8511`, HTTP 200 confirme, PID `16648` arrete proprement ; browser-use a refuse localhost et n'a pas ete contourne. Aucun generateur, moteur documentaire, wording juridique source, Track A, repo anchor, push ou merge n'a ete modifie.

TRACK-B-SELARL-UX-FOLLOWUP-001 : corrections apres test local du clean front SELARL V1. Dates visibles passees en champs texte `JJ/MM/AAAA` sans borne Streamlit, bouton `Aujourd'hui` conserve, `Situation matrimoniale` en liste courte, doublon visible `Regime matrimonial` retire au profit de la case `Documents regime de la communaute`, valeur nominale calculee par capital / parts, champs ordre clarifies. Validations : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py -q` OK, 12 tests passes ; clean front lance sur `http://localhost:8510`, HTTP 200 confirme, PID `3480` arrete proprement. Aucun generateur, moteur documentaire, wording juridique source, Track A, repo anchor, push ou merge n'a ete modifie.

TRACK-B-SELARL-UX-DEDUP-RECONCILIATION-001 : reconciliation UX du clean front SELARL V1 apres retours associe / NotebookLM. Livrables : `src/sydel_doc_engine/front_app/field_derivations.py`, corrections ciblees dans `data_entry.py`, `shell.py`, `selarl_slice.py`, tests `tests/unit/test_clean_front_app.py` et pilotage mis a jour. Corrections appliquees : suppression des champs visibles de genre grammatical et titre d'affichage, derivation des accords depuis la civilite, suppression des champs en lettres derivables, capital/parts/valeur nominale en saisie numerique, boutons `Aujourd'hui` sur les dates visibles, lieu d'exercice masque par defaut derriere `Autre lieu d'exercice ?`, conjoint masque hors cas utile, date courrier avertissement visible seulement si regime communautaire, mandataire SYDEL pre-rempli hors parcours principal, seuils de gerance et prestataire Yousign fixes par defaut, repartition associe unique conservee a 100 %, nationalite remplacee par presets courts + `Autre`. Aucun generateur, moteur documentaire, wording juridique source, Track A, repo anchor, push ou merge n'a ete modifie. Validations : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py -q` OK, 11 tests passes ; clean front lance via `.\.venv\Scripts\python.exe -m streamlit run src/sydel_doc_engine/front_app/app.py --server.port 8508 --server.headless true --browser.gatherUsageStats false`, HTTP 200 confirme sur `http://localhost:8508`, PID `18436` arrete proprement. Aucun ticket suivant n'est suggere.

SELARL-FLOW-REALIGN-001 : réalignement de l'ordre conceptuel SELARL dans le schéma et les projections métier. Le flow cible est désormais explicite : Qualification, Fiche Client / Praticien, Fiche Société, Capital & Associés, Contexte & scénarios métier, Documents & génération. `src/sydel_doc_engine/app/selarl_form_schema.py` expose `FormStep`, `SELARL_FLOW_STEPS` et `selarl_blocks_by_step()`, `src/sydel_doc_engine/app/business_wizard.py` expose les projections par étape, les specs actives sont mises à jour in-place et le rapport est `docs/review/selarl_flow_realign_001_report_v1.md`. Aucun générateur, moteur DOCX/PDF/ZIP, `case_catalog.py`, mode SCI ou wording juridique n'a été modifié. `streamlit_app.py` n'a pas été touché ; l'UI visible reste non validée produit et ne doit pas être poussée ou redéployée avant le ticket UI dédié. Ruff OK et pytest OK avec 245 tests passés.

SELARL-WORDING-REALIGN-001 : réalignement du vocabulaire visible SELARL sur les arbitrages associé. L'écran personne visible devient `Fiche Client`, le terme pivot devient `Praticien`, les rôles `Gérant`, `Associé`, `Signataire` et `Mandataire` restent conservés selon contexte, et les specs actives sont mises à jour in-place. Aucun générateur, moteur DOCX/PDF/ZIP, `case_catalog.py`, ordre d'écran ou règle de réutilisation fonctionnelle n'a été modifié. Rapport : `docs/review/selarl_wording_realign_001_report_v1.md`. Ruff OK et pytest OK avec 241 tests passés.

SELARL-PLAN-CORRECTION-001 : correction documentaire de la planification SELARL selon les arbitrages explicites de l'associé. La hiérarchie de sources place désormais les arbitrages associé avant NotebookLM, puis V3, templates/registre et code existant. Le rapport de réconciliation et le backlog ont été resserrés autour de `Fiche Client`, `Praticien` et `Dossier unipersonnel`, avec retrait du mode Projet / filigrane V1, retrait de la couche statut documentaire lourde et sortie du mandataire des priorités UX hors variables ou documents liés. Aucun fichier Python, générateur, moteur DOCX/PDF/ZIP ou UI n'a été modifié ; aucun test code lancé car les modifications sont documentaires.

SELARL-NOTEBOOKLM-RECONCILIATION-001 : réconciliation documentaire du pilote SELARL avec la nouvelle hiérarchie NotebookLM / V3 / templates / code. Les sources validées par l'utilisateur ont été normalisées et committées sous `project/source_truth/notebooklm_selarl_10_prompts_v1.md` et `project/source_truth/Documents_a_generer_par_cas_V3.docx` dans le commit source `f1da08b`. Le ticket crée `docs/project/SELARL_SOURCE_HIERARCHY_V2.md`, `docs/review/selarl_notebooklm_reconciliation_001_report_v1.md` et `docs/project/SELARL_REBUILD_BACKLOG_V2.md`, puis bloque le smoke SELARL prématuré au profit d'une reconstruction contrôlée. Cette reconstruction a été corrigée par `SELARL-PLAN-CORRECTION-001` : wording, flow, réutilisations, UI, smoke réaliste, revue juriste.

SELARL-UI-WIZARD-IMPL-001 : entree historique ; l'affichage `DOC-006` avec reserve source V2 est remplace par la regle courante `DOC-006` generable si regime communautaire actif. `DOC-013` et `DOC-014` restent visibles mais `MANUAL_ONLY`.

SELARL-FORM-SCHEMA-IMPL-001 : implémentation du schéma de données SELARL côté Assistant métier depuis la vraie source V2 `project/source_truth/Documents_a_generer_par_cas_V2.docx`, ajout de `src/sydel_doc_engine/app/selarl_form_schema.py`, couverture machine-readable des blocs métier, champs qualifiés, règles de réutilisation, documents attendus et variables V2, ajout de la réserve source V2 exploitable sur `DOC-006`, clarification finale de `DOC-013` / `DOC-014` comme `MANUAL_ONLY` hors génération pilote, rapport `docs/review/selarl_form_schema_impl_001_report_v1.md`, ruff OK et pytest OK avec 231 tests passés.

SELARL-PILOT-SOURCE-VERIFY-001 : vérification des livrables SELARL contre la vraie source V2 de l'associé `project/source_truth/Documents_a_generer_par_cas_V2.docx` hash SHA-256 `2E9843AA1EC05A01D82DF5FCE12516A8EF49EA2B3842547D186204218C90B23F`, remplacement du fichier V2 canonique provisoire, création du rapport `docs/review/selarl_source_verify_001_report_v1.md`, correction des statuts de dérogation SELARL dans le catalogue (`DOC-013` et `DOC-014` hors génération pilote), enrichissement des specs SELARL avec les variables V2 brutes et réserves source ; ruff OK et pytest OK avec 217 tests passés.

SELARL-PILOT-PROTOCOL-001 : cadrage produit du pilote SELARL depuis `project/source_truth/Documents_a_generer_par_cas_V2.docx`, création du protocole réplicable de construction de processus, des specs SELARL processus/formulaire/wizard, du plan d'implémentation et du rapport `docs/review/selarl_pilot_protocol_001_report_v1.md`, sans modification de l'UI, du moteur DOCX/PDF/ZIP ni des générateurs ; ruff OK et pytest OK avec 217 tests passés.

UI-CASE-WIZARD-002 : branchement du mode Assistant metier Streamlit sur `get_expected_documents(...)` et CASE-CATALOG-001, ajout des conditions UI pour les 8 familles, affichage des documents attendus avec statuts generable / manuel / non implemente / mapping / contexte incomplet V2, filtrage de la generation sur les seuls documents attendus generables avec `DOC-XXX` et contexte pret, mode Technique / diagnostic conserve, rapport `docs/review/ui_case_wizard_002_report_v1.md`, ruff OK et pytest OK avec 217 tests passes.

CASE-CATALOG-001 : creation de la couche metier catalogue des cas depuis `project/source_truth/Documents_a_generer_par_cas.docx`, ajout de `src/sydel_doc_engine/domain/case_catalog.py` avec `get_expected_documents(...)`, 46 documents attendus uniques modelises dont 43 mappes au registre `DOC-001` a `DOC-043`, 2 documents manuels, 1 document non implemente, rapport `docs/review/case_catalog_001_report_v1.md`, ruff OK et pytest OK avec 208 tests passes.

DEPLOY-STREAMLIT-CLOUD-FIX-001 : correction de packaging Streamlit Cloud depuis le dossier canonique `C:\Users\Gad\Desktop\Sydel\sydel-document-engine`, ajout de la declaration Poetry explicite `{ include = "sydel_doc_engine", from = "src" }` dans `pyproject.toml`, rapport `docs/review/deploy_streamlit_cloud_fix_001_report_v1.md`, installation editable OK, ruff OK et pytest OK avec 196 tests passes ; Poetry local indisponible, donc `poetry check` et `poetry install` non executes localement.

UI-BUSINESS-WIZARD-001 : mode Assistant metier Streamlit ajoute depuis le dossier canonique `C:\Users\Gad\Desktop\Sydel\sydel-document-engine`, formulaire SCI simple pour `DOC-001` a `DOC-004`, validation champs manquants/incoherences, boutons DOCX/ZIP/PDF, telechargements, mode technique YAML/JSON conserve et rapport `docs/review/ui_business_wizard_001_report_v1.md` ajoute.

REVIEW-FINAL-001 : revue finale executee depuis le dossier canonique `C:\Users\Gad\Desktop\Sydel\sydel-document-engine`, rapport ajoute dans `docs/review/review_final_001_execution_report_v1.md`, ruff/pytest verts, smoke DOCX/ZIP OK sur `lot_02_orchestrator_positive_example.yaml`, backend PDF local indisponible pendant la revue et decision GO avec reserves pour `UI-BUSINESS-WIZARD-001`.

WORKTREE-CLEANUP-AND-UI-STATUS-001 : consolidation du contenu restant de `codex/review-final-001` dans `main`, creation du rapport `docs/project/23_WORKTREE_CLEANUP_AND_UI_STATUS_V1.md`, clarification du dossier canonique final et archivage local prevu des anciens worktrees `sydel-document-engine-*`.

SYNC-FINAL-FOUNDATIONS-001 : synchronisation finale de `main` avant revue/cloture, absorption des complements UI/PDF/ZIP manquants, confirmation des audits/fondations presents, remplacement de `UI-CORE-001` par `UI-PDF-ZIP-INTEGRATION-001` et pilotage final limite a `REVIEW-FINAL-001` puis `CLOSE-PROJECT-V1-001`.

UI-PDF-ZIP-INTEGRATION-001 : integration de l'UI Streamlit avec la generation dossier DOCX, l'export PDF local optionnel et le ZIP dossier, avec telechargements par fichier, smoke manuel documente et validations locales vertes.

SYNC-POST-MOTOR-UI-001 : absorption dans `main` des fondations UI/PDF/recette issues des branches `codex/ui-flow-001`, `codex/ui-occurrences-001`, `codex/ui-form-schema-001`, `codex/pdf-backend-001` et `codex/recipe-frame-001`, puis réalignement du pilotage vers `UI-CORE-001`, `RESUME-ZIP-BACKEND-001` et `REVIEW-FINAL-001`.

PDF-BACKEND-001 : implementation d'un backend local d'export PDF depuis DOCX genere, avec priorite LibreOffice headless si disponible puis fallback Word COM Windows, erreurs explicites, tests ciblés, smoke réel DOCX vers PDF et aucune modification UI.

RECONCILE-MOTOR-CLOSE-001 : reconciliation finale du moteur DOCX V1, exposition des generateurs ordre/SPFPL sous `DOC-034` a `DOC-043`, consolidation des referentiels `08/09`, integration des audits `17/18`, requalification de l'audit `16`, validations ruff/pytest et cloture moteur hors UI/PDF/ZIP/recette finale.

SYNC-CLOSE-AUDIT-001 : absorption dans `main` du commit source `0139202b170531fd628f25811c55855a2512acc0` depuis `origin/codex/close-motor-audit-001`, confirmation de `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` et conservation de la version finale plus récente déjà présente dans `main`, sans modification de code Python.

FINAL-SCM-CESSION-WAVE-001 : restauration de la résolution V1 cession SCM depuis la branche d'arbitrage, implémentation du bloc cession SCM sous `DOC-031` à `DOC-033`, smoke DOCX réel, validations ruff/pytest et audit de clôture moteur V1.

SYNC-WAVE-010 : absorption finale dans `main` des branches `codex/arbitrage-scm-cession-resolve-001` et `codex/code-scm-cession-block-001`, passage en DONE des tickets SCM cession finaux et réalignement du pilotage vers UI, PDF, ZIP et recette finale.

SYNC-WAVE-009 : absorption dans `main` des commits sources `4288837648d099935d6c57307003f3b33d038d90`, `af1020a165d11e830428394e02a5baca4a110f5c`, `81f7a7e407002428d8fce1ce31d16f3a798bd2e5`, `fa3cb65ffd1055bbf16ba3a5352f4a7d5deb713a` et `bdf61166b0770c5ab8f3610f48d89e5cdcb3f582`, puis réalignement du pilotage.

SYNC-WAVE-008 : absorption dans `main` des branches acte actions, sources SCM cession, reviews Lot 03/Lot 04, audit restant, analyses style Lot 03/statuts et specs blocage cession SCM, puis réalignement du pilotage.

SYNC-WAVE-007 : absorption dans `main` des branches SCM et acte actions, passage en DONE des tickets absorbés et réalignement du pilotage.

SYNC-WAVE-006 : absorption dans `main` des branches tardives Lot 04 / Lot 05, passage en DONE des tickets absorbés et réalignement du pilotage.

CONVERT-ACTE-ACTIONS-001 : conversion du candidat legacy `Acte_cession_SPFPL_tiers_modele.doc` en DOCX exploitable, placement dans `project/source_documents/lot_05/` et documentation de préparation V1.

CONVERT-DEROG-SALARIEE-001 : tentative de conversion Word COM du `.doc` legacy salariee, aucun DOCX exploitable produit, blocage documente.

SYNC-WAVE-005 : absorption dans `main` des commits sources `91436f0916fdecbcc98450b72ba6e602cb8f1a3b`, `1b3ba14d0bcc31fc7dcbf1752d6d3263645ae8b3`, `32059155c618b4e985893f42ef2817187599c281`, `74d41db53543b790e197082e8b9c713f7de92dc2` et `d1d649e11fdc638e6d7da0640c154d1f213739ee`, puis réalignement du pilotage.

TRACK-B-SELARL-VERTICAL-SLICE-IMPLEMENT-001 : implementation de la vertical slice SELARL V1 bornee dans le nouveau front propre Track B. Livrables : `src/sydel_doc_engine/front_app/selarl_slice.py`, realignement de `data_entry.py`, `dossier_selection.py`, `generation.py`, `shell.py`, tests `tests/unit/test_clean_front_app.py` et pilotage mis a jour. Perimetre implemente : creation SELARL medecin/chirurgien-dentiste, associe unique, generation DOCX/ZIP de `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-017` ou `DOC-016`, et `DOC-005` seulement si regime communautaire actif. Hors scope volontairement bloque ou signale : cession, SCM, derogations, site distinct, `DOC-006`, SELAS, micro-holding et statuts multi-associes. Aucun push, aucun merge, aucune modification du moteur documentaire ni du wording juridique source.

TRACK-B-SELARL-SOURCE-OF-TRUTH-CONTRACT-001 : gel du contrat metier-front SELARL V1 depuis les sources de verite Track B. Livrable : `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md`. Sources consolidees : reponse metier Albane, sources V2/V3, NotebookLM utilise uniquement en resolution/vocabulaire/flow, specs SELARL, lots ordre/PV/statuts, revues front/schema/flow et verification de coherence `front_data`/catalogue. Conclusion : GO pour une vertical slice SELARL V1 bornee a creation medecin/chirurgien-dentiste unipersonnelle avec `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016` ou `DOC-017`, et `DOC-005` conditionnel. Hors generation automatique V1 : cession, SCM, derogations, site distinct, `DOC-006` et statuts multi-associes. Aucun code, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

TRACK-B-FRONT-ARCHITECTURE-RESET-001 : refondation du chemin front Track B propre apres arbitrage produit. Livrables : nouveau package `src/sydel_doc_engine/front_app/` avec entrypoint `app.py`, shell minimal, routing, selection dossier, zone de saisie, zone generation placeholder, frontiere legacy, tests `tests/unit/test_clean_front_app.py`, rapport `docs/review/track_b_front_architecture_reset_001_report_v1.md`, commande de lancement documentee et mise a jour du pilotage. Constats : le moteur documentaire et `front_data/` restent conserves ; l'ancien `src/sydel_doc_engine/app/streamlit_app.py` reste reference historique mais n'est pas importe par le nouveau point d'entree ; Assistant metier prototype, Document unitaire, Technique / diagnostic, Debug interne et ecrans historiques ne sont pas exposes dans `front_app`. Limite volontaire : aucune vraie implementation metier SELARL n'est ajoutee ; la zone Generation affiche un slot non generable jusqu'au branchement d'une vertical slice propre. Aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie.

SELARL-COMPLETE-CONTEXT-ADAPTER-001 : branchement de l'adaptateur front SELARL complet apres le playbook. Livrables : `src/sydel_doc_engine/app/front_selarl_complete.py`, extension limitee de `src/sydel_doc_engine/app/front_dossier_entry.py`, `src/sydel_doc_engine/app/front_generation_actions.py`, `src/sydel_doc_engine/app/streamlit_app.py`, tests front mis a jour, rapport `docs/review/selarl_complete_context_adapter_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Constats : le nouveau front global n'est plus limite a `DOC-001` a `DOC-004`; SELARL medecin simple genere `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034` et `DOC-017`; SELARL chirurgien-dentiste bascule vers `DOC-016`; regime communautaire ajoute `DOC-005` tout en gardant `DOC-006` en reserve exclue ; `DOC-013`, `DOC-014` et la derogation SEL BNC sans code restent manuels/exclus. Limite volontaire : cession medicale/dentaire et cession SCM sont selectionnees depuis le catalogue mais restent `context_incomplete` jusqu'aux sous-formulaires metier. Aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie. Validations : `ruff check .` OK ; tests cibles front OK, 23 tests passes ; smoke DOCX dentiste et regime communautaire OK ; `pytest` complet tente mais non conclusif par `PermissionError` Windows sur les dossiers temporaires `tmp_path`/`basetemp`. Prochaine etape courante : lire `docs/project/SELARL_CANONICAL_STATUS_V1.md` puis lancer la revue humaine ou choisir un seul sous-cas avec `GO dev`.

SELARL-COMPLETE-CASE-PLAYBOOK-001 : cadrage de la SELARL complete apres retour utilisateur sur la limite actuelle a quatre documents. Livrables : `docs/project/SELARL_COMPLETE_CASE_PLAYBOOK_V1.md`, `docs/review/selarl_complete_case_playbook_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Constats : le moteur contient deja les generateurs principaux SELARL (`DOC-001` a `DOC-012`, `DOC-016`, `DOC-017`, `DOC-031`, `DOC-032`, `DOC-033`, `DOC-034`), mais le nouveau front global et les garde-fous de readiness restent explicitement limites a `DOC-001` a `DOC-004`. `DOC-013`, `DOC-014` et les documents sans code restent manuels dans le flux SELARL verifie ; `DOC-006` conserve sa reserve. Aucun Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie. Aucun test Python requis. Prochaine etape recommandee : `SELARL-COMPLETE-CONTEXT-ADAPTER-001`.

FRONT-MINIMAL-SURFACE-CLEANUP-001 : application de la surface utilisateur minimale avant test. Livrables : coupe UI dans `src/sydel_doc_engine/app/streamlit_app.py`, tests AppTest adaptes, rapport `docs/review/front_minimal_surface_cleanup_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Constats : la vue normale affiche uniquement `Type de dossier`, `Donnees a saisir` et `Generation`, avec 0 radio, 0 table, 0 expander et aucun outil interne visible. Les outils internes restent accessibles seulement via mode equipe cache (`SYDEL_ENABLE_INTERNAL_TOOLS=1` ou flag de session interne). Le PDF est cache quand le backend local est indisponible ; les blocages data-layer/runtime sont affiches dans `Generation`. Aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie. Validations : tests cibles OK, 79 tests passes ; ruff OK ; pytest OK, 382 tests passes. Prochaine etape recommandee : test utilisateur local du pilote `SELARL creation simple`.

FRONT-REALITY-CHECK-001 : audit de realite du nouveau front global contre les debriefs recents. Livrables : `docs/review/front_reality_check_001_report_v1.md`, `docs/project/FRONT_MINIMAL_USER_SURFACE_V1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Constats : la vue normale est bien reduite techniquement a `Type de dossier`, `Donnees a saisir` et `Generation`, sans radio ni tableau par defaut, mais elle reste chargee par 3 expanders ouverts, 22 champs texte, la checkbox sidebar `Outils internes`, un bouton PDF visible meme lorsque le backend est indisponible et des blocages runtime non expliques. Generation reelle : DOCX et ZIP branches depuis le nouveau front pour `DOC-001` a `DOC-004`; PDF branche en code mais indisponible localement (`is_pdf_export_available() == False`). Aucun Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie. Prochaine etape recommandee : `FRONT-MINIMAL-SURFACE-CLEANUP-001`.

FRONT-STATE-AUDIT-001 : audit de reprise apres retour utilisateur sur le nouveau front. Livrables : `docs/review/front_state_audit_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Constats : le moteur reste disponible sur 43 documents moteurs (`DOC-001` a `DOC-043`) et le catalogue metier contient 46 documents attendus, mais la surface normale du nouveau front est volontairement limitee au pilote `SELARL creation simple` et a la generation `DOC-001` a `DOC-004`. Cause UX principale : la readiness data-layer peut declarer les quatre documents generables pendant que l'adaptateur moteur bloque ensuite sur un format de date, une adresse ou une ville RCS, sans exposer le detail dans la vue normale. Tests cibles OK : `test_front_generation_actions.py` 6 passes, `test_front_dossier_data_entry.py` 10 passes. Aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique n'a ete modifie. Prochaine etape recommandee : `FRONT-GENERATION-READINESS-UX-001`, puis `FRONT-DOCUMENTS-PANEL-001`.

FRONT-UX-HARD-CUT-001 : retrait complet du bruit non-user de la vue principale normale du nouveau front. Livrables : durcissement de `src/sydel_doc_engine/app/streamlit_app.py`, tests adaptes `tests/unit/test_front_ui_shell.py`, `tests/unit/test_front_dossier_editor.py`, `tests/unit/test_front_dossier_data_entry.py`, `tests/unit/test_front_generation_actions.py`, `tests/unit/test_business_wizard.py`, `tests/unit/test_single_document_mode.py`, rapport `docs/review/front_ux_hard_cut_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Decisions : la vue normale ne rend plus aucun radio de navigation, aucun tableau et aucun diagnostic ; elle affiche uniquement `Type de dossier`, `Donnees a saisir` et `Generation`. Les outils `Assistant metier prototype`, `Document unitaire`, `Technique / diagnostic` et `Debug interne` sont deplaces derriere la checkbox sidebar `Outils internes`. Ruff OK et pytest OK, 380 tests passes. Aucun generateur, moteur DOCX/PDF/ZIP, fondation `front_data` ou wording juridique n'a ete modifie. Prochaine etape recommandee : vrai test local utilisateur sur `SELARL creation simple`.

FRONT-UX-CLEANUP-001 : simplification radicale de la vue principale du nouveau front pour permettre un vrai test utilisateur local. Livrables : nettoyage de `src/sydel_doc_engine/app/streamlit_app.py`, tests adaptes `tests/unit/test_front_ui_shell.py`, `tests/unit/test_front_dossier_editor.py`, `tests/unit/test_front_dossier_data_entry.py`, `tests/unit/test_front_generation_actions.py`, rapport `docs/review/front_ux_cleanup_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Decisions : la vue principale affiche maintenant directement le choix du type de dossier, la saisie, un resume minimal des documents prets/bloques et les actions de generation ; les tableaux de flow, blocs actifs, exigences, statuts documentaires et statut de lot sont replies dans des diagnostics ; le prototype, Document unitaire et Technique / diagnostic restent secondaires. Ruff OK et pytest OK, 380 tests passes. Aucun generateur, moteur DOCX/PDF/ZIP, fondation `front_data` ou wording juridique n'a ete modifie. Prochaine etape recommandee : premier vrai test local du nouveau front simplifie sur `SELARL creation simple`.

FRONT-GENERATION-ACTIONS-001 : premieres actions de generation depuis le nouveau front visible sur le profil prudent `SELARL creation simple`. Livrables : `src/sydel_doc_engine/app/front_generation_actions.py`, enrichissement minimal de `src/sydel_doc_engine/app/front_dossier_entry.py` pour les champs runtime requis, branchement dans `src/sydel_doc_engine/app/streamlit_app.py`, mise a jour de `src/sydel_doc_engine/app/front_shell.py`, tests `tests/unit/test_front_generation_actions.py`, rapport `docs/review/front_generation_actions_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Decisions : seuls `DOC-001`, `DOC-002`, `DOC-003` et `DOC-004` peuvent etre envoyes aux generateurs depuis le nouveau front ; `DOC-006`, `DOC-013` et `DOC-014` restent exclus ; l'action consomme `DossierRecord`, `document_status` et `ui_runtime`, sans dependance au `business_wizard`. DOCX est prioritaire, ZIP est propose apres DOCX, PDF reste optionnel selon backend local. Ruff OK et pytest OK, 380 tests passes. Aucun generateur, moteur DOCX/PDF/ZIP, wording juridique ou prototype historique n'a ete modifie. Prochaine etape recommandee : premier vrai test local du nouveau front, puis `FRONT-DOCUMENTS-PANEL-001`.

FRONT-DOSSIER-DATA-ENTRY-001 : premiere tranche de saisie reelle du nouvel editeur dossier sur le profil `SELARL creation simple`. Livrables : `src/sydel_doc_engine/app/front_dossier_entry.py`, branchement de la saisie dans `src/sydel_doc_engine/app/streamlit_app.py`, mise a jour de `src/sydel_doc_engine/app/front_shell.py`, tests `tests/unit/test_front_dossier_data_entry.py`, rapport `docs/review/front_dossier_data_entry_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Decisions : la saisie V1 alimente un vrai `DossierRecord` avec `PersonRecord`, `CompanyRecord`, `AddressRecord`, `RoleAssignment`, `ReuseRuleState` et `CanonicalFieldValue` ; `Dossier unipersonnel` cree des roles explicites sans fusion silencieuse ; `domiciliation = siege_social` reste une regle tracee ; `DOC-001` a `DOC-004` deviennent generables quand les donnees minimales sont completes. Ruff OK et pytest OK, 374 tests passes. Aucun generateur, moteur DOCX/PDF/ZIP, wording juridique ou prototype historique n'a ete modifie. Prochaine etape recommandee : `FRONT-DOCUMENTS-PANEL-001`.

FRONT-DOSSIER-EDITOR-001 : premiere tranche visible de l'editeur dossier du nouveau front global. Livrables : `src/sydel_doc_engine/app/front_dossier_editor.py`, branchement dans `src/sydel_doc_engine/app/streamlit_app.py`, mise a jour de `src/sydel_doc_engine/app/front_shell.py`, tests `tests/unit/test_front_dossier_editor.py`, rapport `docs/review/front_dossier_editor_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Decisions : l'editeur V1 construit un `DossierRecord` minimal depuis des profils prudents, consomme `dossier_flow` pour les etapes/blocs, consomme `document_status` pour les documents attendus et statuts de lot, et garde la saisie effective/generation pour les tickets suivants. Ruff OK et pytest OK, 364 tests passes. Aucun generateur, moteur DOCX/PDF/ZIP, wording juridique ou prototype historique n'a ete modifie. Prochaine etape recommandee : `FRONT-DOCUMENTS-PANEL-001`.

FRONT-UI-SHELL-001 : premiere tranche visible du nouveau front global. Livrables : `src/sydel_doc_engine/app/front_shell.py`, mise a jour de `src/sydel_doc_engine/app/streamlit_app.py`, tests `tests/unit/test_front_ui_shell.py`, adaptations de navigation AppTest dans `tests/unit/test_business_wizard.py` et `tests/unit/test_single_document_mode.py`, rapport `docs/review/front_ui_shell_001_report_v1.md`, mise a jour de `docs/project/01_EXECUTION_BOARD.md`, `docs/project/04_LAST_STATE.md` et `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`. Decisions : le top-level Streamlit distingue maintenant `Nouveau front global` et `Prototype / outils de test` ; les zones cible `Accueil / selection`, `Dossier`, `Documents attendus` et `Generation` sont visibles ; le prototype historique reste accessible uniquement comme bac a sable, document unitaire et diagnostic technique. Le shell consomme `dossier_flow` et `document_status` en lecture, sans generation et sans editeur dossier complet. Ruff OK et pytest OK. Prochaine etape recommandee : `FRONT-DOSSIER-EDITOR-001`.

FRONT-REVIEW-001 : revue globale du prototype front actuel contre les nouvelles fondations `front_data`, roles, adresses, flow dossier, statuts documentaires, mode document unitaire et prefills. Livrables : `docs/project/FRONT_MIGRATION_MAP_V1.md`, `docs/review/front_review_001_report_v1.md`, mise a jour de `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`, `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md`. Decisions : le prototype Streamlit reste bac a sable et outil de diagnostic ; `front_data/*`, `dossier_flow`, `document_status` et `unit_document_mode` deviennent les fondations a migrer ; `business_wizard.py`, les projections SELARL historiques et les helpers `session_state` sont a deprecier apres remplacement ; `Technique / diagnostic`, Document unitaire et prefills restent des outils de test. Aucun code Python modifie, donc pas de ruff/pytest requis. Prochaine etape recommandee : `FRONT-UI-SHELL-001`.

FRONT-TEST-PREFILL-001 : realignement du pre-remplissage de test `Assistant metier` sur la couche `front_data`, sans modification des generateurs, du moteur DOCX/PDF/ZIP, du wording juridique, du mode `Technique / diagnostic` ni du mode `Document unitaire`. Livrables : `src/sydel_doc_engine/front_data/test_prefill_presets.py`, enrichissement de `src/sydel_doc_engine/app/test_prefill_presets.py`, exports publics dans `src/sydel_doc_engine/front_data/__init__.py`, tests `tests/unit/test_front_prefill_mode.py`, rapport `docs/review/front_test_prefill_001_report_v1.md` et pilotage mis a jour. Decisions : les quatre scenarios existants sont conserves ; les prefills savent maintenant produire un `BusinessWizardInput`, un `DossierRecord` front_data et une synthese de statuts ; le scenario SELARL simple rend `DOC-001` a `DOC-004` generables ; `DOC-006` garde sa reserve, `DOC-013`/`DOC-014` restent manuels, `DOC-009` reste orange/non artificiellement resolu ; SCI reste un scenario de non-regression du wizard historique avec une limite front_data documentee sur `DOC-002`. Ruff OK et pytest OK, 352 tests passes. Prochaine etape recommandee : `FRONT-REVIEW-001`.

FRONT-UNIT-DOCUMENT-MODE-001 : fondation du mode de test Document unitaire adosse a la nouvelle couche `front_data`, sans modification des generateurs, du moteur DOCX/PDF/ZIP ni du wording juridique. Livrables : `src/sydel_doc_engine/front_data/unit_document_mode.py`, exports publics dans `src/sydel_doc_engine/front_data/__init__.py`, realignement de l'adaptateur `src/sydel_doc_engine/app/single_document_mode.py`, affichage minimal des exigences data-layer dans `src/sydel_doc_engine/app/streamlit_app.py`, tests `tests/unit/test_front_unit_document_mode.py`, rapport `docs/review/front_unit_document_mode_001_report_v1.md` et pilotage mis a jour. Decisions : le perimetre V1 generable reste prudent sur `DOC-001`, `DOC-002`, `DOC-003` et `DOC-004` ; `DOC-006` reste visible avec reserve, `DOC-013` et `DOC-014` restent manuels, `DOC-033` et `DOC-034` sont explicitement hors perimetre V1. Le mode unitaire utilise des `DocumentRequirementRecord`, `DocumentStatusRecord`, roles, adresses typees et flow dossier pour verifier la readiness avant generation. Ruff OK et pytest OK, 344 tests passes. Prochaine etape recommandee : `FRONT-TEST-PREFILL-001`.

FRONT-DOCUMENT-STATUS-LAYER-001 : fondation de la couche de statuts documentaires front dans `front_data`, sans modification de l'UI visible, de Streamlit, des generateurs ni du moteur DOCX/PDF/ZIP. Livrables : `src/sydel_doc_engine/front_data/document_status.py`, exports publics dans `src/sydel_doc_engine/front_data/__init__.py`, tests `tests/unit/test_front_document_status_layer.py`, rapport `docs/review/front_document_status_layer_001_report_v1.md` et pilotage mis a jour. Decisions : les statuts documentaires retenus sont `expected`, `generable`, `manual_only`, `not_implemented`, `context_incomplete`, `blocked_missing_data`, `blocked_unresolved_ambiguity` et `generable_with_reserve` ; les statuts de lot sont `ready`, `partial`, `blocked` ; les raisons de statut sont tracees depuis `DocumentRequirementRecord`, validations, flow dossier, catalogue et reserves. `DOC-006` peut etre `generable_with_reserve`, `DOC-013` et `DOC-014` restent `manual_only`, et les sentinelles orange gardent leurs raisons de blocage sans resolution artificielle. Ruff OK et pytest OK, 333 tests passes. Prochaine etape recommandee : `FRONT-UNIT-DOCUMENT-MODE-001`.

FRONT-DOSSIER-FLOW-001 : fondation du flow dossier global dans la couche `front_data`, sans modification de l'UI visible, de Streamlit, des generateurs ni du moteur DOCX/PDF/ZIP. Livrables : `src/sydel_doc_engine/front_data/dossier_flow.py`, exports publics dans `src/sydel_doc_engine/front_data/__init__.py`, tests `tests/unit/test_front_dossier_flow.py`, rapport `docs/review/front_dossier_flow_001_report_v1.md` et pilotage mis a jour. Decisions : le flow retient les etapes Qualification, Fiche personnes, Fiche societe, Roles & parties, Adresses, Capital/titres/apports, Ordre, Operations, Documents attendus et Generation ; les blocs activables couvrent ordre/mandataire, capital, cession cabinet, bail, financement, SCM, SPFPL et apport de titres ; les zones orange restent visibles via warnings et ne sont pas resolues artificiellement. Ruff OK et pytest OK, 324 tests passes. Prochaine etape recommandee : `FRONT-DOCUMENT-STATUS-LAYER-001`.

FRONT-ADDRESS-MODEL-001 : raffinement du modele global des adresses dans la couche `front_data`. Livrables : `src/sydel_doc_engine/front_data/address_model.py`, enrichissement de `AddressRecord`, mapping canonique adresse et validations dediees, tests `tests/unit/test_front_address_model.py` et rapport `docs/review/front_address_model_001_report_v1.md`. Decisions : les adresses restent typees par usage, `domiciliation = siege_social`, `siege_social = lieu_exercice`, `scm = lieu_exercice`, `cabinet_cede = lieu_exercice` et `locaux_loues = lieu_exercice` sont representes par des regles explicites ; `scm_cedee` et `cessionnaire_scm` restent distinctes par defaut ; les formes affichees derivees des composants doivent etre tracees et les overrides legacy doivent etre justifies. Ruff OK et pytest OK, 313 tests passes. Aucun generateur, moteur DOCX/PDF/ZIP, Streamlit ou UI visible n'a ete modifie.

GLOBAL-FRONT-ARCHITECTURE-QA-001 : controle documentaire de l'architecture front globale V1 sur documents sentinelles `DOC-002`, `DOC-034`, `DOC-017`, `DOC-033`, `DOC-009`, `DOC-041` et `DOC-025`. Livrables : `docs/review/global_front_architecture_qa_001_report_v1.md` et `docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv`. Verdict global : ORANGE maitrisable, avec `DOC-002` et `DOC-033` verts, cinq sentinelles orange et aucun rouge. Decision : le rebuild front peut demarrer par `FRONT-DATA-LAYER-001`, mais les sous-blocs ordre, capital, cession, bail, apport_titres, scm_cession et statuts_civils.associes[] doivent devenir des criteres de couverture data. Aucun generateur, moteur DOCX/PDF/ZIP, Streamlit, UI, Python ou wording juridique n'a ete modifie. Aucun test Python requis car aucun fichier Python modifie.

GLOBAL-FRONT-ARCHITECTURE-001 : conception documentaire de l'architecture produit et donnees du nouveau front global a partir du registre canonique global V2.1. Livrables : `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`, `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`, `docs/project/GLOBAL_FRONT_RULES_V1.md`, `docs/project/GLOBAL_FRONT_SCREEN_STRATEGY_V1.md`, `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md` et `docs/review/global_front_architecture_001_report_v1.md`. Decisions : modele front par objets metier role-based, adresses typees par usage, reutilisation uniquement via regles explicites, distinction dossier / document / lot, parcours dossier complet separe du mode document unitaire. Le prototype actuel est conserve comme bac a sable et outil de diagnostic, mais ne sert pas de fondation produit. Aucun generateur, moteur DOCX/PDF/ZIP, Streamlit ou wording juridique n'a ete modifie. Aucun test Python requis car aucun fichier Python modifie.

GLOBAL-HUMAN-ANSWERS-INTEGRATION-001 : intégration des réponses humaines déjà obtenues dans l'audit global des variables, notamment la réponse d'Albane et le modèle SELAS médecin avec micro-holding. Livrables : `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V2.md`, `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md` et `docs/review/global_human_answers_integration_001_report_v1.md`. Couverture : 10 questions V1 reprises, 4 fermées par arbitrage humain, 5 encore arbitrables en interne, 1 basculée en backlog documentaire futur. Décisions : rôles personne explicitement distincts, trois adresses pivots, domiciliation = siège social, siège = lieu d'exercice seulement via option explicite, SCM = lieu d'exercice en standard, SCM cédée distincte du cessionnaire SCM par défaut, vendeur/cédant = praticien BNC et acquéreur/cessionnaire = SEL en constitution dans le parcours SELARL standard. Cas SELAS médecin + micro-holding documenté comme futur ticket séparé ; contradiction filigrane PROJET documentée mais non implémentée. Aucun générateur, moteur DOCX/PDF/ZIP, UI ou wording juridique n'a été modifié. Aucun test Python requis car aucun fichier Python modifié.

GLOBAL-VARIABLE-IDENTITY-AUDIT-001 : audit d'identité sémantique globale des variables documentaires construit à partir de l'inventaire brut global, des référentiels V1, du registre moteur, des templates et des specs. Livrables : `docs/project/GLOBAL_VARIABLE_IDENTITY_MATRIX_V1.csv`, `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2.md`, `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V1.md` et `docs/review/global_variable_identity_audit_001_report_v1.md`. Couverture : 1 334 slugs normalisés distincts audités, 43 documents `DOC-001` à `DOC-043`, 15 familles, 49 champs canoniques V2 proposés, 142 rapprochements représentatifs classés et 10 questions humaines groupées. Décision : aucune fusion silencieuse ; les relations distinguent identité métier, forme différente, réutilisation explicite, champs distincts et arbitrage humain requis. Aucun générateur, moteur DOCX/PDF/ZIP, UI ou wording juridique n'a été modifié. Aucun test Python requis car aucun fichier Python modifié.

GLOBAL-VARIABLE-INVENTORY-001 : inventaire global brut des variables documentaires construit sur tout le périmètre moteur. Livrables : `docs/project/GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv` et `docs/review/global_variable_inventory_001_report_v1.md`. Le CSV contient 12 443 lignes, 1 334 slugs normalisés distincts sur documents `DOC-XXX`, couvre les 43 documents `DOC-001` à `DOC-043` et 15 familles documentaires. Sources lues/exploitées : dictionnaire canonique V1, mapping documents/variables V1, arbre moteur, `src/sydel_doc_engine/registry/catalog.py`, source truth V1/V2/V3, templates présents dans `project/source_documents/`, specs `docs/delivery/` et `case_catalog.py` en aide. Aucun générateur, moteur DOCX/PDF/ZIP, UI ou wording juridique n'a été modifié. Aucun test Python requis car aucun fichier Python modifié ; validations documentaires : couverture complète, absence de lignes `UNMAPPED`, contrôle CSV/report.

ASSISTANT-METIER-PREFILL-001 : ajout d'un mécanisme de préremplissage de test déterministe dans le seul mode `Assistant metier`. L'UI expose un sélecteur `Scénario de test`, un bouton `Préremplir`, un bouton `Réinitialiser` et une indication visible `Mode test — données fictives préremplies`. Les presets couvrent `SELARL médecin unipersonnelle simple`, `SELARL chirurgien-dentiste + régime communautaire + site distinct`, `SELARL médecin + cession cabinet médical + bail + financement` et `SCI simple`. Le `session_state` Streamlit est synchronisé pour les champs visibles et dérivés, notamment `Dossier unipersonnel`, l'associé unique et la domiciliation = siège. Aucun générateur, moteur DOCX/PDF/ZIP, wording juridique, mode `Technique / diagnostic` ou mode `Document unitaire` n'a été modifié. Rapport : `docs/review/assistant_metier_prefill_001_report_v1.md`. Ruff OK et pytest OK avec 272 tests passés.

DOCUMENT-UNITAIRE-001 : ajout du mode Streamlit `Document unitaire` aux côtés de `Assistant metier` et `Technique / diagnostic`. Le mode permet de choisir un document par code/libellé après sélection du cas, affiche uniquement les champs utiles, propose un préremplissage d'exemple, valide les champs manquants et génère un DOCX unique avec téléchargement, ZIP optionnel et PDF optionnel si le backend local est disponible. Le périmètre V1 est limité à `DOC-001`, `DOC-002`, `DOC-003` et `DOC-004`; les documents manuels restent visibles mais non générables, et les autres documents affichent une limite claire de non-support dans ce mode. Aucun générateur, moteur DOCX/PDF/ZIP, catalogue métier, parcours Assistant métier ou mode `Technique / diagnostic` n'a été modifié. Rapport : `docs/review/document_unitaire_001_report_v1.md`. Ruff OK et pytest OK avec 266 tests passés.

SELARL-CLOUD-GENERATION-BUG-001 : bug de génération SELARL visible reproduit avec `streamlit.testing.v1.AppTest`. Le parcours bloquait quand l'utilisateur cochait `Dossier unipersonnel` ou `L'adresse de domiciliation est le siège social` avant de remplir les champs source : les widgets Streamlit dérivés et désactivés conservaient des valeurs vides en `session_state`, `can_generate_docx` restait faux, `generatable_document_codes` restait vide côté UI et le bouton `Generer les DOCX` restait désactivé. Correction minimale dans `streamlit_app.py` : synchronisation explicite du `session_state` pour l'associé unique dérivé et l'adresse de domiciliation dérivée. Aucun générateur, moteur DOCX/PDF/ZIP, catalogue, parcours SCI ou mode `Technique / diagnostic` n'a été modifié. Rapport : `docs/review/selarl_cloud_generation_bug_001_report_v1.md`. Ruff OK et pytest OK avec 266 tests passés. Commit local tenté mais bloqué par refus d'écriture dans `.git/index.lock` / `.git/objects` dans l'environnement Codex.

SELARL-SMOKE-REALISTIC-001 : smoke réaliste du pilote SELARL après réalignement wording / flow / réutilisations / UI. Trois scénarios ont été exécutés : médecin unipersonnelle simple, chirurgien-dentiste avec régime communautaire et site distinct, médecin avec cession de cabinet médical / bail / financement. Chaque scénario génère uniquement `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004` et un ZIP avec manifeste ; les documents manuels `DOC-013` / `DOC-014` restent visibles mais exclus, `DOC-006` garde sa réserve, les documents non prêts restent en contexte incomplet V2, et le PV d'autorisation d'emprunt reste une option de `DOC-004`. Aucun fichier Python, générateur, moteur DOCX/PDF/ZIP, catalogue ou UI n'a été modifié. Artefacts : `artifacts/selarl_smoke_realistic_001/20260519_185045/`. Rapport : `docs/review/selarl_smoke_realistic_001_report_v1.md`. Backend PDF local indisponible pendant le smoke. Ruff OK et pytest OK avec 257 tests passés.

SELARL-UI-REALIGN-001 : réalignement du parcours Streamlit visible SELARL sur le wording, le flow et les règles de réutilisation corrigés. Le parcours affiche désormais : Écran 1 — Qualification, Écran 2 — Fiche Client, Écran 3 — Fiche Société, Écran 4 — Capital & Associés, Écran 5 — Contexte & scénarios métier, Écran 6 — Documents & génération. `Dossier unipersonnel` est exposé en qualification et verrouille le cas Praticien = associé unique = gérant = signataire. Le mandataire est relégué dans un bloc secondaire replié et n'est pas assimilé au signataire par défaut. `DOC-006` garde sa réserve, `DOC-013` et `DOC-014` restent visibles mais non générables, et l'emprunt reste une option du `DOC-004`. Aucun générateur, moteur DOCX/PDF/ZIP, `case_catalog.py`, parcours SCI ou mode `Technique / diagnostic` n'a été modifié. Rapport : `docs/review/selarl_ui_realign_001_report_v1.md`. Ruff OK et pytest OK avec 257 tests passés.

SELARL-REUSE-RULES-REALIGN-001 : réalignement des règles de réutilisation SELARL dans le schéma et les projections métier. `Dossier unipersonnel` est désormais la règle pivot : quand l'option est active, le Praticien alimente l'associé unique, le gérant et le signataire ; quand elle est inactive, aucune dérivation n'est imposée. Les options SELARL acquéreur, SELARL cessionnaire SCM et domiciliation = siège restent explicites. Le mandataire ne dérive plus du signataire par défaut, les relations vendeur / locataire, siège / lieu d'exercice / cabinet, vendeur / Praticien et cédant SCM / Praticien sont documentées comme non automatiques. Rapport : `docs/review/selarl_reuse_rules_realign_001_report_v1.md`. Aucun générateur, moteur DOCX/PDF/ZIP, `case_catalog.py` ou `streamlit_app.py` n'a été modifié. Ruff OK et pytest OK avec 252 tests passés.

SELARL-FLOW-REALIGN-001 : réalignement de l'ordre conceptuel SELARL dans le schéma et les projections métier. Le flow cible est désormais explicite : Qualification, Fiche Client / Praticien, Fiche Société, Capital & Associés, Contexte & scénarios métier, Documents & génération. `src/sydel_doc_engine/app/selarl_form_schema.py` expose `FormStep`, `SELARL_FLOW_STEPS` et `selarl_blocks_by_step()`, `src/sydel_doc_engine/app/business_wizard.py` expose les projections par étape, les specs actives sont mises à jour in-place et le rapport est `docs/review/selarl_flow_realign_001_report_v1.md`. Aucun générateur, moteur DOCX/PDF/ZIP, `case_catalog.py`, mode SCI ou wording juridique n'a été modifié. `streamlit_app.py` n'a pas été touché ; l'UI visible reste non validée produit et ne doit pas être poussée ou redéployée avant le ticket UI dédié. Ruff OK et pytest OK avec 245 tests passés.

SELARL-WORDING-REALIGN-001 : réalignement du vocabulaire visible SELARL sur les arbitrages associé. L'écran personne visible devient `Fiche Client`, le terme pivot devient `Praticien`, les rôles `Gérant`, `Associé`, `Signataire` et `Mandataire` restent conservés selon contexte, et les specs actives sont mises à jour in-place. Aucun générateur, moteur DOCX/PDF/ZIP, `case_catalog.py`, ordre d'écran ou règle de réutilisation fonctionnelle n'a été modifié. Rapport : `docs/review/selarl_wording_realign_001_report_v1.md`. Ruff OK et pytest OK avec 241 tests passés.

SELARL-PLAN-CORRECTION-001 : correction documentaire de la planification SELARL selon les arbitrages explicites de l'associé. La hiérarchie de sources place désormais les arbitrages associé avant NotebookLM, puis V3, templates/registre et code existant. Le rapport de réconciliation et le backlog ont été resserrés autour de `Fiche Client`, `Praticien` et `Dossier unipersonnel`, avec retrait du mode Projet / filigrane V1, retrait de la couche statut documentaire lourde et sortie du mandataire des priorités UX hors variables ou documents liés. Aucun fichier Python, générateur, moteur DOCX/PDF/ZIP ou UI n'a été modifié ; aucun test code lancé car les modifications sont documentaires.

SELARL-NOTEBOOKLM-RECONCILIATION-001 : réconciliation documentaire du pilote SELARL avec la nouvelle hiérarchie NotebookLM / V3 / templates / code. Les sources validées par l'utilisateur ont été normalisées et committées sous `project/source_truth/notebooklm_selarl_10_prompts_v1.md` et `project/source_truth/Documents_a_generer_par_cas_V3.docx` dans le commit source `f1da08b`. Le ticket crée `docs/project/SELARL_SOURCE_HIERARCHY_V2.md`, `docs/review/selarl_notebooklm_reconciliation_001_report_v1.md` et `docs/project/SELARL_REBUILD_BACKLOG_V2.md`, puis bloque le smoke SELARL prématuré au profit d'une reconstruction contrôlée. Cette reconstruction a été corrigée par `SELARL-PLAN-CORRECTION-001` : wording, flow, réutilisations, UI, smoke réaliste, revue juriste.

SELARL-UI-WIZARD-IMPL-001 : branchement du mode `Assistant metier` Streamlit sur le schema machine-readable SELARL, ajout d'un parcours pilote en ecrans qualification / societe / personne et gerant / associes / conditions specifiques / documents attendus / generation, consommation des labels, blocs, regles de reutilisation et documents issus de `src/sydel_doc_engine/app/selarl_form_schema.py` via `business_wizard.py`, conservation du mode SCI et du mode `Technique / diagnostic`, affichage de `DOC-006` avec reserve source V2, `DOC-013` et `DOC-014` visibles mais `MANUAL_ONLY` et exclus de la generation, rapport `docs/review/selarl_ui_wizard_impl_001_report_v1.md`, ruff OK et pytest OK avec 239 tests passes. Ce parcours est techniquement committe, mais pas valide produit.

SELARL-FORM-SCHEMA-IMPL-001 : implémentation du schéma de données SELARL côté Assistant métier depuis la vraie source V2 `project/source_truth/Documents_a_generer_par_cas_V2.docx`, ajout de `src/sydel_doc_engine/app/selarl_form_schema.py`, couverture machine-readable des blocs métier, champs qualifiés, règles de réutilisation, documents attendus et variables V2, ajout de la réserve source V2 exploitable sur `DOC-006`, clarification finale de `DOC-013` / `DOC-014` comme `MANUAL_ONLY` hors génération pilote, rapport `docs/review/selarl_form_schema_impl_001_report_v1.md`, ruff OK et pytest OK avec 231 tests passés.

SELARL-PILOT-SOURCE-VERIFY-001 : vérification des livrables SELARL contre la vraie source V2 de l'associé `project/source_truth/Documents_a_generer_par_cas_V2.docx` hash SHA-256 `2E9843AA1EC05A01D82DF5FCE12516A8EF49EA2B3842547D186204218C90B23F`, remplacement du fichier V2 canonique provisoire, création du rapport `docs/review/selarl_source_verify_001_report_v1.md`, correction des statuts de dérogation SELARL dans le catalogue (`DOC-013` et `DOC-014` hors génération pilote), enrichissement des specs SELARL avec les variables V2 brutes et réserves source ; ruff OK et pytest OK avec 217 tests passés.

SELARL-PILOT-PROTOCOL-001 : cadrage produit du pilote SELARL depuis `project/source_truth/Documents_a_generer_par_cas_V2.docx`, création du protocole réplicable de construction de processus, des specs SELARL processus/formulaire/wizard, du plan d'implémentation et du rapport `docs/review/selarl_pilot_protocol_001_report_v1.md`, sans modification de l'UI, du moteur DOCX/PDF/ZIP ni des générateurs ; ruff OK et pytest OK avec 217 tests passés.

UI-CASE-WIZARD-002 : branchement du mode Assistant metier Streamlit sur `get_expected_documents(...)` et CASE-CATALOG-001, ajout des conditions UI pour les 8 familles, affichage des documents attendus avec statuts generable / manuel / non implemente / mapping / contexte incomplet V2, filtrage de la generation sur les seuls documents attendus generables avec `DOC-XXX` et contexte pret, mode Technique / diagnostic conserve, rapport `docs/review/ui_case_wizard_002_report_v1.md`, ruff OK et pytest OK avec 217 tests passes.

CASE-CATALOG-001 : creation de la couche metier catalogue des cas depuis `project/source_truth/Documents_a_generer_par_cas.docx`, ajout de `src/sydel_doc_engine/domain/case_catalog.py` avec `get_expected_documents(...)`, 46 documents attendus uniques modelises dont 43 mappes au registre `DOC-001` a `DOC-043`, 2 documents manuels, 1 document non implemente, rapport `docs/review/case_catalog_001_report_v1.md`, ruff OK et pytest OK avec 208 tests passes.

DEPLOY-STREAMLIT-CLOUD-FIX-001 : correction de packaging Streamlit Cloud depuis le dossier canonique `C:\Users\Gad\Desktop\Sydel\sydel-document-engine`, ajout de la declaration Poetry explicite `{ include = "sydel_doc_engine", from = "src" }` dans `pyproject.toml`, rapport `docs/review/deploy_streamlit_cloud_fix_001_report_v1.md`, installation editable OK, ruff OK et pytest OK avec 196 tests passes ; Poetry local indisponible, donc `poetry check` et `poetry install` non executes localement.

UI-BUSINESS-WIZARD-001 : mode Assistant metier Streamlit ajoute depuis le dossier canonique `C:\Users\Gad\Desktop\Sydel\sydel-document-engine`, formulaire SCI simple pour `DOC-001` a `DOC-004`, validation champs manquants/incoherences, boutons DOCX/ZIP/PDF, telechargements, mode technique YAML/JSON conserve et rapport `docs/review/ui_business_wizard_001_report_v1.md` ajoute.

REVIEW-FINAL-001 : revue finale executee depuis le dossier canonique `C:\Users\Gad\Desktop\Sydel\sydel-document-engine`, rapport ajoute dans `docs/review/review_final_001_execution_report_v1.md`, ruff/pytest verts, smoke DOCX/ZIP OK sur `lot_02_orchestrator_positive_example.yaml`, backend PDF local indisponible pendant la revue et decision GO avec reserves pour `UI-BUSINESS-WIZARD-001`.

WORKTREE-CLEANUP-AND-UI-STATUS-001 : consolidation du contenu restant de `codex/review-final-001` dans `main`, creation du rapport `docs/project/23_WORKTREE_CLEANUP_AND_UI_STATUS_V1.md`, clarification du dossier canonique final et archivage local prevu des anciens worktrees `sydel-document-engine-*`.

SYNC-FINAL-FOUNDATIONS-001 : synchronisation finale de `main` avant revue/cloture, absorption des complements UI/PDF/ZIP manquants, confirmation des audits/fondations presents, remplacement de `UI-CORE-001` par `UI-PDF-ZIP-INTEGRATION-001` et pilotage final limite a `REVIEW-FINAL-001` puis `CLOSE-PROJECT-V1-001`.

UI-PDF-ZIP-INTEGRATION-001 : integration de l'UI Streamlit avec la generation dossier DOCX, l'export PDF local optionnel et le ZIP dossier, avec telechargements par fichier, smoke manuel documente et validations locales vertes.

SYNC-POST-MOTOR-UI-001 : absorption dans `main` des fondations UI/PDF/recette issues des branches `codex/ui-flow-001`, `codex/ui-occurrences-001`, `codex/ui-form-schema-001`, `codex/pdf-backend-001` et `codex/recipe-frame-001`, puis réalignement du pilotage vers `UI-CORE-001`, `RESUME-ZIP-BACKEND-001` et `REVIEW-FINAL-001`.

PDF-BACKEND-001 : implementation d'un backend local d'export PDF depuis DOCX genere, avec priorite LibreOffice headless si disponible puis fallback Word COM Windows, erreurs explicites, tests ciblés, smoke réel DOCX vers PDF et aucune modification UI.

RECONCILE-MOTOR-CLOSE-001 : reconciliation finale du moteur DOCX V1, exposition des generateurs ordre/SPFPL sous `DOC-034` a `DOC-043`, consolidation des referentiels `08/09`, integration des audits `17/18`, requalification de l'audit `16`, validations ruff/pytest et cloture moteur hors UI/PDF/ZIP/recette finale.

SYNC-CLOSE-AUDIT-001 : absorption dans `main` du commit source `0139202b170531fd628f25811c55855a2512acc0` depuis `origin/codex/close-motor-audit-001`, confirmation de `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` et conservation de la version finale plus récente déjà présente dans `main`, sans modification de code Python.

FINAL-SCM-CESSION-WAVE-001 : restauration de la résolution V1 cession SCM depuis la branche d'arbitrage, implémentation du bloc cession SCM sous `DOC-031` à `DOC-033`, smoke DOCX réel, validations ruff/pytest et audit de clôture moteur V1.

SYNC-WAVE-010 : absorption finale dans `main` des branches `codex/arbitrage-scm-cession-resolve-001` et `codex/code-scm-cession-block-001`, passage en DONE des tickets SCM cession finaux et réalignement du pilotage vers UI, PDF, ZIP et recette finale.

SYNC-WAVE-009 : absorption dans `main` des commits sources `4288837648d099935d6c57307003f3b33d038d90`, `af1020a165d11e830428394e02a5baca4a110f5c`, `81f7a7e407002428d8fce1ce31d16f3a798bd2e5`, `fa3cb65ffd1055bbf16ba3a5352f4a7d5deb713a` et `bdf61166b0770c5ab8f3610f48d89e5cdcb3f582`, puis réalignement du pilotage.

SYNC-WAVE-008 : absorption dans `main` des branches acte actions, sources SCM cession, reviews Lot 03/Lot 04, audit restant, analyses style Lot 03/statuts et specs blocage cession SCM, puis réalignement du pilotage.

SYNC-WAVE-007 : absorption dans `main` des branches SCM et acte actions, passage en DONE des tickets absorbés et réalignement du pilotage.

SYNC-WAVE-006 : absorption dans `main` des branches tardives Lot 04 / Lot 05, passage en DONE des tickets absorbés et réalignement du pilotage.

CONVERT-ACTE-ACTIONS-001 : conversion du candidat legacy `Acte_cession_SPFPL_tiers_modele.doc` en DOCX exploitable, placement dans `project/source_documents/lot_05/` et documentation de préparation V1.

CONVERT-DEROG-SALARIEE-001 : tentative de conversion Word COM du `.doc` legacy salariee, aucun DOCX exploitable produit, blocage documente.

SYNC-WAVE-005 : absorption dans `main` des commits sources `91436f0916fdecbcc98450b72ba6e602cb8f1a3b`, `1b3ba14d0bcc31fc7dcbf1752d6d3263645ae8b3`, `32059155c618b4e985893f42ef2817187599c281`, `74d41db53543b790e197082e8b9c713f7de92dc2` et `d1d649e11fdc638e6d7da0640c154d1f213739ee`, puis réalignement du pilotage.

## État courant du repo
- Le clean front Track B dispose maintenant d'un sous-cas `SELARL dentiste multi-associes simple (PARTIAL statuts)` : plusieurs associes, repartition simple des parts, president choisi parmi eux, gerant unique et unanimite totale. Ce mode genere `DOC-004` et `DOC-016`; `DOC-016` est PARTIAL et couvre les apports/capital/repartition/signatures associes, sans revendiquer le lock complet de la comparution plurielle.
- Le clean front Track B dispose maintenant d'un sous-cas `DOC-004` multi-associes limite : plusieurs associes pour le PV, president choisi parmi eux, gerant unique et unanimite totale. Ce mode genere uniquement `DOC-004` et ne couvre pas les statuts multi-associes, plusieurs gerants, cession, SCM, regime communautaire ou votes non unanimes.
- Le contrat source SELARL multi-associes est disponible : `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md`. Il autorisait initialement seulement un sous-cas borne `DOC-004`; le ticket 008 ouvre ensuite un delta limite `DOC-016` dentiste PARTIAL. Plusieurs gerants, president externe, cession medicale/dentaire et cession SCM restent bloques dans ce contrat.
- Track B dispose maintenant d'un front propre `src/sydel_doc_engine/front_app/` qui branche une vraie slice SELARL V1 bornee. Le point d'entree reste `src/sydel_doc_engine/front_app/app.py`.
- La slice clean construit un `DocumentGenerationContext` moteur depuis le contrat SELARL V1, selectionne strictement les codes autorises, produit les DOCX puis le ZIP, et n'importe pas les anciens ecrans `business_wizard`, `single_document_mode` ou `streamlit_app`.
- Surface visible : type de dossier, donnees a saisir et generation. Les cas hors perimetre restent visibles comme blocages honnetes ; `DOC-006` est genere uniquement si le regime communautaire est actif.
- Validations cibles historiques : `pytest tests/unit/test_clean_front_app.py` OK, 10 tests passes ; `ruff check src/sydel_doc_engine/front_app tests/unit/test_clean_front_app.py` OK.
- Ticket suivant recommande a date : `SELARL-FINAL-ASSOCIE-VALIDATION-001`, sauf choix explicite d'un sous-cas avec `GO dev`.
- L'architecture du nouveau front global est disponible : `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`, `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`, `docs/project/GLOBAL_FRONT_RULES_V1.md`, `docs/project/GLOBAL_FRONT_SCREEN_STRATEGY_V1.md`, `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md` et `docs/review/global_front_architecture_001_report_v1.md`.
- Le shell UI du nouveau front global est disponible dans `src/sydel_doc_engine/app/front_shell.py` et branche dans `src/sydel_doc_engine/app/streamlit_app.py`. Depuis `FRONT-MINIMAL-SURFACE-CLEANUP-001`, la vue normale affiche uniquement `Type de dossier`, `Donnees a saisir` et `Generation`, sans radio, table, expander ou outil interne visible.
- L'editeur dossier V1 du nouveau front global est disponible dans la zone `Dossier` du shell. Le profil visible reste unique cote utilisateur, mais la saisie SELARL couvre maintenant profession, conditions dossier, ordre, mandataire, statuts SEL, depot des fonds, regime communautaire et conjoint.
- Les actions de generation du nouveau front ne sont plus limitees a `DOC-001` a `DOC-004` : SELARL medecin simple genere `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034` et `DOC-017`; SELARL chirurgien-dentiste bascule vers `DOC-016`; regime communautaire ajoute `DOC-005` et `DOC-006`. En surface normale, le PDF reste cache lorsque le backend local est indisponible. `DOC-013`, `DOC-014` et les documents sans code restent exclus/manuels.
- Les scenarios cession medicale/dentaire et cession SCM sont selectionnes depuis le catalogue, mais leurs documents restent `context_incomplete`. Aucun sous-formulaire complexe ne doit demarrer sans gate produit et decision `GO dev`.
- Audit `FRONT-STATE-AUDIT-001` : constat historique de limitation a quatre documents sur l'ancien etat du front ; le statut courant SELARL est desormais consolide dans `docs/project/SELARL_CANONICAL_STATUS_V1.md`.
- Cleanup `FRONT-MINIMAL-SURFACE-CLEANUP-001` : les outils internes sont caches par mode equipe (`SYDEL_ENABLE_INTERNAL_TOOLS=1` ou flag de session interne), les expanders visibles sont supprimes et les blocages data-layer/runtime sont affiches dans `Generation`.
- Le jalon `SELARL-CANONICAL-STATUS-001` est DONE ; le prochain jalon recommande est `SELARL-FINAL-ASSOCIE-VALIDATION-001` avant nouveau developpement complexe.
- Le registre canonique global V2.1 est disponible : `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`. Il intègre les arbitrages humains sur les rôles, les adresses et les parties de cession, et il est suffisamment stable pour lancer l'architecture du nouveau front global.
- La matrice courte des questions humaines V2 est disponible : `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V2.md`. Aucune relance client n'est requise pour le gel V2.1 ; les sujets restants sont à arbitrer en interne ou à remettre en backlog documentaire.
- L'audit d'identité sémantique global V2 est disponible : matrice `docs/project/GLOBAL_VARIABLE_IDENTITY_MATRIX_V1.csv`, registre `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2.md`, questions humaines `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V1.md` et rapport `docs/review/global_variable_identity_audit_001_report_v1.md`. Il couvre tout `DOC-001` à `DOC-043` et prépare l'arbitrage humain avant rebuild front.
- L'inventaire global brut des variables documentaires V1 est disponible dans `docs/project/GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv` avec son rapport exécutif dans `docs/review/global_variable_inventory_001_report_v1.md`; il prépare un audit sémantique V2 avant reconstruction globale du front.
- DOC-001, DOC-002 et DOC-003 disposent chacun d'un générateur dédié déjà terminé.
- L'orchestrateur dossier expose :
  - un registre des générateurs DOC-001 à DOC-043 ;
  - `select_documents(structure)` selon le catalogue ;
  - `select_documents_for_context(ctx)` avec filtrage des batchs regime communautaire, bail/appel de fonds, cession cabinets, derogations, statuts, SPFPL, SCM satellites et cession SCM ;
  - `generate_documents(ctx, output_dir) -> list[Path]`.
- Le moteur documentaire DOCX V1 est feature complete et clos sur le perimetre deterministe valide, hors cas explicitement manuels ou legacy et hors UI/PDF/ZIP/recette finale.
- Le backend PDF V1 est disponible dans `src/sydel_doc_engine/rendering/pdf_export.py` : export unitaire DOCX vers PDF, export batch de chemins DOCX, detection de backend, erreurs bloquantes si aucun convertisseur fiable n'est disponible.
- Le backend ZIP V1 est disponible dans `src/sydel_doc_engine/rendering/zip_bundle.py` : ZIP deterministe DOCX/PDF, chemins relatifs, filtrage des fichiers temporaires et manifeste `manifest.json`.
- Strategie PDF locale retenue apres smoke : LibreOffice headless prioritaire si present ; Word COM Windows utilise localement avec succes. LibreOffice n'est pas installe sur la machine de smoke.
- L'UI Streamlit dispose maintenant de trois modes :
  - `Assistant metier` : selection documentaire pilotee par `get_expected_documents(...)`, conditions metier par famille CASE-CATALOG-001, parcours SELARL pilote branche sur le schema `selarl_form_schema.py`, tableau des documents attendus incluant manuels/non implementes/reserves, generation DOCX filtree sur les documents generables et prets, ZIP avec manifest, PDF local optionnel, telechargements et presets fictifs deterministes de test ;
  - `Technique / diagnostic` : chargement YAML/JSON, selection `select_documents_for_context`, generation dossier DOCX/PDF optionnel/ZIP et telechargements existants ;
  - `Document unitaire` : choix d'un document supporte, champs limites au document, generation DOCX unique, ZIP/PDF optionnels.
- La couche metier catalogue des cas est disponible dans `src/sydel_doc_engine/domain/case_catalog.py` : elle expose `CaseType`, `CaseCondition`, `DocumentOccurrence`, `DocumentAvailability`, `ExpectedDocument` et `get_expected_documents(...)`.
- Le catalogue metier couvre 8 familles, 104 occurrences source et 46 documents attendus uniques : 43 documents restent mappes a un `DOC-XXX`, mais après vérification de la vraie V2 SELARL seuls 41 sont `GENERATABLE`, 4 sont `MANUAL_ONLY`, 1 est `NOT_IMPLEMENTED`, 0 `NEEDS_MAPPING`.
- La vraie source V2 du cadrage produit SELARL est disponible dans `project/source_truth/Documents_a_generer_par_cas_V2.docx` avec hash SHA-256 `2E9843AA1EC05A01D82DF5FCE12516A8EF49EA2B3842547D186204218C90B23F`.
- Les nouvelles sources SELARL validées pour la réconciliation NotebookLM sont disponibles :
  - `project/source_truth/notebooklm_selarl_10_prompts_v1.md` ;
  - `project/source_truth/Documents_a_generer_par_cas_V3.docx`.
- La hiérarchie de sources SELARL V2 corrigée est disponible dans `docs/project/SELARL_SOURCE_HIERARCHY_V2.md` : arbitrages associé, NotebookLM, V3, templates/registre, code existant.
- Le rapport d'écarts NotebookLM / V3 / code corrigé est disponible dans `docs/review/selarl_notebooklm_reconciliation_001_report_v1.md`.
- Le backlog de reconstruction contrôlée SELARL V2 corrigé est disponible dans `docs/project/SELARL_REBUILD_BACKLOG_V2.md`.
- `SELARL-DOCS-GENERATION-SMOKE-001` est bloqué et remplacé par `SELARL-SMOKE-REALISTIC-001` après réalignement wording / flow / règles de réutilisation / UI.
- `SELARL-WORDING-REALIGN-001` est DONE.
- `SELARL-FLOW-REALIGN-001` est DONE.
- `SELARL-REUSE-RULES-REALIGN-001` est DONE.
- `SELARL-UI-REALIGN-001` est DONE.
- `SELARL-SMOKE-REALISTIC-001` est DONE ; le scope a ete consolide par `SELARL-CANONICAL-STATUS-001`, et `SELARL-FINAL-ASSOCIE-VALIDATION-001` est le prochain ticket recommande.
- `SELARL-CLOUD-GENERATION-BUG-001` est DONE ; le parcours visible SELARL resynchronise désormais les champs dérivés de l'associé unique et de la domiciliation avant génération.
- Le protocole réplicable de construction de processus est disponible dans `docs/project/PROCESS_BUILD_PROTOCOL_V1.md`.
- Les specs SELARL pilote sont disponibles :
  - `docs/project/SELARL_PROCESS_SPEC_V1.md` ;
  - `docs/project/SELARL_FORM_SCHEMA_V1.md` ;
  - `docs/project/SELARL_UI_WIZARD_SPEC_V1.md` ;
  - `docs/project/SELARL_IMPLEMENTATION_PLAN_V1.md`.
- Le schéma de données SELARL côté Assistant métier est disponible dans `src/sydel_doc_engine/app/selarl_form_schema.py` : blocs métier, champs UI qualifiés, règles de réutilisation, documents attendus, codes générables et couverture des variables V2.
- Le parcours UI SELARL pilote est disponible dans `src/sydel_doc_engine/app/streamlit_app.py` et consomme le schema via `src/sydel_doc_engine/app/business_wizard.py`, mais il n'est pas encore validé produit ; ne pas pousser ni redéployer avant réalignement wording / flow / réutilisation / UI.
- `DOC-006` porte désormais une réserve source V2 exploitable depuis `case_catalog.py`; `DOC-013` et `DOC-014` restent visibles mais `MANUAL_ONLY` et exclus des codes générables SELARL.
- Le smoke manuel UI/PDF/ZIP est documente dans `docs/review/ui_pdf_zip_integration_001_smoke.md`.
- `examples/contexts/lot_01_example.yaml` utilise encore le champ legacy Lot 1 `adresse_domiciliation_affichee`, en attente d'un refactor dédié vers `domiciliation.adresse_affichee`.
- Un smoke test réel a généré les trois DOCX du Lot 1 dans `artifacts/lot_01_smoke_test/`.
- Le moteur dispose de trois référentiels de cadrage :
  - arbre documentaire document-centré V1 : `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md` ;
  - dictionnaire canonique des variables V1 : `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md` ;
  - table de mapping document -> variables canoniques V1 : `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.
- Les audits/fondations finaux sont disponibles :
  - `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` ;
  - `docs/project/17_FINAL_ENGINE_QUALITY_AUDIT_V1.md` ;
  - `docs/project/18_NEXT_PHASE_FOUNDATION_V1.md` ;
  - `docs/project/19_UI_FLOW_V1.md` ;
  - `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md` ;
  - `docs/project/21_UI_FORM_SCHEMA_V1.md`.
- Le framework de recette finale V1 est disponible dans `docs/review/final_recipe_framework_v1.md`.
- Le pack de revue finale V1 est disponible dans `docs/review/final_review_pack_v1.md`.
- Le rapport d'execution `REVIEW-FINAL-001` est disponible dans `docs/review/review_final_001_execution_report_v1.md`.
- Le rapport d'execution `UI-BUSINESS-WIZARD-001` est disponible dans `docs/review/ui_business_wizard_001_report_v1.md`.
- Le rapport d'execution `DEPLOY-STREAMLIT-CLOUD-FIX-001` est disponible dans `docs/review/deploy_streamlit_cloud_fix_001_report_v1.md`.
- Le rapport d'execution `CASE-CATALOG-001` est disponible dans `docs/review/case_catalog_001_report_v1.md`.
- Le rapport d'execution `UI-CASE-WIZARD-002` est disponible dans `docs/review/ui_case_wizard_002_report_v1.md`.
- Le rapport d'execution `SELARL-PILOT-PROTOCOL-001` est disponible dans `docs/review/selarl_pilot_protocol_001_report_v1.md`.
- Le rapport d'execution `SELARL-PILOT-SOURCE-VERIFY-001` est disponible dans `docs/review/selarl_source_verify_001_report_v1.md`.
- Le rapport d'execution `SELARL-FORM-SCHEMA-IMPL-001` est disponible dans `docs/review/selarl_form_schema_impl_001_report_v1.md`.
- Le rapport d'execution `SELARL-UI-WIZARD-IMPL-001` est disponible dans `docs/review/selarl_ui_wizard_impl_001_report_v1.md`.
- `pyproject.toml` declare explicitement le package Poetry `sydel_doc_engine` depuis `src`, pour eviter l'erreur Streamlit Cloud `No file/folder found for package sydel-document-engine`.
- Le rapport de cleanup local et statut UI est disponible dans `docs/project/23_WORKTREE_CLEANUP_AND_UI_STATUS_V1.md`.
- Le dossier canonique final a utiliser est `C:\Users\Gad\Desktop\Sydel\sydel-document-engine`.
- Les anciens worktrees locaux sont archives sous `C:\Users\Gad\Desktop\Sydel\_codex_worktrees_archive`.
- `UI-CORE-001` est superseded / remplace par `UI-PDF-ZIP-INTEGRATION-001`.
- `RESUME-ZIP-BACKEND-001` est DONE.
- `REVIEW-FINAL-001` est DONE avec decision GO avec reserves.
- `UI-BUSINESS-WIZARD-001` est DONE avec perimetre assistant SCI simple.
- `CASE-CATALOG-001` est DONE ; il n'a pas modifie l'UI, le moteur DOCX/PDF/ZIP ni les generateurs.
- `UI-CASE-WIZARD-002` est DONE ; l'assistant metier est maintenant pilote par le catalogue des cas, avec generation partielle honnete et documents manuels/non implementes visibles.
- `SELARL-PILOT-PROTOCOL-001` est DONE ; il n'a pas modifié l'UI, le moteur DOCX/PDF/ZIP ni les générateurs.
- `SELARL-PILOT-SOURCE-VERIFY-001` est DONE ; il n'a pas modifié l'UI, le moteur DOCX/PDF/ZIP ni les générateurs, mais il a aligné le catalogue produit SELARL sur la vraie V2.
- `SELARL-FORM-SCHEMA-IMPL-001` est DONE ; il n'a pas modifié l'UI visible, le moteur DOCX/PDF/ZIP ni les générateurs.
- `SELARL-UI-WIZARD-IMPL-001` est DONE techniquement ; il n'a pas modifié les générateurs ni le moteur DOCX/PDF/ZIP et conserve SCI ainsi que le mode Technique / diagnostic, mais il n'est pas validé produit.
- `SELARL-PLAN-CORRECTION-001` est DONE ; la séquence SELARL cible est `WORDING -> FLOW -> REUSE -> UI -> SMOKE -> JURIST`.
- `SELARL-WORDING-REALIGN-001` est DONE ; le vocabulaire visible est réaligné, sans changement de flow ni de génération.
- `SELARL-FLOW-REALIGN-001` est DONE ; le flow conceptuel est réaligné dans le schéma et les projections métier, sans refonte Streamlit visible.
- `SELARL-REUSE-RULES-REALIGN-001` est DONE ; `Dossier unipersonnel` et les options explicites sont dans le schéma et les projections métier, sans refonte Streamlit visible.
- `SELARL-UI-REALIGN-001` est DONE ; le rendu Streamlit SELARL visible suit le flow, expose `Dossier unipersonnel` et conserve le mandataire secondaire.
- Ticket SELARL en cours : `SELARL-FINAL-ASSOCIE-VALIDATION-001`; autres tickets prets hors SELARL : `GLOBAL-CANONICAL-V2-ARBITRATION-001`, `CLOSE-PROJECT-V1-001`.
- Le cadrage métier de la famille `PV nomination gérant` est disponible dans `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`.
- La spec canonique V1 de la famille `PV nomination gérant` est disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.
- La spec texte V1 de la famille `PV nomination gérant` est disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.
- `SPEC-PV-001` est DONE.
- `SPEC-TEXTE-PV-001` est DONE.
- `CODE-PV-001` est DONE.
- `REVIEW-PV-001` est DONE.
- `SPEC-RENDER-001` est DONE.
- `RENDER-STYLE-001` est DONE.
- Le générateur PV nomination gérant est disponible dans `src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py`.
- Un contexte exemple de smoke test est disponible dans `examples/contexts/lot_02_pv_nomination_gerant_example.yaml`.
- Le pack de revue humaine est disponible dans `docs/review/lot_02_pv_nomination_gerant_review_v1.md`.
- L'aperçu texte extrait est disponible dans `docs/review/lot_02_pv_nomination_gerant_preview_v1.txt`.
- La spec technique V1 de couche de rendu DOCX commune est disponible dans `docs/delivery/render_style_system_v1.md`.
- Le blueprint de style batch V1 est disponible dans `docs/delivery/render_style_blueprint_batch_v1.md`.
- Le modèle de données supporte désormais les rôles canoniques nécessaires au PV :
  - `associes[]` ;
  - `dirigeant_nomine` ;
  - `decision` ;
  - `reunion` ;
  - `capital` ;
  - `emprunt` ;
  - `bien_immobilier`.
- Le modèle de données supporte désormais les rôles nécessaires à la demande d'inscription à l'ordre :
  - `dossier_options.derogation` ;
  - `personne_signataire.titre_affichage` ;
  - `personne_signataire.adresse_personnelle_affichee` ;
  - `ordre` ;
  - `mandataire`.
- Le modèle de données supporte désormais le batch régime communautaire :
  - `dossier_options.regime_communautaire` ;
  - `conjoint` ;
  - `apport` ;
  - `regime_communautaire.avertissement` ;
  - `regime_communautaire.renonciation`.
- Le modèle de données supporte désormais le mini-batch bail / appel de fonds :
  - `dossier_options.cession` ;
  - `bail` ;
  - `cession.cabinet` ;
  - `cession.financement` ;
  - `cession.vendeur` ;
  - `cession.acquereur`.
- Le PV nomination gérant est branché dans l'orchestrateur pour SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI et SCM.
- Le PV nomination gérant est exclu de la sélection SAS.
- FIX-PV-RENDER-001 est terminé : le PV dispose désormais d'un titre principal encadré, de listes à tirets pour les associés et les décisions, d'intertitres gras/soulignés, de formules de vote en italique et de signatures centrées.
- Deux contextes exemples d'orchestration Lot 2 sont disponibles :
  - `examples/contexts/lot_02_orchestrator_positive_example.yaml`
  - `examples/contexts/lot_02_orchestrator_negative_sas_example.yaml`
- Le smoke orchestrateur Lot 2 a généré les dossiers DOCX attendus :
  - `artifacts/lot_02_orchestrator_positive_smoke_test/`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/`
- La revue smoke orchestrateur Lot 2 est disponible : `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- Le cadrage V1 de la demande d'inscription à l'ordre est disponible : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`.
- La spec canonique V1 de la demande d'inscription à l'ordre est disponible : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`.
- La spec texte V1 de la demande d'inscription à l'ordre est disponible : `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.
- Le cadrage V1 du batch régime communautaire est disponible : `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- La spec canonique V1 du batch régime communautaire est disponible : `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md`.
- La spec texte V1 du batch régime communautaire est disponible : `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`.
- Les générateurs du batch régime communautaire sont disponibles :
  - `src/sydel_doc_engine/generators/lot_02/lettre_renonciation_associe.py` ;
  - `src/sydel_doc_engine/generators/lot_02/lettre_avertissement_conjoint.py`.
- Un contexte exemple de smoke test est disponible : `examples/contexts/lot_02_regime_communautaire_example.yaml`.
- La spec canonique V1 du batch SPFPL spécifique est disponible : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`.
- La spec texte V1 du batch SPFPL spécifique est disponible : `docs/delivery/lot_05_spfpl_spec_texte_v1.md`.
- Les arbitrages V1 du batch SPFPL spécifique sont disponibles : `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.
- Le sous-batch SPFPL agrément / note d'information est codé et testé :
  - `src/sydel_doc_engine/generators/lot_05/note_information.py` ;
  - `src/sydel_doc_engine/generators/lot_05/pv_agrement_cession_spfpl_associe_unique.py` ;
  - `src/sydel_doc_engine/generators/lot_05/pv_agrement_cession_spfpl_plusieurs_associes.py`.
- Un contexte exemple SPFPL agrément / note d'information est disponible : `examples/contexts/lot_05_spfpl_agrement_info_example.yaml`.
- Le cœur SPFPL restant est codé et testé :
  - `src/sydel_doc_engine/generators/lot_05/acte_cession_parts_spfpl.py` ;
  - `src/sydel_doc_engine/generators/lot_05/contrat_apport_spfpl.py` ;
  - `src/sydel_doc_engine/generators/lot_05/attestation_capital_liste_souscripteurs.py` ;
  - `src/sydel_doc_engine/generators/lot_05/attestation_commissaire_apports.py`.
- Un contexte exemple SPFPL cœur est disponible : `examples/contexts/lot_05_spfpl_core_example.yaml`.
- La spec canonique V1 de la famille dérogations est disponible : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`.
- La spec texte V1 de la famille dérogations est disponible : `docs/delivery/lot_03_derogations_spec_texte_v1.md`.
- Les arbitrages V1 de la famille dérogations sont disponibles : `docs/delivery/lot_03_derogations_arbitrages_v1.md`.
- La préparation sources dérogations V1 est disponible :
  - `docs/delivery/lot_03_derogations_preparation_v1.md` ;
  - `docs/delivery/lot_03_derogations_legacy_conversion_report_v1.md`.
- La spec canonique V1 `cession cabinets` est disponible : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`.
- La spec texte V1 `cession cabinets` est disponible : `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.
- Les arbitrages V1 `cession cabinets` sont disponibles : `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`.
- La spec canonique V1 `bail / appel de fonds` est disponible : `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`.
- La spec texte V1 `bail / appel de fonds` est disponible : `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`.
- Les générateurs du mini-batch bail / appel de fonds sont disponibles :
  - `src/sydel_doc_engine/generators/lot_03/avenant_contrat_bail.py` ;
  - `src/sydel_doc_engine/generators/lot_03/appel_fond_sel.py`.
- Le catalogue et l'orchestrateur exposent désormais :
  - `DOC-007` : avenant au contrat de bail ;
  - `DOC-008` : appel de fonds SEL.
- Un contexte exemple du mini-batch bail / appel de fonds est disponible : `examples/contexts/lot_03_bail_appel_fonds_example.yaml`.
- Les générateurs cession cabinets sont disponibles :
  - `src/sydel_doc_engine/generators/lot_03/acte_cession_cabinet_medical.py` ;
  - `src/sydel_doc_engine/generators/lot_03/compromis_cession_cabinet_medical.py` ;
  - `src/sydel_doc_engine/generators/lot_03/acte_cession_cabinet_dentaire.py` ;
  - `src/sydel_doc_engine/generators/lot_03/compromis_cession_cabinet_dentaire.py`.
- Le catalogue et l'orchestrateur exposent désormais :
  - `DOC-009` : acte de cession d'un cabinet médical ;
  - `DOC-010` : compromis de cession d'un cabinet médical ;
  - `DOC-011` : acte de cession d'un cabinet dentaire ;
  - `DOC-012` : compromis de cession d'un cabinet dentaire.
- Un contexte exemple cession cabinets est disponible : `examples/contexts/lot_03_cession_cabinets_example.yaml`.
- Le manifest d'import sources V1 est disponible : `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md`.
- Le rapport de doublons sources V1 est disponible : `docs/project/11_SOURCE_DUPLICATES_REPORT_V1.md`.
- Le plan de placement sources V1 est disponible : `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`.
- Les décisions d'arbitrage sources V1 sont disponibles : `docs/project/13_SOURCE_ARBITRATION_DECISIONS_V1.md`.
- Le journal d'exécution du placement HIGH V1 est disponible : `docs/project/14_SOURCE_PLACEMENT_EXECUTION_V1.md`.
- La préparation V1 des sources statuts est disponible : `docs/delivery/lot_04_statuts_preparation_v1.md`.
- Les specs V1 des statuts SAS sont disponibles :
  - `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md` ;
  - `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`.
- Les specs V1 des statuts SPFPL sont disponibles :
  - `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md` ;
  - `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`.
- Les specs V1 des statuts SEL d'exercice sont disponibles :
  - `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` ;
  - `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.
- Les specs V1 des statuts civils sont disponibles :
  - `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` ;
  - `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.
- Le générateur statuts SAS V1 est disponible dans `src/sydel_doc_engine/generators/lot_04/statuts_sas.py`.
- Les générateurs statuts civils V1 sont disponibles :
  - `src/sydel_doc_engine/generators/lot_04/statuts_scs.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_sci.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_sci_iris.py`.
- Le modèle de données supporte désormais `statuts_civils` pour SCS, SCI et SCI IRIS : associés dynamiques, apports, parts, dépôt de capital et groupes de résultat exceptionnel SCI IRIS.
- Le générateur statuts SCM V1 est disponible dans `src/sydel_doc_engine/generators/lot_04/statuts_scm.py` et branché sous `DOC-025`.
- Les générateurs statuts SPFPL V1 sont disponibles :
  - `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_cession.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_apport.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_common.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_templates.py`.
- Les générateurs statuts SEL d'exercice V1 sont disponibles :
  - `src/sydel_doc_engine/generators/lot_04/statuts_selarl_dentiste.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_selarl_medecin.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_selas_medecin.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_sel_exercice_common.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_sel_exercice_templates.py`.
- Les arbitrages V1 des statuts SEL d'exercice sont disponibles dans `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`.
- Les arbitrages V1 des statuts civils sont disponibles dans `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.
- Les arbitrages V1 des statuts SCM sont disponibles dans `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md`.
- La préparation V1 des satellites SCM est disponible dans `docs/delivery/lot_05_scm_satellites_preparation_v1.md`.
- Les specs V1 des satellites SAS sont disponibles :
  - `docs/delivery/lot_05_sas_satellites_spec_canonique_v1.md` ;
  - `docs/delivery/lot_05_sas_satellites_spec_texte_v1.md`.
- La lettre option IS est codée et testée :
  - `src/sydel_doc_engine/generators/lot_05/lettre_option_is.py` ;
  - `tests/unit/test_lettre_option_is.py` ;
  - `examples/contexts/lot_05_lettre_option_is_example.yaml`.
- Les satellites SCM DOCX hors liste dépenses sont codés et testés :
  - `src/sydel_doc_engine/generators/lot_05/pacte_associes_scm.py` ;
  - `src/sydel_doc_engine/generators/lot_05/contrat_frais_communs.py` ;
  - `src/sydel_doc_engine/generators/lot_05/reglement_interieur_scm.py`.
- Le catalogue et l'orchestrateur exposent désormais :
  - `DOC-026` : pacte d'associés SCM ;
  - `DOC-027` : contrat d'exercice professionnel à frais communs ;
  - `DOC-028` : règlement intérieur de la SCM.
- L'audit V1 de l'acte de cession d'actions est disponible dans `docs/delivery/lot_05_acte_cession_actions_audit_v1.md`.
- Les specs V1 de l'acte de cession d'actions sont disponibles :
  - `docs/delivery/lot_05_acte_cession_actions_spec_canonique_v1.md` ;
  - `docs/delivery/lot_05_acte_cession_actions_spec_texte_v1.md`.
- Le générateur acte de cession d'actions SPFPL est disponible dans `src/sydel_doc_engine/generators/lot_05/acte_cession_actions_spfpl.py` et branché sous `DOC-029`.
- Un contexte exemple acte de cession d'actions SPFPL est disponible dans `examples/contexts/lot_05_acte_cession_actions_example.yaml`.
- La préparation V1 des sources cession SCM est disponible dans `docs/delivery/lot_05_scm_cession_sources_preparation_v1.md`.
- Les sources cession SCM exploitables sont placées dans `project/source_documents/lot_05/`.
- Les specs V1 du blocage cession SCM sont disponibles :
  - `docs/delivery/lot_05_scm_cession_block_spec_canonique_v1.md` ;
  - `docs/delivery/lot_05_scm_cession_block_spec_texte_v1.md`.
- La résolution V1 du bloc cession SCM est disponible dans `docs/delivery/lot_05_scm_cession_block_resolution_v1.md`.
- Le bloc cession SCM est codé, testé et branché :
  - `DOC-031` : PV AGE cession part SCM ;
  - `DOC-032` : courrier SDE cession SCM ;
  - `DOC-033` : acte de cession de parts SCM vers SEL.
- Les générateurs cession SCM sont disponibles :
  - `src/sydel_doc_engine/generators/lot_05/pv_age_cession_scm.py` ;
  - `src/sydel_doc_engine/generators/lot_05/courrier_sde_cession_scm.py` ;
  - `src/sydel_doc_engine/generators/lot_05/acte_cession_parts_scm.py`.
- Un contexte exemple cession SCM est disponible : `examples/contexts/lot_05_scm_cession_block_example.yaml`.
- L'audit de clôture moteur V1 est disponible dans `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md`.
- Les revues batch Lot 03 et Lot 04 sont disponibles :
  - `docs/review/lot_03_batch_review_v1.md` ;
  - `docs/review/lot_04_batch_review_v1.md`.
- L'audit du périmètre restant V1 est disponible dans `docs/project/15_REMAINING_SCOPE_AUDIT_V1.md`.
- Les blueprints style dédiés sont disponibles :
  - `docs/delivery/render_style_blueprint_lot03_batch_v1.md` ;
  - `docs/delivery/render_style_blueprint_statuts_batch_v1.md`.
- `ARBITRAGE-SOURCES-001` est DONE.
- `PLACEMENT-HIGH-001` est DONE.
- `ANALYSE-ORDRE-001` est DONE.
- `SPEC-ORDRE-001` est DONE.
- `SPEC-TEXTE-ORDRE-001` est DONE.
- `CODE-ORDRE-001` est DONE.
- `SPEC-RC-001` est DONE.
- `SPEC-SPFPL-001` est DONE.
- `SPEC-DEROG-001` est DONE.
- `SPEC-CESSION-BAIL-001` est DONE.
- `SYNC-SPECS-001` est DONE.
- `CODE-RC-001` est DONE.
- `SPEC-TEXTE-BAIL-APP-001` est DONE.
- `SPEC-TEXTE-CESSION-CAB-001` est DONE.
- `SPEC-TEXTE-DEROG-001` est DONE.
- `SPEC-TEXTE-SPFPL-001` est DONE.
- `SYNC-TEXTE-SPECS-001` est DONE.
- `SYNC-ARBITRAGES-001` est DONE.
- `CODE-BAIL-APP-001` est DONE.
- `ARBITRAGE-CESSION-001` est DONE.
- `ARBITRAGE-DEROG-001` est DONE.
- `ARBITRAGE-SPFPL-001` est DONE.
- `CODE-CESSION-CAB-001` est DONE.
- `RESUME-CODE-CESSION-CAB-001` est DONE.
- `PREP-DEROG-001` est DONE.
- `CODE-DEROG-CORE-001` est DONE.
- `CODE-SPFPL-AGR-INFO-001` est DONE.
- `CODE-SPFPL-CORE-001` est DONE.
- `PREP-STATUTS-001` est DONE.
- `SPEC-STATUTS-SEL-001` est DONE.
- `SPEC-STATUTS-SPFPL-001` est DONE.
- `SPEC-STATUTS-CIVILS-001` est DONE.
- `SPEC-STATUTS-SAS-001` est DONE.
- `SYNC-STATUTS-SPECS-001` est DONE.
- `CODE-STATUTS-SAS-001` est DONE.
- `CODE-STATUTS-SPFPL-001` est DONE.
- `ARBITRAGE-STATUTS-SEL-001` est DONE.
- `ARBITRAGE-STATUTS-CIVILS-001` est DONE.
- `SYNC-STATUTS-CODE-ARB-001` est DONE.
- `CODE-STATUTS-SEL-001` est DONE.
- `CODE-STATUTS-CIVILS-CORE-001` est DONE pour SCS, SCI et SCI IRIS ; SCM reste hors ticket.
- `FIX-STYLE-LETTERS-001` est DONE.
- `RESUME-FIX-STYLE-LETTERS-001` est DONE.
- `ARBITRAGE-STATUTS-SCM-001` est DONE.
- `PREP-SCM-SAT-001` est DONE.
- `SPEC-SAS-SATELLITES-001` est DONE.
- `CODE-OPTION-IS-001` est DONE.
- `PREP-ACTE-ACTIONS-001` est DONE.
- `SYNC-WAVE-005` est DONE.
- `SYNC-WAVE-006` est DONE.
- `SYNC-WAVE-007` est DONE.
- `CODE-STATUTS-SCM-001` est DONE.
- `CODE-SAS-SATELLITES-001` est DONE.
- `SPEC-SCM-SATELLITES-001` est DONE.
- `CONVERT-DEROG-SALARIEE-001` est DONE.
- `CONVERT-ACTE-ACTIONS-001` est DONE.
- `PREP-SCM-LISTE-DEPENSES-CONVERT-001` est DONE.
- `CODE-SCM-SAT-DOCX-001` est DONE.
- `SPEC-ACTE-ACTIONS-001` est DONE.
- `CODE-ACTE-ACTIONS-001` est DONE.
- `PREP-SCM-CESSION-SOURCES-001` est DONE.
- `REVIEW-BATCH-LOT03-001` est DONE.
- `REVIEW-BATCH-LOT04-001` est DONE.
- `AUDIT-REMAINING-SCOPE-001` est DONE.
- `STYLE-ANALYSE-LOT03-BATCH-001` est DONE.
- `STYLE-ANALYSE-STATUTS-BATCH-001` est DONE.
- `SPEC-SCM-CESSION-BLOCK-001` est DONE.
- `SYNC-WAVE-008` est DONE.
- `CODE-SCM-CESSION-BLOCK-001` est DONE.
- `CODE-SCM-LISTE-DEPENSES-001` est DONE.
- `SPEC-DEROG-SALARIEE-MANUAL-001` est DONE.
- `FIX-STYLE-LOT03-BATCH-001` est DONE.
- `FIX-STYLE-STATUTS-BATCH-001` est DONE.
- `REVIEW-BATCH-LOT05-001` est DONE.
- `SYNC-WAVE-009` est DONE.
- `ARBITRAGE-SCM-CESSION-RESOLVE-001` est DONE.
- `SYNC-WAVE-010` est DONE.
- `FINAL-SCM-CESSION-WAVE-001` est DONE.
- `SYNC-CLOSE-AUDIT-001` est DONE.
- `RECONCILE-MOTOR-CLOSE-001` est DONE.
- `RESUME-ARBITRAGE-STATUTS-CIVILS-001` est DONE, remplacé par l'arbitrage civils V1 absorbé.
- `STYLE-ANALYSE-BATCH-001` est DONE.
- `SYNC-STYLE-CIVILS-001` est DONE.
- `SYNC-STATUTS-SEL-CIVILS-001` est DONE.
- `UI-001` reste explicitement en attente : ne pas brancher Streamlit maintenant.
- Fichiers générés connus :
  - `artifacts/lot_01_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_01_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_01_smoke_test/procuration.docx`
  - `artifacts/lot_05_scm_cession_block_smoke_test/pv_age_cession_parts_scm.docx`
  - `artifacts/lot_05_scm_cession_block_smoke_test/courrier_sde_cession_scm.docx`
  - `artifacts/lot_05_scm_cession_block_smoke_test/acte_cession_parts_scm.docx`
  - `artifacts/lot_02_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/procuration.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/pv_nomination_gerant.docx`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/procuration.docx`
  - `artifacts/lot_02_demande_inscription_ordre_smoke_test/demande_inscription_ordre.docx`
  - `artifacts/lot_02_regime_communautaire_smoke_test/lettre_renonciation_associe.docx`
  - `artifacts/lot_02_regime_communautaire_smoke_test/lettre_avertissement_conjoint.docx`
  - `artifacts/lot_03_cession_cabinets_smoke_test/acte_cession_cabinet_medical.docx`
  - `artifacts/lot_03_cession_cabinets_smoke_test/compromis_cession_cabinet_medical.docx`
  - `artifacts/lot_03_cession_cabinets_smoke_test/acte_cession_cabinet_dentaire.docx`
  - `artifacts/lot_03_cession_cabinets_smoke_test/compromis_cession_cabinet_dentaire.docx`
  - `artifacts/lot_03_derogations_core_smoke_test/formulaire_derogation_sites_sel_formulaire_a_completer.docx`
  - `artifacts/lot_03_derogations_core_smoke_test/demande_derogation_cumul_selarl_bnc_formulaire_a_completer.docx`
  - `artifacts/lot_04_statuts_civils_core_smoke_test/statuts_scs.docx`
  - `artifacts/lot_04_statuts_civils_core_smoke_test/statuts_sci.docx`
  - `artifacts/lot_04_statuts_civils_core_smoke_test/statuts_sci_iris.docx`
- Fichiers smoke RENDER-STYLE-001 générés :
  - `artifacts/render_style_001_lot_01_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/render_style_001_lot_01_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/render_style_001_lot_01_smoke_test/procuration.docx`
  - `artifacts/render_style_001_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`
- Streamlit, PDF, ZIP et `rendering/bundle.py` n'ont pas été modifiés dans ce ticket.
- `artifacts/` reste hors versionnement via `.gitignore`.

## Décisions métier/techniques appliquées dans ce ticket
- Le générateur PV est codé from-scratch dans un module Lot 2 dédié, sans utiliser le DOCX source comme gabarit d'exécution.
- Les variables `personne_1` et `personne_2` ne sont pas introduites dans le modèle de données.
- La liste `associes[]` est répétable pour la liste des associés présents ou représentés et pour les signatures.
- `dirigeant_nomine` est un rôle distinct des associés ; la nomination ne dépend pas de `associes[1]`.
- La branche `emprunt.actif` pilote :
  - la ligne d'ordre du jour emprunt ;
  - la décision emprunt ;
  - la renumérotation du bloc pouvoirs en `DEUXIEME DECISION` ou `TROISIEME DECISION`.
- Les variantes couvertes par tests incluent :
  - un associé / deux associés ;
  - `part` / `parts` ;
  - `né` / `née`.
- La génération bloque si les parts présentes ou représentées ne correspondent pas à la totalité du capital en V1.
- La génération bloque si `societe.capital_variable=false`, faute de wording source validé pour une société non capital variable.
- Aucune intégration orchestrateur Lot 2, UI, PDF ou ZIP n'a été faite.
- Le smoke test réel charge le contexte YAML d'exemple, génère le DOCX PV et vérifie les textes principaux ainsi que l'absence de placeholders résiduels `[` / `]`.
- REVIEW-PV-001 ne modifie pas le code Python et ne change aucun wording juridique ; il documente seulement les points de revue humaine avant branchement.
- Le DOCX de revue couvre la branche `emprunt.actif=true`, deux associés, et un dirigeant nommé féminin distinct des associés.
- La branche `emprunt.actif=false`, le cas associé unique et le dirigeant masculin restent couverts par tests mais doivent faire l'objet d'une revue humaine dédiée avant branchement si l'arbitrage projet l'exige.
- SPEC-RENDER-001 ne modifie pas le code Python et ne change aucun wording juridique ; il formalise uniquement le profil de style global, les paragraphes/blocs, le titre encadré, les signatures simples/encadrées, le rappel légal et le mécanisme de surcharge document par document.
- Les documents déjà impactés par la future couche commune sont DOC-001, DOC-002, DOC-003 et PV nomination gérant.
- Ecart rendu explicitement documenté : les encadrés de signature manquent aujourd'hui dans le rendu généré.
- RENDER-STYLE-001 implémente `SydelDocxStyleProfile` et les helpers communs dans `docx_builder.py`.
- DOC-001, DOC-002 et DOC-003 utilisent désormais le profil global, le cartouche titre commun et un bloc signature encadré commun.
- DOC-001 utilise désormais le rappel légal commun.
- Le PV nomination gérant utilise le profil global, les paragraphes communs, le bloc centré commun et les lignes de signature communes.
- Aucun wording juridique n'a été volontairement modifié ; les changements portent sur le rendu et la factorisation.
- ORCH-L2-PV-001 ajoute le PV nomination gérant au catalogue sous `DOC-004`.
- ORCH-L2-PV-001 enregistre `PvNominationGerantGenerator` dans le registre par défaut de l'orchestrateur.
- Les décisions de sélection appliquées sont : inclusion SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI et SCM ; exclusion SAS.
- SMOKE-ORCH-L2-001 confirme en génération réelle que SCI produit les documents universels et `pv_nomination_gerant.docx`.
- SMOKE-ORCH-L2-001 confirme en génération réelle que SAS produit seulement les documents universels et exclut `pv_nomination_gerant.docx`.
- Aucun wording juridique, aucune UI, aucun PDF et aucun ZIP n'ont été modifiés.
- ANALYSE-ORDRE-001 lit les trois sources Lot 2 en lecture seule et crée deux cadrages dans `docs/delivery/`.
- Les chemins nommés dans le ticket pour les trois DOCX ne correspondent pas littéralement aux noms présents dans le dépôt ; les fichiers transformés correspondants ont été utilisés et l'écart est documenté dans les cadrages.
- La demande d'inscription à l'ordre est considérée suffisamment cadrée pour ouvrir `SPEC-ORDRE-001`, mais pas pour coder.
- Le batch régime communautaire est désormais suffisamment spécifié pour ouvrir `CODE-RC-001`.
- Pour le batch régime communautaire, la mutualisation réaliste porte surtout sur les variables, les rôles, les montants et les helpers de rendu ; deux documents canoniques distincts restent recommandés.
- SPEC-RC-001 compare les variantes SELARL, SELAS et SPFPL du batch régime communautaire.
- Le groupe source Lot 2 / SELAS / SPFPL est retenu comme canonique pour la renonciation ; la variante SELARL brute reste documentée comme écart à relire.
- L'avertissement conserve un overlay limité pour la mention manuscrite SELARL (`à la Société ...`) contre SELAS/SPFPL (`à la [forme_sociale_abregee] ...`).
- CODE-RC-001 produit deux documents canoniques distincts, uniquement pour SELARL, SELAS, SPFPL cession et SPFPL apport lorsque `dossier_options.regime_communautaire == true`.
- CODE-RC-001 ajoute les entrées catalogue `DOC-005` et `DOC-006`, enregistrées dans l'orchestrateur.
- Le filtrage contexte exclut `DOC-005` et `DOC-006` lorsque l'option régime communautaire est fausse.
- La mention manuscrite de l'avertissement applique l'overlay SELARL `à la Société ...` et l'overlay SELAS/SPFPL `à la {forme_sociale_abregee} ...`.
- La renonciation résout `date_courrier_avertissement` explicitement ou par repli sur la date de l'avertissement du batch.
- SPEC-SPFPL-001 formalise le batch SPFPL spécifique sans code Python ; l'acte de cession d'actions reste bloqué faute de source DOCX confirmée.
- SPEC-DEROG-001 formalise les dérogations sans automatiser les formulaires marqués ou traités comme manuels.
- SPEC-CESSION-BAIL-001 formalise deux blocs distincts : `cession cabinets` et `bail / appel de fonds`, sans trancher les anomalies de wording avant code.
- SYNC-SPECS-001 a cherry-pické les quatre specs parallèles dans `main`, puis limite le commit de synchronisation aux fichiers de pilotage.
- SYNC-TEXTE-SPECS-001 a cherry-pické les quatre specs texte parallèles dans `main`.
- Les specs texte intégrées sont bail/appel, cession cabinets, dérogations et SPFPL.
- Le commit final de synchronisation texte est limité aux fichiers de pilotage `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md`.
- Aucun code Python, aucun fichier `project/source_import/raw_drive_dump/` et aucun fichier `artifacts/` n'a été modifié.
- SYNC-ARBITRAGES-001 a cherry-pické les trois arbitrages parallèles dans `main`.
- Les arbitrages intégrés sont cession cabinets, dérogations et SPFPL.
- Le commit final de synchronisation arbitrages est limité aux fichiers de pilotage `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md`.
- Aucun code Python, aucun fichier `project/source_import/raw_drive_dump/` et aucun fichier `artifacts/` n'a été modifié.
- SYNC-CODE-BAIL-APP-001 a absorbé par fast-forward le commit `557a013274aa9f7122c81d5e6e0b52c4043a540c` de `codex/code-bail-app-001` dans `main`.
- CODE-BAIL-APP-001 ajoute `DOC-007` avenant au contrat de bail et `DOC-008` appel de fonds SEL au catalogue et à l'orchestrateur.
- L'avenant au contrat de bail est sélectionné pour SELARL/SELAS lorsque `dossier_options.cession == true`.
- L'appel de fonds SEL est sélectionné uniquement pour SELARL dentaire lorsque `dossier_options.cession == true`.
- Les fichiers `project/source_import/raw_drive_dump/` et `artifacts/` n'ont pas été modifiés.
- SYNC-WAVE-LOT03-05-001 a cherry-pické dans `main` les commits `36828fbc45d6b8a37c2e76eb8227460df441ebde` de `codex/prep-derog-001` et `958fce5d2a9d5d30df4d918cb098fec483f5140e` de `codex/code-spfpl-agr-info-001`.
- PREP-DEROG-001 place les deux sources Lot 03 préparées et ajoute les rapports de préparation / conversion legacy.
- CODE-SPFPL-AGR-INFO-001 ajoute les générateurs SPFPL agrément et note d'information, les sources Lot 05 ciblées, le contexte exemple et les tests unitaires associés.
- Les fichiers `project/source_import/raw_drive_dump/` et `artifacts/` n'ont pas été modifiés.
- SYNC-CODE-WAVE-002 a cherry-pické dans `main` les commits sources `ea35d2af353ac5b8567e82091ab978cf24a27445` de `codex/code-cession-cab-001` et `bee4c8bec27397198a170c4f9888b2470b24c67f` de `codex/code-derog-core-001`.
- Le commit final de synchronisation `SYNC-CODE-WAVE-002` est limité aux fichiers de pilotage `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md`.
- Les fichiers `project/source_import/raw_drive_dump/` et `artifacts/` n'ont pas été modifiés.
- SYNC-WAVE-003 a cherry-pické dans `main` les commits sources `b854821061b85ac66fe785c11cb3c6b0bac5a85b` de `codex/prep-statuts-001` et `09cbad120d22910f05ba5e645971ade56fedb76d` de `codex/code-spfpl-core-001`.
- PREP-STATUTS-001 ajoute la préparation documentaire Lot 04 statuts et place les sources statuts retenues dans `project/source_documents/lot_04/`, sans déduplication ni harmonisation juridique.
- CODE-SPFPL-CORE-001 ajoute les générateurs SPFPL cœur, les sources Lot 05 ciblées, le contexte exemple et les tests unitaires associés.
- Le commit final de synchronisation `SYNC-WAVE-003` est limité aux fichiers de pilotage `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md`.
- Les fichiers `project/source_import/raw_drive_dump/` et `artifacts/` n'ont pas été modifiés.
- SYNC-STATUTS-CODE-ARB-001 a cherry-pické dans `main` les commits sources `82e67120ed714b791d5483108336a570ea520e59`, `a98939c649e4124e40f2cd69c9ed125d342acc31` et `1caafd7`.
- Le conflit modèle entre les apports SAS et SPFPL a été résolu par fusion additive des champs de données nécessaires aux deux familles.
- CODE-STATUTS-SAS-001 ajoute le générateur statuts SAS V1, son contexte exemple, son branchement catalogue/orchestrateur et ses tests ciblés.
- CODE-STATUTS-SPFPL-001 ajoute les générateurs statuts SPFPL cession/apport V1, leur contexte exemple et leurs tests ciblés.
- ARBITRAGE-STATUTS-SEL-001 ajoute les arbitrages V1 des statuts SEL d'exercice dans `docs/delivery/`.
- Les fichiers `project/source_import/raw_drive_dump/` et `artifacts/` n'ont pas été modifiés.
- CODE-DEROG-CORE-001 ajoute `DOC-013` formulaire multi-sites SEL et `DOC-014` demande cumul SELARL/BNC au catalogue et à l'orchestrateur.
- Les deux documents dérogations cœur sont rendus uniquement en `formulaire_a_completer`, avec zones narratives sensibles laissées visibles et non générées par défaut.
- `cumul_salariee` reste hors périmètre tant qu'un DOCX propre n'est pas fourni.
- ARBITRAGE-SOURCES-001 scanne 147 fichiers dans `project/source_import/raw_drive_dump/` et 11 fichiers dans `project/source_documents/`.
- ARBITRAGE-SOURCES-001 identifie 18 groupes de doublons probables, dont 15 groupes de doublons exacts.
- Les 4 cas HIGH documentés sont : DOC-001, DOC-002, DOC-003 et la source canonique `PV nomination gérant`.
- PLACEMENT-HIGH-001 confirme que les 4 cas HIGH sont déjà présents aux emplacements retenus dans `project/source_documents/`.
- PLACEMENT-HIGH-001 n'a effectué aucune nouvelle copie, car chaque cible HIGH existait déjà.
- PLACEMENT-HIGH-001 crée `docs/project/14_SOURCE_PLACEMENT_EXECUTION_V1.md`.
- SPEC-ORDRE-001 compare les variantes raw dump SELARL, SELAS et SPFPL de `Demande d'inscription à l'ordre`.
- Pour cette famille, SELARL et SELAS ont un texte visible identique et plus paramétré ; le groupe SPFPL/source Lot 2 est une copie exacte incluant la mention résiduelle `Dérogation ?`.
- Les structures retenues pour la famille ordre sont SELARL, SELAS, SPFPL cession, SPFPL apport et SCM ; aucune variante SCM dédiée n'a été retrouvée dans le raw dump.
- SPEC-TEXTE-ORDRE-001 retient un tronc commun texte fixe et trois overlays : SELARL/SELAS, SPFPL cession/apport et SCM.
- La mention source `Dérogation ?` n'est pas un wording juridique automatique ; elle devient un bloc conditionnel manuel qui bloque si `dossier.options.derogation == true` sans mention fournie.
- `Dr`, `Monsieur le Président`, la profession ordinale et l'adresse ordinale restent variables ou blocs variables.
- Le mandataire SYDEL peut être préconfiguré, mais ne doit pas être codé en dur dans le générateur.
- CODE-ORDRE-001 implémente le générateur `Demande d'inscription à l'ordre` dans `src/sydel_doc_engine/generators/lot_02/demande_inscription_ordre.py`.
- Le générateur ordre couvre explicitement SELARL, SELAS, SPFPL cession, SPFPL apport et SCM.
- Les overlays SELARL/SELAS, SPFPL et SCM pilotent le rendu de l'adresse ordinale, sans wording SCM spécifique ajouté.
- Le bloc `Dérogation ?` n'est jamais rendu littéralement ; si `dossier_options.derogation=true`, une mention manuelle `ordre.derogation_mention_manuelle` est obligatoire.
- Le mandataire est résolu depuis `mandataire.libelle_affiche` ou depuis les champs détaillés, sans constante SYDEL/Jordan ELBAZ codée dans le générateur.
- Le smoke DOCX dédié a été généré dans `artifacts/lot_02_demande_inscription_ordre_smoke_test/demande_inscription_ordre.docx`, hors versionnement.
- Les 2 cas MEDIUM régime communautaire sont désormais spécifiés et codés dans `CODE-RC-001`.
- Les 3 cas LOW restent bloqués : statuts, liste des souscripteurs / attestation sur le capital, documents sans source claire.
- 16 documents sources sont explicitement hors périmètre moteur courant.
- Aucun fichier de `project/source_import/raw_drive_dump/` ni de `artifacts/` n'a été modifié ; les seules sources ajoutées par la vague sont placées sous `project/source_documents/lot_05/`.
- Aucune UI, aucun PDF, aucun ZIP et aucun wording juridique source n'ont été modifiés.
- FIX-PV-RENDER-001 conserve l'approche from-scratch et ne modifie pas le texte juridique ; les changements portent uniquement sur le rendu DOCX du PV et un helper commun de liste à tiret.
- Le smoke DOCX dédié a été généré dans `artifacts/fix_pv_render_001_smoke_test_2/pv_nomination_gerant.docx`, hors versionnement.

## Prochain ticket à lancer
Prochains chantiers recommandés :
- UI ;
- PDF batch/orchestrateur ;
- ZIP ;
- recette finale.

`SYNC-POST-MOTOR-UI-001` est DONE : les commits UI/PDF/recette `d62670efe10481926437c0e1a5dabbe349fd5938`, `24a881b999371811d39a2403c0b51d9ae8ce0556`, `ef6252b3c15dc3fc39f1efdc05687c0f448f8fe1`, `2f76f61848469ddf2f7b29c3169e8893e83fd3a5` et `c2fc0db4d51485c7c5e721c5184028ae17c68cb3` sont absorbés dans `main`.

`UI-FLOW-001`, `UI-OCCURRENCES-001`, `UI-FORM-SCHEMA-001`, `PDF-BACKEND-001` et `RECIPE-FRAME-001` sont DONE.

`UI-CORE-001`, `RESUME-ZIP-BACKEND-001` et `REVIEW-FINAL-001` sont READY.

`PDF-BACKEND-001` est DONE : le backend PDF local est disponible et intégré à la fondation absorbée, sans ticket PDF supplémentaire confirmé dans cette synchronisation.

`RECONCILE-MOTOR-CLOSE-001` est DONE : le runtime expose `DOC-001` à `DOC-043`, les audits `16/17` concluent la couverture globale OK du moteur DOCX V1, et `docs/project/18_NEXT_PHASE_FOUNDATION_V1.md` cadre la suite UI/PDF/ZIP/recette finale.

`SYNC-CLOSE-AUDIT-001` est DONE : le commit source `0139202b170531fd628f25811c55855a2512acc0` a été absorbé depuis `origin/codex/close-motor-audit-001` par merge de synchronisation ; l'audit présent sur `main` reste la version finale plus récente.

`ARBITRAGE-SCM-CESSION-RESOLVE-001` et `CODE-SCM-CESSION-BLOCK-001` sont DONE et absorbés dans `main` via SYNC-WAVE-010.

`CODE-SCM-LISTE-DEPENSES-001`, `SPEC-DEROG-SALARIEE-MANUAL-001`, `REVIEW-BATCH-LOT05-001`, `FIX-STYLE-STATUTS-BATCH-001` et `FIX-STYLE-LOT03-BATCH-001` sont DONE et absorbés dans `main` via SYNC-WAVE-009.
`CODE-OPTION-IS-001`, `PREP-SCM-SAT-001`, `ARBITRAGE-STATUTS-SCM-001`, `SPEC-SAS-SATELLITES-001` et `PREP-ACTE-ACTIONS-001` sont DONE et absorbés dans `main`.
`RESUME-FIX-STYLE-LETTERS-001`, `CODE-STATUTS-CIVILS-CORE-001`, `CODE-SAS-SATELLITES-001`, `CONVERT-DEROG-SALARIEE-001`, `CONVERT-ACTE-ACTIONS-001` et `SPEC-SCM-SATELLITES-001` sont DONE et absorbés dans `main` via SYNC-WAVE-006.
`CODE-STATUTS-SCM-001`, `PREP-SCM-LISTE-DEPENSES-CONVERT-001`, `CODE-SCM-SAT-DOCX-001` et `SPEC-ACTE-ACTIONS-001` sont DONE et absorbés dans `main` via SYNC-WAVE-007.
`CODE-ACTE-ACTIONS-001`, `PREP-SCM-CESSION-SOURCES-001`, `REVIEW-BATCH-LOT03-001`, `REVIEW-BATCH-LOT04-001`, `AUDIT-REMAINING-SCOPE-001`, `STYLE-ANALYSE-LOT03-BATCH-001`, `STYLE-ANALYSE-STATUTS-BATCH-001` et `SPEC-SCM-CESSION-BLOCK-001` sont DONE et absorbés dans `main` via SYNC-WAVE-008.
`CONVERT-ACTE-ACTIONS-001` est DONE avec DOCX placé dans `project/source_documents/lot_05/` et préparation V1 documentée.
`CONVERT-DEROG-SALARIEE-001` est DONE ; aucun DOCX exploitable n'a ete produit.
`CODE-BAIL-APP-001` est DONE dans `main`.
`PREP-DEROG-001` et `CODE-SPFPL-AGR-INFO-001` sont DONE dans `main`.
`CODE-CESSION-CAB-001` et `CODE-DEROG-CORE-001` sont DONE et absorbés dans `main`.
`PREP-STATUTS-001` et `CODE-SPFPL-CORE-001` sont DONE et absorbés dans `main`.
Les quatre specs statuts SAS, SPFPL, SEL et civils sont DONE et absorbées dans `main`.
`CODE-STATUTS-SAS-001`, `CODE-STATUTS-SPFPL-001` et `ARBITRAGE-STATUTS-SEL-001` sont DONE et absorbés dans `main`.
`STYLE-ANALYSE-BATCH-001` et `ARBITRAGE-STATUTS-CIVILS-001` sont DONE et absorbés dans `main`.
`CODE-STATUTS-SEL-001` est DONE et absorbé dans `main`.
`RESUME-FIX-STYLE-LETTERS-001`, `FIX-STYLE-LETTERS-001` et `CODE-STATUTS-CIVILS-CORE-001` sont DONE et absorbés dans `main`.

## Points ouverts
- Aucun point bloquant moteur DOCX restant après `RECONCILE-MOTOR-CLOSE-001`.
- Restent hors périmètre moteur : UI, ZIP, recette finale, revue humaine juridique/visuelle, documents explicitement manuels et sources legacy non converties.
- PDF-BACKEND-001 est terminé : export DOCX vers PDF disponible en backend local, sans intégration UI.
- Points ouverts PDF après PDF-BACKEND-001 : LibreOffice absent localement, fallback Word COM validé sur smoke, conversion batch/orchestrateur et revue visuelle PDF restent à traiter séparément.
- Fondation UI/PDF/recette synchronisée : `UI-CORE-001`, `RESUME-ZIP-BACKEND-001` et `REVIEW-FINAL-001` sont les prochains tickets READY confirmés.
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Le smoke test confirme la production de trois fichiers DOCX, mais ne remplace pas une revue humaine du rendu visuel ni une validation juridique fine du contenu généré.
- PDF batch/orchestrateur et ZIP restent à intégrer dans des tickets ultérieurs.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'à refactor dédié.
- Le PV nomination gérant est codé, testé et branché dans l'orchestrateur pour les structures concernées.
- Le smoke orchestrateur Lot 2 est vert sur SCI positif et SAS négatif.
- Le pack REVIEW-PV-001 est prêt, mais il ne vaut pas validation juridique.
- La couche commune de rendu DOCX est implémentée.
- Le rendu PV restauré par FIX-PV-RENDER-001 reste soumis à revue humaine visuelle/juridique fine ; le ticket ne vaut pas validation juridique.
- Les signatures encadrées sont disponibles et appliquées aux documents Lot 1 ; le PV conserve des lignes de signature simples sans décision métier supplémentaire.
- UI-001 reste en attente explicite : ne pas brancher Streamlit sans nouveau ticket.
- Points ouverts PV documentés dans la spec texte :
  - périmètre SELAS ;
  - wording capital non variable ;
  - wording société déjà immatriculée ;
  - signature si le dirigeant nommé n'est pas associé ;
  - ponctuation de la dernière ligne `associes[]` ;
  - féminisation éventuelle de la fonction ;
  - règle `euro` / `euros`.
- Points ouverts demande d'inscription à l'ordre après CODE-ORDRE-001 :
  - absence de variante SCM dédiée dans le raw dump, à compenser par une revue humaine du premier rendu SCM ;
  - wording de dérogation non validé, donc bloc manuel obligatoire ou blocage conservé ;
  - valeurs ordinales fournies par contexte ou référentiel ;
  - mandataire SYDEL configurable, jamais imposé comme constante en dur.
- Points ouverts régime communautaire après CODE-RC-001 :
  - revue humaine SELARL de la renonciation canonique, car la variante brute contient des valeurs fixes et `En 2exemplaires` ;
  - féminisation éventuelle de `futur`, non activée automatiquement faute de source ;
  - absence de variante `ma conjointe`, `mon conjoint` restant fixe en V1 ;
  - apport limité à une somme en numéraire ;
  - valeurs par défaut de régime matrimonial, qualité renoncée et formes sociales à fournir par contexte ou référentiel.
  - le smoke DOCX réel ne vaut pas validation juridique fine.
- Points ouverts SPFPL après ARBITRAGE-SPFPL-001 :
  - acte de cession d'actions sans source DOCX confirmée, hors automatisation V1 ;
  - multi-souscripteurs hors automatisation V1 ;
  - commissaire aux apports et évaluateur fournis par contexte ou référentiel validé ;
  - aucune double option `OU` ou cession/apport ne doit être rendue.
- Points ouverts dérogations après CODE-DEROG-CORE-001 :
  - les deux sources Lot 03 préparées sont placées dans `project/source_documents/lot_03/` ;
  - `cumul_salariee` reste bloque apres retentative Word COM : erreur `0x800706BE`, aucun DOCX propre produit ;
  - revue humaine juridique/visuelle du premier rendu `DOC-013` et `DOC-014` ;
  - champs narratifs sensibles toujours fournis explicitement ou laissés comme zones à compléter.
- Points ouverts bail/appel après CODE-BAIL-APP-001 :
  - appel de fonds limité à SELARL dentaire ;
  - avenant limité SELARL/SELAS avec `dossier_options.cession=true` et société en cours d'immatriculation confirmée ;
  - revue humaine juridique/visuelle du premier rendu toujours nécessaire.
- Points ouverts cession après CODE-CESSION-CAB-001 :
  - revue humaine juridique/visuelle du premier rendu DOCX ;
  - variantes SELAS sources non stabilisées au-delà du paramétrage V1 ;
  - PDF et ZIP hors ticket ;
  - les blocages explicites sur validations médicales, crédit-vendeur, SCM, salariés et exercices restent volontaires.
- Points ouverts sources :
  - ne pas élargir la demande d'inscription à l'ordre hors specs V1 sans ticket dédié ;
  - ne pas sortir du choix SPEC-RC-001 pour le régime communautaire sans nouveau ticket d'arbitrage ;
  - ne pas placer automatiquement la famille liste des souscripteurs / attestation sur le capital ;
  - ne pas dedupliquer les statuts entre familles, professions ou variantes.
- Points ouverts statuts après arbitrages V1 :
  - SAS : générateur V1 intégré, modèle source inventorié sous `SAS` mais contenu SAS/SPFPL médecins, actionnaire unique et vocabulaire hétérogène à relire humainement ;
  - SPFPL : générateurs V1 cession/apport intégrés, multi-associés bloqué et corrections d'anomalies non arbitrées toujours exclues ;
  - SEL : générateurs V1 intégrés, multi-associés et signature dirigeant non associé restent bloqués selon arbitrages ;
  - civils : SCS, SCI, SCI IRIS et SCM codés ; SCM reste soumis à revue humaine juridique/visuelle du premier rendu.
- Toute ambiguïté de wording juridique doit bloquer l'implémentation concernée et être documentée.

## Validations connues
- FINAL-SCM-CESSION-WAVE-001 : smoke DOCX OK dans `artifacts/lot_05_scm_cession_block_smoke_test/`, trois documents produits sans placeholder `[` / `]` ni littéral résiduel `Ajouter en cas de CV`.
- FINAL-SCM-CESSION-WAVE-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- FINAL-SCM-CESSION-WAVE-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 172 tests passés.
- FINAL-SCM-CESSION-WAVE-001 : `artifacts/` non versionné.
- SYNC-CLOSE-AUDIT-001 : `git fetch --all --prune` OK.
- SYNC-CLOSE-AUDIT-001 : `origin/codex/close-motor-audit-001` confirmé au commit `0139202b170531fd628f25811c55855a2512acc0`.
- SYNC-CLOSE-AUDIT-001 : `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` présent sur `main` ; relecture documentaire et contrôle du diff, aucun test de code exécuté car aucun fichier Python modifié.
- SYNC-WAVE-010 : `git fetch --all --prune` OK.
- SYNC-WAVE-010 : `codex/arbitrage-scm-cession-resolve-001` confirmé au même commit que `main`, et `codex/code-scm-cession-block-001` confirmé ancêtre de `main`.
- SYNC-WAVE-010 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-010 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 165 tests passés.
- SYNC-WAVE-010 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- FIX-PV-RENDER-001 : source DOCX Lot 2 analysée côté structure/rendu ; en-tête société centré, listes Word, intertitres de décision gras/soulignés et formules de vote en italique identifiés.
- FIX-PV-RENDER-001 : smoke DOCX OK dans `artifacts/fix_pv_render_001_smoke_test_2/pv_nomination_gerant.docx`.
- FIX-PV-RENDER-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- FIX-PV-RENDER-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 49 tests passés.
- CODE-ORDRE-001 : tests unitaires ciblés OK, 7 tests passés dans `tests/unit/test_demande_inscription_ordre.py`.
- CODE-ORDRE-001 : smoke DOCX OK dans `artifacts/lot_02_demande_inscription_ordre_smoke_test/demande_inscription_ordre.docx`, sans placeholder `[` / `]` ni littéral résiduel `Dérogation ?`.
- CODE-ORDRE-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- CODE-ORDRE-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 56 tests passés.
- SPEC-RC-001 : source de vérité, sources Lot 2 et variantes raw dump SELARL / SELAS / SPFPL lues en lecture seule.
- SPEC-RC-001 : specs créées dans `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md` et `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`.
- SPEC-RC-001 : aucun code Python modifié ; validations limitées à la relecture documentaire et au contrôle du diff.
- CODE-RC-001 : smoke DOCX OK dans `artifacts/lot_02_regime_communautaire_smoke_test/`, deux lettres produites sans placeholder `[` / `]`.
- CODE-RC-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- CODE-RC-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 66 tests passés.
- SYNC-SPECS-001 : `git fetch --all --prune` OK.
- SYNC-SPECS-001 : branche `codex/spec-rc-001` créée et poussée avec les deux specs RC uniquement.
- SYNC-SPECS-001 : commits SPFPL, dérogations, cession/bail et RC cherry-pickés dans `main` sans conflit.
- SYNC-SPECS-001 : commit final de pilotage limité à `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md`.
- SYNC-TEXTE-SPECS-001 : `git fetch --all --prune` lancé avant synchronisation.
- SYNC-TEXTE-SPECS-001 : commits `417870da6ee6717a79853547060d6fc0cbacfa9f`, `3672cd129c90e63f440a2316aec54d653b2d24a4`, `18c6614abc1dd3036e1c56565059650748c08883` et `f0424ddad7690d7973d16b00f37aa54b20796d04` cherry-pickés dans `main` sans conflit.
- SYNC-TEXTE-SPECS-001 : relecture documentaire et contrôle du diff ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- SYNC-TEXTE-SPECS-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-ARBITRAGES-001 : `git fetch --all --prune` lancé avant synchronisation.
- SYNC-ARBITRAGES-001 : commits `16a7472610c315fd67f701fa7d9f48d253d62e9c`, `0dda81373125e71ce7817a674322cdcf498a88b0` et `ab8b4c00ead28fcd9ead4ad62e19657f35efa397` cherry-pickés dans `main` sans conflit.
- SYNC-ARBITRAGES-001 : relecture documentaire et contrôle du diff ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- SYNC-ARBITRAGES-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-CODE-BAIL-APP-001 : `git fetch --all --prune` OK.
- SYNC-CODE-BAIL-APP-001 : commit `557a013274aa9f7122c81d5e6e0b52c4043a540c` fast-forwardé dans `main` sans conflit.
- SYNC-CODE-BAIL-APP-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-CODE-BAIL-APP-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 75 tests passés.
- SYNC-CODE-BAIL-APP-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-WAVE-LOT03-05-001 : `git fetch --all --prune` OK.
- SYNC-WAVE-LOT03-05-001 : commits `36828fbc45d6b8a37c2e76eb8227460df441ebde` et `958fce5d2a9d5d30df4d918cb098fec483f5140e` cherry-pickés dans `main` sans conflit.
- SYNC-WAVE-LOT03-05-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-LOT03-05-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 80 tests passés après sauvegarde des fichiers cession non suivis hors ticket.
- SYNC-WAVE-LOT03-05-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- RESUME-CODE-CESSION-CAB-001 : smoke DOCX OK dans `artifacts/lot_03_cession_cabinets_smoke_test/`, quatre documents produits sans placeholder `[` / `]`.
- RESUME-CODE-CESSION-CAB-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- RESUME-CODE-CESSION-CAB-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 89 tests passés.
- CODE-DEROG-CORE-001 : smoke DOCX OK dans `artifacts/lot_03_derogations_core_smoke_test/`, deux formulaires à compléter produits sans placeholder `[` / `]`.
- CODE-DEROG-CORE-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- CODE-DEROG-CORE-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 95 tests passés.
- SYNC-CODE-WAVE-002 : `git fetch --all --prune` OK.
- SYNC-CODE-WAVE-002 : commits sources `ea35d2af353ac5b8567e82091ab978cf24a27445` et `bee4c8bec27397198a170c4f9888b2470b24c67f` cherry-pickés dans `main` sans conflit.
- SYNC-CODE-WAVE-002 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-CODE-WAVE-002 : `.\.venv\Scripts\python.exe -m pytest` OK, 95 tests passés.
- SYNC-CODE-WAVE-002 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-WAVE-003 : `git fetch --all --prune` OK.
- SYNC-WAVE-003 : commits sources `b854821061b85ac66fe785c11cb3c6b0bac5a85b` et `09cbad120d22910f05ba5e645971ade56fedb76d` cherry-pickés dans `main` sans conflit.
- SYNC-WAVE-003 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-003 : `.\.venv\Scripts\python.exe -m pytest` OK, 101 tests passés.
- SYNC-WAVE-003 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-STATUTS-SPECS-001 : `git fetch --all --prune` OK.
- SYNC-STATUTS-SPECS-001 : commits sources `00b7886ac431c8a47d9cdcca8bfed026a756cb69`, `b34c66e5e67f3261317035943e974536be27d6d3`, `9b25e09d08ec2161d757d1581c34073dcbbc594f` et `704eeb7301cf69460c16b2ed9fbc0ea22ca83c8c` cherry-pickés dans `main` sans conflit.
- SYNC-STATUTS-SPECS-001 : relecture documentaire et contrôle du diff ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- SYNC-STATUTS-SPECS-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-STATUTS-CODE-ARB-001 : `git fetch --all --prune` OK.
- SYNC-STATUTS-CODE-ARB-001 : commits sources `82e67120ed714b791d5483108336a570ea520e59`, `a98939c649e4124e40f2cd69c9ed125d342acc31` et `1caafd7` cherry-pickés dans `main`.
- SYNC-STATUTS-CODE-ARB-001 : conflit unique résolu dans `src/sydel_doc_engine/domain/models.py` par fusion additive SAS/SPFPL.
- SYNC-STATUTS-CODE-ARB-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-STATUTS-CODE-ARB-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 111 tests passés.
- SYNC-STATUTS-CODE-ARB-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-STYLE-CIVILS-001 : `git fetch --all --prune` OK.
- SYNC-STYLE-CIVILS-001 : commit source `76dd139da65c233f0c6aecc76bc2ea5e929381ca` intégré dans `main` par fast-forward.
- SYNC-STYLE-CIVILS-001 : commit source `b21f1b0cc5b975049e4acc279b8303f1d739b60f` cherry-pické dans `main` sans conflit.
- SYNC-STYLE-CIVILS-001 : relecture documentaire et contrôle du diff ; aucun test de code exécuté car aucun fichier Python n'a été modifié par le commit final de pilotage.
- SYNC-STYLE-CIVILS-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-STATUTS-SEL-CIVILS-001 : `git fetch --all --prune` OK.
- SYNC-STATUTS-SEL-CIVILS-001 : commit source `9a79560c4bae1ae3a98ec5305b4187f9f4ebd6a8` cherry-pické dans `main` sans conflit.
- SYNC-STATUTS-SEL-CIVILS-001 : arbitrage civils V1 confirmé présent dans `main`, contenu identique au commit source `b21f1b0cc5b975049e4acc279b8303f1d739b60f`.
- SYNC-STATUTS-SEL-CIVILS-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-STATUTS-SEL-CIVILS-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 122 tests passés.
- SYNC-STATUTS-SEL-CIVILS-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- CODE-STATUTS-CIVILS-CORE-001 : smoke DOCX OK dans `artifacts/lot_04_statuts_civils_core_smoke_test/`, trois documents produits sans placeholder `[` / `]`.
- CODE-STATUTS-CIVILS-CORE-001 : tests ciblés OK sur `tests/unit/test_lot_04_statuts_civils.py`, `tests/unit/test_registry_seed.py` et `tests/unit/test_orchestrator_service.py`, 21 tests passés.
- CODE-STATUTS-CIVILS-CORE-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- CODE-STATUTS-CIVILS-CORE-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 129 tests passés.
- SYNC-WAVE-004 : `git fetch --all --prune` OK.
- SYNC-WAVE-004 : commits sources `557fc1920361a8c7831e6b023d70471c9c29e5ff` et `291da7b6db68b3de413fba50cf652dde98a8f6a8` cherry-pickés dans `main` sans conflit.
- SYNC-WAVE-004 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-004 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 130 tests passés.
- SYNC-WAVE-004 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- CONVERT-DEROG-SALARIEE-001 : `Word.Application` COM disponible, mais conversion du `.doc` legacy salariee echouee avec `0x800706BE` ; aucun DOCX cible cree dans `project/source_documents/lot_03/`.
- CONVERT-DEROG-SALARIEE-001 : `LibreOffice` / `soffice`, `pandoc`, `antiword` et `catdoc` non disponibles localement ; aucun code Python modifie.
- SYNC-WAVE-005 : `git fetch --all --prune` OK.
- SYNC-WAVE-005 : commits sources `91436f0916fdecbcc98450b72ba6e602cb8f1a3b`, `1b3ba14d0bcc31fc7dcbf1752d6d3263645ae8b3`, `32059155c618b4e985893f42ef2817187599c281`, `74d41db53543b790e197082e8b9c713f7de92dc2` et `d1d649e11fdc638e6d7da0640c154d1f213739ee` cherry-pickés dans `main` sans conflit.
- SYNC-WAVE-005 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-005 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 135 tests passés.
- SYNC-WAVE-005 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-WAVE-006 : `git fetch --all --prune` OK.
- SYNC-WAVE-006 : commits sources `557fc1920361a8c7831e6b023d70471c9c29e5ff` et `291da7b6db68b3de413fba50cf652dde98a8f6a8` déjà présents par équivalence de contenu ; commits sources `2c55a7ab5f8a44de5c29305cfbc280f930ee32ec`, `568336bed7ccb0a5901abe5d921fd9056573e32d`, `8f0c8ab13d6e8f1a9e50747f8a9d5b607bcb90d6` et `11dc0d8dda23f841d650586e0977e0202270a3b5` cherry-pickés dans `main`.
- SYNC-WAVE-006 : conflits de pilotage résolus dans `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md` en conservant les états les plus récents.
- SYNC-WAVE-006 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-006 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 143 tests passés.
- SYNC-WAVE-006 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-WAVE-007 : `git fetch --all --prune` OK.
- SYNC-WAVE-007 : commits sources `3c040774cdfe57c203b78776a9ea412ec3d14d94`, `6453b6f64665feda898a076f730cba9a6684825b`, `075af377f7c9d7475429f1e738b46483127d757f` et `c221681570782a1b1efc5afc72087cb903cd8a65` cherry-pickés dans `main`.
- SYNC-WAVE-007 : conflits résolus par fusion additive entre statuts SCM, satellites SAS et satellites SCM ; les satellites SCM DOCX sont intégrés sous `DOC-026` à `DOC-028`.
- SYNC-WAVE-007 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-007 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 155 tests passés.
- SYNC-WAVE-007 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-WAVE-008 : `git fetch --all --prune` OK.
- SYNC-WAVE-008 : commits sources `61a1c49353724bbf5b8f1bb8f039d5e96b877ecc`, `d3188c0b4a4a61d889a2ce9ccc37e84e1284adaa`, `939e1c2088892abcf4a8fdcbaa35911f4f8a2f9f`, `19468886f5e885f79b2b35e17e2ff2a097ea9c3a`, `d8747ef20aba478c575c5a491cdf0f634a9c26d3`, `00b4c955b372399bb8701f47a5686748539f061b`, `a181e069f756a1ea846fdcd1824b3f8c57cc11f5` et `518e46fbb8d8bee03a23ea203654b4199103fb7e` cherry-pickés dans `main` sans conflit.
- SYNC-WAVE-008 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-008 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 161 tests passés.
- SYNC-WAVE-008 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SPEC-TEXTE-ORDRE-001 : source de vérité, source Lot 2 et variantes raw dump SELARL / SELAS / SPFPL cession / SPFPL apport lues en lecture seule.
- SPEC-TEXTE-ORDRE-001 : spec texte créée dans `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.
- SPEC-TEXTE-ORDRE-001 : aucun code Python modifié ; validations limitées à la relecture documentaire et au contrôle du diff.
- SPEC-TEXTE-ORDRE-001 : `git status --short --branch` n'était pas propre avant intervention ; aucun commit ni push n'a été effectué.
- SPEC-ORDRE-001 : source de vérité, source Lot 2 et variantes raw dump SELARL / SELAS / SPFPL lues en lecture seule.
- SPEC-ORDRE-001 : spec canonique créée dans `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`.
- SPEC-ORDRE-001 : aucun code Python modifié ; validations limitées à la relecture documentaire et au contrôle du diff.
- SPEC-ORDRE-001 : `git status --short` n'était pas propre avant intervention ; aucun commit ni push n'a été effectué.
- PLACEMENT-HIGH-001 : les 4 fichiers HIGH cibles existent dans `project/source_documents/`.
- PLACEMENT-HIGH-001 : les hashes cibles ont été comparés aux sources brutes correspondantes pour les cas HIGH ; aucune copie nouvelle nécessaire.
- PLACEMENT-HIGH-001 : aucun test de code exécuté car aucun fichier Python n'a été modifié.
- PLACEMENT-HIGH-001 : `git status --short` n'était pas propre avant intervention ; aucun commit ni push n'a été effectué.
- ARBITRAGE-SOURCES-001 : scan documentaire en lecture seule ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- ARBITRAGE-SOURCES-001 : relecture documentaire du diff requise avant toute reprise de placement physique.
- ARBITRAGE-SOURCES-001 : `raw_drive_dump` n'a pas été versionné.
- ANALYSE-ORDRE-001 : relecture documentaire uniquement ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- ANALYSE-ORDRE-001 : `git status --short` consulté avant modifications ; le dépôt contenait déjà des fichiers non suivis hors périmètre du ticket.
- Harnais temporaire de smoke test revue : OK, 1 test passé ; DOCX régénéré et aperçu texte extrait.
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 44 tests passés.
- Smoke test PV réel : OK, DOCX généré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/`.
- Smoke test Lot 1 réel : OK, 3 DOCX produits dans `artifacts/lot_01_smoke_test/`.
- SPEC-RENDER-001 : relecture documentaire uniquement ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- RENDER-STYLE-001 : smoke Lot 1 OK dans `artifacts/render_style_001_lot_01_smoke_test/`.
- RENDER-STYLE-001 : smoke PV OK dans `artifacts/render_style_001_pv_nomination_gerant_smoke_test/`.
- RENDER-STYLE-001 : un premier smoke PV vers l'ancien dossier `artifacts/lot_02_pv_nomination_gerant_smoke_test/` a échoué avec `PermissionError` sur le DOCX existant, probablement verrouillé ; le smoke a été relancé avec succès dans un nouveau dossier d'artefacts.
- ORCH-L2-PV-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- ORCH-L2-PV-001 : `.\.venv\Scripts\python.exe -m pytest` OK.
- SMOKE-ORCH-L2-001 : smoke SCI positif OK, `pv_nomination_gerant.docx` présent.
- SMOKE-ORCH-L2-001 : smoke SAS négatif OK, `pv_nomination_gerant.docx` absent.
- SMOKE-ORCH-L2-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SMOKE-ORCH-L2-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 47 tests passés.
- RECONCILE-MOTOR-CLOSE-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- RECONCILE-MOTOR-CLOSE-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 176 tests passés.
- RECONCILE-MOTOR-CLOSE-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- PDF-BACKEND-001 : tests ciblés `tests/unit/test_pdf_export.py` OK, 6 tests passés.
- PDF-BACKEND-001 : smoke réel OK, `declaration_non_condamnation.docx` généré puis converti en PDF via `word-com` dans `artifacts/pdf_backend_001_smoke_test_2/`, hors versionnement.
- PDF-BACKEND-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- PDF-BACKEND-001 : `.\.venv\Scripts\python.exe -m pytest` OK.
- PDF-BACKEND-001 : `artifacts/` non versionné ; aucun fichier UI modifié.
- SYNC-POST-MOTOR-UI-001 : `git fetch --all --prune` OK.
- SYNC-POST-MOTOR-UI-001 : commits sources `d62670efe10481926437c0e1a5dabbe349fd5938`, `24a881b999371811d39a2403c0b51d9ae8ce0556`, `ef6252b3c15dc3fc39f1efdc05687c0f448f8fe1`, `2f76f61848469ddf2f7b29c3169e8893e83fd3a5` et `c2fc0db4d51485c7c5e721c5184028ae17c68cb3` cherry-pickés dans `main` sans conflit.
- SYNC-POST-MOTOR-UI-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-POST-MOTOR-UI-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 182 tests passés.
- SYNC-POST-MOTOR-UI-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- UI-PDF-ZIP-INTEGRATION-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- UI-PDF-ZIP-INTEGRATION-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 186 tests passés.
- UI-PDF-ZIP-INTEGRATION-001 : smoke lancement Streamlit OK sur `http://localhost:8502`, page UI chargee.
- UI-PDF-ZIP-INTEGRATION-001 : `artifacts/` non versionne ; le PDF reste dependant de LibreOffice ou Word COM local.

- SYNC-FINAL-FOUNDATIONS-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-FINAL-FOUNDATIONS-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 191 tests passes.
- SYNC-FINAL-FOUNDATIONS-001 : fichiers critiques 16/17/18/19/20/21 et `docs/review/final_recipe_framework_v1.md` presents sur `main`.
- SYNC-FINAL-FOUNDATIONS-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifies.
- WORKTREE-CLEANUP-AND-UI-STATUS-001 : `codex/review-final-001` apporte uniquement `docs/review/final_review_pack_v1.md`, integre dans `main`.
- WORKTREE-CLEANUP-AND-UI-STATUS-001 : l'UI actuelle est confirmee comme UI technique de pilotage par contexte YAML/JSON, DOCX, PDF local optionnel et ZIP ; elle n'est pas une UI produit finale ni un wizard metier.
- WORKTREE-CLEANUP-AND-UI-STATUS-001 : les anciens worktrees locaux sont archives sans suppression definitive ; `project/source_import/raw_drive_dump/` n'est pas modifie dans le repo.
- REVIEW-FINAL-001 : `git status --short --branch` OK sur `main...origin/main`, sans diff initial ; `git fetch --prune` bloque sur `.git/FETCH_HEAD` en permission denied, donc l'alignement distant est confirme seulement contre la ref locale `origin/main`.
- REVIEW-FINAL-001 : catalogue et registre alignes sur 43 documents/generateurs, `DOC-001` a `DOC-043`, aucun generateur manquant.
- REVIEW-FINAL-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- REVIEW-FINAL-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 191 tests passes.
- REVIEW-FINAL-001 : tests cibles DOCX/orchestrateur/registre/PDF/ZIP/UI runtime OK, 54 tests passes.
- REVIEW-FINAL-001 : smoke reel `examples/contexts/lot_02_orchestrator_positive_example.yaml` OK en DOCX/ZIP, 4 DOCX produits et ZIP avec manifeste dans `artifacts/review_final_001_smoke/20260518_114432/`.
- REVIEW-FINAL-001 : backend PDF local indisponible pendant la revue ; LibreOffice introuvable et Word COM indisponible, avec un processus Word accroche puis arrete.
- REVIEW-FINAL-001 : balayage des contextes exemples en DOCX/ZIP sans PDF ; seuls `lot_02_orchestrator_negative_sas_example.yaml` et `lot_02_orchestrator_positive_example.yaml` sont complets pour une generation dossier globale, les autres exemples restent des contextes de famille/generateur incomplets.
- UI-BUSINESS-WIZARD-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- UI-BUSINESS-WIZARD-001 : tests cibles UI runtime / orchestrateur / DOCX / ZIP OK, 37 tests passes.
- UI-BUSINESS-WIZARD-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 196 tests passes.
- UI-BUSINESS-WIZARD-001 : test metier reel via runtime OK, 4 DOCX `DOC-001` a `DOC-004` generes et ZIP avec `manifest.json`, sans crochet placeholder detecte.
- DEPLOY-STREAMLIT-CLOUD-FIX-001 : `.\.venv\Scripts\python.exe -m pip install -e .` OK.
- DEPLOY-STREAMLIT-CLOUD-FIX-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- DEPLOY-STREAMLIT-CLOUD-FIX-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 196 tests passes.
- DEPLOY-STREAMLIT-CLOUD-FIX-001 : Poetry non disponible localement (`poetry` absent du PATH et module `poetry` absent de la venv), donc `poetry check` et `poetry install` non executes localement.
- CASE-CATALOG-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- CASE-CATALOG-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 208 tests passes.
- UI-CASE-WIZARD-002 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- UI-CASE-WIZARD-002 : `.\.venv\Scripts\python.exe -m pytest` OK, 217 tests passes.
- SELARL-PILOT-PROTOCOL-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SELARL-PILOT-PROTOCOL-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 217 tests passes.
- SELARL-PILOT-SOURCE-VERIFY-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SELARL-PILOT-SOURCE-VERIFY-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 217 tests passés.
- SELARL-FORM-SCHEMA-IMPL-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SELARL-FORM-SCHEMA-IMPL-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 231 tests passés.
- SELARL-UI-WIZARD-IMPL-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SELARL-UI-WIZARD-IMPL-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 239 tests passés.
- SELARL-FLOW-REALIGN-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SELARL-FLOW-REALIGN-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 245 tests passés.
- SELARL-REUSE-RULES-REALIGN-001 : `.\.venv\Scripts\python.exe -m pytest tests/unit/test_selarl_form_schema.py tests/unit/test_business_wizard.py` OK, 48 tests passés.
- SELARL-REUSE-RULES-REALIGN-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SELARL-REUSE-RULES-REALIGN-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 252 tests passés.
- SELARL-UI-REALIGN-001 : `.\.venv\Scripts\python.exe -m pytest tests/unit/test_business_wizard.py` OK, 34 tests passés.
- SELARL-UI-REALIGN-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SELARL-UI-REALIGN-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 257 tests passés.
- SELARL-SMOKE-REALISTIC-001 : smoke DOCX/ZIP OK sur trois scénarios réalistes, 4 DOCX et 1 ZIP produits par scénario ; backend PDF local indisponible.
- SELARL-SMOKE-REALISTIC-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 257 tests passés.
- SELARL-CLOUD-GENERATION-BUG-001 : bug reproduit via AppTest sur le parcours visible ; avant correction `Documents prets = 0` et `Generer les DOCX` désactivé après saisie tardive des champs source.
- SELARL-CLOUD-GENERATION-BUG-001 : `.\.venv\Scripts\python.exe -m pytest tests/unit/test_business_wizard.py -q` OK, 35 tests passés.
- SELARL-CLOUD-GENERATION-BUG-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SELARL-CLOUD-GENERATION-BUG-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 266 tests passés.
- ASSISTANT-METIER-PREFILL-001 : `.\.venv\Scripts\python.exe -m pytest tests\unit\test_business_wizard.py -q` OK, 41 tests passés.
- ASSISTANT-METIER-PREFILL-001 : `.\.venv\Scripts\python.exe -m pytest tests\unit\test_single_document_mode.py tests\unit\test_ui_runtime.py -q` OK, 12 tests passés.
- ASSISTANT-METIER-PREFILL-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- ASSISTANT-METIER-PREFILL-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 272 tests passés.
- GLOBAL-FRONT-ARCHITECTURE-001 : relecture documentaire et controle du diff OK ; aucun test Python requis car aucun fichier Python modifie.
- GLOBAL-FRONT-ARCHITECTURE-001 : `docs/docssource_truth/` etait non suivi avant intervention et reste hors perimetre.
- GLOBAL-FRONT-ARCHITECTURE-QA-001 : relecture documentaire et controle du diff OK ; aucun test Python requis car aucun fichier Python modifie.
- GLOBAL-FRONT-ARCHITECTURE-QA-001 : `docs/docssource_truth/` etait non suivi avant intervention et reste hors perimetre.
- FRONT-DATA-LAYER-001 : package `src/sydel_doc_engine/front_data/` cree avec objets front globaux, mapping canonique V2.1, exigences sentinelles et diagnostics de validation ; `ruff check .` OK et `pytest` OK, 288 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, Streamlit ou UI visible modifie.
- FRONT-ROLE-MODEL-001 : module `front_data.role_model` cree avec familles de roles, portees, modele ordre, representation de personne morale, tiers commissaire/evaluateur et garde-fous `{role}` ; `ruff check .` OK et `pytest` OK, 298 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, Streamlit ou UI visible modifie.
- FRONT-ADDRESS-MODEL-001 : module `front_data.address_model` cree avec usages d'adresse, politiques de reutilisation explicites, formes affichees/composants, overrides et validations dediees ; `ruff check .` OK et `pytest` OK, 313 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, Streamlit ou UI visible modifie.
- FRONT-DOSSIER-EDITOR-001 : module `app.front_dossier_editor` cree avec profils dossier prudents, `DossierRecord` minimal, lignes UI d'etapes/blocs/exigences/statuts et rendu AppTest de la zone `Dossier` ; `ruff check .` OK et `pytest` OK, 364 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, wording juridique ou prototype historique modifie.
- TRACK-B-SELARL-HUMAN-REFERENCE-LOCK-002 : source humaine prioritaire lue depuis `C:\Users\Gad\Downloads\Retours humains .docx` ; verrou projet cree dans `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md`.
- TRACK-B-SELARL-HUMAN-REFERENCE-LOCK-002 : corrections documentaires appliquees sur `DOC-002` autorisation domiciliation, `DOC-001` DNC, `DOC-005` renonciation, `DOC-004` PV nomination gerant et `DOC-016` statuts SELARL chirurgien-dentiste.
- TRACK-B-SELARL-HUMAN-REFERENCE-LOCK-002 : variables `civilite_president_seance`, `prenom_president_seance`, `nom_personne_seance` conservees et branchees via `reunion.president`, avec derivation clean front depuis l'associe unique/praticien.
- TRACK-B-SELARL-HUMAN-REFERENCE-LOCK-002 : OPEN POINT restant sur le texte parasite `RCS PARIS 788 531 432 0153814303` et la phrase de mandat, non presents dans la renonciation actuelle et vraisemblablement rattaches a la procuration hors scope de ce ticket.
- TRACK-B-SELARL-DENTIST-LINE-BY-LINE-LOCK-003 : rapport cree dans `docs/review/track_b_selarl_dentist_line_by_line_lock_003_report_v1.md`; DOC-016 compare article par article contre `C:\Users\Gad\Downloads\Retours humains .docx`, 243 paragraphes humains attendus, 243 paragraphes generes, 0 ecart sur les articles 1 a 34.
- TRACK-B-SELARL-DENTIST-LINE-BY-LINE-LOCK-003 : le point auparavant ouvert `RCS PARIS 788 531 432 0153814303` / `L'execution de ce mandat...` est ferme dans `DOC-003` procuration par suppression RCS/telephone et ajout de `Fait pour servir et valoir ce que de droit.` avant signature.
- TRACK-B-SELARL-DENTIST-LINE-BY-LINE-LOCK-003 : le PV nomination gerant utilise desormais l'introduction humaine plurielle `Les associes... se sont reunis au siege social`, tout en conservant `Nomination du gerant` en associe unique.
- TRACK-B-SELARL-DENTIST-LINE-BY-LINE-LOCK-003 : OPEN GAP restant limite au wrapper post-article de DOC-016, car la reference humaine disponible couvre le bloc articles 1 a 34 mais ne confirme ni n'interdit les signatures et annexes conservees par la spec statuts existante.
- TRACK-B-SELARL-DENTIST-LINE-BY-LINE-LOCK-003 : validations OK : tests cibles 63 passes, `ruff check .`, smoke DOCX/ZIP dentiste avec controle placeholders/parasites, clean front HTTP 200 sur `http://localhost:8523` puis arret PID `13164`.
- TRACK-B-SELARL-ROLLOUT-NEXT-CASE-001 : matrice des cas SELARL restants creee dans `docs/review/track_b_selarl_rollout_next_case_001_report_v1.md`.
- TRACK-B-SELARL-ROLLOUT-NEXT-CASE-001 : prochain cas choisi = SELARL medecin unipersonnelle standard, decision GO, car delta minimal vs dentiste verrouille et sources/specs existantes suffisantes pour lancer sans inventer.
- TRACK-B-SELARL-ROLLOUT-NEXT-CASE-001 : aucun code moteur/front modifie ; le cas medecin etait deja cable dans le clean front et le delta utile du ticket est la qualification/smoke du rollout.
- TRACK-B-SELARL-ROLLOUT-NEXT-CASE-001 : smoke DOCX/ZIP medecin OK dans `artifacts/track_b_selarl_rollout_next_case_001_medecin`, avec 6 DOCX, ZIP, `DOC-017` present, `DOC-016` absent, aucun placeholder ni parasite RCS/telephone.
- TRACK-B-SELARL-ROLLOUT-NEXT-CASE-001 : statuts finaux constates : documents courts DOC-001/DOC-002/DOC-003/DOC-004 LOCKED, DOC-017 medecin PARTIAL faute de lock humain ligne par ligne specifique, DOC-016 dentiste LOCKED non rouvert.
- TRACK-B-SELARL-ROLLOUT-NEXT-CASE-001 : validations OK : tests cibles 41 passes, `ruff check .`, smoke DOCX/ZIP medecin avec controle texte, clean front HTTP 200 sur `http://localhost:8525`, processus Python/Streamlit arretes (`remaining=0`).
- TRACK-B-SELARL-MEDECIN-LINE-BY-LINE-LOCK-004 : rapport cree dans `docs/review/track_b_selarl_medecin_line_by_line_lock_004_report_v1.md`.
- TRACK-B-SELARL-MEDECIN-LINE-BY-LINE-LOCK-004 : source exploitable retenue pour `DOC-017` = `project/source_documents/lot_04/Modèle statuts SELARL médecins.docx`; le dernier retour humain `Retours humains .docx` ne contient pas de bloc medecin complet equivalent au dentiste.
- TRACK-B-SELARL-MEDECIN-LINE-BY-LINE-LOCK-004 : `DOC-017` classe LOCKED source-level pour SELARL medecin unipersonnelle standard : 311 paragraphes source exploitables compares au rendu, 0 ecart, articles 1 a 36 + signature + annexe couverts.
- TRACK-B-SELARL-MEDECIN-LINE-BY-LINE-LOCK-004 : OPEN GAPS `DOC-017` limites a l'absence de retour humain medecin recent, a la ligne source incomplete `[civilite_personne_2]...` exclue du lock unipersonnel, et aux variantes multi-associes/regime communautaire medecin non verrouillees dans ce ticket.
- TRACK-B-SELARL-MEDECIN-LINE-BY-LINE-LOCK-004 : validations OK : tests cibles 62 passes, `ruff check .`, smoke DOCX/ZIP medecin avec controle placeholders/parasites, clean front HTTP 200 sur `http://localhost:8526`, processus Python/Streamlit arretes (`remaining=0`).
- TRACK-B-SELARL-MEDECIN-REGIME-COMMUNAUTAIRE-005 : entree historique ; le cas medecin + regime communautaire est maintenant corrige par `SELARL-DOC006-REGIME-FIX-001` et genere `DOC-005` + `DOC-006`.
- TRACK-B-SELARL-MEDECIN-REGIME-COMMUNAUTAIRE-005 : smoke DOCX/ZIP OK dans `artifacts/track_b_selarl_medecin_regime_communautaire_005`, avec 7 DOCX, ZIP, `DOC-005` present, `DOC-006` absent, aucun placeholder ni segment parasite RCS/telephone.
- TRACK-B-SELARL-MEDECIN-REGIME-COMMUNAUTAIRE-005 : validations OK : tests cibles 25 passes, tests cibles + statuts 36 passes, `ruff check .`, clean front HTTP 200 sur `http://localhost:8528`, processus Python/Streamlit arretes et port 8528 ferme.

## Recommandation immediate suivante
Recommandation SELARL 2026-06-02 : lire `docs/project/SELARL_CANONICAL_STATUS_V1.md`, puis `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`, puis poursuivre `SELARL-FINAL-ASSOCIE-VALIDATION-001`. Le pack 004 n'est plus la version finale a transmettre ; la version active de validation est `artifacts/selarl_closing_pack_005/`, deja regeneree et auditee.

Recommandation SELARL la plus recente : lire `docs/project/SELARL_CANONICAL_STATUS_V1.md`, puis `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`, puis les rapports `docs/review/selarl_closing_pack_005_report_v1.md` et `docs/review/selarl_human_returns_deep_audit_006_report_v1.md`. Etape officielle en cours : validation finale associe sur pack 005.

Recommandation prioritaire 2026-06-01 : commencer par `docs/project/PROJECT_CONTROL_TOWER_V1.md`, puis lire `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`, puis le fichier actif `docs/sprints/SPRINT_[TYPE]_V1.md`, puis `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`, puis `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`, puis appliquer `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`.

Pour tout nouveau type d'entreprise, le mode d'emploi complete par
`COMPANY-TYPE-SPRINT-PLAYBOOK-002` est maintenant la methode a appliquer :
sources reference + NotebookLM/modele + retours humains, questions uniquement
sur trous reels, reuse audit, matrice, dev borne, pack actif, audit fidelite,
retour associe par ecarts concrets, puis statut `DONE/PARTIAL/BLOCKED`.

Pour un nouveau chat sans identite claire, demander d'abord : `Bonjour, tu es Gad ou Naomi ? Je te route ensuite sur le bon protocole projet.` Si la personne est Gad, appliquer le rail superviseur produit et ne pas declencher NotebookLM seulement parce qu'il parle de Naomi. Si la personne est Naomi/Naomi, le sprint actif est SELAS : appliquer d'abord `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`, puis `docs/sprints/SPRINT_SELAS_V1.md`. Statut : Phase 3 NotebookLM, `NO-GO dev`. La branche cible est `codex/naomie-selas-sprint`. Apres identification de Naomi, meme si elle dit seulement `bonjour`, Codex doit donner le Prompt NotebookLM 01 complet, attendre sa reponse brute, la structurer dans le journal, puis choisir le prompt suivant. Pas de production, generation, audit, matrice, code ou push de fonctionnalite avant couverture NotebookLM suffisante.

Si Gad demande `ou en est Naomi ?`, appliquer `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` : lire tour de controle, dernier etat, `docs/sprints/SPRINT_SELAS_V1.md`, `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`, journal NotebookLM et branche accessible avant de repondre. Reponse attendue : statut Naomi, branche suivie, dernieres traces lues, ce que Naomi a fait, ce qui manque ou bloque, action cote Naomi, action cote Codex/Gad.

Pour la branche Naomi, ne pas confondre blocage local Git et branche distante inaccessible. Si `git fetch` echoue avec `FETCH_HEAD Permission denied` ou identifiants absents, tenter le connecteur GitHub. Etat verifie ici : `codex/naomie-selas-sprint` existe cote GitHub ; fetch local seulement est bloque.

Les rapports Naomi a Gad sont maintenant differentiels : lire la section `Rapports Gad` du worklog, couvrir seulement la periode depuis le dernier rapport, puis inscrire le nouveau rapport comme curseur. Si Gad laisse un message pour Naomi, l'inscrire dans `Messages Gad a transmettre a Naomi` avec statut `a transmettre`; au prochain echange Naomi, citer le message exact et marquer `transmis`.

Correctif branche Naomi 2026-06-02 : `AGENTS.md`, `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` et `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` sont maintenant publies sur `codex/naomie-selas-sprint` via GitHub. Le Git local de ce worktree reste bloque par permissions sur `FETCH_HEAD`, donc utiliser le connecteur GitHub si la lecture locale echoue.

Si Naomi pose une question d'apprentissage, appliquer `docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md`. Le mode professeur explique mais ne declenche jamais de developpement.

Pour la SELARL, lire d'abord `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`, puis `docs/project/SELARL_CANONICAL_STATUS_V1.md`, puis appliquer `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`. Prochaine etape recommandee : faire tester `artifacts/selarl_closing_pack_005/` par l'associe avec `docs/review/selarl_final_validation_001_brief_v1.md`, puis corriger uniquement les ecarts concrets ou clore le perimetre simple/regime. Tout developpement complexe hors validation pack 005 reste en `NO-GO dev` tant qu'un sous-cas unique n'est pas choisi et cadre explicitement.
