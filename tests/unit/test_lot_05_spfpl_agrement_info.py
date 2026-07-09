from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from _accents import assert_no_unaccented_french
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    AssocieCible,
    CessionParts,
    DecisionContext,
    DocumentGenerationContext,
    DossierOptions,
    OperationSpfpl,
    OperationTitres,
    Person,
    ReunionContext,
    ReunionPresident,
    Signature,
    SocieteCible,
    SocieteSpfpl,
    SpfplDirigeant,
    SpfplPerson,
)
from sydel_doc_engine.generators.lot_05.note_information import NoteInformationGenerator
from sydel_doc_engine.generators.lot_05.pv_agrement_cession_spfpl_associe_unique import (
    PvAgrementCessionSpfplAssocieUniqueGenerator,
)
from sydel_doc_engine.generators.lot_05.pv_agrement_cession_spfpl_plusieurs_associes import (
    PvAgrementCessionSpfplPlusieursAssociesGenerator,
)


def _base_context(*, associe_unique: bool = True) -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure="SPFPL cession",
        dossier_options=DossierOptions(cession=True, associe_unique=associe_unique),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Camille",
            nom="Martin",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 14)),
        operation_spfpl=OperationSpfpl(type="cession"),
        societe_spfpl=SocieteSpfpl(
            denomination="SPFPL MARTIN",
            forme_sociale="SPFPL",
            capital_social="1 000",
            siege=Address(adresse_affichee="10 rue de la Paix, 75002 Paris"),
            dirigeant=SpfplDirigeant(fonction="Président"),
        ),
        cedant=SpfplPerson(
            civilite_affichage="Docteur",
            prenom="Camille",
            nom="Martin",
            genre=Gender.MASCULIN,
        ),
        societe_cible=SocieteCible(
            denomination="SELARL CABINET MARTIN",
            forme_sociale="SELARL",
            profession_reglementee="chirurgiens-dentistes",
            capital_social="10 000",
            capital_social_lettres="dix mille euros",
            nb_parts_total=100,
            valeur_nominale_part="100",
            siege=Address(
                num_voie="12",
                voie="avenue des Ternes",
                cp="75017",
                ville="Paris",
                adresse_affichee="12 avenue des Ternes, 75017 Paris",
            ),
            ville_rcs="Paris",
            numero_rcs="900 000 001",
        ),
        cession_parts=CessionParts(
            nb_parts=60,
            nb_parts_lettres="soixante",
            plage_parts="41 a 100",
        ),
        operation_titres=OperationTitres(nb_titres=60),
        reunion=ReunionContext(
            annee_lettres="deux mille vingt-six",
            date_lettres="quatorze mai deux mille vingt-six",
            heure="10 heures",
            president=ReunionPresident(
                civilite_affichage="Docteur",
                prenom="Camille",
                nom="Martin",
                qualite="gérant associé",
            ),
        ),
    )


def _unique_context() -> DocumentGenerationContext:
    ctx = _base_context(associe_unique=True)
    ctx.associes_cible = [
        AssocieCible(
            civilite_affichage="Docteur",
            prenom="Camille",
            nom="Martin",
            nb_parts_avant=100,
            nb_parts_apres=40,
            plage_parts="1 a 40",
        ),
        AssocieCible(
            type="personne_morale",
            denomination="SPFPL MARTIN",
            nb_parts_avant=0,
            nb_parts_apres=60,
            plage_parts="41 a 100",
            est_present_ou_represente=False,
        ),
    ]
    ctx.decision = DecisionContext(date="14/05/2026")
    return ctx


def _plural_context() -> DocumentGenerationContext:
    ctx = _base_context(associe_unique=False)
    ctx.associes_cible = [
        AssocieCible(
            civilite_affichage="Docteur",
            prenom="Camille",
            nom="Martin",
            nb_parts_avant=70,
            nb_parts_apres=10,
            plage_parts="1 a 10",
        ),
        AssocieCible(
            civilite_affichage="Docteur",
            prenom="Louise",
            nom="Bernard",
            nb_parts_avant=30,
            nb_parts_apres=30,
            plage_parts="11 a 40",
        ),
        AssocieCible(
            type="personne_morale",
            denomination="SPFPL MARTIN",
            nb_parts_avant=0,
            nb_parts_apres=60,
            plage_parts="41 a 100",
            est_present_ou_represente=False,
        ),
    ]
    ctx.decision = DecisionContext(date="14/05/2026")
    return ctx


def _apport_note_context() -> DocumentGenerationContext:
    ctx = _unique_context()
    ctx.structure = "SPFPL apport"
    ctx.dossier_options = DossierOptions(apport=True)
    ctx.operation_spfpl = OperationSpfpl(type="apport")
    ctx.apporteur = SpfplPerson(
        civilite_affichage="Docteur",
        prenom="Camille",
        nom="Martin",
        genre=Gender.MASCULIN,
    )
    return ctx


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts = [paragraph.text for paragraph in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(paragraph.text for paragraph in cell.paragraphs)
    return "\n".join(text for text in texts if text)


def _assert_no_placeholders_or_options(text: str) -> None:
    assert "[" not in text
    assert "]" not in text
    assert "\nOU\n" not in text
    assert "d'acquerir/de recevoir" not in text


# SP3 (Albane 2026-06-25) + Akainu M2 : les 2 PV étaient ENTIÈREMENT non accentués. Le garde-fou
# anti-non-accentué est désormais CENTRALISÉ dans ``_accents.assert_no_unaccented_french`` (Akainu
# B1/M1, 2026-06-26) : liste noire unique et exhaustive partagée par tous les générateurs
# from-scratch. « détenant » (presence_lines, fidèle au modèle source) reste hors liste.
# ``_assert_french_accents`` / ``_assert_no_unaccented_french`` conservés comme alias des appels
# existants (PV + note d'information).
_assert_french_accents = assert_no_unaccented_french
_assert_no_unaccented_french = assert_no_unaccented_french


def test_note_information_generates_cession_wording(tmp_path: Path) -> None:
    output_path = NoteInformationGenerator().generate(_unique_context(), tmp_path)

    text = _docx_text(output_path)

    assert output_path.name == "note_information.docx"
    # Apostrophe COURBE U+2019 + insecable (fidelite au modele, Akainu note m2/n2).
    assert "prévoit d’acquérir" in text
    assert "d'acquérir" not in text  # jamais l'apostrophe droite U+0027
    assert "comme suit :" in text  # insecable avant « : » (typographie FR)
    assert "Après ladite cession" in text
    assert "SPFPL MARTIN, titulaire de 60 parts sociales" in text
    _assert_no_placeholders_or_options(text)
    _assert_no_unaccented_french(text)
    # N2 (Rafael 2026-07-09) : le trait de signature est CENTRE (aligne sous/avec le nom du
    # client, egalement centre), plus JUSTIFY (rendu a gauche, desaligne).
    document = Document(output_path)
    trait = next(
        para for para in document.paragraphs if set(para.text.strip()) == {"_"}
    )
    assert trait.alignment == WD_ALIGN_PARAGRAPH.CENTER
    name = next(
        para for para in document.paragraphs if para.text.strip() == "Camille Martin"
    )
    assert name.alignment == WD_ALIGN_PARAGRAPH.CENTER  # trait et nom dans la meme colonne centree


def test_note_information_generates_apport_wording(tmp_path: Path) -> None:
    output_path = NoteInformationGenerator().generate(_apport_note_context(), tmp_path)

    text = _docx_text(output_path)

    assert "prévoit de recevoir en apport en nature" in text
    assert "Après ledit apport" in text
    _assert_no_placeholders_or_options(text)
    _assert_no_unaccented_french(text)


def test_pv_associe_unique_generates_cession_wording(tmp_path: Path) -> None:
    output_path = PvAgrementCessionSpfplAssocieUniqueGenerator().generate(
        _unique_context(),
        tmp_path,
    )

    text = _docx_text(output_path)

    assert output_path.name == "pv_agrement_cession_spfpl_associe_unique.docx"
    assert "L'associé unique autorise la cession" in text
    assert "contrat d'apport" not in text
    assert "autorise l'apport" not in text
    assert "parts apportees" not in text
    # Akainu M1 : la denomination reelle du SPFPL beneficiaire (plus « la SPFPL » hardcode).
    assert "Agrément d'un nouvel associé, la SPFPL MARTIN ;" in text
    assert "la SPFPL ;" not in text
    # Akainu M2 / SP3 : aucun mot francais non accentue.
    _assert_french_accents(text)
    _assert_no_placeholders_or_options(text)


def test_pv_plusieurs_associes_generates_presence_and_signatures(tmp_path: Path) -> None:
    # R3 Rafael 2026-07-07 : Docteur retiré partout (supersede A26-45/49). Civilité
    # PROD-RÉALISTE « Monsieur » sur les slots posés par le slice (cédant, président de
    # séance — le flux réel pose la civilité CIVILE, jamais « Docteur ») ; les associés
    # cible gardent « Docteur » (Camille, option historique -> conversion civile) et
    # « Madame » (Louise, civilité déjà civile -> passe inchangée).
    ctx = _plural_context()
    ctx.cedant.civilite_affichage = "Monsieur"
    ctx.reunion.president.civilite_affichage = "Monsieur"
    ctx.associes_cible[1].civilite_affichage = "Madame"
    output_path = PvAgrementCessionSpfplPlusieursAssociesGenerator().generate(
        ctx,
        tmp_path,
    )

    text = _docx_text(output_path)

    assert output_path.name == "pv_agrement_cession_spfpl_plusieurs_associes.docx"
    # R3 Rafael 2026-07-07 : « Docteur X detenant N parts » -> civilité CIVILE
    # (+ « détenant » accentué, Rafael 2026-07-07).
    assert "Monsieur Camille Martin détenant 70 parts" in text
    assert "Madame Louise Bernard détenant 30 parts" in text
    # R3 Rafael 2026-07-07 : verrou de la convention — plus jamais « Docteur » en sortie.
    assert "Docteur" not in text
    assert "Projet du contrat de cession" in text
    assert "Camille Martin" in text
    assert "Louise Bernard" in text
    # Akainu M1 : la denomination reelle du SPFPL beneficiaire (plus « la SPFPL » hardcode).
    assert "Agrément d'un nouvel associé, la SPFPL MARTIN ;" in text
    assert "la SPFPL ;" not in text
    # Akainu M2 / SP3 : aucun mot francais non accentue.
    _assert_french_accents(text)
    _assert_no_placeholders_or_options(text)


def test_pv_plusieurs_associes_president_qualite_elision(tmp_path: Path) -> None:
    """M1 (Akainu doc-entier 2026-07-09) : « en qualité de <qualite> » ELIDE devant voyelle
    (« d'associé ») — plus de « en qualité de associé ». La qualite EXACTE du president de seance
    pour une cible MULTI reste a confirmer cote metier (defaut generique « associé »)."""
    ctx = _plural_context()
    ctx.reunion.president.civilite_affichage = "Monsieur"
    ctx.reunion.president.qualite = "associé"
    text = _docx_text(
        PvAgrementCessionSpfplPlusieursAssociesGenerator().generate(ctx, tmp_path)
    )
    assert "préside la séance en qualité d’associé." in text
    assert "en qualité de associé" not in text


def test_pv_plusieurs_associes_blocks_missing_total_presence(tmp_path: Path) -> None:
    ctx = _plural_context()
    ctx.associes_cible[1].nb_parts_avant = 20

    with pytest.raises(ValueError, match="totalite des parts"):
        PvAgrementCessionSpfplPlusieursAssociesGenerator().generate(ctx, tmp_path)


# ---------------------------------------------------------------------------
# Verrous de VALEUR / OMISSION (Akainu 2026-07-06).
# ---------------------------------------------------------------------------


def test_note_information_shows_ceded_parts_not_spfpl_actions(tmp_path: Path) -> None:
    """8.2 (Albane 2026-07-06) — VALEUR : en cession, la note affiche le nombre de PARTS
    CÉDÉES a la holding (`cession_parts.nb_parts`), JAMAIS le nombre d'actions de la SPFPL
    (`operation_titres.nb_titres`). On rend les deux DIFFERENTS (60 parts vs 600 actions)
    pour que le test attrape une inversion — une simple presence ne le ferait pas."""
    ctx = _unique_context()
    assert ctx.cession_parts is not None
    ctx.cession_parts.nb_parts = 60  # parts cedees a la holding
    ctx.operation_titres = OperationTitres(nb_titres=600)  # actions SPFPL (leurre)

    text = _docx_text(NoteInformationGenerator().generate(ctx, tmp_path))
    assert "60 parts de la" in text  # parts cedees
    assert "600 parts de la" not in text  # jamais le nb d'actions SPFPL


def _premiere_resolution_line(text: str) -> str:
    """La PREMIÈRE RÉSOLUTION (« … autorise la cession … à compter de ce jour. »), ou
    s'insere (ou non) la mention § 13 « numérotées de <plage> inclus »."""
    for line in text.split("\n"):
        if "autorise la cession" in line:
            return line
    raise AssertionError("PREMIÈRE RÉSOLUTION (« autorise la cession ») absente du PV.")


def test_pv_agrement_plage_mention_present_when_range_set(tmp_path: Path) -> None:
    """13 (Albane 2026-07-06) — la mention « numérotées de <plage> inclus » est PRESENTE
    dans la resolution quand la plage est renseignee (fixture « 41 a 100 »)."""
    ctx = _unique_context()
    assert ctx.cession_parts is not None
    assert ctx.cession_parts.plage_parts  # fixture non vide
    text = _docx_text(
        PvAgrementCessionSpfplAssocieUniqueGenerator().generate(ctx, tmp_path)
    )
    resolution = _premiere_resolution_line(text)
    assert "numérotées de 41 a 100 inclus à compter de ce jour." in resolution


def test_pv_agrement_plage_mention_omitted_when_range_empty(tmp_path: Path) -> None:
    """13 (Albane 2026-07-06) — OMISSION : plage vide -> la mention « numérotées de … inclus »
    est ENTIEREMENT omise de la resolution (pas de « numérotées de  inclus » incomplet) ;
    la phrase enchaine directement « … à la <SPFPL>, à compter de ce jour. »."""
    ctx = _unique_context()
    assert ctx.cession_parts is not None
    ctx.cession_parts.plage_parts = ""  # plage non renseignee
    text = _docx_text(
        PvAgrementCessionSpfplAssocieUniqueGenerator().generate(ctx, tmp_path)
    )
    resolution = _premiere_resolution_line(text)
    assert "numérotées de" not in resolution  # mention omise dans la resolution
    assert "inclus" not in resolution
    assert "à la SPFPL MARTIN, à compter de ce jour." in resolution


# ---------------------------------------------------------------------------
# Retours Rafael 2026-07-09 (soir) — PV d'agrement cession (C1/C2/C3/C4).
# Verbatim = spec : en-tete titre en gras, date en lettres NON dupliquee, tirets
# sur les enonciations des decisions, n° d'article capital SAISISSABLE.
# ---------------------------------------------------------------------------


def _find_paragraph_by_text(path: Path, text: str):
    return next(p for p in Document(path).paragraphs if p.text == text)


def test_pv_agrement_unique_entete_titre_societe_en_gras(tmp_path: Path) -> None:
    # C1 : uniformiser l'en-tete — le titre de la societe (denomination) en GRAS.
    path = PvAgrementCessionSpfplAssocieUniqueGenerator().generate(_unique_context(), tmp_path)
    denomination = _find_paragraph_by_text(path, "SELARL CABINET MARTIN")
    assert denomination.runs[0].bold is True
    # La ligne de forme sociale n'est PAS mise en gras (seul le titre l'est).
    forme = _find_paragraph_by_text(path, "SELARL")
    assert not any(r.bold for r in forme.runs)


def test_pv_agrement_plusieurs_entete_titre_societe_en_gras(tmp_path: Path) -> None:
    # C1 : idem sur le PV « plusieurs associes ».
    path = PvAgrementCessionSpfplPlusieursAssociesGenerator().generate(_plural_context(), tmp_path)
    denomination = _find_paragraph_by_text(path, "SELARL CABINET MARTIN")
    assert denomination.runs[0].bold is True


def test_pv_agrement_date_lettres_annee_non_dupliquee(tmp_path: Path) -> None:
    # C2 : l'annee en lettres n'apparait qu'UNE fois (« L'an <annee>, » puis
    # « Le <jour mois>, a <heure>, » SANS repeter l'annee).
    cases = (
        ("unique", PvAgrementCessionSpfplAssocieUniqueGenerator(), _unique_context()),
        ("plural", PvAgrementCessionSpfplPlusieursAssociesGenerator(), _plural_context()),
    )
    for name, generator, ctx in cases:
        text = _docx_text(generator.generate(ctx, tmp_path / name))
        assert "L'an deux mille vingt-six," in text
        assert "Le quatorze mai, à 10 heures," in text
        # L'ancienne date, qui repetait l'annee, ne doit plus apparaitre.
        assert "Le quatorze mai deux mille vingt-six" not in text
        # « deux mille vingt-six » n'apparait qu'UNE fois (la ligne « L'an … »).
        assert text.count("deux mille vingt-six") == 1


def test_pv_agrement_ordre_du_jour_en_tirets(tmp_path: Path) -> None:
    # C3 : les enonciations des decisions (ordre du jour) sont prefixees d'un tiret « - ».
    cases = (
        ("unique", PvAgrementCessionSpfplAssocieUniqueGenerator(), _unique_context()),
        ("plural", PvAgrementCessionSpfplPlusieursAssociesGenerator(), _plural_context()),
    )
    for name, generator, ctx in cases:
        path = generator.generate(ctx, tmp_path / name)
        paras = [p.text for p in Document(path).paragraphs if p.text]
        assert "- Agrément d'un nouvel associé, la SPFPL MARTIN ;" in paras
        assert "- Modification corrélative des statuts ;" in paras
        assert "- Pouvoirs pour l'accomplissement des formalités." in paras
        # La phrase d'amorce n'est PAS une enonciation -> pas de tiret.
        assert "Dès lors, il est décidé de ce qui suit :" in paras


def test_pv_agrement_article_capital_numero_defaut_7bis(tmp_path: Path) -> None:
    # C4 : sans saisie, le n° d'article du capital reste « 7 bis » aux 2 endroits (byte-neutre).
    text = _docx_text(
        PvAgrementCessionSpfplAssocieUniqueGenerator().generate(_unique_context(), tmp_path)
    )
    assert "l'article 7 bis des statuts sera modifié comme suit" in text
    assert "« Article 7 bis - Capital social" in text


def test_pv_agrement_article_capital_numero_saisissable(tmp_path: Path) -> None:
    # C4 : n° d'article saisissable (ctx.metadata["pv_article_capital_numero"]) — les 2
    # occurrences (phrase de modification ET en-tete du bloc) suivent la saisie.
    ctx = _unique_context()
    ctx.metadata = {"pv_article_capital_numero": "8"}
    text = _docx_text(
        PvAgrementCessionSpfplAssocieUniqueGenerator().generate(ctx, tmp_path)
    )
    assert "l'article 8 des statuts sera modifié comme suit" in text
    assert "« Article 8 - Capital social" in text
    assert "7 bis" not in text
