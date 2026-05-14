# Dernier état projet

## Date de mise à jour
2026-05-14

## Dernier ticket terminé
PLACEMENT-HIGH-001 : confirmation du placement des 4 cas HIGH déjà présents dans `project/source_documents/`, avec journal d'exécution V1, sans code Python, sans nouvelle copie et sans modification des cas MEDIUM/LOW.

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
- Deux contextes exemples d'orchestration Lot 2 sont disponibles :
  - `examples/contexts/lot_02_orchestrator_positive_example.yaml`
  - `examples/contexts/lot_02_orchestrator_negative_sas_example.yaml`
- Le smoke orchestrateur Lot 2 a généré les dossiers DOCX attendus :
  - `artifacts/lot_02_orchestrator_positive_smoke_test/`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/`
- La revue smoke orchestrateur Lot 2 est disponible : `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- Le cadrage V1 de la demande d'inscription à l'ordre est disponible : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`.
- Le cadrage V1 du batch régime communautaire est disponible : `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- Le manifest d'import sources V1 est disponible : `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md`.
- Le rapport de doublons sources V1 est disponible : `docs/project/11_SOURCE_DUPLICATES_REPORT_V1.md`.
- Le plan de placement sources V1 est disponible : `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`.
- Les décisions d'arbitrage sources V1 sont disponibles : `docs/project/13_SOURCE_ARBITRATION_DECISIONS_V1.md`.
- Le journal d'exécution du placement HIGH V1 est disponible : `docs/project/14_SOURCE_PLACEMENT_EXECUTION_V1.md`.
- `ARBITRAGE-SOURCES-001` est DONE.
- `PLACEMENT-HIGH-001` est DONE.
- `ANALYSE-ORDRE-001` est DONE.
- `SPEC-ORDRE-001` est READY.
- `SPEC-RC-001` est READY.
- `UI-001` reste explicitement en attente : ne pas brancher Streamlit maintenant.
- Fichiers générés connus :
  - `artifacts/lot_01_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_01_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_01_smoke_test/procuration.docx`
  - `artifacts/lot_02_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/procuration.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/pv_nomination_gerant.docx`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/procuration.docx`
- Fichiers smoke RENDER-STYLE-001 générés :
  - `artifacts/render_style_001_lot_01_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/render_style_001_lot_01_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/render_style_001_lot_01_smoke_test/procuration.docx`
  - `artifacts/render_style_001_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`
- Streamlit, PDF, ZIP et `rendering/bundle.py` n'ont pas été modifiés dans ce ticket.
- `artifacts/` reste hors versionnement via `.gitignore`.

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
- SMOKE-ORCH-L2-001 confirme en génération réelle que SCI produit les documents universels et `pv_nomination_gerant.docx`.
- SMOKE-ORCH-L2-001 confirme en génération réelle que SAS produit seulement les documents universels et exclut `pv_nomination_gerant.docx`.
- Aucun wording juridique, aucune UI, aucun PDF et aucun ZIP n'ont été modifiés.
- ANALYSE-ORDRE-001 lit les trois sources Lot 2 en lecture seule et crée deux cadrages dans `docs/delivery/`.
- Les chemins nommés dans le ticket pour les trois DOCX ne correspondent pas littéralement aux noms présents dans le dépôt ; les fichiers transformés correspondants ont été utilisés et l'écart est documenté dans les cadrages.
- La demande d'inscription à l'ordre est considérée suffisamment cadrée pour ouvrir `SPEC-ORDRE-001`, mais pas pour coder.
- Le batch régime communautaire est considéré suffisamment cadré pour ouvrir `SPEC-RC-001`, mais pas pour coder.
- Pour le batch régime communautaire, la mutualisation réaliste porte surtout sur les variables, les rôles, les montants et les helpers de rendu ; deux documents canoniques distincts restent recommandés.
- ARBITRAGE-SOURCES-001 scanne 147 fichiers dans `project/source_import/raw_drive_dump/` et 11 fichiers dans `project/source_documents/`.
- ARBITRAGE-SOURCES-001 identifie 18 groupes de doublons probables, dont 15 groupes de doublons exacts.
- Les 4 cas HIGH documentés sont : DOC-001, DOC-002, DOC-003 et la source canonique `PV nomination gérant`.
- PLACEMENT-HIGH-001 confirme que les 4 cas HIGH sont déjà présents aux emplacements retenus dans `project/source_documents/`.
- PLACEMENT-HIGH-001 n'a effectué aucune nouvelle copie, car chaque cible HIGH existait déjà.
- PLACEMENT-HIGH-001 crée `docs/project/14_SOURCE_PLACEMENT_EXECUTION_V1.md`.
- Les 3 cas MEDIUM restent bloqués : demande d'inscription à l'ordre, renonciation régime communautaire, avertissement régime communautaire.
- Les 3 cas LOW restent bloqués : statuts, liste des souscripteurs / attestation sur le capital, documents sans source claire.
- 16 documents sources sont explicitement hors périmètre moteur courant.
- Aucun fichier de `project/source_import/raw_drive_dump/`, aucun fichier source documentaire et aucun artefact n'a été déplacé, supprimé ou renommé.
- Aucun code Python, aucune UI, aucun PDF, aucun ZIP et aucun wording juridique source n'ont été modifiés.

## Prochain ticket à lancer
Lancer `SPEC-ORDRE-001`.

Les cas MEDIUM/LOW doivent rester bloqués tant que les variantes sources n'ont pas été comparées ou arbitrées.

## Points ouverts
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Le smoke test confirme la production de trois fichiers DOCX, mais ne remplace pas une revue humaine du rendu visuel ni une validation juridique fine du contenu généré.
- PDF et ZIP restent à intégrer dans des tickets ultérieurs.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'à refactor dédié.
- Le PV nomination gérant est codé, testé et branché dans l'orchestrateur pour les structures concernées.
- Le smoke orchestrateur Lot 2 est vert sur SCI positif et SAS négatif.
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
- Points ouverts demande d'inscription à l'ordre :
  - traitement de la mention source `Dérogation ?` ;
  - validation du wording `associé et praticien et exerçant` ;
  - accords féminins éventuels ;
  - règle de titre `Dr` ;
  - règle de destinataire `Monsieur le Président` ;
  - mapping canonique de `[profession]`, `[profession_reglementee]`, `[adresse_personnelle]` et `[adresse_ordre]`.
- Points ouverts régime communautaire :
  - périmètre exact du fichier de renonciation nommé `SELAS` ;
  - rôles canoniques `apporteur` et `conjoint` ;
  - correspondance entre `[date_courrier]` et la lettre d'avertissement ;
  - harmonisation des montants d'apport malgré les placeholders divergents ;
  - formes sociales complète / affichée / abrégée ;
  - accords `associé/associée/actionnaire`, `futur/future`, fonctions dirigeantes ;
  - traitement de la mention manuscrite ;
  - absence de prénom du conjoint dans la lettre d'avertissement.
- Points ouverts sources :
  - ne pas choisir une source unique pour la demande d'inscription à l'ordre avant comparaison SELARL / SELAS / SPFPL ;
  - ne pas fusionner les variantes SELARL du régime communautaire avec les copies exactes SELAS/SPFPL sans arbitrage ;
  - ne pas placer automatiquement la famille liste des souscripteurs / attestation sur le capital ;
  - ne pas dedupliquer les statuts entre familles, professions ou variantes.
- Toute ambiguïté de wording juridique doit bloquer l'implémentation concernée et être documentée.

## Validations connues
- PLACEMENT-HIGH-001 : les 4 fichiers HIGH cibles existent dans `project/source_documents/`.
- PLACEMENT-HIGH-001 : les hashes cibles ont été comparés aux sources brutes correspondantes pour les cas HIGH ; aucune copie nouvelle nécessaire.
- PLACEMENT-HIGH-001 : aucun test de code exécuté car aucun fichier Python n'a été modifié.
- PLACEMENT-HIGH-001 : `git status --short` n'était pas propre avant intervention ; aucun commit ni push n'a été effectué.
- ARBITRAGE-SOURCES-001 : scan documentaire en lecture seule ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- ARBITRAGE-SOURCES-001 : relecture documentaire du diff requise avant toute reprise de placement physique.
- ARBITRAGE-SOURCES-001 : `raw_drive_dump` n'a pas été versionné.
- ANALYSE-ORDRE-001 : relecture documentaire uniquement ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- ANALYSE-ORDRE-001 : `git status --short` consulté avant modifications ; le dépôt contenait déjà des fichiers non suivis hors périmètre du ticket.
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
- SMOKE-ORCH-L2-001 : smoke SCI positif OK, `pv_nomination_gerant.docx` présent.
- SMOKE-ORCH-L2-001 : smoke SAS négatif OK, `pv_nomination_gerant.docx` absent.
- SMOKE-ORCH-L2-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SMOKE-ORCH-L2-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 47 tests passés.

## Recommandation immédiate suivante
Lancer `SPEC-ORDRE-001`, puis `SPEC-RC-001` après comparaison documentaire des variantes concernées.
