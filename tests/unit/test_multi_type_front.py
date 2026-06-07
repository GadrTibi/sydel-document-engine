from __future__ import annotations

from datetime import date
from pathlib import Path

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
    return {
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
    }


# --- Generation par type (smoke, 0 placeholder residuel) ----------------------


def test_sci_slice_generates_clean(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCI",
        "sci",
        [_pp("Jean", "Durand", 40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-020",)
    generated = css.generate_dossier(payload, tmp_path / "sci")
    names = {p.name for p in generated.docx_paths}
    assert "statuts_sci.docx" in names
    _assert_clean(_docx_text(generated.docx_paths[0]))


def test_scm_slice_generates_clean(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCM",
        "scm",
        [_pm(70, 1, 70, 700), _pp("Alice", "Martin", 30, 71, 100, 300)],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-025",)
    generated = css.generate_dossier(payload, tmp_path / "scm")
    assert "statuts_scm.docx" in {p.name for p in generated.docx_paths}
    _assert_clean(_docx_text(generated.docx_paths[0]))


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
    assert plan.document_codes == ("DOC-019",)
    generated = css.generate_dossier(payload, tmp_path / "scs")
    assert "statuts_scs.docx" in {p.name for p in generated.docx_paths}
    _assert_clean(_docx_text(generated.docx_paths[0]))


def test_sci_iris_slice_generates_clean(tmp_path: Path) -> None:
    payload = _civil_base(
        "SCI IRIS",
        "sci_iris",
        [_pm(40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
    )
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-021",)
    generated = css.generate_dossier(payload, tmp_path / "iris")
    assert "statuts_sci_iris.docx" in {p.name for p in generated.docx_paths}
    _assert_clean(_docx_text(generated.docx_paths[0]))


def test_sci_blocks_personne_morale() -> None:
    payload = _civil_base("SCI", "sci", [_pm(100, 1, 100, 1000)])
    plan = css.build_civil_plan(payload)
    assert plan.can_generate is False
    assert any("personne morale" in b.casefold() for b in plan.blockers)


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
        "capital_social": "12000",
        "nb_actions_total": 120,
        "valeur_nominale_action": "100",
        "civilite": "Docteur",
        "prenom": "Camille",
        "nom": "Martin",
        "genre": Gender.MASCULIN,
        "qualification_principale": "Medecin cardiologue",
        "date_naissance": "2 janvier 1980",
        "ville_naissance": "Paris",
        "departement_naissance": "75",
        "nationalite": "francaise",
        "regime_matrimonial": "la communaute legale",
        "adresse": "5 rue Royale, 75008 Paris",
        "conjoint_civilite": "Madame",
        "conjoint_prenom": "Alice",
        "conjoint_nom": "Martin",
        "ordre_departement": "Paris",
        "numero_ordre": "12345",
        "numero_rpps": "10000000001",
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
    assert plan.document_codes == ("DOC-015",)
    generated = sas_slice.generate_dossier(payload, tmp_path / "sas")
    assert "statuts_sas_spfpl_medecins.docx" in {p.name for p in generated.docx_paths}
    _assert_clean(_docx_text(generated.docx_paths[0]))


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
        "conjoint_civilite": "Madame",
        "conjoint_prenom": "Alice",
        "conjoint_nom": "Martin",
        "ordre_departement": "Paris",
        "numero_ordre": "12345",
        "numero_rpps": "10000000001",
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


def test_spfpl_cession_slice_generates_clean(tmp_path: Path) -> None:
    payload = _spfpl_payload("SPFPL cession")
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-035",)
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-cession")
    assert "statuts_spfpl_cession.docx" in {p.name for p in generated.docx_paths}
    _assert_clean(_docx_text(generated.docx_paths[0]))


def test_spfpl_apport_slice_generates_clean(tmp_path: Path) -> None:
    payload = _spfpl_payload("SPFPL apport")
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-036",)
    generated = spfpl_slice.generate_dossier(payload, tmp_path / "spfpl-apport")
    assert "statuts_spfpl_apport.docx" in {p.name for p in generated.docx_paths}
    _assert_clean(_docx_text(generated.docx_paths[0]))


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
    }


def test_selas_multi_slice_generates_clean(tmp_path: Path) -> None:
    payload = _selas_payload()
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is True
    assert plan.document_codes == ("DOC-044",)
    generated = selas_multi_slice.generate_dossier(payload, tmp_path / "selas")
    assert "statuts_selas_multi.docx" in {p.name for p in generated.docx_paths}
    _assert_clean(_docx_text(generated.docx_paths[0]))


def test_selas_blocks_incoherent_actions_sum() -> None:
    payload = _selas_payload()
    payload["associes"][1].nb_actions = 10  # 75 + 10 != 100
    plan = selas_multi_slice.build_selas_plan(payload)
    assert plan.can_generate is False
    assert any("Somme des actions" in b for b in plan.blockers)


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
