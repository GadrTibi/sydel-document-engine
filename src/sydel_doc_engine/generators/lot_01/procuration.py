from __future__ import annotations

from datetime import date
from pathlib import Path

from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from sydel_doc_engine.domain.models import Address, Company, DocumentGenerationContext
from sydel_doc_engine.rendering.docx_builder import new_document
from sydel_doc_engine.utils.grammar import subject_line

OUTPUT_FILENAME = "procuration.docx"

MANDATAIRE_NOM = "SYDEL"
MANDATAIRE_ADRESSE = "80 avenue Marceau, 75008 PARIS"
MANDATAIRE_RCS = "RCS PARIS 788 531 432"
MANDATAIRE_TELEPHONE = "0153814303"

MANDATE_PARAGRAPH_1 = (
    "De pour moi et en mon nom faire tous dépôts, immatriculations, modifications, radiations "
    "et de recevoir le registre des bénéficiaires effectifs, concernant mon entreprise auprès "
    "des registres."
)
MANDATE_PARAGRAPH_2 = (
    "En conséquence, faire toutes déclarations et démarches, produire toutes pièces "
    "justificatives, "
    "effectuer tout dépôt de pièces, signer tous documents, requêtes et documents utiles, élire "
    "domicile, substituer en totalité ou en partie, et en général faire tout ce qui sera "
    "nécessaire."
)
MANDATE_PARAGRAPH_3 = "L’exécution de ce mandat vaudra décharge au mandataire."


class ProcurationGenerator:
    """Générateur cible du DOC-003."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        person = ctx.personne_signataire
        company = _required_company(ctx.societe)
        personal_address = _required_address(
            person.adresse_perso,
            "personne_signataire.adresse_perso",
        )
        company_address = _required_address(company.siege, "societe.siege")

        civilite = _required_text(person.civilite, "personne_signataire.civilite")
        prenom = _required_text(person.prenom, "personne_signataire.prenom")
        nom = _required_text(person.nom, "personne_signataire.nom")
        fonction_dirigeant = _required_text(
            person.fonction_dirigeant,
            "personne_signataire.fonction_dirigeant",
        )
        forme_sociale = _required_text(company.forme_sociale, "societe.forme_sociale")
        denomination_societe = _required_text(company.denomination, "societe.denomination")
        lieu_signature = _required_text(ctx.signature.lieu, "signature.lieu")

        document = new_document()
        _configure_document(document)
        _add_title(document)
        _add_paragraph(
            document,
            (
                f"{subject_line(person.genre)} {civilite} {prenom} {nom}, demeurant au "
                f"{personal_address}. Agissant en qualité de {fonction_dirigeant} de "
                f"{forme_sociale} {denomination_societe} dont le siège est situé au "
                f"{company_address}"
            ),
        )
        _add_paragraph(document, "Donne par les présentes pouvoir à :")
        _add_mandataire_block(document)
        for text in (MANDATE_PARAGRAPH_1, MANDATE_PARAGRAPH_2, MANDATE_PARAGRAPH_3):
            _add_paragraph(document, text, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
        _add_final_block(
            document,
            lieu_signature=lieu_signature,
            date_signature=_format_date(ctx.signature.date),
            signatory_name=f"{prenom} {nom}",
        )

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        document.save(output_path)
        return output_path


def _required_company(company: Company | None) -> Company:
    if company is None:
        raise ValueError("societe est obligatoire pour DOC-003.")
    return company


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour DOC-003.")
    return value.strip()


def _required_address(address: Address | None, field_name: str) -> str:
    if address is None:
        raise ValueError(f"{field_name} est obligatoire pour DOC-003.")
    num_voie = _required_text(address.num_voie, f"{field_name}.num_voie")
    voie = _required_text(address.voie, f"{field_name}.voie")
    ville = _required_text(address.ville, f"{field_name}.ville")
    cp = _required_text(address.cp, f"{field_name}.cp")
    return f"{num_voie} {voie}, {ville} {cp}"


def _format_date(value: date) -> str:
    return value.strftime("%d/%m/%Y")


def _configure_document(document) -> None:
    section = document.sections[0]
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

    style = document.styles["Normal"]
    style.font.name = "Roboto"
    style.font.size = Pt(10)
    r_fonts = style.element.rPr.rFonts
    for font_attribute in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        r_fonts.set(qn(font_attribute), "Roboto")


def _add_title(document) -> None:
    table = document.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    cell = table.cell(0, 0)
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run("Procuration")
    run.bold = True
    run.font.size = Pt(10)
    document.add_paragraph()


def _add_paragraph(
    document,
    text: str,
    *,
    alignment: WD_ALIGN_PARAGRAPH | None = None,
) -> None:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(6)
    if alignment is not None:
        paragraph.alignment = alignment
    paragraph.add_run(text)


def _add_mandataire_block(document) -> None:
    for text, bold, italic in (
        (MANDATAIRE_NOM, True, False),
        (MANDATAIRE_ADRESSE, False, True),
        (MANDATAIRE_RCS, False, True),
        (MANDATAIRE_TELEPHONE, False, True),
    ):
        paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.space_after = Pt(0)
        run = paragraph.add_run(text)
        run.bold = bold
        run.italic = italic


def _add_final_block(
    document,
    *,
    lieu_signature: str,
    date_signature: str,
    signatory_name: str,
) -> None:
    document.add_paragraph()
    table = document.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.RIGHT
    right_cell = table.cell(0, 1)
    right_cell.width = Cm(7)
    for text in (f"Fait à {lieu_signature}", f"Le {date_signature}", signatory_name):
        paragraph = right_cell.add_paragraph(text)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
