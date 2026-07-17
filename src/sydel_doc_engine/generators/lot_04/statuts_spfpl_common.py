from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from unicodedata import normalize

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
from sydel_doc_engine.generators.lot_01.civilite import civilite_civile
from sydel_doc_engine.generators.lot_05.scm_cession_common import (
    mentions_conjoint,
    mentions_partenaire_pacse,
    partenaire_pacse_clause,
)
from sydel_doc_engine.rendering.docx_builder import (
    STATUTS_SPFPL_COMPACT_STYLE_PROFILE,
    add_paragraph,
    add_spacer,
    add_statuts_article_heading,
    add_statuts_body_paragraph,
    add_statuts_hanging_list_item,
    add_statuts_part_heading,
    add_statuts_signature_block,
    add_statuts_title_box,
    new_document,
)
from sydel_doc_engine.utils.grammar import (
    accord_euros_apres_montant,
    integer_to_french_words,
)

DOCUMENT_CODE = "CODE-STATUTS-SPFPL-001"
# M2 (Akainu doc-entier 2026-07-09) : espacement COMPACT du bloc identite (soussigne +
# nomination President), aligne sur le PV de nomination (bloc identite a 2pt) — coherence.
_IDENTITY_BLOCK_SPACE_AFTER_PT = 2
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
    # KAN-2 : date manquante -> marqueur « (À COMPLÉTER : …) », non bloquant (R10).
    if value is None:
        return f"(À COMPLÉTER : {field_name})"
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return required_text(value, field_name)


# KAN-2 (Rafael) : un OBJET manquant NE bloque PAS la generation. On retourne une INSTANCE VIDE
# (tous champs None) : ses champs sortiront en marqueurs « (À COMPLÉTER : …) » via required_text /
# quantite_titres. Le client veut generer meme sans AUCUN champ rempli — zero blocage, jamais de
# ValueError sur une donnee absente (une contrainte technique ne devient pas une limite produit).
def required_societe_spfpl(ctx: DocumentGenerationContext) -> SocieteSpfpl:
    return ctx.societe_spfpl if ctx.societe_spfpl is not None else SocieteSpfpl()


def required_capital_souscription(ctx: DocumentGenerationContext) -> CapitalSouscription:
    return ctx.capital_souscription if ctx.capital_souscription is not None else CapitalSouscription()


def required_apport_titres(ctx: DocumentGenerationContext) -> ApportTitres:
    return ctx.apport_titres if ctx.apport_titres is not None else ApportTitres()


def required_societe_cible(ctx: DocumentGenerationContext) -> SocieteCible:
    return ctx.societe_cible if ctx.societe_cible is not None else SocieteCible()


def required_actionnaire_unique(ctx: DocumentGenerationContext) -> SpfplPerson:
    if ctx.actionnaire_unique is not None:
        return ctx.actionnaire_unique
    if ctx.operation_spfpl and ctx.operation_spfpl.type == OPERATION_CESSION and ctx.cedant:
        return ctx.cedant
    if ctx.operation_spfpl and ctx.operation_spfpl.type == OPERATION_APPORT and ctx.apporteur:
        return ctx.apporteur
    return SpfplPerson()


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
    # M2 (Akainu doc-entier 2026-07-09) : le bloc identite (name line « - [civilite] … [nom] »
    # + lignes civiles qui suivent : profession, naissance, adresse, situation maritale,
    # nationalite, inscription) est COMPACTE a 2pt. Le flag reste actif tant qu'on enchaine des
    # lignes d'identite ; toute autre ligne (titre, article, liste, signature) le remet a False.
    in_identity_block = False
    while index < len(blocks):
        block = blocks[index]
        text = replace_placeholders(block, replacements)
        continues_identity = False
        if index < title_block_count:
            # FIX-F1 / STYLE-1 : bloc de titre (denomination / sous-titre / capital / siege)
            # centre dans la source ; la 1re ligne (denomination) est en gras (style Heading 3).
            # S1 (Rafael 2026-07-09) : AUCUN espace entre les lignes de l'en-tete (comme le
            # modele source) -> space_after=0 (l'en-tete est un bloc compact).
            add_paragraph(
                docx,
                text,
                alignment=WD_ALIGN_PARAGRAPH.CENTER,
                bold=(index == 0),
                space_after_pt=0,
                style_profile=style_profile,
            )
        elif text == "STATUTS":
            # S2 (Rafael 2026-07-09) : « STATUTS » dans un ENCADRE (lisibilite), place un peu
            # PLUS BAS que l'en-tete (espaceur avant), PUIS un SAUT DE PAGE pour commencer le
            # deroule de l'acte (comparution + articles) sur une nouvelle page. Le meme encadre
            # partage (add_statuts_title_box) que les statuts SEL/civils -> rendu homogene.
            add_spacer(docx, space_after_pt=10)
            add_statuts_title_box(docx, "STATUTS", style_profile=style_profile)
            docx.add_page_break()
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
            if heading_lines[0] in _SECTION_GROUP_BANNERS:
                # KAN-3 (Albane 2026-07-13) : les bandeaux ENCADRES de groupe de sections
                # etaient INCOHERENTS — presents a partir de « DECISIONS DES ACTIONNAIRES »
                # (apres l'art. 22) mais absents en tete et avant l'art. 19. Albane : « ou on
                # les supprime tous, peu importe mais la ce n'est pas coherent ». Ajouter les
                # manquants exigerait d'INVENTER des intitules de section (decision metier) ;
                # on retient donc la suppression (autorisee explicitement). L'espacement
                # inter-articles existant (notable_space_before_pt) devient l'« espace entre
                # chaque article » homogene qu'Albane demande a la place des cadres.
                pass
            else:
                # S5 (Rafael 2026-07-09) : la partie « ANNEXE » (seul titre majeur restant)
                # demarre sur une NOUVELLE PAGE (saut de page avant l'encadre de l'annexe).
                if heading_lines[0].startswith("ANNEXE"):
                    docx.add_page_break()
                _add_major_heading_box(docx, heading_lines, style_profile=style_profile)
        elif _is_article_heading(text):
            # S4 (Rafael 2026-07-09) : detection ROBUSTE au separateur — l'art. 26 source
            # porte « ARTICLE\t26 » (tabulation, pas espace) ; l'ancienne garde
            # `startswith("ARTICLE ")` (espace) le manquait -> il tombait en paragraphe de
            # corps (ni gras ni style de titre). On matche « ARTICLE » suivi de tout blanc.
            add_statuts_article_heading(docx, text, underline=False, style_profile=style_profile)
        elif text.startswith("Fait à ") or text.startswith("Fait a "):
            in_identity_block = False
            index = _add_signature_split(
                docx,
                blocks,
                replacements,
                index,
                style_profile=style_profile,
            )
            continue
        elif _is_soussigne_line(block):
            # FIX-F2 / STYLE-2 : "Le soussigne :" est souligne dans la source (JUSTIFY + souligne).
            # S3 (Rafael 2026-07-09) : pas d'espacement superflu apres la ligne « Le soussigne »
            # -> space_after=0 (la comparution enchaine immediatement).
            add_paragraph(
                docx,
                text,
                alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                underline=True,
                space_after_pt=0,
                style_profile=style_profile,
            )
        elif _is_identity_line(block):
            # FIX-F3 / STYLE-3 : la ligne d'identite "- [civilite] [prenom(s)] [nom]" est en gras
            # (run unique incl. le tiret) et JUSTIFY dans la source, pas un item de liste.
            # M2 : la name line OUVRE le bloc identite compact (2pt).
            add_paragraph(
                docx,
                text,
                alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                bold=True,
                space_after_pt=_IDENTITY_BLOCK_SPACE_AFTER_PT,
                style_profile=style_profile,
            )
            continues_identity = True
        elif block in _BOLD_CAPITAL_BLOCKS:
            # FIX-F3 / STYLE-4 : lignes de capital / total (Art. 6 & 8) en gras dans la source.
            _add_bold_segments_paragraph(docx, block, replacements, style_profile=style_profile)
        elif text.startswith("- "):
            add_statuts_hanging_list_item(docx, text[2:], style_profile=style_profile)
        elif _looks_like_numbered_list_item(text):
            add_statuts_hanging_list_item(docx, text, marker=None, style_profile=style_profile)
        elif in_identity_block:
            # M2 : lignes civiles du bloc identite (profession, naissance, adresse, situation
            # maritale, nationalite, inscription ordre) -> corps JUSTIFY compacte a 2pt.
            add_paragraph(
                docx,
                text,
                alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                space_after_pt=_IDENTITY_BLOCK_SPACE_AFTER_PT,
                style_profile=style_profile,
            )
            continues_identity = True
        else:
            add_statuts_body_paragraph(docx, text, style_profile=style_profile)
        in_identity_block = continues_identity
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
# Cession Art. 8 : "- [civilite_apport] [prenom] [nom]" en gras, le bourrage de points et "[nb]
# actions" non gras (source : runs idx116 / idx117). Apport Art. 8 : ligne entiere en gras (source
# idx127 / idx128). Cession Art. 6 "Total des apports\t..." : ligne entiere en gras (source idx106).
# R3 « supprimer PARTOUT » (Rafael 2026-07-09) : « - Le Docteur … » -> « - [civilite_apport] … »
# (Monsieur/Madame accorde au genre, sans article) — le token remplace le literal « Le Docteur ».
_BOLD_CAPITAL_SEGMENTS: dict[str, tuple[tuple[bool, str], ...]] = {
    # Cession Art. 6 — total des apports (run unique en gras dans la source)
    "Total des apports\t\t\t\t\t\t\t\t\t[montant_apport]": (
        (True, "Total des apports\t\t\t\t\t\t\t\t\t[montant_apport]"),
    ),
    # Cession Art. 8 — repartition (gras sur l'identite uniquement)
    "- [civilite_apport] [prenom] [nom]………………………………………….…….………..[nb_actions] actions": (
        (True, "- [civilite_apport] [prenom] [nom]"),
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
    "- [civilite_apport] [prenom] [nom]………………………………………….……………..[nb_actions] actions": (
        (True, "- [civilite_apport] [prenom] [nom]………………………………………….……………..[nb_actions] actions"),
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
    # Accord euro/euros (Rafael 2026-07-09, « partout = partout ») : l'unite « euros »
    # est FIGEE dans les blocs sources SPFPL (« Au capital de [capital_social] euros »,
    # « fixé à la somme d'un ([capital_social]) euros ») -> accordee « 1 euro » quand la
    # valeur substituee est singuliere (0/1). Le pluriel n'est jamais touche.
    return accord_euros_apres_montant(rendered)


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
    # B1 (Akainu doc-entier 2026-07-09) : `regime_matrimonial` accentue + preposition unique via
    # `_regime_matrimonial_display` (plus de « sous le régime de regime de communaute »).
    return _capitalize_first(
        f"{statut} sous le régime de {_regime_matrimonial_display(regime_matrimonial)} avec "
        f"{civilite_conjoint} {prenom_conjoint} {nom_conjoint}"
    )


def _regime_matrimonial_display(value: str) -> str:
    """Libelle ACCENTUE du regime matrimonial pour la clause « sous le régime de … » des
    statuts SPFPL cession. Meme PATRON que les statuts SEL
    (statuts_sel_exercice_common.matrimonial_regime_display / statuts_sel_matrimonial_regime) :
    on mappe vers la forme accentuee, avec strip d'un eventuel prefixe « (sous le )régime de »
    en repli.

    B1 (Akainu doc-entier 2026-07-09) : la valeur BRUTE posee par
    field_derivations.regime_matrimonial_from_status (« regime de communaute »,
    « separation de biens », « communaute universelle », « participation aux acquets »)
    partait telle quelle apres « sous le régime de » -> preposition DOUBLEE
    (« de regime de communaute ») + accents perdus. Pour la SPFPL, une communaute NON
    universelle est TOUJOURS la communaute LEGALE (le regime communautaire du menu ne
    capture que le regime legal ; l'universelle porte son propre libelle) -> « la communauté
    légale ».
    """
    normalized = normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = " ".join(normalized.lower().split())
    if "separation" in normalized and "bien" in normalized:
        return "la séparation de biens"
    if "communaute" in normalized and "universelle" in normalized:
        return "la communauté universelle"
    if "communaute" in normalized:
        return "la communauté légale"
    if "participation" in normalized and "acquet" in normalized:
        return "la participation aux acquêts"
    for prefix in ("sous le régime de ", "sous le regime de ", "régime de ", "regime de "):
        if value.lower().startswith(prefix):
            return value[len(prefix) :].strip()
    return value


def _situation_maritale_avec_conjoint(founder: SpfplPerson, field_name: str) -> str:
    """Statut matrimonial + conjoint/partenaire, SANS regime (Rafael 2026-07-09).

    Retour Rafael 2026-07-09 (statuts SPFPL apport, comparution) : « Marié » nu ->
    « Marié avec {Prénom Nom} » (« pas de mention sans nom »). Meme wording que le
    contrat d'apport (DOC-041, cle modele « [situation_maritale] avec [nom_conjoint] » :
    prenom + nom, sans civilite). Branche via les gardes PARTAGEES :
      - MARIE (`mentions_conjoint`) -> « Marié avec <prenom nom> » (required_text :
        conjoint absent -> marqueur visible, fail-loud, le front l'exige de toute facon) ;
      - PACSE (`mentions_partenaire_pacse`) -> clause partenaire ratifiee Albane 6.3/7.3
        (« Pacsé avec {Civilite Prenom Nom} », "" si non renseigne) ;
      - AUTRE -> statut seul.
    M1 (7.2) : 1re lettre en MAJUSCULE, comme chaque element de la liste du soussigne.
    Remplace le bare [situation_maritale] aux 3 blocs liste des statuts SPFPL
    (comparution apport + nomination du President apport/cession — propagation
    regle 68 Q4 : meme surface « bloc liste identite », meme intention).
    """
    statut = required_text(founder.situation_maritale, f"{field_name}.situation_maritale")
    if mentions_conjoint(founder.situation_maritale):
        conjoint = founder.conjoint
        prenom = required_text(
            conjoint.prenom if conjoint else None, f"{field_name}.conjoint.prenom"
        )
        nom = required_text(conjoint.nom if conjoint else None, f"{field_name}.conjoint.nom")
        return _capitalize_first(f"{statut} avec {prenom} {nom}")
    if mentions_partenaire_pacse(founder.situation_maritale):
        return _capitalize_first(f"{statut}{partenaire_pacse_clause(founder.conjoint)}")
    return _capitalize_first(statut)


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
    # R3 « supprimer PARTOUT » (Rafael 2026-07-09) : « Docteur »/« Dr » n'est jamais une
    # civilite dans la sortie. La comparution (« - [civilite] Prenom Nom ») ET la phrase
    # d'apport/repartition (anciennement « Le Docteur Prenom Nom », literal des templates,
    # cf. [civilite_apport]) passent par la civilite CIVILE (Monsieur/Madame accorde au genre).
    civilite = civilite_civile(founder.civilite_affichage, founder.genre)
    return {
        "[civilite]": required_text(
            civilite,
            f"{field_name}.civilite_affichage",
        ),
        # R3 : remplace le literal « Le Docteur » des templates d'apport/repartition (SPFPL
        # cession art. 6 + art. 8, SPFPL apport art. 8). Monsieur/Madame ne prend PAS d'article
        # (« Monsieur X apporte », pas « le Monsieur X ») -> le « Le » literal est retire des
        # templates en meme temps que « Docteur ».
        "[civilite_apport]": civilite,
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
        # matrimonial SEUL. 7.2 exige une MAJUSCULE en tete de chaque element ->
        # « Célibataire », « Marié ». Conserve pour compatibilite (plus reference par les
        # templates SPFPL depuis Rafael 2026-07-09 — remplace par le token _avec_conjoint).
        "[situation_maritale]": _capitalize_first(
            required_text(
                founder.situation_maritale,
                f"{field_name}.situation_maritale",
            )
        ),
        # Rafael 2026-07-09 : statut + conjoint/partenaire SANS regime (« Marié avec
        # Marine Le Painnisse ») pour les blocs liste (comparution apport + nomination
        # du President). NB substring-safe : « [situation_maritale] » (crochet fermant)
        # n'est PAS un sous-texte de ce token.
        "[situation_maritale_avec_conjoint]": _situation_maritale_avec_conjoint(
            founder, field_name
        ),
        # Ligne de comparution matrimoniale BRANCHEE (marie -> ligne complete AVEC
        # regime ; sinon -> juste le statut). Seul le modele CESSION porte ce token.
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


# KAN-3 (Albane 2026-07-13) : bandeaux ENCADRES de groupe de sections a SUPPRIMER (incoherents).
# L'annexe (« ANNEXE 1 » / « ETAT DES ENGAGEMENTS… » / « LA CONSTITUTION DE LA SOCIETE ») N'EST
# PAS un bandeau de groupe : c'est le titre d'une partie distincte (saut de page) -> conserve.
_SECTION_GROUP_BANNERS = frozenset(
    {
        "DECISIONS DES ACTIONNAIRES",
        "RESULTATS SOCIAUX",
        "TRANSFORMATION DE LA SOCIETE",
        "DISSOLUTION – LIQUIDATION",
        "CONTESTATIONS",
        "CONSTITUTION DE LA SOCIETE",
    }
)


def _is_major_heading(text: str) -> bool:
    headings = _SECTION_GROUP_BANNERS | {
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


_ARTICLE_HEADING_RE = re.compile(r"ARTICLE\s")


def _is_article_heading(text: str) -> bool:
    """Un titre d'article = « ARTICLE » suivi d'un blanc (espace, tabulation ou insecable).

    S4 (Rafael 2026-07-09) : l'art. 26 des modeles SPFPL porte « ARTICLE\t26 » (tabulation) ;
    la garde `startswith("ARTICLE ")` (espace seul) le manquait et il n'etait pas mis en gras.
    `\\s` couvre l'espace, la tabulation et l'insecable (mode Unicode) -> tous les titres, quel
    que soit le separateur source, passent par le style de titre d'article (gras)."""
    return bool(_ARTICLE_HEADING_RE.match(text))


def _is_fait_ou_le_line(line: str) -> bool:
    """Ligne de datation du bloc signature (« Fait a <lieu> » / « Le [<date>] »)."""
    return (
        line.startswith("Fait à ")
        or line.startswith("Fait a ")
        or line == "Le"
        or line.startswith("Le ")
    )


def _add_signature_split(
    docx,  # noqa: ANN001 - type docx interne python-docx
    blocks: tuple[str, ...],
    replacements: dict[str, str],
    start_index: int,
    *,
    style_profile,  # noqa: ANN001
) -> int:
    """Bloc signature de la DERNIERE PAGE (S5, Rafael 2026-07-09).

    « Fait a … » et « Le … » alignes a GAUCHE ; la signature du client (nom) et la mention
    « Bon pour acceptation … » alignees a DROITE (meme zone de signature). Retourne l'index
    du prochain bloc a traiter (les lignes de signature/mention sont consommees ici)."""
    signature_lines, mention_lines, next_index = _collect_signature_lines(
        blocks, replacements, start_index
    )
    rendered_paras: list = []
    for line in signature_lines:
        if _is_fait_ou_le_line(line):
            rendered_paras += add_statuts_signature_block(
                docx,
                [line],
                alignment=WD_ALIGN_PARAGRAPH.LEFT,
                style_profile=style_profile,
            )
        else:
            rendered_paras += add_statuts_signature_block(
                docx,
                [line],
                alignment=WD_ALIGN_PARAGRAPH.RIGHT,
                bold=True,
                style_profile=style_profile,
            )
    for line in mention_lines:
        rendered_paras += add_statuts_signature_block(
            docx,
            [],
            mention_lines=[line],
            alignment=WD_ALIGN_PARAGRAPH.RIGHT,
            style_profile=style_profile,
        )
    # KAN-36 : tout le bloc signature (« Fait a / Le » + nom + « Bon pour acceptation ») reste
    # solidaire sur une seule page — keepNext sur chaque paragraphe sauf le dernier.
    for paragraph in rendered_paras[:-1]:
        paragraph.paragraph_format.keep_with_next = True
    return next_index


def _looks_like_numbered_list_item(text: str) -> bool:
    return len(text) > 2 and text[0].isdigit() and text[1] in {"°", "."}
