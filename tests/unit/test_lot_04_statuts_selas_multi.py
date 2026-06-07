from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Company,
    DocumentGenerationContext,
    Person,
    Signature,
    StatutsCivilsApport,
    StatutsCivilsAssocie,
    StatutsCivilsRepresentant,
    StatutsSelasMultiContext,
    StatutsSelasMultiPresident,
)
from sydel_doc_engine.generators.lot_04.statuts_selas_multi import StatutsSelasMultiGenerator


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(paragraph.text for paragraph in cell.paragraphs if paragraph.text)
    return "\n".join(texts)


def _physical_associe(
    *,
    prenoms: str,
    nom: str,
    nb_actions: int,
    montant: str,
    montant_lettres: str,
    qualite: str = "associée exerçante",
) -> StatutsCivilsAssocie:
    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=Gender.FEMININ,
        civilite_affichage="Madame",
        prenom=prenoms,
        prenoms=prenoms,
        nom=nom,
        date_naissance="1 janvier 1980",
        ville_naissance="Lyon",
        departement_naissance="69",
        nationalite="française",
        profession="Docteur",
        situation_maritale="célibataire",
        adresse_personnelle_affichee="10 rue de l'Exemple, 69000 Lyon",
        qualification_principale="qualifiée en médecine générale",
        ordre_departemental="Rhône",
        numero_ordre="69-12345",
        numero_rpps="10100000001",
        apport=StatutsCivilsApport(montant=montant, montant_lettres=montant_lettres),
        qualite_capital=qualite,
        nb_actions=nb_actions,
        nb_actions_lettres=str(nb_actions),
    )


def _morale_associe(
    *,
    nb_actions: int,
    montant: str,
    montant_lettres: str,
) -> StatutsCivilsAssocie:
    return StatutsCivilsAssocie(
        type_personne="personne_morale",
        denomination="SOCIETE CIVILE EXEMPLE",
        forme_juridique="Société Civile, à capital variable",
        capital_social="1 020",
        siege=Address(adresse_affichee="2 avenue Pro, 69000 Lyon"),
        ville_rcs="Lyon",
        numero_rcs="900 000 001",
        representant=StatutsCivilsRepresentant(
            civilite_affichage="Monsieur",
            prenom="Paul",
            nom="Martin",
            fonction="gérant",
        ),
        apport=StatutsCivilsApport(montant=montant, montant_lettres=montant_lettres),
        qualite_capital="associée non exerçante",
        nb_actions=nb_actions,
        nb_actions_lettres=str(nb_actions),
    )


def _context(associes: list[StatutsCivilsAssocie]) -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure="SELAS",
        personne_signataire=Person(
            genre=Gender.FEMININ,
            civilite="Madame",
            prenom="Claire",
            nom="Durand",
        ),
        signature=Signature(lieu="Lyon", date=date(2026, 5, 15)),
        societe=Company(
            denomination="SELAS EXEMPLE",
            forme_sociale="SELAS",
            siege=Address(adresse_affichee="5 place du Centre, 69000 Lyon"),
            ville_rcs="Lyon",
        ),
        statuts_selas_multi=StatutsSelasMultiContext(
            profession_reglementee="médecin",
            profession_reglementee_pluriel="médecins",
            capital_social="1 000",
            capital_social_lettres="mille",
            nb_actions_total=100,
            nb_actions_total_lettres="cent",
            valeur_nominale_action="10",
            valeur_nominale_action_lettres="dix",
            adresse_lieu_exercice="5 place du Centre, 69000 Lyon",
            banque_nom="BANQUE EXEMPLE",
            banque_adresse="1 rue Banque, 69009 Lyon",
            date_cloture_premier_exercice="31 décembre 2026",
            associes=associes,
            president=StatutsSelasMultiPresident(ref_associe_index=0),
        ),
    )


def test_selas_multi_generates_clean_docx(tmp_path: Path) -> None:
    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Claire",
                nom="Durand",
                nb_actions=75,
                montant="750",
                montant_lettres="sept cent cinquante",
            ),
            _morale_associe(
                nb_actions=25,
                montant="250",
                montant_lettres="deux cent cinquante",
            ),
        ]
    )

    output_path = StatutsSelasMultiGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)

    assert output_path.name == "statuts_selas_multi.docx"
    # 0 placeholder residuel
    assert "[" not in text
    assert "]" not in text


def test_selas_multi_asserts_source_wording(tmp_path: Path) -> None:
    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Claire",
                nom="Durand",
                nb_actions=75,
                montant="750",
                montant_lettres="sept cent cinquante",
            ),
            _morale_associe(
                nb_actions=25,
                montant="250",
                montant_lettres="deux cent cinquante",
            ),
        ]
    )

    output_path = StatutsSelasMultiGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)

    # En-tete / forme (wording source)
    assert "Société d’exercice libéral par Actions Simplifiée de médecin" in text
    assert "LES SOUSSIGNEES :" in text
    # Comparution multi : personne physique + ligne ordre + personne morale
    assert (
        "Madame Claire Durand, Docteur qualifiée en médecine générale, née le 1 janvier 1980 "
        "à Lyon (69), de nationalité française, demeurant 10 rue de l'Exemple, 69000 Lyon, "
        "célibataire." in text
    )
    assert (
        "Inscrite au tableau du conseil de l’ordre des médecins du Rhône sous le numéro "
        "départemental 69-12345, et sous le numéro RPPS 10100000001." in text
    )
    assert (
        "La SOCIETE CIVILE EXEMPLE, Société Civile, à capital variable, au capital de 1 020 "
        "euros dont le siège social est situé au 2 avenue Pro, 69000 Lyon, immatriculée au "
        "RCS de Lyon sous le numéro 900 000 001, représentée par son représentant légal, "
        "Monsieur Paul Martin." in text
    )
    # Article 7 - Apports (wording source, point final present pour la morale, absent pour la pp)
    assert (
        "Madame Claire Durand, apporte à la société la somme de sept cent cinquante (750) euros"
        in text
    )
    assert (
        "La SOCIETE CIVILE EXEMPLE, apporte à la société la somme de deux cent cinquante (250) "
        "euros." in text
    )
    assert "Total des apports\xa0en numéraire" in text
    # Article 8 - Capital / repartition en actions (vocabulaire actions, jamais parts)
    assert "Il est divisé en cent (100) actions d" in text
    assert "dix (10 €) chacune, entièrement libérées, et attribuées aux associés comme suit\xa0:" in text
    assert "Madame Claire Durand, associée exerçante, détient 75 actions" in text
    assert "La SOCIETE CIVILE EXEMPLE, associée non exerçante, détient 25 actions" in text
    assert "Total des actions\xa0:\t\t\t\t\t\t\t\t100 actions" in text
    # Les blocs DYNAMIQUES generes par le moteur emploient le vocabulaire actions
    # (jamais "parts sociales") : on l'assert sur les lignes de repartition reinjectees.
    assert "détient 75 actions" in text
    assert "détient 25 actions" in text
    assert "parts sociales" not in text.split("ARTICLE 8")[1].split("ARTICLE 9")[0]
    # Clause majorite de controle (wording source conserve)
    assert (
        "En aucun cas la répartition du capital ne pourra être modifiée dans des conditions "
        "qui retireraient la majorité des droits de vote aux associés exerçant dans la "
        "société." in text
    )
    # Article 14 - Presidence : designation du president (personne physique)
    assert "ARTICLE 14 – PRESIDENCE" in text
    assert "est nommée présidente de la Société et ce pour une durée illimitée." in text
    # Article 15 - Directeurs Generaux : present, generique (source conservee)
    assert "ARTICLE 15 - DIRECTEURS GENERAUX" in text
    assert "15-1 - DESIGNATION" in text
    # Signature multi
    assert "Fait à Lyon, le 15/05/2026" in text


def test_selas_multi_requires_minimum_two_associes(tmp_path: Path) -> None:
    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Claire",
                nom="Durand",
                nb_actions=100,
                montant="1000",
                montant_lettres="mille",
            ),
        ]
    )

    with pytest.raises(ValueError, match="au moins"):
        StatutsSelasMultiGenerator().generate(ctx, tmp_path)


def test_selas_multi_rejects_action_total_mismatch(tmp_path: Path) -> None:
    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Claire",
                nom="Durand",
                nb_actions=75,
                montant="750",
                montant_lettres="sept cent cinquante",
            ),
            _morale_associe(
                nb_actions=10,
                montant="100",
                montant_lettres="cent",
            ),
        ]
    )

    with pytest.raises(ValueError, match="somme des actions"):
        StatutsSelasMultiGenerator().generate(ctx, tmp_path)
