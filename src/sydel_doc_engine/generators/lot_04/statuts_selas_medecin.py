from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    DOCUMENT_CODE,
    OVERLAY_SELAS_MEDECIN,
    STRUCTURE_SELAS,
    add_conjoint_replacements,
    add_depot_replacements,
    add_exercice_replacements,
    add_ordre_replacements,
    common_replacements,
    render_statuts_sel_docx,
    required_associe_unique,
    required_company,
    required_text,
    validate_sel_context,
    validate_selas_second_lieu,
)
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_templates import (
    STATUTS_SELAS_MEDECIN_BLOCKS,
)

OUTPUT_FILENAME = "statuts_selas_medecin.docx"


class StatutsSelasMedecinGenerator:
    """Generateur from-scratch des statuts SELAS medecin V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_sel_context(
            ctx,
            expected_structure=STRUCTURE_SELAS,
            expected_overlay=OVERLAY_SELAS_MEDECIN,
        )
        associate = required_associe_unique(ctx)
        second_lieu_enabled = validate_selas_second_lieu(ctx)
        replacements = common_replacements(ctx, title_type="actions")
        add_conjoint_replacements(replacements, associate)
        add_ordre_replacements(replacements, associate)
        add_depot_replacements(replacements, ctx, require_address=True)
        add_exercice_replacements(
            replacements,
            ctx,
            require_debut_fin=True,
            require_lieu=True,
        )
        if ctx.dirigeant_nomine is None:
            raise ValueError(f"dirigeant_nomine est obligatoire pour {DOCUMENT_CODE}.")
        company = required_company(ctx)
        if ctx.capital is None:
            raise ValueError(f"capital est obligatoire pour {DOCUMENT_CODE}.")
        replacements.update(
            {
                "[forme_sociale]": required_text(
                    company.forme_sociale or company.forme_sociale_affichage,
                    "societe.forme_sociale",
                ),
                "[forme_sociale_abregee]": required_text(
                    company.forme_sociale_abregee,
                    "societe.forme_sociale_abregee",
                ),
                "[duree_societe]": required_text(company.duree, "societe.duree"),
                "[nb_actions_lettres]": required_text(
                    ctx.capital.nombre_titres_total_lettres,
                    "capital.nombre_titres_total_lettres",
                ),
                "[valeur_nominale_action_lettres]": required_text(
                    ctx.capital.valeur_nominale_titre_lettres,
                    "capital.valeur_nominale_titre_lettres",
                ),
                "[titre_professionnel]": required_text(
                    associate.titre_professionnel or associate.civilite_affichage,
                    "associes[0].titre_professionnel",
                ),
                "[qualification_principale]": required_text(
                    associate.qualification_principale,
                    "associes[0].qualification_principale",
                ),
                "[qualite_associe]": required_text(
                    associate.qualite,
                    "associes[0].qualite",
                ),
                "[fonction_dirigeant]": required_text(
                    ctx.dirigeant_nomine.fonction_affichage,
                    "dirigeant_nomine.fonction_affichage",
                ),
                "[duree_mandat_dirigeant]": required_text(
                    ctx.dirigeant_nomine.duree_mandat,
                    "dirigeant_nomine.duree_mandat",
                ),
                "[prestataire_signature_electronique]": required_text(
                    ctx.signature.prestataire_signature_electronique,
                    "signature.prestataire_signature_electronique",
                ),
            }
        )
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
            STATUTS_SELAS_MEDECIN_BLOCKS,
            replacements,
            output_dir / OUTPUT_FILENAME,
            associate=associate,
            render_selas_second_lieu=second_lieu_enabled,
        )
