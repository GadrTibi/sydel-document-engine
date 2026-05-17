# Dernier état projet

## Date de mise à jour
2026-05-17


## Dernier ticket terminé
SYNC-FINAL-FOUNDATIONS-001 : synchronisation finale de `main` avant revue/cloture, absorption des complements UI/PDF/ZIP manquants, confirmation des audits/fondations presents, remplacement de `UI-CORE-001` par `UI-PDF-ZIP-INTEGRATION-001` et pilotage final limite a `REVIEW-FINAL-001` puis `CLOSE-PROJECT-V1-001`.

UI-PDF-ZIP-INTEGRATION-001 : integration de l'UI Streamlit avec la generation dossier DOCX, l'export PDF local optionnel et le ZIP dossier, avec telechargements par fichier, smoke manuel documente et validations locales vertes.

SYNC-POST-MOTOR-UI-001 : absorption dans `main` des fondations UI/PDF/recette issues des branches `codex/ui-flow-001`, `codex/ui-occurrences-001`, `codex/ui-form-schema-001`, `codex/pdf-backend-001` et `codex/recipe-frame-001`, puis réalignement du pilotage vers `UI-CORE-001`, `RESUME-ZIP-BACKEND-001` et `REVIEW-FINAL-001`.

PDF-BACKEND-001 : implementation d'un backend local d'export PDF depuis DOCX genere, avec priorite LibreOffice headless si disponible puis fallback Word COM Windows, erreurs explicites, tests ciblés, smoke réel DOCX vers PDF et aucune modification UI.

RECONCILE-MOTOR-CLOSE-001 : reconciliation finale du moteur DOCX V1, exposition des generateurs ordre/SPFPL sous `DOC-034` a `DOC-043`, consolidation des referentiels `08/09`, integration des audits `17/18`, requalification de l'audit `16`, validations ruff/pytest et cloture moteur hors UI/PDF/ZIP/recette finale.

SYNC-CLOSE-AUDIT-001 : absorption dans `main` du commit source `0139202b170531fd628f25811c55855a2512acc0` depuis `origin/codex/close-motor-audit-001`, confirmation de `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` et conservation de la version finale plus récente déjà présente dans `main`, sans modification de code Python.

FINAL-SCM-CESSION-WAVE-001 : restauration de la résolution V1 cession SCM depuis la branche d'arbitrage, implémentation du bloc cession SCM sous `DOC-031` à `DOC-033`, smoke DOCX réel, validations ruff/pytest et audit de clôture moteur V1.

SYNC-WAVE-010 : absorption finale dans `main` des branches `codex/arbitrage-scm-cession-resolve-001` et `codex/code-scm-cession-block-001`, passage en DONE des tickets SCM cession finaux et réalignement du pilotage vers UI, PDF, ZIP et recette finale.

SYNC-WAVE-009 : absorption dans `main` des commits sources `4288837648d099935d6c57307003f3b33d038d90`, `af1020a165d11e830428394e02a5baca4a110f5c`, `81f7a7e407002428d8fce1ce31d16f3a798bd2e5`, `fa3cb65ffd1055bbf16ba3a5352f4a7d5deb713a` et `bdf61166b0770c5ab8f3610f48d89e5cdcb3f582`, puis réalignement du pilotage.

SYNC-WAVE-008 : absorption dans `main` des branches acte actions, sources SCM cession, reviews Lot 03/Lot 04, audit restant, analyses style Lot 03/statuts et specs blocage cession SCM, puis réalignement du pilotage.

SYNC-WAVE-007 : absorption dans `main` des branches SCM et acte actions, passage en DONE des tickets absorbés et réalignement du pilotage.

SYNC-WAVE-006 : absorption dans `main` des branches tardives Lot 04 / Lot 05, passage en DONE des tickets absorbés et réalignement du pilotage.

CONVERT-ACTE-ACTIONS-001 : conversion du candidat legacy `Acte_cession_SPFPL_tiers_modele.doc` en DOCX exploitable, placement dans `project/source_documents/lot_05/` et documentation de préparation V1.

CONVERT-DEROG-SALARIEE-001 : tentative de conversion Word COM du `.doc` legacy salariee, aucun DOCX exploitable produit, blocage documente.

SYNC-WAVE-005 : absorption dans `main` des commits sources `91436f0916fdecbcc98450b72ba6e602cb8f1a3b`, `1b3ba14d0bcc31fc7dcbf1752d6d3263645ae8b3`, `32059155c618b4e985893f42ef2817187599c281`, `74d41db53543b790e197082e8b9c713f7de92dc2` et `d1d649e11fdc638e6d7da0640c154d1f213739ee`, puis réalignement du pilotage.

## État courant du repo
- DOC-001, DOC-002 et DOC-003 disposent chacun d'un générateur dédié déjà terminé.
- L'orchestrateur dossier expose :
  - un registre des générateurs DOC-001 à DOC-043 ;
  - `select_documents(structure)` selon le catalogue ;
  - `select_documents_for_context(ctx)` avec filtrage des batchs regime communautaire, bail/appel de fonds, cession cabinets, derogations, statuts, SPFPL, SCM satellites et cession SCM ;
  - `generate_documents(ctx, output_dir) -> list[Path]`.
- Le moteur documentaire DOCX V1 est feature complete et clos sur le perimetre deterministe valide, hors cas explicitement manuels ou legacy et hors UI/PDF/ZIP/recette finale.
- Le backend PDF V1 est disponible dans `src/sydel_doc_engine/rendering/pdf_export.py` : export unitaire DOCX vers PDF, export batch de chemins DOCX, detection de backend, erreurs bloquantes si aucun convertisseur fiable n'est disponible.
- Le backend ZIP V1 est disponible dans `src/sydel_doc_engine/rendering/zip_bundle.py` : ZIP deterministe DOCX/PDF, chemins relatifs, filtrage des fichiers temporaires et manifeste `manifest.json`.
- Strategie PDF locale retenue apres smoke : LibreOffice headless prioritaire si present ; Word COM Windows utilise localement avec succes. LibreOffice n'est pas installe sur la machine de smoke.
- L'UI Streamlit charge un contexte YAML/JSON, affiche la selection `select_documents_for_context`, genere les DOCX via `generate_documents`, propose les telechargements DOCX, lance les PDF si un backend local est disponible et cree un ZIP dossier via `rendering/zip_bundle.py`.
- Le smoke manuel UI/PDF/ZIP est documente dans `docs/review/ui_pdf_zip_integration_001_smoke.md`.
- `examples/contexts/lot_01_example.yaml` utilise encore le champ legacy Lot 1 `adresse_domiciliation_affichee`, en attente d'un refactor dédié vers `domiciliation.adresse_affichee`.
- Un smoke test réel a généré les trois DOCX du Lot 1 dans `artifacts/lot_01_smoke_test/`.
- Le moteur dispose de trois référentiels de cadrage :
  - arbre documentaire document-centré V1 : `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md` ;
  - dictionnaire canonique des variables V1 : `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md` ;
  - table de mapping document -> variables canoniques V1 : `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.
- Les audits/fondations finaux sont disponibles :
  - `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` ;
  - `docs/project/17_FINAL_ENGINE_QUALITY_AUDIT_V1.md` ;
  - `docs/project/18_NEXT_PHASE_FOUNDATION_V1.md` ;
  - `docs/project/19_UI_FLOW_V1.md` ;
  - `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md` ;
  - `docs/project/21_UI_FORM_SCHEMA_V1.md`.
- Le framework de recette finale V1 est disponible dans `docs/review/final_recipe_framework_v1.md`.
- `UI-CORE-001` est superseded / remplace par `UI-PDF-ZIP-INTEGRATION-001`.
- `RESUME-ZIP-BACKEND-001` est DONE.
- Tickets READY confirmes uniquement : `REVIEW-FINAL-001` et `CLOSE-PROJECT-V1-001`.
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
- Le blueprint de style batch V1 est disponible dans `docs/delivery/render_style_blueprint_batch_v1.md`.
- Le modèle de données supporte désormais les rôles canoniques nécessaires au PV :
  - `associes[]` ;
  - `dirigeant_nomine` ;
  - `decision` ;
  - `reunion` ;
  - `capital` ;
  - `emprunt` ;
  - `bien_immobilier`.
- Le modèle de données supporte désormais les rôles nécessaires à la demande d'inscription à l'ordre :
  - `dossier_options.derogation` ;
  - `personne_signataire.titre_affichage` ;
  - `personne_signataire.adresse_personnelle_affichee` ;
  - `ordre` ;
  - `mandataire`.
- Le modèle de données supporte désormais le batch régime communautaire :
  - `dossier_options.regime_communautaire` ;
  - `conjoint` ;
  - `apport` ;
  - `regime_communautaire.avertissement` ;
  - `regime_communautaire.renonciation`.
- Le modèle de données supporte désormais le mini-batch bail / appel de fonds :
  - `dossier_options.cession` ;
  - `bail` ;
  - `cession.cabinet` ;
  - `cession.financement` ;
  - `cession.vendeur` ;
  - `cession.acquereur`.
- Le PV nomination gérant est branché dans l'orchestrateur pour SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI et SCM.
- Le PV nomination gérant est exclu de la sélection SAS.
- FIX-PV-RENDER-001 est terminé : le PV dispose désormais d'un titre principal encadré, de listes à tirets pour les associés et les décisions, d'intertitres gras/soulignés, de formules de vote en italique et de signatures centrées.
- Deux contextes exemples d'orchestration Lot 2 sont disponibles :
  - `examples/contexts/lot_02_orchestrator_positive_example.yaml`
  - `examples/contexts/lot_02_orchestrator_negative_sas_example.yaml`
- Le smoke orchestrateur Lot 2 a généré les dossiers DOCX attendus :
  - `artifacts/lot_02_orchestrator_positive_smoke_test/`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/`
- La revue smoke orchestrateur Lot 2 est disponible : `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- Le cadrage V1 de la demande d'inscription à l'ordre est disponible : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`.
- La spec canonique V1 de la demande d'inscription à l'ordre est disponible : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`.
- La spec texte V1 de la demande d'inscription à l'ordre est disponible : `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.
- Le cadrage V1 du batch régime communautaire est disponible : `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- La spec canonique V1 du batch régime communautaire est disponible : `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md`.
- La spec texte V1 du batch régime communautaire est disponible : `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`.
- Les générateurs du batch régime communautaire sont disponibles :
  - `src/sydel_doc_engine/generators/lot_02/lettre_renonciation_associe.py` ;
  - `src/sydel_doc_engine/generators/lot_02/lettre_avertissement_conjoint.py`.
- Un contexte exemple de smoke test est disponible : `examples/contexts/lot_02_regime_communautaire_example.yaml`.
- La spec canonique V1 du batch SPFPL spécifique est disponible : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`.
- La spec texte V1 du batch SPFPL spécifique est disponible : `docs/delivery/lot_05_spfpl_spec_texte_v1.md`.
- Les arbitrages V1 du batch SPFPL spécifique sont disponibles : `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.
- Le sous-batch SPFPL agrément / note d'information est codé et testé :
  - `src/sydel_doc_engine/generators/lot_05/note_information.py` ;
  - `src/sydel_doc_engine/generators/lot_05/pv_agrement_cession_spfpl_associe_unique.py` ;
  - `src/sydel_doc_engine/generators/lot_05/pv_agrement_cession_spfpl_plusieurs_associes.py`.
- Un contexte exemple SPFPL agrément / note d'information est disponible : `examples/contexts/lot_05_spfpl_agrement_info_example.yaml`.
- Le cœur SPFPL restant est codé et testé :
  - `src/sydel_doc_engine/generators/lot_05/acte_cession_parts_spfpl.py` ;
  - `src/sydel_doc_engine/generators/lot_05/contrat_apport_spfpl.py` ;
  - `src/sydel_doc_engine/generators/lot_05/attestation_capital_liste_souscripteurs.py` ;
  - `src/sydel_doc_engine/generators/lot_05/attestation_commissaire_apports.py`.
- Un contexte exemple SPFPL cœur est disponible : `examples/contexts/lot_05_spfpl_core_example.yaml`.
- La spec canonique V1 de la famille dérogations est disponible : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`.
- La spec texte V1 de la famille dérogations est disponible : `docs/delivery/lot_03_derogations_spec_texte_v1.md`.
- Les arbitrages V1 de la famille dérogations sont disponibles : `docs/delivery/lot_03_derogations_arbitrages_v1.md`.
- La préparation sources dérogations V1 est disponible :
  - `docs/delivery/lot_03_derogations_preparation_v1.md` ;
  - `docs/delivery/lot_03_derogations_legacy_conversion_report_v1.md`.
- La spec canonique V1 `cession cabinets` est disponible : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`.
- La spec texte V1 `cession cabinets` est disponible : `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.
- Les arbitrages V1 `cession cabinets` sont disponibles : `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`.
- La spec canonique V1 `bail / appel de fonds` est disponible : `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`.
- La spec texte V1 `bail / appel de fonds` est disponible : `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`.
- Les générateurs du mini-batch bail / appel de fonds sont disponibles :
  - `src/sydel_doc_engine/generators/lot_03/avenant_contrat_bail.py` ;
  - `src/sydel_doc_engine/generators/lot_03/appel_fond_sel.py`.
- Le catalogue et l'orchestrateur exposent désormais :
  - `DOC-007` : avenant au contrat de bail ;
  - `DOC-008` : appel de fonds SEL.
- Un contexte exemple du mini-batch bail / appel de fonds est disponible : `examples/contexts/lot_03_bail_appel_fonds_example.yaml`.
- Les générateurs cession cabinets sont disponibles :
  - `src/sydel_doc_engine/generators/lot_03/acte_cession_cabinet_medical.py` ;
  - `src/sydel_doc_engine/generators/lot_03/compromis_cession_cabinet_medical.py` ;
  - `src/sydel_doc_engine/generators/lot_03/acte_cession_cabinet_dentaire.py` ;
  - `src/sydel_doc_engine/generators/lot_03/compromis_cession_cabinet_dentaire.py`.
- Le catalogue et l'orchestrateur exposent désormais :
  - `DOC-009` : acte de cession d'un cabinet médical ;
  - `DOC-010` : compromis de cession d'un cabinet médical ;
  - `DOC-011` : acte de cession d'un cabinet dentaire ;
  - `DOC-012` : compromis de cession d'un cabinet dentaire.
- Un contexte exemple cession cabinets est disponible : `examples/contexts/lot_03_cession_cabinets_example.yaml`.
- Le manifest d'import sources V1 est disponible : `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md`.
- Le rapport de doublons sources V1 est disponible : `docs/project/11_SOURCE_DUPLICATES_REPORT_V1.md`.
- Le plan de placement sources V1 est disponible : `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`.
- Les décisions d'arbitrage sources V1 sont disponibles : `docs/project/13_SOURCE_ARBITRATION_DECISIONS_V1.md`.
- Le journal d'exécution du placement HIGH V1 est disponible : `docs/project/14_SOURCE_PLACEMENT_EXECUTION_V1.md`.
- La préparation V1 des sources statuts est disponible : `docs/delivery/lot_04_statuts_preparation_v1.md`.
- Les specs V1 des statuts SAS sont disponibles :
  - `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md` ;
  - `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`.
- Les specs V1 des statuts SPFPL sont disponibles :
  - `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md` ;
  - `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`.
- Les specs V1 des statuts SEL d'exercice sont disponibles :
  - `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` ;
  - `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.
- Les specs V1 des statuts civils sont disponibles :
  - `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` ;
  - `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.
- Le générateur statuts SAS V1 est disponible dans `src/sydel_doc_engine/generators/lot_04/statuts_sas.py`.
- Les générateurs statuts civils V1 sont disponibles :
  - `src/sydel_doc_engine/generators/lot_04/statuts_scs.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_sci.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_sci_iris.py`.
- Le modèle de données supporte désormais `statuts_civils` pour SCS, SCI et SCI IRIS : associés dynamiques, apports, parts, dépôt de capital et groupes de résultat exceptionnel SCI IRIS.
- Le générateur statuts SCM V1 est disponible dans `src/sydel_doc_engine/generators/lot_04/statuts_scm.py` et branché sous `DOC-025`.
- Les générateurs statuts SPFPL V1 sont disponibles :
  - `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_cession.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_apport.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_common.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_templates.py`.
- Les générateurs statuts SEL d'exercice V1 sont disponibles :
  - `src/sydel_doc_engine/generators/lot_04/statuts_selarl_dentiste.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_selarl_medecin.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_selas_medecin.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_sel_exercice_common.py` ;
  - `src/sydel_doc_engine/generators/lot_04/statuts_sel_exercice_templates.py`.
- Les arbitrages V1 des statuts SEL d'exercice sont disponibles dans `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`.
- Les arbitrages V1 des statuts civils sont disponibles dans `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.
- Les arbitrages V1 des statuts SCM sont disponibles dans `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md`.
- La préparation V1 des satellites SCM est disponible dans `docs/delivery/lot_05_scm_satellites_preparation_v1.md`.
- Les specs V1 des satellites SAS sont disponibles :
  - `docs/delivery/lot_05_sas_satellites_spec_canonique_v1.md` ;
  - `docs/delivery/lot_05_sas_satellites_spec_texte_v1.md`.
- La lettre option IS est codée et testée :
  - `src/sydel_doc_engine/generators/lot_05/lettre_option_is.py` ;
  - `tests/unit/test_lettre_option_is.py` ;
  - `examples/contexts/lot_05_lettre_option_is_example.yaml`.
- Les satellites SCM DOCX hors liste dépenses sont codés et testés :
  - `src/sydel_doc_engine/generators/lot_05/pacte_associes_scm.py` ;
  - `src/sydel_doc_engine/generators/lot_05/contrat_frais_communs.py` ;
  - `src/sydel_doc_engine/generators/lot_05/reglement_interieur_scm.py`.
- Le catalogue et l'orchestrateur exposent désormais :
  - `DOC-026` : pacte d'associés SCM ;
  - `DOC-027` : contrat d'exercice professionnel à frais communs ;
  - `DOC-028` : règlement intérieur de la SCM.
- L'audit V1 de l'acte de cession d'actions est disponible dans `docs/delivery/lot_05_acte_cession_actions_audit_v1.md`.
- Les specs V1 de l'acte de cession d'actions sont disponibles :
  - `docs/delivery/lot_05_acte_cession_actions_spec_canonique_v1.md` ;
  - `docs/delivery/lot_05_acte_cession_actions_spec_texte_v1.md`.
- Le générateur acte de cession d'actions SPFPL est disponible dans `src/sydel_doc_engine/generators/lot_05/acte_cession_actions_spfpl.py` et branché sous `DOC-029`.
- Un contexte exemple acte de cession d'actions SPFPL est disponible dans `examples/contexts/lot_05_acte_cession_actions_example.yaml`.
- La préparation V1 des sources cession SCM est disponible dans `docs/delivery/lot_05_scm_cession_sources_preparation_v1.md`.
- Les sources cession SCM exploitables sont placées dans `project/source_documents/lot_05/`.
- Les specs V1 du blocage cession SCM sont disponibles :
  - `docs/delivery/lot_05_scm_cession_block_spec_canonique_v1.md` ;
  - `docs/delivery/lot_05_scm_cession_block_spec_texte_v1.md`.
- La résolution V1 du bloc cession SCM est disponible dans `docs/delivery/lot_05_scm_cession_block_resolution_v1.md`.
- Le bloc cession SCM est codé, testé et branché :
  - `DOC-031` : PV AGE cession part SCM ;
  - `DOC-032` : courrier SDE cession SCM ;
  - `DOC-033` : acte de cession de parts SCM vers SEL.
- Les générateurs cession SCM sont disponibles :
  - `src/sydel_doc_engine/generators/lot_05/pv_age_cession_scm.py` ;
  - `src/sydel_doc_engine/generators/lot_05/courrier_sde_cession_scm.py` ;
  - `src/sydel_doc_engine/generators/lot_05/acte_cession_parts_scm.py`.
- Un contexte exemple cession SCM est disponible : `examples/contexts/lot_05_scm_cession_block_example.yaml`.
- L'audit de clôture moteur V1 est disponible dans `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md`.
- Les revues batch Lot 03 et Lot 04 sont disponibles :
  - `docs/review/lot_03_batch_review_v1.md` ;
  - `docs/review/lot_04_batch_review_v1.md`.
- L'audit du périmètre restant V1 est disponible dans `docs/project/15_REMAINING_SCOPE_AUDIT_V1.md`.
- Les blueprints style dédiés sont disponibles :
  - `docs/delivery/render_style_blueprint_lot03_batch_v1.md` ;
  - `docs/delivery/render_style_blueprint_statuts_batch_v1.md`.
- `ARBITRAGE-SOURCES-001` est DONE.
- `PLACEMENT-HIGH-001` est DONE.
- `ANALYSE-ORDRE-001` est DONE.
- `SPEC-ORDRE-001` est DONE.
- `SPEC-TEXTE-ORDRE-001` est DONE.
- `CODE-ORDRE-001` est DONE.
- `SPEC-RC-001` est DONE.
- `SPEC-SPFPL-001` est DONE.
- `SPEC-DEROG-001` est DONE.
- `SPEC-CESSION-BAIL-001` est DONE.
- `SYNC-SPECS-001` est DONE.
- `CODE-RC-001` est DONE.
- `SPEC-TEXTE-BAIL-APP-001` est DONE.
- `SPEC-TEXTE-CESSION-CAB-001` est DONE.
- `SPEC-TEXTE-DEROG-001` est DONE.
- `SPEC-TEXTE-SPFPL-001` est DONE.
- `SYNC-TEXTE-SPECS-001` est DONE.
- `SYNC-ARBITRAGES-001` est DONE.
- `CODE-BAIL-APP-001` est DONE.
- `ARBITRAGE-CESSION-001` est DONE.
- `ARBITRAGE-DEROG-001` est DONE.
- `ARBITRAGE-SPFPL-001` est DONE.
- `CODE-CESSION-CAB-001` est DONE.
- `RESUME-CODE-CESSION-CAB-001` est DONE.
- `PREP-DEROG-001` est DONE.
- `CODE-DEROG-CORE-001` est DONE.
- `CODE-SPFPL-AGR-INFO-001` est DONE.
- `CODE-SPFPL-CORE-001` est DONE.
- `PREP-STATUTS-001` est DONE.
- `SPEC-STATUTS-SEL-001` est DONE.
- `SPEC-STATUTS-SPFPL-001` est DONE.
- `SPEC-STATUTS-CIVILS-001` est DONE.
- `SPEC-STATUTS-SAS-001` est DONE.
- `SYNC-STATUTS-SPECS-001` est DONE.
- `CODE-STATUTS-SAS-001` est DONE.
- `CODE-STATUTS-SPFPL-001` est DONE.
- `ARBITRAGE-STATUTS-SEL-001` est DONE.
- `ARBITRAGE-STATUTS-CIVILS-001` est DONE.
- `SYNC-STATUTS-CODE-ARB-001` est DONE.
- `CODE-STATUTS-SEL-001` est DONE.
- `CODE-STATUTS-CIVILS-CORE-001` est DONE pour SCS, SCI et SCI IRIS ; SCM reste hors ticket.
- `FIX-STYLE-LETTERS-001` est DONE.
- `RESUME-FIX-STYLE-LETTERS-001` est DONE.
- `ARBITRAGE-STATUTS-SCM-001` est DONE.
- `PREP-SCM-SAT-001` est DONE.
- `SPEC-SAS-SATELLITES-001` est DONE.
- `CODE-OPTION-IS-001` est DONE.
- `PREP-ACTE-ACTIONS-001` est DONE.
- `SYNC-WAVE-005` est DONE.
- `SYNC-WAVE-006` est DONE.
- `SYNC-WAVE-007` est DONE.
- `CODE-STATUTS-SCM-001` est DONE.
- `CODE-SAS-SATELLITES-001` est DONE.
- `SPEC-SCM-SATELLITES-001` est DONE.
- `CONVERT-DEROG-SALARIEE-001` est DONE.
- `CONVERT-ACTE-ACTIONS-001` est DONE.
- `PREP-SCM-LISTE-DEPENSES-CONVERT-001` est DONE.
- `CODE-SCM-SAT-DOCX-001` est DONE.
- `SPEC-ACTE-ACTIONS-001` est DONE.
- `CODE-ACTE-ACTIONS-001` est DONE.
- `PREP-SCM-CESSION-SOURCES-001` est DONE.
- `REVIEW-BATCH-LOT03-001` est DONE.
- `REVIEW-BATCH-LOT04-001` est DONE.
- `AUDIT-REMAINING-SCOPE-001` est DONE.
- `STYLE-ANALYSE-LOT03-BATCH-001` est DONE.
- `STYLE-ANALYSE-STATUTS-BATCH-001` est DONE.
- `SPEC-SCM-CESSION-BLOCK-001` est DONE.
- `SYNC-WAVE-008` est DONE.
- `CODE-SCM-CESSION-BLOCK-001` est DONE.
- `CODE-SCM-LISTE-DEPENSES-001` est DONE.
- `SPEC-DEROG-SALARIEE-MANUAL-001` est DONE.
- `FIX-STYLE-LOT03-BATCH-001` est DONE.
- `FIX-STYLE-STATUTS-BATCH-001` est DONE.
- `REVIEW-BATCH-LOT05-001` est DONE.
- `SYNC-WAVE-009` est DONE.
- `ARBITRAGE-SCM-CESSION-RESOLVE-001` est DONE.
- `SYNC-WAVE-010` est DONE.
- `FINAL-SCM-CESSION-WAVE-001` est DONE.
- `SYNC-CLOSE-AUDIT-001` est DONE.
- `RECONCILE-MOTOR-CLOSE-001` est DONE.
- `RESUME-ARBITRAGE-STATUTS-CIVILS-001` est DONE, remplacé par l'arbitrage civils V1 absorbé.
- `STYLE-ANALYSE-BATCH-001` est DONE.
- `SYNC-STYLE-CIVILS-001` est DONE.
- `SYNC-STATUTS-SEL-CIVILS-001` est DONE.
- `UI-001` reste explicitement en attente : ne pas brancher Streamlit maintenant.
- Fichiers générés connus :
  - `artifacts/lot_01_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_01_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_01_smoke_test/procuration.docx`
  - `artifacts/lot_05_scm_cession_block_smoke_test/pv_age_cession_parts_scm.docx`
  - `artifacts/lot_05_scm_cession_block_smoke_test/courrier_sde_cession_scm.docx`
  - `artifacts/lot_05_scm_cession_block_smoke_test/acte_cession_parts_scm.docx`
  - `artifacts/lot_02_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/procuration.docx`
  - `artifacts/lot_02_orchestrator_positive_smoke_test/pv_nomination_gerant.docx`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/declaration_non_condamnation.docx`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/autorisation_domiciliation.docx`
  - `artifacts/lot_02_orchestrator_negative_sas_smoke_test/procuration.docx`
  - `artifacts/lot_02_demande_inscription_ordre_smoke_test/demande_inscription_ordre.docx`
  - `artifacts/lot_02_regime_communautaire_smoke_test/lettre_renonciation_associe.docx`
  - `artifacts/lot_02_regime_communautaire_smoke_test/lettre_avertissement_conjoint.docx`
  - `artifacts/lot_03_cession_cabinets_smoke_test/acte_cession_cabinet_medical.docx`
  - `artifacts/lot_03_cession_cabinets_smoke_test/compromis_cession_cabinet_medical.docx`
  - `artifacts/lot_03_cession_cabinets_smoke_test/acte_cession_cabinet_dentaire.docx`
  - `artifacts/lot_03_cession_cabinets_smoke_test/compromis_cession_cabinet_dentaire.docx`
  - `artifacts/lot_03_derogations_core_smoke_test/formulaire_derogation_sites_sel_formulaire_a_completer.docx`
  - `artifacts/lot_03_derogations_core_smoke_test/demande_derogation_cumul_selarl_bnc_formulaire_a_completer.docx`
  - `artifacts/lot_04_statuts_civils_core_smoke_test/statuts_scs.docx`
  - `artifacts/lot_04_statuts_civils_core_smoke_test/statuts_sci.docx`
  - `artifacts/lot_04_statuts_civils_core_smoke_test/statuts_sci_iris.docx`
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
- Le batch régime communautaire est désormais suffisamment spécifié pour ouvrir `CODE-RC-001`.
- Pour le batch régime communautaire, la mutualisation réaliste porte surtout sur les variables, les rôles, les montants et les helpers de rendu ; deux documents canoniques distincts restent recommandés.
- SPEC-RC-001 compare les variantes SELARL, SELAS et SPFPL du batch régime communautaire.
- Le groupe source Lot 2 / SELAS / SPFPL est retenu comme canonique pour la renonciation ; la variante SELARL brute reste documentée comme écart à relire.
- L'avertissement conserve un overlay limité pour la mention manuscrite SELARL (`à la Société ...`) contre SELAS/SPFPL (`à la [forme_sociale_abregee] ...`).
- CODE-RC-001 produit deux documents canoniques distincts, uniquement pour SELARL, SELAS, SPFPL cession et SPFPL apport lorsque `dossier_options.regime_communautaire == true`.
- CODE-RC-001 ajoute les entrées catalogue `DOC-005` et `DOC-006`, enregistrées dans l'orchestrateur.
- Le filtrage contexte exclut `DOC-005` et `DOC-006` lorsque l'option régime communautaire est fausse.
- La mention manuscrite de l'avertissement applique l'overlay SELARL `à la Société ...` et l'overlay SELAS/SPFPL `à la {forme_sociale_abregee} ...`.
- La renonciation résout `date_courrier_avertissement` explicitement ou par repli sur la date de l'avertissement du batch.
- SPEC-SPFPL-001 formalise le batch SPFPL spécifique sans code Python ; l'acte de cession d'actions reste bloqué faute de source DOCX confirmée.
- SPEC-DEROG-001 formalise les dérogations sans automatiser les formulaires marqués ou traités comme manuels.
- SPEC-CESSION-BAIL-001 formalise deux blocs distincts : `cession cabinets` et `bail / appel de fonds`, sans trancher les anomalies de wording avant code.
- SYNC-SPECS-001 a cherry-pické les quatre specs parallèles dans `main`, puis limite le commit de synchronisation aux fichiers de pilotage.
- SYNC-TEXTE-SPECS-001 a cherry-pické les quatre specs texte parallèles dans `main`.
- Les specs texte intégrées sont bail/appel, cession cabinets, dérogations et SPFPL.
- Le commit final de synchronisation texte est limité aux fichiers de pilotage `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md`.
- Aucun code Python, aucun fichier `project/source_import/raw_drive_dump/` et aucun fichier `artifacts/` n'a été modifié.
- SYNC-ARBITRAGES-001 a cherry-pické les trois arbitrages parallèles dans `main`.
- Les arbitrages intégrés sont cession cabinets, dérogations et SPFPL.
- Le commit final de synchronisation arbitrages est limité aux fichiers de pilotage `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md`.
- Aucun code Python, aucun fichier `project/source_import/raw_drive_dump/` et aucun fichier `artifacts/` n'a été modifié.
- SYNC-CODE-BAIL-APP-001 a absorbé par fast-forward le commit `557a013274aa9f7122c81d5e6e0b52c4043a540c` de `codex/code-bail-app-001` dans `main`.
- CODE-BAIL-APP-001 ajoute `DOC-007` avenant au contrat de bail et `DOC-008` appel de fonds SEL au catalogue et à l'orchestrateur.
- L'avenant au contrat de bail est sélectionné pour SELARL/SELAS lorsque `dossier_options.cession == true`.
- L'appel de fonds SEL est sélectionné uniquement pour SELARL dentaire lorsque `dossier_options.cession == true`.
- Les fichiers `project/source_import/raw_drive_dump/` et `artifacts/` n'ont pas été modifiés.
- SYNC-WAVE-LOT03-05-001 a cherry-pické dans `main` les commits `36828fbc45d6b8a37c2e76eb8227460df441ebde` de `codex/prep-derog-001` et `958fce5d2a9d5d30df4d918cb098fec483f5140e` de `codex/code-spfpl-agr-info-001`.
- PREP-DEROG-001 place les deux sources Lot 03 préparées et ajoute les rapports de préparation / conversion legacy.
- CODE-SPFPL-AGR-INFO-001 ajoute les générateurs SPFPL agrément et note d'information, les sources Lot 05 ciblées, le contexte exemple et les tests unitaires associés.
- Les fichiers `project/source_import/raw_drive_dump/` et `artifacts/` n'ont pas été modifiés.
- SYNC-CODE-WAVE-002 a cherry-pické dans `main` les commits sources `ea35d2af353ac5b8567e82091ab978cf24a27445` de `codex/code-cession-cab-001` et `bee4c8bec27397198a170c4f9888b2470b24c67f` de `codex/code-derog-core-001`.
- Le commit final de synchronisation `SYNC-CODE-WAVE-002` est limité aux fichiers de pilotage `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md`.
- Les fichiers `project/source_import/raw_drive_dump/` et `artifacts/` n'ont pas été modifiés.
- SYNC-WAVE-003 a cherry-pické dans `main` les commits sources `b854821061b85ac66fe785c11cb3c6b0bac5a85b` de `codex/prep-statuts-001` et `09cbad120d22910f05ba5e645971ade56fedb76d` de `codex/code-spfpl-core-001`.
- PREP-STATUTS-001 ajoute la préparation documentaire Lot 04 statuts et place les sources statuts retenues dans `project/source_documents/lot_04/`, sans déduplication ni harmonisation juridique.
- CODE-SPFPL-CORE-001 ajoute les générateurs SPFPL cœur, les sources Lot 05 ciblées, le contexte exemple et les tests unitaires associés.
- Le commit final de synchronisation `SYNC-WAVE-003` est limité aux fichiers de pilotage `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md`.
- Les fichiers `project/source_import/raw_drive_dump/` et `artifacts/` n'ont pas été modifiés.
- SYNC-STATUTS-CODE-ARB-001 a cherry-pické dans `main` les commits sources `82e67120ed714b791d5483108336a570ea520e59`, `a98939c649e4124e40f2cd69c9ed125d342acc31` et `1caafd7`.
- Le conflit modèle entre les apports SAS et SPFPL a été résolu par fusion additive des champs de données nécessaires aux deux familles.
- CODE-STATUTS-SAS-001 ajoute le générateur statuts SAS V1, son contexte exemple, son branchement catalogue/orchestrateur et ses tests ciblés.
- CODE-STATUTS-SPFPL-001 ajoute les générateurs statuts SPFPL cession/apport V1, leur contexte exemple et leurs tests ciblés.
- ARBITRAGE-STATUTS-SEL-001 ajoute les arbitrages V1 des statuts SEL d'exercice dans `docs/delivery/`.
- Les fichiers `project/source_import/raw_drive_dump/` et `artifacts/` n'ont pas été modifiés.
- CODE-DEROG-CORE-001 ajoute `DOC-013` formulaire multi-sites SEL et `DOC-014` demande cumul SELARL/BNC au catalogue et à l'orchestrateur.
- Les deux documents dérogations cœur sont rendus uniquement en `formulaire_a_completer`, avec zones narratives sensibles laissées visibles et non générées par défaut.
- `cumul_salariee` reste hors périmètre tant qu'un DOCX propre n'est pas fourni.
- ARBITRAGE-SOURCES-001 scanne 147 fichiers dans `project/source_import/raw_drive_dump/` et 11 fichiers dans `project/source_documents/`.
- ARBITRAGE-SOURCES-001 identifie 18 groupes de doublons probables, dont 15 groupes de doublons exacts.
- Les 4 cas HIGH documentés sont : DOC-001, DOC-002, DOC-003 et la source canonique `PV nomination gérant`.
- PLACEMENT-HIGH-001 confirme que les 4 cas HIGH sont déjà présents aux emplacements retenus dans `project/source_documents/`.
- PLACEMENT-HIGH-001 n'a effectué aucune nouvelle copie, car chaque cible HIGH existait déjà.
- PLACEMENT-HIGH-001 crée `docs/project/14_SOURCE_PLACEMENT_EXECUTION_V1.md`.
- SPEC-ORDRE-001 compare les variantes raw dump SELARL, SELAS et SPFPL de `Demande d'inscription à l'ordre`.
- Pour cette famille, SELARL et SELAS ont un texte visible identique et plus paramétré ; le groupe SPFPL/source Lot 2 est une copie exacte incluant la mention résiduelle `Dérogation ?`.
- Les structures retenues pour la famille ordre sont SELARL, SELAS, SPFPL cession, SPFPL apport et SCM ; aucune variante SCM dédiée n'a été retrouvée dans le raw dump.
- SPEC-TEXTE-ORDRE-001 retient un tronc commun texte fixe et trois overlays : SELARL/SELAS, SPFPL cession/apport et SCM.
- La mention source `Dérogation ?` n'est pas un wording juridique automatique ; elle devient un bloc conditionnel manuel qui bloque si `dossier.options.derogation == true` sans mention fournie.
- `Dr`, `Monsieur le Président`, la profession ordinale et l'adresse ordinale restent variables ou blocs variables.
- Le mandataire SYDEL peut être préconfiguré, mais ne doit pas être codé en dur dans le générateur.
- CODE-ORDRE-001 implémente le générateur `Demande d'inscription à l'ordre` dans `src/sydel_doc_engine/generators/lot_02/demande_inscription_ordre.py`.
- Le générateur ordre couvre explicitement SELARL, SELAS, SPFPL cession, SPFPL apport et SCM.
- Les overlays SELARL/SELAS, SPFPL et SCM pilotent le rendu de l'adresse ordinale, sans wording SCM spécifique ajouté.
- Le bloc `Dérogation ?` n'est jamais rendu littéralement ; si `dossier_options.derogation=true`, une mention manuelle `ordre.derogation_mention_manuelle` est obligatoire.
- Le mandataire est résolu depuis `mandataire.libelle_affiche` ou depuis les champs détaillés, sans constante SYDEL/Jordan ELBAZ codée dans le générateur.
- Le smoke DOCX dédié a été généré dans `artifacts/lot_02_demande_inscription_ordre_smoke_test/demande_inscription_ordre.docx`, hors versionnement.
- Les 2 cas MEDIUM régime communautaire sont désormais spécifiés et codés dans `CODE-RC-001`.
- Les 3 cas LOW restent bloqués : statuts, liste des souscripteurs / attestation sur le capital, documents sans source claire.
- 16 documents sources sont explicitement hors périmètre moteur courant.
- Aucun fichier de `project/source_import/raw_drive_dump/` ni de `artifacts/` n'a été modifié ; les seules sources ajoutées par la vague sont placées sous `project/source_documents/lot_05/`.
- Aucune UI, aucun PDF, aucun ZIP et aucun wording juridique source n'ont été modifiés.
- FIX-PV-RENDER-001 conserve l'approche from-scratch et ne modifie pas le texte juridique ; les changements portent uniquement sur le rendu DOCX du PV et un helper commun de liste à tiret.
- Le smoke DOCX dédié a été généré dans `artifacts/fix_pv_render_001_smoke_test_2/pv_nomination_gerant.docx`, hors versionnement.

## Prochain ticket à lancer
Prochains chantiers recommandés :
- UI ;
- PDF batch/orchestrateur ;
- ZIP ;
- recette finale.

`SYNC-POST-MOTOR-UI-001` est DONE : les commits UI/PDF/recette `d62670efe10481926437c0e1a5dabbe349fd5938`, `24a881b999371811d39a2403c0b51d9ae8ce0556`, `ef6252b3c15dc3fc39f1efdc05687c0f448f8fe1`, `2f76f61848469ddf2f7b29c3169e8893e83fd3a5` et `c2fc0db4d51485c7c5e721c5184028ae17c68cb3` sont absorbés dans `main`.

`UI-FLOW-001`, `UI-OCCURRENCES-001`, `UI-FORM-SCHEMA-001`, `PDF-BACKEND-001` et `RECIPE-FRAME-001` sont DONE.

`UI-CORE-001`, `RESUME-ZIP-BACKEND-001` et `REVIEW-FINAL-001` sont READY.

`PDF-BACKEND-001` est DONE : le backend PDF local est disponible et intégré à la fondation absorbée, sans ticket PDF supplémentaire confirmé dans cette synchronisation.

`RECONCILE-MOTOR-CLOSE-001` est DONE : le runtime expose `DOC-001` à `DOC-043`, les audits `16/17` concluent la couverture globale OK du moteur DOCX V1, et `docs/project/18_NEXT_PHASE_FOUNDATION_V1.md` cadre la suite UI/PDF/ZIP/recette finale.

`SYNC-CLOSE-AUDIT-001` est DONE : le commit source `0139202b170531fd628f25811c55855a2512acc0` a été absorbé depuis `origin/codex/close-motor-audit-001` par merge de synchronisation ; l'audit présent sur `main` reste la version finale plus récente.

`ARBITRAGE-SCM-CESSION-RESOLVE-001` et `CODE-SCM-CESSION-BLOCK-001` sont DONE et absorbés dans `main` via SYNC-WAVE-010.

`CODE-SCM-LISTE-DEPENSES-001`, `SPEC-DEROG-SALARIEE-MANUAL-001`, `REVIEW-BATCH-LOT05-001`, `FIX-STYLE-STATUTS-BATCH-001` et `FIX-STYLE-LOT03-BATCH-001` sont DONE et absorbés dans `main` via SYNC-WAVE-009.
`CODE-OPTION-IS-001`, `PREP-SCM-SAT-001`, `ARBITRAGE-STATUTS-SCM-001`, `SPEC-SAS-SATELLITES-001` et `PREP-ACTE-ACTIONS-001` sont DONE et absorbés dans `main`.
`RESUME-FIX-STYLE-LETTERS-001`, `CODE-STATUTS-CIVILS-CORE-001`, `CODE-SAS-SATELLITES-001`, `CONVERT-DEROG-SALARIEE-001`, `CONVERT-ACTE-ACTIONS-001` et `SPEC-SCM-SATELLITES-001` sont DONE et absorbés dans `main` via SYNC-WAVE-006.
`CODE-STATUTS-SCM-001`, `PREP-SCM-LISTE-DEPENSES-CONVERT-001`, `CODE-SCM-SAT-DOCX-001` et `SPEC-ACTE-ACTIONS-001` sont DONE et absorbés dans `main` via SYNC-WAVE-007.
`CODE-ACTE-ACTIONS-001`, `PREP-SCM-CESSION-SOURCES-001`, `REVIEW-BATCH-LOT03-001`, `REVIEW-BATCH-LOT04-001`, `AUDIT-REMAINING-SCOPE-001`, `STYLE-ANALYSE-LOT03-BATCH-001`, `STYLE-ANALYSE-STATUTS-BATCH-001` et `SPEC-SCM-CESSION-BLOCK-001` sont DONE et absorbés dans `main` via SYNC-WAVE-008.
`CONVERT-ACTE-ACTIONS-001` est DONE avec DOCX placé dans `project/source_documents/lot_05/` et préparation V1 documentée.
`CONVERT-DEROG-SALARIEE-001` est DONE ; aucun DOCX exploitable n'a ete produit.
`CODE-BAIL-APP-001` est DONE dans `main`.
`PREP-DEROG-001` et `CODE-SPFPL-AGR-INFO-001` sont DONE dans `main`.
`CODE-CESSION-CAB-001` et `CODE-DEROG-CORE-001` sont DONE et absorbés dans `main`.
`PREP-STATUTS-001` et `CODE-SPFPL-CORE-001` sont DONE et absorbés dans `main`.
Les quatre specs statuts SAS, SPFPL, SEL et civils sont DONE et absorbées dans `main`.
`CODE-STATUTS-SAS-001`, `CODE-STATUTS-SPFPL-001` et `ARBITRAGE-STATUTS-SEL-001` sont DONE et absorbés dans `main`.
`STYLE-ANALYSE-BATCH-001` et `ARBITRAGE-STATUTS-CIVILS-001` sont DONE et absorbés dans `main`.
`CODE-STATUTS-SEL-001` est DONE et absorbé dans `main`.
`RESUME-FIX-STYLE-LETTERS-001`, `FIX-STYLE-LETTERS-001` et `CODE-STATUTS-CIVILS-CORE-001` sont DONE et absorbés dans `main`.

## Points ouverts
- Aucun point bloquant moteur DOCX restant après `RECONCILE-MOTOR-CLOSE-001`.
- Restent hors périmètre moteur : UI, ZIP, recette finale, revue humaine juridique/visuelle, documents explicitement manuels et sources legacy non converties.
- PDF-BACKEND-001 est terminé : export DOCX vers PDF disponible en backend local, sans intégration UI.
- Points ouverts PDF après PDF-BACKEND-001 : LibreOffice absent localement, fallback Word COM validé sur smoke, conversion batch/orchestrateur et revue visuelle PDF restent à traiter séparément.
- Fondation UI/PDF/recette synchronisée : `UI-CORE-001`, `RESUME-ZIP-BACKEND-001` et `REVIEW-FINAL-001` sont les prochains tickets READY confirmés.
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Le smoke test confirme la production de trois fichiers DOCX, mais ne remplace pas une revue humaine du rendu visuel ni une validation juridique fine du contenu généré.
- PDF batch/orchestrateur et ZIP restent à intégrer dans des tickets ultérieurs.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'à refactor dédié.
- Le PV nomination gérant est codé, testé et branché dans l'orchestrateur pour les structures concernées.
- Le smoke orchestrateur Lot 2 est vert sur SCI positif et SAS négatif.
- Le pack REVIEW-PV-001 est prêt, mais il ne vaut pas validation juridique.
- La couche commune de rendu DOCX est implémentée.
- Le rendu PV restauré par FIX-PV-RENDER-001 reste soumis à revue humaine visuelle/juridique fine ; le ticket ne vaut pas validation juridique.
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
- Points ouverts demande d'inscription à l'ordre après CODE-ORDRE-001 :
  - absence de variante SCM dédiée dans le raw dump, à compenser par une revue humaine du premier rendu SCM ;
  - wording de dérogation non validé, donc bloc manuel obligatoire ou blocage conservé ;
  - valeurs ordinales fournies par contexte ou référentiel ;
  - mandataire SYDEL configurable, jamais imposé comme constante en dur.
- Points ouverts régime communautaire après CODE-RC-001 :
  - revue humaine SELARL de la renonciation canonique, car la variante brute contient des valeurs fixes et `En 2exemplaires` ;
  - féminisation éventuelle de `futur`, non activée automatiquement faute de source ;
  - absence de variante `ma conjointe`, `mon conjoint` restant fixe en V1 ;
  - apport limité à une somme en numéraire ;
  - valeurs par défaut de régime matrimonial, qualité renoncée et formes sociales à fournir par contexte ou référentiel.
  - le smoke DOCX réel ne vaut pas validation juridique fine.
- Points ouverts SPFPL après ARBITRAGE-SPFPL-001 :
  - acte de cession d'actions sans source DOCX confirmée, hors automatisation V1 ;
  - multi-souscripteurs hors automatisation V1 ;
  - commissaire aux apports et évaluateur fournis par contexte ou référentiel validé ;
  - aucune double option `OU` ou cession/apport ne doit être rendue.
- Points ouverts dérogations après CODE-DEROG-CORE-001 :
  - les deux sources Lot 03 préparées sont placées dans `project/source_documents/lot_03/` ;
  - `cumul_salariee` reste bloque apres retentative Word COM : erreur `0x800706BE`, aucun DOCX propre produit ;
  - revue humaine juridique/visuelle du premier rendu `DOC-013` et `DOC-014` ;
  - champs narratifs sensibles toujours fournis explicitement ou laissés comme zones à compléter.
- Points ouverts bail/appel après CODE-BAIL-APP-001 :
  - appel de fonds limité à SELARL dentaire ;
  - avenant limité SELARL/SELAS avec `dossier_options.cession=true` et société en cours d'immatriculation confirmée ;
  - revue humaine juridique/visuelle du premier rendu toujours nécessaire.
- Points ouverts cession après CODE-CESSION-CAB-001 :
  - revue humaine juridique/visuelle du premier rendu DOCX ;
  - variantes SELAS sources non stabilisées au-delà du paramétrage V1 ;
  - PDF et ZIP hors ticket ;
  - les blocages explicites sur validations médicales, crédit-vendeur, SCM, salariés et exercices restent volontaires.
- Points ouverts sources :
  - ne pas élargir la demande d'inscription à l'ordre hors specs V1 sans ticket dédié ;
  - ne pas sortir du choix SPEC-RC-001 pour le régime communautaire sans nouveau ticket d'arbitrage ;
  - ne pas placer automatiquement la famille liste des souscripteurs / attestation sur le capital ;
  - ne pas dedupliquer les statuts entre familles, professions ou variantes.
- Points ouverts statuts après arbitrages V1 :
  - SAS : générateur V1 intégré, modèle source inventorié sous `SAS` mais contenu SAS/SPFPL médecins, actionnaire unique et vocabulaire hétérogène à relire humainement ;
  - SPFPL : générateurs V1 cession/apport intégrés, multi-associés bloqué et corrections d'anomalies non arbitrées toujours exclues ;
  - SEL : générateurs V1 intégrés, multi-associés et signature dirigeant non associé restent bloqués selon arbitrages ;
  - civils : SCS, SCI, SCI IRIS et SCM codés ; SCM reste soumis à revue humaine juridique/visuelle du premier rendu.
- Toute ambiguïté de wording juridique doit bloquer l'implémentation concernée et être documentée.

## Validations connues
- FINAL-SCM-CESSION-WAVE-001 : smoke DOCX OK dans `artifacts/lot_05_scm_cession_block_smoke_test/`, trois documents produits sans placeholder `[` / `]` ni littéral résiduel `Ajouter en cas de CV`.
- FINAL-SCM-CESSION-WAVE-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- FINAL-SCM-CESSION-WAVE-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 172 tests passés.
- FINAL-SCM-CESSION-WAVE-001 : `artifacts/` non versionné.
- SYNC-CLOSE-AUDIT-001 : `git fetch --all --prune` OK.
- SYNC-CLOSE-AUDIT-001 : `origin/codex/close-motor-audit-001` confirmé au commit `0139202b170531fd628f25811c55855a2512acc0`.
- SYNC-CLOSE-AUDIT-001 : `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` présent sur `main` ; relecture documentaire et contrôle du diff, aucun test de code exécuté car aucun fichier Python modifié.
- SYNC-WAVE-010 : `git fetch --all --prune` OK.
- SYNC-WAVE-010 : `codex/arbitrage-scm-cession-resolve-001` confirmé au même commit que `main`, et `codex/code-scm-cession-block-001` confirmé ancêtre de `main`.
- SYNC-WAVE-010 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-010 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 165 tests passés.
- SYNC-WAVE-010 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- FIX-PV-RENDER-001 : source DOCX Lot 2 analysée côté structure/rendu ; en-tête société centré, listes Word, intertitres de décision gras/soulignés et formules de vote en italique identifiés.
- FIX-PV-RENDER-001 : smoke DOCX OK dans `artifacts/fix_pv_render_001_smoke_test_2/pv_nomination_gerant.docx`.
- FIX-PV-RENDER-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- FIX-PV-RENDER-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 49 tests passés.
- CODE-ORDRE-001 : tests unitaires ciblés OK, 7 tests passés dans `tests/unit/test_demande_inscription_ordre.py`.
- CODE-ORDRE-001 : smoke DOCX OK dans `artifacts/lot_02_demande_inscription_ordre_smoke_test/demande_inscription_ordre.docx`, sans placeholder `[` / `]` ni littéral résiduel `Dérogation ?`.
- CODE-ORDRE-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- CODE-ORDRE-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 56 tests passés.
- SPEC-RC-001 : source de vérité, sources Lot 2 et variantes raw dump SELARL / SELAS / SPFPL lues en lecture seule.
- SPEC-RC-001 : specs créées dans `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md` et `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`.
- SPEC-RC-001 : aucun code Python modifié ; validations limitées à la relecture documentaire et au contrôle du diff.
- CODE-RC-001 : smoke DOCX OK dans `artifacts/lot_02_regime_communautaire_smoke_test/`, deux lettres produites sans placeholder `[` / `]`.
- CODE-RC-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- CODE-RC-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 66 tests passés.
- SYNC-SPECS-001 : `git fetch --all --prune` OK.
- SYNC-SPECS-001 : branche `codex/spec-rc-001` créée et poussée avec les deux specs RC uniquement.
- SYNC-SPECS-001 : commits SPFPL, dérogations, cession/bail et RC cherry-pickés dans `main` sans conflit.
- SYNC-SPECS-001 : commit final de pilotage limité à `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md`.
- SYNC-TEXTE-SPECS-001 : `git fetch --all --prune` lancé avant synchronisation.
- SYNC-TEXTE-SPECS-001 : commits `417870da6ee6717a79853547060d6fc0cbacfa9f`, `3672cd129c90e63f440a2316aec54d653b2d24a4`, `18c6614abc1dd3036e1c56565059650748c08883` et `f0424ddad7690d7973d16b00f37aa54b20796d04` cherry-pickés dans `main` sans conflit.
- SYNC-TEXTE-SPECS-001 : relecture documentaire et contrôle du diff ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- SYNC-TEXTE-SPECS-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-ARBITRAGES-001 : `git fetch --all --prune` lancé avant synchronisation.
- SYNC-ARBITRAGES-001 : commits `16a7472610c315fd67f701fa7d9f48d253d62e9c`, `0dda81373125e71ce7817a674322cdcf498a88b0` et `ab8b4c00ead28fcd9ead4ad62e19657f35efa397` cherry-pickés dans `main` sans conflit.
- SYNC-ARBITRAGES-001 : relecture documentaire et contrôle du diff ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- SYNC-ARBITRAGES-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-CODE-BAIL-APP-001 : `git fetch --all --prune` OK.
- SYNC-CODE-BAIL-APP-001 : commit `557a013274aa9f7122c81d5e6e0b52c4043a540c` fast-forwardé dans `main` sans conflit.
- SYNC-CODE-BAIL-APP-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-CODE-BAIL-APP-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 75 tests passés.
- SYNC-CODE-BAIL-APP-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-WAVE-LOT03-05-001 : `git fetch --all --prune` OK.
- SYNC-WAVE-LOT03-05-001 : commits `36828fbc45d6b8a37c2e76eb8227460df441ebde` et `958fce5d2a9d5d30df4d918cb098fec483f5140e` cherry-pickés dans `main` sans conflit.
- SYNC-WAVE-LOT03-05-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-LOT03-05-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 80 tests passés après sauvegarde des fichiers cession non suivis hors ticket.
- SYNC-WAVE-LOT03-05-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- RESUME-CODE-CESSION-CAB-001 : smoke DOCX OK dans `artifacts/lot_03_cession_cabinets_smoke_test/`, quatre documents produits sans placeholder `[` / `]`.
- RESUME-CODE-CESSION-CAB-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- RESUME-CODE-CESSION-CAB-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 89 tests passés.
- CODE-DEROG-CORE-001 : smoke DOCX OK dans `artifacts/lot_03_derogations_core_smoke_test/`, deux formulaires à compléter produits sans placeholder `[` / `]`.
- CODE-DEROG-CORE-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- CODE-DEROG-CORE-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 95 tests passés.
- SYNC-CODE-WAVE-002 : `git fetch --all --prune` OK.
- SYNC-CODE-WAVE-002 : commits sources `ea35d2af353ac5b8567e82091ab978cf24a27445` et `bee4c8bec27397198a170c4f9888b2470b24c67f` cherry-pickés dans `main` sans conflit.
- SYNC-CODE-WAVE-002 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-CODE-WAVE-002 : `.\.venv\Scripts\python.exe -m pytest` OK, 95 tests passés.
- SYNC-CODE-WAVE-002 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-WAVE-003 : `git fetch --all --prune` OK.
- SYNC-WAVE-003 : commits sources `b854821061b85ac66fe785c11cb3c6b0bac5a85b` et `09cbad120d22910f05ba5e645971ade56fedb76d` cherry-pickés dans `main` sans conflit.
- SYNC-WAVE-003 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-003 : `.\.venv\Scripts\python.exe -m pytest` OK, 101 tests passés.
- SYNC-WAVE-003 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-STATUTS-SPECS-001 : `git fetch --all --prune` OK.
- SYNC-STATUTS-SPECS-001 : commits sources `00b7886ac431c8a47d9cdcca8bfed026a756cb69`, `b34c66e5e67f3261317035943e974536be27d6d3`, `9b25e09d08ec2161d757d1581c34073dcbbc594f` et `704eeb7301cf69460c16b2ed9fbc0ea22ca83c8c` cherry-pickés dans `main` sans conflit.
- SYNC-STATUTS-SPECS-001 : relecture documentaire et contrôle du diff ; aucun test de code exécuté car aucun fichier Python n'a été modifié.
- SYNC-STATUTS-SPECS-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-STATUTS-CODE-ARB-001 : `git fetch --all --prune` OK.
- SYNC-STATUTS-CODE-ARB-001 : commits sources `82e67120ed714b791d5483108336a570ea520e59`, `a98939c649e4124e40f2cd69c9ed125d342acc31` et `1caafd7` cherry-pickés dans `main`.
- SYNC-STATUTS-CODE-ARB-001 : conflit unique résolu dans `src/sydel_doc_engine/domain/models.py` par fusion additive SAS/SPFPL.
- SYNC-STATUTS-CODE-ARB-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-STATUTS-CODE-ARB-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 111 tests passés.
- SYNC-STATUTS-CODE-ARB-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-STYLE-CIVILS-001 : `git fetch --all --prune` OK.
- SYNC-STYLE-CIVILS-001 : commit source `76dd139da65c233f0c6aecc76bc2ea5e929381ca` intégré dans `main` par fast-forward.
- SYNC-STYLE-CIVILS-001 : commit source `b21f1b0cc5b975049e4acc279b8303f1d739b60f` cherry-pické dans `main` sans conflit.
- SYNC-STYLE-CIVILS-001 : relecture documentaire et contrôle du diff ; aucun test de code exécuté car aucun fichier Python n'a été modifié par le commit final de pilotage.
- SYNC-STYLE-CIVILS-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-STATUTS-SEL-CIVILS-001 : `git fetch --all --prune` OK.
- SYNC-STATUTS-SEL-CIVILS-001 : commit source `9a79560c4bae1ae3a98ec5305b4187f9f4ebd6a8` cherry-pické dans `main` sans conflit.
- SYNC-STATUTS-SEL-CIVILS-001 : arbitrage civils V1 confirmé présent dans `main`, contenu identique au commit source `b21f1b0cc5b975049e4acc279b8303f1d739b60f`.
- SYNC-STATUTS-SEL-CIVILS-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-STATUTS-SEL-CIVILS-001 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 122 tests passés.
- SYNC-STATUTS-SEL-CIVILS-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- CODE-STATUTS-CIVILS-CORE-001 : smoke DOCX OK dans `artifacts/lot_04_statuts_civils_core_smoke_test/`, trois documents produits sans placeholder `[` / `]`.
- CODE-STATUTS-CIVILS-CORE-001 : tests ciblés OK sur `tests/unit/test_lot_04_statuts_civils.py`, `tests/unit/test_registry_seed.py` et `tests/unit/test_orchestrator_service.py`, 21 tests passés.
- CODE-STATUTS-CIVILS-CORE-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- CODE-STATUTS-CIVILS-CORE-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 129 tests passés.
- SYNC-WAVE-004 : `git fetch --all --prune` OK.
- SYNC-WAVE-004 : commits sources `557fc1920361a8c7831e6b023d70471c9c29e5ff` et `291da7b6db68b3de413fba50cf652dde98a8f6a8` cherry-pickés dans `main` sans conflit.
- SYNC-WAVE-004 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-004 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 130 tests passés.
- SYNC-WAVE-004 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- CONVERT-DEROG-SALARIEE-001 : `Word.Application` COM disponible, mais conversion du `.doc` legacy salariee echouee avec `0x800706BE` ; aucun DOCX cible cree dans `project/source_documents/lot_03/`.
- CONVERT-DEROG-SALARIEE-001 : `LibreOffice` / `soffice`, `pandoc`, `antiword` et `catdoc` non disponibles localement ; aucun code Python modifie.
- SYNC-WAVE-005 : `git fetch --all --prune` OK.
- SYNC-WAVE-005 : commits sources `91436f0916fdecbcc98450b72ba6e602cb8f1a3b`, `1b3ba14d0bcc31fc7dcbf1752d6d3263645ae8b3`, `32059155c618b4e985893f42ef2817187599c281`, `74d41db53543b790e197082e8b9c713f7de92dc2` et `d1d649e11fdc638e6d7da0640c154d1f213739ee` cherry-pickés dans `main` sans conflit.
- SYNC-WAVE-005 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-005 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 135 tests passés.
- SYNC-WAVE-005 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-WAVE-006 : `git fetch --all --prune` OK.
- SYNC-WAVE-006 : commits sources `557fc1920361a8c7831e6b023d70471c9c29e5ff` et `291da7b6db68b3de413fba50cf652dde98a8f6a8` déjà présents par équivalence de contenu ; commits sources `2c55a7ab5f8a44de5c29305cfbc280f930ee32ec`, `568336bed7ccb0a5901abe5d921fd9056573e32d`, `8f0c8ab13d6e8f1a9e50747f8a9d5b607bcb90d6` et `11dc0d8dda23f841d650586e0977e0202270a3b5` cherry-pickés dans `main`.
- SYNC-WAVE-006 : conflits de pilotage résolus dans `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md` en conservant les états les plus récents.
- SYNC-WAVE-006 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-006 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 143 tests passés.
- SYNC-WAVE-006 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-WAVE-007 : `git fetch --all --prune` OK.
- SYNC-WAVE-007 : commits sources `3c040774cdfe57c203b78776a9ea412ec3d14d94`, `6453b6f64665feda898a076f730cba9a6684825b`, `075af377f7c9d7475429f1e738b46483127d757f` et `c221681570782a1b1efc5afc72087cb903cd8a65` cherry-pickés dans `main`.
- SYNC-WAVE-007 : conflits résolus par fusion additive entre statuts SCM, satellites SAS et satellites SCM ; les satellites SCM DOCX sont intégrés sous `DOC-026` à `DOC-028`.
- SYNC-WAVE-007 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-007 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 155 tests passés.
- SYNC-WAVE-007 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SYNC-WAVE-008 : `git fetch --all --prune` OK.
- SYNC-WAVE-008 : commits sources `61a1c49353724bbf5b8f1bb8f039d5e96b877ecc`, `d3188c0b4a4a61d889a2ce9ccc37e84e1284adaa`, `939e1c2088892abcf4a8fdcbaa35911f4f8a2f9f`, `19468886f5e885f79b2b35e17e2ff2a097ea9c3a`, `d8747ef20aba478c575c5a491cdf0f634a9c26d3`, `00b4c955b372399bb8701f47a5686748539f061b`, `a181e069f756a1ea846fdcd1824b3f8c57cc11f5` et `518e46fbb8d8bee03a23ea203654b4199103fb7e` cherry-pickés dans `main` sans conflit.
- SYNC-WAVE-008 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-WAVE-008 : `C:\Users\Gad\Desktop\Sydel\sydel-document-engine\.venv\Scripts\python.exe -m pytest` OK, 161 tests passés.
- SYNC-WAVE-008 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- SPEC-TEXTE-ORDRE-001 : source de vérité, source Lot 2 et variantes raw dump SELARL / SELAS / SPFPL cession / SPFPL apport lues en lecture seule.
- SPEC-TEXTE-ORDRE-001 : spec texte créée dans `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.
- SPEC-TEXTE-ORDRE-001 : aucun code Python modifié ; validations limitées à la relecture documentaire et au contrôle du diff.
- SPEC-TEXTE-ORDRE-001 : `git status --short --branch` n'était pas propre avant intervention ; aucun commit ni push n'a été effectué.
- SPEC-ORDRE-001 : source de vérité, source Lot 2 et variantes raw dump SELARL / SELAS / SPFPL lues en lecture seule.
- SPEC-ORDRE-001 : spec canonique créée dans `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`.
- SPEC-ORDRE-001 : aucun code Python modifié ; validations limitées à la relecture documentaire et au contrôle du diff.
- SPEC-ORDRE-001 : `git status --short` n'était pas propre avant intervention ; aucun commit ni push n'a été effectué.
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
- RECONCILE-MOTOR-CLOSE-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- RECONCILE-MOTOR-CLOSE-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 176 tests passés.
- RECONCILE-MOTOR-CLOSE-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- PDF-BACKEND-001 : tests ciblés `tests/unit/test_pdf_export.py` OK, 6 tests passés.
- PDF-BACKEND-001 : smoke réel OK, `declaration_non_condamnation.docx` généré puis converti en PDF via `word-com` dans `artifacts/pdf_backend_001_smoke_test_2/`, hors versionnement.
- PDF-BACKEND-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- PDF-BACKEND-001 : `.\.venv\Scripts\python.exe -m pytest` OK.
- PDF-BACKEND-001 : `artifacts/` non versionné ; aucun fichier UI modifié.
- SYNC-POST-MOTOR-UI-001 : `git fetch --all --prune` OK.
- SYNC-POST-MOTOR-UI-001 : commits sources `d62670efe10481926437c0e1a5dabbe349fd5938`, `24a881b999371811d39a2403c0b51d9ae8ce0556`, `ef6252b3c15dc3fc39f1efdc05687c0f448f8fe1`, `2f76f61848469ddf2f7b29c3169e8893e83fd3a5` et `c2fc0db4d51485c7c5e721c5184028ae17c68cb3` cherry-pickés dans `main` sans conflit.
- SYNC-POST-MOTOR-UI-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-POST-MOTOR-UI-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 182 tests passés.
- SYNC-POST-MOTOR-UI-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifiés.
- UI-PDF-ZIP-INTEGRATION-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- UI-PDF-ZIP-INTEGRATION-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 186 tests passés.
- UI-PDF-ZIP-INTEGRATION-001 : smoke lancement Streamlit OK sur `http://localhost:8502`, page UI chargee.
- UI-PDF-ZIP-INTEGRATION-001 : `artifacts/` non versionne ; le PDF reste dependant de LibreOffice ou Word COM local.

- SYNC-FINAL-FOUNDATIONS-001 : `.\.venv\Scripts\python.exe -m ruff check .` OK.
- SYNC-FINAL-FOUNDATIONS-001 : `.\.venv\Scripts\python.exe -m pytest` OK, 191 tests passes.
- SYNC-FINAL-FOUNDATIONS-001 : fichiers critiques 16/17/18/19/20/21 et `docs/review/final_recipe_framework_v1.md` presents sur `main`.
- SYNC-FINAL-FOUNDATIONS-001 : `project/source_import/raw_drive_dump/` et `artifacts/` non modifies.

## Recommandation immédiate suivante
Lancer `REVIEW-FINAL-001` pour controler le flux complet UI -> DOCX -> PDF -> ZIP avec revue humaine, puis `CLOSE-PROJECT-V1-001`.
