from __future__ import annotations

import re
from pathlib import Path

from sydel_doc_engine.domain.models import Associe, DocumentGenerationContext
from sydel_doc_engine.generators.lot_04.statuts_sel_exercice_common import (
    DOCUMENT_CODE,
    OVERLAY_SELAS_MEDECIN,
    STRUCTURE_SELAS,
    add_conjoint_replacements,
    add_depot_replacements,
    add_exercice_replacements,
    add_ordre_replacements,
    common_replacements,
    qualite_associe_display,
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
from sydel_doc_engine.utils.grammar import elision_de, montant_lettres_avec_unite

OUTPUT_FILENAME = "statuts_selas_medecin.docx"


def _duree_en_annees(value: str | None) -> str:
    """Akainu M1/M2 (2026-06-25) : le template porte deja « [duree_societe] années » -> le slot
    attend le NOMBRE seul. Les slices SEL d'exercice passent « 99 ans » (defaut SELARL/SELAS) ; on
    retire un suffixe d'unite eventuel pour eviter le doublon « 99 ans années ». « 99 » et
    « 99 ans » rendent donc tous deux « fixée à 99 années »."""
    text = required_text(value, "societe.duree")
    stripped = re.sub(
        r"\s+(ans|an|années|année|annees|annee)\.?\s*$", "", text, flags=re.IGNORECASE
    ).strip()
    return stripped or text

# Voyelles + « h » muet déclenchant l'élision « de l' » (au lieu de « du »)
# devant le nom de l'Ordre dans la ligne d'identité SELAS mono. Le modèle source
# SELAS porte « inscrit au Tableau du [ordre_professionnel] » : avec un nom
# d'ordre commençant par une voyelle (« Ordre des médecins »...), « du Ordre »
# est agrammatical. On corrige UNIQUEMENT l'élision, sans toucher au wording du
# nom de l'Ordre lui-même (fidélité au libellé saisi par l'opérateur).
_ELISION_INITIALS = set("aàâäeéèêëiîïoôöuùûüyhAÀÂÄEÉÈÊËIÎÏOÔÖUÙÛÜYH")


def _ordre_professionnel_inscription(associate: Associe) -> str:
    """Connecteur « du / de l' » + nom de l'Ordre, avec élision correcte.

    Le bloc source SELAS dit « inscrit au Tableau [token] ». Le token rend
    « de l'Ordre des médecins » (élision devant voyelle/h muet) ou « du Conseil… »
    (consonne), pour ne plus produire « du Ordre ». Le nom de l'Ordre provient de
    `associes[0].ordre.professionnel` (saisie opérateur) et n'est jamais réécrit.
    """
    if associate.ordre is None:
        raise ValueError(f"associes[0].ordre est obligatoire pour {DOCUMENT_CODE}.")
    nom_ordre = required_text(
        associate.ordre.professionnel,
        "associes[0].ordre.professionnel",
    )
    first_char = nom_ordre[0]
    if first_char in _ELISION_INITIALS:
        return f"de l’{nom_ordre}"
    return f"du {nom_ordre}"


def _profession_qualification_segment(associate: Associe) -> str:
    """Segment « profession reglementee + qualification » de la comparution SELAS medecin.

    Retour Albane « mise en forme » 2.1 : la comparution rendait « [profession_reglementee]
    [qualification_principale] », d'ou « medecin medecin » quand la qualification saisie
    est identique a la profession reglementee. On dedoublonne A LA RACINE : si les deux
    valeurs sont equivalentes (comparaison insensible a la casse/aux espaces), on n'emet
    QU'UNE fois le mot ; sinon, on garde la juxtaposition (« medecin cardiologue »), qui
    reste une donnee saisie volontairement. Aucun wording juridique invente.
    """
    profession = required_text(
        associate.profession_reglementee, "associes[0].profession_reglementee"
    )
    qualification = required_text(
        associate.qualification_principale, "associes[0].qualification_principale"
    )
    if profession.strip().casefold() == qualification.strip().casefold():
        return profession
    return f"{profession} {qualification}"


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
        replacements["[inscription_ordre_professionnel]"] = _ordre_professionnel_inscription(
            associate
        )
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
                "[duree_societe]": _duree_en_annees(company.duree),
                "[nb_actions_lettres]": required_text(
                    ctx.capital.nombre_titres_total_lettres,
                    "capital.nombre_titres_total_lettres",
                ),
                # Akainu B1 (regle 68) : le modele art.8 colle « d’[valeur…] » -> elision via
                # le helper partage (« de cent euros », « d’un euro »). Cle combinee traitee en
                # premier (replace_placeholders trie par longueur desc). 7.5 (Albane 2026-07-06) :
                # token unique lettres+unite ; DECIMAL -> « d’un centime d’euro » /
                # « de cinquante centimes d’euro » (elision correcte sur la phrase complete).
                "d’[valeur_nominale_action_avec_unite]": elision_de(
                    montant_lettres_avec_unite(
                        required_text(
                            ctx.capital.valeur_nominale_titre_lettres,
                            "capital.valeur_nominale_titre_lettres",
                        ),
                        ctx.capital.valeur_nominale_titre,
                    )
                ),
                "[valeur_nominale_action_avec_unite]": montant_lettres_avec_unite(
                    required_text(
                        ctx.capital.valeur_nominale_titre_lettres,
                        "capital.valeur_nominale_titre_lettres",
                    ),
                    ctx.capital.valeur_nominale_titre,
                ),
                "[titre_professionnel]": required_text(
                    associate.titre_professionnel or associate.civilite_affichage,
                    "associes[0].titre_professionnel",
                ),
                "[qualification_principale]": required_text(
                    associate.qualification_principale,
                    "associes[0].qualification_principale",
                ),
                # Retour Albane « mise en forme » 2.1 : la comparution juxtapose
                # « [profession_reglementee] [qualification_principale] ». Quand la
                # qualification saisie est IDENTIQUE a la profession reglementee (ex.
                # « medecin » / « medecin »), le rendu doublait le mot (« medecin
                # medecin »). On dedoublonne A LA RACINE via une cle COMBINEE
                # (traitee avant les tokens nus, tri par longueur desc de
                # replace_placeholders) : profession == qualification -> un seul mot ;
                # qualification distincte -> juxtaposition preservee.
                "[profession_reglementee] [qualification_principale]": (
                    _profession_qualification_segment(associate)
                ),
                # R4 (Albane 2026-07-07) : le flux pose « associe unique » BRUT ->
                # la designation rendait « L'associe unique, … ». Token route par
                # qualite_associe_display (accentue + accorde au genre).
                "[qualite_associe]": qualite_associe_display(associate),
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
            # Retours Albane « mise en forme » : mise en forme SELAS (adresse du
            # siege / designation President en gras, sous-articles soulignes) et
            # saut de page avant l'ANNEXE (2.10).
            selas_formatting=True,
            annex_page_break=True,
        )
