from __future__ import annotations

from sydel_doc_engine.registry.catalog import build_seed_catalog


def test_seed_catalog_contains_four_documents() -> None:
    catalog = build_seed_catalog()
    assert len(catalog) == 4


def test_seed_catalog_contains_lot_one_and_lot_two_entries() -> None:
    catalog = build_seed_catalog()
    assert {document.lot for document in catalog} == {1, 2}


def test_seed_catalog_pv_nomination_gerant_scope_excludes_sas() -> None:
    catalog = build_seed_catalog()

    pv_document = next(document for document in catalog if document.doc_id == "DOC-004")

    assert set(pv_document.structures) == {
        "SELARL",
        "SELAS",
        "SPFPL cession",
        "SPFPL apport",
        "SCS",
        "SCI",
        "SCM",
    }
    assert "SAS" not in pv_document.structures
