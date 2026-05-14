from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_03.cession_cabinets_common import (
    ACTE,
    DENTAIRE,
    CessionCabinetVariant,
    generate_cession_cabinet_docx,
)

OUTPUT_FILENAME = "acte_cession_cabinet_dentaire.docx"


class ActeCessionCabinetDentaireGenerator:
    """Generateur from-scratch de l'acte de cession d'un cabinet dentaire."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        return generate_cession_cabinet_docx(
            ctx,
            output_dir,
            CessionCabinetVariant(
                etape=ACTE,
                type_cabinet=DENTAIRE,
                output_filename=OUTPUT_FILENAME,
            ),
        )
