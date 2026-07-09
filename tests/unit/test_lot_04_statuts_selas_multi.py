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

    # ST1 (Albane 2026-06-26) : le nom de la societe est porte par l'intitule du doc
    # (« Statuts <denomination>.docx »), comme les statuts civils / SELARL.
    assert output_path.name == "Statuts SELAS EXEMPLE.docx"
    # 0 placeholder residuel
    assert "[" not in text
    assert "]" not in text


def test_selas_multi_valeur_nominale_decimale_n1(tmp_path: Path) -> None:
    # N1 (Akainu re-gate 2026-06-24) : une valeur nominale DECIMALE (1,25) doit GENERER le SELAS
    # multi sans crash ni marqueur « À COMPLÉTER », et sans DOUBLE « euro ».
    # 7.5 (Albane 2026-07-06, verbatim RATIFIE) : la mise en LETTRES monetaire est desormais
    # ratifiee -> 1,25 rend « un euro et vingt-cinq centimes (1,25 €) » (la figure entre
    # parentheses est preservee). Plus de figure nue dans le slot lettres.
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

    assert "un euro et vingt-cinq centimes (1,25 €)" in text  # 7.5 : lettres + figure
    assert "À COMPLÉTER" not in text  # pas de marqueur technique dans l'acte
    assert "euro euro" not in text and "euros euro" not in text  # pas de double euro


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
    # Comparution multi : personne physique + ligne ordre + personne morale.
    # ST2 (Albane 2026-06-26) : plus de titre « Docteur » parasite devant la
    # qualification (le front figeait profession=« Docteur ») -> la qualification
    # (profession reelle saisie) porte seule. Le fixture garde date_naissance
    # « 1 janvier 1980 » : ST3 (zero-pad du jour) est applique au FRONT a la saisie,
    # pas dans le generateur (echo fidele) -> ce builder direct conserve « 1 janvier ».
    assert (
        "Madame Claire Durand, qualifiée en médecine générale, née le 1 janvier 1980 "
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
    # Retour Albane « mise en forme » 2.3 : le mot « euros » (accorde, VN=10 -> pluriel)
    # doit figurer apres la valeur en lettres — « de dix euros (10 €) chacune ». L'ancien
    # rendu « dix (10 €) chacune » (sans euro) etait le DEFAUT corrige (M1).
    assert (
        "de dix euros (10 €) chacune, entièrement libérées, et attribuées aux associés "
        "comme suit\xa0:" in text
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
    # Article 14 - Presidence (Albane 2026-06-26, DOUBLON-PRESIDENT) : la designation
    # NOMINATIVE du president a ete RETIREE du statut (le PV de nomination reste le seul a le
    # nommer). Seule subsiste la CLAUSE GENERIQUE de gerance.
    assert "ARTICLE 14 – PRESIDENCE" in text
    assert (
        "est gérée par un Président, choisi parmi les associés exerçant la profession au sein "
        "de la Société et nommé avec ou sans limitation de durée"
    ) in text  # clause generique conservee
    assert "est nommée présidente de la Société et ce pour une durée illimitée." not in text
    assert "est nommé président de la Société et ce pour une durée illimitée." not in text
    assert "Sa rémunération sera fixée ultérieurement" not in text
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


def test_selas_multi_dentiste_n6_entete_tirets_annexe(tmp_path: Path) -> None:
    # N6 (Rafael 2026-06-24, re-gate Akainu) : verrouille les 3 points codables des statuts SELAS
    # dentiste pluri : pt1 en-tete « STATUTS », pt3 puces a tiret (style « Tirets » du modele :
    # art.1, 14, 16, 21...), pt4 annexe sur nouvelle page. pt2 (aeration) = flag Rafael (ambigu).
    from docx.oxml.ns import qn

    ctx = _dentiste_context(
        associes=[
            _dentiste_associe(
                prenoms="Jean-Guillaume", nom="FUCHS", genre=Gender.MASCULIN,
                civilite="Monsieur", nb_actions=510, montant="510",
                montant_lettres="CINQ CENT DIX", qualite="associé exerçant",
                situation_maritale="marié sous le régime de la séparation des biens",
            ),
            _dentiste_associe(
                prenoms="Marie", nom="LEROUX", genre=Gender.FEMININ,
                civilite="Madame", nb_actions=510, montant="510",
                montant_lettres="CINQ CENT DIX", qualite="associée exerçante",
                situation_maritale="mariée sous le régime de la communauté",
            ),
        ]
    )
    output_path = StatutsSelasMultiGenerator().generate(ctx, tmp_path)
    full_text = _docx_text(output_path)  # inclut les tables (la title box STATUTS est une table)
    document = Document(output_path)
    texts = [p.text for p in document.paragraphs]

    # pt1 : en-tete STATUTS present (rendu dans une title box = table, pas un paragraphe simple)
    assert "STATUTS" in full_text, "en-tete STATUTS manquant (pt1)"
    # pt3 : les puces a tiret du CORPUS STATIQUE doivent etre rendues avec « - ». Ancres reparties
    # sur PLUSIEURS articles (art.1, art. fin-de-mandat, decisions collectives) pour verrouiller le
    # caractere SYSTEMIQUE revendique — PAS les blocs dynamiques apports/capital qui ont deja leur
    # propre « - » (Akainu re-gate N6 : sans ces ancres statiques, neutraliser le fix garde le test
    # vert). Sans _is_tiret_list_paragraph, ces lignes du modele perdent leur tiret.
    assert "- par les présents statuts." in full_text, "tiret art.1 manquant (pt3)"
    assert "- son décès," in full_text, "tiret art. fin-de-mandat manquant (pt3)"
    assert (
        "- fusion, scission, apport partiel" in full_text
    ), "tiret art. decisions collectives manquant (pt3)"
    assert texts  # garde-fou : le document a bien des paragraphes
    # pt4 : un saut de page existe (avant l'annexe)
    has_page_break = any(
        br.get(qn("w:type")) == "page"
        for p in document.paragraphs
        for run in p.runs
        for br in run._element.findall(qn("w:br"))
    )
    assert has_page_break, "aucun saut de page annexe (pt4)"


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
    # ST5 (Albane 2026-06-26) : le nom de la societe est harmonise en MAJUSCULES.
    assert "La société est dénommée « CABINET DENTAIRE TEST & ASSOCIÉS »," in text
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

    # Apports (Article 6, wording dentiste). Rafael 2026-07-09 « supprimer partout » : l'apporteur
    # designe « Le Docteur X » -> civilite CIVILE accordee au genre (Monsieur/Madame), sans article.
    assert "- Monsieur Jean-Guillaume FUCHS, apporte CINQ CENT DIX euros" in text
    assert "- Madame Marie LEROUX, apporte CINQ CENT DIX euros" in text
    assert "Docteur" not in text
    assert "Total des apports\t\t\t\t\t\t\t\t\t1 020 euros" in text
    # Repartition du capital (Article 6, wording dentiste) : "- [civilite] X, [LETTRES] actions".
    assert "- Monsieur Jean-Guillaume FUCHS, 510 actions" in text
    assert "- Madame Marie LEROUX, 510 actions" in text
    assert "Total des actions composant le capital social\xa0: \t\t\t\t\t1020 actions" in text

    # Signature dentiste : "Fait a [lieu]" + date + cases de signature (ST7h : tableau borde,
    # une case ~5 cm par signataire — les noms ne sont plus tabules sur une seule ligne).
    assert "Fait à Rennes" in text
    assert "Le 22/09/2026" in text
    assert "Jean-Guillaume FUCHS" in text
    assert "Marie LEROUX" in text


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

    # Femme : accord feminin conserve. ST2 (2026-06-26) : plus de « Docteur » parasite.
    assert "Madame Claire Durand, qualifiée en médecine générale, née le" in text
    assert "Inscrite au tableau du conseil de l’ordre des médecins" in text
    # Homme : accord masculin (le bug).
    assert "Monsieur Paul Martin, qualifiée en médecine générale, né le" in text
    assert "Inscrit au tableau du conseil de l’ordre des médecins" in text
    # Pas de « née »/« Inscrite » accole au nom de l'homme.
    assert "Monsieur Paul Martin, qualifiée en médecine générale, née le" not in text


# --- Retours Albane 2026-06-26 (lot « Statuts SELAS multi ») : tests adversariaux ----------


def test_st1_nom_fichier_porte_la_denomination(tmp_path: Path) -> None:
    # ST1 : « remettre le nom de la societe dans l'intitule du doc des statuts pour avoir
    # "Statuts nom" ». Le fichier de sortie n'est plus fige « statuts_selas_multi.docx ».
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
    ctx.societe.denomination = "Cabinet Durand"

    output_path = StatutsSelasMultiGenerator().generate(ctx, tmp_path)

    assert output_path.name == "Statuts Cabinet Durand.docx"
    assert output_path.name != "statuts_selas_multi.docx"


def test_st2_comparution_sans_docteur_parasite(tmp_path: Path) -> None:
    # ST2 : « j'ai "Monsieur Jean Durant, Docteur Medecin generaliste", il y a un "Docteur"
    # en trop car je n'ai rien ajoute dans le formulaire ». La profession « Docteur » figee
    # par le front ne doit plus prefixer la qualification (= profession reelle saisie).
    homme = _physical_associe(
        prenoms="Jean", nom="Durant", nb_actions=75,
        montant="750", montant_lettres="sept cent cinquante",
        qualite="associé exerçant",
    ).model_copy(
        update={
            "genre": Gender.MASCULIN,
            "civilite_affichage": "Monsieur",
            "profession": "Docteur",  # valeur figee par le front (#9)
            "qualification_principale": "Médecin généraliste",
        }
    )
    autre = _physical_associe(
        prenoms="Claire", nom="Martin", nb_actions=25,
        montant="250", montant_lettres="deux cent cinquante",
    )
    ctx = _context(associes=[homme, autre])

    text = _docx_text(StatutsSelasMultiGenerator().generate(ctx, tmp_path))

    assert "Monsieur Jean Durant, Médecin généraliste, né le" in text
    # Le « Docteur » parasite a disparu (ni « Docteur Médecin » double, ni « Docteur » seul).
    assert "Docteur Médecin généraliste" not in text
    assert "Jean Durant, Docteur" not in text


def test_st5_denomination_article_en_majuscules(tmp_path: Path) -> None:
    # ST5 : « le nom est a moitie en majuscule et minuscule, harmoniser pour mettre en
    # majuscule partout ». Le paragraphe autonome portant la denomination (art. 3) sort en
    # MAJUSCULES, quelle que soit la casse saisie.
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
    ctx.societe.denomination = "Cabinet Durand"

    document = Document(StatutsSelasMultiGenerator().generate(ctx, tmp_path))
    paras = [p.text.strip() for p in document.paragraphs if p.text.strip()]

    # Le paragraphe AUTONOME du nom (art. 3) est en majuscules.
    assert "CABINET DURAND" in paras
    # La casse mixte saisie n'apparait PAS comme paragraphe-nom autonome.
    assert "Cabinet Durand" not in paras


def test_doublon_president_designation_nominative_retiree_des_statuts(tmp_path: Path) -> None:
    # DOUBLON-PRESIDENT (Albane 2026-06-26) : « on a deja nomme le president dans les statuts et
    # on a une nouvelle decision [PV] qui le nomme president ; il ne faudrait pas de doublon ->
    # retirer la partie des statuts [designation nominative] et supprimer le paragraphe suivant
    # sur sa remuneration. » Albane TRANCHE : le PV reste le seul a nommer nominativement le
    # dirigeant. Ce test SUPERSEDE l'ancien test ST6 (accord de genre de la phrase nominative
    # DANS le statut) : la phrase ayant disparu du statut, son accord est sans objet (le genre
    # reste gere dans le PV de nomination, hors de ce generateur).
    #
    # Verrou pour les DEUX sexes : ni la variante masculine ni la feminine ne doit subsister, ni
    # le bloc nom+adresse nominatif, ni le paragraphe de remuneration. La clause GENERIQUE de
    # gerance, elle, est CONSERVEE.
    homme = _physical_associe(
        prenoms="Jean", nom="Durant", nb_actions=75,
        montant="750", montant_lettres="sept cent cinquante", qualite="associé exerçant",
    ).model_copy(update={"genre": Gender.MASCULIN, "civilite_affichage": "Monsieur"})
    autre = _physical_associe(
        prenoms="Claire", nom="Martin", nb_actions=25,
        montant="250", montant_lettres="deux cent cinquante",
    )

    for label, president, autres in (
        ("homme", homme, [autre]),
        (
            "femme",
            _physical_associe(
                prenoms="Claire", nom="Durand", nb_actions=75,
                montant="750", montant_lettres="sept cent cinquante",
            ),
            [_morale_associe(nb_actions=25, montant="250", montant_lettres="deux cent cinquante")],
        ),
    ):
        ctx = _context(associes=[president, *autres])
        text = _docx_text(StatutsSelasMultiGenerator().generate(ctx, tmp_path / label))
        # (1) designation nominative RETIREE (les deux genres).
        assert "est nommé président de la Société et ce pour une durée illimitée." not in text
        assert "est nommée présidente de la Société et ce pour une durée illimitée." not in text
        # (2) paragraphe de remuneration (qui suivait la designation) RETIRE.
        assert "Sa rémunération sera fixée ultérieurement" not in text
        # (3) le nom + l'adresse nominatifs du president ne sont plus injectes a l'art. 14.1
        #     (le PV les porte desormais seul).
        assert "Monsieur Jean Durant\nDemeurant" not in text
        assert "Madame Claire Durand\nDemeurant" not in text
        # (4) la CLAUSE GENERIQUE de gerance est CONSERVEE (cadre statutaire intact).
        assert (
            "est gérée par un Président, choisi parmi les associés exerçant la profession au "
            "sein de la Société et nommé avec ou sans limitation de durée"
        ) in text


# =============================================================================================
# ST7 — PRESENTATION des statuts SELAS multi (Albane 2026-06-26, section « Statuts »).
# Tests ADVERSARIAUX sur la sortie DOCX reelle : alignement, gras, casse, hauteur de case.
# =============================================================================================

from docx.enum.text import WD_ALIGN_PARAGRAPH as _AL  # noqa: E402


def _para_is_bold(paragraph) -> bool:
    """Vrai si tous les runs non vides du paragraphe sont en gras."""
    runs = [r for r in paragraph.runs if r.text.strip()]
    return bool(runs) and all(r.bold for r in runs)


def _find_paras(document, predicate):
    return [p for p in document.paragraphs if predicate(p.text.strip())]


def test_st7a_entete_medecin_centre_et_nom_gras(tmp_path: Path) -> None:
    # ST7a : centrer l'en-tete, et le NOM de la societe en gras dans l'en-tete.
    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Jean", nom="Durand", nb_actions=75,
                montant="750", montant_lettres="sept cent cinquante",
            ),
            _morale_associe(
                nb_actions=25, montant="250", montant_lettres="deux cent cinquante",
            ),
        ]
    )
    ctx.societe.denomination = "Cabinet Durand"
    document = Document(StatutsSelasMultiGenerator().generate(ctx, tmp_path))

    # Le NOM de la societe (token autonome) : 1re occurrence = en-tete -> CENTRE + GRAS + MAJ.
    noms = _find_paras(document, lambda t: t == "CABINET DURAND")
    assert noms, "le nom de la societe en majuscules est introuvable"
    entete_nom = noms[0]
    assert entete_nom.alignment == _AL.CENTER
    assert _para_is_bold(entete_nom)

    # Les 3 lignes d'en-tete (forme, capital, siege) sont CENTREES (le nom seul est gras).
    forme = _find_paras(document, lambda t: t.startswith("Société d’exercice libéral"))
    capital = _find_paras(document, lambda t: t.startswith("Au capital de"))
    siege_entete = _find_paras(document, lambda t: t.startswith("Siège social"))
    assert forme and forme[0].alignment == _AL.CENTER
    assert capital and capital[0].alignment == _AL.CENTER
    assert siege_entete and siege_entete[0].alignment == _AL.CENTER


def test_st7d_article3_nom_centre_et_gras(tmp_path: Path) -> None:
    # ST7d : article 3 — le nom de la societe au milieu (centre) en gras.
    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Jean", nom="Durand", nb_actions=75,
                montant="750", montant_lettres="sept cent cinquante",
            ),
            _morale_associe(
                nb_actions=25, montant="250", montant_lettres="deux cent cinquante",
            ),
        ]
    )
    ctx.societe.denomination = "Cabinet Durand"
    document = Document(StatutsSelasMultiGenerator().generate(ctx, tmp_path))

    # 2e occurrence du nom autonome = art. 3 (la 1re est l'en-tete) ; centree + grasse.
    noms = _find_paras(document, lambda t: t == "CABINET DURAND")
    assert len(noms) >= 2, "le nom autonome de l'article 3 est introuvable"
    art3_nom = noms[1]
    assert art3_nom.alignment == _AL.CENTER
    assert _para_is_bold(art3_nom)


def test_st7e_article4_siege_centre_et_gras(tmp_path: Path) -> None:
    # ST7e : article 4 — le siege social centre/gras comme le nom.
    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Jean", nom="Durand", nb_actions=75,
                montant="750", montant_lettres="sept cent cinquante",
            ),
            _morale_associe(
                nb_actions=25, montant="250", montant_lettres="deux cent cinquante",
            ),
        ]
    )
    document = Document(StatutsSelasMultiGenerator().generate(ctx, tmp_path))
    siege = _find_paras(document, lambda t: t.startswith("Le siège social est fixé au"))
    assert siege, "la phrase du siege social (art. 4) est introuvable"
    assert siege[0].alignment == _AL.CENTER
    assert _para_is_bold(siege[0])


def test_st7f_president_designation_nominative_supprimee(tmp_path: Path) -> None:
    # ST7f (nom+adresse du president en gras a l'art. 14.1) est SUPERSEDE par DOUBLON-PRESIDENT
    # (Albane 2026-06-26) : la designation nominative ayant ete retiree du statut, il n'y a plus
    # de bloc nom+adresse a mettre en gras a l'art. 14.1. Ce test verrouille desormais l'ABSENCE
    # de ce bloc nominatif (le PV de nomination le porte seul).
    president = _physical_associe(
        prenoms="Jean", nom="Durant", nb_actions=75,
        montant="750", montant_lettres="sept cent cinquante", qualite="associé exerçant",
    ).model_copy(update={"genre": Gender.MASCULIN, "civilite_affichage": "Monsieur"})
    autre = _physical_associe(
        prenoms="Claire", nom="Martin", nb_actions=25,
        montant="250", montant_lettres="deux cent cinquante",
    )
    ctx = _context(associes=[president, autre])
    document = Document(StatutsSelasMultiGenerator().generate(ctx, tmp_path))

    # Le bloc nominatif du president (« Monsieur Jean Durant » + « Demeurant … ») n'est PLUS
    # injecte a l'art. 14.1 : aucun paragraphe ne porte ce nom seul, ni l'adresse en designation.
    nom_pres = _find_paras(document, lambda t: t == "Monsieur Jean Durant")
    adresse_pres = _find_paras(document, lambda t: t.startswith("Demeurant 10 rue de l'Exemple"))
    assert not nom_pres, "le nom nominatif du president ne doit plus figurer a l'art. 14.1"
    assert not adresse_pres, "l'adresse nominative du president ne doit plus figurer a l'art. 14.1"


def test_st7g_titres_articles_16_17_22_en_majuscules(tmp_path: Path) -> None:
    # ST7g : articles 16, 17, 22 — titres a casse cassee mis en MAJUSCULES integrales.
    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Jean", nom="Durand", nb_actions=75,
                montant="750", montant_lettres="sept cent cinquante",
            ),
            _morale_associe(
                nb_actions=25, montant="250", montant_lettres="deux cent cinquante",
            ),
        ]
    )
    text = _docx_text(StatutsSelasMultiGenerator().generate(ctx, tmp_path))

    # Les titres source a casse cassee sont ABSENTS ; leur version MAJUSCULES est presente.
    assert "des DECISIONS sociales" not in text
    assert "ENTRE leS DIRIgerantS" not in text
    assert "variation du capital" not in text
    assert "ARTICLE 16 – DES DECISIONS SOCIALES" in text
    assert "ARTICLE 17 - CONVENTIONS ENTRE LES DIRIGERANTS OU LES ASSOCIES ET LA SOCIETE" in text
    assert "ARTICLE 22 – VARIATION DU CAPITAL" in text


def test_st7h_signature_cases_borduees_de_cinq_cm(tmp_path: Path) -> None:
    # ST7h : cases de signature ~5 cm pour que l'encadre passe sans decaler les noms.
    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Jean", nom="Durand", nb_actions=75,
                montant="750", montant_lettres="sept cent cinquante",
            ),
            _morale_associe(
                nb_actions=25, montant="250", montant_lettres="deux cent cinquante",
            ),
        ]
    )
    document = Document(StatutsSelasMultiGenerator().generate(ctx, tmp_path))

    # Une case (cellule de tableau) par signataire, hauteur de ligne >= ~5 cm.
    signature_tables = []
    for table in document.tables:
        cell_texts = [c.text for c in table.rows[0].cells]
        if any("Jean Durand" in t for t in cell_texts):
            signature_tables.append(table)
    assert signature_tables, "le tableau de signature (ST7h) est introuvable"
    sig = signature_tables[0]
    row = sig.rows[0]
    assert row.height is not None, "la hauteur de case de signature n'est pas posee"
    assert row.height.cm >= 4.9, f"case de signature trop petite : {row.height.cm} cm"
    # Une cellule par signataire (le nom n'est plus tabule sur une seule ligne).
    assert len(sig.rows[0].cells) == 2
    cell_texts = [c.text for c in sig.rows[0].cells]
    assert any("Jean Durand" in t for t in cell_texts)
    assert any("SOCIETE CIVILE EXEMPLE" in t for t in cell_texts)


def test_st7b_espace_avant_et_apres_le_cadre_statuts(tmp_path: Path) -> None:
    # ST7b : de l'espace avant ET apres le cadre des statuts.
    from docx.oxml.ns import qn

    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Jean", nom="Durand", nb_actions=75,
                montant="750", montant_lettres="sept cent cinquante",
            ),
            _morale_associe(
                nb_actions=25, montant="250", montant_lettres="deux cent cinquante",
            ),
        ]
    )
    document = Document(StatutsSelasMultiGenerator().generate(ctx, tmp_path))

    # Parcours du corps en ordre de document : reperer le cadre « STATUTS » (table) et verifier
    # qu'un paragraphe (espaceur) le precede ET le suit immediatement.
    body = document.element.body
    seq = []
    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            txt = "".join(n.text or "" for n in child.iter(qn("w:t")))
            seq.append(("P", txt.strip()))
        elif child.tag == qn("w:tbl"):
            txt = "".join(n.text or "" for n in child.iter(qn("w:t")))
            seq.append(("TBL", txt.strip()))
    box_idx = next(i for i, (k, t) in enumerate(seq) if k == "TBL" and "STATUTS" in t)
    assert seq[box_idx - 1] == ("P", ""), "espaceur AVANT le cadre STATUTS manquant (ST7b)"
    assert seq[box_idx + 1] == ("P", ""), "espaceur APRES le cadre STATUTS manquant (ST7b)"


def test_st7c_espace_entre_chaque_soussigne(tmp_path: Path) -> None:
    # ST7c : de l'espace entre chaque soussigne (au debut).
    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Jean", nom="Durand", nb_actions=50,
                montant="500", montant_lettres="cinq cents",
            ),
            _physical_associe(
                prenoms="Claire", nom="Martin", nb_actions=50,
                montant="500", montant_lettres="cinq cents",
            ),
        ]
    )
    document = Document(StatutsSelasMultiGenerator().generate(ctx, tmp_path))
    texts = [p.text.strip() for p in document.paragraphs]

    # Entre la fin de la comparution de l'associe 1 (ligne « Inscrit(e)… ») et le debut de
    # l'associe 2 (« Madame Claire Martin … »), il y a un paragraphe vide (espaceur ST7c).
    idx_a1_fin = next(
        i for i, t in enumerate(texts) if t.startswith("Inscrit") and "au tableau du conseil" in t
    )
    idx_a2_debut = next(
        i for i, t in enumerate(texts)
        if t.startswith("Madame Claire Martin") and i > idx_a1_fin
    )
    assert any(texts[j] == "" for j in range(idx_a1_fin + 1, idx_a2_debut)), (
        "aucun espaceur entre les deux soussignes (ST7c)"
    )


def test_st7h_signature_cases_dentiste(tmp_path: Path) -> None:
    # ST7h propage au corpus dentiste : cases de signature ~5 cm, une par signataire.
    ctx = _dentiste_context(
        associes=[
            _dentiste_associe(
                prenoms="Jean-Guillaume", nom="FUCHS", genre=Gender.MASCULIN,
                civilite="Monsieur", nb_actions=510, montant="510",
                montant_lettres="CINQ CENT DIX", qualite="associé exerçant",
                situation_maritale="marié sous le régime de la séparation des biens",
            ),
            _dentiste_associe(
                prenoms="Marie", nom="LEROUX", genre=Gender.FEMININ,
                civilite="Madame", nb_actions=510, montant="510",
                montant_lettres="CINQ CENT DIX", qualite="associée exerçante",
                situation_maritale="mariée sous le régime de la communauté",
            ),
        ]
    )
    document = Document(StatutsSelasMultiGenerator().generate(ctx, tmp_path))
    signature_tables = [
        t for t in document.tables
        if any("FUCHS" in c.text for c in t.rows[0].cells)
    ]
    assert signature_tables, "tableau de signature dentiste introuvable (ST7h)"
    row = signature_tables[0].rows[0]
    assert row.height is not None and row.height.cm >= 4.9
    assert len(row.cells) == 2


def _art8_line(text: str) -> str:
    """Ligne art.8 « Il est divisé en ... actions ... chacune » du corps rendu."""
    for line in text.split("\n"):
        if "Il est divisé en" in line and "actions" in line and "chacune" in line:
            return line
    raise AssertionError("ligne article 8 introuvable dans le rendu SELAS multi")


def test_selas_multi_article_8_rend_euro_singulier_vn_1(tmp_path: Path) -> None:
    # Retour Albane « mise en forme » 2.3 (M1) : la SELAS PLURIPERSONNELLE doit rendre
    # le mot « euro » (accorde) apres la valeur nominale en lettres. VN=1 -> « un euro ».
    # Le modele multi ne portait PAS le token « [euro_nominal_word] » -> le mot manquait.
    from sydel_doc_engine.front_app.field_derivations import number_words_from_value

    ctx = _context(
        associes=[
            _physical_associe(
                prenoms="Claire", nom="Durand", nb_actions=75,
                montant="75", montant_lettres="soixante-quinze",
            ),
            _morale_associe(
                nb_actions=25, montant="25", montant_lettres="vingt-cinq",
            ),
        ]
    )
    ctx.statuts_selas_multi.valeur_nominale_action = "1"
    ctx.statuts_selas_multi.valeur_nominale_action_lettres = number_words_from_value("1")

    line = _art8_line(_docx_text(StatutsSelasMultiGenerator().generate(ctx, tmp_path)))
    # Elision voyelle + euro singulier + figure : « d'un euro (1 €) ».
    assert "actions d’un euro (1 €) chacune" in line
    # Pas de double euro, pas de forme sans euro.
    assert "euro euro" not in line and "euros euro" not in line
    assert "d’un (1 €)" not in line  # ancien defaut (sans euro)


def test_selas_multi_article_8_rend_euros_pluriel_vn_10(tmp_path: Path) -> None:
    # Retour Albane 2.3 (M1) : VN>=2 -> « euros » au pluriel + connecteur « de » (consonne).
    line = _art8_line(
        _docx_text(
            StatutsSelasMultiGenerator().generate(
                _context(
                    associes=[
                        _physical_associe(
                            prenoms="Claire", nom="Durand", nb_actions=75,
                            montant="750", montant_lettres="sept cent cinquante",
                        ),
                        _morale_associe(
                            nb_actions=25, montant="250",
                            montant_lettres="deux cent cinquante",
                        ),
                    ]
                ),
                tmp_path,
            )
        )
    )
    # Contexte par defaut : VN=10 -> « de dix euros (10 €) ».
    assert "actions de dix euros (10 €) chacune" in line
    assert "de dix (10 €)" not in line  # ancien defaut (sans euro)
