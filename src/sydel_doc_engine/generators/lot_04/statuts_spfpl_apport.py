from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_spfpl_common import (
    DOCUMENT_CODE,
    OPERATION_APPORT,
    SPFPL_APPORT_STRUCTURE,
    company_siege_display,
    format_display_date,
    founder_common_replacements,
    render_statuts_docx,
    required_actionnaire_unique,
    required_apport_titres,
    required_capital_souscription,
    required_societe_cible,
    required_societe_spfpl,
    required_text,
    validate_common_statuts_context,
)
from sydel_doc_engine.generators.lot_04.statuts_spfpl_templates import (
    STATUTS_SPFPL_APPORT_BLOCKS,
)

OUTPUT_FILENAME = "statuts_spfpl_apport.docx"


class StatutsSpfplApportGenerator:
    """Generateur from-scratch des statuts SPFPL apport V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_common_statuts_context(
            ctx,
            structure=SPFPL_APPORT_STRUCTURE,
            operation=OPERATION_APPORT,
        )
        societe_spfpl = required_societe_spfpl(ctx)
        founder = required_actionnaire_unique(ctx)
        capital_souscription = required_capital_souscription(ctx)
        apport_titres = required_apport_titres(ctx)
        societe_cible = required_societe_cible(ctx)

        if ctx.commissaire_aux_apports is None:
            raise ValueError(f"commissaire_aux_apports est obligatoire pour {DOCUMENT_CODE}.")
        if ctx.exercice_social is None:
            raise ValueError(f"exercice_social est obligatoire pour {DOCUMENT_CODE}.")

        replacements = founder_common_replacements(founder, "actionnaire_unique")
        replacements.update(
            {
                "[denomination_societe]": required_text(
                    societe_spfpl.denomination,
                    "societe_spfpl.denomination",
                ),
                "[capital_social]": required_text(
                    societe_spfpl.capital_social,
                    "societe_spfpl.capital_social",
                ),
                "[adresse_siege]": company_siege_display(societe_spfpl, "societe_spfpl"),
                "[adresse_siege_societe_cible]": company_siege_display(
                    societe_cible,
                    "societe_cible",
                ),
                "[forme_sociale]": required_text(
                    societe_spfpl.forme_sociale,
                    "societe_spfpl.forme_sociale",
                ),
                "[profession_reglementee]": required_text(
                    founder.profession_reglementee,
                    "actionnaire_unique.profession_reglementee",
                ),
                "[ville_ordre]": required_text(
                    founder.ordre.ville if founder.ordre else None,
                    "actionnaire_unique.ordre.ville",
                ),
                "[nb_parts_apportees]": str(
                    required_text(
                        str(apport_titres.nb_parts)
                        if apport_titres.nb_parts is not None
                        else None,
                        "apport_titres.nb_parts",
                    )
                ),
                "[nb_parts_apportees_lettres]": required_text(
                    apport_titres.nb_parts_lettres,
                    "apport_titres.nb_parts_lettres",
                ),
                "[plage_parts_cedees]": required_text(
                    apport_titres.plage_parts,
                    "apport_titres.plage_parts",
                ),
                "[denomination_societe_cedee]": required_text(
                    societe_cible.denomination,
                    "societe_cible.denomination",
                ),
                "[ville_rcs_societe_cedee]": required_text(
                    societe_cible.ville_rcs,
                    "societe_cible.ville_rcs",
                ),
                "[numero_rcs_societe_cedee]": required_text(
                    societe_cible.numero_rcs,
                    "societe_cible.numero_rcs",
                ),
                "[montant_apports_nature]": required_text(
                    apport_titres.valeur_globale,
                    "apport_titres.valeur_globale",
                ),
                "[nb_actions]": str(
                    required_text(
                        str(capital_souscription.nb_actions_total)
                        if capital_souscription.nb_actions_total is not None
                        else None,
                        "capital_souscription.nb_actions_total",
                    )
                ),
                "[valeur_nominale_part]": required_text(
                    capital_souscription.valeur_nominale_action
                    or apport_titres.valeur_nominale_action,
                    "capital_souscription.valeur_nominale_action",
                ),
                "[valeur_nominale_part_lettres]": required_text(
                    apport_titres.valeur_nominale_action_lettres,
                    "apport_titres.valeur_nominale_action_lettres",
                ),
                "[fin_exercice]": required_text(
                    ctx.exercice_social.date_cloture_premier_exercice,
                    "exercice_social.date_cloture_premier_exercice",
                ),
                "[lieu_signature]": required_text(ctx.signature.lieu, "signature.lieu"),
                "[date_signature]": format_display_date(ctx.signature.date, "signature.date"),
            }
        )

        return render_statuts_docx(
            _apport_blocks_with_contextual_siege(),
            replacements,
            output_dir / OUTPUT_FILENAME,
        )


def _apport_blocks_with_contextual_siege() -> tuple[str, ...]:
    return tuple(
        block.replace(
            "ayant son siège [adresse_siege]",
            "ayant son siège [adresse_siege_societe_cible]",
        )
        if "ayant son siège [adresse_siege]" in block
        else block
        for block in STATUTS_SPFPL_APPORT_BLOCKS
    )
