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


def test_selas_multi_valeur_nominale_decimale_n1(tmp_path: Path) -> None:
    # N1 (Akainu re-gate 2026-06-24) : une valeur nominale DECIMALE (1,25) doit GENERER le SELAS
    # multi sans crash (_required_text levait sur lettres vide = BLOQUANT B1), sans marqueur
    # « À COMPLÉTER » dans l'acte (M2), et sans DOUBLE « euro ». La mise en lettres d'un decimal
    # = la FIGURE (number_words_from_value). Ce test est le verrou bout-en-bout qui manquait.
    from sydel_doc_engine.front_app.field_derivations import number_words_from_value

    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Claire", nom="Durand", nb_actions=75,
                montant="750", montant_lettres="sept cent cinquante",
            ),
            _morale_associe(
                nb_actions=25, montant="250", montant_lettres="deux cent cinquante",
            ),
        ]
    )
    # Cas B1 prouve par Akainu : 125 / 100 actions = 1,25 (valeur nominale decimale).
    ctx.statuts_selas_multi.valeur_nominale_action = "1,25"
    ctx.statuts_selas_multi.valeur_nominale_action_lettres = number_words_from_value("1,25")

    output_path = StatutsSelasMultiGenerator().generate(ctx, tmp_path)  # ne doit PAS lever
    text = _docx_text(output_path)

    assert "1,25" in text  # figure decimale presente
    assert "À COMPLÉTER" not in text  # pas de marqueur technique dans l'acte
    assert "euro euro" not in text and "euros euro" not in text  # pas de double euro
    assert "centimes" not in text  # pas de forme monetaire non ratifiee emise


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
    assert (
        "dix (10 €) chacune, entièrement libérées, et attribuées aux associés comme suit\xa0:"
        in text
    )
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


def _dentiste_associe(
    *,
    prenoms: str,
    nom: str,
    genre: Gender,
    civilite: str,
    nb_actions: int,
    montant: str,
    montant_lettres: str,
    qualite: str,
    situation_maritale: str,
) -> StatutsCivilsAssocie:
    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=genre,
        civilite_affichage=civilite,
        prenom=prenoms,
        prenoms=prenoms,
        nom=nom,
        date_naissance="20 février 1994",
        ville_naissance="RENNES",
        departement_naissance="35",
        nationalite="française",
        profession="chirurgien-dentiste",
        situation_maritale=situation_maritale,
        adresse_personnelle_affichee="31B Boulevard de Sévigné, 35700 RENNES",
        qualification_principale="qualifié en chirurgie dentaire",
        ordre_departemental="l’Ille et Vilaine",
        numero_ordre="79630",
        numero_rpps="10101676194",
        apport=StatutsCivilsApport(montant=montant, montant_lettres=montant_lettres),
        qualite_capital=qualite,
        nb_actions=nb_actions,
        nb_actions_lettres=str(nb_actions),
    )


def _dentiste_context(associes: list[StatutsCivilsAssocie]) -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure="SELAS",
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Jean-Guillaume",
            nom="FUCHS",
        ),
        signature=Signature(lieu="Rennes", date=date(2026, 9, 22)),
        societe=Company(
            denomination="Cabinet Dentaire Test & Associés",
            forme_sociale="SELAS",
            siege=Address(adresse_affichee="12 rue de la Paix, 35000 RENNES"),
            ville_rcs="Rennes",
        ),
        statuts_selas_multi=StatutsSelasMultiContext(
            profession_reglementee="chirurgien-dentiste",
            profession_reglementee_pluriel="chirurgiens-dentistes",
            capital_social="1 020",
            capital_social_lettres="MILLE VINGT",
            nb_actions_total=1020,
            nb_actions_total_lettres="MILLE VINGT",
            valeur_nominale_action="0,01",
            valeur_nominale_action_lettres="UN CENTIME D’EURO",
            adresse_lieu_exercice="12 rue de la Paix, 35000 RENNES",
            banque_nom="Crédit Mutuel",
            banque_adresse="5 rue du Centre, 35000 Rennes",
            date_cloture_premier_exercice="31 décembre 2026",
            associes=associes,
            president=StatutsSelasMultiPresident(ref_associe_index=0),
        ),
    )


def test_selas_multi_dentiste_genere_depuis_le_corpus_dentiste(tmp_path: Path) -> None:
    # Fidelite : une SELAS dentiste pluripersonnelle doit sortir le corpus DENTISTE
    # (R. 4113-1 Code de la sante publique, "chirurgien-dentiste", articles 1-32, Directeur
    # General) et JAMAIS le wording medecin (deontologie medicale, conseil de l'ordre des
    # medecins). Le choix se fait sur profession_reglementee.
    ctx = _dentiste_context(
        associes=[
            _dentiste_associe(
                prenoms="Jean-Guillaume",
                nom="FUCHS",
                genre=Gender.MASCULIN,
                civilite="Monsieur",
                nb_actions=510,
                montant="510",
                montant_lettres="CINQ CENT DIX",
                qualite="associé exerçant",
                situation_maritale="marié sous le régime de la séparation des biens",
            ),
            _dentiste_associe(
                prenoms="Marie",
                nom="LEROUX",
                genre=Gender.FEMININ,
                civilite="Madame",
                nb_actions=510,
                montant="510",
                montant_lettres="CINQ CENT DIX",
                qualite="associée exerçante",
                situation_maritale="mariée sous le régime de la communauté",
            ),
        ]
    )

    output_path = StatutsSelasMultiGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)

    # 0 placeholder residuel.
    assert "[" not in text
    assert "]" not in text

    # Marqueurs PROPRES au corpus dentiste (absents du corpus medecin).
    assert "R. 4113-1 et suivants du Code de la santé publique" in text
    assert "l’exercice en commun de la profession de chirurgien-dentiste" in text
    assert "l’ordonnance n°2023-77 du 8 février 2023" in text
    assert "Conseil Départemental de l’Ordre des Chirurgiens-dentistes" in text
    assert "Article 19 - Président de La société" in text
    assert "Article 20 - Directeur Général" in text
    assert "Article 32 - Convention sur la preuve – signature électronique" in text

    # AUCUN wording medecin ne doit fuiter.
    assert "conseil de l’ordre des médecins" not in text
    assert "Société d’exercice libéral par Actions Simplifiée de médecin" not in text

    # Comparution dentiste : UNE ligne combinee par associe, wording dentiste
    # ("au tableau de l'Ordre des ...", "numero national"), accord en genre.
    assert (
        "Monsieur Jean-Guillaume FUCHS, chirurgien-dentiste, de nationalité française, né le "
        "20 février 1994 à RENNES (35), marié sous le régime de la séparation des biens, "
        "demeurant 31B Boulevard de Sévigné, 35700 RENNES, inscrit au tableau de l’Ordre des "
        "chirurgiens-dentistes de l’Ille et Vilaine sous le numéro national 79630 et sous le "
        "numéro RPPS 10101676194." in text
    )
    assert (
        "Madame Marie LEROUX, chirurgien-dentiste, de nationalité française, née le 20 février "
        "1994 à RENNES (35), mariée sous le régime de la communauté, demeurant 31B Boulevard "
        "de Sévigné, 35700 RENNES, inscrite au tableau de l’Ordre des chirurgiens-dentistes de "
        "l’Ille et Vilaine sous le numéro national 79630 et sous le numéro RPPS 10101676194."
        in text
    )

    # Boilerplate concret du modele dentiste remplace par les donnees de la societe.
    assert "La société est dénommée « Cabinet Dentaire Test & Associés »," in text
    assert "Le siège de la société est fixé au 12 rue de la Paix, 35000 RENNES." in text
    assert (
        "Cette somme a été déposée au crédit du compte ouvert dans les livres de la Banque "
        "Crédit Mutuel, 5 rue du Centre, 35000 Rennes." in text
    )
    assert (
        "Le capital social est fixé à la somme de 1 020 € (MILLE VINGT) euros divisé en 1020 "
        "actions de 0,01 € (UN CENTIME D’EURO) chacune, entièrement libéré et attribué comme "
        "suit" in text
    )
    # Les valeurs-exemple du modele ne doivent pas fuiter.
    assert "Cabinet Dentaire Fuchs & Associés" not in text
    assert "Chassereau" not in text
    assert "Banque BPGO" not in text
    assert "102.000 actions" not in text

    # Apports (Article 6, wording dentiste) : "- Le Docteur X, apporte [LETTRES] euros" + "Ci".
    assert "- Le Docteur Jean-Guillaume FUCHS, apporte CINQ CENT DIX euros" in text
    assert "- Le Docteur Marie LEROUX, apporte CINQ CENT DIX euros" in text
    assert "Total des apports\t\t\t\t\t\t\t\t\t1 020 euros" in text
    # Repartition du capital (Article 6, wording dentiste) : "- [civilite] X, [LETTRES] actions".
    assert "- Monsieur Jean-Guillaume FUCHS, 510 actions" in text
    assert "- Madame Marie LEROUX, 510 actions" in text
    assert "Total des actions composant le capital social\xa0: \t\t\t\t\t1020 actions" in text

    # Signature dentiste : "Fait a [lieu]" + date + ligne de noms.
    assert "Fait à Rennes" in text
    assert "Le 22/09/2026" in text
    assert "Jean-Guillaume FUCHS\t\t\t\tMarie LEROUX" in text


def test_selas_multi_physical_associe_masculin_accorde_ne_et_inscrit(tmp_path: Path) -> None:
    # Audit 2026-06-17 : « née » et « Inscrite » etaient figes au feminin dans la
    # comparution -> un associe MASCULIN sortait « née … Inscrite ». Desormais
    # accorde sur le genre de chaque associe.
    homme = _physical_associe(
        prenoms="Paul",
        nom="Martin",
        nb_actions=25,
        montant="250",
        montant_lettres="deux cent cinquante",
        qualite="associé exerçant",
    ).model_copy(update={"genre": Gender.MASCULIN, "civilite_affichage": "Monsieur"})
    femme = _physical_associe(
        prenoms="Claire",
        nom="Durand",
        nb_actions=75,
        montant="750",
        montant_lettres="sept cent cinquante",
    )
    ctx = _context(associes=[femme, homme])

    text = _docx_text(StatutsSelasMultiGenerator().generate(ctx, tmp_path))

    # Femme : accord feminin conserve.
    assert "Madame Claire Durand, Docteur qualifiée en médecine générale, née le" in text
    assert "Inscrite au tableau du conseil de l’ordre des médecins" in text
    # Homme : accord masculin (le bug).
    assert "Monsieur Paul Martin, Docteur qualifiée en médecine générale, né le" in text
    assert "Inscrit au tableau du conseil de l’ordre des médecins" in text
    # Pas de « née »/« Inscrite » accole au nom de l'homme.
    assert "Monsieur Paul Martin, Docteur qualifiée en médecine générale, née le" not in text
