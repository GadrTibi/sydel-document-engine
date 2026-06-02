from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from docx import Document
from docx.oxml.ns import qn

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Company,
    DocumentGenerationContext,
    Person,
    Signature,
)
from sydel_doc_engine.generators.lot_01.procuration import ProcurationGenerator


def _context(
    genre: Gender = Gender.MASCULIN,
    *,
    image_optionnelle: Path | None = None,
    fonction_dirigeant: str = "Président",
    forme_sociale: str = "SAS",
    denomination: str = "DURAND CONSEIL",
) -> DocumentGenerationContext:
    civilite = "Madame" if genre == Gender.FEMININ else "Monsieur"
    prenom = "Marie" if genre == Gender.FEMININ else "Jean"
    return DocumentGenerationContext(
        personne_signataire=Person(
            genre=genre,
            civilite=civilite,
            prenom=prenom,
            nom="Durand",
            adresse_perso=Address(
                num_voie="12",
                voie="rue des Lilas",
                cp="75008",
                ville="Paris",
            ),
            fonction_dirigeant=fonction_dirigeant,
        ),
        societe=Company(
            forme_sociale=forme_sociale,
            denomination=denomination,
            siege=Address(
                num_voie="80",
                voie="avenue Marceau",
                cp="75008",
                ville="Paris",
            ),
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
    image_optionnelle: Path | None = None,
    fonction_dirigeant: str = "Président",
    forme_sociale: str = "SAS",
    denomination: str = "DURAND CONSEIL",
) -> Path:
    return ProcurationGenerator().generate(
        _context(
            genre,
            image_optionnelle=image_optionnelle,
            fonction_dirigeant=fonction_dirigeant,
            forme_sociale=forme_sociale,
            denomination=denomination,
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


def _document_paragraphs(path: Path) -> list[str]:
    document = Document(path)
    return [paragraph.text for paragraph in document.paragraphs if paragraph.text]


def _table_has_explicit_borders(table) -> bool:
    borders = table._tbl.tblPr.find(qn("w:tblBorders"))
    return borders is not None and borders.find(qn("w:top")) is not None


def test_procuration_creates_docx(tmp_path: Path) -> None:
    output_dir = tmp_path / "nested"

    output_path = _generate(output_dir)

    assert output_path == output_dir / "procuration.docx"
    assert output_path.is_file()


def test_procuration_contains_essential_texts(tmp_path: Path) -> None:
    text = _docx_text(_generate(tmp_path))

    assert "Procuration" in text
    assert "Je soussigné Monsieur Jean Durand" in text
    assert "Agissant en qualité de Président de SAS DURAND CONSEIL" in text
    assert "Donne par les présentes pouvoir à :" in text
    assert (
        "De pour moi et en mon nom faire tous dépôts, immatriculations, modifications, "
        "radiations et de recevoir le registre des bénéficiaires effectifs, concernant mon "
        "entreprise auprès des registres."
    ) in text
    assert (
        "En conséquence, faire toutes déclarations et démarches, produire toutes pièces "
        "justificatives, effectuer tout dépôt de pièces, signer tous documents, requêtes et "
        "documents utiles, élire domicile, substituer en totalité ou en partie, et en général "
        "faire tout ce qui sera nécessaire."
    ) in text
    assert "L’exécution de ce mandat vaudra décharge au mandataire." in text
    assert "Fait pour servir et valoir ce que de droit." in text
    assert "RCS PARIS 788 531 432" not in text
    assert "0153814303" not in text
    assert "Fait à Paris" in text
    assert "Le 12/05/2026" in text
    assert "Jean Durand" in text


def test_procuration_selas_president_contains_required_terms(tmp_path: Path) -> None:
    text = _docx_text(
        _generate(
            tmp_path,
            fonction_dirigeant="Président",
            forme_sociale="SELAS",
            denomination="DURAND MEDECIN",
        )
    )

    assert "Procuration" in text
    assert "Je soussigné Monsieur Jean Durand" in text
    assert "Agissant en qualité de President de SELAS DURAND MEDECIN" in text
    assert "80 avenue Marceau, 75008 PARIS" in text
    assert "demeurant au 12 rue des Lilas, Paris 75008" in text
    assert "dont le siège est situé au 80 avenue Marceau, Paris 75008" in text
    assert "Gerant" not in text
    assert "gerant" not in text
    assert "Gérant" not in text
    assert "gérant" not in text
    assert "SELARL" not in text
    assert "parts sociales" not in text
    assert "Directeur General" not in text
    assert "Directeur Général" not in text


def test_procuration_selas_normalizes_abbreviated_forme_sociale(tmp_path: Path) -> None:
    text = _docx_text(
        _generate(
            tmp_path,
            fonction_dirigeant="President",
            forme_sociale="selas",
            denomination="DURAND MEDECIN",
        )
    )

    assert "Agissant en qualité de President de SELAS DURAND MEDECIN" in text
    assert " de selas " not in text


def test_procuration_selas_rejects_gerant_function(tmp_path: Path) -> None:
    with pytest.raises(
        ValueError,
        match="personne_signataire.fonction_dirigeant doit etre President",
    ):
        _generate(tmp_path, fonction_dirigeant="Gerant", forme_sociale="SELAS")


def test_procuration_selas_rejects_directeur_general(tmp_path: Path) -> None:
    with pytest.raises(
        ValueError,
        match="Directeur General est hors perimetre V1",
    ):
        _generate(tmp_path, fonction_dirigeant="Directeur General", forme_sociale="SELAS")


def test_procuration_uses_feminine_agreement(tmp_path: Path) -> None:
    text = _docx_text(_generate(tmp_path, Gender.FEMININ))

    assert "Je soussignée Madame Marie Durand" in text


def test_procuration_composes_personal_address_in_source_order(tmp_path: Path) -> None:
    text = _docx_text(_generate(tmp_path))

    assert "demeurant au 12 rue des Lilas, Paris 75008" in text
    assert "demeurant au 12 rue des Lilas, 75008 Paris" not in text


def test_procuration_composes_company_address_in_source_order(tmp_path: Path) -> None:
    text = _docx_text(_generate(tmp_path))

    assert "dont le siège est situé au 80 avenue Marceau, Paris 75008" in text
    assert "dont le siège est situé au 80 avenue Marceau, 75008 Paris" not in text


def test_procuration_contains_exact_sydel_block(tmp_path: Path) -> None:
    paragraphs = _document_paragraphs(_generate(tmp_path))

    start = paragraphs.index("SYDEL")
    assert paragraphs[start : start + 2] == [
        "SYDEL",
        "80 avenue Marceau, 75008 PARIS",
    ]


def test_procuration_does_not_use_signature_image(tmp_path: Path) -> None:
    missing_image = tmp_path / "signature_absente.png"

    output_path = _generate(tmp_path, image_optionnelle=missing_image)

    assert len(Document(output_path).inline_shapes) == 0


def test_procuration_uses_framed_signature_block(tmp_path: Path) -> None:
    document = Document(_generate(tmp_path))

    signature_table = document.tables[1]
    assert signature_table.style.name == "Table Grid"
    assert _table_has_explicit_borders(signature_table)
    assert "Jean Durand" in signature_table.cell(0, 0).text
