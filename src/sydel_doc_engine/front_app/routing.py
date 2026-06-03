from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class CleanFrontRoute:
    key: str
    label: str
    order: int


CLEAN_FRONT_ROUTES: Final[tuple[CleanFrontRoute, ...]] = (
    CleanFrontRoute(key="dossier_type", label="Type de dossier", order=1),
    CleanFrontRoute(key="data_entry", label="Donnees a saisir", order=2),
    CleanFrontRoute(key="generation", label="Generation", order=3),
)


def clean_front_routes() -> tuple[CleanFrontRoute, ...]:
    return CLEAN_FRONT_ROUTES

