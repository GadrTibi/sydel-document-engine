from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    OVERLAY_SELARL_DENTISTE,
    SELARL_DENTISTE_ARTICLE_5_BODY,
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
    validate_selas_second_lieu,
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
        second_lieu_enabled = validate_selas_second_lieu(ctx)
        replacements = common_replacements(
            ctx,
            title_type="parts_sociales",
        )
        add_ordre_replacements(replacements, associate)
        # KAN-42 (Rafael) : l'adresse de la banque doit etre reportee dans les
        # statuts SELARL dentiste (alignement sur le sibling medecin, qui l'a
        # deja). Supersede le modele source dentiste qui l'omettait.
        add_depot_replacements(replacements, ctx, require_address=True)
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
        # 2e lieu d'exercice (ticket 2.2, ADDITIF) : [adresse_lieu_exercice]
        # (= lieux[0] = le siège) est déjà posé par add_exercice_replacements
        # (require_lieu=True). On n'ajoute les tokens du 2e lieu QUE si un 2e
        # lieu réel est saisi ; sinon, l'article 5 dentiste garde son bloc source
        # « ...lieu d'exercice unique... » inchangé (sortie byte-identique).
        if second_lieu_enabled and ctx.exercice_social is not None:
            second_lieu = ctx.exercice_social.lieux[1]
            replacements.update(
                {
                    "[nom_lieu_exercice_2]": required_text(
                        second_lieu.nom,
                        "exercice_social.lieux[1].nom",
                    ),
                    "[adresse_lieu_exercice_2]": required_text(
                        second_lieu.adresse_affichee,
                        "exercice_social.lieux[1].adresse_affichee",
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
            render_selas_second_lieu=second_lieu_enabled,
            selarl_second_lieu_block=SELARL_DENTISTE_ARTICLE_5_BODY,
        )
