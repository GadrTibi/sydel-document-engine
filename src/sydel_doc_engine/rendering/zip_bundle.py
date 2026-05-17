from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

DEFAULT_ALLOWED_SUFFIXES = (".docx", ".pdf")
DEFAULT_MANIFEST_NAME = "manifest.json"
DETERMINISTIC_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
TEMPORARY_FILE_PREFIXES = ("~$", ".~")
TEMPORARY_FILE_SUFFIXES = (".tmp", ".part", ".crdownload")


class ZipBundleError(ValueError):
    pass


@dataclass(frozen=True)
class ZipBundleEntry:
    source_path: Path
    archive_path: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class ZipBundleResult:
    zip_path: Path
    entries: tuple[ZipBundleEntry, ...]
    manifest_archive_path: str | None


def create_zip_bundle(
    zip_path: Path,
    files: Sequence[Path],
    *,
    root_dir: Path | None = None,
    include_manifest: bool = True,
    manifest_name: str = DEFAULT_MANIFEST_NAME,
    allowed_suffixes: Sequence[str] = DEFAULT_ALLOWED_SUFFIXES,
) -> ZipBundleResult:
    """Create a deterministic ZIP archive from already generated dossier files."""
    if not files:
        raise ZipBundleError("Aucun fichier genere fourni pour constituer le ZIP.")

    normalized_root = root_dir.resolve() if root_dir is not None else None
    allowed_suffixes_normalized = tuple(suffix.lower() for suffix in allowed_suffixes)
    entries = _build_entries(files, normalized_root, allowed_suffixes_normalized)

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, mode="w") as archive:
        for entry in entries:
            _write_file(archive, entry.source_path, entry.archive_path)
        if include_manifest:
            manifest_bytes = _build_manifest(zip_path.name, entries)
            _write_bytes(archive, manifest_name, manifest_bytes)

    return ZipBundleResult(
        zip_path=zip_path,
        entries=entries,
        manifest_archive_path=manifest_name if include_manifest else None,
    )


def _build_entries(
    files: Sequence[Path],
    root_dir: Path | None,
    allowed_suffixes: tuple[str, ...],
) -> tuple[ZipBundleEntry, ...]:
    entries_by_archive_path: dict[str, ZipBundleEntry] = {}
    for file_path in files:
        source_path = file_path.resolve()
        _validate_source_path(source_path, allowed_suffixes)
        archive_path = _archive_path_for(source_path, root_dir)
        if archive_path in entries_by_archive_path:
            raise ZipBundleError(f"Chemin ZIP duplique : {archive_path}")
        entries_by_archive_path[archive_path] = ZipBundleEntry(
            source_path=source_path,
            archive_path=archive_path,
            size_bytes=source_path.stat().st_size,
            sha256=_sha256(source_path),
        )
    return tuple(entries_by_archive_path[key] for key in sorted(entries_by_archive_path))


def _validate_source_path(source_path: Path, allowed_suffixes: tuple[str, ...]) -> None:
    if not source_path.is_file():
        raise ZipBundleError(f"Fichier genere introuvable : {source_path}")
    name_lower = source_path.name.lower()
    if source_path.name.startswith(TEMPORARY_FILE_PREFIXES) or name_lower.endswith(
        TEMPORARY_FILE_SUFFIXES
    ):
        raise ZipBundleError(f"Fichier temporaire exclu du ZIP : {source_path.name}")
    if source_path.suffix.lower() not in allowed_suffixes:
        allowed = ", ".join(allowed_suffixes)
        raise ZipBundleError(
            f"Format non autorise pour le ZIP : {source_path.name} "
            f"(formats autorises : {allowed})."
        )


def _archive_path_for(source_path: Path, root_dir: Path | None) -> str:
    if root_dir is None:
        return source_path.name
    try:
        return source_path.relative_to(root_dir).as_posix()
    except ValueError as error:
        raise ZipBundleError(
            f"Fichier hors dossier de generation : {source_path} "
            f"(racine attendue : {root_dir})."
        ) from error


def _build_manifest(zip_name: str, entries: tuple[ZipBundleEntry, ...]) -> bytes:
    payload = {
        "zip_name": zip_name,
        "file_count": len(entries),
        "formats": sorted({entry.source_path.suffix.lower().lstrip(".") for entry in entries}),
        "files": [
            {
                "archive_path": entry.archive_path,
                "source_name": entry.source_path.name,
                "format": entry.source_path.suffix.lower().lstrip("."),
                "size_bytes": entry.size_bytes,
                "sha256": entry.sha256,
            }
            for entry in entries
        ],
    }
    return json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True).encode("utf-8")


def _write_file(archive: ZipFile, source_path: Path, archive_path: str) -> None:
    _write_bytes(archive, archive_path, source_path.read_bytes())


def _write_bytes(archive: ZipFile, archive_path: str, content: bytes) -> None:
    info = ZipInfo(archive_path, date_time=DETERMINISTIC_ZIP_TIMESTAMP)
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o600 << 16
    archive.writestr(info, content)


def _sha256(source_path: Path) -> str:
    digest = hashlib.sha256()
    with source_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
