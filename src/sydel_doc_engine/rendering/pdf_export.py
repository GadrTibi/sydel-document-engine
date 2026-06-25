from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal

PdfBackendName = Literal["auto", "libreoffice", "word"]

DEFAULT_TIMEOUT_SECONDS: Final[int] = 120
PDF_EXTENSION: Final[str] = ".pdf"
DOCX_EXTENSION: Final[str] = ".docx"
WORD_PDF_FORMAT: Final[int] = 17
LIBREOFFICE_ENV_VAR: Final[str] = "SYDEL_LIBREOFFICE_PATH"


class PdfExportError(RuntimeError):
    pass


class PdfExporterUnavailableError(PdfExportError):
    pass


class PdfExportFailedError(PdfExportError):
    pass


@dataclass(frozen=True)
class PdfExportResult:
    source_docx: Path
    pdf_path: Path
    backend: str


@dataclass(frozen=True)
class _ResolvedBackend:
    name: Literal["libreoffice", "word-com"]
    executable: Path


def export_docx_to_pdf(
    docx_path: Path,
    pdf_path: Path | None = None,
    *,
    backend: PdfBackendName = "auto",
    overwrite: bool = True,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    _resolved_backend: _ResolvedBackend | None = None,
) -> PdfExportResult:
    source_path = _validate_source_docx(docx_path)
    target_path = _resolve_pdf_path(source_path, pdf_path)
    if target_path.exists():
        if not overwrite:
            raise PdfExportFailedError(f"Le PDF cible existe deja : {target_path}")
        target_path.unlink()

    target_path.parent.mkdir(parents=True, exist_ok=True)
    # Perf (chantier 2026-06-24) : reutilise un backend deja resolu si fourni (chemin batch),
    # sinon resout (appel unitaire). Evite de re-sonder Word COM (~4 s) a chaque document.
    resolved_backend = _resolved_backend or _resolve_backend(
        backend, timeout_seconds=timeout_seconds
    )
    if resolved_backend.name == "libreoffice":
        _export_with_libreoffice(
            source_path,
            target_path,
            resolved_backend.executable,
            timeout_seconds,
        )
    else:
        _export_with_word_com(
            source_path,
            target_path,
            resolved_backend.executable,
            timeout_seconds,
        )
    _ensure_pdf_created(target_path, resolved_backend.name)
    return PdfExportResult(
        source_docx=source_path,
        pdf_path=target_path,
        backend=resolved_backend.name,
    )


def export_docx_batch_to_pdf(
    docx_paths: Iterable[Path],
    output_dir: Path | None = None,
    *,
    backend: PdfBackendName = "auto",
    overwrite: bool = True,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> list[PdfExportResult]:
    docx_list = [Path(p) for p in docx_paths]
    results: list[PdfExportResult] = []
    if not docx_list:
        return results
    # Perf (chantier 2026-06-24) : resoudre le backend PDF UNE SEULE FOIS pour tout le lot
    # au lieu de re-sonder a chaque document (sonde Word COM ~4 s x N docs, 100% gaspillee
    # sur un dossier complet). Garde lot vide : on ne sonde pas s'il n'y a rien a convertir.
    resolved_backend = _resolve_backend(backend, timeout_seconds=timeout_seconds)
    # Perf (Bilan de Sante 2026-06-26) : LibreOffice convertit TOUT le lot en UN SEUL process
    # (`soffice ... --convert-to pdf --outdir <dir> doc1 doc2 ... docN`) -> 1 cold-start (~2-4 s)
    # au lieu de N. Word COM ne supporte pas le batch -> on garde la boucle unitaire (backend deja
    # resolu, donc pas de re-sonde). Le batch n'est emprunte que si une cible de sortie est fournie.
    if resolved_backend.name == "libreoffice" and output_dir is not None:
        return _export_batch_with_libreoffice(
            docx_list,
            output_dir,
            resolved_backend.executable,
            timeout_seconds=timeout_seconds,
            overwrite=overwrite,
        )
    for source_path in docx_list:
        target_path = (
            output_dir / source_path.with_suffix(PDF_EXTENSION).name
            if output_dir is not None
            else None
        )
        results.append(
            export_docx_to_pdf(
                source_path,
                target_path,
                backend=backend,
                overwrite=overwrite,
                timeout_seconds=timeout_seconds,
                _resolved_backend=resolved_backend,
            )
        )
    return results


def is_pdf_export_available(backend: PdfBackendName = "auto") -> bool:
    try:
        _resolve_backend(backend, timeout_seconds=20)
    except PdfExporterUnavailableError:
        return False
    return True


def _validate_source_docx(docx_path: Path) -> Path:
    source_path = Path(docx_path)
    if source_path.suffix.lower() != DOCX_EXTENSION:
        raise PdfExportFailedError(f"Le fichier source n'est pas un DOCX : {source_path}")
    if not source_path.is_file():
        raise PdfExportFailedError(f"Le fichier DOCX source est introuvable : {source_path}")
    return source_path.resolve(strict=True)


def _resolve_pdf_path(source_path: Path, pdf_path: Path | None) -> Path:
    target_path = source_path.with_suffix(PDF_EXTENSION) if pdf_path is None else Path(pdf_path)
    if target_path.suffix.lower() != PDF_EXTENSION:
        raise PdfExportFailedError(f"Le fichier cible n'est pas un PDF : {target_path}")
    return target_path.resolve(strict=False)


def _resolve_backend(
    backend: PdfBackendName,
    *,
    timeout_seconds: int,
) -> _ResolvedBackend:
    libreoffice_path = _find_libreoffice_executable()
    if backend in {"auto", "libreoffice"} and libreoffice_path is not None:
        return _ResolvedBackend(name="libreoffice", executable=libreoffice_path)
    if backend == "libreoffice":
        raise PdfExporterUnavailableError(
            "LibreOffice headless est indisponible. Installez LibreOffice ou configurez "
            f"{LIBREOFFICE_ENV_VAR}."
        )

    powershell_path = _find_powershell_executable()
    if backend in {"auto", "word"} and powershell_path is not None:
        if _word_com_is_available(powershell_path, timeout_seconds=timeout_seconds):
            return _ResolvedBackend(name="word-com", executable=powershell_path)
    if backend == "word":
        raise PdfExporterUnavailableError(
            "Microsoft Word COM est indisponible sur cette machine."
        )

    raise PdfExporterUnavailableError(
        "Aucun backend PDF local fiable n'est disponible : LibreOffice headless introuvable "
        "et Microsoft Word COM indisponible."
    )


def _find_libreoffice_executable() -> Path | None:
    configured_path = os.environ.get(LIBREOFFICE_ENV_VAR)
    if configured_path:
        path = Path(configured_path)
        if path.is_file():
            return path

    for command in ("soffice", "libreoffice"):
        executable = shutil.which(command)
        if executable:
            return Path(executable)

    for candidate in _libreoffice_windows_candidates():
        if candidate.is_file():
            return candidate
    return None


def _libreoffice_windows_candidates() -> tuple[Path, ...]:
    return (
        Path("C:/Program Files/LibreOffice/program/soffice.exe"),
        Path("C:/Program Files (x86)/LibreOffice/program/soffice.exe"),
    )


def _find_powershell_executable() -> Path | None:
    if os.name != "nt":
        return None
    executable = shutil.which("powershell")
    if executable:
        return Path(executable)
    fallback = Path("C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe")
    if fallback.is_file():
        return fallback
    return None


def _word_com_is_available(powershell_path: Path, *, timeout_seconds: int) -> bool:
    command = [
        str(powershell_path),
        "-NoProfile",
        "-NonInteractive",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        (
            "$word = $null; "
            "try { "
            "$word = New-Object -ComObject Word.Application; "
            "$word.Visible = $false; "
            "exit 0 "
            "} catch { exit 1 } "
            "finally { if ($word -ne $null) { $word.Quit() | Out-Null } }"
        ),
    ]
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
            timeout=timeout_seconds,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return completed.returncode == 0


def _export_with_libreoffice(
    source_path: Path,
    target_path: Path,
    executable: Path,
    timeout_seconds: int,
) -> None:
    with tempfile.TemporaryDirectory(prefix="sydel_pdf_export_") as temporary_dir:
        temporary_path = Path(temporary_dir)
        command = [
            str(executable),
            "--headless",
            "--nologo",
            "--nodefault",
            "--nofirststartwizard",
            "--nolockcheck",
            "--convert-to",
            "pdf",
            "--outdir",
            str(temporary_path),
            str(source_path),
        ]
        completed = _run_conversion_process(command, timeout_seconds, "LibreOffice")
        if completed.returncode != 0:
            raise PdfExportFailedError(_format_process_failure("LibreOffice", completed))

        converted_path = temporary_path / source_path.with_suffix(PDF_EXTENSION).name
        if not converted_path.is_file():
            process_output = (
                f"{completed.stdout.strip()} {completed.stderr.strip()}".strip()
                or "aucun detail de sortie"
            )
            raise PdfExportFailedError(
                "LibreOffice n'a pas produit le PDF attendu : "
                f"{converted_path}. Sortie : {process_output}"
            )
        shutil.move(str(converted_path), str(target_path))


def _export_batch_with_libreoffice(
    source_paths: list[Path],
    output_dir: Path,
    executable: Path,
    *,
    timeout_seconds: int,
    overwrite: bool,
) -> list[PdfExportResult]:
    """Convertit TOUT le lot en UN SEUL appel LibreOffice (1 cold-start au lieu de N).

    `soffice ... --convert-to pdf --outdir <output_dir> doc1.docx doc2.docx … docN.docx` produit
    `output_dir/docK.pdf` (meme basename) -> pas de repertoire temporaire ni de move par document.
    Le timeout est augmente proportionnellement au nombre de documents (1 process, N conversions).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    validated = [_validate_source_docx(p) for p in source_paths]
    targets = [output_dir / p.with_suffix(PDF_EXTENSION).name for p in validated]
    for target in targets:
        if target.exists():
            if not overwrite:
                raise PdfExportFailedError(f"Le PDF cible existe deja : {target}")
            target.unlink()
    command = [
        str(executable),
        "--headless",
        "--nologo",
        "--nodefault",
        "--nofirststartwizard",
        "--nolockcheck",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_dir.resolve()),
        *[str(p) for p in validated],
    ]
    batch_timeout = timeout_seconds + 5 * max(0, len(validated) - 1)
    completed = _run_conversion_process(command, batch_timeout, "LibreOffice")
    if completed.returncode != 0:
        raise PdfExportFailedError(_format_process_failure("LibreOffice", completed))
    results: list[PdfExportResult] = []
    for source, target in zip(validated, targets, strict=True):
        _ensure_pdf_created(target, "libreoffice")
        results.append(
            PdfExportResult(source_docx=source, pdf_path=target, backend="libreoffice")
        )
    return results


def _export_with_word_com(
    source_path: Path,
    target_path: Path,
    powershell_path: Path,
    timeout_seconds: int,
) -> None:
    script_path = _write_word_export_script()
    try:
        command = [
            str(powershell_path),
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script_path),
            str(source_path),
            str(target_path),
            str(WORD_PDF_FORMAT),
        ]
        completed = _run_conversion_process(command, timeout_seconds, "Microsoft Word COM")
        if completed.returncode != 0:
            raise PdfExportFailedError(_format_process_failure("Microsoft Word COM", completed))
    finally:
        script_path.unlink(missing_ok=True)


def _write_word_export_script() -> Path:
    script = """
param(
    [Parameter(Mandatory=$true)][string]$SourcePath,
    [Parameter(Mandatory=$true)][string]$TargetPath,
    [Parameter(Mandatory=$true)][int]$PdfFormat
)
$ErrorActionPreference = 'Stop'
$word = $null
$document = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $document = $word.Documents.Open($SourcePath, $false, $true)
    $document.ExportAsFixedFormat($TargetPath, $PdfFormat)
} finally {
    if ($document -ne $null) {
        $document.Close($false) | Out-Null
    }
    if ($word -ne $null) {
        $word.Quit() | Out-Null
    }
}
if (-not (Test-Path -LiteralPath $TargetPath)) {
    throw "PDF target was not created: $TargetPath"
}
"""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".ps1",
        prefix="sydel_word_pdf_export_",
        encoding="utf-8",
        delete=False,
    ) as script_file:
        script_file.write(script)
        return Path(script_file.name)


def _ensure_pdf_created(target_path: Path, backend_name: str) -> None:
    if not target_path.is_file():
        raise PdfExportFailedError(f"{backend_name} n'a pas produit le PDF cible : {target_path}")
    if target_path.stat().st_size <= 0:
        raise PdfExportFailedError(f"{backend_name} a produit un PDF vide : {target_path}")


def _run_conversion_process(
    command: list[str],
    timeout_seconds: int,
    backend_name: str,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise PdfExportFailedError(
            f"{backend_name} a depasse le delai de conversion de {timeout_seconds} secondes."
        ) from exc
    except OSError as exc:
        raise PdfExportFailedError(f"{backend_name} n'a pas pu etre lance : {exc}") from exc


def _format_process_failure(
    backend_name: str,
    completed: subprocess.CompletedProcess[str],
) -> str:
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    details = " ".join(part for part in (stdout, stderr) if part)
    if not details:
        details = "aucun detail de sortie"
    return f"{backend_name} a echoue avec le code {completed.returncode} : {details}"
