# Tableau d'exécution

## Statuts
- READY
- IN_PROGRESS
- BLOCKED
- DONE

## Tickets actifs

| ID | Statut | Objet | Entrées obligatoires | Sorties obligatoires |
|---|---|---|---|---|
| PM-001 | DONE | Installer la mémoire projet dans le repo | source de vérité + specs Lot 1 | docs/project/* |
| PM-002 | DONE | Vérifier et compléter la mémoire projet opérationnelle | AGENTS.md + docs/project/* | docs/project complétés + artefact parasite traité |
| PM-003 | DONE | Installer le kit de reprise nouveau ChatGPT / Codex | mémoire projet existante | handoff + last state + prompt nouveau chat |
| DOC-001 | DONE | Implémenter la déclaration de non-condamnation | source doc + spec Lot 1 | générateur + tests + MAJ doc |
| DOC-003 | DONE | Implémenter la procuration | source doc + spec Lot 1 | générateur + tests + MAJ doc |
| DOC-002 | DONE | Implémenter l'autorisation de domiciliation | source doc + spec Lot 1 + décision V1 adresse libre | générateur + tests + MAJ doc |
| ORCH-001 | DONE | Brancher l'orchestrateur Lot 1 | générateurs DOC-001/002/003 | service orchestrateur + tests |
| PM-004 | DONE | Intégrer l'arbre moteur document-centré V1 dans la mémoire projet | arbre moteur document-centré V1 | board + dernier état mis à jour |
| PM-005 | DONE | Intégrer le dictionnaire canonique des variables V1 dans la mémoire projet | dictionnaire canonique des variables V1 | board + dernier état mis à jour |
| SMOKE-001 | DONE | Smoke test réel Lot 1 via orchestrateur | contexte exemple Lot 1 + orchestrateur | 3 DOCX générés + docs projet mises à jour |
| VAR-001 | DONE | Ajouter une table de mapping document -> variables canoniques | arbre documentaire V1 + dictionnaire canonique V1 + specs | table de mapping document -> variables canoniques |
| PM-006 | DONE | Intégrer le cadrage métier PV nomination gérant V1 dans la mémoire projet | cadrage Lot 2 PV nomination gérant | board + dernier état mis à jour |
| SPEC-PV-001 | DONE | Formaliser la spec canonique du PV nomination gérant à partir du cadrage V1 | cadrage Lot 2 + arbre documentaire V1 + dictionnaire canonique V1 + table de mapping V1 | spec canonique écrite, blocs conditionnels, mapping variables, règles `associes[]`, points ouverts |
| SPEC-TEXTE-PV-001 | DONE | Stabiliser le texte canonique et les variantes du PV nomination gérant | spec canonique PV nomination gérant V1 + source Lot 2 | spec textuelle détaillée, variantes structurelles, wording à valider, critères avant code |
| CODE-PV-001 | DONE | Implémenter le générateur canonique PV nomination gérant | spec canonique V1 + spec texte V1 + source Lot 2 | générateur PV from-scratch + tests associes[]/genre/emprunt + MAJ doc |
| REVIEW-PV-001 | DONE | Préparer la revue humaine du PV nomination gérant généré | contexte exemple Lot 2 + générateur PV existant | DOCX régénéré + aperçu texte + checklist de revue humaine |
| SPEC-RENDER-001 | DONE | Spécifier une couche de rendu DOCX commune | générateurs DOC-001/002/003 + PV nomination gérant + specs existantes | spec technique render style system V1 |
| RENDER-STYLE-001 | DONE | Implémenter la couche de rendu DOCX commune | spec render style system V1 + générateurs existants | helpers communs + générateurs migrés + tests + smoke DOCX |
| ORCH-L2-PV-001 | DONE | Brancher le PV nomination gérant dans l'orchestrateur | générateur PV + specs Lot 2 + décisions de sélection | catalogue + registre orchestrateur + tests ciblés |
| SMOKE-ORCH-L2-001 | DONE | Smoke test réel orchestrateur Lot 2 positif SCI / négatif SAS | contextes exemples Lot 2 + orchestrateur | DOCX générés, PV présent en SCI et absent en SAS, revue smoke |
| FIX-PV-RENDER-001 | DONE | Restaurer la structure visuelle essentielle du PV nomination gérant | source Lot 2 + specs PV + render style system V1 | listes à tirets, titre, intertitres, italique votes, smoke DOCX |
| ANALYSE-ORDRE-001 | DONE | Cadrer Demande d'inscription à l'ordre et batch régime communautaire Lot 2 | sources Lot 2 ordre + régime communautaire + référentiels V1 | cadrages delivery + tickets SPEC-ORDRE-001/SPEC-RC-001 READY |
| ARBITRAGE-SOURCES-001 | DONE | Réparer le manifest d'import sources et arbitrer les placements V1 | source truth + raw_drive_dump + source_documents + décisions métier | docs projet 10/11/12/13 + prochain ticket placement |
| PLACEMENT-HIGH-001 | DONE | Déplacer physiquement dans source_documents uniquement les cas HIGH validés | plan de placement V1 + décisions d'arbitrage sources V1 | placement HIGH confirmé no-op + journal d'exécution |
| SPEC-ORDRE-001 | DONE | Formaliser la spec canonique Demande d'inscription à l'ordre | cadrage ordre V1 + source Lot 2 + référentiels V1 + variantes raw dump | spec canonique écrite, variantes comparées, mapping variables, accords, points ouverts |
| SPEC-TEXTE-ORDRE-001 | DONE | Stabiliser le texte canonique et les variantes de Demande d'inscription à l'ordre | spec canonique ordre V1 + variantes SELARL/SELAS/SPFPL/SPFPL apport/SCM | spec texte détaillée, tronc commun, overlays, blocs conditionnels/manuels, règles de blocage avant code |
| CODE-ORDRE-001 | DONE | Implémenter le générateur canonique Demande d'inscription à l'ordre | spec canonique ordre V1 + spec texte ordre V1 + source Lot 2 + variantes raw dump | générateur ordre from-scratch + tests overlays/dérogation/mandataire + MAJ doc |
| SPEC-RC-001 | DONE | Formaliser la spec canonique batch régime communautaire | cadrage régime communautaire V1 + deux sources Lot 2 + référentiels V1 | spec canonique batch, spec texte batch, mapping commun, règles de génération, points ouverts |
| CODE-RC-001 | DONE | Implémenter le batch régime communautaire v1 | specs canonique et texte régime communautaire V1 + sources Lot 2 + variantes raw dump | deux générateurs DOCX from-scratch + sélection orchestrateur + tests ciblés + MAJ doc |
| SPEC-SPFPL-001 | DONE | Formaliser le batch SPFPL spécifique | source vérité + raw dump SPFPL | spec canonique SPFPL V1 |
| SPEC-DEROG-001 | DONE | Formaliser la famille dérogations | source vérité + raw dump dérogations | spec canonique dérogations V1 |
| SPEC-CESSION-BAIL-001 | DONE | Formaliser les blocs cession cabinets et bail/appel de fonds | source vérité + raw dump cession | specs canoniques cession cabinets + bail/appel de fonds V1 |
| SYNC-SPECS-001 | DONE | Synchroniser les specs parallèles dans main | branches SPEC-RC/SPFPL/DEROG/CESSION | specs intégrées + pilotage aligné |
| SPEC-TEXTE-BAIL-APP-001 | DONE | Stabiliser le texte canonique bail / appel de fonds | spec canonique bail/appel de fonds V1 + sources raw dump | spec texte V1 bail / appel de fonds |
| SPEC-TEXTE-CESSION-CAB-001 | DONE | Stabiliser le texte canonique cession cabinets | spec canonique cession cabinets V1 + sources raw dump | spec texte V1 cession cabinets |
| SPEC-TEXTE-DEROG-001 | DONE | Stabiliser le texte canonique dérogations | spec canonique dérogations V1 + sources raw dump | spec texte V1 dérogations |
| SPEC-TEXTE-SPFPL-001 | DONE | Stabiliser le texte canonique SPFPL spécifique | spec canonique SPFPL V1 + sources raw dump | spec texte V1 SPFPL |
| SYNC-TEXTE-SPECS-001 | DONE | Synchroniser les specs texte parallèles dans main | branches SPEC-TEXTE bail/appel, cession, dérogations, SPFPL | specs texte intégrées + pilotage aligné |
| SYNC-ARBITRAGES-001 | DONE | Synchroniser les arbitrages parallèles dans main | branches ARBITRAGE cession, dérogations, SPFPL | arbitrages intégrés + pilotage aligné |
| CODE-BAIL-APP-001 | DONE | Implémenter le mini-batch bail / appel de fonds | specs canonique et texte bail/appel V1 + arbitrages de blocage V1 | générateurs DOCX + tests ciblés + MAJ doc |
| ARBITRAGE-CESSION-001 | DONE | Arbitrer les points bloquants cession cabinets avant code | spec texte cession cabinets V1 + points ouverts | décisions métier tracées pour acte/compromis, medical/dentaire et anomalies source |
| ARBITRAGE-DEROG-001 | DONE | Arbitrer les points bloquants dérogations avant code | spec texte dérogations V1 + sources Lot 03 | décisions métier sur formulaires préremplis, rôles et sources legacy |
| ARBITRAGE-SPFPL-001 | DONE | Arbitrer les points bloquants SPFPL avant code | spec texte SPFPL V1 + points ouverts | décisions métier cession/apport, commissaire, souscripteurs et sources |
| CODE-CESSION-CAB-001 | DONE | Implémenter la famille cession cabinets | specs canonique/texte cession cabinets V1 + arbitrage V1 | générateurs DOCX + blocages explicites + tests ciblés + MAJ doc |
| RESUME-CODE-CESSION-CAB-001 | DONE | Reprendre proprement CODE-CESSION-CAB-001 sur main synchronisé | main à jour Lot 03/Lot 05 + specs/arbitrages cession V1 | reprise cadrée de la famille cession cabinets |
| PREP-DEROG-001 | DONE | Préparer les sources dérogations avant code | arbitrages dérogations V1 + raw dump + plan de placement | sources Lot 03 placées + rapport de préparation |
| CODE-DEROG-CORE-001 | DONE | Implémenter le cœur dérogations | specs/arbitrages dérogations V1 + PREP-DEROG-001 | générateurs DOCX dérogations cœur + blocages explicites + tests |
| CODE-SPFPL-AGR-INFO-001 | DONE | Implémenter le sous-batch SPFPL agrément / note d'information | specs canonique/texte SPFPL V1 + arbitrage V1 | générateurs DOCX ciblés + tests + sources Lot 05 placées |
| CODE-SPFPL-CORE-001 | DONE | Implémenter le cœur SPFPL restant | specs canonique/texte SPFPL V1 + arbitrage V1 + sources préparées | générateurs SPFPL ciblés + blocages explicites + tests |
| PREP-STATUTS-001 | DONE | Préparer les sources statuts avant spécification/code | source vérité + raw dump + plan de placement/arbitrage sources | sources statuts cadrées + écarts documentés |
| SPEC-STATUTS-SEL-001 | DONE | Spécifier les statuts SEL d'exercice | préparation statuts V1 + sources Lot 04 SELARL/SELAS | spec canonique + spec texte avant code |
| SPEC-STATUTS-SPFPL-001 | DONE | Spécifier les statuts SPFPL | préparation statuts V1 + sources Lot 04 SPFPL cession/apport | spec canonique + spec texte avant code |
| SPEC-STATUTS-CIVILS-001 | DONE | Spécifier les statuts civils | préparation statuts V1 + sources Lot 04 SCI/SCI IRIS/SCM/SCS | spec canonique + spec texte avant code |
| SPEC-STATUTS-SAS-001 | DONE | Spécifier les statuts SAS | préparation statuts V1 + source Lot 04 SAS | spec canonique + spec texte avant code |
| SYNC-STATUTS-SPECS-001 | DONE | Synchroniser les specs statuts parallèles dans main | branches statuts SAS/SPFPL/SEL/CIVILS | specs intégrées + pilotage aligné |
| CODE-STATUTS-SAS-001 | DONE | Implémenter les statuts SAS | specs statuts SAS V1 + blocages explicites | générateur DOCX + tests ciblés + MAJ doc |
| CODE-STATUTS-SPFPL-001 | DONE | Implémenter les statuts SPFPL cession/apport | specs statuts SPFPL V1 + blocages explicites | générateurs DOCX + tests ciblés + MAJ doc |
| ARBITRAGE-STATUTS-SEL-001 | DONE | Arbitrer les points bloquants statuts SEL avant code | specs statuts SEL V1 + points ouverts | décisions pluralité associés, SELAS et wording |
| ARBITRAGE-STATUTS-CIVILS-001 | DONE | Arbitrer les points bloquants statuts civils avant code | specs statuts civils V1 + points ouverts | décisions SCI/SCI IRIS/SCM/SCS avant code |
| SYNC-STATUTS-CODE-ARB-001 | DONE | Synchroniser code statuts SAS/SPFPL et arbitrage SEL dans main | branches code/arbitrage statuts | commits intégrés + pilotage réaligné |
| CODE-STATUTS-SEL-001 | READY | Implémenter les statuts SEL d'exercice | specs statuts SEL V1 + arbitrages SEL V1 | générateur(s) DOCX + tests ciblés + MAJ doc |
| CODE-STATUTS-CIVILS-CORE-001 | READY | Implémenter le cœur des statuts civils | specs statuts civils V1 + arbitrages civils V1 | générateurs SCS/SCI/SCI IRIS/SCM + tests ciblés + MAJ doc |
| FIX-STYLE-LETTERS-001 | READY | Corriger les écarts de style prioritaires des lettres | blueprint style batch V1 + générateurs existants | rendu lettres harmonisé + tests/smoke ciblés |
| RESUME-ARBITRAGE-STATUTS-CIVILS-001 | DONE | Reprendre proprement l'arbitrage des statuts civils | specs statuts civils V1 + état main synchronisé | remplacé par l'arbitrage civils V1 absorbé |
| STYLE-ANALYSE-BATCH-001 | DONE | Analyser le style documentaire en batch avant harmonisation | générateurs/statuts disponibles + besoins de rendu | cadrage style batch + points d'arbitrage |
| SYNC-STYLE-CIVILS-001 | DONE | Synchroniser style batch et arbitrage civils dans main | branches style/arbitrage civils | commits intégrés + pilotage réaligné |
| UI-001 | BLOCKED | Brancher Streamlit V0 Lot 1 | orchestrateur Lot 1 + spec canonique PV nomination gérant validée | écran simple + test manuel |

## Référentiels moteur disponibles
- Le moteur dispose désormais d'un arbre documentaire document-centré V1 : `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`.
- Le moteur dispose désormais d'un dictionnaire canonique des variables V1 : `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`.
- Le moteur dispose désormais d'une table de mapping document -> variables canoniques V1 : `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.
- Le cadrage métier de la famille `PV nomination gérant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`.
- La spec canonique V1 de la famille `PV nomination gérant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.
- La spec texte V1 de la famille `PV nomination gérant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.
- La spec technique V1 de couche de rendu DOCX commune est disponible : `docs/delivery/render_style_system_v1.md`.
- Le cadrage V1 `Demande d'inscription à l'ordre` est disponible : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`.
- La spec canonique V1 `Demande d'inscription à l'ordre` est disponible : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`.
- La spec texte V1 `Demande d'inscription à l'ordre` est disponible : `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.
- Le cadrage V1 du batch `régime communautaire` est disponible : `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- La spec canonique V1 du batch `régime communautaire` est disponible : `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md`.
- La spec texte V1 du batch `régime communautaire` est disponible : `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`.
- La spec canonique V1 du batch SPFPL spécifique est disponible : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`.
- La spec texte V1 du batch SPFPL spécifique est disponible : `docs/delivery/lot_05_spfpl_spec_texte_v1.md`.
- La préparation V1 des sources statuts est disponible : `docs/delivery/lot_04_statuts_preparation_v1.md`.
- La spec canonique V1 de la famille `dérogations` est disponible : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`.
- La spec texte V1 de la famille `dérogations` est disponible : `docs/delivery/lot_03_derogations_spec_texte_v1.md`.
- La spec canonique V1 `cession cabinets` est disponible : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`.
- La spec texte V1 `cession cabinets` est disponible : `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.
- Les arbitrages V1 `cession cabinets` sont disponibles : `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`.
- La spec canonique V1 `bail / appel de fonds` est disponible : `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`.
- La spec texte V1 `bail / appel de fonds` est disponible : `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`.
- Les arbitrages V1 `dérogations` sont disponibles : `docs/delivery/lot_03_derogations_arbitrages_v1.md`.
- Les arbitrages V1 du batch SPFPL spécifique sont disponibles : `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.
- Les specs V1 des statuts SEL d'exercice sont disponibles : `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.
- Les specs V1 des statuts SPFPL sont disponibles : `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`.
- Les specs V1 des statuts civils sont disponibles : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.
- Les specs V1 des statuts SAS sont disponibles : `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`.
- Le manifest d'import sources V1 est disponible : `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md`.
- Le rapport de doublons sources V1 est disponible : `docs/project/11_SOURCE_DUPLICATES_REPORT_V1.md`.
- Le plan de placement sources V1 est disponible : `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`.
- Les décisions d'arbitrage sources V1 sont disponibles : `docs/project/13_SOURCE_ARBITRATION_DECISIONS_V1.md`.
- Le journal d'exécution du placement HIGH V1 est disponible : `docs/project/14_SOURCE_PLACEMENT_EXECUTION_V1.md`.
- Le pack de revue humaine du PV nomination gérant est disponible : `docs/review/lot_02_pv_nomination_gerant_review_v1.md`.
- L'aperçu texte extrait du DOCX généré est disponible : `docs/review/lot_02_pv_nomination_gerant_preview_v1.txt`.
- La revue smoke orchestrateur Lot 2 est disponible : `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- Ces référentiels cadrent les prochains tickets ; ils ne doivent pas être réinventés pendant l'implémentation.

## Ecart temporaire connu
- Nom canonique retenu pour la domiciliation : `domiciliation.adresse_affichee`.
- Alias legacy temporaire présent dans le code Lot 1 : `adresse_domiciliation_affichee`.
- Le présent ticket ne refactore pas le code Python ; les prochains tickets doivent converger vers le nom canonique sans recréer de variante locale.

## Détail des prochains tickets

### DOC-001
- Objectif : générer la déclaration sur l'honneur de non-condamnation.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- ADR à relire : ADR-0001, ADR-0002, ADR-0004, ADR-0005.
- Contraintes : source reçue, spec écrite, accords de genre, DOCX propre, tests obligatoires.
- Sortie attendue : générateur DOC-001, tests, mise à jour documentaire.

### DOC-003
- Objectif : générer la procuration après DOC-001.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- Contraintes : bloc mandataire SYDEL externalisé en configuration, wording source conservé.
- Sortie attendue : générateur DOC-003, tests, mise à jour documentaire.

### DOC-002
- Objectif : générer l'autorisation de domiciliation après arbitrage V1 déjà posé.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- Contrainte sensible : le nom canonique documentaire est désormais `domiciliation.adresse_affichee`; le code Lot 1 existant conserve temporairement l'alias legacy `adresse_domiciliation_affichee`.
- Sortie : générateur DOC-002 terminé, tests unitaires ciblés ajoutés, validations locales vertes.

### ORCH-001
- Objectif : brancher les trois générateurs Lot 1 dans l'orchestrateur dossier.
- Prérequis : DOC-001, DOC-002 et DOC-003 terminés.
- Sortie : registre minimal DOC-001/DOC-002/DOC-003 branché, génération DOCX dossier selon `ctx.structure`, tests d'orchestration ajoutés.

### VAR-001
- Objectif : ajouter une table de mapping document -> variables canoniques sans refaire le dictionnaire.
- Prérequis : arbre documentaire V1 et dictionnaire canonique des variables V1 intégrés.
- Sortie : table de mapping V1 intégrée à la mémoire projet, sans réécriture ; écart temporaire documenté entre `domiciliation.adresse_affichee` et l'alias legacy `adresse_domiciliation_affichee`.

### SPEC-PV-001
- Objectif : formaliser la spec canonique du PV nomination gérant à partir du cadrage V1, sans refaire le cadrage.
- Spec/cadrage à lire : `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`.
- Prérequis : arbre documentaire V1, dictionnaire canonique V1 et table de mapping document -> variables canoniques V1.
- Contraintes : traiter `PV nomination gérant` comme une famille documentaire mutualisable, gérer `associes[]` dynamiquement, distinguer `dirigeant_nomine` de `associes[]`, identifier les blocs conditionnels, ne coder aucun générateur.
- Sortie attendue : spec canonique écrite dans `docs/delivery/`, avec structure, blocs fixes, blocs conditionnels, mapping variables, règles de répétition, règles de grammaire minimales et points ouverts.
- Statut : terminé ; spec canonique V1 disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.

### SPEC-TEXTE-PV-001
- Objectif : stabiliser le texte canonique et les variantes du PV nomination gérant avant tout codage.
- Spec à lire : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.
- Source à consulter : `project/source_documents/lot_02/PV nomination gérant - transforme.docx`.
- Contraintes : ne pas refaire la spec canonique, ne pas coder de générateur, ne pas modifier implicitement le wording juridique ; signaler les formulations à validation.
- Sortie attendue : spec textuelle détaillée du PV nomination gérant, variantes structurelles explicites, wording à valider, critères d'entrée avant code.
- Statut : terminé ; spec texte V1 disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.

### CODE-PV-001
- Objectif : implémenter le générateur canonique `PV nomination gérant` à partir des specs V1, sans reprendre `personne_1` / `personne_2` comme vérité métier.
- Specs à lire : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md` et `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.
- Source à consulter : `project/source_documents/lot_02/PV nomination gérant - transforme.docx`.
- Contraintes : générateur DOCX from-scratch, `associes[]` dynamique, `dirigeant_nomine` distinct, variantes `né/née`, branche `emprunt.actif`, renumérotation des décisions, aucun changement de wording juridique hors spec texte.
- Sortie attendue : générateur dédié, tests unitaires ciblés, validation locale, mise à jour documentaire.
- Statut : terminé ; générateur disponible dans `src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py`, non branché à l'orchestrateur.
- Smoke test réel : contexte exemple disponible dans `examples/contexts/lot_02_pv_nomination_gerant_example.yaml`, DOCX généré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/`.

### REVIEW-PV-001
- Objectif : préparer la revue humaine du rendu DOCX et du wording du PV nomination gérant déjà codé, sans modifier le code métier.
- Entrées : générateur PV existant, contexte exemple `examples/contexts/lot_02_pv_nomination_gerant_example.yaml`, specs Lot 2.
- Sortie : DOCX régénéré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`, aperçu texte et checklist de revue dans `docs/review/`.
- Statut : terminé ; le PV reste non branché à l'orchestrateur Lot 2 tant qu'une validation humaine explicite n'a pas été donnée.

### SPEC-RENDER-001
- Objectif : formaliser une couche de rendu DOCX commune avant refactor du code métier.
- Spec à lire : `docs/delivery/render_style_system_v1.md`.
- Contraintes : ne modifier aucun générateur, ne changer aucun wording juridique, documenter les styles communs, le titre encadré, les signatures simples/encadrées, le rappel légal et les surcharges documentaires.
- Sortie : spec technique V1 créée ; documents impactés listés : DOC-001, DOC-002, DOC-003 et PV nomination gérant.
- Statut : terminé ; le point d'écart explicite est que les encadrés de signature manquent aujourd'hui dans le rendu généré.

### RENDER-STYLE-001
- Objectif : implémenter la couche commune de rendu DOCX dans `src/sydel_doc_engine/rendering/docx_builder.py`.
- Prérequis : `docs/delivery/render_style_system_v1.md`.
- Contraintes : ticket technique uniquement, aucun changement de wording juridique, migration progressive, tests existants à conserver verts.
- Sortie attendue : profil global de style, helpers de paragraphes/blocs, titre encadré, signature simple, signature encadrée disponible, rappel légal commun.
- Statut : terminé ; couche commune implémentée et appliquée à DOC-001, DOC-002, DOC-003 et PV nomination gérant.

### ORCH-L2-PV-001
- Objectif : brancher le générateur PV nomination gérant dans le catalogue et l'orchestrateur, sans UI, PDF ni ZIP.
- Prérequis : générateur PV existant, specs Lot 2, décisions de sélection SELARL/SELAS/SPFPL cession/SPFPL apport/SCS/SCI/SCM et exclusion SAS.
- Sortie : `DOC-004` ajouté au catalogue, générateur enregistré, sélection testée pour SELARL/SCI/SAS, génération orchestrée testée avec production du DOCX PV.
- Statut : terminé ; aucune modification de wording juridique.

### SMOKE-ORCH-L2-001
- Objectif : vérifier en génération réelle l'orchestrateur Lot 2 avec un cas positif SCI et un cas négatif SAS.
- Entrées : contextes `examples/contexts/lot_02_orchestrator_positive_example.yaml` et `examples/contexts/lot_02_orchestrator_negative_sas_example.yaml`.
- Sortie : smoke DOCX dans `artifacts/lot_02_orchestrator_positive_smoke_test/` et `artifacts/lot_02_orchestrator_negative_sas_smoke_test/`, revue dans `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- Statut : terminé ; le PV est généré pour SCI et absent pour SAS.

### FIX-PV-RENDER-001
- Objectif : améliorer le rendu from-scratch du PV nomination gérant sans chercher une copie parfaite du Word source.
- Entrées : source Lot 2 `PV nomination gérant - transforme.docx`, specs PV V1 et spec `render_style_system_v1.md`.
- Contraintes : ne pas modifier le wording juridique, ne pas toucher à l'UI, ne pas générer PDF/ZIP, ne pas versionner `artifacts/`.
- Sortie : bloc société centré avec dénomination en gras, titre principal encadré, listes à tirets pour associés et décisions, intertitres de décision gras/soulignés, formules de vote en italique, signatures centrées, smoke DOCX.
- Statut : terminé ; aucun changement de wording juridique volontaire.

### ANALYSE-ORDRE-001
- Objectif : préparer le prochain batch mutualisable Lot 2 sans coder, en analysant la demande d'inscription à l'ordre et les deux lettres de régime communautaire.
- Entrées : référentiels projet V1 + trois sources Lot 2 présentes dans `project/source_documents/lot_02/`.
- Sortie : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md` et `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- Statut : terminé ; aucun code Python modifié.

### ARBITRAGE-SOURCES-001
- Objectif : réparer les prérequis documentaires d'import sources puis arbitrer les placements possibles sans déplacer de fichier.
- Entrées : `project/source_truth/Documents_a_generer_par_cas.docx`, `project/source_import/raw_drive_dump/`, `project/source_documents/`, décisions métier chef de projet.
- Sortie : manifest import sources V1, rapport doublons V1, plan placement V1, décisions arbitrage V1.
- Statut : terminé ; aucun code Python, aucun fichier source, aucun artefact modifié.

### PLACEMENT-HIGH-001
- Objectif : déplacer physiquement dans `source_documents` uniquement les cas HIGH validés par `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`.
- Entrées : plan de placement V1 + décisions d'arbitrage sources V1.
- Contraintes : ne pas toucher aux cas MEDIUM/LOW, ne pas versionner `project/source_import/raw_drive_dump/`, documenter les no-op si les fichiers HIGH sont déjà présents.
- Statut : terminé ; les 4 cas HIGH sont déjà présents aux emplacements cibles et ont été confirmés en no-op documenté. Aucun fichier MEDIUM/LOW ou hors périmètre n'a été modifié.

### SPEC-ORDRE-001
- Objectif : formaliser la spec canonique `Demande d'inscription à l'ordre` à partir du cadrage V1.
- Cadrage à lire : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`.
- Contraintes : ne pas coder, comparer les variantes SELARL / SELAS / SPFPL, identifier le traitement de `Dérogation ?`, les accords de genre, le titre `Dr`, le destinataire ordinal et le mapping des données ordinales.
- Sortie : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`, avec périmètre structures, comparaison des variantes, noyau texte, variables canoniques, règles de blocage et points ouverts.
- Statut : terminé ; aucun code Python modifié.

### SPEC-TEXTE-ORDRE-001
- Objectif : stabiliser le texte canonique et les variantes de `Demande d'inscription à l'ordre` avant tout codage.
- Spec à lire : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`.
- Sources à consulter : source Lot 2 + variantes raw dump SELARL, SELAS et SPFPL comparées dans la spec canonique.
- Contraintes : ne pas coder, trancher le wording de `Dérogation ?`, la granularité des données ordinales, le mandataire, les accords et le destinataire ordinal.
- Sortie attendue : spec texte détaillée, wording stabilisé ou points de blocage explicites, critères avant code.
- Statut : terminé ; spec texte V1 disponible dans `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.

### CODE-ORDRE-001
- Objectif : implémenter le générateur canonique `Demande d'inscription à l'ordre`.
- Specs à lire : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md` et `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.
- Sources à consulter : source Lot 2 + variantes raw dump SELARL, SELAS, SPFPL cession, SPFPL apport et absence de variante SCM dédiée documentée.
- Contraintes : générateur DOCX from-scratch, overlays SELARL/SELAS, SPFPL cession/apport et SCM, bloc `Dérogation ?` manuel/conditionnel, mandataire configurable, aucune constante SYDEL en dur, aucun changement de wording juridique hors spec texte.
- Sortie attendue : générateur dédié, tests unitaires ciblés, validation locale, mise à jour documentaire.
- Statut : terminé ; générateur disponible dans `src/sydel_doc_engine/generators/lot_02/demande_inscription_ordre.py`, tests ciblés ajoutés, smoke DOCX réel généré hors versionnement.

### SPEC-RC-001
- Objectif : formaliser la spec canonique du batch `régime communautaire` pour la lettre de renonciation et la lettre d'avertissement.
- Cadrage à lire : `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- Contraintes : garder deux documents canoniques distincts, mutualiser le pack de variables, arbitrer les rôles `apporteur` / `conjoint`, les montants, les dates croisées, les formes sociales et la mention manuscrite.
- Sortie : specs canonique et texte créées dans `docs/delivery/`, variantes SELARL / SELAS / SPFPL comparées, mapping commun écrit, overlays de mention manuscrite documentés, règles de blocage avant code précisées.
- Statut : terminé ; `CODE-RC-001` est ajouté en READY.

### CODE-RC-001
- Objectif : implémenter le batch `régime communautaire` V1 pour la lettre d'avertissement au conjoint et la lettre de renonciation.
- Specs à lire : `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md` et `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`.
- Sources à consulter : sources Lot 2 placées + variantes raw dump SELARL, SELAS et SPFPL comparées dans SPEC-RC-001.
- Contraintes : deux documents canoniques distincts, génération DOCX from-scratch, sélection uniquement si `dossier.options.regime_communautaire == true`, structures SELARL / SELAS / SPFPL cession / SPFPL apport, aucun changement de wording juridique hors variables et overlays documentés.
- Sortie attendue : générateurs dédiés, branchement orchestrateur/catalogue si nécessaire, tests ciblés des quatre structures, de la mention manuscrite SELARL vs SELAS/SPFPL, des dates croisées et des blocages.
- Statut : terminé ; générateurs `lettre_renonciation_associe` et `lettre_avertissement_conjoint` disponibles, catalogue/orchestrateur branchés, contexte exemple et smoke DOCX générés.

### SPEC-SPFPL-001
- Objectif : formaliser le batch documentaire SPFPL spécifique sans coder.
- Spec à lire : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`.
- Contraintes : garder les documents universels et le régime communautaire hors de cette spec, ne pas coder depuis une source absente, ne pas corriger les ambiguïtés cession/apport sans arbitrage.
- Sortie : spec canonique V1 SPFPL, sous-familles, variables proposées, blocages et points ouverts.
- Statut : terminé ; aucun code Python modifié.

### SPEC-DEROG-001
- Objectif : formaliser la famille documentaire `dérogations` sans automatiser les formulaires manuels.
- Spec à lire : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`.
- Contraintes : distinguer site distinct, multi-sites SEL, cumul SEL/BNC, cumul salariée et pièces manuelles ; ne pas générer de contenu narratif sensible.
- Sortie : spec canonique V1 dérogations, périmètre automatisable/manuel, variables et blocages.
- Statut : terminé ; aucun code Python modifié.

### SPEC-CESSION-BAIL-001
- Objectif : formaliser les blocs `cession cabinets` et `bail / appel de fonds` avant tout code.
- Specs à lire : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md` et `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`.
- Contraintes : ne pas fusionner acte/compromis ou médical/dentaire sans arbitrage, traiter les anomalies de bail et de placeholders comme points ouverts.
- Sortie : deux specs canoniques V1, variables, conditions, règles de blocage et points ouverts.
- Statut : terminé ; aucun code Python modifié.

### SYNC-SPECS-001
- Objectif : absorber dans `main` les specs parallèles RC, SPFPL, dérogations et cession/bail.
- Entrées : branches et commits de specs déjà produits en parallèle.
- Sortie : commits de specs intégrés dans `main`, pilotage aligné, `CODE-RC-001` confirmé READY.
- Statut : terminé ; aucun fichier Python stagé pour le commit de synchronisation.

### SPEC-TEXTE-BAIL-APP-001
- Objectif : stabiliser le texte canonique du mini-batch `bail / appel de fonds` avant code.
- Spec à lire : `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`.
- Contraintes : conserver le wording source, bloquer l'appel de fonds médical et les cas SELAS non arbitrés, ne pas coder.
- Statut : terminé ; aucun code Python modifié.

### SPEC-TEXTE-CESSION-CAB-001
- Objectif : stabiliser le texte canonique de la famille `cession cabinets`.
- Spec à lire : `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.
- Contraintes : ne pas harmoniser médical/dentaire, acte/compromis ou SELARL/SELAS sans arbitrage.
- Statut : terminé ; aucun code Python modifié.

### SPEC-TEXTE-DEROG-001
- Objectif : stabiliser le texte canonique des dérogations.
- Spec à lire : `docs/delivery/lot_03_derogations_spec_texte_v1.md`.
- Contraintes : ne pas automatiser les formulaires manuels, ne pas inventer les zones narratives sensibles.
- Statut : terminé ; aucun code Python modifié.

### SPEC-TEXTE-SPFPL-001
- Objectif : stabiliser le texte canonique du batch SPFPL spécifique.
- Spec à lire : `docs/delivery/lot_05_spfpl_spec_texte_v1.md`.
- Contraintes : ne pas corriger les conflits cession/apport, commissaire aux apports ou souscripteurs sans arbitrage.
- Statut : terminé ; aucun code Python modifié.

### SYNC-TEXTE-SPECS-001
- Objectif : absorber dans `main` les quatre specs texte parallèles bail/appel, cession cabinets, dérogations et SPFPL.
- Entrées : branches `codex/spec-texte-bail-app-001`, `codex/spec-texte-cession-cab-001`, `codex/spec-texte-derog-001`, `codex/spec-texte-spfpl-001`.
- Sortie : quatre specs texte intégrées dans `main`, pilotage aligné, prochains tickets READY confirmés.
- Statut : terminé ; aucun fichier Python, aucun `project/source_import/raw_drive_dump/` et aucun `artifacts/` modifié.

### SYNC-ARBITRAGES-001
- Objectif : absorber dans `main` les trois arbitrages parallèles cession cabinets, dérogations et SPFPL.
- Entrées : branches `codex/arbitrage-cession-001`, `codex/arbitrage-derog-001`, `codex/arbitrage-spfpl-001`.
- Sortie : arbitrages intégrés dans `main`, pilotage aligné, prochains tickets READY confirmés.
- Statut : terminé ; aucun fichier Python, aucun `project/source_import/raw_drive_dump/` et aucun `artifacts/` modifié.

### CODE-BAIL-APP-001
- Objectif : implémenter le mini-batch `bail / appel de fonds`.
- Specs à lire : `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md` et `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`.
- Contraintes : génération DOCX from-scratch, activation cession SELARL/SELAS pour l'avenant, appel de fonds limité SELARL dentaire, blocages explicites sur les points ouverts.
- Statut : DONE ; commit `557a013274aa9f7122c81d5e6e0b52c4043a540c` absorbé dans `main`, générateurs `avenant_contrat_bail` et `appel_fond_sel` disponibles, catalogue/orchestrateur branchés et tests ciblés intégrés.

### ARBITRAGE-CESSION-001
- Objectif : arbitrer les points bloquants de la famille `cession cabinets` avant tout code.
- Entrées : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md` et `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.
- Sortie attendue : décisions sur acte/compromis, SELAS, anomalies médical/dentaire, placeholders acquéreur/vendeur, crédit-vendeur, SCM et salariés.
- Statut : terminé ; arbitrages V1 disponibles dans `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`.

### ARBITRAGE-DEROG-001
- Objectif : arbitrer les points bloquants de la famille `dérogations` avant code.
- Entrées : `docs/delivery/lot_03_derogations_spec_canonique_v1.md` et `docs/delivery/lot_03_derogations_spec_texte_v1.md`.
- Sortie attendue : décisions sur formulaires préremplis, placement sources Lot 03, conversion `.doc`, rôles et champs narratifs obligatoires.
- Statut : terminé ; arbitrages V1 disponibles dans `docs/delivery/lot_03_derogations_arbitrages_v1.md`.

### ARBITRAGE-SPFPL-001
- Objectif : arbitrer les points bloquants du batch SPFPL spécifique avant code.
- Entrées : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_05_spfpl_spec_texte_v1.md`.
- Sortie attendue : décisions sur note d'information cession/apport, PV agrément, commissaire aux apports, liste des souscripteurs et sources manquantes.
- Statut : terminé ; arbitrages V1 disponibles dans `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.

### CODE-CESSION-CAB-001
- Objectif : implémenter la famille `cession cabinets` en respectant les arbitrages V1.
- Specs à lire : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`, `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md` et `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`.
- Contraintes : quatre documents canoniques distincts, sélection par étape explicite, séparation médical/dentaire, blocages explicites sur les anomalies restantes, aucun wording corrigé silencieusement.
- Statut : DONE ; quatre générateurs cession cabinets disponibles sous `DOC-009` à `DOC-012`, branchés au catalogue et à l'orchestrateur.

### RESUME-CODE-CESSION-CAB-001
- Objectif : reprendre proprement `CODE-CESSION-CAB-001` depuis `main` après absorption de la préparation dérogations et du sous-batch SPFPL.
- Entrées : `main` synchronisé, specs/arbitrages cession cabinets V1, état local CODE-CESSION non fusionné.
- Contraintes : repartir d'un état Git propre, ne pas reprendre de fichiers non suivis sans revue, conserver les blocages explicites déjà arbitrés.
- Statut : DONE ; branche reprise depuis `main`, travail cession restauré, validations locales et smoke DOCX verts.

### PREP-DEROG-001
- Objectif : préparer les sources de la famille `dérogations` avant code.
- Specs à lire : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`, `docs/delivery/lot_03_derogations_spec_texte_v1.md` et `docs/delivery/lot_03_derogations_arbitrages_v1.md`.
- Contraintes : placer uniquement les sources Lot 03 explicitement décidées, convertir ou remplacer le `.doc` legacy si `cumul_salariee` est ciblé, ne pas automatiser les formulaires manuels.
- Statut : DONE ; commit source `36828fbc45d6b8a37c2e76eb8227460df441ebde` absorbé dans `main`, sources Lot 03 placées et rapports de préparation disponibles.

### CODE-DEROG-CORE-001
- Objectif : implémenter le cœur de la famille `dérogations` après préparation des sources.
- Specs à lire : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`, `docs/delivery/lot_03_derogations_spec_texte_v1.md`, `docs/delivery/lot_03_derogations_arbitrages_v1.md` et `docs/delivery/lot_03_derogations_preparation_v1.md`.
- Contraintes : ne pas automatiser les formulaires manuels, distinguer document finalisé et formulaire à compléter, bloquer les narratifs sensibles manquants.
- Statut : DONE ; générateurs partiels `multi_sites_sel` et `cumul_sel_bnc` codés en formulaires à compléter, sources DOCX propres utilisées, `cumul_salariee` legacy non traité.

### CODE-SPFPL-AGR-INFO-001
- Objectif : implémenter le sous-batch SPFPL `agrément / note d'information` limité par les arbitrages V1.
- Specs à lire : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`, `docs/delivery/lot_05_spfpl_spec_texte_v1.md` et `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.
- Contraintes : piloter le wording cession/apport par `operation_spfpl.type`, bloquer l'acte de cession d'actions et les multi-souscripteurs, ne jamais rendre `OU` ou une double option non tranchée.
- Statut : DONE ; commit source `958fce5d2a9d5d30df4d918cb098fec483f5140e` absorbé dans `main`, générateurs ciblés SPFPL et tests intégrés.

### CODE-SPFPL-CORE-001
- Objectif : implémenter le cœur SPFPL restant dans le respect des specs et arbitrages V1.
- Specs à lire : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`, `docs/delivery/lot_05_spfpl_spec_texte_v1.md` et `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.
- Contraintes : rester limité aux documents SPFPL sourcés/arbitrés, bloquer l'acte de cession d'actions sans source DOCX confirmée, bloquer les multi-souscripteurs hors V1 et ne pas corriger le wording juridique sans validation explicite.
- Statut : DONE ; commit source `09cbad120d22910f05ba5e645971ade56fedb76d` absorbé dans `main`, générateurs SPFPL cœur et tests ciblés intégrés.

### PREP-STATUTS-001
- Objectif : préparer les sources statuts avant toute spécification ou implémentation.
- Entrées : source de vérité, raw dump, référentiels projet et décisions de placement/arbitrage sources.
- Contraintes : ne pas dédupliquer ni harmoniser les statuts sans comparaison documentée, ne pas coder de générateur, ne pas modifier le wording juridique source.
- Statut : DONE ; commit source `b854821061b85ac66fe785c11cb3c6b0bac5a85b` absorbé dans `main`, sources Lot 04 cadrées et écarts documentés.

### SPEC-STATUTS-SEL-001
- Objectif : spécifier les statuts SEL d'exercice avant tout codage.
- Specs/sources à lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et sources Lot 04 SELARL chirurgien-dentiste, SELARL médecin, SELAS médecin.
- Contraintes : comparer les variantes, extraire les variables, documenter les clauses sensibles, ne pas coder de générateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.

### SPEC-STATUTS-SPFPL-001
- Objectif : spécifier les statuts SPFPL cession/apport avant tout codage.
- Specs/sources à lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et sources Lot 04 SPFPL.
- Contraintes : traiter cession et apport en comparaison, conserver les sorties distinctes tant que la fusion n'est pas prouvée, ne pas coder de générateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`.

### SPEC-STATUTS-CIVILS-001
- Objectif : spécifier les statuts civils SCI, SCI IRIS, SCM et SCS avant tout codage.
- Specs/sources à lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et sources Lot 04 civiles.
- Contraintes : ne pas dédupliquer SCI/SCI IRIS/SCM/SCS sans analyse documentée, identifier les variables capital, associés, siège, objet et options fiscales, ne pas coder de générateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.

### SPEC-STATUTS-SAS-001
- Objectif : spécifier les statuts SAS avant tout codage.
- Specs/sources à lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et source Lot 04 SAS.
- Contraintes : vérifier le fichier source dont le nom contient aussi SPFPL, traiter séparément la liste des souscripteurs et l'attestation sur le capital si nécessaire, ne pas coder de générateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`.

### SYNC-STATUTS-SPECS-001
- Objectif : absorber dans `main` les specs statuts parallèles SAS, SPFPL, SEL et civils.
- Entrées : branches `codex/spec-statuts-sas-001`, `codex/spec-statuts-spfpl-001`, `codex/spec-statuts-sel-001` et `codex/spec-statuts-civils-001`.
- Sortie : commits de specs intégrés dans `main`, pilotage aligné et prochains tickets confirmés READY.
- Statut : DONE ; specs intégrées sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.

### CODE-STATUTS-SAS-001
- Objectif : implémenter les statuts SAS à partir des specs V1.
- Specs à lire : `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`.
- Contraintes : limiter le périmètre au modèle SAS/SPFPL médecins source, bloquer les cas non arbitrés, ne pas corriger le wording juridique sans validation.
- Statut : DONE ; générateur SAS V1 intégré dans `main` avec tests ciblés.

### CODE-STATUTS-SPFPL-001
- Objectif : implémenter les statuts SPFPL cession/apport à partir des specs V1.
- Specs à lire : `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`.
- Contraintes : conserver deux overlays cession/apport, bloquer le multi-associés non arbitré et les anomalies de wording non validées.
- Statut : DONE ; générateurs SPFPL cession/apport V1 intégrés dans `main` avec tests ciblés.

### ARBITRAGE-STATUTS-SEL-001
- Objectif : arbitrer les points bloquants des statuts SEL avant code.
- Specs à lire : `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.
- Contraintes : trancher pluralité des associés, ligne `personne_2`, second lieu SELAS, féminisation dirigeant et signatures.
- Statut : DONE ; arbitrages disponibles dans `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`.

### ARBITRAGE-STATUTS-CIVILS-001
- Objectif : arbitrer les points bloquants des statuts civils avant code.
- Specs à lire : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.
- Contraintes : trancher SCI/SCI IRIS, SCM, SCS, associés personnes morales, signatures dynamiques et lettre option IS hors statuts.
- Statut : DONE ; arbitrages disponibles dans `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.

### SYNC-STATUTS-CODE-ARB-001
- Objectif : absorber dans `main` les branches code statuts SAS/SPFPL et arbitrage statuts SEL.
- Entrées : `codex/code-statuts-sas-001`, `codex/code-statuts-spfpl-001`, `codex/arbitrage-statuts-sel-001`.
- Sortie : commits intégrés, tests relancés, pilotage aligné sur les tickets suivants.
- Statut : DONE ; intégration effectuée sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.

### CODE-STATUTS-SEL-001
- Objectif : implémenter les statuts SEL d'exercice après arbitrages V1.
- Specs à lire : `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`, `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`.
- Contraintes : appliquer strictement les arbitrages SEL, conserver les blocages explicites et ne pas corriger le wording juridique sans validation.
- Statut : READY.

### CODE-STATUTS-CIVILS-CORE-001
- Objectif : implémenter le cœur des statuts civils après arbitrages V1.
- Specs à lire : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md`, `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md` et `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.
- Contraintes : couvrir uniquement SCS, SCI, SCI IRIS et SCM en V1, utiliser `associes[]`, bloquer les données legacy insuffisantes et garder l'option IS hors générateur statuts.
- Statut : READY.

### RESUME-ARBITRAGE-STATUTS-CIVILS-001
- Objectif : reprendre proprement l'arbitrage des statuts civils depuis `main` synchronisé.
- Specs à lire : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.
- Contraintes : arbitrer SCI/SCI IRIS, SCM, SCS, associés personnes morales, signatures dynamiques et lettre option IS hors statuts avant tout code.
- Statut : DONE ; remplacé par l'absorption de `ARBITRAGE-STATUTS-CIVILS-001`.

### STYLE-ANALYSE-BATCH-001
- Objectif : cadrer l'analyse de style documentaire en batch avant harmonisation de rendu.
- Entrées : générateurs existants, specs disponibles et rendus DOCX déjà produits hors versionnement.
- Contraintes : analyse/cadrage uniquement, sans modification de wording juridique ni déplacement de sources.
- Statut : DONE ; blueprint disponible dans `docs/delivery/render_style_blueprint_batch_v1.md`.

### FIX-STYLE-LETTERS-001
- Objectif : corriger les écarts de style prioritaires des lettres à partir du blueprint batch V1.
- Specs à lire : `docs/delivery/render_style_blueprint_batch_v1.md` et specs texte des lettres concernées.
- Contraintes : ne pas modifier le wording juridique, limiter les changements au rendu DOCX, conserver les artefacts hors versionnement.
- Statut : READY.

### UI-001
- Objectif : exposer une Streamlit simple pour générer le Lot 1.
- Statut : en attente explicite ; ne pas lancer sans ticket explicite dédié.
- Prérequis : orchestrateur Lot 1 fonctionnel et spec canonique `PV nomination gérant` validée.
- Sortie attendue : écran simple, génération testable manuellement, aucun métier caché dans l'UI.

## Règle de mise à jour
Chaque ticket terminé doit mettre à jour ce fichier :
- passer son statut à DONE
- déplacer le ticket actif en IN_PROGRESS pendant l'exécution si la tâche dure plus qu'une modification courte
- indiquer le prochain ticket à lancer
- indiquer les éventuels points ouverts
- mettre à jour `docs/project/04_LAST_STATE.md`

## Prochaine étape prévue
- prochaine action recommandée : lancer `CODE-STATUTS-SEL-001`, `CODE-STATUTS-CIVILS-CORE-001` ou `FIX-STYLE-LETTERS-001` selon la priorité métier.
- tickets READY confirmés : `CODE-STATUTS-SEL-001`, `CODE-STATUTS-CIVILS-CORE-001` et `FIX-STYLE-LETTERS-001`.
- `STYLE-ANALYSE-BATCH-001` et `ARBITRAGE-STATUTS-CIVILS-001` sont DONE et absorbés dans `main`.
- `CODE-STATUTS-SAS-001`, `CODE-STATUTS-SPFPL-001` et `ARBITRAGE-STATUTS-SEL-001` sont DONE et absorbés dans `main`.
- `CODE-BAIL-APP-001` est DONE et absorbé dans `main`.
- `PREP-DEROG-001` est DONE et absorbé dans `main`.
- `CODE-SPFPL-AGR-INFO-001` est DONE et absorbé dans `main`.
- `CODE-CESSION-CAB-001` est DONE et absorbé dans `main`.
- `CODE-DEROG-CORE-001` est DONE et absorbé dans `main`.
- `PREP-STATUTS-001` est DONE et absorbé dans `main`.
- `CODE-SPFPL-CORE-001` est DONE et absorbé dans `main`.
- `SPEC-STATUTS-SAS-001`, `SPEC-STATUTS-SPFPL-001`, `SPEC-STATUTS-SEL-001` et `SPEC-STATUTS-CIVILS-001` sont DONE et absorbés dans `main`.
- revue humaine toujours recommandée : smoke DOCX `régime communautaire`, notamment le rendu SELARL de la renonciation canonique.
- les autres cas MEDIUM/LOW restent bloqués tant que leurs variantes sources n'ont pas été comparées.
- UI-001 reste explicitement en attente.

## Points ouverts
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Les trois DOCX sont bien produits par l'orchestrateur dans `artifacts/lot_01_smoke_test/`, mais le rendu visuel et le wording juridique restent à relire humainement dans les fichiers générés.
- PDF et ZIP restent hors ORCH-001 et devront être traités dans un ticket dédié.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'à refactor dédié.
- ORCH-L2-PV-001 est terminé ; le PV nomination gérant est branché dans l'orchestrateur pour les structures concernées et exclu pour SAS.
- SMOKE-ORCH-L2-001 est terminé ; le smoke réel confirme la génération du PV pour SCI et son absence pour SAS.
- FIX-PV-RENDER-001 est terminé ; le PV from-scratch restaure les structures visuelles essentielles du document source sans UI, PDF ni ZIP.
- ANALYSE-ORDRE-001 est terminé ; les cadrages V1 ordre et régime communautaire sont disponibles dans `docs/delivery/`.
- ARBITRAGE-SOURCES-001 est terminé ; le scan a identifié 147 fichiers dans `raw_drive_dump`, 11 fichiers dans `source_documents`, 18 groupes de doublons probables, 6 documents sans source claire et 16 documents hors périmètre.
- PLACEMENT-HIGH-001 est terminé ; les 4 cas HIGH documentés dans le plan de placement V1 ont été confirmés comme déjà présents, sans nouvelle copie.
- SPEC-ORDRE-001, SPEC-TEXTE-ORDRE-001, CODE-ORDRE-001, SPEC-RC-001, CODE-RC-001, SPEC-SPFPL-001, SPEC-DEROG-001, SPEC-CESSION-BAIL-001, SPEC-TEXTE-BAIL-APP-001, SPEC-TEXTE-CESSION-CAB-001, SPEC-TEXTE-DEROG-001, SPEC-TEXTE-SPFPL-001, ARBITRAGE-CESSION-001, ARBITRAGE-DEROG-001, ARBITRAGE-SPFPL-001 et CODE-BAIL-APP-001 sont DONE.
- REVIEW-PV-001 est terminé, mais la validation humaine du rendu DOCX et du wording reste à obtenir pour la revue juridique fine.
- RENDER-STYLE-001 est terminé ; les signatures encadrées sont disponibles dans la couche commune et appliquées aux signatures Lot 1.
- Le PV nomination gérant conserve des signatures répétables simples ; toute signature encadrée dirigeant/associés séparée reste soumise à validation métier.
- UI-001 reste en attente explicite : ne pas lancer le branchement Streamlit sans nouveau ticket.
- Points ouverts PV documentés dans la spec texte : périmètre SELAS, capital non variable, société déjà immatriculée, dirigeant non associé, ponctuation finale des associés, féminisation éventuelle de la fonction, règle `euro/euros`.
- Points ouverts ordre post-CODE-ORDRE-001 : revue humaine du premier rendu SCM, mention de dérogation limitée au bloc manuel fourni, valeurs ordinales et mandataire toujours fournis par contexte/référentiel.
- Points ouverts régime communautaire après SPEC-RC-001 : revue humaine SELARL de la renonciation canonique, féminisation éventuelle de `futur`, absence de variante `ma conjointe`, apport limité à une somme en numéraire, valeurs par défaut de régime matrimonial / qualité renoncée / formes sociales à fournir par contexte ou référentiel.
- CODE-RC-001 est terminé ; le smoke DOCX réel confirme la production des deux lettres, mais ne vaut pas validation juridique fine.
- Points ouverts SPFPL après ARBITRAGE-SPFPL-001 : acte de cession d'actions hors automatisation faute de source DOCX confirmée, multi-souscripteurs hors V1, commissaire et évaluateur fournis par contexte ou référentiel validé.
- Points ouverts dérogations après PREP-DEROG-001 : les deux sources Lot 03 préparées sont placées, le `.doc` legacy reste à convertir ou remplacer si `cumul_salariee` entre dans le périmètre, et le mode de rendu `document finalisé` ou `formulaire à compléter` doit être porté explicitement dans le registre ou le nom de sortie.
- CODE-DEROG-CORE-001 est terminé ; `DOC-013` formulaire multi-sites SEL et `DOC-014` demande cumul SELARL/BNC sont branchés dans le catalogue/orchestrateur comme formulaires à compléter.
- Points ouverts dérogations après CODE-DEROG-CORE-001 : revue humaine juridique/visuelle du premier rendu, `cumul_salariee` toujours bloqué faute de DOCX propre, zones narratives sensibles laissées à compléter.
- CODE-BAIL-APP-001 est terminé ; `DOC-007` avenant au contrat de bail et `DOC-008` appel de fonds SEL sont branchés dans le catalogue/orchestrateur.
- Points ouverts bail/appel après CODE-BAIL-APP-001 : appel de fonds limité à SELARL dentaire, avenant limité SELARL/SELAS avec `dossier_options.cession=true`, revue humaine juridique/visuelle du premier rendu toujours nécessaire.
- Points ouverts cession après CODE-CESSION-CAB-001 : revue humaine juridique/visuelle du premier rendu DOCX, sources SELAS non stabilisées au-delà du paramétrage V1, PDF/ZIP hors ticket.
- Points ouverts statuts après arbitrages V1 : SAS limité au modèle SAS/SPFPL médecins source ; SPFPL doit conserver cession/apport sans harmonisation ; SEL est prêt à coder ; civils est prêt à coder sur SCS, SCI, SCI IRIS et SCM.

## Journal court
- 2026-05-12 : mémoire projet installée dans `docs/project/`.
- 2026-05-12 : mémoire projet complétée pour servir de contexte opérationnel autonome ; artefact `tall -U pip` identifié comme fichier parasite à supprimer.
- 2026-05-12 : kit de reprise ajouté pour nouveau ChatGPT / Codex avec handoff, dernier état et prompt de reprise.
- 2026-05-12 : DOC-001 implémenté en génération DOCX from-scratch avec tests unitaires ; validations locales vertes.
- 2026-05-12 : DOC-001 corrigé pour rendre l'adresse personnelle dans l'ordre source `num voie + voie, ville cp`.
- 2026-05-12 : DOC-003 implémenté en génération DOCX from-scratch avec tests unitaires ; validations locales vertes.
- 2026-05-12 : DOC-002 implémenté en génération DOCX from-scratch avec champ libre `adresse_domiciliation_affichee` ; validations locales vertes.
- 2026-05-12 : ORCH-001 branche les générateurs DOC-001, DOC-002 et DOC-003 dans l'orchestrateur dossier ; génération DOCX uniquement.
- 2026-05-13 : logique documentaire du moteur formalisée par l'arbre document-centré V1 ; mémoire projet alignée sans réécriture de l'arbre.
- 2026-05-13 : SMOKE-001 génère réellement les trois DOCX du Lot 1 via l'orchestrateur avec `examples/contexts/lot_01_example.yaml` corrigé au strict minimum.
- 2026-05-13 : dictionnaire canonique des variables V1 intégré dans la mémoire projet ; le moteur dispose désormais d'un arbre documentaire et d'un dictionnaire canonique de variables.
- 2026-05-13 : table de mapping document -> variables canoniques V1 intégrée dans la mémoire projet sans réécriture ; écart temporaire `domiciliation.adresse_affichee` / `adresse_domiciliation_affichee` documenté.
- 2026-05-13 : cadrage métier V1 de la famille `PV nomination gérant` intégré dans la mémoire projet ; SPEC-PV-001 ajouté en READY et UI-001 placé en attente tant que cette famille n'est pas spécifiée.
- 2026-05-13 : spec canonique V1 de la famille `PV nomination gérant` intégrée dans la mémoire projet ; SPEC-PV-001 passé DONE, SPEC-TEXTE-PV-001 ajouté READY, UI-001 maintenu en attente explicite.
- 2026-05-13 : spec texte V1 de la famille `PV nomination gérant` créée ; SPEC-TEXTE-PV-001 passé DONE, CODE-PV-001 ajouté READY, aucun code Python modifié.
- 2026-05-13 : CODE-PV-001 implémente le générateur DOCX from-scratch du PV nomination gérant avec `associes[]`, `dirigeant_nomine`, branche `emprunt.actif`, variantes de genre/singulier-pluriel et tests ciblés ; ruff et pytest verts.
- 2026-05-13 : smoke test réel CODE-PV-001 ajouté via `examples/contexts/lot_02_pv_nomination_gerant_example.yaml` ; DOCX généré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/` hors versionnement.
- 2026-05-13 : REVIEW-PV-001 régénère le DOCX PV depuis le contexte exemple, extrait un aperçu texte et crée une checklist de revue humaine dans `docs/review/`, sans modification du code Python.
- 2026-05-13 : SPEC-RENDER-001 crée la spec technique `docs/delivery/render_style_system_v1.md` pour une couche de rendu DOCX commune, sans modification de code Python.
- 2026-05-13 : RENDER-STYLE-001 implémente la couche commune de rendu DOCX, migre DOC-001/DOC-002/DOC-003/PV nomination gérant, ajoute les tests de rendu et génère les smoke DOCX dans `artifacts/render_style_001_*`.
- 2026-05-13 : ORCH-L2-PV-001 branche le PV nomination gérant dans le catalogue et l'orchestrateur pour SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI et SCM ; SAS reste exclue ; ruff et pytest verts.
- 2026-05-13 : SMOKE-ORCH-L2-001 ajoute deux contextes orchestrateur Lot 2, génère réellement le dossier SCI positif et le dossier SAS négatif, puis documente la présence/absence du PV dans `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- 2026-05-13 : ANALYSE-ORDRE-001 crée les cadrages V1 pour `Demande d'inscription à l'ordre` et le batch `régime communautaire`, puis ajoute SPEC-ORDRE-001 et SPEC-RC-001 en READY, sans modification de code Python.
- 2026-05-13 : ARBITRAGE-SOURCES-001 répare les docs projet 10/11/12, crée les décisions d'arbitrage sources V1, classe les cas HIGH/MEDIUM/LOW et ajoute PLACEMENT-HIGH-001 en READY, sans déplacer de fichier source.
- 2026-05-14 : PLACEMENT-HIGH-001 confirme en no-op les 4 cas HIGH déjà présents dans `source_documents`, crée le journal d'exécution V1 et ne touche pas aux cas MEDIUM/LOW ni au raw dump.
- 2026-05-14 : SPEC-ORDRE-001 compare les variantes `Demande d'inscription à l'ordre` SELARL, SELAS et SPFPL, crée la spec canonique V1 et ajoute SPEC-TEXTE-ORDRE-001 en READY, sans modification de code Python.
- 2026-05-14 : SPEC-TEXTE-ORDRE-001 crée la spec texte V1 `Demande d'inscription à l'ordre`, retient un tronc commun avec overlays SELARL/SELAS, SPFPL cession/apport et SCM, classe `Dérogation ?` en bloc manuel conditionnel, puis ajoute CODE-ORDRE-001 en READY, sans modification de code Python.
- 2026-05-14 : FIX-PV-RENDER-001 améliore la structure visuelle du PV nomination gérant from-scratch : listes à tirets, titre encadré, intertitres visibles, formules de vote en italique et smoke DOCX dédié.
- 2026-05-14 : CODE-ORDRE-001 implémente le générateur DOCX from-scratch `Demande d'inscription à l'ordre`, couvre SELARL, SELAS, SPFPL cession, SPFPL apport et SCM, teste la dérogation manuelle et le mandataire configurable, puis génère un smoke DOCX dédié.
- 2026-05-14 : SPEC-RC-001 crée les specs canonique et texte V1 du batch régime communautaire, compare les variantes SELARL / SELAS / SPFPL, retient deux documents canoniques distincts et ajoute CODE-RC-001 en READY, sans modification de code Python.
- 2026-05-14 : SYNC-SPECS-001 absorbe dans `main` les specs parallèles RC, SPFPL, dérogations et cession/bail, puis aligne le pilotage sur `CODE-RC-001` READY, sans stage de code Python.
- 2026-05-14 : CODE-RC-001 implémente le batch régime communautaire V1 avec deux générateurs DOCX from-scratch, champs modèle dédiés, catalogue/orchestrateur conditionnés par `dossier_options.regime_communautaire`, tests ciblés et smoke DOCX réel.
- 2026-05-14 : SYNC-TEXTE-SPECS-001 absorbe dans `main` les specs texte parallèles bail/appel, cession cabinets, dérogations et SPFPL, puis confirme `CODE-BAIL-APP-001`, `ARBITRAGE-CESSION-001`, `ARBITRAGE-DEROG-001` et `ARBITRAGE-SPFPL-001` en READY, sans modification de code Python.
- 2026-05-14 : SYNC-ARBITRAGES-001 absorbe dans `main` les arbitrages cession cabinets, dérogations et SPFPL, passe les trois tickets d'arbitrage en DONE et confirme `CODE-BAIL-APP-001`, `CODE-CESSION-CAB-001` et `CODE-SPFPL-001` en READY, sans modification de code Python.
- 2026-05-14 : SYNC-CODE-BAIL-APP-001 absorbe dans `main` le commit `557a013274aa9f7122c81d5e6e0b52c4043a540c`, passe `CODE-BAIL-APP-001` en DONE et confirme `CODE-CESSION-CAB-001`, `PREP-DEROG-001` et `CODE-SPFPL-AGR-INFO-001` en READY/parallélisables, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-WAVE-LOT03-05-001 absorbe dans `main` les commits `36828fbc45d6b8a37c2e76eb8227460df441ebde` et `958fce5d2a9d5d30df4d918cb098fec483f5140e`, passe `PREP-DEROG-001` et `CODE-SPFPL-AGR-INFO-001` en DONE, puis confirme `RESUME-CODE-CESSION-CAB-001` et `CODE-DEROG-CORE-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : RESUME-CODE-CESSION-CAB-001 reprend `CODE-CESSION-CAB-001` depuis `main`, restaure les générateurs cession cabinets, branche `DOC-009` à `DOC-012`, génère quatre DOCX de smoke test et valide `ruff` / `pytest`.
- 2026-05-14 : CODE-DEROG-CORE-001 implémente les générateurs DOCX partiels `multi_sites_sel` et `cumul_sel_bnc`, les branche au catalogue/orchestrateur sous `DOC-013` et `DOC-014`, ajoute le contexte exemple et les tests ciblés, puis génère le smoke DOCX réel dans `artifacts/lot_03_derogations_core_smoke_test/`.
- 2026-05-14 : SYNC-CODE-WAVE-002 absorbe dans `main` les commits sources `ea35d2af353ac5b8567e82091ab978cf24a27445` et `bee4c8bec27397198a170c4f9888b2470b24c67f`, confirme `CODE-CESSION-CAB-001` et `CODE-DEROG-CORE-001` en DONE, puis confirme `CODE-SPFPL-CORE-001` et `PREP-STATUTS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-WAVE-003 absorbe dans `main` les commits sources `b854821061b85ac66fe785c11cb3c6b0bac5a85b` et `09cbad120d22910f05ba5e645971ade56fedb76d`, passe `PREP-STATUTS-001` et `CODE-SPFPL-CORE-001` en DONE, puis confirme `SPEC-STATUTS-SEL-001`, `SPEC-STATUTS-SPFPL-001`, `SPEC-STATUTS-CIVILS-001` et `SPEC-STATUTS-SAS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-STATUTS-SPECS-001 absorbe dans `main` les commits sources `00b7886ac431c8a47d9cdcca8bfed026a756cb69`, `b34c66e5e67f3261317035943e974536be27d6d3`, `9b25e09d08ec2161d757d1581c34073dcbbc594f` et `704eeb7301cf69460c16b2ed9fbc0ea22ca83c8c`, passe les quatre specs statuts en DONE, puis confirme `CODE-STATUTS-SAS-001`, `CODE-STATUTS-SPFPL-001`, `ARBITRAGE-STATUTS-SEL-001` et `ARBITRAGE-STATUTS-CIVILS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-STATUTS-CODE-ARB-001 absorbe dans `main` les commits sources `82e67120ed714b791d5483108336a570ea520e59`, `a98939c649e4124e40f2cd69c9ed125d342acc31` et `1caafd7`, passe `CODE-STATUTS-SAS-001`, `CODE-STATUTS-SPFPL-001` et `ARBITRAGE-STATUTS-SEL-001` en DONE, puis confirme `CODE-STATUTS-SEL-001`, `RESUME-ARBITRAGE-STATUTS-CIVILS-001` et `STYLE-ANALYSE-BATCH-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : SYNC-STYLE-CIVILS-001 absorbe dans `main` les commits sources `76dd139da65c233f0c6aecc76bc2ea5e929381ca` et `b21f1b0cc5b975049e4acc279b8303f1d739b60f`, passe `STYLE-ANALYSE-BATCH-001` et `ARBITRAGE-STATUTS-CIVILS-001` en DONE, puis confirme `CODE-STATUTS-SEL-001`, `CODE-STATUTS-CIVILS-CORE-001` et `FIX-STYLE-LETTERS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
