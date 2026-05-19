# Hiérarchie des sources SELARL V2

Ticket source : `SELARL-NOTEBOOKLM-RECONCILIATION-001`

## Objet

Ce document remplace le cadrage implicite SELARL fondé uniquement sur `Documents à générer par cas` par une hiérarchie explicite de sources. Il ne modifie pas l'architecture moteur, les générateurs, l'UI ni les formulations juridiques.

La hiérarchie ci-dessous vaut pour le cadrage SELARL et doit être traitée comme un overlay métier à intégrer dans une ADR dédiée si elle devient règle générale du projet.

## Hiérarchie retenue

### 1. NotebookLM / transcriptions client

Fichier lu : `project/source_truth/notebooklm_selarl_10_prompts_v1.md`.

NotebookLM apporte la source métier vivante :

- vocabulaire réellement attendu par les juristes ;
- ordre naturel du processus de saisie ;
- rôles métier et juridiques à ne pas confondre ;
- règles de réutilisation des données ;
- statut attendu des documents dans le parcours ;
- attentes UX sur le mode `Projet`, les brouillons Word et les documents à relire ;
- points de blocage liés à l'Ordre, aux pièces jointes, à la banque et aux cas complexes.

NotebookLM ne doit pas décider seul :

- du wording juridique dans les actes ;
- de la liste finale des documents à générer ;
- des variables exactes extraites des modèles DOCX ;
- du statut technique d'un générateur déjà implémenté.

### 2. Documents à générer par cas V3

Fichier lu : `project/source_truth/Documents_a_generer_par_cas_V3.docx`.

V3 apporte la source documentaire :

- documents attendus par cas SELARL ;
- conditions documentaires ;
- noms de fichiers source ;
- variables par document ;
- questions fonctionnelles nouvelles ajoutées par rapport à V2.

Constat important : V3 conserve le contenu V2 puis ajoute une couche de questions par document. Elle améliore donc l'exploitation formulaire, mais ne règle pas seule les sujets UX, rôles et statut `Projet`.

V3 ne doit pas décider seul :

- du libellé visible côté juriste si NotebookLM donne un vocabulaire plus métier ;
- de la réutilisation automatique entre personnes et rôles ;
- du fait qu'un document générable moteur soit présenté comme définitif ;
- de la nécessité d'une revue humaine ou de pièces justificatives.

### 3. Templates DOCX et registre moteur

Sources techniques :

- templates DOCX dans `project/source_documents/` ;
- registre moteur et catalogue de documents ;
- générateurs existants `DOC-001` à `DOC-043`.

Ils apportent :

- faisabilité technique de génération ;
- variables réellement consommées par les générateurs ;
- noms de sortie ;
- limitations déjà codées ;
- statut technique d'un document : générateur présent, absent, manuel, incomplet.

Ils ne doivent pas décider seuls :

- de l'ordre de saisie ;
- du vocabulaire affiché dans l'Assistant métier ;
- de la source métier du dossier ;
- de la qualification juridique d'un document comme final, projet, brouillon ou manuel.

### 4. Code existant

Fichiers concernés par l'audit :

- `src/sydel_doc_engine/domain/case_catalog.py` ;
- `src/sydel_doc_engine/app/selarl_form_schema.py` ;
- `src/sydel_doc_engine/app/business_wizard.py` ;
- `src/sydel_doc_engine/app/streamlit_app.py`.

Le code existant est une implémentation à corriger. Il sert à mesurer les écarts, pas à trancher la vérité métier.

Le code ne doit pas décider seul :

- qu'un libellé est acceptable parce qu'il est déjà testé ;
- qu'un document est définitif parce qu'il est techniquement générable ;
- qu'un rôle peut être dérivé par défaut sans validation métier ;
- qu'un ordre d'écran est correct parce qu'il est déjà branché ;
- qu'une adresse peut être copiée sans case explicite.

## Règles d'arbitrage

| Situation | Source prioritaire | Règle |
|---|---|---|
| Vocabulaire visible, ordre des écrans, rôles et UX | NotebookLM | Appliquer le vocabulaire client sauf contradiction juridique explicite. |
| Liste documentaire, variables, conditions par cas | V3 | Utiliser V3 comme source documentaire principale. |
| Différence V2 vs V3 | V3 | V3 remplace V2 pour le cadrage SELARL, sauf anomalie documentée. |
| Document générable mais signalé complexe par NotebookLM | V3 + NotebookLM | Garder le document dans le catalogue, mais l'afficher comme brouillon / projet à relire si la complexité métier l'exige. |
| Document manuel dans V3 | V3 | Ne pas envoyer à la génération sans arbitrage explicite. |
| Template/générateur existant contredit V3 | V3 + décision métier | Ne pas corriger en silence ; documenter l'écart et ouvrir un ticket. |
| NotebookLM contredit le wording juridique d'un template | Template + revue juriste | Ne jamais modifier le wording juridique sans validation. |
| Ambiguïté de rôle ou d'adresse | NotebookLM | Ne pas dériver automatiquement ; demander une case explicite ou bloquer. |

## Conséquences immédiates

- Le terme visible `professionnel principal` doit être remplacé par `Praticien` ou par le rôle juridique exact.
- L'écran identité doit être requalifié en `Fiche Client` ou `Fiche de création`, avec préférence NotebookLM pour `Fiche Client`.
- L'ordre cible devient : qualification, Fiche Client / Praticien, Fiche Société, Capital & Associés, Contexte & scénarios métier, Documents & génération.
- `Mandataire = signataire` ne doit plus être une hypothèse par défaut.
- `Mandataire` doit être un membre Sydel par défaut, avec possibilité d'exception.
- Les documents complexes techniquement générables doivent pouvoir être affichés comme `Projet`, `brouillon à relire` ou `semi-automatique`, pas seulement `Générable`.
- Le smoke SELARL doit attendre une réalignement minimal du wording, de l'ordre et des règles de réutilisation.
