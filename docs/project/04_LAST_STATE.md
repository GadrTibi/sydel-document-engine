# Dernier état projet

## Date de mise à jour
2026-05-13

## Dernier ticket terminé
SPEC-PV-001 : intégration de la spec canonique V1 de la famille `PV nomination gérant` dans la mémoire projet.

## État courant du repo
- DOC-001, DOC-002 et DOC-003 disposent chacun d'un générateur dédié déjà terminé.
- L'orchestrateur dossier expose :
  - un registre minimal des générateurs Lot 1 ;
  - `select_documents(structure)` selon le catalogue ;
  - `generate_documents(ctx, output_dir) -> list[Path]`.
- `examples/contexts/lot_01_example.yaml` utilise encore le champ legacy Lot 1 `adresse_domiciliation_affichee`, en attente d'un refactor dédié vers `domiciliation.adresse_affichee`.
- Un smoke test réel a généré les trois DOCX du Lot 1 dans `artifacts/lot_01_smoke_test/`.
- Le moteur dispose désormais de trois référentiels de cadrage :
  - arbre documentaire document-centré V1 : `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md` ;
  - dictionnaire canonique des variables V1 : `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md` ;
  - table de mapping document -> variables canoniques V1 : `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.
- Le cadrage métier de la famille `PV nomination gérant` est disponible dans `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`.
- La spec canonique V1 de la famille `PV nomination gérant` est disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.
- `SPEC-PV-001` est DONE.
- `SPEC-TEXTE-PV-001` est READY pour stabiliser le texte canonique et les variantes du PV nomination gérant.
- `UI-001` reste explicitement en attente : ne pas brancher Streamlit maintenant.
- Fichiers générés :
  - `artifacts/lot_01_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_01_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_01_smoke_test/procuration.docx`
- Streamlit, PDF, ZIP et `rendering/bundle.py` n'ont pas été modifiés dans ce ticket.
- Aucun code Python n'a été modifié pour intégrer le dictionnaire V1 ou la table de mapping V1.
- Aucun commit, push ou PR n'a été fait.

## Décisions métier/techniques appliquées dans ce ticket
- Le smoke test utilise le catalogue moteur existant via `DocumentOrchestrator(build_seed_catalog())`.
- Le contexte d'exemple reste un contexte SELARL exploitable pour les trois documents universels du Lot 1.
- La correction du YAML ne change aucun wording juridique : elle conserve seulement la compatibilité avec le modèle Pydantic Lot 1 existant.
- Aucun autre lot n'a été touché.
- Le dictionnaire canonique V1 est intégré comme référentiel existant, sans réécriture ni reconstruction.
- La table de mapping document -> variables canoniques V1 est intégrée comme référentiel existant, sans réécriture ni reconstruction.
- Le nom canonique retenu pour la domiciliation est `domiciliation.adresse_affichee`.
- `adresse_domiciliation_affichee` reste un alias legacy temporaire du code Lot 1 existant ; aucun refactor Python n'a été fait dans ce ticket.
- Le fichier dictionnaire a été renommé de `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md.md` vers `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`.
- Le cadrage métier `PV nomination gérant` est intégré comme cadrage existant, sans réécriture ni extension.
- La spec canonique V1 `PV nomination gérant` est intégrée comme spec existante, sans réécriture ni extension.
- Cette spec fixe notamment les rôles `societe`, `associes[]`, `dirigeant_nomine`, `signature`, les blocs conditionnels `emprunt` / `bien_immobilier`, la sortie de la logique `personne_1` / `personne_2` et la séparation `civilite_affichage` / `genre`.
- La prochaine étape documentaire doit stabiliser le texte canonique et les variantes : wording de tête, bloc pouvoirs, acceptation finale, féminisation éventuelle de la fonction, périmètre SELAS et conditions exactes du bloc emprunt.
- `UI-001` reste explicitement en attente.

## Prochain ticket à lancer
SPEC-TEXTE-PV-001 : stabiliser le texte canonique et les variantes du PV nomination gérant.

## Points ouverts
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Le smoke test confirme la production de trois fichiers DOCX, mais ne remplace pas une revue humaine du rendu visuel ni une validation juridique fine du contenu généré.
- PDF et ZIP restent à intégrer dans des tickets ultérieurs.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'à refactor dédié.
- UI-001 reste en attente explicite : la prochaine priorité est `SPEC-TEXTE-PV-001`, pas le branchement Streamlit.
- Points ouverts avant code PV : wording canonique de la tête selon les structures, bloc pouvoirs, acceptation finale, féminisation éventuelle de la fonction, périmètre SELAS et conditions exactes du bloc emprunt.
- Toute ambiguïté de wording juridique doit bloquer l'implémentation concernée et être documentée.

## Validations connues
- Tâche documentaire pure : diff relu, aucun code Python modifié.
- Aucun test Python relancé pour ce ticket documentaire.
- Smoke test Lot 1 réel : OK, 3 DOCX produits dans `artifacts/lot_01_smoke_test/`.
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 31 tests passés.

## Recommandation immédiate suivante
Lancer SPEC-TEXTE-PV-001 avec lecture préalable de :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`
- `project/source_documents/lot_02/PV nomination gérant - transforme.docx`

Objectif : stabiliser le texte canonique et les variantes du PV nomination gérant sans coder, sans lancer UI-001 et sans refaire la spec canonique V1.
