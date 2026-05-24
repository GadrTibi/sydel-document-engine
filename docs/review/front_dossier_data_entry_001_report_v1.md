# Rapport FRONT-DOSSIER-DATA-ENTRY-001

Date : 2026-05-24

## 1. Perimetre

Ce ticket ajoute la premiere saisie reelle du nouvel editeur dossier, limitee au
profil prudent `SELARL creation simple`.

Il ne modifie ni les generateurs, ni le moteur DOCX/PDF/ZIP, ni le wording
juridique. Le prototype historique reste disponible dans `Prototype / outils de
test`.

## 2. Sources utilisees

- `docs/review/front_dossier_editor_001_report_v1.md`
- `docs/review/front_data_layer_001_report_v1.md`
- `docs/review/front_role_model_001_report_v1.md`
- `docs/review/front_address_model_001_report_v1.md`
- `docs/review/front_dossier_flow_001_report_v1.md`
- `docs/review/front_document_status_layer_001_report_v1.md`
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`
- `docs/project/GLOBAL_FRONT_RULES_V1.md`
- `docs/project/GLOBAL_FRONT_SCREEN_STRATEGY_V1.md`
- `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`
- `src/sydel_doc_engine/app/front_dossier_editor.py`
- `src/sydel_doc_engine/app/front_shell.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `src/sydel_doc_engine/front_data/models.py`
- `src/sydel_doc_engine/front_data/dossier_flow.py`
- `src/sydel_doc_engine/front_data/document_status.py`
- `src/sydel_doc_engine/front_data/validation.py`
- `src/sydel_doc_engine/front_data/canonical_mapping.py`

ADR applicables : ADR-0001 source de verite documentaire, ADR-0002 moteur par
document canonique et ADR-0005 mode de travail Codex/repo-first.

## 3. Ce qui est maintenant saisissable

Dans `Nouveau front global > Dossier`, le profil `SELARL creation simple` expose
une tranche de saisie V1 :

- `Dossier unipersonnel` ;
- personne principale : civilite, genre, prenom, nom, naissance, nationalite,
  filiation et adresse personnelle ;
- societe principale : denomination, forme sociale, capital social, siege social ;
- domiciliation, avec option explicite `domiciliation = siege social` ;
- capital simple : nombre total de titres, valeur nominale, repartition associes ;
- decision, reunion et signature : dates, heure, lieu et nombre d'exemplaires.

Les autres profils (`ordre`, `cession cabinet`, `SCM`, `SPFPL`) restent en lecture
flow/statuts afin de ne pas resoudre artificiellement les zones orange.

## 4. Alimentation du DossierRecord

Nouveau module :

- `src/sydel_doc_engine/app/front_dossier_entry.py`

Le module reste pur et ne depend pas de Streamlit. Il transforme une
`FrontDossierSimpleEntry` en `DossierRecord`.

Objets alimentes :

- `PersonRecord` pour la personne principale ;
- `CompanyRecord` pour la societe principale ;
- `AddressRecord` pour `adresse_personnelle`, `siege_social` et `domiciliation` ;
- `RoleAssignment` pour `praticien`, `associe`, `gerant`, `signataire` et
  `societe_principale` ;
- `ReuseRuleState` pour `Dossier unipersonnel` et `domiciliation = siege social` ;
- `CanonicalFieldValue` pour les champs requis par `DOC-001` a `DOC-004`.

Le role `signataire` est scope au lot V1, pas globalise silencieusement au dossier.
Les roles `associe`, `gerant` et `signataire` pointent vers la meme personne
uniquement quand `Dossier unipersonnel` est actif et trace.

## 5. Impact sur les statuts documentaires

Apres saisie, l'editeur reconstruit :

- le `DossierFlow` ;
- les blocs actifs ;
- les exigences documentaires ;
- le `DocumentStatusSummary` ;
- le statut de lot.

Avec les donnees minimales completes du cas simple, `DOC-001`, `DOC-002`,
`DOC-003` et `DOC-004` passent a `generable` dans la couche de statuts.

Si la saisie est incomplete, les documents restent `blocked_missing_data` avec les
roles, adresses ou valeurs canoniques manquants.

## 6. Ce qui reste placeholder

- Pas d'overrides avances depuis l'UI.
- Pas de generation DOCX/PDF/ZIP depuis le nouveau front.
- Pas de saisie ordre, mandataire, SCM, SPFPL, cession cabinet, bail ou
  financement.
- Pas d'adaptateur `DossierRecord` vers contexte moteur.
- Pas de migration du vieux `session_state` du prototype.

Ces sujets restent pour les tickets suivants.

## 7. Decisions de modelisation

- La saisie V1 ne cree pas une deuxieme logique de formulaire metier : Streamlit
  collecte les champs, puis `front_dossier_entry.py` construit le `DossierRecord`.
- Les adresses restent typees meme quand le siege et la domiciliation ont la meme
  valeur affichee.
- La domiciliation derivee reference explicitement la regle
  `address:siege_social -> address:domiciliation`.
- La repartition associe peut etre derivee prudemment du dossier unipersonnel si
  le nombre de titres et le nom de la personne sont presents.
- Le profil hors scope reste visible mais read-only, afin de garder les blocages
  orange honnetes.

## 8. Tests

Tests ajoutes :

- `tests/unit/test_front_dossier_data_entry.py`

Couverture :

- saisie personne vers `DossierRecord.persons` ;
- saisie societe vers `DossierRecord.companies` ;
- saisie adresses vers `DossierRecord.addresses` ;
- `Dossier unipersonnel` vers roles explicites ;
- `domiciliation = siege social` via `ReuseRuleState` ;
- recalcul des statuts documentaires apres saisie ;
- progression `DOC-001` a `DOC-004` ;
- non-regression shell/prototype.

Validation cible executee pendant le ticket :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_dossier_data_entry.py tests/unit/test_front_dossier_editor.py tests/unit/test_front_ui_shell.py -q`
  : OK, 22 tests passes.

Validation finale :

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 374 tests passes.

## 9. Prochaine etape recommandee

Lancer `FRONT-DOCUMENTS-PANEL-001`.

Le panneau Documents attendus peut maintenant s'appuyer sur un dossier saisi
partiellement, pas seulement sur une vitrine read-only. Il doit consolider les
statuts, reserves, blocages, documents manuels et statuts de lot avant toute
action de generation.
