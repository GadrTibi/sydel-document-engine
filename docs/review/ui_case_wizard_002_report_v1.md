# Rapport UI-CASE-WIZARD-002

## Objet

Brancher le mode `Assistant metier` Streamlit sur le catalogue metier
`CASE-CATALOG-001`, afin que la liste des documents attendus soit derivee de
`get_expected_documents(...)` et de la source de verite
`project/source_truth/Documents_a_generer_par_cas.docx`.

## Etat Git initial

- Branche : `main`.
- Dernier commit avant ticket : `7ee6d4f feat: add case document catalog v1`.
- CASE-CATALOG-001 present.
- Working tree non strictement clean avant intervention : dossier non suivi
  preexistant `docs/docssource_truth/`, laisse hors scope et non stage.

## Fichiers modifies

- `src/sydel_doc_engine/app/business_wizard.py`
- `src/sydel_doc_engine/app/ui_runtime.py`
- `src/sydel_doc_engine/app/streamlit_app.py`
- `tests/unit/test_business_wizard.py`
- `docs/review/ui_case_wizard_002_report_v1.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/04_LAST_STATE.md`

## Logique UI ajoutee

- Ajout d'une couche de conditions UI par famille via
  `get_ui_conditions_for_case(case_type)`.
- Les 8 familles du catalogue sont exposees dans le mode Assistant metier :
  `SELARL`, `SELAS`, `SPFPL cession`, `SPFPL apport`, `SCS`, `SCI`, `SCM`,
  `SAS`.
- Les conditions sensibles ne sont plus choisies par defaut silencieux :
  `SCI simple / SCI IRIS`, `associe unique`, `cession de parts / actions`,
  options oui/non et type de cabinet doivent etre explicitement renseignes
  quand ils pilotent la selection.
- Le nombre d'associes reste collecte comme signal UI, sans resoudre dans ce
  ticket toute la generation variable des associes.

## Utilisation du catalogue

`evaluate_business_wizard(...)` construit un `CaseInput` puis appelle
`get_expected_documents(...)`. Le tableau documentaire affiche chaque
`ExpectedDocument` avec :

- code document si disponible ;
- libelle document ;
- statut ;
- raison de presence ;
- notes et limites de generation.

Les statuts affiches distinguent :

- `Generable` ;
- `A remplir manuellement` ;
- `Non implemente` ;
- `Mapping a confirmer` ;
- `Bloque par champs manquants` ;
- `Contexte incomplet pour generation V2`.

## Cas affichables

Tous les cas de `CaseType` sont affichables dans l'assistant :

- SELARL : profession, site distinct, SCM cession, regime communautaire,
  derogation, cession, type de cabinet si cession.
- SELAS : profession, SCM, regime communautaire, derogation, cession, type de
  cabinet si cession.
- SPFPL cession : regime communautaire, associe unique, cession de parts ou
  d'actions.
- SPFPL apport : regime communautaire.
- SCI : SCI simple / SCI IRIS, option IS.
- SCS, SCM : pas de condition metier specifique V1.
- SAS : associe unique collecte comme vigilance UI.

## Cas generables

La generation automatique du mode Assistant est volontairement filtree :

- seuls les documents `DocumentAvailability.GENERATABLE` ;
- avec un `document_code` non vide ;
- marques comme prets par la validation du contexte formulaire ;
- sont transmis a `generate_docx_files_for_document_codes(...)`.

En pratique, le formulaire V2 sait encore construire un contexte fiable pour le
socle deja recette `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`. Les autres
documents attendus restent visibles, mais sont marques `Contexte incomplet pour
generation V2` tant que le formulaire ne collecte pas leurs champs complets.

## Documents manuels visibles

Les documents `MANUAL_ONLY` restent visibles et exclus de la generation :

- formulaire de declaration prealable de site distinct CD94 avec la SEL ;
- derogation SEL BNC.

## Documents non implementes visibles

Le document `NOT_IMPLEMENTED` reste visible et exclu de la generation :

- demande de derogation cumul SELARL salariee, source legacy `.doc` non
  convertie en DOCX propre dans le moteur V1.

## Vigilances traitees

- SELAS + SCM : une reserve est affichee lorsque `SELAS` + `SCM` est actif,
  car le catalogue mappe le bloc vers `DOC-031`, `DOC-032`, `DOC-033` alors que
  la source mentionne des fichiers SELAS specifiques.
- SCI IRIS : le catalogue affiche `DOC-021` et n'affiche pas `DOC-020`.
- Option IS : `DOC-022` est affiche lorsque l'option IS est active, mais reste
  bloque tant que le formulaire ne collecte pas le contexte fiscal et statutaire
  complet.
- Documents manuels et non implementes : visibles dans le tableau, jamais
  envoyes a la generation automatique.

## Limites connues

- Le mode Assistant ne pretend pas generer un dossier complet pour toutes les
  familles.
- Les statuts, regime communautaire, cession cabinet, SPFPL, SCM satellites,
  option IS et demande d'inscription a l'ordre peuvent etre attendus par le
  catalogue mais restent incomplets cote formulaire V2.
- Le mode Technique / diagnostic YAML/JSON reste le moyen de piloter des
  contextes complets hors assistant.
- Aucun generateur, aucune formulation juridique source et aucun moteur
  DOCX/PDF/ZIP de production n'ont ete modifies.

## Tests lances

- `.\.venv\Scripts\python.exe -m ruff check .`
- `.\.venv\Scripts\python.exe -m pytest`

## Resultats des tests

- Ruff : OK.
- Pytest : OK, 217 tests passes.

## Prochaine etape recommandee

Lancer un ticket `UI-CASE-WIZARD-003` pour enrichir progressivement les blocs de
formulaire permettant de rendre prets les documents aujourd'hui marques
`Contexte incomplet pour generation V2`, en commencant par un seul lot ou une
seule famille documentaire.
