from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from sydel_doc_engine.app import ui_runtime
from sydel_doc_engine.app.ui_runtime import (
    build_output_dir,
    generate_dossier,
    parse_context_payload,
    rename_dnc_with_signataire,
    selected_document_rows,
)
from sydel_doc_engine.rendering.pdf_export import PdfExportResult


def test_parse_context_payload_accepts_yaml_example() -> None:
    payload = Path("examples/contexts/lot_01_example.yaml").read_text(encoding="utf-8")

    ctx = parse_context_payload(payload)

    assert ctx.structure == "SELARL"
    assert ctx.personne_signataire.nom == "Martin"


def test_selected_document_rows_uses_orchestrator_selection() -> None:
    payload = Path("examples/contexts/lot_01_example.yaml").read_text(encoding="utf-8")
    ctx = parse_context_payload(payload)

    rows = selected_document_rows(ctx)

    assert [row["doc_id"] for row in rows] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
    ]


def test_build_output_dir_sanitizes_source_name() -> None:
    output_dir = build_output_dir("Contexte dossier #1.yaml", Path("artifacts") / "ui")

    assert output_dir == Path("artifacts") / "ui" / "Contexte_dossier_1"


def test_rename_dnc_with_signataire_is_idempotent(tmp_path: Path) -> None:
    # O24-05 (NITPICK, re-Akainu T5) : le renommage de la DNC doit etre IDEMPOTENT /
    # robuste. Avant le fix, un 2e appel (ou un basetemp reutilise) levait
    # FileNotFoundError sur `path.replace` -> faux « failed ». On appelle 2x de suite et
    # avec une liste portant le chemin GENERIQUE perime (source deja renommee) : aucun
    # appel ne doit lever, et le resultat pointe toujours sur la DNC nommee.
    ctx = parse_context_payload(
        Path("examples/contexts/lot_01_example.yaml").read_text(encoding="utf-8")
    )
    slug = ctx.personne_signataire.nom  # "Martin"
    expected = f"declaration_non_condamnation_{slug}.docx"

    generic = tmp_path / "declaration_non_condamnation.docx"
    generic.write_bytes(b"dnc")
    other = tmp_path / "procuration.docx"
    other.write_bytes(b"proc")

    first = rename_dnc_with_signataire([generic, other], ctx)
    assert [p.name for p in first] == [expected, "procuration.docx"]
    assert (tmp_path / expected).exists()

    # 2e appel sur le RESULTAT (deja renomme) : no-op, ne leve pas.
    second = rename_dnc_with_signataire(first, ctx)
    assert [p.name for p in second] == [expected, "procuration.docx"]

    # 3e appel avec le chemin GENERIQUE perime (source absente, cible deja presente) :
    # ne leve pas et retourne la cible existante (robustesse basetemp reutilise).
    third = rename_dnc_with_signataire([generic, other], ctx)
    assert [p.name for p in third] == [expected, "procuration.docx"]


def test_generate_dossier_creates_zip_with_docx_and_pdf(
    tmp_path: Path,
    monkeypatch,
) -> None:
    payload = Path("examples/contexts/lot_02_orchestrator_positive_example.yaml").read_text(
        encoding="utf-8"
    )
    ctx = parse_context_payload(payload)

    def fake_export_docx_batch_to_pdf(
        docx_paths: list[Path],
        output_dir: Path | None = None,
        **_: object,
    ) -> list[PdfExportResult]:
        assert output_dir is not None
        output_dir.mkdir(parents=True, exist_ok=True)
        results: list[PdfExportResult] = []
        for docx_path in docx_paths:
            pdf_path = output_dir / docx_path.with_suffix(".pdf").name
            pdf_path.write_bytes(b"%PDF-1.4")
            results.append(PdfExportResult(docx_path, pdf_path, "test"))
        return results

    monkeypatch.setattr(
        ui_runtime,
        "export_docx_batch_to_pdf",
        fake_export_docx_batch_to_pdf,
    )

    result = generate_dossier(ctx, tmp_path, generate_pdf=True)

    assert len(result.docx_paths) == 4
    assert len(result.pdf_paths) == 4
    assert result.pdf_error is None
    with ZipFile(result.zip_path) as archive:
        names = set(archive.namelist())
    assert "declaration_non_condamnation.docx" in names
    assert "pdf/declaration_non_condamnation.pdf" in names
    assert "manifest.json" in names
