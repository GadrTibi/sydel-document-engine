# Rapport executif - GLOBAL-FRONT-ARCHITECTURE-001

## Objet

Concevoir l'architecture du nouveau front global a partir du registre canonique global V2.1, sans modifier l'UI existante, les generateurs, le moteur DOCX/PDF/ZIP ou le wording juridique.

Ce ticket est documentaire uniquement.

## Etat Git initial

- Branche initiale : `main`.
- `main` etait en avance de 3 commits sur `origin/main`.
- Fichier ou dossier non suivi initial : `docs/docssource_truth/`.
- Aucun push demande ni effectue.

## Sources utilisees

Sources obligatoires lues :

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv`
- `docs/project/GLOBAL_VARIABLE_IDENTITY_MATRIX_V1.csv`
- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`
- `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V2.md`
- `docs/review/global_variable_identity_audit_001_report_v1.md`
- `docs/review/global_human_answers_integration_001_report_v1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `src/sydel_doc_engine/registry/catalog.py`
- `project/source_truth/albane_reponse_mail_selarl_v1.md`
- `project/source_truth/notebooklm_selarl_10_prompts_v1.md`
- `project/source_truth/Documents_a_generer_par_cas_V3.docx`

References secondaires lues uniquement pour qualifier le prototype :

- `src/sydel_doc_engine/app/selarl_form_schema.py`
- `src/sydel_doc_engine/app/business_wizard.py`
- `src/sydel_doc_engine/app/streamlit_app.py`

ADR applicables :

- `docs/adr/0001-source-of-truth.md`
- `docs/adr/0002-engine-per-document.md`
- `docs/adr/0003-lot-based-delivery.md`
- `docs/adr/0005-codex-working-mode.md`

Note : aucun fichier de specification dedie a `GLOBAL-FRONT-ARCHITECTURE-001` n'existe dans `docs/delivery/`. Le ticket utilisateur, le registre V2.1, les audits globaux et les sources listees ci-dessus ont donc servi de cadrage de livraison.

## Livrables crees

- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`
- `docs/project/GLOBAL_FRONT_RULES_V1.md`
- `docs/project/GLOBAL_FRONT_SCREEN_STRATEGY_V1.md`
- `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`
- `docs/review/global_front_architecture_001_report_v1.md`

## Hypotheses retenues

- Le registre V2.1 est la source stable pour l'architecture front globale, mais pas une spec de generation documentaire.
- Le prototype Streamlit est un outil de diagnostic et de preuve technique, pas une fondation de modele produit global.
- Le nouveau front doit etre data-first : objets metier, roles, adresses typees, documents attendus, regles de reutilisation.
- Les documents manuels ou reserves doivent rester visibles dans le futur front, mais exclus de la generation automatique.
- Les questions V2 encore ouvertes sont arbitrables en interne et ne bloquent pas l'architecture.

## Objets metier retenus

Les objets retenus pour le rebuild sont :

- `Person`
- `Organization / Company`
- `Address`
- `RoleAssignment`
- `Dossier / Matter / Operation`
- `DocumentRequirement`
- `FieldDefinition`
- `ReuseRule`
- `ValidationIssue`
- `SupportingEvidence`

Le choix structurant est la separation entre fiche et role. Une meme fiche peut alimenter plusieurs roles, mais seulement via une regle explicite, visible et reversible.

## Architecture retenue

Le front cible doit :

- entrer par type d'operation et famille documentaire ;
- construire des fiches personnes, societes et adresses ;
- assigner les roles explicitement ;
- afficher les reutilisations actives ;
- distinguer les champs identiques, les formes differentes, les reutilisations explicites et les champs distincts ;
- afficher les documents attendus avant generation ;
- separer parcours dossier complet et mode document unitaire ;
- garder les documents manuels, reserves et non implementes visibles dans le statut documentaire.

## Grands risques de rebuild

Les risques principaux sont :

- reutiliser implicitement une personne dans plusieurs roles sans validation ;
- confondre domicile, lieu d'exercice, siege, domiciliation, locaux loues et adresses SCM ;
- transformer des variables spec-only ou template-only en champs front definitifs ;
- traiter les calculs de capital, prix, parts/actions ou droits financiers comme automatiques trop tot ;
- generaliser le prototype Streamlit alors qu'il encode des choix locaux ;
- cacher les documents manuels au lieu de les signaler ;
- confondre generation technique et validation juridique.

## Points encore ouverts

Les sujets suivants restent a traiter dans les tickets de rebuild ou de revue :

- modele final `ordre` par inscrit : personne physique, societe, departement, RPPS, numero d'ordre ;
- capital, titres, apports, prix, actions de preference, droits financiers et overrides ;
- signataire par document, mandataire et representant de personne morale ;
- dates homonymes : signature, decision, PV, bail, effet, jouissance, limite de realisation ;
- separation entre donnees dossier et parametrage cabinet/SYDEL pour banque, fiscalite, enregistrement et signature electronique ;
- bail et locataire selon presence d'une SCM ;
- cas SELAS medecin avec societe civile micro-holding ;
- mode Projet / filigrane, documente mais non implemente.

## Registre V2.1 suffisant pour le rebuild ?

Oui, le registre canonique global V2.1 est suffisant pour demarrer le rebuild front au niveau architecture produit et donnees.

Limite : il n'est pas suffisant pour modifier les generateurs, le wording juridique, les calculs sensibles, les documents manuels, le filigrane Projet ou le cas SELAS medecin avec micro-holding. Ces sujets restent soumis a des tickets dedies et au pipeline documentaire.

## Prototype actuel

### Ce qu'on garde

- Le principe de trois modes separes : Assistant metier, Document unitaire, Technique / diagnostic.
- La capacite a afficher les documents attendus avec un statut.
- Les actions separees DOCX, PDF local optionnel et ZIP.
- Les telechargements par fichier.
- Les presets fictifs de test, a condition de les rendre clairement non metier.
- Les validations visibles et les messages de contexte incomplet.

### Ce qu'on jette

- Les ecrans actuels comme modele produit global.
- Les listes de champs SELARL codees dans le prototype comme source de verite.
- La logique de reutilisation enfouie dans les widgets.
- Le `session_state` comme modele de donnees.
- Toute generalisation depuis les parcours SCI/SELARL existants.

### Ce qu'on migre

- Le concept de document attendu avec statut, mais dans une couche data globale.
- Le concept de mode document unitaire, mais comme outil de test separe.
- Les prefill de test, mais dans une couche de scenarios fictifs versionnee.
- Les validations de champs manquants, mais rattachees aux objets et `DocumentRequirement`.
- Les mecanismes de telechargement et packaging, une fois le nouveau front pret.

### Ce qu'on garde comme outil de diagnostic uniquement

- Le mode `Technique / diagnostic` YAML/JSON.
- Le prototype Streamlit existant tant qu'il reste utile pour tester DOCX/PDF/ZIP.
- Les scenarios de smoke et prefill du prototype.
- Le mode document unitaire existant tant que le futur mode n'est pas reconstruit.

## Backlog du rebuild

Le backlog V1 cree les tickets suivants :

- `FRONT-DATA-LAYER-001`
- `FRONT-ROLE-MODEL-001`
- `FRONT-ADDRESS-MODEL-001`
- `FRONT-DOSSIER-FLOW-001`
- `FRONT-DOCUMENT-STATUS-LAYER-001`
- `FRONT-UNIT-DOCUMENT-MODE-001`
- `FRONT-TEST-PREFILL-001`
- `FRONT-REVIEW-001`

La prochaine etape recommandee est `FRONT-DATA-LAYER-001`, puis `FRONT-ROLE-MODEL-001` et `FRONT-ADDRESS-MODEL-001`.

## Validations

- Relecture documentaire des livrables.
- Controle du diff.
- Aucun test Python execute : aucun fichier Python modifie.
- Aucun ruff/pytest requis.

## Prochaine etape recommandee

Lancer `FRONT-DATA-LAYER-001` : creer la couche de donnees front globale a partir des objets et regles V1, sans toucher aux generateurs, au moteur DOCX/PDF/ZIP ni au prototype Streamlit.
