from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    RegimeCommunautaireAssocie,
    StatutsCivilsApport,
    StatutsCivilsAssocie,
    StatutsCivilsParts,
    StatutsCivilsRepresentant,
)
from sydel_doc_engine.front_app import (
    civil_statuts_slice as css,
)
from sydel_doc_engine.front_app import (
    sas_slice,
    selas_multi_slice,
    spfpl_slice,
)
from sydel_doc_engine.front_app.dossier_selection import (
    dossier_type_by_label,
    dossier_type_labels,
)
from sydel_doc_engine.front_app.type_registry import registered_types


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(p.text for p in cell.paragraphs if p.text)
    for section in document.sections:
        texts.extend(p.text for p in section.footer.paragraphs if p.text)
    return "\n".join(texts)


def _assert_clean(text: str) -> None:
    assert "[" not in text
    assert "]" not in text


# --- Registre + deroulante ----------------------------------------------------


def test_registry_exposes_all_ready_types() -> None:
    labels = dossier_type_labels()
    assert labels[0] == "SELARL creation V1"  # SELARL TOUJOURS en premier (defaut)
    structures = {item.structure for item in registered_types()}
    assert {
        "SELARL",
        "SCM",
        "SCI",
        "SCI IRIS",
        "SCS",
        "SAS",
        "SPFPL cession",
        "SPFPL apport",
        "SELAS",
        "SELAS uni medecin",
    } == structures


def test_selarl_option_unchanged() -> None:
    option = dossier_type_by_label("SELARL creation V1")
    assert option.key == "selarl_v1"
    assert option.structure == "SELARL"
    assert option.generation_enabled is True
    assert option.slice_module is None  # chemin historique dedie


# --- Helpers de construction d'associes civils --------------------------------


def _pp(prenom, nom, nb, debut, fin, apport, role=None, prof="chirurgien-dentiste"):
    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        role_statutaire=role,
        genre=Gender.MASCULIN,
        civilite_affichage="Monsieur",
        prenom=prenom,
        prenoms=prenom,
        nom=nom,
        profession=prof,
        date_naissance="1 janvier 1980",
        ville_naissance="Paris",
        departement_naissance="75",
        nationalite="francaise",
        situation_maritale="celibataire",
        adresse_personnelle_affichee="1 rue Exemple, 75000 Paris",
        apport=StatutsCivilsApport(montant=str(apport), montant_lettres=str(apport)),
        parts=StatutsCivilsParts(
            nb=nb,
            nb_lettres=str(nb),
            plage_affichee=f"{debut} a {fin}",
            debut=debut,
            fin=fin,
            qualite_associe=role,
        ),
    )


def _pm(nb, debut, fin, apport, prof="chirurgien-dentiste"):
    return StatutsCivilsAssocie(
        type_personne="personne_morale",
        denomination="SEL IRIS",
        forme_juridique="SELARL",
        profession=prof,
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
        apport=StatutsCivilsApport(montant=str(apport), montant_lettres=str(apport)),
        parts=StatutsCivilsParts(nb=nb, nb_lettres=str(nb), debut=debut, fin=fin),
    )


def _civil_base(structure, statuts_type, associes):
    payload = {
        "structure": structure,
        "statuts_type": statuts_type,
        "denomination": f"{structure} EXEMPLE",
        "forme_sociale": "societe civile",
        "capital_social": "1000",
        "nb_parts_total": 100,
        "valeur_nominale_part": "10",
        "duree_societe": "99",
        "siege_num": "10",
        "siege_voie": "rue de la Paix",
        "siege_cp": "75002",
        "siege_ville": "Paris",
        "ville_rcs": "Paris",
        "banque_nom": "BANQUE",
        "banque_adresse": "1 rue Banque, 75009 Paris",
        "date_cloture_premier_exercice": "31 decembre 2026",
        "signature_lieu": "Paris",
        "signature_date": date(2026, 5, 15),
        "associes": associes,
        # Documents communs (DNC / procuration / PV gerant) : signataire = 1er physique.
        "signataire_nom_pere": "Pierre Durand",
        "signataire_nom_mere": "Anne Durand",
        "signataire_adresse_num": "1",
        "signataire_adresse_voie": "rue Exemple",
        "signataire_adresse_cp": "75000",
        "signataire_adresse_ville": "Paris",
        "signataire_fonction": "gerant",
        "signataire_titre": "Docteur",
        "decision_date": date(2026, 5, 15),
    }
    if structure == "SCM":
        payload.update(
            {
                "ordre_conseil": "Conseil departemental",
                "ordre_departement": "75",
                "ordre_adresse_ligne_1": "1 rue de l'Ordre",
                "ordre_cp": "75008",
                "ordre_ville": "Paris",
                "ordre_numero": "ORD-1",
                # Satellites SCM (pacte + liste depenses, generes a 2 associes).
                "pacte_ville_tribunal": "Paris",
                "societe_numero_rcs": "en cours de constitution",
            }
        )
    return payload


# --- Generation par type (smoke, 0 placeholder residuel) ----------------------


def _assert_bundle_clean(generated, expected_names) -> None:
    names = {p.name for p in generated.docx_paths}
    assert expected_names <= names
    for path in generated.docx_paths:
        _assert_clean(_docx_text(path))


# Tronc commun present dans CHAQUE bundle de creation.
_TRONC_DOCS = {
    "declaration_non_condamnation.docx",
    "autorisation_domiciliation.docx",
    "procuration.docx",
    "pv_nomination_gerant.docx",
}


def test_sci_slice_generates_clean(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCI",
        "sci",
        [_pp("Jean", "Durand", 40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-020", "DOC-001", "DOC-002", "DOC-003", "DOC-004")
    generated = css.generate_dossier(payload, tmp_path / "sci")
    _assert_bundle_clean(generated, _TRONC_DOCS | {"statuts_sci.docx"})


# Centre des impots requis par la lettre d'option IS (DOC-022) ; saisies utilisateur.
_OPTION_IS_INPUTS = {
    "option_is": True,
    "siren": "900 000 001",
    "impots_service": "SIE",
    "impots_centre": "Centre des Finances Publiques",
    "impots_adresse_ligne_1": "1 rue des Impots",
    "impots_adresse_ligne_2": "BP 100",
    "impots_cp": "75002",
    "impots_ville": "Paris",
}


def test_sci_option_is_off_keeps_base_bundle(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCI",
        "sci",
        [_pp("Jean", "Durand", 40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    payload["option_is"] = False
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert "DOC-022" not in plan.document_codes
    generated = css.generate_dossier(payload, tmp_path / "sci-is-off")
    names = {p.name for p in generated.docx_paths}
    assert "lettre_option_is.docx" not in names


def test_sci_option_is_on_adds_lettre_option_is(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCI",
        "sci",
        [_pp("Jean", "Durand", 40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    payload.update(_OPTION_IS_INPUTS)
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == (
        "DOC-020",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-022",
    )
    generated = css.generate_dossier(payload, tmp_path / "sci-is-on")
    _assert_bundle_clean(
        generated,
        _TRONC_DOCS | {"statuts_sci.docx", "lettre_option_is.docx"},
    )


def test_sci_iris_option_is_on_adds_lettre_option_is(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCI IRIS",
        "sci_iris",
        [_pm(40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    payload.update(_OPTION_IS_INPUTS)
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert "DOC-022" in plan.document_codes
    generated = css.generate_dossier(payload, tmp_path / "iris-is-on")
    _assert_bundle_clean(
        generated,
        _TRONC_DOCS | {"statuts_sci_iris.docx", "lettre_option_is.docx"},
    )


def test_sci_option_is_on_requires_centre_des_impots() -> None:
    payload = _civil_base(
        "SCI",
        "sci",
        [_pp("Jean", "Durand", 40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    payload["option_is"] = True  # toggle ON mais aucune saisie centre des impots
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is False
    assert any("option IS" in b for b in plan.blockers)


def test_scm_slice_generates_clean(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCM",
        "scm",
        [_pm(70, 1, 70, 700), _pp("Alice", "Martin", 30, 71, 100, 300)],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    # SCM a 2 associes : le bundle inclut les satellites pacte (DOC-026) + liste
    # des depenses communes (DOC-030), decision Rafael 2026-06-08.
    assert plan.document_codes == (
        "DOC-025",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-030",
        "DOC-026",
    )
    generated = css.generate_dossier(payload, tmp_path / "scm")
    _assert_bundle_clean(
        generated,
        _TRONC_DOCS
        | {
            "statuts_scm.docx",
            "demande_inscription_ordre.docx",
            "pacte_associes_scm.docx",
            "liste_depenses_communes_scm.docx",
        },
    )


# Documents inter-SEL (opt-in) : identite de la SEL de chaque associe + telephone +
# parametres du contrat de frais communs / reglement interieur. Personnes derivees des
# associes (pas de ressaisie). Forme sociale IDENTIQUE pour les 2 SEL (contrainte source).
_SCM_INTER_SEL_INPUTS = {
    "inter_sel_active": True,
    "inter_sel_forme": "SELARL",
    "inter_sel_titre": "Docteur",
    "inter_sel_parties": [
        {
            "denomination": "SEL DOCTEUR DURAND",
            "capital": "1 000 euros",
            "siege": "1 rue des Soins, 75001 Paris",
            "ville_rcs": "Paris",
            "numero_rcs": "900 000 001",
            "telephone": "01 00 00 00 01",
        },
        {
            "denomination": "SEL DOCTEUR MARTIN",
            "capital": "1 000 euros",
            "siege": "2 rue des Soins, 75002 Paris",
            "ville_rcs": "Paris",
            "numero_rcs": "900 000 002",
            "telephone": "01 00 00 00 02",
        },
    ],
    "inter_sel_locaux": "10 rue de la Paix, 75002 Paris",
    "inter_sel_date_effet": "1er janvier 2027",
    "inter_sel_seuil": "1 500 euros",
    "inter_sel_annee_ref": "2027",
    "inter_sel_date_fin_gestion": "31 decembre 2027",
    "inter_sel_date_attribution": "1er janvier",
}

_SCM_INTER_SEL_DOCS = {"contrat_frais_communs.docx", "reglement_interieur_scm.docx"}


def test_scm_inter_sel_adds_frais_communs_reglement(tmp_path: Path) -> None:
    # Opt-in actif + 2 associes physiques -> le bundle ajoute le contrat de frais
    # communs (DOC-027) et le reglement interieur (DOC-028).
    payload = _civil_base(
        "SCM",
        "scm",
        [_pp("Jean", "Durand", 50, 1, 50, 500), _pp("Alice", "Martin", 50, 51, 100, 500)],
    )
    payload.update(_SCM_INTER_SEL_INPUTS)
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == (
        "DOC-025",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-030",
        "DOC-026",
        "DOC-027",
        "DOC-028",
    )
    generated = css.generate_dossier(payload, tmp_path / "scm-inter-sel")
    _assert_bundle_clean(
        generated,
        _TRONC_DOCS
        | {
            "statuts_scm.docx",
            "pacte_associes_scm.docx",
            "liste_depenses_communes_scm.docx",
        }
        | _SCM_INTER_SEL_DOCS,
    )


def test_scm_inter_sel_off_keeps_base_satellites(tmp_path: Path) -> None:
    # Inter-SEL explicitement inactif (bascule decochee) -> pas de docs inter-SEL, bundle
    # satellites de base inchange. NB : depuis R22-03/04 le defaut UI est ACTIF ; ce test
    # couvre le cas ou l'utilisateur decoche (SCM sans SEL distincte).
    payload = _civil_base(
        "SCM",
        "scm",
        [_pp("Jean", "Durand", 50, 1, 50, 500), _pp("Alice", "Martin", 50, 51, 100, 500)],
    )
    payload["inter_sel_active"] = False
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert "DOC-027" not in plan.document_codes
    assert "DOC-028" not in plan.document_codes
    generated = css.generate_dossier(payload, tmp_path / "scm-no-inter-sel")
    names = {p.name for p in generated.docx_paths}
    assert "contrat_frais_communs.docx" not in names
    assert "reglement_interieur_scm.docx" not in names


def test_scm_inter_sel_blocks_with_personne_morale(tmp_path: Path) -> None:
    # Opt-in actif mais un associe est une personne morale -> blocage (la SEL de chaque
    # associe physique est la partie ; une PM ne fournit pas de praticien-representant).
    payload = _civil_base(
        "SCM",
        "scm",
        [_pm(50, 1, 50, 500), _pp("Alice", "Martin", 50, 51, 100, 500)],
    )
    payload.update(_SCM_INTER_SEL_INPUTS)
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is False
    assert any("personnes physiques" in b for b in plan.blockers)


def test_civil_capital_not_divisible_by_parts_blocks(tmp_path: Path) -> None:
    # Dogfood 2026-06-22 : capital non divisible par le nb de parts -> valeur nominale non
    # entiere (1000/3 = 333.3333... a 28 chiffres dans l'acte). Doit bloquer proprement, pas
    # generer un document casse. Garde de divisibilite partagee.
    payload = _civil_base("SCI", "sci", [_pp("Jean", "Durand", 3, 1, 3, 1000)])
    payload["capital_social"] = "1000"
    payload["nb_parts_total"] = 3
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is False
    assert any("divisible" in b for b in plan.blockers)


def test_civil_capital_divisible_by_parts_ok(tmp_path: Path) -> None:
    # Contre-epreuve : 999 / 3 = 333 (entier) -> pas de blocage de divisibilite.
    payload = _civil_base("SCI", "sci", [_pp("Jean", "Durand", 3, 1, 3, 999)])
    payload["capital_social"] = "999"
    payload["nb_parts_total"] = 3
    plan = css.build_civil_plan(payload)
    assert not any("divisible" in b for b in plan.blockers)


def test_civil_capital_zero_blocks() -> None:
    # Dogfood 2026-06-22 : « 0 » passait la garde de presence -> capital 0. Doit bloquer.
    payload = _civil_base(
        "SCM", "scm", [_pp("Jean", "Durand", 50, 1, 50, 0), _pp("Alice", "Martin", 50, 51, 100, 0)]
    )
    payload["capital_social"] = "0"
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is False
    assert any("apital" in b and "superieur a zero" in b for b in plan.blockers)


def test_civil_missing_banque_adresse_blocks() -> None:
    # Dogfood 2026-06-22 : le generateur exige l'adresse de la banque -> bloquer avant crash.
    payload = _civil_base("SCI", "sci", [_pp("Jean", "Durand", 100, 1, 100, 1000)])
    payload["banque_adresse"] = ""
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is False
    assert any("anque" in b and "dresse" in b for b in plan.blockers)


def test_civil_morale_associe_without_representant_blocks() -> None:
    # Dogfood 2026-06-22 : associe personne morale sans representant -> can_generate=True
    # puis ValueError au generateur. Doit bloquer proprement.
    pm = _pm(50, 1, 50, 500)
    pm.representant = None
    payload = _civil_base("SCM", "scm", [pm, _pp("Alice", "Martin", 50, 51, 100, 500)])
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is False
    assert any("representant" in b.lower() for b in plan.blockers)


def test_scs_slice_generates_clean(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCS",
        "scs",
        [
            _pp("Jean", "Durand", 60, 1, 60, 600, role="commandite"),
            _pp("Alice", "Martin", 40, 61, 100, 400, role="commanditaire"),
        ],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-019", "DOC-001", "DOC-002", "DOC-003", "DOC-004")
    generated = css.generate_dossier(payload, tmp_path / "scs")
    _assert_bundle_clean(generated, _TRONC_DOCS | {"statuts_scs.docx"})


def test_sci_iris_slice_generates_clean(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCI IRIS",
        "sci_iris",
        [_pm(40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-021", "DOC-001", "DOC-002", "DOC-003", "DOC-004")
    generated = css.generate_dossier(payload, tmp_path / "iris")
    _assert_bundle_clean(generated, _TRONC_DOCS | {"statuts_sci_iris.docx"})


def test_sci_standard_allows_personne_morale(tmp_path: Path) -> None:
    # Ratifie Rafael 2026-06-08 : une SCI classique peut avoir une societe comme
    # associee (SCI -> micro-holding -> SPFPL). Le moteur ne bloque plus ; l'identite
    # morale est rendue proprement (meme machinerie que SCM / SCI IRIS).
    payload = _civil_base(
        "SCI",
        "sci",
        [_pm(40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-020", "DOC-001", "DOC-002", "DOC-003", "DOC-004")
    generated = css.generate_dossier(payload, tmp_path / "sci_pm")
    _assert_bundle_clean(generated, _TRONC_DOCS | {"statuts_sci.docx"})
    statuts_text = _docx_text(
        next(p for p in generated.docx_paths if p.name == "statuts_sci.docx")
    )
    # L'identite morale de l'associe societe apparait dans les statuts.
    assert "SEL IRIS" in statuts_text


def test_civil_blocks_incoherent_parts_sum() -> None:
    payload = _civil_base(
        "SCI",
        "sci",
        [_pp("Jean", "Durand", 40, 1, 40, 400), _pp("Alice", "Martin", 50, 41, 90, 500)],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is False
    assert any("Somme des parts" in b for b in plan.blockers)


# --- A2 : preuve multi-associes N (3 et 5) ------------------------------------
# Le socle multi-N est DEJA cable (repeater 1..6, generateurs iterent sur la
# liste d'associes). Ces tests PROUVENT qu'il tient a 3 et 5 ; ils ne corrigent
# rien. Si l'un casse -> bug reel a remonter, pas a patcher a l'aveugle.


def _names_in(generated, docx_name: str) -> str:
    return _docx_text(next(p for p in generated.docx_paths if p.name == docx_name))


def test_sci_three_associes_generates_clean(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCI",
        "sci",
        [
            _pp("Jean", "Durand", 40, 1, 40, 400),
            _pp("Alice", "Martin", 30, 41, 70, 300),
            _pp("Paul", "Petit", 30, 71, 100, 300),
        ],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-020", "DOC-001", "DOC-002", "DOC-003", "DOC-004")
    generated = css.generate_dossier(payload, tmp_path / "sci3")
    _assert_bundle_clean(generated, _TRONC_DOCS | {"statuts_sci.docx"})
    # Les 3 associes apparaissent dans les statuts ET sont listes au PV nomination.
    statuts_text = _names_in(generated, "statuts_sci.docx")
    pv_text = _names_in(generated, "pv_nomination_gerant.docx")
    for nom in ("Durand", "Martin", "Petit"):
        assert nom in statuts_text
        assert nom in pv_text


def test_sci_five_associes_generates_clean(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCI",
        "sci",
        [
            _pp("Jean", "Durand", 20, 1, 20, 200),
            _pp("Alice", "Martin", 20, 21, 40, 200),
            _pp("Paul", "Petit", 20, 41, 60, 200),
            _pp("Marie", "Robert", 20, 61, 80, 200),
            _pp("Luc", "Bernard", 20, 81, 100, 200),
        ],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    generated = css.generate_dossier(payload, tmp_path / "sci5")
    _assert_bundle_clean(generated, _TRONC_DOCS | {"statuts_sci.docx"})
    statuts_text = _names_in(generated, "statuts_sci.docx")
    for nom in ("Durand", "Martin", "Petit", "Robert", "Bernard"):
        assert nom in statuts_text


def test_scs_three_associes_generates_clean(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCS",
        "scs",
        [
            _pp("Jean", "Durand", 40, 1, 40, 400, role="commandite"),
            _pp("Alice", "Martin", 30, 41, 70, 300, role="commanditaire"),
            _pp("Paul", "Petit", 30, 71, 100, 300, role="commanditaire"),
        ],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-019", "DOC-001", "DOC-002", "DOC-003", "DOC-004")
    generated = css.generate_dossier(payload, tmp_path / "scs3")
    _assert_bundle_clean(generated, _TRONC_DOCS | {"statuts_scs.docx"})
    statuts_text = _names_in(generated, "statuts_scs.docx")
    for nom in ("Durand", "Martin", "Petit"):
        assert nom in statuts_text


def test_sci_iris_three_associes_generates_clean(tmp_path: Path) -> None:
    # 1 personne morale (contrainte IRIS) + 2 personnes physiques.
    payload = _civil_base(
        "SCI IRIS",
        "sci_iris",
        [
            _pm(40, 1, 40, 400),
            _pp("Alice", "Martin", 30, 41, 70, 300),
            _pp("Paul", "Petit", 30, 71, 100, 300),
        ],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-021", "DOC-001", "DOC-002", "DOC-003", "DOC-004")
    generated = css.generate_dossier(payload, tmp_path / "iris3")
    # Les groupes de resultat IRIS sont produits sans token residuel pour 3 plages.
    _assert_bundle_clean(generated, _TRONC_DOCS | {"statuts_sci_iris.docx"})


def test_scm_three_associes_drops_satellites(tmp_path: Path) -> None:
    # Les satellites SCM (pacte DOC-026 + liste depenses DOC-030) sont verrouilles
    # a EXACTEMENT 2 associes (modeles batis pour 2). A 3, ils disparaissent ; le
    # bundle de base reste genere proprement. Generaliser >2 = FLAG Rafael.
    payload = _civil_base(
        "SCM",
        "scm",
        [
            _pp("Jean", "Durand", 40, 1, 40, 400),
            _pp("Alice", "Martin", 30, 41, 70, 300),
            _pp("Paul", "Petit", 30, 71, 100, 300),
        ],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert "DOC-026" not in plan.document_codes
    assert "DOC-030" not in plan.document_codes
    assert plan.document_codes == (
        "DOC-025",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
    )
    generated = css.generate_dossier(payload, tmp_path / "scm3")
    names = {p.name for p in generated.docx_paths}
    assert "pacte_associes_scm.docx" not in names
    assert "liste_depenses_communes_scm.docx" not in names
    _assert_bundle_clean(
        generated,
        _TRONC_DOCS | {"statuts_scm.docx", "demande_inscription_ordre.docx"},
    )


# --- A3/A4 civils : selection du gerant + DNC sous le gerant -------------------


def test_civil_gerant_selectable_via_index() -> None:
    # Le gerant civil peut etre un autre associe physique que le 1er.
    payload = _civil_base(
        "SCI",
        "sci",
        [_pp("Jean", "Durand", 40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    payload["gerant_index"] = 1  # Alice Martin gerante
    ctx = css.build_generation_context(payload)
    assert ctx.personne_signataire.nom == "Martin"


def test_civil_gerant_defaults_to_first_physique_skipping_morale() -> None:
    # SCI IRIS : associe 0 = personne morale -> le gerant par defaut = 1er associe
    # PHYSIQUE (index 1), jamais la personne morale.
    payload = _civil_base(
        "SCI IRIS",
        "sci_iris",
        [_pm(40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    ctx = css.build_generation_context(payload)  # pas de gerant_index
    assert ctx.personne_signataire.nom == "Martin"


def test_civil_gerant_index_morale_falls_back() -> None:
    # Un gerant_index pointant la personne morale retombe sur le 1er physique.
    payload = _civil_base(
        "SCI IRIS",
        "sci_iris",
        [_pm(40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    payload["gerant_index"] = 0  # pointe la personne morale -> fallback index 1
    ctx = css.build_generation_context(payload)
    assert ctx.personne_signataire.nom == "Martin"


def _sas_payload():
    return {
        "denomination": "SPFPL MARTIN",
        "siege": "10 rue de la Paix, 75002 Paris",
        "siege_num": "10",
        "siege_voie": "rue de la Paix",
        "siege_cp": "75002",
        "siege_ville": "Paris",
        "capital_social": "12000",
        "nb_actions_total": 120,
        "valeur_nominale_action": "100",
        "apports_nature_montant": "10000",
        "apports_numeraire_montant": "2000",
        "civilite": "Docteur",
        "prenom": "Camille",
        "nom": "Martin",
        "genre": Gender.MASCULIN,
        "qualification_principale": "Medecin cardiologue",
        "date_naissance": "2 janvier 1980",
        "date_naissance_iso": date(1980, 1, 2),
        "ville_naissance": "Paris",
        "departement_naissance": "75",
        "nationalite": "francaise",
        "regime_matrimonial": "la communaute legale",
        "adresse": "5 rue Royale, 75008 Paris",
        "adresse_num": "5",
        "adresse_voie": "rue Royale",
        "adresse_cp": "75008",
        "adresse_ville": "Paris",
        "nom_pere": "Pierre Martin",
        "nom_mere": "Anne Martin",
        "conjoint_civilite": "Madame",
        "conjoint_prenom": "Alice",
        "conjoint_nom": "Martin",
        "ordre_departement": "Paris",
        "numero_ordre": "12345",
        "numero_rpps": "10000000001",
        "cible_denomination": "SELARL CABINET MARTIN",
        "cible_forme": "SELARL",
        "cible_siege": "12 avenue des Ternes, 75017 Paris",
        "cible_ville_rcs": "Paris",
        "cible_numero_rcs": "900 000 001",
        "apport_nb_parts": 50,
        "banque_nom": "BANQUE EXEMPLE",
        "signature_lieu": "Paris",
        "exercice_debut": "1er janvier",
        "exercice_fin": "31 decembre",
        "date_cloture": "31 decembre 2026",
        "signature_date": date(2026, 5, 14),
    }


def test_sas_slice_generates_clean(tmp_path: Path) -> None:
    payload = _sas_payload()
    plan = sas_slice.build_sas_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-015", "DOC-001", "DOC-002", "DOC-003", "DOC-024", "DOC-023")
    generated = sas_slice.generate_dossier(payload, tmp_path / "sas")
    _assert_bundle_clean(
        generated,
        {
            "statuts_sas_spfpl_medecins.docx",
            "declaration_non_condamnation.docx",
            "autorisation_domiciliation.docx",
            "procuration.docx",
            "attestation_capital_liste_souscripteurs_sas.docx",
            "pv_remuneration_president.docx",
        },
    )


def _spfpl_payload(structure):
    operation = "apport" if "apport" in structure else "cession"
    return {
        "structure": structure,
        "operation": operation,
        "is_apport": operation == "apport",
        "cession_data": {
            "nb_cedees": 60,
            "prix_unitaire": "1000",
            "plage_cedee": "41 a 100",
            "cible_forme_complete": "societe d'exercice liberal a responsabilite limitee",
            "cible_siege_num": "12",
            "cible_siege_voie": "avenue des Ternes",
            "cible_siege_cp": "75017",
            "cible_siege_ville": "Paris",
            "associes": [
                {
                    "civilite": "Docteur", "prenom": "Camille", "nom": "Martin",
                    "avant": 70, "apres": 10, "plage": "1 a 10",
                },
                {
                    "civilite": "Docteur", "prenom": "Louise", "nom": "Bernard",
                    "avant": 30, "apres": 30, "plage": "11 a 40",
                },
            ],
        },
        "denomination": "SPFPL MARTIN",
        "siege": "10 rue de la Paix, 75002 Paris",
        "capital_social": "60000",
        "valeur_nominale_action": "100",
        # §14.2 : civilite = civilite CIVILE (M./Mme) ; le titre pro « Docteur »
        # est porte par titre_affichage (automatique pour une SPFPL dentiste).
        "civilite": "Monsieur",
        "titre_affichage": "Docteur",
        "prenom": "Camille",
        "prenoms": "Camille Andre",
        "nom": "Martin",
        "genre": Gender.MASCULIN,
        "date_naissance": "02/01/1980",
        "ville_naissance": "Paris",
        "departement_naissance": "75",
        "nationalite": "francaise",
        "regime_matrimonial": "la communaute legale",
        "adresse": "5 rue Royale, 75008 Paris",
        "adresse_num": "5",
        "adresse_voie": "rue Royale",
        "adresse_cp": "75008",
        "adresse_ville": "Paris",
        "nom_pere": "Pierre Martin",
        "nom_mere": "Anne Martin",
        "decision_date": date(2026, 5, 14),
        "siege_num": "10",
        "siege_voie": "rue de la Paix",
        "siege_cp": "75002",
        "siege_ville": "Paris",
        "ville_rcs": "Paris",
        "conjoint_civilite": "Madame",
        "conjoint_prenom": "Alice",
        "conjoint_nom": "Martin",
        "ordre_departement": "Paris",
        "numero_ordre": "12345",
        "numero_rpps": "10000000001",
        "ordre_conseil": "Conseil departemental",
        "ordre_adresse_ligne_1": "1 rue de l'Ordre",
        "ordre_cp": "75008",
        "ordre_ville": "Paris",
        "banque_nom": "BANQUE EXEMPLE",
        "banque_adresse": "1 boulevard Haussmann, 75009 Paris",
        "apport_montant": "60000",
        "apport_nb_parts": 60,
        "apport_plage": "41 a 100",
        "apport_valeur_globale": "60000",
        "cible_denomination": "SELARL CABINET MARTIN",
        "cible_siege": "12 avenue des Ternes, 75017 Paris",
        "cible_ville_rcs": "Paris",
        "cible_numero_rcs": "900 000 001",
        "cible_forme": "SELARL",
        "cible_profession": "chirurgien-dentiste",
        "cible_capital": "10000",
        "cible_nb_parts": 100,
        "cible_valeur_part": "100",
        # Operation apport (DOC-041/042/043) : detail des titres + organes de controle.
        "apport_nature_titres": "parts sociales",
        "apport_valeur_par_titre": "1000",
        "commissaire_denomination": "CAA EXPERTISE",
        "commissaire_forme": "SAS",
        "commissaire_capital": "1 000 euros",
        "commissaire_siege": "1 rue Scheffer, 75016 Paris",
        "commissaire_ville_rcs": "Paris",
        "commissaire_numero_rcs": "948 483 730",
        "commissaire_rep_civilite": "Monsieur",
        "commissaire_rep_prenom": "Nabil",
        "commissaire_rep_nom": "Saidi",
        "evaluateur_denomination": "EVAL CONSEIL",
        "evaluateur_forme": "SAS",
        "evaluateur_capital": "1 000 euros",
        "evaluateur_siege": "1 rue Scheffer, 75016 Paris",
        "evaluateur_ville_rcs": "Paris",
        "evaluateur_numero_rcs": "948 483 730",
        "evaluateur_rep_civilite": "Madame",
        "evaluateur_rep_prenom": "Eva",
        "evaluateur_rep_nom": "Lemoine",
        "exercice_debut": "1er janvier",
        "exercice_fin": "31 decembre",
        "date_cloture": "31 decembre 2026",
        "signature_lieu": "Paris",
        "signature_date": date(2026, 5, 14),
    }


_SPFPL_BUNDLE_TRONC = {
    "declaration_non_condamnation.docx",
    "autorisation_domiciliation.docx",
    "procuration.docx",
    "pv_nomination_gerant.docx",
    "demande_inscription_ordre.docx",
}

# Documents d'operation apport (DOC-041/042/043) ajoutes au bundle de creation.
_SPFPL_APPORT_DOCS = {
    "contrat_apport_spfpl.docx",
    "attestation_capital_liste_souscripteurs.docx",
    "attestation_commissaire_apports.docx",
}

# Documents d'operation cession : note d'info (DOC-037) + PV d'agrement plusieurs
# associes (DOC-039, car le payload de test a 2 associes cible) + acte (DOC-040).
_SPFPL_CESSION_DOCS = {
    "note_information.docx",
    "pv_agrement_cession_spfpl_plusieurs_associes.docx",
    "acte_cession_parts_spfpl.docx",
}


def test_spfpl_cession_slice_generates_clean(tmp_path: Path) -> None:
    payload = _spfpl_payload("SPFPL cession")
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    # Creation + documents d'operation cession (note + PV agrement plusieurs + acte).
    assert plan.document_codes == (
        "DOC-035",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-037",
        "DOC-039",
        "DOC-040",
    )
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-cession")
    _assert_bundle_clean(
        generated,
        _SPFPL_BUNDLE_TRONC | {"statuts_spfpl_cession.docx"} | _SPFPL_CESSION_DOCS,
    )


def test_spfpl_apport_slice_generates_clean(tmp_path: Path) -> None:
    payload = _spfpl_payload("SPFPL apport")
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    # L'apport complete le bundle de creation par ses 3 documents d'operation
    # (contrat d'apport DOC-041 + attestations capital DOC-042 / commissaire DOC-043).
    assert plan.document_codes == (
        "DOC-036",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-041",
        "DOC-042",
        "DOC-043",
    )
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-apport")
    _assert_bundle_clean(
        generated,
        _SPFPL_BUNDLE_TRONC | {"statuts_spfpl_apport.docx"} | _SPFPL_APPORT_DOCS,
    )


_REGIME_DOCS = {
    "lettre_renonciation_associe.docx",
    "lettre_avertissement_conjoint.docx",
}


def test_spfpl_regime_off_keeps_base_bundle(tmp_path: Path) -> None:
    payload = _spfpl_payload("SPFPL cession")
    payload["regime_communautaire"] = False
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    assert "DOC-005" not in plan.document_codes
    assert "DOC-006" not in plan.document_codes
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-regime-off")
    names = {p.name for p in generated.docx_paths}
    assert not (_REGIME_DOCS & names)


def test_spfpl_cession_regime_on_adds_regime_docs(tmp_path: Path) -> None:
    payload = _spfpl_payload("SPFPL cession")
    payload["regime_communautaire"] = True
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == (
        "DOC-035",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-005",
        "DOC-006",
        "DOC-037",
        "DOC-039",
        "DOC-040",
    )
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-cession-regime")
    _assert_bundle_clean(
        generated,
        _SPFPL_BUNDLE_TRONC
        | {"statuts_spfpl_cession.docx"}
        | _SPFPL_CESSION_DOCS
        | _REGIME_DOCS,
    )


def test_spfpl_apport_regime_on_adds_regime_docs(tmp_path: Path) -> None:
    payload = _spfpl_payload("SPFPL apport")
    payload["regime_communautaire"] = True
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    assert "DOC-005" in plan.document_codes
    assert "DOC-006" in plan.document_codes
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-apport-regime")
    _assert_bundle_clean(
        generated,
        _SPFPL_BUNDLE_TRONC | {"statuts_spfpl_apport.docx"} | _SPFPL_APPORT_DOCS | _REGIME_DOCS,
    )


# --- Regressions « variables mal injectees » (audit 2026-06-09) ---------------


def test_spfpl_apport_capital_not_duplicated(tmp_path: Path) -> None:
    # Le capital (art. 8) ne doit plus etre injecte en double (« 60000 € 60000euros »).
    payload = _spfpl_payload("SPFPL apport")
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-apport-cap")
    text = _docx_text(
        next(p for p in generated.docx_paths if p.name == "statuts_spfpl_apport.docx")
    )
    assert "60000euros" not in text  # plus de « euros » colle
    assert "€ 60000" not in text  # plus de montant duplique apres le €
    assert "60000 euros" in text  # forme propre


# --- §14.2 : SPFPL dentiste, « Docteur » automatique (hors deroulante civilite) -


def test_spfpl_titre_docteur_automatic_civilite_is_civil() -> None:
    # §14.2 : la civilite portee au contexte est la civilite CIVILE (M./Mme), et le
    # titre pro « Docteur » est applique automatiquement (titre_affichage), sans
    # dependre de la valeur choisie dans la deroulante civilite.
    payload = _spfpl_payload("SPFPL cession")
    assert payload["civilite"] == "Monsieur"  # civilite civile, plus « Docteur »
    ctx = spfpl_slice.build_generation_context(payload)
    assert ctx.personne_signataire.civilite == "Monsieur"
    assert ctx.personne_signataire.titre_affichage == "Docteur"
    # Le dirigeant / president gardent la civilite CIVILE (mutualise SELARL/SELAS).
    assert ctx.dirigeant_nomine.civilite_affichage == "Monsieur"


def test_spfpl_demande_ordre_uses_docteur_title(tmp_path: Path) -> None:
    # §14.2 : la demande d'inscription a l'ordre (titre_affichage) affiche « Docteur »
    # automatiquement, meme si la civilite civile est « Monsieur ».
    payload = _spfpl_payload("SPFPL cession")
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-titre-ordre")
    text = _docx_text(
        next(p for p in generated.docx_paths if p.name == "demande_inscription_ordre.docx")
    )
    assert "Docteur Camille Martin" in text


def test_spfpl_form_civilite_drops_docteur_and_genre_selector() -> None:
    # §14.2 : la deroulante civilite ne propose plus « Docteur » (M./Mme seulement)
    # et le selecteur « Genre civil » redondant a disparu.
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=120)
    app.selectbox(key="clean_dossier_type").set_value("SPFPL dentistes - cession creation V1")
    app = app.run(timeout=120)

    civilite_box = next(s for s in app.selectbox if str(s.key) == "spfpl_cession_civilite")
    assert "Docteur" not in list(civilite_box.options)
    assert set(civilite_box.options) == {"Monsieur", "Madame"}
    assert not any(str(s.key) == "spfpl_cession_genre_label" for s in app.selectbox)


def test_sas_attestation_no_double_docteur(tmp_path: Path) -> None:
    # Le titre « Docteur » ne doit plus etre injecte en double
    # (« Le Docteur Docteur Camille Martin »).
    payload = _sas_payload()
    generated = sas_slice.generate_dossier(payload, tmp_path / "sas-titre")
    text = _docx_text(
        next(
            p
            for p in generated.docx_paths
            if p.name == "attestation_capital_liste_souscripteurs_sas.docx"
        )
    )
    assert "Docteur Docteur" not in text
    assert "Le Docteur Camille Martin a fait" in text


def _selas_payload():
    phys = StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=Gender.FEMININ,
        civilite_affichage="Madame",
        prenom="Claire",
        prenoms="Claire",
        nom="Durand",
        date_naissance="1 janvier 1980",
        ville_naissance="Lyon",
        departement_naissance="69",
        nationalite="française",
        profession="Docteur",
        situation_maritale="célibataire",
        adresse_personnelle_affichee="10 rue Exemple, 69000 Lyon",
        qualification_principale="qualifiée en médecine générale",
        ordre_departemental="Rhône",
        numero_ordre="69-12345",
        numero_rpps="10100000001",
        qualite_capital="associée exerçante",
        nb_actions=75,
        nb_actions_lettres="soixante-quinze",
        apport=StatutsCivilsApport(montant="750", montant_lettres="sept cent cinquante"),
    )
    mor = StatutsCivilsAssocie(
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
        qualite_capital="associée non exerçante",
        nb_actions=25,
        nb_actions_lettres="vingt-cinq",
        apport=StatutsCivilsApport(montant="250", montant_lettres="deux cent cinquante"),
    )
    return {
        "denomination": "SELAS EXEMPLE",
        "siege": "5 place du Centre, 69000 Lyon",
        "siege_num": "5",
        "siege_voie": "place du Centre",
        "siege_cp": "69000",
        "siege_ville": "Lyon",
        "profession_reglementee": "médecin",
        "profession_reglementee_pluriel": "médecins",
        "capital_social": "1000",
        "nb_actions_total": 100,
        "valeur_nominale_action": "10",
        "ville_rcs": "Lyon",
        "adresse_lieu_exercice": "5 place du Centre, 69000 Lyon",
        "banque_nom": "BANQUE EXEMPLE",
        "banque_adresse": "1 rue Banque, 69009 Lyon",
        "date_cloture": "31 décembre 2026",
        "signature_lieu": "Lyon",
        "signature_date": date(2026, 5, 15),
        "associes": [phys, mor],
        # Documents communs : signataire = president (1er physique).
        "signataire_nom_pere": "Pierre Durand",
        "signataire_nom_mere": "Anne Durand",
        "signataire_adresse_num": "10",
        "signataire_adresse_voie": "rue Exemple",
        "signataire_adresse_cp": "69000",
        "signataire_adresse_ville": "Lyon",
        "signataire_nationalite": "française",
        "signataire_titre": "Docteur",
        "signataire_date_naissance": date(1980, 1, 1),
        "decision_date": date(2026, 5, 15),
        "ordre_conseil": "Conseil departemental",
        "ordre_departement": "Rhône",
        "ordre_adresse_ligne_1": "1 rue de l'Ordre",
        "ordre_cp": "69002",
        "ordre_ville": "Lyon",
        "ordre_numero": "69-12345",
    }


def test_selas_multi_slice_generates_clean(tmp_path: Path) -> None:
    payload = _selas_payload()
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-044", "DOC-001", "DOC-002", "DOC-003", "DOC-004", "DOC-034")
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas")
    _assert_bundle_clean(
        generated,
        {
            "statuts_selas_multi.docx",
            "declaration_non_condamnation.docx",
            "autorisation_domiciliation.docx",
            "procuration.docx",
            "pv_nomination_gerant.docx",
            "demande_inscription_ordre.docx",
        },
    )


def test_selas_ordre_conseil_derive_sans_champ_libelle(tmp_path: Path) -> None:
    # R5 (2026-06-18) : le « Conseil departemental » n'est plus saisi ; le libelle
    # de la demande d'inscription est derive du departement + connecteur. Sans
    # ordre_conseil dans le payload (champ supprime), la generation reste propre
    # et le libelle est reconstruit cote moteur.
    payload = _selas_payload()
    payload.pop("ordre_conseil", None)  # champ supprime du formulaire
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is True  # plus de blocage sur ordre_conseil
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas-ordre-derive")
    text = _docx_text(
        next(p for p in generated.docx_paths if p.name == "demande_inscription_ordre.docx")
    )
    # Connecteur par defaut « de » (ordre_connecteur absent).
    assert "Conseil départemental de l'Ordre des médecins de Rhône" in text


def test_selas_ordre_connecteur_du(tmp_path: Path) -> None:
    # R6 (2026-06-18) : le connecteur grammatical « du » remplace « de » avant le
    # departement de l'ordre dans le libelle derive (gestion de l'accord).
    payload = _selas_payload()
    payload.pop("ordre_conseil", None)
    payload["ordre_connecteur"] = "du"
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas-ordre-du")
    text = _docx_text(
        next(p for p in generated.docx_paths if p.name == "demande_inscription_ordre.docx")
    )
    assert "Conseil départemental de l'Ordre des médecins du Rhône" in text
    assert "des médecins de Rhône" not in text


def test_selas_blocks_incoherent_actions_sum() -> None:
    payload = _selas_payload()
    payload["associes"][1].nb_actions = 10  # 75 + 10 != 100
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is False
    # R3 (2026-06-18) : message reformule façon Rafael (explicite, sans jargon).
    assert any("Problème de calcul" in b for b in plan.blockers)
    assert any("ne correspond pas au nombre total d'actions" in b for b in plan.blockers)


# Saisies conjoint requises par DOC-005 / DOC-006 (regime communautaire).
_SELAS_REGIME_INPUTS = {
    "regime_communautaire": True,
    "conjoint_civilite": "Monsieur",
    "conjoint_genre": Gender.MASCULIN,
    "conjoint_prenom": "Paul",
    "conjoint_nom": "Durand",
    "regime_matrimonial": "la communaute legale",
}


def test_selas_regime_off_keeps_base_bundle(tmp_path: Path) -> None:
    payload = _selas_payload()
    payload["regime_communautaire"] = False
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is True
    assert "DOC-005" not in plan.document_codes
    assert "DOC-006" not in plan.document_codes
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas-regime-off")
    names = {p.name for p in generated.docx_paths}
    assert not (_REGIME_DOCS & names)


def test_selas_regime_on_adds_regime_docs(tmp_path: Path) -> None:
    payload = _selas_payload()
    payload.update(_SELAS_REGIME_INPUTS)
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == (
        "DOC-044",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-005",
        "DOC-006",
    )
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas-regime-on")
    _assert_bundle_clean(
        generated,
        {
            "statuts_selas_multi.docx",
            "declaration_non_condamnation.docx",
            "autorisation_domiciliation.docx",
            "procuration.docx",
            "pv_nomination_gerant.docx",
            "demande_inscription_ordre.docx",
        }
        | _REGIME_DOCS,
    )


def _regime_associe(
    prenom: str,
    nom: str,
    conjoint_civilite: str = "Monsieur",
    conjoint_genre: Gender = Gender.MASCULIN,
) -> RegimeCommunautaireAssocie:
    return RegimeCommunautaireAssocie(
        actif=True,
        regime_matrimonial="la communaute legale",
        conjoint_civilite=conjoint_civilite,
        conjoint_genre=conjoint_genre,
        conjoint_prenom=prenom,
        conjoint_nom=nom,
    )


def test_selas_regime_par_associe_active_les_docs(tmp_path: Path) -> None:
    # R7 (2026-06-18) : le regime communautaire est porte PAR associe physique.
    # Toggle global INACTIF mais le 1er associe (president) marie sous communaute
    # -> DOC-005/006 generes (chemin per-associe), sans toggle global.
    payload = _selas_payload()
    payload["regime_communautaire"] = False  # pas de toggle global
    payload["associes"][0].regime_communautaire_associe = _regime_associe("Paul", "Durand")
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is True
    assert "DOC-005" in plan.document_codes
    assert "DOC-006" in plan.document_codes
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas-regime-assoc")
    names = {p.name for p in generated.docx_paths}
    assert _REGIME_DOCS <= names


def test_selas_regime_par_associe_valide_le_conjoint(tmp_path: Path) -> None:
    # R7 : un associe marie sous communaute sans conjoint complet -> blocage.
    payload = _selas_payload()
    payload["regime_communautaire"] = False
    payload["associes"][0].regime_communautaire_associe = RegimeCommunautaireAssocie(
        actif=True
    )  # conjoint + regime manquants
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is False
    assert any("conjoint" in b.lower() for b in plan.blockers)


def _selas_payload_deux_maries():
    """Payload SELAS avec 2 associes physiques maries sous communaute (R7).

    Associe 0 = Claire Durand (conjoint Paul Durand) ; associe 1 = Marc Petit
    (conjoint Sophie Petit). On remplace la personne morale du payload de base
    par un 2e physique valide (etat civil complet) pour avoir deux maries."""
    payload = _selas_payload()
    payload["regime_communautaire"] = False
    phys2 = payload["associes"][0].model_copy(
        update={
            "genre": Gender.MASCULIN,
            "civilite_affichage": "Monsieur",
            "prenom": "Marc",
            "prenoms": "Marc",
            "nom": "Petit",
            "nb_actions": 25,
            "nb_actions_lettres": "vingt-cinq",
            "qualite_capital": "associé exerçant",
            "apport": StatutsCivilsApport(montant="250", montant_lettres="deux cent cinquante"),
            # Conjointe de Marc : Sophie Petit (civilite feminine coherente).
            "regime_communautaire_associe": _regime_associe(
                "Sophie", "Petit", conjoint_civilite="Madame", conjoint_genre=Gender.FEMININ
            ),
        }
    )
    payload["associes"][0].regime_communautaire_associe = _regime_associe("Paul", "Durand")
    payload["associes"][0].nb_actions = 75
    payload["associes"][1] = phys2
    return payload


def test_selas_deux_associes_maries_flag_multiplication(tmp_path: Path) -> None:
    # R7 : 2 associes physiques maries sous communaute -> warning explicite qu'un
    # couple DOC-005/006 sera genere POUR CHACUN (generation par-personne).
    payload = _selas_payload_deux_maries()
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is True
    assert any("2 associes maries" in w and "POUR CHACUN" in w for w in plan.warnings)


def test_selas_deux_maries_generent_deux_couples_distincts(tmp_path: Path) -> None:
    # R7 : 2 associes maries -> 2 renonciations + 2 avertissements, fichiers de
    # noms distincts (suffixes par nom d'associe), chacun avec le BON conjoint.
    payload = _selas_payload_deux_maries()
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas-2maries")
    names = {p.name for p in generated.docx_paths}
    # Deux couples nommes par associe (le couple historique de nom fixe NE doit
    # PAS apparaitre quand il y a plusieurs maries).
    assert "lettre_renonciation_associe_Durand.docx" in names
    assert "lettre_avertissement_conjoint_Durand.docx" in names
    assert "lettre_renonciation_associe_Petit.docx" in names
    assert "lettre_avertissement_conjoint_Petit.docx" in names
    assert "lettre_renonciation_associe.docx" not in names
    assert "lettre_avertissement_conjoint.docx" not in names
    renonciation_count = sum(1 for n in names if n.startswith("lettre_renonciation_associe"))
    avertissement_count = sum(1 for n in names if n.startswith("lettre_avertissement_conjoint"))
    assert renonciation_count == 2
    assert avertissement_count == 2
    # Le BON conjoint dans le BON fichier (renonciation = signature du conjoint).
    durand_renonciation = _docx_text(
        next(p for p in generated.docx_paths if p.name == "lettre_renonciation_associe_Durand.docx")
    )
    petit_renonciation = _docx_text(
        next(p for p in generated.docx_paths if p.name == "lettre_renonciation_associe_Petit.docx")
    )
    assert "Paul Durand" in durand_renonciation
    assert "Sophie Petit" not in durand_renonciation
    assert "Sophie Petit" in petit_renonciation
    assert "Paul Durand" not in petit_renonciation
    # L'apporteur (renoncant) est bien CHAQUE associe dans son propre fichier.
    assert "Claire Durand" in durand_renonciation
    assert "Marc Petit" in petit_renonciation
    # Avertissement : le conjoint destinataire (civilite + nom) et l'apporteur
    # (civilite prenom nom dans la mention) correspondent a CHAQUE associe.
    durand_avert = _docx_text(
        next(
            p
            for p in generated.docx_paths
            if p.name == "lettre_avertissement_conjoint_Durand.docx"
        )
    )
    petit_avert = _docx_text(
        next(
            p
            for p in generated.docx_paths
            if p.name == "lettre_avertissement_conjoint_Petit.docx"
        )
    )
    # Apporteur correct par fichier (mention manuscrite « ... par {apporteur} »).
    assert "Madame Claire Durand" in durand_avert
    assert "Monsieur Marc Petit" in petit_avert
    # Conjoint destinataire correct (civilite + nom) : Monsieur Durand / Madame Petit.
    assert "Monsieur Durand" in durand_avert
    assert "Madame Petit" in petit_avert
    _assert_bundle_clean(generated, {"statuts_selas_multi.docx"})


def test_selas_deux_maries_adresses_foyer_distinctes(tmp_path: Path) -> None:
    # R7 (2026-06-18) : chaque associe marie porte SON adresse de foyer structuree
    # dans son propre avertissement (DOC-006), plus de repli sur l'adresse du
    # president (residu d63393c). Le president habite « 10 rue Exemple, 69000 Lyon ».
    payload = _selas_payload_deux_maries()
    payload["associes"][0].adresse_personnelle = Address(
        num_voie="3",
        voie="rue des Lilas",
        cp="33000",
        ville="Bordeaux",
        adresse_affichee="3 rue des Lilas, 33000 Bordeaux",
    )
    payload["associes"][1].adresse_personnelle = Address(
        num_voie="7",
        voie="avenue du Parc",
        cp="44000",
        ville="Nantes",
        adresse_affichee="7 avenue du Parc, 44000 Nantes",
    )
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas-2foyers")
    durand_avert = _docx_text(
        next(
            p
            for p in generated.docx_paths
            if p.name == "lettre_avertissement_conjoint_Durand.docx"
        )
    )
    petit_avert = _docx_text(
        next(
            p
            for p in generated.docx_paths
            if p.name == "lettre_avertissement_conjoint_Petit.docx"
        )
    )
    # Chaque avertissement porte SON foyer (bloc destinataire conjoint).
    assert "rue des Lilas" in durand_avert
    assert "33000 Bordeaux" in durand_avert
    assert "avenue du Parc" in petit_avert
    assert "44000 Nantes" in petit_avert
    # Pas de fuite croisee entre les deux foyers.
    assert "avenue du Parc" not in durand_avert
    assert "44000 Nantes" not in durand_avert
    assert "rue des Lilas" not in petit_avert
    assert "33000 Bordeaux" not in petit_avert
    # Plus de repli sur l'adresse PERSONNELLE du president (residu d63393c).
    # Le president habite « 10 rue Exemple, 69000 Lyon » ; « rue Exemple » ne doit
    # plus apparaitre comme adresse du foyer dans les avertissements per-associe.
    # (Le siege social de la societe contient « 69000 Lyon » et reste legitime en
    # en-tete expediteur, donc on ne l'asserte pas.)
    assert "rue Exemple" not in durand_avert
    assert "rue Exemple" not in petit_avert


def test_selas_un_seul_marie_garde_nom_fixe(tmp_path: Path) -> None:
    # R7 : un SEUL associe marie (chemin per-associe) -> couple unique au nom
    # FIXE historique (byte-identique avec le toggle global), pas de suffixe.
    payload = _selas_payload()
    payload["regime_communautaire"] = False
    payload["associes"][0].regime_communautaire_associe = _regime_associe("Paul", "Durand")
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas-1marie")
    names = {p.name for p in generated.docx_paths}
    assert "lettre_renonciation_associe.docx" in names
    assert "lettre_avertissement_conjoint.docx" in names
    # Pas de fichier suffixe pour un seul marie.
    assert not any(n.startswith("lettre_renonciation_associe_") for n in names)
    renonciation = _docx_text(
        next(p for p in generated.docx_paths if p.name == "lettre_renonciation_associe.docx")
    )
    assert "Paul Durand" in renonciation
    assert "Claire Durand" in renonciation


def test_selas_zero_marie_aucun_doc_regime(tmp_path: Path) -> None:
    # R7 : aucun associe marie + toggle global inactif -> aucun document regime.
    payload = _selas_payload()
    payload["regime_communautaire"] = False
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas-0marie")
    names = {p.name for p in generated.docx_paths}
    assert not (_REGIME_DOCS & names)
    assert not any(n.startswith("lettre_renonciation_associe") for n in names)
    assert not any(n.startswith("lettre_avertissement_conjoint") for n in names)


def test_selas_regime_on_requires_conjoint() -> None:
    payload = _selas_payload()
    payload["regime_communautaire"] = True  # toggle ON sans saisies conjoint
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is False
    assert any("regime communautaire" in b.casefold() for b in plan.blockers)


# --- A2 SELAS : preuve multi-associes N (3 et 5, borne moteur 5) --------------


def _selas_phys(prenom, nom, nb_actions, qualite="associé exerçant"):
    """Associe SELAS personne physique exercante, tous champs requis remplis."""
    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=Gender.MASCULIN,
        civilite_affichage="Monsieur",
        prenom=prenom,
        prenoms=prenom,
        nom=nom,
        date_naissance="1 janvier 1980",
        ville_naissance="Lyon",
        departement_naissance="69",
        nationalite="française",
        profession="Docteur",
        situation_maritale="célibataire",
        adresse_personnelle_affichee="10 rue Exemple, 69000 Lyon",
        qualification_principale="qualifié en médecine générale",
        ordre_departemental="Rhône",
        numero_ordre="69-12345",
        numero_rpps="10100000001",
        qualite_capital=qualite,
        nb_actions=nb_actions,
        nb_actions_lettres=str(nb_actions),
        apport=StatutsCivilsApport(
            montant=str(nb_actions * 10), montant_lettres=str(nb_actions * 10)
        ),
    )


def _selas_payload_n(associes):
    """Payload SELAS de base, avec une liste d'associes custom (somme actions auto)."""
    payload = _selas_payload()
    payload["associes"] = associes
    payload["nb_actions_total"] = sum(int(a.nb_actions or 0) for a in associes)
    return payload


_SELAS_BUNDLE_NAMES = {
    "statuts_selas_multi.docx",
    "declaration_non_condamnation.docx",
    "autorisation_domiciliation.docx",
    "procuration.docx",
    "pv_nomination_gerant.docx",
    "demande_inscription_ordre.docx",
}


def test_selas_three_associes_generates_clean(tmp_path: Path) -> None:
    payload = _selas_payload_n(
        [
            _selas_phys("Claire", "Durand", 40),
            _selas_phys("Paul", "Martin", 30),
            _selas_phys("Marie", "Petit", 30),
        ]
    )
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == (
        "DOC-044",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
    )
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas3")
    _assert_bundle_clean(generated, _SELAS_BUNDLE_NAMES)
    statuts_text = _docx_text(
        next(p for p in generated.docx_paths if p.name == "statuts_selas_multi.docx")
    )
    for nom in ("Durand", "Martin", "Petit"):
        assert nom in statuts_text


def test_selas_five_associes_generates_clean(tmp_path: Path) -> None:
    payload = _selas_payload_n(
        [
            _selas_phys("Claire", "Durand", 20),
            _selas_phys("Paul", "Martin", 20),
            _selas_phys("Marie", "Petit", 20),
            _selas_phys("Luc", "Robert", 20),
            _selas_phys("Anne", "Bernard", 20),
        ]
    )
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is True
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas5")
    _assert_bundle_clean(generated, _SELAS_BUNDLE_NAMES)
    statuts_text = _docx_text(
        next(p for p in generated.docx_paths if p.name == "statuts_selas_multi.docx")
    )
    for nom in ("Durand", "Martin", "Petit", "Robert", "Bernard"):
        assert nom in statuts_text


# --- A1 : bornes du repeater nommees + alignees sur le moteur -----------------


def test_repeater_bounds_are_named_and_aligned() -> None:
    # A1 : les bornes sont des constantes nommees (pas de litteraux disperses) et
    # la borne SELAS front est ALIGNEE sur le generateur (un ecart silencieux
    # casserait la generation). Ce test verrouille les valeurs.
    from sydel_doc_engine.generators.lot_04.statuts_selas_multi import (
        MAX_ASSOCIES,
        MIN_ASSOCIES,
    )

    assert css.CIVIL_NB_MIN_BY_STRUCTURE == {
        "SCI": 1,
        "SCM": 1,
        "SCI IRIS": 2,
        "SCS": 2,
    }
    assert css.CIVIL_NB_MAX_ASSOCIES == 6
    assert (selas_multi_slice.SELAS_NB_MIN, selas_multi_slice.SELAS_NB_MAX) == (
        MIN_ASSOCIES,
        MAX_ASSOCIES,
    )


# --- A3 : selection du dirigeant (president) SELAS ----------------------------


def test_selas_president_defaults_to_first_physique() -> None:
    # Sans choix UI (payload sans president_index) : le 1er associe physique est
    # president — comportement historique, non-regression.
    payload = _selas_payload_n(
        [
            _selas_phys("Claire", "Durand", 40),
            _selas_phys("Paul", "Martin", 30),
            _selas_phys("Marie", "Petit", 30),
        ]
    )
    ctx = selas_multi_slice.build_generation_context(payload)
    assert ctx.dirigeant_nomine.ref_associe_index == 0
    assert ctx.statuts_selas_multi.president.ref_associe_index == 0
    assert ctx.dirigeant_nomine.nom == "Durand"


def test_selas_president_selectable() -> None:
    # Le dirigeant peut etre un autre associe physique (le 3e ici).
    payload = _selas_payload_n(
        [
            _selas_phys("Claire", "Durand", 40),
            _selas_phys("Paul", "Martin", 30),
            _selas_phys("Marie", "Petit", 30),
        ]
    )
    payload["president_index"] = 2
    ctx = selas_multi_slice.build_generation_context(payload)
    assert ctx.dirigeant_nomine.ref_associe_index == 2
    assert ctx.statuts_selas_multi.president.ref_associe_index == 2
    assert ctx.dirigeant_nomine.nom == "Petit"


def test_selas_president_index_morale_falls_back_to_physique() -> None:
    # Un index pointant une personne morale ne doit JAMAIS atteindre le moteur
    # (President = personne physique) : on retombe sur le 1er physique.
    morale = _selas_payload()["associes"][1]
    morale.nb_actions = 40
    payload = _selas_payload_n([_selas_phys("Claire", "Durand", 60), morale])
    payload["president_index"] = 1  # pointe la personne morale
    ctx = selas_multi_slice.build_generation_context(payload)
    assert ctx.dirigeant_nomine.ref_associe_index == 0
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is True


# --- Surface UI Streamlit -----------------------------------------------------


def test_front_dropdown_lists_all_types_with_selarl_default() -> None:
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=120)

    selector = app.selectbox(key="clean_dossier_type")
    assert selector.value == "SELARL creation V1"
    assert list(selector.options) == [
        "SELARL creation V1",
        "SCM creation V1",
        "SCI creation V1",
        "SCI IRIS creation V1",
        "SCS creation V1",
        "SPFPL medecins (forme SAS) creation V1",
        "SPFPL dentistes - cession creation V1",
        "SPFPL dentistes - apport creation V1",
        "SELAS multi-associes creation V1",
        "SELAS dentiste pluripersonnelle creation V1",
        "SELAS unipersonnelle medecin creation V1",
    ]
    # Surface SELARL inchangee : aucun expander sur le defaut.
    assert len(app.expander) == 0


def test_front_routes_to_sci_slice_and_generates(tmp_path: Path, monkeypatch) -> None:
    from streamlit.testing.v1 import AppTest

    from sydel_doc_engine.front_app import shell

    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui-sci")
    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=180)
    app.selectbox(key="clean_dossier_type").set_value("SCI creation V1")
    app = app.run(timeout=180)

    def set_text(key: str, value: str) -> None:
        for widget in app.text_input:
            if str(widget.key) == key:
                widget.set_value(value)
                return
        raise KeyError(key)

    def set_number(key: str, value: int) -> None:
        for widget in app.number_input:
            if str(widget.key) == key:
                widget.set_value(value)
                return
        raise KeyError(key)

    # forme_sociale derivee (§18.1), valeur nominale calculee (§18.2), duree figee
    # (§18.3), lieu signature = ville siege (§18.4) : ces champs ne sont plus saisis.
    society = {
        "sci_denomination": "SCI EXEMPLE",
        "sci_siege_num": "10",
        "sci_siege_voie": "rue de la Paix",
        "sci_siege_cp": "75002",
        "sci_siege_ville": "Paris",
        "sci_ville_rcs": "Paris",
        "sci_banque_nom": "BANQUE",
        "sci_banque_adresse": "1 rue Banque, 75009 Paris",
        "sci_date_cloture_premier_exercice": "31 decembre 2026",
        # Documents communs (hors identite du gerant : fonction/titre/decision).
        "sci_signataire_fonction": "gerant",
        "sci_signataire_titre": "Docteur",
        "sci_decision_date": "15/05/2026",
    }
    for key, value in society.items():
        set_text(key, value)
    # Capital social = number_input (parite gold) -> set via set_number.
    set_number("sci_capital_social", 1000)
    set_text("sci_signature_date", "15/05/2026")
    app = app.run(timeout=180)

    # Nationalite = deroulant (§SCREEN-1, cle _choice) ; adresse personnelle
    # structuree (§18.5) ; profession non demandee hors SCM (§18.6) ; parts debut/fin
    # derivees (§18.5) ; DNC = noms des parents uniquement.
    associes_text = {
        "sci_associe_0_prenom": "Jean",
        "sci_associe_0_nom": "Durand",
        "sci_associe_0_date_naissance": "1 janvier 1980",
        "sci_associe_0_ville_naissance": "Paris",
        "sci_associe_0_departement_naissance": "75",
        "sci_associe_0_situation_maritale": "celibataire",
        "sci_associe_0_adresse_num": "1",
        "sci_associe_0_adresse_voie": "rue Exemple",
        "sci_associe_0_adresse_cp": "75000",
        "sci_associe_0_adresse_ville": "Paris",
        "sci_associe_0_apport_montant": "400",
        # DNC du gerant (associe 0, coche « Dirigeant » par defaut) saisie sous lui.
        "sci_associe_0_sig_nom_pere": "Pierre Durand",
        "sci_associe_0_sig_nom_mere": "Anne Durand",
        "sci_associe_1_prenom": "Alice",
        "sci_associe_1_nom": "Martin",
        "sci_associe_1_date_naissance": "2 fevrier 1982",
        "sci_associe_1_ville_naissance": "Lyon",
        "sci_associe_1_departement_naissance": "69",
        "sci_associe_1_situation_maritale": "celibataire",
        "sci_associe_1_adresse_num": "2",
        "sci_associe_1_adresse_voie": "rue Exemple",
        "sci_associe_1_adresse_cp": "69000",
        "sci_associe_1_adresse_ville": "Lyon",
        "sci_associe_1_apport_montant": "600",
    }
    for key, value in associes_text.items():
        set_text(key, value)
    associes_numbers = {
        "sci_associe_0_nb_titres": 40,
        "sci_associe_1_nb_titres": 60,
        "sci_nb_parts_total": 100,
    }
    for key, value in associes_numbers.items():
        set_number(key, value)
    app = app.run(timeout=180)

    generate_button = next(
        b for b in app.button if str(b.key) == "clean_typed_generate_dossier"
    )
    assert generate_button.disabled is False
    assert not any("Blocage" in item.value for item in app.caption)

    generate_button.click()
    app = app.run(timeout=180)

    download_labels = [item.label for item in app.get("download_button")]
    assert "Telecharger statuts_sci.docx" in download_labels
    assert "Telecharger le dossier ZIP" in download_labels


@pytest.mark.parametrize(
    "label, statuts_name",
    [
        ("SCM creation V1", "statuts_scm.docx"),
        ("SCI creation V1", "statuts_sci.docx"),
        ("SCI IRIS creation V1", "statuts_sci_iris.docx"),
        ("SCS creation V1", "statuts_scs.docx"),
        ("SPFPL medecins (forme SAS) creation V1", "statuts_sas_spfpl_medecins.docx"),
        ("SPFPL dentistes - cession creation V1", "statuts_spfpl_cession.docx"),
        ("SPFPL dentistes - apport creation V1", "statuts_spfpl_apport.docx"),
        ("SELAS multi-associes creation V1", "statuts_selas_multi.docx"),
        ("SELAS dentiste pluripersonnelle creation V1", "statuts_selas_multi.docx"),
    ],
)
def test_typed_test_data_button_generates(
    tmp_path: Path, monkeypatch, label: str, statuts_name: str
) -> None:
    from streamlit.testing.v1 import AppTest

    from sydel_doc_engine.front_app import shell

    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui-civil")
    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=180)
    app.selectbox(key="clean_dossier_type").set_value(label)
    app = app.run(timeout=180)

    # Le bouton "donnees de test" remplit le dossier sans saisie manuelle.
    test_data_button = next(b for b in app.button if "test_data" in str(b.key))
    test_data_button.click()
    app = app.run(timeout=180)

    generate_button = next(
        b for b in app.button if str(b.key) == "clean_typed_generate_dossier"
    )
    assert generate_button.disabled is False
    assert not any("Blocage" in item.value for item in app.caption)

    generate_button.click()
    app = app.run(timeout=180)

    download_labels = [item.label for item in app.get("download_button")]
    assert f"Telecharger {statuts_name}" in download_labels
    assert "Telecharger le dossier ZIP" in download_labels


def test_selas_madame_la_presidente_toggle_drives_destinataire() -> None:
    # Parite gold (RAF-003 / Albane 2026-06-10) : la SELAS doit, comme la SELARL,
    # adresser « Madame la Presidente » quand la presidente de l'ordre est une femme
    # (demande d'inscription DOC-034), au lieu de « Monsieur le President » en dur.
    from sydel_doc_engine.front_app import selas_multi_slice as sms

    base = _selas_payload()
    assert sms.build_generation_context(base).ordre.destinataire_appel == (
        "Monsieur le Président"
    )
    feminin = {**_selas_payload(), "ordre_president_feminin": True}
    assert sms.build_generation_context(feminin).ordre.destinataire_appel == (
        "Madame la Présidente"
    )


def test_selas_cession_codes_flow_into_plan_and_orchestrator() -> None:
    # Completude V2 : la SELAS reutilise les sous-formulaires cession SELARL
    # valides (prefix='selas'). Des qu'un contexte cession/bail/scm est saisi,
    # les codes des documents de cession doivent entrer dans le bundle (plan ET
    # codes confies a l'orchestrateur), comme la SELARL.
    from sydel_doc_engine.domain.models import (
        BailContext,
        CessionContext,
        ScmCessionContext,
    )
    from sydel_doc_engine.front_app import selas_multi_slice as sms

    payload = {
        "cession_context": CessionContext.model_validate(
            {"etape": "compromis", "type_cabinet": "dentaire"}
        ),
        "bail_context": BailContext(),
        "scm_cession_context": ScmCessionContext(),
    }
    plan = sms._selas_document_codes(payload)
    orch = sms._orchestrator_codes(payload)
    for code in ("DOC-012", "DOC-007", "DOC-031", "DOC-032", "DOC-033"):
        assert code in plan, f"{code} absent du plan SELAS"
        assert code in orch, f"{code} absent des codes orchestrateur SELAS"
    # ANO-008 : l'appel de fonds (DOC-008) est restreint a la SELARL cote moteur et
    # non clairement requis pour la SELAS au canon -> il ne doit PAS etre inscrit au
    # plan SELAS (sinon annonce mais jamais genere). Question metier flaggee (Albane).
    assert "DOC-008" not in plan
    # Sans cession : aucun code cession ajoute (bundle de creation inchange).
    assert sms._cession_codes({}) == ()


def test_front_selas_dentiste_pluri_uses_dentiste_corpus(
    tmp_path: Path, monkeypatch
) -> None:
    # Cas NOMME « SELAS dentiste pluripersonnelle » : selectionner l'entree puis
    # cliquer « donnees de test » et generer doit produire les STATUTS DENTISTE
    # (corpus chirurgien-dentiste), pas le corpus medecin. Prouve que la cle de
    # type pre-regle bien la profession et bascule le moteur sur le bon corpus.
    from streamlit.testing.v1 import AppTest

    from sydel_doc_engine.front_app import shell

    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui-selas-dentiste")
    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=180)
    app.selectbox(key="clean_dossier_type").set_value(
        "SELAS dentiste pluripersonnelle creation V1"
    )
    app = app.run(timeout=180)

    next(b for b in app.button if "test_data" in str(b.key)).click()
    app = app.run(timeout=180)

    generate_button = next(
        b for b in app.button if str(b.key) == "clean_typed_generate_dossier"
    )
    assert generate_button.disabled is False
    assert not any("Blocage" in item.value for item in app.caption)
    generate_button.click()
    app = app.run(timeout=180)

    statuts_files = list(
        (tmp_path / "ui-selas-dentiste").rglob("statuts_selas_multi.docx")
    )
    assert statuts_files, "Statuts SELAS dentiste non generes."
    text = _docx_text(statuts_files[0])
    # Marqueurs PROPRES au corpus dentiste (absents du corpus medecin).
    assert "l’exercice en commun de la profession de chirurgien-dentiste" in text
    assert "Conseil Départemental de l’Ordre des Chirurgiens-dentistes" in text


def test_front_selas_change_dirigeant_generates(tmp_path: Path, monkeypatch) -> None:
    # Reunion 2026-06-09, feature #1 : on peut designer un autre associe que le
    # premier comme dirigeant ; ses champs DNC se saisissent SOUS lui, et la
    # generation reussit. Prouve le cablage UI checkbox -> president -> DNC.
    from streamlit.testing.v1 import AppTest

    from sydel_doc_engine.front_app import shell

    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui-selas-dir")
    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=180)
    app.selectbox(key="clean_dossier_type").set_value("SELAS multi-associes creation V1")
    app = app.run(timeout=180)

    # Prefill (2 associes, dirigeant = associe 0 par defaut).
    next(b for b in app.button if "test_data" in str(b.key)).click()
    app = app.run(timeout=180)

    # Designer l'associe 1 comme dirigeant a la place de l'associe 0.
    app.checkbox(key="selas_associe_0_is_dirigeant").set_value(False)
    app.checkbox(key="selas_associe_1_is_dirigeant").set_value(True)
    app = app.run(timeout=180)

    def set_text(key: str, value: str) -> None:
        for widget in app.text_input:
            if str(widget.key) == key:
                widget.set_value(value)
                return
        raise KeyError(key)

    # DNC du NOUVEAU dirigeant (associe 1) : apparait sous sa case « Dirigeant ».
    set_text("selas_associe_1_sig_nom_pere", "Paul Martin")
    set_text("selas_associe_1_sig_nom_mere", "Marie Martin")
    set_text("selas_associe_1_sig_adresse_num", "2")
    set_text("selas_associe_1_sig_adresse_voie", "rue Martin")
    set_text("selas_associe_1_sig_adresse_cp", "75000")
    set_text("selas_associe_1_sig_adresse_ville", "Paris")
    set_text("selas_associe_1_sig_date_naissance", "02/02/1982")
    app = app.run(timeout=180)

    generate_button = next(
        b for b in app.button if str(b.key) == "clean_typed_generate_dossier"
    )
    assert generate_button.disabled is False
    assert not any("Blocage" in item.value for item in app.caption)
    generate_button.click()
    app = app.run(timeout=180)

    download_labels = [item.label for item in app.get("download_button")]
    assert "Telecharger statuts_selas_multi.docx" in download_labels
    assert "Telecharger le dossier ZIP" in download_labels


def test_front_today_button_fills_date_non_selarl() -> None:
    # Retour Rafael 2026-06-09 : bouton « Aujourd'hui » sur les dates de TOUS les
    # types (existait deja en SELARL). Preuve sur SCI (non-SELARL) : presence du
    # bouton + remplissage effectif de la date du jour.
    from datetime import date as _date_cls

    from streamlit.testing.v1 import AppTest

    from sydel_doc_engine.front_app.field_derivations import format_french_date

    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=120)
    app.selectbox(key="clean_dossier_type").set_value("SCI creation V1")
    app = app.run(timeout=120)

    today_buttons = [b for b in app.button if str(b.key).endswith("_today")]
    assert today_buttons  # bouton « Aujourd'hui » present sur les dates SCI

    # Vider la date de signature puis cliquer « Aujourd'hui » -> date du jour.
    sig_key = "sci_signature_date"
    next(w for w in app.text_input if str(w.key) == sig_key).set_value("")
    app = app.run(timeout=120)
    next(b for b in app.button if str(b.key) == f"{sig_key}_today").click()
    app = app.run(timeout=120)
    assert next(w for w in app.text_input if str(w.key) == sig_key).value == (
        format_french_date(_date_cls.today())
    )


# --- Retours Albane 2026-06-17 : formulaires civils ---------------------------


def test_civil_forme_sociale_derived_from_structure() -> None:
    # §18.1 : la forme sociale (libelle) n'est plus saisie, elle est derivee.
    assert css.civil_forme_sociale("SCM") == "société civile de moyens"
    assert css.civil_forme_sociale("SCI") == "société civile"
    assert css.civil_forme_sociale("SCI IRIS") == "société civile"
    assert css.civil_forme_sociale("SCS") == "société civile"


def test_civil_build_derives_form_fields() -> None:
    # SCREEN-2 / §18.2 : valeur nominale = capital / nb parts (auto).
    # §18.1 : forme sociale derivee. §18.3 : duree figee 99. §18.4 : lieu = ville siege.
    payload = _civil_base(
        "SCI",
        "sci",
        [_pp("Jean", "Durand", 40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    # On vide les champs derives du payload : le build doit les recalculer.
    payload["forme_sociale"] = ""
    payload["valeur_nominale_part"] = ""
    payload["signature_lieu"] = ""
    payload["duree_societe"] = ""
    ctx = css.build_generation_context(payload)
    assert ctx.statuts_civils.valeur_nominale_part == "10"  # 1000 / 100
    assert ctx.statuts_civils.forme_sociale == "société civile"
    assert ctx.statuts_civils.duree_societe == "99"
    assert ctx.signature.lieu == payload["siege_ville"]


def test_civil_scm_keeps_societe_civile_de_moyens() -> None:
    # §18.1 : la SCM porte « societe civile de moyens » meme si le payload est vide.
    payload = _civil_base(
        "SCM",
        "scm",
        [_pp("Jean", "Durand", 70, 1, 70, 700), _pp("Alice", "Martin", 30, 71, 100, 300)],
    )
    payload["forme_sociale"] = ""
    ctx = css.build_generation_context(payload)
    assert ctx.statuts_civils.forme_sociale == "société civile de moyens"


def test_repeater_assigns_cumulative_part_ranges() -> None:
    # §18.5 : les plages parts debut/fin ne sont plus saisies, elles se derivent de
    # l'ordre + du nombre de parts (contigues 1..N, sans trou ni chevauchement).
    from sydel_doc_engine.domain.models import (
        StatutsCivilsAssocie,
        StatutsCivilsParts,
    )
    from sydel_doc_engine.front_app.associe_repeater import (
        _assign_cumulative_part_ranges,
    )

    def _a(nb: int) -> StatutsCivilsAssocie:
        return StatutsCivilsAssocie(
            type_personne="personne_physique",
            parts=StatutsCivilsParts(nb=nb),
        )

    associes = [_a(40), _a(35), _a(25)]
    _assign_cumulative_part_ranges(associes)
    assert [(a.parts.debut, a.parts.fin) for a in associes] == [(1, 40), (41, 75), (76, 100)]
    assert associes[1].parts.plage_affichee == "41 a 75"


def test_repeater_nationalite_dropdown_lowercased() -> None:
    # §SCREEN-1 : nationalite en deroulant (NATIONALITY_PRESETS), sortie lowercased.
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=120)
    app.selectbox(key="clean_dossier_type").set_value("SCI creation V1")
    app = app.run(timeout=120)

    # Le selectbox de nationalite de l'associe 0 existe (plus de text_input libre).
    choice = next(
        s for s in app.selectbox if str(s.key) == "sci_associe_0_nationalite_choice"
    )
    assert list(choice.options) == [
        "Française",
        "Belge",
        "Portugaise",
        "Suisse",
        "Luxembourgeoise",
        "Autre",
    ]
    assert not any(str(w.key) == "sci_associe_0_nationalite" for w in app.text_input)


def test_civil_non_scm_does_not_collect_profession() -> None:
    # §18.6 : profession demandee uniquement pour la SCM. SCI : pas de champ.
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=120)
    app.selectbox(key="clean_dossier_type").set_value("SCI creation V1")
    app = app.run(timeout=120)
    assert not any(str(w.key) == "sci_associe_0_profession" for w in app.text_input)

    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=120)
    app.selectbox(key="clean_dossier_type").set_value("SCM creation V1")
    app = app.run(timeout=120)
    assert any(str(w.key) == "scm_associe_0_profession" for w in app.text_input)


# --- §17.1 : SELAS UNIPERSONNELLE medecin (DOC-018, generateur rebranche) ------


def test_selas_uni_medecin_present_in_dropdown() -> None:
    # §17.1 : le cas etait orphelin (generateur DOC-018 sans entree de menu). Il
    # doit desormais figurer dans la deroulante, par son nom, generation activee.
    option = dossier_type_by_label("SELAS unipersonnelle medecin creation V1")
    assert option.key == "selas_uni_medecin_v1"
    assert option.structure == "SELAS uni medecin"
    assert option.generation_enabled is True
    assert option.slice_module == "sydel_doc_engine.front_app.selas_uni_medecin_slice"
    # La SELARL reste en premiere position (defaut historique).
    assert dossier_type_labels()[0] == "SELARL creation V1"


def _selas_uni_medecin_payload():
    return {
        "denomination": "SELAS MARTIN",
        "capital_social": "1000",
        "nb_actions_total": 1000,
        "duree": "99 ans",
        "ville_rcs": "Paris",
        "lieu_exercice_adresse": "12 avenue de la Republique, 75011 Paris",
        "siege_num": "10",
        "siege_voie": "rue de la Paix",
        "siege_cp": "75002",
        "siege_ville": "Paris",
        "banque_nom": "BANQUE EXEMPLE",
        "banque_adresse": "1 boulevard Haussmann, 75009 Paris",
        "exercice_debut": "1er janvier",
        "exercice_fin": "31 decembre",
        "exercice_cloture": "31 decembre 2026",
        "civilite": "Monsieur",
        "prenom": "Camille",
        "nom": "Martin",
        "date_naissance": date(1980, 1, 2),
        "ville_naissance": "Paris",
        "departement_naissance": "75",
        "nationalite": "francaise",
        "titre_affichage": "Docteur",
        "adresse_num": "5",
        "adresse_voie": "5 rue Royale",
        "adresse_cp": "75008",
        "adresse_ville": "Paris",
        "nom_pere": "Pierre Martin",
        "nom_mere": "Anne Martin",
        "situation_maritale": "marie",
        "regime_matrimonial": "communaute legale",
        "conjoint_civilite": "Madame",
        "conjoint_prenom": "Alice",
        "conjoint_nom": "Martin",
        "ordre_conseil": "Ordre des medecins",
        "departement_ordre": "Paris",
        "numero_ordre": "12345",
        "numero_rpps": "10000000001",
        "ordre_ville": "Paris",
        "ordre_cp": "75008",
        "ordre_adresse_ligne_1": "1 rue de l'Ordre",
        "signature_lieu": "Paris",
        "signature_date": date(2026, 5, 14),
        "decision_date": date(2026, 5, 14),
    }


def test_selas_uni_medecin_generates_doc018_bundle(tmp_path: Path) -> None:
    # §17.1 : le bundle de creation expose DOC-018 (statuts SELAS medecin) + tronc
    # commun. Genere proprement (aucun token residuel) et porte la forme SELAS.
    from sydel_doc_engine.front_app import selas_uni_medecin_slice as uni

    payload = _selas_uni_medecin_payload()
    plan = uni.build_selas_uni_medecin_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-018", "DOC-001", "DOC-002", "DOC-003", "DOC-004", "DOC-034")

    generated = uni.generate_dossier(payload, tmp_path / "selas-uni-medecin")
    _assert_bundle_clean(
        generated,
        {
            "statuts_selas_medecin.docx",
            "declaration_non_condamnation.docx",
            "autorisation_domiciliation.docx",
            "procuration.docx",
            "pv_nomination_gerant.docx",
            "demande_inscription_ordre.docx",
        },
    )
    statuts_text = _docx_text(
        next(p for p in generated.docx_paths if p.name == "statuts_selas_medecin.docx")
    )
    assert "SELAS MARTIN" in statuts_text


def test_selas_uni_medecin_regime_communautaire_generates_doc005_006(tmp_path: Path) -> None:
    # RAF-001 (regression) : SELAS uni medecin + regime communautaire bloquait la
    # generation (CODE-RC-001 : date_courrier_avertissement absente de l'adaptateur
    # SELARL). Aucun test n'exercait ce chemin -> le bug est passe. On verrouille :
    # regime actif -> DOC-005/006 generes proprement, comme tous les autres types.
    from sydel_doc_engine.front_app import selas_uni_medecin_slice as uni

    payload = _selas_uni_medecin_payload()
    payload["regime_communautaire"] = True
    plan = uni.build_selas_uni_medecin_plan(payload)
    assert plan.can_generate is True
    assert "DOC-005" in plan.document_codes
    assert "DOC-006" in plan.document_codes

    generated = uni.generate_dossier(payload, tmp_path / "selas-uni-medecin-regime")
    names = {p.name for p in generated.docx_paths}
    assert "lettre_renonciation_associe.docx" in names
    assert "lettre_avertissement_conjoint.docx" in names
    for path in generated.docx_paths:
        _assert_clean(_docx_text(path))


def test_selas_uni_medecin_context_is_selas_actions() -> None:
    # §17.1 : le contexte derive du parcours SELARL uni est bien transforme en
    # SELAS medecin (structure SELAS, overlay selas_medecin, titres = actions,
    # dirigeant President). Garde-fou anti-detournement du chemin SELARL.
    from sydel_doc_engine.front_app import selas_uni_medecin_slice as uni

    ctx = uni.build_generation_context(_selas_uni_medecin_payload())
    assert ctx.structure == "SELAS"
    assert ctx.statuts_sel.overlay == "selas_medecin"
    assert ctx.societe.forme_sociale_abregee == "SELAS"
    assert ctx.capital.type_titre == "actions"
    assert ctx.dirigeant_nomine.fonction_affichage == "président"
    assert ctx.dirigeant_nomine.duree_mandat == "illimitée"
