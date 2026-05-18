from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from docx import Document

from sydel_doc_engine.app.business_wizard import (
    BusinessWizardInput,
    business_document_table_rows,
    evaluate_business_wizard,
    sample_business_wizard_input,
)
from sydel_doc_engine.app.ui_runtime import generate_docx_files, generate_zip_file
from sydel_doc_engine.orchestrator.service import DocumentOrchestrator
from sydel_doc_engine.registry.catalog import build_seed_catalog


def test_business_wizard_builds_minimal_valid_context() -> None:
    validation = evaluate_business_wizard(sample_business_wizard_input())

    assert validation.context is not None
    assert validation.can_generate_docx is True
    assert validation.missing_fields == ()
    assert validation.inconsistencies == ()
    assert validation.context.structure == "SCI"


def test_business_wizard_validation_detects_missing_fields() -> None:
    data = BusinessWizardInput(structure="SCI")

    validation = evaluate_business_wizard(data)

    assert validation.can_generate_docx is False
    assert "personne_signataire.civilite" in validation.missing_fields
    assert "societe.denomination" in validation.missing_fields
    assert "signature.date" in validation.missing_fields
    assert any(row.status == "incomplet" for row in validation.document_rows)


def test_business_wizard_document_rows_show_generable_documents() -> None:
    validation = evaluate_business_wizard(sample_business_wizard_input())

    rows = business_document_table_rows(validation)

    assert [row["code document"] for row in rows] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    ]
    assert {row["statut"] for row in rows} == {"generable"}


def test_business_wizard_context_uses_orchestrator_selection() -> None:
    validation = evaluate_business_wizard(sample_business_wizard_input())
    assert validation.context is not None
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents_for_context(validation.context)

    assert [document.doc_id for document in selected] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    ]


def test_business_wizard_generates_docx_and_zip_without_residual_placeholders(
    tmp_path: Path,
) -> None:
    validation = evaluate_business_wizard(sample_business_wizard_input())
    assert validation.context is not None

    docx_paths = generate_docx_files(validation.context, tmp_path)
    zip_path = generate_zip_file(tmp_path, docx_paths)

    assert len(docx_paths) == 4
    for docx_path in docx_paths:
        text = _docx_text(docx_path)
        assert "[" not in text
        assert "]" not in text
    with ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "manifest.json" in names
    assert "declaration_non_condamnation.docx" in names


def _docx_text(path: Path) -> str:
    document = Document(path)
    paragraph_text = [paragraph.text for paragraph in document.paragraphs]
    table_text = [
        cell.text
        for table in document.tables
        for row in table.rows
        for cell in row.cells
    ]
    return "\n".join([*paragraph_text, *table_text])
