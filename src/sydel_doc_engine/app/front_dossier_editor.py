from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Final, TypeVar

from sydel_doc_engine.front_data.document_status import (
    DocumentStatusRecord,
    DocumentStatusSummary,
    build_document_status_summary,
)
from sydel_doc_engine.front_data.dossier_flow import (
    DossierBlock,
    DossierFlow,
    FlowStatus,
    build_dossier_flow,
)
from sydel_doc_engine.front_data.models import (
    BusinessRole,
    DocumentRequirementRecord,
    DossierRecord,
    OperationContext,
    OperationType,
)
from sydel_doc_engine.front_data.unit_document_mode import (
    UNIT_DOCUMENT_V1_SUPPORTED_CODES,
    unit_document_requirement,
)

T = TypeVar("T")


@dataclass(frozen=True)
class FrontDossierEditorProfile:
    key: str
    label: str
    structure: str
    operation_types: tuple[OperationType, ...]
    document_codes: tuple[str, ...]
    description: str


@dataclass(frozen=True)
class FrontDossierEditorView:
    profile: FrontDossierEditorProfile
    dossier: DossierRecord
    flow: DossierFlow
    status_summary: DocumentStatusSummary


FRONT_DOSSIER_EDITOR_PROFILES: Final[tuple[FrontDossierEditorProfile, ...]] = (
    FrontDossierEditorProfile(
        key="selarl_creation_simple",
        label="SELARL creation simple",
        structure="SELARL",
        operation_types=(OperationType.CREATION,),
        document_codes=UNIT_DOCUMENT_V1_SUPPORTED_CODES,
        description=(
            "Premier dossier cible prudent : creation SELARL simple avec les "
            "documents unitaires V1 deja structures."
        ),
    ),
    FrontDossierEditorProfile(
        key="selarl_ordre_inscription",
        label="SELARL ordre / inscription",
        structure="SELARL",
        operation_types=(OperationType.CREATION, OperationType.ORDRE, OperationType.DEROGATION),
        document_codes=("DOC-034", "DOC-017"),
        description=(
            "Vue de travail pour isoler ordre, mandataire, capital, associes "
            "et banque sans les resoudre artificiellement."
        ),
    ),
    FrontDossierEditorProfile(
        key="selarl_cession_cabinet",
        label="SELARL cession cabinet + bail + financement",
        structure="SELARL",
        operation_types=(
            OperationType.CESSION,
            OperationType.BAIL,
            OperationType.FINANCEMENT,
        ),
        document_codes=("DOC-009",),
        description=(
            "Vue de travail pour localiser les blocs cession, bail, origine, "
            "exercices, prix et financement."
        ),
    ),
    FrontDossierEditorProfile(
        key="scm_cession_parts",
        label="SCM cession de parts",
        structure="SCM",
        operation_types=(OperationType.CESSION_PARTS_SCM, OperationType.APPORT),
        document_codes=("DOC-033", "DOC-025"),
        description=(
            "Vue de travail SCM avec cedant, cessionnaire, SCM cedee, associes "
            "et apports distincts."
        ),
    ),
    FrontDossierEditorProfile(
        key="spfpl_apport_titres",
        label="SPFPL apport de titres",
        structure="SPFPL",
        operation_types=(OperationType.APPORT,),
        document_codes=("DOC-041",),
        description=(
            "Vue de travail SPFPL pour apporteur, societe cible, commissaire "
            "et evaluateur."
        ),
    ),
)


def front_dossier_editor_profiles() -> tuple[FrontDossierEditorProfile, ...]:
    return FRONT_DOSSIER_EDITOR_PROFILES


def front_dossier_editor_profile_labels() -> tuple[str, ...]:
    return tuple(profile.label for profile in FRONT_DOSSIER_EDITOR_PROFILES)


def front_dossier_editor_profile(
    key_or_label: str,
) -> FrontDossierEditorProfile:
    for profile in FRONT_DOSSIER_EDITOR_PROFILES:
        if key_or_label in {profile.key, profile.label}:
            return profile
    raise KeyError(f"Unknown front dossier editor profile: {key_or_label}")


def build_front_dossier_editor_dossier(
    profile: FrontDossierEditorProfile | str | None = None,
) -> DossierRecord:
    profile = _resolve_profile(profile)
    dossier = DossierRecord(
        id=f"front-editor-{profile.key}",
        label=profile.label,
        structure=profile.structure,
        metadata={
            "front_editor_profile": profile.key,
            "front_editor_v1": True,
            "placeholder_values": True,
        },
    )

    for operation_type in profile.operation_types:
        dossier.add_operation_context(
            OperationContext(
                id=f"operation-{operation_type.value}",
                operation_type=operation_type,
                label=operation_type.value,
            )
        )

    for requirement in _requirements_for_profile(profile):
        dossier.add_document_requirement(requirement)

    return dossier


def build_front_dossier_editor_view(
    profile: FrontDossierEditorProfile | str | None = None,
) -> FrontDossierEditorView:
    profile = _resolve_profile(profile)
    dossier = build_front_dossier_editor_dossier(profile)
    flow = build_dossier_flow(dossier)
    status_summary = build_document_status_summary(
        dossier,
        lot_id=f"front-editor-{profile.key}",
        lot_label=profile.label,
    )
    return FrontDossierEditorView(
        profile=profile,
        dossier=dossier,
        flow=flow,
        status_summary=status_summary,
    )


def front_dossier_summary_rows(
    view: FrontDossierEditorView,
) -> tuple[dict[str, str], ...]:
    return (
        {
            "type dossier": view.profile.label,
            "structure": view.profile.structure,
            "operations": _labels(operation.value for operation in view.profile.operation_types),
            "documents": _labels(view.profile.document_codes),
            "statut lot": _labels(lot.status.value for lot in view.status_summary.lots),
            "generables": _labels(view.status_summary.generable_doc_codes),
            "bloques": _labels(view.status_summary.blocked_doc_codes),
        },
    )


def front_dossier_flow_step_rows(
    view: FrontDossierEditorView,
) -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "ordre": str(step.order),
            "etape": step.label,
            "statut": _step_status(view.flow.blocks_for_step(step.id)).value,
            "dependances": _labels(
                view.flow.step(dependency).label for dependency in step.dependencies
            ),
            "blocs actifs": _labels(
                block.label for block in view.flow.blocks_for_step(step.id) if block.active
            ),
        }
        for step in view.flow.steps
    )


def front_dossier_block_rows(
    view: FrontDossierEditorView,
) -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for block in view.flow.active_blocks():
        validation = view.flow.validation_for_block(block.id)
        rows.append(
            {
                "bloc": block.label,
                "etape": view.flow.step(block.step_id).label,
                "statut": block.status.value,
                "documents": _labels(block.document_codes),
                "roles requis": _labels(role.value for role in block.required_roles),
                "adresses requises": _labels(
                    usage.value for usage in block.required_address_usages
                ),
                "champs requis": _labels(block.required_canonical_fields),
                "blocages / warnings": _labels(issue.message for issue in validation.issues),
            }
        )
    return tuple(rows)


def front_dossier_requirement_rows(
    view: FrontDossierEditorView,
) -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "document": requirement.doc_code,
            "libelle": requirement.doc_label,
            "roles requis": _labels(
                role.value for role in _required_roles(requirement)
            ),
            "adresses requises": _labels(
                usage.value for usage in requirement.required_address_usages
            ),
            "champs canoniques": _labels(requirement.required_canonical_fields),
            "blocs cible": _labels(requirement.target_screen_blocks),
        }
        for requirement in view.flow.document_requirements
    )


def front_dossier_document_status_rows(
    view: FrontDossierEditorView,
) -> tuple[dict[str, str], ...]:
    return tuple(_document_status_row(status) for status in view.status_summary.documents)


def front_dossier_lot_status_rows(
    view: FrontDossierEditorView,
) -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "lot": lot.label,
            "statut": lot.status.value,
            "prets": _labels(lot.ready_document_codes),
            "avec reserve": _labels(lot.reserve_document_codes),
            "manuels": _labels(lot.manual_document_codes),
            "bloques": _labels(lot.blocked_document_codes),
        }
        for lot in view.status_summary.lots
    )


def front_dossier_lot_status_legend_rows() -> tuple[dict[str, str], ...]:
    return (
        {
            "statut": "ready",
            "sens": "Tous les documents utiles du lot sont generables.",
        },
        {
            "statut": "partial",
            "sens": "Le lot contient des documents prets et des reserves, manuels ou incomplets.",
        },
        {
            "statut": "blocked",
            "sens": "Au moins un document critique est bloque par donnees ou ambiguite.",
        },
    )


def _resolve_profile(
    profile: FrontDossierEditorProfile | str | None,
) -> FrontDossierEditorProfile:
    if profile is None:
        return FRONT_DOSSIER_EDITOR_PROFILES[0]
    if isinstance(profile, FrontDossierEditorProfile):
        return profile
    return front_dossier_editor_profile(profile)


def _requirements_for_profile(
    profile: FrontDossierEditorProfile,
) -> tuple[DocumentRequirementRecord, ...]:
    return tuple(unit_document_requirement(code) for code in profile.document_codes)


def _required_roles(requirement: DocumentRequirementRecord) -> tuple[BusinessRole, ...]:
    return _unique((*requirement.required_roles, *requirement.required_entities))


def _step_status(blocks: Iterable[DossierBlock]) -> FlowStatus:
    blocks = tuple(block for block in blocks if block.active)
    if not blocks:
        return FlowStatus.INACTIVE
    statuses = {block.status for block in blocks}
    if FlowStatus.BLOCKED in statuses:
        return FlowStatus.BLOCKED
    if FlowStatus.WARNING in statuses:
        return FlowStatus.WARNING
    if statuses == {FlowStatus.COMPLETE}:
        return FlowStatus.COMPLETE
    return FlowStatus.AVAILABLE


def _document_status_row(status: DocumentStatusRecord) -> dict[str, str]:
    return {
        "document": status.doc_code,
        "libelle": status.doc_label,
        "statut": status.status.value,
        "generation": "oui" if status.is_ready_for_generation else "non",
        "roles manquants": _labels(role.value for role in status.missing_roles),
        "adresses manquantes": _labels(
            usage.value for usage in status.missing_address_usages
        ),
        "champs manquants": _labels(status.missing_canonical_fields),
        "ambiguities": _labels(status.unresolved_ambiguity_keys),
        "raisons": _labels(reason.message for reason in status.reasons),
    }


def _labels(values: Iterable[object]) -> str:
    labels = tuple(str(value) for value in values if value)
    return ", ".join(labels) if labels else "-"


def _unique(items: Iterable[T]) -> tuple[T, ...]:
    return tuple(dict.fromkeys(items))
