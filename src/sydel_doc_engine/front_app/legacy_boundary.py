from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class LegacyBoundaryItem:
    component: str
    decision: str
    note: str


LEGACY_BOUNDARY: Final[tuple[LegacyBoundaryItem, ...]] = (
    LegacyBoundaryItem(
        component="src/sydel_doc_engine/front_data/",
        decision="reused",
        note="Fondations metier/data conservees pour le futur branchement dossier.",
    ),
    LegacyBoundaryItem(
        component="src/sydel_doc_engine/app/ui_runtime.py",
        decision="reused_later",
        note="Adaptateur moteur DOCX/PDF/ZIP a rebrancher depuis une vertical slice.",
    ),
    LegacyBoundaryItem(
        component="src/sydel_doc_engine/app/streamlit_app.py",
        decision="legacy_reference",
        note="Ancien front conserve en reference, hors nouveau point d'entree.",
    ),
    LegacyBoundaryItem(
        component="src/sydel_doc_engine/app/business_wizard.py",
        decision="ignored_by_clean_front",
        note="Assistant metier prototype non importe par le nouveau front.",
    ),
    LegacyBoundaryItem(
        component="src/sydel_doc_engine/app/single_document_mode.py",
        decision="ignored_by_clean_front",
        note="Document unitaire conserve comme outil historique, non expose.",
    ),
    LegacyBoundaryItem(
        component="debug/internal Streamlit panels",
        decision="remove_later",
        note="A supprimer quand le nouveau front couvrira les besoins de diagnostic.",
    ),
)


def legacy_boundary_items() -> tuple[LegacyBoundaryItem, ...]:
    return LEGACY_BOUNDARY

