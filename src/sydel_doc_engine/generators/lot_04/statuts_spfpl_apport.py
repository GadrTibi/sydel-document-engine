from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    statuts_output_filename,
)
from sydel_doc_engine.generators.lot_04.statuts_spfpl_common import (
    DOCUMENT_CODE,
    OPERATION_APPORT,
    SPFPL_APPORT_STRUCTURE,
    company_siege_display,
    format_display_date,
    founder_common_replacements,
    groupe_milliers,
    montant_en_lettres,
    quantite_titres,
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
from sydel_doc_engine.utils.grammar import elision_de, montant_lettres_avec_unite

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

        # 7.5 : figure de la valeur nominale (chiffres) reutilisee pour l'accord euro(s).
        valeur_nominale_figure = required_text(
            capital_souscription.valeur_nominale_action
            or apport_titres.valeur_nominale_action,
            "capital_souscription.valeur_nominale_action",
        )

        replacements = founder_common_replacements(founder, "actionnaire_unique")
        replacements.update(
            {
                "[denomination_societe]": required_text(
                    societe_spfpl.denomination,
                    "societe_spfpl.denomination",
                ),
                # Albane 2026-07-07 (fix 3) : en-tete « au capital de 60 000 euros » — montant
                # toujours GROUPE.
                "[capital_social]": groupe_milliers(
                    required_text(
                        societe_spfpl.capital_social,
                        "societe_spfpl.capital_social",
                    )
                ),
                "[adresse_siege]": company_siege_display(societe_spfpl, "societe_spfpl"),
                "[adresse_siege_societe_cible]": company_siege_display(
                    societe_cible,
                    "societe_cible",
                ),
                # Albane 2026-07-07 (fix 6 / R4) : « simplifiée(s) » ACCENTUE — orthographe
                # irreprochable, prime sur la typo « simplifiee » du verbatim source/front
                # (valeur injectee par spfpl_slice). Couvre « par actions simplifiee régie »,
                # « aux sociétés par actions simplifiee » et « [forme_sociale]s » (denomination).
                "[forme_sociale]": _forme_sociale_accentuee(
                    required_text(
                        societe_spfpl.forme_sociale,
                        "societe_spfpl.forme_sociale",
                    )
                ),
                "[profession_reglementee]": required_text(
                    founder.profession_reglementee,
                    "actionnaire_unique.profession_reglementee",
                ),
                "[ville_ordre]": required_text(
                    founder.ordre.ville if founder.ordre else None,
                    "actionnaire_unique.ordre.ville",
                ),
                # KAN-2 / B3 : nb de parts apportees non saisi -> marqueur, jamais « 0 » affirme.
                "[nb_parts_apportees]": quantite_titres(
                    apport_titres.nb_parts,
                    "nombre de parts apportées",
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
                # Albane 2026-07-07 (fixes 1+3+4, propagation) : montant en chiffres GROUPE
                # (« 60 000 € » art. 6, « (60 000) euros » art. 8) ; art. 8 en LETTRES puis
                # (chiffres) — lettres du front (`valeur_globale_lettres`) avec repli calcule
                # depuis la figure, cle combinee « de [...] » via elision_de (R6).
                "[montant_apports_nature]": groupe_milliers(
                    required_text(
                        apport_titres.valeur_globale,
                        "apport_titres.valeur_globale",
                    )
                ),
                "de [montant_apports_nature_lettres]": elision_de(
                    montant_en_lettres(
                        apport_titres.valeur_globale_lettres,
                        required_text(
                            apport_titres.valeur_globale,
                            "apport_titres.valeur_globale",
                        ),
                    )
                ),
                # KAN-2 / B1 : nb d'actions non saisi -> marqueur, jamais « 600 » ni « 0 ».
                "[nb_actions]": quantite_titres(
                    capital_souscription.nb_actions_total,
                    "nombre d'actions composant le capital",
                ),
                "[valeur_nominale_part]": valeur_nominale_figure,
                # 7.5 : lettres + unite composees en un seul token (anti double-euro / espace).
                # ENTIER -> « cent euros » (byte-identique) ; DECIMAL -> « un centime d'euro ».
                # Albane 2026-07-07 (fix 2 / R6) : cle combinee « de [...] » via elision_de ->
                # « d'un euro » / « d'un centime d'euro » (jamais « de un ») ; « de cent euros »
                # reste inchange.
                "de [valeur_nominale_part_avec_unite]": elision_de(
                    montant_lettres_avec_unite(
                        required_text(
                            apport_titres.valeur_nominale_action_lettres,
                            "apport_titres.valeur_nominale_action_lettres",
                        ),
                        valeur_nominale_figure,
                    )
                ),
                "[fin_exercice]": required_text(
                    ctx.exercice_social.date_cloture_premier_exercice,
                    "exercice_social.date_cloture_premier_exercice",
                ),
                "[lieu_signature]": required_text(ctx.signature.lieu, "signature.lieu"),
                "[date_signature]": format_display_date(ctx.signature.date, "signature.date"),
            }
        )

        # Retour Rafael 2026-07-07 : TOUS les statuts sont nommes
        # « Statuts <denomination>.docx » (helper partage, fallback historique si vide).
        return render_statuts_docx(
            _apport_blocks_with_contextual_siege(),
            replacements,
            output_dir
            / statuts_output_filename(societe_spfpl.denomination, OUTPUT_FILENAME),
        )


def _forme_sociale_accentuee(forme_sociale: str) -> str:
    """« par actions simplifiee » -> « par actions simplifiée » (Albane 2026-07-07, fix 6 / R4).

    Orthographe irreprochable : l'accent prime sur la typo du verbatim source (le modele
    apport tokenise portait « simplifiee » via la valeur front, `spfpl_slice.py`). Correction
    au POINT D'INJECTION du chemin statuts SPFPL uniquement — la meme valeur front alimente
    aussi des documents lot_05 (contrat d'apport, attestation commissaire), hors perimetre ici."""
    return forme_sociale.replace("simplifiee", "simplifiée").replace(
        "Simplifiee", "Simplifiée"
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
