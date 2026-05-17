from __future__ import annotations

from sydel_doc_engine.domain.document import DocumentDefinition
from sydel_doc_engine.domain.enums import DocumentCategory, WorkflowStatus

ALL_STRUCTURES: list[str] = [
    "SELARL",
    "SELAS",
    "SPFPL cession",
    "SPFPL apport",
    "SCS",
    "SCI",
    "SCI IRIS",
    "SCM",
    "SAS",
]

PV_NOMINATION_GERANT_STRUCTURES: list[str] = [
    "SELARL",
    "SELAS",
    "SPFPL cession",
    "SPFPL apport",
    "SCS",
    "SCI",
    "SCM",
]

DEMANDE_INSCRIPTION_ORDRE_STRUCTURES: list[str] = [
    "SELARL",
    "SELAS",
    "SPFPL cession",
    "SPFPL apport",
    "SCM",
]

REGIME_COMMUNAUTAIRE_STRUCTURES: list[str] = [
    "SELARL",
    "SELAS",
    "SPFPL cession",
    "SPFPL apport",
]

BAIL_AVENANT_STRUCTURES: list[str] = [
    "SELARL",
    "SELAS",
]

APPEL_FONDS_SEL_STRUCTURES: list[str] = [
    "SELARL",
]

CESSION_CABINET_STRUCTURES: list[str] = [
    "SELARL",
    "SELAS",
]


DEROGATION_CORE_STRUCTURES: list[str] = [
    "SELARL",
    "SELAS",
]

STATUTS_SAS_STRUCTURES: list[str] = [
    "SAS",
]

STATUTS_SPFPL_CESSION_STRUCTURES: list[str] = [
    "SPFPL cession",
]

STATUTS_SPFPL_APPORT_STRUCTURES: list[str] = [
    "SPFPL apport",
]

STATUTS_CIVILS_SCS_STRUCTURES: list[str] = [
    "SCS",
]

STATUTS_CIVILS_SCI_STRUCTURES: list[str] = [
    "SCI",
]

STATUTS_CIVILS_SCI_IRIS_STRUCTURES: list[str] = [
    "SCI IRIS",
]

STATUTS_CIVILS_SCM_STRUCTURES: list[str] = [
    "SCM",
]

OPTION_IS_STRUCTURES: list[str] = [
    "SCI",
    "SCI IRIS",
]

SCM_SATELLITES_STRUCTURES: list[str] = [
    "SCM",
]

SCM_CESSION_STRUCTURES: list[str] = [
    "SELARL",
    "SELAS",
]


def build_seed_catalog() -> list[DocumentDefinition]:
    return [
        DocumentDefinition(
            doc_id="DOC-001",
            canonical_name="Déclaration sur l’honneur de non-condamnation",
            generator_name="generate_declaration_sur_l_honneur_de_non_condamnation",
            lot=1,
            category=DocumentCategory.UNIVERSEL,
            structures=ALL_STRUCTURES,
            general_condition="tous les dossiers",
            dynamic_associates=False,
            grammar_variants=True,
            workflow_status=WorkflowStatus.SPECIFIE,
            source_path=(
                "project/source_documents/lot_01/"
                "declaration_non_condamnation_transforme.docx"
            ),
            specification_path="docs/delivery/lot_01_analysis_and_specs_v1.md",
            notes="Implémentation différée tant que les arbitrages de démarrage ne sont pas clos.",
        ),
        DocumentDefinition(
            doc_id="DOC-002",
            canonical_name="Autorisation de domiciliation",
            generator_name="generate_autorisation_de_domiciliation",
            lot=1,
            category=DocumentCategory.UNIVERSEL,
            structures=ALL_STRUCTURES,
            general_condition="tous les dossiers",
            dynamic_associates=False,
            grammar_variants=True,
            workflow_status=WorkflowStatus.SPECIFIE,
            source_path=(
                "project/source_documents/lot_01/"
                "autorisation_domiciliation_transforme.docx"
            ),
            specification_path="docs/delivery/lot_01_analysis_and_specs_v1.md",
            notes=(
                "Arbitrage métier encore requis sur la règle de rendu de l'adresse "
                "de domiciliation."
            ),
        ),
        DocumentDefinition(
            doc_id="DOC-003",
            canonical_name="Procuration",
            generator_name="generate_procuration",
            lot=1,
            category=DocumentCategory.UNIVERSEL,
            structures=ALL_STRUCTURES,
            general_condition="tous les dossiers",
            dynamic_associates=False,
            grammar_variants=True,
            workflow_status=WorkflowStatus.SPECIFIE,
            source_path="project/source_documents/lot_01/procuration_transforme.docx",
            specification_path="docs/delivery/lot_01_analysis_and_specs_v1.md",
            notes="Constantes SYDEL à externaliser avant implémentation.",
        ),
        DocumentDefinition(
            doc_id="DOC-004",
            canonical_name="PV nomination gérant",
            generator_name="generate_pv_nomination_gerant",
            lot=2,
            category=DocumentCategory.MUTUALISABLE,
            structures=PV_NOMINATION_GERANT_STRUCTURES,
            general_condition="dossiers hors SAS listés par la source de vérité",
            dynamic_associates=True,
            grammar_variants=True,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_02/PV nomination gérant - transforme.docx",
            specification_path="docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md",
            notes="Branché dans l'orchestrateur sans UI, PDF ni ZIP.",
        ),
        DocumentDefinition(
            doc_id="DOC-034",
            canonical_name="Demande d'inscription a l'ordre",
            generator_name="generate_demande_inscription_ordre",
            lot=2,
            category=DocumentCategory.MUTUALISABLE,
            structures=DEMANDE_INSCRIPTION_ORDRE_STRUCTURES,
            general_condition=(
                "dossier.structure in {SELARL, SELAS, SPFPL cession, SPFPL apport, SCM}"
            ),
            specific_conditions=[
                "ordre et mandataire fournis explicitement",
                "mention de derogation manuelle obligatoire si dossier.options.derogation == true",
                "SCM accepte uniquement avec donnees ordinales explicites",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_02/"
                "Demande d_inscription à l_ordre - transforme.docx"
            ),
            specification_path=(
                "docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md"
            ),
            notes=(
                "Exposition runtime ajoutee par reconciliation moteur ; aucun wording "
                "juridique modifie."
            ),
        ),
        DocumentDefinition(
            doc_id="DOC-005",
            canonical_name="Lettre de renonciation a revendiquer la qualite d'associe",
            generator_name="generate_lettre_renonciation_associe",
            lot=2,
            category=DocumentCategory.MUTUALISABLE,
            structures=REGIME_COMMUNAUTAIRE_STRUCTURES,
            general_condition="dossier.options.regime_communautaire == true",
            specific_conditions=[
                "SELARL, SELAS, SPFPL cession et SPFPL apport uniquement",
                "date du courrier d'avertissement resolue explicitement ou via l'avertissement",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_02/"
                "Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx"
            ),
            specification_path=(
                "docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md"
            ),
            notes="Batch regime communautaire V1, sans overlay SELARL de renonciation.",
        ),
        DocumentDefinition(
            doc_id="DOC-006",
            canonical_name="Lettre d'avertissement au conjoint en cas d'apport d'un bien commun",
            generator_name="generate_lettre_avertissement_conjoint",
            lot=2,
            category=DocumentCategory.MUTUALISABLE,
            structures=REGIME_COMMUNAUTAIRE_STRUCTURES,
            general_condition="dossier.options.regime_communautaire == true",
            specific_conditions=[
                "SELARL, SELAS, SPFPL cession et SPFPL apport uniquement",
                "overlay de mention manuscrite SELARL vs SELAS/SPFPL",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_02/"
                "Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - "
                "transforme.docx"
            ),
            specification_path=(
                "docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md"
            ),
            notes="Batch regime communautaire V1, DOCX from-scratch uniquement.",
        ),
        DocumentDefinition(
            doc_id="DOC-007",
            canonical_name="Avenant contrat de bail",
            generator_name="generate_avenant_contrat_bail",
            lot=3,
            category=DocumentCategory.MUTUALISABLE,
            structures=BAIL_AVENANT_STRUCTURES,
            general_condition="dossier.options.cession == true",
            specific_conditions=[
                "SELARL et SELAS uniquement",
                "societe en cours d'immatriculation confirmee",
                "cabinet medical ou dentaire",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_03/Avenant Contrat de bail.docx",
            specification_path="docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md",
            notes="Table de signatures source reproduite strictement, doublon inclus.",
        ),
        DocumentDefinition(
            doc_id="DOC-008",
            canonical_name="Appel de fonds SEL",
            generator_name="generate_appel_fond_sel",
            lot=3,
            category=DocumentCategory.MUTUALISABLE,
            structures=APPEL_FONDS_SEL_STRUCTURES,
            general_condition="dossier.options.cession == true",
            specific_conditions=[
                "SELARL uniquement",
                "cabinet dentaire uniquement",
                "montant de deblocage fourni manuellement",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_03/appel de fond sel.docx",
            specification_path="docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md",
            notes="Wording medical et SELAS bloques en V1.",
        ),
        DocumentDefinition(
            doc_id="DOC-009",
            canonical_name="Acte de cession d'un cabinet medical",
            generator_name="generate_acte_cession_cabinet_medical",
            lot=3,
            category=DocumentCategory.MUTUALISABLE,
            structures=CESSION_CABINET_STRUCTURES,
            general_condition="dossier.options.cession == true",
            specific_conditions=[
                "dossier.cession.etape == acte",
                "dossier.cession.type_cabinet == medical",
                "arbitrages cession cabinets V1 explicitement valides",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_03/Acte de cession d_un cabinet médical.docx",
            specification_path="docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md",
            notes="Blocages explicites conserves pour les anomalies medicales arbitrees V1.",
        ),
        DocumentDefinition(
            doc_id="DOC-010",
            canonical_name="Compromis de cession d'un cabinet medical",
            generator_name="generate_compromis_cession_cabinet_medical",
            lot=3,
            category=DocumentCategory.MUTUALISABLE,
            structures=CESSION_CABINET_STRUCTURES,
            general_condition="dossier.options.cession == true",
            specific_conditions=[
                "dossier.cession.etape == compromis",
                "dossier.cession.type_cabinet == medical",
                "arbitrages cession cabinets V1 explicitement valides",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_03/"
                "Compromis de cession d_un cabinet médical.docx"
            ),
            specification_path="docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md",
            notes="Date de realisation et origine de propriete medicale bloquees sans validation.",
        ),
        DocumentDefinition(
            doc_id="DOC-011",
            canonical_name="Acte de cession d'un cabinet dentaire",
            generator_name="generate_acte_cession_cabinet_dentaire",
            lot=3,
            category=DocumentCategory.MUTUALISABLE,
            structures=CESSION_CABINET_STRUCTURES,
            general_condition="dossier.options.cession == true",
            specific_conditions=[
                "dossier.cession.etape == acte",
                "dossier.cession.type_cabinet == dentaire",
                "deux salaries maximum source V1 si la clause est activee",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_03/"
                "Acte de cession d'un cabinet dentaire.docx"
            ),
            specification_path="docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md",
            notes="Clauses accessibilite et conciliation limitees aux documents dentaires.",
        ),
        DocumentDefinition(
            doc_id="DOC-012",
            canonical_name="Compromis de cession d'un cabinet dentaire",
            generator_name="generate_compromis_cession_cabinet_dentaire",
            lot=3,
            category=DocumentCategory.MUTUALISABLE,
            structures=CESSION_CABINET_STRUCTURES,
            general_condition="dossier.options.cession == true",
            specific_conditions=[
                "dossier.cession.etape == compromis",
                "dossier.cession.type_cabinet == dentaire",
                "taux de pret source fixe a 5 %",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_03/"
                "Compromis de cession d_un cabinet dentaire.docx"
            ),
            specification_path="docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md",
            notes="Taux fixe source conserve, sans variable nouvelle.",
        ),
        DocumentDefinition(
            doc_id="DOC-013",
            canonical_name=(
                "Formulaire de derogation pour exercer sur plusieurs sites avec la SEL "
                "- formulaire a completer"
            ),
            generator_name="generate_formulaire_derogation_sites_sel",
            lot=3,
            category=DocumentCategory.MUTUALISABLE,
            structures=DEROGATION_CORE_STRUCTURES,
            general_condition="dossier.options.derogation == true",
            specific_conditions=[
                "derogation.type == multi_sites_sel",
                "derogation.mode_rendu == formulaire_a_completer",
                "roles representant legal et associe exercant fournis explicitement",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_03/"
                "Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL.docx"
            ),
            specification_path="docs/delivery/lot_03_derogations_spec_texte_v1.md",
            notes=(
                "Pre-remplissage partiel uniquement ; zones narratives conservees comme "
                "formulaire a completer."
            ),
        ),
        DocumentDefinition(
            doc_id="DOC-014",
            canonical_name=(
                "Demande de derogation cumul SELARL - BNC - formulaire a completer"
            ),
            generator_name="generate_demande_derogation_cumul_selarl_bnc",
            lot=3,
            category=DocumentCategory.MUTUALISABLE,
            structures=["SELARL"],
            general_condition="dossier.options.derogation == true",
            specific_conditions=[
                "derogation.type == cumul_sel_bnc",
                "derogation.mode_rendu == formulaire_a_completer",
                "zones de cumul et motifs conservees comme champs manuels",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_03/"
                "Demande de dérogation cumul SELARL - BNC.docx"
            ),
            specification_path="docs/delivery/lot_03_derogations_spec_texte_v1.md",
            notes=(
                "Pre-remplissage partiel uniquement ; cumul salariee legacy reste hors "
                "perimetre."
            ),
        ),
        DocumentDefinition(
            doc_id="DOC-015",
            canonical_name="Statuts SAS / SPFPL medecins",
            generator_name="generate_statuts_sas_spfpl_medecins",
            lot=4,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_SAS_STRUCTURES,
            general_condition="dossier.structure == SAS",
            specific_conditions=[
                "statuts_sas.type == spfpl_medecins",
                "statuts_sas.profession == medecin",
                "actionnaire unique uniquement",
                "president rattache a actionnaire_unique",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx",
            specification_path="docs/delivery/lot_04_statuts_sas_spec_texte_v1.md",
            notes="Statuts SAS V1 limites a la source SPFPL medecins actionnaire unique.",
        ),
        DocumentDefinition(
            doc_id="DOC-035",
            canonical_name="Statuts SPFPL cession",
            generator_name="generate_statuts_spfpl_cession",
            lot=4,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_SPFPL_CESSION_STRUCTURES,
            general_condition="dossier.structure == SPFPL cession",
            specific_conditions=[
                "operation_spfpl.type == cession",
                "dossier.options.cession == true",
                "associe unique uniquement en V1",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_04/Statuts_SPFPLAS_dentistes_cession.docx",
            specification_path="docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md",
            notes="Statuts SPFPL cession V1 exposes par reconciliation moteur.",
        ),
        DocumentDefinition(
            doc_id="DOC-036",
            canonical_name="Statuts SPFPL apport",
            generator_name="generate_statuts_spfpl_apport",
            lot=4,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_SPFPL_APPORT_STRUCTURES,
            general_condition="dossier.structure == SPFPL apport",
            specific_conditions=[
                "operation_spfpl.type == apport",
                "dossier.options.apport == true",
                "associe unique uniquement en V1",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_04/Statuts SPFPLAS dentistes - apport.docx",
            specification_path="docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md",
            notes="Statuts SPFPL apport V1 exposes par reconciliation moteur.",
        ),
        DocumentDefinition(
            doc_id="DOC-016",
            canonical_name="Statuts SELARL chirurgien-dentiste",
            generator_name="generate_statuts_selarl_chirurgien_dentiste",
            lot=4,
            category=DocumentCategory.SPECIFIQUE,
            structures=["SELARL"],
            general_condition="dossier.structure == SELARL",
            specific_conditions=[
                "statuts_sel.overlay == selarl_dentiste",
                "associe unique uniquement en V1",
                "pluralite associes bloquee sans wording valide",
            ],
            dynamic_associates=False,
            grammar_variants=True,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_04/"
                "Modele statuts SELARL chirurgien dentiste sans communaute.docx"
            ),
            specification_path=(
                "docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md"
            ),
            notes="Statuts SEL d'exercice V1, overlay dentiste associe unique.",
        ),
        DocumentDefinition(
            doc_id="DOC-017",
            canonical_name="Statuts SELARL medecin",
            generator_name="generate_statuts_selarl_medecin",
            lot=4,
            category=DocumentCategory.SPECIFIQUE,
            structures=["SELARL"],
            general_condition="dossier.structure == SELARL",
            specific_conditions=[
                "statuts_sel.overlay == selarl_medecin",
                "associe unique uniquement en V1",
                "ligne personne_2 source non canonique omise en V1",
            ],
            dynamic_associates=False,
            grammar_variants=True,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_04/Modèle statuts SELARL médecins.docx",
            specification_path=(
                "docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md"
            ),
            notes="Statuts SEL d'exercice V1, overlay medecin associe unique.",
        ),
        DocumentDefinition(
            doc_id="DOC-018",
            canonical_name="Statuts SELAS medecin",
            generator_name="generate_statuts_selas_medecin",
            lot=4,
            category=DocumentCategory.SPECIFIQUE,
            structures=["SELAS"],
            general_condition="dossier.structure == SELAS",
            specific_conditions=[
                "statuts_sel.overlay == selas_medecin",
                "associe unique uniquement en V1",
                "second lieu rendu seulement si nom et adresse sont fournis ensemble",
            ],
            dynamic_associates=False,
            grammar_variants=True,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_04/Statuts_SELAS_medecin.docx",
            specification_path=(
                "docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md"
            ),
            notes="Statuts SEL d'exercice V1, overlay SELAS medecin associe unique.",
        ),
        DocumentDefinition(
            doc_id="DOC-019",
            canonical_name="Statuts SCS",
            generator_name="generate_statuts_scs",
            lot=4,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_CIVILS_SCS_STRUCTURES,
            general_condition="dossier.structure == SCS",
            specific_conditions=[
                "statuts_civils.type == scs",
                "associes[] entre 1 et 6",
                "roles commandite et commanditaire explicites",
            ],
            dynamic_associates=True,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_04/Statuts_SCS_modele.docx",
            specification_path="docs/delivery/lot_04_statuts_civils_arbitrages_v1.md",
            notes="SCM exclu de ce ticket ; statuts SCS reconstruits depuis source DOCX.",
        ),
        DocumentDefinition(
            doc_id="DOC-020",
            canonical_name="Statuts SCI",
            generator_name="generate_statuts_sci",
            lot=4,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_CIVILS_SCI_STRUCTURES,
            general_condition="dossier.structure == SCI",
            specific_conditions=[
                "statuts_civils.type == sci",
                "associes[] personnes physiques entre 1 et 6",
                "option IS hors generateur statuts",
            ],
            dynamic_associates=True,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_04/Modèle statuts SCI.docx",
            specification_path="docs/delivery/lot_04_statuts_civils_arbitrages_v1.md",
            notes="Personnes morales SCI bloquees en V1 faute de source observee.",
        ),
        DocumentDefinition(
            doc_id="DOC-021",
            canonical_name="Statuts SCI IRIS",
            generator_name="generate_statuts_sci_iris",
            lot=4,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_CIVILS_SCI_IRIS_STRUCTURES,
            general_condition="dossier.structure == SCI IRIS",
            specific_conditions=[
                "statuts_civils.type == sci_iris",
                "associe personne morale source requis",
                "resultat.groupes_parts[] explicite",
            ],
            dynamic_associates=True,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_04/Modèle statuts SCI IRIS.docx",
            specification_path="docs/delivery/lot_04_statuts_civils_arbitrages_v1.md",
            notes="Lettre option IS separee hors generateur statuts civils.",
        ),
        DocumentDefinition(
            doc_id="DOC-022",
            canonical_name="Lettre option IS",
            generator_name="generate_lettre_option_is",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=OPTION_IS_STRUCTURES,
            general_condition="dossier.options.option_is == true",
            specific_conditions=[
                "SCI et SCI IRIS uniquement",
                "statuts_civils.type coherent avec la structure",
                "centre des impots fourni explicitement",
            ],
            dynamic_associates=True,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_05/lettre option IS.docx",
            specification_path="docs/delivery/lot_05_lettre_option_is_spec_v1.md",
            notes="Document dedie, non injecte dans les statuts civils.",
        ),
        DocumentDefinition(
            doc_id="DOC-023",
            canonical_name="PV remuneration president SAS",
            generator_name="generate_pv_remuneration_president_sas",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_SAS_STRUCTURES,
            general_condition="dossier.structure == SAS",
            specific_conditions=[
                "statuts_sas.type == spfpl_medecins",
                "statuts_sas.profession == medecin",
                "dossier.options.associe_unique == true",
                "president.ref_associe_index == 0",
                "remuneration_president.type == absence_remuneration",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_import/raw_drive_dump/Creation SAS/"
                "PV remuneration president - transforme.docx"
            ),
            specification_path="docs/delivery/lot_05_sas_satellites_spec_texte_v1.md",
            notes=(
                "Satellite SAS V1 limite au president masculin actionnaire unique et "
                "a l'absence de remuneration jusqu'a la cloture du premier exercice."
            ),
        ),
        DocumentDefinition(
            doc_id="DOC-024",
            canonical_name="Attestation capital / liste des souscripteurs SAS",
            generator_name="generate_attestation_capital_liste_souscripteurs_sas",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_SAS_STRUCTURES,
            general_condition="dossier.structure == SAS",
            specific_conditions=[
                "statuts_sas.type == spfpl_medecins",
                "statuts_sas.profession == medecin",
                "dossier.options.associe_unique == true",
                "dossier.options.apport == true",
                "un seul souscripteur",
                "apports en nature structures",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_05/"
                "Attestation sur le capital - apport - liste des souscripteurs.docx"
            ),
            specification_path="docs/delivery/lot_05_sas_satellites_spec_texte_v1.md",
            notes=(
                "Satellite SAS V1 ; la duplication attestation/liste des souscripteurs "
                "est rendue comme un seul document."
            ),
        ),
        DocumentDefinition(
            doc_id="DOC-037",
            canonical_name="Note d'information SPFPL",
            generator_name="generate_note_information_spfpl",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=["SPFPL cession", "SPFPL apport"],
            general_condition="operation_spfpl.type in {cession, apport}",
            specific_conditions=[
                "dossier.options.cession == true pour SPFPL cession",
                "dossier.options.apport == true pour SPFPL apport",
                "wording cession/apport tranche par operation_spfpl.type",
            ],
            dynamic_associates=True,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_05/NOTE D'INFORMATION.docx",
            specification_path="docs/delivery/lot_05_spfpl_spec_texte_v1.md",
            notes="Generateur SPFPL deja teste, rendu atteignable par l'orchestrateur.",
        ),
        DocumentDefinition(
            doc_id="DOC-038",
            canonical_name="PV agrement cession SPFPL - associe unique",
            generator_name="generate_pv_agrement_cession_spfpl_associe_unique",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_SPFPL_CESSION_STRUCTURES,
            general_condition=(
                "dossier.structure == SPFPL cession et dossier.options.cession == true"
            ),
            specific_conditions=[
                "operation_spfpl.type == cession",
                "dossier.options.associe_unique == true",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_05/"
                "PV SELARL agrément cession SPFPL - SELARL 1 associé - transforme.docx"
            ),
            specification_path="docs/delivery/lot_05_spfpl_spec_texte_v1.md",
            notes="Wording cession conserve selon arbitrage V1, sans formule apport.",
        ),
        DocumentDefinition(
            doc_id="DOC-039",
            canonical_name="PV agrement cession SPFPL - plusieurs associes",
            generator_name="generate_pv_agrement_cession_spfpl_plusieurs_associes",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_SPFPL_CESSION_STRUCTURES,
            general_condition=(
                "dossier.structure == SPFPL cession et dossier.options.cession == true"
            ),
            specific_conditions=[
                "operation_spfpl.type == cession",
                "dossier.options.associe_unique == false",
                "totalite des parts presente ou representee",
            ],
            dynamic_associates=True,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_05/"
                "PV SELARL agrément cession SPFPL - SELARL plusieurs associés - transforme.docx"
            ),
            specification_path="docs/delivery/lot_05_spfpl_spec_texte_v1.md",
            notes="Selection pluralite explicite par dossier.options.associe_unique == false.",
        ),
        DocumentDefinition(
            doc_id="DOC-040",
            canonical_name="Acte de cession de parts SPFPL",
            generator_name="generate_acte_cession_parts_spfpl",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_SPFPL_CESSION_STRUCTURES,
            general_condition=(
                "dossier.structure == SPFPL cession et dossier.options.cession == true"
            ),
            specific_conditions=[
                "operation_spfpl.type == cession",
                "operation_spfpl.nature_titres != actions",
                "operation_spfpl.document_demande != acte_cession_actions",
            ],
            dynamic_associates=True,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_05/Acte_cession_SPFPL_tiers_part_modele.docx",
            specification_path="docs/delivery/lot_05_spfpl_spec_texte_v1.md",
            notes="Document parts distinct de l'acte actions DOC-029.",
        ),
        DocumentDefinition(
            doc_id="DOC-041",
            canonical_name="Contrat d'apport SEL vers SPFPL",
            generator_name="generate_contrat_apport_spfpl",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_SPFPL_APPORT_STRUCTURES,
            general_condition="dossier.structure == SPFPL apport et dossier.options.apport == true",
            specific_conditions=[
                "operation_spfpl.type == apport",
                "evaluateur_apport et commissaire_aux_apports fournis explicitement",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_05/Contrat d_apport SEL SPFPL.docx",
            specification_path="docs/delivery/lot_05_spfpl_spec_texte_v1.md",
            notes="Entites fixes source remplacees par contexte explicite selon tests V1.",
        ),
        DocumentDefinition(
            doc_id="DOC-042",
            canonical_name="Attestation capital / liste des souscripteurs SPFPL",
            generator_name="generate_attestation_capital_liste_souscripteurs_spfpl",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_SPFPL_APPORT_STRUCTURES,
            general_condition="dossier.structure == SPFPL apport et dossier.options.apport == true",
            specific_conditions=[
                "operation_spfpl.type == apport",
                "un seul souscripteur",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_05/"
                "Attestation sur le capital - apport - liste des souscripteurs.docx"
            ),
            specification_path="docs/delivery/lot_05_spfpl_spec_texte_v1.md",
            notes="Document SPFPL distinct du satellite SAS DOC-024.",
        ),
        DocumentDefinition(
            doc_id="DOC-043",
            canonical_name="Attestation nomination commissaire aux apports",
            generator_name="generate_attestation_commissaire_apports",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_SPFPL_APPORT_STRUCTURES,
            general_condition="dossier.structure == SPFPL apport et dossier.options.apport == true",
            specific_conditions=[
                "operation_spfpl.type == apport",
                "commissaire_aux_apports fourni explicitement",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_05/"
                "attestation nomination commissaire aux apports - transforme.docx"
            ),
            specification_path="docs/delivery/lot_05_spfpl_spec_texte_v1.md",
            notes="Libelle commissaire aux apports conserve selon source disponible.",
        ),
        DocumentDefinition(
            doc_id="DOC-025",
            canonical_name="Statuts SCM",
            generator_name="generate_statuts_scm",
            lot=4,
            category=DocumentCategory.SPECIFIQUE,
            structures=STATUTS_CIVILS_SCM_STRUCTURES,
            general_condition="dossier.structure == SCM",
            specific_conditions=[
                "statuts_civils.type == scm",
                "associes[] entre 1 et 6",
                "apports et parts explicites par associe",
                "documents satellites SCM hors generateur statuts",
            ],
            dynamic_associates=True,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_04/Statuts SCM.docx",
            specification_path="docs/delivery/lot_04_statuts_scm_arbitrages_v1.md",
            notes="Statuts SCM V1 reconstruits depuis source DOCX, sans satellites SCM.",
        ),
        DocumentDefinition(
            doc_id="DOC-026",
            canonical_name="Pacte d'associes SCM",
            generator_name="generate_pacte_associes_scm",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=SCM_SATELLITES_STRUCTURES,
            general_condition="dossier.structure == SCM et dossier.options.scm_satellites == true",
            specific_conditions=[
                "scm_satellites.pacte_associes == true",
                "deux associes historiques exactement",
                "source DOCX uniquement, liste depenses communes exclue",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_05/Pacte d_associés SCM.docx",
            specification_path="docs/delivery/lot_05_scm_satellites_spec_texte_v1.md",
            notes="Sous-batch SCM satellites DOCX V1, sans source .doc.",
        ),
        DocumentDefinition(
            doc_id="DOC-027",
            canonical_name="Contrat d'exercice professionnel a frais communs",
            generator_name="generate_contrat_frais_communs",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=SCM_SATELLITES_STRUCTURES,
            general_condition="dossier.structure == SCM et dossier.options.scm_satellites == true",
            specific_conditions=[
                "scm_satellites.contrat_frais_communs == true",
                "deux parties exactement",
                "locaux dentaires source conserves sans adaptation",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_05/CONTRAT FRAIS COMMUNS.docx",
            specification_path="docs/delivery/lot_05_scm_satellites_spec_texte_v1.md",
            notes="Sous-batch SCM satellites DOCX V1, table source fixe.",
        ),
        DocumentDefinition(
            doc_id="DOC-028",
            canonical_name="Reglement interieur de la SCM",
            generator_name="generate_reglement_interieur_scm",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=SCM_SATELLITES_STRUCTURES,
            general_condition="dossier.structure == SCM et dossier.options.scm_satellites == true",
            specific_conditions=[
                "scm_satellites.reglement_interieur == true",
                "deux parties et deux praticiens exactement",
                "formes juridiques des deux parties identiques",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_05/"
                "REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - "
                "SCM DES DOCTEURS XX.docx"
            ),
            specification_path="docs/delivery/lot_05_scm_satellites_spec_texte_v1.md",
            notes="Sous-batch SCM satellites DOCX V1, quatre exemplaires source conserves.",
        ),
        DocumentDefinition(
            doc_id="DOC-029",
            canonical_name="Acte de cession d'actions SPFPL a un tiers",
            generator_name="generate_acte_cession_actions_spfpl",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=["SPFPL cession"],
            general_condition=(
                "dossier.structure == SPFPL cession et dossier.options.cession == true"
            ),
            specific_conditions=[
                "operation_spfpl.type == cession",
                "operation_spfpl.nature_titres == actions",
                "operation_spfpl.document_demande == acte_cession_actions",
                "societe cible limitee au wording source SELAS chirurgien-dentiste",
                "paiement source credit bancaire comptant par cheque de banque confirme",
                "GAP, agrement unanime et PV coherent explicitement confirmes",
                "signature electronique Yousign",
                "cedant masculin uniquement faute de variante source",
            ],
            dynamic_associates=True,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_05/Acte_cession_SPFPL_tiers_modele.docx"
            ),
            specification_path=(
                "docs/delivery/lot_05_acte_cession_actions_spec_texte_v1.md"
            ),
            notes=(
                "Acte actions SPFPL V1 reconstruit from-scratch ; points ouverts "
                "transformes en blocages explicites."
            ),
        ),
        DocumentDefinition(
            doc_id="DOC-030",
            canonical_name="Liste des depenses communes SCM",
            generator_name="generate_liste_depenses_communes_scm",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=SCM_SATELLITES_STRUCTURES,
            general_condition="dossier.structure == SCM et dossier.options.scm_satellites == true",
            specific_conditions=[
                "scm_satellites.liste_depenses_communes == true",
                "source DOCX convertie disponible",
                "deux associes signataires exactement",
                "table des depenses commune source fixe",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_05/Liste dépenses communes SCM.docx",
            specification_path="docs/delivery/lot_05_scm_satellites_spec_texte_v1.md",
            notes=(
                "Satellite SCM V1 reconstruit depuis la source DOCX convertie, table fixe "
                "et deux signatures source conservees."
            ),
        ),
        DocumentDefinition(
            doc_id="DOC-031",
            canonical_name="PV AGE cession part SCM",
            generator_name="generate_pv_age_cession_parts_scm",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=SCM_CESSION_STRUCTURES,
            general_condition=(
                "dossier.structure in {SELARL, SELAS} et "
                "dossier.options.scm_cession == true"
            ),
            specific_conditions=[
                "overlay SELARL ou SELAS selon dossier.structure",
                "trois associes presents et quatre lignes de repartition apres cession",
                "parts apres cession totalisant scm_cedee.nb_parts_total",
            ],
            dynamic_associates=True,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_05/PV AGE cession part SCM.docx",
            specification_path=(
                "docs/delivery/lot_05_scm_cession_block_resolution_v1.md"
            ),
            notes="Bloc cession SCM V1, overlay SELARL / SELAS sans correction de wording.",
        ),
        DocumentDefinition(
            doc_id="DOC-032",
            canonical_name="Courrier SDE cession SCM",
            generator_name="generate_courrier_sde_cession_scm",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=SCM_CESSION_STRUCTURES,
            general_condition=(
                "dossier.structure in {SELARL, SELAS} et "
                "dossier.options.scm_cession == true"
            ),
            specific_conditions=[
                "SELARL sans destinataire fiscal et avec 4 exemplaires fixes",
                "SELAS avec destinataire fiscal et nombre d'exemplaires variable",
                "montant des droits et signataire SDE fournis explicitement",
            ],
            dynamic_associates=False,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path="project/source_documents/lot_05/Courrier SDE.docx",
            specification_path=(
                "docs/delivery/lot_05_scm_cession_block_resolution_v1.md"
            ),
            notes="Bloc cession SCM V1, divergences SELARL / SELAS conservees.",
        ),
        DocumentDefinition(
            doc_id="DOC-033",
            canonical_name="Acte de cession des parts de la SCM vers SEL",
            generator_name="generate_acte_cession_parts_scm",
            lot=5,
            category=DocumentCategory.SPECIFIQUE,
            structures=SCM_CESSION_STRUCTURES,
            general_condition=(
                "dossier.structure in {SELARL, SELAS} et "
                "dossier.options.scm_cession == true"
            ),
            specific_conditions=[
                "representant de la SEL cessionnaire confirme",
                "repartition avant cession totalisant scm_cedee.nb_parts_total",
                "credit-vendeur conditionnel, jamais rendu comme instruction source",
            ],
            dynamic_associates=True,
            grammar_variants=False,
            workflow_status=WorkflowStatus.TESTE,
            source_path=(
                "project/source_documents/lot_05/"
                "Acte de cession des parts de la SCM à la SELARL - transforme.docx"
            ),
            specification_path=(
                "docs/delivery/lot_05_scm_cession_block_resolution_v1.md"
            ),
            notes=(
                "Acte cession parts SCM V1, source SELARL transformee et source SELAS "
                "dediee conservees."
            ),
        ),
    ]


def catalog_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for document in build_seed_catalog():
        rows.append(
            {
                "doc_id": document.doc_id,
                "nom": document.canonical_name,
                "lot": str(document.lot),
                "statut": document.workflow_status.value,
                "categorie": document.category.value,
                "condition": document.general_condition,
            }
        )
    return rows
