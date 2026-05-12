from __future__ import annotations

from sydel_doc_engine.registry.catalog import build_seed_catalog


def test_seed_catalog_contains_three_documents() -> None:
    catalog = build_seed_catalog()
    assert len(catalog) == 3


def test_seed_catalog_uses_lot_one_for_all_entries() -> None:
    catalog = build_seed_catalog()
    assert {document.lot for document in catalog} == {1}
