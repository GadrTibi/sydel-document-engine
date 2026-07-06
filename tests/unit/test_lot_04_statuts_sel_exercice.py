from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pytest
from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Apport,
    Associe,
    CapitalContext,
    CessionBanque,
    Company,
    DepotFonds,
    DirigeantNomine,
    DocumentContext,
    DocumentGenerationContext,
    DocumentSignataire,
    DossierOptions,
    ExerciceLieu,
    ExerciceSocial,
    GeranceContext,
    Person,
    Signature,
    SpfplConjoint,
    SpfplOrdre,
    StatutsCivilsApport,
    StatutsCivilsAssocie,
    StatutsCivilsParts,
    StatutsCivilsRepresentant,
    StatutsSel,
)
from sydel_doc_engine.generators.lot_04.statuts_selarl_dentiste import (
    StatutsSelarlDentisteGenerator,
)
from sydel_doc_engine.generators.lot_04.statuts_selarl_medecin import (
    StatutsSelarlMedecinGenerator,
)
from sydel_doc_engine.generators.lot_04.statuts_selas_medecin import (
    StatutsSelasMedecinGenerator,
)
from sydel_doc_engine.orchestrator.service import DocumentOrchestrator
from sydel_doc_engine.registry.catalog import build_seed_catalog


def _associate(*, gender: Gender = Gender.MASCULIN) -> Associe:
    return Associe(
        genre=gender,
        civilite_affichage="Docteur",
        prenom="Camille",
        nom="Martin",
        nb_parts=1000,
        profession="medecin",
        profession_reglementee="medecin",
        profession_reglementee_pluriel="medecins",
        qualification_principale="cardiologue",
        titre_professionnel="Docteur",
        qualite="associe unique",
        date_naissance=date(1980, 1, 2),
        ville_naissance="Paris",
        departement_naissance="75",
        nationalite="francaise",
        situation_maritale="marie",
        regime_matrimonial="communaute legale",
        conjoint=SpfplConjoint(
            civilite_affichage="Madame",
            prenom="Alice",
            nom="Martin",
        ),
        adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
        ordre=SpfplOrdre(
            professionnel="Ordre des medecins",
            departement="Paris",
            ville="Paris",
            numero="12345",
            numero_rpps="10000000001",
        ),
        apport_numeraire="1 000",
        apport_numeraire_lettres="mille",
    )


def _context(*, overlay: str, gender: Gender = Gender.MASCULIN) -> DocumentGenerationContext:
    structure = "SELAS" if overlay == "selas_medecin" else "SELARL"
    return DocumentGenerationContext(
        structure=structure,
        dossier_options=DossierOptions(associe_unique=True),
        personne_signataire=Person(
            genre=gender,
            civilite="Monsieur" if gender == Gender.MASCULIN else "Madame",
            prenom="Camille",
            nom="Martin",
        ),
        signature=Signature(
            lieu="Paris",
            date=date(2026, 5, 14),
            prestataire_signature_electronique="Yousign",
        ),
        societe=Company(
            denomination="SEL MARTIN",
            forme_sociale="societe d'exercice liberal par actions simplifiee",
            forme_sociale_complete=(
                "Societe d'exercice liberal par actions simplifiee"
                if overlay == "selas_medecin"
                else "Societe d'exercice liberal a responsabilite limitee"
            ),
            forme_sociale_abregee="SELAS",
            capital_social="1 000",
            capital_social_lettres="mille",
            duree="99 ans",
            siege=Address(adresse_affichee="10 rue de la Paix, 75002 Paris"),
        ),
        statuts_sel=StatutsSel(overlay=overlay, profession="medecin"),
        associes=[_associate(gender=gender)],
        dirigeant_nomine=DirigeantNomine(
            genre=gender,
            civilite_affichage="Docteur",
            prenom="Camille",
            nom="Martin",
            fonction_affichage="President",
            ref_associe_index=0,
            duree_mandat="illimitee",
        ),
        capital=CapitalContext(
            montant="1 000",
            montant_lettres="mille",
            nombre_titres_total=1000,
            nombre_titres_total_lettres="mille",
            valeur_nominale_titre="1",
            # Akainu n-1 (2026-07-03) : valeur RÉALISTE (le front dérive via number_words_from_value
            # -> « un », SANS « euro » ; le mot « euro » est ajoute par le token [euro_nominal_word]
            # de l'art.8). « un euro » ici incrustait un double « euro » masque par les assertions.
            valeur_nominale_titre_lettres="un",
            type_titre="actions" if overlay == "selas_medecin" else "parts_sociales",
        ),
        apport=Apport(montant="1 000", montant_lettres="mille"),
        depot_fonds=DepotFonds(
            banque=CessionBanque(
                nom="BANQUE EXEMPLE",
                adresse_affichee="1 boulevard Haussmann, 75009 Paris",
            )
        ),
        exercice_social=ExerciceSocial(
            debut="1er janvier",
            fin="31 decembre",
            date_cloture_premier_exercice="31 decembre 2026",
            lieux=[ExerciceLieu(adresse_affichee="12 avenue de la Republique, 75011 Paris")],
        ),
        gerance=GeranceContext(
            seuil_achat_materiel="10 000 euros",
            seuil_emprunt="50 000 euros",
        ),
        document=DocumentContext(
            nombre_exemplaires_lettres="trois",
            signataire=DocumentSignataire(prenom="Camille", nom="Martin"),
        ),
    )


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(paragraph.text for paragraph in cell.paragraphs if paragraph.text)
    return "\n".join(texts)


def _docx_paragraphs(path: Path) -> list[str]:
    return [paragraph.text for paragraph in Document(path).paragraphs if paragraph.text.strip()]


def _assert_clean(text: str) -> None:
    assert "[" not in text
    assert "]" not in text


def _assert_annex_starts_next_page(path: Path) -> None:
    document = Document(path)
    annex_index = next(
        index for index, paragraph in enumerate(document.paragraphs) if paragraph.text == "ANNEXE"
    )
    preceding_xml = "\n".join(
        paragraph._p.xml for paragraph in document.paragraphs[max(0, annex_index - 2) : annex_index]
    )
    assert 'w:type="page"' in preceding_xml


def test_statuts_selarl_dentiste_generates_unique_associate_docx(tmp_path: Path) -> None:
    ctx = _context(overlay="selarl_dentiste")
    ctx.associes[0].profession = "chirurgien-dentiste"
    ctx.associes[0].profession_reglementee = "chirurgien-dentiste"
    ctx.associes[0].profession_reglementee_pluriel = "chirurgiens-dentistes"
    ctx.associes[0].ordre.professionnel = "Ordre des chirurgiens-dentistes"

    output_path = StatutsSelarlDentisteGenerator().generate(ctx, tmp_path)

    text = _docx_text(output_path)
    document = Document(output_path)
    table_text = "\n".join(
        paragraph.text
        for table in document.tables
        for row in table.rows
        for cell in row.cells
        for paragraph in cell.paragraphs
    )
    article_1 = next(p for p in document.paragraphs if p.text.startswith("ARTICLE 1"))

    # Retour Albane 2026-06-10 : intitulé du doc = « Statuts {dénomination} ».
    assert output_path.name == "Statuts SEL MARTIN.docx"
    assert "SEL MARTIN" in text
    assert "Au capital de 1 000 euros" in text
    # Retour Albane 2026-06-10 (DENTISTE) : « marié avec Mme » déplacé juste après
    # l'adresse du domicile + n° d'inscription à l'ordre ajouté avant le RPPS.
    assert "marié sous le régime de la communauté avec Madame Alice Martin" in text
    assert "sous le numéro d’inscription 12345 et sous le numéro RPPS 10000000001" in text
    assert "sous le numéro RPPS 10000000001, marié" not in text
    assert "marié sous le régime de la communauté légale" not in text
    assert "ARTICLE 5 - LIEU(X) D’EXERCICE" in text
    assert (
        "Le lieu d’exercice de la société est situé au "
        "12 avenue de la Republique, 75011 Paris. Il constitue le lieu d’exercice unique "
        "de la société"
    ) in text
    # Retour Albane 2026-06-10 : « euros » ajouté art. 7 (chiffres + lettres) et art. 8
    # des statuts DENTISTE (le bloc médecin l'avait déjà).
    assert "apporte à la Société la somme de 1 000 euros." in text
    assert "Total des apports en numéraire : ci- 1 000 euros." in text
    assert "Le capital social est fixé à la somme de mille euros." in text
    assert (
        "à Docteur Camille Martin, mille parts sociales en pleine propriété, ci"
    ) in text
    assert "1000 parts" in text
    assert "chirurgiens-dentistes" in text
    assert "Yousign" in text
    assert "STATUTS" in table_text
    assert "- Ouverture d’un compte bancaire" in text
    assert any(run.underline for run in article_1.runs)
    _assert_annex_starts_next_page(output_path)
    _assert_clean(text)


def test_statuts_selarl_medecin_skips_personne_2_source_alias(tmp_path: Path) -> None:
    output_path = StatutsSelarlMedecinGenerator().generate(
        _context(overlay="selarl_medecin"),
        tmp_path,
    )

    text = _docx_text(output_path)

    assert output_path.name == "Statuts SEL MARTIN.docx"
    assert "Conseil" in text
    assert "personne_2" not in text
    assert "50 000 euros" in text
    assert (
        "sous le numéro national 12345 et sous le numéro RPPS 10000000001, "
        "marié sous le régime de la communauté avec Madame Alice Martin."
    ) in text
    assert "Docteur Camille Martin, associé unique." in text
    assert "- Ouverture d’un compte bancaire" in text
    _assert_annex_starts_next_page(output_path)
    _assert_clean(text)


def test_statuts_selarl_medecin_renders_separation_de_biens_clause(
    tmp_path: Path,
) -> None:
    ctx = _context(overlay="selarl_medecin")
    ctx.associes[0].regime_matrimonial = "separation de biens"

    output_path = StatutsSelarlMedecinGenerator().generate(ctx, tmp_path)

    text = _docx_text(output_path)

    assert (
        "marié sous le régime de la séparation de biens avec Madame Alice Martin"
    ) in text
    assert "marié sous le régime de separation de biens" not in text
    _assert_clean(text)


def test_statuts_sel_exercice_celibataire_sans_conjoint(tmp_path: Path) -> None:
    # Retour Rafael 2026-06-25 (#2) : un associé CÉLIBATAIRE ne doit PAS exiger de conjoint
    # (avant : add_conjoint_replacements levait ValueError) ni rendre de clause matrimoniale
    # parasite. La clause rend juste « célibataire », sans « sous le régime de … avec … ».
    ctx = _context(overlay="selarl_medecin")
    # Le front fournit la situation deja accentuee (situation_display) ; le generateur est
    # byte-fidele a son entree.
    ctx.associes[0].situation_maritale = "célibataire"
    ctx.associes[0].regime_matrimonial = ""
    ctx.associes[0].conjoint = None

    output_path = StatutsSelarlMedecinGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)

    assert "célibataire" in text
    assert "marié" not in text
    assert "mariée" not in text
    assert "avec Madame" not in text
    assert "sous le régime de" not in text
    _assert_clean(text)


def test_statuts_sel_exercice_pacse_shows_partner(tmp_path: Path) -> None:
    # Albane 6.3/7.3 (RATIFIE 2026-07-06) : un associe PACSE affiche son PARTENAIRE
    # (« pacsé avec Madame Alice Martin »), SANS « sous le régime de … » (pas de sous-regime PACS).
    ctx = _context(overlay="selarl_medecin")
    ctx.associes[0].situation_maritale = "pacsé"
    ctx.associes[0].regime_matrimonial = ""
    text = _docx_text(StatutsSelarlMedecinGenerator().generate(ctx, tmp_path))
    assert "pacsé avec Madame Alice Martin" in text
    assert "sous le régime de" not in text
    _assert_clean(text)


def test_statuts_sel_exercice_pacse_feminin_sans_partenaire(tmp_path: Path) -> None:
    # Genre feminin + « pas de mention sans nom » : un pacse SANS partenaire rend « pacsée » nu.
    ctx = _context(overlay="selarl_medecin", gender=Gender.FEMININ)
    ctx.associes[0].situation_maritale = "pacsée"
    ctx.associes[0].regime_matrimonial = ""
    ctx.associes[0].conjoint = None
    text = _docx_text(StatutsSelarlMedecinGenerator().generate(ctx, tmp_path))
    assert "pacsée" in text
    assert "pacsée avec" not in text
    assert "sous le régime de" not in text
    assert "COMPLÉTER" not in text
    _assert_clean(text)


def test_statuts_sel_exercice_pacse_brut_value_accented(tmp_path: Path) -> None:
    # Le flux SELARL PRINCIPAL passe la valeur BRUTE (« pacse », non accentuee) au generateur ;
    # `marital_status_display` doit l'ACCENTUER (« pacsé »), comme pour le marie — jamais « pacse
    # avec … » (accent manquant) en sortie. (Root-cause de l'accent, pas un garde-fou de surface.)
    ctx = _context(overlay="selarl_medecin")
    ctx.associes[0].situation_maritale = "pacse"  # BRUT
    ctx.associes[0].regime_matrimonial = ""
    text = _docx_text(StatutsSelarlMedecinGenerator().generate(ctx, tmp_path))
    assert "pacsé avec Madame Alice Martin" in text
    assert "pacse avec" not in text  # jamais la forme non accentuee
    _assert_clean(text)


def test_statuts_sel_exercice_married_unchanged(tmp_path: Path) -> None:
    # Non-regression : un MARIE conserve « marié sous le régime de … avec … » (byte-fidele).
    ctx = _context(overlay="selarl_medecin")  # marie + Alice Martin par defaut
    text = _docx_text(StatutsSelarlMedecinGenerator().generate(ctx, tmp_path))
    assert "sous le régime de" in text
    assert "avec Madame Alice Martin" in text
    _assert_clean(text)


def test_statuts_selarl_medecin_article_8_agrees_female_unique(
    tmp_path: Path,
) -> None:
    ctx = _context(overlay="selarl_medecin", gender=Gender.FEMININ)

    output_path = StatutsSelarlMedecinGenerator().generate(ctx, tmp_path)

    text = _docx_text(output_path)

    assert "Docteur Camille Martin, associée unique." in text
    _assert_clean(text)


def test_statuts_selarl_dentiste_deposit_agrees_female_unique(
    tmp_path: Path,
) -> None:
    ctx = _context(overlay="selarl_dentiste", gender=Gender.FEMININ)

    output_path = StatutsSelarlDentisteGenerator().generate(ctx, tmp_path)

    text = _docx_text(output_path)

    assert "déposée par l’associée unique conformément à la loi" in text
    assert "déposée par l’associé unique conformément à la loi" not in text
    _assert_clean(text)


def test_statuts_selarl_medecin_matches_source_docx_line_by_line(
    tmp_path: Path,
) -> None:
    ctx = _context(overlay="selarl_medecin")
    output_path = StatutsSelarlMedecinGenerator().generate(ctx, tmp_path)
    source_path = next(Path("project/source_documents/lot_04").glob("*SELARL*decins.docx"))

    source_article = _article_paragraphs(
        _render_source_medecin_paragraph(paragraph, ctx)
        for paragraph in _docx_paragraphs(source_path)
        if "[civilite_personne_2]" not in paragraph
    )
    generated_article = _article_paragraphs(_docx_paragraphs(output_path))

    assert generated_article == source_article


def test_statuts_selarl_medecin_pluralizes_euros_for_value_two_or_more(tmp_path: Path) -> None:
    # Bug Rafael 2026-06-08 : « 10 euro » sans s. La valeur nominale des parts >= 2
    # doit donner « euros ». La SELARL de reference (valeur 1) reste « 1 euro »
    # (cf. test ligne-par-ligne ci-dessus : sortie inchangee, prod-safe).
    ctx = _context(overlay="selarl_medecin")
    ctx.capital.valeur_nominale_titre = "10"
    text = _docx_text(StatutsSelarlMedecinGenerator().generate(ctx, tmp_path))
    assert "parts de 10 euros chacune" in text
    assert "10 euro chacune" not in text


def test_statuts_selarl_medecin_single_lieu_keeps_unique_wording(tmp_path: Path) -> None:
    # Ticket 2.2 ADDITIF : sans 2e lieu (cas actuel = 100% des dossiers), l'article 5
    # SELARL medecin garde son wording d'origine « ...lieu d'exercice unique... »
    # et n'expose aucun token de 2e lieu (sortie byte-identique a l'existant).
    output_path = StatutsSelarlMedecinGenerator().generate(
        _context(overlay="selarl_medecin"),
        tmp_path,
    )
    text = _docx_text(output_path)
    assert "Il constitue le lieu d’exercice unique de la société" in text
    assert "nom_lieu_exercice_2" not in text
    _assert_clean(text)


def test_statuts_selarl_dentiste_single_lieu_keeps_unique_wording(tmp_path: Path) -> None:
    # Ticket 2.2 ADDITIF : meme garantie cote dentiste sans 2e lieu saisi.
    ctx = _context(overlay="selarl_dentiste")
    ctx.associes[0].profession = "chirurgien-dentiste"
    ctx.associes[0].profession_reglementee = "chirurgien-dentiste"
    ctx.associes[0].profession_reglementee_pluriel = "chirurgiens-dentistes"
    ctx.associes[0].ordre.professionnel = "Ordre des chirurgiens-dentistes"

    output_path = StatutsSelarlDentisteGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)
    assert "Il constitue le lieu d’exercice unique de la société" in text
    assert "nom_lieu_exercice_2" not in text
    _assert_clean(text)


def test_statuts_selarl_medecin_renders_complete_second_lieu(tmp_path: Path) -> None:
    # Ticket 2.2 ADDITIF : un 2e lieu reel saisi -> les DEUX lieux apparaissent a
    # l'article 5 (siege en lieu #1 + 2e lieu nomme), et le mot « unique » disparait.
    ctx = _context(overlay="selarl_medecin")
    ctx.exercice_social.lieux.append(
        ExerciceLieu(
            nom="Cabinet secondaire",
            adresse_affichee="20 rue Bleue, 75009 Paris",
        )
    )

    output_path = StatutsSelarlMedecinGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)

    # Lieu #1 = lieux[0] (adresse du lieu d'exercice principal de la fixture).
    assert "12 avenue de la Republique, 75011 Paris" in text
    # Lieu #2 = nom + adresse saisis.
    assert "Cabinet secondaire, 20 rue Bleue, 75009 Paris" in text
    # Le wording « unique » est retire en presence d'un 2e lieu.
    assert "lieu d’exercice unique" not in text
    _assert_clean(text)


def test_statuts_selarl_dentiste_renders_complete_second_lieu(tmp_path: Path) -> None:
    # Ticket 2.2 ADDITIF : meme garantie cote dentiste avec un 2e lieu reel.
    ctx = _context(overlay="selarl_dentiste")
    ctx.associes[0].profession = "chirurgien-dentiste"
    ctx.associes[0].profession_reglementee = "chirurgien-dentiste"
    ctx.associes[0].profession_reglementee_pluriel = "chirurgiens-dentistes"
    ctx.associes[0].ordre.professionnel = "Ordre des chirurgiens-dentistes"
    # lieux[0] = siege (12 avenue de la Republique dans la fixture), + 2e lieu.
    ctx.exercice_social.lieux.append(
        ExerciceLieu(
            nom="Cabinet secondaire",
            adresse_affichee="20 rue Bleue, 75009 Paris",
        )
    )

    output_path = StatutsSelarlDentisteGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)

    assert "12 avenue de la Republique, 75011 Paris" in text
    assert "Cabinet secondaire, 20 rue Bleue, 75009 Paris" in text
    assert "lieu d’exercice unique" not in text
    _assert_clean(text)


def test_statuts_selarl_blocks_partial_second_lieu(tmp_path: Path) -> None:
    # Ticket 2.2 : nom OU adresse seul -> ValueError (contrat aligne sur la SELAS).
    ctx = _context(overlay="selarl_medecin")
    ctx.exercice_social.lieux.append(ExerciceLieu(nom="Cabinet secondaire"))

    with pytest.raises(ValueError, match="doivent etre fournis ensemble"):
        StatutsSelarlMedecinGenerator().generate(ctx, tmp_path)


def test_statuts_selas_medecin_generates_without_second_lieu_by_default(
    tmp_path: Path,
) -> None:
    output_path = StatutsSelasMedecinGenerator().generate(
        _context(overlay="selas_medecin"),
        tmp_path,
    )

    text = _docx_text(output_path)

    assert output_path.name == "statuts_selas_medecin.docx"
    assert "Societe d'exercice liberal par actions simplifiee" in text
    assert "President" in text
    assert "nom_lieu_exercice_2" not in text
    # Ligne d'identite nominative : la clause matrimoniale passe par le token
    # composite [situation_matrimoniale_statuts] (pas de double article "de la la")
    # et l'inscription a l'Ordre est elidee ("de l'Ordre", pas "du Ordre").
    assert "de la la" not in text
    assert "du Ordre" not in text
    assert (
        "marié sous le régime de la communauté avec Madame Alice Martin, "
        "inscrit au Tableau de l’Ordre des medecins sous le numéro RPPS 10000000001."
    ) in text
    _assert_clean(text)


def test_statuts_selas_medecin_article_8_elision_valeur_nominale(tmp_path: Path) -> None:
    # Akainu B1 (regle 68) : l'article 8 colle « d’[valeur…] ». Valeur a initiale CONSONNE
    # (« cent ») -> « actions de cent euros » (pas « d’cent »). Valeur a initiale VOYELLE
    # (« un ») -> « d’un euro ». Apostrophe COURBE (U+2019) comme le rendu reel.
    # Akainu M-1/n-1 (2026-07-03) : lettres RÉALISTES (« cent »/« un », le front n'incruste pas
    # « euro »), figure COHÉRENTE (euro_word accorde sur la figure), + garde anti DOUBLE-euro.
    ctx = _context(overlay="selas_medecin")
    ctx.capital.valeur_nominale_titre = "100"
    ctx.capital.valeur_nominale_titre_lettres = "cent"
    text = _docx_text(StatutsSelasMedecinGenerator().generate(ctx, tmp_path))
    assert "actions de cent euros" in text  # consonne : pas d'elision + accord pluriel
    assert "d’cent" not in text
    assert "d'cent" not in text
    assert "euros euro" not in text and "euro euro" not in text  # jamais de double « euro »
    # Cas voyelle : « un » -> « d’un euro » (elision + singulier).
    ctx_v = _context(overlay="selas_medecin")  # valeur nominale 1 / « un » (defaut fixture)
    text_v = _docx_text(StatutsSelasMedecinGenerator().generate(ctx_v, tmp_path))
    assert "actions d’un euro" in text_v
    assert "euro euro" not in text_v  # pas de double « euro »


def test_statuts_selas_interligne_simple(tmp_path: Path) -> None:
    # Retour Albane « mise en forme » 1.1 : « interligne 0,5 ou 1 ». Les generateurs from-scratch
    # partaient a 1,15 (defaut python-docx). On impose l'interligne SIMPLE (1,0) sur « Normal ».
    from docx import Document

    out = StatutsSelasMedecinGenerator().generate(_context(overlay="selas_medecin"), tmp_path)
    assert Document(out).styles["Normal"].paragraph_format.line_spacing == 1.0


def test_statuts_selas_medecin_renders_complete_second_lieu(tmp_path: Path) -> None:
    ctx = _context(overlay="selas_medecin")
    ctx.exercice_social.lieux.append(
        ExerciceLieu(
            nom="Cabinet secondaire",
            adresse_affichee="20 rue Bleue, 75009 Paris",
        )
    )

    output_path = StatutsSelasMedecinGenerator().generate(ctx, tmp_path)

    text = _docx_text(output_path)

    assert "Cabinet secondaire, 20 rue Bleue, 75009 Paris" in text
    _assert_clean(text)


def test_statuts_sel_blocks_multi_associes(tmp_path: Path) -> None:
    ctx = _context(overlay="selarl_medecin")
    ctx.associes.append(_associate())

    with pytest.raises(ValueError, match="multi-associes"):
        StatutsSelarlMedecinGenerator().generate(ctx, tmp_path)


def test_statuts_selarl_dentiste_blocks_multi_associes(tmp_path: Path) -> None:
    # SELARL = unipersonnelle (decision Gad 2026-06-04) : deux associes -> ValueError,
    # meme si l'ancien flag PARTIAL est present dans metadata (sous-cas abandonne).
    ctx = _context(overlay="selarl_dentiste")
    ctx.metadata["selarl_dentiste_multi_associes_statuts_partial"] = "true"
    ctx.associes.append(_associate())

    with pytest.raises(ValueError, match="multi-associes"):
        StatutsSelarlDentisteGenerator().generate(ctx, tmp_path)


def test_statuts_selas_blocks_partial_second_lieu(tmp_path: Path) -> None:
    ctx = _context(overlay="selas_medecin")
    ctx.exercice_social.lieux.append(ExerciceLieu(nom="Cabinet secondaire"))

    with pytest.raises(ValueError, match="doivent etre fournis ensemble"):
        StatutsSelasMedecinGenerator().generate(ctx, tmp_path)


def test_statuts_selas_blocks_dirigeant_non_associe_signature(tmp_path: Path) -> None:
    ctx = _context(overlay="selas_medecin")
    ctx.dirigeant_nomine.nom = "Bernard"
    ctx.dirigeant_nomine.ref_associe_index = None

    with pytest.raises(ValueError, match="dirigeant non associe"):
        StatutsSelasMedecinGenerator().generate(ctx, tmp_path)


def test_statuts_sel_applies_female_birth_agreement(tmp_path: Path) -> None:
    ctx = _context(overlay="selas_medecin", gender=Gender.FEMININ)

    output_path = StatutsSelasMedecinGenerator().generate(ctx, tmp_path)

    text = _docx_text(output_path)

    assert "nÃ©e le" in text or "née le" in text
    _assert_clean(text)


def test_statuts_selas_header_agrees_masculine(tmp_path: Path) -> None:
    # Entete figee au masculin dans les blocs : conservee telle quelle pour un homme.
    output_path = StatutsSelasMedecinGenerator().generate(
        _context(overlay="selas_medecin", gender=Gender.MASCULIN),
        tmp_path,
    )

    text = _docx_text(output_path)

    assert "LE SOUSSIGNE" in text
    assert "LA SOUSSIGNÉE" not in text
    # Ligne d'identification masculine.
    assert "né le 02/01/1980" in text
    assert "née le 02/01/1980" not in text
    _assert_clean(text)


def test_statuts_selas_header_agrees_feminine(tmp_path: Path) -> None:
    # Entete figee au masculin -> accordee au feminin pour une associee.
    output_path = StatutsSelasMedecinGenerator().generate(
        _context(overlay="selas_medecin", gender=Gender.FEMININ),
        tmp_path,
    )

    text = _docx_text(output_path)

    assert "LA SOUSSIGNÉE" in text
    assert "LE SOUSSIGNE\xa0:" not in text
    assert "née le 02/01/1980" in text
    _assert_clean(text)


def test_statuts_selas_article_8_uses_dynamic_associate_label(tmp_path: Path) -> None:
    # Le bloc fige « à l'associé unique » est remplace par le token dynamique :
    # masculin -> « associé unique », feminin -> « associée unique ».
    masc = _docx_text(
        StatutsSelasMedecinGenerator().generate(
            _context(overlay="selas_medecin", gender=Gender.MASCULIN),
            tmp_path / "masc",
        )
    )
    fem = _docx_text(
        StatutsSelasMedecinGenerator().generate(
            _context(overlay="selas_medecin", gender=Gender.FEMININ),
            tmp_path / "fem",
        )
    )

    assert "attribuées en totalité à l’associé unique, Docteur Camille Martin." in masc
    assert "attribuées en totalité à l’associée unique, Docteur Camille Martin." in fem
    _assert_clean(masc)
    _assert_clean(fem)


def test_statuts_sel_orchestrator_selects_only_requested_overlay() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents_for_context(_context(overlay="selarl_medecin"))

    selected_ids = {document.doc_id for document in selected}
    assert "DOC-017" in selected_ids
    assert "DOC-016" not in selected_ids
    assert "DOC-018" not in selected_ids


def test_statuts_sel_orchestrator_ignores_sel_statuts_without_overlay() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())
    ctx = _context(overlay="selarl_medecin")
    ctx.statuts_sel = None

    selected = orchestrator.select_documents_for_context(ctx)

    assert {"DOC-016", "DOC-017", "DOC-018"}.isdisjoint(
        {document.doc_id for document in selected}
    )


# --- Multi-associes SELARL (retours V3 2026-06-17) — strictement additif --------------


def _membre_pp(
    *,
    prenom: str,
    nom: str,
    civilite: str = "Monsieur",
    genre: Gender = Gender.MASCULIN,
    nb_parts: int,
    nb_parts_lettres: str,
    apport: str,
    apport_lettres: str,
    profession: str = "medecin",
    est_signataire: bool = True,
) -> StatutsCivilsAssocie:
    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=genre,
        civilite_affichage=civilite,
        prenom=prenom,
        nom=nom,
        date_naissance=date(1980, 1, 2),
        ville_naissance="Paris",
        departement_naissance="75",
        nationalite="francaise",
        profession=profession,
        situation_maritale="celibataire",
        adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
        ordre_departemental="Paris",
        numero_ordre="12345",
        numero_rpps="10000000001",
        apport=StatutsCivilsApport(montant=apport, montant_lettres=apport_lettres),
        parts=StatutsCivilsParts(nb=nb_parts, nb_lettres=nb_parts_lettres),
        est_signataire=est_signataire,
    )


def _membre_pm(
    *,
    denomination: str,
    nb_parts: int,
    nb_parts_lettres: str,
    apport: str,
    apport_lettres: str,
) -> StatutsCivilsAssocie:
    return StatutsCivilsAssocie(
        type_personne="personne_morale",
        denomination=denomination,
        forme_juridique="SPFPL",
        capital_social="10 000",
        siege=Address(adresse_affichee="2 rue des Lilas, 75009 Paris"),
        numero_rcs="123 456 789",
        ville_rcs="Paris",
        representant=StatutsCivilsRepresentant(
            civilite_affichage="Monsieur",
            prenom="Paul",
            nom="Holding",
        ),
        apport=StatutsCivilsApport(montant=apport, montant_lettres=apport_lettres),
        parts=StatutsCivilsParts(nb=nb_parts, nb_lettres=nb_parts_lettres),
    )


def _multi_context(
    *,
    overlay: str,
    membres: list[StatutsCivilsAssocie],
) -> DocumentGenerationContext:
    ctx = _context(overlay=overlay)
    if overlay == "selarl_dentiste":
        ctx.associes[0].profession = "chirurgien-dentiste"
        ctx.associes[0].profession_reglementee = "chirurgien-dentiste"
        ctx.associes[0].profession_reglementee_pluriel = "chirurgiens-dentistes"
        ctx.associes[0].ordre.professionnel = "Ordre des chirurgiens-dentistes"
    ctx.statuts_sel.membres = membres
    return ctx


def test_statuts_selarl_medecin_multi_two_physical_associates(tmp_path: Path) -> None:
    membres = [
        _membre_pp(
            prenom="Camille",
            nom="Martin",
            nb_parts=600,
            nb_parts_lettres="six cents",
            apport="600",
            apport_lettres="six cents",
        ),
        _membre_pp(
            prenom="Lea",
            nom="Bernard",
            civilite="Madame",
            genre=Gender.FEMININ,
            nb_parts=400,
            nb_parts_lettres="quatre cents",
            apport="400",
            apport_lettres="quatre cents",
        ),
    ]
    ctx = _multi_context(overlay="selarl_medecin", membres=membres)

    output_path = StatutsSelarlMedecinGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)

    # Comparution pluriel + une ligne d'identite par membre.
    assert "LES SOUSSIGNÉS" in text
    assert "Monsieur Camille Martin, medecin," in text
    assert "Madame Lea Bernard, medecin," in text
    # Article 7 : un apport par membre + total.
    assert "Monsieur Camille Martin apporte à la Société la somme de 600 euros." in text
    assert "Madame Lea Bernard apporte à la Société la somme de 400 euros." in text
    # Article 8 : repartition numerotee « 1° ... ; / 2° ... . » (wording ticket V3).
    assert "1° Camille Martin, détenant 600 parts ;" in text
    assert "2° Lea Bernard, détenant 400 parts." in text
    # Signature : un libelle par signataire.
    assert "Camille Martin" in text
    assert "Lea Bernard" in text
    _assert_clean(text)


def test_statuts_selarl_dentiste_multi_physical_plus_morale(tmp_path: Path) -> None:
    membres = [
        _membre_pp(
            prenom="Camille",
            nom="Martin",
            profession="chirurgien-dentiste",
            nb_parts=700,
            nb_parts_lettres="sept cents",
            apport="700",
            apport_lettres="sept cents",
        ),
        _membre_pm(
            denomination="HOLDING MEDICA",
            nb_parts=300,
            nb_parts_lettres="trois cents",
            apport="300",
            apport_lettres="trois cents",
        ),
    ]
    ctx = _multi_context(overlay="selarl_dentiste", membres=membres)

    output_path = StatutsSelarlDentisteGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)

    assert "LES SOUSSIGNÉS" in text
    # Personne physique : ligne d'identite ; personne morale : ligne d'identification societe.
    assert "Monsieur Camille Martin, chirurgien-dentiste," in text
    assert "La HOLDING MEDICA, SPFPL, au capital de 10 000 euros" in text
    assert "représentée par son représentant légal, Monsieur Paul Holding." in text
    # Article 7 : apport personne physique + personne morale.
    assert "Monsieur Camille Martin apporte à la Société la somme de 700 euros." in text
    assert "La HOLDING MEDICA apporte à la Société la somme de 300 euros." in text
    # Article 8 : repartition — PM par denomination, PP par prenom/nom (wording V3).
    assert "1° Camille Martin, détenant 700 parts ;" in text
    assert "2° HOLDING MEDICA, détenant 300 parts." in text
    _assert_clean(text)


def test_statuts_selarl_multi_requires_total_parts_consistency(tmp_path: Path) -> None:
    # Calcul auto du nombre d'associes / coherence capital : la somme des parts des
    # membres doit egaler le capital (1000). Ici 600 + 300 = 900 -> ValueError.
    membres = [
        _membre_pp(
            prenom="Camille",
            nom="Martin",
            nb_parts=600,
            nb_parts_lettres="six cents",
            apport="600",
            apport_lettres="six cents",
        ),
        _membre_pp(
            prenom="Lea",
            nom="Bernard",
            nb_parts=300,
            nb_parts_lettres="trois cents",
            apport="300",
            apport_lettres="trois cents",
        ),
    ]
    ctx = _multi_context(overlay="selarl_medecin", membres=membres)

    with pytest.raises(ValueError, match="somme des parts"):
        StatutsSelarlMedecinGenerator().generate(ctx, tmp_path)


def test_statuts_selarl_single_member_list_stays_mono(tmp_path: Path) -> None:
    # Garde-fou retro-compat : une liste membres a 1 element NE declenche PAS le multi
    # -> sortie mono historique (entete singulier « LE SOUSSIGNE »).
    ctx = _context(overlay="selarl_medecin")
    ctx.statuts_sel.membres = [
        _membre_pp(
            prenom="Camille",
            nom="Martin",
            nb_parts=1000,
            nb_parts_lettres="mille",
            apport="1 000",
            apport_lettres="mille",
        )
    ]
    output_path = StatutsSelarlMedecinGenerator().generate(ctx, tmp_path)
    text = _docx_text(output_path)
    assert "LE SOUSSIGNE" in text
    assert "LES SOUSSIGNÉS" not in text
    assert "Docteur Camille Martin, associé unique." in text
    _assert_clean(text)


def _article_paragraphs(paragraphs) -> list[str]:
    normalized = [_normalize_source_line(paragraph) for paragraph in paragraphs]
    for index, paragraph in enumerate(normalized):
        if paragraph.startswith("ARTICLE 1"):
            return normalized[index:]
    raise AssertionError("ARTICLE 1 introuvable dans les statuts SEL.")


def _normalize_source_line(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u00a0", " ").strip())


def _render_source_medecin_paragraph(
    paragraph: str,
    ctx: DocumentGenerationContext,
) -> str:
    associate = ctx.associes[0]
    replacements = {
        "[denomination_societe]": ctx.societe.denomination,
        "[capital_social]": ctx.capital.montant,
        "[adresse_siege]": ctx.societe.siege.adresse_affichee,
        "[civilite]": associate.civilite_affichage,
        "[prenom]": associate.prenom,
        "[nom]": associate.nom,
        "[profession]": associate.profession,
        "[date_naissance]": associate.date_naissance.strftime("%d/%m/%Y"),
        "[ville_naissance]": associate.ville_naissance,
        "[departement_naissance]": associate.departement_naissance,
        "[nationalite]": associate.nationalite,
        "[adresse_personnelle]": associate.adresse_personnelle_affichee,
        "[ville_ordre]": associate.ordre.ville,
        "[numero_ordre]": associate.ordre.numero,
        "[numero_rpps]": associate.ordre.numero_rpps,
        "[situation_maritale]": (
            "marié sous le régime de la communauté avec Madame Alice Martin"
        ),
        "[forme_sociale_complete]": ctx.societe.forme_sociale_complete,
        "[capital_lettres]": ctx.capital.montant_lettres,
        "[nom_banque]": ctx.depot_fonds.banque.nom,
        "[adresse_banque]": ctx.depot_fonds.banque.adresse_affichee,
        "[nb_parts_total]": str(ctx.capital.nombre_titres_total),
        "[valeur_nominale_part]": ctx.capital.valeur_nominale_titre,
        "[seuil_achat_materiel]": ctx.gerance.seuil_achat_materiel,
        "[seuil_emprunt_gerance]": ctx.gerance.seuil_emprunt,
        "[date_cloture_exercice_1]": ctx.exercice_social.date_cloture_premier_exercice,
        "[lieu_signature]": ctx.signature.lieu,
        "[date_signature]": ctx.signature.date.strftime("%d/%m/%Y"),
        "[nombre_exemplaires_lettres]": ctx.document.nombre_exemplaires_lettres,
        "[prenom_signataire]": ctx.document.signataire.prenom,
        "[nom_signataire]": ctx.document.signataire.nom,
    }
    rendered = paragraph
    # Correction Albane 2026-06-10 (« "fixé à la somme de mille" il faudrait ajouter "euros" »
    # / forme cible « de [capital_lettres] euros ») propagee au template medecin (Art. 8) ;
    # le DOCX source porte encore la coquille « somme [capital_social] euros » -> on aligne
    # le rendu source sur la correction pour la comparaison ligne-a-ligne.
    rendered = rendered.replace(
        "fixé à la somme [capital_social] euros",
        "fixé à la somme de [capital_lettres] euros",
    )
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    rendered = rendered.replace("associée unique", "associé unique")
    if rendered == "Ouverture d’un compte bancaire":
        return "- Ouverture d’un compte bancaire"
    return rendered


def _art8_line(text: str) -> str:
    for line in text.split("\n"):
        if "Il est divisé en" in line and "actions" in line and "chacune" in line:
            return line
    raise AssertionError("ligne article 8 introuvable dans le rendu SELAS")


def _paragraphs_with_runs(path: Path):
    return list(Document(path).paragraphs)


def _all_runs_bold(paragraph) -> bool:
    runs = [run for run in paragraph.runs if run.text.strip()]
    return bool(runs) and all(run.bold for run in runs)


# --- 2.3 euro (uni medecin, valeur nominale reelle number_words) ---------------------------


def test_statuts_selas_medecin_article_8_euro_singulier_valeur_reelle(tmp_path: Path) -> None:
    # Retour Albane 2.3 : art.8 rend « d'un euro (1 €) » quand la valeur nominale en lettres
    # est la valeur REELLE (front-app : number_words_from_value('1') = « un », SANS euro). Le
    # token « [euro_nominal_word] » du modele medecin ajoute « euro » accorde (VN=1 -> singulier).
    from sydel_doc_engine.front_app.field_derivations import number_words_from_value

    ctx = _context(overlay="selas_medecin")
    ctx.capital.valeur_nominale_titre = "1"
    ctx.capital.valeur_nominale_titre_lettres = number_words_from_value("1")  # « un »
    line = _art8_line(_docx_text(StatutsSelasMedecinGenerator().generate(ctx, tmp_path)))
    assert "actions d’un euro (1 €) chacune" in line
    assert "euro euro" not in line and "euros euro" not in line  # pas de double euro
    assert "d’un (1 €)" not in line  # euro ne doit pas manquer


def test_statuts_selas_medecin_article_8_euros_pluriel_valeur_reelle(tmp_path: Path) -> None:
    # Retour Albane 2.3 : VN>=2 -> « euros » pluriel + connecteur « de » (consonne).
    from sydel_doc_engine.front_app.field_derivations import number_words_from_value

    ctx = _context(overlay="selas_medecin")
    ctx.capital.valeur_nominale_titre = "10"
    ctx.capital.valeur_nominale_titre_lettres = number_words_from_value("10")  # « dix »
    line = _art8_line(_docx_text(StatutsSelasMedecinGenerator().generate(ctx, tmp_path)))
    assert "actions de dix euros (10 €) chacune" in line
    assert "de dix (10 €)" not in line  # euro ne doit pas manquer


# --- 2.1 dedoublonnage profession / qualification (comparution) ----------------------------


def test_statuts_selas_medecin_comparution_dedoublonne_profession_qualification(
    tmp_path: Path,
) -> None:
    # Retour Albane 2.1 : quand la qualification saisie == profession reglementee, la
    # comparution ne doit emettre le mot QU'UNE fois (« medecin », pas « medecin medecin »).
    ctx = _context(overlay="selas_medecin")
    ctx.associes[0].profession_reglementee = "medecin"
    ctx.associes[0].qualification_principale = "medecin"
    text = _docx_text(StatutsSelasMedecinGenerator().generate(ctx, tmp_path))
    assert "medecin medecin" not in text
    assert "Docteur Camille Martin, medecin, né le" in text


def test_statuts_selas_medecin_comparution_preserve_qualification_distincte(
    tmp_path: Path,
) -> None:
    # Retour Albane 2.1 : une qualification DISTINCTE de la profession est preservee
    # (« medecin cardiologue » = juxtaposition volontaire, non dedoublonnee).
    ctx = _context(overlay="selas_medecin")
    ctx.associes[0].profession_reglementee = "medecin"
    ctx.associes[0].qualification_principale = "cardiologue"
    text = _docx_text(StatutsSelasMedecinGenerator().generate(ctx, tmp_path))
    assert "medecin cardiologue" in text


# --- 2.6 / 2.7 / 2.8 mise en forme SELAS (gras siege / gras president / sous-articles) -----


def test_statuts_selas_medecin_siege_art4_en_gras(tmp_path: Path) -> None:
    # Retour Albane 2.6 : l'ADRESSE du siege (art.4) rendue en gras (le libelle reste normal).
    paragraphs = _paragraphs_with_runs(
        StatutsSelasMedecinGenerator().generate(_context(overlay="selas_medecin"), tmp_path)
    )
    siege = next(
        p for p in paragraphs if "siège" in p.text.lower() and "fixé au" in p.text
    )
    # Le libelle (« Le siège social est fixé au ») N'est PAS gras ; l'adresse l'est.
    label_run = siege.runs[0]
    adresse_run = siege.runs[-1]
    assert label_run.bold is not True
    assert adresse_run.bold is True
    assert "10 rue de la Paix" in adresse_run.text


def test_statuts_selas_medecin_president_designation_art15_en_gras(tmp_path: Path) -> None:
    # Retour Albane 2.7 : la designation nominative du President (art.15 medecin) en gras.
    paragraphs = _paragraphs_with_runs(
        StatutsSelasMedecinGenerator().generate(_context(overlay="selas_medecin"), tmp_path)
    )
    nomme = next(
        p for p in paragraphs if "est nommé" in p.text and "Société et ce pour" in p.text
    )
    assert _all_runs_bold(nomme)


def test_statuts_selas_medecin_sous_articles_soulignes(tmp_path: Path) -> None:
    # Retour Albane 2.8 : les en-tetes de sous-articles (« 15.1- », « 16-1 - »...) soulignes.
    paragraphs = _paragraphs_with_runs(
        StatutsSelasMedecinGenerator().generate(_context(overlay="selas_medecin"), tmp_path)
    )
    subarticles = [
        p for p in paragraphs if re.match(r"^\s*\d{1,2}\s*[.\-]\s*\d{1,2}\b", p.text)
    ]
    assert subarticles, "aucun en-tete de sous-article trouve"
    for paragraph in subarticles:
        assert all(run.underline for run in paragraph.runs if run.text.strip())


def test_statuts_selas_medecin_corps_sans_faux_positif_gras_souligne(tmp_path: Path) -> None:
    # Garde-fou anti faux-positif : une ligne de CORPS quelconque (art.8) n'est ni gras
    # ni soulignee — la mise en forme SELAS ne deborde pas sur le corps.
    paragraphs = _paragraphs_with_runs(
        StatutsSelasMedecinGenerator().generate(_context(overlay="selas_medecin"), tmp_path)
    )
    art8 = next(p for p in paragraphs if "entièrement libérées" in p.text)
    assert all(run.bold is not True for run in art8.runs)
    assert all(run.underline is not True for run in art8.runs)


# --- byte-neutralite SELARL : selas_formatting OFF -> aucun gras/souligne parasite ---------


def test_statuts_selarl_medecin_sans_mise_en_forme_selas_parasite(tmp_path: Path) -> None:
    # Le flag selas_formatting est OFF pour SELARL : aucune adresse de siege en gras et
    # aucun sous-article souligne parasite (la mise en forme SELAS ne fuit pas vers SELARL).
    paragraphs = _paragraphs_with_runs(
        StatutsSelarlMedecinGenerator().generate(_context(overlay="selarl_medecin"), tmp_path)
    )
    # Sous-articles (« 20.1 – », « 23.1 - »...) : AUCUN souligne (contrairement au SELAS).
    subarticles = [
        p for p in paragraphs if re.match(r"^\s*\d{1,2}\s*[.\-]\s*\d{1,2}\b", p.text)
    ]
    assert subarticles, "aucun sous-article SELARL trouve (fixture inattendue)"
    for paragraph in subarticles:
        assert all(run.underline is not True for run in paragraph.runs)
    # Ligne du siege SELARL : aucun run en gras parasite.
    siege = [p for p in paragraphs if "siège" in p.text.lower() and "fixé" in p.text]
    for paragraph in siege:
        assert all(run.bold is not True for run in paragraph.runs)


# ---------------------------------------------------------------------------
# Containment monetaire 2026-07-06 (re-architecture) — apport/capital SEL DECIMAL.
# Bug B1/B2 : `number_words_from_value` etait decimal-aware globalement et injectait
# « un centime d'euro » LA OU le template accolait deja « euros » -> « un centime
# d'euro euros ». Depuis le revert, `number_words_from_value(decimal)` = FIGURE, donc
# apport/capital rendent « 0,01 euros » (figure + unite), sans double ; la phrase
# monetaire 7.5 n'apparait QUE sur la valeur nominale via `montant_lettres_avec_unite`.
# ---------------------------------------------------------------------------


def _apply_capital_from_front(ctx, *, capital: str, vn: str, apport: str) -> None:
    """Simule ce que POSE le front : les slots `_lettres` derives via number_words_from_value.

    Sur un decimal (containment), number_words_from_value rend la FIGURE ; sur un entier,
    des mots nus. C'est exactement l'entree que recoivent les generateurs SEL exercice."""
    from sydel_doc_engine.front_app.field_derivations import number_words_from_value

    ctx.societe.capital_social = capital
    ctx.societe.capital_social_lettres = number_words_from_value(capital)
    ctx.capital.montant = capital
    ctx.capital.montant_lettres = number_words_from_value(capital)
    ctx.capital.valeur_nominale_titre = vn
    ctx.capital.valeur_nominale_titre_lettres = number_words_from_value(vn)
    if ctx.apport is not None:
        ctx.apport.montant = apport
        ctx.apport.montant_lettres = number_words_from_value(apport)
    ctx.associes[0].apport_numeraire = apport
    ctx.associes[0].apport_numeraire_lettres = number_words_from_value(apport)


def _set_dentiste_professions(ctx) -> None:
    ctx.associes[0].profession = "chirurgien-dentiste"
    ctx.associes[0].profession_reglementee = "chirurgien-dentiste"
    ctx.associes[0].profession_reglementee_pluriel = "chirurgiens-dentistes"
    ctx.associes[0].ordre.professionnel = "Ordre des chirurgiens-dentistes"


_SEL_DECIMAL_GENERATORS = [
    ("selarl_dentiste", StatutsSelarlDentisteGenerator, True),
    ("selarl_medecin", StatutsSelarlMedecinGenerator, False),
    ("selas_medecin", StatutsSelasMedecinGenerator, False),
]


@pytest.mark.parametrize("overlay,gen_cls,dentiste", _SEL_DECIMAL_GENERATORS)
@pytest.mark.parametrize("montant", ["0,01", "1500,50"])
def test_sel_exercice_apport_capital_decimal_sans_double_euro(
    tmp_path: Path, overlay: str, gen_cls, dentiste: bool, montant: str
) -> None:
    # M1 (Akainu) : apport ET capital decimaux (0,01 / 1500,50) ne doivent JAMAIS produire de
    # double « euro » (« un centime d'euro euros », « ... euros euros ») ; ils rendent la FIGURE
    # + « euros » via le template. Aucun token residuel, apostrophe courbe.
    ctx = _context(overlay=overlay)
    if dentiste:
        _set_dentiste_professions(ctx)
    _apply_capital_from_front(ctx, capital=montant, vn=montant, apport=montant)
    text = _docx_text(gen_cls().generate(ctx, tmp_path))
    _assert_clean(text)  # 0 token residuel
    low = text.lower()
    assert "euro euro" not in low, f"{overlay}/{montant}: double euro"
    assert "euros euros" not in low, f"{overlay}/{montant}: double euros"
    assert "d’euro euro" not in text and "d'euro euro" not in text
    assert "un centime d’euro euro" not in text
    # L'apport/capital rendent la FIGURE + unite (jamais la phrase monetaire cote apport).
    figure = montant if montant == "0,01" else "1500,5"  # normalisation format_numeric_value
    assert f"{figure} euros" in text or f"{montant} euros" in text


@pytest.mark.parametrize(
    "montant,phrase",
    [
        ("0,01", "un centime d’euro (0,01 €)"),
        ("1500,50", "mille cinq cents euros et cinquante centimes (1500,50 €)"),
    ],
)
def test_selas_medecin_valeur_nominale_decimale_7_5(
    tmp_path: Path, montant: str, phrase: str
) -> None:
    # 7.5 (Albane 2026-07-06) : la VALEUR NOMINALE decimale d'une SELAS medecin (SEL exercice)
    # rend la phrase monetaire complete « <lettres> (X €) », calculee DEPUIS LA FIGURE par
    # montant_lettres_avec_unite, meme quand le slot lettres ne porte que la figure (containment).
    ctx = _context(overlay="selas_medecin")
    _apply_capital_from_front(ctx, capital="1 000", vn=montant, apport="1 000")
    text = _docx_text(StatutsSelasMedecinGenerator().generate(ctx, tmp_path))
    assert phrase in text
    assert "d’euro euro" not in text
    _assert_clean(text)


def test_sel_exercice_valeur_nominale_entiere_byte_fidele(tmp_path: Path) -> None:
    # Byte-fidelite ENTIER : « un euro » (SELAS art.8), figure « parts de 1 » (SELARL dentiste),
    # « parts de 1 euro » (SELARL medecin) — EXACTEMENT comme avant le containment.
    ctx_selas = _context(overlay="selas_medecin")
    _apply_capital_from_front(ctx_selas, capital="1 000", vn="1", apport="1 000")
    text_selas = _docx_text(StatutsSelasMedecinGenerator().generate(ctx_selas, tmp_path))
    assert "actions d’un euro (1 €) chacune" in text_selas
    assert "somme de mille" in text_selas  # capital entier byte-fidele

    ctx_med = _context(overlay="selarl_medecin")
    _apply_capital_from_front(ctx_med, capital="1 000", vn="1", apport="1 000")
    text_med = _docx_text(StatutsSelarlMedecinGenerator().generate(ctx_med, tmp_path))
    assert "parts de 1 euro chacune" in text_med
    assert "somme de mille euros" in text_med
