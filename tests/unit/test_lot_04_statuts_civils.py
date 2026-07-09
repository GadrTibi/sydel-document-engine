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
    StatutsCivilsGroupeParts,
    StatutsCivilsParts,
    StatutsCivilsRepresentant,
)
from sydel_doc_engine.generators.lot_04.statuts_sci import StatutsSciGenerator
from sydel_doc_engine.generators.lot_04.statuts_sci_iris import StatutsSciIrisGenerator
from sydel_doc_engine.generators.lot_04.statuts_scs import StatutsScsGenerator


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


def _person_associe(
    *,
    prenom: str,
    nom: str,
    nb_parts: int,
    debut: int,
    fin: int,
    role: str | None = None,
    montant: str | None = None,
) -> StatutsCivilsAssocie:
    amount = montant or str(nb_parts * 10)
    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        role_statutaire=role,
        genre=Gender.MASCULIN,
        civilite_affichage="Monsieur",
        prenom=prenom,
        prenoms=prenom,
        nom=nom,
        date_naissance="1 janvier 1980",
        ville_naissance="Paris",
        departement_naissance="75",
        nationalite="francaise",
        situation_maritale="celibataire",
        adresse_personnelle=Address(
            num_voie="1",
            voie="rue Exemple",
            cp="75000",
            ville="Paris",
        ),
        apport=StatutsCivilsApport(montant=amount, montant_lettres=amount),
        parts=StatutsCivilsParts(
            nb=nb_parts,
            nb_lettres=str(nb_parts),
            plage_affichee=f"{debut} a {fin}",
            debut=debut,
            fin=fin,
            qualite_associe=role,
        ),
    )


def _morale_associe(*, nb_parts: int, debut: int, fin: int) -> StatutsCivilsAssocie:
    amount = str(nb_parts * 10)
    return StatutsCivilsAssocie(
        type_personne="personne_morale",
        denomination="SEL IRIS",
        forme_juridique="SELARL",
        capital_social="1 000 euros",
        siege=Address(adresse_affichee="2 rue Pro, 75000 Paris"),
        numero_rcs="900 000 001",
        ville_rcs="Paris",
        representant=StatutsCivilsRepresentant(
            civilite_affichage="Monsieur",
            prenom="Jean",
            nom="Durand",
            fonction="gerant",
        ),
        apport=StatutsCivilsApport(montant=amount, montant_lettres=amount),
        parts=StatutsCivilsParts(
            nb=nb_parts,
            nb_lettres=str(nb_parts),
            debut=debut,
            fin=fin,
        ),
    )


def _base_context(
    *,
    structure: str,
    statuts_type: str,
    associes: list[StatutsCivilsAssocie],
) -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure=structure,
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Jean",
            nom="Durand",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 15)),
        societe=Company(
            denomination=f"{structure} EXEMPLE",
            forme_sociale=structure,
            siege=Address(
                num_voie="10",
                voie="rue de la Paix",
                cp="75002",
                ville="Paris",
                adresse_affichee="10 rue de la Paix, 75002 Paris",
            ),
            ville_rcs="Paris",
        ),
        statuts_civils=StatutsCivilsContext(
            type=statuts_type,
            forme_sociale="societe civile",
            mention_capital_variable="a capital variable",
            capital_social="1000",
            capital_social_lettres="mille",
            capital_autorise="10000",
            capital_autorise_lettres="dix mille",
            capital_maximal="10000",
            capital_maximal_lettres="dix mille",
            nb_parts_total=100,
            nb_parts_total_lettres="cent",
            valeur_nominale_part="10",
            valeur_nominale_part_lettres="dix",
            plage_parts_totale="1 a 100",
            duree_societe="99",
            capital_depot=StatutsCivilsCapitalDepot(
                banque_nom="BANQUE EXEMPLE",
                banque_adresse="1 rue Banque, 75009 Paris",
            ),
            associes=associes,
            date_cloture_premier_exercice="31 decembre 2026",
            nombre_exemplaires_lettres="trois",
            denomination_cabinet_mandataire="DAAT",
        ),
    )


def test_statuts_sci_generates_dynamic_associates(tmp_path: Path) -> None:
    ctx = _base_context(
        structure="SCI",
        statuts_type="sci",
        associes=[
            _person_associe(prenom="Jean", nom="Durand", nb_parts=40, debut=1, fin=40),
            _person_associe(prenom="Alice", nom="Martin", nb_parts=60, debut=41, fin=100),
        ],
    )

    output_path = StatutsSciGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)

    # R10 (Rafael 2026-07-07) : le fichier statuts porte la denomination.
    assert output_path.name == "Statuts SCI EXEMPLE.docx"
    assert "ARTICLE 1 - FORME" in text
    assert "Monsieur Jean Durand" in text
    assert "Monsieur Alice Martin" in text
    assert "A Paris, le 15/05/2026" in text
    _assert_clean(text)
    # Retour Albane « mise en forme » 3.2 : le cadre « STATUTS » du SCI (perdu par l'injection,
    # zone de texte flottante du modele) est RESTAURE (comme SCS/micro) entre l'en-tete et les
    # soussignes. Verrou : une table du docx porte « STATUTS ».
    from docx import Document as _Doc

    box_texts = [
        p.text.strip()
        for table in _Doc(output_path).tables
        for row in table.rows
        for cell in row.cells
        for p in cell.paragraphs
        if p.text.strip()
    ]
    assert "STATUTS" in box_texts, "cadre « STATUTS » absent du SCI (3.2)"


def test_statuts_sci_birthdate_reformats_numeric_input(tmp_path: Path) -> None:
    # B1 (Albane 2026-07-09) : la date de naissance saisie au format numerique « JJ/MM/AAAA »
    # (ou ISO) sort en francais lettre « JJ mois AAAA » dans les statuts civils (propagation
    # SCI / SCM / SCS / micro via le socle partage). Une date deja lettree reste inchangee.
    jean = _person_associe(prenom="Jean", nom="Durand", nb_parts=40, debut=1, fin=40)
    jean.date_naissance = "10/03/1975"
    ctx = _base_context(
        structure="SCI",
        statuts_type="sci",
        associes=[
            jean,
            _person_associe(prenom="Alice", nom="Martin", nb_parts=60, debut=41, fin=100),
        ],
    )
    text = _docx_text(StatutsSciGenerator().generate(ctx, tmp_path))
    assert "Né le 10 mars 1975" in text
    assert "10/03/1975" not in text
    # Le second associe garde sa date deja lettree (« 1 janvier 1980 ») telle quelle.
    assert "1 janvier 1980" in text


def test_statuts_scs_requires_commandite_and_commanditaire(tmp_path: Path) -> None:
    ctx = _base_context(
        structure="SCS",
        statuts_type="scs",
        associes=[
            _person_associe(
                prenom="Jean",
                nom="Durand",
                nb_parts=100,
                debut=1,
                fin=100,
                role="commandite",
                montant="1000",
            )
        ],
    )
    ctx.statuts_civils.total_apports_commandites = "1000"

    with pytest.raises(ValueError, match="commanditaire"):
        StatutsScsGenerator().generate(ctx, tmp_path)


def test_statuts_scs_comparution_nom_usage_epouse(tmp_path: Path) -> None:
    # Q4/MH-épouse (Albane 2026-07-01, « comme les modeles ») : le modele SCS ecrit la comparution
    # d'une associee mariee « [civilite] [prenom] [nom_naissance], épouse [nom], née le… » (virgule
    # AVANT « épouse »). Convention : nom = nom d'usage (apport/signature) ; nom_naissance = maiden.
    ctx = _base_context(
        structure="SCS",
        statuts_type="scs",
        associes=[
            _person_associe(
                prenom="Jean", nom="Durand", nb_parts=60, debut=1, fin=60,
                role="commandite", montant="600",
            ),
            _person_associe(
                prenom="Alice", nom="BERTE", nb_parts=40, debut=61, fin=100,
                role="commanditaire", montant="400",
            ),
        ],
    )
    ctx.statuts_civils.total_apports_commandites = "600"
    alice = ctx.statuts_civils.associes[1]
    alice.genre = Gender.FEMININ
    alice.civilite_affichage = "Madame"
    alice.nom_naissance = "GOSSET"  # maiden distinct du nom d'usage marital "BERTE"

    text = _docx_text(StatutsScsGenerator().generate(ctx, tmp_path))
    # Comparution : maiden AVANT, virgule, puis nom d'usage apres « épouse ».
    assert "Madame Alice GOSSET, épouse BERTE" in text


def test_statuts_scs_generates_roles_and_lu_approuve(tmp_path: Path) -> None:
    ctx = _base_context(
        structure="SCS",
        statuts_type="scs",
        associes=[
            _person_associe(
                prenom="Jean",
                nom="Durand",
                nb_parts=60,
                debut=1,
                fin=60,
                role="commandite",
                montant="600",
            ),
            _person_associe(
                prenom="Alice",
                nom="Martin",
                nb_parts=40,
                debut=61,
                fin=100,
                role="commanditaire",
                montant="400",
            ),
        ],
    )
    ctx.statuts_civils.total_apports_commandites = "600"

    output_path = StatutsScsGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)
    document = Document(output_path)
    signature_table_text = "\n".join(
        paragraph.text
        for table in document.tables
        for row in table.rows
        for cell in row.cells
        for paragraph in cell.paragraphs
    )

    assert output_path.name == "Statuts SCS EXEMPLE.docx"
    # En-tete apport (source para 41, accents) rendu par le chemin source, non reduplique.
    assert "Associés commandités" in text
    assert text.count("Associés commandités") == 1
    # Commanditaire : singulier + accent + NBSP avant deux-points (source para 51).
    assert "Associé commanditaire :" in text
    assert "Associes commandites" not in text
    assert "Associes commanditaires" not in text
    # Totaux fideles SCS (source paras 49/56/57/75, NBSP source compris), pas "SOIT AU TOTAL".
    # Rafael 2026-07-09 (SCS art. 6, devise automatique) : lettres + « euros » et
    # chiffres + « € », derives par le moteur (assertion de conformite du jour meme).
    assert "la somme de 600 euros, 	600 €" in text
    assert "Le montant total versé par le commandité est de" in text
    assert "600 €." in text
    assert "Le montant total versé par le commanditaire est de" in text
    assert "400 €." in text
    assert "Total des apports en numéraires :" in text
    assert "1000 €" in text  # capital fixture non groupe (le front groupe en amont)
    assert "euros euros" not in text
    assert "Total des parts sociales composant le capital :" in text
    assert "SOIT AU TOTAL" not in text
    # Depot SCS (source para 57).
    assert "Cette somme de" in text
    assert "a été intégralement versée dès avant ce jour" in text
    # Preambule capital SCS reintroduit (source para 63).
    assert "Le capital social effectif est fixé à" in text
    assert "lesquelles sont attribuées aux associés comme suit" in text
    # Mention signature SCS reaccentuee (source : "Lu et approuvé").
    assert "Lu et approuvé" in signature_table_text
    assert "Lu et approuve" not in signature_table_text
    assert "Monsieur Jean Durand" in signature_table_text
    assert "Monsieur Alice Martin" in signature_table_text
    _assert_clean(text)


def test_statuts_sci_iris_requires_result_groups(tmp_path: Path) -> None:
    ctx = _base_context(
        structure="SCI IRIS",
        statuts_type="sci_iris",
        associes=[
            _morale_associe(nb_parts=40, debut=1, fin=40),
            _person_associe(prenom="Alice", nom="Martin", nb_parts=60, debut=41, fin=100),
        ],
    )

    with pytest.raises(ValueError, match="resultat_groupes_parts"):
        StatutsSciIrisGenerator().generate(ctx, tmp_path)


def test_statuts_sci_iris_generates_morale_and_result_groups(tmp_path: Path) -> None:
    ctx = _base_context(
        structure="SCI IRIS",
        statuts_type="sci_iris",
        associes=[
            _morale_associe(nb_parts=40, debut=1, fin=40),
            _person_associe(prenom="Alice", nom="Martin", nb_parts=60, debut=41, fin=100),
        ],
    )
    ctx.statuts_civils.resultat_groupes_parts = [
        StatutsCivilsGroupeParts(
            parts_debut=1,
            parts_fin=40,
            quote_part_resultat_exceptionnel="40 %",
        ),
        StatutsCivilsGroupeParts(
            parts_debut=41,
            parts_fin=100,
            quote_part_resultat_exceptionnel="60 %",
        ),
    ]
    ctx.statuts_civils.resultat_quote_part_exceptionnel_total = "100 %"

    output_path = StatutsSciIrisGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)
    document = Document(output_path)
    matrix_table_text = "\n".join(
        paragraph.text
        for table in document.tables
        for row in table.rows
        for cell in row.cells
        for paragraph in cell.paragraphs
    )

    # R10 (Rafael 2026-07-07) : le fichier statuts porte la denomination.
    assert output_path.name == "Statuts SCI IRIS EXEMPLE.docx"
    assert "SCI IRIS" in text
    # R4 (Albane 2026-07-07) : « représentée » accentué (comparution + signature),
    # bloc morale « siège / immatriculée / numéro » accentué (constat conformité).
    assert "SEL IRIS, représentée par Monsieur Jean Durand" in text
    assert "representee" not in text
    assert "ayant son siège 2 rue Pro, 75000 Paris" in text
    assert "immatriculée au RCS de Paris sous le numéro 900 000 001." in text
    assert "Représentée par Monsieur Jean Durand, gerant." in text
    assert "ayant son siege" not in text
    assert "immatriculee" not in text
    assert "sous le numero" not in text
    # En-tete + lignes du tableau resultat reaccentues, fideles au modele source IRIS
    # ("Quote-part du résultat exceptionnel", "Parts numérotées de [debut] à [fin]").
    assert "Quote-part du résultat exceptionnel" in matrix_table_text
    assert "Parts numérotées de 1 à 40" in matrix_table_text
    assert "Parts numérotées de 41 à 100" in matrix_table_text
    assert "Parts 1 a 40" not in matrix_table_text
    assert "40 %" in matrix_table_text
    assert "Total" in matrix_table_text
    assert "100 %" in matrix_table_text
    _assert_clean(text)


# --- FORME : filet R1 (la sortie herite la forme du modele Albane, plus l'ancien profil SYDEL) -


def _named_styles_present(document: Document) -> set[str]:
    return {style.name for style in document.styles}


def _has_title_box(document: Document) -> bool:
    return any(p.text.strip() == "STATUTS" for t in document.tables for r in t.rows
              for c in r.cells for p in c.paragraphs)


def test_statuts_sci_inherits_model_form(tmp_path: Path) -> None:
    # R1 (Albane 2026-06-30) : la SCI doit heriter la FORME du modele Albane (page custom
    # 20,95 x 29,67, marge droite 2,19 cm de la section gouvernante, styles nommes Title /
    # Heading 1) — plus l'ancien profil SYDEL (Letter US 21,59 x 27,94, marges 2,5, Roboto 10).
    ctx = _base_context(
        structure="SCI",
        statuts_type="sci",
        associes=[
            _person_associe(prenom="Jean", nom="Durand", nb_parts=40, debut=1, fin=40),
            _person_associe(prenom="Alice", nom="Martin", nb_parts=60, debut=41, fin=100),
        ],
    )
    document = Document(StatutsSciGenerator().generate(ctx, tmp_path))
    section = document.sections[0]

    assert abs(section.page_width - Cm(20.95)) < Cm(0.05)
    assert abs(section.page_height - Cm(29.67)) < Cm(0.05)
    assert abs(section.right_margin - Cm(2.19)) < Cm(0.05)
    # PAS la page Letter US ni les marges 2,5 du profil SYDEL ecrase.
    assert abs(section.page_width - Cm(21.59)) > Cm(0.05)
    assert {"Title", "Heading 1"} <= _named_styles_present(document)
    # Un seul sectPr (section unifiee) -> mise en page coherente.
    assert len(document.element.body.findall(qn("w:sectPr"))) == 1
    # M2 (Akainu 2026-06-30) : pas de paragraphe vide d'amorce en tete de page 1 -> body[0] est
    # le titre (la denomination), comme le modele (l'amorce vide decalait le rendu vers le bas).
    assert document.paragraphs[0].text.strip() == "SCI EXEMPLE"


def test_statuts_sci_iris_inherits_model_form_and_pagination_footer(tmp_path: Path) -> None:
    ctx = _base_context(
        structure="SCI IRIS",
        statuts_type="sci_iris",
        associes=[
            _morale_associe(nb_parts=40, debut=1, fin=40),
            _person_associe(prenom="Alice", nom="Martin", nb_parts=60, debut=41, fin=100),
        ],
    )
    ctx.statuts_civils.resultat_groupes_parts = [
        StatutsCivilsGroupeParts(
            parts_debut=1, parts_fin=40, quote_part_resultat_exceptionnel="40 %"
        ),
        StatutsCivilsGroupeParts(
            parts_debut=41, parts_fin=100, quote_part_resultat_exceptionnel="60 %"
        ),
    ]
    document = Document(StatutsSciIrisGenerator().generate(ctx, tmp_path))
    section = document.sections[0]

    assert abs(section.page_width - Cm(20.95)) < Cm(0.05)
    # Marge droite gouvernante 2,19 cm (PAS la marge 3,2 cm du sectPr final du modele).
    assert abs(section.right_margin - Cm(2.19)) < Cm(0.05)
    assert {"Title", "Heading 1"} <= _named_styles_present(document)
    # Footer de pagination natif du modele preserve (champ PAGE).
    assert "PAGE" in section.footer._element.xml


def test_statuts_scs_inherits_model_form(tmp_path: Path) -> None:
    ctx = _base_context(
        structure="SCS",
        statuts_type="scs",
        associes=[
            _person_associe(prenom="Jean", nom="Durand", nb_parts=60, debut=1, fin=60,
                            role="commandite", montant="600"),
            _person_associe(prenom="Alice", nom="Martin", nb_parts=40, debut=61, fin=100,
                            role="commanditaire", montant="400"),
        ],
    )
    ctx.statuts_civils.total_apports_commandites = "600"
    document = Document(StatutsScsGenerator().generate(ctx, tmp_path))
    section = document.sections[0]

    # Modele SCS = A4 (21 x 29,7), marges 2,5 propres au modele (et non au profil SYDEL Letter US).
    assert abs(section.page_width - Cm(21.0)) < Cm(0.05)
    assert abs(section.page_height - Cm(29.7)) < Cm(0.05)
    assert abs(section.page_width - Cm(21.59)) > Cm(0.05)  # pas Letter US
    assert {"Title", "Heading 1"} <= _named_styles_present(document)
