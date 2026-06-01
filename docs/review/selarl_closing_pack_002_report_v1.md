# SELARL closing pack 002 report V1

Note 2026-06-01 : ce pack est historique. Il est remplace par
`artifacts/selarl_closing_pack_003/` apres audit approfondi des retours humains
sur le `DOC-004` PV nomination gerant.

Ticket : `SELARL-CLOSING-PACK-002`

Date : 2026-06-01

## Decision

`GO validation finale associe`, `NO-GO extension complexe`.

Le pack 002 remplace le pack 001. La difference principale est la correction du
regime communautaire : `DOC-006` est maintenant genere avec `DOC-005`.

## Pack produit

Racine artefacts :

- `artifacts/selarl_closing_pack_002/`

Manifest :

- `artifacts/selarl_closing_pack_002/manifest_selarl_closing_pack_002.json`

## Scenarios generes

| Scenario | Dossier | Documents DOCX | ZIP | Controle `DOC-006` |
| --- | --- | ---: | --- | --- |
| Medecin simple | `artifacts/selarl_closing_pack_002/medecin_simple/` | 6 | `dossier_generation.zip` | Absent, correct hors regime |
| Dentiste simple | `artifacts/selarl_closing_pack_002/dentiste_simple/` | 6 | `dossier_generation.zip` | Absent, correct hors regime |
| Medecin regime communautaire | `artifacts/selarl_closing_pack_002/medecin_regime_communautaire/` | 8 | `dossier_generation.zip` | Present |
| Dentiste regime communautaire | `artifacts/selarl_closing_pack_002/dentiste_regime_communautaire/` | 8 | `dossier_generation.zip` | Present |

## Documents produits

### Medecin simple

- `DOC-001` declaration de non-condamnation
- `DOC-002` autorisation de domiciliation
- `DOC-003` procuration
- `DOC-004` PV nomination gerant
- `DOC-034` demande d'inscription a l'ordre
- `DOC-017` statuts SELARL medecin

### Dentiste simple

- `DOC-001` declaration de non-condamnation
- `DOC-002` autorisation de domiciliation
- `DOC-003` procuration
- `DOC-004` PV nomination gerant
- `DOC-034` demande d'inscription a l'ordre
- `DOC-016` statuts SELARL chirurgien-dentiste

### Medecin regime communautaire

- `DOC-001` declaration de non-condamnation
- `DOC-002` autorisation de domiciliation
- `DOC-003` procuration
- `DOC-004` PV nomination gerant
- `DOC-034` demande d'inscription a l'ordre
- `DOC-005` lettre de renonciation a revendiquer la qualite d'associe
- `DOC-006` lettre d'avertissement au conjoint
- `DOC-017` statuts SELARL medecin

### Dentiste regime communautaire

- `DOC-001` declaration de non-condamnation
- `DOC-002` autorisation de domiciliation
- `DOC-003` procuration
- `DOC-004` PV nomination gerant
- `DOC-034` demande d'inscription a l'ordre
- `DOC-005` lettre de renonciation a revendiquer la qualite d'associe
- `DOC-006` lettre d'avertissement au conjoint
- `DOC-016` statuts SELARL chirurgien-dentiste

## Controles effectues

- ZIP produit pour chaque scenario.
- `DOC-006` present uniquement dans les scenarios regime communautaire.
- Aucun placeholder `[` / `]` detecte dans les DOCX generes.
- Parasites connus `RCS PARIS 788 531 432` et `0153814303` absents.
- La renonciation contient la formulation communaute attendue.
- L'avertissement conjoint contient l'adresse du conjoint.
- `ruff check .` OK.
- Tests cibles SELARL/documents : 83 passes.
- `pytest -q` complet : 415 passes.

## Points a faire verifier par l'associe

La revue finale ne doit pas reprendre des questions abstraites. Elle doit
verifier au document :

1. qu'il n'y a pas d'ecart de texte par rapport aux sources attendues ;
2. que les variables injectees sont au bon endroit ;
3. que `DOC-006` est present quand le regime communautaire est actif ;
4. que `DOC-006` est absent hors regime communautaire ;
5. que le ZIP contient exactement les documents attendus.

## Prochaine action

Lancer `SELARL-FINAL-ASSOCIE-VALIDATION-001` avec le brief :

- `docs/review/selarl_final_validation_001_brief_v1.md`
