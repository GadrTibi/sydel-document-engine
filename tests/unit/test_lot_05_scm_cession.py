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
    DocumentGenerationContext,
    DossierOptions,
    Person,
    ScmCessionAgrement,
    ScmCessionAssocie,
    ScmCessionCedant,
    ScmCessionConjoint,
    ScmCessionContext,
    ScmCessionCreditVendeur,
    ScmCessionEnregistrement,
    ScmCessionOrdre,
    ScmCessionPartsAttribution,
    ScmCessionPartsCedees,
    ScmCessionPrix,
    ScmCessionRepresentant,
    ScmCessionSignataire,
    ScmCessionSociete,
    Signature,
)
from sydel_doc_engine.generators.lot_05.acte_cession_parts_scm import (
    ActeCessionPartsScmGenerator,
)
from sydel_doc_engine.generators.lot_05.courrier_sde_cession_scm import (
    CourrierSdeCessionScmGenerator,
)
from sydel_doc_engine.generators.lot_05.pv_age_cession_scm import PvAgeCessionScmGenerator
from sydel_doc_engine.orchestrator.service import DocumentOrchestrator
from sydel_doc_engine.registry.catalog import build_seed_catalog


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
    assert "Ajouter en cas de CV" not in text


def _associe(
    name: str,
    parts: int,
    plage: str,
    *,
    morale: bool = False,
) -> ScmCessionAssocie:
    if morale:
        return ScmCessionAssocie(
            type_personne="personne_morale",
            denomination=name,
            forme_juridique="SELARL",
            parts=ScmCessionPartsAttribution(nb=parts, plage=plage),
        )
    prenom, nom = name.split(" ", 1)
    return ScmCessionAssocie(
        civilite_affichage="Monsieur" if prenom != "Anne" else "Madame",
        prenom=prenom,
        nom=nom,
        parts=ScmCessionPartsAttribution(nb=parts, plage=plage),
    )


def test_scm_cession_plage_cedee_auto_derivee_n4() -> None:
    # N4 (Rafael 2026-06-24) : la plage cedee est auto-derivee de la plage du cedant + nb cede,
    # convention « le cedant cede ses dernieres parts » -> residu contigu au debut. Plus de saisie
    # manuelle. Verrouille le helper pur + la derivation integree (Akainu N4 M2/m2).
    from sydel_doc_engine.front_app.shell import (
        _derive_scm_apres_cession,
        _plage_dernieres_parts,
    )

    # N4 (2026-07-01) : plages avec « à » accentue (parser _parse_plage accepte a/à/-).
    assert _plage_dernieres_parts("1 à 100", 40) == "61 à 100"
    assert _plage_dernieres_parts("41 à 100", 20) == "81 à 100"
    assert _plage_dernieres_parts("1 à 40", 50) == ""  # nb > taille de la plage
    assert _plage_dernieres_parts("", 10) == ""  # plage non parsable

    presents = [_associe("Jean Dupont", 100, "1 à 100")]
    cedant = {"prenom": "Jean", "nom": "Dupont", "civilite_affichage": "Monsieur"}
    cessionnaire = {"denomination": "SELARL X", "forme_juridique": "SELARL"}
    parts_cedees: dict[str, object] = {"nb": 40}  # plage NON fournie -> doit etre derivee
    apres = _derive_scm_apres_cession(presents, cedant, cessionnaire, parts_cedees)
    assert parts_cedees["plage"] == "61 à 100"  # derivee in-place (dernieres 40 parts)
    cedant_apres = next(a for a in apres if a.type_personne == "personne_physique")
    assert cedant_apres.parts is not None
    assert cedant_apres.parts.plage == "1 à 60" and cedant_apres.parts.nb == 60
    sel = next(a for a in apres if a.type_personne == "personne_morale")
    assert sel.parts is not None and sel.parts.plage == "61 à 100"


def _base_context(structure: str = "SELARL") -> DocumentGenerationContext:
    variant = structure.lower()
    is_selas = structure == "SELAS"
    cessionnaire_forme = "SELAS" if is_selas else "SELARL"
    return DocumentGenerationContext(
        structure=structure,
        dossier_options=DossierOptions(scm_cession=True),
        personne_signataire=Person(
            genre=Gender.MASCULIN,
            civilite="Monsieur",
            prenom="Jean",
            nom="Dupont",
        ),
        signature=Signature(
            lieu="Paris",
            date=date(2026, 5, 15),
            prestataire_signature_electronique="DocuSign",
        ),
        scm_cession=ScmCessionContext(
            variante_structure=variant,
            scm_cedee=ScmCessionSociete(
                denomination="SCM CABINET CENTRAL",
                forme_juridique="Société Civile de Moyens",
                capital_social="3 000",
                siege=Address(adresse_affichee="12 rue des Soins, 75008 Paris"),
                ville_rcs="Paris",
                numero_rcs="900 111 222",
                nb_parts_total=300,
                valeur_nominale_part="10",
                plage_parts_total="1 à 300",
                cogerants=["Monsieur Paul Bernard", "Monsieur Jean Dupont", "Madame Anne Martin"],
            ),
            cessionnaire=ScmCessionSociete(
                denomination=f"{cessionnaire_forme} CABINET DUPONT",
                forme_juridique=cessionnaire_forme,
                capital_social="10 000",
                siege=Address(adresse_affichee="20 avenue des Praticiens, 75008 Paris"),
                ville_rcs="Paris",
                representant=ScmCessionRepresentant(
                    civilite_affichage="Monsieur",
                    civilite_courte="M.",
                    prenom="Jean",
                    nom="Dupont",
                    fonction="président" if is_selas else "gérant",
                ),
            ),
            cedant=ScmCessionCedant(
                civilite_affichage="Monsieur",
                prenom="Jean",
                nom="Dupont",
                profession="chirurgien-dentiste",
                profession_reglementee_pluriel="chirurgiens-dentistes",
                date_naissance="1er janvier 1980",
                ville_naissance="Paris",
                departement_naissance="75",
                nationalite="française",
                adresse_affichee="1 rue du Cédant, 75008 Paris",
                situation_maritale="marié",
                ordre=ScmCessionOrdre(departemental="Paris", numero="12345"),
                numero_rpps="10000000001",
                conjoint=ScmCessionConjoint(
                    civilite_affichage="Madame",
                    prenom="Claire",
                    nom="Dupont",
                ),
            ),
            agrement=ScmCessionAgrement(
                date_pv="15 mai 2026",
                date_pv_lettres="deux mille vingt-six, le quinze mai",
                delai_mois="3" if is_selas else None,
                date_limite="15 août 2026" if is_selas else None,
            ),
            associes_presents=[
                _associe("Paul Bernard", 100, "1 à 100"),
                _associe("Jean Dupont", 100, "101 à 200"),
                _associe("Anne Martin", 100, "201 à 300"),
            ],
            associes_avant_cession=[
                _associe("Paul Bernard", 100, "1 à 100"),
                _associe("Jean Dupont", 100, "101 à 200"),
                _associe("Anne Martin", 100, "201 à 300"),
            ],
            associes_apres_cession=[
                _associe("Paul Bernard", 100, "1 à 100"),
                _associe("Jean Dupont", 50, "101 à 150"),
                _associe(f"{cessionnaire_forme} CABINET DUPONT", 50, "151 à 200", morale=True),
                _associe("Anne Martin", 100, "201 à 300"),
            ],
            signataires_pv=["M. Jean Dupont", "M. Paul Bernard", "Mme Anne Martin"],
            parts_cedees=ScmCessionPartsCedees(nb=50, plage="151 à 200"),
            prix=ScmCessionPrix(
                unitaire="100",
                unitaire_lettres="cent",
                global_="5 000",
                global_lettres="cinq mille",
            ),
            paiement_mode="pret_bancaire",
            credit_vendeur=ScmCessionCreditVendeur(actif=False),
            enregistrement=ScmCessionEnregistrement(
                service="SERVICE DEPARTEMENTAL DE L'ENREGISTREMENT",
                centre_finances_publiques="Centre des finances publiques de Paris",
                adresse_service="6 rue Paganini",
                cp_ville_service="75020 Paris",
                nombre_exemplaires="3",
                montant_droits="150",
            ),
            signataire_sde=ScmCessionSignataire(prenom="Sarah", nom="Durand"),
            nombre_exemplaires_lettres="quatre",
            prestataire_signature_electronique="DocuSign",
            date_acte_affichee="15 mai 2026",
            representant_cessionnaire_confirme=True,
        ),
    )


def test_scm_cession_selarl_generates_three_clean_docx(tmp_path: Path) -> None:
    ctx = _base_context("SELARL")

    outputs = [
        PvAgeCessionScmGenerator().generate(ctx, tmp_path),
        CourrierSdeCessionScmGenerator().generate(ctx, tmp_path),
        ActeCessionPartsScmGenerator().generate(ctx, tmp_path),
    ]
    texts = {path.name: _docx_text(path) for path in outputs}

    assert {path.name for path in outputs} == {
        "pv_age_cession_parts_scm.docx",
        "courrier_sde_cession_scm.docx",
        "acte_cession_parts_scm.docx",
    }
    assert "à compter de ce jour" in texts["pv_age_cession_parts_scm.docx"]
    assert "dans un délai de" not in texts["pv_age_cession_parts_scm.docx"]
    assert "4 exemplaires" in texts["courrier_sde_cession_scm.docx"]
    # §8.1 — bloc destinataire SDE rendu pour TOUTES structures (ligne fixe).
    assert (
        "Service départemental de l'enregistrement de"
        in texts["courrier_sde_cession_scm.docx"]
    )
    # §8.2 — nom de la SCM imprime dans le corps.
    # Albane 2026-06-26 §C2 : « de la Société {denom} » (plus de doublon « SCM SCM »).
    assert (
        "de parts de la Société SCM CABINET CENTRAL"
        in texts["courrier_sde_cession_scm.docx"]
    )
    assert "SCM SCM CABINET CENTRAL" not in texts["courrier_sde_cession_scm.docx"]
    assert "chirurgiens-dentistes" in texts["acte_cession_parts_scm.docx"]
    assert "Yousign" in texts["acte_cession_parts_scm.docx"]
    for text in texts.values():
        _assert_clean(text)


def test_acte_cession_scm_omits_conjoint_when_not_married(tmp_path: Path) -> None:
    # R22-02 (Rafael 2026-06-22) : pas de conjoint fantome quand le cedant n'est pas marie.
    # Cas Rafael : « divorce avec Madame Claire Dupont » alors qu'aucune epouse n'existe. On
    # garde la donnee conjoint en residu (comme dans son test) pour prouver que le GENERATEUR
    # ne l'affiche plus.
    ctx = _base_context("SELARL")
    ctx.scm_cession.cedant.situation_maritale = "divorcé"
    acte = ActeCessionPartsScmGenerator().generate(ctx, tmp_path)
    text = _docx_text(acte)
    assert "divorcé" in text
    assert "Claire Dupont" not in text
    assert "avec Madame" not in text
    _assert_clean(text)


def test_acte_cession_scm_keeps_conjoint_when_married(tmp_path: Path) -> None:
    # Contre-epreuve : un cedant marie affiche bien son conjoint (comportement gold conserve).
    ctx = _base_context("SELARL")  # situation_maritale="marié" + conjoint Claire Dupont
    acte = ActeCessionPartsScmGenerator().generate(ctx, tmp_path)
    text = _docx_text(acte)
    assert "marié avec Madame Claire Dupont" in text


def test_acte_cession_scm_shows_partner_when_pacse_masculin(tmp_path: Path) -> None:
    # Albane 6.3/7.3 (RATIFIE 2026-07-06) : un cedant PACSE affiche son PARTENAIRE
    # (« pacsé avec {Civilite Prenom Nom} »), SANS « sous le régime de … ».
    ctx = _base_context("SELARL")
    ctx.scm_cession.cedant.situation_maritale = "pacsé"
    acte = ActeCessionPartsScmGenerator().generate(ctx, tmp_path)
    text = _docx_text(acte)
    assert "pacsé avec Madame Claire Dupont" in text
    assert "sous le régime de" not in text
    _assert_clean(text)


def test_acte_cession_scm_shows_partner_when_pacsee_feminin(tmp_path: Path) -> None:
    # Genre feminin : « pacsée avec … ».
    ctx = _base_context("SELARL")
    ctx.scm_cession.cedant.situation_maritale = "pacsée"
    ctx.scm_cession.cedant.conjoint = ScmCessionConjoint(
        civilite_affichage="Monsieur", prenom="Marc", nom="Durand"
    )
    acte = ActeCessionPartsScmGenerator().generate(ctx, tmp_path)
    text = _docx_text(acte)
    assert "pacsée avec Monsieur Marc Durand" in text
    _assert_clean(text)


def test_acte_cession_scm_pacse_without_partner_no_mention(tmp_path: Path) -> None:
    # « Pas de mention sans nom » (Albane 6.3) : un pacse SANS partenaire renseigne rend
    # « pacsé » nu — jamais « avec (À COMPLÉTER) » ni « avec » orphelin.
    ctx = _base_context("SELARL")
    ctx.scm_cession.cedant.situation_maritale = "pacsé"
    ctx.scm_cession.cedant.conjoint = ScmCessionConjoint()
    acte = ActeCessionPartsScmGenerator().generate(ctx, tmp_path)
    text = _docx_text(acte)
    assert "pacsé" in text
    assert "pacsé avec" not in text
    assert "COMPLÉTER" not in text
    _assert_clean(text)


def test_scm_cession_non_divisible_capital_now_generates(tmp_path: Path) -> None:
    # N1 (Rafael/Vincent 2026-06-24) : la valeur nominale PEUT etre decimale (regle ratifiee).
    # Un capital de SCM cedee non divisible par le nb de parts ne bloque PLUS le generateur ;
    # l'acte se genere (l'arrondi au centime cote saisie evite la decimale infinie). Ancien
    # plancher O24-05 (raise) retire.
    ctx = _base_context("SELARL")
    ctx.scm_cession.scm_cedee.capital_social = "1000"  # 1000 / 300 = valeur nominale decimale
    acte = ActeCessionPartsScmGenerator().generate(ctx, tmp_path)
    assert acte.exists()


def test_scm_cession_selas_generates_overlays(tmp_path: Path) -> None:
    ctx = _base_context("SELAS")

    pv_path = PvAgeCessionScmGenerator().generate(ctx, tmp_path)
    courrier_path = CourrierSdeCessionScmGenerator().generate(ctx, tmp_path)
    acte_path = ActeCessionPartsScmGenerator().generate(ctx, tmp_path)

    pv_text = _docx_text(pv_path)
    courrier_text = _docx_text(courrier_path)
    acte_text = _docx_text(acte_path)
    # Albane 2026-06-26 §P4 : la 1re résolution n'utilise plus « dans un délai de 3 mois ...
    # soit jusqu'au {date} » (supprimé pour TOUTES structures, SELAS comprise) mais « à compter
    # de ce jour », et autorise la cession.
    assert "dans un délai de" not in pv_text
    assert "15 août 2026" not in pv_text
    assert "à compter de ce jour" in pv_text
    assert "autorise la cession de 50 parts sociales de Monsieur Jean Dupont" in pv_text
    # Akainu B1/M1 : le PV AGE cession SCM est un générateur FROM-SCRATCH -> garde-fou centralisé
    # anti-non-accentué sur sa SORTIE. Le courrier/acte sont token-replacement (hors périmètre :
    # ils préservent les intitulés source en CAPITALES non accentuées, cf. §8.1 ci-dessous).
    assert_no_unaccented_french(pv_text)
    # §8.1 — ligne destinataire fixe presente quelle que soit la structure ;
    # la valeur saisie du service (quand fournie) suit la ligne fixe.
    assert "Service départemental de l'enregistrement de" in courrier_text
    assert "SERVICE DEPARTEMENTAL DE L'ENREGISTREMENT" in courrier_text
    # §8.2/§8.3 — nombre d'exemplaires fixe « 4 » et montant droits fixe « 25 ».
    assert "4 exemplaires" in courrier_text
    assert "3 exemplaires" not in courrier_text
    assert "chèque de 25 euros" in courrier_text
    assert "SELAS au capital de 10 000" in acte_text
    assert "président" in acte_text
    assert "DocuSign" in acte_text
    for text in [pv_text, courrier_text, acte_text]:
        _assert_clean(text)
        # re-Akainu tour 2 (NITPICK LIVE-03) : garde générique anti-mois-non-accentué sur la
        # SORTIE réelle (DOCX rendu), pas seulement la fixture en amont. Une régression de
        # rendu (lowercase / strip d'accents côté template) serait attrapée ici.
        low = text.casefold()
        for non_accentue in ("aout", "fevrier", "decembre"):
            assert non_accentue not in low, f"LIVE-03 : « {non_accentue} » non accentué (rendu)"


@pytest.mark.parametrize(
    ("preset_brut", "genre", "attendu_regime"),
    [
        (
            "Marié(e) sous le régime de la séparation de biens",
            Gender.MASCULIN,
            "marié sous le régime de séparation de biens",
        ),
        (
            "Marié(e) sous le régime de la communauté universelle",
            Gender.FEMININ,
            "mariée sous le régime de communauté universelle",
        ),
    ],
)
def test_scm_cession_acte_selas_situation_cedant_accentuee(
    tmp_path: Path, monkeypatch, preset_brut, genre, attendu_regime
) -> None:
    # O24-11 (MINEUR 2a) : preuve BOUT-EN-BOUT sur le chemin SELAS (prefix='selas').
    # Le BLOQUANT O24-11 n'etait prouve e2e que sur SELARL. On exerce ici le HELPER
    # REEL `shell._scm_cedant_situation_maritale_display(prefix="selas")` — exactement
    # le code que le sous-formulaire de cession SELAS appelle pour poser la situation
    # du cedant — puis on rend l'acte avec le VRAI generateur et on asserte le libelle
    # accentue + accorde au genre (2 regimes), et l'absence de « marie sous » nu.
    from sydel_doc_engine.front_app import shell

    # Le helper lit la valeur collapsee du praticien (genre + statut) ET le libelle BRUT
    # du preset depuis st.session_state[f"{prefix}_situation_maritale"]. On pose un st
    # minimal porteur de cette cle (comme le ferait le menu SELAS de l'associe vendeur).
    class _FakeSt:
        def __init__(self) -> None:
            self.session_state = {"selas_situation_maritale": preset_brut}

    monkeypatch.setattr(shell, "st", _FakeSt())
    praticien = {"situation_maritale": "marie", "genre": genre}
    situation_complete = shell._scm_cedant_situation_maritale_display(
        praticien, prefix="selas"
    )
    assert situation_complete == attendu_regime  # garde sur la valeur produite par le slice

    ctx = _base_context("SELAS")
    ctx.scm_cession.cedant.situation_maritale = situation_complete
    acte = ActeCessionPartsScmGenerator().generate(ctx, tmp_path)
    acte_text = _docx_text(acte)
    # Le libelle complet accentue (« <regime> avec <conjoint> ») ressort dans le DOCX.
    assert f"{attendu_regime} avec Madame Claire Dupont" in acte_text
    # Aucune fuite de « marie sous » non accentue.
    assert "marie sous" not in acte_text
    _assert_clean(acte_text)


def test_mois_tables_accentuees_identiques() -> None:
    # La dette de duplication (tables de mois identiques) est résorbée : la table accentuée est
    # centralisée dans utils.months.FRENCH_MONTHS et importée par field_derivations /
    # cession_cabinets_common. Ce test garde la garantie d'accentuation (LIVE-03) et vérifie que
    # les modules pointent bien sur la table centralisée (plus aucune copie locale susceptible de
    # dériver). NB : autorisation_domiciliation n'utilise plus FRENCH_MONTHS depuis la propagation
    # des dates satellites en JJ/MM/AAAA (Gad 2026-06-29) — retiré de l'assertion.
    from sydel_doc_engine.front_app import field_derivations
    from sydel_doc_engine.generators.lot_03 import cession_cabinets_common
    from sydel_doc_engine.utils.months import FRENCH_MONTHS

    assert (
        field_derivations.FRENCH_MONTHS
        is cession_cabinets_common.FRENCH_MONTHS
        is FRENCH_MONTHS
    )
    assert "février" in FRENCH_MONTHS and "août" in FRENCH_MONTHS and "décembre" in FRENCH_MONTHS


def test_scm_cession_fixture_pas_de_mois_non_accentue() -> None:
    # LIVE-03 (onglet 24) : les mois sont accentués en SORTIE. La fixture de PRODUCTION
    # scm_cession_fixture() — chargée telle quelle par le shell SELAS (shell.py:957) et
    # émise verbatim dans le PV — ne doit contenir AUCUN mois non accentué. Le test
    # existant ci-dessus reconstruit un contexte accentué et masquait donc le défaut.
    from sydel_doc_engine.scenarios.selarl import scm_cession_fixture

    blob = str(scm_cession_fixture().model_dump()).casefold()
    for non_accentue in ("aout", "fevrier", "decembre"):
        assert non_accentue not in blob, f"LIVE-03 : « {non_accentue} » non accentué"


def test_orchestrator_selects_scm_cession_block_only_when_enabled() -> None:
    orchestrator = DocumentOrchestrator(build_seed_catalog())
    enabled = orchestrator.select_documents_for_context(_base_context("SELARL"))
    enabled_ids = [document.doc_id for document in enabled]

    disabled_ctx = _base_context("SELARL")
    disabled_ctx.dossier_options = DossierOptions(scm_cession=False)
    disabled = orchestrator.select_documents_for_context(disabled_ctx)
    disabled_ids = [document.doc_id for document in disabled]

    assert {"DOC-031", "DOC-032", "DOC-033"}.issubset(enabled_ids)
    assert {"DOC-031", "DOC-032", "DOC-033"}.isdisjoint(disabled_ids)


def test_pv_blocks_incoherent_parts_after_cession(tmp_path: Path) -> None:
    ctx = _base_context("SELARL")
    ctx.scm_cession.associes_apres_cession[0].parts.nb = 99

    with pytest.raises(ValueError, match="totaliser"):
        PvAgeCessionScmGenerator().generate(ctx, tmp_path)


def test_pv_blocks_incoherent_apres_cession_roster(tmp_path: Path) -> None:
    # §4.1 : le nombre d'associes apres-cession n'est plus fige (4). Retirer un
    # associe casse desormais la COHERENCE des parts (somme != nb_parts_total),
    # qui reste l'invariant bloquant. Le PV refuse toujours un roster incoherent.
    ctx = _base_context("SELARL")
    ctx.scm_cession.associes_apres_cession.pop()

    with pytest.raises(ValueError, match="totaliser"):
        PvAgeCessionScmGenerator().generate(ctx, tmp_path)


def test_pv_accepts_two_associes_presents_coherent(tmp_path: Path) -> None:
    # §4.1 : roster de N associes accepte tant que les parts totalisent le capital.
    # Ici 2 presents (60 + 40 = 100) ; apres-cession = cedant reduit (40) +
    # SEL acquereur entrante (60), total 100. Plus de fixture 3/4 figee.
    ctx = _base_context("SELARL")
    scm = ctx.scm_cession
    scm.scm_cedee.nb_parts_total = 100
    scm.associes_presents = [
        ScmCessionAssocie(
            civilite_affichage="Monsieur", prenom="Paul", nom="Bernard",
            parts=ScmCessionPartsAttribution(nb=40, plage="1 a 40"),
        ),
        ScmCessionAssocie(
            civilite_affichage="Monsieur", prenom="Jean", nom="Dupont",
            parts=ScmCessionPartsAttribution(nb=60, plage="41 a 100"),
        ),
    ]
    scm.associes_apres_cession = [
        ScmCessionAssocie(
            civilite_affichage="Monsieur", prenom="Paul", nom="Bernard",
            parts=ScmCessionPartsAttribution(nb=40, plage="1 a 40"),
        ),
        ScmCessionAssocie(
            civilite_affichage="Monsieur", prenom="Jean", nom="Dupont",
            parts=ScmCessionPartsAttribution(nb=40, plage="41 a 80"),
        ),
        ScmCessionAssocie(
            type_personne="personne_morale", denomination="SELARL CABINET DUPONT",
            forme_juridique="SELARL",
            parts=ScmCessionPartsAttribution(nb=20, plage="81 a 100"),
        ),
    ]
    scm.signataires_pv = ["M. Paul Bernard", "M. Jean Dupont"]

    path = PvAgeCessionScmGenerator().generate(ctx, tmp_path)
    assert path.exists()
    text = _docx_text(path)
    assert "Paul Bernard" in text
    assert "Jean Dupont" in text
    # Le dernier present (Jean Dupont) preside la seance.
    assert "préside la séance" in text


def test_acte_blocks_incomplete_credit_vendeur(tmp_path: Path) -> None:
    ctx = _base_context("SELAS")
    ctx.scm_cession.credit_vendeur = ScmCessionCreditVendeur(
        actif=True,
        montant="1 000",
        duree="2 ans",
        taux=None,
        majoration_interet_retard="4 points",
    )

    # R10 (Rafael 2026-06-24) : donnee manquante (credit_vendeur.taux) ne bloque plus -> marqueur
    # « (À COMPLÉTER : ...) » visible dans l'acte (sans crochets), generation reussie.
    text = _docx_text(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    assert "COMPLÉTER" in text and "credit_vendeur.taux" in text


def test_pv_age_renders_hyphen_bullets_on_two_lists(tmp_path: Path) -> None:
    # Retour UAT Rafael (DOC-031) : les 2 listes (documents deposes + ordre du
    # jour) doivent etre rendues en puces tiret « - ... », texte inchange.
    ctx = _base_context("SELARL")
    document = Document(PvAgeCessionScmGenerator().generate(ctx, tmp_path))
    para_texts = [p.text for p in document.paragraphs]

    # Liste A (documents deposes) : chaque item prefixe d'un tiret.
    assert "- Les copies des convocations des associés ;" in para_texts
    assert "- Un exemplaire du compromis de cession des parts sociales ;" in para_texts
    assert "- Le rapport de la gérance ;" in para_texts
    assert "- Le texte des résolutions proposées." in para_texts
    # Liste B (ordre du jour) : chaque item prefixe d'un tiret.
    assert "- Lecture du rapport de la gérance ;" in para_texts
    assert "- Agrément d'un nouvel associé, la SELARL CABINET DUPONT ;" in para_texts
    assert "- Modification corrélative des statuts." in para_texts
    # Garde-fou : les phrases hors liste ne sont PAS transformees en puces.
    assert (
        "Le Président dépose et met à la disposition des associés les documents suivants :"
        in para_texts
    )


def test_pv_age_adoption_lines_italic_and_signature_frame_enlarged(tmp_path: Path) -> None:
    # §4.2 — (a) « Cette résolution est adoptée à l'unanimité. » en italique
    # (3 occurrences, point final harmonisé) ; (b) cadre de signature agrandi
    # (hauteur de ligne minimale) tout en conservant les bordures.
    from docx.enum.table import WD_ROW_HEIGHT_RULE
    from docx.shared import Cm

    ctx = _base_context("SELARL")
    document = Document(PvAgeCessionScmGenerator().generate(ctx, tmp_path))

    adoption = [
        p
        for p in document.paragraphs
        if p.text == "Cette résolution est adoptée à l'unanimité."
    ]
    assert len(adoption) == 3
    for paragraph in adoption:
        assert paragraph.runs[0].italic is True

    # le cadre de signature (derniere table) garde des bordures explicites...
    signature_table = document.tables[-1]
    assert _table_has_borders(signature_table)
    # ...et est agrandi via une hauteur de ligne minimale (>= ~2,5 cm).
    for row in signature_table.rows:
        assert row.height_rule == WD_ROW_HEIGHT_RULE.AT_LEAST
        assert row.height >= Cm(2.4)


def test_pv_age_president_derived_from_last_present_associe(tmp_path: Path) -> None:
    # §4.1 — le president de seance est derive du DERNIER associe present (gerant
    # associe), pas d'un index fixe « [2] ». On renomme le dernier present et on
    # verifie qu'il preside, sans index code en dur.
    ctx = _base_context("SELARL")
    ctx.scm_cession.associes_presents[-1] = _associe("Sophie Leroy", 100, "201 à 300")
    text = _docx_text(PvAgeCessionScmGenerator().generate(ctx, tmp_path))

    assert "Sophie Leroy préside la séance en qualité de gérant associé" in text
    assert "Anne Martin préside la séance" not in text


def test_pv_age_uses_real_scm_data_not_fixture_capital(tmp_path: Path) -> None:
    # §4.1 — capital / parts / nominal / plage du PV proviennent du contexte
    # (donc de la saisie front), pas d'une valeur figee. On change le capital et
    # le nb de parts et on verifie qu'ils s'impriment.
    ctx = _base_context("SELARL")
    ctx.scm_cession.scm_cedee.capital_social = "4 500"
    ctx.scm_cession.scm_cedee.valeur_nominale_part = "15"
    text = _docx_text(PvAgeCessionScmGenerator().generate(ctx, tmp_path))

    # entete centre (« Au capital de … € ») + corps (« au capital de … euros »)
    assert "Au capital de 4 500 €" in text
    assert "au capital de 4 500 euros" in text
    assert "15 euros chacune" in text
    assert "3 000" not in text


def _table_has_borders(table) -> bool:
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.find(
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tblBorders"
    )
    if borders is None:
        return False
    top = borders.find(
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}top"
    )
    return top is not None and top.get(
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"
    ) == "single"


def test_courrier_sde_objet_bold_underline_and_signataire_right(tmp_path: Path) -> None:
    # Retour UAT Rafael (DOC-032) : objet en gras + souligne, signataire a droite.
    ctx = _base_context("SELARL")
    document = Document(CourrierSdeCessionScmGenerator().generate(ctx, tmp_path))

    objet = next(p for p in document.paragraphs if p.text.startswith("Objet :"))
    assert objet.runs[0].bold is True
    assert objet.runs[0].underline is True

    # §8.4a — signataire FIXE SYDEL « Clémence ROUSSEL », aligne a droite.
    signataire = next(p for p in document.paragraphs if p.text == "Clémence ROUSSEL")
    assert signataire.alignment == WD_ALIGN_PARAGRAPH.RIGHT
    assert "Sarah Durand" not in "\n".join(p.text for p in document.paragraphs)


def test_courrier_sde_montant_droits_fixe_25_sans_couleur(tmp_path: Path) -> None:
    # §8.3 — montant FIXE « 25 ». R22b-01 (Rafael 2026-06-22) : plus de rouge.
    ctx = _base_context("SELARL")
    document = Document(CourrierSdeCessionScmGenerator().generate(ctx, tmp_path))

    paragraph = next(p for p in document.paragraphs if "chèque de 25 euros" in p.text)
    montant_run = next(r for r in paragraph.runs if r.text.strip() == "25")
    assert montant_run.font.color.rgb is None
    # le montant n'est PAS une variable saisie (« 150 » de la fixture absent).
    assert "150" not in "\n".join(p.text for p in document.paragraphs)


def test_courrier_sde_scm_name_sans_surlignage(tmp_path: Path) -> None:
    # §8.2 — nom de la SCM dans le corps. R22b-01 : plus de surlignage jaune.
    # Albane 2026-06-26 §C2 : le corps dit « de parts de la Société {denom} » (plus de doublon).
    ctx = _base_context("SELARL")
    document = Document(CourrierSdeCessionScmGenerator().generate(ctx, tmp_path))

    paragraph = next(
        p for p in document.paragraphs if "de parts de la Société" in p.text
    )
    name_run = next(r for r in paragraph.runs if r.text == "SCM CABINET CENTRAL")
    assert name_run.font.highlight_color is None


def test_courrier_sde_footer_contains_sydel_coordinates(tmp_path: Path) -> None:
    # §8.4b — pied de page coordonnees SYDEL pour contact par le SDE.
    ctx = _base_context("SELARL")
    document = Document(CourrierSdeCessionScmGenerator().generate(ctx, tmp_path))

    footer_text = "\n".join(p.text for p in document.sections[0].footer.paragraphs)
    # Verbatim du modele client : espaces insecables (\xa0) preserves avant les « : ».
    assert "80 avenue Marceau, 75008 PARIS" in footer_text
    assert "Tél\xa0: 01 53 81 43 03" in footer_text
    assert "RCS Paris\xa0: 788\xa0531\xa0432 00029" in footer_text
    assert "ORIAS N°12069007" in footer_text


def test_courrier_sde_destinataire_block_for_selarl_with_placeholders(tmp_path: Path) -> None:
    # §8.1 — quand la saisie ne fournit pas les lignes service/adresse, le bloc
    # destinataire reste rendu avec des champs « à compléter » SANS surlignage (R22b-01).
    ctx = _base_context("SELARL")
    ctx.scm_cession.enregistrement = ScmCessionEnregistrement()
    document = Document(CourrierSdeCessionScmGenerator().generate(ctx, tmp_path))

    texts = [p.text for p in document.paragraphs]
    assert "Service départemental de l'enregistrement de" in texts
    fillable = [p for p in document.paragraphs if "à compléter" in p.text]
    assert len(fillable) == 4
    # R22b-01 : aucun surlignage sur ces champs.
    assert all(all(r.font.highlight_color is None for r in p.runs) for p in fillable)


# ==========================================================================
# Albane 2026-06-26 — LOT acte de cession de parts SCM (S1..S12).
# Tests ADVERSARIAUX : verifient le DEFAUT corrige (pas seulement la presence),
# avec preuve de non-regression SELARL pour les correctifs partages.
# ==========================================================================


def test_s1_cessionnaire_overrides_selas_forme(tmp_path: Path) -> None:
    # S1 : « la SELAS il y a écrit ... SELARL au lieu de SELAS ». Le helper front qui
    # decrit la SEL cessionnaire DOIT poser forme_juridique='SELAS' en prefix='selas',
    # et NE PAS la poser en prefix='selarl' (le generateur force 'SELARL', gold intact).
    from sydel_doc_engine.front_app.shell import _scm_cessionnaire_overrides

    societe = {"denomination": "SELAS X", "capital_social": "1 000", "ville_rcs": "Lyon"}
    sel = _scm_cessionnaire_overrides(societe, prefix="selas")
    assert sel["forme_juridique"] == "SELAS"
    selarl = _scm_cessionnaire_overrides(societe, prefix="selarl")
    assert "forme_juridique" not in selarl  # SELARL force 'SELARL' cote generateur


def test_s1_acte_selas_forme_et_president(tmp_path: Path) -> None:
    # S1 (bout-en-bout) : en contexte SELAS, l'acte imprime « SELAS au capital de … » et
    # « Représentée par son président » — JAMAIS « SELARL » / « gérant » pour le cessionnaire.
    ctx = _base_context("SELAS")
    text = _docx_text(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    assert "SELAS au capital de 10 000" in text
    assert "Représentée par son président" in text
    # Pas de forme/fonction SELARL dans la description du cessionnaire (le mot « gérance »
    # de la SCM apparait ailleurs ; on cible la ligne de representation du cessionnaire).
    assert "Représentée par son gérant" not in text


def test_s1_acte_selarl_forme_et_gerant_non_regression(tmp_path: Path) -> None:
    # S1 NON-REGRESSION : en SELARL, l'acte garde « SELARL au capital de … € » et
    # « Représentée par son gérant ». Le code partage SELARL/SELAS via ctx.structure.
    ctx = _base_context("SELARL")
    text = _docx_text(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    assert "SELARL au capital de 10 000 €" in text
    assert "Représentée par son gérant" in text
    assert "Représentée par son président" not in text


def test_s2_prix_unitaire_recalcule_global_sur_nb() -> None:
    # S2 : « si j'ai cédé 20 parts pour 20€ ... la part cédée vaut un (1) euro et non 100 € ».
    # Le prix unitaire DOIT etre derive = global / nb (chiffre + lettres), pas fige.
    from sydel_doc_engine.front_app.shell import _derive_scm_prix_unitaire

    prix = {"global": "20", "unitaire": "100", "unitaire_lettres": "cent"}
    _derive_scm_prix_unitaire(prix, 20)
    assert prix["unitaire"] == "1"
    assert prix["unitaire_lettres"] == "un"

    # 5 000 / 50 = 100 (cas SELARL, byte-identique au gold).
    prix2 = {"global": "5 000", "unitaire": "x", "unitaire_lettres": "x"}
    _derive_scm_prix_unitaire(prix2, 50)
    assert prix2["unitaire"] == "100" and prix2["unitaire_lettres"] == "cent"

    # Non divisible : figure decimale francaise, jamais de crash.
    prix3 = {"global": "10", "unitaire": "x", "unitaire_lettres": "x"}
    _derive_scm_prix_unitaire(prix3, 4)
    assert prix3["unitaire"] == "2,5"
    # Akainu m1 2026-07-06 : le slot LETTRES d'un prix decimal garde la FIGURE (jamais la
    # phrase monetaire « deux euros et cinquante centimes » -> double euro dans l'acte).
    assert prix3["unitaire_lettres"] == "2,5"

    # Donnees absentes / nb == 0 : on ne touche a rien (pas de crash, pas de cle videe).
    prix4 = {"global": "", "unitaire": "100", "unitaire_lettres": "cent"}
    _derive_scm_prix_unitaire(prix4, 0)
    assert prix4["unitaire"] == "100"


def test_s2_acte_prix_unitaire_un_euro(tmp_path: Path) -> None:
    # S2 (bout-en-bout) : un acte avec prix unitaire « 1 » imprime « un (1) ... par part cédée ».
    ctx = _base_context("SELAS")
    ctx.scm_cession.prix = ScmCessionPrix(
        unitaire="1", unitaire_lettres="un", global_="20", global_lettres="vingt"
    )
    text = _docx_text(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    assert "un (1)" in text and "par part cédée" in text
    assert "cent (100)" not in text


def test_s3_acte_quatre_exemplaires(tmp_path: Path) -> None:
    # S3 : « le nombre d'exemplaires c'est quatre et non trois pour cet acte ».
    ctx = _base_context("SELARL")
    text = _docx_text(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    assert "En quatre exemplaires originaux," in text
    assert "trois exemplaires" not in text


def test_s4_plage_cedee_coherente_avec_nb() -> None:
    # S4 : « les numéros de parts ne correspondent pas à la somme de mes parts (20 cédées,
    # numérotées de 151 à 200) » — 151..200 = 50, incoherent. Avec la plage EFFACEE en amont
    # (forcage front), la derivation produit une plage COHERENTE avec le nb (20 dernieres parts).
    from sydel_doc_engine.front_app.shell import _derive_scm_apres_cession

    presents = [_associe("Jean Dupont", 100, "101 à 200")]
    cedant = {"prenom": "Jean", "nom": "Dupont", "civilite_affichage": "Monsieur"}
    cessionnaire = {"denomination": "SELAS X", "forme_juridique": "SELAS"}
    parts_cedees: dict[str, object] = {"nb": 20}  # plage NON fournie (effacee par le front)
    _derive_scm_apres_cession(presents, cedant, cessionnaire, parts_cedees)
    # 20 dernieres parts de [101..200] = [181..200] (20 parts), pas 151..200 (50 parts).
    # N4 (2026-07-01) : plage avec « à » accentue.
    assert parts_cedees["plage"] == "181 à 200"
    debut, fin = (int(x) for x in parts_cedees["plage"].split(" à "))
    assert fin - debut + 1 == 20  # plage <=> nb cede


def test_s6_cadre_contient_denomination_scm(tmp_path: Path) -> None:
    # S6 : « mettre dans le cadre sur une 3e ligne le nom de la SCM ... ».
    ctx = _base_context("SELARL")
    document = Document(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    cadre = document.tables[0].cell(0, 0).text
    assert "SCM CABINET CENTRAL" in cadre
    assert cadre.splitlines() == [
        "CESSION DES PARTS",
        "DE LA SOCIETE CIVILE DE MOYENS",
        "SCM CABINET CENTRAL",
    ]


def test_s7_party_markers_droite_et_gras(tmp_path: Path) -> None:
    # S7 : « soussigné de première part » / « soussigné de seconde part » / « ci après dénommé
    # La Société » alignes a DROITE et en GRAS.
    ctx = _base_context("SELARL")
    document = Document(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    markers = [
        p
        for p in document.paragraphs
        if p.text.startswith(("Soussigné de première", "Soussignée de seconde"))
        or p.text == "Ci-après dénommé « LA SOCIETE »,"
    ]
    assert len(markers) == 3
    for paragraph in markers:
        assert paragraph.alignment == WD_ALIGN_PARAGRAPH.RIGHT
        assert paragraph.runs and paragraph.runs[0].bold is True


def test_s8_cedant_civilite_majuscule(tmp_path: Path) -> None:
    # S8 : « pour le soussigné 1 que monsieur soit avec une majuscule au début ».
    ctx = _base_context("SELARL")
    ctx.scm_cession.cedant.civilite_affichage = "monsieur"  # saisie en minuscule
    text = _docx_text(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    assert "Monsieur Jean Dupont" in text
    assert "monsieur Jean Dupont" not in text


def test_s9_date_naissance_jour_deux_chiffres(tmp_path: Path) -> None:
    # S9 : « pareil sur la date de naissance (01 non 1) ».
    ctx = _base_context("SELARL")
    ctx.scm_cession.cedant.date_naissance = "1/1/1980"  # saisie texte jour 1 chiffre
    text = _docx_text(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    assert "né le 01/01/1980" in text
    assert "né le 1/1/1980" not in text


def test_s11_origine_propriete_commence_par_majuscule(tmp_path: Path) -> None:
    # S11 : « Origine de propriété ... la civilité il faudrait une majuscule en début de phrase ».
    ctx = _base_context("SELARL")
    ctx.scm_cession.cedant.civilite_affichage = "monsieur"
    document = Document(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    origine = next(p for p in document.paragraphs if "le CEDANT, déclare" in p.text)
    assert origine.text[0].isupper()
    assert origine.text.startswith("Monsieur ")


def test_s12_signatures_cote_a_cote(tmp_path: Path) -> None:
    # S12 : « pour les signatures il faudrait soit les mettre côte à côte soit avec plus
    # d'espace ». On rend une table 2 colonnes (cedant | cessionnaire) cote a cote.
    ctx = _base_context("SELARL")
    document = Document(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    signature_table = document.tables[-1]
    assert len(signature_table.columns) == 2
    assert signature_table.cell(0, 0).text.startswith("Le cédant")
    assert signature_table.cell(0, 1).text.startswith("Le cessionnaire")
    assert "Jean Dupont" in signature_table.cell(1, 0).text
    assert "CABINET DUPONT" in signature_table.cell(1, 1).text


def test_s10_section_headings_have_space_after(tmp_path: Path) -> None:
    # S10 : « Mettre des espaces après chaque titre ». Les headings de section de l'acte
    # portent un space_after explicite (> 0) pour aerer sous le titre.
    from docx.shared import Pt

    ctx = _base_context("SELARL")
    document = Document(ActeCessionPartsScmGenerator().generate(ctx, tmp_path))
    prix_heading = next(p for p in document.paragraphs if p.text == "PRIX")
    assert prix_heading.paragraph_format.space_after is not None
    assert prix_heading.paragraph_format.space_after >= Pt(10)


def test_accord_euro_M1_singulier_si_un() -> None:
    # M1 (Akainu 2026-06-26) : « euro » au singulier quand le prix unitaire vaut 1
    # (verbatim Albane « la part cédée vaut un (1) euro »), « euros » sinon.
    from sydel_doc_engine.generators.lot_05.acte_cession_parts_scm import _accord_euro

    assert _accord_euro("1") == "euro"
    assert _accord_euro("1,00") == "euro"
    assert _accord_euro("100") == "euros"
    assert _accord_euro("10") == "euros"  # surtout pas confondre avec 1
    assert _accord_euro("33,33") == "euros"


def test_derive_scm_prix_unitaire_M2_arrondi_centime() -> None:
    # M2 (Akainu 2026-06-26) : prix unitaire = global/nb arrondi au CENTIME (pas 28
    # décimales brutes) ; divisible exact -> entier propre.
    from sydel_doc_engine.front_app.shell import _derive_scm_prix_unitaire

    p = {"global": "100"}
    _derive_scm_prix_unitaire(p, 3)
    assert p["unitaire"] == "33,33"  # 2 décimales, jamais 33,33333...

    p2 = {"global": "20"}
    _derive_scm_prix_unitaire(p2, 20)
    assert p2["unitaire"] == "1"
    assert p2["unitaire_lettres"] == "un"


# ==========================================================================
# Albane 2026-06-26 — LOT « PV AGE cession SCM + courrier SDE » (P2..P7, C1..C3).
# Tests ADVERSARIAUX : verifient le DEFAUT corrige, avec preuve de
# non-regression SELARL pour les correctifs partages.
# ==========================================================================


def test_p4_premiere_resolution_autorise_cession_sans_delai_selas(tmp_path: Path) -> None:
    # P4 : « ajouter ... "et par conséquent, autorise la cession de XX parts sociales de
    # Monsieur XXX à la SEL XX" » + remplacer « dans un délai de 3 mois à compter de ce jour
    # soit jusqu'au {date} » par « à compter de ce jour ». Le verbatim s'applique a la 1re
    # resolution -> on l'exerce sur SELAS (ou l'ancien wording « delai » existait).
    ctx = _base_context("SELAS")
    text = _docx_text(PvAgeCessionScmGenerator().generate(ctx, tmp_path))
    assert "dans un délai de" not in text  # plus aucun delai de 3 mois
    assert "soit jusqu'au" not in text
    assert (
        "autorise la cession de 50 parts sociales de Monsieur Jean Dupont "
        "à la SELAS CABINET DUPONT" in text
    )
    assert "à compter de ce jour" in text


def test_p4_premiere_resolution_autorise_cession_selarl(tmp_path: Path) -> None:
    # P4 NON-REGRESSION SELARL : meme clause « autorise la cession » + « à compter de ce jour ».
    ctx = _base_context("SELARL")
    text = _docx_text(PvAgeCessionScmGenerator().generate(ctx, tmp_path))
    assert "dans un délai de" not in text
    assert (
        "autorise la cession de 50 parts sociales de Monsieur Jean Dupont "
        "à la SELARL CABINET DUPONT" in text
    )


def test_p5_deuxieme_resolution_sans_sous_reserve_et_a_compter(tmp_path: Path) -> None:
    # P5 : (a) SUPPRIMER « et sous réserve de la réalisation définitive de la cession, » ;
    # (c) ajouter « à compter de ce jour » a la formule d'entree en vigueur.
    ctx = _base_context("SELARL")
    text = _docx_text(PvAgeCessionScmGenerator().generate(ctx, tmp_path))
    assert "sous réserve de la réalisation définitive" not in text
    deuxieme = next(
        line
        for line in text.splitlines()
        if "compte tenu de la résolution qui précède" in line
    )
    assert "des statuts qui sera rédigé ainsi, à compter de ce jour :" in deuxieme


def test_p5_numero_article_surligne(tmp_path: Path) -> None:
    # P5 (b) : le numero d'article modifie est SURLIGNE (champ variable a adapter).
    from docx.enum.text import WD_COLOR_INDEX

    ctx = _base_context("SELARL")
    document = Document(PvAgeCessionScmGenerator().generate(ctx, tmp_path))
    para = next(
        p
        for p in document.paragraphs
        if "compte tenu de la résolution qui précède" in p.text
    )
    article_run = next(r for r in para.runs if r.text.strip() == "7")
    assert article_run.font.highlight_color == WD_COLOR_INDEX.YELLOW
    # le reste du paragraphe n'est PAS surligne.
    for run in para.runs:
        if run.text.strip() != "7":
            assert run.font.highlight_color is None


def test_p3a_president_femme_gerante_associee(tmp_path: Path) -> None:
    # P3a : « il faudrait pouvoir le féminiser pour que ce soit gérante associée ». Quand le
    # president de seance (dernier present) est une femme -> « gérante associée ».
    ctx = _base_context("SELARL")
    ctx.scm_cession.associes_presents[-1] = ScmCessionAssocie(
        civilite_affichage="Madame",
        prenom="Sophie",
        nom="Leroy",
        parts=ScmCessionPartsAttribution(nb=100, plage="201 à 300"),
    )
    text = _docx_text(PvAgeCessionScmGenerator().generate(ctx, tmp_path))
    assert "Sophie Leroy préside la séance en qualité de gérante associée" in text
    assert "gérant associé." not in text


def test_p3a_president_homme_gerant_associe(tmp_path: Path) -> None:
    # P3a CONTRE-EPREUVE : un president homme reste « gérant associé » (accord au sexe).
    ctx = _base_context("SELARL")
    ctx.scm_cession.associes_presents[-1] = ScmCessionAssocie(
        civilite_affichage="Monsieur",
        prenom="Marc",
        nom="Petit",
        parts=ScmCessionPartsAttribution(nb=100, plage="201 à 300"),
    )
    text = _docx_text(PvAgeCessionScmGenerator().generate(ctx, tmp_path))
    assert "Marc Petit préside la séance en qualité de gérant associé" in text
    assert "gérante associée" not in text


def test_p6_a_concurrence_sur_meme_ligne(tmp_path: Path) -> None:
    # P6 : « "à concurrence de" ne doit pas être sur la ligne du dessous, mais à la suite de
    # l'associé ». Chaque ligne de repartition fusionne l'associe + « à concurrence de ... ».
    ctx = _base_context("SELARL")
    document = Document(PvAgeCessionScmGenerator().generate(ctx, tmp_path))
    para_texts = [p.text for p in document.paragraphs]
    # l'associe et « à concurrence de » sont sur la MEME ligne.
    assert "à Monsieur Paul Bernard, à concurrence de 100 parts," in para_texts
    assert "à Monsieur Jean Dupont, à concurrence de 50 parts," in para_texts
    # plus aucune ligne isolee « à concurrence de ... » (retour a la ligne supprime).
    assert not any(p.strip().startswith("à concurrence de") for p in para_texts)


def test_p7_signature_tous_associes_pas_gerance(tmp_path: Path) -> None:
    # P7 : « mettre que c'est signé par tous les associés (enlever la gérance) ». La formule
    # finale ne mentionne plus « la gérance » ; le cadre de signature liste les associes.
    ctx = _base_context("SELARL")
    document = Document(PvAgeCessionScmGenerator().generate(ctx, tmp_path))
    para_texts = [p.text for p in document.paragraphs]
    closing = next(p for p in para_texts if "a été signé" in p)
    assert closing == (
        "De tout ceci, il a été dressé le présent procès-verbal qui, après lecture, "
        "a été signé par tous les associés présents."
    )
    assert "signé par la gérance" not in closing
    # le cadre de signature (derniere table) liste les associes (signataires_pv),
    # pas « la gérance ».
    signature_cells = [
        cell.text
        for row in document.tables[-1].rows
        for cell in row.cells
    ]
    signature_blob = "\n".join(signature_cells)
    assert "Jean Dupont" in signature_blob
    assert "Paul Bernard" in signature_blob
    assert "Anne Martin" in signature_blob
    assert "la gérance" not in signature_blob.casefold()
    assert "gérant" not in signature_blob.casefold()


def test_p2_paragraphes_aeres(tmp_path: Path) -> None:
    # P2 : « mettre de l'espace entre les paragraphes ». Les paragraphes de corps du PV
    # portent un space_after superieur au standard (6 pt).
    from docx.shared import Pt

    ctx = _base_context("SELARL")
    document = Document(PvAgeCessionScmGenerator().generate(ctx, tmp_path))
    corps = next(p for p in document.paragraphs if p.text.startswith("L'an "))
    assert corps.paragraph_format.space_after > Pt(6)


def test_c1_entete_destinataire_retrait_12cm(tmp_path: Path) -> None:
    # C1 : « les 5 premières lignes ... aligné à gauche mais qui démarre vers le cm 12 ».
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm

    ctx = _base_context("SELARL")
    document = Document(CourrierSdeCessionScmGenerator().generate(ctx, tmp_path))
    entete = [
        p
        for p in document.paragraphs
        if p.text
        and (
            p.text.startswith("Service départemental")
            or p.text.startswith("SERVICE DEPARTEMENTAL")
            or p.text.startswith("Centre des finances")
            or p.text.startswith("6 rue Paganini")
            or p.text.startswith("75020 Paris")
        )
    ]
    assert len(entete) == 5
    for paragraph in entete:
        assert paragraph.alignment in (WD_ALIGN_PARAGRAPH.LEFT, None)
        indent = paragraph.paragraph_format.left_indent
        assert indent is not None and indent >= Cm(11.5)


def test_c2_societe_sans_doublon_scm(tmp_path: Path) -> None:
    # C2 : « il y a une répétition de la SCM ; mettre "de la Société {dénomination}" ».
    ctx = _base_context("SELARL")
    text = _docx_text(CourrierSdeCessionScmGenerator().generate(ctx, tmp_path))
    assert "de parts de la Société SCM CABINET CENTRAL" in text
    assert "SCM SCM CABINET CENTRAL" not in text  # doublon elimine


def test_c3_objet_corps_plus_bas(tmp_path: Path) -> None:
    # C3 : « mettre de l'espace pour que l'objet et le début du courrier commencent plus bas ».
    from docx.shared import Pt

    ctx = _base_context("SELARL")
    document = Document(CourrierSdeCessionScmGenerator().generate(ctx, tmp_path))
    objet = next(p for p in document.paragraphs if p.text.startswith("Objet :"))
    assert objet.paragraph_format.space_before is not None
    assert objet.paragraph_format.space_before >= Pt(12)
