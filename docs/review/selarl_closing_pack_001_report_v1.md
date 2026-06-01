# SELARL closing pack 001 report V1

Ticket : `SELARL-CLOSING-PACK-001`

Date : 2026-06-01

Note 2026-06-01 : ce pack est historique et remplace par
`docs/review/selarl_closing_pack_002_report_v1.md`. Le pack 001 excluait
`DOC-006`; le pack 002 corrige cette erreur et genere `DOC-006` quand le regime
communautaire est actif.

## Decision

`GO recette`, `NO-GO dev`.

Le ticket a regenere le pack de revue SELARL simple sans modifier le code, les
generateurs, le moteur DOCX/PDF/ZIP, les sources de verite ni le wording
juridique.

## Pourcentage d'avancement

Estimation PM au 2026-06-01 apres generation du pack :

| Perimetre | Avancement | Lecture |
| --- | ---: | --- |
| SELARL globale, tous cas confondus | 70 % | Le coeur simple est avance, mais cession, SCM, site distinct, derogations, statuts multi-associes complets, plusieurs gerants et president externe restent a cadrer. |
| SELARL simple cloturable | 90 % | Les packs medecin, dentiste et regime communautaire sont produits et testes ; il manque la revue associe / juriste, puis les corrections eventuelles. |
| Fin de sprint SELARL simple | 35 % | Cadrage et pack sont faits ; revue humaine, triage, corrections, smoke final et cloture canonique restent a faire. |

## Pack produit

Racine artefacts :

- `artifacts/selarl_closing_pack_001/`

Scenarios generes :

| Scenario | Dossier | Documents DOCX | ZIP |
| --- | --- | ---: | --- |
| Medecin simple | `artifacts/selarl_closing_pack_001/medecin_simple/` | 6 | `dossier_generation.zip` |
| Dentiste simple | `artifacts/selarl_closing_pack_001/dentiste_simple/` | 6 | `dossier_generation.zip` |
| Medecin regime communautaire | `artifacts/selarl_closing_pack_001/medecin_regime_communautaire/` | 7 | `dossier_generation.zip` |

Manifest :

- `artifacts/selarl_closing_pack_001/manifest_selarl_closing_pack_001.json`

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
- `DOC-017` statuts SELARL medecin

## Documents reserves, manuels ou exclus

| Document | Statut | Decision |
| --- | --- | --- |
| `DOC-006` avertissement conjoint | Reserve | Non genere, absent des ZIP. |
| `DOC-013` / `DOC-014` derogations | Manuel / hors V1 | Non genere. |
| Site distinct | Manuel / hors V1 | Non genere. |
| Cession cabinet medicale / dentaire | Bloque | Nouveau sous-cas requis. |
| Cession SCM | Bloque | Nouveau sous-cas requis. |
| Statuts multi-associes complets | Bloque | Source humaine / spec requise. |
| Plusieurs gerants | Bloque | Source humaine / spec requise. |
| President externe | Bloque | Source humaine / spec requise. |

## Controles effectues

- ZIP produit pour chaque scenario.
- `DOC-006` absent des fichiers DOCX et des ZIP.
- Aucun placeholder `[` / `]` detecte dans les DOCX generes.
- Parasites connus `RCS PARIS 788 531 432` et `0153814303` absents.
- Tests cibles SELARL : 5 passes.

Commande de test :

```text
.\.venv\Scripts\python.exe -m pytest tests/unit/test_clean_front_app.py::test_clean_front_selarl_slice_is_generable_for_medecin tests/unit/test_clean_front_app.py::test_clean_front_selarl_slice_switches_statuts_for_dentiste tests/unit/test_clean_front_app.py::test_clean_front_selarl_slice_adds_doc_005_only_for_regime tests/unit/test_clean_front_app.py::test_clean_front_selarl_generation_smoke tests/unit/test_clean_front_app.py::test_clean_front_selarl_medecin_regime_communautaire_generation_smoke -q
```

Resultat :

```text
5 passed
```

## Note de revue pour l'associe

La revue humaine doit verifier en priorite :

1. `DOC-034` demande d'inscription a l'ordre, encore PARTIAL faute de lock humain specifique.
2. `DOC-016` statuts dentiste, surtout le wrapper post-article.
3. `DOC-017` statuts medecin, source-level locked mais sans retour humain medecin recent equivalent au dentiste.
4. La coherence des variables dossier sur les documents courts `DOC-001` a `DOC-004`.
5. L'absence de document reserve `DOC-006` dans le pack regime communautaire.

## Prochaine action

Lancer `SELARL-ASSOCIE-REVIEW-001` : transmettre ou faire tester ce pack par
l'associe / juriste, puis revenir avec une validation explicite ou des retours
classes.

Tant que ce retour humain n'est pas recu, `SELARL-REVIEW-TRIAGE-001`,
`SELARL-REVIEW-FIXES-001`, `SELARL-CLOSING-SMOKE-001` et
`SELARL-CANONICAL-CLOSE-001` restent bloques.
