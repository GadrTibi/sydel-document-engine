from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    OVERLAY_SELARL_DENTISTE,
    STRUCTURE_SELARL,
    add_conjoint_replacements,
    add_depot_replacements,
    add_exercice_replacements,
    add_ordre_replacements,
    common_replacements,
    dentiste_multi_associes_partial_blocks,
    is_selarl_dentiste_multi_associes_partial,
    render_statuts_sel_docx,
    required_associe_principal,
    required_associe_unique,
    required_company,
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
        multi_partial = is_selarl_dentiste_multi_associes_partial(ctx)
        company = required_company(ctx)
        associate = (
            required_associe_principal(ctx) if multi_partial else required_associe_unique(ctx)
        )
        replacements = common_replacements(
            ctx,
            title_type="parts_sociales",
            allow_multi_associes_partial=multi_partial,
        )
        add_conjoint_replacements(replacements, associate)
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
                "[duree_societe]": required_text(company.duree, "societe.duree"),
                "[prestataire_signature_electronique]": required_text(
                    ctx.signature.prestataire_signature_electronique,
                    "signature.prestataire_signature_electronique",
                ),
            }
        )
        blocks = (
            dentiste_multi_associes_partial_blocks(STATUTS_SELARL_DENTISTE_BLOCKS, ctx)
            if multi_partial
            else STATUTS_SELARL_DENTISTE_BLOCKS
        )
        return render_statuts_sel_docx(
            blocks,
            replacements,
            output_dir / OUTPUT_FILENAME,
            associate=associate,
        )
