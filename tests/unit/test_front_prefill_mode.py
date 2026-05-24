from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.app.business_wizard import (
    STATUS_MANUAL_ONLY,
    evaluate_business_wizard,
)
from sydel_doc_engine.app.test_prefill_presets import (
    business_test_prefill_by_label,
    business_test_prefill_front_data_profile,
    business_test_prefill_front_dossier,
    business_test_prefill_input,
    business_test_prefill_presets,
    business_test_prefill_status_summary,
    business_test_prefill_widget_keys,
)
from sydel_doc_engine.front_data.document_status import DocumentStatus
from sydel_doc_engine.front_data.models import BusinessRole, OperationType
from sydel_doc_engine.front_data.unit_document_mode import (
    build_unit_document_plan,
    unit_document_v1_supported_codes,
)


def test_business_prefill_controls_remain_assistant_only() -> None:
    source = Path("src/sydel_doc_engine/app/streamlit_app.py").read_text(encoding="utf-8")
    business_mode = source.split("def _render_single_document_mode", maxsplit=1)[0]
    single_document_mode = source.split("def _render_single_document_mode", maxsplit=1)[1]
    single_document_mode = single_document_mode.split(
        "def _render_technical_mode",
        maxsplit=1,
    )[0]
    technical_mode = source.split("def _render_technical_mode", maxsplit=1)[1]

    assert "_render_business_prefill_controls()" in business_mode
    assert "_render_business_prefill_controls()" not in single_document_mode
    assert "_render_business_prefill_controls()" not in technical_mode


def test_prefill_presets_are_backed_by_front_data_profiles() -> None:
    profile_source = Path(
        "src/sydel_doc_engine/front_data/test_prefill_presets.py"
    ).read_text(encoding="utf-8")

    assert "streamlit" not in profile_source
    assert "session_state" not in profile_source
    assert tuple(preset.key for preset in business_test_prefill_presets()) == (
        "selarl_medecin_unipersonnelle_simple",
        "selarl_dentiste_regime_site",
        "selarl_medecin_cession_bail_financement",
        "sci_simple",
    )
    for preset in business_test_prefill_presets():
        assert preset.front_data_profile.key == preset.key
        assert business_test_prefill_by_label(preset.label) is preset


def test_selarl_simple_prefill_is_generable_in_wizard_and_front_data() -> None:
    label = _label_for_key("selarl_medecin_unipersonnelle_simple")
    data = business_test_prefill_input(label)
    validation = evaluate_business_wizard(data)
    status_by_code = _status_by_code(label)
    dossier = business_test_prefill_front_dossier(label)

    assert data.selarl_dossier_unipersonnel is True
    assert data.associes[0].prenom == data.personne_prenom
    assert data.domiciliation_adresse_affichee == "14 rue de Lisbonne, 75008 Paris"
    assert validation.can_generate_docx is True
    assert validation.generatable_document_codes == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    )
    assert {
        code
        for code, status in status_by_code.items()
        if status.status is DocumentStatus.GENERABLE
    } == {"DOC-001", "DOC-002", "DOC-003", "DOC-004"}
    assert _role_targets(dossier, BusinessRole.PRATICIEN) == _role_targets(
        dossier,
        BusinessRole.ASSOCIE,
    )
    assert _role_targets(dossier, BusinessRole.PRATICIEN) == _role_targets(
        dossier,
        BusinessRole.GERANT,
    )
    assert _role_targets(dossier, BusinessRole.PRATICIEN) == _role_targets(
        dossier,
        BusinessRole.SIGNATAIRE,
    )


def test_dentist_regime_site_prefill_keeps_reserve_and_manual_documents() -> None:
    label = _label_for_key("selarl_dentiste_regime_site")
    data = business_test_prefill_input(label)
    validation = evaluate_business_wizard(data)
    status_by_code = _status_by_code(label)

    assert data.regime_communautaire is True
    assert data.site_distinct is True
    assert data.derogation is True
    assert status_by_code["DOC-006"].status is DocumentStatus.GENERABLE_WITH_RESERVE
    assert status_by_code["DOC-013"].status is DocumentStatus.MANUAL_ONLY
    assert status_by_code["DOC-014"].status is DocumentStatus.MANUAL_ONLY
    assert _row_status(validation, "DOC-013") == STATUS_MANUAL_ONLY
    assert _row_status(validation, "DOC-014") == STATUS_MANUAL_ONLY


def test_cession_bail_financement_prefill_tracks_complex_blocks() -> None:
    label = _label_for_key("selarl_medecin_cession_bail_financement")
    data = business_test_prefill_input(label)
    validation = evaluate_business_wizard(data)
    profile = business_test_prefill_front_data_profile(label)
    dossier = business_test_prefill_front_dossier(label)
    status_by_code = _status_by_code(label)

    assert data.cession is True
    assert data.emprunt_actif is True
    assert validation.can_generate_docx is True
    assert set(profile.operation_types) == {
        OperationType.CREATION,
        OperationType.CESSION,
        OperationType.BAIL,
        OperationType.FINANCEMENT,
    }
    assert set(profile.required_roles).issubset(
        {assignment.role for assignment in dossier.role_assignments.values()}
    )
    assert set(profile.required_address_usages).issubset(
        {address.usage for address in dossier.addresses.values()}
    )
    assert status_by_code["DOC-009"].status in {
        DocumentStatus.BLOCKED_MISSING_DATA,
        DocumentStatus.BLOCKED_UNRESOLVED_AMBIGUITY,
    }
    assert "DOC-009" not in validation.generatable_document_codes


def test_sci_simple_prefill_keeps_legacy_business_path_coherent() -> None:
    label = _label_for_key("sci_simple")
    data = business_test_prefill_input(label)
    validation = evaluate_business_wizard(data)
    status_by_code = _status_by_code(label)

    assert data.structure == "SCI"
    assert data.option_is is False
    assert validation.can_generate_docx is True
    assert set(validation.generatable_document_codes) == {
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    }
    assert status_by_code["DOC-001"].status is DocumentStatus.GENERABLE
    assert status_by_code["DOC-003"].status is DocumentStatus.GENERABLE
    assert status_by_code["DOC-004"].status is DocumentStatus.GENERABLE
    assert status_by_code["DOC-002"].status is DocumentStatus.BLOCKED_MISSING_DATA


def test_prefill_reset_key_list_covers_visible_and_derived_state() -> None:
    keys = set(business_test_prefill_widget_keys())
    all_preset_keys = {
        key
        for preset in business_test_prefill_presets()
        for key in preset.widget_values
    }

    assert all_preset_keys.issubset(keys)
    assert {
        "selarl_associe_genre_0",
        "selarl_associe_civilite_0",
        "selarl_associe_prenom_0",
        "selarl_associe_nom_0",
        "selarl_domiciliation_adresse_affichee",
        "selarl_dirigeant_prenom",
        "selarl_dirigeant_nom",
    }.issubset(keys)


def test_document_unitaire_scope_is_unchanged_by_prefill_ticket() -> None:
    assert unit_document_v1_supported_codes() == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    )
    assert build_unit_document_plan("DOC-013").status_record.status is (
        DocumentStatus.MANUAL_ONLY
    )


def _label_for_key(key: str) -> str:
    return next(preset.label for preset in business_test_prefill_presets() if preset.key == key)


def _status_by_code(label: str):
    return {
        status.doc_code: status
        for status in business_test_prefill_status_summary(label).documents
    }


def _role_targets(dossier, role: BusinessRole) -> set[str]:
    return {assignment.target_id for assignment in dossier.roles_for(role)}


def _row_status(validation, doc_code: str) -> str:
    return next(
        row.status for row in validation.document_rows if row.document_code == doc_code
    )
