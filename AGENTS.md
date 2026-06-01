# AGENTS.md

Ce dépôt sert à construire un moteur documentaire juridique **déterministe** pour DAAT x SYDEL.

## Mission de l'agent

Tu interviens comme agent de développement dans un cadre très contraint.

Tu peux :

- structurer le dépôt ;
- écrire du code Python ;
- écrire des tests ;
- améliorer la documentation technique ;
- proposer des refactors sûrs ;
- préparer des PR propres et limitées.

Tu ne dois pas :

- réinventer l'architecture métier ;
- modifier la source de vérité sans décision explicite ;
- coder un document sans respecter le pipeline documentaire ;
- introduire de logique d'IA générative dans le moteur de production ;
- modifier des formulations juridiques sans les signaler explicitement.

## Source de vérité métier

Le document de référence est :

- `project/source_truth/Documents_a_generer_par_cas.docx`

L'arbre théorique abandonné n'est pas une source valide.
Il n'existe pas de fichier séparé « Documents avec variables ».

## Principes d'architecture non négociables

1. Le moteur se construit **par document canonique**.
2. Le référentiel de départ est **par cas métier**.
3. L'orchestrateur appelle les bons générateurs selon le contexte dossier.
4. Les documents marqués « à remplir à la main » restent hors automatisation initiale.
5. Toute génération doit pouvoir sortir un DOCX propre, puis PDF, puis ZIP dossier.

## Pipeline documentaire obligatoire

Aucun document ne doit passer en implémentation sans ce cycle :

`Inventorié → Validé → Source reçue → Analysé → Spécifié → Codé → Testé → Validé`

Concrètement :

- pas de code documentaire sans source reçue ;
- pas de code documentaire sans spec écrite ;
- pas de merge sans test ;
- pas de changement de wording sans note de validation.

## Mode de travail attendu

### Déclencheur immédiat Naomie / Bonjour

Si le contexte indique que l'utilisatrice est Naomie/Naomi, même si son premier
message est seulement `Bonjour`, Codex ne doit jamais répondre de manière
générique du type "qu'est-ce qu'on attaque dans le moteur documentaire ?".

Réaction obligatoire :

1. appliquer `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` ;
2. lire `docs/sprints/SPRINT_SELAS_V1.md` ;
3. lire `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_PROMPTS_V1.md` ;
4. vérifier que la branche cible est `codex/naomie-selas-sprint` ou s'y placer ;
5. répondre en phase 0 `ACCUEIL / NO-GO dev` ;
6. inclure un `Point pédagogie` ;
7. donner à Naomie le prochain prompt NotebookLM court à copier-coller ;
8. ne lancer aucun développement.

Cette règle s'applique aussi si Naomie dit qu'elle veut `lancer`, `demarrer` ou
`reprendre` le sprint SELAS/CELAS. Dans ce contexte, `lancer le sprint` signifie
uniquement : ouvrir le sous-sprint NotebookLM et donner le prochain prompt a
copier-coller. Cela ne signifie jamais produire, generer, coder, passer en
matrice finale, ni passer en production.

Réponse attendue si Naomie dit seulement `Bonjour` :

```text
Statut sprint : Phase 0 - ACCUEIL / NO-GO dev
Action maintenant : je vérifie que tu es bien sur la branche codex/naomie-selas-sprint et que tu reprends le sprint SELAS.
Point pédagogie : tu n'as pas à gérer Git ni les commandes ; Codex protège la branche et l'ordre des étapes.
Prochaine étape : colle le Prompt NotebookLM 01 dans NotebookLM, puis donne-moi sa réponse pour que je la structure dans le journal SELAS.
```

Si Codex n'est pas dans le dépôt SYDEL ou ne peut pas vérifier la branche, il
doit le dire immédiatement et demander à ouvrir le projet dans le bon dossier.

Codex ne doit pas demander vaguement "fournis la source NotebookLM SELAS".
Il doit piloter une boucle :

- donner un prompt NotebookLM court ;
- recevoir la réponse de Naomie ;
- l'écrire de manière structurée dans `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` ;
- décider du prompt suivant ;
- continuer jusqu'à couverture suffisante avant audit de réutilisation et matrice.

Tant que la boucle NotebookLM n'est pas suffisante, Codex reste dans le ticket
`SELAS-SOURCES-NOTEBOOKLM-001` et ne doit pas lancer `SELAS-REUSE-AUDIT-001`,
`SELAS-MATRIX-001`, un generateur, un smoke, une preview produit ou un push de
fonctionnalite.

### Lecture obligatoire avant toute implémentation

Avant toute tâche d'implémentation, lire dans cet ordre :

1. `AGENTS.md` ;
2. `docs/project/00_MASTER_PLAN.md` ;
3. `docs/project/01_EXECUTION_BOARD.md` ;
4. `docs/project/02_CODEX_WORKFLOW.md` ;
5. `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` ;
6. `docs/project/04_LAST_STATE.md` ;
7. le fichier de livraison/specification pertinent dans `docs/delivery/`.

Si l'un de ces fichiers manque ou contredit le ticket demandé, arrêter l'implémentation et signaler le blocage.

### Pour toute tâche Codex

1. lire la doc liée dans `docs/` ;
2. repérer l'ADR applicable ;
3. limiter le changement au périmètre du ticket ;
4. ajouter ou mettre à jour les tests ;
5. documenter les hypothèses ;
6. ne pas toucher à plusieurs documents métier dans la même PR sauf ticket explicite.

### Gate produit / métier obligatoire

Avant tout développement, appliquer `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`.
Ce protocole est l'application locale de la doctrine globale
`docs/project/GLOBAL_CODEX_PRODUCT_GUARDRAIL_V1.md`, destinée à tous les projets
pilotés avec Codex.

Codex agit comme pilote projet / produit principal :

- reformuler l'intention métier avant de coder ;
- vérifier que le technique colle au besoin fonctionnel, aux sources et aux specs ;
- qualifier le ticket en `GO dev` ou `NO-GO dev` ;
- documenter les hypothèses, exclusions, réserves et arbitrages requis ;
- utiliser des sous-agents spécialisés si cela aide à protéger le périmètre ;
- maintenir une mémoire de reprise suffisante pour qu'un nouveau chat sache où en est le projet.

Si le fonctionnel n'est pas défini, ne pas coder : produire ou mettre à jour le cadrage nécessaire.

### Pour toute PR

- rester petite et traçable ;
- annoncer les risques ;
- lister les fichiers touchés ;
- signaler toute hypothèse métier ;
- vérifier que le wording juridique n'a pas dérivé.

## Commandes utiles

```bash
python -m pip install -U pip
python -m pip install -e ".[dev]"
pytest
ruff check .
streamlit run src/sydel_doc_engine/app/streamlit_app.py
```

## Conventions de code

- Python 3.11+
- typage explicite
- fonctions courtes
- logique métier séparée des couches UI / I/O
- pas de constantes magiques en dur dans les générateurs
- helpers transverses mutualisés dès que deux documents en dépendent

## Conventions de projet

- `DOC-xxx` = document canonique
- `LOT-x` = lot documentaire
- `ADR-xxxx` = décision d'architecture
- `EPIC-x` = chantier transversal GitHub

## Priorités actuelles

1. appliquer le gate produit / métier avant tout développement ;
2. maintenir `docs/project/04_LAST_STATE.md` comme état immédiatement reprenable ;
3. utiliser `docs/project/SELARL_CANONICAL_STATUS_V1.md` comme point de reprise SELARL ;
4. appliquer `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` avant tout nouveau sprint par type d'entreprise ;
5. appliquer `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` avant tout nouveau sprint par type d'entreprise ;
6. appliquer `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md` avant tout nouveau sprint par type d'entreprise ;
7. lire le fichier actif `docs/sprints/SPRINT_[TYPE]_V1.md` quand il existe ;
8. ne rouvrir un développement SELARL complexe qu'après décision explicite `GO dev` ;
9. capitaliser la méthode SELARL comme protocole réutilisable pour les autres formes sociales.

## Garde-fous juridiques

- ne jamais « améliorer » le texte juridique sans ticket explicite ;
- préférer l'identité stricte avec la source ;
- si une ambiguïté existe, bloquer la génération et documenter la décision requise.

## Mandatory project memory
Before any implementation task, read:
- docs/project/00_MASTER_PLAN.md
- docs/project/01_EXECUTION_BOARD.md
- docs/project/02_CODEX_WORKFLOW.md
- docs/project/03_HANDOFF_FOR_NEW_AGENT.md
- docs/project/04_LAST_STATE.md
- docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md when opening or following a company-type sprint
- docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md
- docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md when opening or following a company-type sprint
- docs/sprints/SPRINT_[TYPE]_V1.md when the sprint file exists
- docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md
- the relevant delivery/spec file

At the end of each task:
- update docs/project/01_EXECUTION_BOARD.md
- update docs/project/04_LAST_STATE.md
- mention the next recommended step
- do not rewrite legal wording unless the spec explicitly asks for it
