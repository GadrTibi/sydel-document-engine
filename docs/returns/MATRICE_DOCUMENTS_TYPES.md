# MATRICE DOCUMENTS × TYPES — moteur Sydel

> **But** : quand un retour touche un document, cette matrice dit instantanément TOUS les types
> concernés + où est le code. Complète le `REGISTRE_PROPAGATION.md` (règle 68 Q4).
> **Source de vérité = le CODE** (lu au HEAD `6dd209c`, branche `sprint/engine-completion`) :
> `src/sydel_doc_engine/registry/catalog.py` (catalogue moteur), `src/sydel_doc_engine/orchestrator/service.py`
> (gates d'activation), `src/sydel_doc_engine/domain/case_catalog.py` (canon documents-par-cas),
> `src/sydel_doc_engine/front_app/*` (slices + bundles).
> Généré 2026-07-07 (lecture seule). Chemins générateurs relatifs à `src/sydel_doc_engine/generators/`.

## Légende

- **Partagé** = UN générateur sert plusieurs types (un fix s'y propage automatiquement — vérifier la byte-neutralité des types non visés).
- **Partagé structure-aware** = générateur unique avec branches par structure (un fix peut être conditionné).
- **Spécifique** = générateur dédié à un seul type (un retour « universel » doit être répliqué à la main dans les cousins → registre de propagation).
- Structures moteur : `SELARL · SELAS · SPFPL cession · SPFPL apport · SCS · SCI · SCI IRIS · SCM · MICRO_HOLDING · SAS · SASU_HOLDING` (`registry/catalog.py::ALL_STRUCTURES`).

## 1. Par DOCUMENT (DOC-001 → DOC-051 + non mappés)

### Tronc commun (universels)

| DOC | Nom | Générateur | Fichier de sortie | Types porteurs | Condition d'activation | Partage |
|---|---|---|---|---|---|---|
| DOC-001 | Déclaration sur l'honneur de non-condamnation | `lot_01/declaration_non_condamnation.py` | `declaration_non_condamnation.docx` (renommée avec le nom du dirigeant, O24-02, via `rename_dnc_with_signataire`) | **TOUS (11)** | tous les dossiers ; une DNC PAR dirigeant | **Partagé** |
| DOC-002 | Autorisation de domiciliation | `lot_01/autorisation_domiciliation.py` | `autorisation_domiciliation.docx` | **TOUS (11)** | tous les dossiers | **Partagé structure-aware** (mention capital variable MICRO_HOLDING) — ⚠️ **VALIDÉE Albane, ne pas modifier** (mise en forme 1.8) |
| DOC-003 | Procuration | `lot_01/procuration.py` | `procuration.docx` | **TOUS (11)** | tous les dossiers | **Partagé structure-aware** (« Fait pour servir » omis pour SASU_HOLDING, `procuration.py:91`) |
| DOC-004 | PV nomination dirigeant (clé technique `pv_nomination_gerant`) | `lot_02/pv_nomination_gerant.py` | `pv_nomination_gerant.docx` | SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI, SCI IRIS, SCM, MICRO_HOLDING (9) | toujours pour ces types | **Partagé** (label affiché « dirigeant », A26-24/A26-label) |
| DOC-034 | Demande d'inscription à l'Ordre | `lot_02/demande_inscription_ordre.py` | `demande_inscription_ordre.docx` | SELARL, SELAS, SPFPL cession, SPFPL apport, SCM (5) | structure ∈ {SELARL, SELAS, SPFPL×2, SCM} ; mention dérogation si `options.derogation` | **Partagé** — mise en forme **VALIDÉE** (9.1) |

### Régime matrimonial (conditionnels)

| DOC | Nom | Générateur | Fichier de sortie | Types porteurs | Condition | Partage |
|---|---|---|---|---|---|---|
| DOC-005 | Lettre de renonciation à revendiquer la qualité d'associé | `lot_02/lettre_renonciation_associe.py` | `lettre_renonciation_associe.docx` | SELARL, SELAS, SPFPL cession, SPFPL apport, SCS (5) | `options.regime_communautaire == true` (dérivé du menu matrimonial ; per-associé en SELAS multi / civils) | **Partagé** |
| DOC-006 | Lettre d'avertissement au conjoint (apport de bien commun) | `lot_02/lettre_avertissement_conjoint.py` | `lettre_avertissement_conjoint.docx` | SELARL, SELAS, SPFPL cession, SPFPL apport, SCS (5) | idem DOC-005 | **Partagé structure-aware** (overlay mention manuscrite SELARL vs SELAS/SPFPL) |

### Cession de cabinet + bail (SEL)

| DOC | Nom | Générateur | Fichier de sortie | Types porteurs | Condition | Partage |
|---|---|---|---|---|---|---|
| DOC-007 | Avenant contrat de bail | `lot_03/avenant_contrat_bail.py` | `avenant_contrat_bail.docx` | SELARL, SELAS | `options.cession == true` | **Partagé** |
| DOC-008 | Appel de fonds SEL | `lot_03/appel_fond_sel.py` | `appel_fond_sel.docx` | **SELARL uniquement** | cession + `cession.type_cabinet` renseigné (médical ET dentaire) | **Spécifique** (SELAS explicitement hors périmètre — Q Rafael) |
| DOC-009 | Acte de cession d'un cabinet médical | `lot_03/acte_cession_cabinet_medical.py` (socle `cession_cabinets_common.py`) | `acte_cession_cabinet_medical.docx` | SELARL, SELAS | cession + cabinet médical + étape acte (⚠️ **SELAS : acte ET compromis ensemble**, O24-14, l'étape ne filtre plus) | **Partagé** (socle commun 4 documents) |
| DOC-010 | Compromis de cession d'un cabinet médical | `lot_03/compromis_cession_cabinet_medical.py` | `compromis_cession_cabinet_medical.docx` | SELARL, SELAS | cession + médical + étape compromis (SELAS : ensemble) | **Partagé** |
| DOC-011 | Acte de cession d'un cabinet dentaire | `lot_03/acte_cession_cabinet_dentaire.py` | `acte_cession_cabinet_dentaire.docx` | SELARL, SELAS | cession + dentaire + étape acte (SELAS : ensemble) | **Partagé** |
| DOC-012 | Compromis de cession d'un cabinet dentaire | `lot_03/compromis_cession_cabinet_dentaire.py` | `compromis_cession_cabinet_dentaire.docx` | SELARL, SELAS | cession + dentaire + étape compromis (SELAS : ensemble) | **Partagé** |

### Dérogations

| DOC | Nom | Générateur | Fichier de sortie | Types porteurs | Condition | Partage |
|---|---|---|---|---|---|---|
| DOC-013 | Formulaire dérogation plusieurs sites SEL (à compléter) | `lot_03/formulaire_derogation_sites_sel.py` | `formulaire_derogation_sites_sel_formulaire_a_completer.docx` | SELARL, SELAS | `options.derogation` + type `multi_sites_sel` + mode `formulaire_a_completer` | **Partagé** — ⚠️ `case_catalog.py` le classe MANUAL_ONLY (pré-remplissage partiel) alors que le moteur le génère : divergence de statut interne, pas un bug |
| DOC-014 | Demande dérogation cumul SELARL - BNC (à compléter) | `lot_03/demande_derogation_cumul_selarl_bnc.py` | `demande_derogation_cumul_selarl_bnc_formulaire_a_completer.docx` | **SELARL uniquement** | dérogation + type `cumul_sel_bnc` | **Spécifique** (même divergence MANUAL_ONLY que DOC-013) |

### Statuts (un générateur par corpus)

| DOC | Nom | Générateur | Fichier de sortie | Types porteurs | Condition | Partage |
|---|---|---|---|---|---|---|
| DOC-016 | Statuts SELARL chirurgien-dentiste | `lot_04/statuts_selarl_dentiste.py` (socle `statuts_sel_exercice_common.py` + `statuts_sel_exercice_templates.py`) | `Statuts {dénomination}.docx` (fallback `statuts_selarl_chirurgien_dentiste.docx`) | SELARL | overlay `selarl_dentiste` | **Spécifique** (socle SEL exercice PARTAGÉ avec DOC-017/018/046) |
| DOC-017 | Statuts SELARL médecin | `lot_04/statuts_selarl_medecin.py` | `Statuts {dénomination}.docx` (fallback `statuts_selarl_medecin.docx`) | SELARL | overlay `selarl_medecin` | **Spécifique** (socle partagé) |
| DOC-018 | Statuts SELAS médecin (unipersonnelle) | `lot_04/statuts_selas_medecin.py` | `statuts_selas_medecin.docx` (**nom fixe** — pas de « Statuts [Nom] », dette registre) | SELAS (front : type dédié « SELAS uni médecin ») | overlay `selas_medecin`, associé unique | **Spécifique** (socle partagé) |
| DOC-046 | Statuts SELAS dentiste (unipersonnelle) | `lot_04/statuts_selas_dentiste.py` | `statuts_selas_dentiste.docx` (**nom fixe**) | SELAS (front : « SELAS uni dentiste ») | overlay `selas_dentiste`, associé unique | **Spécifique** (socle partagé) |
| DOC-044 | Statuts SELAS multi (2-5 associés) | `lot_04/statuts_selas_multi.py` | `Statuts {dénomination}.docx` | SELAS | `statuts_selas_multi` fourni ; 2-5 associés dont ≥1 PP exerçante ; PM + DG optionnels | **Spécifique** (injection modèle Reynaud — ⚠️ ne passe PAS par le renderer SEL exercice : la mise en forme uni ne se propage pas ici, cf. tracé 2.6/2.7/2.8) |
| DOC-015 | Statuts SAS / SPFPL médecins | `lot_04/statuts_sas.py` | `statuts_sas_spfpl_medecins.docx` | SAS | type `spfpl_medecins` + profession médecin + actionnaire unique | **Spécifique** |
| DOC-048 | Statuts SASU Holding | `lot_04/statuts_sasu_holding.py` | `statuts_sasu_holding.docx` | SASU_HOLDING | contexte `statuts_sasu_holding` présent | **Spécifique** (DISTINCT de DOC-015, conservés tous deux) |
| DOC-035 | Statuts SPFPL cession | `lot_04/statuts_spfpl_cession.py` (socle `statuts_spfpl_common.py` + `statuts_spfpl_templates.py`) | `statuts_spfpl_cession.docx` | SPFPL cession | `operation_spfpl.type == cession` + `options.cession` | **Spécifique** (socle SPFPL PARTAGÉ avec DOC-036) |
| DOC-036 | Statuts SPFPL apport | `lot_04/statuts_spfpl_apport.py` | `statuts_spfpl_apport.docx` | SPFPL apport | `operation_spfpl.type == apport` + `options.apport` | **Spécifique** (socle partagé) |
| DOC-019 | Statuts SCS | `lot_04/statuts_scs.py` (socle `statuts_civils_common.py`, injection modèle) | `Statuts {dénomination}.docx` (SCS6 ; fallback `statuts_scs.docx`) | SCS | `statuts_civils.type == scs` ; 1-6 associés | **Spécifique** (socle civils PARTAGÉ avec DOC-020/021/025/047) |
| DOC-020 | Statuts SCI | `lot_04/statuts_sci.py` | `statuts_sci.docx` (**nom fixe**) | SCI | `statuts_civils.type == sci` | **Spécifique** (socle partagé) |
| DOC-021 | Statuts SCI IRIS | `lot_04/statuts_sci_iris.py` | `statuts_sci_iris.docx` (**nom fixe**) | SCI IRIS | `statuts_civils.type == sci_iris` + associé PM | **Spécifique** (socle partagé) |
| DOC-025 | Statuts SCM | `lot_04/statuts_scm.py` | `statuts_scm.docx` (**nom fixe**) | SCM | `statuts_civils.type == scm` ; 1-6 associés | **Spécifique** (socle partagé) |
| DOC-047 | Statuts micro holding | `lot_04/statuts_micro_holding.py` | `statuts_micro_holding.docx` (**nom fixe**) | MICRO_HOLDING | `statuts_civils.type == micro_holding` ; capital variable (max = 10× min) | **Spécifique** (socle partagé ; modèle officiel Albane 2026-06-29, 26 articles) |

### Satellites SAS / SASU

| DOC | Nom | Générateur | Fichier de sortie | Types porteurs | Condition | Partage |
|---|---|---|---|---|---|---|
| DOC-023 | PV rémunération président SAS | `lot_05/pv_remuneration_president.py` (socle `sas_satellites_common.py`) | `pv_remuneration_president.docx` | SAS | associé unique + président index 0 + absence de rémunération | **Spécifique** (⚠️ verrouillé masculin — garde `sas_slice.py:491-495`) |
| DOC-024 | Attestation capital / liste souscripteurs SAS | `lot_05/attestation_capital_liste_souscripteurs_sas.py` | `attestation_capital_liste_souscripteurs_sas.docx` | SAS | associé unique + apport + 1 souscripteur + apports en nature | **Spécifique** |
| DOC-049 | PV rémunération président SASU Holding | `lot_05/pv_remuneration_president_sasu_holding.py` | `pv_remuneration_president_sasu_holding.docx` | SASU_HOLDING | contexte SASU présent | **Spécifique** (DISTINCT de DOC-023, genre libre) |
| DOC-050 | Liste des souscripteurs SASU Holding | `lot_05/liste_souscripteurs_sasu_holding.py` | `liste_souscripteurs_sasu_holding.docx` | SASU_HOLDING | contexte SASU présent | **Spécifique** (DISTINCT de DOC-024) |

### Attestations capital / souscripteurs (famille éclatée — ⚠️ 6 générateurs cousins)

| DOC | Nom | Générateur | Fichier de sortie | Types porteurs | Condition | Partage |
|---|---|---|---|---|---|---|
| DOC-042 | Attestation capital / liste souscripteurs SPFPL (apport) | `lot_05/attestation_capital_liste_souscripteurs.py` | `attestation_capital_liste_souscripteurs.docx` | SPFPL apport | apport + 1 souscripteur | **Spécifique** |
| DOC-051 | Attestation capital / liste souscripteurs SPFPL (cession) | `lot_05/attestation_capital_liste_souscripteurs_cession.py` | `attestation_capital_liste_souscripteurs_cession.docx` | SPFPL cession | cession + 1 souscripteur (critère Albane n°14) | **Spécifique** |
| DOC-045 | Attestation capital / liste souscripteurs SELAS | `lot_05/attestation_capital_souscripteurs_selas.py` | `attestation_capital_souscripteurs_selas.docx` | SELAS | 1-6 souscripteurs physiques, numéraire ; conditionnelle au bundle (ANO-045 : émise si dossier « attestable ») | **Spécifique** |
| DOC-LSS-SCS *(non mappé DOC-0xx)* | Liste des souscripteurs SCS | `lot_05/liste_souscripteurs_scs.py` | `liste_souscripteurs_scs.docx` | SCS | toujours (appel DIRECT du front `civil_statuts_slice.py:1516`, **hors orchestrateur**) | **Spécifique** (adaptation parts/Président — arbitrage Rafael SCS5) |
| — | *Manquantes signalées Albane (mise en forme §4)* | *(inexistant)* | — | **SELARL, SCI, SCM, SCI IRIS, MICRO_HOLDING** | — | ⚠️ **TROU** : Albane veut une attestation capital dans TOUTES les créations ; flag 4.1/4.9 (quel modèle pour les civils ?) |

### SPFPL cession/apport — satellites

| DOC | Nom | Générateur | Fichier de sortie | Types porteurs | Condition | Partage |
|---|---|---|---|---|---|---|
| DOC-037 | Note d'information SPFPL | `lot_05/note_information.py` | `note_information.docx` | SPFPL cession, SPFPL apport | wording cession/apport tranché par `operation_spfpl.type` | **Partagé** (les 2 SPFPL) |
| DOC-038 | PV agrément cession SPFPL — associé unique | `lot_05/pv_agrement_cession_spfpl_associe_unique.py` (socle `pv_agrement_common.py`) | `pv_agrement_cession_spfpl_associe_unique.docx` | SPFPL cession | cession + `options.associe_unique == true` | **Spécifique** (socle partagé avec DOC-039) |
| DOC-039 | PV agrément cession SPFPL — plusieurs associés | `lot_05/pv_agrement_cession_spfpl_plusieurs_associes.py` | `pv_agrement_cession_spfpl_plusieurs_associes.docx` | SPFPL cession | cession + `associe_unique == false` | **Spécifique** (socle partagé) |
| DOC-040 | Acte de cession de parts SPFPL | `lot_05/acte_cession_parts_spfpl.py` | `acte_cession_parts_spfpl.docx` | SPFPL cession | cession + nature titres ≠ actions | **Spécifique** |
| DOC-029 | Acte de cession d'actions SPFPL à un tiers | `lot_05/acte_cession_actions_spfpl.py` | `acte_cession_actions_spfpl.docx` | SPFPL cession | cession + nature titres == actions + document demandé == acte_cession_actions | **Spécifique** |
| DOC-041 | Contrat d'apport SEL vers SPFPL | `lot_05/contrat_apport_spfpl.py` | `contrat_apport_spfpl.docx` | SPFPL apport | apport + évaluateur + commissaire fournis | **Spécifique** |
| DOC-043 | Attestation nomination commissaire aux apports | `lot_05/attestation_commissaire_apports.py` | `attestation_commissaire_apports.docx` | SPFPL apport | apport + commissaire fourni | **Spécifique** |

### SCM — satellites & cession de parts

| DOC | Nom | Générateur | Fichier de sortie | Types porteurs | Condition | Partage |
|---|---|---|---|---|---|---|
| DOC-026 | Pacte d'associés SCM | `lot_05/pacte_associes_scm.py` (socle `scm_satellites_common.py`) | `pacte_associes_scm.docx` | SCM | `options.scm_satellites` + `scm_satellites.pacte_associes` | **Spécifique** |
| DOC-027 | Contrat d'exercice professionnel à frais communs | `lot_05/contrat_frais_communs.py` | `contrat_frais_communs.docx` | SCM | satellites + `contrat_frais_communs` | **Spécifique** |
| DOC-028 | Règlement intérieur de la SCM | `lot_05/reglement_interieur_scm.py` | `reglement_interieur_scm.docx` | SCM | satellites + `reglement_interieur` | **Spécifique** |
| DOC-030 | Liste des dépenses communes SCM | `lot_05/liste_depenses_communes_scm.py` | `liste_depenses_communes_scm.docx` | SCM | satellites + `liste_depenses_communes` | **Spécifique** |
| DOC-031 | PV AGE cession part SCM | `lot_05/pv_age_cession_scm.py` (socle `scm_cession_common.py`) | `pv_age_cession_parts_scm.docx` | **SELARL, SELAS** (la SEL qui rachète les parts SCM) | `options.scm_cession` + contexte `scm_cession` (overlay par structure) | **Partagé structure-aware** |
| DOC-032 | Courrier SDE cession SCM | `lot_05/courrier_sde_cession_scm.py` | `courrier_sde_cession_scm.docx` | SELARL, SELAS | idem (SELARL : 4 exemplaires fixes ; SELAS : destinataire fiscal + exemplaires variables) | **Partagé structure-aware** |
| DOC-033 | Acte de cession des parts de la SCM vers SEL | `lot_05/acte_cession_parts_scm.py` | `acte_cession_parts_scm.docx` | SELARL, SELAS | idem + répartition avant cession totalisant `nb_parts_total` | **Partagé structure-aware** |

### Option IS

| DOC | Nom | Générateur | Fichier de sortie | Types porteurs | Condition | Partage |
|---|---|---|---|---|---|---|
| DOC-022 | Lettre option IS | `lot_05/lettre_option_is.py` | `lettre_option_is.docx` | SCI, SCI IRIS, MICRO_HOLDING | `options.option_is == true` | **Partagé** (qualité « gérant(e) » dérivée pour MICRO_HOLDING) |

### Non générés (catalogue canon sans générateur)

| Clé canon | Nom | Statut | Types |
|---|---|---|---|
| `site_distinct_cd94_sel` | Formulaire déclaration préalable site distinct CD94 | **MANUAL_ONLY** (« à remplir à la main », source) | SELARL |
| `derogation_sel_bnc` | Dérogation SEL BNC | **MANUAL_ONLY** (pas de source DOCX) | SELARL |
| `derogation_cumul_selarl_salariee` | Demande dérogation cumul SELARL salariée | **NOT_IMPLEMENTED** (source legacy `.doc` non convertie) | SELAS (occurrence canon « si dérogation ») |

## 2. Par TYPE → documents

> Bundle réel = tronc commun + statuts + conditionnels. Les gates exacts sont dans
> `orchestrator/service.py::_non_regime_document_enabled` ; les bundles front dans les slices.

| Type (moteur) | Slice front | Documents |
|---|---|---|
| **SELARL** | `selarl_slice.py` (chemin historique dédié, uni + multi additif) | DOC-001/002/003 · DOC-004 · DOC-034 · **DOC-016 ou DOC-017** (profession) · DOC-005/006 (communauté) · DOC-007/008 (cession) · DOC-009/010 ou DOC-011/012 (cession selon cabinet + étape) · DOC-013/014 (dérogations) · DOC-031/032/033 (cession parts SCM) |
| **SELAS** (pluri) | `selas_multi_slice.py` | DOC-001/002/003 · DOC-004 · DOC-034 · **DOC-044** · DOC-045 (si attestable) · DOC-005/006 (communauté, per-associé) · DOC-007 (cession) · DOC-009+010 ou DOC-011+012 (cession : acte ET compromis ensemble) · DOC-013 · DOC-031/032/033 (cession parts SCM) |
| **SELAS uni médecin** (structure front dédiée) | `selas_uni_medecin_slice.py` | DOC-001/002/003 · DOC-004 · DOC-034 · **DOC-018** · attestation via `selas_uni_attestation.py` (DOC-045) · DOC-005/006 |
| **SELAS uni dentiste** (structure front dédiée) | `selas_uni_dentiste_slice.py` | idem avec **DOC-046** |
| **SPFPL cession** | `spfpl_cession_slice.py` (socle `spfpl_slice.py`) | DOC-001/002/003 · DOC-004 · DOC-034 · **DOC-035** · DOC-037 · DOC-038 ou DOC-039 (selon associé unique) · DOC-040 ou DOC-029 (parts vs actions) · **DOC-051** (attestation capital cession) · DOC-005/006 |
| **SPFPL apport** | `spfpl_apport_slice.py` (socle `spfpl_slice.py`) | DOC-001/002/003 · DOC-004 · DOC-034 · **DOC-036** · DOC-037 · DOC-041 · DOC-042 · DOC-043 · DOC-005/006 |
| **SCS** | `scs_slice.py` (socle `civil_statuts_slice.py`) | DOC-001/002/003 · DOC-004 · **DOC-019** · DOC-005/006 (communauté per-associé, SCS4) · **DOC-LSS-SCS** (liste souscripteurs, appel direct front) |
| **SCI** | `sci_slice.py` (socle civils) | DOC-001/002/003 · DOC-004 · **DOC-020** · DOC-022 (si IS) |
| **SCI IRIS** | `sci_iris_slice.py` (socle civils) | DOC-001/002/003 · DOC-004 · **DOC-021** · DOC-022 (si IS) |
| **SCM** | `scm_slice.py` (socle civils) | DOC-001/002/003 · DOC-004 · DOC-034 · **DOC-025** · DOC-026/027/028/030 (satellites cochés) |
| **MICRO_HOLDING** | `micro_holding_slice.py` (socle civils) | DOC-001/002/003 · DOC-004 · **DOC-047** · DOC-022 (si IS) — bundle 6 pièces mail Albane 2026-06-29 |
| **SAS** (SPFPL médecins forme SAS) | `sas_slice.py` | DOC-001/002/003 · **DOC-015** · DOC-023 · DOC-024 |
| **SASU_HOLDING** | `sasu_holding_slice.py` | DOC-001/002/003 · **DOC-048** · DOC-049 · DOC-050 — bundle 6 pièces |

## 3. Familles à propagation (rappel opérationnel)

Un retour sur l'un de ces documents doit être **vérifié sur toute la famille** :

- **Statuts SEL exercice** (socle `statuts_sel_exercice_common.py`) : DOC-016, DOC-017, DOC-018, DOC-046 — mais **PAS** DOC-044 (SELAS multi = injection séparée) ni DOC-035/036 (socle SPFPL séparé) ni DOC-015/048 (SAS).
- **Statuts civils** (socle `statuts_civils_common.py`, injection) : DOC-019, DOC-020, DOC-021, DOC-025, DOC-047.
- **Attestations capital** (6 générateurs SANS socle commun) : DOC-024, DOC-042, DOC-045, DOC-050, DOC-051, DOC-LSS-SCS → un retour « attestation » se propage À LA MAIN sur 6 fichiers.
- **Cession cabinet** (socle `cession_cabinets_common.py`) : DOC-009/010/011/012 — attention au siloing médical↔dentaire (incident lot 9, 2026-06-26).
- **Cession parts SCM** (socle `scm_cession_common.py`) : DOC-031/032/033, overlays SELARL/SELAS.
- **PV agrément SPFPL** (socle `pv_agrement_common.py`) : DOC-038/039.
- **Tronc commun** : DOC-001/002/003 touchent les 11 types ; DOC-004 en touche 9 ; DOC-034 en touche 5.
