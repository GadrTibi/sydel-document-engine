# TRACK-B-SELARL-MEDECIN-REGIME-COMMUNAUTAIRE-005 - Rapport V1

## Contexte prouve

- `pwd` : `C:\Users\Gad\Desktop\Sydel\sydel-track-b`
- `git rev-parse --show-toplevel` : `C:/Users/Gad/Desktop/Sydel/sydel-track-b`
- `git branch --show-current` : `track-b/clean-rebuild`
- `git rev-parse HEAD` : `cc54110df73fe5b3df2268710c38b2d6d6d0d05f`
- `git status --short --branch` : worktree deja modifiee par les tickets Track B SELARL precedents, aucun reset effectue.

## References lues

- `docs/review/track_b_selarl_medecin_line_by_line_lock_004_report_v1.md`
- `docs/review/track_b_selarl_dentist_line_by_line_lock_003_report_v1.md`
- `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md`
- `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md`
- `docs/project/SELARL_PRODUCTION_FACTORY_V1.md`
- `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md`
- `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`
- `src/sydel_doc_engine/front_app/selarl_slice.py`
- `src/sydel_doc_engine/front_app/shell.py`
- `src/sydel_doc_engine/front_app/data_entry.py`
- `tests/unit/test_clean_front_app.py`
- `tests/unit/test_regime_communautaire.py`

## Decision

Decision : GO, sans changement de wording juridique.

Le cas `SELARL medecin unipersonnelle + regime communautaire` etait deja cable dans le clean front Track B :

- `profession=medecin` selectionne `DOC-017` et l'overlay `selarl_medecin` ;
- `regime_communautaire=True` ajoute `DOC-005` ;
- `DOC-006` reste reserve et exclu de la generation V1 bornee ;
- le conjoint et la date du courrier d'avertissement sont requis uniquement quand le regime communautaire est actif ;
- le cas medecin standard reste sans conjoint et sans `DOC-005`.

Le delta du ticket est donc une industrialisation de preuve : test cible, smoke reel, rapport et backlog.

## Ce qui est reutilise

- Locks documents courts herites :
  - `DOC-001` declaration de non-condamnation ;
  - `DOC-002` autorisation de domiciliation ;
  - `DOC-003` procuration ;
  - `DOC-004` PV de nomination de gerant ;
  - `DOC-005` lettre de renonciation du conjoint.
- Lock source-level `DOC-017` medecin unipersonnelle standard du ticket `004`.
- Clean front Track B `src/sydel_doc_engine/front_app/`.
- Derivations deja etablies :
  - praticien = associe unique = gerant = signataire ;
  - siege = domiciliation ;
  - capital / parts / valeur nominale ;
  - president de seance depuis l'associe unique ;
  - regime matrimonial canonique `communaute` pour `DOC-005`.

## Delta exact vs medecin standard

| Point | Medecin standard | Medecin + regime communautaire |
|---|---|---|
| Option front | `regime_communautaire=False` | `regime_communautaire=True` |
| Conjoint | non requis, non injecte dans le contexte | requis et injecte dans `ctx.conjoint` |
| Date courrier avertissement | non utile, remise a `None` | requise pour `DOC-005` |
| Documents generes | 6 DOCX | 7 DOCX |
| Statuts | `DOC-017` | `DOC-017` conserve |
| Lettre renonciation | absente | `DOC-005` generee |
| Lettre avertissement conjoint | absente | `DOC-006` reste reserve |

## Documents generes au smoke

Artefact :

- `artifacts/track_b_selarl_medecin_regime_communautaire_005`
- `artifacts/track_b_selarl_medecin_regime_communautaire_005/dossier_generation.zip`

Documents :

- `declaration_non_condamnation.docx`
- `autorisation_domiciliation.docx`
- `procuration.docx`
- `pv_nomination_gerant.docx`
- `demande_inscription_ordre.docx`
- `lettre_renonciation_associe.docx`
- `statuts_selarl_medecin.docx`

Contenu ZIP :

- les 7 DOCX ci-dessus ;
- `manifest.json`.

## Controles texte

- Plan generable : oui.
- Codes selectionnes : `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-017`, `DOC-005`.
- `DOC-006` absent des codes selectionnes.
- `ctx.conjoint` present.
- `ctx.regime_communautaire` present.
- Overlay statuts : `selarl_medecin`.
- Aucun placeholder residuel `[` / `]`.
- Aucun segment parasite `RCS PARIS 788 531 432`.
- Aucun segment parasite `0153814303`.
- La renonciation contient la date de courrier `20/05/2026`.
- La renonciation rend `euros dependant de notre communaute` apres normalisation ASCII.
- L'ancien rendu `regime de communaute` n'est pas present dans la renonciation.

## Tests ajoutes

`tests/unit/test_clean_front_app.py` couvre maintenant :

- la non-regression du medecin standard sans conjoint et sans contexte regime communautaire ;
- le cas medecin + regime avec conjoint, date courrier, renonciation et overlay `selarl_medecin` ;
- le smoke DOCX/ZIP du pack medecin + regime communautaire avec 7 documents ;
- l'absence de `DOC-006`, de statuts dentiste, de placeholders et de segments parasites.

## Statuts documentaires

| Document | Statut | Commentaire |
|---|---|---|
| DOC-001 | LOCKED | Herite du lock documents courts. |
| DOC-002 | LOCKED | Herite du lock documents courts. |
| DOC-003 | LOCKED | Herite du lock documents courts. |
| DOC-004 | LOCKED | Herite du lock documents courts. |
| DOC-005 | LOCKED | Herite du lock humain ; active proprement pour medecin + regime communautaire. |
| DOC-017 | LOCKED source-level | Non rouvert ; conserve depuis le ticket `004`. |
| DOC-034 | PARTIAL | Smoke OK, pas de lock humain specifique dans cette serie. |
| DOC-006 | OPEN GAP / reserve | Non genere par la slice V1 bornee. |
| DOC-016 | LOCKED | Golden standard dentiste non rouvert. |

## OPEN GAPS

- `DOC-006` reste reserve source et n'est pas active dans ce cas.
- `DOC-034` reste PARTIAL faute de lock humain specifique.
- `DOC-017` reste LOCKED source-level, sans retour humain medecin recent equivalent au bloc dentiste.
- Les variantes multi-associes, multi-gerants, president distinct, cession, SCM, derogation et site distinct restent hors perimetre.

## Validations

- Tests cibles `tests/unit/test_clean_front_app.py tests/unit/test_regime_communautaire.py` : OK, 25 passes.
- Tests cibles et non-regression statuts `tests/unit/test_clean_front_app.py tests/unit/test_regime_communautaire.py tests/unit/test_lot_04_statuts_sel_exercice.py` : OK, 36 passes.
- Smoke DOCX/ZIP medecin + regime communautaire : OK.
- Controle placeholders / segments parasites : OK.
- `ruff check .` : OK.
- Clean front Track B : HTTP 200 sur `http://localhost:8528`.
- Process front : arret controle apres sonde HTTP ; verification finale sans process Python/Streamlit restant et sans port 8528 ouvert.
