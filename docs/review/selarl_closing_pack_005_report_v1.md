# SELARL closing pack 005 report V1

Ticket : `SELARL-CLOSING-PACK-005`

Date : 2026-06-02

Statut : `DONE - pack apres retours humains 006`

## Decision

Le pack 005 remplace le pack 004 pour la prochaine validation associe.

Raison : tous les tickets `SELARL-RETURNS-006-*` sont corriges cote code/test,
puis le pack a ete regenere et controle par manifest.

## Pack

Racine :

- `artifacts/selarl_closing_pack_005/`

Manifest :

- `artifacts/selarl_closing_pack_005/manifest_selarl_closing_pack_005.json`

## Scenarios generes

| Scenario | Dossier | DOCX | ZIP | `DOC-005` / `DOC-006` |
| --- | --- | ---: | --- | --- |
| Medecin simple | `artifacts/selarl_closing_pack_005/medecin_simple/` | 6 | `dossier_generation.zip` | Absents, correct hors regime |
| Dentiste simple | `artifacts/selarl_closing_pack_005/dentiste_simple/` | 6 | `dossier_generation.zip` | Absents, correct hors regime |
| Medecin regime communautaire | `artifacts/selarl_closing_pack_005/medecin_regime_communautaire/` | 8 | `dossier_generation.zip` | Presents |
| Dentiste regime communautaire | `artifacts/selarl_closing_pack_005/dentiste_regime_communautaire/` | 8 | `dossier_generation.zip` | Presents |

## Controles manifest

Tous les scenarios indiquent :

- ZIP present ;
- nombre de DOCX attendu ;
- aucun placeholder `[` / `]` ;
- aucun parasite connu `RCS PARIS 788 531 432` / `0153814303` ;
- aucun doublon `SELARL SELARL` ;
- `DOC-005` et `DOC-006` presents uniquement si regime communautaire ;
- demande d'inscription a l'Ordre composee depuis profession + departement ;
- PV avec forme juridique redigee et capital `Au capital de ...` ;
- procuration avec `demeurant..., agissant...` sur la meme phrase ;
- declaration de non condamnation avec ville de naissance ;
- autorisation de domiciliation avec `pour 99 ans` ;
- adresses avec code postal avant ville ;
- signatures non encadrees sur `DOC-001`, `DOC-002`, `DOC-003` ;
- `DOC-006` avec quatre exemplaires ;
- adresse conjoint de `DOC-006` derivee de l'adresse personnelle ;
- statuts regime communautaire avec clause matrimoniale ;
- accord feminin `associee unique` dans les statuts quand l'associee est une femme.

Manifest : 4 scenarios, 0 echec.

## Corrections detectees pendant la generation pack

Deux ecarts ont ete detectes pendant l'audit du premier manifest 005, puis
corriges avant ce rapport :

- `DOC-006` affichait encore `Fait en trois exemplaires` ; corrige en `Fait en quatre exemplaires`.
- `DOC-016` dentiste pouvait rendre une formule non accordee / incomplete autour de `associe unique` ; corrige via le placeholder d'accord existant.

Amendement 2026-06-03 :

- `DOC-002` affichait encore `pour une duree indeterminee` dans l'autorisation
  de domiciliation ; corrige en `pour 99 ans` et pack 005 regenere localement.
- Manifest enrichi avec le controle `doc002_duration_99_years=true`.
- Rapport incident :
  `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`.

## Validations

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_lot_04_statuts_sel_exercice.py tests/unit/test_regime_communautaire.py -q` : OK, 25 tests passes.
- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_demande_inscription_ordre.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_front_dossier_data_entry.py tests/unit/test_business_wizard.py tests/unit/test_single_document_mode.py tests/unit/test_lot_04_statuts_sel_exercice.py tests/unit/test_pv_nomination_gerant.py tests/unit/test_declaration_non_condamnation.py tests/unit/test_autorisation_domiciliation.py tests/unit/test_procuration.py tests/unit/test_regime_communautaire.py -q` : OK, 166 tests passes.
- Amendement 2026-06-03 :
  `.\.venv\Scripts\python.exe -m pytest tests/unit/test_demande_inscription_ordre.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_front_dossier_data_entry.py tests/unit/test_business_wizard.py tests/unit/test_single_document_mode.py tests/unit/test_lot_04_statuts_sel_exercice.py tests/unit/test_pv_nomination_gerant.py tests/unit/test_declaration_non_condamnation.py tests/unit/test_autorisation_domiciliation.py tests/unit/test_procuration.py tests/unit/test_regime_communautaire.py tests/unit/test_selarl_form_schema.py -q`
  : OK, 187 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check ...` sur fichiers touches SELARL 006 : OK.

## Suite

Prochain ticket recommande : `SELARL-HUMAN-RETURNS-DEEP-AUDIT-006`.
