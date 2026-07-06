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
from sydel_doc_engine.utils.departements import departement_nom
from sydel_doc_engine.utils.grammar import euro_word

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
        # Retour Rafael 2026-07-02 : le conjoint n'est PLUS obligatoire (menu complet
        # « Situation matrimoniale » — un celibataire n'a pas de conjoint). La ligne de
        # comparution matrimoniale est branchee dans `founder_common_replacements`
        # (marie -> ligne complete avec conjoint ; sinon -> juste le statut).

        # 7.5 : figure de la valeur nominale (chiffres) reutilisee pour l'accord euro(s).
        valeur_nominale_figure = required_text(
            capital_souscription.valeur_nominale_action
            or societe_spfpl.valeur_nominale_action,
            "capital_souscription.valeur_nominale_action",
        )

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
                # Retour Rafael 2026-07-02 : les tokens [regime_matrimonial] /
                # [*_conjoint] de la comparution sont remplaces par [ligne_situation_maritale]
                # (branche marie/non-marie, construit dans founder_common_replacements).
                # 7.4 (Albane 2026-07-06) : l'Ordre s'affiche par le NOM du departement
                # (« de Seine-et-Marne »), plus par le numero (« de 77 »). Le champ
                # `ordre.departement` porte le numero -> `departement_nom` le convertit
                # (passthrough si deja un nom).
                "[ordre_departemental]": departement_nom(
                    required_text(
                        founder.ordre.departement if founder.ordre else None,
                        "actionnaire_unique.ordre.departement",
                    )
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
                "[valeur_nominale_action]": valeur_nominale_figure,
                "[valeur_nominale_action_lettres]": required_text(
                    societe_spfpl.valeur_nominale_action_lettres,
                    "societe_spfpl.valeur_nominale_action_lettres",
                ),
                # 7.5 : accord « euro » / « euros » sur la FIGURE de la valeur nominale.
                "[euro_nominal_word]": euro_word(valeur_nominale_figure),
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
