from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_civils_common import (
    SCI_IRIS_TEMPLATE,
    generate_statuts_civil_docx,
)


class StatutsSciIrisGenerator:
    """Generateur from-scratch des statuts SCI IRIS civils V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        return generate_statuts_civil_docx(ctx, output_dir, SCI_IRIS_TEMPLATE)
