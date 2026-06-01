from __future__ import annotations

from sydel_doc_engine.domain.case_catalog import (
    CATALOG_DOCUMENTS,
    DocumentAvailability,
    get_expected_documents,
    mapped_document_codes,
)
from sydel_doc_engine.registry.catalog import build_seed_catalog


def _doc_codes(case_type: str, **conditions: object) -> list[str]:
    return [
        document.document_code or document.document_key
        for document in get_expected_documents(
            {"case_type": case_type, "conditions": conditions}
        )
    ]


def test_case_catalog_documents_mapped_to_existing_registry() -> None:
    registry_codes = {document.doc_id for document in build_seed_catalog()}

    assert len(CATALOG_DOCUMENTS) == 46
    assert set(mapped_document_codes()) == registry_codes


def test_sci_simple_returns_expected_documents() -> None:
    assert _doc_codes("SCI") == [
        "DOC-020",
        "DOC-001",
        "DOC-003",
        "DOC-002",
        "DOC-004",
    ]


def test_sci_option_is_adds_option_letter() -> None:
    without_option = _doc_codes("SCI")
    with_option = _doc_codes("SCI", option_is=True)

    assert "DOC-022" not in without_option
    assert "DOC-022" in with_option


def test_sci_iris_selects_iris_statuts_instead_of_simple_sci_statuts() -> None:
    selected = _doc_codes("SCI", sci_iris=True)

    assert "DOC-021" in selected
    assert "DOC-020" not in selected


def test_selarl_regime_communautaire_adds_conjoint_letters() -> None:
    selected = _doc_codes("SELARL", regime_communautaire=True)

    assert "DOC-005" in selected
    assert "DOC-006" in selected


def test_doc_006_carries_regime_communautaire_source_note() -> None:
    documents = get_expected_documents(
        {"case_type": "SELARL", "conditions": {"regime_communautaire": True}}
    )
    doc_006 = next(document for document in documents if document.document_code == "DOC-006")

    assert doc_006.availability == DocumentAvailability.GENERATABLE
    assert any("Source DOCX Lot 2 disponible" in note for note in doc_006.notes)
    assert not any("reserve" in note.casefold() for note in doc_006.notes)


def test_selarl_scm_cession_adds_scm_cession_documents() -> None:
    selected = _doc_codes("SELARL", scm_cession=True)

    assert {"DOC-031", "DOC-032", "DOC-033"}.issubset(selected)


def test_selas_scm_adds_scm_selas_documents() -> None:
    selected = _doc_codes("SELAS", scm=True)

    assert {"DOC-031", "DOC-032", "DOC-033"}.issubset(selected)


def test_spfpl_cession_selects_agrement_by_associate_count() -> None:
    unique = _doc_codes("SPFPL cession", associe_unique=True)
    several = _doc_codes("SPFPL cession", associe_unique=False)

    assert "DOC-038" in unique
    assert "DOC-039" not in unique
    assert "DOC-039" in several
    assert "DOC-038" not in several


def test_spfpl_apport_adds_apport_documents() -> None:
    selected = _doc_codes("SPFPL apport")

    assert {"DOC-041", "DOC-042", "DOC-043"}.issubset(selected)


def test_scm_returns_scm_expected_documents() -> None:
    assert _doc_codes("SCM") == [
        "DOC-025",
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-034",
        "DOC-026",
        "DOC-030",
        "DOC-027",
        "DOC-028",
    ]


def test_sas_returns_sas_expected_documents_without_duplicate_capital_document() -> None:
    selected = _doc_codes("SAS")

    assert selected == ["DOC-015", "DOC-001", "DOC-002", "DOC-003", "DOC-024", "DOC-023"]
    assert selected.count("DOC-024") == 1


def test_manual_or_not_implemented_documents_are_not_generatable() -> None:
    selarl_documents = get_expected_documents(
        {
            "case_type": "SELARL",
            "conditions": {"site_distinct": True, "derogation": True},
        }
    )
    selas_documents = get_expected_documents(
        {"case_type": "SELAS", "conditions": {"derogation": True}}
    )
    blocked_documents = {
        document.document_key: document
        for document in [*selarl_documents, *selas_documents]
        if document.availability is not DocumentAvailability.GENERATABLE
    }

    assert blocked_documents["site_distinct_cd94_sel"].availability == (
        DocumentAvailability.MANUAL_ONLY
    )
    assert blocked_documents["formulaire_derogation_sites_sel"].availability == (
        DocumentAvailability.MANUAL_ONLY
    )
    assert blocked_documents["derogation_sel_bnc"].availability == (
        DocumentAvailability.MANUAL_ONLY
    )
    assert blocked_documents["derogation_cumul_selarl_bnc"].availability == (
        DocumentAvailability.MANUAL_ONLY
    )
    assert blocked_documents["derogation_cumul_selarl_salariee"].availability == (
        DocumentAvailability.NOT_IMPLEMENTED
    )
    assert blocked_documents["site_distinct_cd94_sel"].document_code is None
    assert blocked_documents["derogation_sel_bnc"].document_code is None
    assert blocked_documents["derogation_cumul_selarl_salariee"].document_code is None
