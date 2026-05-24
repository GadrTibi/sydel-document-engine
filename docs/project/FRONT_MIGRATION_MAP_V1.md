# Carte de migration front V1

Ticket source : `FRONT-REVIEW-001`

Statut : decision d'execution pour le rebuild UI visible, sans implementation UI dans ce ticket.

## Lecture

Categories utilisees :

- `KEEP_AS_PROTOTYPE` : conserver dans le prototype actuel comme bac a sable runnable, sans en faire la cible produit.
- `MIGRATE_TO_NEW_FRONT` : reprendre comme fondation ou composant du nouveau front.
- `KEEP_AS_TEST_TOOL` : conserver comme outil de diagnostic, smoke, prefill ou test unitaire.
- `DEPRECATE_LATER` : garder temporairement pour compatibilite, puis remplacer quand le nouveau front couvre le meme besoin.

## Carte de migration

| composant actuel | categorie | justification | dependances | risque si supprime trop tot | ticket futur cible |
|---|---|---|---|---|---|
| Shell Streamlit actuel dans `streamlit_app.py` | KEEP_AS_PROTOTYPE | Le radio `Assistant metier` / `Document unitaire` / `Technique / diagnostic` reste le seul lanceur local complet. Il n'est pas une architecture produit cible. | Streamlit, `ui_runtime`, adaptateurs app | Perte du point d'entree local pour smoke, diagnostic et telechargements. | `FRONT-UI-SHELL-001` |
| Assistant metier actuel | KEEP_AS_PROTOTYPE | Parcours utile pour comparer le comportement historique et tester `DOC-001` a `DOC-004`, mais encore fortement couple aux widgets et au `session_state`. | `business_wizard.py`, `test_prefill_presets.py`, `ui_runtime` | Perte du parcours bac a sable avant que le dossier editor global existe. | `FRONT-DOSSIER-EDITOR-001` puis `FRONT-PROTOTYPE-DEPRECATION-001` |
| Parcours SELARL visible dans `streamlit_app.py` | DEPRECATE_LATER | Il a servi a stabiliser wording, flow et prefill, mais il encode encore les ecrans dans une fonction longue et manipule directement les champs derives. | `business_wizard.py`, `selarl_form_schema.py`, `session_state` | Regression sur les tests SELARL et sur les prefills si remplace sans adapter les scenarios. | `FRONT-DOSSIER-EDITOR-001` |
| Parcours SCI simple dans l'Assistant metier | KEEP_AS_TEST_TOOL | Il sert surtout de non-regression historique et de cas simple pour l'orchestrateur. Il ne doit pas devenir le modele du front global. | `business_wizard.py`, catalogue de cas | Perte d'un smoke simple sur les documents de base. | `FRONT-TEST-TOOLS-CONSOLIDATION-001` |
| Mode Technique / diagnostic | KEEP_AS_TEST_TOOL | C'est le meilleur outil actuel pour charger un contexte YAML/JSON, verifier la selection orchestrateur et produire DOCX/PDF/ZIP hors parcours produit. | `ui_runtime`, exemples de contexte, orchestrateur | Perte de diagnostic moteur et de reproduction rapide des anomalies. | `FRONT-TEST-TOOLS-CONSOLIDATION-001` |
| Mode Document unitaire visible actuel | KEEP_AS_TEST_TOOL | Le mode est propre pour tester un document isole, mais son UI reste un outil de diagnostic separe du parcours dossier complet. | `app/single_document_mode.py`, `front_data/unit_document_mode.py`, `ui_runtime` | Perte du test unitaire document avant consolidation du nouveau panneau. | `FRONT-UNIT-DOCUMENT-UI-001` |
| `src/sydel_doc_engine/app/single_document_mode.py` | MIGRATE_TO_NEW_FRONT | L'adaptateur est deja adosse a `front_data/unit_document_mode.py` et prepare un contexte minimal honnete. A garder comme base transitoire. | `front_data.unit_document_mode`, `domain.models`, catalogue | Regressions sur `DOC-001` a `DOC-004`, `DOC-006`, `DOC-013` et `DOC-014` en mode unitaire. | `FRONT-UNIT-DOCUMENT-UI-001` |
| `src/sydel_doc_engine/front_data/unit_document_mode.py` | MIGRATE_TO_NEW_FRONT | Couche data cible du mode document unique : scope V1, exigences, plan et readiness. | `document_status`, `DocumentRequirementRecord` | Perte de la distinction dossier complet / document unitaire. | `FRONT-UNIT-DOCUMENT-UI-001` |
| Prefill de test visible dans l'Assistant metier | KEEP_AS_TEST_TOOL | Les controles `Scenario de test`, `Preremplir`, `Reinitialiser` sont utiles, mais doivent rester marques comme fictifs. | `app/test_prefill_presets.py`, `front_data/test_prefill_presets.py` | Perte des scenarios reproductibles de QA. | `FRONT-TEST-TOOLS-CONSOLIDATION-001` |
| `src/sydel_doc_engine/app/test_prefill_presets.py` | KEEP_AS_TEST_TOOL | Pont utile entre widgets historiques, `BusinessWizardInput`, `DossierRecord` et statuts. Ce n'est pas une source metier. | `front_data.test_prefill_presets`, `business_wizard.py` | Regressions sur les tests de prefill et sur le smoke Assistant. | `FRONT-TEST-TOOLS-CONSOLIDATION-001` |
| `src/sydel_doc_engine/front_data/test_prefill_presets.py` | KEEP_AS_TEST_TOOL | Profils front_data deterministes, reutilisables pour QA et demo interne, mais explicitement fictifs. | `front_data.models` | Perte des scenarios reproductibles alignes sur roles/adresses/statuts. | `FRONT-TEST-TOOLS-CONSOLIDATION-001` |
| `src/sydel_doc_engine/app/business_wizard.py` | DEPRECATE_LATER | Module pur et teste, mais son modele plat `BusinessWizardInput` et ses validations `DOC-001` a `DOC-004` ne sont pas le modele global cible. | `case_catalog`, `domain.models`, `selarl_form_schema.py` | Perte de l'adaptateur de generation actuel avant creation d'un builder dossier global. | `FRONT-DOSSIER-EDITOR-001` puis `FRONT-PROTOTYPE-DEPRECATION-001` |
| Projections UI SELARL historiques (`selarl_form_schema.py` via `business_wizard.py`) | DEPRECATE_LATER | Elles documentent des labels et blocs utiles, mais elles precedent le registre global V2.1 et la couche `front_data`. | `business_wizard.py`, specs SELARL | Risque de perdre des libelles stabilises avant leur migration dans le nouveau flow. | `FRONT-DOSSIER-EDITOR-001` |
| Helpers `session_state` business/single document | DEPRECATE_LATER | Ils sont necessaires au prototype Streamlit, mais ne doivent pas porter les regles metier du nouveau front. | `streamlit_app.py` | Casse les modes existants si retire avant shell et state model cible. | `FRONT-UI-SHELL-001` puis `FRONT-PROTOTYPE-DEPRECATION-001` |
| ZIP/PDF/download UI existants | MIGRATE_TO_NEW_FRONT | Les actions de telechargement et la separation DOCX/PDF/ZIP sont utiles. La presentation et les clefs Streamlit seront a reconstruire. | `ui_runtime`, backend PDF, zip bundle | Perte de la boucle utilisateur finale de generation et recuperation des artefacts. | `FRONT-GENERATION-ACTIONS-001` |
| `src/sydel_doc_engine/app/ui_runtime.py` | MIGRATE_TO_NEW_FRONT | Adaptateur app utile pour parser/generer/zipper sans mettre la logique dans l'UI. | orchestrateur, PDF, ZIP | Duplication de logique de generation dans le nouveau front. | `FRONT-GENERATION-ACTIONS-001` |
| `src/sydel_doc_engine/front_data/models.py` | MIGRATE_TO_NEW_FRONT | Source cible des objets front : dossier, personnes, societes, roles, adresses, valeurs canoniques, reuse, validations. | registre canonique V2.1 | Perte de la separation UI / donnees qui justifie le rebuild. | Socle de tous les tickets UI visibles |
| `src/sydel_doc_engine/front_data/role_model.py` | MIGRATE_TO_NEW_FRONT | Garde-fous de roles, portees et representation ; indispensable pour eviter les fusions silencieuses. | `front_data.models` | Retour aux roles implicites du prototype. | `FRONT-DOSSIER-EDITOR-001` |
| `src/sydel_doc_engine/front_data/address_model.py` | MIGRATE_TO_NEW_FRONT | Modele explicite des adresses typees, reutilisations et formes affichees/decomposees. | `front_data.models` | Retour aux adresses libres ou fusionnees trop tot. | `FRONT-DOSSIER-EDITOR-001` |
| `src/sydel_doc_engine/front_data/dossier_flow.py` | MIGRATE_TO_NEW_FRONT | Definit les etapes, blocs, dependances et validations du futur parcours dossier. | roles, adresses, validations, requirements | UI reconstruite sans sequence metier fiable. | `FRONT-UI-SHELL-001`, `FRONT-DOSSIER-EDITOR-001` |
| `src/sydel_doc_engine/front_data/document_status.py` | MIGRATE_TO_NEW_FRONT | Source cible des statuts documentaires, raisons, blocages, reserves et lots. | `dossier_flow`, validations, catalogue | Confusion entre documents attendus, prets, manuels et reserves. | `FRONT-DOCUMENTS-PANEL-001` |
| `src/sydel_doc_engine/front_data/canonical_mapping.py` | MIGRATE_TO_NEW_FRONT | Point de correspondance entre registre V2.1 et objets data. | registre V2.1, matrice identite | Reapparition d'aliases legacy comme champs metier concurrents. | `FRONT-DOSSIER-EDITOR-001` |
| `src/sydel_doc_engine/front_data/validation.py` | MIGRATE_TO_NEW_FRONT | Diagnostics data-layer transverses : roles, adresses, valeurs, reuse, ambiguities. | `front_data.models`, role/address models | UI incapable d'expliquer les blocages autrement qu'en champs vides. | `FRONT-DOCUMENTS-PANEL-001` |
| Scenarios de smoke et tests unitaires front | KEEP_AS_TEST_TOOL | Ils servent de filet de securite pour les fondations et le prototype pendant la migration. | `tests/unit/*front*`, scenarios prefills | Perte de confiance pendant la separation prototype / nouveau front. | `FRONT-TEST-TOOLS-CONSOLIDATION-001` |

## Decision courte

Le nouveau front doit partir de `front_data`, pas de `streamlit_app.py`. Le prototype reste vivant comme banc d'essai jusqu'a ce que le shell UI, l'editeur dossier, le panneau documents et les actions de generation couvrent les memes usages sans dependance aux fusions implicites du prototype.
