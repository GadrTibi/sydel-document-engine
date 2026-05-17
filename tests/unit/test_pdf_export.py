from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from sydel_doc_engine.rendering import pdf_export
from sydel_doc_engine.rendering.pdf_export import (
    PdfExporterUnavailableError,
    PdfExportFailedError,
    export_docx_batch_to_pdf,
    export_docx_to_pdf,
)


def _write_docx_placeholder(path: Path) -> Path:
    path.write_bytes(b"docx-placeholder")
    return path


def test_export_docx_to_pdf_uses_libreoffice_backend(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_path = _write_docx_placeholder(tmp_path / "source.docx")
    target_path = tmp_path / "target.pdf"

    def fake_run(
        command: list[str],
        *,
        capture_output: bool,
        check: bool,
        text: bool,
        timeout: int,
    ) -> subprocess.CompletedProcess[str]:
        assert capture_output is True
        assert check is False
        assert text is True
        assert timeout == 120
        output_dir = Path(command[command.index("--outdir") + 1])
        (output_dir / "source.pdf").write_bytes(b"%PDF-1.4")
        return subprocess.CompletedProcess(command, 0, stdout="converted", stderr="")

    monkeypatch.setattr(pdf_export, "_find_libreoffice_executable", lambda: Path("soffice"))
    monkeypatch.setattr(pdf_export.subprocess, "run", fake_run)

    result = export_docx_to_pdf(source_path, target_path, backend="libreoffice")

    assert result.source_docx == source_path
    assert result.pdf_path == target_path
    assert result.backend == "libreoffice"
    assert target_path.read_bytes() == b"%PDF-1.4"


def test_export_docx_to_pdf_uses_word_com_backend(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_path = _write_docx_placeholder(tmp_path / "source.docx")
    target_path = tmp_path / "target.pdf"

    def fake_run(
        command: list[str],
        *,
        capture_output: bool,
        check: bool,
        text: bool,
        timeout: int,
    ) -> subprocess.CompletedProcess[str]:
        assert capture_output is True
        assert check is False
        assert text is True
        assert timeout == 120
        Path(command[-2]).write_bytes(b"%PDF-1.4")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(pdf_export, "_find_libreoffice_executable", lambda: None)
    monkeypatch.setattr(pdf_export, "_find_powershell_executable", lambda: Path("powershell"))
    monkeypatch.setattr(pdf_export, "_word_com_is_available", lambda *args, **kwargs: True)
    monkeypatch.setattr(pdf_export.subprocess, "run", fake_run)

    result = export_docx_to_pdf(source_path, target_path, backend="word")

    assert result.backend == "word-com"
    assert target_path.read_bytes() == b"%PDF-1.4"


def test_export_docx_to_pdf_raises_when_no_backend_is_available(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_path = _write_docx_placeholder(tmp_path / "source.docx")

    monkeypatch.setattr(pdf_export, "_find_libreoffice_executable", lambda: None)
    monkeypatch.setattr(pdf_export, "_find_powershell_executable", lambda: None)

    with pytest.raises(PdfExporterUnavailableError, match="Aucun backend PDF local fiable"):
        export_docx_to_pdf(source_path)


def test_export_docx_to_pdf_refuses_existing_target_without_overwrite(tmp_path: Path) -> None:
    source_path = _write_docx_placeholder(tmp_path / "source.docx")
    target_path = tmp_path / "source.pdf"
    target_path.write_bytes(b"existing")

    with pytest.raises(PdfExportFailedError, match="existe deja"):
        export_docx_to_pdf(source_path, target_path, overwrite=False)


def test_export_docx_to_pdf_requires_docx_source(tmp_path: Path) -> None:
    source_path = tmp_path / "source.txt"
    source_path.write_text("not a docx", encoding="utf-8")

    with pytest.raises(PdfExportFailedError, match="n'est pas un DOCX"):
        export_docx_to_pdf(source_path)


def test_export_docx_batch_to_pdf_writes_to_output_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_paths = [
        _write_docx_placeholder(tmp_path / "first.docx"),
        _write_docx_placeholder(tmp_path / "second.docx"),
    ]
    output_dir = tmp_path / "pdf"

    def fake_export(
        docx_path: Path,
        pdf_path: Path | None = None,
        *,
        backend: pdf_export.PdfBackendName = "auto",
        overwrite: bool = True,
        timeout_seconds: int = 120,
    ) -> pdf_export.PdfExportResult:
        assert backend == "word"
        assert overwrite is False
        assert timeout_seconds == 30
        assert pdf_path is not None
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(b"%PDF-1.4")
        return pdf_export.PdfExportResult(docx_path, pdf_path, "word-com")

    monkeypatch.setattr(pdf_export, "export_docx_to_pdf", fake_export)

    results = export_docx_batch_to_pdf(
        source_paths,
        output_dir,
        backend="word",
        overwrite=False,
        timeout_seconds=30,
    )

    assert [result.pdf_path for result in results] == [
        output_dir / "first.pdf",
        output_dir / "second.pdf",
    ]
