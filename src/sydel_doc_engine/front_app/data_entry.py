from __future__ import annotations

from typing import Any

from sydel_doc_engine.front_app.dossier_selection import DossierTypeOption
from sydel_doc_engine.front_app.selarl_slice import SelarlSliceInput

CleanDataEntry = SelarlSliceInput


def build_clean_data_entry(
    dossier_type: DossierTypeOption,
    **values: Any,
) -> CleanDataEntry:
    normalized = dict(values)

    legacy_company_label = normalized.pop("company_label", "")
    normalized.pop("client_label", None)
    normalized.pop("internal_note", None)
    if legacy_company_label and not normalized.get("denomination"):
        normalized["denomination"] = legacy_company_label

    for key, value in tuple(normalized.items()):
        if isinstance(value, str):
            normalized[key] = value.strip()

    return CleanDataEntry(
        dossier_type_key=dossier_type.key,
        **normalized,
    )
