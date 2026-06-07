from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from sydel_doc_engine.front_app.type_registry import registered_types


@dataclass(frozen=True)
class DossierTypeOption:
    key: str
    label: str
    structure: str
    generation_enabled: bool
    status: str
    slice_module: str | None = None


def _build_options() -> tuple[DossierTypeOption, ...]:
    return tuple(
        DossierTypeOption(
            key=item.key,
            label=item.label,
            structure=item.structure,
            generation_enabled=item.generation_enabled,
            status=item.status,
            slice_module=item.slice_module,
        )
        for item in registered_types()
    )


# Source de verite = `type_registry`. La deroulante liste TOUS les types prets et
# reste auto-extensible : ajouter une entree au registre suffit.
CLEAN_DOSSIER_TYPE_OPTIONS: Final[tuple[DossierTypeOption, ...]] = _build_options()


def dossier_type_options() -> tuple[DossierTypeOption, ...]:
    return CLEAN_DOSSIER_TYPE_OPTIONS


def dossier_type_labels() -> tuple[str, ...]:
    return tuple(option.label for option in CLEAN_DOSSIER_TYPE_OPTIONS)


def dossier_type_by_label(label: str) -> DossierTypeOption:
    for option in CLEAN_DOSSIER_TYPE_OPTIONS:
        if option.label == label:
            return option
    raise KeyError(f"Unknown dossier type: {label}")


def dossier_type_by_key(key: str) -> DossierTypeOption:
    for option in CLEAN_DOSSIER_TYPE_OPTIONS:
        if option.key == key:
            return option
    raise KeyError(f"Unknown dossier type: {key}")
