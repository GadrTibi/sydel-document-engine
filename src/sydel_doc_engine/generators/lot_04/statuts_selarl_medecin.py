from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.front_app.field_derivations import format_grouped_numeric_value
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    DOCUMENT_CODE,
    OVERLAY_SELARL_MEDECIN,
    SELARL_MEDECIN_ARTICLE_5_BODY,
    SELARL_MEDECIN_MULTI_ZONES,
    STRUCTURE_SELARL,
    add_depot_replacements,
    add_exercice_replacements,
    add_ordre_replacements,
    common_replacements,
    first_lieu_exercice,
    render_statuts_sel_docx,
    representative_associe,
    required_text,
    sel_membres,
    statuts_output_filename,
    validate_sel_context,
    validate_selas_second_lieu,
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
        membres = sel_membres(ctx)
        associate = representative_associe(ctx)
        second_lieu_enabled = validate_selas_second_lieu(ctx)
        replacements = common_replacements(ctx, title_type="parts_sociales")
        add_ordre_replacements(replacements, associate)
        add_depot_replacements(replacements, ctx, require_address=True)
        add_exercice_replacements(
            replacements,
            ctx,
            require_debut_fin=False,
            require_lieu=False,
        )
        # 2e lieu d'exercice (ticket 2.2, ADDITIF) : on n'expose les tokens du
        # patron SELAS (lieu #1 = siege, lieu #2) QUE si un 2e lieu reel est
        # saisi. Sans 2e lieu, l'article 5 medecin garde son bloc source
        # « ...situé au [adresse_siege]... » inchangé (sortie byte-identique).
        if second_lieu_enabled and ctx.exercice_social is not None:
            second_lieu = ctx.exercice_social.lieux[1]
            replacements.update(
                {
                    "[adresse_lieu_exercice]": first_lieu_exercice(ctx),
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
        if ctx.gerance is None:
            raise ValueError(f"gerance est obligatoire pour {DOCUMENT_CODE}.")
        replacements.update(
            {
                # R5 (Albane 2026-07-07, groupement des montants) : les seuils du
                # flux arrivent NON groupés (« 5000 »/« 10000 » par défaut) -> on
                # groupe à l'affichage (« 5 000 € »/« 10 000 € ») ; une valeur non
                # numérique (« 10 000 euros ») passe inchangée.
                "[seuil_achat_materiel]": format_grouped_numeric_value(
                    required_text(
                        ctx.gerance.seuil_achat_materiel,
                        "gerance.seuil_achat_materiel",
                    )
                ),
                "[seuil_emprunt_gerance]": format_grouped_numeric_value(
                    required_text(
                        ctx.gerance.seuil_emprunt,
                        "gerance.seuil_emprunt",
                    )
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
            output_dir / statuts_output_filename(
                ctx.societe.denomination if ctx.societe else None,
                OUTPUT_FILENAME,
            ),
            associate=associate,
            skip_personne_2_line=True,
            title_box_bordered=False,
            annex_page_break=True,
            # Restaure le pied de page non vide du modele source medecin
            # (pagination PAGE + ligne « Statuts <denomination> », Roboto 8 pt).
            # Le dentiste a un footer source vide -> ne passe pas ce parametre.
            footer_medecin_denomination=replacements["[denomination_societe]"],
            membres=membres,
            multi_zones=SELARL_MEDECIN_MULTI_ZONES,
            render_selas_second_lieu=second_lieu_enabled,
            selarl_second_lieu_block=SELARL_MEDECIN_ARTICLE_5_BODY,
        )
