# Tableau d'exécution

## Statuts
- READY
- IN_PROGRESS
- BLOCKED
- DONE

## Tickets actifs

| ID | Statut | Objet | Entrées obligatoires | Sorties obligatoires |
|---|---|---|---|---|
| PROJECT-CLARITY-AUDIT-001 | DONE | Auditer le statut reel des types d'entreprise et corriger la confusion catalogue/moteur vs sprint produit | demande Gad 2026-06-02 + confusion issue du premier traitement fonde sur `Documents_a_generer_par_cas.docx` seul | `docs/review/project_clarity_audit_001_report_v1.md` + `docs/project/COMPANY_TYPE_STATUS_REGISTRY_V1.md` + tour de controle/master plan alignes : seuls SELARL et SELAS sont en traitement metier ; autres types = inventaire technique/non sprint produit |
| PROJECT-COMPANY-TYPE-UI-STATUS-001 | DONE | Durcir l'affichage front/rapports pour ne pas presenter les types non sprintes comme generables produit V1 | `COMPANY_TYPE_STATUS_REGISTRY_V1.md` + audit `PROJECT-CLARITY-AUDIT-001` + front/wizard exposant plusieurs types | `business_dossier_types()` distingue `SELARL` product generable, `SELAS` sprint actif `NO-GO dev`, et `SCI`/`SCM`/`SPFPL`/`SCS`/`SAS` en `INVENTAIRE_TECHNIQUE`; warnings wizard + tests cibles + rapport `docs/review/company_type_ui_status_001_report_v1.md` |
| FRONT-INFORMATION-DEDUP-AGENT-001 | DONE | Formaliser l'agent qui empeche la redondance de saisie front | demande Gad 2026-06-02 : une information identique doit etre demandee une seule fois | `docs/project/FRONT_INFORMATION_DEDUP_AGENT_PROTOCOL_V1.md` + org chart/product guardrail/playbook/AGENTS raccordes ; controle obligatoire avant `GO dev` front |
| GLOBAL-NAOMIE-COLLABORATION-001 | DONE | Formaliser le workflow Gad / Naomi / Codex reusable sur tous les projets | demande Gad 2026-06-01 + incidents cadrage Naomi + besoin multi-projets | `GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md` + `PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md` + pointeurs projet mis a jour |
| GLOBAL-CHAT-IDENTITY-ROUTING-001 | DONE | Corriger le routage nouveau chat Gad / Naomi avant declenchement de protocole | demande Gad 2026-06-02 + incident prompt NotebookLM declenche alors que Gad parlait de Naomi | `AGENTS.md` + tour de controle + runtime Naomi + sprint SELAS + workflow global/template + workflow/handoff/master plan alignes : `bonjour` sans identite => demander Gad ou Naomi ; Gad => superviseur ; Naomi => runtime SELAS |
| NAOMIE-SUPERVISION-ORCHESTRATOR-001 | DONE | Formaliser l'orchestrateur de suivi Naomi generique et le worklog de sprint | demande Gad 2026-06-02 : suivre l'avancee de Naomi sans lui demander un statut oral, lire branche/worklog/tour de controle | `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` + `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` + protocole global/template/runtime/tour de controle/workflow/handoff/master plan alignes |
| NAOMIE-REPORT-CURSOR-AND-MESSAGE-QUEUE-001 | DONE | Ajouter rapports differentiels Gad et messages Gad en attente pour Naomi | demande Gad 2026-06-02 : noter le dernier rapport demande et transmettre au prochain echange les messages de Gad a Naomi | protocole orchestrateur + worklog SELAS + runtime/template/global/tour de controle/orchestrateur de sprint alignes : dernier rapport Gad, delta depuis curseur, file messages `a transmettre/transmis` |
| NAOMIE-BRANCH-READ-FALLBACK-001 | DONE | Corriger le diagnostic branche Naomi quand `git fetch` local est bloque | capture Gad 2026-06-02 : `FETCH_HEAD Permission denied` puis branche declaree inaccessible | protocole orchestrateur + worklog SELAS + global/template alignes : tenter connecteur GitHub avant de dire branche inaccessible ; branche distante confirmee visible |
| NAOMIE-REPORT-FRESHNESS-AUDIT-001 | DONE | Corriger les rapports Gad stale sur Naomi/SELAS | capture Gad 2026-06-02 : rapport dit que Naomi est au demarrage NotebookLM alors que le repo contient deja de la matiere SELAS | diagnostic `PROJECT_STATE_IGNORED + WORKLOG_STALE` ; audit de fraicheur obligatoire ; base corrigee ensuite par `WORKSTREAM-TRACE-BOSS-REPORT-001` |
| PROJECT-AGENT-ORG-CHART-001 | DONE | Formaliser la pyramide des agents et le rattrapage retroactif | demande Gad 2026-06-02 : avoir un big orchestrateur, des sous-agents et une chaine A-Z pour savoir ou demander les preuves | `PROJECT_AGENT_ORG_CHART_V1.md` cree ; AGENTS/tour/handoff/workflow/master plan/sprint/worklog raccordes ; rapport `docs/review/selas_naomie_backfill_001_report_v1.md` produit |
| WORKSTREAM-TRACE-BOSS-REPORT-001 | DONE | Corriger le suivi Naomi en tracabilite de flux et rapport boss court | demande Gad 2026-06-02 : ne pas evaluer Naomi personnellement ; tout travail fait dans son perimetre remonte comme flux Naomi ; rapport court et decisionnel | `WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` cree ; AGENTS/tour/workflow/handoff/org chart/sprint/worklog/rattrapage alignes sur flux Naomi + rattrapage retroactif |
| NAOMIE-SYNC-CHECKPOINT-001 | IN_PROGRESS | Recuperer l'avancee SELAS annoncee mais absente des traces publiees | Gad 2026-06-02 indique que Naomi a termine SELAS jusqu'a attente retour humain ; branche `codex/naomie-selas-sprint` ne montre que les commits protocole | `NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md` cree ; sprint/worklog/tour/orchestrateur traces : attendre commit pousse ou Sync packet de Naomi avant requalification |
| SELARL-CLOSING-PLAN-001 | DONE | Ecrire la fin de sprint SELARL avec tickets et gates | `SELARL_CANONICAL_STATUS_V1.md` + backlog/factory SELARL + demande Gad | `docs/sprints/SPRINT_SELARL_CLOSING_V1.md` + tickets de cloture `SELARL-CLOSING-*` |
| SELARL-CLOSING-PACK-001 | DONE | Regenerer le pack de revue SELARL simple historique | `SPRINT_SELARL_CLOSING_V1.md` + clean front Track B + scenarios medecin/dentiste/regime communautaire | pack 001 produit puis remplace par packs 002/003 |
| SELARL-ASSOCIE-REVIEW-001 | DONE | Recevoir et classer le retour associe initial | retour Gad/associe : questions inutiles, `DOC-006` evident, exigence fidelite source | decision : corriger `DOC-006`, ne plus poser de questions abstraites |
| SELARL-REVIEW-TRIAGE-001 | DONE | Classer les retours humains SELARL | retour associe/juriste | correction reelle identifiee : `DOC-006` doit etre actif en regime communautaire |
| SELARL-DOC006-REGIME-FIX-001 | DONE | Activer `DOC-006` avec `DOC-005` quand regime communautaire actif | sources Lot 2 + specs regime communautaire + clean front | front, contexte conjoint adresse, tests et docs alignes |
| SELARL-CLOSING-PACK-002 | DONE | Regenerer le pack SELARL corrige | correction `DOC-006` + scenarios medecin/dentiste/regime | `artifacts/selarl_closing_pack_002/` + `docs/review/selarl_closing_pack_002_report_v1.md` |
| SELARL-HUMAN-RETURNS-DEEP-AUDIT-002 | DONE | Relire les retours humains et auditer le pack 002 | `C:\Users\Gad\Downloads\Retours humains .docx` + pack 002 | `docs/review/selarl_human_returns_deep_audit_002_report_v1.md` + trois ecarts PV corriges |
| SELARL-CLOSING-PACK-003 | DONE | Regenerer le pack SELARL apres audit retours humains | correction PV `DOC-004` + correction `DOC-006` | `artifacts/selarl_closing_pack_003/` + `docs/review/selarl_closing_pack_003_report_v1.md` |
| SELARL-THREE-SOURCE-AUDIT-004 | DONE | Verifier SELARL avec les trois sources : document a generer, retours modele, retour humain | `Documents_a_generer_par_cas.docx` + NotebookLM/reconciliation + `Retours humains .docx` + pack 003 | ecart `DOC-003` trouve : `SELARL SELARL MARTIN` dans la procuration |
| SELARL-CLOSING-PACK-004 | DONE | Corriger `DOC-003` et regenerer le pack SELARL | audit trois sources + correction procuration | `artifacts/selarl_closing_pack_004/` + `docs/review/selarl_closing_pack_004_report_v1.md` + `docs/review/selarl_three_source_alignment_004_report_v1.md` |
| SELARL-CLOSING-SMOKE-001 | DONE | Relancer smoke final SELARL simple/regime | corrections validees | ruff OK + tests cibles OK + `pytest -q` 416 passes + manifest pack 004 sans echec |
| SELARL-HUMAN-RETURNS-DEEP-AUDIT-005 | DONE | Reverifier les retours humains sur le pack 004 | `C:\Users\Gad\Downloads\Retours humains .docx` + pack 004 | `docs/review/selarl_human_returns_deep_audit_005_report_v1.md` + 116 controles cibles OK + nuance article 8 statuts dentiste documentee |
| SELARL-FINAL-ASSOCIE-VALIDATION-001 | READY | Faire valider le pack final par l'associe | pack 005 controle puis amende apres retours humains 006 | `docs/review/selarl_final_validation_001_brief_v1.md` pret ; attendre verdict associe par ecarts concrets |
| SELARL-HUMAN-RETURNS-006-TRIAGE-001 | DONE | Enregistrer et classer les nouveaux retours humains SELARL | message Gad 2026-06-02 | `docs/review/selarl_human_returns_006_raw_v1.md` + `docs/review/selarl_human_returns_triage_006_report_v1.md` + tickets corrections 006 |
| SELARL-RETURNS-006-STATUTS-001 | DONE | Corriger les retours 006 sur statuts SELARL | rapport triage 006 + `DOC-016`/`DOC-017` | mentions matrimoniales, accord associe, annexe page suivante, tiret `Ouverture...`, tests statuts OK + `docs/review/selarl_returns_006_statuts_001_report_v1.md` |
| SELARL-RETURNS-006-DNC-001 | DONE | Corriger la declaration de non condamnation et le champ `au` ville naissance | rapport triage 006 + `DOC-001` | naissance `a/au`, champ `ville_naissance_article_au`, fronts/wizard/document unitaire propages, tests DNC/front OK + `docs/review/selarl_returns_006_dnc_001_report_v1.md` |
| SELARL-RETURNS-006-PV-001 | DONE | Corriger le PV nomination gerant | rapport triage 006 + `DOC-004` | forme juridique redigee en header, capital `Au capital de ...`, tests PV/front OK + `docs/review/selarl_returns_006_pv_001_report_v1.md` |
| SELARL-RETURNS-006-PROCURATION-001 | DONE | Corriger la procuration | rapport triage 006 + `DOC-003` | phrase `demeurant..., agissant...` conforme, adresses CP avant ville, tests procuration OK + `docs/review/selarl_returns_006_procuration_001_report_v1.md` |
| SELARL-RETURNS-006-CONJOINT-LETTERS-001 | DONE | Corriger les lettres regime communautaire | rapport triage 006 + `DOC-005`/`DOC-006` | adresse conjoint derivee, forme juridique redigee, date renonciation retiree, tests regime/front OK + `docs/review/selarl_returns_006_conjoint_letters_001_report_v1.md` |
| SELARL-RETURNS-006-ORDRE-001 | DONE | Corriger la demande d'inscription a l'ordre | rapport triage 006 + `DOC-034` | conseil departemental compose depuis profession + departement, tests ordre/front OK + `docs/review/selarl_returns_006_ordre_001_report_v1.md` |
| SELARL-RETURNS-006-FRONT-VARIABLES-001 | DONE | Simplifier variables/front SELARL selon retour 006 | rapport triage 006 + clean front Track B | constantes 99 ans / 4 exemplaires / associe / date du jour, nationalite portugaise, reuse siege=adresse perso + `docs/review/selarl_returns_006_front_variables_001_report_v1.md` |
| SELARL-RETURNS-006-ADDRESS-SIGNATURE-001 | DONE | Appliquer les regles transversales adresses/signatures du retour 006 | rapport triage 006 + pack SELARL | CP avant ville + suppression encadres signature controles par tests + `docs/review/selarl_returns_006_address_signature_001_report_v1.md` |
| SELARL-CLOSING-PACK-005 | DONE | Regenerer un nouveau pack SELARL apres corrections 006 | tickets `SELARL-RETURNS-006-*` DONE | `artifacts/selarl_closing_pack_005/` + manifest 0 echec + `docs/review/selarl_closing_pack_005_report_v1.md` |
| SELARL-HUMAN-RETURNS-DEEP-AUDIT-006 | DONE | Auditer les retours 006 sur le pack 005 | pack 005 | Rapport historique `docs/review/selarl_human_returns_deep_audit_006_report_v1.md` ; a lire avec l'amendement `SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001` |
| SELARL-EXTERNAL-RECHECK-RETURNS-006-001 | DONE | Refaire une reverification presque exterieure des derniers retours humains 006 | retours 006 bruts + pack 005 + front propre actif + tests | `docs/review/selarl_external_recheck_returns_006_pack_005_report_v1.md` ; extraction DOCX/XML 4 scenarios 0 failure ; tests cibles 84 passes ; reserve legacy explicite |
| SELARL-RETURNS-006-CONJOINT-ADDRESS-FRONT-LOCK-001 | DONE | Verrouiller toutes les branches front contre la saisie adresse conjoint | retour Gad/associe 2026-06-02 : adresse conjoint encore visible en regime communautaire | `docs/review/selarl_returns_006_conjoint_address_front_lock_001_report_v1.md` ; clean front + assistant metier + schema `DOC-006` alignes ; tests anti-regression 6 passes ; ruff cible OK ; smokes larges bloques par permissions temporaires Windows |
| SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001 | DONE | Generaliser les incidents associe et reverifier toutes les surfaces retours 006 | demande Gad 2026-06-03 + exemples associe : signatures, DOC-002 duree, adresse conjoint front | `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md` ; vrai ecart `DOC-002` corrige en `pour 99 ans` ; pack 005 regenere localement ; regression 187 tests OK ; ruff cible OK |
| SELARL-RETURNS-007-SIGNATURE-DNC-001 | DONE | Traiter les nouveaux retours associe signatures/DNC | message Gad 2026-06-03 : carres de signature encore visibles, ville naissance DNC contestee, adresse conjoint OK | `docs/review/selarl_associe_returns_007_signature_dnc_report_v1.md` ; signatures sans table sur DOC-001/002/003 ; DNC ville naissance verifiee dans pack 005 regenere ; tests 23 passes + regression SELARL 187 passes + ruff OK |
| SELARL-RETURNS-008-MAIN-AUDIT-FIX-001 | DONE | Corriger les ecarts trouves sur `main` apres audit retours associe SELARL | audit Gad 2026-06-03 sur `main` + retours associe 006/007 + cas separation de biens | `docs/review/selarl_returns_008_main_audit_fix_report_v1.md` ; separation de biens front/contexte/statuts corrigee ; libelles medecin accentues ; capital rendu `1 000` ; generation reelle 3 scenarios OK ; audit DOCX 32 controles OK ; ruff OK ; pytest bloque par ACL temporaires Windows |
| SELARL-CANONICAL-CLOSE-001 | BLOCKED | Clore le statut canonique SELARL simple/regime | validation finale associe ou corrections traitees | bloque jusqu'au verdict associe sur pack 005 |
| SELARL-NEXT-SUBCASE-SELECTION-001 | READY | Choisir le prochain sous-cas SELARL complexe | `SPRINT_SELARL_CLOSING_V1.md` + arbitrage Gad | un seul sous-cas choisi ou report explicite |
| NAOMIE-RUNTIME-FAILSAFE-001 | DONE | Corriger l'accueil Naomi quand un nouveau chat repond encore trop vaguement | captures 2026-06-01 + incidents `bonjour` / ancien ticket NotebookLM | `NAOMIE_RUNTIME_PROTOCOL_V1.md` + consigne prioritaire en tete de `AGENTS.md` + sprint SELAS aligne sur Phase 3 NotebookLM + ancien libelle `SELAS-NOTEBOOKLM-RECONCILIATION-001` declare obsolete |
| PM-PRODUCT-GUARDRAIL-001 | DONE | Installer le gate produit / métier obligatoire avant tout développement | demande utilisateur 2026-06-01 + workflow projet + handoff | doctrine globale `GLOBAL_CODEX_PRODUCT_GUARDRAIL_V1.md` + protocole local `PRODUCT_GUARDRAIL_PROTOCOL_V1.md` + AGENTS/workflow/handoff/master plan mis à jour + mémoire de reprise alignée |
| SELARL-CANONICAL-STATUS-001 | DONE | Consolider l'état SELARL canonique avant tout nouveau dev | gate produit + backlog/playbook/factory SELARL + dernier état Track B | `docs/project/SELARL_CANONICAL_STATUS_V1.md` + `NO-GO dev` pour extension complexe sans sous-cas choisi |
| COMPANY-TYPE-SPRINT-PLAYBOOK-001 | DONE | Formaliser le sprint par type d'entreprise pour Gad / Naomi / associe | demande utilisateur 2026-06-01 + methode SELARL + gate produit | `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` + workflow NotebookLM + boucle retour associe + pointers projet |
| COMPANY-TYPE-SPRINT-PLAYBOOK-002 | DONE | Completer le mode d'emploi reusable avec les apprentissages de cloture SELARL | pack 004 + audit trois sources + retours humains 005 + demande Gad | playbook/orchestrateur/protocoles Naomi alignes : trois sources, questions utiles seulement, pack actif, audit fidelite, retour associe par ecarts concrets, cloture `DONE/PARTIAL/BLOCKED` |
| REUSE-AUDIT-AGENT-PROTOCOL-001 | DONE | Formaliser le sous-agent de reutilisation SELARL/global pour les prochains sprints | demande utilisateur 2026-06-01 + synthese sous-agent Reuse Auditor + registres globaux | `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md` + playbook/workflow/handoff/master plan mis a jour + audit reuse obligatoire avant `GO dev` |
| NAOMIE-GITHUB-ONBOARDING-001 | DONE | Ecrire le mode d'emploi GitHub / branche pour Naomi | demande utilisateur 2026-06-01 + remote GitHub + branche courante `track-b/clean-rebuild` | `docs/project/NAOMIE_GITHUB_ONBOARDING_V1.md` + regle `1 sprint = 1 branche = 1 type d'entreprise` + Git/commandes geres par Codex, pas par Naomi |
| NAOMIE-LEARNING-MENTOR-001 | DONE | Ajouter le sous-agent Professeur Naomi pour l'apprentissage | demande utilisateur 2026-06-01 + synthese sous-agent Professeur Naomi | `docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md` + onboarding/playbook/workflow/handoff/master plan mis a jour + `GO pedagogie`, `NO-GO dev` |
| SPRINT-ORCHESTRATOR-PROTOCOL-001 | DONE | Installer l'orchestrateur de sprint pour empecher le demarrage direct en dev/prod | demande utilisateur 2026-06-01 + incident lancement SELAS sans NotebookLM | `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` + workflow Naomi/Gad raccorde + `NO-GO dev` par defaut |
| SPRINT-SELAS-V1-001 | IN_PROGRESS | Suivre le sprint SELAS pour Naomi en phase NotebookLM | choix logique Codex valide par Gad + methode SELARL + protocols sprint/reuse | `docs/sprints/SPRINT_SELAS_V1.md` + phase 3 NOTEBOOKLM + Prompt 01 a donner apres identification de Naomi + aucun dev autorise |
| NAOMIE-BRANCH-CREATION-001 | DONE | Creer et pousser la branche de sprint de Naomi | checkpoint documentaire publie + type d'entreprise choisi : SELAS | branche distante `codex/naomie-selas-sprint` creee depuis le checkpoint Track B |
| NAOMIE-HELLO-TRIGGER-001 | DONE | Corriger le declencheur d'accueil Naomi apres reponse generique incorrecte | incident 2026-06-01 : reponse "tu veux qu'on attaque quoi..." | trigger explicite dans `AGENTS.md`, orchestrateur, sprint SELAS et workflow ; branche a verifier avant toute suite |
| SELAS-NOTEBOOKLM-PROMPT-LOOP-001 | DONE | Formaliser la boucle NotebookLM SELAS par prompts courts | demande Gad 2026-06-01 + limite caracteres NotebookLM + besoin iteration Naomi | `SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md` + `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` + workflow mis a jour |
| SELAS-NOTEBOOKLM-START-TRIGGER-001 | DONE | Corriger le cas ou Naomi dit qu'elle veut lancer/reprendre le sprint SELAS/CELAS | incident 2026-06-01 : lancement sprint interprete comme production/dev | `lancer sprint` = lancer uniquement le sous-sprint NotebookLM ; audit/matrice/dev/prod interdits avant journal NotebookLM suffisant |
| PROJECT-CONTROL-TOWER-001 | DONE | Installer la tour de controle chef de projet globale | demande Gad 2026-06-01 : Codex doit prendre en main tout le projet et savoir ou en est chaque sprint | `PROJECT_CONTROL_TOWER_V1.md` + ordre de reprise mis a jour + cycle standard unique par type d'entreprise + etat courant SELARL/SELAS |
| MAIN-NAOMIE-TRIGGER-001 | DONE | Corriger le cas ou un nouveau chat Naomi demarre sur `main` | capture 2026-06-01 : `bonjour` / `je suis naomi` repond de maniere generique sur `main` | fail-safe `main` dans `AGENTS.md` et `PROJECT_CONTROL_TOWER_V1.md`, kit gouvernance pousse sur `main` |
| TRACK-B-PREVIEW-VALIDATION-AND-CHECKPOINT-009 | DONE | Valider la preview clean front et creer un checkpoint Git local | ticket 008 + clean front Track B + worktree non commite | preview HTTP 200 sans Start-Process + mode dentiste multi PARTIAL verifie + validations minimales + commit checkpoint local sans push |
| TRACK-B-SELARL-DENTIST-MULTI-ASSOCIES-STATUTS-PARTIAL-008 | DONE | Implementer une version PARTIAL de SELARL dentiste multi-associes simple | retours humains + contrat multi-associes 006 + lock dentiste 003 + rapport DOC-004 007 + backlog SELARL | front clean mode dentiste PARTIAL + contexte multi + DOC-004/DOC-016 smoke + rapport 008 + tests/ruff/HTTP |
| TRACK-B-SELARL-MULTI-ASSOCIES-DOC004-LIMITED-007 | DONE | Implementer le sous-cas SELARL multi-associes simple limite a DOC-004 | contrat multi-associes 006 + retours humains + locks PV/gouvernance | front clean mode limite + contexte associes/president + DOC-004 smoke + rapport 007 + tests/ruff/HTTP |
| TRACK-B-SELARL-MULTI-ASSOCIES-SOURCE-CONTRACT-006 | DONE | Produire le contrat source SELARL multi-associes / president de seance / plusieurs gerants | backlog/factory SELARL + human reference lock + reports 003/004/005 + retours humains + specs PV/statuts/cession/SCM | `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md` + matrice readiness GO/NO-GO + recommandation unique bornee |
| TRACK-B-SELARL-MEDECIN-REGIME-COMMUNAUTAIRE-005 | DONE | Industrialiser la SELARL medecin unipersonnelle avec regime communautaire | lock medecin 004 + lock dentiste 003 + human reference lock + backlog/factory + DOC-005 | rapport 005 + tests ciblant DOC-005/conjoint + smoke medecin regime + ruff/HTTP |
| TRACK-B-SELARL-MEDECIN-LINE-BY-LINE-LOCK-004 | DONE | Tenter le lock ligne par ligne DOC-017 SELARL medecin | source DOCX medecin + backlog/factory + rapport dentiste line-by-line | rapport 004 + test source-line-by-line DOC-017 + smoke medecin + tests/ruff/HTTP |
| TRACK-B-SELARL-ROLLOUT-NEXT-CASE-001 | DONE | Choisir et lancer le prochain cas SELARL apres le lock dentiste | backlog/factory/reference lock/rapport line-by-line + clean front Track B | matrice cas restants + choix SELARL medecin standard GO + smoke DOCX/ZIP + tests/ruff/HTTP |
| TRACK-B-SELARL-DENTIST-LINE-BY-LINE-LOCK-003 | DONE | Verrouiller la SELARL dentiste ligne par ligne contre la référence humaine | `Retours humains .docx` + `SELARL_HUMAN_REFERENCE_LOCK_V1.md` + clean front Track B | rapport line-by-line + DOC-003/DOC-004 fermés + DOC-016 articles 1-34 LOCKED + tests/smoke/HTTP |
| TRACK-B-SELARL-HUMAN-REFERENCE-LOCK-002 | DONE | Verrouiller la conformité humaine SELARL sur les documents prioritaires | `Retours humains .docx` du 31/05/2026 + clean front Track B + arbitrages SELARL | `SELARL_HUMAN_REFERENCE_LOCK_V1.md` + alignements DOC-002/DOC-001/DOC-005/DOC-004/DOC-016 + tests/smoke/HTTP |
| TRACK-B-SELARL-PRODUCTION-PACK-001 | DONE | Transformer la SELARL en premier pack de production Track B | retours humains recents + arbitrages actes + clean front Track B + specs SELARL | corrections DOC-001/DOC-002/DOC-004/DOC-005/DOC-016 + variables president de seance + factory/backlog SELARL + tests/smoke/HTTP |
| TRACK-B-SELARL-TEST-DATA-PREFILL-001 | DONE | Ajouter un pre-remplissage aleatoire coherent au clean front SELARL | demande utilisateur du 2026-05-27 + clean front SELARL V1 | bouton sous Type de dossier + donnees SELARL coherentes + generation/test rapide + ruff/test/HTTP 200 + push |
| TRACK-B-SELARL-DOWNLOAD-UX-001 | DONE | Rendre le dossier genere telechargeable depuis le clean front | retour testeur du 2026-05-27 + capture console + clean front SELARL V1 | boutons de telechargement Streamlit ZIP et DOCX apres generation + test AppTest + ruff/test/HTTP 200 |
| TRACK-B-SELARL-UX-FOLLOWUP-001 | DONE | Corriger les retours UI SELARL apres test local | retour utilisateur du 2026-05-27 + clean front SELARL V1 | dates JJ/MM/AAAA sans borne Streamlit + situation matrimoniale en liste + valeur nominale calculee + labels ordre clarifies + ruff/test/HTTP 200 |
| TRACK-B-SELARL-UX-DEDUP-RECONCILIATION-001 | DONE | Corriger l'UX SELARL V1 apres reconciliation associe / NotebookLM | retours associe + NotebookLM + audit dedup + branche track-b/clean-rebuild | front_app SELARL sans doubles saisies implicites + derivations + tests cibles + lancement local |
| TRACK-B-FRONT-ARCHITECTURE-RESET-001 | DONE | Refonder le chemin front Track B propre et isoler le legacy | arbitrage produit front + fondations front_data + branche track-b/clean-rebuild | nouveau front_app clean + rapport + tests + lancement local |
| TRACK-B-SELARL-SOURCE-OF-TRUTH-CONTRACT-001 | DONE | Figer le contrat metier-front SELARL V1 depuis les sources de verite | sources SELARL V2/V3 + reponse metier + NotebookLM + specs/revues + branche track-b/clean-rebuild | `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md` + conclusion GO bornee |
| TRACK-B-SELARL-VERTICAL-SLICE-IMPLEMENT-001 | DONE | Brancher la vraie vertical slice SELARL V1 dans le front_app clean | contrat `TRACK_B_SELARL_FRONT_CONTRACT_V1.md` + moteur documentaire existant + branche track-b/clean-rebuild | slice SELARL V1 bornee dans `front_app` + generation DOCX/ZIP + tests cibles |
| TRACK-B-SELARL-FIELD-DEDUP-AUDIT-001 | DONE | Auditer les doublons de champs utilisateur dans le clean front SELARL V1 | front_app SELARL V1 + contrat metier-front + branche track-b/clean-rebuild | rapport `docs/review/track_b_selarl_field_dedup_audit_001_report_v1.md` + conclusion PASS |
| PM-001 | DONE | Installer la mémoire projet dans le repo | source de vérité + specs Lot 1 | docs/project/* |
| PM-002 | DONE | Vérifier et compléter la mémoire projet opérationnelle | AGENTS.md + docs/project/* | docs/project complétés + artefact parasite traité |
| PM-003 | DONE | Installer le kit de reprise nouveau ChatGPT / Codex | mémoire projet existante | handoff + last state + prompt nouveau chat |
| DOC-001 | DONE | Implémenter la déclaration de non-condamnation | source doc + spec Lot 1 | générateur + tests + MAJ doc |
| DOC-003 | DONE | Implémenter la procuration | source doc + spec Lot 1 | générateur + tests + MAJ doc |
| DOC-002 | DONE | Implémenter l'autorisation de domiciliation | source doc + spec Lot 1 + décision V1 adresse libre | générateur + tests + MAJ doc |
| ORCH-001 | DONE | Brancher l'orchestrateur Lot 1 | générateurs DOC-001/002/003 | service orchestrateur + tests |
| PM-004 | DONE | Intégrer l'arbre moteur document-centré V1 dans la mémoire projet | arbre moteur document-centré V1 | board + dernier état mis à jour |
| PM-005 | DONE | Intégrer le dictionnaire canonique des variables V1 dans la mémoire projet | dictionnaire canonique des variables V1 | board + dernier état mis à jour |
| SMOKE-001 | DONE | Smoke test réel Lot 1 via orchestrateur | contexte exemple Lot 1 + orchestrateur | 3 DOCX générés + docs projet mises à jour |
| VAR-001 | DONE | Ajouter une table de mapping document -> variables canoniques | arbre documentaire V1 + dictionnaire canonique V1 + specs | table de mapping document -> variables canoniques |
| PM-006 | DONE | Intégrer le cadrage métier PV nomination gérant V1 dans la mémoire projet | cadrage Lot 2 PV nomination gérant | board + dernier état mis à jour |
| SPEC-PV-001 | DONE | Formaliser la spec canonique du PV nomination gérant à partir du cadrage V1 | cadrage Lot 2 + arbre documentaire V1 + dictionnaire canonique V1 + table de mapping V1 | spec canonique écrite, blocs conditionnels, mapping variables, règles `associes[]`, points ouverts |
| SPEC-TEXTE-PV-001 | DONE | Stabiliser le texte canonique et les variantes du PV nomination gérant | spec canonique PV nomination gérant V1 + source Lot 2 | spec textuelle détaillée, variantes structurelles, wording à valider, critères avant code |
| CODE-PV-001 | DONE | Implémenter le générateur canonique PV nomination gérant | spec canonique V1 + spec texte V1 + source Lot 2 | générateur PV from-scratch + tests associes[]/genre/emprunt + MAJ doc |
| REVIEW-PV-001 | DONE | Préparer la revue humaine du PV nomination gérant généré | contexte exemple Lot 2 + générateur PV existant | DOCX régénéré + aperçu texte + checklist de revue humaine |
| SPEC-RENDER-001 | DONE | Spécifier une couche de rendu DOCX commune | générateurs DOC-001/002/003 + PV nomination gérant + specs existantes | spec technique render style system V1 |
| RENDER-STYLE-001 | DONE | Implémenter la couche de rendu DOCX commune | spec render style system V1 + générateurs existants | helpers communs + générateurs migrés + tests + smoke DOCX |
| ORCH-L2-PV-001 | DONE | Brancher le PV nomination gérant dans l'orchestrateur | générateur PV + specs Lot 2 + décisions de sélection | catalogue + registre orchestrateur + tests ciblés |
| SMOKE-ORCH-L2-001 | DONE | Smoke test réel orchestrateur Lot 2 positif SCI / négatif SAS | contextes exemples Lot 2 + orchestrateur | DOCX générés, PV présent en SCI et absent en SAS, revue smoke |
| FIX-PV-RENDER-001 | DONE | Restaurer la structure visuelle essentielle du PV nomination gérant | source Lot 2 + specs PV + render style system V1 | listes à tirets, titre, intertitres, italique votes, smoke DOCX |
| ANALYSE-ORDRE-001 | DONE | Cadrer Demande d'inscription à l'ordre et batch régime communautaire Lot 2 | sources Lot 2 ordre + régime communautaire + référentiels V1 | cadrages delivery + tickets SPEC-ORDRE-001/SPEC-RC-001 READY |
| ARBITRAGE-SOURCES-001 | DONE | Réparer le manifest d'import sources et arbitrer les placements V1 | source truth + raw_drive_dump + source_documents + décisions métier | docs projet 10/11/12/13 + prochain ticket placement |
| PLACEMENT-HIGH-001 | DONE | Déplacer physiquement dans source_documents uniquement les cas HIGH validés | plan de placement V1 + décisions d'arbitrage sources V1 | placement HIGH confirmé no-op + journal d'exécution |
| SPEC-ORDRE-001 | DONE | Formaliser la spec canonique Demande d'inscription à l'ordre | cadrage ordre V1 + source Lot 2 + référentiels V1 + variantes raw dump | spec canonique écrite, variantes comparées, mapping variables, accords, points ouverts |
| SPEC-TEXTE-ORDRE-001 | DONE | Stabiliser le texte canonique et les variantes de Demande d'inscription à l'ordre | spec canonique ordre V1 + variantes SELARL/SELAS/SPFPL/SPFPL apport/SCM | spec texte détaillée, tronc commun, overlays, blocs conditionnels/manuels, règles de blocage avant code |
| CODE-ORDRE-001 | DONE | Implémenter le générateur canonique Demande d'inscription à l'ordre | spec canonique ordre V1 + spec texte ordre V1 + source Lot 2 + variantes raw dump | générateur ordre from-scratch + tests overlays/dérogation/mandataire + MAJ doc |
| SPEC-RC-001 | DONE | Formaliser la spec canonique batch régime communautaire | cadrage régime communautaire V1 + deux sources Lot 2 + référentiels V1 | spec canonique batch, spec texte batch, mapping commun, règles de génération, points ouverts |
| CODE-RC-001 | DONE | Implémenter le batch régime communautaire v1 | specs canonique et texte régime communautaire V1 + sources Lot 2 + variantes raw dump | deux générateurs DOCX from-scratch + sélection orchestrateur + tests ciblés + MAJ doc |
| SPEC-SPFPL-001 | DONE | Formaliser le batch SPFPL spécifique | source vérité + raw dump SPFPL | spec canonique SPFPL V1 |
| SPEC-DEROG-001 | DONE | Formaliser la famille dérogations | source vérité + raw dump dérogations | spec canonique dérogations V1 |
| SPEC-CESSION-BAIL-001 | DONE | Formaliser les blocs cession cabinets et bail/appel de fonds | source vérité + raw dump cession | specs canoniques cession cabinets + bail/appel de fonds V1 |
| SYNC-SPECS-001 | DONE | Synchroniser les specs parallèles dans main | branches SPEC-RC/SPFPL/DEROG/CESSION | specs intégrées + pilotage aligné |
| SPEC-TEXTE-BAIL-APP-001 | DONE | Stabiliser le texte canonique bail / appel de fonds | spec canonique bail/appel de fonds V1 + sources raw dump | spec texte V1 bail / appel de fonds |
| SPEC-TEXTE-CESSION-CAB-001 | DONE | Stabiliser le texte canonique cession cabinets | spec canonique cession cabinets V1 + sources raw dump | spec texte V1 cession cabinets |
| SPEC-TEXTE-DEROG-001 | DONE | Stabiliser le texte canonique dérogations | spec canonique dérogations V1 + sources raw dump | spec texte V1 dérogations |
| SPEC-TEXTE-SPFPL-001 | DONE | Stabiliser le texte canonique SPFPL spécifique | spec canonique SPFPL V1 + sources raw dump | spec texte V1 SPFPL |
| SYNC-TEXTE-SPECS-001 | DONE | Synchroniser les specs texte parallèles dans main | branches SPEC-TEXTE bail/appel, cession, dérogations, SPFPL | specs texte intégrées + pilotage aligné |
| SYNC-ARBITRAGES-001 | DONE | Synchroniser les arbitrages parallèles dans main | branches ARBITRAGE cession, dérogations, SPFPL | arbitrages intégrés + pilotage aligné |
| CODE-BAIL-APP-001 | DONE | Implémenter le mini-batch bail / appel de fonds | specs canonique et texte bail/appel V1 + arbitrages de blocage V1 | générateurs DOCX + tests ciblés + MAJ doc |
| ARBITRAGE-CESSION-001 | DONE | Arbitrer les points bloquants cession cabinets avant code | spec texte cession cabinets V1 + points ouverts | décisions métier tracées pour acte/compromis, medical/dentaire et anomalies source |
| ARBITRAGE-DEROG-001 | DONE | Arbitrer les points bloquants dérogations avant code | spec texte dérogations V1 + sources Lot 03 | décisions métier sur formulaires préremplis, rôles et sources legacy |
| ARBITRAGE-SPFPL-001 | DONE | Arbitrer les points bloquants SPFPL avant code | spec texte SPFPL V1 + points ouverts | décisions métier cession/apport, commissaire, souscripteurs et sources |
| CODE-CESSION-CAB-001 | DONE | Implémenter la famille cession cabinets | specs canonique/texte cession cabinets V1 + arbitrage V1 | générateurs DOCX + blocages explicites + tests ciblés + MAJ doc |
| RESUME-CODE-CESSION-CAB-001 | DONE | Reprendre proprement CODE-CESSION-CAB-001 sur main synchronisé | main à jour Lot 03/Lot 05 + specs/arbitrages cession V1 | reprise cadrée de la famille cession cabinets |
| PREP-DEROG-001 | DONE | Préparer les sources dérogations avant code | arbitrages dérogations V1 + raw dump + plan de placement | sources Lot 03 placées + rapport de préparation |
| CODE-DEROG-CORE-001 | DONE | Implémenter le cœur dérogations | specs/arbitrages dérogations V1 + PREP-DEROG-001 | générateurs DOCX dérogations cœur + blocages explicites + tests |
| CODE-SPFPL-AGR-INFO-001 | DONE | Implémenter le sous-batch SPFPL agrément / note d'information | specs canonique/texte SPFPL V1 + arbitrage V1 | générateurs DOCX ciblés + tests + sources Lot 05 placées |
| CODE-SPFPL-CORE-001 | DONE | Implémenter le cœur SPFPL restant | specs canonique/texte SPFPL V1 + arbitrage V1 + sources préparées | générateurs SPFPL ciblés + blocages explicites + tests |
| PREP-STATUTS-001 | DONE | Préparer les sources statuts avant spécification/code | source vérité + raw dump + plan de placement/arbitrage sources | sources statuts cadrées + écarts documentés |
| SPEC-STATUTS-SEL-001 | DONE | Spécifier les statuts SEL d'exercice | préparation statuts V1 + sources Lot 04 SELARL/SELAS | spec canonique + spec texte avant code |
| SPEC-STATUTS-SPFPL-001 | DONE | Spécifier les statuts SPFPL | préparation statuts V1 + sources Lot 04 SPFPL cession/apport | spec canonique + spec texte avant code |
| SPEC-STATUTS-CIVILS-001 | DONE | Spécifier les statuts civils | préparation statuts V1 + sources Lot 04 SCI/SCI IRIS/SCM/SCS | spec canonique + spec texte avant code |
| SPEC-STATUTS-SAS-001 | DONE | Spécifier les statuts SAS | préparation statuts V1 + source Lot 04 SAS | spec canonique + spec texte avant code |
| SYNC-STATUTS-SPECS-001 | DONE | Synchroniser les specs statuts parallèles dans main | branches statuts SAS/SPFPL/SEL/CIVILS | specs intégrées + pilotage aligné |
| CODE-STATUTS-SAS-001 | DONE | Implémenter les statuts SAS | specs statuts SAS V1 + blocages explicites | générateur DOCX + tests ciblés + MAJ doc |
| CODE-STATUTS-SPFPL-001 | DONE | Implémenter les statuts SPFPL cession/apport | specs statuts SPFPL V1 + blocages explicites | générateurs DOCX + tests ciblés + MAJ doc |
| ARBITRAGE-STATUTS-SEL-001 | DONE | Arbitrer les points bloquants statuts SEL avant code | specs statuts SEL V1 + points ouverts | décisions pluralité associés, SELAS et wording |
| ARBITRAGE-STATUTS-CIVILS-001 | DONE | Arbitrer les points bloquants statuts civils avant code | specs statuts civils V1 + points ouverts | décisions SCI/SCI IRIS/SCM/SCS avant code |
| SYNC-STATUTS-CODE-ARB-001 | DONE | Synchroniser code statuts SAS/SPFPL et arbitrage SEL dans main | branches code/arbitrage statuts | commits intégrés + pilotage réaligné |
| CODE-STATUTS-SEL-001 | DONE | Implémenter les statuts SEL d'exercice | specs statuts SEL V1 + arbitrages SEL V1 | générateur(s) DOCX + tests ciblés + MAJ doc |
| CODE-STATUTS-CIVILS-CORE-001 | DONE | Implémenter le cœur des statuts civils | specs statuts civils V1 + arbitrages civils V1 | générateurs SCS/SCI/SCI IRIS + tests ciblés + MAJ doc |
| FIX-STYLE-LETTERS-001 | DONE | Corriger les écarts de style prioritaires des lettres | blueprint style batch V1 + générateurs existants | rendu lettres harmonisé + tests/smoke ciblés |
| RESUME-FIX-STYLE-LETTERS-001 | DONE | Reprendre proprement les corrections de style lettres | blueprint style batch V1 + état main synchronisé | reprise cadrée de FIX-STYLE-LETTERS-001 absorbée |
| ARBITRAGE-STATUTS-SCM-001 | DONE | Arbitrer les points bloquants statuts SCM avant code | specs statuts civils V1 + anomalies SCM documentées | décisions SCM avant spec/code |
| PREP-SCM-SAT-001 | DONE | Préparer le périmètre SCM et satellites | arbitrage SCM + sources disponibles | cadrage sources et périmètre exploitable |
| SPEC-SAS-SATELLITES-001 | DONE | Spécifier les satellites SAS | specs statuts SAS V1 + sources satellites | spec canonique + spec texte avant code |
| CODE-OPTION-IS-001 | DONE | Implémenter la lettre option IS | specs/arbitrages applicables + source reçue | générateur DOCX + tests ciblés |
| PREP-ACTE-ACTIONS-001 | DONE | Préparer les sources acte de cession d'actions | arbitrages SPFPL + sources disponibles | source confirmée ou blocage documenté |
| RESUME-ARBITRAGE-STATUTS-CIVILS-001 | DONE | Reprendre proprement l'arbitrage des statuts civils | specs statuts civils V1 + état main synchronisé | remplacé par l'arbitrage civils V1 absorbé |
| STYLE-ANALYSE-BATCH-001 | DONE | Analyser le style documentaire en batch avant harmonisation | générateurs/statuts disponibles + besoins de rendu | cadrage style batch + points d'arbitrage |
| SYNC-STYLE-CIVILS-001 | DONE | Synchroniser style batch et arbitrage civils dans main | branches style/arbitrage civils | commits intégrés + pilotage réaligné |
| SYNC-STATUTS-SEL-CIVILS-001 | DONE | Synchroniser code statuts SEL et arbitrage civils dans main | branches code SEL/arbitrage civils | commits intégrés + pilotage réaligné |
| SYNC-WAVE-005 | DONE | Synchroniser SCM, satellites SAS, option IS et préparation legacy dans main | branches CODE-OPTION-IS/PREP-SCM-SAT/ARBITRAGE-STATUTS-SCM/SPEC-SAS-SATELLITES/PREP-ACTE-ACTIONS | commits intégrés + pilotage réaligné |
| SYNC-WAVE-006 | DONE | Synchroniser la vague tardive Lot 04 / Lot 05 dans main | branches style/civils/SAS satellites/conversions/spec SCM | commits intégrés + pilotage réaligné |
| SYNC-WAVE-007 | DONE | Synchroniser la vague SCM et acte actions dans main | branches statuts SCM / liste dépenses / satellites SCM / spec acte actions | commits intégrés + pilotage réaligné |
| SYNC-WAVE-008 | DONE | Synchroniser la vague SCM style review et acte actions dans main | branches acte actions / sources SCM cession / reviews / audits / style / spec SCM cession | commits intégrés + pilotage réaligné |
| CODE-STATUTS-SCM-001 | DONE | Implémenter les statuts SCM | specs statuts civils V1 + arbitrages SCM V1 | générateur DOCX + tests ciblés |
| CODE-SAS-SATELLITES-001 | DONE | Implémenter les satellites SAS | specs satellites SAS V1 + sources confirmées | générateurs DOCX + tests ciblés |
| SPEC-SCM-SATELLITES-001 | DONE | Spécifier les satellites SCM | préparation SCM satellites V1 + sources confirmées | spec canonique + spec texte avant code |
| CONVERT-ACTE-ACTIONS-001 | DONE | Convertir ou remplacer la source acte de cession d'actions | audit source acte actions V1 | DOCX exploitable placé + préparation documentée |
| CONVERT-DEROG-SALARIEE-001 | DONE | Convertir ou remplacer la source dérogation salariée legacy | préparation dérogations V1 + source legacy `.doc` | blocage conversion documenté |
| PREP-SCM-LISTE-DEPENSES-CONVERT-001 | DONE | Convertir la source legacy liste dépenses communes SCM | source legacy Lot 05 SCM | DOCX exploitable + préparation documentée |
| CODE-SCM-SAT-DOCX-001 | DONE | Implémenter les satellites SCM DOCX hors liste dépenses | specs satellites SCM V1 + sources DOCX confirmées | générateurs DOCX + tests ciblés |
| SPEC-ACTE-ACTIONS-001 | DONE | Spécifier l'acte de cession d'actions SPFPL avant code | source DOCX convertie + préparation V1 | spec canonique + spec texte avant code |
| CODE-ACTE-ACTIONS-001 | DONE | Implémenter l'acte de cession d'actions SPFPL | specs acte actions V1 + source DOCX convertie | générateur DOCX + tests ciblés |
| PREP-SCM-CESSION-SOURCES-001 | DONE | Préparer les sources cession SCM | raw dump SCM cession + plan de placement | sources placées + préparation documentée |
| REVIEW-BATCH-LOT03-001 | DONE | Revoir le batch Lot 03 généré | générateurs Lot 03 + smoke DOCX disponibles | revue humaine juridique/visuelle documentée |
| REVIEW-BATCH-LOT04-001 | DONE | Revoir le batch Lot 04 généré | générateurs statuts + smoke DOCX disponibles | revue humaine juridique/visuelle documentée |
| AUDIT-REMAINING-SCOPE-001 | DONE | Auditer le périmètre restant | board + specs + registre moteur | audit restant documenté |
| STYLE-ANALYSE-LOT03-BATCH-001 | DONE | Analyser le style du batch Lot 03 avant harmonisation | générateurs Lot 03 intégrés + besoins de rendu | blueprint style Lot 03 |
| STYLE-ANALYSE-STATUTS-BATCH-001 | DONE | Analyser le style du batch statuts avant harmonisation | générateurs statuts intégrés + besoins de rendu | blueprint style statuts |
| SPEC-SCM-CESSION-BLOCK-001 | DONE | Spécifier le blocage cession SCM avant code | sources SCM cession disponibles + arbitrages SCM | spec canonique + spec texte de blocage |
| CODE-SCM-CESSION-BLOCK-001 | DONE | Implémenter le blocage cession SCM | specs SCM cession block V1 | blocage explicite historique + tests ciblés |
| CODE-SCM-LISTE-DEPENSES-001 | DONE | Implémenter la liste des dépenses communes SCM | source DOCX convertie + specs satellites SCM V1 | générateur DOCX + tests ciblés |
| SPEC-DEROG-SALARIEE-MANUAL-001 | DONE | Spécifier le traitement manuel de la dérogation salariée legacy | blocage conversion dérogation salariée V1 | spec manuelle ou décision de blocage documentée |
| FIX-STYLE-LOT03-BATCH-001 | DONE | Corriger les écarts de style prioritaires du batch Lot 03 | blueprint style Lot 03 | rendu Lot 03 harmonisé + tests ciblés |
| FIX-STYLE-STATUTS-BATCH-001 | DONE | Corriger les écarts de style prioritaires du batch statuts | blueprint style statuts | rendu statuts harmonisé + tests ciblés |
| REVIEW-BATCH-LOT05-001 | DONE | Revoir le batch Lot 05 généré | générateurs Lot 05 + smoke DOCX disponibles | revue humaine juridique/visuelle documentée |
| ARBITRAGE-SCM-CESSION-RESOLVE-001 | DONE | Arbitrer la résolution de la cession SCM | specs de blocage cession SCM + sources préparées + vague style/revue absorbée | décision de résolution avant code |
| SYNC-WAVE-010 | DONE | Synchroniser la vague finale moteur SCM cession dans main | branches arbitrage/code SCM cession | commits intégrés + pilotage final moteur aligné |
| FINAL-SCM-CESSION-WAVE-001 | DONE | Finaliser le bloc cession SCM et clôturer la vague moteur V1 | résolution SCM cession V1 + specs + six sources | DOC-031 à DOC-033 + tests + smoke + audit moteur |
| SYNC-CLOSE-AUDIT-001 | DONE | Synchroniser l'audit de clôture moteur V1 dans main | `origin/codex/close-motor-audit-001` @ `0139202b170531fd628f25811c55855a2512acc0` | merge de synchronisation + audit présent + pilotage aligné |
| RECONCILE-MOTOR-CLOSE-001 | DONE | Réconcilier et clôturer le moteur DOCX V1 | audits 16/17 + fondation 18 + catalogue/orchestrateur | DOC-001 à DOC-043 alignés + audits conclusifs + tests |
| PDF-BACKEND-001 | DONE | Implémenter le backend d'export PDF V1 | moteur DOCX clos + fondation phase 18 | backend PDF best-effort + tests + smoke DOCX vers PDF |
| UI-FLOW-001 | DONE | Cadrer le flux UI Streamlit V1 | moteur DOCX clos + fondation phase 18 | référentiel de flux UI V1 |
| UI-OCCURRENCES-001 | DONE | Cadrer les occurrences documentaires affichables en UI | registre moteur DOC-001 à DOC-043 | référentiel occurrences UI V1 |
| UI-FORM-SCHEMA-001 | DONE | Cadrer le schéma formulaire UI V1 | flux UI + occurrences UI | schéma formulaire UI V1 |
| RECIPE-FRAME-001 | DONE | Cadrer la recette finale V1 | moteur DOCX clos + fondations UI/PDF/ZIP | framework de recette finale V1 |
| SYNC-POST-MOTOR-UI-001 | DONE | Synchroniser la fondation UI/PDF/recette dans main | branches UI/PDF/recette listées | commits intégrés + pilotage aligné |
| UI-CORE-001 | DONE | Implémenter le cœur UI Streamlit V1 | UI flow + occurrences + form schema + backend PDF | superseded / remplacé par `UI-PDF-ZIP-INTEGRATION-001` |
| RESUME-ZIP-BACKEND-001 | DONE | Reprendre le backend ZIP V1 sur main synchronisé | moteur DOCX clos + backend PDF + fondation phase 18 | backend ZIP dossier documenté et testé |
| REVIEW-FINAL-001 | DONE | Exécuter la revue finale V1 | moteur DOCX + UI/PDF/ZIP intégrés | rapport d'execution + decision GO avec reserves |
| UI-PDF-ZIP-INTEGRATION-001 | DONE | Brancher PDF et ZIP dans l'UI Streamlit | UI core + backend PDF + backend ZIP | téléchargements DOCX/PDF/ZIP + smoke manuel + tests |
| SYNC-FINAL-FOUNDATIONS-001 | DONE | Synchroniser les fondations finales UI/PDF/ZIP/clôture dans main | branches finales listées | main réaligné + pilotage final |
| WORKTREE-CLEANUP-AND-UI-STATUS-001 | DONE | Consolider la revue finale, clarifier le statut UI et archiver les anciens worktrees locaux | `main` propre + audit branches/worktrees + `codex/review-final-001` | rapport 23 + pack de revue finale intégré + dossier canonique unique |
| CLOSE-PROJECT-V1-001 | READY | Clore le projet V1 après revue finale | `REVIEW-FINAL-001` terminé | clôture V1 documentée |
| UI-BUSINESS-WIZARD-001 | DONE | Lancer le wizard metier UI dossier-centre | `REVIEW-FINAL-001` + docs UI 19/20/21 + moteur DOCX/ZIP | UI metier guidee sans logique juridique cachee |
| DEPLOY-STREAMLIT-CLOUD-FIX-001 | DONE | Corriger l'installation Poetry Streamlit Cloud | erreur cloud package `sydel-document-engine` + package source `src/sydel_doc_engine` | `pyproject.toml` package explicite + rapport de deploiement + validations locales |
| CASE-CATALOG-001 | DONE | Créer la couche métier catalogue des cas depuis la source de vérité | `project/source_truth/Documents_a_generer_par_cas.docx` + registre DOC-001 à DOC-043 | service pur `get_expected_documents` + tests + rapport |
| UI-CASE-WIZARD-002 | DONE | Brancher l'assistant métier Streamlit sur le catalogue des cas | `CASE-CATALOG-001` + docs UI 19/20/21 + assistant existant | sélection documentaire via `get_expected_documents` + statuts honnêtes + tests + rapport |
| SELARL-PILOT-PROTOCOL-001 | DONE | Cadrer le protocole produit SELARL pilote depuis la source V2 | `Documents_a_generer_par_cas_V2.docx` + CASE-CATALOG-001 + UI actuelle | protocole réplicable + specs SELARL + plan d'implémentation + rapport |
| SELARL-PILOT-SOURCE-VERIFY-001 | DONE | Réconcilier les specs SELARL avec la vraie source V2 | vraie V2 `project/source_truth/Documents_a_generer_par_cas_V2.docx` + specs SELARL + catalogue | matrice d'écarts + statuts dérogation corrigés + specs alignées + tests |
| SELARL-FORM-SCHEMA-IMPL-001 | DONE | Implémenter le schéma de données SELARL côté Assistant métier | vraie V2 + specs SELARL + catalogue corrigé | module `selarl_form_schema.py` + réserve DOC-006 + couverture variables V2 + tests + rapport |
| SELARL-UI-WIZARD-IMPL-001 | DONE | Brancher l'UI Assistant métier sur le schéma SELARL | `selarl_form_schema.py` + spec UI SELARL | parcours SELARL visible, documents manuels visibles mais exclus de la génération + tests + rapport |
| SELARL-NOTEBOOKLM-RECONCILIATION-001 | DONE | Réconcilier le pilote SELARL avec NotebookLM et la V3 | NotebookLM + V3 + V2 + code/specs SELARL | hiérarchie source V2 + rapport d'écarts + backlog de reconstruction contrôlée |
| SELARL-PLAN-CORRECTION-001 | DONE | Resserrer le plan SELARL selon arbitrages associé | rapport NotebookLM + backlog V2 | hiérarchie source corrigée, backlog simplifié, UI SELARL non validée produit |
| SELARL-WORDING-REALIGN-001 | DONE | Réaligner le vocabulaire visible SELARL | rapport NotebookLM corrigé + backlog V2 corrigé | labels Praticien/Fiche Client/rôles + tests anti-régression |
| SELARL-FLOW-REALIGN-001 | DONE | Réaligner l'ordre du formulaire SELARL | `SELARL-WORDING-REALIGN-001` | flow schema/projections Qualification / Fiche Client / Société / Capital / Scénarios / Documents + tests |
| SELARL-REUSE-RULES-REALIGN-001 | DONE | Corriger les règles de réutilisation SELARL | `SELARL-FLOW-REALIGN-001` | Dossier unipersonnel, Praticien source, dérivations explicites |
| SELARL-UI-REALIGN-001 | DONE | Réaligner le parcours UI SELARL après schéma corrigé | `SELARL-REUSE-RULES-REALIGN-001` | Streamlit SELARL réaligné sans push/redéploiement prématuré |
| SELARL-SMOKE-REALISTIC-001 | DONE | Smoke tester SELARL avec données réalistes après réalignement | `SELARL-UI-REALIGN-001` | rapport de smoke réaliste, documents manuels exclus, catalogue existant respecté |
| SELARL-CLOUD-GENERATION-BUG-001 | DONE | Corriger le blocage de génération SELARL visible | test utilisateur Cloud + parcours Streamlit SELARL | session state dérivé corrigé, génération visible restaurée, test AppTest |
| DOCUMENT-UNITAIRE-001 | DONE | Ajouter le mode Streamlit Document unitaire | Streamlit + catalogue cas + schéma SELARL | choix document, champs limités, DOCX unique, ZIP/PDF optionnels, rapport |
| ASSISTANT-METIER-PREFILL-001 | DONE | Ajouter des scénarios fictifs déterministes de préremplissage dans Assistant métier | Assistant métier SELARL/SCI + specs UI/SELARL | module presets + boutons Préremplir/Réinitialiser + tests + rapport |
| GLOBAL-VARIABLE-INVENTORY-001 | DONE | Construire l'inventaire global brut des variables documentaires | référentiels V1 + source truth V1/V2/V3 + templates + specs + registre | CSV global brut + rapport exécutif + pilotage |
| GLOBAL-VARIABLE-IDENTITY-AUDIT-001 | DONE | Auditer l'identité sémantique globale des variables avant rebuild front | `GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv` + référentiels V1 + templates + specs | matrice identité V2 + registre canonique global V2 + questions humaines + rapport |
| GLOBAL-HUMAN-ANSWERS-INTEGRATION-001 | DONE | Intégrer les réponses humaines dans le registre canonique global | audit global V2 + réponse Albane + modèle SELAS micro-holding + V3/NotebookLM | questions V2 + registre canonique V2.1 + rapport exécutif |
| GLOBAL-FRONT-ARCHITECTURE-001 | DONE | Concevoir l'architecture du nouveau front global sur le registre V2.1 | registre canonique global V2.1 + questions V2 | architecture front sans modification moteur/générateurs/UI existante |
| GLOBAL-FRONT-ARCHITECTURE-QA-001 | DONE | Contrôler l'architecture front globale sur documents sentinelles | architecture front V1 + registre V2.1 + catalogue moteur + templates sentinelles | rapport QA + CSV sentinelles sans modification moteur/générateurs/UI |
| FRONT-DATA-LAYER-001 | DONE | Créer la couche de données front globale | architecture front V1 + registre V2.1 | objets front globaux + tests/validations sans toucher aux générateurs |
| FRONT-ROLE-MODEL-001 | DONE | Modéliser les rôles explicites du front global | `FRONT-DATA-LAYER-001` | RoleAssignment sans fusion silencieuse |
| FRONT-ADDRESS-MODEL-001 | DONE | Modéliser les adresses typées par usage | `FRONT-DATA-LAYER-001` + `FRONT-ROLE-MODEL-001` | adresses pivots, règles de réutilisation, overrides |
| FRONT-DOSSIER-FLOW-001 | DONE | Définir le flow dossier complet global | data layer + rôles + adresses | flow dossier par opération/famille documentaire |
| FRONT-DOCUMENT-STATUS-LAYER-001 | DONE | Construire la couche de statuts documentaires front | `FRONT-DOSSIER-FLOW-001` | documents attendus, manuels, réservés, non prêts |
| FRONT-UNIT-DOCUMENT-MODE-001 | DONE | Reconcevoir le mode document unitaire comme diagnostic séparé | `FRONT-DOCUMENT-STATUS-LAYER-001` | test document unique sans polluer le parcours dossier |
| FRONT-TEST-PREFILL-001 | DONE | Concevoir les préremplissages fictifs de test du nouveau front | `FRONT-DOSSIER-FLOW-001` + status layer | scénarios déterministes non métier |
| FRONT-REVIEW-001 | DONE | Faire valider le modèle front global avant UI visible | tickets front data/role/address/flow/status/prefill | carte de migration + backlog UI visible |
| FRONT-UI-SHELL-001 | DONE | Creer la premiere tranche visible du nouveau front global | `FRONT-REVIEW-001` + `front_data` | shell cible distinct du prototype, outils de test isoles |
| FRONT-DOSSIER-EDITOR-001 | DONE | Construire l'editeur dossier data-first | `FRONT-UI-SHELL-001` | editeur dossier V1, flow/blocs/exigences/statuts visibles |
| FRONT-DOSSIER-DATA-ENTRY-001 | DONE | Ajouter la premiere saisie reelle du nouvel editeur dossier | `FRONT-DOSSIER-EDITOR-001` + `front_data` | saisie SELARL simple vers DossierRecord + statuts recalcules |
| FRONT-DOCUMENTS-PANEL-001 | BLOCKED | Afficher les documents attendus et leurs statuts | decision post-test utilisateur minimal | ne pas ajouter de panneau visible sans besoin confirme |
| FRONT-GENERATION-ACTIONS-001 | DONE | Brancher les actions DOCX/PDF/ZIP du nouveau front | `FRONT-DOSSIER-DATA-ENTRY-001` + status layer | generation V1 DOC-001 a DOC-004 depuis le nouveau front |
| FRONT-UX-CLEANUP-001 | DONE | Simplifier le nouveau front pour test utilisateur reel | `FRONT-GENERATION-ACTIONS-001` | parcours principal type dossier / saisie / resume / generation, diagnostics replies |
| FRONT-UX-HARD-CUT-001 | DONE | Retirer tout bruit non-user du nouveau front | `FRONT-UX-CLEANUP-001` | vue principale limitee a type dossier, saisie et generation ; outils internes en sidebar |
| FRONT-STATE-AUDIT-001 | DONE | Auditer l'etat reel projet/front apres retour utilisateur | docs projet + front Streamlit + tests front | rapport d'audit + direction front immediate |
| FRONT-REALITY-CHECK-001 | DONE | Auditer l'ecart entre debriefs front et code reel | code Streamlit + debriefs front + etat Git | rapport de realite + plan surface minimale |
| FRONT-MINIMAL-SURFACE-CLEANUP-001 | DONE | Appliquer la surface utilisateur minimale | `FRONT-REALITY-CHECK-001` + `FRONT_MINIMAL_USER_SURFACE_V1.md` | type dossier / saisie / generation, debug cache |
| SELARL-COMPLETE-CASE-PLAYBOOK-001 | DONE | Cadrer la SELARL complete et la recette reproductible | specs SELARL + code front reel + catalogue moteur | playbook SELARL complet + rapport de realite |
| SELARL-COMPLETE-CONTEXT-ADAPTER-001 | DONE | Brancher l'adaptateur contexte SELARL complet cote front | `SELARL_COMPLETE_CASE_PLAYBOOK_V1.md` + `front_data` + catalogue | selection documentaire conditionnelle + readiness + contexte moteur |
| SELARL-COMPLETE-COMPLEX-SUBFORMS-001 | BLOCKED | Completer les sous-formulaires SELARL complexes | `SELARL-COMPLETE-CONTEXT-ADAPTER-001` + catalogue + specs cession/SCM + `SELARL_CANONICAL_STATUS_V1.md` | bloque jusqu'au choix explicite d'un seul sous-cas et `GO dev` |
| FRONT-GENERATION-READINESS-UX-001 | BLOCKED | Expliquer les blocages de generation dans la vue normale | a absorber dans `FRONT-MINIMAL-SURFACE-CLEANUP-001` | ne pas lancer comme ticket separe avant la coupe UX |
| FRONT-UNIT-DOCUMENT-UI-001 | BLOCKED | Consolider l'UI Document unitaire autour de `front_data` | `FRONT-UI-SHELL-001` | mode document unique separe du dossier complet |
| FRONT-TEST-TOOLS-CONSOLIDATION-001 | BLOCKED | Regrouper prefills, smoke et diagnostic | `FRONT-UI-SHELL-001` | outils de test marques et separes du produit |
| FRONT-PROTOTYPE-DEPRECATION-001 | BLOCKED | Deprecier le prototype historique sans perte de diagnostic | nouveaux parcours UI visibles | prototype marque obsolete ou archive |
| SELARL-JURIST-REVIEW-001 | BLOCKED | Ancien libelle de revue humaine SELARL | remplace par `SELARL-ASSOCIE-REVIEW-001` | ne pas utiliser comme prochaine action |
| SELARL-DOCS-GENERATION-SMOKE-001 | BLOCKED | Smoke tester la génération SELARL depuis le parcours Assistant métier | parcours SELARL réaligné + catalogue + schema + contextes réalistes | bloqué par la réconciliation NotebookLM ; remplacé par `SELARL-SMOKE-REALISTIC-001` après réalignement |
| UI-001 | BLOCKED | Brancher Streamlit V0 Lot 1 | orchestrateur Lot 1 + spec canonique PV nomination gérant validée | écran simple + test manuel |

## Référentiels moteur disponibles
- Le moteur dispose désormais d'un arbre documentaire document-centré V1 : `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`.
- Le moteur dispose désormais d'un dictionnaire canonique des variables V1 : `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`.
- Le moteur dispose désormais d'une table de mapping document -> variables canoniques V1 : `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.
- Le cadrage métier de la famille `PV nomination gérant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`.
- La spec canonique V1 de la famille `PV nomination gérant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.
- La spec texte V1 de la famille `PV nomination gérant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.
- La spec technique V1 de couche de rendu DOCX commune est disponible : `docs/delivery/render_style_system_v1.md`.
- Le cadrage V1 `Demande d'inscription à l'ordre` est disponible : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`.
- La spec canonique V1 `Demande d'inscription à l'ordre` est disponible : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`.
- La spec texte V1 `Demande d'inscription à l'ordre` est disponible : `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.
- Le cadrage V1 du batch `régime communautaire` est disponible : `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- La spec canonique V1 du batch `régime communautaire` est disponible : `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md`.
- La spec texte V1 du batch `régime communautaire` est disponible : `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`.
- La spec canonique V1 du batch SPFPL spécifique est disponible : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`.
- La spec texte V1 du batch SPFPL spécifique est disponible : `docs/delivery/lot_05_spfpl_spec_texte_v1.md`.
- La préparation V1 des sources statuts est disponible : `docs/delivery/lot_04_statuts_preparation_v1.md`.
- La spec canonique V1 de la famille `dérogations` est disponible : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`.
- La spec texte V1 de la famille `dérogations` est disponible : `docs/delivery/lot_03_derogations_spec_texte_v1.md`.
- La spec canonique V1 `cession cabinets` est disponible : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`.
- La spec texte V1 `cession cabinets` est disponible : `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.
- Les arbitrages V1 `cession cabinets` sont disponibles : `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`.
- La spec canonique V1 `bail / appel de fonds` est disponible : `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`.
- La spec texte V1 `bail / appel de fonds` est disponible : `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`.
- Les arbitrages V1 `dérogations` sont disponibles : `docs/delivery/lot_03_derogations_arbitrages_v1.md`.
- Les arbitrages V1 du batch SPFPL spécifique sont disponibles : `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.
- Les specs V1 des statuts SEL d'exercice sont disponibles : `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.
- Les specs V1 des statuts SPFPL sont disponibles : `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`.
- Les specs V1 des statuts civils sont disponibles : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.
- Les specs V1 des statuts SAS sont disponibles : `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`.
- Les arbitrages V1 des statuts SCM sont disponibles : `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md`.
- La préparation V1 des satellites SCM est disponible : `docs/delivery/lot_05_scm_satellites_preparation_v1.md`.
- Les specs V1 des satellites SAS sont disponibles : `docs/delivery/lot_05_sas_satellites_spec_canonique_v1.md` et `docs/delivery/lot_05_sas_satellites_spec_texte_v1.md`.
- La spec V1 de la lettre option IS est disponible : `docs/delivery/lot_05_lettre_option_is_spec_v1.md`.
- L'audit V1 de l'acte de cession d'actions est disponible : `docs/delivery/lot_05_acte_cession_actions_audit_v1.md`.
- Les specs V1 de l'acte de cession d'actions sont disponibles : `docs/delivery/lot_05_acte_cession_actions_spec_canonique_v1.md` et `docs/delivery/lot_05_acte_cession_actions_spec_texte_v1.md`.
- La préparation V1 des sources cession SCM est disponible : `docs/delivery/lot_05_scm_cession_sources_preparation_v1.md`.
- Les specs V1 du blocage cession SCM sont disponibles : `docs/delivery/lot_05_scm_cession_block_spec_canonique_v1.md` et `docs/delivery/lot_05_scm_cession_block_spec_texte_v1.md`.
- La résolution V1 du bloc cession SCM est disponible : `docs/delivery/lot_05_scm_cession_block_resolution_v1.md`.
- L'audit de clôture moteur V1 est disponible : `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md`.
- L'audit qualité final moteur V1 est disponible : `docs/project/17_FINAL_ENGINE_QUALITY_AUDIT_V1.md`.
- Le plan de fondation post-moteur V1 est disponible : `docs/project/18_NEXT_PHASE_FOUNDATION_V1.md`.
- Le flux UI V1 est disponible : `docs/project/19_UI_FLOW_V1.md`.
- Le référentiel des occurrences UI V1 est disponible : `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md`.
- Le schéma formulaire UI V1 est disponible : `docs/project/21_UI_FORM_SCHEMA_V1.md`.
- Le framework de recette finale V1 est disponible : `docs/review/final_recipe_framework_v1.md`.
- Le blueprint style Lot 03 est disponible : `docs/delivery/render_style_blueprint_lot03_batch_v1.md`.
- Le blueprint style statuts est disponible : `docs/delivery/render_style_blueprint_statuts_batch_v1.md`.
- Le manifest d'import sources V1 est disponible : `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md`.
- Le rapport de doublons sources V1 est disponible : `docs/project/11_SOURCE_DUPLICATES_REPORT_V1.md`.
- Le plan de placement sources V1 est disponible : `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`.
- Les décisions d'arbitrage sources V1 sont disponibles : `docs/project/13_SOURCE_ARBITRATION_DECISIONS_V1.md`.
- Le journal d'exécution du placement HIGH V1 est disponible : `docs/project/14_SOURCE_PLACEMENT_EXECUTION_V1.md`.
- L'audit du périmètre restant V1 est disponible : `docs/project/15_REMAINING_SCOPE_AUDIT_V1.md`.
- Le pack de revue humaine du PV nomination gérant est disponible : `docs/review/lot_02_pv_nomination_gerant_review_v1.md`.
- L'aperçu texte extrait du DOCX généré est disponible : `docs/review/lot_02_pv_nomination_gerant_preview_v1.txt`.
- La revue smoke orchestrateur Lot 2 est disponible : `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- Les revues batch Lot 03 et Lot 04 sont disponibles : `docs/review/lot_03_batch_review_v1.md` et `docs/review/lot_04_batch_review_v1.md`.
- Ces référentiels cadrent les prochains tickets ; ils ne doivent pas être réinventés pendant l'implémentation.

## Ecart temporaire connu
- Nom canonique retenu pour la domiciliation : `domiciliation.adresse_affichee`.
- Alias legacy temporaire présent dans le code Lot 1 : `adresse_domiciliation_affichee`.
- Le présent ticket ne refactore pas le code Python ; les prochains tickets doivent converger vers le nom canonique sans recréer de variante locale.

## Détail des prochains tickets

### DOC-001
- Objectif : générer la déclaration sur l'honneur de non-condamnation.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- ADR à relire : ADR-0001, ADR-0002, ADR-0004, ADR-0005.
- Contraintes : source reçue, spec écrite, accords de genre, DOCX propre, tests obligatoires.
- Sortie attendue : générateur DOC-001, tests, mise à jour documentaire.

### DOC-003
- Objectif : générer la procuration après DOC-001.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- Contraintes : bloc mandataire SYDEL externalisé en configuration, wording source conservé.
- Sortie attendue : générateur DOC-003, tests, mise à jour documentaire.

### DOC-002
- Objectif : générer l'autorisation de domiciliation après arbitrage V1 déjà posé.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- Contrainte sensible : le nom canonique documentaire est désormais `domiciliation.adresse_affichee`; le code Lot 1 existant conserve temporairement l'alias legacy `adresse_domiciliation_affichee`.
- Sortie : générateur DOC-002 terminé, tests unitaires ciblés ajoutés, validations locales vertes.

### ORCH-001
- Objectif : brancher les trois générateurs Lot 1 dans l'orchestrateur dossier.
- Prérequis : DOC-001, DOC-002 et DOC-003 terminés.
- Sortie : registre minimal DOC-001/DOC-002/DOC-003 branché, génération DOCX dossier selon `ctx.structure`, tests d'orchestration ajoutés.

### VAR-001
- Objectif : ajouter une table de mapping document -> variables canoniques sans refaire le dictionnaire.
- Prérequis : arbre documentaire V1 et dictionnaire canonique des variables V1 intégrés.
- Sortie : table de mapping V1 intégrée à la mémoire projet, sans réécriture ; écart temporaire documenté entre `domiciliation.adresse_affichee` et l'alias legacy `adresse_domiciliation_affichee`.

### SPEC-PV-001
- Objectif : formaliser la spec canonique du PV nomination gérant à partir du cadrage V1, sans refaire le cadrage.
- Spec/cadrage à lire : `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`.
- Prérequis : arbre documentaire V1, dictionnaire canonique V1 et table de mapping document -> variables canoniques V1.
- Contraintes : traiter `PV nomination gérant` comme une famille documentaire mutualisable, gérer `associes[]` dynamiquement, distinguer `dirigeant_nomine` de `associes[]`, identifier les blocs conditionnels, ne coder aucun générateur.
- Sortie attendue : spec canonique écrite dans `docs/delivery/`, avec structure, blocs fixes, blocs conditionnels, mapping variables, règles de répétition, règles de grammaire minimales et points ouverts.
- Statut : terminé ; spec canonique V1 disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.

### SPEC-TEXTE-PV-001
- Objectif : stabiliser le texte canonique et les variantes du PV nomination gérant avant tout codage.
- Spec à lire : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.
- Source à consulter : `project/source_documents/lot_02/PV nomination gérant - transforme.docx`.
- Contraintes : ne pas refaire la spec canonique, ne pas coder de générateur, ne pas modifier implicitement le wording juridique ; signaler les formulations à validation.
- Sortie attendue : spec textuelle détaillée du PV nomination gérant, variantes structurelles explicites, wording à valider, critères d'entrée avant code.
- Statut : terminé ; spec texte V1 disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.

### CODE-PV-001
- Objectif : implémenter le générateur canonique `PV nomination gérant` à partir des specs V1, sans reprendre `personne_1` / `personne_2` comme vérité métier.
- Specs à lire : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md` et `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.
- Source à consulter : `project/source_documents/lot_02/PV nomination gérant - transforme.docx`.
- Contraintes : générateur DOCX from-scratch, `associes[]` dynamique, `dirigeant_nomine` distinct, variantes `né/née`, branche `emprunt.actif`, renumérotation des décisions, aucun changement de wording juridique hors spec texte.
- Sortie attendue : générateur dédié, tests unitaires ciblés, validation locale, mise à jour documentaire.
- Statut : terminé ; générateur disponible dans `src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py`, non branché à l'orchestrateur.
- Smoke test réel : contexte exemple disponible dans `examples/contexts/lot_02_pv_nomination_gerant_example.yaml`, DOCX généré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/`.

### REVIEW-PV-001
- Objectif : préparer la revue humaine du rendu DOCX et du wording du PV nomination gérant déjà codé, sans modifier le code métier.
- Entrées : générateur PV existant, contexte exemple `examples/contexts/lot_02_pv_nomination_gerant_example.yaml`, specs Lot 2.
- Sortie : DOCX régénéré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`, aperçu texte et checklist de revue dans `docs/review/`.
- Statut : terminé ; le PV reste non branché à l'orchestrateur Lot 2 tant qu'une validation humaine explicite n'a pas été donnée.

### SPEC-RENDER-001
- Objectif : formaliser une couche de rendu DOCX commune avant refactor du code métier.
- Spec à lire : `docs/delivery/render_style_system_v1.md`.
- Contraintes : ne modifier aucun générateur, ne changer aucun wording juridique, documenter les styles communs, le titre encadré, les signatures simples/encadrées, le rappel légal et les surcharges documentaires.
- Sortie : spec technique V1 créée ; documents impactés listés : DOC-001, DOC-002, DOC-003 et PV nomination gérant.
- Statut : terminé ; le point d'écart explicite est que les encadrés de signature manquent aujourd'hui dans le rendu généré.

### RENDER-STYLE-001
- Objectif : implémenter la couche commune de rendu DOCX dans `src/sydel_doc_engine/rendering/docx_builder.py`.
- Prérequis : `docs/delivery/render_style_system_v1.md`.
- Contraintes : ticket technique uniquement, aucun changement de wording juridique, migration progressive, tests existants à conserver verts.
- Sortie attendue : profil global de style, helpers de paragraphes/blocs, titre encadré, signature simple, signature encadrée disponible, rappel légal commun.
- Statut : terminé ; couche commune implémentée et appliquée à DOC-001, DOC-002, DOC-003 et PV nomination gérant.

### ORCH-L2-PV-001
- Objectif : brancher le générateur PV nomination gérant dans le catalogue et l'orchestrateur, sans UI, PDF ni ZIP.
- Prérequis : générateur PV existant, specs Lot 2, décisions de sélection SELARL/SELAS/SPFPL cession/SPFPL apport/SCS/SCI/SCM et exclusion SAS.
- Sortie : `DOC-004` ajouté au catalogue, générateur enregistré, sélection testée pour SELARL/SCI/SAS, génération orchestrée testée avec production du DOCX PV.
- Statut : terminé ; aucune modification de wording juridique.

### SMOKE-ORCH-L2-001
- Objectif : vérifier en génération réelle l'orchestrateur Lot 2 avec un cas positif SCI et un cas négatif SAS.
- Entrées : contextes `examples/contexts/lot_02_orchestrator_positive_example.yaml` et `examples/contexts/lot_02_orchestrator_negative_sas_example.yaml`.
- Sortie : smoke DOCX dans `artifacts/lot_02_orchestrator_positive_smoke_test/` et `artifacts/lot_02_orchestrator_negative_sas_smoke_test/`, revue dans `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- Statut : terminé ; le PV est généré pour SCI et absent pour SAS.

### FIX-PV-RENDER-001
- Objectif : améliorer le rendu from-scratch du PV nomination gérant sans chercher une copie parfaite du Word source.
- Entrées : source Lot 2 `PV nomination gérant - transforme.docx`, specs PV V1 et spec `render_style_system_v1.md`.
- Contraintes : ne pas modifier le wording juridique, ne pas toucher à l'UI, ne pas générer PDF/ZIP, ne pas versionner `artifacts/`.
- Sortie : bloc société centré avec dénomination en gras, titre principal encadré, listes à tirets pour associés et décisions, intertitres de décision gras/soulignés, formules de vote en italique, signatures centrées, smoke DOCX.
- Statut : terminé ; aucun changement de wording juridique volontaire.

### ANALYSE-ORDRE-001
- Objectif : préparer le prochain batch mutualisable Lot 2 sans coder, en analysant la demande d'inscription à l'ordre et les deux lettres de régime communautaire.
- Entrées : référentiels projet V1 + trois sources Lot 2 présentes dans `project/source_documents/lot_02/`.
- Sortie : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md` et `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- Statut : terminé ; aucun code Python modifié.

### ARBITRAGE-SOURCES-001
- Objectif : réparer les prérequis documentaires d'import sources puis arbitrer les placements possibles sans déplacer de fichier.
- Entrées : `project/source_truth/Documents_a_generer_par_cas.docx`, `project/source_import/raw_drive_dump/`, `project/source_documents/`, décisions métier chef de projet.
- Sortie : manifest import sources V1, rapport doublons V1, plan placement V1, décisions arbitrage V1.
- Statut : terminé ; aucun code Python, aucun fichier source, aucun artefact modifié.

### PLACEMENT-HIGH-001
- Objectif : déplacer physiquement dans `source_documents` uniquement les cas HIGH validés par `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`.
- Entrées : plan de placement V1 + décisions d'arbitrage sources V1.
- Contraintes : ne pas toucher aux cas MEDIUM/LOW, ne pas versionner `project/source_import/raw_drive_dump/`, documenter les no-op si les fichiers HIGH sont déjà présents.
- Statut : terminé ; les 4 cas HIGH sont déjà présents aux emplacements cibles et ont été confirmés en no-op documenté. Aucun fichier MEDIUM/LOW ou hors périmètre n'a été modifié.

### SPEC-ORDRE-001
- Objectif : formaliser la spec canonique `Demande d'inscription à l'ordre` à partir du cadrage V1.
- Cadrage à lire : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`.
- Contraintes : ne pas coder, comparer les variantes SELARL / SELAS / SPFPL, identifier le traitement de `Dérogation ?`, les accords de genre, le titre `Dr`, le destinataire ordinal et le mapping des données ordinales.
- Sortie : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`, avec périmètre structures, comparaison des variantes, noyau texte, variables canoniques, règles de blocage et points ouverts.
- Statut : terminé ; aucun code Python modifié.

### SPEC-TEXTE-ORDRE-001
- Objectif : stabiliser le texte canonique et les variantes de `Demande d'inscription à l'ordre` avant tout codage.
- Spec à lire : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`.
- Sources à consulter : source Lot 2 + variantes raw dump SELARL, SELAS et SPFPL comparées dans la spec canonique.
- Contraintes : ne pas coder, trancher le wording de `Dérogation ?`, la granularité des données ordinales, le mandataire, les accords et le destinataire ordinal.
- Sortie attendue : spec texte détaillée, wording stabilisé ou points de blocage explicites, critères avant code.
- Statut : terminé ; spec texte V1 disponible dans `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.

### CODE-ORDRE-001
- Objectif : implémenter le générateur canonique `Demande d'inscription à l'ordre`.
- Specs à lire : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md` et `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.
- Sources à consulter : source Lot 2 + variantes raw dump SELARL, SELAS, SPFPL cession, SPFPL apport et absence de variante SCM dédiée documentée.
- Contraintes : générateur DOCX from-scratch, overlays SELARL/SELAS, SPFPL cession/apport et SCM, bloc `Dérogation ?` manuel/conditionnel, mandataire configurable, aucune constante SYDEL en dur, aucun changement de wording juridique hors spec texte.
- Sortie attendue : générateur dédié, tests unitaires ciblés, validation locale, mise à jour documentaire.
- Statut : terminé ; générateur disponible dans `src/sydel_doc_engine/generators/lot_02/demande_inscription_ordre.py`, tests ciblés ajoutés, smoke DOCX réel généré hors versionnement.

### SPEC-RC-001
- Objectif : formaliser la spec canonique du batch `régime communautaire` pour la lettre de renonciation et la lettre d'avertissement.
- Cadrage à lire : `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- Contraintes : garder deux documents canoniques distincts, mutualiser le pack de variables, arbitrer les rôles `apporteur` / `conjoint`, les montants, les dates croisées, les formes sociales et la mention manuscrite.
- Sortie : specs canonique et texte créées dans `docs/delivery/`, variantes SELARL / SELAS / SPFPL comparées, mapping commun écrit, overlays de mention manuscrite documentés, règles de blocage avant code précisées.
- Statut : terminé ; `CODE-RC-001` est ajouté en READY.

### CODE-RC-001
- Objectif : implémenter le batch `régime communautaire` V1 pour la lettre d'avertissement au conjoint et la lettre de renonciation.
- Specs à lire : `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md` et `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`.
- Sources à consulter : sources Lot 2 placées + variantes raw dump SELARL, SELAS et SPFPL comparées dans SPEC-RC-001.
- Contraintes : deux documents canoniques distincts, génération DOCX from-scratch, sélection uniquement si `dossier.options.regime_communautaire == true`, structures SELARL / SELAS / SPFPL cession / SPFPL apport, aucun changement de wording juridique hors variables et overlays documentés.
- Sortie attendue : générateurs dédiés, branchement orchestrateur/catalogue si nécessaire, tests ciblés des quatre structures, de la mention manuscrite SELARL vs SELAS/SPFPL, des dates croisées et des blocages.
- Statut : terminé ; générateurs `lettre_renonciation_associe` et `lettre_avertissement_conjoint` disponibles, catalogue/orchestrateur branchés, contexte exemple et smoke DOCX générés.

### SPEC-SPFPL-001
- Objectif : formaliser le batch documentaire SPFPL spécifique sans coder.
- Spec à lire : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`.
- Contraintes : garder les documents universels et le régime communautaire hors de cette spec, ne pas coder depuis une source absente, ne pas corriger les ambiguïtés cession/apport sans arbitrage.
- Sortie : spec canonique V1 SPFPL, sous-familles, variables proposées, blocages et points ouverts.
- Statut : terminé ; aucun code Python modifié.

### SPEC-DEROG-001
- Objectif : formaliser la famille documentaire `dérogations` sans automatiser les formulaires manuels.
- Spec à lire : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`.
- Contraintes : distinguer site distinct, multi-sites SEL, cumul SEL/BNC, cumul salariée et pièces manuelles ; ne pas générer de contenu narratif sensible.
- Sortie : spec canonique V1 dérogations, périmètre automatisable/manuel, variables et blocages.
- Statut : terminé ; aucun code Python modifié.

### SPEC-CESSION-BAIL-001
- Objectif : formaliser les blocs `cession cabinets` et `bail / appel de fonds` avant tout code.
- Specs à lire : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md` et `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`.
- Contraintes : ne pas fusionner acte/compromis ou médical/dentaire sans arbitrage, traiter les anomalies de bail et de placeholders comme points ouverts.
- Sortie : deux specs canoniques V1, variables, conditions, règles de blocage et points ouverts.
- Statut : terminé ; aucun code Python modifié.

### SYNC-SPECS-001
- Objectif : absorber dans `main` les specs parallèles RC, SPFPL, dérogations et cession/bail.
- Entrées : branches et commits de specs déjà produits en parallèle.
- Sortie : commits de specs intégrés dans `main`, pilotage aligné, `CODE-RC-001` confirmé READY.
- Statut : terminé ; aucun fichier Python stagé pour le commit de synchronisation.

### SPEC-TEXTE-BAIL-APP-001
- Objectif : stabiliser le texte canonique du mini-batch `bail / appel de fonds` avant code.
- Spec à lire : `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`.
- Contraintes : conserver le wording source, bloquer l'appel de fonds médical et les cas SELAS non arbitrés, ne pas coder.
- Statut : terminé ; aucun code Python modifié.

### SPEC-TEXTE-CESSION-CAB-001
- Objectif : stabiliser le texte canonique de la famille `cession cabinets`.
- Spec à lire : `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.
- Contraintes : ne pas harmoniser médical/dentaire, acte/compromis ou SELARL/SELAS sans arbitrage.
- Statut : terminé ; aucun code Python modifié.

### SPEC-TEXTE-DEROG-001
- Objectif : stabiliser le texte canonique des dérogations.
- Spec à lire : `docs/delivery/lot_03_derogations_spec_texte_v1.md`.
- Contraintes : ne pas automatiser les formulaires manuels, ne pas inventer les zones narratives sensibles.
- Statut : terminé ; aucun code Python modifié.

### SPEC-TEXTE-SPFPL-001
- Objectif : stabiliser le texte canonique du batch SPFPL spécifique.
- Spec à lire : `docs/delivery/lot_05_spfpl_spec_texte_v1.md`.
- Contraintes : ne pas corriger les conflits cession/apport, commissaire aux apports ou souscripteurs sans arbitrage.
- Statut : terminé ; aucun code Python modifié.

### SYNC-TEXTE-SPECS-001
- Objectif : absorber dans `main` les quatre specs texte parallèles bail/appel, cession cabinets, dérogations et SPFPL.
- Entrées : branches `codex/spec-texte-bail-app-001`, `codex/spec-texte-cession-cab-001`, `codex/spec-texte-derog-001`, `codex/spec-texte-spfpl-001`.
- Sortie : quatre specs texte intégrées dans `main`, pilotage aligné, prochains tickets READY confirmés.
- Statut : terminé ; aucun fichier Python, aucun `project/source_import/raw_drive_dump/` et aucun `artifacts/` modifié.

### SYNC-ARBITRAGES-001
- Objectif : absorber dans `main` les trois arbitrages parallèles cession cabinets, dérogations et SPFPL.
- Entrées : branches `codex/arbitrage-cession-001`, `codex/arbitrage-derog-001`, `codex/arbitrage-spfpl-001`.
- Sortie : arbitrages intégrés dans `main`, pilotage aligné, prochains tickets READY confirmés.
- Statut : terminé ; aucun fichier Python, aucun `project/source_import/raw_drive_dump/` et aucun `artifacts/` modifié.

### CODE-BAIL-APP-001
- Objectif : implémenter le mini-batch `bail / appel de fonds`.
- Specs à lire : `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md` et `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`.
- Contraintes : génération DOCX from-scratch, activation cession SELARL/SELAS pour l'avenant, appel de fonds limité SELARL dentaire, blocages explicites sur les points ouverts.
- Statut : DONE ; commit `557a013274aa9f7122c81d5e6e0b52c4043a540c` absorbé dans `main`, générateurs `avenant_contrat_bail` et `appel_fond_sel` disponibles, catalogue/orchestrateur branchés et tests ciblés intégrés.

### ARBITRAGE-CESSION-001
- Objectif : arbitrer les points bloquants de la famille `cession cabinets` avant tout code.
- Entrées : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md` et `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.
- Sortie attendue : décisions sur acte/compromis, SELAS, anomalies médical/dentaire, placeholders acquéreur/vendeur, crédit-vendeur, SCM et salariés.
- Statut : terminé ; arbitrages V1 disponibles dans `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`.

### ARBITRAGE-DEROG-001
- Objectif : arbitrer les points bloquants de la famille `dérogations` avant code.
- Entrées : `docs/delivery/lot_03_derogations_spec_canonique_v1.md` et `docs/delivery/lot_03_derogations_spec_texte_v1.md`.
- Sortie attendue : décisions sur formulaires préremplis, placement sources Lot 03, conversion `.doc`, rôles et champs narratifs obligatoires.
- Statut : terminé ; arbitrages V1 disponibles dans `docs/delivery/lot_03_derogations_arbitrages_v1.md`.

### ARBITRAGE-SPFPL-001
- Objectif : arbitrer les points bloquants du batch SPFPL spécifique avant code.
- Entrées : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_05_spfpl_spec_texte_v1.md`.
- Sortie attendue : décisions sur note d'information cession/apport, PV agrément, commissaire aux apports, liste des souscripteurs et sources manquantes.
- Statut : terminé ; arbitrages V1 disponibles dans `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.

### CODE-CESSION-CAB-001
- Objectif : implémenter la famille `cession cabinets` en respectant les arbitrages V1.
- Specs à lire : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`, `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md` et `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`.
- Contraintes : quatre documents canoniques distincts, sélection par étape explicite, séparation médical/dentaire, blocages explicites sur les anomalies restantes, aucun wording corrigé silencieusement.
- Statut : DONE ; quatre générateurs cession cabinets disponibles sous `DOC-009` à `DOC-012`, branchés au catalogue et à l'orchestrateur.

### RESUME-CODE-CESSION-CAB-001
- Objectif : reprendre proprement `CODE-CESSION-CAB-001` depuis `main` après absorption de la préparation dérogations et du sous-batch SPFPL.
- Entrées : `main` synchronisé, specs/arbitrages cession cabinets V1, état local CODE-CESSION non fusionné.
- Contraintes : repartir d'un état Git propre, ne pas reprendre de fichiers non suivis sans revue, conserver les blocages explicites déjà arbitrés.
- Statut : DONE ; branche reprise depuis `main`, travail cession restauré, validations locales et smoke DOCX verts.

### PREP-DEROG-001
- Objectif : préparer les sources de la famille `dérogations` avant code.
- Specs à lire : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`, `docs/delivery/lot_03_derogations_spec_texte_v1.md` et `docs/delivery/lot_03_derogations_arbitrages_v1.md`.
- Contraintes : placer uniquement les sources Lot 03 explicitement décidées, convertir ou remplacer le `.doc` legacy si `cumul_salariee` est ciblé, ne pas automatiser les formulaires manuels.
- Statut : DONE ; commit source `36828fbc45d6b8a37c2e76eb8227460df441ebde` absorbé dans `main`, sources Lot 03 placées et rapports de préparation disponibles.

### CODE-DEROG-CORE-001
- Objectif : implémenter le cœur de la famille `dérogations` après préparation des sources.
- Specs à lire : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`, `docs/delivery/lot_03_derogations_spec_texte_v1.md`, `docs/delivery/lot_03_derogations_arbitrages_v1.md` et `docs/delivery/lot_03_derogations_preparation_v1.md`.
- Contraintes : ne pas automatiser les formulaires manuels, distinguer document finalisé et formulaire à compléter, bloquer les narratifs sensibles manquants.
- Statut : DONE ; générateurs partiels `multi_sites_sel` et `cumul_sel_bnc` codés en formulaires à compléter, sources DOCX propres utilisées, `cumul_salariee` legacy non traité.

### CODE-SPFPL-AGR-INFO-001
- Objectif : implémenter le sous-batch SPFPL `agrément / note d'information` limité par les arbitrages V1.
- Specs à lire : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`, `docs/delivery/lot_05_spfpl_spec_texte_v1.md` et `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.
- Contraintes : piloter le wording cession/apport par `operation_spfpl.type`, bloquer l'acte de cession d'actions et les multi-souscripteurs, ne jamais rendre `OU` ou une double option non tranchée.
- Statut : DONE ; commit source `958fce5d2a9d5d30df4d918cb098fec483f5140e` absorbé dans `main`, générateurs ciblés SPFPL et tests intégrés.

### CODE-SPFPL-CORE-001
- Objectif : implémenter le cœur SPFPL restant dans le respect des specs et arbitrages V1.
- Specs à lire : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`, `docs/delivery/lot_05_spfpl_spec_texte_v1.md` et `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.
- Contraintes : rester limité aux documents SPFPL sourcés/arbitrés, bloquer l'acte de cession d'actions sans source DOCX confirmée, bloquer les multi-souscripteurs hors V1 et ne pas corriger le wording juridique sans validation explicite.
- Statut : DONE ; commit source `09cbad120d22910f05ba5e645971ade56fedb76d` absorbé dans `main`, générateurs SPFPL cœur et tests ciblés intégrés.

### PREP-STATUTS-001
- Objectif : préparer les sources statuts avant toute spécification ou implémentation.
- Entrées : source de vérité, raw dump, référentiels projet et décisions de placement/arbitrage sources.
- Contraintes : ne pas dédupliquer ni harmoniser les statuts sans comparaison documentée, ne pas coder de générateur, ne pas modifier le wording juridique source.
- Statut : DONE ; commit source `b854821061b85ac66fe785c11cb3c6b0bac5a85b` absorbé dans `main`, sources Lot 04 cadrées et écarts documentés.

### SPEC-STATUTS-SEL-001
- Objectif : spécifier les statuts SEL d'exercice avant tout codage.
- Specs/sources à lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et sources Lot 04 SELARL chirurgien-dentiste, SELARL médecin, SELAS médecin.
- Contraintes : comparer les variantes, extraire les variables, documenter les clauses sensibles, ne pas coder de générateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.

### SPEC-STATUTS-SPFPL-001
- Objectif : spécifier les statuts SPFPL cession/apport avant tout codage.
- Specs/sources à lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et sources Lot 04 SPFPL.
- Contraintes : traiter cession et apport en comparaison, conserver les sorties distinctes tant que la fusion n'est pas prouvée, ne pas coder de générateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`.

### SPEC-STATUTS-CIVILS-001
- Objectif : spécifier les statuts civils SCI, SCI IRIS, SCM et SCS avant tout codage.
- Specs/sources à lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et sources Lot 04 civiles.
- Contraintes : ne pas dédupliquer SCI/SCI IRIS/SCM/SCS sans analyse documentée, identifier les variables capital, associés, siège, objet et options fiscales, ne pas coder de générateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.

### SPEC-STATUTS-SAS-001
- Objectif : spécifier les statuts SAS avant tout codage.
- Specs/sources à lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et source Lot 04 SAS.
- Contraintes : vérifier le fichier source dont le nom contient aussi SPFPL, traiter séparément la liste des souscripteurs et l'attestation sur le capital si nécessaire, ne pas coder de générateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`.

### SYNC-STATUTS-SPECS-001
- Objectif : absorber dans `main` les specs statuts parallèles SAS, SPFPL, SEL et civils.
- Entrées : branches `codex/spec-statuts-sas-001`, `codex/spec-statuts-spfpl-001`, `codex/spec-statuts-sel-001` et `codex/spec-statuts-civils-001`.
- Sortie : commits de specs intégrés dans `main`, pilotage aligné et prochains tickets confirmés READY.
- Statut : DONE ; specs intégrées sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.

### CODE-STATUTS-SAS-001
- Objectif : implémenter les statuts SAS à partir des specs V1.
- Specs à lire : `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`.
- Contraintes : limiter le périmètre au modèle SAS/SPFPL médecins source, bloquer les cas non arbitrés, ne pas corriger le wording juridique sans validation.
- Statut : DONE ; générateur SAS V1 intégré dans `main` avec tests ciblés.

### CODE-STATUTS-SPFPL-001
- Objectif : implémenter les statuts SPFPL cession/apport à partir des specs V1.
- Specs à lire : `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`.
- Contraintes : conserver deux overlays cession/apport, bloquer le multi-associés non arbitré et les anomalies de wording non validées.
- Statut : DONE ; générateurs SPFPL cession/apport V1 intégrés dans `main` avec tests ciblés.

### ARBITRAGE-STATUTS-SEL-001
- Objectif : arbitrer les points bloquants des statuts SEL avant code.
- Specs à lire : `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.
- Contraintes : trancher pluralité des associés, ligne `personne_2`, second lieu SELAS, féminisation dirigeant et signatures.
- Statut : DONE ; arbitrages disponibles dans `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`.

### ARBITRAGE-STATUTS-CIVILS-001
- Objectif : arbitrer les points bloquants des statuts civils avant code.
- Specs à lire : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.
- Contraintes : trancher SCI/SCI IRIS, SCM, SCS, associés personnes morales, signatures dynamiques et lettre option IS hors statuts.
- Statut : DONE ; arbitrages disponibles dans `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.

### SYNC-STATUTS-CODE-ARB-001
- Objectif : absorber dans `main` les branches code statuts SAS/SPFPL et arbitrage statuts SEL.
- Entrées : `codex/code-statuts-sas-001`, `codex/code-statuts-spfpl-001`, `codex/arbitrage-statuts-sel-001`.
- Sortie : commits intégrés, tests relancés, pilotage aligné sur les tickets suivants.
- Statut : DONE ; intégration effectuée sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.

### CODE-STATUTS-SEL-001
- Objectif : implémenter les statuts SEL d'exercice après arbitrages V1.
- Specs à lire : `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`, `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`.
- Contraintes : appliquer strictement les arbitrages SEL, conserver les blocages explicites et ne pas corriger le wording juridique sans validation.
- Statut : DONE ; générateurs SEL d'exercice V1 intégrés dans `main` avec tests ciblés.

### CODE-STATUTS-CIVILS-CORE-001
- Objectif : implémenter le cœur des statuts civils après arbitrages V1.
- Specs à lire : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md`, `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md` et `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.
- Contraintes : couvrir uniquement SCS, SCI et SCI IRIS dans ce ticket, utiliser `associes[]`, bloquer les données legacy insuffisantes et garder l'option IS hors générateur statuts.
- Statut : DONE ; SCM reste hors ticket à cause des ambiguïtés source documentées.

### RESUME-ARBITRAGE-STATUTS-CIVILS-001
- Objectif : reprendre proprement l'arbitrage des statuts civils depuis `main` synchronisé.
- Specs à lire : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.
- Contraintes : arbitrer SCI/SCI IRIS, SCM, SCS, associés personnes morales, signatures dynamiques et lettre option IS hors statuts avant tout code.
- Statut : DONE ; remplacé par l'absorption de `ARBITRAGE-STATUTS-CIVILS-001`.

### STYLE-ANALYSE-BATCH-001
- Objectif : cadrer l'analyse de style documentaire en batch avant harmonisation de rendu.
- Entrées : générateurs existants, specs disponibles et rendus DOCX déjà produits hors versionnement.
- Contraintes : analyse/cadrage uniquement, sans modification de wording juridique ni déplacement de sources.
- Statut : DONE ; blueprint disponible dans `docs/delivery/render_style_blueprint_batch_v1.md`.

### FIX-STYLE-LETTERS-001
- Objectif : corriger les écarts de style prioritaires des lettres à partir du blueprint batch V1.
- Specs à lire : `docs/delivery/render_style_blueprint_batch_v1.md` et specs texte des lettres concernées.
- Contraintes : ne pas modifier le wording juridique, limiter les changements au rendu DOCX, conserver les artefacts hors versionnement.
- Statut : DONE ; rendu lettres harmonisé et absorbé dans `main` via `RESUME-FIX-STYLE-LETTERS-001`.

### RESUME-FIX-STYLE-LETTERS-001
- Objectif : reprendre proprement la correction des écarts de style prioritaires des lettres depuis `main` synchronisé.
- Specs à lire : `docs/delivery/render_style_blueprint_batch_v1.md` et specs texte des lettres concernées.
- Contraintes : ne pas modifier le wording juridique, limiter les changements au rendu DOCX, conserver les artefacts hors versionnement.
- Statut : DONE ; commit source `557fc1920361a8c7831e6b023d70471c9c29e5ff` absorbé dans `main`.

### ARBITRAGE-STATUTS-SCM-001
- Objectif : arbitrer les points bloquants statuts SCM avant toute implémentation.
- Specs à lire : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md`, `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md` et `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.
- Contraintes : traiter l'anomalie source de parts et la ligne fixe `510 euros` avant code.
- Statut : DONE ; arbitrages V1 disponibles dans `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md`.

### PREP-SCM-SAT-001
- Objectif : préparer le périmètre SCM et satellites avant spécification/code.
- Specs à lire : specs statuts civils V1 et arbitrages SCM à venir.
- Contraintes : ne pas déplacer de sources sans décision explicite et documenter tout blocage de source.
- Statut : DONE ; préparation V1 disponible dans `docs/delivery/lot_05_scm_satellites_preparation_v1.md`.

### SPEC-SAS-SATELLITES-001
- Objectif : spécifier les satellites SAS avant code.
- Specs à lire : specs statuts SAS V1 et sources satellites à confirmer.
- Contraintes : conserver le wording source et isoler les satellites du générateur statuts SAS existant.
- Statut : DONE ; specs V1 disponibles dans `docs/delivery/lot_05_sas_satellites_spec_canonique_v1.md` et `docs/delivery/lot_05_sas_satellites_spec_texte_v1.md`.

### CODE-OPTION-IS-001
- Objectif : implémenter la lettre option IS hors générateurs statuts.
- Specs à lire : spec/arbitrage applicable avant code.
- Contraintes : ne pas intégrer l'option IS dans les statuts civils ; générer un document dédié avec tests.
- Statut : DONE ; générateur et tests intégrés dans `main`.

### PREP-ACTE-ACTIONS-001
- Objectif : préparer les sources de l'acte de cession d'actions.
- Specs à lire : specs/arbitrages SPFPL V1 et source documentaire à confirmer.
- Contraintes : ne pas coder sans source DOCX confirmée.
- Statut : DONE ; audit V1 disponible dans `docs/delivery/lot_05_acte_cession_actions_audit_v1.md`.

### CODE-STATUTS-SCM-001
- Objectif : implémenter les statuts SCM.
- Specs à lire : specs statuts civils V1 et arbitrages SCM V1.
- Contraintes : respecter les arbitrages SCM, bloquer toute ambiguïté de wording, ajouter tests et branchement orchestrateur ciblés.
- Statut : DONE ; générateur statuts SCM intégré sous `DOC-025` avec tests ciblés.

### CODE-SAS-SATELLITES-001
- Objectif : implémenter les satellites SAS.
- Specs à lire : specs satellites SAS V1.
- Contraintes : isoler les satellites du générateur statuts SAS existant et conserver le wording source.
- Statut : DONE ; générateurs satellites SAS intégrés et testés.

### SPEC-SCM-SATELLITES-001
- Objectif : spécifier les satellites SCM avant code.
- Specs à lire : préparation SCM satellites V1 et sources Lot 05 confirmées.
- Contraintes : ne pas coder les satellites SCM sans spec canonique et texte.
- Statut : DONE ; specs canonique et texte disponibles dans `docs/delivery/`.

### CONVERT-ACTE-ACTIONS-001
- Objectif : convertir ou remplacer la source de l'acte de cession d'actions.
- Specs à lire : audit acte de cession d'actions V1.
- Contraintes : ne pas automatiser l'acte tant qu'une source DOCX propre n'est pas confirmée.
- Statut : DONE ; DOCX converti dans `project/source_documents/lot_05/` et préparation disponible dans `docs/delivery/lot_05_acte_cession_actions_preparation_v1.md`.

### CONVERT-DEROG-SALARIEE-001
- Objectif : convertir ou remplacer la source legacy de dérogation salariée.
- Specs à lire : préparation dérogations V1 et arbitrages dérogations V1.
- Contraintes : ne pas coder `cumul_salariee` sans source DOCX exploitable.
- Statut : DONE ; tentative Word COM retentée, aucun DOCX produit, blocage documenté dans `docs/delivery/lot_03_derogation_salariee_conversion_blocker_v1.md`.

### SPEC-ACTE-ACTIONS-001
- Objectif : spécifier l'acte de cession d'actions SPFPL avant tout code.
- Specs à lire : audit et préparation acte de cession d'actions V1.
- Contraintes : ne pas coder sans spec canonique et texte.
- Statut : DONE ; specs canonique et texte disponibles dans `docs/delivery/`.

### SPEC-DEROG-SALARIEE-MANUAL-001
- Objectif : spécifier le traitement manuel ou le blocage V1 de la dérogation salariée legacy.
- Specs à lire : préparation dérogations V1 et blocage conversion salariée V1.
- Contraintes : ne pas automatiser sans source DOCX exploitable.
- Statut : DONE ; stratégie V1 documentée dans `docs/delivery/lot_03_derogation_salariee_v1_strategy.md`.

### PREP-SCM-LISTE-DEPENSES-CONVERT-001
- Objectif : préparer une source exploitable pour la liste de dépenses SCM.
- Specs à lire : préparation SCM satellites V1.
- Contraintes : ne pas toucher au raw dump ; documenter tout blocage de conversion.
- Statut : DONE ; DOCX exploitable placé dans `project/source_documents/lot_05/` et préparation documentée.

### CODE-SCM-SAT-DOCX-001
- Objectif : implémenter les satellites SCM DOCX hors liste dépenses.
- Specs à lire : specs satellites SCM V1.
- Contraintes : ne pas coder la liste dépenses dans ce ticket ; conserver le wording source des trois DOCX.
- Statut : DONE ; générateurs `DOC-026`, `DOC-027` et `DOC-028` intégrés et testés.

### CODE-SCM-LISTE-DEPENSES-001
- Objectif : implémenter la liste des dépenses communes SCM.
- Specs à lire : specs satellites SCM V1 et préparation conversion liste dépenses.
- Contraintes : limiter le ticket à la liste dépenses communes SCM, avec tests ciblés.
- Statut : DONE ; générateur liste dépenses communes SCM intégré et testé.

### CODE-ACTE-ACTIONS-001
- Objectif : implémenter l'acte de cession d'actions SPFPL.
- Specs à lire : specs acte actions V1 et préparation source.
- Contraintes : ne pas modifier le wording juridique hors spec.
- Statut : DONE ; générateur acte de cession d'actions SPFPL intégré et testé.

### SPEC-SCM-CESSION-BLOCK-001
- Objectif : spécifier le blocage ou le périmètre de la cession SCM.
- Specs à lire : arbitrages SCM et sources SCM cession disponibles.
- Contraintes : pas de code avant décision documentée.
- Statut : DONE ; specs canonique et texte disponibles dans `docs/delivery/`.

### CODE-SCM-CESSION-BLOCK-001
- Objectif : implémenter le blocage explicite de la cession SCM.
- Specs à lire : `docs/delivery/lot_05_scm_cession_block_spec_canonique_v1.md` et `docs/delivery/lot_05_scm_cession_block_spec_texte_v1.md`.
- Contraintes : ne pas générer de document cession SCM tant que le blocage V1 s'applique ; tests ciblés obligatoires.
- Statut : DONE ; blocage explicite cession SCM historique, levé par `FINAL-SCM-CESSION-WAVE-001` selon résolution V1.

### REVIEW-BATCH-LOT03-001
- Objectif : documenter la revue juridique/visuelle du batch Lot 03.
- Specs à lire : specs et arbitrages Lot 03, smoke DOCX disponibles.
- Contraintes : revue uniquement, sans modification de wording juridique.
- Statut : DONE ; revue disponible dans `docs/review/lot_03_batch_review_v1.md`.

### REVIEW-BATCH-LOT04-001
- Objectif : documenter la revue juridique/visuelle du batch Lot 04.
- Specs à lire : specs et arbitrages statuts Lot 04, smoke DOCX disponibles.
- Contraintes : revue uniquement, sans modification de wording juridique.
- Statut : DONE ; revue disponible dans `docs/review/lot_04_batch_review_v1.md`.

### AUDIT-REMAINING-SCOPE-001
- Objectif : auditer le périmètre restant après les vagues SCM, statuts et acte actions.
- Specs à lire : board, dernier état, registre moteur et specs disponibles.
- Contraintes : audit documentaire, sans code ni déplacement de sources.
- Statut : DONE ; audit disponible dans `docs/project/15_REMAINING_SCOPE_AUDIT_V1.md`.

### STYLE-ANALYSE-LOT03-BATCH-001
- Objectif : analyser le style du batch Lot 03 avant harmonisation.
- Specs à lire : générateurs Lot 03, specs texte et rendus disponibles.
- Contraintes : analyse de rendu uniquement, sans modification de wording juridique.
- Statut : DONE ; blueprint disponible dans `docs/delivery/render_style_blueprint_lot03_batch_v1.md`.

### STYLE-ANALYSE-STATUTS-BATCH-001
- Objectif : analyser le style du batch statuts avant harmonisation.
- Specs à lire : specs et générateurs statuts intégrés.
- Contraintes : analyse et cadrage avant modification de rendu.
- Statut : DONE ; blueprint disponible dans `docs/delivery/render_style_blueprint_statuts_batch_v1.md`.

### PREP-SCM-CESSION-SOURCES-001
- Objectif : préparer les sources cession SCM.
- Specs à lire : plan de placement sources et raw dump SCM cession.
- Contraintes : ne pas toucher au raw dump ; documenter tout placement ou blocage.
- Statut : DONE ; sources cession SCM placées dans `project/source_documents/lot_05/` et préparation documentée.

### FIX-STYLE-LOT03-BATCH-001
- Objectif : corriger les écarts de style prioritaires du batch Lot 03.
- Specs à lire : `docs/delivery/render_style_blueprint_lot03_batch_v1.md`.
- Contraintes : limiter les changements au rendu DOCX, sans dérive de wording juridique.
- Statut : DONE ; rendu Lot 03 harmonisé avec tests ciblés.

### FIX-STYLE-STATUTS-BATCH-001
- Objectif : corriger les écarts de style prioritaires du batch statuts.
- Specs à lire : `docs/delivery/render_style_blueprint_statuts_batch_v1.md`.
- Contraintes : limiter les changements au rendu DOCX, sans dérive de wording juridique.
- Statut : DONE ; rendu statuts harmonisé avec tests ciblés.

### REVIEW-BATCH-LOT05-001
- Objectif : documenter la revue juridique/visuelle du batch Lot 05.
- Specs à lire : specs Lot 05, générateurs intégrés et smoke DOCX disponibles.
- Contraintes : revue uniquement, sans modification de wording juridique.
- Statut : DONE ; revue disponible dans `docs/review/lot_05_batch_review_v1.md`.

### ARBITRAGE-SCM-CESSION-RESOLVE-001
- Objectif : arbitrer la résolution de la cession SCM après blocage V1 et vague style/revue.
- Specs à lire : specs cession SCM, sources préparées et revues Lot 05.
- Contraintes : décision métier avant tout code documentaire de cession SCM.
- Statut : DONE ; arbitrage absorbé dans `main`.

### FINAL-SCM-CESSION-WAVE-001
- Objectif : finaliser le bloc cession SCM V1 et clôturer la vague moteur documentaire.
- Specs à lire : résolution V1 cession SCM, specs canonique/texte, six sources SCM cession et audit moteur.
- Contraintes : DOCX uniquement, sans UI, PDF, ZIP, ni versionnement de `artifacts/`.
- Statut : DONE ; `DOC-031`, `DOC-032` et `DOC-033` sont branchés, testés et couverts par smoke DOCX réel.

### SYNC-CLOSE-AUDIT-001
- Objectif : absorber proprement le commit d'audit moteur `0139202b170531fd628f25811c55855a2512acc0` dans `main`.
- Contraintes : conserver l'audit de clôture plus récent déjà présent dans `main`, sans modification de code Python.
- Statut : DONE ; merge de synchronisation effectué, `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` confirmé présent.

### RECONCILE-MOTOR-CLOSE-001
- Objectif : lever les incohérences finales signalées par `FINAL-MOTOR-AUDIT-002` et clôturer le moteur DOCX V1.
- Contraintes : correction minimale, aucun wording juridique modifié, aucun toucher à `project/source_import/raw_drive_dump/` ni `artifacts/`.
- Statut : DONE ; runtime aligné sur 43 documents, audits `16/17/18` et référentiels `08/09` consolidés.
- Validation : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 176 tests passés.

### PDF-BACKEND-001
- Objectif : ajouter une capacité locale d'export PDF depuis les DOCX générés, sans toucher à l'UI ni modifier le contenu juridique.
- Contraintes : backend best-effort explicite, erreurs bloquantes si aucun convertisseur fiable n'est disponible, `artifacts/` hors versionnement.
- Statut : DONE ; `src/sydel_doc_engine/rendering/pdf_export.py` expose l'export DOCX vers PDF avec priorité LibreOffice headless puis fallback Word COM Windows.
- Validation : tests ciblés OK, smoke réel DOCX vers PDF OK via Word COM ; validations globales ruff/pytest à jour.

### UI-FLOW-001
- Objectif : cadrer le flux Streamlit V1 post-moteur sans implémenter l'UI.
- Sortie : `docs/project/19_UI_FLOW_V1.md`.
- Statut : DONE ; commit source `d62670efe10481926437c0e1a5dabbe349fd5938` absorbé dans `main`.

### UI-OCCURRENCES-001
- Objectif : cadrer les occurrences documentaires nécessaires à l'UI V1.
- Sortie : `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md`.
- Statut : DONE ; commit source `24a881b999371811d39a2403c0b51d9ae8ce0556` absorbé dans `main`.

### UI-FORM-SCHEMA-001
- Objectif : cadrer le schéma formulaire UI V1.
- Sortie : `docs/project/21_UI_FORM_SCHEMA_V1.md`.
- Statut : DONE ; commit source `ef6252b3c15dc3fc39f1efdc05687c0f448f8fe1` absorbé dans `main`.

### RECIPE-FRAME-001
- Objectif : cadrer la recette finale V1.
- Sortie : `docs/review/final_recipe_framework_v1.md`.
- Statut : DONE ; commit source `c2fc0db4d51485c7c5e721c5184028ae17c68cb3` absorbé dans `main`.

### SYNC-POST-MOTOR-UI-001
- Objectif : intégrer proprement les fondations UI/PDF/recette dans `main`.
- Entrées : branches `codex/ui-flow-001`, `codex/ui-occurrences-001`, `codex/ui-form-schema-001`, `codex/pdf-backend-001`, `codex/recipe-frame-001`.
- Contraintes : ne pas toucher à `project/source_import/raw_drive_dump/` ni à `artifacts/`.
- Statut : DONE ; les cinq commits sources sont absorbés dans `main` et le pilotage confirme `UI-CORE-001`, `RESUME-ZIP-BACKEND-001` et `REVIEW-FINAL-001` en READY.
- Validation : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 182 tests passés.

### UI-CORE-001
- Objectif : implémenter le cœur Streamlit V1 à partir des référentiels UI absorbés.
- Prérequis : `docs/project/19_UI_FLOW_V1.md`, `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md`, `docs/project/21_UI_FORM_SCHEMA_V1.md`, orchestrateur moteur clos et backend PDF disponible.
- Statut : DONE par remplacement ; le périmètre est superseded / remplacé par `UI-PDF-ZIP-INTEGRATION-001`, qui livre directement le flux Streamlit dossier avec DOCX, PDF local optionnel et ZIP.

### RESUME-ZIP-BACKEND-001
- Objectif : reprendre le backend ZIP V1 sur `main` synchronisé.
- Prérequis : moteur DOCX clos, backend PDF intégré et fondation phase 18.
- Statut : DONE ; le backend ZIP déterministe `src/sydel_doc_engine/rendering/zip_bundle.py` est présent, testé et utilisé par le runtime UI.

### REVIEW-FINAL-001
- Objectif : exécuter la revue finale V1 après intégration UI/PDF/ZIP.
- Prérequis : moteur DOCX clos, UI cœur, PDF et ZIP intégrés.
- Statut : DONE ; rapport d'execution disponible dans `docs/review/review_final_001_execution_report_v1.md`.
- Decision : GO avec reserves pour lancer `UI-BUSINESS-WIZARD-001`.
- Reserves : `git fetch --prune` bloque sur `.git/FETCH_HEAD`, backend PDF local indisponible pendant la revue, la detection Word COM peut accrocher un processus Word, et la majorite des contextes exemples sont des contextes de famille/generateur incomplets pour le flux dossier global.

### UI-PDF-ZIP-INTEGRATION-001
- Objectif : brancher les sorties DOCX, PDF local optionnel et ZIP dossier dans l'UI Streamlit.
- Prérequis : moteur DOCX clos, backend PDF `rendering/pdf_export.py`, backend ZIP disponible sous `rendering/zip_bundle.py`.
- Statut : DONE ; l'UI charge un contexte YAML/JSON, affiche la sélection orchestrateur, génère les DOCX, propose les téléchargements DOCX, tente les PDF si un backend local est disponible et produit un ZIP déterministe avec manifeste.
- Limitation : le PDF dépend de l'environnement local LibreOffice ou Word COM ; un échec PDF est affiché sans modifier les DOCX.
- Smoke manuel : `docs/review/ui_pdf_zip_integration_001_smoke.md`.

### SYNC-FINAL-FOUNDATIONS-001
- Objectif : réaligner `main` avant revue/clôture avec les fondations UI, audits, PDF, ZIP et recette finale.
- Entrées : `codex/ui-flow-001`, `codex/ui-occurrences-001`, `codex/ui-form-schema-001`, `codex/pdf-backend-001`, `codex/recipe-frame-001`, `codex/ui-pdf-zip-integration-001`, `codex/zip-backend-001`, `codex/close-motor-audit-001`, `codex/final-motor-audit-002`, `codex/next-phase-foundation-001`.
- Contraintes : ne pas toucher à `project/source_import/raw_drive_dump/` ni à `artifacts/`.
- Statut : DONE ; les fichiers critiques de cadrage/clôture sont présents sur `main`, l'UI intégrée et les backends PDF/ZIP sont présents, et le pilotage confirme uniquement `REVIEW-FINAL-001` et `CLOSE-PROJECT-V1-001` en READY.
- Validation : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 191 tests passés.

### WORKTREE-CLEANUP-AND-UI-STATUS-001
- Objectif : rendre le poste local lisible avec un seul dossier canonique, consolider le contenu restant de `codex/review-final-001` dans `main` et clarifier le statut reel de l'UI.
- Entrées : worktree `main`, branches locales/distantes, dossier parent `C:\Users\Gad\Desktop\Sydel\`, branche `codex/review-final-001`.
- Contraintes : archiver sans suppression definitive, ne pas toucher a `project/source_import/raw_drive_dump/`, ne pas inventer d'UI wizard non implementee.
- Statut : DONE ; `docs/review/final_review_pack_v1.md` est integre dans `main`, `docs/project/23_WORKTREE_CLEANUP_AND_UI_STATUS_V1.md` documente l'etat local et l'UI actuelle est qualifiee comme UI technique de pilotage par contexte, pas UI produit finale.

### CLOSE-PROJECT-V1-001
- Objectif : clore le projet V1 après revue finale.
- Prérequis : `REVIEW-FINAL-001` terminé.
- Statut : READY.

### UI-BUSINESS-WIZARD-001
- Objectif : lancer le wizard metier dossier-centre a partir des specs UI `19_UI_FLOW_V1.md`, `20_UI_DOCUMENT_OCCURRENCES_V1.md` et `21_UI_FORM_SCHEMA_V1.md`.
- Prérequis : `REVIEW-FINAL-001` termine, moteur DOCX/ZIP vert, reserves PDF et contextes exemples documentees.
- Statut : DONE.
- Livraison : mode `Assistant metier` ajoute dans Streamlit avec formulaire structure, validation, liste de documents, generation DOCX, ZIP et PDF optionnel ; mode `Technique / diagnostic` YAML/JSON conserve.
- Perimetre V1 : generation assistant limitee au scenario SCI simple pour `DOC-001`, `DOC-002`, `DOC-003` et `DOC-004`.
- Rapport : `docs/review/ui_business_wizard_001_report_v1.md`.
- Garde-fous : ne pas relancer l'ancien `UI-WIZARD-001`, ne pas dupliquer la selection documentaire hors orchestrateur, ne pas presenter la generation comme validation juridique.

### CASE-CATALOG-001
- Objectif : creer la couche metier `catalogue des cas` depuis la source de verite produit, sans modifier l'UI, le moteur DOCX/PDF/ZIP ni les generateurs.
- Source analysee : `project/source_truth/Documents_a_generer_par_cas.docx` ; les chemins `docs/source_truth/*` demandes par le ticket ne sont pas presents dans ce workspace.
- Statut : DONE.
- Livraison : `src/sydel_doc_engine/domain/case_catalog.py` expose `CaseType`, `CaseCondition`, `DocumentOccurrence`, `DocumentAvailability`, `ExpectedDocument` et `get_expected_documents(...)`.
- Couverture courante après `SELARL-PILOT-SOURCE-VERIFY-001` : 8 familles, 46 documents attendus uniques, 104 occurrences source, 43 documents mappes a `DOC-XXX`, 41 documents `GENERATABLE`, 4 documents `MANUAL_ONLY`, 1 document `NOT_IMPLEMENTED`, 0 `NEEDS_MAPPING`.
- Rapport : `docs/review/case_catalog_001_report_v1.md`.
- Prochaine etape realisee : `UI-CASE-WIZARD-002`.

### UI-CASE-WIZARD-002
- Objectif : brancher le mode `Assistant metier` Streamlit sur `get_expected_documents(...)` pour piloter l'affichage documentaire depuis CASE-CATALOG-001.
- Prerequis : `CASE-CATALOG-001`, docs UI 19/20/21, assistant metier existant et mode technique YAML/JSON conserve.
- Statut : DONE.
- Livraison : conditions UI par famille, tableau des documents attendus avec statuts `Generable`, `A remplir manuellement`, `Non implemente`, `Mapping a confirmer`, blocages de champs et contexte incomplet V2.
- Generation : filtree sur les documents attendus, `GENERATABLE`, avec `document_code`, et prets dans le contexte formulaire ; documents manuels/non implementes exclus.
- Rapport : `docs/review/ui_case_wizard_002_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 217 tests passes.
- Prochaine etape recommandee : `UI-CASE-WIZARD-003`, enrichir les blocs formulaire pour rendre generables les documents aujourd'hui marques contexte incomplet V2, par famille ou lot limite.

### SELARL-PILOT-PROTOCOL-001
- Objectif : reprendre le cadrage produit de l'Assistant metier a partir du processus pilote SELARL et de la source V2 fournie par l'associe.
- Source V2 : `project/source_truth/Documents_a_generer_par_cas_V2.docx`, copie du fichier non suivi initial `docs/docssource_truth/Documents à générer par cas.docx`.
- Statut : DONE.
- Livraison : `docs/project/PROCESS_BUILD_PROTOCOL_V1.md`, `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md`, `docs/project/SELARL_UI_WIZARD_SPEC_V1.md`, `docs/project/SELARL_IMPLEMENTATION_PLAN_V1.md`.
- Rapport : `docs/review/selarl_pilot_protocol_001_report_v1.md`.
- Decisions historiques : pas de modification UI/moteur/generateurs ; `PV d'autorisation d'emprunt` traite comme branche conditionnelle du `DOC-004` ; wording SELARL ensuite corrigé par `SELARL-PLAN-CORRECTION-001` vers `Fiche Client` / `Praticien`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 217 tests passes.
- Prochaine etape recommandee : `SELARL-FORM-SCHEMA-IMPL-001`.

### SELARL-PILOT-SOURCE-VERIFY-001
- Objectif : vérifier les livrables SELARL contre la vraie source V2 fournie par l'associé, puis corriger uniquement les écarts.
- Source V2 vérifiée : `project/source_truth/Documents_a_generer_par_cas_V2.docx`, hash SHA-256 `2E9843AA1EC05A01D82DF5FCE12516A8EF49EA2B3842547D186204218C90B23F`.
- Statut : DONE.
- Livraison : `docs/review/selarl_source_verify_001_report_v1.md`, source V2 canonique remplacée, specs SELARL réconciliées, `case_catalog.py` aligné sur les statuts dérogation V2.
- Décisions : `DOC-013` et `DOC-014` restent connus côté moteur mais sont `MANUAL_ONLY` dans le catalogue produit ; `DOC-006` garde une réserve source V2.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 217 tests passés.
- Prochaine étape recommandée : `SELARL-FORM-SCHEMA-IMPL-001`.

### SELARL-FORM-SCHEMA-IMPL-001
- Objectif : implémenter le schéma de données SELARL côté Assistant métier, sans refaire l'UI visible et sans modifier les générateurs ni le moteur DOCX/PDF/ZIP.
- Source V2 utilisée : `project/source_truth/Documents_a_generer_par_cas_V2.docx`, hash SHA-256 `2E9843AA1EC05A01D82DF5FCE12516A8EF49EA2B3842547D186204218C90B23F`.
- Statut : DONE.
- Livraison : `src/sydel_doc_engine/app/selarl_form_schema.py` expose blocs métier, champs qualifiés, règles de réutilisation, documents attendus SELARL, codes générables et couverture des variables V2.
- Corrections QA : `DOC-006` porte une réserve source V2 exploitable dans le catalogue ; le rapport source V2 clarifie que `DOC-013` et `DOC-014` sont finaux `MANUAL_ONLY`.
- Garde-fous : `DOC-013` et `DOC-014` restent visibles mais exclus des codes générables SELARL ; aucun changement Streamlit, moteur DOCX/PDF/ZIP ou générateur.
- Rapport : `docs/review/selarl_form_schema_impl_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 231 tests passés.
- Prochaine étape recommandée : `SELARL-UI-WIZARD-IMPL-001`.

### SELARL-UI-WIZARD-IMPL-001
- Objectif : brancher l'Assistant métier visible sur le schéma SELARL, sans modifier les générateurs ni le moteur DOCX/PDF/ZIP.
- Statut : DONE.
- Livraison : parcours Streamlit SELARL en écrans qualification, société, professionnel/gérant, associés, conditions spécifiques, documents attendus et génération.
- Schéma consommé : conditions, labels, blocs, règles de réutilisation, champs par bloc et documents depuis `selarl_form_schema.py` via `business_wizard.py`.
- Garde-fous : mode SCI existant et mode Technique / diagnostic conservés ; `DOC-006` affiché avec réserve ; `DOC-013` et `DOC-014` visibles mais `MANUAL_ONLY` et exclus de la génération automatique.
- Rapport : `docs/review/selarl_ui_wizard_impl_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 239 tests passés.
- Prochaine étape recommandée corrigée : `SELARL-WORDING-REALIGN-001`, puis `SELARL-FLOW-REALIGN-001` avant tout smoke réaliste.

### SELARL-NOTEBOOKLM-RECONCILIATION-001
- Objectif : reprendre le cadrage SELARL avec la hiérarchie NotebookLM / V3 / templates / code, sans coder ni modifier l'UI ou les générateurs.
- Statut : DONE.
- Sources ajoutées : `project/source_truth/notebooklm_selarl_10_prompts_v1.md` et `project/source_truth/Documents_a_generer_par_cas_V3.docx`, commit source `f1da08b`.
- Livraison : `docs/project/SELARL_SOURCE_HIERARCHY_V2.md`, `docs/review/selarl_notebooklm_reconciliation_001_report_v1.md`, `docs/project/SELARL_REBUILD_BACKLOG_V2.md`.
- Diagnostic initial : le cadrage documentaire V2/V3 est conservable, mais le wording, l'ordre du formulaire et les réutilisations doivent être corrigés avant smoke.
- Garde-fous : aucun fichier Python, générateur, moteur DOCX/PDF/ZIP ou UI modifié.
- Tests : non lancés ; ticket documentaire Markdown uniquement.
- Prochaine étape recommandée : `SELARL-WORDING-REALIGN-001`.

### SELARL-PLAN-CORRECTION-001
- Objectif : corriger la planification SELARL selon les arbitrages explicites de l'associé, sans modifier le code applicatif.
- Statut : DONE.
- Arbitrages intégrés : `Fiche Client`, `Praticien`, logique `Dossier unipersonnel`, abandon du mode Projet / filigrane V1, pas de couche produit documentaire lourde, mandataire hors priorités UX si aucune variable ne l'impose.
- Livraison : hiérarchie de sources, rapport de réconciliation et backlog V2 corrigés.
- Garde-fous : aucun fichier Python, générateur, moteur DOCX/PDF/ZIP ou UI modifié ; ne pas pousser ni redéployer l'UI SELARL existante avant réalignement produit.
- Tests : non lancés ; modifications documentaires uniquement.
- Prochaine étape recommandée : `SELARL-WORDING-REALIGN-001`.

### SELARL-WORDING-REALIGN-001
- Objectif : réaligner uniquement le vocabulaire visible SELARL sur `Fiche Client`, `Praticien` et les rôles juridiques exacts.
- Statut : DONE.
- Livraison : labels visibles corrigés dans le schéma, Streamlit et specs actives ; rapport `docs/review/selarl_wording_realign_001_report_v1.md`.
- Garde-fous : aucun générateur, moteur DOCX/PDF/ZIP, `case_catalog.py`, ordre d'écran ou règle de réutilisation fonctionnelle modifié.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 241 tests passés.
- Prochaine étape recommandée : `SELARL-FLOW-REALIGN-001`.

### SELARL-FLOW-REALIGN-001
- Objectif : réaligner l'ordre conceptuel SELARL dans le schéma et les projections métier, sans générateurs ni moteur DOCX/PDF/ZIP.
- Statut : DONE.
- Livraison : `FormStep`, `SELARL_FLOW_STEPS`, projections par étape dans `business_wizard.py`, specs actives mises à jour et rapport `docs/review/selarl_flow_realign_001_report_v1.md`.
- Ordre cible : Qualification, Fiche Client / Praticien, Fiche Société, Capital & Associés, Contexte & scénarios métier, Documents & génération.
- Garde-fous : `streamlit_app.py` non modifié ; réordonnancement visible complet repoussé à `SELARL-UI-REALIGN-001` après les règles de réutilisation.
- Tests : `.\.venv\Scripts\python.exe -m pytest tests/unit/test_selarl_form_schema.py tests/unit/test_business_wizard.py` OK, 41 tests passés ; `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 245 tests passés.
- Prochaine étape recommandée : `SELARL-REUSE-RULES-REALIGN-001`.

### SELARL-REUSE-RULES-REALIGN-001
- Objectif : réaligner les règles de réutilisation SELARL, sans générateurs ni moteur DOCX/PDF/ZIP.
- Statut : DONE.
- Livraison : `Dossier unipersonnel` ajouté comme règle pivot dans `selarl_form_schema.py` et projeté dans `business_wizard.py`.
- Règles : Praticien = associé unique = gérant = signataire seulement si `Dossier unipersonnel` est actif ; SELARL acquéreur, SELARL cessionnaire SCM et domiciliation = siège restent des options explicites ; mandataire / signataire n'est pas un défaut.
- Relations non automatiques : vendeur / locataire, siège / lieu d'exercice / cabinet, vendeur / Praticien et cédant SCM / Praticien.
- Garde-fous : `streamlit_app.py` non modifié ; documents attendus SELARL inchangés ; `DOC-013` et `DOC-014` restent exclus de la génération ; `DOC-006` conserve sa réserve.
- Rapport : `docs/review/selarl_reuse_rules_realign_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m pytest tests/unit/test_selarl_form_schema.py tests/unit/test_business_wizard.py` OK, 48 tests passés ; `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 252 tests passés.
- Prochaine étape recommandée : `SELARL-UI-REALIGN-001`.

### SELARL-UI-REALIGN-001
- Objectif : réaligner le parcours Streamlit visible SELARL sur le wording, le flow et les règles de réutilisation corrigés.
- Statut : DONE.
- Livraison : titres d'écrans dérivés du flow métier, Fiche Client avant Fiche Société, `Dossier unipersonnel` en qualification, écran 6 unique Documents & génération.
- Consommation schéma/projections : `selarl_ui_visible_screen_title(...)`, `selarl_ui_visible_fields_by_step(...)`, `selarl_ui_reuse_projection(...)`, `selarl_ui_reuse_rules()` et `selarl_ui_document_specs()`.
- Mandataire : déplacé dans un expander secondaire replié ; aucune assimilation au signataire par défaut.
- Garde-fous : générateurs, moteur DOCX/PDF/ZIP, `case_catalog.py`, parcours SCI et mode `Technique / diagnostic` non modifiés ; aucun mode Projet ni filigrane ajouté.
- Rapport : `docs/review/selarl_ui_realign_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m pytest tests/unit/test_business_wizard.py` OK, 34 tests passés ; `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 257 tests passés.
- Prochaine étape recommandée : `SELARL-SMOKE-REALISTIC-001`.

### SELARL-SMOKE-REALISTIC-001
- Objectif : smoke tester le parcours SELARL réaligné avec trois dossiers réalistes, sans générateurs ni moteur DOCX/PDF/ZIP modifiés.
- Statut : DONE.
- Scénarios exécutés : médecin unipersonnelle simple ; chirurgien-dentiste avec régime communautaire, site distinct et dérogation ; médecin avec cession de cabinet médical, bail et financement.
- Résultat génération : chaque scénario génère uniquement `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004` et un ZIP avec manifeste.
- Documents visibles non générés : `DOC-034`, statuts SELARL `DOC-016` / `DOC-017`, régime communautaire `DOC-005` / `DOC-006`, bail/cession `DOC-007` à `DOC-010` restent en contexte incomplet V2 selon scénario.
- Documents manuels : `DOC-013`, `DOC-014` et les formulaires sans code liés à la dérogation/site distinct restent visibles et exclus de génération.
- Contrôles : `DOC-006` conserve sa réserve, aucun document manuel n'entre dans les ZIP, le PV d'autorisation d'emprunt reste une option de `DOC-004`, `Dossier unipersonnel` produit les verrouillages attendus.
- Artefacts : `artifacts/selarl_smoke_realistic_001/20260519_185045/`.
- Rapport : `docs/review/selarl_smoke_realistic_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 257 tests passés.
- Prochaine étape courante : `SELARL-FINAL-ASSOCIE-VALIDATION-001`.

### SELARL-CLOUD-GENERATION-BUG-001
- Objectif : diagnostiquer le blocage utilisateur où le parcours SELARL visible ne permettait pas de générer, malgré le smoke local.
- Statut : DONE.
- Cause racine : état Streamlit de widgets dérivés désactivés conservé à vide lorsque `Dossier unipersonnel` ou la domiciliation par siège était coché avant la saisie des champs source.
- Correction : synchronisation explicite du `session_state` pour l'associé unique dérivé et l'adresse de domiciliation dérivée dans `streamlit_app.py`.
- Garde-fous : générateurs, moteur DOCX/PDF/ZIP, `case_catalog.py`, SCI et `Technique / diagnostic` non modifiés.
- Rapport : `docs/review/selarl_cloud_generation_bug_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m pytest tests/unit/test_business_wizard.py -q` OK, 35 tests passés ; `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 266 tests passés.
- Prochaine étape recommandée : rétablir les permissions Git locales, créer le commit de correction, push manuel puis redéploiement Streamlit Cloud et retest utilisateur SELARL.

### DOCUMENT-UNITAIRE-001
- Objectif : ajouter un mode Streamlit `Document unitaire` pour tester un seul document sans saisir tout un dossier.
- Statut : DONE.
- Implémentation : nouveau module UI pur `single_document_mode.py`, branchement dans `streamlit_app.py`, sélection par code/libellé et génération d'un DOCX unique via les services existants.
- Périmètre V1 : `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`; documents manuels affichés mais non générés ; documents hors périmètre marqués comme pas encore supportés dans ce mode.
- Garde-fous : générateurs, moteur DOCX/PDF/ZIP, catalogue métier, Assistant métier et mode `Technique / diagnostic` conservés.
- Rapport : `docs/review/document_unitaire_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 266 tests passés.
- Prochaine étape recommandée : revue utilisateur sur les quatre documents supportés, puis extension incrémentale document par document si les champs sont couverts.

### ASSISTANT-METIER-PREFILL-001
- Objectif : ajouter un préremplissage de test déterministe dans le seul mode `Assistant metier`.
- Statut : DONE.
- Implémentation : module dédié `src/sydel_doc_engine/app/test_prefill_presets.py`, sélecteur `Scénario de test`, boutons `Préremplir` et `Réinitialiser`, indication visible des données fictives chargées.
- Scénarios : `SELARL médecin unipersonnelle simple`, `SELARL chirurgien-dentiste + régime communautaire + site distinct`, `SELARL médecin + cession cabinet médical + bail + financement`, `SCI simple`.
- Garde-fous : générateurs, moteur DOCX/PDF/ZIP, wording juridique, mode `Technique / diagnostic` et mode `Document unitaire` non modifiés.
- Rapport : `docs/review/assistant_metier_prefill_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m pytest tests\unit\test_business_wizard.py -q` OK, 41 tests passés ; `.\.venv\Scripts\python.exe -m pytest tests\unit\test_single_document_mode.py tests\unit\test_ui_runtime.py -q` OK, 12 tests passés ; `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 272 tests passés.
- Prochaine étape courante : revue manuelle du pack actif `artifacts/selarl_closing_pack_005/`, puis `SELARL-CANONICAL-CLOSE-001` si l'associe valide.

### GLOBAL-VARIABLE-INVENTORY-001
- Objectif : construire un inventaire global brut des variables documentaires sur tout le périmètre moteur, sans décider les fusions.
- Statut : DONE.
- Livrables : `docs/project/GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv` et `docs/review/global_variable_inventory_001_report_v1.md`.
- Couverture : 12 443 lignes de variables brutes, 1 334 slugs normalisés distincts sur documents `DOC-XXX`, 43 documents `DOC-001` à `DOC-043` couverts, 15 familles couvertes.
- Sources : dictionnaire canonique V1, mapping documents/variables V1, arbre moteur, registre `catalog.py`, source truth V1/V2/V3, templates `project/source_documents/`, specs `docs/delivery/`, `case_catalog.py` en aide uniquement.
- Garde-fous : aucun générateur, moteur DOCX/PDF/ZIP, UI ou wording juridique modifié ; les groupes suspects sont signalés sans fusion canonique définitive.
- Validations : contrôle CSV/report, absence de lignes `UNMAPPED`, couverture complète `DOC-001` à `DOC-043`; aucun test Python requis car aucun fichier Python modifié.
- Prochaine étape réalisée : `GLOBAL-VARIABLE-IDENTITY-AUDIT-001`, audit d'identité sémantique et registre canonique global V2.

### GLOBAL-VARIABLE-IDENTITY-AUDIT-001
- Objectif : auditer l'identité sémantique globale des variables de tous les documents afin de minimiser le futur front sans fusionner des informations distinctes.
- Statut : DONE.
- Livrables : `docs/project/GLOBAL_VARIABLE_IDENTITY_MATRIX_V1.csv`, `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2.md`, `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V1.md` et `docs/review/global_variable_identity_audit_001_report_v1.md`.
- Couverture : 1 334 slugs normalisés distincts audités, 43 documents `DOC-001` à `DOC-043`, 15 familles, 49 champs canoniques V2 proposés, 142 rapprochements représentatifs, 10 questions humaines groupées.
- Décision : pas de fusion silencieuse ; les relations sont classées en `SAME_FIELD`, `SAME_DATA_DIFFERENT_SHAPE`, `EXPLICIT_REUSE_ONLY`, `DISTINCT_FIELDS` ou `UNCERTAIN_REQUIRES_HUMAN_DECISION`.
- Garde-fous : aucun générateur, moteur DOCX/PDF/ZIP, UI ou wording juridique modifié ; aucun test Python requis car aucun fichier Python modifié.
- Prochaine étape réalisée : `GLOBAL-HUMAN-ANSWERS-INTEGRATION-001`, intégrer les réponses humaines disponibles puis geler un registre V2.1 avant architecture front.

### GLOBAL-HUMAN-ANSWERS-INTEGRATION-001
- Objectif : intégrer les réponses humaines déjà obtenues dans l'audit global des variables et figer une version V2.1 du registre canonique global.
- Statut : DONE.
- Livrables : `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V2.md`, `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md` et `docs/review/global_human_answers_integration_001_report_v1.md`.
- Décisions : 4 questions V1 fermées, 5 questions restant arbitrables en interne, 1 question basculée en backlog documentaire ; règles V2.1 sur rôles, adresses, parties de cession, SCM, bail et cas futur SELAS micro-holding.
- Garde-fous : aucun générateur, moteur DOCX/PDF/ZIP, UI ou wording juridique modifié ; contradiction filigrane PROJET documentée mais non implémentée.
- Validation : relecture documentaire et contrôle du diff ; aucun test Python requis car aucun fichier Python modifié.
- Prochaine étape recommandée : `GLOBAL-FRONT-ARCHITECTURE-001`, concevoir l'architecture du nouveau front global sur le registre V2.1.

### GLOBAL-FRONT-ARCHITECTURE-001
- Objectif : concevoir l'architecture produit et données du nouveau front global sur le registre canonique global V2.1.
- Statut : DONE.
- Livrables : `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`, `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`, `docs/project/GLOBAL_FRONT_RULES_V1.md`, `docs/project/GLOBAL_FRONT_SCREEN_STRATEGY_V1.md`, `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md` et `docs/review/global_front_architecture_001_report_v1.md`.
- Décisions : modèle front par objets métier role-based, adresses typées par usage, reutilisation uniquement via règles explicites, distinction dossier / document / lot, mode document unitaire séparé du parcours dossier complet.
- Prototype : conserver les concepts utiles et le diagnostic technique ; ne pas généraliser les écrans, le `session_state` ou les listes de champs du prototype actuel.
- Garde-fous : aucun générateur, moteur DOCX/PDF/ZIP, Streamlit ou wording juridique modifié ; `docs/docssource_truth/` non suivi laissé hors périmètre.
- Validation : relecture documentaire et contrôle du diff ; aucun test Python requis car aucun fichier Python modifié.
- Prochaine étape recommandée : `FRONT-DATA-LAYER-001`, créer la couche de données front globale sans toucher au moteur ni au prototype.

### GLOBAL-FRONT-ARCHITECTURE-QA-001
- Objectif : vérifier l'architecture front globale V1 sur des documents sentinelles représentatifs du moteur.
- Statut : DONE.
- Sentinelles contrôlées : `DOC-002`, `DOC-034`, `DOC-017`, `DOC-033`, `DOC-009`, `DOC-041` et `DOC-025`.
- Livrables : `docs/review/global_front_architecture_qa_001_report_v1.md` et `docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv`.
- Verdict : architecture globalement ORANGE maîtrisable ; `DOC-002` et `DOC-033` verts, cinq sentinelles orange, aucun rouge.
- Garde-fous : aucun générateur, moteur DOCX/PDF/ZIP, Streamlit, UI ou wording juridique modifié ; `docs/docssource_truth/` non suivi laissé hors périmètre.
- Validation : relecture documentaire et contrôle du diff ; aucun test Python requis car aucun fichier Python modifié.
- Prochaine étape recommandée : `FRONT-DATA-LAYER-001`, en intégrant les sentinelles orange comme critères de couverture data.

### FRONT-STATE-AUDIT-001
- Objectif : auditer l'etat reel du projet et du nouveau front apres retour utilisateur sur la limitation a quatre documents et le blocage de generation.
- Statut : DONE.
- Livrable : `docs/review/front_state_audit_001_report_v1.md`.
- Constat : le moteur reste disponible sur 43 documents moteurs, mais la surface normale du nouveau front est volontairement limitee au pilote `SELARL creation simple` et a `DOC-001` a `DOC-004`.
- Cause UX identifiee : la readiness data-layer peut annoncer quatre documents generables tandis que l'adaptateur moteur bloque ensuite sur un format de date, une adresse ou une ville RCS, sans exposer le detail dans la vue normale.
- Validation : tests cibles `test_front_generation_actions.py` et `test_front_dossier_data_entry.py` OK ; diagnostic lecture seule des blocages runtime OK.
- Prochaine étape recommandee : `FRONT-GENERATION-READINESS-UX-001`, avant toute extension du perimetre SELARL.

### FRONT-REALITY-CHECK-001
- Objectif : auditer l'ecart entre les debriefs recents du nouveau front et le code reel visible / branche.
- Statut : DONE.
- Livrables : `docs/review/front_reality_check_001_report_v1.md` et `docs/project/FRONT_MINIMAL_USER_SURFACE_V1.md`.
- Constat : le hard cut est reel sur la vue normale (3 titres, 0 table, 0 radio), mais la surface reste chargee par les expanders ouverts, 22 champs, la sidebar `Outils internes`, le bouton PDF visible quand le backend est indisponible et les blocages runtime non expliques.
- Generation reelle : DOCX et ZIP branches pour `DOC-001` a `DOC-004`; PDF branche en code mais indisponible localement (`is_pdf_export_available() == False`).
- Decision de pilotage : ne pas ajouter de panneau documents visible avant une coupe UX minimale ; absorber les explications de readiness dans un ticket unique de surface minimale.
- Validation : audit code + inventaire AppTest de la vue normale + controle PDF local ; aucun fichier Python modifie, donc pas de ruff/pytest requis.
- Prochaine étape recommandee : `FRONT-MINIMAL-SURFACE-CLEANUP-001`.

### FRONT-MINIMAL-SURFACE-CLEANUP-001
- Objectif : appliquer la surface utilisateur minimale avant tout push, redeploiement ou test utilisateur.
- Statut : DONE.
- Contraintes : ne pas modifier les generateurs, le moteur DOCX/PDF/ZIP, la source de verite ou le wording juridique ; ne pas etendre le perimetre documentaire.
- Livrables : coupe UI dans `src/sydel_doc_engine/app/streamlit_app.py`, tests AppTest adaptes, rapport `docs/review/front_minimal_surface_cleanup_001_report_v1.md`.
- Sortie realisee : page normale limitee a `Type de dossier`, `Donnees a saisir`, `Generation`; 0 radio, 0 table, 0 expander ; debug interne cache hors session utilisateur ; PDF cache si backend indisponible ; blocages data-layer/runtime visibles dans `Generation`.
- Validation : tests cibles front OK, 79 tests passes ; `ruff check .` OK ; `pytest` OK, 382 tests passes.
- Prochaine étape ensuite : test utilisateur local du pilote `SELARL creation simple`.

### SELARL-COMPLETE-CASE-PLAYBOOK-001
- Objectif : transformer le retour utilisateur "SELARL seulement quatre documents / encore test" en cadrage executable pour une SELARL complete.
- Statut : DONE.
- Contraintes : aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique modifie ; pas de push ni redeploiement.
- Livrables : `docs/project/SELARL_COMPLETE_CASE_PLAYBOOK_V1.md` et `docs/review/selarl_complete_case_playbook_001_report_v1.md`.
- Constat : le moteur sait deja generer les familles SELARL principales, mais le nouveau front global reste explicitement limite a `DOC-001` a `DOC-004` via `FRONT_GENERATION_SUPPORTED_DOC_CODES`, `UNIT_DOCUMENT_V1_SUPPORTED_CODES` et `BUSINESS_WIZARD_CONTEXT_READY_DOCUMENT_IDS`.
- Decision : la cible SELARL complete passe par un adaptateur contexte/readiness front, pas par une modification immediate des generateurs.
- Validation : documentation et pilotage uniquement ; aucun test Python requis.
- Prochaine étape recommandee : `SELARL-COMPLETE-CONTEXT-ADAPTER-001`.

### SELARL-COMPLETE-CONTEXT-ADAPTER-001
- Objectif : brancher cote nouveau front une selection documentaire SELARL conditionnelle et un `DocumentGenerationContext` complet pour les documents deja autorises par la source et disponibles cote moteur.
- Statut : DONE.
- Contraintes : ne pas modifier les generateurs, le moteur DOCX/PDF/ZIP ou le wording juridique ; conserver `DOC-013`, `DOC-014` et les documents sans code en manuel ; generer `DOC-006` uniquement si le regime communautaire est actif.
- Livrables : `src/sydel_doc_engine/app/front_selarl_complete.py`, extension de `front_dossier_entry.py`, `front_generation_actions.py`, `streamlit_app.py`, tests unitaires front et rapport `docs/review/selarl_complete_context_adapter_001_report_v1.md`.
- Sortie realisee : la SELARL medecin simple genere maintenant `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034` et `DOC-017` depuis le nouveau front ; la profession chirurgien-dentiste bascule vers `DOC-016` ; le regime communautaire ajoute `DOC-005` et `DOC-006`.
- Limite volontaire : cession medicale/dentaire et cession SCM sont selectionnees depuis le catalogue, mais restent `context_incomplete` tant que les sous-formulaires metier detailles ne sont pas branches.
- Validation : `ruff check .` OK ; tests cibles `test_front_generation_actions.py` + `test_front_dossier_data_entry.py` OK, 23 tests passes ; smoke DOCX dentiste et regime communautaire OK ; `pytest` complet tente mais non conclusif a cause de `PermissionError` Windows sur les dossiers temporaires `tmp_path`/`basetemp`.
- Prochaine etape recommandee : utiliser `docs/project/SELARL_CANONICAL_STATUS_V1.md`, puis faire valider le pack 005 avant de rouvrir `SELARL-COMPLETE-COMPLEX-SUBFORMS-001`.

### SELARL-COMPLETE-COMPLEX-SUBFORMS-001
- Objectif : brancher les sous-formulaires et l'adaptateur contexte pour les scenarios cession medicale/dentaire, bail/appel de fonds et cession SCM.
- Statut : BLOCKED tant que le prochain sous-cas n'est pas choisi dans `docs/project/SELARL_CANONICAL_STATUS_V1.md` ou dans un ticket dedie, avec decision explicite `GO dev`.
- Contraintes : ne pas modifier les generateurs, le moteur DOCX/PDF/ZIP, la source de verite ou le wording juridique ; ne pas exposer de nouveau panneau de diagnostic en surface principale.
- Sorties attendues : champs metier detailles, contexte moteur complet pour `DOC-007` a `DOC-012` et `DOC-031` a `DOC-033`, readiness actionnable, tests par scenario et smoke DOCX/ZIP.
- Prochaine etape ensuite : à définir après gate produit.

### FRONT-GENERATION-READINESS-UX-001
- Objectif : rendre les blocages de generation visibles et actionnables dans la vue normale du nouveau front.
- Statut : BLOCKED.
- Contraintes : ne pas modifier les generateurs, le moteur DOCX/PDF/ZIP, la source de verite ou le wording juridique.
- Sortie attendue : a absorber dans `FRONT-MINIMAL-SURFACE-CLEANUP-001` pour eviter un ticket qui ajoute de la surface avant la coupe UX.
- Prochaine étape ensuite : reassessment apres le test utilisateur local minimal.

### UI-001
- Objectif : exposer une Streamlit simple pour générer le Lot 1.
- Statut : en attente explicite ; ne pas lancer sans ticket explicite dédié.
- Prérequis : orchestrateur Lot 1 fonctionnel et spec canonique `PV nomination gérant` validée.
- Sortie attendue : écran simple, génération testable manuellement, aucun métier caché dans l'UI.

## Règle de mise à jour
Chaque ticket terminé doit mettre à jour ce fichier :
- passer son statut à DONE
- déplacer le ticket actif en IN_PROGRESS pendant l'exécution si la tâche dure plus qu'une modification courte
- indiquer le prochain ticket à lancer
- indiquer les éventuels points ouverts
- mettre à jour `docs/project/04_LAST_STATE.md`

## Prochaine étape prévue
- Reprise officielle sprint : lire `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`, puis le fichier actif `docs/sprints/SPRINT_[TYPE]_V1.md`, puis `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`, puis `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`, puis appliquer `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`.
- Nouveau chat sans identite : demander d'abord `Bonjour, tu es Gad ou Naomi ?`, puis router. Ne pas declencher NotebookLM sur un simple bonjour anonyme.
- Statut Naomi demande par Gad : appliquer `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, lire tour de controle, dernier etat, sprint, worklog, journal et branche accessible avant de repondre.
- Rapport Naomi demande par Gad : produire le delta depuis le dernier rapport inscrit dans le worklog, puis noter le nouveau curseur. Message Gad pour Naomi : inscrire en `a transmettre`, citer au prochain echange, marquer `transmis`.
- Lecture branche Naomi : si `git fetch` local echoue (`FETCH_HEAD Permission denied` ou credentials), utiliser le connecteur GitHub avant de conclure que la branche est inaccessible.
- Sprint Naomi actif : SELAS, `docs/sprints/SPRINT_SELAS_V1.md`, phase 0 `ACCUEIL / INITIALISATION`, statut `NO-GO dev`.
- Branche Naomi cible : `codex/naomie-selas-sprint`, creee/poussee par Codex depuis le checkpoint documentaire ; Naomi ne gere pas Git.
- Pour l'accueil de Naomi apres identification : repondre avec `Statut sprint`, `Action maintenant`, `Point pedagogie`, `Prochaine etape`; aucun dev avant NotebookLM, audit reutilisation, matrice documentaire, tickets et `GO dev` explicite de Gad.
- Pour tout nouveau type d'entreprise : produire la matrice de reutilisation selon `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md` avant le premier `GO dev`.
- Pour la SELARL : lire `docs/project/SELARL_CANONICAL_STATUS_V1.md`, puis poursuivre `SELARL-FINAL-ASSOCIE-VALIDATION-001` sur le pack 005 ou choisir un seul sous-cas avec `GO dev` explicite apres validation/report. Aucun ticket de dev SELARL complexe ne doit demarrer sans ce choix.
- `SELARL-COMPLETE-CONTEXT-ADAPTER-001` est DONE ; le nouveau front n'est plus limite a quatre documents : medecin simple cible et genere `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-017`, dentiste bascule vers `DOC-016`, regime communautaire ajoute `DOC-005` et `DOC-006`.
- `SELARL-COMPLETE-COMPLEX-SUBFORMS-001` est bloqué tant que le prochain sous-cas n'est pas cadré sous gate produit.
- `SELARL-COMPLETE-CASE-PLAYBOOK-001` est DONE ; la SELARL complete est cadree comme une extension front/adaptateur/readiness, avec matrice documentaire et mode d'emploi reproductible pour les autres cas.
- `FRONT-MINIMAL-SURFACE-CLEANUP-001` est DONE ; la surface normale est maintenant limitee a `Type de dossier`, `Donnees a saisir`, `Generation`, sans outil interne visible, sans radio, sans table et sans expander.
- Le test utilisateur local du pilote `SELARL creation simple` reste utile, mais ne remplace pas le gate produit avant extension documentaire.
- `FRONT-REALITY-CHECK-001` est DONE ; l'audit confirme que la vue normale etait reduite techniquement a trois zones, mais encore trop chargee dans la saisie et trop muette sur les blocages runtime.
- `FRONT-STATE-AUDIT-001` est DONE ; constat historique sur l'ancien etat du front, remplace pour la reprise SELARL par `docs/project/SELARL_CANONICAL_STATUS_V1.md`.
- `FRONT-GENERATION-READINESS-UX-001` reste a reassesser apres test utilisateur ; `FRONT-DOCUMENTS-PANEL-001` reste suspendu comme panneau visible tant que le besoin n'est pas confirme.
- `FRONT-REVIEW-001` est DONE ; le prototype actuel est confirme comme bac a sable / outil de diagnostic, la carte de migration V1 est creee et le backlog pointe maintenant vers les tickets UI visibles.
- Jalon front revise apres `FRONT-MINIMAL-SURFACE-CLEANUP-001` : ne pas ajouter `FRONT-DOCUMENTS-PANEL-001` en surface visible avant test utilisateur local.
- `GLOBAL-FRONT-ARCHITECTURE-QA-001` est DONE ; l'architecture front globale a ete controlee sur 7 documents sentinelles, avec 2 verts, 5 oranges et aucun rouge.
- `GLOBAL-FRONT-ARCHITECTURE-001` est DONE ; l'architecture produit et données du nouveau front global est cadrée sans toucher au moteur, aux générateurs, à Streamlit ni au wording juridique.
- `GLOBAL-HUMAN-ANSWERS-INTEGRATION-001` est DONE ; les réponses humaines disponibles sont intégrées dans les questions V2, le registre canonique global V2.1 et le rapport exécutif, sans toucher au moteur ni à l'UI.
- `WORKTREE-CLEANUP-AND-UI-STATUS-001` est DONE ; le pack `REVIEW-FINAL-001` est consolide dans `main`, le rapport 23 clarifie le dossier canonique et le statut UI, et les anciens worktrees locaux sont a considerer comme archives.
- `SYNC-FINAL-FOUNDATIONS-001` est DONE ; `main` contient les audits 16/17/18, les cadrages UI 19/20/21, le framework de recette finale, l'UI intégrée, le backend PDF et le backend ZIP déterministe.
- `UI-PDF-ZIP-INTEGRATION-001` est DONE ; l'UI sait produire et telecharger DOCX, PDF local optionnel et ZIP dossier.
- `UI-CORE-001` est superseded / remplacé par `UI-PDF-ZIP-INTEGRATION-001`.
- `RESUME-ZIP-BACKEND-001` est DONE ; `rendering/zip_bundle.py` est intégré et testé.
- `SYNC-POST-MOTOR-UI-001` est DONE ; les fondations UI/PDF/recette sont absorbées dans `main`.
- `REVIEW-FINAL-001` est DONE ; rapport d'execution disponible dans `docs/review/review_final_001_execution_report_v1.md`.
- `UI-BUSINESS-WIZARD-001` est DONE ; l'UI Streamlit dispose maintenant d'un mode assistant metier SCI V1 et conserve le mode technique YAML/JSON.
- `CASE-CATALOG-001` est DONE ; le catalogue metier par cas couvre 46 documents attendus, dont 43 mappes au registre moteur et 3 non generables.
- `UI-CASE-WIZARD-002` est DONE ; l'assistant metier utilise maintenant `get_expected_documents(...)` pour afficher les documents attendus et exclut les documents manuels/non implementes de la generation.
- `SELARL-PILOT-PROTOCOL-001` est DONE ; le pilote SELARL dispose d'un protocole réplicable, d'une spec processus, d'une spec formulaire, d'une spec wizard et d'un plan d'implémentation.
- `SELARL-PILOT-SOURCE-VERIFY-001` est DONE ; la vraie V2 est au chemin canonique, les dérogations SELARL sont réconciliées en manuel et les variables V2 brutes sont reprises dans les specs.
- `SELARL-FORM-SCHEMA-IMPL-001` est DONE ; le schéma machine-readable SELARL existe, `DOC-006` porte une réserve V2 exploitable, `DOC-013` / `DOC-014` restent manuels et la couverture des variables V2 est testée.
- `SELARL-UI-WIZARD-IMPL-001` est DONE techniquement ; l'Assistant métier expose le parcours SELARL pilote depuis le schéma, conserve SCI et Technique / diagnostic, et garde `DOC-013` / `DOC-014` hors génération, mais il n'est pas encore validé produit.
- `SELARL-PLAN-CORRECTION-001` est DONE ; les arbitrages associé priment désormais sur NotebookLM pour `Fiche Client`, `Praticien`, `Dossier unipersonnel`, l'absence de mode Projet / filigrane V1 et l'absence de couche statut produit lourde.
- `SELARL-FLOW-REALIGN-001` est DONE ; le schéma et les projections métier expriment Qualification, Fiche Client / Praticien, Fiche Société, Capital & Associés, Contexte & scénarios métier, Documents & génération.
- `SELARL-REUSE-RULES-REALIGN-001` est DONE ; `Dossier unipersonnel` pilote les liens Praticien / associé unique / gérant / signataire, les autres réutilisations restent opt-in et les relations sensibles sont non automatiques.
- `SELARL-UI-REALIGN-001` est DONE ; le parcours Streamlit visible SELARL suit les six écrans métier et consomme le schéma/projections corrigés.
- ticket SELARL en cours : `SELARL-FINAL-ASSOCIE-VALIDATION-001`; autre ticket pret hors SELARL : `CLOSE-PROJECT-V1-001`.
- ticket SELARL smoke précédent bloqué : `SELARL-DOCS-GENERATION-SMOKE-001`, remplacé par la séquence `WORDING -> FLOW -> REUSE -> UI -> SMOKE -> JURIST`.
- prochain ticket recommandé : `SELARL-FINAL-ASSOCIE-VALIDATION-001`, puis `SELARL-CANONICAL-CLOSE-001` si l'associe valide.
- ne pas pousser ni redéployer l'UI SELARL actuelle sans décision explicite après smoke et revue.
- moteur documentaire DOCX V1 feature complete et clos après `RECONCILE-MOTOR-CLOSE-001`.
- tickets absorbés par `SYNC-POST-MOTOR-UI-001` : `UI-FLOW-001`, `UI-OCCURRENCES-001`, `UI-FORM-SCHEMA-001`, `PDF-BACKEND-001` et `RECIPE-FRAME-001`.
- `RECONCILE-MOTOR-CLOSE-001` est DONE ; les générateurs ordre/SPFPL orphelins sont exposés sous `DOC-034` à `DOC-043`, `08/09/16/17/18` sont alignés et les références delivery Lot 2 manquantes sont présentes sur `main`.
- `PDF-BACKEND-001` est DONE ; le backend PDF est intégré à la fondation absorbée, sans ticket PDF supplémentaire confirmé dans cette synchronisation.
- `FINAL-SCM-CESSION-WAVE-001` est DONE ; `DOC-031`, `DOC-032` et `DOC-033` cession SCM sont branchés au catalogue/orchestrateur et couverts par tests/smoke.
- `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` conclut la clôture moteur V1 et liste les exclusions restantes.
- `SYNC-CLOSE-AUDIT-001` est DONE ; le commit source `0139202b170531fd628f25811c55855a2512acc0` a été absorbé via merge de synchronisation en conservant la version finale plus récente de l'audit.
- tickets absorbés par SYNC-WAVE-010 : `ARBITRAGE-SCM-CESSION-RESOLVE-001` et `CODE-SCM-CESSION-BLOCK-001`.
- `ARBITRAGE-SCM-CESSION-RESOLVE-001` est DONE.
- `CODE-SCM-CESSION-BLOCK-001` est DONE.
- tickets absorbés par SYNC-WAVE-009 : `CODE-SCM-LISTE-DEPENSES-001`, `SPEC-DEROG-SALARIEE-MANUAL-001`, `REVIEW-BATCH-LOT05-001`, `FIX-STYLE-STATUTS-BATCH-001` et `FIX-STYLE-LOT03-BATCH-001`.
- tickets absorbés par SYNC-WAVE-008 : `CODE-ACTE-ACTIONS-001`, `PREP-SCM-CESSION-SOURCES-001`, `REVIEW-BATCH-LOT03-001`, `REVIEW-BATCH-LOT04-001`, `AUDIT-REMAINING-SCOPE-001`, `STYLE-ANALYSE-LOT03-BATCH-001`, `STYLE-ANALYSE-STATUTS-BATCH-001` et `SPEC-SCM-CESSION-BLOCK-001`.
- tickets absorbés par SYNC-WAVE-007 : `CODE-STATUTS-SCM-001`, `PREP-SCM-LISTE-DEPENSES-CONVERT-001`, `CODE-SCM-SAT-DOCX-001` et `SPEC-ACTE-ACTIONS-001`.
- tickets absorbés par SYNC-WAVE-006 : `RESUME-FIX-STYLE-LETTERS-001`, `CODE-STATUTS-CIVILS-CORE-001`, `CODE-SAS-SATELLITES-001`, `CONVERT-DEROG-SALARIEE-001`, `CONVERT-ACTE-ACTIONS-001` et `SPEC-SCM-SATELLITES-001`.
- `CODE-SCM-LISTE-DEPENSES-001` est DONE ; `DOC-030` liste des dépenses communes SCM est branché au catalogue/orchestrateur.
- `SPEC-DEROG-SALARIEE-MANUAL-001` est DONE ; la stratégie V1 reste manuelle/faute de source DOCX exploitable.
- `REVIEW-BATCH-LOT05-001` est DONE ; la revue Lot 05 est documentée.
- `FIX-STYLE-STATUTS-BATCH-001` et `FIX-STYLE-LOT03-BATCH-001` sont DONE ; les corrections portent sur le rendu DOCX sans dérive volontaire de wording juridique.
- `CODE-ACTE-ACTIONS-001` est DONE ; l'acte de cession d'actions SPFPL est intégré au catalogue/orchestrateur.
- `PREP-SCM-CESSION-SOURCES-001` est DONE ; les sources cession SCM exploitables sont placées dans `project/source_documents/lot_05/`.
- `SPEC-SCM-CESSION-BLOCK-001` est DONE ; les specs de blocage cession SCM V1 sont disponibles dans `docs/delivery/`.
- `ARBITRAGE-SCM-CESSION-RESOLVE-001` est DONE ; la résolution V1 cession SCM est disponible dans `docs/delivery/`.
- `STYLE-ANALYSE-LOT03-BATCH-001` et `STYLE-ANALYSE-STATUTS-BATCH-001` sont DONE ; les blueprints style dédiés sont disponibles dans `docs/delivery/`.
- `REVIEW-BATCH-LOT03-001`, `REVIEW-BATCH-LOT04-001` et `AUDIT-REMAINING-SCOPE-001` sont DONE.
- `CODE-STATUTS-SCM-001` est DONE ; les statuts SCM sont branchés sous `DOC-025`.
- `CODE-SCM-SAT-DOCX-001` est DONE ; les satellites SCM DOCX sont branchés sous `DOC-026`, `DOC-027` et `DOC-028`.
- `PREP-SCM-LISTE-DEPENSES-CONVERT-001` est DONE ; le DOCX exploitable est placé dans `project/source_documents/lot_05/`.
- `SPEC-ACTE-ACTIONS-001` est DONE ; les specs acte actions V1 sont disponibles dans `docs/delivery/`.
- `CONVERT-ACTE-ACTIONS-001` est DONE ; le DOCX exploitable est placé dans `project/source_documents/lot_05/`.
- `CONVERT-DEROG-SALARIEE-001` est DONE ; la source salariee reste non convertie et `cumul_salariee` demeure bloque faute de DOCX propre.
- `CODE-OPTION-IS-001`, `PREP-SCM-SAT-001`, `ARBITRAGE-STATUTS-SCM-001`, `SPEC-SAS-SATELLITES-001` et `PREP-ACTE-ACTIONS-001` sont DONE et absorbés dans `main`.
- `RESUME-FIX-STYLE-LETTERS-001` est DONE et absorbé dans `main`.
- `FIX-STYLE-LETTERS-001` est DONE et absorbé dans `main`.
- `CODE-STATUTS-SEL-001` est DONE et absorbé dans `main`.
- `CODE-STATUTS-CIVILS-CORE-001` est DONE pour SCS, SCI et SCI IRIS.
- `STYLE-ANALYSE-BATCH-001` et `ARBITRAGE-STATUTS-CIVILS-001` sont DONE et absorbés dans `main`.
- `CODE-STATUTS-SAS-001`, `CODE-STATUTS-SPFPL-001` et `ARBITRAGE-STATUTS-SEL-001` sont DONE et absorbés dans `main`.
- `CODE-BAIL-APP-001` est DONE et absorbé dans `main`.
- `PREP-DEROG-001` est DONE et absorbé dans `main`.
- `CODE-SPFPL-AGR-INFO-001` est DONE et absorbé dans `main`.
- `CODE-CESSION-CAB-001` est DONE et absorbé dans `main`.
- `CODE-DEROG-CORE-001` est DONE et absorbé dans `main`.
- `PREP-STATUTS-001` est DONE et absorbé dans `main`.
- `CODE-SPFPL-CORE-001` est DONE et absorbé dans `main`.
- `SPEC-STATUTS-SAS-001`, `SPEC-STATUTS-SPFPL-001`, `SPEC-STATUTS-SEL-001` et `SPEC-STATUTS-CIVILS-001` sont DONE et absorbés dans `main`.
- revue humaine toujours recommandée : smoke DOCX `régime communautaire`, notamment le rendu SELARL de la renonciation canonique.
- les autres cas MEDIUM/LOW restent bloqués tant que leurs variantes sources n'ont pas été comparées.
- UI-001 reste explicitement en attente.

## Points ouverts
- Aucun point bloquant moteur DOCX identifié après `RECONCILE-MOTOR-CLOSE-001`.
- Restent hors périmètre moteur : UI, ZIP, recette finale, revue humaine juridique/visuelle, documents explicitement manuels et sources legacy non converties.
- PDF-BACKEND-001 est terminé : le backend local `rendering/pdf_export.py` produit un PDF depuis un DOCX généré via Word COM, avec LibreOffice headless prioritaire si disponible.
- Points ouverts PDF après PDF-BACKEND-001 : LibreOffice n'est pas installé localement, l'intégration batch/orchestrateur reste hors ticket, et le succès technique PDF ne vaut pas validation visuelle ou juridique.
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Les trois DOCX sont bien produits par l'orchestrateur dans `artifacts/lot_01_smoke_test/`, mais le rendu visuel et le wording juridique restent à relire humainement dans les fichiers générés.
- PDF et ZIP restent hors ORCH-001 et devront être traités dans un ticket dédié.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'à refactor dédié.
- ORCH-L2-PV-001 est terminé ; le PV nomination gérant est branché dans l'orchestrateur pour les structures concernées et exclu pour SAS.
- SMOKE-ORCH-L2-001 est terminé ; le smoke réel confirme la génération du PV pour SCI et son absence pour SAS.
- FIX-PV-RENDER-001 est terminé ; le PV from-scratch restaure les structures visuelles essentielles du document source sans UI, PDF ni ZIP.
- ANALYSE-ORDRE-001 est terminé ; les cadrages V1 ordre et régime communautaire sont disponibles dans `docs/delivery/`.
- ARBITRAGE-SOURCES-001 est terminé ; le scan a identifié 147 fichiers dans `raw_drive_dump`, 11 fichiers dans `source_documents`, 18 groupes de doublons probables, 6 documents sans source claire et 16 documents hors périmètre.
- PLACEMENT-HIGH-001 est terminé ; les 4 cas HIGH documentés dans le plan de placement V1 ont été confirmés comme déjà présents, sans nouvelle copie.
- SPEC-ORDRE-001, SPEC-TEXTE-ORDRE-001, CODE-ORDRE-001, SPEC-RC-001, CODE-RC-001, SPEC-SPFPL-001, SPEC-DEROG-001, SPEC-CESSION-BAIL-001, SPEC-TEXTE-BAIL-APP-001, SPEC-TEXTE-CESSION-CAB-001, SPEC-TEXTE-DEROG-001, SPEC-TEXTE-SPFPL-001, ARBITRAGE-CESSION-001, ARBITRAGE-DEROG-001, ARBITRAGE-SPFPL-001 et CODE-BAIL-APP-001 sont DONE.
- REVIEW-PV-001 est terminé, mais la validation humaine du rendu DOCX et du wording reste à obtenir pour la revue juridique fine.
- RENDER-STYLE-001 est terminé ; les signatures encadrées sont disponibles dans la couche commune et appliquées aux signatures Lot 1.
- Le PV nomination gérant conserve des signatures répétables simples ; toute signature encadrée dirigeant/associés séparée reste soumise à validation métier.
- UI-001 reste en attente explicite : ne pas lancer le branchement Streamlit sans nouveau ticket.
- Points ouverts PV documentés dans la spec texte : périmètre SELAS, capital non variable, société déjà immatriculée, dirigeant non associé, ponctuation finale des associés, féminisation éventuelle de la fonction, règle `euro/euros`.
- Points ouverts ordre post-CODE-ORDRE-001 : revue humaine du premier rendu SCM, mention de dérogation limitée au bloc manuel fourni, valeurs ordinales et mandataire toujours fournis par contexte/référentiel.
- Points ouverts régime communautaire après SPEC-RC-001 : revue humaine SELARL de la renonciation canonique, féminisation éventuelle de `futur`, absence de variante `ma conjointe`, apport limité à une somme en numéraire, valeurs par défaut de régime matrimonial / qualité renoncée / formes sociales à fournir par contexte ou référentiel.
- CODE-RC-001 est terminé ; le smoke DOCX réel confirme la production des deux lettres, mais ne vaut pas validation juridique fine.
- Points ouverts SPFPL après ARBITRAGE-SPFPL-001 : acte de cession d'actions hors automatisation faute de source DOCX confirmée, multi-souscripteurs hors V1, commissaire et évaluateur fournis par contexte ou référentiel validé.
- Points ouverts dérogations après PREP-DEROG-001 : les deux sources Lot 03 préparées sont placées, le `.doc` legacy reste à convertir ou remplacer si `cumul_salariee` entre dans le périmètre, et le mode de rendu `document finalisé` ou `formulaire à compléter` doit être porté explicitement dans le registre ou le nom de sortie.
- CODE-DEROG-CORE-001 est terminé ; `DOC-013` formulaire multi-sites SEL et `DOC-014` demande cumul SELARL/BNC sont branchés dans le catalogue/orchestrateur comme formulaires à compléter.
- Points ouverts dérogations après CONVERT-DEROG-SALARIEE-001 : revue humaine juridique/visuelle du premier rendu `DOC-013` et `DOC-014`, `cumul_salariee` toujours bloqué faute de DOCX propre apres erreur Word COM `0x800706BE`, zones narratives sensibles laissées à compléter.
- CODE-BAIL-APP-001 est terminé ; `DOC-007` avenant au contrat de bail et `DOC-008` appel de fonds SEL sont branchés dans le catalogue/orchestrateur.
- Points ouverts bail/appel après CODE-BAIL-APP-001 : appel de fonds limité à SELARL dentaire, avenant limité SELARL/SELAS avec `dossier_options.cession=true`, revue humaine juridique/visuelle du premier rendu toujours nécessaire.
- Points ouverts cession après CODE-CESSION-CAB-001 : revue humaine juridique/visuelle du premier rendu DOCX, sources SELAS non stabilisées au-delà du paramétrage V1, PDF/ZIP hors ticket.
- Points ouverts statuts après SYNC-WAVE-007 : SAS limité au modèle SAS/SPFPL médecins source ; SPFPL doit conserver cession/apport sans harmonisation ; SCM est codé en V1 mais reste soumis à revue humaine juridique/visuelle du premier rendu.

## Journal court
- 2026-06-02 : PROJECT-COMPANY-TYPE-UI-STATUS-001 durcit l'affichage Assistant metier : `business_dossier_types()` ne marque plus tous les `CaseType` comme generables produit V1. `SELARL` reste sprint produit actif/PARTIAL et seul type `generable_in_v1=True`; `SELAS` est sprint actif mais `NO-GO dev`; `SCI`, `SCM`, `SPFPL`, `SCS` et `SAS` deviennent `INVENTAIRE_TECHNIQUE` avec warning de diagnostic. Agent Git Curie consulte avant edition ; generateurs SELARL evites ; validations ciblees OK.
- 2026-06-01 : SPRINT-ORCHESTRATOR-PROTOCOL-001 / SPRINT-SELAS-V1-001 cree `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` et `docs/sprints/SPRINT_SELAS_V1.md`, ouvre le sprint SELAS pour Naomi en phase 0 `NO-GO dev`, impose le format de reponse avec point pedagogie et bloque tout dev avant NotebookLM, audit reutilisation, matrice, tickets et `GO dev` explicite de Gad.
- 2026-06-01 : NAOMIE-HELLO-TRIGGER-001 corrige l'incident d'accueil ou un nouveau chat a repondu genericement a `Bonjour Naomi`; le trigger est remonte dans `AGENTS.md`, `SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`, `SPRINT_SELAS_V1.md` et `02_CODEX_WORKFLOW.md` : un simple bonjour apres identification de Naomi impose verification branche `codex/naomie-selas-sprint`, phase 0 `NO-GO dev`, point pedagogie et prochaine etape NotebookLM.
- 2026-06-01 : SELAS-NOTEBOOKLM-PROMPT-LOOP-001 ajoute une boucle NotebookLM operationnelle pour Naomi : prompts courts dans `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md`, journal structure dans `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, et regle que Codex doit donner le prompt exact, structurer chaque reponse, puis iterer jusqu'a couverture suffisante avant reuse audit/matrice/dev.
- 2026-06-01 : SELAS-NOTEBOOKLM-START-TRIGGER-001 corrige l'ambiguite `je veux lancer le sprint SELAS/CELAS` : pour Naomi, `lancer` signifie lancer uniquement le sous-sprint NotebookLM. Codex doit donner le prompt courant a copier-coller, attendre la reponse brute, la structurer dans le journal, puis iterer ; il ne doit pas passer en production, generation, audit, matrice ou code avant couverture suffisante.
- 2026-06-01 : PROJECT-CONTROL-TOWER-001 cree `docs/project/PROJECT_CONTROL_TOWER_V1.md`, la tour de controle chef de projet globale. Elle force Codex a identifier acteur, type d'entreprise, sprint actif, branche, phase, action autorisee et interdits avant d'agir ; elle inscrit SELARL en production partielle/revue humaine et SELAS en sprint actif Naomi/sous-sprint NotebookLM.
- 2026-06-01 : MAIN-NAOMIE-TRIGGER-001 corrige le cas observe en capture ou un nouveau chat sur `main` repond genericement a `bonjour` / `je suis naomi`. La regle devient : si Naomi/SELAS arrive sur `main`, Codex doit basculer vers `codex/naomie-selas-sprint` ou bloquer en `NO-GO dev`, jamais demander une tache ou un ticket.
- 2026-06-02 : GLOBAL-CHAT-IDENTITY-ROUTING-001 corrige le routage Gad / Naomi : un `bonjour` anonyme demande d'abord `Gad ou Naomi ?`; `Gad` active le rail superviseur produit ; `Naomi` active le runtime SELAS ; parler de Naomi avec Gad ne declenche pas NotebookLM par reflexe.
- 2026-06-02 : NAOMIE-SUPERVISION-ORCHESTRATOR-001 cree l'agent/protocole generique `Orchestrateur Naomi` : quand Gad demande ou en est Naomi, Codex lit les traces (tour de controle, dernier etat, sprint, worklog, journal, branche) et repond sans solliciter Naomi. Premier worklog cree : `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`.
- 2026-06-02 : NAOMIE-REPORT-CURSOR-AND-MESSAGE-QUEUE-001 ajoute deux fonctions au suivi Naomi : rapports differentiels depuis le dernier rapport Gad et messages Gad a transmettre a Naomi au prochain echange, suivis dans le worklog avec statuts `a transmettre/transmis`.
- 2026-06-02 : NAOMIE-BRANCH-READ-FALLBACK-001 corrige le probleme observe en capture : la branche `codex/naomie-selas-sprint` existe cote GitHub et le connecteur la voit ; le `fetch` local est bloque par permission/identifiants. Codex doit donc utiliser le connecteur GitHub avant tout diagnostic `branche inaccessible`.
- 2026-06-01 : NAOMIE-LEARNING-MENTOR-001 cree `docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md`, formalise le sous-agent `Professeur Naomi`, fixe la decision `GO pedagogie` / `NO-GO dev`, et precise que Naomi apprend le projet, Git et la methode sans gerer les commandes ni prendre de decisions de scope.
- 2026-06-01 : REUSE-AUDIT-AGENT-PROTOCOL-001 cree `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`, lance un sous-agent Reuse Auditor en lecture seule, integre sa synthese sur les artefacts SELARL/globaux reutilisables, et impose une matrice `identique / reuse-check / adapter / no-go` avant tout `GO dev` d'un nouveau type d'entreprise.
- 2026-06-01 : NAOMIE-GITHUB-ONBOARDING-001 cree `docs/project/NAOMIE_GITHUB_ONBOARDING_V1.md`, formalise l'installation GitHub, la venv Python, les validations locales, le lancement Streamlit et la regle `1 sprint = 1 branche = 1 type d'entreprise`; correction produit : Naomi ne gere pas Git ni les commandes, Codex execute les operations techniques pour elle ; la creation de branche reste bloquee tant que le type d'entreprise et le checkpoint pousse ne sont pas confirmes.
- 2026-06-01 : COMPANY-TYPE-SPRINT-PLAYBOOK-001 cree `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`, formalise `1 sprint = 1 type d'entreprise`, impose le demarrage en `NO-GO dev`, l'interrogation NotebookLM large, l'identification de Naomi, le guidage etape par etape, et la boucle retour de l'associe avant validation 100 %.
- 2026-06-01 : COMPANY-TYPE-SPRINT-PLAYBOOK-002 capitalise les apprentissages de la cloture SELARL dans la methode reusable : triangulation document de reference / NotebookLM-modele / retours humains, interdiction des questions humaines deja resolues par les sources, pack actif numerote, audit fidelite source, revue associe par ecarts concrets, regeneration apres correction et cloture en `DONE`, `PARTIAL` ou `BLOCKED`.
- 2026-06-01 : SELARL-CANONICAL-STATUS-001 cree `docs/project/SELARL_CANONICAL_STATUS_V1.md`, designe ce fichier comme point de reprise SELARL unique, classe l'extension complexe en `NO-GO dev` tant qu'un sous-cas n'est pas choisi, et confirme la revue humaine comme prochaine etape recommandee avant nouveau developpement. Apres correction `DOC-006`, le ticket courant est `SELARL-FINAL-ASSOCIE-VALIDATION-001`.
- 2026-06-01 : TRACK-B-PREVIEW-VALIDATION-AND-CHECKPOINT-009 valide le clean front Track B sans `Start-Process` via `python -m streamlit run src/sydel_doc_engine/front_app/app.py --server.port 8534 --server.headless true --browser.gatherUsageStats false`, confirme HTTP 200 sur `http://127.0.0.1:8534`, arrete le process proprement, verifie le mode `SELARL dentiste multi-associes simple (PARTIAL statuts)`, classe les changements Track B a committer et prepare le checkpoint local `feat: advance track B SELARL production pack` sans push.
- 2026-05-31 : TRACK-B-SELARL-DENTIST-MULTI-ASSOCIES-STATUTS-PARTIAL-008 ajoute dans le clean front le mode `SELARL dentiste multi-associes simple (PARTIAL statuts)`, genere `DOC-004` et `DOC-016`, derive les apports simples par associe, rend la repartition du capital dentiste multi-associes simple et documente `DOC-016` en PARTIAL sur comparution/signatures strictes ; tests cibles, ruff et smoke DOCX/ZIP OK ; preview HTTP non validee car le lancement Streamlit via `Start-Process` est reste bloque dans le shell local, ports 8532/8533 verifies libres ; plusieurs gerants, president externe, cession, SCM, votes non unanimes et medecin multi-associes restent hors scope.
- 2026-05-31 : TRACK-B-SELARL-MULTI-ASSOCIES-DOC004-LIMITED-007 ajoute dans le clean front un mode `SELARL multi-associes simple (limite DOC-004)`, collecte les associes du PV, choisit le president parmi les associes, genere uniquement `DOC-004`, garde un gerant unique et bloque les parts incoherentes ; statuts multi-associes, plusieurs gerants, cession, SCM et votes non unanimes restent hors scope.
- 2026-05-31 : TRACK-B-SELARL-MULTI-ASSOCIES-SOURCE-CONTRACT-006 cree `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md`, classe le sous-cas multi-associes simple / president associe existant / gerant unique en GO limite pour `DOC-004`, et maintient en NO-GO les statuts multi-associes, plusieurs gerants, president externe, cession medicale/dentaire et cession SCM dans ce contrat ; aucun code/front/generateur modifie.
- 2026-05-31 : TRACK-B-SELARL-DENTIST-LINE-BY-LINE-LOCK-003 crée `docs/review/track_b_selarl_dentist_line_by_line_lock_003_report_v1.md`, compare DOC-016 articles 1 à 34 ligne par ligne contre `Retours humains .docx` avec 243/243 paragraphes conformes, ferme le point procuration RCS/téléphone + clause finale, corrige l'introduction PV en formulation humaine plurielle et conserve un OPEN GAP limité au wrapper post-article statuts non couvert par la référence humaine.
- 2026-05-31 : TRACK-B-SELARL-HUMAN-REFERENCE-LOCK-002 verrouille `Retours humains .docx` comme référence prioritaire SELARL, crée `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md`, finalise les corrections humaines sur autorisation de domiciliation, DNC, renonciation, PV nomination gérant et statuts SELARL chirurgien-dentiste, avec variables de président de séance et dérivation depuis l'associé unique dans le clean front.
- 2026-05-27 : TRACK-B-SELARL-TEST-DATA-PREFILL-001 ajoute un bouton `Generer des donnees de test` sous `Type de dossier` dans le clean front SELARL ; il pre-remplit un cas aleatoire coherent, hors scope V1 desactive, capital/parts coherents, dates JJ/MM/AAAA, ordre, banque et conjoint si necessaire ; AppTest verifie que le cas devient generable et expose le telechargement ZIP ; `ruff check .` OK, test clean front OK, HTTP 200 sur `http://localhost:8512` avec PID `35648` arrete, browser-use refuse localhost donc non contourne.
- 2026-05-27 : TRACK-B-SELARL-DOWNLOAD-UX-001 ajoute des boutons `Telecharger le dossier ZIP` et `Telecharger ...docx` dans le clean front apres generation, avec conservation du dernier dossier genere en session Streamlit ; test AppTest ajoute pour verifier l'apparition des 7 boutons de telechargement ; `ruff check .` OK, test clean front OK, HTTP 200 sur `http://localhost:8511` avec PID `16648` arrete, browser-use refuse localhost donc non contourne.
- 2026-05-27 : TRACK-B-SELARL-UX-FOLLOWUP-001 remplace les dates Streamlit par des champs `JJ/MM/AAAA`, ajoute la liste `Situation matrimoniale`, retire le doublon visible `Regime matrimonial`, calcule la valeur nominale depuis capital / parts et clarifie les champs d'ordre ; `ruff check .` OK, test clean front OK, HTTP 200 sur `http://localhost:8510` avec PID `3480` arrete.
- 2026-05-27 : TRACK-B-SELARL-UX-DEDUP-RECONCILIATION-001 nettoie l'UX du clean front SELARL V1 : genre/titre, montants et dates en lettres, mandataire, prestataire de signature, seuils de gerance, lieu d'exercice et conjoint sont derives, pre-remplis ou conditionnels ; tests clean front et ruff valides, aucun push/merge.
- 2026-05-12 : mémoire projet installée dans `docs/project/`.
- 2026-05-12 : mémoire projet complétée pour servir de contexte opérationnel autonome ; artefact `tall -U pip` identifié comme fichier parasite à supprimer.
- 2026-05-12 : kit de reprise ajouté pour nouveau ChatGPT / Codex avec handoff, dernier état et prompt de reprise.
- 2026-05-12 : DOC-001 implémenté en génération DOCX from-scratch avec tests unitaires ; validations locales vertes.
- 2026-05-12 : DOC-001 corrigé pour rendre l'adresse personnelle dans l'ordre source `num voie + voie, ville cp`.
- 2026-05-12 : DOC-003 implémenté en génération DOCX from-scratch avec tests unitaires ; validations locales vertes.
- 2026-05-12 : DOC-002 implémenté en génération DOCX from-scratch avec champ libre `adresse_domiciliation_affichee` ; validations locales vertes.
- 2026-05-12 : ORCH-001 branche les générateurs DOC-001, DOC-002 et DOC-003 dans l'orchestrateur dossier ; génération DOCX uniquement.
- 2026-05-13 : logique documentaire du moteur formalisée par l'arbre document-centré V1 ; mémoire projet alignée sans réécriture de l'arbre.
- 2026-05-13 : SMOKE-001 génère réellement les trois DOCX du Lot 1 via l'orchestrateur avec `examples/contexts/lot_01_example.yaml` corrigé au strict minimum.
- 2026-05-13 : dictionnaire canonique des variables V1 intégré dans la mémoire projet ; le moteur dispose désormais d'un arbre documentaire et d'un dictionnaire canonique de variables.
- 2026-05-13 : table de mapping document -> variables canoniques V1 intégrée dans la mémoire projet sans réécriture ; écart temporaire `domiciliation.adresse_affichee` / `adresse_domiciliation_affichee` documenté.
- 2026-05-13 : cadrage métier V1 de la famille `PV nomination gérant` intégré dans la mémoire projet ; SPEC-PV-001 ajouté en READY et UI-001 placé en attente tant que cette famille n'est pas spécifiée.
- 2026-05-13 : spec canonique V1 de la famille `PV nomination gérant` intégrée dans la mémoire projet ; SPEC-PV-001 passé DONE, SPEC-TEXTE-PV-001 ajouté READY, UI-001 maintenu en attente explicite.
- 2026-05-13 : spec texte V1 de la famille `PV nomination gérant` créée ; SPEC-TEXTE-PV-001 passé DONE, CODE-PV-001 ajouté READY, aucun code Python modifié.
- 2026-05-13 : CODE-PV-001 implémente le générateur DOCX from-scratch du PV nomination gérant avec `associes[]`, `dirigeant_nomine`, branche `emprunt.actif`, variantes de genre/singulier-pluriel et tests ciblés ; ruff et pytest verts.
- 2026-05-13 : smoke test réel CODE-PV-001 ajouté via `examples/contexts/lot_02_pv_nomination_gerant_example.yaml` ; DOCX généré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/` hors versionnement.
- 2026-05-13 : REVIEW-PV-001 régénère le DOCX PV depuis le contexte exemple, extrait un aperçu texte et crée une checklist de revue humaine dans `docs/review/`, sans modification du code Python.
- 2026-05-13 : SPEC-RENDER-001 crée la spec technique `docs/delivery/render_style_system_v1.md` pour une couche de rendu DOCX commune, sans modification de code Python.
- 2026-05-13 : RENDER-STYLE-001 implémente la couche commune de rendu DOCX, migre DOC-001/DOC-002/DOC-003/PV nomination gérant, ajoute les tests de rendu et génère les smoke DOCX dans `artifacts/render_style_001_*`.
- 2026-05-13 : ORCH-L2-PV-001 branche le PV nomination gérant dans le catalogue et l'orchestrateur pour SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI et SCM ; SAS reste exclue ; ruff et pytest verts.
- 2026-05-13 : SMOKE-ORCH-L2-001 ajoute deux contextes orchestrateur Lot 2, génère réellement le dossier SCI positif et le dossier SAS négatif, puis documente la présence/absence du PV dans `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- 2026-05-13 : ANALYSE-ORDRE-001 crée les cadrages V1 pour `Demande d'inscription à l'ordre` et le batch `régime communautaire`, puis ajoute SPEC-ORDRE-001 et SPEC-RC-001 en READY, sans modification de code Python.
- 2026-05-13 : ARBITRAGE-SOURCES-001 répare les docs projet 10/11/12, crée les décisions d'arbitrage sources V1, classe les cas HIGH/MEDIUM/LOW et ajoute PLACEMENT-HIGH-001 en READY, sans déplacer de fichier source.
- 2026-05-14 : PLACEMENT-HIGH-001 confirme en no-op les 4 cas HIGH déjà présents dans `source_documents`, crée le journal d'exécution V1 et ne touche pas aux cas MEDIUM/LOW ni au raw dump.
- 2026-05-14 : SPEC-ORDRE-001 compare les variantes `Demande d'inscription à l'ordre` SELARL, SELAS et SPFPL, crée la spec canonique V1 et ajoute SPEC-TEXTE-ORDRE-001 en READY, sans modification de code Python.
- 2026-05-14 : SPEC-TEXTE-ORDRE-001 crée la spec texte V1 `Demande d'inscription à l'ordre`, retient un tronc commun avec overlays SELARL/SELAS, SPFPL cession/apport et SCM, classe `Dérogation ?` en bloc manuel conditionnel, puis ajoute CODE-ORDRE-001 en READY, sans modification de code Python.
- 2026-05-14 : FIX-PV-RENDER-001 améliore la structure visuelle du PV nomination gérant from-scratch : listes à tirets, titre encadré, intertitres visibles, formules de vote en italique et smoke DOCX dédié.
- 2026-05-14 : CODE-ORDRE-001 implémente le générateur DOCX from-scratch `Demande d'inscription à l'ordre`, couvre SELARL, SELAS, SPFPL cession, SPFPL apport et SCM, teste la dérogation manuelle et le mandataire configurable, puis génère un smoke DOCX dédié.
- 2026-05-14 : SPEC-RC-001 crée les specs canonique et texte V1 du batch régime communautaire, compare les variantes SELARL / SELAS / SPFPL, retient deux documents canoniques distincts et ajoute CODE-RC-001 en READY, sans modification de code Python.
- 2026-05-14 : SYNC-SPECS-001 absorbe dans `main` les specs parallèles RC, SPFPL, dérogations et cession/bail, puis aligne le pilotage sur `CODE-RC-001` READY, sans stage de code Python.
- 2026-05-14 : CODE-RC-001 implémente le batch régime communautaire V1 avec deux générateurs DOCX from-scratch, champs modèle dédiés, catalogue/orchestrateur conditionnés par `dossier_options.regime_communautaire`, tests ciblés et smoke DOCX réel.
- 2026-05-14 : SYNC-TEXTE-SPECS-001 absorbe dans `main` les specs texte parallèles bail/appel, cession cabinets, dérogations et SPFPL, puis confirme `CODE-BAIL-APP-001`, `ARBITRAGE-CESSION-001`, `ARBITRAGE-DEROG-001` et `ARBITRAGE-SPFPL-001` en READY, sans modification de code Python.
- 2026-05-14 : SYNC-ARBITRAGES-001 absorbe dans `main` les arbitrages cession cabinets, dérogations et SPFPL, passe les trois tickets d'arbitrage en DONE et confirme `CODE-BAIL-APP-001`, `CODE-CESSION-CAB-001` et `CODE-SPFPL-001` en READY, sans modification de code Python.
- 2026-05-14 : SYNC-CODE-BAIL-APP-001 absorbe dans `main` le commit `557a013274aa9f7122c81d5e6e0b52c4043a540c`, passe `CODE-BAIL-APP-001` en DONE et confirme `CODE-CESSION-CAB-001`, `PREP-DEROG-001` et `CODE-SPFPL-AGR-INFO-001` en READY/parallélisables, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-WAVE-LOT03-05-001 absorbe dans `main` les commits `36828fbc45d6b8a37c2e76eb8227460df441ebde` et `958fce5d2a9d5d30df4d918cb098fec483f5140e`, passe `PREP-DEROG-001` et `CODE-SPFPL-AGR-INFO-001` en DONE, puis confirme `RESUME-CODE-CESSION-CAB-001` et `CODE-DEROG-CORE-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : RESUME-CODE-CESSION-CAB-001 reprend `CODE-CESSION-CAB-001` depuis `main`, restaure les générateurs cession cabinets, branche `DOC-009` à `DOC-012`, génère quatre DOCX de smoke test et valide `ruff` / `pytest`.
- 2026-05-14 : CODE-DEROG-CORE-001 implémente les générateurs DOCX partiels `multi_sites_sel` et `cumul_sel_bnc`, les branche au catalogue/orchestrateur sous `DOC-013` et `DOC-014`, ajoute le contexte exemple et les tests ciblés, puis génère le smoke DOCX réel dans `artifacts/lot_03_derogations_core_smoke_test/`.
- 2026-05-14 : SYNC-CODE-WAVE-002 absorbe dans `main` les commits sources `ea35d2af353ac5b8567e82091ab978cf24a27445` et `bee4c8bec27397198a170c4f9888b2470b24c67f`, confirme `CODE-CESSION-CAB-001` et `CODE-DEROG-CORE-001` en DONE, puis confirme `CODE-SPFPL-CORE-001` et `PREP-STATUTS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-WAVE-003 absorbe dans `main` les commits sources `b854821061b85ac66fe785c11cb3c6b0bac5a85b` et `09cbad120d22910f05ba5e645971ade56fedb76d`, passe `PREP-STATUTS-001` et `CODE-SPFPL-CORE-001` en DONE, puis confirme `SPEC-STATUTS-SEL-001`, `SPEC-STATUTS-SPFPL-001`, `SPEC-STATUTS-CIVILS-001` et `SPEC-STATUTS-SAS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-STATUTS-SPECS-001 absorbe dans `main` les commits sources `00b7886ac431c8a47d9cdcca8bfed026a756cb69`, `b34c66e5e67f3261317035943e974536be27d6d3`, `9b25e09d08ec2161d757d1581c34073dcbbc594f` et `704eeb7301cf69460c16b2ed9fbc0ea22ca83c8c`, passe les quatre specs statuts en DONE, puis confirme `CODE-STATUTS-SAS-001`, `CODE-STATUTS-SPFPL-001`, `ARBITRAGE-STATUTS-SEL-001` et `ARBITRAGE-STATUTS-CIVILS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-STATUTS-CODE-ARB-001 absorbe dans `main` les commits sources `82e67120ed714b791d5483108336a570ea520e59`, `a98939c649e4124e40f2cd69c9ed125d342acc31` et `1caafd7`, passe `CODE-STATUTS-SAS-001`, `CODE-STATUTS-SPFPL-001` et `ARBITRAGE-STATUTS-SEL-001` en DONE, puis confirme `CODE-STATUTS-SEL-001`, `RESUME-ARBITRAGE-STATUTS-CIVILS-001` et `STYLE-ANALYSE-BATCH-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : SYNC-STYLE-CIVILS-001 absorbe dans `main` les commits sources `76dd139da65c233f0c6aecc76bc2ea5e929381ca` et `b21f1b0cc5b975049e4acc279b8303f1d739b60f`, passe `STYLE-ANALYSE-BATCH-001` et `ARBITRAGE-STATUTS-CIVILS-001` en DONE, puis confirme `CODE-STATUTS-SEL-001`, `CODE-STATUTS-CIVILS-CORE-001` et `FIX-STYLE-LETTERS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : SYNC-STATUTS-SEL-CIVILS-001 absorbe dans `main` le commit source `9a79560c4bae1ae3a98ec5305b4187f9f4ebd6a8`, confirme l'arbitrage civils V1 déjà présent avec un contenu identique au commit source `b21f1b0cc5b975049e4acc279b8303f1d739b60f`, passe `CODE-STATUTS-SEL-001` en DONE, puis confirme `RESUME-FIX-STYLE-LETTERS-001` et `CODE-STATUTS-CIVILS-CORE-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : CODE-STATUTS-CIVILS-CORE-001 implémente les générateurs statuts SCS, SCI et SCI IRIS, ajoute le modèle `statuts_civils`, branche DOC-019 à DOC-021 au catalogue/orchestrateur, ajoute le contexte exemple et génère le smoke DOCX réel ; SCM reste hors ticket.
- 2026-05-15 : SYNC-WAVE-004 absorbe dans `main` les commits sources `557fc1920361a8c7831e6b023d70471c9c29e5ff` et `291da7b6db68b3de413fba50cf652dde98a8f6a8`, passe `RESUME-FIX-STYLE-LETTERS-001`, `FIX-STYLE-LETTERS-001` et `CODE-STATUTS-CIVILS-CORE-001` en DONE, puis confirme `ARBITRAGE-STATUTS-SCM-001`, `PREP-SCM-SAT-001`, `SPEC-SAS-SATELLITES-001`, `CODE-OPTION-IS-001` et `PREP-ACTE-ACTIONS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : SYNC-WAVE-005 absorbe dans `main` les commits sources `91436f0916fdecbcc98450b72ba6e602cb8f1a3b`, `1b3ba14d0bcc31fc7dcbf1752d6d3263645ae8b3`, `32059155c618b4e985893f42ef2817187599c281`, `74d41db53543b790e197082e8b9c713f7de92dc2` et `d1d649e11fdc638e6d7da0640c154d1f213739ee`, passe `CODE-OPTION-IS-001`, `PREP-SCM-SAT-001`, `ARBITRAGE-STATUTS-SCM-001`, `SPEC-SAS-SATELLITES-001` et `PREP-ACTE-ACTIONS-001` en DONE, puis confirme `CODE-STATUTS-SCM-001`, `CODE-SAS-SATELLITES-001`, `SPEC-SCM-SATELLITES-001`, `CONVERT-ACTE-ACTIONS-001` et `CONVERT-DEROG-SALARIEE-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : CONVERT-DEROG-SALARIEE-001 retente la conversion Word COM du `.doc` legacy salariee ; aucun DOCX exploitable n'est produit, le blocage est documente dans `docs/delivery/lot_03_derogation_salariee_conversion_blocker_v1.md`, sans modification de code Python.
- 2026-05-15 : CONVERT-ACTE-ACTIONS-001 convertit `Acte_cession_SPFPL_tiers_modele.doc` en DOCX via `Wordconv.exe`, place le résultat dans `project/source_documents/lot_05/` et documente l'origine/confiance dans `docs/delivery/lot_05_acte_cession_actions_preparation_v1.md`, sans modification de code Python.
- 2026-05-15 : SYNC-WAVE-006 absorbe dans `main` les commits sources `557fc1920361a8c7831e6b023d70471c9c29e5ff` et `291da7b6db68b3de413fba50cf652dde98a8f6a8` par équivalence, puis cherry-picke `2c55a7ab5f8a44de5c29305cfbc280f930ee32ec`, `568336bed7ccb0a5901abe5d921fd9056573e32d`, `8f0c8ab13d6e8f1a9e50747f8a9d5b607bcb90d6` et `11dc0d8dda23f841d650586e0977e0202270a3b5`, passe la vague en DONE, puis confirme les prochains tickets READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : SYNC-WAVE-007 absorbe dans `main` les commits sources `3c040774cdfe57c203b78776a9ea412ec3d14d94`, `6453b6f64665feda898a076f730cba9a6684825b`, `075af377f7c9d7475429f1e738b46483127d757f` et `c221681570782a1b1efc5afc72087cb903cd8a65`, passe les quatre tickets correspondants en DONE, puis confirme les prochains tickets READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : SYNC-WAVE-008 absorbe dans `main` les commits sources `61a1c49353724bbf5b8f1bb8f039d5e96b877ecc`, `d3188c0b4a4a61d889a2ce9ccc37e84e1284adaa`, `939e1c2088892abcf4a8fdcbaa35911f4f8a2f9f`, `19468886f5e885f79b2b35e17e2ff2a097ea9c3a`, `d8747ef20aba478c575c5a491cdf0f634a9c26d3`, `00b4c955b372399bb8701f47a5686748539f061b`, `a181e069f756a1ea846fdcd1824b3f8c57cc11f5` et `518e46fbb8d8bee03a23ea203654b4199103fb7e`, passe les huit tickets correspondants en DONE, puis confirme les prochains tickets READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : FINAL-SCM-CESSION-WAVE-001 restaure la résolution V1 cession SCM, implémente `DOC-031` à `DOC-033`, génère le smoke DOCX réel, valide ruff/pytest et crée l'audit de clôture moteur V1.
- 2026-05-15 : SYNC-CLOSE-AUDIT-001 absorbe le commit source `0139202b170531fd628f25811c55855a2512acc0` depuis `origin/codex/close-motor-audit-001`, confirme `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` sur `main` et conserve la version finale plus récente, sans modification de code Python.
- 2026-05-17 : RECONCILE-MOTOR-CLOSE-001 expose les générateurs ordre/SPFPL sous `DOC-034` à `DOC-043`, consolide `08/09`, intègre `17/18`, corrige l'audit `16` et clôt le moteur DOCX V1 hors UI/PDF/ZIP/recette finale.
- 2026-05-17 : PDF-BACKEND-001 ajoute un backend d'export PDF best-effort avec priorité LibreOffice headless puis fallback Word COM Windows, tests ciblés et smoke réel DOCX vers PDF.
- 2026-05-17 : SYNC-POST-MOTOR-UI-001 absorbe dans `main` les commits sources `d62670efe10481926437c0e1a5dabbe349fd5938`, `24a881b999371811d39a2403c0b51d9ae8ce0556`, `ef6252b3c15dc3fc39f1efdc05687c0f448f8fe1`, `2f76f61848469ddf2f7b29c3169e8893e83fd3a5` et `c2fc0db4d51485c7c5e721c5184028ae17c68cb3`, passe les fondations UI/PDF/recette en DONE et confirme `UI-CORE-001`, `RESUME-ZIP-BACKEND-001` et `REVIEW-FINAL-001` en READY.
- 2026-05-17 : UI-PDF-ZIP-INTEGRATION-001 branche l'UI Streamlit sur la génération dossier DOCX, l'export PDF local optionnel et le ZIP de sortie, ajoute un smoke manuel documenté et conserve `artifacts/` hors versionnement.
- 2026-05-17 : SYNC-FINAL-FOUNDATIONS-001 absorbe les compléments manquants `UI-PDF-ZIP-INTEGRATION-001` et `ZIP-BACKEND-001`, confirme les fondations/audits déjà présents sur `main`, remplace `UI-CORE-001` par `UI-PDF-ZIP-INTEGRATION-001`, valide ruff/pytest 191 tests et confirme uniquement `REVIEW-FINAL-001` puis `CLOSE-PROJECT-V1-001` en READY.
- 2026-05-18 : WORKTREE-CLEANUP-AND-UI-STATUS-001 integre le pack `docs/review/final_review_pack_v1.md` depuis `codex/review-final-001`, cree `docs/project/23_WORKTREE_CLEANUP_AND_UI_STATUS_V1.md`, documente l'archivage local des worktrees et confirme que l'UI actuelle est une UI technique de pilotage par contexte, pas une UI produit finale.
- 2026-05-18 : UI-BUSINESS-WIZARD-001 ajoute le mode Assistant metier Streamlit en deux modes, construit un contexte SCI simple pour `DOC-001` a `DOC-004`, conserve le mode technique YAML/JSON, separe les actions DOCX/ZIP/PDF et valide ruff + pytest 196 tests.
- 2026-05-18 : DEPLOY-STREAMLIT-CLOUD-FIX-001 ajoute la declaration Poetry explicite du package `src/sydel_doc_engine`, documente la cause racine Streamlit Cloud et valide installation editable, ruff et pytest 196 tests ; Poetry local reste indisponible.
- 2026-05-18 : CASE-CATALOG-001 cree le service pur `get_expected_documents(...)` et le catalogue metier par cas depuis la source Word canonique, couvre 46 documents attendus uniques dont 43 mappes a `DOC-XXX`, documente 2 manuels et 1 non implemente, ajoute les tests unitaires de selection et valide ruff + pytest 208 tests.
- 2026-05-19 : SELARL-PILOT-PROTOCOL-001 ajoute la source V2 cible, cree le protocole de construction de processus, les specs produit/formulaire/wizard SELARL et le plan d'implementation, puis valide ruff + pytest 217 tests sans modifier l'UI, le moteur ni les generateurs.
- 2026-05-19 : SELARL-PILOT-SOURCE-VERIFY-001 lit la vraie source V2, remplace le fichier canonique provisoire, corrige les statuts SELARL `DOC-013` / `DOC-014` en manuel, complète les variables V2 dans les specs et crée la matrice d'écarts source.
- 2026-05-19 : SELARL-FORM-SCHEMA-IMPL-001 ajoute le module `selarl_form_schema.py`, verrouille la réserve source V2 sur `DOC-006`, confirme `DOC-013` / `DOC-014` hors génération pilote et teste la couverture des variables V2 ; ruff OK et pytest 231 tests passés.
- 2026-05-19 : SELARL-UI-WIZARD-IMPL-001 branche l'Assistant métier Streamlit sur le schéma SELARL, ajoute le parcours pilote visible, conserve SCI et Technique / diagnostic, affiche les documents manuels/réservés et valide ruff + pytest 239 tests.
- 2026-05-19 : SELARL-NOTEBOOKLM-RECONCILIATION-001 ajoute les sources NotebookLM/V3, crée la hiérarchie source SELARL V2, le rapport d'écarts et le backlog de reconstruction ; aucun code Python modifié, smoke SELARL bloqué jusqu'au réalignement wording / flow / réutilisations / UI.
- 2026-05-19 : SELARL-PLAN-CORRECTION-001 corrige la planification selon les arbitrages associé (`Fiche Client`, `Praticien`, `Dossier unipersonnel`), retire le ticket statut documentaire lourd, exclut mode Projet / filigrane V1 et confirme que l'UI SELARL ne doit pas être poussée/redéployée avant réalignement produit.
- 2026-05-19 : SELARL-WORDING-REALIGN-001 remplace le vocabulaire visible SELARL par `Fiche Client` / `Praticien` / rôles juridiques exacts, conserve l'ordre et la logique, ajoute les tests anti-régression wording et valide ruff + pytest 241 tests.
- 2026-05-19 : SELARL-FLOW-REALIGN-001 ajoute le flow conceptuel SELARL en six étapes dans le schéma et les projections métier, met à jour les specs actives, laisse `streamlit_app.py` intact pour le ticket UI dédié et valide les tests ciblés schema/wizard.
- 2026-05-19 : SELARL-REUSE-RULES-REALIGN-001 ajoute `Dossier unipersonnel` comme règle pivot, conserve les réutilisations utiles en opt-in, sort le mandataire du défaut UX, documente les relations non automatiques et valide ruff + pytest 252 tests.
- 2026-05-19 : SELARL-UI-REALIGN-001 réaligne le parcours Streamlit visible SELARL en six écrans, expose `Dossier unipersonnel`, rend le mandataire secondaire, conserve SCI et Technique / diagnostic, puis valide ruff + pytest 257 tests.
- 2026-05-19 : SELARL-SMOKE-REALISTIC-001 exécute trois scénarios SELARL réalistes, génère `DOC-001` à `DOC-004` et un ZIP par scénario, confirme l'exclusion des documents manuels `DOC-013` / `DOC-014`, la réserve `DOC-006`, le blocage contexte incomplet V2 des documents non prêts et prépare la revue associé / juriste.
- 2026-05-20 : SELARL-CLOUD-GENERATION-BUG-001 reproduit le blocage de génération visible quand les réutilisations SELARL sont cochées avant saisie, corrige le `session_state` des champs dérivés associé/domiciliation, ajoute un test AppTest de génération réelle et valide ruff + pytest 266 tests ; commit local bloqué par refus d'écriture dans `.git`.
- 2026-05-20 : DOCUMENT-UNITAIRE-001 ajoute le mode Streamlit `Document unitaire`, limite la V1 à `DOC-001` à `DOC-004`, affiche honnêtement les documents manuels ou non encore supportés et valide ruff + pytest 266 tests.
- 2026-05-20 : ASSISTANT-METIER-PREFILL-001 ajoute des scénarios de test déterministes dans l'Assistant métier, avec sélecteur, préremplissage, réinitialisation, indication visible, synchronisation `session_state` des champs dérivés SELARL/domiciliation et non-régression SCI/Document unitaire/Technique ; aucun générateur, moteur DOCX/PDF/ZIP ni wording juridique modifié.
- 2026-05-20 : GLOBAL-VARIABLE-INVENTORY-001 crée l'inventaire global brut `docs/project/GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv` et le rapport `docs/review/global_variable_inventory_001_report_v1.md` : 12 443 lignes, 43 documents `DOC-001` à `DOC-043`, 15 familles, aucun générateur/moteur/UI/wording juridique modifié.
- 2026-05-20 : GLOBAL-VARIABLE-IDENTITY-AUDIT-001 crée la matrice d'identité V2, le registre canonique global V2, la liste de 10 questions humaines et le rapport exécutif : 1 334 slugs distincts audités, 49 champs proposés, 142 rapprochements classés, aucun générateur/moteur/UI/wording juridique modifié.
- 2026-05-24 : GLOBAL-FRONT-ARCHITECTURE-001 crée l'architecture front globale V1, le modèle d'objets, les règles structurelles, la stratégie d'écrans, le backlog de rebuild et le rapport exécutif ; aucun générateur, moteur DOCX/PDF/ZIP, Streamlit ou wording juridique modifié.
- 2026-05-24 : GLOBAL-FRONT-ARCHITECTURE-QA-001 contrôle l'architecture front sur 7 documents sentinelles, crée le rapport QA et le CSV de couverture ; verdict global ORANGE maîtrisable, aucun rouge, aucun générateur/moteur/UI/Python modifié.
- 2026-05-24 : FRONT-DATA-LAYER-001 crée le package `front_data` avec objets front globaux, mapping canonique V2.1, checks sentinelles, diagnostics de validation et tests unitaires ; ruff OK et pytest 288 tests passés ; aucun générateur, moteur DOCX/PDF/ZIP, Streamlit ou UI visible modifié.
- 2026-05-24 : FRONT-ROLE-MODEL-001 raffine les roles front globaux avec familles, portees, modele ordre, representation de personne morale, tiers commissaire/evaluateur, garde-fous de placeholders et tests dedies ; ruff OK et pytest 298 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, Streamlit ou UI visible modifie.
- 2026-05-24 : FRONT-ADDRESS-MODEL-001 raffine les adresses typees avec usages explicites, politiques de reutilisation tracees, formes affichees/composants, overrides legacy, mapping canonique et validations dediees ; ruff OK et pytest 313 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, Streamlit ou UI visible modifie.
- 2026-05-24 : FRONT-TEST-PREFILL-001 realigne les prefills fictifs de l'Assistant metier sur `front_data`, conserve les quatre scenarios existants, ajoute les profils front_data, la conversion en `BusinessWizardInput`, le `DossierRecord` de test, la synthese de statuts documentaires et les tests dedies ; ruff OK et pytest OK, 352 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, wording juridique, mode Technique ou mode Document unitaire modifie.
- 2026-05-24 : FRONT-REVIEW-001 audite le prototype Streamlit face aux fondations `front_data`, classe les briques en prototype / migration / test / deprecation, cree `FRONT_MIGRATION_MAP_V1.md`, met a jour le backlog vers `FRONT-UI-SHELL-001` puis les tickets UI visibles ; aucun code Python, generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-24 : FRONT-DOSSIER-EDITOR-001 ajoute un editeur dossier V1 dans le nouveau shell, avec profils prudents, `DossierRecord` minimal, etapes/blocs `dossier_flow`, exigences, documents attendus et statuts/lots `document_status` ; ruff OK et pytest OK, 364 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, wording juridique ou prototype historique modifie.
- 2026-05-24 : FRONT-DOSSIER-DATA-ENTRY-001 ajoute la premiere saisie reelle du nouvel editeur dossier sur le profil `SELARL creation simple` : personne principale, societe principale, adresses typees, role assignments explicites, `domiciliation = siege` via `ReuseRuleState`, valeurs canoniques et statuts DOC-001 a DOC-004 recalcules ; aucun generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-24 : FRONT-GENERATION-ACTIONS-001 branche les actions de generation du nouveau front sur le profil `SELARL creation simple`, cree l'adaptateur `DossierRecord` vers contexte moteur, limite la generation a `DOC-001` a `DOC-004`, exclut `DOC-006`, `DOC-013` et `DOC-014`, expose DOCX/ZIP/PDF optionnel dans le shell, valide ruff et pytest 380 tests, et conserve le prototype comme zone secondaire ; aucun generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-24 : FRONT-UX-CLEANUP-001 simplifie la vue principale du nouveau front : suppression de la navigation interne visible, tables de flow/blocs/exigences/statuts repliees en diagnostics, parcours principal limite a type de dossier, saisie, resume documents et generation ; ruff OK et pytest OK 380 tests ; aucun generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-24 : FRONT-UX-HARD-CUT-001 retire les diagnostics et outils de la surface utilisateur normale : aucun radio, aucun tableau par defaut, seulement Type de dossier / Donnees a saisir / Generation ; les outils internes sont accessibles via sidebar `Outils internes`, ruff OK et pytest OK 380 tests ; aucun generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-25 : FRONT-REALITY-CHECK-001 audite le front reel contre les debriefs recents, confirme DOCX/ZIP branches sur `DOC-001` a `DOC-004`, PDF conditionnel indisponible localement, identifie les pollutions restantes de surface et cree le plan `FRONT_MINIMAL_USER_SURFACE_V1.md`; aucun Python, generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-25 : FRONT-MINIMAL-SURFACE-CLEANUP-001 applique la surface minimale du nouveau front : 3 zones principales, 0 radio, 0 table, 0 expander, outils internes caches par mode equipe, PDF cache si backend indisponible et blocages visibles dans `Generation`; ruff OK et pytest OK, 382 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique modifie.
- 2026-05-25 : SELARL-COMPLETE-CASE-PLAYBOOK-001 cadre la SELARL complete : le moteur est plus avance que le front, la generation visible reste limitee a `DOC-001` a `DOC-004`, les documents manuels restent hors generation, et le prochain ticket unique devient `SELARL-COMPLETE-CONTEXT-ADAPTER-001`; aucun Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique modifie.
- 2026-05-25 : SELARL-COMPLETE-CONTEXT-ADAPTER-001 branche la selection/readiness/contexte SELARL complet cote nouveau front : medecin simple genere 6 DOCX (`DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-017`), dentiste bascule vers `DOC-016`, regime communautaire ajoute `DOC-005`; note 2026-06-01 : `DOC-006` est desormais ajoute aussi par `SELARL-DOC006-REGIME-FIX-001`.
- 2026-05-26 : TRACK-B-FRONT-ARCHITECTURE-RESET-001 cree le nouveau point d'entree clean `src/sydel_doc_engine/front_app/app.py`, separe shell/routing/selection/saisie/generation du legacy, conserve `app/streamlit_app.py` comme reference historique non importee, documente la frontiere legacy et le lancement local ; generation SELARL volontairement non implementee dans ce ticket ; aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique modifie.
- 2026-05-26 : TRACK-B-SELARL-SOURCE-OF-TRUTH-CONTRACT-001 cree le contrat `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md`, consolide les sources metier SELARL et conclut GO pour une vertical slice V1 strictement bornee ; aucun code, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique modifie.
- 2026-05-31 : TRACK-B-SELARL-ROLLOUT-NEXT-CASE-001 choisit la SELARL medecin unipersonnelle standard comme prochain cas GO apres le lock dentiste, cree le rapport de matrice/decision, lance le smoke DOCX/ZIP medecin et ne modifie pas le moteur/front car le delta utile est deja cable.
- 2026-05-31 : TRACK-B-SELARL-MEDECIN-LINE-BY-LINE-LOCK-004 compare `DOC-017` a la source repo `Modèle statuts SELARL médecins.docx`, ajoute un test ligne par ligne article/signature/annexe, classe le `DOC-017` LOCKED source-level en unipersonnel standard avec OPEN GAP limite a l'absence de retour humain medecin recent et a la ligne source `personne_2` incomplete.
- 2026-05-31 : TRACK-B-SELARL-MEDECIN-REGIME-COMMUNAUTAIRE-005 industrialise le cas SELARL medecin unipersonnelle avec regime communautaire ; note 2026-06-01 : `DOC-006` n'est plus reserve et est genere avec `DOC-005` dans les packs regime communautaire.
- 2026-06-01 : SELARL-ASSOCIE-REVIEW-001 recoit le retour associe initial. Suite corrigee : `SELARL-DOC006-REGIME-FIX-001`, audit retours humains approfondi, audit trois sources, pack 004, puis `SELARL-FINAL-ASSOCIE-VALIDATION-001`.
- 2026-06-02 : SELARL-HUMAN-RETURNS-006-TRIAGE-001 recoit de nouveaux retours humains SELARL sous forme texte, cree `docs/review/selarl_human_returns_006_raw_v1.md`, cree le triage `docs/review/selarl_human_returns_triage_006_report_v1.md`, ouvre les tickets de correction `SELARL-RETURNS-006-*`, bloque `SELARL-CANONICAL-CLOSE-001` jusqu'au pack 005 et recommande de commencer par `SELARL-RETURNS-006-STATUTS-001`.
- 2026-06-02 : SELARL-RETURNS-006-STATUTS-001 corrige `DOC-016`/`DOC-017` selon retours humains 006 : clause matrimoniale communaute/separation de biens apres l'identite ordinale, accord d'`associe` article 8, annexe page suivante, tiret devant `Ouverture...`. Rapport `docs/review/selarl_returns_006_statuts_001_report_v1.md`. Validations : tests statuts SEL 14 passes, ruff cible OK. Prochaine action : `SELARL-RETURNS-006-DNC-001`.
- 2026-06-02 : SELARL-RETURNS-006-DNC-001 corrige `DOC-001` selon retours humains 006 : naissance avec ville `a/au`, champ moteur/front `ville_naissance_article_au`, propagation clean front, front historique, wizard metier et document unitaire. Rapport `docs/review/selarl_returns_006_dnc_001_report_v1.md`. Validations : tests DNC/front 94 passes, ruff cible OK. Ticket suivant ensuite traite : `SELARL-RETURNS-006-PV-001`.
- 2026-06-02 : PROJECT-BLOCKER-QUESTION-PROTOCOL-001 formalise la regle demandee par Gad : si un ticket bloque, les agents projet doivent verifier sources/specs/retours/code/tests, puis soit avancer avec une decision sourcee, soit poser une question concrete a Gad avec impact et action possible. Pointeurs mis a jour : `AGENTS.md`, `PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `PROJECT_CONTROL_TOWER_V1.md`, `PROJECT_AGENT_ORG_CHART_V1.md`, `COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`.
- 2026-06-02 : SELARL-RETURNS-006-PV-001 corrige `DOC-004` selon retours humains 006 : header avec forme juridique redigee pour SELARL et profession derivee des associes, remplacement de `Au capital minimum et effectif...` par `Au capital de ...`. Rapport `docs/review/selarl_returns_006_pv_001_report_v1.md`. Validations : tests PV 10 passes, tests front cibles 99 passes, ruff cible OK. Prochaine action : `SELARL-RETURNS-006-PROCURATION-001`.
- 2026-06-02 : SELARL-RETURNS-006-PROCURATION-001 corrige `DOC-003` selon retours humains 006 : phrase introductive `demeurant..., agissant...` sur une meme phrase avec `agissant` en minuscule, `de la {designation societe}`, siege sans ajout de `au`, adresses CP avant ville. Rapport `docs/review/selarl_returns_006_procuration_001_report_v1.md`. Validations : tests procuration 9 passes, tests front cibles 98 passes, ruff cible OK. Prochaine action : `SELARL-RETURNS-006-CONJOINT-LETTERS-001`.
- 2026-06-02 : SELARL-RETURNS-006-CONJOINT-LETTERS-001 corrige `DOC-005`/`DOC-006` selon retours humains 006 : forme sociale redigee dans la lettre d'avertissement, adresse conjoint derivee de l'adresse personnelle de l'associe/signataire, adresse conjoint retiree des exigences front/readiness, date sous la ville retiree de la renonciation. Rapport `docs/review/selarl_returns_006_conjoint_letters_001_report_v1.md`. Validations : tests regime 10 passes, tests front/regime 50 passes, non-regression SELARL 139 passes, ruff cible OK. Prochaine action : `SELARL-RETURNS-006-ORDRE-001`.
- 2026-06-02 : SELARL-RETURNS-006-ORDRE-001 corrige `DOC-034` selon retours humains 006 : le conseil departemental est compose depuis la profession et le departement d'inscription a l'Ordre ; le front SELARL ne demande plus le libelle complet visible comme source principale. Rapport `docs/review/selarl_returns_006_ordre_001_report_v1.md`. Validations : tests ordre/front 57 passes, regression SELARL large 165 passes, ruff cible OK. Prochaine action traitee : `SELARL-RETURNS-006-FRONT-VARIABLES-001`.
- 2026-06-02 : SELARL-RETURNS-006-FRONT-VARIABLES-001 simplifie les variables SELARL selon retours humains 006 : duree sociale forcee a 99 ans, quatre exemplaires par defaut, qualite renoncee associe, date courrier derivee du jour, nationalite portugaise ajoutee, checkbox siege social identique adresse personnelle. Rapport `docs/review/selarl_returns_006_front_variables_001_report_v1.md`. Validations : tests front 100 passes, regression SELARL large 165 passes, ruff cible OK. Prochaine action traitee : `SELARL-RETURNS-006-ADDRESS-SIGNATURE-001`.
- 2026-06-02 : SELARL-RETURNS-006-ADDRESS-SIGNATURE-001 applique les regles transversales retours humains 006 : normalisation CP avant ville dans les adresses front/moteur et suppression des encadres de signature restants sur le perimetre pack SELARL. Rapport `docs/review/selarl_returns_006_address_signature_001_report_v1.md`. Validations : tests adresses/signatures 37 passes, regression SELARL large 165 passes, ruff cible OK. Prochaine action alors traitee : `SELARL-CLOSING-PACK-005`.
- 2026-06-02 : SELARL-CLOSING-PACK-005 regenere le pack SELARL apres retours humains 006 dans `artifacts/selarl_closing_pack_005/`, avec 4 scenarios, 6/6/8/8 DOCX et manifest 0 echec. Rapport `docs/review/selarl_closing_pack_005_report_v1.md`. Deux ecarts detectes pendant audit ont ete corriges avant validation du rapport : `DOC-006` en quatre exemplaires et accord feminin `associee unique` dans les statuts dentiste. Validations : tests statuts/regime 25 passes, regression SELARL large 166 passes, ruff cible OK.
- 2026-06-02 : SELARL-HUMAN-RETURNS-DEEP-AUDIT-006 controle les retours humains 006 sur le pack 005 et produit une conclusion historique trop confiante. Rapport historique `docs/review/selarl_human_returns_deep_audit_006_report_v1.md`. Ce statut est amende le 2026-06-03 par `SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001`, qui trouve puis corrige `DOC-002`. Prochaine action : `SELARL-FINAL-ASSOCIE-VALIDATION-001` avec demande d'ecarts concrets document par document.
- 2026-06-02 : SELARL-RETURNS-006-CONJOINT-ADDRESS-FRONT-LOCK-001 corrige l'incident confirme par Gad/associe : l'adresse conjoint pouvait encore survivre dans des branches front/schema malgre la correction document `DOC-006`. Corrections : suppression des cles `conjoint_adresse_*` du clean front et de son prefill, discard legacy des anciennes cles, suppression de `conjoint_adresse` du formulaire simple historique, suppression de `adresse_conjoint` des exigences `DOC-006`, contrats front actifs alignes. Rapport `docs/review/selarl_returns_006_conjoint_address_front_lock_001_report_v1.md`. Validations : 6 tests anti-regression passes, ruff cible OK ; le paquet large affiche 107 passes puis des erreurs de permissions temporaires Windows sur les smokes `tmp_path`.
- 2026-06-03 : SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001 generalise les incidents associe sur les surfaces document/front/schema/tests/pack. Verdict : l'associe avait raison sur un deuxieme vrai manque, `DOC-002` affichait encore `pour une duree indeterminee`. Correction appliquee : autorisation de domiciliation rend `pour 99 ans`, test DOC-002 mis a jour, pack 005 regenere localement avec controle `doc002_duration_99_years=true`. Rapport `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`. Validations : regression SELARL ciblee 187 tests passes, ruff cible OK. Prochaine action : validation associe sur version candidate, demander seulement des ecarts concrets.
- 2026-06-03 : SELARL-RETURNS-007-SIGNATURE-DNC-001 traite les nouveaux retours associe. Signature : retour fonde, l'ancien correctif supprimait les bordures mais gardait une table invisible ; correction appliquee dans `add_simple_signature_block`, qui rend maintenant des paragraphes alignes a droite. DNC : non reproduit dans le pack 005 regenere, la ligne `Ne le 12/04/1984 a Paris.` est presente dans les 4 scenarios. Rapport `docs/review/selarl_associe_returns_007_signature_dnc_report_v1.md`. Validations : 23 tests Lot 1 passes, regression SELARL ciblee 187 tests passes, ruff OK. Prochaine action : transmettre/faire tester le pack 005 regenere ou pousser la correction si Gad le demande.
- 2026-06-03 : SELARL-RETURNS-008-MAIN-AUDIT-FIX-001 corrige les ecarts trouves sur `main` apres audit retours associe. Vrai ecart nouveau : le cas medecin marie sous separation de biens demandait insuffisamment l'identite conjoint et pouvait echouer a la generation des statuts ; il est maintenant generable, sans `DOC-005`/`DOC-006`, avec la phrase `separation de biens`. Correctifs associes : libelles medecin accentues dans les rendus et capital visible formate `1 000`. Rapport `docs/review/selarl_returns_008_main_audit_fix_report_v1.md`. Validations : ruff OK, py_compile OK, generation reelle 3 scenarios OK, audit DOCX 32 controles OK ; pytest bloque par permissions Windows sur les temporaires.
- 2026-06-02 : FRONT-INFORMATION-DEDUP-AGENT-001 formalise l'agent dedie a la non-redondance front : une information metier identique doit etre demandee une seule fois, puis reutilisee, derivee ou affichee en lecture seule. Livrable principal `docs/project/FRONT_INFORMATION_DEDUP_AGENT_PROTOCOL_V1.md`, raccorde a `PROJECT_AGENT_ORG_CHART_V1.md`, `PRODUCT_GUARDRAIL_PROTOCOL_V1.md`, `COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` et `AGENTS.md`.
- 2026-06-02 : NAOMIE-BRANCH-PUBLISH-001 publie directement sur `codex/naomie-selas-sprint` le protocole `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, le worklog `SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` et le routage d'accueil `AGENTS.md`; le fetch Git local reste bloque, mais la lecture/ecriture via connecteur GitHub est verifiee.
- 2026-06-02 : NAOMIE-REPORT-FRESHNESS-AUDIT-001 diagnostique le faux rapport Gad `Naomi au demarrage NotebookLM` : le worklog/journal etaient vides, mais le repo contient deja sources, catalogue, `DOC-018`, generateur, UI, tests et exemples SELAS. Correction : rapports Gad = audit de fraicheur obligatoire, `Fiabilite du suivi`, `Etat reel du type`, et interdiction de conclure `worklog vide = projet au debut`.
