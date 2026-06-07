from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    OVERLAY_SELARL_DENTISTE,
    STRUCTURE_SELARL,
    add_depot_replacements,
    add_exercice_replacements,
    add_ordre_replacements,
    common_replacements,
    render_statuts_sel_docx,
    required_associe_unique,
    required_text,
    validate_sel_context,
)
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_templates import (
    STATUTS_SELARL_DENTISTE_BLOCKS,
)

OUTPUT_FILENAME = "statuts_selarl_chirurgien_dentiste.docx"


class StatutsSelarlDentisteGenerator:
    """Generateur from-scratch des statuts SELARL chirurgien-dentiste V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_sel_context(
            ctx,
            expected_structure=STRUCTURE_SELARL,
            expected_overlay=OVERLAY_SELARL_DENTISTE,
        )
        associate = required_associe_unique(ctx)
        replacements = common_replacements(
            ctx,
            title_type="parts_sociales",
        )
        add_ordre_replacements(replacements, associate)
        add_depot_replacements(replacements, ctx, require_address=False)
        add_exercice_replacements(
            replacements,
            ctx,
            require_debut_fin=True,
            require_lieu=True,
        )
        replacements.update(
            {
                # La durée SELARL dentiste est figée en dur à « 99 ans » dans le
                # template (décision Rafael 2026-06-05) : plus de token
                # [duree_societe] à remplacer côté dentiste.
                "[prestataire_signature_electronique]": required_text(
                    ctx.signature.prestataire_signature_electronique,
                    "signature.prestataire_signature_electronique",
                ),
            }
        )
        return render_statuts_sel_docx(
            STATUTS_SELARL_DENTISTE_BLOCKS,
            replacements,
            output_dir / OUTPUT_FILENAME,
            associate=associate,
            annex_page_break=True,
        )
