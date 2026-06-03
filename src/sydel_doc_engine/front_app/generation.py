from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from sydel_doc_engine.front_app.data_entry import CleanDataEntry
from sydel_doc_engine.front_app.dossier_selection import DossierTypeOption
from sydel_doc_engine.front_app.selarl_slice import (
    SelarlDocumentRow,
    build_selarl_plan,
    front_data_scope_summary,
)

UNSUPPORTED_DOSSIER_REASON: Final = "Type de dossier non branche dans le front clean."


@dataclass(frozen=True)
class CleanGenerationPlan:
    dossier_type_key: str
    can_generate: bool
    status: str
    reason: str
    target_engine_adapter: str
    document_codes: tuple[str, ...] = ()
    document_rows: tuple[SelarlDocumentRow, ...] = ()
    blockers: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    front_data_scope: tuple[str, ...] = ()


def build_clean_generation_plan(
    dossier_type: DossierTypeOption,
    data_entry: CleanDataEntry,
) -> CleanGenerationPlan:
    if not dossier_type.generation_enabled or dossier_type.structure != "SELARL":
        return CleanGenerationPlan(
            dossier_type_key=dossier_type.key,
            can_generate=False,
            status="unsupported_dossier_type",
            reason=UNSUPPORTED_DOSSIER_REASON,
            target_engine_adapter="none",
        )

    selarl_plan = build_selarl_plan(data_entry)
    return CleanGenerationPlan(
        dossier_type_key=dossier_type.key,
        can_generate=selarl_plan.can_generate,
        status=selarl_plan.status,
        reason=selarl_plan.reason,
        target_engine_adapter=selarl_plan.target_engine_adapter,
        document_codes=selarl_plan.document_codes,
        document_rows=selarl_plan.document_rows,
        blockers=selarl_plan.blockers,
        warnings=selarl_plan.warnings,
        front_data_scope=front_data_scope_summary(),
    )
