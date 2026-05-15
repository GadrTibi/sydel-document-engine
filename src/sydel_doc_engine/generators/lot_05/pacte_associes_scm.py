from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_05.scm_satellites_common import (
    generate_from_template,
    pacte_associes_replacements,
    validate_scm_satellite_enabled,
)
from sydel_doc_engine.generators.lot_05.scm_satellites_templates import (
    PACTE_ASSOCIES_BLOCKS,
)

OUTPUT_FILENAME = "pacte_associes_scm.docx"


class PacteAssociesScmGenerator:
    """Generateur from-scratch du pacte d'associes SCM V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_scm_satellite_enabled(ctx, "pacte_associes")
        return generate_from_template(
            ctx=ctx,
            output_dir=output_dir,
            output_filename=OUTPUT_FILENAME,
            blocks=PACTE_ASSOCIES_BLOCKS,
            replacements=pacte_associes_replacements(ctx),
        )
