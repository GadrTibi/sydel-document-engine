from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from unicodedata import normalize

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Associe,
    Company,
    DocumentGenerationContext,
    StatutsCivilsAssocie,
)
from sydel_doc_engine.rendering.docx_builder import (
    add_paragraph,
    add_statuts_annex_heading,
    add_statuts_article_heading,
    add_statuts_body_paragraph,
    add_statuts_hanging_list_item,
    add_statuts_signature_block,
    add_statuts_title_box,
    new_document,
)
from sydel_doc_engine.utils.grammar import apply_gender_pairs, euro_word

DOCUMENT_CODE = "CODE-STATUTS-SEL-001"
STRUCTURE_SELARL = "SELARL"
STRUCTURE_SELAS = "SELAS"
OVERLAY_SELARL_DENTISTE = "selarl_dentiste"
OVERLAY_SELARL_MEDECIN = "selarl_medecin"
OVERLAY_SELAS_MEDECIN = "selas_medecin"


def required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value.strip()


def required_int(value: int | None, field_name: str) -> int:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


def format_display_date(value: date | str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return required_text(value, field_name)


def is_sel_multi(ctx: DocumentGenerationContext) -> bool:
    """Le dossier SELARL est multi-associes ssi `statuts_sel.membres` porte >= 2 membres.

    Retours V3 2026-06-17 : sous-cas ADDITIF active explicitement par le PM (contredit
    SELARL-SCOPE-1 / Albane 05/06). Sans cette liste -> parcours mono historique."""
    return ctx.statuts_sel is not None and len(ctx.statuts_sel.membres) >= 2


def sel_membres(ctx: DocumentGenerationContext) -> list[StatutsCivilsAssocie]:
    """Liste des membres SELARL si multi (>= 2), sinon liste vide (mono)."""
    if not is_sel_multi(ctx) or ctx.statuts_sel is None:
        return []
    return list(ctx.statuts_sel.membres)


def validate_sel_context(
    ctx: DocumentGenerationContext,
    *,
    expected_structure: str,
    expected_overlay: str,
) -> None:
    if ctx.structure != expected_structure:
        raise ValueError(f"dossier.structure doit etre {expected_structure} pour {DOCUMENT_CODE}.")
    if ctx.statuts_sel is not None and ctx.statuts_sel.overlay != expected_overlay:
        raise ValueError(f"statuts_sel.overlay doit etre {expected_overlay} pour {DOCUMENT_CODE}.")
    if is_sel_multi(ctx):
        # Mode multi-associes V3 : la coherence est portee par `statuts_sel.membres`.
        # `ctx.associes` reste l'associe representatif (entete/articles statiques).
        _validate_sel_membres(ctx)
        return
    if len(ctx.associes) != 1:
        raise ValueError(
            f"les statuts SEL multi-associes requierent statuts_sel.membres pour "
            f"{DOCUMENT_CODE}."
        )
    if ctx.capital_souscription and len(ctx.capital_souscription.souscripteurs) > 1:
        raise ValueError(
            f"les statuts SEL multi-associes requierent statuts_sel.membres pour "
            f"{DOCUMENT_CODE}."
        )
    if ctx.dirigeant_nomine is not None and not _dirigeant_is_unique_associe(ctx):
        raise ValueError(
            "la signature du dirigeant non associe reste manuelle en V1 "
            f"pour {DOCUMENT_CODE}."
        )


def _validate_sel_membres(ctx: DocumentGenerationContext) -> None:
    """Coherence des membres SELARL multi : au moins un signataire physique, et la
    somme des parts des membres = nombre de parts du capital (calcul auto du nombre
    d'associes = tous les signataires, retours V3 2026-06-17)."""
    if ctx.statuts_sel is None:
        return
    membres = ctx.statuts_sel.membres
    physiques = [m for m in membres if m.type_personne != _MORALE]
    if not physiques:
        raise ValueError(
            "au moins un associe personne physique (praticien) est obligatoire pour "
            f"les statuts SELARL multi {DOCUMENT_CODE}."
        )
    if not any(m.est_signataire for m in membres):
        raise ValueError(
            f"au moins un membre signataire est obligatoire pour {DOCUMENT_CODE}."
        )
    total_parts = sum(_membre_nb_parts(m) for m in membres)
    expected = capital_titles_total(ctx)
    if total_parts != expected:
        raise ValueError(
            "la somme des parts des membres doit correspondre a "
            f"capital.nombre_titres_total pour {DOCUMENT_CODE}."
        )


def validate_selas_second_lieu(ctx: DocumentGenerationContext) -> bool:
    if ctx.exercice_social is None or len(ctx.exercice_social.lieux) < 2:
        return False
    second_lieu = ctx.exercice_social.lieux[1]
    has_name = bool(second_lieu.nom and second_lieu.nom.strip())
    has_address = bool(second_lieu.adresse_affichee and second_lieu.adresse_affichee.strip())
    if has_name != has_address:
        raise ValueError(
            "exercice_social.lieux[1].nom et adresse_affichee doivent etre fournis "
            f"ensemble pour {DOCUMENT_CODE}."
        )
    return has_name and has_address


def common_replacements(
    ctx: DocumentGenerationContext,
    *,
    title_type: str,
) -> dict[str, str]:
    company = required_company(ctx)
    associate = required_associe_unique(ctx)
    replacements = {
        "[denomination_societe]": required_text(company.denomination, "societe.denomination"),
        "[adresse_siege]": address_display(company.siege, "societe.siege"),
        "[capital_social]": capital_amount(ctx, company),
        "[capital_lettres]": capital_amount_letters(ctx, company),
        "[forme_sociale_complete]": required_text(
            company.forme_sociale_complete or company.forme_sociale_libelle_long,
            "societe.forme_sociale_complete",
        ),
        "[civilite]": required_text(
            associate.civilite_affichage,
            "associes[0].civilite_affichage",
        ),
        "[prenom]": required_text(associate.prenom, "associes[0].prenom"),
        "[nom]": required_text(associate.nom, "associes[0].nom"),
        "[PRENOM]": required_text(associate.prenom, "associes[0].prenom"),
        "[NOM]": required_text(associate.nom, "associes[0].nom"),
        "[profession]": required_text(associate.profession, "associes[0].profession"),
        "[profession_reglementee]": required_text(
            associate.profession_reglementee,
            "associes[0].profession_reglementee",
        ),
        "[profession_reglementee_pluriel]": required_text(
            associate.profession_reglementee_pluriel,
            "associes[0].profession_reglementee_pluriel",
        ),
        "[date_naissance]": format_display_date(
            associate.date_naissance,
            "associes[0].date_naissance",
        ),
        "[ville_naissance]": required_text(
            associate.ville_naissance,
            "associes[0].ville_naissance",
        ),
        "[departement_naissance]": required_text(
            associate.departement_naissance,
            "associes[0].departement_naissance",
        ),
        "[nationalite]": required_text(associate.nationalite, "associes[0].nationalite"),
        "[adresse_personnelle]": person_address_display(associate),
        "[situation_maritale]": marital_status_display(associate),
        "[situation_matrimoniale_statuts]": statuts_sel_matrimonial_clause(associate),
        "[regime_matrimonial]": matrimonial_regime_display(associate),
        "[qualite_associe_article_8]": article_8_associate_label(ctx, associate),
        "[nb_parts_total]": str(capital_titles_total(ctx)),
        "[nb_parts_total_lettres]": capital_titles_total_letters(ctx),
        "[nb_actions]": str(capital_titles_total(ctx)),
        "[valeur_nominale_part]": capital_title_value(ctx, title_type),
        "[valeur_nominale_action]": capital_title_value(ctx, title_type),
        # Accord « euro »/« euros » de la valeur nominale (1 euro vs 10 euros).
        "[euro_nominal_word]": euro_word(capital_title_value(ctx, title_type)),
        "[montant_apport]": apport_amount(ctx, associate),
        "[montant_apport_lettres]": apport_amount_letters(ctx, associate),
        "[apport_personne_1]": apport_amount(ctx, associate),
        "[apport_lettres_personne_1]": apport_amount_letters(ctx, associate),
        "[lieu_signature]": required_text(ctx.signature.lieu, "signature.lieu"),
        "[date_signature]": format_display_date(ctx.signature.date, "signature.date"),
    }
    _validate_unique_associate_capital(ctx, associate)
    return replacements


def add_conjoint_replacements(
    replacements: dict[str, str],
    associate: Associe,
) -> None:
    if associate.conjoint is None:
        raise ValueError(f"associes[0].conjoint est obligatoire pour {DOCUMENT_CODE}.")
    replacements.update(
        {
            "[civilite_conjoint]": required_text(
                associate.conjoint.civilite_affichage,
                "associes[0].conjoint.civilite_affichage",
            ),
            "[prenom_conjoint]": required_text(
                associate.conjoint.prenom,
                "associes[0].conjoint.prenom",
            ),
            "[nom_conjoint]": required_text(
                associate.conjoint.nom,
                "associes[0].conjoint.nom",
            ),
        }
    )


def marital_status_display(associate: Associe) -> str:
    value = required_text(
        associate.situation_maritale,
        "associes[0].situation_maritale",
    )
    normalized = _normalized_text(value)
    if normalized in {"marie", "mariee"}:
        return "mariée" if associate.genre == Gender.FEMININ else "marié"
    return value


def matrimonial_regime_display(associate: Associe) -> str:
    value = required_text(
        associate.regime_matrimonial,
        "associes[0].regime_matrimonial",
    )
    normalized = _normalized_text(value)
    if "communaute" in normalized and "legale" in normalized:
        return "la communauté légale"
    if "communaute" in normalized and "universelle" in normalized:
        return "la communauté universelle"
    if "communaute" in normalized:
        return "la communauté"
    if "participation" in normalized and "acquet" in normalized:
        return "la participation aux acquêts"
    for prefix in ("sous le régime de ", "sous le regime de ", "régime de ", "regime de "):
        if value.lower().startswith(prefix):
            return value[len(prefix) :].strip()
    return value


def statuts_sel_matrimonial_clause(associate: Associe) -> str:
    status = marital_status_display(associate)
    normalized_status = _normalized_text(status)
    if normalized_status not in {"marie", "mariee"}:
        return status
    conjoint = associate.conjoint
    if conjoint is None:
        raise ValueError(f"associes[0].conjoint est obligatoire pour {DOCUMENT_CODE}.")
    conjoint_label = " ".join(
        (
            required_text(
                conjoint.civilite_affichage,
                "associes[0].conjoint.civilite_affichage",
            ),
            required_text(conjoint.prenom, "associes[0].conjoint.prenom"),
            required_text(conjoint.nom, "associes[0].conjoint.nom"),
        )
    )
    return (
        f"{status} sous le régime de {statuts_sel_matrimonial_regime(associate)} "
        f"avec {conjoint_label}"
    )


def statuts_sel_matrimonial_regime(associate: Associe) -> str:
    value = required_text(
        associate.regime_matrimonial,
        "associes[0].regime_matrimonial",
    )
    normalized = _normalized_text(value)
    if "separation" in normalized and "bien" in normalized:
        return "la séparation de biens"
    if "communaute" in normalized and "universelle" in normalized:
        return "la communauté universelle"
    if "communaute" in normalized:
        return "la communauté"
    if "participation" in normalized and "acquet" in normalized:
        return "la participation aux acquêts"
    return matrimonial_regime_display(associate)


def article_8_associate_label(
    ctx: DocumentGenerationContext,
    associate: Associe,
) -> str:
    if len(ctx.associes) == 1:
        return "associée unique" if associate.genre == Gender.FEMININ else "associé unique"
    if all(other.genre == Gender.FEMININ for other in ctx.associes):
        return "associées"
    return "associés"


def _normalized_text(value: str) -> str:
    ascii_text = normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.lower().split())


def add_ordre_replacements(
    replacements: dict[str, str],
    associate: Associe,
) -> None:
    if associate.ordre is None:
        raise ValueError(f"associes[0].ordre est obligatoire pour {DOCUMENT_CODE}.")
    replacements.update(
        {
            "[numero_ordre]": required_text(
                associate.ordre.numero,
                "associes[0].ordre.numero",
            ),
            "[numero_rpps]": required_text(
                associate.ordre.numero_rpps,
                "associes[0].ordre.numero_rpps",
            ),
            "[ordre_departemental]": required_text(
                associate.ordre.departement,
                "associes[0].ordre.departement",
            ),
            "[ville_ordre]": required_text(
                associate.ordre.ville or associate.ordre.departement,
                "associes[0].ordre.ville",
            ),
            "[ordre_professionnel]": required_text(
                associate.ordre.professionnel,
                "associes[0].ordre.professionnel",
            ),
        }
    )
    # Mention d'inscription a l'ordre (retour Albane 2026-06-10, statuts DENTISTE) :
    # le numero d'inscription a l'ordre est ajoute AVANT le RPPS, mais SEULEMENT
    # si le champ est renseigne (sinon on garde le seul RPPS). Le bloc medecin
    # porte deja le numero national dans son texte source ; cette mention sert le
    # template dentiste via [mention_inscription_ordre_rpps].
    numero_inscription = (associate.ordre.numero or "").strip()
    numero_rpps = required_text(associate.ordre.numero_rpps, "associes[0].ordre.numero_rpps")
    if numero_inscription:
        replacements["[mention_inscription_ordre_rpps]"] = (
            f"sous le numéro d’inscription {numero_inscription} "
            f"et sous le numéro RPPS {numero_rpps}"
        )
    else:
        replacements["[mention_inscription_ordre_rpps]"] = f"sous le numéro RPPS {numero_rpps}"


def add_depot_replacements(
    replacements: dict[str, str],
    ctx: DocumentGenerationContext,
    *,
    require_address: bool,
) -> None:
    if ctx.depot_fonds is None or ctx.depot_fonds.banque is None:
        raise ValueError(f"depot_fonds.banque est obligatoire pour {DOCUMENT_CODE}.")
    replacements["[nom_banque]"] = required_text(
        ctx.depot_fonds.banque.nom,
        "depot_fonds.banque.nom",
    )
    if require_address:
        # Retours client 2026-06-11 (ticket 3.2) : l'adresse de la banque ne
        # bloque plus la generation — vide, elle laisse une zone a completer.
        replacements["[adresse_banque]"] = (
            ctx.depot_fonds.banque.adresse_affichee or ""
        ).strip()


def add_exercice_replacements(
    replacements: dict[str, str],
    ctx: DocumentGenerationContext,
    *,
    require_debut_fin: bool,
    require_lieu: bool,
) -> None:
    if ctx.exercice_social is None:
        raise ValueError(f"exercice_social est obligatoire pour {DOCUMENT_CODE}.")
    if require_debut_fin:
        replacements.update(
            {
                "[debut_exercice]": required_text(
                    ctx.exercice_social.debut,
                    "exercice_social.debut",
                ),
                "[fin_exercice]": required_text(
                    ctx.exercice_social.fin,
                    "exercice_social.fin",
                ),
            }
        )
    replacements["[date_cloture_exercice_1]"] = required_text(
        ctx.exercice_social.date_cloture_premier_exercice,
        "exercice_social.date_cloture_premier_exercice",
    )
    if require_lieu:
        replacements["[adresse_lieu_exercice]"] = first_lieu_exercice(ctx)


# Police du pied de page des modeles SEL : Roboto 8 pt (= sz 16 demi-points dans
# le XML source footer1/footer3.xml du modele SELARL medecin).
_FOOTER_FONT_NAME = "Roboto"
_FOOTER_FONT_SIZE_PT = 8


def _add_page_number_field(paragraph: Any) -> None:
    """Insere un champ Word `PAGE` (numerotation dynamique) dans un paragraphe.

    Reproduit la sequence de runs `fldChar begin / instrText PAGE /
    fldChar separate / fldChar end` du footer source du modele SELARL medecin.
    Le champ s'evalue a l'ouverture/impression Word (et au passage LibreOffice
    -> PDF), exactement comme dans le .docx d'origine.
    """
    run = paragraph.add_run()
    run.font.name = _FOOTER_FONT_NAME
    run.font.size = Pt(_FOOTER_FONT_SIZE_PT)

    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for element in (begin, instr, separate, end):
        run._r.append(element)


def _add_selarl_medecin_footer(docx: Any, denomination: str) -> None:
    """Restaure le pied de page du modele source SELARL medecin.

    Le modele source (`footer1.xml` / `footer3.xml`) porte DEUX paragraphes,
    Roboto 8 pt :
      1. un champ `PAGE` (pagination) aligne a droite ;
      2. la ligne « Statuts <denomination> » alignee a gauche.
    Le generateur from-scratch repartait d'un document vierge -> footer vide
    (perte de fidelite, audit _SELARL_FIDELITY_RECHECK_V1.md). On le repose ici.
    Pose uniquement pour le medecin : le modele dentiste a un footer source vide.
    """
    footer = docx.sections[0].footer
    footer.is_linked_to_previous = False

    page_paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    page_paragraph.text = ""
    page_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _add_page_number_field(page_paragraph)

    label_paragraph = footer.add_paragraph()
    label_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    label_run = label_paragraph.add_run(f"Statuts {denomination}")
    label_run.font.name = _FOOTER_FONT_NAME
    label_run.font.size = Pt(_FOOTER_FONT_SIZE_PT)


# ---------------------------------------------------------------------------
# Multi-associes SELARL (retours V3 2026-06-17) — STRICTEMENT ADDITIF.
#
# Decision de gouvernance : ce sous-cas contredit SELARL-SCOPE-1 (SELARL =
# unipersonnelle) et l'arbitrage Albane du 05/06 ; il est construit sur demande
# EXPLICITE du PM. Garde-fou DUR : a 0 ou 1 membre, RIEN de ce code ne s'active
# -> le parcours mono historique reste byte-identique (verrou ligne-par-ligne
# `test_statuts_selarl_medecin_matches_source_docx_line_by_line`).
#
# A >= 2 membres, on intercepte par CONTENU (chaines source exactes, jamais par
# index fragile) quatre fenetres dynamiques :
#   - la comparution (« LE SOUSSIGNE : » + ligne(s) d'identite) ;
#   - l'article 7 (apports) : une ligne par membre + ligne « Total des apports » ;
#   - l'article 8 (repartition du capital) : liste numerotee « 1° ... ; / 2° ... . » ;
#   - la ligne de signature (un libelle par signataire).
# Membre personne morale OU physique (reutilise le modele riche
# `StatutsCivilsAssocie`, deja employe par la SELAS multi et le repeater).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SelMultiZones:
    """Chaines source EXACTES des blocs dynamiques d'un template SELARL.

    Chaque champ est la string telle qu'elle figure dans le tuple `*_BLOCKS`
    (prouvee par extraction). A >= 2 membres, le bloc correspondant est
    intercepte et remplace par la version iteree ; tout le reste du template
    est rendu a l'identique. None = le template ne porte pas ce bloc separe."""

    soussigne_header: str
    identite_lines: tuple[str, ...]
    apport_line: str
    apport_total_line: str
    capital_attribution_line: str
    capital_total_line: str
    signature_line: str


# Ancres des blocs dynamiques — chaines EXACTES des tuples *_BLOCKS
# (statuts_sel_exercice_templates.py). Si l'une diverge du template, le mode multi
# n'intercepte plus ce bloc (rendu mono) ; les tests multi le detectent.
SELARL_MEDECIN_MULTI_ZONES = SelMultiZones(
    soussigne_header="LE SOUSSIGNE\xa0:",
    identite_lines=(
        "[civilite] [prenom] [nom], [profession], né le [date_naissance] à "
        "[ville_naissance] ([departement_naissance]), de nationalité [nationalite], "
        "demeurant [adresse_personnelle], inscrit au tableau du Conseil départemental "
        "de [ville_ordre] sous le numéro national [numero_ordre] et sous le numéro RPPS "
        "[numero_rpps], [situation_matrimoniale_statuts]. ",
    ),
    apport_line=(
        "Dr [prenom] [nom] apporte à la Société la somme de [capital_lettres] euros "
        "([capital_social] €)"
    ),
    apport_total_line="ci- [capital_social] €.",
    capital_attribution_line=(
        "Il est divisé en [nb_parts_total] parts de [valeur_nominale_part] "
        "[euro_nominal_word] chacune, entièrement souscrites et libérées dans les "
        "conditions exposées ci-dessus et attribuées en totalité au Docteur [prenom] "
        "[nom], [qualite_associe_article_8]."
    ),
    capital_total_line=(
        "Total du nombre de parts composant le capital social\xa0: "
        "……………………………………….[nb_parts_total] parts"
    ),
    signature_line="    [prenom_signataire] [nom_signataire]",
)

SELARL_DENTISTE_MULTI_ZONES = SelMultiZones(
    soussigne_header="LE SOUSSIGNE\xa0:",
    identite_lines=(
        "[civilite] [prenom] [nom], [profession], né le [date_naissance] à "
        "[ville_naissance] ([departement_naissance]), de nationalité [nationalite], "
        "demeurant [adresse_personnelle], [situation_matrimoniale_statuts]",
        "Inscrit au Tableau de l’ordre départemental des [profession_reglementee_pluriel] "
        "de [ordre_departemental] [mention_inscription_ordre_rpps]. ",
    ),
    apport_line=(
        "[civilite] [prenom] [nom] apporte à la Société la somme de [montant_apport] euros.   "
    ),
    apport_total_line="Total des apports en numéraire : ci- [montant_apport] euros.",
    capital_attribution_line=(
        "à [civilite] [prenom] [nom], [nb_parts_total_lettres] parts sociales en pleine "
        "propriété, ci \t[nb_parts_total] parts  "
    ),
    capital_total_line=(
        "Total du nombre de parts composant le capital social : "
        "………………………………………. [nb_parts_total] parts"
    ),
    signature_line="[prenom] [nom]",
)


_MORALE = "personne_morale"


def _membre_is_morale(membre: StatutsCivilsAssocie) -> bool:
    return membre.type_personne == _MORALE


def _membre_est_feminin(membre: StatutsCivilsAssocie) -> bool:
    if membre.genre is not None:
        return membre.genre == Gender.FEMININ
    civilite = (membre.civilite_affichage or "").strip().casefold().replace(".", "")
    return civilite in {"madame", "mme", "mademoiselle", "mlle"}


def _membre_person_label(membre: StatutsCivilsAssocie) -> str:
    prenoms = membre.prenoms or membre.prenom
    return (
        f"{required_text(membre.civilite_affichage, 'membres[].civilite_affichage')} "
        f"{required_text(prenoms, 'membres[].prenom')} "
        f"{required_text(membre.nom, 'membres[].nom')}"
    )


def _membre_person_address(membre: StatutsCivilsAssocie) -> str:
    if membre.adresse_personnelle_affichee:
        return membre.adresse_personnelle_affichee.strip()
    return address_display(membre.adresse_personnelle, "membres[].adresse_personnelle")


def _membre_nb_parts(membre: StatutsCivilsAssocie) -> int:
    if membre.parts is not None and membre.parts.nb is not None:
        return membre.parts.nb
    if membre.nb_actions is not None:
        return membre.nb_actions
    raise ValueError(f"membres[].parts.nb est obligatoire pour {DOCUMENT_CODE}.")


def _membre_nb_parts_lettres(membre: StatutsCivilsAssocie) -> str:
    if membre.parts is not None and membre.parts.nb_lettres:
        return membre.parts.nb_lettres.strip()
    if membre.nb_actions_lettres:
        return membre.nb_actions_lettres.strip()
    raise ValueError(f"membres[].parts.nb_lettres est obligatoire pour {DOCUMENT_CODE}.")


def _membre_apport_montant(membre: StatutsCivilsAssocie) -> str:
    if membre.apport is None or not (membre.apport.montant or "").strip():
        raise ValueError(f"membres[].apport.montant est obligatoire pour {DOCUMENT_CODE}.")
    return membre.apport.montant.strip()


def _membre_apport_lettres(membre: StatutsCivilsAssocie) -> str:
    if membre.apport is None or not (membre.apport.montant_lettres or "").strip():
        raise ValueError(
            f"membres[].apport.montant_lettres est obligatoire pour {DOCUMENT_CODE}."
        )
    return membre.apport.montant_lettres.strip()


def _membre_short_label(membre: StatutsCivilsAssocie) -> str:
    """Libelle court pour la repartition / la signature : denomination (PM) ou
    « prenom nom » (PP), repris de la mecanique SELAS multi."""
    if _membre_is_morale(membre):
        return required_text(membre.denomination, "membres[].denomination")
    prenoms = membre.prenoms or membre.prenom
    return (
        f"{required_text(prenoms, 'membres[].prenom')} "
        f"{required_text(membre.nom, 'membres[].nom')}"
    )


def _add_multi_comparution(
    docx: Any,
    membres: list[StatutsCivilsAssocie],
    replacements: dict[str, str],
) -> None:
    """Comparution multi : « LES SOUSSIGNÉS : » (pluriel) puis une ligne par membre.

    Personne physique : reprend la ligne d'identite source (civilite, profession,
    naissance, nationalite, domicile, situation matrimoniale, inscription a l'ordre).
    Personne morale : ligne d'identification societe (denomination, forme, capital,
    siege, RCS, representant) reprise de la mecanique SELAS multi.
    """
    feminin_all = all(_membre_est_feminin(m) for m in membres if not _membre_is_morale(m))
    header = "LES SOUSSIGNÉES\xa0:" if feminin_all else "LES SOUSSIGNÉS\xa0:"
    add_paragraph(docx, header)
    profession_pluriel = replacements.get("[profession_reglementee_pluriel]", "")
    for membre in membres:
        if _membre_is_morale(membre):
            add_statuts_body_paragraph(docx, _multi_morale_identite(membre))
        else:
            for line in _multi_physique_identite(membre, profession_pluriel):
                add_statuts_body_paragraph(docx, line)


def _multi_physique_identite(
    membre: StatutsCivilsAssocie,
    profession_pluriel: str,
) -> tuple[str, ...]:
    feminin = _membre_est_feminin(membre)
    ne = "née" if feminin else "né"
    inscrit = "Inscrite" if feminin else "Inscrit"
    profession = required_text(membre.profession, "membres[].profession")
    ordre_dep = required_text(membre.ordre_departemental, "membres[].ordre_departemental")
    identite = (
        f"{_membre_person_label(membre)}, {profession}, "
        f"{ne} le {format_display_date(membre.date_naissance, 'membres[].date_naissance')} "
        f"à {required_text(membre.ville_naissance, 'membres[].ville_naissance')} "
        f"({required_text(membre.departement_naissance, 'membres[].departement_naissance')}), "
        f"de nationalité {required_text(membre.nationalite, 'membres[].nationalite')}, "
        f"demeurant {_membre_person_address(membre)}, "
        f"{required_text(membre.situation_maritale, 'membres[].situation_maritale')}."
    )
    inscription = (
        f"{inscrit} au tableau de l’ordre des {profession_pluriel} de {ordre_dep} "
        f"sous le numéro national "
        f"{required_text(membre.numero_ordre, 'membres[].numero_ordre')} "
        f"et sous le numéro RPPS "
        f"{required_text(membre.numero_rpps, 'membres[].numero_rpps')}."
    )
    return (identite, inscription)


def _multi_morale_identite(membre: StatutsCivilsAssocie) -> str:
    representant = membre.representant
    if representant is None:
        raise ValueError(
            f"membres[].representant est obligatoire pour une personne morale {DOCUMENT_CODE}."
        )
    return (
        f"La {required_text(membre.denomination, 'membres[].denomination')}, "
        f"{required_text(membre.forme_juridique, 'membres[].forme_juridique')}, "
        f"au capital de {required_text(membre.capital_social, 'membres[].capital_social')} euros "
        f"dont le siège social est situé au {address_display(membre.siege, 'membres[].siege')}, "
        f"immatriculée au RCS de {required_text(membre.ville_rcs, 'membres[].ville_rcs')} "
        f"sous le numéro {required_text(membre.numero_rcs, 'membres[].numero_rcs')}, "
        "représentée par son représentant légal, "
        f"{required_text(representant.civilite_affichage, 'membres[].representant.civilite')} "
        f"{required_text(representant.prenom, 'membres[].representant.prenom')} "
        f"{required_text(representant.nom, 'membres[].representant.nom')}."
    )


def _add_multi_apports(
    docx: Any,
    membres: list[StatutsCivilsAssocie],
    zones: SelMultiZones,
    replacements: dict[str, str],
) -> None:
    """Article 7 : une ligne d'apport par membre, puis « Total des apports »."""
    for membre in membres:
        label = (
            f"La {required_text(membre.denomination, 'membres[].denomination')}"
            if _membre_is_morale(membre)
            else _membre_person_label(membre)
        )
        add_statuts_body_paragraph(
            docx,
            f"{label} apporte à la Société la somme de "
            f"{_membre_apport_montant(membre)} euros.",
        )
    total = replacements.get("[capital_social]", replacements.get("[capital_lettres]", ""))
    add_statuts_body_paragraph(
        docx,
        f"Total des apports en numéraire : ci- {total} euros.",
    )


def _add_multi_capital_attribution(
    docx: Any,
    membres: list[StatutsCivilsAssocie],
) -> None:
    """Article 8 : liste numerotee de la repartition du capital (wording ticket V3).

    Personne morale : « N° [denomination], détenant [nb] parts ».
    Personne physique : « N° [prenom] [nom], détenant [nb] parts ».
    Separateur « ; » entre membres, « . » sur le dernier (retours V3 2026-06-17).
    """
    dernier = len(membres) - 1
    for ordinal, membre in enumerate(membres, start=1):
        nb_parts = _membre_nb_parts(membre)
        ponctuation = "." if ordinal - 1 == dernier else " ;"
        add_statuts_body_paragraph(
            docx,
            f"{ordinal}° {_membre_short_label(membre)}, "
            f"détenant {nb_parts} parts{ponctuation}",
        )


# --- Article 5 SELARL : 2e lieu d'exercice (ticket 2.2, ADDITIF) --------------
# Blocs source figes de l'article 5 SELARL (corps), interceptes par CONTENU au
# rendu — meme technique que les `multi_zones`. A UN seul lieu, ces blocs sont
# rendus tels quels (sortie byte-identique a l'existant). A DEUX lieux, ils sont
# remplaces par le patron SELAS valide (en-tete + lieu #1 + nom2, adresse2).
SELARL_DENTISTE_ARTICLE_5_BODY = (
    "Le lieu d’exercice de la société est situé au [adresse_lieu_exercice]. "
    "Il constitue le lieu d’exercice unique de la société"
)
SELARL_MEDECIN_ARTICLE_5_BODY = (
    "Le lieu d’exercice de la société est situé au [adresse_siege]. "
    "Il constitue le lieu d’exercice unique de la société."
)
# Patron SELAS valide repris pour le corps de l'article 5 SELARL a 2 lieux.
# wording art.5 SELARL a 2 lieux repris du patron SELAS valide — A VALIDER Albane
SELARL_ARTICLE_5_TWO_LIEUX_HEADER = "Le lieu d’exercice de la société est situé : "
SELARL_ARTICLE_5_TWO_LIEUX_LINE_1 = "[adresse_lieu_exercice]"
SELARL_ARTICLE_5_TWO_LIEUX_LINE_2 = "[nom_lieu_exercice_2], [adresse_lieu_exercice_2]"


def _render_selarl_two_lieux_article_5(
    docx: Any, replacements: dict[str, str], associate: Associe
) -> None:
    """Rend le corps de l'article 5 SELARL avec DEUX lieux (patron SELAS).

    Reproduit la structure validee cote SELAS (en-tete + lieu #1 sur sa propre
    ligne + « nom2, adresse2 »). Appele uniquement quand un 2e lieu reel est
    saisi ; le cas 1-lieu garde le bloc source d'origine inchange.
    """
    for raw in (
        SELARL_ARTICLE_5_TWO_LIEUX_HEADER,
        SELARL_ARTICLE_5_TWO_LIEUX_LINE_1,
        SELARL_ARTICLE_5_TWO_LIEUX_LINE_2,
    ):
        text = replace_placeholders(raw, replacements)
        text = apply_gender_variants(text, associate)
        add_statuts_body_paragraph(docx, text)


def render_statuts_sel_docx(
    blocks: tuple[str, ...],
    replacements: dict[str, str],
    output_path: Path,
    *,
    associate: Associe,
    skip_personne_2_line: bool = False,
    render_selas_second_lieu: bool = False,
    title_box_bordered: bool = True,
    annex_page_break: bool = False,
    footer_medecin_denomination: str | None = None,
    membres: list[StatutsCivilsAssocie] | None = None,
    multi_zones: SelMultiZones | None = None,
    selarl_second_lieu_block: str | None = None,
) -> Path:
    # Mode multi-associes : actif UNIQUEMENT a partir de 2 membres et si le template
    # fournit ses ancres (`multi_zones`). A 0/1 membre -> parcours mono inchange.
    multi = (
        membres is not None and len(membres) >= 2 and multi_zones is not None
    )
    multi_membres: list[StatutsCivilsAssocie] = list(membres) if multi else []
    # Lignes d'identite source a SAUTER en multi (remplacees par la comparution iteree).
    skip_identite = set(multi_zones.identite_lines) if multi and multi_zones else set()

    docx = new_document()
    signature_mode = False
    for index, block in enumerate(blocks):
        if skip_personne_2_line and "[civilite_personne_2]" in block:
            continue
        if "[nom_lieu_exercice_2]" in block and not render_selas_second_lieu:
            continue
        # Article 5 SELARL a 2 lieux (ticket 2.2, ADDITIF) : si un 2e lieu est
        # saisi, le bloc source « ...lieu d'exercice unique... » est remplace par
        # le patron SELAS valide (en-tete + lieu #1 + nom2, adresse2). Sinon, le
        # bloc source est rendu tel quel (sortie 1-lieu byte-identique).
        if (
            selarl_second_lieu_block is not None
            and render_selas_second_lieu
            and block == selarl_second_lieu_block
        ):
            _render_selarl_two_lieux_article_5(docx, replacements, associate)
            continue
        if index == 4:
            add_statuts_title_box(docx, "STATUTS", bordered=title_box_bordered)

        if multi and multi_zones is not None:
            # Interception par CONTENU (chaines source exactes) des 4 fenetres dynamiques.
            if block == multi_zones.soussigne_header:
                _add_multi_comparution(docx, multi_membres, replacements)
                continue
            if block in skip_identite:
                # Deja rendue dans la comparution iteree ci-dessus.
                continue
            if block == multi_zones.apport_line:
                _add_multi_apports(docx, multi_membres, multi_zones, replacements)
                continue
            if block == multi_zones.apport_total_line:
                # Total deja emis par _add_multi_apports.
                continue
            if block == multi_zones.capital_attribution_line:
                _add_multi_capital_attribution(docx, multi_membres)
                continue
            if block == multi_zones.signature_line:
                signataires = [m for m in multi_membres if m.est_signataire]
                for membre in signataires:
                    add_statuts_signature_block(
                        docx, [_membre_short_label(membre)], bold=True
                    )
                signature_mode = True
                continue

        text = replace_placeholders(block, replacements)
        text = apply_gender_variants(text, associate)
        # Entete (denomination / forme sociale / capital / siege) centree et
        # compacte (retour Albane 2026-06-10 : centrer l'entete, reduire les
        # interlignes). Denomination (index 0) en gras.
        if index < 4:
            add_paragraph(
                docx,
                text,
                alignment=WD_ALIGN_PARAGRAPH.CENTER,
                bold=index == 0,
                space_after_pt=0,
            )
            continue
        if _is_heading(text):
            if text.startswith("ANNEXE"):
                signature_mode = False
            if text.startswith("ANNEXE"):
                if annex_page_break:
                    docx.add_page_break()
                add_statuts_annex_heading(docx, text)
            else:
                add_paragraph(docx, text, alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
        elif text.startswith("ARTICLE "):
            add_statuts_article_heading(docx, text)
        elif block == "[denomination_societe]":
            # Article 3 : nom de la societe en gras et centre (retour Albane 2026-06-10).
            add_paragraph(docx, text, alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
        elif text.startswith("Fait à ") or text.startswith("Fait a "):
            signature_mode = True
            # « Fait a » aligne a GAUCHE (retour Albane 2026-06-10).
            add_statuts_signature_block(
                docx, [text], alignment=WD_ALIGN_PARAGRAPH.LEFT
            )
        elif signature_mode and (
            "Faire précéder" in text
            or "Faire prÃ©cÃ©der" in text
            or text.startswith("«")
            or text.startswith("Â«")
        ):
            add_statuts_signature_block(docx, [], mention_lines=[text])
        elif signature_mode:
            # Nom du client (signataire) en GRAS (retour Albane 2026-06-10).
            add_statuts_signature_block(docx, [text], bold=True)
        elif text.startswith("Liste des actes"):
            # Derniere page : ligne « Liste des actes accomplis... » centree (Albane).
            add_paragraph(docx, text, alignment=WD_ALIGN_PARAGRAPH.CENTER)
        elif text.startswith("-") or text.startswith("-\t"):
            add_statuts_hanging_list_item(docx, text.lstrip("-\t "))
        else:
            add_statuts_body_paragraph(docx, text)

    full_text = "\n".join(paragraph.text for paragraph in docx.paragraphs)
    if "[" in full_text or "]" in full_text:
        raise ValueError(f"placeholder source residuel dans le rendu {DOCUMENT_CODE}.")
    if footer_medecin_denomination is not None:
        _add_selarl_medecin_footer(docx, footer_medecin_denomination)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    docx.save(output_path)
    return output_path


def replace_placeholders(text: str, replacements: dict[str, str]) -> str:
    rendered = text
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


# Paires d'accord en genre des statuts SEL, pilotees par le genre de l'associe.
# Chaque paire = (forme_masculin, forme_feminin), chaine EXACTE telle que figee
# dans les blocs sources (cf. *_BLOCKS de statuts_sel_exercice_templates.py).
# JAMAIS de regex de terminaison : uniquement ces chaines litterales ancrees.
#  - "LE SOUSSIGNE\xa0:" -> "LA SOUSSIGNEE\xa0:" : l'entete figee au masculin doit
#    s'accorder pour une associee (insecable avant les deux-points conserve).
#  - "ne le " -> "nee le " : la date de naissance dans la ligne d'identification.
# Les variantes mojibake (nÃ©) couvrent un eventuel rendu Word mal encode.
_STATUTS_GENDER_PAIRS: list[tuple[str, str]] = [
    ("LE SOUSSIGNE\xa0:", "LA SOUSSIGNÉE\xa0:"),
    (", né le ", ", née le "),
    ("né le ", "née le "),
    (", nÃ© le ", ", nÃ©e le "),
    ("nÃ© le ", "nÃ©e le "),
]


def apply_gender_variants(text: str, associate: Associe) -> str:
    """Accorde l'entete et la ligne de naissance des statuts selon l'associe.

    Remplace l'ancienne logique unidirectionnelle (masc->fem sur « né le »
    seulement) par un accord BIDIRECTIONNEL pilote par `associate.genre` via
    `grammar.apply_gender_pairs`. Pour un homme, l'entete masculine « LE
    SOUSSIGNE » et « né le » des blocs sont laissees telles quelles ; pour une
    femme, elles deviennent « LA SOUSSIGNÉE » et « née le ».
    """
    return apply_gender_pairs(text, associate.genre, _STATUTS_GENDER_PAIRS)


def required_company(ctx: DocumentGenerationContext) -> Company:
    if ctx.societe is None:
        raise ValueError(f"societe est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.societe


def required_associe_unique(ctx: DocumentGenerationContext) -> Associe:
    if len(ctx.associes) != 1:
        raise ValueError(
            f"les statuts SEL multi-associes requierent statuts_sel.membres pour "
            f"{DOCUMENT_CODE}."
        )
    return ctx.associes[0]


def representative_associe(ctx: DocumentGenerationContext) -> Associe:
    """Associe representatif pour l'entete et les articles statiques du template.

    En mode multi, `ctx.associes` porte le praticien representatif (longueur 1) et
    `statuts_sel.membres` porte la liste complete. En mono, c'est l'associe unique.
    Dans les deux cas on attend exactement un associe representatif dans `ctx.associes`."""
    return required_associe_unique(ctx)


def statuts_output_filename(denomination: str | None, fallback: str) -> str:
    """Nom de fichier des statuts = « Statuts {denomination}.docx » (retour Albane
    2026-06-10 : mettre d'office le nom dans l'intitule du doc pour eviter le
    renommage manuel). Denomination vide ou non sanitizable -> fallback historique.
    """
    name = (denomination or "").strip()
    if not name:
        return fallback
    safe = re.sub(r"[^\w .\-]+", " ", name, flags=re.UNICODE)
    safe = re.sub(r"\s+", " ", safe).strip(" .")
    return f"Statuts {safe}.docx" if safe else fallback


def address_display(address: Address | None, field_name: str) -> str:
    if address is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if address.adresse_affichee:
        return address.adresse_affichee.strip()
    return (
        f"{required_text(address.num_voie, f'{field_name}.num_voie')} "
        f"{required_text(address.voie, f'{field_name}.voie')}, "
        f"{required_text(address.cp, f'{field_name}.cp')} "
        f"{required_text(address.ville, f'{field_name}.ville')}"
    )


def person_address_display(associate: Associe) -> str:
    if associate.adresse_personnelle_affichee:
        return associate.adresse_personnelle_affichee.strip()
    return address_display(associate.adresse_personnelle, "associes[0].adresse_personnelle")


def first_lieu_exercice(ctx: DocumentGenerationContext) -> str:
    if ctx.exercice_social is None or not ctx.exercice_social.lieux:
        raise ValueError(f"exercice_social.lieux[0] est obligatoire pour {DOCUMENT_CODE}.")
    return required_text(
        ctx.exercice_social.lieux[0].adresse_affichee,
        "exercice_social.lieux[0].adresse_affichee",
    )


def capital_amount(ctx: DocumentGenerationContext, company: Company) -> str:
    return required_text(
        company.capital_social or company.capital or (ctx.capital.montant if ctx.capital else None),
        "capital.montant",
    )


def capital_amount_letters(ctx: DocumentGenerationContext, company: Company) -> str:
    return required_text(
        company.capital_social_lettres or (ctx.capital.montant_lettres if ctx.capital else None),
        "capital.montant_lettres",
    )


def capital_titles_total(ctx: DocumentGenerationContext) -> int:
    if ctx.capital is None:
        raise ValueError(f"capital est obligatoire pour {DOCUMENT_CODE}.")
    return required_int(
        ctx.capital.nombre_titres_total or ctx.capital.nb_parts_total,
        "capital.nombre_titres_total",
    )


def capital_titles_total_letters(ctx: DocumentGenerationContext) -> str:
    if ctx.capital is None:
        raise ValueError(f"capital est obligatoire pour {DOCUMENT_CODE}.")
    return required_text(
        ctx.capital.nombre_titres_total_lettres,
        "capital.nombre_titres_total_lettres",
    )


def capital_title_value(ctx: DocumentGenerationContext, title_type: str) -> str:
    if ctx.capital is None:
        raise ValueError(f"capital est obligatoire pour {DOCUMENT_CODE}.")
    field_name = (
        "capital.valeur_nominale_part"
        if title_type == "parts_sociales"
        else "capital.valeur_nominale_titre"
    )
    return required_text(
        ctx.capital.valeur_nominale_titre or ctx.capital.valeur_nominale_part,
        field_name,
    )


def apport_amount(ctx: DocumentGenerationContext, associate: Associe) -> str:
    return required_text(
        associate.apport_numeraire or (ctx.apport.montant if ctx.apport else None),
        "associes[0].apport_numeraire",
    )


def apport_amount_letters(ctx: DocumentGenerationContext, associate: Associe) -> str:
    return required_text(
        associate.apport_numeraire_lettres
        or (ctx.apport.montant_lettres if ctx.apport else None),
        "associes[0].apport_numeraire_lettres",
    )


def _validate_unique_associate_capital(
    ctx: DocumentGenerationContext,
    associate: Associe,
) -> None:
    # En multi-associes, le praticien representatif ne detient qu'une fraction du
    # capital : la coherence totale est verifiee par `_validate_sel_membres`.
    if is_sel_multi(ctx):
        return
    total = capital_titles_total(ctx)
    if associate.nb_parts != total:
        raise ValueError(
            "associes[0].nb_parts doit etre coherent avec "
            f"capital.nombre_titres_total pour {DOCUMENT_CODE}."
        )


def _dirigeant_is_unique_associe(ctx: DocumentGenerationContext) -> bool:
    if ctx.dirigeant_nomine is None or len(ctx.associes) != 1:
        return True
    associate = ctx.associes[0]
    if ctx.dirigeant_nomine.ref_associe_index == 0:
        return True
    return (
        ctx.dirigeant_nomine.prenom == associate.prenom
        and ctx.dirigeant_nomine.nom == associate.nom
    )


def _is_heading(text: str) -> bool:
    if text == "STATUTS":
        return True
    return text in {
        "DECISIONS DES ACTIONNAIRES",
        "RESULTATS SOCIAUX",
        "TRANSFORMATION DE LA SOCIETE",
        "DISSOLUTION â€“ LIQUIDATION",
        "CONTESTATIONS",
        "CONSTITUTION DE LA SOCIETE",
        "ANNEXE",
        "ANNEXE 1",
    }
