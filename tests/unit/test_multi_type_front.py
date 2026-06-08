from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
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
    assert plan.document_codes == (
        "DOC-025",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
    )
    generated = css.generate_dossier(payload, tmp_path / "scm")
    _assert_bundle_clean(
        generated,
        _TRONC_DOCS | {"statuts_scm.docx", "demande_inscription_ordre.docx"},
    )


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
        "denomination": "SPFPL MARTIN",
        "siege": "10 rue de la Paix, 75002 Paris",
        "capital_social": "60000",
        "valeur_nominale_action": "100",
        "civilite": "Docteur",
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


def test_spfpl_cession_slice_generates_clean(tmp_path: Path) -> None:
    payload = _spfpl_payload("SPFPL cession")
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-035", "DOC-001", "DOC-002", "DOC-003", "DOC-004", "DOC-034")
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-cession")
    _assert_bundle_clean(generated, _SPFPL_BUNDLE_TRONC | {"statuts_spfpl_cession.docx"})


def test_spfpl_apport_slice_generates_clean(tmp_path: Path) -> None:
    payload = _spfpl_payload("SPFPL apport")
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-036", "DOC-001", "DOC-002", "DOC-003", "DOC-004", "DOC-034")
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-apport")
    _assert_bundle_clean(generated, _SPFPL_BUNDLE_TRONC | {"statuts_spfpl_apport.docx"})


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
    )
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-cession-regime")
    _assert_bundle_clean(
        generated,
        _SPFPL_BUNDLE_TRONC | {"statuts_spfpl_cession.docx"} | _REGIME_DOCS,
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
        _SPFPL_BUNDLE_TRONC | {"statuts_spfpl_apport.docx"} | _REGIME_DOCS,
    )


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


def test_selas_blocks_incoherent_actions_sum() -> None:
    payload = _selas_payload()
    payload["associes"][1].nb_actions = 10  # 75 + 10 != 100
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is False
    assert any("Somme des actions" in b for b in plan.blockers)


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


def test_selas_regime_on_requires_conjoint() -> None:
    payload = _selas_payload()
    payload["regime_communautaire"] = True  # toggle ON sans saisies conjoint
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is False
    assert any("regime communautaire" in b.casefold() for b in plan.blockers)


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
        "SAS SPFPL medecins creation V1",
        "SPFPL cession creation V1",
        "SPFPL apport creation V1",
        "SELAS multi-associes creation V1",
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

    society = {
        "sci_denomination": "SCI EXEMPLE",
        "sci_forme_sociale": "societe civile immobiliere",
        "sci_capital_social": "1000",
        "sci_valeur_nominale_part": "10",
        "sci_duree_societe": "99",
        "sci_siege_num": "10",
        "sci_siege_voie": "rue de la Paix",
        "sci_siege_cp": "75002",
        "sci_siege_ville": "Paris",
        "sci_ville_rcs": "Paris",
        "sci_banque_nom": "BANQUE",
        "sci_banque_adresse": "1 rue Banque, 75009 Paris",
        "sci_date_cloture_premier_exercice": "31 decembre 2026",
        "sci_signature_lieu": "Paris",
        "sci_signature_date": "15/05/2026",
        # Documents communs (signataire = 1er associe physique).
        "sci_signataire_nom_pere": "Pierre Durand",
        "sci_signataire_nom_mere": "Anne Durand",
        "sci_signataire_adresse_num": "1",
        "sci_signataire_adresse_voie": "rue Exemple",
        "sci_signataire_adresse_cp": "75000",
        "sci_signataire_adresse_ville": "Paris",
        "sci_signataire_fonction": "gerant",
        "sci_signataire_titre": "Docteur",
        "sci_decision_date": "15/05/2026",
    }
    for key, value in society.items():
        set_text(key, value)
    app = app.run(timeout=180)

    associes_text = {
        "sci_associe_0_prenom": "Jean",
        "sci_associe_0_nom": "Durand",
        "sci_associe_0_date_naissance": "1 janvier 1980",
        "sci_associe_0_ville_naissance": "Paris",
        "sci_associe_0_departement_naissance": "75",
        "sci_associe_0_nationalite": "francaise",
        "sci_associe_0_situation_maritale": "celibataire",
        "sci_associe_0_profession": "medecin",
        "sci_associe_0_adresse": "1 rue Exemple, 75000 Paris",
        "sci_associe_0_apport_montant": "400",
        "sci_associe_1_prenom": "Alice",
        "sci_associe_1_nom": "Martin",
        "sci_associe_1_date_naissance": "2 fevrier 1982",
        "sci_associe_1_ville_naissance": "Lyon",
        "sci_associe_1_departement_naissance": "69",
        "sci_associe_1_nationalite": "francaise",
        "sci_associe_1_situation_maritale": "celibataire",
        "sci_associe_1_profession": "medecin",
        "sci_associe_1_adresse": "2 rue Exemple, 69000 Lyon",
        "sci_associe_1_apport_montant": "600",
    }
    for key, value in associes_text.items():
        set_text(key, value)
    associes_numbers = {
        "sci_associe_0_nb_titres": 40,
        "sci_associe_0_parts_debut": 1,
        "sci_associe_0_parts_fin": 40,
        "sci_associe_1_nb_titres": 60,
        "sci_associe_1_parts_debut": 41,
        "sci_associe_1_parts_fin": 100,
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
        ("SAS SPFPL medecins creation V1", "statuts_sas_spfpl_medecins.docx"),
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
