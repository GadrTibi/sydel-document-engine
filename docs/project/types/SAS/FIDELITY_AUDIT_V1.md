# SAS — AUDIT DE FIDELITE V1 (fond + forme)

Date : 2026-06-07
Auteur : audit de fidelite + fix (lecture du modele source python-docx, comparaison para-par-para,
pytest cible).
Type : SAS V1 = exclusivement **SPFPL de Medecins par actions simplifiee unipersonnelle**
(President / actions, actionnaire unique = President). Aucune SAS generique / autre profession.
Perimetre audite : generateur statuts (`lot_04/statuts_sas.py`) + satellite attestation capital /
liste des souscripteurs (`lot_05/attestation_capital_liste_souscripteurs_sas.py`).

## Verdict

**FIDELE apres correctifs de FORME.** Le **fond** (wording) des statuts SAS etait deja une
reproduction verbatim fidele du modele source — y compris les coquilles propres a la source
(reproduites a dessein, jamais corrigees). **Aucun wording invente ni croise** detecte. Les
divergences trouvees etaient de **FORME** (gras/souligne des sous-titres + tiret du pied de page) ;
elles sont **corrigees**. Le satellite attestation est fidele a sa source canonique.

## Methode

- Sources lues telles quelles via python-docx (pas de gabarit d'execution ; rendu from-scratch
  ADR-0004) :
  - `project/source_documents/lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx` (454 paragraphes,
    0 tableau, **0 vrai logo** — voir Forme),
  - `project/source_documents/lot_05/Attestation sur le capital - apport - liste des souscripteurs.docx`
    (source canonique de DOC-024 ; **narrative**, pas tabulaire).
- Echantillon regenere via le contexte de test (`tests/unit/test_statuts_sas.py::_context`,
  `tests/unit/test_lot_05_sas_satellites.py::_base_context`).
- Diff para-par-para normalise (NBSP/tab/espaces) dans les **deux sens** : 0 paragraphe source
  (hors placeholder) manquant cote genere ; 0 paragraphe genere sans correspondance source.
- Inspection run-level (gras / souligne / italique) des intitules + pied de page + en-tetes/medias
  du paquet DOCX.
- Verification : `PYTHONPATH=.../src python -m pytest tests/ -k sas -q --basetemp=.../pt_nuit_sas`
  -> **19 passed, 318 deselected** (etait 18 avant ajout du test de regression de forme).
  Confirme separement : `import sydel_doc_engine` resout bien vers `-claude/src` (piege editable
  ecarte).

## FOND — wording (statuts)

Reproduction verbatim integrale et fidele. Points confirmes :
- Cartouche, comparution "Le soussigné :", phrase d'institution sous condition suspensive, 27
  articles, signature + ANNEXE : tous presents et identiques au modele.
- **Coquilles source reproduites volontairement** (fidelite, ne PAS corriger sans Rafael) :
  "incription", "statuts ," (espace avant virgule), "obiet"/"I'objet"/"I'acte"/"pouvaíent",
  "suppérieure", "êlre"/"sut", "tente (30) jours", "ìmmatriculation", "(SAS – SA)peut" (espace
  manquant). Ce sont des fautes du modele juridique, pas des bugs du generateur.
- Incoherences de vocabulaire source ("gérant", "parts sociales", "parts" dans une SAS par actions)
  egalement reproduites verbatim — arbitrage Rafael ouvert (cf. BUILD_READINESS B9 / pt 5).

## FOND — wording (attestation capital / DOC-024)

Fidele a la source canonique narrative (`lot_05/Attestation ...docx`) : "ATTESTATION",
"Liste des souscripteurs", "Capital social :", "Nombre d'actions :", "Répartition :",
"Apports en nature :", "Total des apports en nature", "Apports en numéraire :", clause de
certification, "Fait à". Note : la copie `project/source_documents/sas/liste_souscripteurs_*.docx`
est une **variante transformee tabulaire** divergente, ce n'est PAS la source canonique de DOC-024
(qui est narrative) — pas de divergence reelle.

## FORME — divergences trouvees et CORRIGEES

Fichier touche : `src/sydel_doc_engine/generators/lot_04/statuts_sas.py` (+ test).

1. **Pied de page — tiret.** Source = `[denomination] – Statuts constitutifs` (tiret demi-cadratin
   U+2013). Generateur utilisait un trait d'union `-`. **Corrige** en `–`. Le test
   `test_statuts_sas.py` encodait le bug (`" - "`) ; corrige pour asserter le wording SOURCE.
2. **Sous-articles numerotes** ("Article 9.1", "Article 9.2", "Article 10.1" a "10.4") : source =
   **gras, NON souligne** ; generateur les rendait en corps de texte (ni gras ni souligne).
   **Corrige** (gras sans souligne).
3. **Sous-articles a tiret** ("ARTICLE 13-1 - DESIGNATION" a "ARTICLE 13-5 - POUVOIRS") : source =
   **gras, NON souligne** ; generateur les rendait comme des articles principaux (gras **+
   souligne**). **Corrige** (gras sans souligne), tout en gardant l'article principal
   "ARTICLE 13 - DIRECTEURS GENERAUX" en gras + souligne.
4. **Intitules de l'article 12** ("NOMINATION ET POUVOIRS", "REMUNERATION") : source = **souligne,
   NON gras** ; generateur les rendait en corps de texte non souligne. **Corrige** (souligne non
   gras).

Mecanique du fix : nouvelles fonctions `_sub_article` (gras, `underline=False`) et `_underline_label`
(souligne, non gras), plus un routage par motif dans `_paragraphs`
(`_SUB_ARTICLE_RE` = `^Article \d`, `_DASHED_SUB_ARTICLE_RE` = `^ARTICLE \d+-\d`,
`_UNDERLINE_LABELS`). Aucun wording modifie.

Verification post-fix (run-level) :
- ARTICLE 1 / 8 / 13 / 24 (principaux) -> (gras, souligne) = (True, True) ;
- Article 9.1/9.2/10.1-10.4, ARTICLE 13-1..13-5 -> (True, False) ;
- NOMINATION ET POUVOIRS / REMUNERATION -> (False, True) ;
- Pied de page -> `SPFPL ... – Statuts constitutifs`.

## FORME — points NON-divergents (controles, OK)

- **Logo** : le paquet contient un seul media `word/media/image2.png` qui est une image **1x1 px**
  (extent ~25000 EMU ≈ 0,02 pouce) logee dans `header2.xml` (en-tete "pair", rId9). C'est un
  **artefact decoratif/espaceur**, PAS un logo. L'en-tete par defaut (rId7 = header3) est vide. Le
  generateur n'ajoute pas de logo : **correct**, il n'y a pas de logo a reproduire.
- **Ordre des articles** : identique a la source (1-27, avec art. 11 Comptes courants apres art. 10).
- **Titre STATUTS** : centre + gras (non souligne) cote source ET genere.
- **Bloc signature + mention italique + ANNEXE** : conformes.

## Divergences RESTANTES (mineures, non bloquantes — signalees, non inventees)

- **Pied de page — champ PAGE.** La source porte aussi un numero de page (champ `PAGE`) dans le
  footer ; le generateur n'emet que la ligne "denomination – Statuts constitutifs". Numerotation de
  page = enrichissement de forme, non un wording. A trancher au cadrage front (cosmetique).
- **Alignement des intitules d'article.** Source : articles principaux en JUSTIFY ; genere : par
  defaut (None). Sans effet visible (titres mono-ligne). Laisse tel quel pour ne pas elargir le
  scope.
- **Attestation — alignements.** Quelques paragraphes du corps attestation sont en JUSTIFY a la
  source vs defaut au genere ; cosmetique, non corrige.
- **Attestation — "Le Docteur [civilite] ..." (source para 23).** La source juxtapose "Le Docteur "
  et `[civilite]` (=Docteur), produisant nativement "Le Docteur Docteur ...". Le generateur
  reproduit **fidelement** cette redondance source. A confirmer Rafael (quirk source), **ne pas
  corriger par invention**.
- **Quirks/incoherences de vocabulaire et coquilles source** (cf. FOND) : reproduits volontairement,
  arbitrage juridique Rafael ouvert (BUILD_READINESS B7/B9, pts 2/5/6).

## Fichiers modifies

- `src/sydel_doc_engine/generators/lot_04/statuts_sas.py` — fix de forme (sous-titres + pied de
  page), aucun wording change.
- `tests/unit/test_statuts_sas.py` — correction de l'assertion pied de page (en-dash source) +
  nouveau test `test_statuts_sas_heading_formatting_matches_source`.

Aucun autre type ni fichier partage d'un autre type n'a ete touche.
