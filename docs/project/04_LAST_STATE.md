# Dernier état projet

## Date de mise à jour
2026-05-13

## Dernier ticket terminé
ORCH-L2-PV-001 : branchement du PV nomination gérant dans le catalogue et l'orchestrateur.

## État courant du repo
- DOC-001, DOC-002 et DOC-003 disposent chacun d'un générateur dédié déjà terminé.
- L'orchestrateur dossier expose :
  - un registre des générateurs DOC-001, DOC-002, DOC-003 et DOC-004 ;
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
- `REVIEW-PV-001` est DONE.
- `SPEC-RENDER-001` est DONE.
- `RENDER-STYLE-001` est DONE.
- Le générateur PV nomination gérant est disponible dans `src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py`.
- Un contexte exemple de smoke test est disponible dans `examples/contexts/lot_02_pv_nomination_gerant_example.yaml`.
- Le pack de revue humaine est disponible dans `docs/review/lot_02_pv_nomination_gerant_review_v1.md`.
- L'aperçu texte extrait est disponible dans `docs/review/lot_02_pv_nomination_gerant_preview_v1.txt`.
- La spec technique V1 de couche de rendu DOCX commune est disponible dans `docs/delivery/render_style_system_v1.md`.
- Le modèle de données supporte désormais les rôles canoniques nécessaires au PV :
  - `associes[]` ;
  - `dirigeant_nomine` ;
  - `decision` ;
  - `reunion` ;
  - `capital` ;
  - `emprunt` ;
  - `bien_immobilier`.
- Le PV nomination gérant est branché dans l'orchestrateur pour SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI et SCM.
- Le PV nomination gérant est exclu de la sélection SAS.
- `UI-001` reste explicitement en attente : ne pas brancher Streamlit maintenant.
- Fichiers générés connus :
  - `artifacts/lot_01_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_01_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_01_smoke_test/procuration.docx`
  - `artifacts/lot_02_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`
- Fichiers smoke RENDER-STYLE-001 générés :
  - `artifacts/render_style_001_lot_01_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/render_style_001_lot_01_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/render_style_001_lot_01_smoke_test/procuration.docx`
  - `artifacts/render_style_001_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`
- Streamlit, PDF, ZIP et `rendering/bundle.py` n'ont pas été modifiés dans ce ticket.
- `artifacts/` reste hors versionnement via `.gitignore`.
- Commit et push non effectués : `git add` est bloqué par un refus d'écriture sur `.git/index.lock` dans l'environnement Codex local.

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
- REVIEW-PV-001 ne modifie pas le code Python et ne change aucun wording juridique ; il documente seulement les points de revue humaine avant branchement.
- Le DOCX de revue couvre la branche `emprunt.actif=true`, deux associés, et un dirigeant nommé féminin distinct des associés.
- La branche `emprunt.actif=false`, le cas associé unique et le dirigeant masculin restent couverts par tests mais doivent faire l'objet d'une revue humaine dédiée avant branchement si l'arbitrage projet l'exige.
- SPEC-RENDER-001 ne modifie pas le code Python et ne change aucun wording juridique ; il formalise uniquement le profil de style global, les paragraphes/blocs, le titre encadré, les signatures simples/encadrées, le rappel légal et le mécanisme de surcharge document par document.
- Les documents déjà impactés par la future couche commune sont DOC-001, DOC-002, DOC-003 et PV nomination gérant.
- Ecart rendu explicitement documenté : les encadrés de signature manquent aujourd'hui dans le rendu généré.
- RENDER-STYLE-001 implémente `SydelDocxStyleProfile` et les helpers communs dans `docx_builder.py`.
- DOC-001, DOC-002 et DOC-003 utilisent désormais le profil global, le cartouche titre commun et un bloc signature encadré commun.
- DOC-001 utilise désormais le rappel légal commun.
- Le PV nomination gérant utilise le profil global, les paragraphes communs, le bloc centré commun et les lignes de signature communes.
- Aucun wording juridique n'a été volontairement modifié ; les changements portent sur le rendu et la factorisation.
- ORCH-L2-PV-001 ajoute le PV nomination gérant au catalogue sous `DOC-004`.
- ORCH-L2-PV-001 enregistre `PvNominationGerantGenerator` dans le registre par défaut de l'orchestrateur.
- Les décisions de sélection appliquées sont : inclusion SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI et SCM ; exclusion SAS.
- Aucun wording juridique, aucune UI, aucun PDF et aucun ZIP n'ont été modifiés.

## Prochain ticket à lancer
Lancer un ticket dédié de smoke dossier Lot 2 via orchestrateur sur contexte réel, sans PDF/ZIP/UI.

En parallèle métier, relire humainement le rendu DOCX et le wording à partir du pack `docs/review/`.

## Points ouverts
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Le smoke test confirme la production de trois fichiers DOCX, mais ne remplace pas une revue humaine du rendu visuel ni une validation juridique fine du contenu généré.
- PDF et ZIP restent à intégrer dans des tickets ultérieurs.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'à refactor dédié.
- Le PV nomination gérant est codé, testé et branché dans l'orchestrateur pour les structures concernées.
- Le pack REVIEW-PV-001 est prêt, mais il ne vaut pas validation juridique.
- La couche commune de rendu DOCX est implémentée.
- Les signatures encadrées sont disponibles et appliquées aux documents Lot 1 ; le PV conserve des lignes de signature simples sans décision métier supplémentaire.
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
- Harnais temporaire de smoke test revue : OK, 1 test passé ; DOCX régénéré et aperçu texte extrait.
- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 44 tests passés.
- Smoke test PV réel : OK, DOCX généré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/`.
- Smoke test Lot 1 réel : OK, 3 DOCX produits dans `artifacts/lot_01_smoke_test/`.
- SPEC-RENDER-001 : relecture documentaire uniquement ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- RENDER-STYLE-001 : smoke Lot 1 OK dans `artifacts/render_style_001_lot_01_smoke_test/`.
- RENDER-STYLE-001 : smoke PV OK dans `artifacts/render_style_001_pv_nomination_gerant_smoke_test/`.
- RENDER-STYLE-001 : un premier smoke PV vers l'ancien dossier `artifacts/lot_02_pv_nomination_gerant_smoke_test/` a échoué avec `PermissionError` sur le DOCX existant, probablement verrouillé ; le smoke a été relancé avec succès dans un nouveau dossier d'artefacts.
- ORCH-L2-PV-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- ORCH-L2-PV-001 : `.\.venv\Scripts\python.exe -m pytest` OK.
- ORCH-L2-PV-001 : staging Git local bloqué par `fatal: Unable to create '.git/index.lock': Permission denied`.

## Recommandation immédiate suivante
Lancer un smoke dossier Lot 2 via orchestrateur sur contexte réel, puis relire humainement le DOCX PV et le pack `docs/review/lot_02_pv_nomination_gerant_review_v1.md`, notamment le rendu Word, la ponctuation finale des associés, la branche emprunt inactive, les accords singulier/pluriel, la fonction `gérant/gérante` et la signature si le dirigeant nommé n'est pas associé.
