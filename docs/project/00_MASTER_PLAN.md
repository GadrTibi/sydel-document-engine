# Plan maître — SYDEL Document Engine

## Objet
Construire un moteur documentaire juridique déterministe pour DAAT x SYDEL, versionné dans le dépôt et exploitable sans dépendre de la mémoire du chat.

Ce fichier fixe la mémoire opérationnelle globale : il doit permettre à un nouvel intervenant de comprendre ce qui est construit, dans quel ordre, avec quelles sources et avec quels garde-fous.

## Périmètre V1
- Génération DOCX propre.
- Conversion PDF.
- Constitution d'un ZIP dossier.
- Interface Streamlit simple pour piloter une génération dossier.
- Lot 1 uniquement au démarrage.
- Pas d'IA générative dans le moteur de production.
- Pas d'automatisation initiale des documents marqués "à remplir à la main".

## Source de vérité
- Source de vérité métier : `project/source_truth/Documents_a_generer_par_cas.docx`.
- Sources documentaires Lot 1 : `project/source_documents/lot_01/*`.
- Specs de livraison : `docs/delivery/`.
- L'arbre théorique abandonné n'est pas une source valide.
- Il n'existe pas de fichier séparé "Documents avec variables".

Clarification 2026-06-02 : `Documents_a_generer_par_cas.docx` reste la source
de reference pour l'inventaire documentaire, mais elle ne suffit pas a declarer
un type d'entreprise `traite`. Un sprint produit par type exige aussi la
triangulation NotebookLM/modele, les retours humains disponibles, un audit de
reutilisation, une matrice documentaire et un statut canonique.

## Architecture retenue
- Le moteur est construit par document canonique, pas par cas métier.
- Le référentiel de départ reste par cas métier pour décider quels documents produire.
- L'orchestrateur dossier appelle les générateurs de documents canoniques selon le contexte.
- Chaque document automatisé dispose d'un générateur dédié.
- Les conditions générales et spécifiques sont explicites et testables.
- La génération DOCX cible des fichiers propres, reconstruits de manière déterministe.
- Les sorties cibles V1 sont : DOCX, PDF, ZIP.
- L'interface cible est une Streamlit simple, sans logique métier cachée dans l'UI.

## ADR applicables
- `docs/adr/0001-source-of-truth.md` : la source de vérité documentaire est le document Word métier.
- `docs/adr/0002-engine-per-document.md` : le moteur se construit par document canonique.
- `docs/adr/0003-lot-based-delivery.md` : la livraison se fait par lots documentaires.
- `docs/adr/0004-from-scratch-docx-generation.md` : les DOCX propres sont reconstruits plutôt que nettoyés en production.
- `docs/adr/0005-codex-working-mode.md` : le travail Codex doit rester repo-first, traçable et limité.

## Règles de travail
- ne pas coder un document sans source + analyse + spec
- appliquer le gate produit / métier `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md` avant tout développement
- qualifier explicitement une demande en `GO dev` ou `NO-GO dev`
- ne pas réécrire implicitement un texte juridique
- travailler par petits tickets traçables
- documenter ce qui est fait et ce qui vient après
- garder l'Excel comme pilotage humain
- garder le Markdown du repo comme mémoire opérationnelle

## Phases
1. bootstrap technique du repo
2. mémoire projet versionnée dans le repo
3. implémentation Lot 1
4. orchestrateur Lot 1
5. Streamlit V0 Lot 1
6. lots documentaires suivants

## Etat actuel
- moteur documentaire DOCX V1 avancé avec catalogue et générateurs principaux versionnés ;
- sorties DOCX, ZIP et PDF best-effort intégrées côté moteur/runtime ;
- clean front Track B disponible dans `src/sydel_doc_engine/front_app/` ;
- etat SELARL courant consolide dans `docs/project/SELARL_CANONICAL_STATUS_V1.md` ;
- tour de controle projet disponible dans `docs/project/PROJECT_CONTROL_TOWER_V1.md` ;
- pyramide des agents et chaine d'escalade disponible dans
  `docs/project/PROJECT_AGENT_ORG_CHART_V1.md` ;
- registre de statut des types d'entreprise disponible dans
  `docs/project/COMPANY_TYPE_STATUS_REGISTRY_V1.md` : seuls SELARL et SELAS
  sont en traitement metier ; SPFPL, SCS, SCI, SCM et SAS sont inventories /
  cables historiquement mais non traites en sprint produit ;
- protocole de tracabilite de flux disponible dans
  `docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` ;
- protocole de synchronisation de flux disponible dans
  `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md` ;
- protocole runtime Naomi disponible dans `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md` ;
- protocole global Gad/Naomi/Codex disponible dans `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md` ;
- template runtime Naomi multi-projets disponible dans `docs/project/PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md` ;
- protocole d'orchestration du suivi Naomi disponible dans
  `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` ;
- protocole sprint par type d'entreprise disponible dans `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` ;
- orchestrateur de sprint operationnel disponible dans `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` ;
- sprint SELAS ouvert en `NO-GO dev` dans `docs/sprints/SPRINT_SELAS_V1.md` ;
- sous-sprint NotebookLM SELAS actif : Naomi doit recevoir un prompt court,
  le coller dans NotebookLM, puis donner la reponse brute a Codex pour
  structuration et iteration ;
- worklog Naomi SELAS disponible dans
  `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` pour repondre a Gad depuis
  les traces ;
- protocole de reutilisation SELARL/global disponible dans `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md` ;
- methode SELARL capitalisee pour tous les types d'entreprise : trois sources,
  questions humaines seulement sur trous reels, pack actif, audit fidelite et
  cloture `DONE/PARTIAL/BLOCKED` dans `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` ;
- mode d'emploi branche / installation Naomi disponible dans `docs/project/NAOMIE_GITHUB_ONBOARDING_V1.md` ;
- couche pedagogique Naomi disponible dans `docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md` ;
- SELARL V1 de production limitée disponible pour création simple médecin / chirurgien-dentiste ;
- fin de sprint SELARL structuree dans `docs/sprints/SPRINT_SELARL_CLOSING_V1.md` ;
- régime communautaire SELARL : `DOC-005` et `DOC-006` générés quand l'option est active ;
- multi-associés SELARL : `DOC-004` limité implémenté, `DOC-016` dentiste multi-associés en PARTIAL ;
- cession, SCM, dérogations, site distinct, plusieurs gérants et statuts multi-associés complets restent à cadrer/arbitrer avant extension ;
- gate produit / métier obligatoire installé dans `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`.

## Lot 1 historique
- DOC-001 : Déclaration sur l'honneur de non-condamnation
- DOC-002 : Autorisation de domiciliation
- DOC-003 : Procuration

Le Lot 1 n'est plus le prochain chantier : il constitue le socle documentaire
historique déjà implémenté. L'état opérationnel courant se lit dans
`docs/project/04_LAST_STATE.md`.

## Entrées nécessaires avant codage d'un document
- Le document doit être inventorié dans la source de vérité.
- La source documentaire correspondante doit être reçue.
- Une analyse et une spec doivent exister dans `docs/delivery/`.
- Les variables obligatoires doivent être listées.
- Les règles de génération et critères de recette doivent être écrits.
- Les décisions sensibles doivent être explicites avant implémentation.

## Sorties attendues par document codé
- Un générateur déterministe dédié au document canonique.
- Des validations d'entrée claires pour les champs obligatoires.
- Un DOCX propre, sans artefact de transformation.
- Des tests couvrant les règles documentaires spécifiées.
- Une mise à jour du tableau d'exécution.
- Aucune modification implicite du wording juridique.

## Décision temporaire V1
Pour DOC-002, l'adresse de domiciliation est gérée en champ libre :
- adresse_domiciliation_libre

## Ordre d'exécution immédiat
1. si un nouveau chat commence par `bonjour` ou une reprise vague sans identite, demander d'abord `Bonjour, tu es Gad ou Naomi ?` ;
2. lire `docs/project/04_LAST_STATE.md` pour l'état réellement reprenable ;
3. lire `docs/project/PROJECT_CONTROL_TOWER_V1.md` pour identifier sprint actif, phase et action autorisee ;
4. lire `docs/project/PROJECT_AGENT_ORG_CHART_V1.md` si la demande concerne la chaine d'agents, un statut transverse ou un rattrapage retroactif ;
5. lire `docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` si Gad demande un rapport boss sur un flux pilote ;
6. lire `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md` si Gad annonce une avancee absente de la branche ou du worklog ;
7. si l'interlocutrice active est Naomi/Naomi, appliquer `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md` et donner le Prompt NotebookLM 01 ;
8. si l'interlocuteur est Gad, le traiter comme superviseur produit et ne pas declencher NotebookLM seulement parce qu'il parle de Naomi ;
9. si Gad demande ou en est Naomi, appliquer `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` et repondre par defaut sur le flux Naomi, format boss court ;
10. si le suivi est stale, activer l'Agent de tracabilite de flux et son mode rattrapage retroactif ;
11. pour tout nouveau type d'entreprise, lire `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` ;
12. pour tout nouveau type d'entreprise, lire `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` ;
13. pour tout nouveau type d'entreprise, lire le fichier actif `docs/sprints/SPRINT_[TYPE]_V1.md` s'il existe ;
14. si le sprint est pilote par Naomi, lancer d'abord le sous-sprint NotebookLM par prompts courts et attendre les reponses structurees ;
15. pour tout nouveau type d'entreprise, appliquer ensuite `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md` ;
16. pour toute demande SELARL, lire `docs/project/SELARL_CANONICAL_STATUS_V1.md` ;
17. pour cloturer la SELARL, lire `docs/sprints/SPRINT_SELARL_CLOSING_V1.md` ;
18. appliquer `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md` ;
19. qualifier la demande en `GO dev` ou `NO-GO dev` ;
19. si `GO dev`, limiter l'implémentation au ticket cadré ;
20. si `NO-GO dev`, produire ou mettre à jour le cadrage fonctionnel requis.

## Documents que Codex doit lire avant toute implémentation
- AGENTS.md
- docs/project/00_MASTER_PLAN.md
- docs/project/01_EXECUTION_BOARD.md
- docs/project/02_CODEX_WORKFLOW.md
- docs/project/03_HANDOFF_FOR_NEW_AGENT.md
- docs/project/04_LAST_STATE.md
- docs/project/PROJECT_CONTROL_TOWER_V1.md
- docs/project/PROJECT_AGENT_ORG_CHART_V1.md si le ticket concerne la chaine d'agents, un statut transverse ou un rattrapage retroactif
- docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md si le ticket concerne la tracabilite d'un flux pilote ou un rapport boss
- docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md si le ticket concerne une avancee annoncee mais absente de la branche/worklog
- docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md si l'interlocutrice active est Naomi/Naomi, ou si Gad demande explicitement le workflow Naomi/SELAS
- docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md pour les workflows multi-projets avec Naomi
- docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md si Gad demande le statut ou le suivi de Naomi
- docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md pour tout sprint de type d'entreprise
- docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md
- docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md pour tout sprint de type d'entreprise
- docs/sprints/SPRINT_[TYPE]_V1.md si le sprint existe
- docs/project/SELARL_CANONICAL_STATUS_V1.md pour toute reprise SELARL
- docs/sprints/SPRINT_SELARL_CLOSING_V1.md pour toute cloture SELARL
- docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md
- le fichier de spec ou de livraison concerné dans docs/delivery/

## Garde-fous permanents
- Ne pas introduire d'IA générative dans le moteur de production.
- Ne pas automatiser un document marqué "à remplir à la main" sans décision explicite.
- Ne pas faire dériver le texte juridique ; en cas d'ambiguïté, bloquer et documenter la décision requise.
- Ne pas toucher plusieurs documents métier dans une même PR sauf ticket explicite.
- Toujours documenter ce qui est fait et ce qui vient après.
