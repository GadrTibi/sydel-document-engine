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