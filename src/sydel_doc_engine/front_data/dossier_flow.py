from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from typing import TypeVar

from sydel_doc_engine.front_data.address_model import ADDRESS_REUSE_POLICIES
from sydel_doc_engine.front_data.canonical_mapping import (
    all_sentinel_requirements,
    sentinel_requirement,
)
from sydel_doc_engine.front_data.models import (
    AddressUsage,
    BusinessRole,
    CanonicalFieldValue,
    DocumentRequirementRecord,
    DossierRecord,
    OperationType,
    ReuseRuleStatus,
    ValidationIssue,
    ValidationIssueType,
    ValidationSeverity,
)
from sydel_doc_engine.front_data.role_model import ROLE_REUSE_POLICIES

T = TypeVar("T")


class DossierStepId(StrEnum):
    QUALIFICATION = "qualification"
    PERSONS = "fiche_personnes"
    COMPANY = "fiche_societe"
    ROLES_PARTIES = "roles_parties"
    ADDRESSES = "adresses"
    CAPITAL_TITLES_APPORTS = "capital_titres_apports"
    ORDER = "ordre_inscription"
    OPERATIONS = "operations"
    DOCUMENTS = "documents_attendus"
    GENERATION = "generation"


class DossierBlockId(StrEnum):
    OPERATION_QUALIFICATION = "operation_qualification"
    PERSON_RECORDS = "person_records"
    COMPANY_RECORDS = "company_records"
    ROLE_ASSIGNMENTS = "role_assignments"
    ADDRESS_USAGE = "address_usage"
    ADDRESS_REUSE = "address_reuse"
    CAPITAL_ASSOCIATES = "capital_associes"
    CAPITAL_TITLES = "capital_titres"
    APPORTS = "apports"
    ORDER_IDENTIFIERS = "ordre_identifiants"
    ORDER_MANDATE = "ordre_mandataire"
    ORDER_EVIDENCE = "ordre_pieces"
    CESSION_CABINET = "cession_cabinet"
    CESSION_PRICE = "cession_prix"
    CESSION_ORIGIN = "cession_origine"
    CESSION_EXERCISES = "cession_exercices"
    BAIL = "bail"
    FINANCING = "financement"
    SCM = "scm"
    SCM_ASSOCIATES = "scm_associes"
    SPFPL = "spfpl"
    APPORT_TITRES = "apport_titres"
    DOCUMENT_REQUIREMENTS = "documents_attendus"
    GENERATION_READINESS = "generation_readiness"


class FlowStatus(StrEnum):
    INACTIVE = "inactive"
    AVAILABLE = "available"
    BLOCKED = "blocked"
    WARNING = "warning"
    COMPLETE = "complete"


@dataclass(frozen=True)
class DossierStep:
    id: DossierStepId
    label: str
    order: int
    description: str
    dependencies: tuple[DossierStepId, ...] = ()


@dataclass(frozen=True)
class BlockActivationRule:
    block_id: DossierBlockId
    required_document_codes: tuple[str, ...] = ()
    required_operation_types: tuple[OperationType, ...] = ()
    always_active: bool = False
    notes: str = ""


@dataclass(frozen=True)
class FlowDependency:
    source_step: DossierStepId
    target_step: DossierStepId
    source_block: DossierBlockId | None = None
    target_block: DossierBlockId | None = None
    reason: str = ""
    blocking: bool = True


@dataclass(frozen=True)
class DossierBlock:
    id: DossierBlockId
    label: str
    step_id: DossierStepId
    status: FlowStatus
    activation_rule: BlockActivationRule
    document_codes: tuple[str, ...] = ()
    required_roles: tuple[BusinessRole, ...] = ()
    required_address_usages: tuple[AddressUsage, ...] = ()
    required_canonical_fields: tuple[str, ...] = ()
    possible_reuse_rules: tuple[str, ...] = ()
    unresolved_ambiguity_keys: tuple[str, ...] = ()
    dependencies: tuple[DossierBlockId, ...] = ()
    notes: str = ""

    @property
    def active(self) -> bool:
        return self.status is not FlowStatus.INACTIVE


@dataclass(frozen=True)
class FlowValidationResult:
    block_id: DossierBlockId
    status: FlowStatus
    issues: tuple[ValidationIssue, ...] = ()
    missing_roles: tuple[BusinessRole, ...] = ()
    missing_address_usages: tuple[AddressUsage, ...] = ()
    missing_canonical_fields: tuple[str, ...] = ()
    unresolved_ambiguity_keys: tuple[str, ...] = ()
    document_codes: tuple[str, ...] = ()

    @property
    def blocking_issues(self) -> tuple[ValidationIssue, ...]:
        return tuple(
            issue for issue in self.issues if issue.severity is ValidationSeverity.BLOCKING
        )

    @property
    def warning_issues(self) -> tuple[ValidationIssue, ...]:
        return tuple(
            issue for issue in self.issues if issue.severity is ValidationSeverity.WARNING
        )


@dataclass(frozen=True)
class DossierFlow:
    steps: tuple[DossierStep, ...]
    blocks: tuple[DossierBlock, ...]
    dependencies: tuple[FlowDependency, ...]
    document_requirements: tuple[DocumentRequirementRecord, ...]
    validation_results: tuple[FlowValidationResult, ...]

    def step(self, step_id: DossierStepId) -> DossierStep:
        return next(step for step in self.steps if step.id is step_id)

    def block(self, block_id: DossierBlockId) -> DossierBlock:
        return next(block for block in self.blocks if block.id is block_id)

    def validation_for_block(self, block_id: DossierBlockId) -> FlowValidationResult:
        return next(result for result in self.validation_results if result.block_id is block_id)

    def blocks_for_step(self, step_id: DossierStepId) -> tuple[DossierBlock, ...]:
        return tuple(block for block in self.blocks if block.step_id is step_id)

    def active_blocks(self) -> tuple[DossierBlock, ...]:
        return tuple(block for block in self.blocks if block.active)

    def documents_for_block(self, block_id: DossierBlockId) -> tuple[str, ...]:
        return self.block(block_id).document_codes


@dataclass(frozen=True)
class _BlockSpec:
    id: DossierBlockId
    label: str
    step_id: DossierStepId
    activation_rule: BlockActivationRule
    required_roles: tuple[BusinessRole, ...] = ()
    required_address_usages: tuple[AddressUsage, ...] = ()
    required_canonical_fields: tuple[str, ...] = ()
    possible_reuse_rules: tuple[str, ...] = ()
    unresolved_ambiguity_keys: tuple[str, ...] = ()
    dependencies: tuple[DossierBlockId, ...] = ()
    include_document_requirements: bool = False
    notes: str = ""


SENTINEL_CODES: tuple[str, ...] = (
    "DOC-002",
    "DOC-034",
    "DOC-017",
    "DOC-033",
    "DOC-009",
    "DOC-041",
    "DOC-025",
)


DOSSIER_STEPS: tuple[DossierStep, ...] = (
    DossierStep(
        id=DossierStepId.QUALIFICATION,
        label="Qualification / type d'operation",
        order=10,
        description="Selectionne les familles documentaires et les operations du dossier.",
    ),
    DossierStep(
        id=DossierStepId.PERSONS,
        label="Fiche client / personnes",
        order=20,
        description="Regroupe les personnes physiques sans role implicite.",
        dependencies=(DossierStepId.QUALIFICATION,),
    ),
    DossierStep(
        id=DossierStepId.COMPANY,
        label="Fiche societe",
        order=30,
        description="Regroupe les personnes morales distinctes.",
        dependencies=(DossierStepId.QUALIFICATION,),
    ),
    DossierStep(
        id=DossierStepId.ROLES_PARTIES,
        label="Roles et parties",
        order=40,
        description="Affecte les roles aux personnes et societes par declaration explicite.",
        dependencies=(DossierStepId.PERSONS, DossierStepId.COMPANY),
    ),
    DossierStep(
        id=DossierStepId.ADDRESSES,
        label="Adresses",
        order=50,
        description="Saisit les adresses typees et les reutilisations tracees.",
        dependencies=(DossierStepId.PERSONS, DossierStepId.COMPANY),
    ),
    DossierStep(
        id=DossierStepId.CAPITAL_TITLES_APPORTS,
        label="Capital / titres / apports",
        order=60,
        description="Structure les titres, apports, associes et repartitions.",
        dependencies=(DossierStepId.COMPANY, DossierStepId.ROLES_PARTIES),
    ),
    DossierStep(
        id=DossierStepId.ORDER,
        label="Ordre / inscription",
        order=70,
        description="Isole l'inscrit, la societe inscrite, le conseil de l'ordre et le mandataire.",
        dependencies=(
            DossierStepId.PERSONS,
            DossierStepId.COMPANY,
            DossierStepId.ROLES_PARTIES,
            DossierStepId.ADDRESSES,
        ),
    ),
    DossierStep(
        id=DossierStepId.OPERATIONS,
        label="Cession / apport / SCM / bail / financement",
        order=80,
        description="Porte les blocs operationnels sans raccourci entre parties.",
        dependencies=(
            DossierStepId.ROLES_PARTIES,
            DossierStepId.ADDRESSES,
            DossierStepId.CAPITAL_TITLES_APPORTS,
        ),
    ),
    DossierStep(
        id=DossierStepId.DOCUMENTS,
        label="Documents attendus",
        order=90,
        description="Expose les documents concernes et leurs donnees consommees.",
        dependencies=(
            DossierStepId.ROLES_PARTIES,
            DossierStepId.ADDRESSES,
            DossierStepId.ORDER,
            DossierStepId.OPERATIONS,
        ),
    ),
    DossierStep(
        id=DossierStepId.GENERATION,
        label="Generation",
        order=100,
        description="Declare les blocages et warnings avant appel aux generateurs.",
        dependencies=(DossierStepId.DOCUMENTS,),
    ),
)


FLOW_DEPENDENCIES: tuple[FlowDependency, ...] = (
    FlowDependency(
        source_step=DossierStepId.QUALIFICATION,
        target_step=DossierStepId.PERSONS,
        reason="Les personnes dependent de la famille de dossier retenue.",
    ),
    FlowDependency(
        source_step=DossierStepId.QUALIFICATION,
        target_step=DossierStepId.COMPANY,
        reason="Les societes affichees dependent de l'operation qualifiee.",
    ),
    FlowDependency(
        source_step=DossierStepId.PERSONS,
        target_step=DossierStepId.ROLES_PARTIES,
        target_block=DossierBlockId.ROLE_ASSIGNMENTS,
        reason="Un role ne doit pas creer une personne implicite.",
    ),
    FlowDependency(
        source_step=DossierStepId.COMPANY,
        target_step=DossierStepId.ROLES_PARTIES,
        target_block=DossierBlockId.ROLE_ASSIGNMENTS,
        reason="Un role societe pointe vers une societe deja identifiee.",
    ),
    FlowDependency(
        source_step=DossierStepId.ADDRESSES,
        target_step=DossierStepId.OPERATIONS,
        source_block=DossierBlockId.ADDRESS_USAGE,
        reason="Les operations consomment des adresses typees, jamais fusionnees.",
    ),
    FlowDependency(
        source_step=DossierStepId.ROLES_PARTIES,
        target_step=DossierStepId.ORDER,
        source_block=DossierBlockId.ROLE_ASSIGNMENTS,
        target_block=DossierBlockId.ORDER_MANDATE,
        reason="Mandataire, signataire et ordre sont des roles distincts.",
    ),
    FlowDependency(
        source_step=DossierStepId.DOCUMENTS,
        target_step=DossierStepId.GENERATION,
        source_block=DossierBlockId.DOCUMENT_REQUIREMENTS,
        target_block=DossierBlockId.GENERATION_READINESS,
        reason="La generation depend des pre-requis documentaires explicites.",
    ),
)


def build_dossier_flow(
    dossier: DossierRecord | None = None,
    *,
    document_codes: Iterable[str] | None = None,
) -> DossierFlow:
    requirements = _resolve_requirements(dossier, document_codes)
    active_document_codes = tuple(requirement.doc_code for requirement in requirements)
    blocks: list[DossierBlock] = []
    validation_results: list[FlowValidationResult] = []

    for spec in BLOCK_SPECS:
        related_requirements = _related_requirements(spec, requirements)
        active = _is_block_active(spec, related_requirements, active_document_codes, dossier)
        block_document_codes = tuple(
            requirement.doc_code for requirement in related_requirements
        )
        block = _build_block(spec, related_requirements, active)
        result = _validate_block(dossier, block) if active else _inactive_result(block)
        blocks.append(
            DossierBlock(
                id=block.id,
                label=block.label,
                step_id=block.step_id,
                status=result.status,
                activation_rule=block.activation_rule,
                document_codes=block_document_codes,
                required_roles=block.required_roles,
                required_address_usages=block.required_address_usages,
                required_canonical_fields=block.required_canonical_fields,
                possible_reuse_rules=block.possible_reuse_rules,
                unresolved_ambiguity_keys=block.unresolved_ambiguity_keys,
                dependencies=block.dependencies,
                notes=block.notes,
            )
        )
        validation_results.append(result)

    return DossierFlow(
        steps=DOSSIER_STEPS,
        blocks=tuple(blocks),
        dependencies=FLOW_DEPENDENCIES,
        document_requirements=requirements,
        validation_results=tuple(validation_results),
    )


def build_sentinel_dossier_flow(
    dossier: DossierRecord | None = None,
) -> DossierFlow:
    return build_dossier_flow(dossier, document_codes=SENTINEL_CODES if dossier is None else None)


def validate_dossier_flow(dossier: DossierRecord) -> tuple[FlowValidationResult, ...]:
    return build_dossier_flow(dossier).validation_results


def _resolve_requirements(
    dossier: DossierRecord | None,
    document_codes: Iterable[str] | None,
) -> tuple[DocumentRequirementRecord, ...]:
    if dossier and dossier.document_requirements:
        return tuple(dossier.document_requirements.values())
    if document_codes is not None:
        return tuple(sentinel_requirement(code) for code in document_codes)
    return all_sentinel_requirements()


def _related_requirements(
    spec: _BlockSpec,
    requirements: tuple[DocumentRequirementRecord, ...],
) -> tuple[DocumentRequirementRecord, ...]:
    codes = spec.activation_rule.required_document_codes
    if spec.activation_rule.always_active or not codes:
        return requirements
    code_set = set(codes)
    return tuple(requirement for requirement in requirements if requirement.doc_code in code_set)


def _is_block_active(
    spec: _BlockSpec,
    related_requirements: tuple[DocumentRequirementRecord, ...],
    active_document_codes: tuple[str, ...],
    dossier: DossierRecord | None,
) -> bool:
    rule = spec.activation_rule
    if rule.always_active:
        return bool(active_document_codes)
    if rule.required_document_codes and not related_requirements:
        return False
    if rule.required_operation_types:
        if not dossier:
            return bool(related_requirements)
        operation_types = {
            context.operation_type for context in dossier.operation_contexts.values()
        }
        if operation_types.intersection(rule.required_operation_types):
            return True
        return bool(related_requirements)
    return bool(related_requirements)


def _build_block(
    spec: _BlockSpec,
    requirements: tuple[DocumentRequirementRecord, ...],
    active: bool,
) -> DossierBlock:
    status = FlowStatus.AVAILABLE if active else FlowStatus.INACTIVE
    roles = list(spec.required_roles)
    addresses = list(spec.required_address_usages)
    fields = list(spec.required_canonical_fields)
    reuse_rules = list(spec.possible_reuse_rules)
    ambiguities = list(spec.unresolved_ambiguity_keys)

    if spec.include_document_requirements:
        for requirement in requirements:
            roles.extend((*requirement.required_roles, *requirement.required_entities))
            addresses.extend(requirement.required_address_usages)
            fields.extend(requirement.required_canonical_fields)
            reuse_rules.extend(requirement.possible_reuse_rules)
            ambiguities.extend(requirement.unresolved_ambiguity_keys)

    return DossierBlock(
        id=spec.id,
        label=spec.label,
        step_id=spec.step_id,
        status=status,
        activation_rule=spec.activation_rule,
        document_codes=tuple(requirement.doc_code for requirement in requirements),
        required_roles=_unique(roles),
        required_address_usages=_unique(addresses),
        required_canonical_fields=_unique(fields),
        possible_reuse_rules=_unique(reuse_rules),
        unresolved_ambiguity_keys=_unique(ambiguities),
        dependencies=spec.dependencies,
        notes=spec.notes,
    )


def _validate_block(
    dossier: DossierRecord | None,
    block: DossierBlock,
) -> FlowValidationResult:
    if dossier is None:
        return FlowValidationResult(
            block_id=block.id,
            status=FlowStatus.AVAILABLE,
            document_codes=block.document_codes,
        )

    issues: list[ValidationIssue] = []
    missing_roles = tuple(
        role for role in block.required_roles if not dossier.roles_for(role)
    )
    for role in missing_roles:
        issues.append(
            ValidationIssue(
                issue_type=ValidationIssueType.MISSING_ROLE,
                severity=ValidationSeverity.BLOCKING,
                message=f"Required flow role is missing: {role.value}",
                doc_code=_single_doc_code(block.document_codes),
                role=role,
                action="Assign the role explicitly before opening generation.",
            )
        )

    missing_addresses = tuple(
        usage
        for usage in block.required_address_usages
        if not dossier.is_address_usage_available(usage)
    )
    for usage in missing_addresses:
        issues.append(
            ValidationIssue(
                issue_type=ValidationIssueType.MISSING_TYPED_ADDRESS,
                severity=ValidationSeverity.BLOCKING,
                message=f"Required flow address is missing: {usage.value}",
                doc_code=_single_doc_code(block.document_codes),
                address_usage=usage,
                action="Create the typed address or activate an explicit reuse rule.",
            )
        )

    missing_fields = tuple(
        field_path
        for field_path in block.required_canonical_fields
        if not _canonical_value_present(dossier, field_path)
    )
    for field_path in missing_fields:
        issues.append(
            ValidationIssue(
                issue_type=ValidationIssueType.MISSING_CANONICAL_VALUE,
                severity=ValidationSeverity.BLOCKING,
                message=f"Required flow canonical value is missing: {field_path}",
                doc_code=_single_doc_code(block.document_codes),
                field_path=field_path,
                action="Populate the canonical field in the data layer.",
            )
        )

    unresolved = tuple(
        key for key in block.unresolved_ambiguity_keys if key not in dossier.resolved_ambiguity_keys
    )
    for key in unresolved:
        issues.append(
            ValidationIssue(
                issue_type=ValidationIssueType.UNRESOLVED_AMBIGUITY,
                severity=ValidationSeverity.WARNING,
                message=f"Flow ambiguity is not resolved: {key}",
                doc_code=_single_doc_code(block.document_codes),
                action="Keep the block orange until the product/legal decision is recorded.",
            )
        )

    status = _status_from_issues(issues)
    return FlowValidationResult(
        block_id=block.id,
        status=status,
        issues=tuple(issues),
        missing_roles=missing_roles,
        missing_address_usages=missing_addresses,
        missing_canonical_fields=missing_fields,
        unresolved_ambiguity_keys=unresolved,
        document_codes=block.document_codes,
    )


def _inactive_result(block: DossierBlock) -> FlowValidationResult:
    return FlowValidationResult(
        block_id=block.id,
        status=FlowStatus.INACTIVE,
        document_codes=block.document_codes,
    )


def _status_from_issues(issues: list[ValidationIssue]) -> FlowStatus:
    if any(issue.severity is ValidationSeverity.BLOCKING for issue in issues):
        return FlowStatus.BLOCKED
    if any(issue.severity is ValidationSeverity.WARNING for issue in issues):
        return FlowStatus.WARNING
    return FlowStatus.COMPLETE


def _canonical_value_present(dossier: DossierRecord, required_field_path: str) -> bool:
    if required_field_path in dossier.canonical_values:
        return _value_has_content(dossier.canonical_values[required_field_path])

    pattern = _required_field_pattern(required_field_path)
    if pattern is None:
        return False
    return any(
        _value_has_content(value) and pattern.fullmatch(field_path)
        for field_path, value in dossier.canonical_values.items()
    )


def _required_field_pattern(required_field_path: str) -> re.Pattern[str] | None:
    escaped = re.escape(required_field_path)
    escaped = escaped.replace(re.escape("{role}"), r"[^.]+")
    escaped = escaped.replace(re.escape("{champ}"), r"[^.]+")
    if escaped.endswith(re.escape(".*")):
        escaped = escaped[: -len(re.escape(".*"))] + r"\..+"
    if escaped.endswith(re.escape("[]")):
        escaped = escaped[: -len(re.escape("[]"))] + r"\[\d+\].+"
    if escaped == re.escape(required_field_path):
        return None
    return re.compile(escaped)


def _value_has_content(value: CanonicalFieldValue) -> bool:
    return value.value not in (None, "")


def _single_doc_code(document_codes: tuple[str, ...]) -> str | None:
    if len(document_codes) == 1:
        return document_codes[0]
    return None


def _unique(items: Iterable[T]) -> tuple[T, ...]:
    return tuple(dict.fromkeys(items))


def _all_role_reuse_labels() -> tuple[str, ...]:
    return tuple(
        f"role:{policy.source_role.value} -> role:{policy.target_role.value}"
        for policy in ROLE_REUSE_POLICIES.values()
    )


def _all_address_reuse_labels() -> tuple[str, ...]:
    return tuple(
        f"address:{policy.source_usage.value} -> address:{policy.target_usage.value}"
        for policy in ADDRESS_REUSE_POLICIES.values()
    )


def _active_reuse_rule_labels(dossier: DossierRecord) -> tuple[str, ...]:
    return tuple(
        f"{rule.source_ref} -> {rule.target_ref}"
        for rule in dossier.reuse_rules.values()
        if rule.status is ReuseRuleStatus.ACTIVE
    )


def active_reuse_rules_for_flow(dossier: DossierRecord) -> tuple[str, ...]:
    """Expose active reuse links without creating additional business facts."""
    return _active_reuse_rule_labels(dossier)


BLOCK_SPECS: tuple[_BlockSpec, ...] = (
    _BlockSpec(
        id=DossierBlockId.OPERATION_QUALIFICATION,
        label="Qualification dossier",
        step_id=DossierStepId.QUALIFICATION,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.OPERATION_QUALIFICATION,
            always_active=True,
            notes="Premier bloc du dossier, independant de l'UI.",
        ),
        include_document_requirements=True,
        notes="Liste les documents retenus et les operations pressenties.",
    ),
    _BlockSpec(
        id=DossierBlockId.PERSON_RECORDS,
        label="Personnes physiques",
        step_id=DossierStepId.PERSONS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.PERSON_RECORDS,
            always_active=True,
        ),
        include_document_requirements=True,
        notes="Collecte les personnes sans deduire leurs roles.",
    ),
    _BlockSpec(
        id=DossierBlockId.COMPANY_RECORDS,
        label="Personnes morales",
        step_id=DossierStepId.COMPANY,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.COMPANY_RECORDS,
            always_active=True,
        ),
        include_document_requirements=True,
        notes="Collecte les societes distinctes, y compris banque, ordre, SCM et SPFPL.",
    ),
    _BlockSpec(
        id=DossierBlockId.ROLE_ASSIGNMENTS,
        label="Assignments de roles",
        step_id=DossierStepId.ROLES_PARTIES,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.ROLE_ASSIGNMENTS,
            always_active=True,
        ),
        possible_reuse_rules=_all_role_reuse_labels(),
        include_document_requirements=True,
        dependencies=(DossierBlockId.PERSON_RECORDS, DossierBlockId.COMPANY_RECORDS),
        notes="Aucune fusion silencieuse entre praticien, signataire et mandataire.",
    ),
    _BlockSpec(
        id=DossierBlockId.ADDRESS_USAGE,
        label="Adresses typees",
        step_id=DossierStepId.ADDRESSES,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.ADDRESS_USAGE,
            always_active=True,
        ),
        include_document_requirements=True,
        dependencies=(DossierBlockId.PERSON_RECORDS, DossierBlockId.COMPANY_RECORDS),
        notes="Une adresse reste typee par usage meme si son texte est identique.",
    ),
    _BlockSpec(
        id=DossierBlockId.ADDRESS_REUSE,
        label="Reutilisations d'adresses",
        step_id=DossierStepId.ADDRESSES,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.ADDRESS_REUSE,
            always_active=True,
        ),
        possible_reuse_rules=_all_address_reuse_labels(),
        dependencies=(DossierBlockId.ADDRESS_USAGE,),
        notes="Expose les reutilisations permises sans les activer automatiquement.",
    ),
    _BlockSpec(
        id=DossierBlockId.CAPITAL_ASSOCIATES,
        label="Associes et repartitions",
        step_id=DossierStepId.CAPITAL_TITLES_APPORTS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.CAPITAL_ASSOCIATES,
            required_document_codes=("DOC-017", "DOC-025"),
            required_operation_types=(OperationType.CREATION, OperationType.APPORT),
        ),
        required_roles=(BusinessRole.ASSOCIE,),
        required_canonical_fields=("capital.repartition_associes", "statuts_civils.associes[]"),
        unresolved_ambiguity_keys=(
            "pluralite_associes_statuts_selarl",
            "associes_scm_one_to_six",
        ),
        dependencies=(DossierBlockId.ROLE_ASSIGNMENTS, DossierBlockId.COMPANY_RECORDS),
    ),
    _BlockSpec(
        id=DossierBlockId.CAPITAL_TITLES,
        label="Capital et titres",
        step_id=DossierStepId.CAPITAL_TITLES_APPORTS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.CAPITAL_TITLES,
            required_document_codes=("DOC-017", "DOC-025", "DOC-041"),
            required_operation_types=(OperationType.CREATION, OperationType.APPORT),
        ),
        required_canonical_fields=(
            "capital.titres.nombre_total",
            "capital.titres.valeur_nominale",
            "capital.titres.*",
        ),
        unresolved_ambiguity_keys=("seuils_gerance", "apports_parts_per_associe"),
        dependencies=(DossierBlockId.CAPITAL_ASSOCIATES,),
    ),
    _BlockSpec(
        id=DossierBlockId.APPORTS,
        label="Apports",
        step_id=DossierStepId.CAPITAL_TITLES_APPORTS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.APPORTS,
            required_document_codes=("DOC-025",),
            required_operation_types=(OperationType.APPORT,),
        ),
        required_canonical_fields=("apport.numeraire.montant", "apport.nature.montant"),
        dependencies=(DossierBlockId.CAPITAL_TITLES,),
    ),
    _BlockSpec(
        id=DossierBlockId.ORDER_IDENTIFIERS,
        label="Ordre et identifiants ordinaux",
        step_id=DossierStepId.ORDER,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.ORDER_IDENTIFIERS,
            required_document_codes=("DOC-034", "DOC-017"),
            required_operation_types=(OperationType.ORDRE,),
        ),
        required_roles=(BusinessRole.ORDRE_PROFESSIONNEL,),
        required_address_usages=(AddressUsage.ORDRE,),
        required_canonical_fields=(
            "ordre.professionnel",
            "ordre.adresse",
            "personne.{role}.numero_ordre",
            "personne.{role}.numero_rpps",
            "personne.{role}.profession",
        ),
        unresolved_ambiguity_keys=("ordre_model_per_inscrit",),
        dependencies=(DossierBlockId.ROLE_ASSIGNMENTS, DossierBlockId.ADDRESS_USAGE),
    ),
    _BlockSpec(
        id=DossierBlockId.ORDER_MANDATE,
        label="Mandataire et derogation ordre",
        step_id=DossierStepId.ORDER,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.ORDER_MANDATE,
            required_document_codes=("DOC-034",),
            required_operation_types=(OperationType.ORDRE, OperationType.DEROGATION),
        ),
        required_roles=(
            BusinessRole.SIGNATAIRE,
            BusinessRole.MANDATAIRE,
            BusinessRole.SOCIETE_PRINCIPALE,
        ),
        required_canonical_fields=("personne.mandataire.*", "dossier.options.derogation"),
        unresolved_ambiguity_keys=("mandataire_configurable", "derogation_manual_block"),
        dependencies=(DossierBlockId.ORDER_IDENTIFIERS, DossierBlockId.ROLE_ASSIGNMENTS),
        notes="Mandataire et signataire restent deux assignments separes.",
    ),
    _BlockSpec(
        id=DossierBlockId.ORDER_EVIDENCE,
        label="Pieces ordinales",
        step_id=DossierStepId.ORDER,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.ORDER_EVIDENCE,
            required_document_codes=("DOC-034",),
            required_operation_types=(OperationType.ORDRE,),
        ),
        unresolved_ambiguity_keys=("ordre_model_per_inscrit", "derogation_manual_block"),
        dependencies=(DossierBlockId.ORDER_IDENTIFIERS,),
        notes="Bloc reserve aux pieces ordinales, sans choix documentaire implicite.",
    ),
    _BlockSpec(
        id=DossierBlockId.CESSION_CABINET,
        label="Cession cabinet",
        step_id=DossierStepId.OPERATIONS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.CESSION_CABINET,
            required_document_codes=("DOC-009",),
            required_operation_types=(OperationType.CESSION,),
        ),
        required_roles=(
            BusinessRole.VENDEUR,
            BusinessRole.ACQUEREUR,
            BusinessRole.REPRESENTANT_PERSONNE_MORALE,
        ),
        required_address_usages=(
            AddressUsage.DOMICILE_CEDANT,
            AddressUsage.LIEU_EXERCICE,
            AddressUsage.CABINET_CEDE,
            AddressUsage.SIEGE_SOCIAL,
        ),
        required_canonical_fields=(
            "cession.cabinet.adresse",
            "cession.vendeur.*",
            "cession.acquereur.*",
        ),
        possible_reuse_rules=("address:lieu_exercice -> address:cabinet_cede",),
        dependencies=(DossierBlockId.ROLE_ASSIGNMENTS, DossierBlockId.ADDRESS_USAGE),
    ),
    _BlockSpec(
        id=DossierBlockId.CESSION_PRICE,
        label="Prix de cession",
        step_id=DossierStepId.OPERATIONS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.CESSION_PRICE,
            required_document_codes=("DOC-009", "DOC-033"),
            required_operation_types=(OperationType.CESSION, OperationType.CESSION_PARTS_SCM),
        ),
        required_canonical_fields=(
            "cession.cabinet.prix_composantes",
            "cession.parts.nombre",
            "cession.parts.plage",
            "cession.prix.*",
            "cession.prix.total",
            "cession.prix.unitaire",
        ),
        unresolved_ambiguity_keys=("credit_vendeur_conditionnel",),
        dependencies=(DossierBlockId.CESSION_CABINET,),
    ),
    _BlockSpec(
        id=DossierBlockId.CESSION_ORIGIN,
        label="Origine de propriete",
        step_id=DossierStepId.OPERATIONS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.CESSION_ORIGIN,
            required_document_codes=("DOC-009",),
            required_operation_types=(OperationType.CESSION,),
        ),
        unresolved_ambiguity_keys=("origine_propriete_libre",),
        dependencies=(DossierBlockId.CESSION_CABINET,),
        notes="Localise l'ambiguite sans inventer de champ canonique non tranche.",
    ),
    _BlockSpec(
        id=DossierBlockId.CESSION_EXERCISES,
        label="Exercices financiers",
        step_id=DossierStepId.OPERATIONS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.CESSION_EXERCISES,
            required_document_codes=("DOC-009",),
            required_operation_types=(OperationType.CESSION,),
        ),
        required_canonical_fields=("cession.exercices[]",),
        unresolved_ambiguity_keys=("exercices_financiers_collection",),
        dependencies=(DossierBlockId.CESSION_CABINET,),
    ),
    _BlockSpec(
        id=DossierBlockId.BAIL,
        label="Bail et locaux loues",
        step_id=DossierStepId.OPERATIONS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.BAIL,
            required_document_codes=("DOC-009",),
            required_operation_types=(OperationType.BAIL,),
        ),
        required_roles=(BusinessRole.BAILLEUR, BusinessRole.LOCATAIRE),
        required_address_usages=(
            AddressUsage.BAILLEUR,
            AddressUsage.LOCATAIRE,
            AddressUsage.LOCAUX_LOUES,
        ),
        required_canonical_fields=("bail.parties", "bail.dates"),
        possible_reuse_rules=("address:lieu_exercice -> address:locaux_loues",),
        unresolved_ambiguity_keys=("bailleur_locataire_no_deduction",),
        dependencies=(DossierBlockId.ROLE_ASSIGNMENTS, DossierBlockId.ADDRESS_USAGE),
    ),
    _BlockSpec(
        id=DossierBlockId.FINANCING,
        label="Financement et banque",
        step_id=DossierStepId.OPERATIONS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.FINANCING,
            required_document_codes=("DOC-009", "DOC-017", "DOC-025"),
            required_operation_types=(OperationType.FINANCEMENT,),
        ),
        required_roles=(BusinessRole.BANQUE,),
        required_address_usages=(AddressUsage.BANQUE,),
        required_canonical_fields=("cession.financement.*", "banque.{role}"),
        unresolved_ambiguity_keys=("banque_depot_parametrage",),
        dependencies=(DossierBlockId.ROLE_ASSIGNMENTS, DossierBlockId.ADDRESS_USAGE),
    ),
    _BlockSpec(
        id=DossierBlockId.SCM,
        label="SCM et cession de parts",
        step_id=DossierStepId.OPERATIONS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.SCM,
            required_document_codes=("DOC-033", "DOC-025"),
            required_operation_types=(OperationType.CESSION_PARTS_SCM,),
        ),
        include_document_requirements=True,
        possible_reuse_rules=("address:scm_cedee -> address:cessionnaire_scm",),
        unresolved_ambiguity_keys=("representant_cessionnaire_explicit",),
        dependencies=(DossierBlockId.ROLE_ASSIGNMENTS, DossierBlockId.ADDRESS_USAGE),
        notes="SCM cedee et cessionnaire SCM restent distincts par defaut.",
    ),
    _BlockSpec(
        id=DossierBlockId.SCM_ASSOCIATES,
        label="Associes SCM et apports",
        step_id=DossierStepId.OPERATIONS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.SCM_ASSOCIATES,
            required_document_codes=("DOC-025",),
            required_operation_types=(OperationType.CESSION_PARTS_SCM, OperationType.APPORT),
        ),
        required_roles=(BusinessRole.ASSOCIE, BusinessRole.REPRESENTANT_PERSONNE_MORALE),
        required_canonical_fields=(
            "statuts_civils.associes[]",
            "apport.numeraire.montant",
            "capital.repartition_associes",
        ),
        unresolved_ambiguity_keys=("legacy_nb_parts_personne_2", "apports_parts_per_associe"),
        dependencies=(DossierBlockId.SCM, DossierBlockId.CAPITAL_ASSOCIATES),
    ),
    _BlockSpec(
        id=DossierBlockId.SPFPL,
        label="SPFPL et societe cible",
        step_id=DossierStepId.OPERATIONS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.SPFPL,
            required_document_codes=("DOC-041",),
            required_operation_types=(OperationType.APPORT,),
        ),
        required_roles=(BusinessRole.SPFPL_BENEFICIAIRE, BusinessRole.SOCIETE_CIBLE),
        required_address_usages=(AddressUsage.SPFPL, AddressUsage.SOCIETE_CIBLE),
        required_canonical_fields=("spfpl.operation.type", "societe_spfpl.*", "societe_cible.*"),
        unresolved_ambiguity_keys=("spfpl_uncertain_fields",),
        dependencies=(DossierBlockId.COMPANY_RECORDS, DossierBlockId.ADDRESS_USAGE),
    ),
    _BlockSpec(
        id=DossierBlockId.APPORT_TITRES,
        label="Apport de titres",
        step_id=DossierStepId.OPERATIONS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.APPORT_TITRES,
            required_document_codes=("DOC-041",),
            required_operation_types=(OperationType.APPORT,),
        ),
        required_roles=(
            BusinessRole.APPORTEUR,
            BusinessRole.DIRIGEANT,
            BusinessRole.EVALUATEUR_APPORT,
            BusinessRole.COMMISSAIRE_AUX_APPORTS,
            BusinessRole.SIGNATAIRE,
        ),
        required_address_usages=(AddressUsage.DOMICILE_PRATICIEN,),
        required_canonical_fields=(
            "apport_titres.*",
            "commissaire_aux_apports.{champ}",
            "capital.titres.*",
        ),
        unresolved_ambiguity_keys=(
            "evaluateur_commissaire_fixed_source",
            "commissaire_label_confirm",
        ),
        dependencies=(DossierBlockId.SPFPL, DossierBlockId.CAPITAL_TITLES),
        notes="Commissaire et evaluateur restent tiers de controle, pas parties.",
    ),
    _BlockSpec(
        id=DossierBlockId.DOCUMENT_REQUIREMENTS,
        label="Documents attendus",
        step_id=DossierStepId.DOCUMENTS,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.DOCUMENT_REQUIREMENTS,
            always_active=True,
        ),
        include_document_requirements=True,
        dependencies=(
            DossierBlockId.ROLE_ASSIGNMENTS,
            DossierBlockId.ADDRESS_USAGE,
            DossierBlockId.CAPITAL_TITLES,
            DossierBlockId.ORDER_IDENTIFIERS,
            DossierBlockId.CESSION_CABINET,
            DossierBlockId.SPFPL,
            DossierBlockId.SCM,
        ),
        notes="Agrège les pre-requis documentaires sans lancer la generation.",
    ),
    _BlockSpec(
        id=DossierBlockId.GENERATION_READINESS,
        label="Readiness generation",
        step_id=DossierStepId.GENERATION,
        activation_rule=BlockActivationRule(
            block_id=DossierBlockId.GENERATION_READINESS,
            always_active=True,
        ),
        include_document_requirements=True,
        dependencies=(DossierBlockId.DOCUMENT_REQUIREMENTS,),
        notes="Expose les blocages et warnings pour la future UI.",
    ),
)
