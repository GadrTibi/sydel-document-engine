from __future__ import annotations

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from sydel_doc_engine.rendering.docx_builder import (
    add_framed_signature_block,
    add_framed_title,
    add_hyphen_list_item,
    add_legal_reminder,
    add_paragraph,
    new_document,
)


def _table_has_explicit_borders(table) -> bool:
    borders = table._tbl.tblPr.find(qn("w:tblBorders"))
    return borders is not None and all(
        borders.find(qn(f"w:{edge}")) is not None
        for edge in ("top", "left", "bottom", "right")
    )


def test_new_document_applies_global_style_profile() -> None:
    document = new_document()
    section = document.sections[0]

    assert abs(section.top_margin - Cm(2.5)) < 300
    assert abs(section.bottom_margin - Cm(2.5)) < 300
    assert abs(section.left_margin - Cm(2.5)) < 300
    assert abs(section.right_margin - Cm(2.5)) < 300
    assert document.styles["Normal"].font.name == "Roboto"
    assert document.styles["Normal"].font.size == Pt(10)


def test_framed_title_uses_centered_bordered_table() -> None:
    document = new_document()

    table = add_framed_title(document, ["TITRE", "SOUS-TITRE"])

    assert table.style.name == "Table Grid"
    assert _table_has_explicit_borders(table)
    paragraph = table.cell(0, 0).paragraphs[0]
    assert paragraph.alignment == WD_ALIGN_PARAGRAPH.CENTER
    assert paragraph.text == "TITRE\nSOUS-TITRE"
    assert all(run.bold for run in paragraph.runs if run.text.strip())


def test_framed_signature_block_uses_explicit_borders() -> None:
    document = new_document()

    table = add_framed_signature_block(document, ["Fait à Paris", "Le 12/05/2026"])

    assert table.style.name == "Table Grid"
    assert _table_has_explicit_borders(table)
    assert table.cell(0, 0).paragraphs[0].text == "Fait à Paris"
    assert table.cell(0, 0).paragraphs[1].text == "Le 12/05/2026"


def test_hyphen_list_item_uses_visible_marker_and_hanging_indent() -> None:
    document = new_document()

    paragraph = add_hyphen_list_item(document, "Nomination du gérant ;")

    assert paragraph.text == "- Nomination du gérant ;"
    assert paragraph.paragraph_format.left_indent is not None
    assert paragraph.paragraph_format.first_line_indent is not None
    assert paragraph.paragraph_format.first_line_indent < 0


def test_paragraph_and_legal_reminder_helpers_apply_text_styles() -> None:
    document = new_document()

    paragraph = add_paragraph(document, "Texte", bold=True)
    add_legal_reminder(
        document,
        title="Rappel",
        title_suffix=" : Article",
        paragraphs=["Texte légal"],
    )

    assert paragraph.runs[0].bold is True
    reminder_title = document.paragraphs[2]
    assert reminder_title.runs[0].text == "Rappel"
    assert reminder_title.runs[0].italic is True
    assert reminder_title.runs[0].underline is True
    assert reminder_title.runs[1].italic is True
    reminder_text = document.paragraphs[3]
    assert reminder_text.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY
    assert reminder_text.runs[0].italic is True
