from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest
from streamlit.testing.v1 import AppTest

from sydel_doc_engine.app.front_dossier_entry import (
    FrontDossierSimpleEntry,
    build_front_dossier_entry_dossier,
)
from sydel_doc_engine.app.front_generation_actions import (
    FRONT_GENERATION_EXCLUDED_DOC_CODES,
    FRONT_GENERATION_SUPPORTED_DOC_CODES,
    FrontGenerationBlockedError,
    build_front_generation_context,
    front_generation_readiness,
    generate_front_docx,
    generate_front_zip,
)
from sydel_doc_engine.front_data.document_status import DocumentStatus
from sydel_doc_engine.rendering.pdf_export import is_pdf_export_available


def test_front_generation_readiness_targets_only_simple_selarl_docs() -> None:
    dossier = build_front_dossier_entry_dossier(_complete_generation_entry())

    readiness = front_generation_readiness(dossier)
    context = build_front_generation_context(dossier)

    assert set(FRONT_GENERATION_SUPPORTED_DOC_CODES).issuperset(readiness.target_doc_codes)
    assert readiness.target_doc_codes == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-017",
    )
    assert readiness.generable_doc_codes == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-017",
    )
    assert set(FRONT_GENERATION_EXCLUDED_DOC_CODES).isdisjoint(readiness.target_doc_codes)
    assert readiness.can_generate_docx is True
    assert context.structure == "SELARL"
    assert context.societe is not None
    assert context.societe.ville_rcs == "Paris"
    assert context.capital is not None
    assert context.capital.nb_parts_total == 100
    assert context.ordre is not None
    assert context.mandataire is not None
    assert context.statuts_sel is not None
    assert context.statuts_sel.overlay == "selarl_medecin"


def test_front_generation_readiness_switches_statuts_for_dentiste() -> None:
    dossier = build_front_dossier_entry_dossier(
        _complete_generation_entry(
            profession="chirurgien_dentiste",
            ordre_profession_signataire_affichee="chirurgien-dentiste",
            ordre_profession_ligne_destinataire="chirurgiens-dentistes",
            ordre_profession_reglementee_pluriel="chirurgiens-dentistes",
            statuts_associe_qualification_principale="orthodontiste",
        )
    )

    readiness = front_generation_readiness(dossier)
    context = build_front_generation_context(dossier)

    assert "DOC-016" in readiness.target_doc_codes
    assert "DOC-017" not in readiness.target_doc_codes
    assert readiness.can_generate_docx is True
    assert context.statuts_sel is not None
    assert context.statuts_sel.overlay == "selarl_dentiste"


def test_front_generation_regime_communautaire_adds_doc_005_and_excludes_reserve() -> None:
    dossier = build_front_dossier_entry_dossier(
        _complete_generation_entry(regime_communautaire=True)
    )

    readiness = front_generation_readiness(dossier)
    context = build_front_generation_context(dossier)
    statuses = {status.doc_code: status.status for status in readiness.summary.documents}

    assert "DOC-005" in readiness.target_doc_codes
    assert "DOC-006" in readiness.excluded_doc_codes
    assert statuses["DOC-005"] is DocumentStatus.GENERABLE
    assert statuses["DOC-006"] is DocumentStatus.GENERABLE_WITH_RESERVE
    assert readiness.can_generate_docx is True
    assert context.regime_communautaire is not None


@pytest.mark.parametrize(
    ("overrides", "pending_doc_codes"),
    (
        (
            {"cession": True, "cabinet_type": "medical"},
            {"DOC-007", "DOC-008", "DOC-009", "DOC-010"},
        ),
        (
            {
                "profession": "chirurgien_dentiste",
                "cession": True,
                "cabinet_type": "dentaire",
                "ordre_profession_signataire_affichee": "chirurgien-dentiste",
                "ordre_profession_ligne_destinataire": "chirurgiens-dentistes",
                "ordre_profession_reglementee_pluriel": "chirurgiens-dentistes",
            },
            {"DOC-007", "DOC-008", "DOC-011", "DOC-012"},
        ),
        (
            {"scm_cession": True},
            {"DOC-031", "DOC-032", "DOC-033"},
        ),
    ),
)
def test_front_generation_marks_complex_scenarios_as_context_incomplete(
    overrides: dict[str, object],
    pending_doc_codes: set[str],
) -> None:
    dossier = build_front_dossier_entry_dossier(_complete_generation_entry(**overrides))

    readiness = front_generation_readiness(dossier)
    statuses = {status.doc_code: status.status for status in readiness.summary.documents}

    assert pending_doc_codes.issubset(readiness.target_doc_codes)
    assert all(
        statuses[doc_code] is DocumentStatus.CONTEXT_INCOMPLETE
        for doc_code in pending_doc_codes
    )
    assert readiness.can_generate_docx is False


def test_front_generation_creates_docx_and_zip_for_simple_scope() -> None:
    dossier = build_front_dossier_entry_dossier(_complete_generation_entry())
    output_dir = Path("artifacts") / "test_front_generation_actions" / "simple_scope"
    output_dir.mkdir(parents=True, exist_ok=True)

    result = generate_front_docx(dossier, output_dir)
    zip_path = generate_front_zip(result.output_dir, result.docx_paths)

    assert {path.name for path in result.docx_paths} == {
        "declaration_non_condamnation.docx",
        "autorisation_domiciliation.docx",
        "procuration.docx",
        "pv_nomination_gerant.docx",
        "demande_inscription_ordre.docx",
        "statuts_selarl_medecin.docx",
    }
    assert all(path.is_file() for path in result.docx_paths)
    with ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "manifest.json" in names
    assert "declaration_non_condamnation.docx" in names


def test_front_generation_blocks_incomplete_dossier() -> None:
    dossier = build_front_dossier_entry_dossier(
        FrontDossierSimpleEntry(prenom="Alice", nom="Martin")
    )
    output_dir = Path("artifacts") / "test_front_generation_actions" / "blocked_scope"
    output_dir.mkdir(parents=True, exist_ok=True)

    readiness = front_generation_readiness(dossier)

    assert readiness.can_generate_docx is False
    assert set(readiness.blocked_doc_codes) == {
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-017",
        "DOC-034",
    }
    with pytest.raises(FrontGenerationBlockedError):
        generate_front_docx(dossier, output_dir)


def test_front_generation_never_includes_manual_or_reserved_docs() -> None:
    dossier = build_front_dossier_entry_dossier(
        _complete_generation_entry(
            regime_communautaire=True,
            derogation=True,
            ordre_derogation_mention_manuelle="avec demande de derogation jointe",
        )
    )

    readiness = front_generation_readiness(dossier)
    statuses = {status.doc_code: status.status for status in readiness.summary.documents}

    assert "DOC-005" in statuses
    assert "DOC-006" in statuses
    assert "DOC-013" in statuses
    assert "DOC-014" in statuses
    assert "DOC-006" in readiness.excluded_doc_codes
    assert "DOC-013" in readiness.excluded_doc_codes
    assert "DOC-014" in readiness.excluded_doc_codes
    assert statuses["DOC-006"] is DocumentStatus.GENERABLE_WITH_RESERVE
    assert statuses["DOC-013"] is DocumentStatus.MANUAL_ONLY
    assert statuses["DOC-014"] is DocumentStatus.MANUAL_ONLY


def test_front_generation_module_does_not_depend_on_business_wizard() -> None:
    source = Path("src/sydel_doc_engine/app/front_generation_actions.py").read_text(
        encoding="utf-8"
    )

    assert "business_wizard" not in source


def test_streamlit_new_front_generates_docx_then_zip() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/app/streamlit_app.py").run(timeout=120)

    _fill_front_generation_fields(app)
    app.run(timeout=120)

    generate_button = _button_by_label(app, "Generer les DOCX")
    assert generate_button.disabled is False

    generate_button.click().run(timeout=120)

    assert any("6 DOCX generes depuis le nouveau front." in item.value for item in app.success)
    generated_paths = [Path(path) for path in app.session_state.front_generation_docx_paths]
    assert {path.name for path in generated_paths} == {
        "declaration_non_condamnation.docx",
        "autorisation_domiciliation.docx",
        "procuration.docx",
        "pv_nomination_gerant.docx",
        "demande_inscription_ordre.docx",
        "statuts_selarl_medecin.docx",
    }
    assert all(path.is_file() for path in generated_paths)

    zip_button = _button_by_label(app, "Generer le ZIP")
    assert zip_button.disabled is False
    zip_button.click().run(timeout=120)
    assert Path(app.session_state.front_generation_zip_path).is_file()


def test_streamlit_new_front_hides_pdf_when_backend_is_unavailable() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/app/streamlit_app.py").run(timeout=120)

    button_labels = {button.label for button in app.button}
    if is_pdf_export_available():
        assert "Generer les PDF" in button_labels
    else:
        assert "Generer les PDF" not in button_labels


def test_streamlit_new_front_shows_runtime_blocker_in_generation() -> None:
    app = AppTest.from_file("src/sydel_doc_engine/app/streamlit_app.py").run(timeout=120)

    _fill_front_generation_fields(app)
    app.text_input(key="front_entry_signature_date").set_value("24/05/2026")
    app.run(timeout=120)

    assert _button_by_label(app, "Generer les DOCX").disabled is True
    assert any(
        "signature.date doit etre au format AAAA-MM-JJ." in item.value
        for item in app.markdown
    )


def _complete_generation_entry(**overrides: object) -> FrontDossierSimpleEntry:
    values = {
        "civilite_affichage": "Madame",
        "genre": "feminin",
        "prenom": "Alice",
        "nom": "Martin",
        "date_naissance": "1980-01-01",
        "ville_naissance": "Lyon",
        "departement_naissance": "Rhone",
        "nationalite": "francaise",
        "nom_pere": "Jean Martin",
        "nom_mere": "Claire Durand",
        "adresse_personnelle": "12 rue Exemple, 75001 Paris",
        "societe_denomination": "SELARL Alice Martin",
        "societe_capital_social": "10 000 euros",
        "societe_ville_rcs": "Paris",
        "siege_social": "12 rue Exemple, 75001 Paris",
        "capital_titres_nombre_total": "100",
        "capital_titres_valeur_nominale": "100 euros",
        "decision_date": "2026-05-24",
        "reunion_date_lettres": "vingt-quatre mai deux mille vingt-six",
        "reunion_heure": "10 heures",
        "signature_lieu": "Paris",
        "signature_date": "2026-05-24",
        "signature_nombre_exemplaires": "3",
        "signature_prestataire": "Yousign",
        "titre_affichage": "Dr",
        "ordre_conseil_departemental_libelle": "Conseil departemental de l'Ordre",
        "ordre_destinataire_appel": "Madame la Presidente",
        "ordre_profession_signataire_affichee": "medecin",
        "ordre_profession_ligne_destinataire": "medecins",
        "ordre_profession_reglementee_pluriel": "medecins",
        "ordre_adresse_ligne_1": "6 rue du Conseil",
        "ordre_adresse_cp": "75001",
        "ordre_adresse_ville": "Paris",
        "ordre_numero": "12345",
        "ordre_numero_rpps": "10000000001",
        "mandataire_civilite_affichage": "Madame",
        "mandataire_prenom": "Sophie",
        "mandataire_nom": "Durand",
        "mandataire_fonction": "juriste",
        "mandataire_cabinet": "DAAT",
        "statuts_capital_social_lettres": "dix mille",
        "statuts_apport_montant": "10 000",
        "statuts_apport_montant_lettres": "dix mille",
        "statuts_nombre_titres_total_lettres": "cent",
        "statuts_valeur_nominale_titre_lettres": "cent euros",
        "statuts_associe_qualification_principale": "cardiologue",
        "statuts_associe_situation_maritale": "celibataire",
        "statuts_associe_regime_matrimonial": "neant",
        "conjoint_civilite_affichage": "Madame",
        "conjoint_prenom": "Claire",
        "conjoint_nom": "Martin",
        "conjoint_adresse": "14 rue Exemple, 75001 Paris",
        "depot_banque_nom": "BANQUE EXEMPLE",
        "depot_banque_adresse": "1 boulevard Haussmann, 75009 Paris",
        "exercice_social_debut": "1er janvier",
        "exercice_social_fin": "31 decembre",
        "exercice_social_date_cloture_premier_exercice": "31 decembre 2026",
        "exercice_lieu_principal_adresse": "12 avenue de la Republique, 75011 Paris",
        "gerance_seuil_achat_materiel": "10 000 euros",
        "gerance_seuil_emprunt": "50 000 euros",
        "document_nombre_exemplaires_lettres": "trois",
        "regime_apport_montant": "10 000",
        "regime_apport_montant_lettres": "dix mille",
        "regime_matrimonial": "communaute legale",
        "regime_qualite_renoncee": "associe",
        "regime_date_courrier_avertissement": "2026-05-24",
        "regime_renonciation_lieu_signature": "Paris",
        "regime_renonciation_date_signature": "2026-05-24",
        "regime_renonciation_nombre_exemplaires_lettres": "trois",
        "regime_avertissement_date_signature": "2026-05-24",
    }
    values.update(overrides)
    return FrontDossierSimpleEntry(**values)


def _fill_front_generation_fields(app: AppTest) -> None:
    app.selectbox(key="front_entry_person_civilite").set_value("Madame")
    app.selectbox(key="front_entry_person_genre").set_value("feminin")
    app.text_input(key="front_entry_person_titre").set_value("Dr")
    app.selectbox(key="front_entry_mandataire_civilite").set_value("Madame")
    for key, value in (
        ("front_entry_person_prenom", "Alice"),
        ("front_entry_person_nom", "Martin"),
        ("front_entry_person_date_naissance", "1980-01-01"),
        ("front_entry_person_ville_naissance", "Lyon"),
        ("front_entry_person_departement_naissance", "Rhone"),
        ("front_entry_person_nationalite", "francaise"),
        ("front_entry_person_nom_pere", "Jean Martin"),
        ("front_entry_person_nom_mere", "Claire Durand"),
        ("front_entry_person_adresse_personnelle", "12 rue Exemple, 75001 Paris"),
        ("front_entry_company_denomination", "SELARL Alice Martin"),
        ("front_entry_company_capital_social", "10 000 euros"),
        ("front_entry_company_ville_rcs", "Paris"),
        ("front_entry_company_siege_social", "12 rue Exemple, 75001 Paris"),
        ("front_entry_capital_titres_nombre_total", "100"),
        ("front_entry_capital_titres_valeur_nominale", "100 euros"),
        ("front_entry_decision_date", "2026-05-24"),
        ("front_entry_reunion_date_lettres", "vingt-quatre mai deux mille vingt-six"),
        ("front_entry_reunion_heure", "10 heures"),
        ("front_entry_signature_lieu", "Paris"),
        ("front_entry_signature_date", "2026-05-24"),
        ("front_entry_signature_nombre_exemplaires", "3"),
        ("front_entry_signature_prestataire", "Yousign"),
        ("front_entry_order_conseil", "Conseil departemental de l'Ordre"),
        ("front_entry_order_destinataire_appel", "Madame la Presidente"),
        ("front_entry_order_profession_signataire", "medecin"),
        ("front_entry_order_profession_destinataire", "medecins"),
        ("front_entry_order_profession_pluriel", "medecins"),
        ("front_entry_order_adresse_ligne_1", "6 rue du Conseil"),
        ("front_entry_order_adresse_cp", "75001"),
        ("front_entry_order_adresse_ville", "Paris"),
        ("front_entry_order_numero", "12345"),
        ("front_entry_order_numero_rpps", "10000000001"),
        ("front_entry_mandataire_prenom", "Sophie"),
        ("front_entry_mandataire_nom", "Durand"),
        ("front_entry_mandataire_fonction", "juriste"),
        ("front_entry_mandataire_cabinet", "DAAT"),
        ("front_entry_statuts_capital_lettres", "dix mille"),
        ("front_entry_statuts_apport_montant", "10 000"),
        ("front_entry_statuts_apport_montant_lettres", "dix mille"),
        ("front_entry_statuts_titres_total_lettres", "cent"),
        ("front_entry_statuts_valeur_nominale_lettres", "cent euros"),
        ("front_entry_statuts_qualification", "cardiologue"),
        ("front_entry_statuts_situation_maritale", "celibataire"),
        ("front_entry_statuts_regime_matrimonial", "neant"),
        ("front_entry_depot_banque_nom", "BANQUE EXEMPLE"),
        ("front_entry_depot_banque_adresse", "1 boulevard Haussmann, 75009 Paris"),
        ("front_entry_exercice_social_debut", "1er janvier"),
        ("front_entry_exercice_social_fin", "31 decembre"),
        ("front_entry_exercice_social_cloture", "31 decembre 2026"),
        ("front_entry_exercice_lieu_adresse", "12 avenue de la Republique, 75011 Paris"),
        ("front_entry_gerance_seuil_achat", "10 000 euros"),
        ("front_entry_gerance_seuil_emprunt", "50 000 euros"),
        ("front_entry_document_exemplaires_lettres", "trois"),
    ):
        app.text_input(key=key).set_value(value)


def _button_by_label(app: AppTest, label: str):
    matching = [widget for widget in app.button if widget.label == label]
    assert len(matching) == 1
    return matching[0]
