from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from _accents import assert_no_unaccented_french
from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    ApportTitres,
    CapitalSouscripteur,
    CapitalSouscription,
    DocumentGenerationContext,
    DossierOptions,
    ExerciceSocial,
    Person,
    RemunerationPresident,
    Signature,
    SocieteCible,
    SocieteSpfpl,
    SpfplPerson,
    StatutsPresident,
    StatutsSas,
)
from sydel_doc_engine.generators.lot_05.attestation_capital_liste_souscripteurs_sas import (
    AttestationCapitalListeSouscripteursSasGenerator,
)
from sydel_doc_engine.generators.lot_05.pv_remuneration_president import (
    PvRemunerationPresidentGenerator,
)


def _base_context() -> DocumentGenerationContext:
    return DocumentGenerationContext(
        structure="SAS",
        dossier_options=DossierOptions(associe_unique=True, apport=True),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Camille",
            nom="Martin",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 15)),
        statuts_sas=StatutsSas(type="spfpl_medecins", profession="medecin"),
        societe_spfpl=SocieteSpfpl(
            denomination="SPFPL MARTIN",
            forme_sociale="Société par actions simplifiée",
            capital_social="60 000",
            nb_actions_total=600,
            valeur_nominale_action="100",
            profession="Médecins",
            ville_rcs="Paris",
            siege=Address(
                num_voie="10",
                voie="rue de la Paix",
                cp="75002",
                ville="Paris",
                adresse_affichee="10 rue de la Paix, 75002 Paris",
            ),
        ),
        actionnaire_unique=SpfplPerson(
            civilite_affichage="Docteur",
            prenom="Camille",
            nom="Martin",
            genre=Gender.MASCULIN,
            profession="médecin",
            qualite_associe="actionnaire unique",
            adresse_personnelle=Address(
                num_voie="5",
                voie="rue Royale",
                cp="75008",
                ville="Paris",
            ),
            adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
        ),
        president=StatutsPresident(
            ref_associe_index=0,
            civilite_affichage="Docteur",
            prenom="Camille",
            nom="Martin",
            fonction="Président",
            adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
        ),
        exercice_social=ExerciceSocial(
            date_cloture_premier_exercice="31 décembre 2026",
        ),
        remuneration_president=RemunerationPresident(
            type="absence_remuneration",
            date_fin_non_remuneree="31 décembre 2026",
        ),
        capital_souscription=CapitalSouscription(
            nb_actions_total=600,
            valeur_nominale_action="100",
            apports_nature_montant="50 000",
            apports_numeraire_montant="10 000",
            souscripteurs=[
                CapitalSouscripteur(
                    civilite_affichage="Docteur",
                    prenom="Camille",
                    nom="Martin",
                    profession="médecin",
                    adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
                    nb_actions=600,
                    qualite="actionnaire unique",
                )
            ],
        ),
        apport_titres=ApportTitres(nb_parts=50),
        societe_cible=SocieteCible(
            denomination="SELARL CABINET MARTIN",
            forme_sociale="SELARL",
            siege=Address(adresse_affichee="12 avenue des Ternes, 75017 Paris"),
            ville_rcs="Paris",
            numero_rcs="900 000 001",
        ),
    )


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts = [paragraph.text for paragraph in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(paragraph.text for paragraph in cell.paragraphs)
    return "\n".join(text for text in texts if text)


def _assert_clean(text: str) -> None:
    assert "[" not in text
    assert "]" not in text


def test_pv_remuneration_president_generates_source_wording(tmp_path: Path) -> None:
    output_path = PvRemunerationPresidentGenerator().generate(_base_context(), tmp_path)

    text = _docx_text(output_path)

    assert output_path.name == "pv_remuneration_president.docx"
    assert "PROCES-VERBAL DES DECISIONS" in text
    # R3 Rafael 2026-07-07 : Docteur retiré partout (supersede A26-45/49) — la décision
    # rend la civilité CIVILE (fixture « Docteur » -> « Monsieur »).
    assert "Monsieur Camille Martin, actionnaire unique, décide qu'il ne percevra" in text
    assert "Docteur" not in text
    assert "Fait à Paris en trois exemplaires" in text
    _assert_clean(text)
    assert_no_unaccented_french(text)


def test_pv_remuneration_president_blocks_feminine_wording(tmp_path: Path) -> None:
    ctx = _base_context()
    ctx.actionnaire_unique.genre = Gender.FEMININ

    with pytest.raises(ValueError, match="president masculin"):
        PvRemunerationPresidentGenerator().generate(ctx, tmp_path)


def test_attestation_capital_sas_generates_unique_subscriber_wording(
    tmp_path: Path,
) -> None:
    output_path = AttestationCapitalListeSouscripteursSasGenerator().generate(
        _base_context(),
        tmp_path,
    )

    text = _docx_text(output_path)

    assert output_path.name == "attestation_capital_liste_souscripteurs_sas.docx"
    assert "Liste des souscripteurs" in text
    # R3 Rafael 2026-07-07 : Docteur retiré partout (supersede A26-45/49) — répartition
    # « à Monsieur X » (plus « au Dr X »).
    assert (
        "Répartition : 600 actions attribuées à Monsieur Camille Martin, actionnaire unique"
        in text
    )
    assert "au Dr " not in text
    assert "Apports en nature" in text
    # R3 (Albane 2026-07-07) : « Docteur » n'est pas une civilité — tête de
    # désignation, « par le Président, __ » et signature rendent la civilité CIVILE
    # (Monsieur/Madame) ; durci Rafael 2026-07-07 : la phrase d'apport aussi (plus de
    # titre « Le Docteur X », supersede A26-45/49).
    assert "Monsieur Camille Martin médecin, demeurant" in text
    assert "par le Président, Monsieur Camille Martin." in text
    assert "Président, Docteur" not in text
    assert text.rstrip().endswith("Monsieur Camille Martin")
    assert "Monsieur Camille Martin a fait la totalité des apports en nature." in text
    assert "Docteur" not in text
    _assert_clean(text)
    assert_no_unaccented_french(text)


def test_attestation_capital_sas_aere_titre_designation_corps_et_apports(
    tmp_path: Path,
) -> None:
    # Retour Albane « mise en forme » 1.6 (M2) : MEME aeration que la variante SPFPL —
    # (a) espace APRES la phrase d'apport et APRES « Total des apports » ; (b) espace entre
    # la designation de la societe, le bloc titre et le corps (paragraphes-espaceurs 10 pt).
    from docx.shared import Pt

    document = Document(
        AttestationCapitalListeSouscripteursSasGenerator().generate(_base_context(), tmp_path)
    )
    paragraphs = document.paragraphs

    def _index(predicate) -> int:
        return next(i for i, p in enumerate(paragraphs) if predicate(p.text))

    designation_idx = _index(lambda t: t.startswith("Siège social :"))
    titre_idx = _index(lambda t: t.strip() == "ATTESTATION")
    liste_idx = _index(lambda t: t.strip() == "Liste des souscripteurs")
    corps_idx = _index(lambda t: "atteste que le capital" in t)
    apport_idx = _index(lambda t: "fait apport de" in t and "pour une valeur de" in t)
    total_idx = _index(lambda t: t.startswith("Total des apports en nature"))

    # (b) Un paragraphe-espaceur (vide, 10 pt) separe la designation du titre, et le titre
    # du corps.
    spacer_designation_titre = paragraphs[designation_idx + 1]
    assert not spacer_designation_titre.text.strip()
    assert spacer_designation_titre.paragraph_format.space_after == Pt(10)
    assert titre_idx == designation_idx + 2

    spacer_titre_corps = paragraphs[liste_idx + 1]
    assert not spacer_titre_corps.text.strip()
    assert spacer_titre_corps.paragraph_format.space_after == Pt(10)
    assert corps_idx == liste_idx + 2

    # (a) Espace de 10 pt APRES la phrase d'apport et APRES « Total des apports ».
    assert paragraphs[apport_idx].paragraph_format.space_after == Pt(10)
    assert paragraphs[total_idx].paragraph_format.space_after == Pt(10)


def test_attestation_capital_sas_blocks_multiple_subscribers(tmp_path: Path) -> None:
    ctx = _base_context()
    ctx.capital_souscription.souscripteurs.append(
        CapitalSouscripteur(
            civilite_affichage="Docteur",
            prenom="Louise",
            nom="Bernard",
            profession="médecin",
            adresse_personnelle_affichee="9 rue Bleue, 75009 Paris",
            nb_actions=1,
        )
    )

    with pytest.raises(ValueError, match="exactement un souscripteur"):
        AttestationCapitalListeSouscripteursSasGenerator().generate(ctx, tmp_path)


def test_attestation_capital_sas_blocks_capital_mismatch(tmp_path: Path) -> None:
    ctx = _base_context()
    ctx.capital_souscription.apports_numeraire_montant = "9 000"

    with pytest.raises(ValueError, match="apports en nature et en numeraire"):
        AttestationCapitalListeSouscripteursSasGenerator().generate(ctx, tmp_path)
