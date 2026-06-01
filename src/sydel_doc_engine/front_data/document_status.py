from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from sydel_doc_engine.domain.case_catalog import (
    CATALOG_DOCUMENTS,
    DocumentAvailability,
)
from sydel_doc_engine.front_data.canonical_mapping import (
    SENTINEL_DOCUMENT_REQUIREMENTS,
    sentinel_requirement,
)
from sydel_doc_engine.front_data.dossier_flow import (
    DossierBlockId,
    DossierFlow,
    FlowValidationResult,
    build_dossier_flow,
)
from sydel_doc_engine.front_data.models import (
    AddressUsage,
    BusinessRole,
    DocumentRequirementRecord,
    DocumentRequirementStatus,
    DossierRecord,
    ValidationIssue,
    ValidationIssueType,
    ValidationSeverity,
)
from sydel_doc_engine.front_data.validation import (
    validate_address_records,
    validate_document_requirement,
    validate_reuse_rules,
    validate_role_assignments,
)


class DocumentStatus(StrEnum):
    EXPECTED = "expected"
    GENERABLE = "generable"
    MANUAL_ONLY = "manual_only"
    NOT_IMPLEMENTED = "not_implemented"
    CONTEXT_INCOMPLETE = "context_incomplete"
    BLOCKED_MISSING_DATA = "blocked_missing_data"
    BLOCKED_UNRESOLVED_AMBIGUITY = "blocked_unresolved_ambiguity"
    GENERABLE_WITH_RESERVE = "generable_with_reserve"


class DocumentLotStatus(StrEnum):
    READY = "ready"
    PARTIAL = "partial"
    BLOCKED = "blocked"


class DocumentStatusReasonType(StrEnum):
    MISSING_ROLE = "missing_role"
    MISSING_TYPED_ADDRESS = "missing_typed_address"
    MISSING_CANONICAL_VALUE = "missing_canonical_value"
    UNRESOLVED_AMBIGUITY = "unresolved_ambiguity"
    REUSE_CONFLICT = "reuse_conflict"
    INVALID_DATA = "invalid_data"
    MANUAL_ONLY = "manual_only"
    NOT_IMPLEMENTED = "not_implemented"
    CONTEXT_INCOMPLETE = "context_incomplete"
    RESERVE = "reserve"
    CATALOG_NOTE = "catalog_note"


class DocumentStatusReasonSource(StrEnum):
    DOCUMENT_REQUIREMENT = "document_requirement"
    VALIDATION = "validation"
    DOSSIER_FLOW = "dossier_flow"
    CATALOG = "catalog"
    RESERVE = "reserve"


@dataclass(frozen=True)
class DocumentStatusReason:
    reason_type: DocumentStatusReasonType
    severity: ValidationSeverity
    message: str
    source: DocumentStatusReasonSource
    doc_code: str | None = None
    block_id: DossierBlockId | None = None
    field_path: str | None = None
    role: BusinessRole | None = None
    address_usage: AddressUsage | None = None
    ambiguity_key: str | None = None
    source_ref: str | None = None
    target_ref: str | None = None
    action: str | None = None

    @property
    def blocking(self) -> bool:
        return self.severity is ValidationSeverity.BLOCKING


@dataclass(frozen=True)
class DocumentStatusRecord:
    doc_code: str
    doc_label: str
    status: DocumentStatus
    reasons: tuple[DocumentStatusReason, ...] = ()
    lot_id: str | None = None
    family: str | None = None
    document_key: str | None = None
    catalog_availability: str | None = None
    source_template_filename: str | None = None

    @property
    def is_generable(self) -> bool:
        return self.status in {
            DocumentStatus.GENERABLE,
            DocumentStatus.GENERABLE_WITH_RESERVE,
        }

    @property
    def is_ready_for_generation(self) -> bool:
        return self.is_generable

    @property
    def is_blocked(self) -> bool:
        return self.status in {
            DocumentStatus.BLOCKED_MISSING_DATA,
            DocumentStatus.BLOCKED_UNRESOLVED_AMBIGUITY,
            DocumentStatus.NOT_IMPLEMENTED,
            DocumentStatus.CONTEXT_INCOMPLETE,
        }

    @property
    def blocking_reasons(self) -> tuple[DocumentStatusReason, ...]:
        return tuple(reason for reason in self.reasons if reason.blocking)

    @property
    def warning_reasons(self) -> tuple[DocumentStatusReason, ...]:
        return tuple(
            reason for reason in self.reasons if reason.severity is ValidationSeverity.WARNING
        )

    @property
    def reserve_reasons(self) -> tuple[DocumentStatusReason, ...]:
        return tuple(
            reason
            for reason in self.reasons
            if reason.reason_type is DocumentStatusReasonType.RESERVE
        )

    @property
    def missing_roles(self) -> tuple[BusinessRole, ...]:
        return _unique(reason.role for reason in self.reasons if reason.role is not None)

    @property
    def missing_address_usages(self) -> tuple[AddressUsage, ...]:
        return _unique(
            reason.address_usage for reason in self.reasons if reason.address_usage is not None
        )

    @property
    def missing_canonical_fields(self) -> tuple[str, ...]:
        return _unique(
            reason.field_path for reason in self.reasons if reason.field_path is not None
        )

    @property
    def unresolved_ambiguity_keys(self) -> tuple[str, ...]:
        return _unique(
            reason.ambiguity_key
            for reason in self.reasons
            if reason.ambiguity_key is not None
        )

    def why_not_generable(self) -> tuple[DocumentStatusReason, ...]:
        if self.is_generable:
            return ()
        return self.reasons


@dataclass(frozen=True)
class DocumentLotStatusRecord:
    lot_id: str
    label: str
    status: DocumentLotStatus
    document_statuses: tuple[DocumentStatusRecord, ...]
    reasons: tuple[DocumentStatusReason, ...] = ()

    @property
    def ready_document_codes(self) -> tuple[str, ...]:
        return tuple(
            status.doc_code
            for status in self.document_statuses
            if status.status is DocumentStatus.GENERABLE
        )

    @property
    def reserve_document_codes(self) -> tuple[str, ...]:
        return tuple(
            status.doc_code
            for status in self.document_statuses
            if status.status is DocumentStatus.GENERABLE_WITH_RESERVE
        )

    @property
    def manual_document_codes(self) -> tuple[str, ...]:
        return tuple(
            status.doc_code
            for status in self.document_statuses
            if status.status is DocumentStatus.MANUAL_ONLY
        )

    @property
    def blocked_document_codes(self) -> tuple[str, ...]:
        return tuple(status.doc_code for status in self.document_statuses if status.is_blocked)


@dataclass(frozen=True)
class DocumentStatusSummary:
    documents: tuple[DocumentStatusRecord, ...]
    lots: tuple[DocumentLotStatusRecord, ...] = ()

    @property
    def generable_doc_codes(self) -> tuple[str, ...]:
        return tuple(document.doc_code for document in self.documents if document.is_generable)

    @property
    def blocked_doc_codes(self) -> tuple[str, ...]:
        return tuple(document.doc_code for document in self.documents if document.is_blocked)

    @property
    def manual_doc_codes(self) -> tuple[str, ...]:
        return tuple(
            document.doc_code
            for document in self.documents
            if document.status is DocumentStatus.MANUAL_ONLY
        )


NON_BLOCKING_AMBIGUITY_KEYS = frozenset({"legacy_domiciliation_display_alias"})

DOCUMENT_RESERVES: dict[str, tuple[str, ...]] = {}

CATALOG_BY_CODE = {
    document.document_code: document
    for document in CATALOG_DOCUMENTS
    if document.document_code is not None
}


def build_document_status(
    dossier: DossierRecord | None,
    requirement: DocumentRequirementRecord,
    *,
    flow: DossierFlow | None = None,
    lot_id: str | None = None,
    family: str | None = None,
) -> DocumentStatusRecord:
    catalog_document = CATALOG_BY_CODE.get(requirement.doc_code)
    metadata_reasons = _metadata_reasons(requirement, catalog_document)
    forced_status = _forced_status_from_metadata(requirement, catalog_document)
    if forced_status is not None:
        return _status_record(
            requirement=requirement,
            status=forced_status,
            reasons=metadata_reasons,
            lot_id=lot_id,
            family=family,
            catalog_document=catalog_document,
        )

    if dossier is None:
        status = (
            DocumentStatus.GENERABLE_WITH_RESERVE
            if _reserve_reasons(requirement.doc_code)
            else DocumentStatus.EXPECTED
        )
        return _status_record(
            requirement=requirement,
            status=status,
            reasons=metadata_reasons,
            lot_id=lot_id,
            family=family,
            catalog_document=catalog_document,
        )

    reasons = [*metadata_reasons]
    reasons.extend(_document_validation_reasons(dossier, requirement))
    reasons.extend(_flow_reasons_for_document(dossier, requirement, flow))
    reasons = list(_unique_reasons(reasons))

    status = _status_from_reasons(requirement.doc_code, reasons)
    return _status_record(
        requirement=requirement,
        status=status,
        reasons=tuple(reasons),
        lot_id=lot_id,
        family=family,
        catalog_document=catalog_document,
    )


def build_document_status_for_code(
    doc_code: str,
    dossier: DossierRecord | None = None,
    *,
    lot_id: str | None = None,
    family: str | None = None,
) -> DocumentStatusRecord:
    requirement = _requirement_for_code(doc_code, dossier)
    flow = build_dossier_flow(dossier) if dossier and dossier.document_requirements else None
    return build_document_status(
        dossier,
        requirement,
        flow=flow,
        lot_id=lot_id,
        family=family,
    )


def build_document_status_summary(
    dossier: DossierRecord | None,
    *,
    document_codes: Iterable[str] | None = None,
    lot_id: str = "dossier",
    lot_label: str = "Dossier",
) -> DocumentStatusSummary:
    requirements = _requirements_for_summary(dossier, document_codes)
    flow = build_dossier_flow(dossier) if dossier and dossier.document_requirements else None
    statuses = tuple(
        build_document_status(dossier, requirement, flow=flow, lot_id=lot_id)
        for requirement in requirements
    )
    return DocumentStatusSummary(
        documents=statuses,
        lots=(build_document_lot_status(lot_id, lot_label, statuses),),
    )


def build_document_lot_status(
    lot_id: str,
    label: str,
    document_statuses: Iterable[DocumentStatusRecord],
    *,
    critical_doc_codes: Iterable[str] | None = None,
) -> DocumentLotStatusRecord:
    statuses = tuple(document_statuses)
    critical_set = set(critical_doc_codes or ())
    blocked = [
        status for status in statuses if _status_blocks_lot(status, critical_set)
    ]
    if blocked:
        lot_status = DocumentLotStatus.BLOCKED
    elif all(status.status is DocumentStatus.GENERABLE for status in statuses):
        lot_status = DocumentLotStatus.READY
    else:
        lot_status = DocumentLotStatus.PARTIAL

    return DocumentLotStatusRecord(
        lot_id=lot_id,
        label=label,
        status=lot_status,
        document_statuses=statuses,
        reasons=tuple(reason for status in statuses for reason in status.reasons),
    )


def document_blocking_reasons(status: DocumentStatusRecord) -> tuple[DocumentStatusReason, ...]:
    return status.blocking_reasons


def document_missing_roles(status: DocumentStatusRecord) -> tuple[BusinessRole, ...]:
    return status.missing_roles


def document_missing_addresses(status: DocumentStatusRecord) -> tuple[AddressUsage, ...]:
    return status.missing_address_usages


def document_missing_canonical_fields(status: DocumentStatusRecord) -> tuple[str, ...]:
    return status.missing_canonical_fields


def document_unresolved_ambiguities(status: DocumentStatusRecord) -> tuple[str, ...]:
    return status.unresolved_ambiguity_keys


def _status_blocks_lot(
    status: DocumentStatusRecord,
    critical_doc_codes: set[str],
) -> bool:
    if critical_doc_codes:
        return status.doc_code in critical_doc_codes and status.is_blocked
    return status.status in {
        DocumentStatus.BLOCKED_MISSING_DATA,
        DocumentStatus.BLOCKED_UNRESOLVED_AMBIGUITY,
    }


def _requirement_for_code(
    doc_code: str,
    dossier: DossierRecord | None,
) -> DocumentRequirementRecord:
    if dossier and doc_code in dossier.document_requirements:
        return dossier.document_requirements[doc_code]
    if doc_code in SENTINEL_DOCUMENT_REQUIREMENTS:
        return sentinel_requirement(doc_code)
    catalog_document = CATALOG_BY_CODE.get(doc_code)
    if catalog_document:
        return _requirement_from_catalog(catalog_document)
    return DocumentRequirementRecord(
        doc_code=doc_code,
        doc_label=doc_code,
        status=DocumentRequirementStatus.CONTEXT_INCOMPLETE,
        action_needed="No DocumentRequirementRecord or catalog metadata is available.",
    )


def _requirement_from_catalog(catalog_document: object) -> DocumentRequirementRecord:
    status = _requirement_status_from_catalog(catalog_document.availability)
    return DocumentRequirementRecord(
        doc_code=catalog_document.document_code or catalog_document.document_key,
        doc_label=catalog_document.document_label,
        status=status,
        action_needed=catalog_document.notes or "",
    )


def _requirements_for_summary(
    dossier: DossierRecord | None,
    document_codes: Iterable[str] | None,
) -> tuple[DocumentRequirementRecord, ...]:
    if document_codes is not None:
        return tuple(_requirement_for_code(code, dossier) for code in document_codes)
    if dossier and dossier.document_requirements:
        return tuple(dossier.document_requirements.values())
    return tuple(SENTINEL_DOCUMENT_REQUIREMENTS.values())


def _requirement_status_from_catalog(
    availability: DocumentAvailability,
) -> DocumentRequirementStatus:
    if availability is DocumentAvailability.MANUAL_ONLY:
        return DocumentRequirementStatus.MANUAL_ONLY
    if availability is DocumentAvailability.NOT_IMPLEMENTED:
        return DocumentRequirementStatus.NOT_IMPLEMENTED
    if availability is DocumentAvailability.NEEDS_MAPPING:
        return DocumentRequirementStatus.CONTEXT_INCOMPLETE
    return DocumentRequirementStatus.EXPECTED


def _forced_status_from_metadata(
    requirement: DocumentRequirementRecord,
    catalog_document: object | None,
) -> DocumentStatus | None:
    if requirement.status is DocumentRequirementStatus.MANUAL_ONLY:
        return DocumentStatus.MANUAL_ONLY
    if requirement.status is DocumentRequirementStatus.NOT_IMPLEMENTED:
        return DocumentStatus.NOT_IMPLEMENTED
    if requirement.status is DocumentRequirementStatus.CONTEXT_INCOMPLETE:
        return DocumentStatus.CONTEXT_INCOMPLETE
    if catalog_document and catalog_document.availability is DocumentAvailability.MANUAL_ONLY:
        return DocumentStatus.MANUAL_ONLY
    if catalog_document and catalog_document.availability is DocumentAvailability.NOT_IMPLEMENTED:
        return DocumentStatus.NOT_IMPLEMENTED
    if catalog_document and catalog_document.availability is DocumentAvailability.NEEDS_MAPPING:
        return DocumentStatus.CONTEXT_INCOMPLETE
    return None


def _metadata_reasons(
    requirement: DocumentRequirementRecord,
    catalog_document: object | None,
) -> tuple[DocumentStatusReason, ...]:
    reasons: list[DocumentStatusReason] = []
    reasons.extend(_requirement_status_reasons(requirement))
    if catalog_document and catalog_document.notes:
        reasons.append(
            DocumentStatusReason(
                reason_type=DocumentStatusReasonType.CATALOG_NOTE,
                severity=ValidationSeverity.INFO,
                message=catalog_document.notes,
                source=DocumentStatusReasonSource.CATALOG,
                doc_code=requirement.doc_code,
            )
        )
    reasons.extend(_reserve_reasons(requirement.doc_code))
    return tuple(reasons)


def _requirement_status_reasons(
    requirement: DocumentRequirementRecord,
) -> tuple[DocumentStatusReason, ...]:
    if requirement.status is DocumentRequirementStatus.MANUAL_ONLY:
        return (
            DocumentStatusReason(
                reason_type=DocumentStatusReasonType.MANUAL_ONLY,
                severity=ValidationSeverity.INFO,
                message="Document visible but manual only; it must not enter generation.",
                source=DocumentStatusReasonSource.DOCUMENT_REQUIREMENT,
                doc_code=requirement.doc_code,
                action=requirement.action_needed,
            ),
        )
    if requirement.status is DocumentRequirementStatus.NOT_IMPLEMENTED:
        return (
            DocumentStatusReason(
                reason_type=DocumentStatusReasonType.NOT_IMPLEMENTED,
                severity=ValidationSeverity.BLOCKING,
                message="Document is not implemented in the engine.",
                source=DocumentStatusReasonSource.DOCUMENT_REQUIREMENT,
                doc_code=requirement.doc_code,
                action=requirement.action_needed,
            ),
        )
    if requirement.status is DocumentRequirementStatus.CONTEXT_INCOMPLETE:
        return (
            DocumentStatusReason(
                reason_type=DocumentStatusReasonType.CONTEXT_INCOMPLETE,
                severity=ValidationSeverity.WARNING,
                message="Document context is incomplete.",
                source=DocumentStatusReasonSource.DOCUMENT_REQUIREMENT,
                doc_code=requirement.doc_code,
                action=requirement.action_needed,
            ),
        )
    return ()


def _reserve_reasons(doc_code: str) -> tuple[DocumentStatusReason, ...]:
    return tuple(
        DocumentStatusReason(
            reason_type=DocumentStatusReasonType.RESERVE,
            severity=ValidationSeverity.WARNING,
            message=message,
            source=DocumentStatusReasonSource.RESERVE,
            doc_code=doc_code,
        )
        for message in DOCUMENT_RESERVES.get(doc_code, ())
    )


def _document_validation_reasons(
    dossier: DossierRecord,
    requirement: DocumentRequirementRecord,
) -> tuple[DocumentStatusReason, ...]:
    issues: list[ValidationIssue] = list(validate_document_requirement(dossier, requirement))
    issues.extend(_relevant_dossier_issues(dossier, requirement))
    return tuple(
        reason
        for issue in issues
        if (reason := _reason_from_issue(issue, DocumentStatusReasonSource.VALIDATION))
        is not None
    )


def _relevant_dossier_issues(
    dossier: DossierRecord,
    requirement: DocumentRequirementRecord,
) -> tuple[ValidationIssue, ...]:
    issues = [
        *validate_role_assignments(dossier),
        *validate_address_records(dossier),
        *validate_reuse_rules(dossier),
    ]
    roles = {*requirement.required_roles, *requirement.required_entities}
    addresses = set(requirement.required_address_usages)
    return tuple(
        issue
        for issue in issues
        if (issue.role in roles if issue.role else False)
        or (issue.address_usage in addresses if issue.address_usage else False)
        or _issue_mentions_requirement_ref(issue, requirement)
    )


def _flow_reasons_for_document(
    dossier: DossierRecord,
    requirement: DocumentRequirementRecord,
    flow: DossierFlow | None,
) -> tuple[DocumentStatusReason, ...]:
    flow = flow or build_dossier_flow(dossier)
    reasons: list[DocumentStatusReason] = []
    for result in _flow_results_for_doc(flow, requirement.doc_code):
        reasons.extend(_flow_result_reasons(result, requirement.doc_code))
    return tuple(reasons)


def _flow_results_for_doc(
    flow: DossierFlow,
    doc_code: str,
) -> tuple[FlowValidationResult, ...]:
    return tuple(
        result for result in flow.validation_results if doc_code in result.document_codes
    )


def _flow_result_reasons(
    result: FlowValidationResult,
    doc_code: str,
) -> tuple[DocumentStatusReason, ...]:
    reasons: list[DocumentStatusReason] = []
    for issue in result.issues:
        if issue.doc_code not in {None, doc_code}:
            continue
        reason = _reason_from_issue(
            issue,
            DocumentStatusReasonSource.DOSSIER_FLOW,
            block_id=result.block_id,
        )
        if reason:
            reasons.append(reason)
    return tuple(reasons)


def _reason_from_issue(
    issue: ValidationIssue,
    source: DocumentStatusReasonSource,
    *,
    block_id: DossierBlockId | None = None,
) -> DocumentStatusReason | None:
    reason_type = _reason_type_from_issue(issue)
    if reason_type is None:
        return None
    ambiguity_key = _ambiguity_key_from_issue(issue)
    severity = issue.severity
    if ambiguity_key in NON_BLOCKING_AMBIGUITY_KEYS:
        severity = ValidationSeverity.INFO
    return DocumentStatusReason(
        reason_type=reason_type,
        severity=severity,
        message=issue.message,
        source=source,
        doc_code=issue.doc_code,
        block_id=block_id,
        field_path=issue.field_path,
        role=issue.role,
        address_usage=issue.address_usage,
        ambiguity_key=ambiguity_key,
        source_ref=issue.source_ref,
        target_ref=issue.target_ref,
        action=issue.action,
    )


def _reason_type_from_issue(
    issue: ValidationIssue,
) -> DocumentStatusReasonType | None:
    if issue.issue_type is ValidationIssueType.MISSING_ROLE:
        return DocumentStatusReasonType.MISSING_ROLE
    if issue.issue_type is ValidationIssueType.MISSING_TYPED_ADDRESS:
        return DocumentStatusReasonType.MISSING_TYPED_ADDRESS
    if issue.issue_type is ValidationIssueType.MISSING_CANONICAL_VALUE:
        return DocumentStatusReasonType.MISSING_CANONICAL_VALUE
    if issue.issue_type is ValidationIssueType.UNRESOLVED_AMBIGUITY:
        return DocumentStatusReasonType.UNRESOLVED_AMBIGUITY
    if issue.issue_type in {
        ValidationIssueType.REUSE_CONFLICT,
        ValidationIssueType.IMPLICIT_ROLE_REUSE_FORBIDDEN,
        ValidationIssueType.ADDRESS_REUSE_FORBIDDEN,
        ValidationIssueType.ROLE_CONFUSION,
    }:
        return DocumentStatusReasonType.REUSE_CONFLICT
    return DocumentStatusReasonType.INVALID_DATA


def _status_from_reasons(
    doc_code: str,
    reasons: Iterable[DocumentStatusReason],
) -> DocumentStatus:
    reasons = tuple(reasons)
    missing_data_reasons = [
        reason
        for reason in reasons
        if reason.blocking
        and reason.reason_type
        in {
            DocumentStatusReasonType.MISSING_ROLE,
            DocumentStatusReasonType.MISSING_TYPED_ADDRESS,
            DocumentStatusReasonType.MISSING_CANONICAL_VALUE,
            DocumentStatusReasonType.REUSE_CONFLICT,
            DocumentStatusReasonType.INVALID_DATA,
        }
    ]
    if missing_data_reasons:
        return DocumentStatus.BLOCKED_MISSING_DATA

    blocking_ambiguities = [
        reason
        for reason in reasons
        if reason.reason_type is DocumentStatusReasonType.UNRESOLVED_AMBIGUITY
        and reason.ambiguity_key not in NON_BLOCKING_AMBIGUITY_KEYS
    ]
    if blocking_ambiguities:
        return DocumentStatus.BLOCKED_UNRESOLVED_AMBIGUITY

    if _reserve_reasons(doc_code):
        return DocumentStatus.GENERABLE_WITH_RESERVE
    return DocumentStatus.GENERABLE


def _status_record(
    *,
    requirement: DocumentRequirementRecord,
    status: DocumentStatus,
    reasons: tuple[DocumentStatusReason, ...],
    lot_id: str | None,
    family: str | None,
    catalog_document: object | None,
) -> DocumentStatusRecord:
    return DocumentStatusRecord(
        doc_code=requirement.doc_code,
        doc_label=requirement.doc_label,
        status=status,
        reasons=reasons,
        lot_id=lot_id,
        family=family,
        document_key=catalog_document.document_key if catalog_document else None,
        catalog_availability=(
            catalog_document.availability.value if catalog_document else None
        ),
        source_template_filename=(
            catalog_document.source_template_filename if catalog_document else None
        ),
    )


def _issue_mentions_requirement_ref(
    issue: ValidationIssue,
    requirement: DocumentRequirementRecord,
) -> bool:
    refs = {issue.source_ref, issue.target_ref}
    return any(
        rule_part in refs
        for rule in requirement.possible_reuse_rules
        for rule_part in (part.strip() for part in rule.split("->"))
    )


def _ambiguity_key_from_issue(issue: ValidationIssue) -> str | None:
    if issue.issue_type is not ValidationIssueType.UNRESOLVED_AMBIGUITY:
        return None
    marker = "not resolved:"
    if marker in issue.message:
        return issue.message.split(marker, maxsplit=1)[1].strip()
    marker = "before reuse."
    if issue.message.endswith(marker):
        return issue.target_ref or issue.source_ref
    return None


def _unique(items: Iterable[object]) -> tuple:
    return tuple(dict.fromkeys(item for item in items if item is not None))


def _unique_reasons(
    reasons: Iterable[DocumentStatusReason],
) -> tuple[DocumentStatusReason, ...]:
    deduped: dict[tuple[object, ...], DocumentStatusReason] = {}
    for reason in reasons:
        key = (
            reason.reason_type,
            reason.source,
            reason.block_id,
            reason.field_path,
            reason.role,
            reason.address_usage,
            reason.ambiguity_key,
            reason.source_ref,
            reason.target_ref,
            reason.message,
        )
        deduped.setdefault(key, reason)
    return tuple(deduped.values())
