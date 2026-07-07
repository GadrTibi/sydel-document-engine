from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

from sydel_doc_engine.domain.models import (
    ApportTitres,
    CapitalSouscription,
    DocumentGenerationContext,
    SocieteCible,
    SocieteSpfpl,
    SpfplPerson,
)
from sydel_doc_engine.generators.lot_05.scm_cession_common import (
    mentions_conjoint,
    mentions_partenaire_pacse,
    partenaire_pacse_clause,
)
from sydel_doc_engine.rendering.docx_builder import (
    STATUTS_SPFPL_COMPACT_STYLE_PROFILE,
    add_paragraph,
    add_statuts_article_heading,
    add_statuts_body_paragraph,
    add_statuts_hanging_list_item,
    add_statuts_part_heading,
    add_statuts_signature_block,
    new_document,
)
from sydel_doc_engine.utils.grammar import integer_to_french_words

DOCUMENT_CODE = "CODE-STATUTS-SPFPL-001"
SPFPL_CESSION_STRUCTURE = "SPFPL cession"
SPFPL_APPORT_STRUCTURE = "SPFPL apport"
OPERATION_CESSION = "cession"
OPERATION_APPORT = "apport"


def required_text(value: str | None, field_name: str) -> str:
    # R10 (Rafael 2026-06-24) : une donnee manquante NE bloque PAS la generation -> on ecrit un
    # marqueur visible « (A COMPLETER : data) » SANS crochets (pour ne pas declencher le garde-fou
    # anti-placeholder source qui interdit les [ ]) au lieu de lever.
    if value is None or not value.strip():
        return f"(À COMPLÉTER : {field_name})"
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


def required_societe_spfpl(ctx: DocumentGenerationContext) -> SocieteSpfpl:
    if ctx.societe_spfpl is None:
        raise ValueError(f"societe_spfpl est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.societe_spfpl


def required_capital_souscription(ctx: DocumentGenerationContext) -> CapitalSouscription:
    if ctx.capital_souscription is None:
        raise ValueError(f"capital_souscription est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.capital_souscription


def required_apport_titres(ctx: DocumentGenerationContext) -> ApportTitres:
    if ctx.apport_titres is None:
        raise ValueError(f"apport_titres est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.apport_titres


def required_societe_cible(ctx: DocumentGenerationContext) -> SocieteCible:
    if ctx.societe_cible is None:
        raise ValueError(f"societe_cible est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.societe_cible


def required_actionnaire_unique(ctx: DocumentGenerationContext) -> SpfplPerson:
    if ctx.actionnaire_unique is not None:
        return ctx.actionnaire_unique
    if ctx.operation_spfpl and ctx.operation_spfpl.type == OPERATION_CESSION and ctx.cedant:
        return ctx.cedant
    if ctx.operation_spfpl and ctx.operation_spfpl.type == OPERATION_APPORT and ctx.apporteur:
        return ctx.apporteur
    raise ValueError(f"actionnaire_unique est obligatoire pour {DOCUMENT_CODE}.")


def validate_common_statuts_context(  # noqa: C901
    ctx: DocumentGenerationContext,
    *,
    structure: str,
    operation: str,
) -> None:
    if ctx.structure != structure:
        raise ValueError(f"dossier.structure doit etre {structure} pour {DOCUMENT_CODE}.")
    if ctx.operation_spfpl is None:
        raise ValueError(f"operation_spfpl est obligatoire pour {DOCUMENT_CODE}.")
    operation_type = required_text(ctx.operation_spfpl.type, "operation_spfpl.type").lower()
    if operation_type != operation:
        raise ValueError(f"operation_spfpl.type doit etre {operation} pour {DOCUMENT_CODE}.")
    if ctx.dossier_options is None:
        raise ValueError(f"dossier.options est obligatoire pour {DOCUMENT_CODE}.")
    if operation == OPERATION_CESSION and not ctx.dossier_options.cession:
        raise ValueError(f"dossier.options.cession doit etre vrai pour {DOCUMENT_CODE}.")
    if operation == OPERATION_APPORT and not ctx.dossier_options.apport:
        raise ValueError(f"dossier.options.apport doit etre vrai pour {DOCUMENT_CODE}.")
    if operation == OPERATION_CESSION and ctx.dossier_options.apport:
        raise ValueError(f"un seul overlay SPFPL peut etre rendu pour {DOCUMENT_CODE}.")
    if operation == OPERATION_APPORT and ctx.dossier_options.cession:
        raise ValueError(f"un seul overlay SPFPL peut etre rendu pour {DOCUMENT_CODE}.")
    if len(ctx.associes) > 1:
        raise ValueError(
            f"les statuts SPFPL multi-associes sont bloques en V1 pour {DOCUMENT_CODE}."
        )
    if (
        ctx.capital_souscription is not None
        and len(ctx.capital_souscription.souscripteurs) > 1
    ):
        raise ValueError(
            f"les statuts SPFPL multi-associes sont bloques en V1 pour {DOCUMENT_CODE}."
        )


def company_siege_display(societe: SocieteSpfpl | SocieteCible, field_name: str) -> str:
    if societe.siege is None:
        raise ValueError(f"{field_name}.siege est obligatoire pour {DOCUMENT_CODE}.")
    if societe.siege.adresse_affichee:
        return societe.siege.adresse_affichee.strip()
    return (
        f"{required_text(societe.siege.num_voie, f'{field_name}.siege.num_voie')} "
        f"{required_text(societe.siege.voie, f'{field_name}.siege.voie')}, "
        f"{required_text(societe.siege.cp, f'{field_name}.siege.cp')} "
        f"{required_text(societe.siege.ville, f'{field_name}.siege.ville')}"
    )


def person_address_display(person: SpfplPerson, field_name: str) -> str:
    if person.adresse_personnelle_affichee:
        return person.adresse_personnelle_affichee.strip()
    if person.adresse_personnelle is None:
        raise ValueError(f"{field_name}.adresse_personnelle est obligatoire pour {DOCUMENT_CODE}.")
    address = person.adresse_personnelle
    if address.adresse_affichee:
        return address.adresse_affichee.strip()
    return (
        f"{required_text(address.num_voie, f'{field_name}.adresse_personnelle.num_voie')} "
        f"{required_text(address.voie, f'{field_name}.adresse_personnelle.voie')}, "
        f"{required_text(address.cp, f'{field_name}.adresse_personnelle.cp')} "
        f"{required_text(address.ville, f'{field_name}.adresse_personnelle.ville')}"
    )


# --- Montants (Albane 2026-07-07, R5/R6 rapport conformance) -------------------------------
#
# Le front injecte les montants BRUTS tels que saisis (« 60000 ») ; Albane exige des montants
# GROUPES en sortie (« 60 000 »). Groupage LOCAL au chemin SPFPL (les autres types = lots/agents
# separes) ; toute valeur non purement numerique (marqueur « (À COMPLÉTER : …) ») passe telle
# quelle — fail-safe, aucune invention.

# NB : `\s` (str, Unicode) couvre aussi les separateurs de milliers insecables (U+00A0, U+202F).
_MONTANT_NUMERIQUE = re.compile(r"(\d[\d\s]*)(?:[.,](\d+))?")


def _montant_numerique_groupe(value: str) -> str | None:
    """« 60000 » / « 60 000 » -> « 60 000 » (idempotent) ; « 60000,50 » -> « 60 000,50 » ;
    valeur non purement numerique -> None."""
    cleaned = value.strip()
    match = _MONTANT_NUMERIQUE.fullmatch(cleaned)
    if match is None:
        return None
    digits = re.sub(r"\D", "", match.group(1))
    grouped = f"{int(digits):,}".replace(",", " ")
    if match.group(2):
        return f"{grouped},{match.group(2)}"
    return grouped


def groupe_milliers(value: str) -> str:
    """Groupage FR des milliers d'un montant en chiffres (« 60000 » -> « 60 000 »)."""
    grouped = _montant_numerique_groupe(value)
    return grouped if grouped is not None else value.strip()


def montant_euro_symbole(value: str) -> str:
    """« 60000 » / « 60 000 € » -> « 60 000 € » (groupe + symbole €, sans doublon).

    Albane 2026-07-07 (fix 4) : la ligne « Ci … [montant] » (et le total qui la suit,
    meme token) rend « 60 000 € », pas « 60000 » nu. Une valeur non numerique
    (marqueur « À COMPLÉTER ») est rendue telle quelle, sans symbole invente."""
    cleaned = value.strip()
    if cleaned.endswith("€"):
        cleaned = cleaned[:-1].rstrip()
    grouped = _montant_numerique_groupe(cleaned)
    if grouped is None:
        return value.strip()
    return f"{grouped} €"


def montant_en_lettres(lettres: str | None, figure: str) -> str:
    """Lettres d'un montant pour l'art. 8 : slot front (`*_lettres`) si present, sinon repli
    CALCULE depuis la figure (entier -> mots via `integer_to_french_words`, semantique
    identique a `number_words_from_value` cote front ; non-entier -> figure telle quelle)."""
    if lettres and lettres.strip():
        return lettres.strip()
    digits = re.sub(r"\s", "", figure.strip())
    if digits.isdigit():
        return integer_to_french_words(int(digits))
    return figure.strip()


def render_statuts_docx(  # noqa: C901
    blocks: tuple[str, ...],
    replacements: dict[str, str],
    output_path: Path,
) -> Path:
    # FORME (FIDELITY_AUDIT_V1, FIX-F4 / STYLE-6) : les deux DOCX source SPFPL ont des marges
    # compactes (haut 2.82 / bas 0 / gauche 0.74). Le profil compact existant en est l'image la
    # plus proche cote moteur ; on le cable ici plutot que le DEFAULT (marges 2.5) jamais fidele.
    docx = new_document(style_profile=STATUTS_SPFPL_COMPACT_STYLE_PROFILE)
    style_profile = STATUTS_SPFPL_COMPACT_STYLE_PROFILE
    title_block_count = _title_block_count(blocks, replacements)
    index = 0
    while index < len(blocks):
        block = blocks[index]
        text = replace_placeholders(block, replacements)
        if index < title_block_count:
            # FIX-F1 / STYLE-1 : bloc de titre (denomination / sous-titre / capital / siege)
            # centre dans la source ; la 1re ligne (denomination) est en gras (style Heading 3).
            add_paragraph(
                docx,
                text,
                alignment=WD_ALIGN_PARAGRAPH.CENTER,
                bold=(index == 0),
                style_profile=style_profile,
            )
        elif text == "STATUTS":
            # FIX-F4 / STYLE-5 : "STATUTS" est en Heading 3 taille 12 dans la source (run sz=12).
            paragraph = add_paragraph(
                docx,
                text,
                alignment=WD_ALIGN_PARAGRAPH.CENTER,
                bold=True,
                style_profile=style_profile,
            )
            paragraph.runs[0].font.size = Pt(12)
        elif _is_major_heading(text):
            # Albane 2026-07-07 (fix 5) : des titres majeurs CONSECUTIFS (annexe : « ANNEXE 1 »
            # + « ETAT DES ENGAGEMENTS PRIS AVANT » + « LA CONSTITUTION DE LA SOCIETE ») sortaient
            # en PLUSIEURS cadres empiles (« cadres multiples inutiles ») -> UN SEUL cadre
            # multi-lignes. Un titre isole garde le rendu historique (byte-identique).
            heading_lines = [text]
            while index + 1 < len(blocks):
                next_text = replace_placeholders(blocks[index + 1], replacements)
                if not _is_major_heading(next_text):
                    break
                heading_lines.append(next_text)
                index += 1
            _add_major_heading_box(docx, heading_lines, style_profile=style_profile)
        elif text.startswith("ARTICLE "):
            add_statuts_article_heading(docx, text, underline=False, style_profile=style_profile)
        elif text.startswith("Fait à ") or text.startswith("Fait a "):
            signature_lines, mention_lines, index = _collect_signature_lines(
                blocks,
                replacements,
                index,
            )
            add_statuts_signature_block(
                docx,
                signature_lines,
                mention_lines=mention_lines,
                style_profile=style_profile,
            )
            continue
        elif _is_soussigne_line(block):
            # FIX-F2 / STYLE-2 : "Le soussigne :" est souligne dans la source (JUSTIFY + souligne).
            add_paragraph(
                docx,
                text,
                alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                underline=True,
                style_profile=style_profile,
            )
        elif _is_identity_line(block):
            # FIX-F3 / STYLE-3 : la ligne d'identite "- [civilite] [prenom(s)] [nom]" est en gras
            # (run unique incl. le tiret) et JUSTIFY dans la source, pas un item de liste.
            add_paragraph(
                docx,
                text,
                alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                bold=True,
                style_profile=style_profile,
            )
        elif block in _BOLD_CAPITAL_BLOCKS:
            # FIX-F3 / STYLE-4 : lignes de capital / total (Art. 6 & 8) en gras dans la source.
            _add_bold_segments_paragraph(docx, block, replacements, style_profile=style_profile)
        elif text.startswith("- "):
            add_statuts_hanging_list_item(docx, text[2:], style_profile=style_profile)
        elif _looks_like_numbered_list_item(text):
            add_statuts_hanging_list_item(docx, text, marker=None, style_profile=style_profile)
        else:
            add_statuts_body_paragraph(docx, text, style_profile=style_profile)
        index += 1

    full_text = "\n".join(paragraph.text for paragraph in docx.paragraphs)
    if "[" in full_text or "]" in full_text:
        raise ValueError(f"placeholder source residuel dans le rendu {DOCUMENT_CODE}.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    docx.save(output_path)
    return output_path


# --- FORME : routage de mise en forme fidele au modele source (FIDELITY_AUDIT_V1, volet 2) ---
#
# Les segments de gras sont decoupes EXACTEMENT sur les frontieres de runs des DOCX source
# (python-docx), pas inventes. Chaque entree mappe un bloc-source brut vers la suite ordonnee de
# segments (is_bold, fragment-de-template) ; chaque fragment est ensuite substitue puis ajoute en
# run distinct, ce qui reproduit le decoupage gras / non-gras du modele.
#
# Cession Art. 8 : "- Le Docteur [prenom] [nom]" en gras, le bourrage de points et "[nb] actions"
# non gras (source : runs idx116 / idx117). Apport Art. 8 : ligne entiere en gras (source idx127 /
# idx128). Cession Art. 6 "Total des apports\t..." : ligne entiere en gras (source idx106).
_BOLD_CAPITAL_SEGMENTS: dict[str, tuple[tuple[bool, str], ...]] = {
    # Cession Art. 6 — total des apports (run unique en gras dans la source)
    "Total des apports\t\t\t\t\t\t\t\t\t[montant_apport]": (
        (True, "Total des apports\t\t\t\t\t\t\t\t\t[montant_apport]"),
    ),
    # Cession Art. 8 — repartition (gras sur l'identite uniquement)
    "- Le Docteur [prenom] [nom]………………………………………….…….………..[nb_actions] actions": (
        (True, "- Le Docteur [prenom] [nom]"),
        (False, "………………………………………….…….………..[nb_actions] actions"),
    ),
    # Art. 8 — total des actions (chaine IDENTIQUE cession/apport). Source apport idx128 : ligne
    # entiere en gras ; source cession idx117 : gras sauf le bourrage de points (leader dots).
    # On retient le gras de ligne entiere : exact pour l'apport, et pour la cession la seule
    # difference porte sur des points de conduite (gras imperceptible) — pas d'invention.
    "Total des actions composant le capital social……………………………. [nb_actions] actions": (
        (True, "Total des actions composant le capital social……………………………. [nb_actions] actions"),
    ),
    # Apport Art. 8 — repartition (ligne entiere en gras dans la source)
    "- Le Docteur [prenom] [nom]………………………………………….……………..[nb_actions] actions": (
        (True, "- Le Docteur [prenom] [nom]………………………………………….……………..[nb_actions] actions"),
    ),
}
_BOLD_CAPITAL_BLOCKS = frozenset(_BOLD_CAPITAL_SEGMENTS)


def _title_block_count(blocks: tuple[str, ...], replacements: dict[str, str]) -> int:
    """Nombre de blocs de titre (avant "STATUTS") a centrer (FIX-F1)."""
    for index, block in enumerate(blocks):
        if replace_placeholders(block, replacements) == "STATUTS":
            return index
    return 0


def _is_soussigne_line(block: str) -> bool:
    return block.startswith("Le soussigné")


def _is_identity_line(block: str) -> bool:
    return block.startswith("- [civilite] ") and block.rstrip().endswith("[nom]")


def _add_bold_segments_paragraph(
    docx,  # noqa: ANN001 - type docx interne python-docx
    block: str,
    replacements: dict[str, str],
    *,
    style_profile,  # noqa: ANN001
):
    paragraph = docx.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(style_profile.standard_space_after_pt)
    for is_bold, fragment in _BOLD_CAPITAL_SEGMENTS[block]:
        run = paragraph.add_run(replace_placeholders(fragment, replacements))
        run.bold = is_bold
    return paragraph


def replace_placeholders(text: str, replacements: dict[str, str]) -> str:
    rendered = text
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def _ligne_situation_maritale(founder: SpfplPerson, field_name: str) -> str:
    """Ligne de comparution matrimoniale de l'actionnaire fondateur (cession).

    Retour Rafael 2026-07-02 : la comparution SPFPL cession portait une ligne assumant
    un MARIE (« <statut> sous le régime de <regime> avec <conjoint> »). La SPFPL utilise
    desormais le menu complet « Situation matrimoniale » : cette ligne BRANCHE sur le STATUT.
    - MARIE -> ligne complete BYTE-IDENTIQUE a avant (wording PROPRE A LA SPFPL : « avec »,
      pas « époux/épouse de »). Regime + conjoint rendus via required_text : absents -> marqueur
      VISIBLE « (À COMPLÉTER) » (R10), JAMAIS une perte silencieuse du regime.
    - AUTRE (celibataire / pacse / divorce / veuf) -> juste le statut matrimonial.

    Akainu m3 (2026-07-02) : on branche sur le STATUT (« marié »/« mariée ») et NON plus sur
    « regime present ET conjoint present ». L'ancienne garde faisait du fail-SILENT (un marie
    sans conjoint retombait sur le statut seul en PERDANT le regime) ; on veut du fail-LOUD
    (marqueur visible). Cas atteignables inchanges (front : marie => regime+conjoint requis).
    Akainu n1 (round 2) : garde UNIQUE `mentions_conjoint` (normalisation NFKD, ensemble
    {marie, mariee}) partagee avec les actes de cession/apport — plus de `startswith` divergent.
    """
    statut = required_text(founder.situation_maritale, f"{field_name}.situation_maritale")
    if not mentions_conjoint(founder.situation_maritale):
        # Albane 6.3/7.3 (RATIFIE 2026-07-06) : un PACSE affiche son PARTENAIRE (« Pacsé avec
        # {Civilite Prenom Nom} »), SANS « sous le régime de … » (le menu « Pacsé(e) » ne
        # capture aucun sous-regime PACS). « Pas de mention sans nom » : partenaire_pacse_clause
        # -> "" si non renseigne -> on retombe sur le statut nu.
        if mentions_partenaire_pacse(founder.situation_maritale):
            return _capitalize_first(
                f"{statut}{partenaire_pacse_clause(founder.conjoint)}"
            )
        # M1 (Akainu 2026-07-06) : 7.2 exige que CHAQUE element de la liste du soussigne
        # commence par une MAJUSCULE (« Celibataire », pas « celibataire »).
        return _capitalize_first(statut)
    conjoint = founder.conjoint
    civilite_conjoint = required_text(
        conjoint.civilite_affichage if conjoint else None,
        f"{field_name}.conjoint.civilite_affichage",
    )
    prenom_conjoint = required_text(
        conjoint.prenom if conjoint else None, f"{field_name}.conjoint.prenom"
    )
    nom_conjoint = required_text(conjoint.nom if conjoint else None, f"{field_name}.conjoint.nom")
    regime_matrimonial = required_text(
        founder.regime_matrimonial, f"{field_name}.regime_matrimonial"
    )
    # M1 (Akainu 2026-07-06) : idem — la ligne matrimoniale complete commence par une MAJUSCULE
    # (« Marié sous le régime de … »). `_capitalize_first` preserve le reste (accents, casse).
    return _capitalize_first(
        f"{statut} sous le régime de {regime_matrimonial} avec "
        f"{civilite_conjoint} {prenom_conjoint} {nom_conjoint}"
    )


def _capitalize_first(value: str) -> str:
    """Capitalise la 1re lettre en preservant le reste (« chirurgien-dentiste » ->
    « Chirurgien-dentiste »). N'utilise PAS str.capitalize() qui abaisserait le reste
    (« ... -Dentiste » deviendrait « ...-dentiste »)."""
    if not value:
        return value
    return value[0].upper() + value[1:]


def founder_common_replacements(founder: SpfplPerson, field_name: str) -> dict[str, str]:
    ordre = founder.ordre
    if ordre is None:
        raise ValueError(f"{field_name}.ordre est obligatoire pour {DOCUMENT_CODE}.")
    return {
        "[civilite]": required_text(
            founder.civilite_affichage,
            f"{field_name}.civilite_affichage",
        ),
        "[prenom]": required_text(founder.prenom, f"{field_name}.prenom"),
        "[prenoms]": required_text(founder.prenoms or founder.prenom, f"{field_name}.prenoms"),
        "[nom]": required_text(founder.nom, f"{field_name}.nom"),
        "[profession]": required_text(founder.profession, f"{field_name}.profession"),
        # 7.2 (Albane 2026-07-06) : dans la liste du soussigne, « <Profession> de
        # profession » commence en MAJUSCULE comme les autres lignes (Civilite / Ne /
        # Demeurant...). Token DISTINCT de [profession] (utilise ailleurs en minuscule) :
        # seule la 1re lettre est capitalisee, le reste du libelle est preserve.
        "[profession_capitale]": _capitalize_first(
            required_text(founder.profession, f"{field_name}.profession")
        ),
        "[date_naissance]": format_display_date(
            founder.date_naissance,
            f"{field_name}.date_naissance",
        ),
        "[ville_naissance]": required_text(
            founder.ville_naissance,
            f"{field_name}.ville_naissance",
        ),
        "[departement_naissance]": required_text(
            founder.departement_naissance,
            f"{field_name}.departement_naissance",
        ),
        "[adresse_personnelle]": person_address_display(founder, field_name),
        # M1 (Akainu 2026-07-06, propagation regle 68 Q4) : ce token bare porte le statut
        # matrimonial SEUL dans la nomination du President (cession) et la comparution
        # (apport). 7.2 exige une MAJUSCULE en tete de chaque element -> « Célibataire »,
        # « Marié », comme la ligne combinee. (La ligne combinee marie de la comparution
        # cession passe par [ligne_situation_maritale], traite longest-first.)
        "[situation_maritale]": _capitalize_first(
            required_text(
                founder.situation_maritale,
                f"{field_name}.situation_maritale",
            )
        ),
        # Ligne de comparution matrimoniale BRANCHEE (marie -> ligne complete ;
        # sinon -> juste le statut). Seul le modele CESSION porte ce token ; l'apport
        # rend deja le bare [situation_maritale] (token inoffensif s'il n'apparait pas).
        "[ligne_situation_maritale]": _ligne_situation_maritale(founder, field_name),
        "[nationalite]": required_text(founder.nationalite, f"{field_name}.nationalite"),
        "[numero_ordre]": required_text(ordre.numero, f"{field_name}.ordre.numero"),
        "[numero_rpps]": required_text(ordre.numero_rpps, f"{field_name}.ordre.numero_rpps"),
    }


def _add_major_heading_box(
    docx,  # noqa: ANN001 - type docx interne python-docx
    lines: list[str],
    *,
    style_profile,  # noqa: ANN001
):
    """Titre(s) majeur(s) encadre(s). UNE ligne -> délégation pure a `add_statuts_part_heading`
    (rendu historique byte-identique). PLUSIEURS lignes consecutives (annexe) -> le MEME cadre
    accueille les lignes suivantes via des sauts de ligne dans le paragraphe de la cellule
    (Albane 2026-07-07, fix 5 : un cadre UNIQUE au lieu de cadres empiles).

    Modif limitee au chemin SPFPL : le builder PARTAGE (`add_statuts_part_heading` /
    `add_statuts_title_box`, utilise par d'autres types de statuts) n'est PAS modifie."""
    table = add_statuts_part_heading(
        docx, lines[0], mode="boxed", style_profile=style_profile
    )
    if len(lines) == 1:
        return table
    paragraph = table.cell(0, 0).paragraphs[0]
    reference_run = paragraph.runs[0]
    for line in lines[1:]:
        paragraph.runs[-1].add_break()
        run = paragraph.add_run(line)
        run.bold = True
        run.font.name = reference_run.font.name
        run.font.size = reference_run.font.size
    return table


def _is_major_heading(text: str) -> bool:
    headings = {
        "DECISIONS DES ACTIONNAIRES",
        "RESULTATS SOCIAUX",
        "TRANSFORMATION DE LA SOCIETE",
        "DISSOLUTION – LIQUIDATION",
        "CONTESTATIONS",
        "CONSTITUTION DE LA SOCIETE",
        "ANNEXE 1",
        "ETAT DES ENGAGEMENTS PRIS AVANT",
        "LA CONSTITUTION DE LA SOCIETE",
    }
    return text in headings


def _collect_signature_lines(
    blocks: tuple[str, ...],
    replacements: dict[str, str],
    start_index: int,
) -> tuple[list[str], list[str], int]:
    signature_lines: list[str] = []
    mention_lines: list[str] = []
    index = start_index
    while index < len(blocks):
        rendered = replace_placeholders(blocks[index], replacements)
        if index > start_index and (rendered.startswith("ANNEXE") or _is_major_heading(rendered)):
            break
        if "Bon pour acceptation" in rendered:
            mention_lines.append(rendered)
        else:
            signature_lines.append(rendered)
        index += 1
    return signature_lines, mention_lines, index


def _looks_like_numbered_list_item(text: str) -> bool:
    return len(text) > 2 and text[0].isdigit() and text[1] in {"°", "."}
