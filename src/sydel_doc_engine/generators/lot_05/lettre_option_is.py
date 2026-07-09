from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

from sydel_doc_engine.domain.models import (
    Address,
    CentreImpots,
    Company,
    DocumentGenerationContext,
    StatutsCivilsAssocie,
    StatutsCivilsContext,
)
from sydel_doc_engine.rendering.docx_builder import (
    LETTER_WIDE_STYLE_PROFILE,
    add_framed_address_block,
    add_letter_place_date,
    add_paragraph,
    add_spacer,
    add_subject_heading,
    new_document,
)
from sydel_doc_engine.utils.dates import format_date_fr

OUTPUT_FILENAME = "lettre_option_is.docx"
DOCUMENT_CODE = "CODE-OPTION-IS-001"
# Micro holding (Albane 2026-06-29) : la lettre d'option IS fait partie du bundle de creation
# de la micro holding (societe civile) — meme modele que la SCI (« la societe civile … opte
# pour le regime de l'IS »).
SUPPORTED_STRUCTURES = {"SCI", "SCI IRIS", "MICRO_HOLDING"}
_EXPECTED_STATUTS_TYPE = {"SCI": "sci", "SCI IRIS": "sci_iris", "MICRO_HOLDING": "micro_holding"}


class LettreOptionIsGenerator:
    """Generateur from-scratch de la lettre d'option IS V1."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        _validate_context(ctx)
        company = _required_company(ctx.societe)
        tax_office = _required_tax_office(ctx.impots)
        statuts = _required_statuts_civils(ctx.statuts_civils)

        document = new_document(LETTER_WIDE_STYLE_PROFILE)
        _add_tax_office_block(document, tax_office)
        _add_place_date_and_subject(document, ctx.signature.lieu, ctx.signature.date)
        _add_body_intro(document, company)
        _add_identification_table(document, company, statuts)
        _add_body_close(document)
        _add_signature(document)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        document.save(output_path)
        return output_path


def _validate_context(ctx: DocumentGenerationContext) -> None:
    if ctx.structure not in SUPPORTED_STRUCTURES:
        supported = ", ".join(sorted(SUPPORTED_STRUCTURES))
        raise ValueError(f"dossier.structure doit etre dans [{supported}] pour {DOCUMENT_CODE}.")
    if ctx.dossier_options is None or not ctx.dossier_options.option_is:
        raise ValueError(f"dossier.options.option_is doit etre vrai pour {DOCUMENT_CODE}.")
    statuts = _required_statuts_civils(ctx.statuts_civils)
    expected_type = _EXPECTED_STATUTS_TYPE[ctx.structure]
    if statuts.type != expected_type:
        raise ValueError(f"statuts_civils.type doit etre {expected_type} pour {DOCUMENT_CODE}.")


def _required_company(company: Company | None) -> Company:
    if company is None:
        raise ValueError(f"societe est obligatoire pour {DOCUMENT_CODE}.")
    return company


def _required_tax_office(tax_office: CentreImpots | None) -> CentreImpots:
    if tax_office is None:
        raise ValueError(f"impots est obligatoire pour {DOCUMENT_CODE}.")
    return tax_office


def _required_statuts_civils(statuts: StatutsCivilsContext | None) -> StatutsCivilsContext:
    if statuts is None:
        raise ValueError(f"statuts_civils est obligatoire pour {DOCUMENT_CODE}.")
    if not statuts.associes:
        raise ValueError(f"statuts_civils.associes est obligatoire pour {DOCUMENT_CODE}.")
    return statuts


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value.strip()


def _required_int(value: int | None, field_name: str) -> int:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


# Retour Rafael R22-07 (2026-06-22) : le centre est TOUJOURS « Centre des Finances
# Publiques » (le service + l'adresse portent l'identification). On fige le libelle au
# lieu d'une variable saisie -> plus de champ « Centre » dans le formulaire.
CENTRE_FINANCES_PUBLIQUES = "Centre des Finances Publiques"

# R3 (Albane 2026-06-30) : la lettre d'option IS est emise PENDANT la constitution de la
# societe — elle n'est donc PAS encore immatriculee. Le SIREN ne doit JAMAIS afficher un
# numero (meme saisi par erreur), mais la constante « En cours d'immatriculation » (E
# majuscule, apostrophe COURBE U+2019, conforme au modele client
# docs/review/albane_micro_holding_2026-06-29/lettre_option_IS.docx). On retire donc
# l'exigence de non-vide sur company.siren pour ce document.
SIREN_EN_COURS_IMMATRICULATION = "En cours d’immatriculation"


# R2 (Albane 2026-06-30) : le bloc DESTINATAIRE (centre des impots) doit etre ENCADRE
# (enveloppe a fenetre) ET DESCENDU a la hauteur de la fenetre. Le calage a DROITE est
# conserve (« le côté me paraît bien »).
# DEFAUT DOCUMENTE (a valider Albane sur rendu) : la cote exacte n'est pas chiffree par
# Albane -> on vise ~4,5 cm du haut de page (fenetre standard FR). La marge haute du
# courrier est 2,5 cm (LETTER_WIDE_STYLE_PROFILE) ; il reste donc ~2,0 cm a descendre via
# un spacer pour amener le bloc a ~4,5 cm.
_FENETRE_DROP_TOP_CM = 2.0


def _add_tax_office_block(document: Any, tax_office: CentreImpots) -> None:
    add_framed_address_block(
        document,
        [
            _required_text(tax_office.service, "impots.service"),
            CENTRE_FINANCES_PUBLIQUES,
            _required_text(tax_office.adresse_ligne_1, "impots.adresse_ligne_1"),
            _required_text(tax_office.adresse_ligne_2, "impots.adresse_ligne_2"),
            (
                f"{_required_text(tax_office.cp, 'impots.cp')} "
                f"{_required_text(tax_office.ville, 'impots.ville')}"
            ),
        ],
        width_cm=7.5,
        drop_top_cm=_FENETRE_DROP_TOP_CM,
        style_profile=LETTER_WIDE_STYLE_PROFILE,
    )
    add_spacer(document, space_after_pt=16)


def _add_place_date_and_subject(document: Any, lieu: str, signature_date: date) -> None:
    add_letter_place_date(
        document,
        f"Fait à {lieu}, le {format_date_fr(signature_date)}",
        space_after_pt=12,
        style_profile=LETTER_WIDE_STYLE_PROFILE,
    )
    add_subject_heading(
        document,
        "Objet : Demande d'option pour le régime de l'impôt sur les sociétés",
        space_after_pt=12,
        style_profile=LETTER_WIDE_STYLE_PROFILE,
    )


def _add_body_intro(document: Any, company: Company) -> None:
    # Mise en forme (Albane, retour « mise en forme » 2026-07) : le NOM DE LA
    # SOCIETE doit figurer EN GRAS dans la PREMIERE LIGNE du courrier. La
    # denomination ne paraissait jusqu'ici que dans la table d'identite, sans
    # emphase -> on l'ajoute en tete du corps, en gras (choix retenu : premiere
    # ligne du courrier avant « Madame, Monsieur, », plutot que dans la table,
    # car Albane demande explicitement « la PREMIERE LIGNE du courrier »).
    add_paragraph(
        document,
        _required_text(company.denomination, "societe.denomination"),
        bold=True,
        style_profile=LETTER_WIDE_STYLE_PROFILE,
    )
    add_paragraph(document, "Madame, Monsieur,", style_profile=LETTER_WIDE_STYLE_PROFILE)
    add_paragraph(
        document,
        (
            "Nous vous informons que la société civile dont vous trouverez la description "
            "ci-après opte pour le régime de l'Impôt sur les Sociétés, et souhaite que cette "
            "option produise ses effets à compter de l'exercice ouvert dès l'immatriculation."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        style_profile=LETTER_WIDE_STYLE_PROFILE,
    )
    add_paragraph(
        document,
        "Cette décision est prise en accord avec les associés participant.",
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        style_profile=LETTER_WIDE_STYLE_PROFILE,
    )
    add_paragraph(
        document,
        (
            "État d'identification de la société et liste des associés au 1er jour du premier "
            "exercice d'option :"
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        style_profile=LETTER_WIDE_STYLE_PROFILE,
    )


def _add_identification_table(
    document: Any,
    company: Company,
    statuts: StatutsCivilsContext,
) -> None:
    _validate_capital_distribution(statuts)
    table = document.add_table(rows=0, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    table.columns[0].width = Cm(6)
    table.columns[1].width = Cm(10)

    capital = _required_text(
        company.capital_social or statuts.capital_social,
        "societe.capital_social",
    )
    denomination = _required_text(company.denomination, "societe.denomination")
    _add_table_row(table, "Dénomination", denomination)
    _add_table_row(table, "Adresse (siège ou principal établissement)", _company_address(company))
    # R3 (Albane 2026-06-30) : societe EN COURS DE CONSTITUTION -> jamais de numero SIREN,
    # toujours la constante (le numero saisi, s'il existe, est volontairement ignore ici).
    _add_table_row(table, "SIREN", SIREN_EN_COURS_IMMATRICULATION)
    label = (
        "Nom, prénom et adresse des différents associés de la société, "
        f"et répartition du capital de {capital} €"
    )
    for index, associe in enumerate(statuts.associes):
        _add_table_row(table, label, _associe_table_text(associe, index))

    add_spacer(document, space_after_pt=12)


def _add_table_row(table: Any, label: str, value: str) -> None:
    row_cells = table.add_row().cells
    row_cells[0].text = label
    row_cells[1].text = value
    for cell in row_cells:
        for paragraph in cell.paragraphs:
            paragraph.paragraph_format.space_after = Pt(2)


def _validate_capital_distribution(statuts: StatutsCivilsContext) -> None:
    total = _required_int(statuts.nb_parts_total, "statuts_civils.nb_parts_total")
    associes_total = 0
    for index, associe in enumerate(statuts.associes):
        if associe.parts is None:
            raise ValueError(f"statuts_civils.associes[{index}].parts est obligatoire.")
        associes_total += _required_int(
            associe.parts.nb,
            f"statuts_civils.associes[{index}].parts.nb",
        )
    if associes_total != total:
        raise ValueError(
            "La repartition des parts doit correspondre a statuts_civils.nb_parts_total "
            f"pour {DOCUMENT_CODE}."
        )


def _company_address(company: Company) -> str:
    if company.siege is None:
        raise ValueError(f"societe.siege est obligatoire pour {DOCUMENT_CODE}.")
    return _address_display(company.siege, "societe.siege")


def _address_display(address: Address, field_name: str) -> str:
    if address.adresse_affichee:
        return address.adresse_affichee.strip()
    return (
        f"{_required_text(address.num_voie, f'{field_name}.num_voie')} "
        f"{_required_text(address.voie, f'{field_name}.voie')}, "
        f"{_required_text(address.cp, f'{field_name}.cp')} "
        f"{_required_text(address.ville, f'{field_name}.ville')}"
    )


def _associe_table_text(associe: StatutsCivilsAssocie, index: int) -> str:
    field_name = f"statuts_civils.associes[{index}]"
    if associe.parts is None:
        raise ValueError(f"{field_name}.parts est obligatoire pour {DOCUMENT_CODE}.")
    nb_parts = _required_int(associe.parts.nb, f"{field_name}.parts.nb")
    if associe.type_personne == "personne_morale":
        return _associe_morale_table_text(associe, field_name, nb_parts)
    return _associe_physique_table_text(associe, field_name, nb_parts)


def _associe_physique_table_text(
    associe: StatutsCivilsAssocie,
    field_name: str,
    nb_parts: int,
) -> str:
    address = associe.adresse_personnelle
    if associe.adresse_personnelle_affichee:
        address_display = associe.adresse_personnelle_affichee.strip()
    elif address is not None:
        address_display = _address_display(address, f"{field_name}.adresse_personnelle")
    else:
        raise ValueError(f"{field_name}.adresse_personnelle est obligatoire pour {DOCUMENT_CODE}.")
    qualite = _required_text(
        associe.parts.qualite_associe or associe.role_statutaire,
        f"{field_name}.parts.qualite_associe",
    )
    return (
        f"{_required_text(associe.civilite_affichage, f'{field_name}.civilite_affichage')} "
        f"{_required_text(associe.prenom, f'{field_name}.prenom')} "
        f"{_required_text(associe.nom, f'{field_name}.nom')}, demeurant au {address_display}, "
        f"{qualite}, détenant {nb_parts} parts."
    )


def _associe_morale_table_text(
    associe: StatutsCivilsAssocie,
    field_name: str,
    nb_parts: int,
) -> str:
    if associe.siege is None:
        raise ValueError(f"{field_name}.siege est obligatoire pour {DOCUMENT_CODE}.")
    return (
        f"La société {_required_text(associe.denomination, f'{field_name}.denomination')}, "
        f"ayant son siège social au {_address_display(associe.siege, f'{field_name}.siege')}, "
        f"détenant {nb_parts} parts."
    )


def _add_body_close(document: Any) -> None:
    add_paragraph(
        document,
        (
            "Nous vous remercions de bien vouloir nous confirmer que cette demande est validée, "
            "et vous prions de recevoir, Madame, Monsieur, l'assurance de notre parfaite "
            "considération."
        ),
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        style_profile=LETTER_WIDE_STYLE_PROFILE,
    )


def _add_signature(document: Any) -> None:
    add_spacer(document, space_after_pt=12)
    add_paragraph(
        document,
        "Le gérant",
        alignment=WD_ALIGN_PARAGRAPH.RIGHT,
        style_profile=LETTER_WIDE_STYLE_PROFILE,
    )
