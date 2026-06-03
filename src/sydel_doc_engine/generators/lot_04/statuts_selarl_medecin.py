from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    DOCUMENT_CODE,
    OVERLAY_SELARL_MEDECIN,
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
    STATUTS_SELARL_MEDECIN_BLOCKS,
)

OUTPUT_FILENAME = "statuts_selarl_medecin.docx"


class StatutsSelarlMedecinGenerator:
    """Generateur from-scratch des statuts SELARL medecin V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_sel_context(
            ctx,
            expected_structure=STRUCTURE_SELARL,
            expected_overlay=OVERLAY_SELARL_MEDECIN,
        )
        associate = required_associe_unique(ctx)
        replacements = common_replacements(ctx, title_type="parts_sociales")
        add_ordre_replacements(replacements, associate)
        add_depot_replacements(replacements, ctx, require_address=True)
        add_exercice_replacements(
            replacements,
            ctx,
            require_debut_fin=False,
            require_lieu=False,
        )
        if ctx.gerance is None:
            raise ValueError(f"gerance est obligatoire pour {DOCUMENT_CODE}.")
        replacements.update(
            {
                "[seuil_achat_materiel]": required_text(
                    ctx.gerance.seuil_achat_materiel,
                    "gerance.seuil_achat_materiel",
                ),
                "[seuil_emprunt_gerance]": required_text(
                    ctx.gerance.seuil_emprunt,
                    "gerance.seuil_emprunt",
                ),
                "[nombre_exemplaires_lettres]": required_text(
                    ctx.document.nombre_exemplaires_lettres if ctx.document else None,
                    "document.nombre_exemplaires_lettres",
                ),
                "[prenom_signataire]": (
                    required_text(ctx.document.signataire.prenom, "document.signataire.prenom")
                    if ctx.document and ctx.document.signataire
                    else required_text(associate.prenom, "associes[0].prenom")
                ),
                "[nom_signataire]": (
                    required_text(ctx.document.signataire.nom, "document.signataire.nom")
                    if ctx.document and ctx.document.signataire
                    else required_text(associate.nom, "associes[0].nom")
                ),
            }
        )

        return render_statuts_sel_docx(
            STATUTS_SELARL_MEDECIN_BLOCKS,
            replacements,
            output_dir / OUTPUT_FILENAME,
            associate=associate,
            skip_personne_2_line=True,
            title_box_bordered=False,
            annex_page_break=True,
        )
