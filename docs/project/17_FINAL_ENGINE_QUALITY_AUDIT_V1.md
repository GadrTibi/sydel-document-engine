# Audit qualite final moteur V1

Ticket : `FINAL-MOTOR-AUDIT-002`

Date : 2026-05-15

## Objet

Ce document realise l'audit transversal final du moteur documentaire sur l'etat present de `main`, en lecture seule sur le code Python.

Il audite :

- la couverture documentaire ;
- la couverture variables ;
- les cas manuels assumes ;
- les accords genre / nombre ;
- la coherence catalogue / orchestrateur / generateurs ;
- les trous restants eventuels.

Il ne modifie aucun wording juridique et ne vaut pas validation juridique ou visuelle humaine des DOCX generes.

## Sources lues

- `AGENTS.md`
- `docs/adr/0001-source-of-truth.md`
- `docs/adr/0002-engine-per-document.md`
- `docs/adr/0003-lot-based-delivery.md`
- `docs/adr/0004-from-scratch-docx-generation.md`
- `docs/adr/0005-codex-working-mode.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/project/15_REMAINING_SCOPE_AUDIT_V1.md`
- `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md`
- `project/source_truth/Documents_a_generer_par_cas.docx`
- tous les fichiers presents dans `docs/delivery/`
- tous les fichiers presents dans `src/sydel_doc_engine/generators/`
- `src/sydel_doc_engine/registry/catalog.py`
- `src/sydel_doc_engine/orchestrator/service.py`

## Legende

| Classement | Sens |
|---|---|
| OK | Coherent pour le perimetre moteur DOCX audite. |
| a revoir | Ecart, dette ou contradiction a traiter avant de considerer la qualite moteur globalement close. |
| hors perimetre V1 assume | Exclusion documentee, volontaire ou bloquee par source/spec/arbitrage. |

## Conclusion globale

| Point | Classement | Conclusion |
|---|---|---|
| Registre moteur `DOC-001` a `DOC-033` | OK | Le catalogue et le registre de generateurs de l'orchestrateur exposent le meme ensemble de 33 `doc_id`, sans `doc_id` manquant d'un cote ou de l'autre. |
| Couverture documentaire globale source de verite -> orchestrateur | a revoir | Des generateurs et tests existent pour des documents attendus par la source de verite ou les tickets `DONE`, mais ils ne sont pas presents dans le catalogue/orchestrateur. |
| Couverture variables globale | a revoir | Les specs tardives definissent de nombreux packs variables non consolides dans le dictionnaire canonique V1 ni dans la table de mapping V1. |
| Cas manuels documentes | OK | Les exclusions manuelles et legacy sont majoritairement tracees et bloquees plutot qu'automatisees implicitement. |
| Qualite juridique / visuelle finale | hors perimetre V1 assume | Les tests et smoke DOCX ne remplacent pas une revue humaine juridique et visuelle. |
| UI / PDF / ZIP | hors perimetre V1 assume | Ces chantiers restent explicitement hors du ticket moteur DOCX final. |

Statut global : **couverture globale non OK** tant que les generateurs orphelins et les ecarts de referentiel variables ne sont pas traites ou explicitement reclasses hors V1.

## 1. Couverture documentaire

### 1.1 Documents effectivement exposes par le moteur

| Point | Classement | Constat |
|---|---|---|
| `DOC-001` a `DOC-003` - documents universels | OK | Declarations, domiciliation et procuration sont dans le catalogue, le registre orchestrateur et les generateurs. |
| `DOC-004` - PV nomination gerant | OK | Document mutualise hors SAS, avec generateur et selection catalogue/orchestrateur. |
| `DOC-005` et `DOC-006` - regime communautaire | OK | Les deux lettres sont conditionnees par `dossier_options.regime_communautaire`. |
| `DOC-007` a `DOC-012` - bail / appel de fonds / cession cabinets | OK | Les conditions cession, etape et type de cabinet sont implementees dans l'orchestrateur. |
| `DOC-013` et `DOC-014` - derogations coeur | OK | Les deux documents sont exposes comme formulaires a completer, avec selection par type de derogation. |
| `DOC-015` a `DOC-021` et `DOC-025` - statuts SAS, SEL, SCS, SCI, SCI IRIS, SCM | OK | Ces statuts sont exposes par le catalogue et filtres par contexte. |
| `DOC-022` - lettre option IS | OK | Document dedie, conditionne par `dossier_options.option_is`. |
| `DOC-023` et `DOC-024` - satellites SAS | OK | PV remuneration president et attestation capital/liste souscripteurs SAS sont conditionnes par le contexte SAS V1. |
| `DOC-026` a `DOC-030` - satellites SCM et acte actions SPFPL | OK | Les satellites SCM, la liste des depenses communes SCM et l'acte de cession d'actions SPFPL sont exposes. |
| `DOC-031` a `DOC-033` - cession SCM | OK | Les trois documents de cession SCM sont exposes pour SELARL/SELAS avec `dossier_options.scm_cession`. |

### 1.2 Documents attendus mais non exposes par le moteur

| Point | Classement | Constat |
|---|---|---|
| Demande d'inscription a l'ordre | a revoir | `DemandeInscriptionOrdreGenerator` existe et des tests unitaires existent, mais aucun `DocumentDefinition`, aucun `doc_id`, aucun import et aucune selection orchestrateur ne l'exposent. |
| Statuts SPFPL cession | a revoir | `StatutsSpfplCessionGenerator` existe et est teste, mais n'est pas dans le catalogue ni dans le registre orchestrateur. |
| Statuts SPFPL apport | a revoir | `StatutsSpfplApportGenerator` existe et est teste, mais n'est pas dans le catalogue ni dans le registre orchestrateur. |
| Note d'information SPFPL | a revoir | `NoteInformationGenerator` existe et est teste, mais n'est pas dans le catalogue ni dans le registre orchestrateur. |
| PV agrement cession SPFPL - associe unique | a revoir | Le generateur existe et est teste, mais n'est pas dans le catalogue ni dans le registre orchestrateur. |
| PV agrement cession SPFPL - plusieurs associes | a revoir | Le generateur existe et est teste, mais n'est pas dans le catalogue ni dans le registre orchestrateur. |
| Acte de cession de parts SPFPL | a revoir | Le generateur existe et est teste, mais n'est pas dans le catalogue ni dans le registre orchestrateur. |
| Contrat d'apport SEL/SPFPL | a revoir | Le generateur existe et est teste, mais n'est pas dans le catalogue ni dans le registre orchestrateur. |
| Attestation capital / liste des souscripteurs SPFPL | a revoir | Le generateur non-SAS existe et est teste, mais seul le satellite SAS est expose sous `DOC-024`. |
| Attestation nomination commissaire aux apports | a revoir | Le generateur existe et est teste, mais n'est pas dans le catalogue ni dans le registre orchestrateur. |

### 1.3 Coherence avec les audits precedents

| Point | Classement | Constat |
|---|---|---|
| `docs/project/15_REMAINING_SCOPE_AUDIT_V1.md` | OK | Cet audit historique signalait deja plusieurs generateurs presents mais non constates dans le catalogue/orchestrateur. |
| `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` | a revoir | La conclusion "feature complete" est trop large au regard du runtime audite : plusieurs familles citees comme disponibles ne sont pas activables par l'orchestrateur. |
| References delivery dans `docs/project/` | a revoir | `docs/project/*` reference des fichiers absents sur `main` : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`, `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md` et `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`. |

## 2. Couverture variables

| Point | Classement | Constat |
|---|---|---|
| Variables Lot 1 et PV initial | OK | Le dictionnaire canonique V1 et la table de mapping couvrent le socle initial, les roles `signataire`, `societe`, `signature`, `domiciliation`, `associes[]` et `dirigeant_nomine`. |
| Variables des lots tardifs | a revoir | Les packs `ordre`, `mandataire`, `statuts_sas`, `statuts_sel`, `statuts_civils`, `capital_souscription`, `operation_spfpl`, `societe_spfpl`, `societe_cible`, `scm_satellites`, `scm_cession` et assimilés sont surtout portes par les specs et le modele Python, pas par `08`/`09`. |
| Alias domiciliation | a revoir | Le referentiel canonique retient `domiciliation.adresse_affichee`, mais l'historique signale encore l'alias legacy `adresse_domiciliation_affichee` cote Lot 1/exemples. |
| Champs ponctuels manuels | OK | La source de verite accepte que certaines informations utilisees une seule fois restent des champs manuels plutot que des variables globales. |
| Variables UI futures | hors perimetre V1 assume | L'arbre UI et le pack unique de questions ne sont pas finalises dans ce ticket. |

## 3. Cas manuels assumes

| Point | Classement | Constat |
|---|---|---|
| Documents explicitement "a remplir a la main" | hors perimetre V1 assume | Le formulaire site distinct CD94, la derogation SEL BNC complet et les documents equivalents restent exclus sans decision explicite. |
| Derogation cumul salariee legacy | hors perimetre V1 assume | Le `.doc` legacy reste bloque par conversion non aboutie ; la strategie manuelle est documentee. |
| `DOC-013` et `DOC-014` | OK | Le moteur les expose comme formulaires a completer, sans automatiser les zones narratives sensibles. |
| Mentions manuelles conditionnelles | OK | Exemple : la mention de derogation dans la demande d'inscription a l'ordre est specifiee comme champ manuel bloquant si l'option est activee. |
| Revue humaine juridique / visuelle | hors perimetre V1 assume | Toutes les familles codées restent soumises a revue humaine ; les tests ne valident pas le fond juridique. |

## 4. Accords genre / nombre

| Point | Classement | Constat |
|---|---|---|
| Helper genre Lot 1 | OK | `utils/grammar.py` fournit les accords `Je soussigne/soussignee`, `Ne/Nee`, `fils/fille` et les generateurs Lot 1 les utilisent. |
| Documents marques `grammar_variants=True` dans le catalogue | OK | Les documents universels, le PV nomination gerant et les statuts SEL exposent explicitement des variantes grammaticales. |
| Gestion dynamique d'associes | OK | Le catalogue marque plusieurs documents comme dynamiques, notamment PV nomination gerant, statuts civils, lettre option IS, acte actions et cession SCM. |
| Generalisation genre/nombre tous documents | a revoir | Plusieurs documents conservent volontairement un wording source fixe : demande d'inscription a l'ordre sans feminisation automatique, president SAS masculin, cedant masculin pour l'acte actions, variantes SPFPL non generalisees. |
| Pluralite hors source ou non arbitree | hors perimetre V1 assume | Les specs bloquent plusieurs cas : multi-souscripteurs SPFPL, multi-associes SEL/SPFPL selon familles, plus de deux parties pour certains satellites SCM, et adaptations non sourcees. |

## 5. Coherence catalogue / orchestrateur / generateurs

| Point | Classement | Constat |
|---|---|---|
| Ensemble `doc_id` catalogue vs registre orchestrateur | OK | Les deux ensembles sont identiques : `DOC-001` a `DOC-033`. |
| Generateurs enregistres pour les `doc_id` catalogues | OK | Aucun `doc_id` catalogue audite n'est absent du registre de generateurs. |
| Filtres de selection orchestrateur | OK | Les filtres couvrent regime communautaire, bail/appel, cession cabinets, derogations, statuts, option IS, satellites SAS, satellites SCM, acte actions et cession SCM. |
| Generateurs orphelins | a revoir | Dix generateurs documentaires existent hors orchestrateur : demande ordre, statuts SPFPL cession/apport, note d'information, deux PV agrement SPFPL, acte cession parts SPFPL, contrat apport, attestation capital SPFPL, attestation commissaire. |
| Tests unitaires des generateurs orphelins | a revoir | Les tests demontrent une capacite de generation directe, mais pas une generation dossier via orchestrateur. |
| Nom historique `build_lot_01_generator_registry` | a revoir | La fonction construit maintenant tout le registre moteur ; le nom conserve `lot_01` et peut induire en erreur. |

## 6. Trous restants

| Trou | Classement | Impact |
|---|---|---|
| Alignement catalogue/orchestrateur des generateurs orphelins | a revoir | Bloque une conclusion de couverture documentaire globale OK. |
| Reconciliation de `docs/project/16` avec l'etat runtime | a revoir | L'audit 16 surconclut par rapport aux fichiers Python audites. |
| Consolidation du dictionnaire variables et de la table mapping | a revoir | Les variables tardives existent dans les specs/code mais pas dans le referentiel canonique global. |
| Fichiers delivery references mais absents de `main` | a revoir | Memoire projet incoherente pour quelques cadrages/specs Lot 2. |
| UI Streamlit V0 | hors perimetre V1 assume | Ticket separe requis. |
| PDF | hors perimetre V1 assume | Flux non integre au moteur audite. |
| ZIP dossier | hors perimetre V1 assume | Flux non integre au moteur audite. |
| Recette finale metier | hors perimetre V1 assume | Doit etre realisee humainement sur rendus. |

## 7. Synthese qualite

Le moteur est solide sur le sous-ensemble effectivement expose par `catalog.py` et `service.py` : le registre `DOC-001` a `DOC-033` est coherent et les conditions de selection principales sont explicites.

La couverture globale ne peut toutefois pas etre classee OK, car le depot contient des generateurs documentaires termines et testes qui ne sont pas atteignables par l'orchestrateur. La source de verite et les specs citent notamment la demande d'inscription a l'ordre et plusieurs documents SPFPL ; leur absence du catalogue/orchestrateur cree un ecart runtime.

Prochaine etape recommandee : ouvrir un ticket d'alignement moteur ciblé, sans nouveau wording juridique, pour soit enregistrer ces generateurs dans le catalogue/orchestrateur avec `doc_id` et conditions explicites, soit les reclasser formellement hors perimetre V1 assume.
