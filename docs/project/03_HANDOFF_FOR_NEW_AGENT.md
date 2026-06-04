# Handoff pour nouvel agent

## Objet du projet
Le dépôt construit un moteur documentaire juridique déterministe pour DAAT x SYDEL. Le moteur doit produire des documents de dossier de manière reproductible, traçable et contrôlable, sans dépendre de la mémoire d'une conversation précédente.

## Source de vérité
- Source de vérité métier : `project/source_truth/Documents_a_generer_par_cas.docx`.
- Specs opérationnelles : `docs/delivery/`.
- Mémoire projet : `docs/project/`.
- ADR : `docs/adr/`.

L'arbre théorique abandonné n'est pas une source valide. Il n'existe pas de fichier séparé "Documents avec variables".

## Architecture retenue
- Le moteur est construit par document canonique.
- Le référentiel de départ est par cas métier, pour décider quels documents produire.
- Un orchestrateur dossier appelle les générateurs de documents canoniques.
- Chaque document automatisé a son générateur dédié.
- Les sorties cibles V1 sont DOCX, PDF et ZIP.
- L'interface cible est une Streamlit simple.
- Le moteur de production ne doit pas contenir de logique d'IA générative.

## Décisions déjà figées
- La source de vérité documentaire est `project/source_truth/Documents_a_generer_par_cas.docx`.
- Le moteur n'est pas construit par arbre de cas, mais par document canonique.
- Les documents marqués "à remplir à la main" restent hors automatisation initiale.
- Aucun document ne doit être codé sans source reçue, analyse et spec écrite.
- Les DOCX propres sont reconstruits de manière déterministe plutôt que nettoyés à la volée en production.
- Pour DOC-002 en V1, l'adresse de domiciliation est un champ libre : `domiciliation.adresse_domiciliation_affichee`.
- Codex est désormais pilote projet / produit principal dans le dépôt.
- Avant tout développement, appliquer `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md` et établir `GO dev` ou `NO-GO dev`.
- Avant tout nouveau sprint de type d'entreprise, appliquer `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`.
- Avant tout nouveau sprint de type d'entreprise, appliquer `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`.
- Avant tout nouveau sprint de type d'entreprise, appliquer aussi `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`.
- Quand un sprint existe, lire son fichier `docs/sprints/SPRINT_[TYPE]_V1.md` avant de repondre.
- Pour tout nouveau sprint, appliquer l'amendement SELARL 2026-06-01 du playbook :
  trois sources, questions humaines seulement si trou reel, pack actif, audit
  fidelite, retour associe par ecarts concrets, cloture `DONE/PARTIAL/BLOCKED`.
- La tour de controle projet est `docs/project/PROJECT_CONTROL_TOWER_V1.md` ;
  elle indique sprint actif, phase courante, action autorisee et actions
  interdites.
- La pyramide des agents est `docs/project/PROJECT_AGENT_ORG_CHART_V1.md` ;
  elle indique quel agent interroger, dans quel ordre, et ou trouver la preuve
  avant de repondre a Gad.
- L'agent de tracabilite de flux est
  `docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` ; il trace l'avancement
  d'un flux pilote sans demander au pilote humain de tenir le journal.
- Le protocole de synchronisation de flux est
  `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md` ; il s'applique quand
  une avancee est annoncee mais absente de la branche ou du worklog.
- Un nouveau chat doit d'abord identifier l'interlocuteur. Si le message est
  seulement `bonjour`, Codex doit demander `Bonjour, tu es Gad ou Naomi ?` et ne
  pas declencher de sprint avant la reponse.
- Le protocole runtime Naomi est `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md` ;
  il prime seulement si l'interlocutrice active est Naomi/Naomi, ou si Gad
  demande explicitement de preparer/simuler/reprendre son workflow operationnel.
- Le protocole d'orchestration du suivi Naomi est
  `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` ; il s'applique
  quand Gad demande ou en est Naomi, et il impose de lire les traces avant de
  demander quoi que ce soit a Naomi.
- La doctrine Naomi multi-projets est `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md`.
- La fin de sprint SELARL est suivie dans `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`.
- Un nouveau chat doit pouvoir reprendre le projet depuis `docs/project/04_LAST_STATE.md`, sans dépendre d'un chat externe.

## Ce qui est déjà fait
- Le dépôt de base existe.
- La mémoire projet est installée dans `docs/project/`.
- Les ADR principales existent dans `docs/adr/`.
- Le moteur documentaire a dépassé le Lot 1 initial : le catalogue, l'orchestrateur, les générateurs principaux, DOCX, ZIP et PDF best-effort existent.
- Le clean front Track B existe dans `src/sydel_doc_engine/front_app/`.
- La SELARL V1 limitée est générable pour création simple médecin / chirurgien-dentiste.
- Le régime communautaire SELARL génère `DOC-005` et `DOC-006`.
- Le multi-associés SELARL est disponible seulement en sous-cas limité : `DOC-004`, et `DOC-016` dentiste en PARTIAL.
- L'état SELARL courant se lit d'abord dans `docs/project/SELARL_CANONICAL_STATUS_V1.md`.
- La méthode de sprint par type d'entreprise est formalisée dans `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`.
- L'orchestrateur de sprint operationnel est formalise dans `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`.
- Le sprint SELAS est ouvert en `NO-GO dev` dans `docs/sprints/SPRINT_SELAS_V1.md`.
- La réutilisation SELARL/global est cadrée dans `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`.
- Le mode d'emploi d'installation et branche Naomi est `docs/project/NAOMIE_GITHUB_ONBOARDING_V1.md`.
- La couche pedagogique pour Naomi est `docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md`.
- Le gate produit / métier obligatoire est défini dans `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`.
- La tour de controle chef de projet est disponible dans `docs/project/PROJECT_CONTROL_TOWER_V1.md`.
- La pyramide agents / rattrapage est disponible dans `docs/project/PROJECT_AGENT_ORG_CHART_V1.md`.
- Le registre de statut des types d'entreprise est disponible dans
  `docs/project/COMPANY_TYPE_STATUS_REGISTRY_V1.md`.
- Clarification 2026-06-02 : seuls `SELARL` et `SELAS` sont en traitement
  metier. Les autres types presents dans le catalogue ou le moteur (`SPFPL
  cession`, `SPFPL apport`, `SCS`, `SCI`, `SCM`, `SAS`) sont des acquis
  techniques/historiques et ne doivent pas etre presentes comme sprints produit
  traites.
- La tracabilite de flux est disponible dans `docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md`.
- Le workflow global Gad / Naomi / Codex est disponible dans `docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md`.
- La fin de sprint SELARL est disponible dans `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`.

## Ce qui n'est pas encore fait
- La SELARL complète n'est pas juridiquement finalisée sur toutes ses variantes.
- Les types `SPFPL cession`, `SPFPL apport`, `SCS`, `SCI`, `SCM` et `SAS`
  n'ont pas encore ete traites comme sprints produit selon la methode actuelle
  source + NotebookLM + reuse audit + matrice + pack + retour humain.
- Les cessions cabinet, cession SCM, dérogations, site distinct, président externe, plusieurs gérants et statuts multi-associés complets restent à cadrer/arbitrer avant développement front complet.
- Le wording juridique ne doit pas être étendu ou modifié sans validation explicite.
- Chaque prochain développement doit passer par le gate `GO dev` / `NO-GO dev`.

## Ordre de lecture des fichiers
Avant toute proposition ou implémentation, lire dans cet ordre :

1. `AGENTS.md`
2. `docs/project/00_MASTER_PLAN.md`
3. `docs/project/01_EXECUTION_BOARD.md`
4. `docs/project/02_CODEX_WORKFLOW.md`
5. `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
6. `docs/project/04_LAST_STATE.md`
7. `docs/project/PROJECT_CONTROL_TOWER_V1.md`
8. `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md` si l'interlocutrice active est Naomi/Naomi, ou si Gad demande explicitement le workflow Naomi/SELAS
9. `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` si Gad demande le statut ou le suivi de Naomi
10. `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` pour tout sprint de type d'entreprise
11. `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` pour tout sprint de type d'entreprise
12. `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md` pour tout sprint de type d'entreprise
13. `docs/sprints/SPRINT_[TYPE]_V1.md` si le sprint existe
14. `docs/project/SELARL_CANONICAL_STATUS_V1.md` pour toute reprise SELARL
15. `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`
16. Le fichier de spec concerné dans `docs/delivery/`
17. Les ADR applicables dans `docs/adr/`

Note : si la demande concerne une chaine d'agents, un statut transverse, une
orchestration descendante ou un rattrapage retroactif, lire aussi
`docs/project/PROJECT_AGENT_ORG_CHART_V1.md` juste apres la tour de controle.
Si la demande concerne un rapport boss sur un flux pilote, lire aussi
`docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md`.
Si la demande concerne une avancee annoncee mais absente des traces publiees,
lire aussi `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md`.

Note : pour un workflow Naomi global, lire aussi
`docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md` et
`docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`, puis
`docs/project/PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md`. Pour la cloture SELARL,
lire aussi `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`.

## Travail avec Codex pilote projet / produit
- Codex cadre les tickets, reformule l'intention métier, arbitre le passage en `GO dev` ou `NO-GO dev` et explicite les décisions métier à documenter.
- Codex doit d'abord consulter la tour de controle projet pour connaitre sprint actif, phase, action autorisee et actions interdites.
- Si Gad demande qui orchestre quoi, ou si un suivi est stale, Codex doit
  consulter `PROJECT_AGENT_ORG_CHART_V1.md` et activer l'agent specialise
  indique, notamment l'Agent de tracabilite de flux si les traces anciennes
  manquent.
- Si Gad s'identifie, Codex le traite comme superviseur produit et decisionnaire :
  il applique la tour de controle, donne l'etat utile et ne declenche pas
  NotebookLM seulement parce que Gad parle de Naomi.
- Si Gad demande ou en est Naomi, Codex applique l'orchestrateur Naomi :
  lecture tour de controle, dernier etat, sprint, worklog, journal et branche
  accessible avant toute demande a Naomi.
- Si Gad annonce que Naomi a avance mais que la branche/worklog ne montrent pas
  cette avancee, Codex ne relance pas le travail metier : il demande un Sync
  checkpoint, commit/push ou Sync packet.
- Le rapport Gad par defaut doit porter sur le flux Naomi et rester court :
  statut, avancement, prochaine etape, blocage/risque, fiabilite.
- Si Naomi démarre un sprint, elle doit s'identifier et Codex doit la guider étape par étape selon `SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` et `COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`.
- Pour le sprint SELAS, l'etat immediat est `docs/sprints/SPRINT_SELAS_V1.md` : `NO-GO dev`, sous-sprint NotebookLM actif, prochaine action = donner a Naomi le prompt NotebookLM courant a copier-coller.
- Si Naomi dit seulement `bonjour` apres identification comme Naomi, Codex doit quand meme donner le Prompt NotebookLM 01 et ne pas attendre qu'elle choisisse une tache.
- Si Naomi dit qu'elle veut lancer/demarrer/reprendre le sprint SELAS/CELAS, Codex doit comprendre `lancer = lancer le sous-sprint NotebookLM`, et ne doit pas passer en production, generation, audit, matrice ou code.
- Pour la SELARL, la prochaine action de cloture est `SELARL-FINAL-ASSOCIE-VALIDATION-001` sur le pack corrige `artifacts/selarl_closing_pack_005/`, selon `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`.
- Si Naomi travaille sur un nouveau type d'entreprise, elle doit partir d'une branche dediee selon `NAOMIE_GITHUB_ONBOARDING_V1.md`, mais Codex gere Git, les commandes, les tests et les checkpoints pour elle.
- Si Naomi pose une question d'apprentissage, utiliser le mode `Professeur Naomi` defini dans `NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md`.
- Le sous-agent prioritaire pour un nouveau sprint est `Reuse Auditor`, défini dans `REUSE_AUDIT_AGENT_PROTOCOL_V1.md`.
- Codex peut utiliser des sous-agents spécialisés pour auditer le produit, les sources, le front, le moteur ou la QA, mais reste responsable de la synthèse et de l'intégration.
- Codex ne modifie pas le wording juridique sans instruction explicite et validation tracée.
- Codex met à jour `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md` à la fin de chaque ticket.
- En cas d'ambiguïté métier, Codex bloque l'implémentation concernée et documente la décision requise.
- Les PR doivent rester petites, traçables et centrées sur un seul document métier sauf demande explicite.
