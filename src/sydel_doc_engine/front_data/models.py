from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class CanonicalRelationType(StrEnum):
    SAME_FIELD = "SAME_FIELD"
    SAME_DATA_DIFFERENT_SHAPE = "SAME_DATA_DIFFERENT_SHAPE"
    EXPLICIT_REUSE_ONLY = "EXPLICIT_REUSE_ONLY"
    DISTINCT_FIELDS = "DISTINCT_FIELDS"
    UNCERTAIN_REQUIRES_HUMAN_DECISION = "UNCERTAIN_REQUIRES_HUMAN_DECISION"


class FrontObjectType(StrEnum):
    PERSON = "Person"
    COMPANY = "Organization"
    ADDRESS = "Address"
    ROLE_ASSIGNMENT = "RoleAssignment"
    DOSSIER = "Dossier"
    OPERATION = "OperationContext"
    DOCUMENT_REQUIREMENT = "DocumentRequirement"
    FIELD_DEFINITION = "FieldDefinition"
    REUSE_RULE = "ReuseRule"
    VALIDATION_ISSUE = "ValidationIssue"
    SUPPORTING_EVIDENCE = "SupportingEvidence"


class FieldFormKind(StrEnum):
    BUSINESS = "business"
    DISPLAY = "display"
    DOCUMENTARY_ALIAS = "documentary_alias"
    OVERRIDE = "override"


class AddressDisplaySource(StrEnum):
    MANUAL = "manual"
    COMPONENTS = "components"
    REUSE_RULE = "reuse_rule"
    DOCUMENTARY_ALIAS = "documentary_alias"
    OVERRIDE = "override"


class AddressUsage(StrEnum):
    DOMICILE_PRATICIEN = "domicile_praticien"
    DOMICILE_CEDANT = "domicile_cedant"
    ADRESSE_PERSONNELLE = "adresse_personnelle"
    LIEU_EXERCICE = "lieu_exercice"
    SIEGE_SOCIAL = "siege_social"
    DOMICILIATION = "domiciliation"
    CABINET_CEDE = "cabinet_cede"
    LOCAUX_LOUES = "locaux_loues"
    BAILLEUR = "bailleur"
    LOCATAIRE = "locataire"
    BANQUE = "banque"
    ORDRE = "ordre"
    SCM = "scm"
    SCM_CEDEE = "scm_cedee"
    CESSIONNAIRE_SCM = "cessionnaire_scm"
    SPFPL = "spfpl"
    SOCIETE_CIBLE = "societe_cible"


class BusinessRole(StrEnum):
    PRATICIEN = "praticien"
    ASSOCIE = "associe"
    GERANT = "gerant"
    PRESIDENT = "president"
    DIRIGEANT = "dirigeant"
    SIGNATAIRE = "signataire"
    MANDATAIRE = "mandataire"
    VENDEUR = "vendeur"
    CEDANT = "cedant"
    ACQUEREUR = "acquereur"
    CESSIONNAIRE = "cessionnaire"
    APPORTEUR = "apporteur"
    BAILLEUR = "bailleur"
    LOCATAIRE = "locataire"
    CONJOINT = "conjoint"
    REPRESENTANT_PERSONNE_MORALE = "representant_personne_morale"
    COMMISSAIRE_AUX_APPORTS = "commissaire_aux_apports"
    EVALUATEUR_APPORT = "evaluateur_apport"
    SOCIETE_PRINCIPALE = "societe_principale"
    SOCIETE_CIBLE = "societe_cible"
    SOCIETE_APPORTEE = "societe_apportee"
    SPFPL_BENEFICIAIRE = "spfpl_beneficiaire"
    SCM = "scm"
    SCM_CEDEE = "scm_cedee"
    BANQUE = "banque"
    ORDRE_PROFESSIONNEL = "ordre_professionnel"


class RoleTargetType(StrEnum):
    PERSON = "person"
    COMPANY = "company"


class RoleScope(StrEnum):
    DOSSIER = "dossier"
    OPERATION = "operation"
    DOCUMENT = "document"
    LOT = "lot"


class OperationType(StrEnum):
    CREATION = "creation"
    CESSION = "cession"
    APPORT = "apport"
    CESSION_PARTS_SCM = "cession_parts_scm"
    REGIME_COMMUNAUTAIRE = "regime_communautaire"
    DEROGATION = "derogation"
    ORDRE = "ordre"
    BAIL = "bail"
    FINANCEMENT = "financement"


class ReuseRuleKind(StrEnum):
    REFERENCE = "reference"
    PREFILL = "prefill"
    DERIVATION = "derivation"
    FORMAT = "format"
    OVERRIDE = "override"


class ReuseRuleStatus(StrEnum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    REJECTED = "rejected"
    CONFLICT = "conflict"


class DocumentRequirementStatus(StrEnum):
    EXPECTED = "expected"
    GENERABLE = "generable"
    MANUAL_ONLY = "manual_only"
    NOT_IMPLEMENTED = "not_implemented"
    CONTEXT_INCOMPLETE = "context_incomplete"


class ValidationIssueType(StrEnum):
    MISSING_ROLE = "missing_role"
    MISSING_TYPED_ADDRESS = "missing_typed_address"
    REUSE_CONFLICT = "reuse_conflict"
    UNRESOLVED_AMBIGUITY = "unresolved_ambiguity"
    MISSING_CANONICAL_VALUE = "missing_canonical_value"
    UNLINKED_REQUIRED_ENTITY = "unlinked_required_entity"
    INCOMPATIBLE_ROLE_TARGET = "incompatible_role_target"
    INVALID_ROLE_SCOPE = "invalid_role_scope"
    ROLE_CONFUSION = "role_confusion"
    MISSING_REPRESENTED_ENTITY = "missing_represented_entity"
    THIRD_PARTY_ROLE_CONFLICT = "third_party_role_conflict"
    IMPLICIT_ROLE_REUSE_FORBIDDEN = "implicit_role_reuse_forbidden"
    ADDRESS_REUSE_FORBIDDEN = "address_reuse_forbidden"
    WRONG_ADDRESS_USAGE = "wrong_address_usage"
    INCONSISTENT_ADDRESS_OVERRIDE = "inconsistent_address_override"
    MISSING_ADDRESS_REUSE_SOURCE = "missing_address_reuse_source"


class ValidationSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


@dataclass(frozen=True)
class CanonicalFieldDefinition:
    field_path: str
    front_object: FrontObjectType
    relation_type: CanonicalRelationType
    role: BusinessRole | None = None
    address_usage: AddressUsage | None = None
    operation_type: OperationType | None = None
    form_kind: FieldFormKind = FieldFormKind.BUSINESS
    notes: str = ""


@dataclass
class CanonicalFieldValue:
    field_path: str
    value: Any
    owner_object_type: FrontObjectType | None = None
    owner_object_id: str | None = None
    relation_type: CanonicalRelationType = CanonicalRelationType.SAME_FIELD
    form_kind: FieldFormKind = FieldFormKind.BUSINESS
    source_field_path: str | None = None
    source_aliases: tuple[str, ...] = ()
    document_code: str | None = None
    is_override: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_business_field(self) -> bool:
        return self.form_kind is FieldFormKind.BUSINESS


@dataclass
class AddressRecord:
    id: str
    usage: AddressUsage
    display_value: str | None = None
    street_number: str | None = None
    street_name: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country: str = "France"
    display_source: AddressDisplaySource | None = None
    display_source_rule_id: str | None = None
    display_override_reason: str | None = None
    owner_object_type: FrontObjectType | None = None
    owner_object_id: str | None = None
    source_address_id: str | None = None
    source_rule_id: str | None = None
    is_override: bool = False
    document_aliases: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def ref(self) -> str:
        return address_ref(self.usage)

    def has_value(self) -> bool:
        return any(
            [
                self.display_value,
                self.street_number,
                self.street_name,
                self.postal_code,
                self.city,
            ]
        )


@dataclass
class PersonRecord:
    id: str
    civilite_affichage: str | None = None
    genre: str | None = None
    prenom: str | None = None
    nom: str | None = None
    profession: str | None = None
    fonction: str | None = None
    numero_rpps: str | None = None
    numero_ordre: str | None = None
    address_ids: set[str] = field(default_factory=set)
    canonical_values: dict[str, CanonicalFieldValue] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_address(self, address_id: str) -> None:
        self.address_ids.add(address_id)


@dataclass
class CompanyRecord:
    id: str
    denomination: str
    forme_sociale: str | None = None
    capital_social: str | None = None
    rcs_numero: str | None = None
    rcs_ville: str | None = None
    address_ids: set[str] = field(default_factory=set)
    canonical_values: dict[str, CanonicalFieldValue] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_address(self, address_id: str) -> None:
        self.address_ids.add(address_id)


@dataclass
class RoleAssignment:
    id: str
    role: BusinessRole
    target_type: RoleTargetType
    target_id: str
    scope: RoleScope = RoleScope.DOSSIER
    scope_id: str | None = None
    explicit: bool = True
    source_rule_id: str | None = None
    document_code: str | None = None
    represented_target_type: RoleTargetType | None = None
    represented_target_id: str | None = None
    represented_role: BusinessRole | None = None
    notes: str = ""


@dataclass
class OperationContext:
    id: str
    operation_type: OperationType
    label: str | None = None
    fields: dict[str, CanonicalFieldValue] = field(default_factory=dict)
    linked_role_assignment_ids: set[str] = field(default_factory=set)
    linked_address_ids: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)

    def set_value(self, value: CanonicalFieldValue) -> None:
        self.fields[value.field_path] = value


@dataclass
class ReuseRuleState:
    id: str
    source_ref: str
    target_ref: str
    relation_type: CanonicalRelationType
    label: str = ""
    kind: ReuseRuleKind = ReuseRuleKind.REFERENCE
    status: ReuseRuleStatus = ReuseRuleStatus.PROPOSED
    explicit: bool = True
    allow_override: bool = False
    override_value: Any | None = None
    notes: str = ""

    @property
    def is_active(self) -> bool:
        return self.status is ReuseRuleStatus.ACTIVE


@dataclass(frozen=True)
class DocumentRequirementRecord:
    doc_code: str
    doc_label: str
    required_roles: tuple[BusinessRole, ...] = ()
    required_address_usages: tuple[AddressUsage, ...] = ()
    required_entities: tuple[BusinessRole, ...] = ()
    required_canonical_fields: tuple[str, ...] = ()
    target_screen_blocks: tuple[str, ...] = ()
    possible_reuse_rules: tuple[str, ...] = ()
    unresolved_ambiguity_keys: tuple[str, ...] = ()
    verdict: str = "ORANGE"
    action_needed: str = ""
    status: DocumentRequirementStatus = DocumentRequirementStatus.EXPECTED


@dataclass(frozen=True)
class ValidationIssue:
    issue_type: ValidationIssueType
    severity: ValidationSeverity
    message: str
    doc_code: str | None = None
    field_path: str | None = None
    role: BusinessRole | None = None
    address_usage: AddressUsage | None = None
    source_ref: str | None = None
    target_ref: str | None = None
    action: str | None = None


@dataclass
class DossierRecord:
    id: str
    label: str | None = None
    structure: str | None = None
    persons: dict[str, PersonRecord] = field(default_factory=dict)
    companies: dict[str, CompanyRecord] = field(default_factory=dict)
    addresses: dict[str, AddressRecord] = field(default_factory=dict)
    role_assignments: dict[str, RoleAssignment] = field(default_factory=dict)
    operation_contexts: dict[str, OperationContext] = field(default_factory=dict)
    document_requirements: dict[str, DocumentRequirementRecord] = field(default_factory=dict)
    canonical_values: dict[str, CanonicalFieldValue] = field(default_factory=dict)
    reuse_rules: dict[str, ReuseRuleState] = field(default_factory=dict)
    resolved_ambiguity_keys: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_person(self, person: PersonRecord) -> PersonRecord:
        if person.id in self.persons:
            raise ValueError(f"Person already exists: {person.id}")
        self.persons[person.id] = person
        return person

    def add_company(self, company: CompanyRecord) -> CompanyRecord:
        if company.id in self.companies:
            raise ValueError(f"Company already exists: {company.id}")
        self.companies[company.id] = company
        return company

    def add_address(self, address: AddressRecord) -> AddressRecord:
        if address.id in self.addresses:
            raise ValueError(f"Address already exists: {address.id}")
        self.addresses[address.id] = address
        if address.owner_object_type is FrontObjectType.PERSON and address.owner_object_id:
            person = self.persons.get(address.owner_object_id)
            if person:
                person.add_address(address.id)
        if address.owner_object_type is FrontObjectType.COMPANY and address.owner_object_id:
            company = self.companies.get(address.owner_object_id)
            if company:
                company.add_address(address.id)
        return address

    def add_operation_context(self, context: OperationContext) -> OperationContext:
        if context.id in self.operation_contexts:
            raise ValueError(f"Operation context already exists: {context.id}")
        self.operation_contexts[context.id] = context
        return context

    def add_document_requirement(
        self,
        requirement: DocumentRequirementRecord,
    ) -> DocumentRequirementRecord:
        self.document_requirements[requirement.doc_code] = requirement
        return requirement

    def add_canonical_value(self, value: CanonicalFieldValue) -> CanonicalFieldValue:
        self.canonical_values[value.field_path] = value
        return value

    def add_reuse_rule(self, rule: ReuseRuleState) -> ReuseRuleState:
        if rule.id in self.reuse_rules:
            raise ValueError(f"Reuse rule already exists: {rule.id}")
        self.reuse_rules[rule.id] = rule
        return rule

    def assign_role(
        self,
        role: BusinessRole,
        target_type: RoleTargetType,
        target_id: str,
        *,
        assignment_id: str | None = None,
        scope: RoleScope = RoleScope.DOSSIER,
        scope_id: str | None = None,
        document_code: str | None = None,
        source_rule_id: str | None = None,
        explicit: bool = True,
        represented_target_type: RoleTargetType | None = None,
        represented_target_id: str | None = None,
        represented_role: BusinessRole | None = None,
        notes: str = "",
    ) -> RoleAssignment:
        role_id = assignment_id or f"role-{len(self.role_assignments) + 1:03d}"
        if role_id in self.role_assignments:
            raise ValueError(f"Role assignment already exists: {role_id}")
        assignment = RoleAssignment(
            id=role_id,
            role=role,
            target_type=target_type,
            target_id=target_id,
            scope=scope,
            scope_id=scope_id,
            explicit=explicit,
            source_rule_id=source_rule_id,
            document_code=document_code,
            represented_target_type=represented_target_type,
            represented_target_id=represented_target_id,
            represented_role=represented_role,
            notes=notes,
        )
        self.role_assignments[role_id] = assignment
        return assignment

    def roles_for(self, role: BusinessRole) -> tuple[RoleAssignment, ...]:
        return tuple(
            assignment
            for assignment in self.role_assignments.values()
            if assignment.role is role
        )

    def addresses_for_usage(self, usage: AddressUsage) -> tuple[AddressRecord, ...]:
        return tuple(address for address in self.addresses.values() if address.usage is usage)

    def active_reuse_rules_for_target(self, target_ref: str) -> tuple[ReuseRuleState, ...]:
        return tuple(
            rule
            for rule in self.reuse_rules.values()
            if rule.target_ref == target_ref and rule.is_active
        )

    def has_active_reuse_rule(self, source_ref: str, target_ref: str) -> bool:
        return any(
            rule.source_ref == source_ref
            and rule.target_ref == target_ref
            and rule.is_active
            and rule.explicit
            for rule in self.reuse_rules.values()
        )

    def is_address_usage_available(self, usage: AddressUsage) -> bool:
        if any(address.has_value() for address in self.addresses_for_usage(usage)):
            return True
        return bool(self.active_reuse_rules_for_target(address_ref(usage)))

    def resolve_ambiguity(self, key: str) -> None:
        self.resolved_ambiguity_keys.add(key)


def address_ref(usage: AddressUsage) -> str:
    return f"address:{usage.value}"


def canonical_field_ref(field_path: str) -> str:
    return f"field:{field_path}"
