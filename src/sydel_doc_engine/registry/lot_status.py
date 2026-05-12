from __future__ import annotations

from collections import Counter

from sydel_doc_engine.registry.catalog import build_seed_catalog


def count_by_status() -> dict[str, int]:
    counter: Counter[str] = Counter()
    for document in build_seed_catalog():
        counter[document.workflow_status.value] += 1
    return dict(counter)
