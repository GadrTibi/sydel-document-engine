# Dernier état projet

## Date de mise à jour
2026-05-13

## Dernier ticket terminé
CODE-PV-001 : implémentation du générateur canonique from-scratch du PV nomination gérant.

## État courant du repo
- DOC-001, DOC-002 et DOC-003 disposent chacun d'un générateur dédié déjà terminé.
- L'orchestrateur dossier expose :
  - un registre minimal des générateurs Lot 1 ;
  - `select_documents(structure)` selon le catalogue ;
  - `generate_documents(ctx, output_dir) -> list[Path]`.
- `examples/contexts/lot_01_example.yaml` utilise encore le champ legacy Lot 1 `adresse_domiciliation_affichee`, en attente d'un refactor dédié vers `domiciliation.adresse_affichee`.
- Un smoke test réel a généré les trois DOCX du Lot 1 dans `artifacts/lot_01_smoke_test/`.
- Le moteur dispose de trois référentiels de cadrage :
  - arbre documentaire document-centré V1 : `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md` ;
  - dictionnaire canonique des variables V1 : `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md` ;
  - table de mapping document -> variables canoniques V1 : `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.
- Le cadrage métier de la famille `PV nomination gérant` est disponible dans `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`.
- La spec canonique V1 de la famille `PV nomination gérant` est disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.
- La spec texte V1 de la famille `PV nomination gérant` est disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.
- `SPEC-PV-001` est DONE.
- `SPEC-TEXTE-PV-001` est DONE.
- `CODE-PV-001` est DONE.
- Le générateur PV nomination gérant est disponible dans `src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py`.
- Un contexte exemple de smoke test est disponible dans `examples/contexts/lot_02_pv_nomination_gerant_example.yaml`.
- Le modèle de données supporte désormais les rôles canoniques nécessaires au PV :
  - `associes[]` ;
  - `dirigeant_nomine` ;
  - `decision` ;
  - `reunion` ;
  - `capital` ;
  - `emprunt` ;
  - `bien_immobilier`.
- Le PV nomination gérant n'est pas branché dans l'orchestrateur Lot 2.
- `UI-001` reste explicitement en attente : ne pas brancher Streamlit maintenant.
- Fichiers générés connus :
  - `artifacts/lot_01_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_01_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_01_smoke_test/procuration.docx`
  - `artifacts/lot_02_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`
- Streamlit, PDF, ZIP, orchestrateur et `rendering/bundle.py` n'ont pas été modifiés dans ce ticket.
- `artifacts/` reste hors versionnement via `.gitignore`.
- La clôture Git de CODE-PV-001 est gérée par Codex après smoke test réel et validations locales.

## Décisions métier/techniques appliquées dans ce ticket
- Le générateur PV est codé from-scratch dans un module Lot 2 dédié, sans utiliser le DOCX source comme gabarit d'exécution.
- Les variables `personne_1` et `personne_2` ne sont pas introduites dans le modèle de données.
- La liste `associes[]` est répétable pour la liste des associés présents ou représentés et pour les signatures.
- `dirigeant_nomine` est un rôle distinct des associés ; la nomination ne dépend pas de `associes[1]`.
- La branche `emprunt.actif` pilote :
  - la ligne d'ordre du jour emprunt ;
  - la décision emprunt ;
  - la renumérotation du bloc pouvoirs en `DEUXIEME DECISION` ou `TROISIEME DECISION`.
- Les variantes couvertes par tests incluent :
  - un associé / deux associés ;
  - `part` / `parts` ;
  - `né` / `née`.
- La génération bloque si les parts présentes ou représentées ne correspondent pas à la totalité du capital en V1.
- La génération bloque si `societe.capital_variable=false`, faute de wording source validé pour une société non capital variable.
- Aucune intégration orchestrateur Lot 2, UI, PDF ou ZIP n'a été faite.
- Le smoke test réel charge le contexte YAML d'exemple, génère le DOCX PV et vérifie les textes principaux ainsi que l'absence de placeholders résiduels `[` / `]`.

## Prochain ticket à lancer
Revue humaine du rendu DOCX et du wording du PV nomination gérant généré, puis ticket explicite de branchement Lot 2/orchestrateur si validation.

## Points ouverts
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Le smoke test confirme la production de trois fichiers DOCX, mais ne remplace pas une revue humaine du rendu visuel ni une validation juridique fine du contenu généré.
- PDF et ZIP restent à intégrer dans des tickets ultérieurs.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'à refactor dédié.
- Le PV nomination gérant est codé et testé, mais il n'est pas encore branché dans l'orchestrateur.
- UI-001 reste en attente explicite : ne pas brancher Streamlit sans nouveau ticket.
- Points ouverts PV documentés dans la spec texte :
  - périmètre SELAS ;
  - wording capital non variable ;
  - wording société déjà immatriculée ;
  - signature si le dirigeant nommé n'est pas associé ;
  - ponctuation de la dernière ligne `associes[]` ;
  - féminisation éventuelle de la fonction ;
  - règle `euro` / `euros`.
- Toute ambiguïté de wording juridique doit bloquer l'implémentation concernée et être documentée.

## Validations connues
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 38 tests passés.
- Smoke test PV réel : OK, DOCX généré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/`.
- Smoke test Lot 1 réel : OK, 3 DOCX produits dans `artifacts/lot_01_smoke_test/`.

## Recommandation immédiate suivante
Relire humainement le DOCX généré par `PvNominationGerantGenerator` sur un contexte réel PV, notamment le rendu Word, la ponctuation finale des associés, le wording capital variable et la signature si le dirigeant nommé n'est pas associé.

Après validation, ouvrir un ticket dédié pour brancher le PV nomination gérant dans un orchestrateur Lot 2 ou dans le registre documentaire, sans mélanger avec Streamlit/PDF/ZIP.
