from __future__ import annotations

from pathlib import Path
from typing import Protocol

from sydel_doc_engine.domain.models import DocumentGenerationContext


class DocumentGenerator(Protocol):
    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        ...
