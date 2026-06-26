# ruff: noqa: E501
from __future__ import annotations

from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.shared import Pt

from sydel_doc_engine.domain.models import DocumentGenerationContext, ScmCessionAssocie
from sydel_doc_engine.generators.lot_05.scm_cession_common import (
    add_body_paragraph,
    add_heading,
    address_display,
    associe_display,
    cedant_display,
    format_display_date,
    required_text,
    save_clean_document,
    validate_pv_context,
)
from sydel_doc_engine.rendering.docx_builder import (
    add_framed_title,
    add_hyphen_list_item,
    add_paragraph,
    add_signature_table,
    add_spacer,
    new_document,
)

OUTPUT_FILENAME = "pv_age_cession_parts_scm.docx"

# Mise en forme (Albane 2026-06-17, §1) : aerer le PV SCM, juge trop serre.
# Espace avant chaque grande resolution (meme valeur que l'acte SCM §13.1 pour
# rester coherent) + spacers entre les grands blocs (entete<->corps, avant la
# signature). Local au PV : n'affecte ni l'acte ni le courrier SCM.
_RESOLUTION_SPACE_BEFORE_PT = 12
_BLOCK_SPACER_PT = 10

# Albane 2026-06-26 §P5 : numero de l'article des statuts modifie par la nouvelle repartition
# du capital. Reste « 7 » (gold V1) ; il est SURLIGNE dans la 2e resolution pour signaler un
# champ variable a adapter selon les statuts.
_ARTICLE_REPARTITION = "7"

# Albane 2026-06-26 §P2 : « mettre de l'espace entre les paragraphes ». On aere le corps du PV
# (espace apres chaque paragraphe superieur au standard 6 pt). Local au PV : n'affecte ni
# l'acte ni le courrier SCM (ils ne passent pas ce parametre).
_PARAGRAPH_SPACE_AFTER_PT = 8


def _body(document, text: str, *, bold: bool = False, italic: bool = False) -> None:
    # §P2 — wrapper local : chaque paragraphe de corps du PV est aere (space_after dedie).
    add_body_paragraph(
        document,
        text,
        bold=bold,
        italic=italic,
        space_after_pt=_PARAGRAPH_SPACE_AFTER_PT,
    )


class PvAgeCessionScmGenerator:
    """Generateur from-scratch du PV AGE de cession de parts SCM V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        scm_cession = validate_pv_context(ctx)
        scm_cedee = scm_cession.scm_cedee
        cessionnaire = scm_cession.cessionnaire
        agrement = scm_cession.agrement
        if scm_cedee is None or cessionnaire is None or agrement is None:
            raise ValueError("scm_cession est incomplet pour le PV AGE cession SCM.")

        document = new_document()
        add_paragraph(
            document,
            required_text(scm_cedee.denomination, "scm_cession.scm_cedee.denomination"),
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            bold=True,
            space_after_pt=2,
        )
        add_paragraph(
            document,
            "Société civile de moyens",
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            space_after_pt=2,
        )
        add_paragraph(
            document,
            f"Au capital de {required_text(scm_cedee.capital_social, 'scm_cession.scm_cedee.capital_social')} €",
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            space_after_pt=2,
        )
        add_paragraph(
            document,
            f"Siège social : {address_display(scm_cedee.siege, 'scm_cession.scm_cedee.siege')}",
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            space_after_pt=2,
        )
        add_paragraph(
            document,
            (
                f"RCS de {required_text(scm_cedee.ville_rcs, 'scm_cession.scm_cedee.ville_rcs')} "
                f"sous le n° {required_text(scm_cedee.numero_rcs, 'scm_cession.scm_cedee.numero_rcs')}"
            ),
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
        )
        add_framed_title(
            document,
            [
                "PROCES-VERBAL DES DECISIONS",
                "DE L'ASSEMBLEE GENERALE EXTRAORDINAIRE",
                f"DU {format_display_date(agrement.date_pv, 'scm_cession.agrement.date_pv')}",
            ],
        )

        # §1 — aeration : espace entre le cadre de titre et le corps du PV.
        add_spacer(document, space_after_pt=_BLOCK_SPACER_PT)
        _body(
            document,
            f"L'an {required_text(agrement.date_pv_lettres, 'scm_cession.agrement.date_pv_lettres')}",
        )
        _body(
            document,
            (
                f"Les associés de la {required_text(scm_cedee.denomination, 'scm_cession.scm_cedee.denomination')}, "
                f"au capital de {required_text(scm_cedee.capital_social, 'scm_cession.scm_cedee.capital_social')} euros, "
                f"composé de {scm_cedee.nb_parts_total} parts de "
                f"{required_text(scm_cedee.valeur_nominale_part, 'scm_cession.scm_cedee.valeur_nominale_part')} euros chacune, "
                "se sont réunis sur convocation régulière de la gérance au siège de la Société."
            ),
        )
        _body(document, "Sont présents ou représentés :")
        for index, associe in enumerate(scm_cession.associes_presents, start=1):
            parts = associe.parts
            if parts is None:
                raise ValueError("associe present sans parts.")
            _body(
                document,
                f"{index}° {associe_display(associe, f'scm_cession.associes_presents[{index - 1}]')}, détenant {parts.nb} parts sociales",
            )
        _body(
            document,
            "Les associés présents ou représentés disposent ensemble la totalité des parts formant le capital de la société. L'assemblée est habilitée à prendre les décisions extraordinaires.",
        )
        # §4.1 — le president de seance (gerant associe) est le DERNIER associe
        # present, derive du nombre reel d'associes saisis et non d'un index fixe
        # (l'ancien code codait associes_presents[2], qui levait IndexError des
        # qu'il y avait moins de 3 associes presents). Conventionnellement, le
        # gerant associe figure en derniere position de la liste des presents
        # (rendu byte-identique pour la fixture de demo a 3 associes : [-1] == [2]).
        if not scm_cession.associes_presents:
            raise ValueError("scm_cession.associes_presents est obligatoire pour le PV AGE cession SCM.")
        president_index = len(scm_cession.associes_presents) - 1
        president = scm_cession.associes_presents[president_index]
        # Albane 2026-06-26 §P3a : la qualite du president de seance s'accorde au SEXE du
        # president (« gerante associee » si femme, « gerant associe » si homme). Le sexe est
        # derive de la civilite d'affichage deja saisie (« Madame » -> feminin), pas d'un champ
        # nouveau.
        qualite_president = (
            "gérante associée"
            if _est_feminin(president.civilite_affichage)
            else "gérant associé"
        )
        _body(
            document,
            (
                f"{associe_display(president, f'scm_cession.associes_presents[{president_index}]')} "
                f"préside la séance en qualité de {qualite_president}."
            ),
        )
        _body(
            document,
            "Le Président dépose et met à la disposition des associés les documents suivants :",
        )
        # Liste A (puces tiret) : documents deposes par le President (retour UAT Rafael).
        for item in [
            "Les copies des convocations des associés ;",
            "Un exemplaire du compromis de cession des parts sociales ;",
            "Le rapport de la gérance ;",
            "Le texte des résolutions proposées.",
        ]:
            add_hyphen_list_item(document, item, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
        for text in [
            "Le Président déclare que tous les documents prévus par la réglementation et les statuts ont bien été adressés aux associés avec la convocation.",
            "Ils ont été tenus à leur disposition au siège social pendant le délai de quinze jours ayant précédé l'assemblée.",
            "L'assemblée lui donne acte de ses déclarations et reconnaît la validité de la convocation.",
            "Puis le Président rappelle l'ordre du jour :",
        ]:
            _body(document, text)
        # Liste B (puces tiret) : ordre du jour (retour UAT Rafael).
        for item in [
            "Lecture du rapport de la gérance ;",
            f"Agrément d'un nouvel associé, la {required_text(cessionnaire.denomination, 'scm_cession.cessionnaire.denomination')} ;",
            "Modification corrélative des statuts.",
        ]:
            add_hyphen_list_item(document, item, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
        for text in [
            "Le président donne lecture aux associés du rapport de la gérance.",
            "Une discussion sans débat s'engage entre les associés.",
            "Plus personne ne demandant la parole, le Président met successivement aux voix les résolutions inscrites à l'ordre du jour.",
        ]:
            _body(document, text)

        add_heading(
            document, "PREMIERE RESOLUTION", space_before_pt=_RESOLUTION_SPACE_BEFORE_PT
        )
        _body(document, _agrement_resolution(ctx, cessionnaire.denomination or ""))
        _body(
            document, "Cette résolution est adoptée à l'unanimité.", italic=True
        )

        add_heading(
            document, "DEUXIEME RESOLUTION", space_before_pt=_RESOLUTION_SPACE_BEFORE_PT
        )
        # Albane 2026-06-26 §P5 : (a) suppression de « et sous reserve de la realisation
        # definitive de la cession, » ; (b) le numero d'article modifie est SURLIGNE (champ
        # variable a adapter) ; (c) la formule d'entree en vigueur ajoute « a compter de ce
        # jour ».
        _add_resolution2_paragraph(document, _ARTICLE_REPARTITION)
        _body(
            document,
            (
                f"« A la suite de son évolution depuis la constitution de la Société, le capital social est fixé à "
                f"{required_text(scm_cedee.capital_social, 'scm_cession.scm_cedee.capital_social')} €. Il est divisé en "
                f"{scm_cedee.nb_parts_total} parts sociales, d'un montant nominal de "
                f"{required_text(scm_cedee.valeur_nominale_part, 'scm_cession.scm_cedee.valeur_nominale_part')} € chacune, "
                f"numérotées de {required_text(scm_cedee.plage_parts_total, 'scm_cession.scm_cedee.plage_parts_total')}, qui ont été attribuées aux associés tant en vertu des apports effectués lors de la constitution de la société, que des augmentations et réductions du capital et des cessions intervenues depuis la constitution de la société, à savoir :"
            ),
        )
        _add_repartition_apres_cession(document, scm_cession.associes_apres_cession)
        _body(
            document,
            f"Total égal au nombre de parts composant le capital social : {scm_cedee.nb_parts_total} parts ».",
        )
        _body(
            document, "Cette résolution est adoptée à l'unanimité.", italic=True
        )

        add_heading(
            document, "TROISIEME RESOLUTION", space_before_pt=_RESOLUTION_SPACE_BEFORE_PT
        )
        _body(
            document,
            "L'assemblée générale confère tous pouvoirs au porteur d'une copie ou d'un extrait du présent procès-verbal afin d'accomplir toutes les formalités consécutives aux décisions prises.",
        )
        _body(
            document, "Cette résolution est adoptée à l'unanimité.", italic=True
        )
        # Albane 2026-06-26 §P7 : le PV est signe par TOUS les associes presents (on enleve « la
        # gerance » de la formule finale ; le cadre de signature liste les associes, plus la
        # gerance).
        _body(
            document,
            "De tout ceci, il a été dressé le présent procès-verbal qui, après lecture, a été signé par tous les associés présents.",
        )
        # §1 — aeration : espace avant le cadre de signature.
        add_spacer(document, space_after_pt=_BLOCK_SPACER_PT)
        # §4.2 — cadre de signature agrandi (zone manuscrite/YouSign suffisante),
        # bordures conservees. 2,5 cm de hauteur minimale par ligne de signataires.
        add_signature_table(
            document,
            _signature_rows(scm_cession.signataires_pv),
            min_row_height_cm=2.5,
        )

        return save_clean_document(document, output_dir, OUTPUT_FILENAME)


def _agrement_resolution(ctx: DocumentGenerationContext, cessionnaire_name: str) -> str:
    # Albane 2026-06-26 §P4 : la 1re resolution agree le nouvel associe PUIS autorise la
    # cession. (a) « dans un delai de 3 mois ... soit jusqu'au {date} » remplace par « a
    # compter de ce jour » (plus de delai, plus de date limite) — pour TOUTES structures.
    # (b) clause ajoutee « et par consequent, autorise la cession de {nb} parts sociales de
    # {cedant} a la {SEL cessionnaire} » avec les variables reelles (parts cedees, cedant,
    # denomination cessionnaire).
    scm_cession = ctx.scm_cession
    if scm_cession is None or scm_cession.agrement is None:
        raise ValueError("scm_cession.agrement est obligatoire.")
    cedant = scm_cession.cedant
    if cedant is None:
        raise ValueError("scm_cession.cedant est obligatoire pour le PV AGE cession SCM.")
    parts_cedees = scm_cession.parts_cedees
    if parts_cedees is None:
        raise ValueError(
            "scm_cession.parts_cedees est obligatoire pour le PV AGE cession SCM."
        )
    cedant_nom = cedant_display(cedant)
    nb_cedees = required_text(parts_cedees.nb, "scm_cession.parts_cedees.nb")
    return (
        "L'assemblée générale, après avoir entendu lecture du rapport de la gérance et pris connaissance du projet de cession qui a été notifié à la société, décide d'agréer, comme nouvel associé la "
        f"{cessionnaire_name}, à compter de ce jour, et par conséquent, autorise la cession de "
        f"{nb_cedees} parts sociales de {cedant_nom} à la {cessionnaire_name}."
    )


def _est_feminin(civilite_affichage: str | None) -> bool:
    # Albane 2026-06-26 §P3a : feminisation de la qualite du president. Le sexe est lu sur la
    # civilite d'affichage deja saisie ; « Madame » (insensible casse/accents) -> feminin.
    if not civilite_affichage:
        return False
    return civilite_affichage.strip().casefold().startswith("madame")


def _add_resolution2_paragraph(document, numero_article: str) -> None:
    # Albane 2026-06-26 §P5 : 2e resolution sans « et sous reserve de la realisation
    # definitive de la cession, » ; le numero d'article est SURLIGNE (champ variable) ;
    # la formule d'entree en vigueur ajoute « a compter de ce jour ».
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragraph.paragraph_format.space_after = Pt(_PARAGRAPH_SPACE_AFTER_PT)
    paragraph.add_run(
        "L'assemblée générale, compte tenu de la résolution qui précède, décide, pour tenir "
        "compte de la nouvelle répartition du capital, de modifier l'article "
    )
    article_run = paragraph.add_run(numero_article)
    article_run.font.highlight_color = WD_COLOR_INDEX.YELLOW
    paragraph.add_run(
        " des statuts qui sera rédigé ainsi, à compter de ce jour :"
    )


def _add_repartition_apres_cession(
    document,
    associes: list[ScmCessionAssocie],
) -> None:
    for index, associe in enumerate(associes):
        prefix = f"scm_cession.associes_apres_cession[{index}]"
        parts = associe.parts
        if parts is None:
            raise ValueError(f"{prefix}.parts est obligatoire.")
        # Albane 2026-06-26 §P6 : « a concurrence de {nb} parts » sur la MEME ligne que
        # l'associe (plus de retour a la ligne). On fusionne les deux fragments.
        _body(
            document,
            f"à {associe_display(associe, prefix)}, à concurrence de {parts.nb} parts,",
        )
        _body(
            document,
            f"numérotées de {required_text(parts.plage, f'{prefix}.parts.plage')},",
        )
        _body(document, f"ci                                    {parts.nb} parts")


def _signature_rows(signataires: list[str]) -> list[list[str]]:
    rows: list[list[str]] = []
    current: list[str] = []
    for signataire in signataires:
        current.append(signataire)
        if len(current) == 2:
            rows.append(current)
            current = []
    if current:
        current.append("")
        rows.append(current)
    return rows
