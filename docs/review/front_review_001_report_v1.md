# Rapport FRONT-REVIEW-001

Date : 2026-05-24

## 1. Perimetre

Ce ticket est une revue produit et execution du prototype front actuel a la lumiere des fondations globales creees depuis `GLOBAL-FRONT-ARCHITECTURE-001`.

Aucun generateur, moteur DOCX/PDF/ZIP, wording juridique ou code Python n'a ete modifie dans ce ticket. Le prototype Streamlit n'a pas ete supprime et aucun rebuild UI visible n'a ete code.

Livrables :

- `docs/project/FRONT_MIGRATION_MAP_V1.md`;
- `docs/review/front_review_001_report_v1.md`;
- mise a jour de `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`;
- mise a jour de `docs/project/01_EXECUTION_BOARD.md`;
- mise a jour de `docs/project/04_LAST_STATE.md`.

## 2. Sources utilisees

Sources de fondation lues :

- `docs/review/front_data_layer_001_report_v1.md`;
- `docs/review/front_role_model_001_report_v1.md`;
- `docs/review/front_address_model_001_report_v1.md`;
- `docs/review/front_dossier_flow_001_report_v1.md`;
- `docs/review/front_document_status_layer_001_report_v1.md`;
- `docs/review/front_unit_document_mode_001_report_v1.md`;
- `docs/review/front_test_prefill_001_report_v1.md`;
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`;
- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`;
- `docs/project/GLOBAL_FRONT_RULES_V1.md`;
- `docs/project/GLOBAL_FRONT_SCREEN_STRATEGY_V1.md`;
- `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`.

Sources code lues en audit, sans modification :

- `src/sydel_doc_engine/app/streamlit_app.py`;
- `src/sydel_doc_engine/app/business_wizard.py`;
- `src/sydel_doc_engine/app/single_document_mode.py`;
- `src/sydel_doc_engine/app/test_prefill_presets.py`;
- `src/sydel_doc_engine/front_data/models.py`;
- `src/sydel_doc_engine/front_data/role_model.py`;
- `src/sydel_doc_engine/front_data/address_model.py`;
- `src/sydel_doc_engine/front_data/dossier_flow.py`;
- `src/sydel_doc_engine/front_data/document_status.py`;
- `src/sydel_doc_engine/front_data/unit_document_mode.py`.

## 3. Verdict global sur le prototype

Verdict : le prototype actuel reste utile, mais il ne doit plus servir de base architecturale produit.

Il faut le conserver comme bac a sable et outil de diagnostic tant que le nouveau shell UI n'est pas disponible. En revanche, le rebuild visible doit partir de la couche `front_data`, du flow dossier et des statuts documentaires. Le prototype contient trop de logique de collecte, de synchronisation derivee et de `session_state` pour devenir le front global sans reconstruction.

Le registre canonique global V2.1 et les fondations `front_data` sont suffisants pour commencer la premiere tranche visible du rebuild, a condition de demarrer par un shell UI limite et de ne pas tenter de remplacer tout l'Assistant metier en une seule fois.

## 4. Audit du prototype actuel

### Ce qui releve du prototype historique

- `streamlit_app.py` concentre le shell, les trois modes, la collecte de donnees, les boutons de generation, les telechargements et les synchronisations `session_state`.
- Le parcours `Assistant metier` reconstruit un `BusinessWizardInput` plat depuis les widgets, puis convertit ce modele vers un `DocumentGenerationContext`.
- Le parcours SELARL visible contient encore des decisions de presentation et des champs derives directement dans l'UI.
- Le parcours SCI simple reste un cas de non-regression historique, pas un modele d'architecture globale.
- Les clefs `session_state` portent des effets metier temporaires : structure override, sorties generees, champs d'associe derives, domiciliation derivee.

### Ce qui a une vraie valeur durable

- Le decoupage en trois usages reste bon : dossier metier, document unitaire, diagnostic technique.
- Les actions DOCX / PDF local optionnel / ZIP et les telechargements sont utiles.
- Le mode `Technique / diagnostic` reste indispensable pour charger un contexte YAML/JSON et reproduire les comportements moteur.
- Le mode `Document unitaire` a deja ete realigne sur `front_data/unit_document_mode.py`.
- Les prefills sont maintenant deterministes, fictifs et relies a `front_data`.
- Les libelles et quelques avertissements SELARL stabilises peuvent inspirer la future UI, mais ils doivent etre revalides contre le registre global.

### Ce qui est encore trop couple a Streamlit

- `streamlit_app.py` manipule directement `st.session_state` pour des regles derivees.
- Les widgets et les objets de donnees sont trop proches : les champs visibles deviennent presque le modele metier.
- Les statuts de l'Assistant metier viennent encore de `business_wizard.py`, pas de `front_data/document_status.py`.
- Les actions de generation sont melangees aux sections de formulaire.
- Le mode unitaire construit encore son contexte moteur dans `app/single_document_mode.py`, meme si son plan de readiness vient de `front_data`.

### Ce qui est deja abstrait dans `front_data`

- Objets metier : dossier, personnes, societes, adresses, roles, operations, requirements, valeurs canoniques, reuse rules et validations.
- Roles : familles, portees, representation, ordre, tiers de controle, garde-fous contre les placeholders generiques.
- Adresses : usages, reutilisations explicites, formes affichees/decomposees et overrides.
- Flow dossier : etapes, blocs, dependances, documents associes et validations.
- Statuts documentaires : readiness, raisons de blocage, reserves, documents manuels et lots.
- Mode document unitaire : scope V1, exigences, plan de preparation et explication des blocages.
- Prefills de test : profils front_data deterministes et fictifs.

## 5. Ce qu'on garde du prototype

A garder comme prototype :

- le lanceur Streamlit actuel, jusqu'a livraison du nouveau shell ;
- l'Assistant metier existant, uniquement comme comparaison fonctionnelle et smoke historique ;
- le parcours SCI simple comme cas de non-regression ;
- les boutons DOCX / PDF / ZIP et les telechargements comme reference ergonomique minimale ;
- les messages de prudence sur PDF local, generation non juridique et documents manuels.

A garder uniquement comme outil de test :

- `Technique / diagnostic`;
- le mode `Document unitaire` visible actuel ;
- les prefills de test et leurs profils front_data ;
- les scenarios de smoke et tests unitaires front ;
- les exemples de contextes YAML/JSON.

A migrer vers le nouveau front :

- les objets et regles de `front_data/*`;
- les statuts documentaires et raisons de blocage ;
- le flow dossier par etapes et blocs ;
- la separation dossier complet / document unitaire ;
- les actions de generation et telechargement via un adaptateur propre ;
- les profils de prefill comme jeu de QA, pas comme donnees metier.

A remplacer / deprecier plus tard :

- `BusinessWizardInput` comme modele metier principal ;
- la logique de validation `DOC-001` a `DOC-004` portee par `business_wizard.py` ;
- les projections SELARL historiques qui precedent le registre global ;
- les synchronisations metier directement codees dans `streamlit_app.py`;
- les listes de champs UI manuelles quand le flow et le mapping canonique peuvent les porter.

## 6. Ce qu'on doit reconstruire

Le rebuild visible doit reconstruire, dans cet ordre logique :

1. un shell UI global qui separe clairement nouveau front, outils de test et prototype ;
2. un editeur dossier data-first, adosse a `DossierRecord`, `RoleAssignment`, `AddressRecord` et `DossierFlow`;
3. un panneau Documents attendus adosse a `document_status.py`;
4. des actions de generation qui consomment uniquement les documents prets et expliquent les blocages ;
5. un mode Document unitaire UI consolide, separe du dossier complet ;
6. une zone de test/prefill/diagnostic explicite ;
7. la deprecation progressive du prototype historique.

## 7. Premiere tranche visible recommandee

Premiere tranche recommandee : `FRONT-UI-SHELL-001`.

Raison : avant de reconstruire les fiches dossier, il faut isoler le prototype et poser un shell cible qui empeche la confusion entre "ancien Assistant metier" et "nouveau front global". Ce ticket doit etre visible, mais limite.

Perimetre recommande :

- ajouter une entree claire vers le nouveau front global ;
- conserver les modes existants dans une zone prototype / diagnostic ;
- afficher un squelette read-only du flow dossier global depuis `front_data/dossier_flow.py`;
- afficher la place future du panneau documents depuis `front_data/document_status.py`, sans promettre une generation complete ;
- ne pas coder encore les formulaires complets de parties, roles et adresses ;
- ne pas modifier les generateurs ni le moteur.

Critere de succes : l'utilisateur voit ou commence le nouveau front, ou restent les outils de test, et pourquoi le prototype actuel n'est plus le parcours cible.

## 8. Risques si on pousse le prototype trop tot

- Fusion silencieuse de roles : praticien, associe, gerant, signataire et mandataire peuvent sembler equivaloir selon les widgets, alors que le modele cible exige des assignments explicites.
- Fusion d'adresses : les champs derives du prototype peuvent masquer la distinction siege, domiciliation, lieu d'exercice, cabinet cede, bailleur, banque ou ordre.
- Statuts incomplets : l'Assistant actuel sait signaler generable / bloque pour certains cas, mais ne porte pas encore toute la structure `document_status`.
- Confusion dossier complet / document unique : le mode unitaire est utile mais ne doit pas devenir un raccourci de dossier.
- `session_state` fragile : des champs desactives ou derives peuvent rester vides ou stale si la saisie arrive dans un ordre different.
- Fausse maturite produit : le prototype peut donner l'impression que le front global est pret, alors qu'il ne couvre pas encore tous les blocs orange.

## 9. Ordre d'implementation recommande

1. `FRONT-UI-SHELL-001` : shell visible du nouveau front et isolement du prototype.
2. `FRONT-DOSSIER-EDITOR-001` : editeur dossier minimal, data-first, avec qualification, personnes, societes, roles et adresses.
3. `FRONT-DOCUMENTS-PANEL-001` : panneau documents attendus, statuts, raisons, reserves, blocages.
4. `FRONT-GENERATION-ACTIONS-001` : actions DOCX/PDF/ZIP depuis les seuls documents prets, via adaptateurs existants.
5. `FRONT-UNIT-DOCUMENT-UI-001` : consolidation UI du mode document unitaire.
6. `FRONT-TEST-TOOLS-CONSOLIDATION-001` : regroupement prefills, smoke et diagnostic.
7. `FRONT-PROTOTYPE-DEPRECATION-001` : marquage et retrait progressif du prototype quand la couverture cible est suffisante.

En parallele, `SELARL-JURIST-REVIEW-001` reste recommande pour valider juridiquement le parcours SELARL, mais il ne doit pas bloquer le shell UI technique du rebuild.

## 10. Points encore ouverts

- Adapter proprement un `DossierRecord` global vers `DocumentGenerationContext` pour une generation dossier large, sans reconstruire les generateurs.
- Definir le niveau de granularite UI des collections : associes, apporteurs, cessionnaires, representants, exercices, lignes de parts.
- Decider le style final des composants Streamlit ou d'un autre shell front si Streamlit reste seulement transitoire.
- Clarifier la place des pieces justificatives ordinales et des documents a remplir manuellement dans le panneau documents.
- Continuer a qualifier les zones orange : ordre/mandataire/document-lot, capital/titres/apports, cession cabinet/bail/financement, SCM/SPFPL.

## 11. Validation

Validation documentaire realisee :

- audit des sources et modules listes dans le ticket ;
- creation de la carte de migration ;
- mise a jour du backlog UI visible ;
- verification que le ticket ne modifie aucun fichier Python.

Pas de `ruff` ni de `pytest` requis : aucun code Python n'a ete modifie.

## 12. Prochaine etape recommandee

Lancer `FRONT-UI-SHELL-001`.

Le ticket doit creer la premiere tranche visible du nouveau front sans remplacer le prototype, sans coder l'editeur dossier complet et sans toucher aux generateurs ni au moteur DOCX/PDF/ZIP.
