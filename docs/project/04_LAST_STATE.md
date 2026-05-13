# Dernier état projet

## Date de mise à jour
2026-05-13

## Dernier ticket terminé
SPEC-TEXTE-PV-001 : création de la spec texte V1 de la famille `PV nomination gérant`.

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
- `CODE-PV-001` est READY pour implémenter le générateur canonique PV nomination gérant.
- `UI-001` reste explicitement en attente : ne pas brancher Streamlit maintenant.
- Fichiers générés connus :
  - `artifacts/lot_01_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_01_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_01_smoke_test/procuration.docx`
- Streamlit, PDF, ZIP et `rendering/bundle.py` n'ont pas été modifiés dans ce ticket.
- Aucun code Python n'a été modifié dans ce ticket.
- Aucun commit, push ou PR n'a été fait.

## Décisions métier/techniques appliquées dans ce ticket
- Le DOCX source `project/source_documents/lot_02/PV nomination gérant - transforme.docx` a été extrait comme texte de référence pour la spec texte.
- La spec texte conserve le wording source visible avant canonisation.
- Le texte canonique V1 est organisé en blocs :
  - en-tête société ;
  - titre et réunion ;
  - introduction de l'assemblée ;
  - associés présents ou représentés ;
  - ordre du jour ;
  - décision nomination ;
  - décision conditionnelle emprunt / bien immobilier ;
  - décision pouvoirs ;
  - clôture et signatures.
- Les blocs répétables `associes[]` sont explicités pour la liste des associés et les signatures.
- `personne_1` et `personne_2` restent uniquement des repères de remapping source, pas des variables canoniques.
- `dirigeant_nomine` reste distinct de `associes[]`, même s'il peut référencer un associé.
- Les variantes singulier/pluriel et masculin/féminin sont documentées :
  - `L'associé` / `Les associés` ;
  - `part` / `parts` ;
  - `né` / `née` ;
  - fonction affichée pilotée par `dirigeant_nomine.fonction_affichage`.
- La branche `emprunt.actif` est explicitée, avec renumérotation du bloc pouvoirs si le bloc emprunt est absent.
- La spec texte documente les points à surveiller avant ou pendant le code, sans inventer de nouveau wording juridique.
- `UI-001` reste explicitement en attente.

## Prochain ticket à lancer
CODE-PV-001 : implémenter le générateur canonique PV nomination gérant.

## Points ouverts
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Le smoke test confirme la production de trois fichiers DOCX, mais ne remplace pas une revue humaine du rendu visuel ni une validation juridique fine du contenu généré.
- PDF et ZIP restent à intégrer dans des tickets ultérieurs.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'à refactor dédié.
- UI-001 reste en attente explicite : la prochaine priorité est `CODE-PV-001`, pas le branchement Streamlit.
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
- Tâche documentaire pure : diff relu, aucun code Python modifié.
- Aucun test Python relancé pour ce ticket documentaire.
- Smoke test Lot 1 réel : OK, 3 DOCX produits dans `artifacts/lot_01_smoke_test/`.
- Dernières validations connues avant ce ticket :
  - `.\.venv\Scripts\python.exe -m ruff check .` : OK.
  - `.\.venv\Scripts\python.exe -m pytest` : OK, 31 tests passés.

## Recommandation immédiate suivante
Lancer CODE-PV-001 avec lecture préalable de :
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
- `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`
- `project/source_documents/lot_02/PV nomination gérant - transforme.docx`

Objectif : implémenter le générateur canonique PV nomination gérant from-scratch, avec `associes[]` dynamique, `dirigeant_nomine` distinct, variantes de genre, branche emprunt et tests ciblés.
