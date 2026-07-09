from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    CapitalSouscripteur,
    CapitalSouscription,
    CessionBanque,
    DepotFonds,
    DocumentGenerationContext,
    DossierOptions,
    ExerciceSocial,
    Person,
    Signature,
    SocieteSpfpl,
    SpfplConjoint,
    SpfplOrdre,
    SpfplPerson,
    StatutsPresident,
    StatutsSas,
)
from sydel_doc_engine.generators.lot_04.statuts_sas import StatutsSasGenerator
from sydel_doc_engine.orchestrator.service import DocumentOrchestrator
from sydel_doc_engine.registry.catalog import build_seed_catalog


def _context() -> DocumentGenerationContext:
    actionnaire = SpfplPerson(
        civilite_affichage="Docteur",
        prenom="Camille",
        nom="Martin",
        genre=Gender.MASCULIN,
        profession="medecin",
        qualification_principale="Médecin cardiologue",
        date_naissance="2 janvier 1980",
        ville_naissance="Paris",
        departement_naissance="75",
        nationalite="française",
        situation_maritale="Marié",
        regime_matrimonial="la communauté légale",
        conjoint=SpfplConjoint(
            civilite_affichage="Madame",
            prenom="Alice",
            nom="Martin",
        ),
        adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
        ordre=SpfplOrdre(
            departement="Paris",
            numero="12345",
            numero_rpps="10000000001",
        ),
        nb_actions=120,
    )
    return DocumentGenerationContext(
        structure="SAS",
        dossier_options=DossierOptions(associe_unique=True),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Camille",
            nom="Martin",
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 14)),
        statuts_sas=StatutsSas(type="spfpl_medecins", profession="medecin"),
        societe_spfpl=SocieteSpfpl(
            denomination="SPFPL MARTIN",
            capital_social="12 000",
            capital_social_lettres="douze mille",
            nb_actions_total=120,
            nb_actions_total_lettres="cent vingt",
            valeur_nominale_action="100",
            valeur_nominale_action_lettres="cent euros",
            profession="medecin",
            siege=Address(adresse_affichee="10 rue de la Paix, 75002 Paris"),
        ),
        actionnaire_unique=actionnaire,
        president=StatutsPresident(
            ref_associe_index=0,
            civilite_affichage="Docteur",
            prenom="Camille",
            nom="Martin",
            adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
            duree_mandat="illimitee",
        ),
        depot_fonds=DepotFonds(
            banque=CessionBanque(nom="BANQUE EXEMPLE"),
            montant="12 000",
        ),
        exercice_social=ExerciceSocial(
            debut="1er janvier",
            fin="31 décembre",
            date_cloture_premier_exercice="31 décembre 2026",
        ),
        capital_souscription=CapitalSouscription(
            nb_actions_total=120,
            valeur_nominale_action="100",
            apports_numeraire_montant="12 000",
            souscripteurs=[
                CapitalSouscripteur(
                    civilite_affichage="Docteur",
                    prenom="Camille",
                    nom="Martin",
                    profession="medecin",
                    adresse_personnelle_affichee="5 rue Royale, 75008 Paris",
                    nb_actions=120,
                    qualite="actionnaire unique",
                )
            ],
        ),
    )


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts = [paragraph.text for paragraph in document.paragraphs]
    for section in document.sections:
        texts.extend(paragraph.text for paragraph in section.footer.paragraphs)
    return "\n".join(text for text in texts if text)


def _assert_clean(text: str) -> None:
    assert "[" not in text
    assert "]" not in text
    assert "OU\n" not in text


def test_statuts_sas_generates_spfpl_medecins_unique_shareholder_docx(
    tmp_path: Path,
) -> None:
    output_path = StatutsSasGenerator().generate(_context(), tmp_path)

    text = _docx_text(output_path)
    document = Document(output_path)
    article_1 = next(p for p in document.paragraphs if p.text == "ARTICLE 1 - FORME")
    acceptance = next(
        p for p in document.paragraphs if "Bon pour acceptation des fonctions" in p.text
    )

    # R10 (Rafael 2026-07-07) : le fichier statuts porte la denomination.
    assert output_path.name == "Statuts SPFPL MARTIN.docx"
    assert "SPFPL MARTIN" in text
    assert "Société de Participations Financières de Profession Libérale de Médecins" in text
    # Rafael 2026-07-09 « supprimer partout » : « Par le Docteur … » / « Le Docteur … » du modele
    # -> civilite CIVILE (« Monsieur … »), sans article, plus jamais « Docteur ».
    assert "Par Monsieur Camille Martin 12 000" in text
    assert "Monsieur Camille Martin 120 actions" in text
    assert "Docteur" not in text
    assert "L’Associé Unique, Monsieur Camille Martin" in text
    assert "BANQUE EXEMPLE" in text
    assert "SPFPL MARTIN – Statuts constitutifs" in text
    assert any(run.underline for run in article_1.runs)
    assert any(run.italic for run in acceptance.runs)
    _assert_clean(text)


def test_statuts_sas_heading_formatting_matches_source(tmp_path: Path) -> None:
    """Fidelite de FORME au modele STATUTS_SAS_SPFPL_medecins_modele.docx.

    Source :
    - articles principaux ("ARTICLE 1 - FORME", "ARTICLE 13 - DIRECTEURS GENERAUX") :
      gras + souligne ;
    - sous-articles ("Article 9.1", "ARTICLE 13-1 - DESIGNATION") : gras SANS souligne ;
    - intitules article 12 ("NOMINATION ET POUVOIRS", "REMUNERATION") : souligne SANS gras.
    """
    document = Document(StatutsSasGenerator().generate(_context(), tmp_path))
    by_text = {p.text.strip(): p for p in document.paragraphs}

    def fmt(label: str) -> tuple[bool, bool]:
        runs = by_text[label].runs
        return (
            any(bool(run.bold) for run in runs),
            any(bool(run.underline) for run in runs),
        )

    # Article principal : gras + souligne
    assert fmt("ARTICLE 1 - FORME") == (True, True)
    assert fmt("ARTICLE 13 - DIRECTEURS GENERAUX") == (True, True)
    # Sous-article numerote : gras, non souligne
    assert fmt("Article 9.1 Augmentation du capital") == (True, False)
    assert fmt("Article 10.1 Clause d’agrément") == (True, False)
    # Sous-article a tiret : gras, non souligne (et NON traite comme article principal)
    assert fmt("ARTICLE 13-1 - DESIGNATION") == (True, False)
    assert fmt("ARTICLE 13-4 - REMUNERATION") == (True, False)
    # Intitules article 12 : souligne, non gras
    assert fmt("NOMINATION ET POUVOIRS") == (False, True)
    assert fmt("REMUNERATION") == (False, True)


def test_statuts_sas_is_selected_only_for_confirmed_spfpl_medecins_context() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())

    selected = orchestrator.select_documents_for_context(_context())

    assert "DOC-015" in [document.doc_id for document in selected]

    ctx = _context()
    ctx.statuts_sas = None

    selected_without_statuts = orchestrator.select_documents_for_context(ctx)

    assert "DOC-015" not in [document.doc_id for document in selected_without_statuts]


def test_statuts_sas_blocks_multiple_souscripteurs(tmp_path: Path) -> None:
    ctx = _context()
    ctx.capital_souscription.souscripteurs.append(
        CapitalSouscripteur(
            civilite_affichage="Docteur",
            prenom="Louise",
            nom="Bernard",
            profession="medecin",
            adresse_personnelle_affichee="9 rue Bleue, 75009 Paris",
            nb_actions=1,
        )
    )

    with pytest.raises(ValueError, match="exactement un souscripteur"):
        StatutsSasGenerator().generate(ctx, tmp_path)


def test_statuts_sas_blocks_incoherent_capital(tmp_path: Path) -> None:
    ctx = _context()
    ctx.societe_spfpl.nb_actions_total = 121

    with pytest.raises(ValueError, match="coherents"):
        StatutsSasGenerator().generate(ctx, tmp_path)


def test_statuts_sas_blocks_president_distinct_from_unique_shareholder(
    tmp_path: Path,
) -> None:
    ctx = _context()
    ctx.president.nom = "Bernard"

    with pytest.raises(ValueError, match="president doit designer"):
        StatutsSasGenerator().generate(ctx, tmp_path)


@pytest.mark.parametrize("statut", ["Célibataire", "Pacsé", "Divorcé", "Veuf"])
def test_statuts_sas_non_marie_replie_sur_le_statut(tmp_path: Path, statut) -> None:
    # R0702-02 (Gad 2026-07-02) : le SAS accepte DESORMAIS tout statut matrimonial (menu complet
    # « Situation matrimoniale », comme la SPFPL). Un NON-MARIE (celibataire/pacse/divorce/veuf)
    # rend juste son statut — la clause mariee du modele (« sous le régime de ... avec <conjoint> »)
    # est repliee sur le seul statut, SANS token/marqueur/conjoint fantome. (Remplace l'ancien test
    # qui verrouillait le blocage « without source variant » — decision levee par Gad ; Akainu n2 :
    # paramétré sur les 4 statuts non-mariés.)
    from docx import Document

    ctx = _context()
    ctx.actionnaire_unique.situation_maritale = statut
    ctx.actionnaire_unique.regime_matrimonial = ""
    ctx.actionnaire_unique.conjoint = None

    out = StatutsSasGenerator().generate(ctx, tmp_path)
    text = "\n".join(p.text for p in Document(out).paragraphs)
    assert statut in text
    # Comparution repliee : plus de clause mariee ni de fuite pour un non-marie.
    assert f"{statut} sous le régime de" not in text
    assert "À COMPLÉTER" not in text
    assert "avec (" not in text
    assert "[" not in text and "]" not in text


@pytest.mark.parametrize(
    ("statut", "conjoint_civilite"),
    [("Pacsé", "Madame"), ("Pacsée", "Monsieur")],
)
def test_statuts_sas_pacse_affiche_partenaire(
    tmp_path: Path, statut, conjoint_civilite
) -> None:
    # Albane 6.3/7.3 (RATIFIE 2026-07-06) : un actionnaire PACSE affiche son PARTENAIRE
    # (« Pacsé avec <Civilite Prenom Nom> »), SANS « sous le régime de … » : la clause mariee
    # du modele est repliee sur « <statut> avec <partenaire> ». Les 2 genres sont couverts.
    from docx import Document

    ctx = _context()
    ctx.actionnaire_unique.situation_maritale = statut
    ctx.actionnaire_unique.regime_matrimonial = ""
    ctx.actionnaire_unique.conjoint = SpfplConjoint(
        civilite_affichage=conjoint_civilite, prenom="Alice", nom="Martin"
    )
    out = StatutsSasGenerator().generate(ctx, tmp_path)
    text = "\n".join(p.text for p in Document(out).paragraphs)
    assert f"{statut} avec {conjoint_civilite} Alice Martin" in text
    assert f"{statut} sous le régime de" not in text
    assert "À COMPLÉTER" not in text
    assert "[" not in text and "]" not in text


@pytest.mark.parametrize("statut", ["Pacsé", "Pacsée"])
def test_statuts_sas_pacse_sans_partenaire_replie_sur_statut(tmp_path: Path, statut) -> None:
    # « Pas de mention sans nom » (Albane 6.3) : un pacse SANS partenaire renseigne rend le SEUL
    # statut (« Pacsé »), sans « avec » orphelin, sans « sous le régime de », sans token/marqueur.
    from docx import Document

    ctx = _context()
    ctx.actionnaire_unique.situation_maritale = statut
    ctx.actionnaire_unique.regime_matrimonial = ""
    ctx.actionnaire_unique.conjoint = None
    out = StatutsSasGenerator().generate(ctx, tmp_path)
    text = "\n".join(p.text for p in Document(out).paragraphs)
    assert statut in text
    assert f"{statut} avec" not in text
    assert f"{statut} sous le régime de" not in text
    assert "À COMPLÉTER" not in text
    assert "[" not in text and "]" not in text


@pytest.mark.parametrize(
    "regime",
    [
        "la communauté légale",
        "la séparation de biens",
        "la communauté universelle",
        "la participation aux acquêts",
    ],
)
def test_statuts_sas_marie_comparution_byte_fidele(tmp_path: Path, regime) -> None:
    # R0702-02 : le cas MARIE reste FIDELE (comparution complete du modele) sur les 4 REGIMES
    # dérivés par `married_regime_display`. Verrou de non-regression du chemin marie — le fix
    # non-marie ne doit rien changer pour un marie. (Akainu n1 : paramétré sur les 4 régimes.)
    from docx import Document

    ctx = _context()  # marie, conjoint Madame Alice Martin
    ctx.actionnaire_unique.regime_matrimonial = regime
    out = StatutsSasGenerator().generate(ctx, tmp_path)
    text = "\n".join(p.text for p in Document(out).paragraphs)
    assert f"Marié sous le régime de {regime} avec Madame Alice Martin" in text
