from __future__ import annotations

import re
from collections import defaultdict

from sydel_doc_engine.front_data.models import (
    CanonicalRelationType,
    DocumentRequirementRecord,
    DossierRecord,
    ReuseRuleState,
    RoleAssignment,
    RoleTargetType,
    ValidationIssue,
    ValidationIssueType,
    ValidationSeverity,
)
from sydel_doc_engine.front_data.role_model import (
    assignment_has_represented_entity,
    has_transaction_party_role_on_same_target,
    is_role_reuse_allowed,
    is_scope_allowed,
    is_target_type_allowed,
    is_third_party_control_role,
    parse_role_ref,
    represented_entity_exists,
    requires_represented_entity,
    role_definition,
)


def validate_document_requirement(
    dossier: DossierRecord,
    requirement: DocumentRequirementRecord,
    *,
    include_unresolved_ambiguities: bool = True,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []

    required_roles = dict.fromkeys(
        (*requirement.required_roles, *requirement.required_entities)
    )
    for role in required_roles:
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

        source_role = parse_role_ref(rule.source_ref)
        target_role = parse_role_ref(rule.target_ref)
        if source_role and target_role and source_role is not target_role:
            if not rule.explicit:
                issues.append(
                    ValidationIssue(
                        issue_type=ValidationIssueType.IMPLICIT_ROLE_REUSE_FORBIDDEN,
                        severity=ValidationSeverity.BLOCKING,
                        message="Distinct roles cannot be reused implicitly.",
                        role=target_role,
                        source_ref=rule.source_ref,
                        target_ref=rule.target_ref,
                        action="Record an explicit RoleReusePolicy-backed rule.",
                    )
                )
            if not is_role_reuse_allowed(source_role, target_role):
                issues.append(
                    ValidationIssue(
                        issue_type=ValidationIssueType.ROLE_CONFUSION,
                        severity=ValidationSeverity.BLOCKING,
                        message=(
                            f"Role reuse is not allowed: {source_role.value} "
                            f"-> {target_role.value}"
                        ),
                        role=target_role,
                        source_ref=rule.source_ref,
                        target_ref=rule.target_ref,
                        action="Keep both role assignments distinct.",
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


def validate_role_assignments(dossier: DossierRecord) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for assignment in dossier.role_assignments.values():
        issues.extend(_validate_role_target(assignment))
        issues.extend(_validate_role_scope(assignment))
        issues.extend(_validate_represented_entity(dossier, assignment))
        issues.extend(_validate_third_party_role(dossier, assignment))
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
    issues.extend(validate_role_assignments(dossier))
    issues.extend(validate_reuse_rules(dossier))
    for requirement in dossier.document_requirements.values():
        issues.extend(validate_document_requirement(dossier, requirement))
    return tuple(issues)


def _validate_role_target(assignment: RoleAssignment) -> tuple[ValidationIssue, ...]:
    if is_target_type_allowed(assignment.role, assignment.target_type):
        return ()
    definition = role_definition(assignment.role)
    allowed = ", ".join(sorted(target_type.value for target_type in definition.target_types))
    return (
        ValidationIssue(
            issue_type=ValidationIssueType.INCOMPATIBLE_ROLE_TARGET,
            severity=ValidationSeverity.BLOCKING,
            message=(
                f"Role {assignment.role.value} cannot target "
                f"{assignment.target_type.value}; allowed: {allowed}."
            ),
            role=assignment.role,
            action="Change the target object kind or use another role.",
        ),
    )


def _validate_role_scope(assignment: RoleAssignment) -> tuple[ValidationIssue, ...]:
    if is_scope_allowed(assignment.role, assignment.scope):
        return ()
    definition = role_definition(assignment.role)
    allowed = ", ".join(sorted(scope.value for scope in definition.allowed_scopes))
    return (
        ValidationIssue(
            issue_type=ValidationIssueType.INVALID_ROLE_SCOPE,
            severity=ValidationSeverity.BLOCKING,
            message=(
                f"Role {assignment.role.value} cannot be scoped as "
                f"{assignment.scope.value}; allowed: {allowed}."
            ),
            role=assignment.role,
            action="Create a scoped assignment or an explicit reuse rule.",
        ),
    )


def _validate_represented_entity(
    dossier: DossierRecord,
    assignment: RoleAssignment,
) -> tuple[ValidationIssue, ...]:
    if not requires_represented_entity(assignment.role):
        return ()
    if assignment_has_represented_entity(assignment) and represented_entity_exists(
        dossier,
        assignment,
    ):
        return ()
    return (
        ValidationIssue(
            issue_type=ValidationIssueType.MISSING_REPRESENTED_ENTITY,
            severity=ValidationSeverity.BLOCKING,
            message="A representative role must reference the represented company.",
            role=assignment.role,
            action="Set represented_target_type and represented_target_id explicitly.",
        ),
    )


def _validate_third_party_role(
    dossier: DossierRecord,
    assignment: RoleAssignment,
) -> tuple[ValidationIssue, ...]:
    if not is_third_party_control_role(assignment.role):
        return ()
    if not has_transaction_party_role_on_same_target(dossier, assignment):
        return ()
    return (
        ValidationIssue(
            issue_type=ValidationIssueType.THIRD_PARTY_ROLE_CONFLICT,
            severity=ValidationSeverity.BLOCKING,
            message=(
                f"Role {assignment.role.value} is a control/evaluation third party "
                "and cannot be a party to the same operation."
            ),
            role=assignment.role,
            action="Use a separate person or organization for this third-party role.",
        ),
    )


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
