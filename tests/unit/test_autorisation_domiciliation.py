from __future__ import annotations

from datetime import date
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Company,
    DocumentGenerationContext,
    Domiciliation,
    Person,
    Signature,
)
from sydel_doc_engine.generators.lot_01.autorisation_domiciliation import (
    AutorisationDomiciliationGenerator,
)


def _context(
    genre: Gender = Gender.MASCULIN,
    *,
    adresse_domiciliation_affichee: str = "15 rue du Libre, Lyon 69002",
    image_optionnelle: Path | None = None,
) -> DocumentGenerationContext:
    civilite = "Madame" if genre == Gender.FEMININ else "Monsieur"
    prenom = "Marie" if genre == Gender.FEMININ else "Jean"
    return DocumentGenerationContext(
        personne_signataire=Person(
            genre=genre,
            civilite=civilite,
            prenom=prenom,
            nom="Durand",
        ),
        societe=Company(
            denomination="DURAND CONSEIL",
            capital="1 000",
            siege=Address(
                num_voie="80",
                voie="avenue Marceau",
                cp="75008",
                ville="Paris",
            ),
        ),
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee=adresse_domiciliation_affichee,
        ),
        signature=Signature(
            lieu="Paris",
            date=date(2026, 5, 12),
            image_optionnelle=image_optionnelle,
        ),
    )


def _generate(
    tmp_path: Path,
    genre: Gender = Gender.MASCULIN,
    *,
    adresse_domiciliation_affichee: str = "15 rue du Libre, Lyon 69002",
    image_optionnelle: Path | None = None,
) -> Path:
    return AutorisationDomiciliationGenerator().generate(
        _context(
            genre,
            adresse_domiciliation_affichee=adresse_domiciliation_affichee,
            image_optionnelle=image_optionnelle,
        ),
        tmp_path,
    )


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts: list[str] = [paragraph.text for paragraph in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(paragraph.text for paragraph in cell.paragraphs)
    return "\n".join(text for text in texts if text)


def _table_has_explicit_borders(table) -> bool:
    borders = table._tbl.tblPr.find(qn("w:tblBorders"))
    return borders is not None and borders.find(qn("w:top")) is not None


def _table_text(table) -> str:
    return "\n".join(cell.text for row in table.rows for cell in row.cells)


def test_autorisation_domiciliation_creates_docx(tmp_path: Path) -> None:
    output_dir = tmp_path / "nested"

    output_path = _generate(output_dir)

    assert output_path == output_dir / "autorisation_domiciliation.docx"
    assert output_path.is_file()


def test_autorisation_domiciliation_contains_essential_texts(tmp_path: Path) -> None:
    text = _docx_text(_generate(tmp_path))

    assert "AUTORISATION DE DOMICILIATION" in text
    assert (
        "Je soussigné Monsieur Jean Durand autorise la domiciliation de la Société "
        "DURAND CONSEIL au capital de 1 000 € en cours de formation, dans les locaux "
        "du cabinet au 80 avenue Marceau, 75008 Paris pour 99 ans."
    ) in text
    assert "Fait à Paris" in text
    assert "Le 12/05/2026" in text
    assert "Monsieur Jean Durand" in text


def test_autorisation_domiciliation_uses_feminine_agreement(tmp_path: Path) -> None:
    text = _docx_text(_generate(tmp_path, Gender.FEMININ))

    assert "Je soussignée Madame Marie Durand" in text


def test_autorisation_domiciliation_uses_masculine_agreement(tmp_path: Path) -> None:
    text = _docx_text(_generate(tmp_path, Gender.MASCULIN))

    assert "Je soussigné Monsieur Jean Durand" in text
    assert "Je soussignée Monsieur Jean Durand" not in text


def test_autorisation_domiciliation_ignores_free_address_for_cabinet_wording(
    tmp_path: Path,
) -> None:
    adresse = "Bâtiment B, 4 impasse des Tests, Marseille 13002"

    text = _docx_text(_generate(tmp_path, adresse_domiciliation_affichee=adresse))

    assert adresse not in text
    assert (
        "dans les locaux du cabinet au 80 avenue Marceau, 75008 Paris "
        "pour 99 ans."
    ) in text


def test_autorisation_domiciliation_uses_company_seat_as_cabinet_address(
    tmp_path: Path,
) -> None:
    text = _docx_text(_generate(tmp_path))

    assert "15 rue du Libre, Lyon 69002" not in text
    assert "80 avenue Marceau, 75008 Paris" in text
    assert "Paris 75008" not in text


def test_autorisation_domiciliation_does_not_use_signature_image(tmp_path: Path) -> None:
    missing_image = tmp_path / "signature_absente.png"

    output_path = _generate(tmp_path, image_optionnelle=missing_image)

    assert len(Document(output_path).inline_shapes) == 0


def test_autorisation_domiciliation_uses_signature_paragraphs_without_table(
    tmp_path: Path,
) -> None:
    document = Document(_generate(tmp_path))

    assert len(document.tables) == 1
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
    assert "Fait à Paris" in paragraphs
    assert "Le 12/05/2026" in paragraphs
    assert "Monsieur Jean Durand" in paragraphs
