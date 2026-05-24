from __future__ import annotations

from sydel_doc_engine.front_data import (
    ORDER_ROLE_MODEL,
    AddressRecord,
    BusinessRole,
    CanonicalRelationType,
    CompanyRecord,
    DossierRecord,
    PersonRecord,
    ReuseRuleState,
    ReuseRuleStatus,
    RoleScope,
    RoleTargetType,
    assign_explicit_role,
    canonical_definition,
    role_from_canonical_path,
    role_placeholder_is_generic,
    role_ref,
    sentinel_requirement,
    validate_document_requirement,
    validate_reuse_rules,
    validate_role_assignments,
)
from sydel_doc_engine.front_data.models import ValidationIssueType


def test_praticien_can_also_be_associe_gerant_signataire_via_explicit_assignments() -> None:
    dossier = DossierRecord(id="dossier-person-roles")
    dossier.add_person(PersonRecord(id="person-praticien", prenom="Alice", nom="Martin"))

    assign_explicit_role(dossier, BusinessRole.PRATICIEN, "person-praticien")
    assign_explicit_role(
        dossier,
        BusinessRole.ASSOCIE,
        "person-praticien",
        target_type=RoleTargetType.PERSON,
    )
    assign_explicit_role(dossier, BusinessRole.GERANT, "person-praticien")
    assign_explicit_role(
        dossier,
        BusinessRole.SIGNATAIRE,
        "person-praticien",
        scope=RoleScope.DOCUMENT,
        document_code="DOC-017",
    )

    assert {assignment.role for assignment in dossier.role_assignments.values()} == {
        BusinessRole.PRATICIEN,
        BusinessRole.ASSOCIE,
        BusinessRole.GERANT,
        BusinessRole.SIGNATAIRE,
    }
    assert validate_role_assignments(dossier) == ()


def test_mandataire_is_not_signataire_by_default_for_doc_034() -> None:
    requirement = sentinel_requirement("DOC-034")
    dossier = DossierRecord(id="dossier-doc-034-mandataire")
    dossier.add_person(PersonRecord(id="person-signataire", prenom="Alice", nom="Martin"))
    dossier.add_company(CompanyRecord(id="company-main", denomination="SEL TEST"))
    dossier.add_company(CompanyRecord(id="company-order", denomination="Conseil de l'ordre"))

    assign_explicit_role(
        dossier,
        BusinessRole.SIGNATAIRE,
        "person-signataire",
        scope=RoleScope.DOCUMENT,
        document_code="DOC-034",
    )
    assign_explicit_role(dossier, BusinessRole.SOCIETE_PRINCIPALE, "company-main")
    assign_explicit_role(
        dossier,
        BusinessRole.ORDRE_PROFESSIONNEL,
        "company-order",
        scope=RoleScope.OPERATION,
    )

    role_issues = [
        issue
        for issue in validate_document_requirement(
            dossier,
            requirement,
            include_unresolved_ambiguities=False,
        )
        if issue.issue_type is ValidationIssueType.MISSING_ROLE
    ]

    assert [issue.role for issue in role_issues] == [BusinessRole.MANDATAIRE]


def test_representant_personne_morale_references_existing_company() -> None:
    dossier = DossierRecord(id="dossier-representation")
    dossier.add_person(PersonRecord(id="person-rep", prenom="Bruno", nom="Durand"))
    dossier.add_company(CompanyRecord(id="company-associated", denomination="SC HOLDING"))

    missing_link = assign_explicit_role(
        dossier,
        BusinessRole.REPRESENTANT_PERSONNE_MORALE,
        "person-rep",
        scope=RoleScope.OPERATION,
    )
    assert missing_link.role is BusinessRole.REPRESENTANT_PERSONNE_MORALE
    assert [issue.issue_type for issue in validate_role_assignments(dossier)] == [
        ValidationIssueType.MISSING_REPRESENTED_ENTITY
    ]

    linked = DossierRecord(id="dossier-representation-ok")
    linked.add_person(PersonRecord(id="person-rep", prenom="Bruno", nom="Durand"))
    linked.add_company(CompanyRecord(id="company-associated", denomination="SC HOLDING"))
    assign_explicit_role(
        linked,
        BusinessRole.REPRESENTANT_PERSONNE_MORALE,
        "person-rep",
        scope=RoleScope.OPERATION,
        represented_target_type=RoleTargetType.COMPANY,
        represented_target_id="company-associated",
        represented_role=BusinessRole.ASSOCIE,
    )

    assert validate_role_assignments(linked) == ()


def test_commissaire_aux_apports_is_distinct_from_operation_parties() -> None:
    dossier = DossierRecord(id="dossier-commissaire-conflict")
    dossier.add_person(PersonRecord(id="person-apporteur", prenom="Claire", nom="Roux"))

    assign_explicit_role(
        dossier,
        BusinessRole.APPORTEUR,
        "person-apporteur",
        target_type=RoleTargetType.PERSON,
        scope=RoleScope.OPERATION,
    )
    assign_explicit_role(
        dossier,
        BusinessRole.COMMISSAIRE_AUX_APPORTS,
        "person-apporteur",
        target_type=RoleTargetType.PERSON,
        scope=RoleScope.OPERATION,
    )

    assert [issue.issue_type for issue in validate_role_assignments(dossier)] == [
        ValidationIssueType.THIRD_PARTY_ROLE_CONFLICT
    ]

    clean = DossierRecord(id="dossier-commissaire-ok")
    clean.add_person(PersonRecord(id="person-apporteur", prenom="Claire", nom="Roux"))
    clean.add_person(PersonRecord(id="person-commissaire", prenom="Denis", nom="Morel"))
    assign_explicit_role(
        clean,
        BusinessRole.APPORTEUR,
        "person-apporteur",
        target_type=RoleTargetType.PERSON,
        scope=RoleScope.OPERATION,
    )
    assign_explicit_role(
        clean,
        BusinessRole.COMMISSAIRE_AUX_APPORTS,
        "person-commissaire",
        target_type=RoleTargetType.PERSON,
        scope=RoleScope.OPERATION,
    )

    assert validate_role_assignments(clean) == ()


def test_doc_034_order_role_model_is_explicit() -> None:
    assert ORDER_ROLE_MODEL.inscrit_personne_role is BusinessRole.SIGNATAIRE
    assert ORDER_ROLE_MODEL.societe_inscrite_role is BusinessRole.SOCIETE_PRINCIPALE
    assert ORDER_ROLE_MODEL.conseil_ordre_role is BusinessRole.ORDRE_PROFESSIONNEL
    assert ORDER_ROLE_MODEL.mandataire_role is BusinessRole.MANDATAIRE

    dossier = _role_ready_sentinel_dossier("DOC-034")
    role_issues = _role_issue_types_for_requirement(dossier, "DOC-034")

    assert role_issues == []
    assert validate_role_assignments(dossier) == ()


def test_doc_041_roles_distinguish_apporteur_spfpl_cible_evaluateur_commissaire() -> None:
    dossier = _role_ready_sentinel_dossier("DOC-041")

    role_targets = {
        assignment.role: assignment.target_id for assignment in dossier.role_assignments.values()
    }

    assert role_targets[BusinessRole.APPORTEUR] != role_targets[BusinessRole.EVALUATEUR_APPORT]
    assert role_targets[BusinessRole.APPORTEUR] != (
        role_targets[BusinessRole.COMMISSAIRE_AUX_APPORTS]
    )
    assert role_targets[BusinessRole.SPFPL_BENEFICIAIRE] != role_targets[BusinessRole.SOCIETE_CIBLE]
    assert _role_issue_types_for_requirement(dossier, "DOC-041") == []
    assert validate_role_assignments(dossier) == ()


def test_doc_033_roles_distinguish_cedant_cessionnaire_scm_and_representant() -> None:
    dossier = _role_ready_sentinel_dossier("DOC-033")

    role_targets = {
        assignment.role: assignment.target_id for assignment in dossier.role_assignments.values()
    }

    assert role_targets[BusinessRole.CEDANT] != role_targets[BusinessRole.CESSIONNAIRE]
    assert role_targets[BusinessRole.CESSIONNAIRE] != role_targets[BusinessRole.SCM_CEDEE]
    assert role_targets[BusinessRole.REPRESENTANT_PERSONNE_MORALE] != (
        role_targets[BusinessRole.CESSIONNAIRE]
    )
    assert _role_issue_types_for_requirement(dossier, "DOC-033") == []
    assert validate_role_assignments(dossier) == ()


def test_role_placeholders_do_not_create_default_fusion() -> None:
    person_definition = canonical_definition("personne.{role}.*")
    company_definition = canonical_definition("societe.{role}.*")

    assert person_definition is not None
    assert company_definition is not None
    assert person_definition.role is None
    assert company_definition.role is None
    assert role_placeholder_is_generic("personne.{role}.nom")
    assert role_from_canonical_path("personne.{role}.nom") is None
    assert role_from_canonical_path("personne.praticien.nom") is BusinessRole.PRATICIEN


def test_role_reuse_rules_reject_implicit_signataire_mandataire_confusion() -> None:
    dossier = DossierRecord(id="dossier-role-reuse")
    dossier.add_reuse_rule(
        ReuseRuleState(
            id="reuse-mandataire-signataire",
            source_ref=role_ref(BusinessRole.MANDATAIRE),
            target_ref=role_ref(BusinessRole.SIGNATAIRE),
            relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
            status=ReuseRuleStatus.ACTIVE,
            explicit=False,
        )
    )

    issue_types = [issue.issue_type for issue in validate_reuse_rules(dossier)]

    assert ValidationIssueType.IMPLICIT_ROLE_REUSE_FORBIDDEN in issue_types
    assert ValidationIssueType.ROLE_CONFUSION in issue_types


def test_document_execution_role_cannot_be_scoped_to_dossier_without_declaration() -> None:
    dossier = DossierRecord(id="dossier-invalid-scope")
    dossier.add_person(PersonRecord(id="person-signataire", prenom="Alice", nom="Martin"))
    dossier.assign_role(
        BusinessRole.SIGNATAIRE,
        RoleTargetType.PERSON,
        "person-signataire",
        scope=RoleScope.DOSSIER,
    )

    assert [issue.issue_type for issue in validate_role_assignments(dossier)] == [
        ValidationIssueType.INVALID_ROLE_SCOPE
    ]


def _role_ready_sentinel_dossier(doc_code: str) -> DossierRecord:
    requirement = sentinel_requirement(doc_code)
    dossier = DossierRecord(id=f"dossier-{doc_code}")
    dossier.add_document_requirement(requirement)

    for role in sorted(requirement.required_roles, key=lambda item: item.value):
        _add_role_target(dossier, role, doc_code)

    for usage in requirement.required_address_usages:
        dossier.add_address(
            AddressRecord(
                id=f"address-{usage.value}",
                usage=usage,
                display_value=f"Adresse {usage.value}",
            )
        )

    return dossier


def _add_role_target(dossier: DossierRecord, role: BusinessRole, doc_code: str) -> None:
    if role in {
        BusinessRole.SOCIETE_PRINCIPALE,
        BusinessRole.SOCIETE_CIBLE,
        BusinessRole.SOCIETE_APPORTEE,
        BusinessRole.SPFPL_BENEFICIAIRE,
        BusinessRole.SCM,
        BusinessRole.SCM_CEDEE,
        BusinessRole.BANQUE,
        BusinessRole.ORDRE_PROFESSIONNEL,
        BusinessRole.ACQUEREUR,
        BusinessRole.CESSIONNAIRE,
    }:
        company_id = f"company-{role.value}"
        dossier.add_company(CompanyRecord(id=company_id, denomination=f"Company {role.value}"))
        assign_explicit_role(
            dossier,
            role,
            company_id,
            scope=RoleScope.OPERATION,
            document_code=doc_code,
        )
        return

    person_id = f"person-{role.value}"
    dossier.add_person(PersonRecord(id=person_id, prenom="Alice", nom=role.value.title()))
    represented_target_type = None
    represented_target_id = None
    represented_role = None
    if role is BusinessRole.REPRESENTANT_PERSONNE_MORALE:
        represented_target_type = RoleTargetType.COMPANY
        represented_target_id = _represented_company_id(dossier)
        represented_role = BusinessRole.CESSIONNAIRE
    assign_explicit_role(
        dossier,
        role,
        person_id,
        target_type=RoleTargetType.PERSON,
        scope=_scope_for_role(role),
        document_code=doc_code,
        represented_target_type=represented_target_type,
        represented_target_id=represented_target_id,
        represented_role=represented_role,
    )


def _scope_for_role(role: BusinessRole) -> RoleScope:
    if role in {BusinessRole.SIGNATAIRE, BusinessRole.MANDATAIRE}:
        return RoleScope.DOCUMENT
    return RoleScope.OPERATION


def _represented_company_id(dossier: DossierRecord) -> str:
    for role in (
        BusinessRole.CESSIONNAIRE,
        BusinessRole.ACQUEREUR,
        BusinessRole.SOCIETE_CIBLE,
        BusinessRole.SCM,
    ):
        for assignment in dossier.roles_for(role):
            if assignment.target_type is RoleTargetType.COMPANY:
                return assignment.target_id
    raise AssertionError("representative role requires a company role in the sentinel setup")


def _role_issue_types_for_requirement(
    dossier: DossierRecord,
    doc_code: str,
) -> list[ValidationIssueType]:
    return [
        issue.issue_type
        for issue in validate_document_requirement(
            dossier,
            sentinel_requirement(doc_code),
            include_unresolved_ambiguities=False,
        )
        if issue.issue_type is ValidationIssueType.MISSING_ROLE
    ]
