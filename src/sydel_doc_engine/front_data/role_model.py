from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from sydel_doc_engine.front_data.models import (
    BusinessRole,
    DossierRecord,
    RoleAssignment,
    RoleScope,
    RoleTargetType,
)


class RoleFamily(StrEnum):
    PERSON_IDENTITY = "person_identity"
    GOVERNANCE = "governance"
    DOCUMENT_EXECUTION = "document_execution"
    TRANSACTION_PARTY = "transaction_party"
    REPRESENTATION = "representation"
    CONTROL_THIRD_PARTY = "control_third_party"
    COMPANY_OPERATION = "company_operation"
    INSTITUTION = "institution"
    FINANCE = "finance"


@dataclass(frozen=True)
class RoleDefinition:
    role: BusinessRole
    label: str
    family: RoleFamily
    target_types: frozenset[RoleTargetType]
    default_scope: RoleScope
    allowed_scopes: frozenset[RoleScope]
    reusable_by_default: bool = False
    requires_represented_entity: bool = False
    third_party_control: bool = False
    notes: str = ""


@dataclass(frozen=True)
class RoleReusePolicy:
    source_role: BusinessRole
    target_role: BusinessRole
    allowed_scopes: frozenset[RoleScope]
    label: str
    requires_explicit_rule: bool = True


@dataclass(frozen=True)
class OrderRoleModel:
    inscrit_personne_role: BusinessRole
    societe_inscrite_role: BusinessRole
    conseil_ordre_role: BusinessRole
    mandataire_role: BusinessRole
    rpps_field_path: str
    numero_ordre_field_path: str
    profession_field_path: str
    ordre_adresse_field_path: str


PERSON_ONLY = frozenset({RoleTargetType.PERSON})
COMPANY_ONLY = frozenset({RoleTargetType.COMPANY})
PERSON_OR_COMPANY = frozenset({RoleTargetType.PERSON, RoleTargetType.COMPANY})

DOSSIER_ONLY = frozenset({RoleScope.DOSSIER})
DOSSIER_OR_OPERATION = frozenset({RoleScope.DOSSIER, RoleScope.OPERATION})
OPERATION_ONLY = frozenset({RoleScope.OPERATION})
OPERATION_OR_DOCUMENT = frozenset({RoleScope.OPERATION, RoleScope.DOCUMENT})
DOCUMENT_OR_LOT = frozenset({RoleScope.DOCUMENT, RoleScope.LOT})
ANY_ROLE_SCOPE = frozenset(
    {RoleScope.DOSSIER, RoleScope.OPERATION, RoleScope.DOCUMENT, RoleScope.LOT}
)


ROLE_DEFINITIONS: dict[BusinessRole, RoleDefinition] = {
    BusinessRole.PRATICIEN: RoleDefinition(
        role=BusinessRole.PRATICIEN,
        label="Praticien",
        family=RoleFamily.PERSON_IDENTITY,
        target_types=PERSON_ONLY,
        default_scope=RoleScope.DOSSIER,
        allowed_scopes=DOSSIER_OR_OPERATION,
        notes="Personne physique cliente ; source possible de roles via regle explicite.",
    ),
    BusinessRole.ASSOCIE: RoleDefinition(
        role=BusinessRole.ASSOCIE,
        label="Associe",
        family=RoleFamily.GOVERNANCE,
        target_types=PERSON_OR_COMPANY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=ANY_ROLE_SCOPE,
        notes="Detenteur de titres ; peut etre personne physique ou personne morale.",
    ),
    BusinessRole.GERANT: RoleDefinition(
        role=BusinessRole.GERANT,
        label="Gerant",
        family=RoleFamily.GOVERNANCE,
        target_types=PERSON_ONLY,
        default_scope=RoleScope.DOSSIER,
        allowed_scopes=DOSSIER_OR_OPERATION,
    ),
    BusinessRole.PRESIDENT: RoleDefinition(
        role=BusinessRole.PRESIDENT,
        label="President",
        family=RoleFamily.GOVERNANCE,
        target_types=PERSON_ONLY,
        default_scope=RoleScope.DOSSIER,
        allowed_scopes=DOSSIER_OR_OPERATION,
    ),
    BusinessRole.DIRIGEANT: RoleDefinition(
        role=BusinessRole.DIRIGEANT,
        label="Dirigeant",
        family=RoleFamily.GOVERNANCE,
        target_types=PERSON_ONLY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=DOSSIER_OR_OPERATION,
        notes="Role parapluie conserve seulement quand gerant/president n'est pas encore tranche.",
    ),
    BusinessRole.SIGNATAIRE: RoleDefinition(
        role=BusinessRole.SIGNATAIRE,
        label="Signataire",
        family=RoleFamily.DOCUMENT_EXECUTION,
        target_types=PERSON_ONLY,
        default_scope=RoleScope.DOCUMENT,
        allowed_scopes=DOCUMENT_OR_LOT,
        notes="Role par document ou lot ; jamais mandataire par defaut.",
    ),
    BusinessRole.MANDATAIRE: RoleDefinition(
        role=BusinessRole.MANDATAIRE,
        label="Mandataire",
        family=RoleFamily.DOCUMENT_EXECUTION,
        target_types=PERSON_OR_COMPANY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
        notes="Personne ou organisation recevant pouvoir pour formalites.",
    ),
    BusinessRole.VENDEUR: RoleDefinition(
        role=BusinessRole.VENDEUR,
        label="Vendeur",
        family=RoleFamily.TRANSACTION_PARTY,
        target_types=PERSON_OR_COMPANY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
    ),
    BusinessRole.CEDANT: RoleDefinition(
        role=BusinessRole.CEDANT,
        label="Cedant",
        family=RoleFamily.TRANSACTION_PARTY,
        target_types=PERSON_OR_COMPANY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
    ),
    BusinessRole.ACQUEREUR: RoleDefinition(
        role=BusinessRole.ACQUEREUR,
        label="Acquereur",
        family=RoleFamily.TRANSACTION_PARTY,
        target_types=COMPANY_ONLY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
    ),
    BusinessRole.CESSIONNAIRE: RoleDefinition(
        role=BusinessRole.CESSIONNAIRE,
        label="Cessionnaire",
        family=RoleFamily.TRANSACTION_PARTY,
        target_types=COMPANY_ONLY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
    ),
    BusinessRole.APPORTEUR: RoleDefinition(
        role=BusinessRole.APPORTEUR,
        label="Apporteur",
        family=RoleFamily.TRANSACTION_PARTY,
        target_types=PERSON_OR_COMPANY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
    ),
    BusinessRole.BAILLEUR: RoleDefinition(
        role=BusinessRole.BAILLEUR,
        label="Bailleur",
        family=RoleFamily.TRANSACTION_PARTY,
        target_types=PERSON_OR_COMPANY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
    ),
    BusinessRole.LOCATAIRE: RoleDefinition(
        role=BusinessRole.LOCATAIRE,
        label="Locataire",
        family=RoleFamily.TRANSACTION_PARTY,
        target_types=PERSON_OR_COMPANY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
    ),
    BusinessRole.CONJOINT: RoleDefinition(
        role=BusinessRole.CONJOINT,
        label="Conjoint",
        family=RoleFamily.PERSON_IDENTITY,
        target_types=PERSON_ONLY,
        default_scope=RoleScope.DOSSIER,
        allowed_scopes=ANY_ROLE_SCOPE,
    ),
    BusinessRole.REPRESENTANT_PERSONNE_MORALE: RoleDefinition(
        role=BusinessRole.REPRESENTANT_PERSONNE_MORALE,
        label="Representant de personne morale",
        family=RoleFamily.REPRESENTATION,
        target_types=PERSON_ONLY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
        requires_represented_entity=True,
        notes="Distinct de la personne morale representee.",
    ),
    BusinessRole.COMMISSAIRE_AUX_APPORTS: RoleDefinition(
        role=BusinessRole.COMMISSAIRE_AUX_APPORTS,
        label="Commissaire aux apports",
        family=RoleFamily.CONTROL_THIRD_PARTY,
        target_types=PERSON_OR_COMPANY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
        third_party_control=True,
        notes="Tiers de controle ; ne doit pas etre une partie a l'operation.",
    ),
    BusinessRole.EVALUATEUR_APPORT: RoleDefinition(
        role=BusinessRole.EVALUATEUR_APPORT,
        label="Evaluateur",
        family=RoleFamily.CONTROL_THIRD_PARTY,
        target_types=PERSON_OR_COMPANY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
        third_party_control=True,
        notes="Tiers d'evaluation ; distinct des parties a l'operation.",
    ),
    BusinessRole.SOCIETE_PRINCIPALE: RoleDefinition(
        role=BusinessRole.SOCIETE_PRINCIPALE,
        label="Societe principale",
        family=RoleFamily.COMPANY_OPERATION,
        target_types=COMPANY_ONLY,
        default_scope=RoleScope.DOSSIER,
        allowed_scopes=DOSSIER_OR_OPERATION,
    ),
    BusinessRole.SOCIETE_CIBLE: RoleDefinition(
        role=BusinessRole.SOCIETE_CIBLE,
        label="Societe cible",
        family=RoleFamily.COMPANY_OPERATION,
        target_types=COMPANY_ONLY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
    ),
    BusinessRole.SOCIETE_APPORTEE: RoleDefinition(
        role=BusinessRole.SOCIETE_APPORTEE,
        label="Societe apportee",
        family=RoleFamily.COMPANY_OPERATION,
        target_types=COMPANY_ONLY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
    ),
    BusinessRole.SPFPL_BENEFICIAIRE: RoleDefinition(
        role=BusinessRole.SPFPL_BENEFICIAIRE,
        label="SPFPL beneficiaire",
        family=RoleFamily.COMPANY_OPERATION,
        target_types=COMPANY_ONLY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
    ),
    BusinessRole.SCM: RoleDefinition(
        role=BusinessRole.SCM,
        label="SCM",
        family=RoleFamily.COMPANY_OPERATION,
        target_types=COMPANY_ONLY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=DOSSIER_OR_OPERATION,
    ),
    BusinessRole.SCM_CEDEE: RoleDefinition(
        role=BusinessRole.SCM_CEDEE,
        label="SCM cedee",
        family=RoleFamily.COMPANY_OPERATION,
        target_types=COMPANY_ONLY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
    ),
    BusinessRole.ORDRE_PROFESSIONNEL: RoleDefinition(
        role=BusinessRole.ORDRE_PROFESSIONNEL,
        label="Conseil de l'ordre",
        family=RoleFamily.INSTITUTION,
        target_types=COMPANY_ONLY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=OPERATION_OR_DOCUMENT,
        notes="Institution ordinale destinataire, distincte de l'inscrit et de la societe.",
    ),
    BusinessRole.BANQUE: RoleDefinition(
        role=BusinessRole.BANQUE,
        label="Banque",
        family=RoleFamily.FINANCE,
        target_types=COMPANY_ONLY,
        default_scope=RoleScope.OPERATION,
        allowed_scopes=DOSSIER_OR_OPERATION,
    ),
}

TRANSACTION_PARTY_ROLES = frozenset(
    {
        BusinessRole.VENDEUR,
        BusinessRole.CEDANT,
        BusinessRole.ACQUEREUR,
        BusinessRole.CESSIONNAIRE,
        BusinessRole.APPORTEUR,
        BusinessRole.BAILLEUR,
        BusinessRole.LOCATAIRE,
        BusinessRole.SOCIETE_CIBLE,
        BusinessRole.SOCIETE_APPORTEE,
        BusinessRole.SPFPL_BENEFICIAIRE,
        BusinessRole.SCM_CEDEE,
    }
)

ROLE_REUSE_POLICIES: dict[tuple[BusinessRole, BusinessRole], RoleReusePolicy] = {
    (
        BusinessRole.PRATICIEN,
        BusinessRole.ASSOCIE,
    ): RoleReusePolicy(
        source_role=BusinessRole.PRATICIEN,
        target_role=BusinessRole.ASSOCIE,
        allowed_scopes=ANY_ROLE_SCOPE,
        label="Dossier unipersonnel : praticien vers associe",
    ),
    (
        BusinessRole.PRATICIEN,
        BusinessRole.GERANT,
    ): RoleReusePolicy(
        source_role=BusinessRole.PRATICIEN,
        target_role=BusinessRole.GERANT,
        allowed_scopes=DOSSIER_OR_OPERATION,
        label="Dossier unipersonnel : praticien vers gerant",
    ),
    (
        BusinessRole.PRATICIEN,
        BusinessRole.SIGNATAIRE,
    ): RoleReusePolicy(
        source_role=BusinessRole.PRATICIEN,
        target_role=BusinessRole.SIGNATAIRE,
        allowed_scopes=DOCUMENT_OR_LOT,
        label="Dossier unipersonnel ou document : praticien vers signataire",
    ),
    (
        BusinessRole.PRATICIEN,
        BusinessRole.VENDEUR,
    ): RoleReusePolicy(
        source_role=BusinessRole.PRATICIEN,
        target_role=BusinessRole.VENDEUR,
        allowed_scopes=OPERATION_OR_DOCUMENT,
        label="Cession SEL standard : praticien BNC vers vendeur",
    ),
    (
        BusinessRole.PRATICIEN,
        BusinessRole.CEDANT,
    ): RoleReusePolicy(
        source_role=BusinessRole.PRATICIEN,
        target_role=BusinessRole.CEDANT,
        allowed_scopes=OPERATION_OR_DOCUMENT,
        label="Cession SEL standard : praticien BNC vers cedant",
    ),
    (
        BusinessRole.SOCIETE_PRINCIPALE,
        BusinessRole.ACQUEREUR,
    ): RoleReusePolicy(
        source_role=BusinessRole.SOCIETE_PRINCIPALE,
        target_role=BusinessRole.ACQUEREUR,
        allowed_scopes=OPERATION_OR_DOCUMENT,
        label="Cession SEL standard : societe principale vers acquereur",
    ),
    (
        BusinessRole.SOCIETE_PRINCIPALE,
        BusinessRole.CESSIONNAIRE,
    ): RoleReusePolicy(
        source_role=BusinessRole.SOCIETE_PRINCIPALE,
        target_role=BusinessRole.CESSIONNAIRE,
        allowed_scopes=OPERATION_OR_DOCUMENT,
        label="Cession SCM/SPFPL : societe principale vers cessionnaire",
    ),
}

ORDER_ROLE_MODEL = OrderRoleModel(
    inscrit_personne_role=BusinessRole.SIGNATAIRE,
    societe_inscrite_role=BusinessRole.SOCIETE_PRINCIPALE,
    conseil_ordre_role=BusinessRole.ORDRE_PROFESSIONNEL,
    mandataire_role=BusinessRole.MANDATAIRE,
    rpps_field_path="personne.{role}.numero_rpps",
    numero_ordre_field_path="personne.{role}.numero_ordre",
    profession_field_path="personne.{role}.profession",
    ordre_adresse_field_path="ordre.adresse",
)


def role_definition(role: BusinessRole) -> RoleDefinition:
    return ROLE_DEFINITIONS[role]


def role_family(role: BusinessRole) -> RoleFamily:
    return role_definition(role).family


def is_target_type_allowed(role: BusinessRole, target_type: RoleTargetType) -> bool:
    return target_type in role_definition(role).target_types


def is_scope_allowed(role: BusinessRole, scope: RoleScope) -> bool:
    return scope in role_definition(role).allowed_scopes


def requires_represented_entity(role: BusinessRole) -> bool:
    return role_definition(role).requires_represented_entity


def is_third_party_control_role(role: BusinessRole) -> bool:
    return role_definition(role).third_party_control


def role_ref(role: BusinessRole) -> str:
    return f"role:{role.value}"


def parse_role_ref(ref: str) -> BusinessRole | None:
    if not ref.startswith("role:"):
        return None
    role_value = ref.removeprefix("role:")
    try:
        return BusinessRole(role_value)
    except ValueError:
        return None


def role_reuse_policy(
    source_role: BusinessRole,
    target_role: BusinessRole,
) -> RoleReusePolicy | None:
    return ROLE_REUSE_POLICIES.get((source_role, target_role))


def is_role_reuse_allowed(source_role: BusinessRole, target_role: BusinessRole) -> bool:
    if source_role is target_role:
        return True
    return role_reuse_policy(source_role, target_role) is not None


def assignment_has_represented_entity(assignment: RoleAssignment) -> bool:
    return bool(assignment.represented_target_type and assignment.represented_target_id)


def represented_entity_exists(dossier: DossierRecord, assignment: RoleAssignment) -> bool:
    if assignment.represented_target_type is RoleTargetType.PERSON:
        return bool(assignment.represented_target_id in dossier.persons)
    if assignment.represented_target_type is RoleTargetType.COMPANY:
        return bool(assignment.represented_target_id in dossier.companies)
    return False


def has_transaction_party_role_on_same_target(
    dossier: DossierRecord,
    assignment: RoleAssignment,
) -> bool:
    return any(
        other.id != assignment.id
        and other.target_type is assignment.target_type
        and other.target_id == assignment.target_id
        and other.role in TRANSACTION_PARTY_ROLES
        for other in dossier.role_assignments.values()
    )


def assign_explicit_role(
    dossier: DossierRecord,
    role: BusinessRole,
    target_id: str,
    *,
    target_type: RoleTargetType | None = None,
    assignment_id: str | None = None,
    scope: RoleScope | None = None,
    scope_id: str | None = None,
    document_code: str | None = None,
    source_rule_id: str | None = None,
    represented_target_type: RoleTargetType | None = None,
    represented_target_id: str | None = None,
    represented_role: BusinessRole | None = None,
    notes: str = "",
) -> RoleAssignment:
    definition = role_definition(role)
    resolved_target_type = target_type or _single_target_type(definition)
    resolved_scope = scope or definition.default_scope
    return dossier.assign_role(
        role,
        resolved_target_type,
        target_id,
        assignment_id=assignment_id,
        scope=resolved_scope,
        scope_id=scope_id,
        document_code=document_code,
        source_rule_id=source_rule_id,
        represented_target_type=represented_target_type,
        represented_target_id=represented_target_id,
        represented_role=represented_role,
        notes=notes,
    )


def role_placeholder_is_generic(field_path: str) -> bool:
    return "{role}" in field_path


def role_from_canonical_path(field_path: str) -> BusinessRole | None:
    parts = field_path.split(".")
    if len(parts) < 2:
        return None
    if parts[0] not in {"personne", "societe", "banque"}:
        return None
    if parts[1] == "{role}":
        return None
    try:
        return BusinessRole(parts[1])
    except ValueError:
        return None


def _single_target_type(definition: RoleDefinition) -> RoleTargetType:
    if len(definition.target_types) != 1:
        raise ValueError(
            f"Role {definition.role.value} needs an explicit target_type "
            "because it can target multiple object kinds."
        )
    return next(iter(definition.target_types))
