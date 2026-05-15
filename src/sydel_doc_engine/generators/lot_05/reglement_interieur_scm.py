from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_05.scm_satellites_common import (
    generate_from_template,
    reglement_interieur_replacements,
    validate_scm_satellite_enabled,
)
from sydel_doc_engine.generators.lot_05.scm_satellites_templates import (
    REGLEMENT_INTERIEUR_SCM_BLOCKS,
)

OUTPUT_FILENAME = "reglement_interieur_scm.docx"


class ReglementInterieurScmGenerator:
    """Generateur from-scratch du reglement interieur SCM V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_scm_satellite_enabled(ctx, "reglement_interieur")
        return generate_from_template(
            ctx=ctx,
            output_dir=output_dir,
            output_filename=OUTPUT_FILENAME,
            blocks=REGLEMENT_INTERIEUR_SCM_BLOCKS,
            replacements=reglement_interieur_replacements(ctx),
        )
