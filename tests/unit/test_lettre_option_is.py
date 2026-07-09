from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    CentreImpots,
    Company,
    DocumentGenerationContext,
    DossierOptions,
    Person,
    Signature,
    StatutsCivilsAssocie,
    StatutsCivilsContext,
    StatutsCivilsParts,
)
from sydel_doc_engine.generators.lot_05.lettre_option_is import LettreOptionIsGenerator


def _docx_text(path: Path) -> str:
    document = Document(path)
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
    cells = [
        cell.text
        for table in document.tables
        for row in table.rows
        for cell in row.cells
        if cell.text
    ]
    return "\n".join(paragraphs + cells)


def _assert_clean(text: str) -> None:
    assert "[" not in text
    assert "]" not in text


def _base_context(*, option_is: bool = True, structure: str = "SCI") -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure=structure,
        dossier_options=DossierOptions(option_is=option_is),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Jean",
            nom="Durand",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 15)),
        impots=CentreImpots(
            service="Service des impots des entreprises",
            centre="SIE Paris Centre",
            adresse_ligne_1="6 rue Paganini",
            adresse_ligne_2="TSA 10000",
            cp="75020",
            ville="Paris",
        ),
        societe=Company(
            denomination="SCI EXEMPLE",
            forme_sociale="SCI",
            capital_social="1000",
            siren="123 456 789",
            siege=Address(
                num_voie="12",
                voie="avenue Victor Hugo",
                cp="75016",
                ville="Paris",
            ),
        ),
        statuts_civils=StatutsCivilsContext(
            type="sci" if structure == "SCI" else "sci_iris",
            capital_social="1000",
            nb_parts_total=100,
            associes=[
                StatutsCivilsAssocie(
                    type_personne="personne_physique",
                    civilite_affichage="Monsieur",
                    prenom="Jean",
                    nom="Durand",
                    adresse_personnelle=Address(
                        num_voie="1",
                        voie="rue Exemple",
                        cp="75000",
                        ville="Paris",
                    ),
                    parts=StatutsCivilsParts(nb=40, qualite_associe="associe"),
                ),
                StatutsCivilsAssocie(
                    type_personne="personne_morale",
                    denomination="SEL IRIS",
                    siege=Address(
                        num_voie="2",
                        voie="rue Pro",
                        cp="75000",
                        ville="Paris",
                    ),
                    parts=StatutsCivilsParts(nb=60),
                ),
            ],
        ),
    )


def test_lettre_option_is_generates_clean_docx(tmp_path: Path) -> None:
    output_path = LettreOptionIsGenerator().generate(_base_context(), tmp_path)
    text = _docx_text(output_path)

    assert output_path.name == "lettre_option_is.docx"
    assert "Service des impots des entreprises" in text
    # R22-07 : le centre est fige (« Centre des Finances Publiques »), plus la valeur saisie
    # (« SIE Paris Centre » fournie au contexte est ignoree).
    assert "Centre des Finances Publiques" in text
    assert "SIE Paris Centre" not in text
    assert "Demande d'option pour le régime de l'impôt sur les sociétés" in text
    assert "SCI EXEMPLE" in text
    # R3 (Albane 2026-06-30) : la societe est EN COURS DE CONSTITUTION -> le SIREN affiche
    # TOUJOURS la constante « En cours d'immatriculation » (apostrophe courbe U+2019),
    # JAMAIS le numero saisi (« 123 456 789 » fourni au contexte est volontairement ignore).
    assert "En cours d’immatriculation" in text
    assert "123 456 789" not in text
    # Rafael/Albane 2026-07-09 : « Demeurant [adresse] » -> « Demeurant au [adresse] ».
    assert "Monsieur Jean Durand, demeurant au 1 rue Exemple, 75000 Paris" in text
    assert "La société SEL IRIS, ayant son siège social au 2 rue Pro, 75000 Paris" in text
    assert "Le gérant" in text
    _assert_clean(text)


def test_lettre_option_is_denomination_en_gras_premiere_ligne_du_corps(
    tmp_path: Path,
) -> None:
    # Retour Albane « mise en forme » 1.7 : le NOM DE LA SOCIETE doit figurer EN GRAS
    # dans la PREMIERE LIGNE du corps du courrier (juste avant « Madame, Monsieur, »).
    document = Document(LettreOptionIsGenerator().generate(_base_context(), tmp_path))
    paragraphs = [p for p in document.paragraphs if p.text.strip()]
    salutation_index = next(
        index for index, p in enumerate(paragraphs) if p.text.strip() == "Madame, Monsieur,"
    )
    # La ligne juste AVANT la salutation porte la denomination, entierement en gras.
    denomination_line = paragraphs[salutation_index - 1]
    assert denomination_line.text.strip() == "SCI EXEMPLE"
    runs = [run for run in denomination_line.runs if run.text.strip()]
    assert runs and all(run.bold for run in runs)


def test_lettre_option_is_siren_always_en_cours_immatriculation(tmp_path: Path) -> None:
    """R3 (Albane 2026-06-30) : meme avec un SIREN saisi, la ligne SIREN doit afficher la
    constante « En cours d'immatriculation » (societe en cours de constitution)."""
    ctx = _base_context()
    ctx.societe.siren = "987 654 321"
    output_path = LettreOptionIsGenerator().generate(ctx, tmp_path)
    document = Document(output_path)

    siren_values = [
        row.cells[1].text
        for table in document.tables
        for row in table.rows
        if row.cells[0].text.strip() == "SIREN"
    ]
    assert siren_values == ["En cours d’immatriculation"]
    assert "987 654 321" not in _docx_text(output_path)


def test_lettre_option_is_siren_not_required(tmp_path: Path) -> None:
    """R3 : la lettre se genere meme SANS SIREN (societe pas encore immatriculee)."""
    ctx = _base_context()
    ctx.societe.siren = None
    output_path = LettreOptionIsGenerator().generate(ctx, tmp_path)
    assert "En cours d’immatriculation" in _docx_text(output_path)


def test_lettre_option_is_recipient_block_is_boxed_and_lowered(tmp_path: Path) -> None:
    """R2 (Albane 2026-06-30) : le bloc destinataire est ENCADRE (boite bordee), cale a
    DROITE, et DESCENDU (spacer en tete) pour une enveloppe a fenetre."""
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn

    output_path = LettreOptionIsGenerator().generate(_base_context(), tmp_path)
    document = Document(output_path)

    # 1re table = boite destinataire : 1x1, bordee, calee a droite.
    box = document.tables[0]
    assert (len(box.rows), len(box.columns)) == (1, 1)
    assert box.alignment == WD_TABLE_ALIGNMENT.RIGHT
    borders = box._tbl.tblPr.find(qn("w:tblBorders"))
    assert borders is not None
    assert borders.find(qn("w:top")).get(qn("w:val")) == "single"
    box_text = box.cell(0, 0).text
    assert "Service des impots des entreprises" in box_text
    assert "Centre des Finances Publiques" in box_text

    # Un spacer (paragraphe vide a space_before non nul) precede la boite -> descente.
    body = document.element.body
    first_paragraph = next(
        child for child in body.iterchildren() if child.tag.endswith("}p")
    )
    p_pr = first_paragraph.find(qn("w:pPr"))
    spacing = p_pr.find(qn("w:spacing")) if p_pr is not None else None
    assert spacing is not None
    assert int(spacing.get(qn("w:before"))) > 0


def test_lettre_option_is_requires_option_flag(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="option_is"):
        LettreOptionIsGenerator().generate(_base_context(option_is=False), tmp_path)


def test_lettre_option_is_rejects_non_sci_structure(tmp_path: Path) -> None:
    ctx = _base_context(structure="SELARL")

    with pytest.raises(ValueError, match="dossier.structure"):
        LettreOptionIsGenerator().generate(ctx, tmp_path)
