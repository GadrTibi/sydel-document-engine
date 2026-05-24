from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Final

from sydel_doc_engine.front_data.document_status import (
    DocumentStatusRecord,
    build_document_status_summary,
)
from sydel_doc_engine.front_data.dossier_flow import (
    DossierFlow,
    build_sentinel_dossier_flow,
)

TARGET_FRONT_LABEL: Final = "Nouveau front global"
PROTOTYPE_TOOLS_LABEL: Final = "Prototype / outils de test"

TARGET_FRONT_AREA_LABELS: Final[tuple[str, ...]] = (
    "Accueil / selection",
    "Dossier",
    "Documents attendus",
    "Generation",
)

PROTOTYPE_TOOL_LABELS: Final[tuple[str, ...]] = (
    "Assistant metier prototype",
    "Document unitaire",
    "Technique / diagnostic",
)

SHELL_STATUS_DOCUMENT_CODES: Final[tuple[str, ...]] = (
    "DOC-002",
    "DOC-006",
    "DOC-013",
    "DOC-014",
    "DOC-034",
)


@dataclass(frozen=True)
class FrontShellNavigationItem:
    key: str
    group: str
    label: str
    status: str
    purpose: str
    next_ticket: str


TARGET_FRONT_ITEMS: Final[tuple[FrontShellNavigationItem, ...]] = (
    FrontShellNavigationItem(
        key="home",
        group=TARGET_FRONT_LABEL,
        label="Accueil / selection",
        status="Visible V1",
        purpose="Point d'entree cible pour choisir le type de travail.",
        next_ticket="FRONT-DOSSIER-EDITOR-001",
    ),
    FrontShellNavigationItem(
        key="dossier",
        group=TARGET_FRONT_LABEL,
        label="Dossier",
        status="Saisie V1",
        purpose="Alimente un DossierRecord simple, puis recalcule le flow et les statuts.",
        next_ticket="FRONT-DOCUMENTS-PANEL-001",
    ),
    FrontShellNavigationItem(
        key="documents",
        group=TARGET_FRONT_LABEL,
        label="Documents attendus",
        status="Squelette read-only",
        purpose="Expose les statuts documentaires sans lancer la generation.",
        next_ticket="FRONT-DOCUMENTS-PANEL-001",
    ),
    FrontShellNavigationItem(
        key="generation",
        group=TARGET_FRONT_LABEL,
        label="Generation",
        status="Placeholder",
        purpose="Reserve l'emplacement des actions DOCX/PDF/ZIP du futur front.",
        next_ticket="FRONT-GENERATION-ACTIONS-001",
    ),
)

PROTOTYPE_TOOL_ITEMS: Final[tuple[FrontShellNavigationItem, ...]] = (
    FrontShellNavigationItem(
        key="assistant_prototype",
        group=PROTOTYPE_TOOLS_LABEL,
        label="Assistant metier prototype",
        status="Bac a sable",
        purpose="Conserve le parcours historique pour smoke et comparaison.",
        next_ticket="FRONT-PROTOTYPE-DEPRECATION-001",
    ),
    FrontShellNavigationItem(
        key="unit_document",
        group=PROTOTYPE_TOOLS_LABEL,
        label="Document unitaire",
        status="Outil de test",
        purpose="Teste un document isole avec la fondation front_data.",
        next_ticket="FRONT-UNIT-DOCUMENT-UI-001",
    ),
    FrontShellNavigationItem(
        key="technical_diagnostic",
        group=PROTOTYPE_TOOLS_LABEL,
        label="Technique / diagnostic",
        status="Outil de diagnostic",
        purpose="Charge des contextes YAML/JSON et verifie le moteur.",
        next_ticket="FRONT-TEST-TOOLS-CONSOLIDATION-001",
    ),
)


def target_front_items() -> tuple[FrontShellNavigationItem, ...]:
    return TARGET_FRONT_ITEMS


def prototype_tool_items() -> tuple[FrontShellNavigationItem, ...]:
    return PROTOTYPE_TOOL_ITEMS


def front_shell_navigation_items() -> tuple[FrontShellNavigationItem, ...]:
    return (*TARGET_FRONT_ITEMS, *PROTOTYPE_TOOL_ITEMS)


def front_shell_navigation_rows() -> tuple[dict[str, str], ...]:
    return tuple(_navigation_row(item) for item in front_shell_navigation_items())


def target_front_navigation_rows() -> tuple[dict[str, str], ...]:
    return tuple(_navigation_row(item) for item in TARGET_FRONT_ITEMS)


def prototype_tool_navigation_rows() -> tuple[dict[str, str], ...]:
    return tuple(_navigation_row(item) for item in PROTOTYPE_TOOL_ITEMS)


def shell_flow_step_rows(flow: DossierFlow | None = None) -> tuple[dict[str, str], ...]:
    flow = flow or build_sentinel_dossier_flow()
    return tuple(
        {
            "ordre": str(step.order),
            "zone": step.label,
            "dependances": _step_dependencies_label(flow, step.dependencies),
            "blocs actifs": _labels(
                block.label for block in flow.blocks_for_step(step.id) if block.active
            ),
        }
        for step in flow.steps
    )


def shell_flow_block_rows(flow: DossierFlow | None = None) -> tuple[dict[str, str], ...]:
    flow = flow or build_sentinel_dossier_flow()
    return tuple(
        {
            "bloc": block.label,
            "etape": flow.step(block.step_id).label,
            "statut": block.status.value,
            "documents": _labels(block.document_codes),
            "roles": _labels(role.value for role in block.required_roles),
            "adresses": _labels(usage.value for usage in block.required_address_usages),
        }
        for block in flow.active_blocks()
    )


def shell_document_status_rows(
    document_codes: Iterable[str] = SHELL_STATUS_DOCUMENT_CODES,
) -> tuple[dict[str, str], ...]:
    summary = build_document_status_summary(
        None,
        document_codes=tuple(document_codes),
        lot_id="shell-preview",
        lot_label="Apercu shell",
    )
    return tuple(_document_status_row(status) for status in summary.documents)


def shell_lot_status_rows(
    document_codes: Iterable[str] = SHELL_STATUS_DOCUMENT_CODES,
) -> tuple[dict[str, str], ...]:
    summary = build_document_status_summary(
        None,
        document_codes=tuple(document_codes),
        lot_id="shell-preview",
        lot_label="Apercu shell",
    )
    return tuple(
        {
            "lot": lot.label,
            "statut": lot.status.value,
            "prets": _labels(lot.ready_document_codes),
            "avec reserve": _labels(lot.reserve_document_codes),
            "manuels": _labels(lot.manual_document_codes),
            "bloques": _labels(lot.blocked_document_codes),
        }
        for lot in summary.lots
    )


def _navigation_row(item: FrontShellNavigationItem) -> dict[str, str]:
    return {
        "espace": item.group,
        "zone": item.label,
        "statut": item.status,
        "role": item.purpose,
        "ticket cible": item.next_ticket,
    }


def _document_status_row(status: DocumentStatusRecord) -> dict[str, str]:
    return {
        "document": status.doc_code,
        "libelle": status.doc_label,
        "statut": status.status.value,
        "generation": "oui" if status.is_ready_for_generation else "non",
        "raisons": _labels(reason.message for reason in status.reasons),
    }


def _step_dependencies_label(flow: DossierFlow, dependencies: object) -> str:
    return _labels(flow.step(step_id).label for step_id in dependencies)


def _labels(values: Iterable[object]) -> str:
    labels = tuple(str(value) for value in values if value)
    return ", ".join(labels) if labels else "-"
