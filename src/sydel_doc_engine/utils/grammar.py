from __future__ import annotations

from sydel_doc_engine.domain.enums import Gender


def subject_line(genre: Gender) -> str:
    return "Je soussignée" if genre == Gender.FEMININ else "Je soussigné"


def birth_label(genre: Gender) -> str:
    return "Née le" if genre == Gender.FEMININ else "Né le"


def filiation_label(genre: Gender) -> str:
    return "fille de Monsieur" if genre == Gender.FEMININ else "fils de Monsieur"
