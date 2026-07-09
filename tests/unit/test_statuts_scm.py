from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Cm

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Company,
    DocumentGenerationContext,
    Person,
    Signature,
    StatutsCivilsApport,
    StatutsCivilsAssocie,
    StatutsCivilsCapitalDepot,
    StatutsCivilsContext,
    StatutsCivilsParts,
    StatutsCivilsRepresentant,
)
from sydel_doc_engine.generators.lot_04.statuts_scm import StatutsScmGenerator


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(paragraph.text for paragraph in cell.paragraphs if paragraph.text)
    return "\n".join(texts)


def _assert_clean(text: str) -> None:
    assert "[" not in text
    assert "]" not in text


def _morale_associe(*, parts: int = 70, apport: str = "700") -> StatutsCivilsAssocie:
    return StatutsCivilsAssocie(
        type_personne="personne_morale",
        denomination="SELARL DURAND",
        forme_juridique="SELARL",
        profession="chirurgien-dentiste",
        capital_social="1 000 euros",
        siege=Address(adresse_affichee="5 rue Royale, 75008 Paris"),
        numero_rcs="900 000 001",
        ville_rcs="Paris",
        representant=StatutsCivilsRepresentant(
            civilite_affichage="Monsieur",
            prenom="Jean",
            nom="Durand",
            fonction="gerant",
        ),
        # Rafael 2026-07-09 : lettres NUES comme le front reel (number_words_from_value) ;
        # l'unite « euro(s) » est desormais DERIVEE par le generateur (art. 6).
        apport=StatutsCivilsApport(montant=apport, montant_lettres="sept cents"),
        parts=StatutsCivilsParts(nb=parts),
    )


def _person_associe(*, parts: int = 50, apport: str = "500") -> StatutsCivilsAssocie:
    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=Gender.FEMININ,
        civilite_affichage="Madame",
        prenom="Alice",
        prenoms="Alice",
        nom="Martin",
        profession="chirurgien-dentiste",
        date_naissance="2 fevrier 1982",
        ville_naissance="Lyon",
        nationalite="francaise",
        situation_maritale="celibataire",
        adresse_personnelle_affichee="2 rue Exemple, 69000 Lyon",
        # Rafael 2026-07-09 : lettres NUES (unite derivee par le generateur, art. 6).
        apport=StatutsCivilsApport(montant=apport, montant_lettres="cinq cents"),
        parts=StatutsCivilsParts(nb=parts),
    )


def _context() -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure="SCM",
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Jean",
            nom="Durand",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 15)),
        societe=Company(
            denomination="SCM CABINET DURAND MARTIN",
            denomination_courte="CABINET DURAND MARTIN",
            forme_sociale="Societe civile de moyens",
            siege=Address(
                num_voie="10",
                voie="rue de la Paix",
                cp="75002",
                ville="Paris",
            ),
        ),
        statuts_civils=StatutsCivilsContext(
            type="scm",
            forme_sociale="Societe civile de moyens",
            capital_social="1200",
            # Rafael 2026-07-09 : lettres NUES (unite derivee par le generateur).
            capital_social_lettres="mille deux cents",
            nb_parts_total=120,
            valeur_nominale_part="10 euros",
            capital_depot=StatutsCivilsCapitalDepot(
                banque_nom="BANQUE EXEMPLE",
                banque_adresse="1 rue Banque, 75009 Paris",
            ),
            associes=[
                _morale_associe(),
                _person_associe(),
            ],
        ),
    )


def test_statuts_scm_generates_dynamic_associates_apports_parts_and_signatures(
    tmp_path: Path,
) -> None:
    output_path = StatutsScmGenerator().generate(_context(), tmp_path)
    text = _docx_text(output_path)
    document = Document(output_path)
    table_text = "\n".join(
        paragraph.text
        for table in document.tables
        for row in table.rows
        for cell in row.cells
        for paragraph in cell.paragraphs
    )
    lu_approuve = next(p for p in document.paragraphs if "Lu et approuvé" in p.text)

    # R10 (Rafael 2026-07-07) : le fichier statuts porte la denomination.
    assert output_path.name == "Statuts SCM CABINET DURAND MARTIN.docx"
    assert "Article 4 ‐ Objet social" in text
    # Ligne d'apport personne morale : le modele source (para 81) porte "La [denomination]
    # apporte ..." SANS representant ("representee par ..." n'existe qu'en comparution).
    assert "La SELARL DURAND apporte à la Société la somme de sept cents euros" in text
    # Ligne de repartition des parts personne morale : source (para 95) = "[denomination][nb]
    # parts", denomination NUE, sans representant.
    assert "SELARL DURAND 70 parts" in text
    # Aucun "representee par ..." ne doit polluer les lignes d'apport / de parts (D1 + D2).
    assert "SELARL DURAND, représentée par Monsieur Jean Durand apporte" not in text
    assert "SELARL DURAND, représentée par Monsieur Jean Durand 70 parts" not in text
    assert "Madame Alice Martin 50 parts" in text
    # Rafael 2026-07-09 (SCM art. 6, devise automatique) : lettres + « euros » et
    # chiffres + « € », derives par le moteur — assertion de conformite du jour meme.
    assert "ci- 500 €." in text
    assert "ci- 700 €." in text
    assert "Total des apports mille deux cents euros (1200 €)" in text
    assert "euros euros" not in text
    assert "510" not in text
    assert "« Lu et approuvé »" in text
    assert "STATUTS" in table_text
    assert any(run.italic for run in lu_approuve.runs)
    _assert_clean(text)


def test_statuts_scm_entete_capital_accord_singulier(tmp_path: Path) -> None:
    # Akainu M1 (2026-07-09) : l'en-tete « [capital_social]euros » codait « euros » en dur
    # -> « Au capital de 1 euros » a capital=1. Accord via montant_avec_euros -> « 1 euro ».
    ctx = _context()
    ctx.statuts_civils.capital_social = "1"
    ctx.statuts_civils.capital_social_lettres = "un"
    ctx.statuts_civils.nb_parts_total = 1
    ctx.statuts_civils.valeur_nominale_part = "1"
    ctx.statuts_civils.associes = [_morale_associe(parts=1, apport="1")]
    text = _docx_text(StatutsScmGenerator().generate(ctx, tmp_path))
    assert "Au capital de 1 euro" in text
    assert "Au capital de 1 euros" not in text


def test_statuts_scm_inherits_model_form_single_logo(tmp_path: Path) -> None:
    # R1 (Albane 2026-06-30) : la SCM herite la FORME du modele (page custom ~21 x 29,7,
    # marges du modele) et son header porte le logo SYDEL DEJA present dans le modele. Le rendu
    # ne doit PAS rappeler add_header_logo (sinon DOUBLE logo) -> exactement 1 image en header,
    # 0 dans le corps. Le footer du modele (vide) n'est plus ecrase par une denomination.
    document = Document(StatutsScmGenerator().generate(_context(), tmp_path))
    section = document.sections[0]

    assert abs(section.page_height - Cm(29.7)) < Cm(0.1)
    # Pas la page Letter US du profil SYDEL ecrase.
    assert abs(section.page_width - Cm(21.59)) > Cm(0.1)
    header_logos = section.header._element.findall(".//" + qn("a:blip"))
    body_logos = document.element.body.findall(".//" + qn("a:blip"))
    assert len(header_logos) == 1  # logo herite du modele, non double
    assert len(body_logos) == 0
    assert len(document.element.body.findall(qn("w:sectPr"))) == 1
    # M2 (Akainu 2026-06-30) : pas de paragraphe vide d'amorce -> body[0] = titre (denomination).
    assert document.paragraphs[0].text.strip() != ""


def test_statuts_scm_blocks_when_parts_total_is_ambiguous(tmp_path: Path) -> None:
    ctx = _context()
    ctx.statuts_civils.associes[1].parts.nb = None

    with pytest.raises(ValueError, match="associes\\[\\]\\.parts\\.nb"):
        StatutsScmGenerator().generate(ctx, tmp_path)


def test_statuts_scm_blocks_when_capital_total_is_inconsistent(tmp_path: Path) -> None:
    ctx = _context()
    ctx.statuts_civils.associes[1].apport.montant = "510"

    with pytest.raises(ValueError, match="capital_social"):
        StatutsScmGenerator().generate(ctx, tmp_path)


def test_statuts_scm_requires_morale_representant_for_signature(tmp_path: Path) -> None:
    ctx = _context()
    ctx.statuts_civils.associes[0].representant = None

    with pytest.raises(ValueError, match="representant"):
        StatutsScmGenerator().generate(ctx, tmp_path)
