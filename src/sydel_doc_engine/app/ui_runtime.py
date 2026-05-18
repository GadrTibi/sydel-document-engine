from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import ValidationError

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.orchestrator.service import DocumentOrchestrator
from sydel_doc_engine.registry.catalog import build_seed_catalog
from sydel_doc_engine.rendering.pdf_export import (
    PdfExportError,
    PdfExportResult,
    export_docx_batch_to_pdf,
)
from sydel_doc_engine.rendering.zip_bundle import create_zip_bundle

DEFAULT_ARTIFACTS_DIR = Path("artifacts") / "ui_pdf_zip_integration_001"
DEFAULT_CONTEXTS_DIR = Path("examples") / "contexts"
PDF_OUTPUT_DIR_NAME = "pdf"
ZIP_FILE_NAME = "dossier_generation.zip"


@dataclass(frozen=True)
class GeneratedDossier:
    output_dir: Path
    docx_paths: list[Path]
    pdf_results: list[PdfExportResult]
    zip_path: Path
    pdf_error: str | None = None

    @property
    def pdf_paths(self) -> list[Path]:
        return [result.pdf_path for result in self.pdf_results]


@dataclass(frozen=True)
class GeneratedPdfBatch:
    pdf_results: list[PdfExportResult]
    pdf_error: str | None = None

    @property
    def pdf_paths(self) -> list[Path]:
        return [result.pdf_path for result in self.pdf_results]


def list_context_examples(contexts_dir: Path = DEFAULT_CONTEXTS_DIR) -> list[Path]:
    if not contexts_dir.is_dir():
        return []
    return sorted(
        path
        for path in contexts_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml", ".json"}
    )


def load_context_payload(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_context_payload(payload: str) -> DocumentGenerationContext:
    loaded = yaml.safe_load(payload)
    if not isinstance(loaded, Mapping):
        raise ValueError("Le contexte doit etre un objet YAML ou JSON.")
    try:
        return DocumentGenerationContext.model_validate(dict(loaded))
    except ValidationError as exc:
        raise ValueError(str(exc)) from exc


def selected_document_rows(ctx: DocumentGenerationContext) -> list[dict[str, str]]:
    orchestrator = DocumentOrchestrator(build_seed_catalog())
    rows: list[dict[str, str]] = []
    for document in orchestrator.select_documents_for_context(ctx):
        rows.append(
            {
                "doc_id": document.doc_id,
                "nom": document.canonical_name,
                "lot": str(document.lot),
                "condition": document.general_condition,
            }
        )
    return rows


def build_output_dir(
    source_name: str,
    base_dir: Path = DEFAULT_ARTIFACTS_DIR,
) -> Path:
    stem = Path(source_name).stem or "contexte"
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", stem).strip("._")
    return base_dir / (slug or "contexte")


def generate_dossier(
    ctx: DocumentGenerationContext,
    output_dir: Path,
    *,
    generate_pdf: bool,
) -> GeneratedDossier:
    docx_paths = generate_docx_files(ctx, output_dir)
    pdf_batch = (
        generate_pdf_files(docx_paths, output_dir)
        if generate_pdf
        else GeneratedPdfBatch(pdf_results=[])
    )
    zip_path = generate_zip_file(output_dir, docx_paths, pdf_batch.pdf_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=pdf_batch.pdf_results,
        zip_path=zip_path,
        pdf_error=pdf_batch.pdf_error,
    )


def generate_docx_files(ctx: DocumentGenerationContext, output_dir: Path) -> list[Path]:
    orchestrator = DocumentOrchestrator(build_seed_catalog())
    selected_documents = orchestrator.select_documents_for_context(ctx)
    if not selected_documents:
        raise RuntimeError("Aucun document selectionne par l'orchestrateur.")
    return orchestrator.generate_documents(ctx, output_dir)


def generate_docx_files_for_document_codes(
    ctx: DocumentGenerationContext,
    output_dir: Path,
    document_codes: Iterable[str],
) -> list[Path]:
    allowed_codes = set(document_codes)
    if not allowed_codes:
        raise RuntimeError("Aucun document generable pret dans l'assistant metier.")
    filtered_catalog = [
        document for document in build_seed_catalog() if document.doc_id in allowed_codes
    ]
    orchestrator = DocumentOrchestrator(filtered_catalog)
    selected_documents = orchestrator.select_documents_for_context(ctx)
    if not selected_documents:
        raise RuntimeError("Aucun document pret selectionne par l'assistant metier.")
    return orchestrator.generate_documents(ctx, output_dir)


def generate_pdf_files(docx_paths: list[Path], output_dir: Path) -> GeneratedPdfBatch:
    try:
        pdf_results = export_docx_batch_to_pdf(
            docx_paths,
            output_dir / PDF_OUTPUT_DIR_NAME,
        )
    except PdfExportError as exc:
        return GeneratedPdfBatch(pdf_results=[], pdf_error=str(exc))
    return GeneratedPdfBatch(pdf_results=pdf_results)


def generate_zip_file(
    output_dir: Path,
    docx_paths: list[Path],
    pdf_paths: list[Path] | None = None,
) -> Path:
    bundle_files = [*docx_paths, *(pdf_paths or [])]
    zip_result = create_zip_bundle(
        output_dir / ZIP_FILE_NAME,
        bundle_files,
        root_dir=output_dir,
    )
    return zip_result.zip_path
