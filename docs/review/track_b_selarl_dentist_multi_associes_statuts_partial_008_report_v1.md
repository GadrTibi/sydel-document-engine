# TRACK-B-SELARL-DENTIST-MULTI-ASSOCIES-STATUTS-PARTIAL-008 - rapport V1

## Objet

Implementation d'un sous-cas limite et explicite :

- SELARL chirurgien-dentiste ;
- multi-associes simple ;
- president de seance choisi parmi les associes existants ;
- gerant unique rattache au praticien / associe 1 ;
- associes presents ou representes disposant ensemble de la totalite des parts ;
- unanimite totale ;
- generation de `DOC-004` et de `DOC-016` en mode PARTIAL.

Ce ticket ne verrouille pas le dossier multi-associes complet.

## Sources utilisees

- `C:\Users\Gad\Downloads\Retours humains .docx` ;
- `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md` ;
- `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md` ;
- `docs/review/track_b_selarl_dentist_line_by_line_lock_003_report_v1.md` ;
- `docs/review/track_b_selarl_multi_associes_doc004_limited_007_report_v1.md` ;
- `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md` ;
- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` ;
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md` ;
- `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`.

## Delta implemente

### Front clean Track B

- Ajout du mode visible `SELARL dentiste multi-associes simple (PARTIAL statuts)`.
- Le mode est expose uniquement quand la profession selectionnee est `Chirurgien-dentiste`.
- Le mode collecte les memes donnees multi-associes simples que le ticket `007` :
  - parts de l'associe 1 / gerant unique ;
  - associes supplementaires ;
  - repartition simple des parts ;
  - president de seance parmi les associes existants.
- Le mode selectionne uniquement `DOC-004` et `DOC-016`.
- Les cas complexes restent exclus en surface : plusieurs gerants, president externe, cession, SCM, votes non unanimes et regime communautaire.

### Contexte moteur

- Ajout du flag `dentist_multi_associes_statuts_partial`.
- Ajout du marqueur moteur `metadata["selarl_dentiste_multi_associes_statuts_partial"] = "true"`.
- Reutilisation de `associes[]`, de la validation de total des parts et de la derivation du president de seance deja creees par le ticket `007`.
- Derivation des apports simples par associe : `nb_parts * valeur_nominale_part`.
- Ajout de `Associe.nb_parts_lettres` pour rendre les lignes de repartition du capital.

## DOC-004

Statut : LOCKED sur le sous-cas multi-associes simple deja etabli par le ticket `007`.

Elements couverts :

- `Les associes de la SELARL...` ;
- `Sont presents ou representes :` ;
- parts detenues par chaque associe ;
- president de seance choisi parmi les associes ;
- `Nomination du gerant` pour gerant unique ;
- resolution adoptee a l'unanimite.

## DOC-016

Statut : PARTIAL.

Elements LOCKED / reutilises :

- articles 1 a 6 et 9 a 34 : texte dentiste deja verrouille par le ticket `003`, reutilise sans rouvrir le lock unipersonnel ;
- article 34 signature electronique : variable de prestataire conservee ;
- gouvernance / vie sociale : bloc humain dentiste reutilise.

Elements implementes en PARTIAL pour le multi-associes simple :

- article 7 : une ligne d'apport par associe ;
- article 7 : total des apports en numeraire aligne sur le capital ;
- article 7 : depot des fonds rendu au pluriel `par les associes` ;
- article 8 : une ligne de repartition de capital par associe ;
- signatures : presence des associes signataires.

## OPEN GAPS

- `DOC-016` preambule / comparution multi-associes : le texte humain disponible verrouille les articles 1 a 34, mais ne fournit pas un bloc complet de comparution plurielle avec etat civil, adresse, situation matrimoniale, conjoint et inscription ordinale pour chaque associe.
- `DOC-016` article 7 : la formule de depot `par les associes` est une adaptation minimale du sous-cas multi, non un lock humain ligne par ligne.
- `DOC-016` signatures : plusieurs signataires sont rendus, mais le bloc complet de signature plurielle reste PARTIAL.
- Plusieurs gerants : hors scope.
- President de seance externe : hors scope.
- Votes non unanimes / quorum partiel / mandats detailles : hors scope.
- Cession medicale/dentaire et cession SCM : hors scope.
- Medecin multi-associes : hors scope.

## Artifacts

Artifacts de smoke attendus :

- `artifacts/track_b_selarl_dentist_multi_associes_statuts_partial_008/pv_nomination_gerant.docx`
- `artifacts/track_b_selarl_dentist_multi_associes_statuts_partial_008/statuts_selarl_chirurgien_dentiste.docx`
- `artifacts/track_b_selarl_dentist_multi_associes_statuts_partial_008/dossier_generation.zip`

## Validations

Validations executees :

- Tests cibles `tests/unit/test_lot_04_statuts_sel_exercice.py tests/unit/test_clean_front_app.py tests/unit/test_pv_nomination_gerant.py` : OK, 46 passes.
- `ruff check .` : OK.
- Smoke DOCX/ZIP dentiste multi-associes simple : OK, 2 DOCX + ZIP.
- Controle texte smoke :
  - aucun placeholder residuel `[` / `]` ;
  - aucun segment parasite `RCS PARIS 788 531 432` ;
  - aucun segment parasite `0153814303` ;
  - `DOC-004` contient le president de seance choisi parmi les associes ;
  - `DOC-016` contient les apports et la repartition du capital pour les deux associes.
- Clean front / HTTP 200 : non valide. Le lancement Streamlit via `Start-Process` dans le shell local est reste bloque et a ete interrompu par l'utilisateur. Les ports de preview testes `8532` et `8533` ont ensuite ete verifies libres. Aucun contournement browser-use ou localhost n'a ete tente.
