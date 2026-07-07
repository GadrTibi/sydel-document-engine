from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.domain.models import DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    statuts_output_filename,
)
from sydel_doc_engine.generators.lot_04.statuts_spfpl_common import (
    DOCUMENT_CODE,
    OPERATION_CESSION,
    SPFPL_CESSION_STRUCTURE,
    company_siege_display,
    founder_common_replacements,
    groupe_milliers,
    montant_euro_symbole,
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
from sydel_doc_engine.utils.grammar import elision_de, montant_lettres_avec_unite

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
                # Albane 2026-07-07 (fixes 1+3) : montant en chiffres toujours GROUPE
                # (« 60 000 », en-tete + art. 8), et art. 8 en LETTRES puis (chiffres) —
                # « soixante mille (60 000) euros ». La cle combinee « de [capital_lettres] »
                # passe par elision_de (« d'un million », « de soixante mille » inchange).
                "[capital_social]": groupe_milliers(
                    required_text(
                        societe_spfpl.capital_social,
                        "societe_spfpl.capital_social",
                    )
                ),
                "de [capital_lettres]": elision_de(
                    required_text(
                        societe_spfpl.capital_social_lettres,
                        "societe_spfpl.capital_social_lettres",
                    )
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
                # Albane 2026-07-07 (fix 4) : « Ci … 60 000 € » (groupe + symbole €), plus
                # « 60000 » nu — meme token pour la ligne « Total des apports » (propagation).
                "[montant_apport]": montant_euro_symbole(
                    required_text(ctx.apport.montant, "apport.montant")
                ),
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
                # 7.5 : lettres + unite composees en un seul token (anti double-euro / espace).
                # ENTIER -> « cent euros » (byte-identique) ; DECIMAL -> « un centime d'euro ».
                # Albane 2026-07-07 (fix 2 / R6) : cle combinee « de [...] » via elision_de ->
                # « d'un euro » / « d'un centime d'euro » (jamais « de un ») ; « de cent euros »
                # reste inchange (l'elision ne touche que l'initiale vocalique).
                "de [valeur_nominale_action_avec_unite]": elision_de(
                    montant_lettres_avec_unite(
                        required_text(
                            societe_spfpl.valeur_nominale_action_lettres,
                            "societe_spfpl.valeur_nominale_action_lettres",
                        ),
                        valeur_nominale_figure,
                    )
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

        # Retour Rafael 2026-07-07 : TOUS les statuts sont nommes
        # « Statuts <denomination>.docx » (helper partage, fallback historique si vide).
        return render_statuts_docx(
            STATUTS_SPFPL_CESSION_BLOCKS,
            replacements,
            output_dir
            / statuts_output_filename(societe_spfpl.denomination, OUTPUT_FILENAME),
        )
