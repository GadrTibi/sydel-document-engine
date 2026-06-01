# TRACK-B-SELARL-MULTI-ASSOCIES-DOC004-LIMITED-007 - report V1

## Objet

Implementation du sous-cas limite :

- SELARL multi-associes simple ;
- `DOC-004` uniquement ;
- president de seance choisi parmi les associes existants ;
- gerant unique ;
- associes presents ou representes disposant ensemble de la totalite des parts ;
- unanimite totale.

Ce ticket ne verrouille pas le dossier multi-associes complet.

## Sources utilisees

- `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md` ;
- `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md` ;
- `docs/review/track_b_selarl_dentist_line_by_line_lock_003_report_v1.md` ;
- `docs/review/track_b_selarl_medecin_line_by_line_lock_004_report_v1.md` ;
- `docs/review/track_b_selarl_medecin_regime_communautaire_005_report_v1.md` ;
- `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md` ;
- `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md` ;
- `C:\Users\Gad\Downloads\Retours humains .docx`.

## Delta implemente

### Front clean Track B

- Ajout du mode visible `SELARL multi-associes simple (limite DOC-004)`.
- Le mode limite selectionne uniquement `DOC-004`.
- Le front collecte :
  - nombre d'associes pour le PV ;
  - parts de l'associe 1 / gerant unique ;
  - civilite, prenom, nom et parts des associes supplementaires ;
  - president de seance choisi dans la liste des associes.
- Le front affiche explicitement que le sous-cas est limite a `DOC-004`.

### Contexte moteur

- Ajout d'une structure front `SelarlAdditionalAssocieInput`.
- Ajout des champs :
  - `multi_associes_doc004_limited` ;
  - `associe_principal_nb_parts` ;
  - `additional_associes` ;
  - `president_seance_associe_index`.
- Construction de `DocumentGenerationContext.associes` avec plusieurs associes.
- Derivation de `reunion.president` depuis l'associe selectionne.
- Conservation du gerant unique sur l'associe 1 / praticien.
- Blocage si la somme des parts ne correspond pas au nombre total de parts.

### DOC-004

- Le generateur conserve les formulations humaines deja verrouillees :
  - `Les associes de la SELARL...` ;
  - `Sont presents ou representes :` ;
  - `detenant` ;
  - phrase sur la totalite des parts sociales ;
  - president de seance ;
  - ordre du jour ;
  - vote `Cette resolution est adoptee a l'unanimite`.
- Le libelle d'ordre du jour reste `Nomination du gerant` lorsque le dirigeant nomme est un gerant unique, meme avec plusieurs associes.

## Honnêtete de surface

Le mode limite ne selectionne pas :

- statuts multi-associes `DOC-016` / `DOC-017` ;
- plusieurs gerants ;
- president externe ;
- cession medicale/dentaire ;
- cession SCM ;
- regime communautaire ;
- votes non unanimes ou quorum partiel.

Ces elements restent hors scope.

## Documents LOCKED / PARTIAL / OPEN GAP

### LOCKED

- `DOC-004` : LOCKED pour le sous-cas limite multi-associes simple, president parmi associes existants, gerant unique, totalite des parts representee et unanimite.

### PARTIAL

- Pack SELARL multi-associes global : PARTIAL, car seul `DOC-004` est implemente.

### OPEN GAPS

- Statuts multi-associes `DOC-016` / `DOC-017`.
- Plusieurs gerants.
- President de seance externe.
- `DOC-001`, `DOC-003`, `DOC-034` en multi-associes.
- Cession medicale/dentaire.
- Cession SCM.
- Regime communautaire par associe.
- Vote non unanime, quorum partiel, abstention ou opposition.

## Artifacts

- `artifacts/track_b_selarl_multi_associes_doc004_limited_007/pv_nomination_gerant.docx`
- `artifacts/track_b_selarl_multi_associes_doc004_limited_007/dossier_generation.zip`

## Validations

- Tests cibles `tests/unit/test_pv_nomination_gerant.py tests/unit/test_clean_front_app.py` : OK, 30 passed.
- Ruff cible sur les fichiers modifies : OK.
- `ruff check .` : OK.
- Smoke DOCX/ZIP `DOC-004` multi-associes limite : OK, 1 DOCX + ZIP.
- Controle texte smoke :
  - `Les associes de la SELARL...` present ;
  - president de seance present ;
  - `Nomination du gerant` present ;
  - formule d'unanimite presente ;
  - aucun placeholder residuel ;
  - aucun `EXTRAORDINAIRE`.

- Clean front lance sur `http://localhost:8531` : HTTP 200, PID `23780` arrete proprement.
