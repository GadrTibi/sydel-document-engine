from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from docx import Document
from docx.enum.table import WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

# ---------------------------------------------------------------------------
# Post-fill : « Demeurant [adresse] » -> « Demeurant au [adresse] » (Rafael/Albane
# 2026-07-09, convention UNIVERSELLE). Pour les documents rendus par TOKEN-REPLACEMENT
# sur un modele .docx binaire (actes de cession, contrat d'apport, statuts SASU/SAS),
# le mot « Demeurant » est FIGE dans le modele source (lecture seule) : on ne peut pas
# l'editer a la source comme pour les generateurs from-scratch. On insere donc « au »
# APRES remplissage des tokens, au niveau des RUNS (formatage preserve : noms en gras,
# etc.). Idempotent (« demeurant au 5 » n'est plus suivi d'un chiffre -> jamais double).
# Regle par INTENTION identique a la R14 de conformite : un « [Dd]emeurant » suivi
# DIRECTEMENT d'un numero de voie (chiffre) recoit « au ». « demeurant a <Ville> »
# (ville seule, sans numero) n'est jamais touche (aucun chiffre ne suit). Le supersede
# de fidelite au modele est trace (retour le plus recent prime, regle 68).
_DEMEURANT_SAME_RUN = re.compile(r"(?i)(demeurant)(\s+)(\d)")
_DEMEURANT_RUN_END = re.compile(r"(?i)demeurant\s*$")
_ADDRESS_RUN_START = re.compile(r"^(\s*)(\d)")


def _fix_demeurant_paragraph(paragraph: Any) -> None:
    # Cas 1 — « demeurant » et le numero dans le MEME run.
    for run in paragraph.runs:
        if run.text:
            fixed = _DEMEURANT_SAME_RUN.sub(r"\1\2au \3", run.text)
            if fixed != run.text:
                run.text = fixed
    # Cas 2 — « demeurant » en fin de run, numero au debut d'un run SUIVANT (token
    # « Demeurant [adresse] » : Word eclate le mot et la valeur en runs distincts, parfois
    # separes par des runs vides / d'espaces — on saute ces runs pour retrouver l'adresse).
    runs = [run for run in paragraph.runs if run.text]
    for index, current in enumerate(runs):
        if not _DEMEURANT_RUN_END.search(current.text):
            continue
        for following in runs[index + 1 :]:
            if not following.text.strip():
                continue  # run d'espaces intercalaire — on l'ignore
            if _ADDRESS_RUN_START.match(following.text):
                following.text = _ADDRESS_RUN_START.sub(r"\1au \2", following.text)
            break


def ensure_demeurant_au(document: Any) -> None:
    """Insere « au » entre « Demeurant » et un numero de voie dans TOUT le document
    (corps + cellules de tableaux), au niveau des runs (formatage preserve). Idempotent.

    A appeler APRES remplissage des tokens, juste avant la sauvegarde, sur les
    generateurs par modele .docx binaire (le from-scratch se corrige a la source)."""
    for paragraph in document.paragraphs:
        _fix_demeurant_paragraph(paragraph)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    _fix_demeurant_paragraph(paragraph)


@dataclass(frozen=True)
class SydelDocxStyleProfile:
    font_name: str = "Roboto"
    font_size_pt: int = 10
    # Retour Albane « mise en forme » 1.1 : « interligne 0,5 ou 1 ». Le defaut python-docx est
    # 1,15 (docDefaults line=276) -> trop aere. On impose l'interligne SIMPLE (1,0) sur le style
    # « Normal » des generateurs from-scratch. None = ne pas toucher (heriter du modele/defaut).
    line_spacing: float | None = 1.0
    margin_top_cm: float = 2.5
    margin_bottom_cm: float = 2.5
    margin_left_cm: float = 2.5
    margin_right_cm: float = 2.5
    standard_space_after_pt: int = 6
    compact_space_after_pt: int = 2
    legal_reminder_space_after_pt: int = 3
    notable_space_before_pt: int = 10
    signature_width_cm: float = 7.0
    signature_image_width_cm: float = 4.0
    # Marges internes des cadres (cellules de tableau 1x1), en dxa/twips (1 pt = 20 dxa).
    # Additif : aere l'interieur des cadres sans toucher aux bordures.
    frame_cell_margin_vertical_dxa: int = 100
    frame_cell_margin_horizontal_dxa: int = 140
    signature_cell_margin_vertical_dxa: int = 120
    signature_cell_margin_horizontal_dxa: int = 140


DEFAULT_STYLE_PROFILE = SydelDocxStyleProfile()
LETTER_WIDE_STYLE_PROFILE = SydelDocxStyleProfile(
    margin_left_cm=3.17,
    margin_right_cm=3.17,
)
STATUTS_STANDARD_STYLE_PROFILE = DEFAULT_STYLE_PROFILE
STATUTS_SPFPL_COMPACT_STYLE_PROFILE = SydelDocxStyleProfile(
    margin_top_cm=2.8,
    margin_bottom_cm=1.6,
    margin_left_cm=2.0,
    margin_right_cm=2.0,
)
STATUTS_CIVIL_COMPACT_STYLE_PROFILE = SydelDocxStyleProfile(
    margin_top_cm=2.8,
    margin_bottom_cm=1.9,
    margin_left_cm=2.35,
    margin_right_cm=2.2,
)
BAIL_COMPACT_STYLE_PROFILE = SydelDocxStyleProfile(
    margin_top_cm=1.75,
    margin_bottom_cm=0.5,
)
DEROGATION_FORM_STYLE_PROFILE = SydelDocxStyleProfile(
    margin_top_cm=2.0,
)
DEROGATION_CUMUL_STYLE_PROFILE = SydelDocxStyleProfile(
    margin_top_cm=3.25,
    margin_bottom_cm=2.0,
)


def new_document(
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    """Create a clean DOCX document with the shared SYDEL style profile applied."""
    document = Document()
    apply_style_profile(document, style_profile)
    return document


def new_document_from_model(model_path: Any) -> Any:
    """Ouvre un modele .docx et le vide de son CORPS en conservant sa FORME.

    R1 (Albane 2026-06-30, « la mise en forme des statuts est toujours l'ancienne ») : les
    statuts civils lisaient le modele Albane pour son TEXTE mais recopiaient ce texte dans un
    ``new_document()`` au profil SYDEL (Roboto 10, marges 2,5, page Letter US, footer parasite)
    -> la forme du modele etait ECRASEE. On herite desormais la forme du modele en partant du
    modele lui-meme et en ne supprimant que le contenu du corps.

    Le document retourne conserve, du modele :
    - la mise en page de section (page / marges) via le ``<w:sectPr>`` GOUVERNANT, c.-a-d. le
      premier dans l'ordre du document — celui que python-docx expose comme ``sections[0]`` et
      qui porte la geometrie de la page 1 ainsi que les references header/footer ;
    - les styles nommes (Title / Heading 1 / Normal...) et la police par defaut (styles.xml) ;
    - le header et le footer (logo de marque, pagination native...).

    Il NE conserve PAS le texte du modele : tous les enfants du corps (``w:p``, ``w:tbl``,
    signets...) sont retires. AUCUN paragraphe d'amorce n'est laisse : ``add_paragraph`` /
    ``add_table`` de python-docx inserent correctement leur contenu AVANT le ``sectPr`` final
    meme quand le corps ne contient que ce sectPr. L'appelant re-injecte ensuite le wording
    valide du code, et son PREMIER bloc devient ``body[0]`` (le titre / la denomination), sans
    ligne blanche parasite en tete de page 1 (m1 : l'amorce vide decalait le rendu vs modele).

    PIEGE multi-sections (vecu SCI IRIS) : certains modeles ont DEUX sectPr — un de niveau
    paragraphe (le ``sectPr`` GOUVERNANT : vraie geometrie page 1 + footer de pagination) et un
    sectPr final aux proprietes differentes (marge droite distincte, sans footer). Garder
    naivement le sectPr FINAL prendrait la mauvaise geometrie et perdrait le footer. On preserve
    donc le PREMIER sectPr de l'ordre du document et on le repose comme unique sectPr du corps.
    """
    document = Document(model_path)
    body = document.element.body
    # Premier sectPr dans l'ordre du document = section gouvernante (geometrie page 1 +
    # references header/footer). On le detache pour le re-poser comme sectPr final unique.
    governing_sect_pr = body.find(".//" + qn("w:sectPr"))
    if governing_sect_pr is None:
        governing_sect_pr = body.find(qn("w:sectPr"))
    if governing_sect_pr is not None:
        governing_sect_pr.getparent().remove(governing_sect_pr)
    # On vide entierement le corps (texte du modele) ; la geometrie/styles/header-footer
    # vivent dans le sectPr gouvernant detache + styles.xml + parts header/footer (preserves).
    for child in list(body.iterchildren()):
        body.remove(child)
    # Repose le sectPr gouvernant comme unique enfant du corps (= sectPr de section finale).
    # Le corps ne contient QUE ce sectPr ; le 1er add_paragraph/add_table de l'appelant s'inserera
    # juste avant lui -> son 1er bloc devient body[0] (titre), sans amorce vide en tete.
    if governing_sect_pr is not None:
        body.append(governing_sect_pr)
    # Charte SYDEL (retour Albane 2026-07-01 : « police Times au lieu de Roboto ») : la police
    # par defaut HERITEE du modele n'est PAS forcement Roboto (ex. le modele micro holding est en
    # Times New Roman). On garde toute la GEOMETRIE / mise en page du modele, mais on IMPOSE la
    # FAMILLE de police de la charte (Roboto) sur les styles -> layout du modele + police SYDEL.
    # On ne touche NI aux marges NI a la geometrie (seules la famille + la taille par defaut).
    _force_charter_font_family(document, DEFAULT_STYLE_PROFILE.font_name)
    # Retour Albane 2026-07-02 : idem pour la TAILLE (« tout en 12 au lieu de 10 ») — le « Normal »
    # herite du modele peut etre a 12 pt ; on impose la taille de la charte (10 pt).
    _force_charter_font_size(document, DEFAULT_STYLE_PROFILE.font_size_pt)
    return document


def _force_charter_font_family(document: Any, font_name: str) -> None:  # noqa: C901
    """Force la FAMILLE de police `font_name` (charte SYDEL) partout, sans toucher aux tailles
    ni a la geometrie. A appeler apres new_document_from_model pour que la mise en page HERITEE
    du modele s'affiche dans la police SYDEL et non celle (arbitraire) du modele.

    Pose la police a 4 niveaux pour couvrir tous les cas d'heritage docx :
    (1) docDefaults (rPrDefault) = police par defaut du document ;
    (2) le style « Normal » (base dont heritent les runs sans police explicite) ;
    (3) chaque style de paragraphe/caractere qui definit une police propre (Title, Heading...) ;
    (4) les parts HEADER / FOOTER de chaque section (XML separe, NON couvert par les styles du
        corps) — dont les champs de pagination (« PAGE ») que certains modeles rendent en Arial
        (Akainu M1, retour Albane 2026-07-01 : la charte Roboto doit s'appliquer AUSSI au numero
        de page en pied/en-tete de SCI, SCM...).
    """

    def _set_rfonts(rpr: Any) -> None:
        if rpr is None:
            return
        rfonts = rpr.find(qn("w:rFonts"))
        if rfonts is None:
            rfonts = OxmlElement("w:rFonts")
            rpr.insert(0, rfonts)
        for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rfonts.set(qn(attr), font_name)

    styles_element = document.styles.element
    # (1) docDefaults / rPrDefault : police par defaut de tout le document.
    doc_defaults = styles_element.find(qn("w:docDefaults"))
    if doc_defaults is not None:
        rpr_default = doc_defaults.find(qn("w:rPrDefault"))
        if rpr_default is not None:
            rpr = rpr_default.find(qn("w:rPr"))
            if rpr is None:
                rpr = OxmlElement("w:rPr")
                rpr_default.append(rpr)
            _set_rfonts(rpr)
    # (2) + (3) chaque style porteur d'une police.
    for style in document.styles:
        try:
            font = style.font
        except (AttributeError, ValueError):
            continue
        try:
            font.name = font_name
            _set_rfonts(style.element.get_or_add_rPr())
        except (AttributeError, ValueError, KeyError):
            continue
    # (4) HEADER / FOOTER de chaque section (parts XML separees) : on force la famille sur TOUS
    # les runs (y compris les champs de pagination « PAGE » rendus en Arial par certains modeles).
    for section in document.sections:
        parts = (
            section.header,
            section.footer,
            section.first_page_header,
            section.first_page_footer,
            section.even_page_header,
            section.even_page_footer,
        )
        for part in parts:
            if part is None:
                continue
            # Force la famille sur TOUS les rFonts existants du header/footer (runs, marques de
            # paragraphe w:pPr/w:rPr, champs PAGE...), pas seulement les runs — sinon un rFonts
            # Arial d'une marque de paragraphe survit (vecu : pagination SCI/SCM).
            for rfonts in part._element.iter(qn("w:rFonts")):
                for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
                    rfonts.set(qn(attr), font_name)
            # + les runs SANS rFonts : leur en creer un (police explicite Roboto).
            for run_element in part._element.iter(qn("w:r")):
                rpr = run_element.find(qn("w:rPr"))
                if rpr is None:
                    rpr = OxmlElement("w:rPr")
                    run_element.insert(0, rpr)
                _set_rfonts(rpr)


def _force_charter_font_size(document: Any, font_size_pt: int) -> None:  # noqa: C901
    """Force la TAILLE de police `font_size_pt` (charte SYDEL = 10 pt) au niveau des DEFAULTS.

    Retour Albane 2026-07-02 (« tout est en police 12 au lieu de 10 ») : `new_document_from_model`
    herite la FORME du modele, dont son style « Normal ». Le modele micro holding a un « Normal » a
    12 pt (alors que ses runs SOURCES portent une taille 10 pt EXPLICITE). Quand le moteur vide le
    corps et RE-EMET le texte, les nouveaux runs n'ont PAS de taille explicite -> ils heritent de
    « Normal » = 12 pt. Pendant de `_force_charter_font_family` : on impose la taille de la charte
    (10 pt) sur les DEFAULTS (docDefaults + style « Normal »), pour que les runs re-emis (heritant
    de « Normal ») s'affichent en 10 pt. On NE touche PAS aux runs a taille EXPLICITE (cadre
    « STATUTS », titre), ni a la geometrie. `w:sz` est en demi-points (10 pt -> « 20 »).
    """
    half_points = str(int(font_size_pt) * 2)

    def _set_size(rpr: Any) -> None:
        if rpr is None:
            return
        for tag in ("w:sz", "w:szCs"):
            element = rpr.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                rpr.append(element)
            element.set(qn("w:val"), half_points)

    styles_element = document.styles.element
    # (1) docDefaults / rPrDefault : taille par defaut de tout le document.
    doc_defaults = styles_element.find(qn("w:docDefaults"))
    if doc_defaults is not None:
        rpr_default = doc_defaults.find(qn("w:rPrDefault"))
        if rpr_default is not None:
            rpr = rpr_default.find(qn("w:rPr"))
            if rpr is None:
                rpr = OxmlElement("w:rPr")
                rpr_default.append(rpr)
            _set_size(rpr)
    # (2) le style « Normal » (base dont heritent les runs re-emis sans taille explicite).
    for style in document.styles:
        try:
            if style.name == "Normal":
                _set_size(style.element.get_or_add_rPr())
                break
        except (AttributeError, ValueError):
            continue


_SYDEL_LOGO_PATH = Path(__file__).resolve().parent.parent / "assets" / "logo_sydel.png"


def add_header_logo(
    document: Any,
    *,
    alignment: WD_ALIGN_PARAGRAPH = WD_ALIGN_PARAGRAPH.LEFT,
    width_cm: float = 4.5,
) -> None:
    """Insere le logo SYDEL (en-tete de marque) dans le header de la page.

    Les generateurs from-scratch reconstruisent le corps du document en code et ont perdu
    le logo qui vivait dans le header des modeles .docx d'origine (retour UAT Rafael) :
    ce helper le retablit. L'image source est `assets/logo_sydel.png` (extrait du modele).
    """
    header = document.sections[0].header
    header.is_linked_to_previous = False
    paragraph = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    paragraph.alignment = alignment
    paragraph.add_run().add_picture(str(_SYDEL_LOGO_PATH), width=Cm(width_cm))


def apply_style_profile(
    document: Any,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> None:
    section = document.sections[0]
    section.top_margin = Cm(style_profile.margin_top_cm)
    section.bottom_margin = Cm(style_profile.margin_bottom_cm)
    section.left_margin = Cm(style_profile.margin_left_cm)
    section.right_margin = Cm(style_profile.margin_right_cm)

    style = document.styles["Normal"]
    style.font.name = style_profile.font_name
    style.font.size = Pt(style_profile.font_size_pt)
    r_fonts = style.element.rPr.rFonts
    for font_attribute in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        r_fonts.set(qn(font_attribute), style_profile.font_name)
    # 1.1 (Albane) : interligne SIMPLE (1,0) sur « Normal » -> les paragraphes du corps
    # (line_spacing=None) l'heritent, au lieu du 1,15 par defaut de docDefaults.
    if style_profile.line_spacing is not None:
        style.paragraph_format.line_spacing = style_profile.line_spacing


def add_paragraph(
    document: Any,
    text: str,
    *,
    alignment: WD_ALIGN_PARAGRAPH | None = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    space_before_pt: int = 0,
    space_after_pt: int | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(space_before_pt)
    paragraph.paragraph_format.space_after = Pt(
        style_profile.standard_space_after_pt if space_after_pt is None else space_after_pt
    )
    if alignment is not None:
        paragraph.alignment = alignment
    run = paragraph.add_run(text)
    run.bold = bold
    run.italic = italic
    run.underline = underline
    return paragraph


def add_subject_heading(
    document: Any,
    text: str,
    *,
    alignment: WD_ALIGN_PARAGRAPH = WD_ALIGN_PARAGRAPH.LEFT,
    space_before_pt: int = 0,
    space_after_pt: int | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    return add_paragraph(
        document,
        text,
        alignment=alignment,
        bold=True,
        underline=True,
        space_before_pt=space_before_pt,
        space_after_pt=space_after_pt,
        style_profile=style_profile,
    )


def add_party_marker(
    document: Any,
    text: str,
    *,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    return add_paragraph(
        document,
        text,
        alignment=WD_ALIGN_PARAGRAPH.RIGHT,
        bold=True,
        underline=True,
        style_profile=style_profile,
    )


def add_article_heading(
    document: Any,
    text: str,
    *,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    return add_paragraph(
        document,
        text,
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        bold=True,
        underline=True,
        space_before_pt=style_profile.notable_space_before_pt,
        style_profile=style_profile,
    )


def add_form_section_heading(
    document: Any,
    text: str,
    *,
    alignment: WD_ALIGN_PARAGRAPH | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    return add_paragraph(
        document,
        text,
        alignment=alignment,
        bold=True,
        underline=True,
        space_before_pt=style_profile.notable_space_before_pt,
        style_profile=style_profile,
    )


def add_letter_place_date(
    document: Any,
    text: str,
    *,
    space_after_pt: int | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    return add_paragraph(
        document,
        text,
        alignment=WD_ALIGN_PARAGRAPH.RIGHT,
        space_after_pt=space_after_pt,
        style_profile=style_profile,
    )


def add_right_aligned_lines(
    document: Any,
    lines: Sequence[str],
    *,
    space_after_pt: int | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> list[Any]:
    return [
        add_paragraph(
            document,
            line,
            alignment=WD_ALIGN_PARAGRAPH.RIGHT,
            space_after_pt=space_after_pt,
            style_profile=style_profile,
        )
        for line in lines
    ]


def add_form_field(
    document: Any,
    label: str,
    value: str,
    *,
    underline_label: bool = False,
    left_indent_cm: float = 0.0,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.left_indent = Cm(left_indent_cm)
    paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
    label_run = paragraph.add_run(f"{label} : ")
    label_run.underline = underline_label
    paragraph.add_run(value)
    return paragraph


def add_form_field_pair(
    document: Any,
    left_label: str,
    left_value: str,
    right_label: str,
    right_value: str,
    *,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
    paragraph.add_run(f"{left_label} : ")
    paragraph.add_run(left_value)
    paragraph.add_run("      ")
    paragraph.add_run(f"{right_label} : ")
    paragraph.add_run(right_value)
    return paragraph


def add_checkbox_line(
    document: Any,
    label: str,
    *,
    checked: bool = False,
    left_indent_cm: float = 0.7,
    hanging_indent_cm: float = 0.35,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    marker = "\u2612" if checked else "\u2610"
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.left_indent = Cm(left_indent_cm)
    paragraph.paragraph_format.first_line_indent = Cm(-hanging_indent_cm)
    paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
    paragraph.add_run(f"{marker} {label}")
    return paragraph


def add_right_indented_block(
    document: Any,
    lines: Sequence[str],
    *,
    left_indent_cm: float = 8.5,
    first_line_indent_cm: float | None = None,
    space_after_pt: int | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> list[Any]:
    paragraphs = []
    for line in lines:
        paragraph = add_paragraph(
            document,
            line,
            space_after_pt=space_after_pt,
            style_profile=style_profile,
        )
        paragraph.paragraph_format.left_indent = Cm(left_indent_cm)
        if first_line_indent_cm is not None:
            paragraph.paragraph_format.first_line_indent = Cm(first_line_indent_cm)
        paragraphs.append(paragraph)
    return paragraphs


def add_centered_amount(
    document: Any,
    lines: Sequence[str],
    *,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> list[Any]:
    return [
        add_paragraph(
            document,
            line,
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            bold=True,
            space_after_pt=style_profile.compact_space_after_pt,
            style_profile=style_profile,
        )
        for line in lines
    ]


def add_company_identity_block(
    document: Any,
    lines: Sequence[str],
    *,
    first_line_bold: bool = True,
    alignment: WD_ALIGN_PARAGRAPH = WD_ALIGN_PARAGRAPH.CENTER,
    space_after_pt: int | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> list[Any]:
    paragraphs = []
    for index, line in enumerate(lines):
        paragraphs.append(
            add_paragraph(
                document,
                line,
                alignment=alignment,
                bold=first_line_bold and index == 0,
                space_after_pt=(
                    style_profile.compact_space_after_pt
                    if space_after_pt is None
                    else space_after_pt
                ),
                style_profile=style_profile,
            )
        )
    return paragraphs


def add_italic_instruction(
    document: Any,
    text: str,
    *,
    alignment: WD_ALIGN_PARAGRAPH | None = None,
    space_after_pt: int | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    return add_paragraph(
        document,
        text,
        alignment=alignment,
        italic=True,
        space_after_pt=space_after_pt,
        style_profile=style_profile,
    )


def add_hyphen_list_item(
    document: Any,
    text: str,
    *,
    alignment: WD_ALIGN_PARAGRAPH | None = None,
    bold: bool = False,
    italic: bool = False,
    space_after_pt: int | None = None,
    left_indent_cm: float = 0.7,
    hanging_indent_cm: float = 0.35,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.left_indent = Cm(left_indent_cm)
    paragraph.paragraph_format.first_line_indent = Cm(-hanging_indent_cm)
    paragraph.paragraph_format.space_after = Pt(
        style_profile.standard_space_after_pt if space_after_pt is None else space_after_pt
    )
    if alignment is not None:
        paragraph.alignment = alignment
    paragraph.add_run("- ")
    run = paragraph.add_run(text)
    run.bold = bold
    run.italic = italic
    return paragraph


def add_statuts_title_box(
    document: Any,
    text: str,
    *,
    bordered: bool = True,
    cell_margin_vertical_dxa: int = 120,
    inner_space_pt: int | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    table = document.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    if bordered:
        _apply_table_grid_style(table)
        _set_table_borders(table)
    else:
        _clear_table_borders(table)

    cell = table.cell(0, 0)
    # Encadre STATUTS agrandi (retour Albane §2.1 : cadre trop petit / trop
    # proche de l'en-tete). ADDITIF : on AGRANDIT le cadre via des marges de
    # cellule + un paragraphe plus haut (space_before/after), bordures conservees.
    # ST1 (Albane 2026-07-10) : les statuts SEL passent des marges/espaces plus
    # grands (« espace avant/apres le mot STATUTS dans le cadre ») ; les autres
    # types de statuts gardent les valeurs par defaut (cadre byte-identique).
    _set_cell_margins(
        cell,
        top=cell_margin_vertical_dxa,
        bottom=cell_margin_vertical_dxa,
        left=160,
        right=160,
    )
    inner_space = (
        style_profile.standard_space_after_pt if inner_space_pt is None else inner_space_pt
    )
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(inner_space)
    paragraph.paragraph_format.space_after = Pt(inner_space)
    run = paragraph.add_run(text)
    run.bold = True
    run.font.name = style_profile.font_name
    run.font.size = Pt(style_profile.font_size_pt)
    add_spacer(document, space_after_pt=style_profile.standard_space_after_pt)
    return table


def add_statuts_article_heading(
    document: Any,
    text: str,
    *,
    underline: bool = True,
    alignment: WD_ALIGN_PARAGRAPH | None = None,
    left_indent_cm: float | None = None,
    space_before_pt: int | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    paragraph = add_paragraph(
        document,
        text,
        alignment=alignment,
        bold=True,
        underline=underline,
        space_before_pt=(
            style_profile.notable_space_before_pt
            if space_before_pt is None
            else space_before_pt
        ),
        style_profile=style_profile,
    )
    if left_indent_cm is not None:
        paragraph.paragraph_format.left_indent = Cm(left_indent_cm)
    return paragraph


def add_statuts_part_heading(
    document: Any,
    text: str,
    *,
    mode: Literal["paragraph", "boxed"] = "paragraph",
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    if mode == "boxed":
        return add_statuts_title_box(document, text, bordered=True, style_profile=style_profile)
    return add_paragraph(
        document,
        text,
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        bold=True,
        space_before_pt=style_profile.notable_space_before_pt,
        style_profile=style_profile,
    )


def add_statuts_body_paragraph(
    document: Any,
    text: str,
    *,
    alignment: WD_ALIGN_PARAGRAPH | None = WD_ALIGN_PARAGRAPH.JUSTIFY,
    indent_profile: Literal["none", "left", "first_line", "hanging"] = "none",
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    paragraph = add_paragraph(
        document,
        text,
        alignment=alignment,
        style_profile=style_profile,
    )
    if indent_profile == "left":
        paragraph.paragraph_format.left_indent = Cm(0.5)
    elif indent_profile == "first_line":
        paragraph.paragraph_format.first_line_indent = Cm(0.5)
    elif indent_profile == "hanging":
        paragraph.paragraph_format.left_indent = Cm(0.7)
        paragraph.paragraph_format.first_line_indent = Cm(-0.35)
    return paragraph


def add_statuts_hanging_list_item(
    document: Any,
    text: str,
    *,
    marker: str | None = "-",
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.left_indent = Cm(0.7)
    paragraph.paragraph_format.first_line_indent = Cm(-0.35)
    paragraph.paragraph_format.space_after = Pt(style_profile.standard_space_after_pt)
    if marker:
        paragraph.add_run(f"{marker} ")
    paragraph.add_run(text)
    return paragraph


def add_statuts_signature_block(
    document: Any,
    lines: Sequence[str],
    *,
    mention_lines: Sequence[str] = (),
    alignment: WD_ALIGN_PARAGRAPH = WD_ALIGN_PARAGRAPH.CENTER,
    bold: bool = False,
    underline: bool = False,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> list[Any]:
    paragraphs = []
    for line in lines:
        paragraphs.append(
            add_paragraph(
                document,
                line,
                alignment=alignment,
                bold=bold,
                underline=underline,
                space_after_pt=style_profile.compact_space_after_pt,
                style_profile=style_profile,
            )
        )
    for line in mention_lines:
        paragraphs.append(
            add_paragraph(
                document,
                line,
                alignment=alignment,
                italic=True,
                space_after_pt=style_profile.compact_space_after_pt,
                style_profile=style_profile,
            )
        )
    return paragraphs


def add_statuts_signature_grid(
    document: Any,
    signers: Sequence[str],
    *,
    mention: str | None = None,
    columns: int = 2,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    if columns <= 0:
        raise ValueError("columns doit etre strictement positif.")
    rows = max(1, (len(signers) + columns - 1) // columns)
    table = document.add_table(rows=rows, cols=columns)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    _set_table_borders(table)
    for index, signer in enumerate(signers):
        cell = table.cell(index // columns, index % columns)
        paragraph = cell.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if mention:
            mention_run = paragraph.add_run(mention)
            mention_run.italic = True
            paragraph.add_run("\n")
        name_run = paragraph.add_run(signer)
        name_run.bold = True
    add_spacer(document, space_after_pt=style_profile.standard_space_after_pt)
    return table


def keep_signature_block_together(
    document: Any, table: Any | None = None, *, intro_paragraphs: int = 3
) -> None:
    """KAN-36 (Rafael 2026-07-16) : garde le bloc signature — les paragraphes d'intro
    (« Fait a … / Le … ») ET la table/grille des signataires — sur une SEULE page, pour que
    toutes les informations relatives aux signataires + la zone de signature soient visibles
    ensemble (sinon « Fait a … » reste orphelin en bas d'une page et les signataires basculent
    sur la suivante — vecu SELAS multi). Mecanique : `keepNext` garde un paragraphe sur la meme
    page que l'element suivant (paragraphe OU table) ; `cantSplit` empeche une ligne (case de
    signature) de se scinder entre deux pages. A appeler juste APRES avoir rendu la table.
    `intro_paragraphs` = nombre de paragraphes juste avant la table a solidariser avec elle."""
    body_paras = document.paragraphs
    for paragraph in body_paras[-intro_paragraphs:] if intro_paragraphs > 0 else []:
        paragraph.paragraph_format.keep_with_next = True
    if table is not None:
        for row in table.rows:
            tr_pr = row._tr.get_or_add_trPr()
            if tr_pr.find(qn("w:cantSplit")) is None:
                tr_pr.append(OxmlElement("w:cantSplit"))


def keep_final_signature_block_together(document: Any) -> bool:
    """KAN-36 (Rafael 2026-07-16) — variante GENERIQUE, a appeler en fin de generation sur
    N'IMPORTE QUEL document a fin-de-doc signee (actes, PV, attestations, lettres). Repere la
    DERNIERE ligne d'ouverture de signature (« Fait a … » / « Fait le … » / « A …, le … ») et pose
    `keepNext` sur ce paragraphe et tous ceux qui suivent (sauf le tout dernier), pour que le bloc
    signature reste ENTIER sur une seule page. N'ajoute pas de contenu, ne change aucun texte :
    seule une propriete de pagination est posee (byte-neutre cote texte). Retourne True si un bloc
    a ete trouve et solidarise, False sinon (aucun « Fait a » -> no-op). A preferer a
    keep_signature_block_together quand le bloc est purement paragraphes (pas de table de cases)."""
    paras = document.paragraphs
    start = None
    # 1) DEBUT DE BLOC par ancre — pour les blocs a LONGUEUR VARIABLE ou l'ancre precede des lignes
    # nombreuses (ex. PV : cloture + N signataires). Ce sont des DEBUTS de bloc (block-starters), PAS
    # les mentions internes « Bon pour … » / « Lu et approuvé » : « Fait a/le/en/pour … » (toutes les
    # clôtures « Fait … »), l'en-tête d'acte « A/À <lieu>, le <date> », et la clôture de PROCES-VERBAL
    # (« … dressé le présent procès-verbal … signé après lecture … »). DERNIERE occurrence.
    # Une ancre n'est une SIGNATURE que dans la partie BASSE du document : « Fait à … » / « A …, le
    # <date> » en HAUT est un en-tête de date de LETTRE (ex. lettre d'option IS), pas la signature
    # (qui est « Le gérant » en bas). En dessous du seuil -> pas d'ancre valable, on bascule au
    # fallback « queue de document ». (Intention, pas tournure — règle 68.)
    anchor_floor = len(paras) * 0.4
    for index in range(len(paras) - 1, -1, -1):
        if index < anchor_floor:
            break
        stripped = paras[index].text.strip()
        if (
            (stripped.startswith("Fait ") and "générateur" not in stripped)
            # En-tete d'acte « A <lieu>, le <date> » : INTENTION = une DATE (chiffre) suit « le »,
            # sinon on false-matche de la prose de corps (« A l'expiration du delai …, le conjoint
            # … »). Regle 68 : coder l'intention, pas la tournure.
            or (
                stripped.startswith(("A ", "À "))
                and re.search(r",\s*le\s+\d", stripped) is not None
            )
            or "signé après lecture" in stripped
            or "dressé le présent procès-verbal" in stripped
            or "il a été dressé le présent" in stripped
        ):
            start = index
            break
    # 2) FALLBACK par INTENTION (pas une liste de tournures — règle 68 2026-07-09) : si aucune ancre
    # n'est reconnue, le bloc signature est neanmoins la FIN du document (cloture de lettre « … prie
    # d'agréer … » + nom, ligne « ____ » + nom/qualité…). On protege la QUEUE : les ~6 derniers
    # paragraphes non vides. Couvre toute fin signee sans coder chaque formule de politesse.
    if start is None:
        non_empty = [i for i, p in enumerate(paras) if p.text.strip()]
        if len(non_empty) < 2:
            return False
        start = non_empty[max(0, len(non_empty) - 6)]
    # 3) BORNE au premier saut de page apres le debut : les statuts ont une ANNEXE apres le « Fait a »
    # -> le keepNext ne doit pas traverser le saut de page (sinon il tire l'annexe dans le bloc).
    end = len(paras)
    for index in range(start + 1, len(paras)):
        if paras[index].paragraph_format.page_break_before:
            end = index
            break
    for paragraph in paras[start : max(start, end - 1)]:
        paragraph.paragraph_format.keep_with_next = True
    return True


def add_statuts_annex_heading(
    document: Any,
    title: str,
    subtitle: str | None = None,
    *,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> list[Any]:
    paragraphs = [
        add_paragraph(
            document,
            title,
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            bold=True,
            space_before_pt=style_profile.notable_space_before_pt,
            style_profile=style_profile,
        )
    ]
    if subtitle:
        paragraphs.append(
            add_paragraph(
                document,
                subtitle,
                alignment=WD_ALIGN_PARAGRAPH.CENTER,
                bold=True,
                style_profile=style_profile,
            )
        )
    return paragraphs


def add_statuts_matrix_table(
    document: Any,
    headers: Sequence[str],
    rows: Sequence[Sequence[str]],
    *,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    table = document.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    _apply_table_grid_style(table)
    _set_table_borders(table)
    for cell, header in zip(table.rows[0].cells, headers, strict=True):
        paragraph = cell.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run(header)
        run.bold = True
    for row in rows:
        cells = table.add_row().cells
        for cell, value in zip(cells, row, strict=True):
            paragraph = cell.paragraphs[0]
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
            paragraph.add_run(value)
    add_spacer(document, space_after_pt=style_profile.standard_space_after_pt)
    return table


def add_spacer(document: Any, *, space_after_pt: int = 0) -> Any:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(space_after_pt)
    return paragraph


# Pied de page SYDEL des courriers (coordonnees stables, non saisies).
# Verbatim extrait du MODELE CLIENT courrier_cession_scm_modele.docx (footer F0-F2) :
# permet au destinataire (Service Departemental de l'Enregistrement) de contacter SYDEL.
# Roboto 6,5 pt centre ; ligne siege en bleu gras 315184, lignes legales en gris 808080.
_SYDEL_FOOTER_FONT_NAME = "Roboto"
_SYDEL_FOOTER_FONT_SIZE_PT = 6.5
_SYDEL_FOOTER_BLUE = RGBColor(0x31, 0x51, 0x84)
_SYDEL_FOOTER_GRAY = RGBColor(0x80, 0x80, 0x80)
_SYDEL_FOOTER_LINES: tuple[tuple[str, RGBColor, bool], ...] = (
    (
        "Siège social : 80 avenue Marceau, 75008 PARIS Tél : 01 53 81 43 03",
        _SYDEL_FOOTER_BLUE,
        True,
    ),
    (
        "SYDEL SARL au capital minimum de 500 000€, RCS Paris : 788 531 432 00029, "
        "Code APE/NAF : 6832 B – Membre de l’Anacofi CIF",
        _SYDEL_FOOTER_GRAY,
        False,
    ),
    (
        "ORIAS N°12069007 – TVA intracommunautaire : FR 18 788531432 - "
        "RC PRO : 2.101.395/OC100000394",
        _SYDEL_FOOTER_GRAY,
        False,
    ),
)


def add_sydel_letter_footer(document: Any) -> None:
    """Pose le pied de page coordonnees SYDEL sur la 1re section du courrier.

    Texte VERBATIM du modele client (coordonnees stables, non-saisies) pour que
    le Service Departemental de l'Enregistrement puisse contacter SYDEL (retour
    Albane lot 2, §8.4b). Reutilisable par d'autres courriers (ex. appel de fonds).
    """
    footer = document.sections[0].footer
    footer.is_linked_to_previous = False
    for index, (text, color, bold) in enumerate(_SYDEL_FOOTER_LINES):
        if index < len(footer.paragraphs):
            paragraph = footer.paragraphs[index]
        else:
            paragraph = footer.add_paragraph()
        paragraph.text = ""
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run(text)
        run.bold = bold
        run.font.name = _SYDEL_FOOTER_FONT_NAME
        run.font.size = Pt(_SYDEL_FOOTER_FONT_SIZE_PT)
        run.font.color.rgb = color


def add_framed_title(
    document: Any,
    lines: Sequence[str],
    *,
    inner_spacing: bool = False,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    table = document.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    _apply_table_grid_style(table)
    _set_table_borders(table)

    cell = table.cell(0, 0)
    _set_cell_margins(
        cell,
        top=style_profile.frame_cell_margin_vertical_dxa,
        bottom=style_profile.frame_cell_margin_vertical_dxa,
        left=style_profile.frame_cell_margin_horizontal_dxa,
        right=style_profile.frame_cell_margin_horizontal_dxa,
    )
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Albane 2026-06-26 §S5 : aerer l'INTERIEUR du cadre-titre (espace avant/apres le texte
    # dans la cellule). OPT-IN via `inner_spacing` (defaut False) pour rester byte-neutre sur
    # les 7 autres appelants (procuration, PV, bail...) ; seul l'acte de cession SCM l'active.
    if inner_spacing:
        paragraph.paragraph_format.space_before = Pt(style_profile.standard_space_after_pt)
        paragraph.paragraph_format.space_after = Pt(style_profile.standard_space_after_pt)
    for index, line in enumerate(lines):
        if index:
            paragraph.add_run("\n")
        run = paragraph.add_run(line)
        run.bold = True
        run.font.name = style_profile.font_name
        run.font.size = Pt(style_profile.font_size_pt)

    add_spacer(document)
    return table


def add_framed_section_title(
    document: Any,
    text: str,
    *,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    table = document.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    _apply_table_grid_style(table)
    _set_table_borders(table)

    cell = table.cell(0, 0)
    _set_cell_margins(
        cell,
        top=style_profile.frame_cell_margin_vertical_dxa,
        bottom=style_profile.frame_cell_margin_vertical_dxa,
        left=style_profile.frame_cell_margin_horizontal_dxa,
        right=style_profile.frame_cell_margin_horizontal_dxa,
    )
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
    run = paragraph.add_run(text)
    run.bold = True
    run.underline = True
    run.font.name = style_profile.font_name
    run.font.size = Pt(style_profile.font_size_pt)
    add_spacer(document, space_after_pt=style_profile.compact_space_after_pt)
    return table


def add_notice_box(
    document: Any,
    lines: Sequence[str],
    *,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    table = document.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    _apply_table_grid_style(table)
    _set_table_borders(table)
    cell = table.cell(0, 0)
    _set_cell_margins(
        cell,
        top=style_profile.frame_cell_margin_vertical_dxa,
        bottom=style_profile.frame_cell_margin_vertical_dxa,
        left=style_profile.frame_cell_margin_horizontal_dxa,
        right=style_profile.frame_cell_margin_horizontal_dxa,
    )
    for index, line in enumerate(lines):
        paragraph = cell.paragraphs[0] if index == 0 else cell.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
        paragraph.add_run(line)
    add_spacer(document, space_after_pt=style_profile.compact_space_after_pt)
    return table


def add_bordered_data_table(
    document: Any,
    headers: Sequence[str],
    rows: Sequence[Sequence[str]],
    *,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    table = document.add_table(rows=1, cols=len(headers))
    _apply_table_grid_style(table)
    _set_table_borders(table)
    for index, header in enumerate(headers):
        paragraph = table.rows[0].cells[index].paragraphs[0]
        paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
        paragraph.add_run(header).bold = True
    for row in rows:
        cells = table.add_row().cells
        for index, value in enumerate(row):
            paragraph = cells[index].paragraphs[0]
            paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
            paragraph.add_run(value)
    return table


def add_centered_block(
    document: Any,
    lines: Sequence[tuple[str, bool, bool] | str],
    *,
    space_after_pt: int | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> list[Any]:
    paragraphs = []
    for line in lines:
        if isinstance(line, str):
            text = line
            bold = False
            italic = False
        else:
            text, bold, italic = line
        paragraphs.append(
            add_paragraph(
                document,
                text,
                alignment=WD_ALIGN_PARAGRAPH.CENTER,
                bold=bold,
                italic=italic,
                space_after_pt=(
                    style_profile.compact_space_after_pt
                    if space_after_pt is None
                    else space_after_pt
                ),
                style_profile=style_profile,
            )
        )
    return paragraphs


def add_signature_block(
    document: Any,
    lines: Sequence[str],
    *,
    image_path: Path | None = None,
    framed: bool = False,
    width_cm: float | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    if framed:
        return add_framed_signature_block(
            document,
            lines,
            image_path=image_path,
            width_cm=width_cm,
            style_profile=style_profile,
        )
    return add_simple_signature_block(
        document,
        lines,
        image_path=image_path,
        width_cm=width_cm,
        style_profile=style_profile,
    )


def add_simple_signature_block(
    document: Any,
    lines: Sequence[str],
    *,
    image_path: Path | None = None,
    width_cm: float | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    add_spacer(document)
    paragraphs = [
        add_paragraph(
            document,
            line,
            alignment=WD_ALIGN_PARAGRAPH.RIGHT,
            space_after_pt=style_profile.compact_space_after_pt,
            style_profile=style_profile,
        )
        for line in lines
    ]

    signature_paragraph = document.add_paragraph()
    signature_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    signature_paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
    if image_path is not None:
        if not image_path.exists():
            raise ValueError(f"signature.image_optionnelle est introuvable : {image_path}")
        signature_paragraph.add_run().add_picture(
            str(image_path),
            width=Cm(width_cm or style_profile.signature_image_width_cm),
        )
    else:
        signature_paragraph.add_run("\n\n\n")
    paragraphs.append(signature_paragraph)
    return paragraphs


def add_framed_signature_block(
    document: Any,
    lines: Sequence[str],
    *,
    image_path: Path | None = None,
    width_cm: float | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    add_spacer(document)
    table = document.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.RIGHT
    _apply_table_grid_style(table)
    _set_table_borders(table)
    cell = table.cell(0, 0)
    cell.width = Cm(width_cm or style_profile.signature_width_cm)
    _set_cell_margins(
        cell,
        top=style_profile.signature_cell_margin_vertical_dxa,
        bottom=style_profile.signature_cell_margin_vertical_dxa,
        left=style_profile.signature_cell_margin_horizontal_dxa,
        right=style_profile.signature_cell_margin_horizontal_dxa,
    )
    _add_signature_cell_content(cell, lines, image_path, style_profile)
    return table


def add_framed_address_block(
    document: Any,
    lines: Sequence[str],
    *,
    width_cm: float = 7.5,
    drop_top_cm: float = 0.0,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    """Bloc DESTINATAIRE encadre et aligne a droite, pour enveloppe a fenetre.

    R2 (Albane 2026-06-30) : le destinataire d'un courrier doit tenir dans un ENCADRE
    (boite bordee) afin d'apparaitre dans la fenetre d'une enveloppe a fenetre, et etre
    DESCENDU a la hauteur de la fenetre. Helper additif (n'impacte aucun appelant
    existant) :

    - `width_cm` : largeur de la boite (cale a droite via `WD_TABLE_ALIGNMENT.RIGHT`,
      « le côté me paraît bien » = on garde le calage a droite actuel).
    - `drop_top_cm` : hauteur du spacer pose AVANT la boite pour la descendre a la
      hauteur de la fenetre standard FR. 0 = pas de descente. La cote exacte est
      pilotee par l'appelant (defaut documente cote appelant, a valider sur rendu).
    """
    if drop_top_cm > 0:
        spacer = document.add_paragraph()
        spacer.paragraph_format.space_after = Pt(0)
        spacer.paragraph_format.space_before = Pt(0)
        # python-docx ne sait pas poser une hauteur de paragraphe directement ; on
        # convertit la descente voulue (cm) en espace-avant en points (1 cm = 28.35 pt)
        # sur un paragraphe vide -> pousse le bloc destinataire vers le bas.
        spacer.paragraph_format.space_before = Pt(round(drop_top_cm * 28.35))
    table = document.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.RIGHT
    _apply_table_grid_style(table)
    _set_table_borders(table)
    cell = table.cell(0, 0)
    cell.width = Cm(width_cm)
    _set_cell_margins(
        cell,
        top=style_profile.frame_cell_margin_vertical_dxa,
        bottom=style_profile.frame_cell_margin_vertical_dxa,
        left=style_profile.frame_cell_margin_horizontal_dxa,
        right=style_profile.frame_cell_margin_horizontal_dxa,
    )
    first_paragraph = cell.paragraphs[0]
    for index, text in enumerate(lines):
        paragraph = first_paragraph if index == 0 else cell.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
        run = paragraph.add_run(text)
        run.font.name = style_profile.font_name
        run.font.size = Pt(style_profile.font_size_pt)
    return table


def add_signature_lines(
    document: Any,
    names: Sequence[str],
    *,
    alignment: WD_ALIGN_PARAGRAPH | None = None,
    bold: bool = False,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> list[Any]:
    return [
        add_paragraph(
            document,
            name,
            alignment=alignment,
            bold=bold,
            style_profile=style_profile,
        )
        for name in names
    ]


def add_signature_table(
    document: Any,
    labels: Sequence[Sequence[str]],
    *,
    min_row_height_cm: float | None = None,
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> Any:
    if not labels or not labels[0]:
        raise ValueError("labels doit contenir au moins une cellule de signature.")
    column_count = len(labels[0])
    table = document.add_table(rows=len(labels), cols=column_count)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    _apply_table_grid_style(table)
    _set_table_borders(table)
    for row_index, row in enumerate(labels):
        if len(row) != column_count:
            raise ValueError("Toutes les lignes de signature doivent avoir la meme largeur.")
        # min_row_height_cm optionnel (defaut None -> aucune contrainte, rendu
        # inchange pour tous les appelants existants). Quand fourni, agrandit le
        # cadre de signature pour laisser une zone manuscrite/YouSign suffisante
        # (§4.2 : cadre du PV SCM trop petit). Bordures conservees.
        if min_row_height_cm is not None:
            table_row = table.rows[row_index]
            table_row.height = Cm(min_row_height_cm)
            table_row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        for cell_index, label in enumerate(row):
            cell = table.rows[row_index].cells[cell_index]
            _set_cell_margins(
                cell,
                top=style_profile.signature_cell_margin_vertical_dxa,
                bottom=style_profile.signature_cell_margin_vertical_dxa,
                left=style_profile.signature_cell_margin_horizontal_dxa,
                right=style_profile.signature_cell_margin_horizontal_dxa,
            )
            paragraph = cell.paragraphs[0]
            paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
            paragraph.add_run(label)
            cell.add_paragraph("\n\n\n")
    return table


def add_legal_reminder(
    document: Any,
    *,
    title: str,
    title_suffix: str,
    paragraphs: Sequence[str],
    style_profile: SydelDocxStyleProfile = DEFAULT_STYLE_PROFILE,
) -> None:
    add_spacer(document)

    title_paragraph = document.add_paragraph()
    title_paragraph.paragraph_format.space_after = Pt(style_profile.legal_reminder_space_after_pt)
    title_paragraph.style = document.styles["Normal"]
    reminder = title_paragraph.add_run(title)
    reminder.italic = True
    reminder.underline = True
    suffix = title_paragraph.add_run(title_suffix)
    suffix.italic = True

    for text in paragraphs:
        add_paragraph(
            document,
            text,
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
            italic=True,
            space_after_pt=style_profile.legal_reminder_space_after_pt,
            style_profile=style_profile,
        )


def _add_signature_cell_content(
    cell: Any,
    lines: Sequence[str],
    image_path: Path | None,
    style_profile: SydelDocxStyleProfile,
) -> None:
    first_paragraph = cell.paragraphs[0]
    for index, text in enumerate(lines):
        paragraph = first_paragraph if index == 0 else cell.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        paragraph.paragraph_format.space_after = Pt(style_profile.compact_space_after_pt)
        paragraph.add_run(text)

    signature_paragraph = cell.add_paragraph()
    signature_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if image_path is not None:
        if not image_path.exists():
            raise ValueError(f"signature.image_optionnelle est introuvable : {image_path}")
        signature_paragraph.add_run().add_picture(
            str(image_path),
            width=Cm(style_profile.signature_image_width_cm),
        )
    else:
        signature_paragraph.add_run("\n\n\n")


def _set_cell_margins(
    cell: Any,
    *,
    top: int = 0,
    bottom: int = 0,
    left: int = 0,
    right: int = 0,
) -> None:
    """Set internal cell margins (padding) in dxa/twips via ``w:tcMar``.

    Additif uniquement : aere l'interieur des cadres (cellules de tableau 1x1)
    sans toucher aux bordures. 1 pt = 20 dxa. Toute valeur a 0 est posee
    explicitement pour rendre la marge deterministe.
    """
    tc_pr = cell._tc.get_or_add_tcPr()
    existing = tc_pr.find(qn("w:tcMar"))
    if existing is not None:
        tc_pr.remove(existing)

    tc_mar = OxmlElement("w:tcMar")
    for edge, value in (
        ("top", top),
        ("start", left),
        ("left", left),
        ("bottom", bottom),
        ("end", right),
        ("right", right),
    ):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:w"), str(value))
        element.set(qn("w:type"), "dxa")
        tc_mar.append(element)
    tc_pr.append(tc_mar)


def _apply_table_grid_style(table: Any) -> None:
    """Applique le style nomme « Table Grid » UNIQUEMENT s'il existe dans le document.

    R1 (2026-06-30) : depuis ``new_document_from_model``, un document peut heriter du
    styles.xml d'un modele client qui ne definit PAS « Table Grid » (cas SCI / SCI IRIS /
    SCS / SCM). Affecter un style absent leve une erreur. Le quadrillage VISIBLE est de toute
    facon pose explicitement par ``_set_table_borders`` (bordures XML), donc l'absence du
    style nomme ne change pas le rendu. Garde-fou : on n'affecte le style que s'il est present
    (cas du ``Document()`` vierge et du modele micro holding), sinon on s'appuie sur les
    bordures explicites -> comportement inchange pour les appelants existants.
    """
    if "Table Grid" in {style.name for style in table.part.document.styles}:
        table.style = "Table Grid"


def _set_table_borders(table: Any) -> None:
    tbl_pr = table._tbl.tblPr
    existing_borders = tbl_pr.first_child_found_in("w:tblBorders")
    if existing_borders is not None:
        tbl_pr.remove(existing_borders)

    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), "4")
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), "000000")
        borders.append(element)
    tbl_pr.append(borders)


def _clear_table_borders(table: Any) -> None:
    tbl_pr = table._tbl.tblPr
    existing_borders = tbl_pr.first_child_found_in("w:tblBorders")
    if existing_borders is not None:
        tbl_pr.remove(existing_borders)

    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "nil")
        element.set(qn("w:sz"), "0")
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), "FFFFFF")
        borders.append(element)
    tbl_pr.append(borders)
