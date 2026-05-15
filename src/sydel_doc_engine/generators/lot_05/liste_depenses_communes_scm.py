from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_05.scm_satellites_common import (
    generate_from_template,
    liste_depenses_communes_replacements,
    validate_scm_satellite_enabled,
)
from sydel_doc_engine.generators.lot_05.scm_satellites_templates import (
    LISTE_DEPENSES_COMMUNES_SCM_BLOCKS,
)

OUTPUT_FILENAME = "liste_depenses_communes_scm.docx"


class ListeDepensesCommunesScmGenerator:
    """Generateur from-scratch de la liste des depenses communes SCM V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_scm_satellite_enabled(ctx, "liste_depenses_communes")
        return generate_from_template(
            ctx=ctx,
            output_dir=output_dir,
            output_filename=OUTPUT_FILENAME,
            blocks=LISTE_DEPENSES_COMMUNES_SCM_BLOCKS,
            replacements=liste_depenses_communes_replacements(ctx),
        )
