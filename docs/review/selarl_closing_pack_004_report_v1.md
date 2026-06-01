# SELARL closing pack 004 report V1

Ticket : `SELARL-CLOSING-PACK-004`

Date : 2026-06-01

Statut : `DONE - pack de validation associe apres audit trois sources`

## Decision

Le pack 004 remplace le pack 003.

Raison : l'audit trois sources a detecte un ecart restant dans le `DOC-003`
procuration du pack 003 : la designation de societe pouvait afficher
`SELARL SELARL MARTIN` quand la denomination contenait deja la forme sociale.

## Pack

Racine :

- `artifacts/selarl_closing_pack_004/`

Manifest :

- `artifacts/selarl_closing_pack_004/manifest_selarl_closing_pack_004.json`

## Scenarios generes

| Scenario | Dossier | DOCX | ZIP | `DOC-005` / `DOC-006` |
| --- | --- | ---: | --- | --- |
| Medecin simple | `artifacts/selarl_closing_pack_004/medecin_simple/` | 6 | `dossier_generation.zip` | Absents, correct hors regime |
| Dentiste simple | `artifacts/selarl_closing_pack_004/dentiste_simple/` | 6 | `dossier_generation.zip` | Absents, correct hors regime |
| Medecin regime communautaire | `artifacts/selarl_closing_pack_004/medecin_regime_communautaire/` | 8 | `dossier_generation.zip` | Presents |
| Dentiste regime communautaire | `artifacts/selarl_closing_pack_004/dentiste_regime_communautaire/` | 8 | `dossier_generation.zip` | Presents |

## Controles manifest

Tous les scenarios indiquent :

- ZIP present ;
- aucun placeholder `[` / `]` ;
- aucun parasite connu `RCS PARIS 788 531 432` / `0153814303` ;
- aucun doublon `SELARL SELARL` dans l'ensemble du dossier ;
- `DOC-005` et `DOC-006` presents uniquement si regime communautaire ;
- PV sans `au RCS de ...` ;
- PV avec `En cours d'immatriculation` ;
- PV avec `DE L'ASSEMBLEE GENERALE` ;
- PV sans `EXTRAORDINAIRE` ;
- procuration avec clause finale `Fait pour servir et valoir ce que de droit.`.

Scenarios regime communautaire :

- renonciation : `A/À {ville}` corrige ;
- renonciation : `euros dependant de notre communaute.` corrige ;
- avertissement conjoint : adresse du conjoint presente.

## Correction incluse depuis pack 003

`DOC-003` :

- si la denomination commence deja par la forme sociale ou son abreviation, le
  generateur ne prefixe pas une seconde fois ;
- exemple corrige : `de SELARL MARTIN`, pas `de SELARL SELARL MARTIN`.

## Validation

- `pytest tests/unit/test_procuration.py tests/unit/test_clean_front_app.py -q` : 34 passes.
- `ruff check src/sydel_doc_engine/generators/lot_01/procuration.py tests/unit/test_procuration.py tests/unit/test_clean_front_app.py` : OK.
- `ruff check .` : OK.
- `pytest -q` : 416 passes.
- Controle manifest pack 004 : 4 scenarios, aucun check en echec.

Le pack 004 remplace le pack 003 pour la validation associe.
