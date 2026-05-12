from __future__ import annotations

from datetime import date
from pathlib import Path

from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from sydel_doc_engine.domain.models import Company, DocumentGenerationContext, Domiciliation
from sydel_doc_engine.rendering.docx_builder import new_document
from sydel_doc_engine.utils.grammar import subject_line

OUTPUT_FILENAME = "autorisation_domiciliation.docx"


class AutorisationDomiciliationGenerator:
    """Générateur cible du DOC-002."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        person = ctx.personne_signataire
        company = _required_company(ctx.societe)
        domiciliation = _required_domiciliation(ctx.domiciliation)

        civilite = _required_text(person.civilite, "personne_signataire.civilite")
        prenom = _required_text(person.prenom, "personne_signataire.prenom")
        nom = _required_text(person.nom, "personne_signataire.nom")
        denomination_societe = _required_text(company.denomination, "societe.denomination")
        capital_social = _required_text(company.capital, "societe.capital")
        adresse_domiciliation = _required_text(
            domiciliation.adresse_domiciliation_affichee,
            "domiciliation.adresse_domiciliation_affichee",
        )
        lieu_signature = _required_text(ctx.signature.lieu, "signature.lieu")

        document = new_document()
        _configure_document(document)
        _add_title(document)
        _add_paragraph(
            document,
            (
                f"{subject_line(person.genre)} {civilite} {prenom} {nom} autorise la "
                f"domiciliation de la Société {denomination_societe} au capital de "
                f"{capital_social} € en cours de formation, dans les locaux situés au "
                f"{adresse_domiciliation}, pour une durée indéterminée."
            ),
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
        _add_final_block(
            document,
            lieu_signature=lieu_signature,
            date_signature=_format_date(ctx.signature.date),
            signatory_name=f"{civilite} {prenom} {nom}",
        )

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        document.save(output_path)
        return output_path


def _required_company(company: Company | None) -> Company:
    if company is None:
        raise ValueError("societe est obligatoire pour DOC-002.")
    return company


def _required_domiciliation(domiciliation: Domiciliation | None) -> Domiciliation:
    if domiciliation is None:
        raise ValueError("domiciliation est obligatoire pour DOC-002.")
    return domiciliation


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour DOC-002.")
    return value.strip()


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
    run = paragraph.add_run("AUTORISATION DE DOMICILIATION")
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
