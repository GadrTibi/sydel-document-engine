from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile


def create_bundle(bundle_path: Path, files: list[Path]) -> Path:
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(bundle_path, mode="w") as archive:
        for file_path in files:
            archive.write(file_path, arcname=file_path.name)
    return bundle_path
