from __future__ import annotations

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.utils.grammar import birth_label, filiation_label, subject_line


def test_subject_line_masculin() -> None:
    assert subject_line(Gender.MASCULIN) == "Je soussigné"


def test_subject_line_feminin() -> None:
    assert subject_line(Gender.FEMININ) == "Je soussignée"


def test_birth_label_and_filiation_label_feminin() -> None:
    assert birth_label(Gender.FEMININ) == "Née le"
    assert filiation_label(Gender.FEMININ) == "fille de Monsieur"
