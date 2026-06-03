from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class DossierTypeOption:
    key: str
    label: str
    structure: str
    generation_enabled: bool
    status: str


CLEAN_DOSSIER_TYPE_OPTIONS: Final[tuple[DossierTypeOption, ...]] = (
    DossierTypeOption(
        key="selarl_v1",
        label="SELARL creation V1",
        structure="SELARL",
        generation_enabled=True,
        status="bounded_vertical_slice",
    ),
)


def dossier_type_options() -> tuple[DossierTypeOption, ...]:
    return CLEAN_DOSSIER_TYPE_OPTIONS


def dossier_type_labels() -> tuple[str, ...]:
    return tuple(option.label for option in CLEAN_DOSSIER_TYPE_OPTIONS)


def dossier_type_by_label(label: str) -> DossierTypeOption:
    for option in CLEAN_DOSSIER_TYPE_OPTIONS:
        if option.label == label:
            return option
    raise KeyError(f"Unknown dossier type: {label}")
