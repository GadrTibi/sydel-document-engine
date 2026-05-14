from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_03.cession_cabinets_common import (
    COMPROMIS,
    MEDICAL,
    CessionCabinetVariant,
    generate_cession_cabinet_docx,
)

OUTPUT_FILENAME = "compromis_cession_cabinet_medical.docx"


class CompromisCessionCabinetMedicalGenerator:
    """Generateur from-scratch du compromis de cession d'un cabinet medical."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        return generate_cession_cabinet_docx(
            ctx,
            output_dir,
            CessionCabinetVariant(
                etape=COMPROMIS,
                type_cabinet=MEDICAL,
                output_filename=OUTPUT_FILENAME,
            ),
        )
