from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    OVERLAY_SELARL_DENTISTE,
    SELARL_DENTISTE_MULTI_ZONES,
    STRUCTURE_SELARL,
    add_depot_replacements,
    add_exercice_replacements,
    add_ordre_replacements,
    common_replacements,
    render_statuts_sel_docx,
    representative_associe,
    required_text,
    sel_membres,
    statuts_output_filename,
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
        membres = sel_membres(ctx)
        associate = representative_associe(ctx)
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
            output_dir / statuts_output_filename(
                ctx.societe.denomination if ctx.societe else None,
                OUTPUT_FILENAME,
            ),
            associate=associate,
            annex_page_break=True,
            membres=membres,
            multi_zones=SELARL_DENTISTE_MULTI_ZONES,
        )
