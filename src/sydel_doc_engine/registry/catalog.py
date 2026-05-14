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
