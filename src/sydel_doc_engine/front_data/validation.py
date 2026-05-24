from __future__ import annotations

import re
from collections import defaultdict

from sydel_doc_engine.front_data.models import (
    CanonicalRelationType,
    DocumentRequirementRecord,
    DossierRecord,
    ReuseRuleState,
    RoleTargetType,
    ValidationIssue,
    ValidationIssueType,
    ValidationSeverity,
)


def validate_document_requirement(
    dossier: DossierRecord,
    requirement: DocumentRequirementRecord,
    *,
    include_unresolved_ambiguities: bool = True,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []

    for role in (*requirement.required_roles, *requirement.required_entities):
        if not dossier.roles_for(role):
            issues.append(
                ValidationIssue(
                    issue_type=ValidationIssueType.MISSING_ROLE,
                    severity=ValidationSeverity.BLOCKING,
                    message=f"Required role is missing: {role.value}",
                    doc_code=requirement.doc_code,
                    role=role,
                    action="Assign the role explicitly to a person or company.",
                )
            )

    for usage in requirement.required_address_usages:
        if not dossier.is_address_usage_available(usage):
            issues.append(
                ValidationIssue(
                    issue_type=ValidationIssueType.MISSING_TYPED_ADDRESS,
                    severity=ValidationSeverity.BLOCKING,
                    message=f"Required typed address is missing: {usage.value}",
                    doc_code=requirement.doc_code,
                    address_usage=usage,
                    action="Create the typed address or activate an explicit reuse rule.",
                )
            )

    for field_path in requirement.required_canonical_fields:
        if not _canonical_value_present(dossier, field_path):
            issues.append(
                ValidationIssue(
                    issue_type=ValidationIssueType.MISSING_CANONICAL_VALUE,
                    severity=ValidationSeverity.BLOCKING,
                    message=f"Required canonical value is missing: {field_path}",
                    doc_code=requirement.doc_code,
                    field_path=field_path,
                    action="Populate the canonical field without using a legacy alias as source.",
                )
            )

    if include_unresolved_ambiguities:
        issues.extend(validate_unresolved_ambiguities(dossier, requirement))

    return tuple(issues)


def validate_unresolved_ambiguities(
    dossier: DossierRecord,
    requirement: DocumentRequirementRecord,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for key in requirement.unresolved_ambiguity_keys:
        if key not in dossier.resolved_ambiguity_keys:
            issues.append(
                ValidationIssue(
                    issue_type=ValidationIssueType.UNRESOLVED_AMBIGUITY,
                    severity=ValidationSeverity.WARNING,
                    message=f"Document ambiguity is not resolved: {key}",
                    doc_code=requirement.doc_code,
                    action=requirement.action_needed,
                )
            )
    return tuple(issues)


def validate_reuse_rules(dossier: DossierRecord) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    active_by_target: dict[str, list[ReuseRuleState]] = defaultdict(list)

    for rule in dossier.reuse_rules.values():
        if not rule.is_active:
            continue

        active_by_target[rule.target_ref].append(rule)

        if rule.relation_type is CanonicalRelationType.DISTINCT_FIELDS:
            issues.append(
                ValidationIssue(
                    issue_type=ValidationIssueType.REUSE_CONFLICT,
                    severity=ValidationSeverity.BLOCKING,
                    message="A DISTINCT_FIELDS relation cannot be reused automatically.",
                    source_ref=rule.source_ref,
                    target_ref=rule.target_ref,
                    action="Remove the rule or change the target into an explicit override.",
                )
            )
        if rule.relation_type is CanonicalRelationType.UNCERTAIN_REQUIRES_HUMAN_DECISION:
            issues.append(
                ValidationIssue(
                    issue_type=ValidationIssueType.UNRESOLVED_AMBIGUITY,
                    severity=ValidationSeverity.BLOCKING,
                    message="An uncertain relation must be decided before reuse.",
                    source_ref=rule.source_ref,
                    target_ref=rule.target_ref,
                    action="Record the human decision before activating this reuse rule.",
                )
            )

    for target_ref, rules in active_by_target.items():
        source_refs = {rule.source_ref for rule in rules}
        if len(source_refs) > 1 and not any(rule.allow_override for rule in rules):
            issues.append(
                ValidationIssue(
                    issue_type=ValidationIssueType.REUSE_CONFLICT,
                    severity=ValidationSeverity.BLOCKING,
                    message="Multiple active reuse rules target the same field or address.",
                    target_ref=target_ref,
                    action="Keep one explicit source or mark the override intentionally.",
                )
            )

    return tuple(issues)


def validate_required_entities_linked(dossier: DossierRecord) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for assignment in dossier.role_assignments.values():
        if (
            assignment.target_type is RoleTargetType.PERSON
            and assignment.target_id not in dossier.persons
        ):
            issues.append(
                ValidationIssue(
                    issue_type=ValidationIssueType.UNLINKED_REQUIRED_ENTITY,
                    severity=ValidationSeverity.BLOCKING,
                    message=f"Role target person does not exist: {assignment.target_id}",
                    role=assignment.role,
                    action="Create the PersonRecord or correct the RoleAssignment target.",
                )
            )
        if (
            assignment.target_type is RoleTargetType.COMPANY
            and assignment.target_id not in dossier.companies
        ):
            issues.append(
                ValidationIssue(
                    issue_type=ValidationIssueType.UNLINKED_REQUIRED_ENTITY,
                    severity=ValidationSeverity.BLOCKING,
                    message=f"Role target company does not exist: {assignment.target_id}",
                    role=assignment.role,
                    action="Create the CompanyRecord or correct the RoleAssignment target.",
                )
            )
    return tuple(issues)


def validate_dossier(dossier: DossierRecord) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_required_entities_linked(dossier))
    issues.extend(validate_reuse_rules(dossier))
    for requirement in dossier.document_requirements.values():
        issues.extend(validate_document_requirement(dossier, requirement))
    return tuple(issues)


def _canonical_value_present(dossier: DossierRecord, required_path: str) -> bool:
    if required_path in dossier.canonical_values:
        return True

    pattern = _required_field_pattern(required_path)
    return any(pattern.match(field_path) for field_path in dossier.canonical_values)


def _required_field_pattern(required_path: str) -> re.Pattern[str]:
    collection_path = required_path.endswith("[]")
    wildcard_path = required_path.endswith(".*")
    base = required_path
    if collection_path:
        base = required_path[:-2]
    if wildcard_path:
        base = required_path[:-2]

    pattern = re.escape(base)
    pattern = pattern.replace(r"\{role\}", r"[^.]+")
    pattern = pattern.replace(r"\{champ\}", r"[^.]+")

    if collection_path:
        pattern = f"{pattern}(\\[\\d+\\])?(\\..+)?"
    elif wildcard_path:
        pattern = f"{pattern}(\\..+)?"

    return re.compile(f"^{pattern}$")
