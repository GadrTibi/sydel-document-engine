# Rapport FRONT-DATA-LAYER-001

Date : 2026-05-24

## 1. Sources utilisees

- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`
- `docs/project/GLOBAL_VARIABLE_IDENTITY_MATRIX_V1.csv`
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`
- `docs/project/GLOBAL_FRONT_RULES_V1.md`
- `docs/project/GLOBAL_FRONT_SCREEN_STRATEGY_V1.md`
- `docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv`
- `docs/review/global_front_architecture_qa_001_report_v1.md`
- `docs/review/global_human_answers_integration_001_report_v1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `src/sydel_doc_engine/registry/catalog.py`
- References secondaires lues : `src/sydel_doc_engine/domain/models.py`,
  `src/sydel_doc_engine/app/selarl_form_schema.py`,
  `src/sydel_doc_engine/app/business_wizard.py`.

## 2. Objets crees

Package cree : `src/sydel_doc_engine/front_data/`.

Objets principaux :

- `PersonRecord`
- `CompanyRecord`
- `AddressRecord`
- `RoleAssignment`
- `DossierRecord`
- `OperationContext`
- `DocumentRequirementRecord`
- `CanonicalFieldValue`
- `ReuseRuleState`
- `ValidationIssue`

Enums structurants :

- `BusinessRole`
- `AddressUsage`
- `OperationType`
- `CanonicalRelationType`
- `FieldFormKind`
- `ReuseRuleStatus`
- `ValidationIssueType`

Modules :

- `models.py` : objets pivots de la couche data, sans dependance Streamlit.
- `canonical_mapping.py` : mapping initial registre V2.1 vers objets front,
  aliases legacy documentaires, exigences sentinelles.
- `validation.py` : diagnostics data-layer.

## 3. Decisions de modelisation

- Une personne est creee une seule fois puis rattachee a des roles explicites par
  `RoleAssignment`.
- Les societes restent des `CompanyRecord` distincts, meme si denomination ou adresse
  coincident.
- Les adresses sont typees par `AddressUsage`. Aucune adresse n'est fusionnee par
  egalite de texte ou de composants.
- `domiciliation = siege_social` et `siege_social = lieu_exercice` passent par
  `ReuseRuleState`, jamais par une regle implicite.
- Les relations de matrice sont portees par `CanonicalRelationType` :
  `SAME_FIELD`, `SAME_DATA_DIFFERENT_SHAPE`, `EXPLICIT_REUSE_ONLY`,
  `DISTINCT_FIELDS`, `UNCERTAIN_REQUIRES_HUMAN_DECISION`.
- Les aliases legacy, dont `domiciliation.adresse_domiciliation_affichee`, sont
  modelises comme formes documentaires (`DOCUMENTARY_ALIAS`) et non comme champs
  metier concurrents.
- Les operations sensibles (`ordre`, `cession`, `apport`, `cession_parts_scm`,
  `bail`, `financement`, `regime_communautaire`, `derogation`) sont portees par
  `OperationContext` et les champs canoniques associes.

## 4. Couverture sentinelles

| Document | Verdict QA | Couverture data-layer |
|---|---:|---|
| `DOC-002` | VERT | Couvert : roles signataire/praticien/societe, siege/domiciliation, alias legacy documentaire. |
| `DOC-034` | ORANGE | Couvert : signataire, mandataire, ordre, derogation comme champ dossier ; modele ordre a affiner ensuite. |
| `DOC-017` | ORANGE | Couvert : associes, praticien, gerant, banque, ordre, capital/titres/repartition. |
| `DOC-033` | VERT | Couvert : cedant, conjoint, cessionnaire, representant, SCM cedee, adresses distinctes. |
| `DOC-009` | ORANGE | Couvert : cession cabinet, bail, financement, exercices, prix, parties distinctes. |
| `DOC-041` | ORANGE | Couvert : apport_titres, SPFPL, societe cible, evaluateur, commissaire. |
| `DOC-025` | ORANGE | Couvert : SCM, associes[], representant personne morale, banque, apports/parts. |

Le test unitaire compare les codes du mapping a
`docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv`.

## 5. Diagnostics couverts

Helpers crees :

- role manquant ;
- adresse typee manquante ;
- conflit de reutilisation ;
- ambiguite non resolue ;
- valeur canonique absente ;
- entite requise non liee.

Les validations bloquent les reutilisations activees sur `DISTINCT_FIELDS` ou
`UNCERTAIN_REQUIRES_HUMAN_DECISION`.

## 6. Ce qui reste non couvert

- Pas d'UI visible.
- Pas de schema de formulaire definitif.
- Pas de mapping complet de tous les champs du registre V2.1.
- Pas de calcul metier capital/titres/apports.
- Pas de validation juridique de wording.
- Pas de modification des generateurs, du moteur DOCX/PDF/ZIP ou de Streamlit.

## 7. Ce qu'on garde du prototype

- Garder le prototype Streamlit comme outil de diagnostic, de lancement manuel et de
  comparaison ponctuelle.
- Ne pas reutiliser son `session_state` comme modele de donnees.
- Ne pas generaliser ses noms de champs historiques.
- Migrer uniquement les enseignements utiles : modes de test, prefill deterministe,
  distinction parcours dossier vs document unitaire.

## 8. Tests

Tests ajoutes :

- `tests/unit/test_front_data_layer.py`

Validation cible executee pendant le ticket :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_data_layer.py`
  : OK, 16 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 288 tests passes.

## 9. Prochaine etape recommandee

Lancer `FRONT-ROLE-MODEL-001`.

Ce ticket doit raffiner les roles fins deja poses par la data layer :
signataire, mandataire, representant personne morale, cedant, cessionnaire,
apporteur, evaluateur, commissaire et roles d'ordre. Il doit rester hors UI visible
et hors generateurs.
