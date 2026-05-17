from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZipFile

import pytest

from sydel_doc_engine.rendering.zip_bundle import ZipBundleError, create_zip_bundle


def test_create_zip_bundle_smoke_from_generated_files(tmp_path: Path) -> None:
    output_dir = tmp_path / "generated"
    output_dir.mkdir()
    docx_path = output_dir / "declaration_non_condamnation.docx"
    pdf_path = output_dir / "declaration_non_condamnation.pdf"
    docx_path.write_bytes(b"docx content")
    pdf_path.write_bytes(b"pdf content")

    result = create_zip_bundle(
        tmp_path / "dossier.zip",
        [pdf_path, docx_path],
        root_dir=output_dir,
    )

    assert result.zip_path.is_file()
    assert [entry.archive_path for entry in result.entries] == [
        "declaration_non_condamnation.docx",
        "declaration_non_condamnation.pdf",
    ]
    assert result.manifest_archive_path == "manifest.json"

    with ZipFile(result.zip_path) as archive:
        assert archive.namelist() == [
            "declaration_non_condamnation.docx",
            "declaration_non_condamnation.pdf",
            "manifest.json",
        ]
        assert archive.read("declaration_non_condamnation.docx") == b"docx content"
        manifest = json.loads(archive.read("manifest.json"))

    assert manifest["file_count"] == 2
    assert manifest["formats"] == ["docx", "pdf"]
    assert [file_info["archive_path"] for file_info in manifest["files"]] == [
        "declaration_non_condamnation.docx",
        "declaration_non_condamnation.pdf",
    ]
    assert all(file_info["sha256"] for file_info in manifest["files"])


def test_create_zip_bundle_preserves_relative_paths_when_root_dir_is_provided(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "generated"
    sub_dir = output_dir / "docx"
    sub_dir.mkdir(parents=True)
    docx_path = sub_dir / "procuration.docx"
    docx_path.write_bytes(b"content")

    result = create_zip_bundle(tmp_path / "dossier.zip", [docx_path], root_dir=output_dir)

    assert [entry.archive_path for entry in result.entries] == ["docx/procuration.docx"]
    with ZipFile(result.zip_path) as archive:
        assert "docx/procuration.docx" in archive.namelist()


def test_create_zip_bundle_rejects_missing_files(tmp_path: Path) -> None:
    with pytest.raises(ZipBundleError, match="introuvable"):
        create_zip_bundle(tmp_path / "dossier.zip", [tmp_path / "missing.docx"])


def test_create_zip_bundle_rejects_temporary_or_unsupported_files(tmp_path: Path) -> None:
    temp_file = tmp_path / "~$document.docx"
    txt_file = tmp_path / "notes.txt"
    temp_file.write_bytes(b"temp")
    txt_file.write_text("notes", encoding="utf-8")

    with pytest.raises(ZipBundleError, match="temporaire"):
        create_zip_bundle(tmp_path / "temp.zip", [temp_file])

    with pytest.raises(ZipBundleError, match="Format non autorise"):
        create_zip_bundle(tmp_path / "notes.zip", [txt_file])


def test_create_zip_bundle_rejects_duplicate_archive_paths(tmp_path: Path) -> None:
    first = tmp_path / "a" / "same.docx"
    second = tmp_path / "b" / "same.docx"
    first.parent.mkdir()
    second.parent.mkdir()
    first.write_bytes(b"first")
    second.write_bytes(b"second")

    with pytest.raises(ZipBundleError, match="duplique"):
        create_zip_bundle(tmp_path / "dossier.zip", [first, second])
