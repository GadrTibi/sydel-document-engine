# Mode opératoire Codex

## Lecture obligatoire avant tout ticket
1. AGENTS.md
2. docs/project/00_MASTER_PLAN.md
3. docs/project/01_EXECUTION_BOARD.md
4. docs/project/02_CODEX_WORKFLOW.md
5. docs/project/03_HANDOFF_FOR_NEW_AGENT.md
6. docs/project/04_LAST_STATE.md
7. docs/project/PROJECT_CONTROL_TOWER_V1.md
8. docs/project/PROJECT_AGENT_ORG_CHART_V1.md si le ticket concerne la chaine d'agents, un statut transverse ou un rattrapage retroactif
9. docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md si le ticket concerne la tracabilite d'un flux pilote ou un rapport boss
10. docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md si le ticket concerne une avancee annoncee mais absente de la branche/worklog ou une sync inter-threads
11. docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md si l'interlocutrice active est Naomi/Naomi, ou si Gad demande explicitement le workflow Naomi/SELAS
12. docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md si le ticket formalise un workflow Naomi multi-projets
13. docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md si Gad demande le statut ou le suivi de Naomi
14. docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md si le ticket ouvre ou suit un sprint de type d'entreprise
15. docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md si le ticket ouvre ou suit un sprint de type d'entreprise
16. docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md si le ticket ouvre ou suit un sprint de type d'entreprise
16. docs/sprints/SPRINT_[TYPE]_V1.md si le sprint existe
17. docs/project/SELARL_CANONICAL_STATUS_V1.md si le ticket touche la SELARL
18. docs/sprints/SPRINT_SELARL_CLOSING_V1.md si le ticket touche la cloture SELARL
19. docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md
20. le document de spec concerné

Pour un ticket documentaire, vérifier aussi l'ADR applicable dans `docs/adr/` avant d'écrire du code.

## Gate produit / métier avant développement

Avant de coder, Codex doit appliquer `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`.
Avant meme de choisir une action, Codex doit appliquer
`docs/project/PROJECT_CONTROL_TOWER_V1.md` pour identifier le sprint actif, la
phase courante, l'action autorisee et les actions interdites.

Si la demande porte sur la chaine d'agents, l'orchestration descendante, un
statut transverse ou un suivi stale a reconstruire, Codex doit appliquer aussi
`docs/project/PROJECT_AGENT_ORG_CHART_V1.md`.

Si la demande porte sur le statut d'un flux pilote, par exemple `ou en est
Naomi ?`, Codex doit appliquer
`docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` et repondre par defaut en
rapport boss court.

Si Gad annonce une avancee du flux que la branche ou le worklog ne montrent pas,
Codex doit appliquer `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md`.
Le statut devient `avancee annoncee, synchronisation manquante` jusqu'a commit
pousse ou Sync packet.

Au debut d'un nouveau chat, si l'interlocuteur n'est pas identifie et dit
seulement `bonjour`, `salut`, `ca va` ou une reprise vague, Codex doit demander
`Bonjour, tu es Gad ou Naomi ? Je te route ensuite sur le bon protocole projet.`
Il ne doit pas lancer NotebookLM, demander une tache ou inferer un sprint avant
cette identification.

Si l'interlocuteur est Gad, Codex le traite comme superviseur produit et
decisionnaire. Mentionner Naomi, Naomi, SELAS ou le protocole d'accueil dans
une question de Gad ne declenche pas automatiquement le runtime Naomi.

Si Gad demande `ou en est Naomi ?`, `que fait Naomi ?` ou un statut equivalent,
Codex doit appliquer `docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`
et lire les traces disponibles : tour de controle, dernier etat, fichier de
sprint, worklog Naomi, journal de base de connaissance, branche Naomi si
accessible. Il ne demande pas a Naomi un statut oral sauf blocage explicite.
Le rapport doit porter sur le flux Naomi, pas sur une evaluation personnelle.
Si ces traces sont stale, Codex active l'Agent de tracabilite de flux et son
mode de rattrapage retroactif.
Pour un nouveau type d'entreprise, Codex doit aussi appliquer
`docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`,
`docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` et
`docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`.

Si un fichier `docs/sprints/SPRINT_[TYPE]_V1.md` existe, il devient l'etat
operationnel du sprint. Si Naomi ou Gad ouvre un sprint et que ce fichier
n'existe pas, Codex doit le creer en phase 0 avec `NO-GO dev` avant toute autre
action.

Le ticket ne peut passer en implémentation que si le besoin métier est reformulé,
les sources et specs applicables sont identifiées, les documents inclus/exclus
sont listés, les réserves/manuels sont protégés et la décision `GO dev` est
explicite.

Si une demande utilisateur est encore une intention métier non stabilisée, Codex
doit produire ou mettre à jour un cadrage fonctionnel avant toute modification de
code. Le bon résultat peut donc être `NO-GO dev` avec arbitrage documenté.

Quand la tâche est large, Codex peut déléguer à des sous-agents spécialisés
produit, source, front, moteur ou QA. Le pilote principal reste responsable de
l'intégration et de la décision finale.

Pour un sprint de type d'entreprise, le sous-agent prioritaire est
`Reuse Auditor` : il compare le besoin au travail déjà fait côté SELARL et aux
registres globaux avant tout `GO dev`.

Si le sprint est pilote par Naomi, verifier aussi
`docs/project/NAOMIE_GITHUB_ONBOARDING_V1.md` avant toute consigne Git ou setup
local. Naomi ne doit pas executer les commandes Git elle-meme ; Codex gere ces
operations dans le terminal du projet.

Si l'interlocutrice active est Naomi/Naomi et que le message est seulement
`Bonjour`, Codex doit traiter le message comme un accueil de sprint, pas comme
une demande generique. Il doit lire `docs/sprints/SPRINT_SELAS_V1.md`, verifier
la branche `codex/naomie-selas-sprint`, repondre avec `Statut sprint`,
`Action maintenant`, `Point pedagogie`, `Prochaine etape`, donner le Prompt
NotebookLM 01 complet, et rester en `NO-GO dev`. Le protocole court prioritaire
est `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`.

Pour le sprint SELAS, Codex doit ensuite donner un prompt court depuis
`docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md`. Quand Naomi colle une
reponse NotebookLM, Codex doit la structurer dans
`docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` avant de poser le prompt
suivant. Il ne doit pas demander vaguement une "source NotebookLM SELAS" sans
donner le prompt exact a utiliser.

Si Naomi dit `je veux lancer le sprint SELAS`, `je veux demarrer le sprint
SELAS`, `je reprends le sprint SELAS`, ou une variante phonetique `CELAS`,
Codex doit comprendre : `lancer = lancer le sous-sprint NotebookLM`. La seule
action utilisateur demandee a Naomi est alors de copier-coller le prompt
NotebookLM courant, puis de rapporter la reponse brute. Codex ne doit pas
passer en production, generation, matrice, audit de reutilisation ou code avant
que le journal NotebookLM soit suffisamment rempli.

Si Naomi pose une question d'apprentissage, appliquer
`docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md`. Le mode professeur explique
mais ne vaut jamais `GO dev`.

Pour un workflow Naomi non specifique a SYDEL, appliquer
`docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md`, appliquer
`docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` pour le suivi, puis
creer un protocole local a partir de
`docs/project/PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md`.

Pour la fin de sprint SELARL, appliquer
`docs/sprints/SPRINT_SELARL_CLOSING_V1.md`. La prochaine action propre courante
est `SELARL-FINAL-ASSOCIE-VALIDATION-001`, maintenant que le pack corrige
`artifacts/selarl_closing_pack_005/` est regenere et audite cote Codex.
Ce n'est pas un developpement complexe.

Pour tout nouveau type d'entreprise, appliquer aussi l'amendement SELARL
2026-06-01 du playbook : trianguler document de reference, NotebookLM/modele et
retours humains ; ne poser aucune question humaine deja resolue par les sources ;
identifier le pack actif ; demander a l'associe des ecarts concrets seulement ;
clore en `DONE`, `PARTIAL` ou `BLOCKED`.

## Choix du périmètre
- Identifier le ticket exact dans `docs/project/01_EXECUTION_BOARD.md`.
- Vérifier le statut du ticket avant de commencer.
- Ne travailler que sur le document ou le composant explicitement demandé.
- Ne pas embarquer de refactor opportuniste.
- Si le ticket implique un document canonique, ne pas toucher un autre document métier dans la même tâche.

Avant de coder, Codex doit appliquer `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`.
Avant meme de choisir une action, Codex doit appliquer
`docs/project/PROJECT_CONTROL_TOWER_V1.md` pour identifier le sprint actif, la
phase courante, l'action autorisee et les actions interdites.
Pour un nouveau type d'entreprise, Codex doit aussi appliquer
`docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`,
`docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` et
`docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`.

Si un fichier `docs/sprints/SPRINT_[TYPE]_V1.md` existe, il devient l'etat
operationnel du sprint. Si Naomi ou Gad ouvre un sprint et que ce fichier
n'existe pas, Codex doit le creer en phase 0 avec `NO-GO dev` avant toute autre
action.

Le ticket ne peut passer en implémentation que si le besoin métier est reformulé,
les sources et specs applicables sont identifiées, les documents inclus/exclus
sont listés, les réserves/manuels sont protégés et la décision `GO dev` est
explicite.

Si une demande utilisateur est encore une intention métier non stabilisée, Codex
doit produire ou mettre à jour un cadrage fonctionnel avant toute modification de
code. Le bon résultat peut donc être `NO-GO dev` avec arbitrage documenté.

Quand la tâche est large, Codex peut déléguer à des sous-agents spécialisés
produit, source, front, moteur ou QA. Le pilote principal reste responsable de
l'intégration et de la décision finale.

Pour un sprint de type d'entreprise, le sous-agent prioritaire est
`Reuse Auditor` : il compare le besoin au travail déjà fait côté SELARL et aux
registres globaux avant tout `GO dev`.

Si le sprint est pilote par Naomi, verifier aussi
`docs/project/NAOMIE_GITHUB_ONBOARDING_V1.md` avant toute consigne Git ou setup
local. Naomi ne doit pas executer les commandes Git elle-meme ; Codex gere ces
operations dans le terminal du projet.

Si le contexte indique Naomi/Naomi et que le message est seulement `Bonjour`,
Codex doit traiter le message comme un accueil de sprint, pas comme une demande
generique. Il doit lire `docs/sprints/SPRINT_SELAS_V1.md`, verifier la branche
`codex/naomie-selas-sprint`, repondre avec `Statut sprint`, `Action maintenant`,
`Point pedagogie`, `Prochaine etape`, donner le Prompt NotebookLM 01 complet, et
rester en `NO-GO dev`. Le protocole court prioritaire est
`docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`.

Pour le sprint SELAS, Codex doit ensuite donner un prompt court depuis
`docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md`. Quand Naomi colle une
reponse NotebookLM, Codex doit la structurer dans
`docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` avant de poser le prompt
suivant. Il ne doit pas demander vaguement une "source NotebookLM SELAS" sans
donner le prompt exact a utiliser.

Si Naomi dit `je veux lancer le sprint SELAS`, `je veux demarrer le sprint
SELAS`, `je reprends le sprint SELAS`, ou une variante phonetique `CELAS`,
Codex doit comprendre : `lancer = lancer le sous-sprint NotebookLM`. La seule
action utilisateur demandee a Naomi est alors de copier-coller le prompt
NotebookLM courant, puis de rapporter la reponse brute. Codex ne doit pas
passer en production, generation, matrice, audit de reutilisation ou code avant
que le journal NotebookLM soit suffisamment rempli.

Si Naomi pose une question d'apprentissage, appliquer
`docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md`. Le mode professeur explique
mais ne vaut jamais `GO dev`.

Pour un workflow Naomi non specifique a SYDEL, appliquer
`docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md` puis creer un protocole
local a partir de `docs/project/PROJECT_NAOMIE_RUNTIME_TEMPLATE_V1.md`.

Pour la fin de sprint SELARL, appliquer
`docs/sprints/SPRINT_SELARL_CLOSING_V1.md`. La prochaine action propre est
`SELARL-CLOSING-PACK-001`, pas un developpement complexe.

## Choix du périmètre
- Identifier le ticket exact dans `docs/project/01_EXECUTION_BOARD.md`.
- Vérifier le statut du ticket avant de commencer.
- Ne travailler que sur le document ou le composant explicitement demandé.
- Ne pas embarquer de refactor opportuniste.
- Si le ticket implique un document canonique, ne pas toucher un autre document métier dans la même tâche.

## Pipeline documentaire à respecter
Un document ne peut être codé que si le cycle suivant est satisfait :

`Inventorié -> Validé -> Source reçue -> Analysé -> Spécifié -> Codé -> Testé -> Validé`

Avant le passage en code, vérifier au minimum :
- source reçue ;
- spec écrite ;
- variables listées ;
- règles de génération décrites ;
- critères de recette présents ;
- décisions métier sensibles explicites.

## Règles d'exécution
- faire un changement petit et ciblé
- ne pas modifier implicitement le texte juridique
- s'appuyer sur les documents source et les specs
- conserver les conventions du repo
- ajouter ou mettre à jour les tests utiles
- exécuter les validations locales avant clôture

## Validations minimales
- .\.venv\Scripts\python.exe -m ruff check .
- .\.venv\Scripts\python.exe -m pytest

Pour une tâche de documentation pure, les validations de code peuvent être remplacées par :
- relecture du diff
- vérification que le scope ne touche pas au code métier Python
- vérification que le tableau d'exécution indique la prochaine étape

Pour un ticket documentaire codé, ajouter des validations ciblées :
- tests du générateur concerné ;
- tests des helpers transverses modifiés ;
- vérification que les sorties ne contiennent pas de placeholder résiduel ;
- vérification que les accords et conditions décrits dans la spec sont couverts.

## Mise à jour documentaire obligatoire en fin de ticket
Mettre à jour :
- docs/project/01_EXECUTION_BOARD.md
- docs/project/04_LAST_STATE.md
- docs/delivery/work_status.md si nécessaire

La mise à jour doit documenter :
- ce qui vient d'être fait
- le prochain ticket recommandé
- les hypothèses ou décisions métier ouvertes
- toute dérive volontaire de wording juridique, si elle a été explicitement demandée

`docs/project/04_LAST_STATE.md` doit toujours refléter l'état immédiatement reprenable du projet : dernier ticket terminé, état du repo, prochain ticket, points ouverts, validations connues et recommandation immédiate.

## Format attendu du compte-rendu Codex
- Fait
- Fichiers modifiés
- Tests exécutés
- Résultat des tests
- Prochaine étape recommandée
- Questions ouvertes éventuelles

Le compte-rendu doit aussi signaler explicitement :
- tout fichier non touché volontairement alors qu'il semblait proche du sujet ;
- toute hypothèse métier ;
- toute impossibilité de lancer une validation ;
- toute modification de wording juridique, uniquement si elle a été demandée par la spec ou le ticket.

## Règles de clôture
- Le diff doit rester lisible et limité.
- Le tableau d'exécution doit indiquer le prochain ticket.
- Les fichiers temporaires ou artefacts accidentels doivent être supprimés s'ils ne servent pas le projet.
- Aucun commit, push ou PR ne doit être fait sauf demande explicite.
- En cas de doute métier, documenter le point ouvert au lieu d'inventer une règle.

## Prompt standard à utiliser avec Codex
Lis d'abord :
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
- docs/project/GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md si le ticket concerne un workflow Naomi global
- docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md si Gad demande le statut ou le suivi de Naomi
- docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md si le ticket ouvre ou suit un sprint de type d'entreprise
- docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md si le ticket ouvre ou suit un sprint de type d'entreprise
- docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md si le ticket ouvre ou suit un sprint de type d'entreprise
- docs/sprints/SPRINT_[TYPE]_V1.md si le sprint existe
- docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md si Naomi pose une question d'apprentissage
- docs/project/SELARL_CANONICAL_STATUS_V1.md si le ticket touche la SELARL
- docs/sprints/SPRINT_SELARL_CLOSING_V1.md si le ticket touche la cloture SELARL
- docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md
- le fichier de spec visé

Ensuite :
- applique le gate produit / métier et annonce `GO dev` ou `NO-GO dev`
- implémente le ticket demandé avec un scope minimal et propre
- ne modifie pas le texte juridique hors besoins explicitement spécifiés
- ajoute ou mets à jour les tests nécessaires
- exécute ruff et pytest
- mets à jour docs/project/01_EXECUTION_BOARD.md et docs/project/04_LAST_STATE.md avec le statut, ce qui a été fait et la prochaine étape
