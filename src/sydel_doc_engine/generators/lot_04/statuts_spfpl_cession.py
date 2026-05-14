from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_spfpl_common import (
    DOCUMENT_CODE,
    OPERATION_CESSION,
    SPFPL_CESSION_STRUCTURE,
    company_siege_display,
    founder_common_replacements,
    render_statuts_docx,
    required_actionnaire_unique,
    required_capital_souscription,
    required_societe_spfpl,
    required_text,
    validate_common_statuts_context,
)
from sydel_doc_engine.generators.lot_04.statuts_spfpl_templates import (
    STATUTS_SPFPL_CESSION_BLOCKS,
)

OUTPUT_FILENAME = "statuts_spfpl_cession.docx"


class StatutsSpfplCessionGenerator:
    """Generateur from-scratch des statuts SPFPL cession V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_common_statuts_context(
            ctx,
            structure=SPFPL_CESSION_STRUCTURE,
            operation=OPERATION_CESSION,
        )
        societe_spfpl = required_societe_spfpl(ctx)
        founder = required_actionnaire_unique(ctx)
        capital_souscription = required_capital_souscription(ctx)

        if ctx.apport is None:
            raise ValueError(f"apport est obligatoire pour {DOCUMENT_CODE}.")
        if ctx.depot_fonds is None or ctx.depot_fonds.banque is None:
            raise ValueError(f"depot_fonds.banque est obligatoire pour {DOCUMENT_CODE}.")
        if ctx.exercice_social is None:
            raise ValueError(f"exercice_social est obligatoire pour {DOCUMENT_CODE}.")
        if founder.conjoint is None:
            raise ValueError(f"actionnaire_unique.conjoint est obligatoire pour {DOCUMENT_CODE}.")

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
                "[capital_lettres]": required_text(
                    societe_spfpl.capital_social_lettres,
                    "societe_spfpl.capital_social_lettres",
                ),
                "[adresse_siege]": company_siege_display(societe_spfpl, "societe_spfpl"),
                "[regime_matrimonial]": required_text(
                    founder.regime_matrimonial,
                    "actionnaire_unique.regime_matrimonial",
                ),
                "[civilite_conjoint]": required_text(
                    founder.conjoint.civilite_affichage,
                    "actionnaire_unique.conjoint.civilite_affichage",
                ),
                "[prenom_conjoint]": required_text(
                    founder.conjoint.prenom,
                    "actionnaire_unique.conjoint.prenom",
                ),
                "[nom_conjoint]": required_text(
                    founder.conjoint.nom,
                    "actionnaire_unique.conjoint.nom",
                ),
                "[ordre_departemental]": required_text(
                    founder.ordre.departement if founder.ordre else None,
                    "actionnaire_unique.ordre.departement",
                ),
                "[montant_apport]": required_text(ctx.apport.montant, "apport.montant"),
                "[montant_apport_lettres]": required_text(
                    ctx.apport.montant_lettres,
                    "apport.montant_lettres",
                ),
                "[nom_banque]": required_text(
                    ctx.depot_fonds.banque.nom,
                    "depot_fonds.banque.nom",
                ),
                "[adresse_banque]": required_text(
                    ctx.depot_fonds.banque.adresse_affichee,
                    "depot_fonds.banque.adresse_affichee",
                ),
                "[nb_actions]": str(
                    required_text(
                        str(capital_souscription.nb_actions_total)
                        if capital_souscription.nb_actions_total is not None
                        else None,
                        "capital_souscription.nb_actions_total",
                    )
                ),
                "[valeur_nominale_action]": required_text(
                    capital_souscription.valeur_nominale_action
                    or societe_spfpl.valeur_nominale_action,
                    "capital_souscription.valeur_nominale_action",
                ),
                "[valeur_nominale_action_lettres]": required_text(
                    societe_spfpl.valeur_nominale_action_lettres,
                    "societe_spfpl.valeur_nominale_action_lettres",
                ),
                "[debut_exercice]": required_text(
                    ctx.exercice_social.debut,
                    "exercice_social.debut",
                ),
                "[fin_exercice]": required_text(
                    ctx.exercice_social.fin,
                    "exercice_social.fin",
                ),
                "[date_cloture_exercice_1]": required_text(
                    ctx.exercice_social.date_cloture_premier_exercice,
                    "exercice_social.date_cloture_premier_exercice",
                ),
                "[lieu_signature]": required_text(ctx.signature.lieu, "signature.lieu"),
            }
        )

        return render_statuts_docx(
            STATUTS_SPFPL_CESSION_BLOCKS,
            replacements,
            output_dir / OUTPUT_FILENAME,
        )
