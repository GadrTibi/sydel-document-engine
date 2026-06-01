# SELARL closing pack 003 report V1

Ticket : `SELARL-CLOSING-PACK-003`

Date : 2026-06-01

Statut : `DONE - historique, remplace par pack 004`

Note 2026-06-01 : ce pack ne doit plus etre transmis a l'associe. L'audit trois
sources a trouve un ecart restant dans `DOC-003` procuration (`SELARL SELARL`).
Le pack actif est desormais `artifacts/selarl_closing_pack_004/`.

## Decision

Le pack 003 remplace le pack 002.

Raison : l'audit approfondi du fichier `Retours humains .docx` a detecte trois
ecarts dans le `DOC-004` PV nomination gerant. Ces ecarts sont corriges dans le
generateurs et dans le pack 003.

## Pack

Racine :

- `artifacts/selarl_closing_pack_003/`

Manifest :

- `artifacts/selarl_closing_pack_003/manifest_selarl_closing_pack_003.json`

## Scenarios generes

| Scenario | Dossier | DOCX | ZIP | `DOC-005` / `DOC-006` |
| --- | --- | ---: | --- | --- |
| Medecin simple | `artifacts/selarl_closing_pack_003/medecin_simple/` | 6 | `dossier_generation.zip` | Absents, correct hors regime |
| Dentiste simple | `artifacts/selarl_closing_pack_003/dentiste_simple/` | 6 | `dossier_generation.zip` | Absents, correct hors regime |
| Medecin regime communautaire | `artifacts/selarl_closing_pack_003/medecin_regime_communautaire/` | 8 | `dossier_generation.zip` | Presents |
| Dentiste regime communautaire | `artifacts/selarl_closing_pack_003/dentiste_regime_communautaire/` | 8 | `dossier_generation.zip` | Presents |

## Controles manifest

Tous les scenarios indiquent :

- ZIP present ;
- aucun placeholder `[` / `]` ;
- aucun parasite connu `RCS PARIS 788 531 432` / `0153814303` ;
- `DOC-005` et `DOC-006` presents uniquement si regime communautaire ;
- PV sans `au RCS de ...` ;
- PV avec `En cours d’immatriculation` ;
- PV avec `DE L’ASSEMBLEE GENERALE` ;
- PV sans `EXTRAORDINAIRE` ;
- PV sans doublon `SELARL SELARL`.

Scenarios regime communautaire :

- renonciation : `À {ville}` ;
- renonciation : `euros dépendant de notre communauté.` ;
- avertissement conjoint : adresse du conjoint presente.

## Corrections incluses depuis pack 002

`DOC-004` :

- conserver `En cours d’immatriculation` ;
- supprimer uniquement la suite `au RCS de ...` ;
- conserver `DE L’ASSEMBLEE GENERALE` dans le titre ;
- supprimer `EXTRAORDINAIRE` ;
- eviter `SELARL SELARL` dans l'introduction si la denomination contient deja
  la forme sociale.

## Validation

- `pytest tests/unit/test_pv_nomination_gerant.py tests/unit/test_clean_front_app.py -q` : 34 passes.
- Tests cibles retours humains/documents : 76 passes.
- `ruff check .` : OK.
- `pytest -q` : 415 passes.
