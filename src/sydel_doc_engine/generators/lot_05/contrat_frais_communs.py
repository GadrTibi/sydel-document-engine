from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_05.scm_satellites_common import (
    contrat_frais_communs_replacements,
    generate_from_template,
    validate_scm_satellite_enabled,
)
from sydel_doc_engine.generators.lot_05.scm_satellites_templates import (
    CONTRAT_FRAIS_COMMUNS_BLOCKS,
)

OUTPUT_FILENAME = "contrat_frais_communs.docx"


class ContratFraisCommunsGenerator:
    """Generateur from-scratch du contrat de frais communs SCM V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_scm_satellite_enabled(ctx, "contrat_frais_communs")
        return generate_from_template(
            ctx=ctx,
            output_dir=output_dir,
            output_filename=OUTPUT_FILENAME,
            blocks=CONTRAT_FRAIS_COMMUNS_BLOCKS,
            replacements=contrat_frais_communs_replacements(ctx),
        )
