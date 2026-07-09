"""Fixtures de la suite de conformité transverse.

Le corpus (bundle COMPLET de chaque type, généré par les slices front réels) est
bâti UNE fois par session (fixture ``corpus``) — jamais à la collecte.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# tests/conformance et tests/unit importables par nom de module (même mécanique que
# la collecte pytest en mode prepend, mais garantie quel que soit l'ordre de collecte).
_ROOT = Path(__file__).resolve().parents[2]
for _p in (
    str(_ROOT / "src"),
    str(_ROOT / "tests" / "unit"),
    str(_ROOT / "tests" / "conformance"),
):
    if _p not in sys.path:
        sys.path.insert(0, _p)


@pytest.fixture(scope="session")
def corpus(tmp_path_factory: pytest.TempPathFactory) -> dict[str, dict[str, str]]:
    from _conformance_corpus import build_corpus

    return build_corpus(tmp_path_factory.mktemp("conformance_corpus"))


@pytest.fixture(scope="session")
def corpus_cap1(tmp_path_factory: pytest.TempPathFactory) -> dict[str, dict[str, str]]:
    """Corpus « montant unitaire = 1 € » (R13, accord euro/euros — Rafael 2026-07-09)."""
    from _conformance_corpus import build_corpus_cap1

    return build_corpus_cap1(tmp_path_factory.mktemp("conformance_corpus_cap1"))
