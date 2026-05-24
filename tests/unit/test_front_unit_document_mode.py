from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.app.single_document_mode import (
    UNIT_STATUS_GENERABLE_WITH_RESERVE,
    UNIT_STATUS_MANUAL_ONLY,
    build_single_document_context,
    build_single_document_unit_plan,
    sample_single_document_input,
    single_document_choices,
    single_document_requirement_rows,
    validate_single_document_input,
)
from sydel_doc_engine.app.ui_runtime import generate_docx_files_for_document_codes
from sydel_doc_engine.front_data.document_status import DocumentStatus
from sydel_doc_engine.front_data.unit_document_mode import (
    UnitDocumentScopeStatus,
    build_unit_document_plan,
    unit_document_v1_supported_codes,
)


def test_unit_document_mode_lists_prudent_v1_scope() -> None:
    assert unit_document_v1_supported_codes() == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
    )


def test_doc_001_is_generable_in_unit_mode(tmp_path: Path) -> None:
    data = sample_single_document_input("DOC-001")

    plan = _ready_plan(data)
    ctx = build_single_document_context(data)
    docx_paths = generate_docx_files_for_document_codes(ctx, tmp_path, ("DOC-001",))

    assert plan.status_record.status is DocumentStatus.GENERABLE
    assert [path.name for path in docx_paths] == ["declaration_non_condamnation.docx"]


def test_doc_002_is_generable_with_siege_and_domiciliation() -> None:
    data = sample_single_document_input("DOC-002")

    plan = _ready_plan(data)

    assert plan.status_record.status is DocumentStatus.GENERABLE
    assert "societe.societe_principale.siege.adresse" in plan.required_canonical_fields
    assert "domiciliation.adresse" in plan.required_canonical_fields


def test_doc_003_is_generable_with_signataire_company_and_siege() -> None:
    data = sample_single_document_input("DOC-003")

    plan = _ready_plan(data)

    assert plan.status_record.status is DocumentStatus.GENERABLE
    assert {role.value for role in plan.required_roles} == {
        "signataire",
        "societe_principale",
    }
    assert {usage.value for usage in plan.required_address_usages} == {
        "adresse_personnelle",
        "siege_social",
    }


def test_doc_004_is_generable_for_simple_case() -> None:
    data = sample_single_document_input("DOC-004")

    plan = _ready_plan(data)

    assert plan.status_record.status is DocumentStatus.GENERABLE
    assert {"associe", "gerant", "signataire", "societe_principale"}.issubset(
        {role.value for role in plan.required_roles}
    )


def test_doc_013_and_doc_014_remain_non_generable_manual_documents() -> None:
    doc_013 = build_unit_document_plan("DOC-013")
    doc_014 = build_unit_document_plan("DOC-014")

    assert doc_013.scope_status is UnitDocumentScopeStatus.MANUAL_ONLY
    assert doc_014.scope_status is UnitDocumentScopeStatus.MANUAL_ONLY
    assert doc_013.status_record.status is DocumentStatus.MANUAL_ONLY
    assert doc_014.status_record.status is DocumentStatus.MANUAL_ONLY
    assert not doc_013.is_generation_allowed
    assert not doc_014.is_generation_allowed


def test_doc_006_keeps_generation_reserve_without_v1_generation() -> None:
    plan = build_unit_document_plan("DOC-006")

    assert plan.scope_status is UnitDocumentScopeStatus.GENERABLE_WITH_RESERVE
    assert plan.status_record.status is DocumentStatus.GENERABLE_WITH_RESERVE
    assert not plan.is_generation_allowed


def test_unit_choices_expose_reserve_and_manual_statuses() -> None:
    choices = single_document_choices(
        "SELARL",
        {"regime_communautaire": True, "derogation": True},
    )
    by_code = {choice.document_code: choice for choice in choices if choice.document_code}

    assert by_code["DOC-006"].status == UNIT_STATUS_GENERABLE_WITH_RESERVE
    assert by_code["DOC-013"].status == UNIT_STATUS_MANUAL_ONLY
    assert by_code["DOC-014"].status == UNIT_STATUS_MANUAL_ONLY


def test_out_of_scope_document_is_announced_cleanly() -> None:
    plan = build_unit_document_plan("DOC-033")

    assert plan.scope_status is UnitDocumentScopeStatus.OUT_OF_SCOPE_V1
    assert not plan.is_generation_allowed
    assert "Hors perimetre V1" in " ".join(plan.explain_blockers())


def test_unit_document_requirement_rows_expose_data_layer_requirements() -> None:
    rows = single_document_requirement_rows("DOC-002")
    by_category = {row["categorie"]: row["valeurs"] for row in rows}

    assert "signataire" in by_category["roles"]
    assert "siege_social" in by_category["adresses"]
    assert "domiciliation.adresse" in by_category["champs canoniques"]


def test_front_unit_document_mode_has_no_streamlit_session_state_dependency() -> None:
    source = Path("src/sydel_doc_engine/front_data/unit_document_mode.py").read_text(
        encoding="utf-8"
    )

    assert "streamlit" not in source
    assert "session_state" not in source


def _ready_plan(data):
    assert validate_single_document_input(data) == ()
    plan = build_single_document_unit_plan(data)
    assert plan.is_generation_allowed, plan.explain_blockers()
    return plan
