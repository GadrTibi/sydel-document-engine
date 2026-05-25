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

    assert readiness.target_doc_codes == FRONT_GENERATION_SUPPORTED_DOC_CODES
    assert readiness.generable_doc_codes == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    )
    assert set(readiness.excluded_doc_codes) == set(FRONT_GENERATION_EXCLUDED_DOC_CODES)
    assert readiness.can_generate_docx is True
    assert context.structure == "SELARL"
    assert context.societe is not None
    assert context.societe.ville_rcs == "Paris"
    assert context.capital is not None
    assert context.capital.nb_parts_total == 100


def test_front_generation_creates_docx_and_zip_for_simple_scope(tmp_path: Path) -> None:
    dossier = build_front_dossier_entry_dossier(_complete_generation_entry())

    result = generate_front_docx(dossier, tmp_path)
    zip_path = generate_front_zip(result.output_dir, result.docx_paths)

    assert [path.name for path in result.docx_paths] == [
        "declaration_non_condamnation.docx",
        "autorisation_domiciliation.docx",
        "procuration.docx",
        "pv_nomination_gerant.docx",
    ]
    assert all(path.is_file() for path in result.docx_paths)
    with ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "manifest.json" in names
    assert "declaration_non_condamnation.docx" in names


def test_front_generation_blocks_incomplete_dossier(tmp_path: Path) -> None:
    dossier = build_front_dossier_entry_dossier(
        FrontDossierSimpleEntry(prenom="Alice", nom="Martin")
    )

    readiness = front_generation_readiness(dossier)

    assert readiness.can_generate_docx is False
    assert set(readiness.blocked_doc_codes) == {
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    }
    with pytest.raises(FrontGenerationBlockedError):
        generate_front_docx(dossier, tmp_path)


def test_front_generation_never_includes_manual_or_reserved_docs() -> None:
    dossier = build_front_dossier_entry_dossier(_complete_generation_entry())

    readiness = front_generation_readiness(dossier)
    statuses = {status.doc_code: status.status for status in readiness.summary.documents}

    assert set(statuses) == {"DOC-001", "DOC-002", "DOC-003", "DOC-004"}
    assert "DOC-006" in readiness.excluded_doc_codes
    assert "DOC-013" in readiness.excluded_doc_codes
    assert "DOC-014" in readiness.excluded_doc_codes
    assert all(status is DocumentStatus.GENERABLE for status in statuses.values())


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

    assert any("4 DOCX generes depuis le nouveau front." in item.value for item in app.success)
    generated_paths = [Path(path) for path in app.session_state.front_generation_docx_paths]
    assert {path.name for path in generated_paths} == {
        "declaration_non_condamnation.docx",
        "autorisation_domiciliation.docx",
        "procuration.docx",
        "pv_nomination_gerant.docx",
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
    }
    values.update(overrides)
    return FrontDossierSimpleEntry(**values)


def _fill_front_generation_fields(app: AppTest) -> None:
    app.selectbox(key="front_entry_person_civilite").set_value("Madame")
    app.selectbox(key="front_entry_person_genre").set_value("feminin")
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
    ):
        app.text_input(key=key).set_value(value)


def _button_by_label(app: AppTest, label: str):
    matching = [widget for widget in app.button if widget.label == label]
    assert len(matching) == 1
    return matching[0]
