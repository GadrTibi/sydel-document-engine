from __future__ import annotations

import csv
from pathlib import Path

import pytest

from sydel_doc_engine.front_data import (
    SENTINEL_DOCUMENT_REQUIREMENTS,
    AddressRecord,
    AddressUsage,
    BusinessRole,
    CanonicalFieldValue,
    CanonicalRelationType,
    CompanyRecord,
    DocumentRequirementRecord,
    DossierRecord,
    FieldFormKind,
    FrontObjectType,
    PersonRecord,
    ReuseRuleState,
    ReuseRuleStatus,
    RoleTargetType,
    address_ref,
    canonical_definition,
    canonicalize_legacy_alias,
    sentinel_requirement,
    validate_document_requirement,
    validate_required_entities_linked,
    validate_reuse_rules,
)
from sydel_doc_engine.front_data.models import ValidationIssueType

SENTINEL_CODES = ("DOC-002", "DOC-034", "DOC-017", "DOC-033", "DOC-009", "DOC-041", "DOC-025")

COMPANY_ROLES = {
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
    BusinessRole.BAILLEUR,
    BusinessRole.LOCATAIRE,
}


def test_person_can_be_assigned_to_multiple_explicit_roles() -> None:
    dossier = DossierRecord(id="dossier-roles")
    dossier.add_person(PersonRecord(id="person-1", prenom="Alice", nom="Martin"))

    for role in (
        BusinessRole.PRATICIEN,
        BusinessRole.ASSOCIE,
        BusinessRole.GERANT,
        BusinessRole.SIGNATAIRE,
    ):
        dossier.assign_role(role, RoleTargetType.PERSON, "person-1")

    assert {assignment.role for assignment in dossier.role_assignments.values()} == {
        BusinessRole.PRATICIEN,
        BusinessRole.ASSOCIE,
        BusinessRole.GERANT,
        BusinessRole.SIGNATAIRE,
    }
    assert all(assignment.explicit for assignment in dossier.role_assignments.values())


def test_companies_remain_distinct_without_silent_fusion() -> None:
    dossier = DossierRecord(id="dossier-companies")
    dossier.add_company(CompanyRecord(id="sel", denomination="CABINET MARTIN"))
    dossier.add_company(CompanyRecord(id="scm", denomination="CABINET MARTIN"))

    dossier.assign_role(BusinessRole.SOCIETE_PRINCIPALE, RoleTargetType.COMPANY, "sel")
    dossier.assign_role(BusinessRole.SCM_CEDEE, RoleTargetType.COMPANY, "scm")

    assert set(dossier.companies) == {"sel", "scm"}
    assert dossier.companies["sel"] is not dossier.companies["scm"]


def test_typed_addresses_are_kept_as_separate_records() -> None:
    dossier = DossierRecord(id="dossier-addresses")
    same_display = "1 rue du Test, 75000 Paris"

    dossier.add_address(
        AddressRecord(id="addr-siege", usage=AddressUsage.SIEGE_SOCIAL, display_value=same_display)
    )
    dossier.add_address(
        AddressRecord(
            id="addr-exercice",
            usage=AddressUsage.LIEU_EXERCICE,
            display_value=same_display,
        )
    )

    assert len(dossier.addresses) == 2
    assert dossier.addresses_for_usage(AddressUsage.SIEGE_SOCIAL)[0].id == "addr-siege"
    assert dossier.addresses_for_usage(AddressUsage.LIEU_EXERCICE)[0].id == "addr-exercice"


def test_domiciliation_reuses_siege_only_with_explicit_rule() -> None:
    requirement = DocumentRequirementRecord(
        doc_code="DOC-X",
        doc_label="Address check",
        required_address_usages=(AddressUsage.DOMICILIATION,),
    )
    dossier = DossierRecord(id="dossier-reuse")
    dossier.add_address(
        AddressRecord(
            id="addr-siege",
            usage=AddressUsage.SIEGE_SOCIAL,
            display_value="1 rue du Test, 75000 Paris",
        )
    )

    issues_without_rule = validate_document_requirement(
        dossier,
        requirement,
        include_unresolved_ambiguities=False,
    )

    dossier.add_reuse_rule(
        ReuseRuleState(
            id="reuse-domiciliation",
            source_ref=address_ref(AddressUsage.SIEGE_SOCIAL),
            target_ref=address_ref(AddressUsage.DOMICILIATION),
            relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
            status=ReuseRuleStatus.ACTIVE,
        )
    )
    issues_with_rule = validate_document_requirement(
        dossier,
        requirement,
        include_unresolved_ambiguities=False,
    )

    assert [issue.issue_type for issue in issues_without_rule] == [
        ValidationIssueType.MISSING_TYPED_ADDRESS
    ]
    assert issues_with_rule == ()


def test_siege_and_lieu_exercice_do_not_merge_without_rule() -> None:
    requirement = DocumentRequirementRecord(
        doc_code="DOC-Y",
        doc_label="Seat check",
        required_address_usages=(AddressUsage.SIEGE_SOCIAL,),
    )
    dossier = DossierRecord(id="dossier-no-implicit-address")
    dossier.add_address(
        AddressRecord(
            id="addr-lieu",
            usage=AddressUsage.LIEU_EXERCICE,
            display_value="2 avenue Claire, 69000 Lyon",
        )
    )

    issues = validate_document_requirement(
        dossier,
        requirement,
        include_unresolved_ambiguities=False,
    )

    assert [issue.issue_type for issue in issues] == [ValidationIssueType.MISSING_TYPED_ADDRESS]
    assert not dossier.has_active_reuse_rule(
        address_ref(AddressUsage.LIEU_EXERCICE),
        address_ref(AddressUsage.SIEGE_SOCIAL),
    )


def test_reuse_validation_rejects_distinct_fields() -> None:
    dossier = DossierRecord(id="dossier-distinct")
    dossier.add_reuse_rule(
        ReuseRuleState(
            id="bad-reuse",
            source_ref=address_ref(AddressUsage.LIEU_EXERCICE),
            target_ref=address_ref(AddressUsage.SIEGE_SOCIAL),
            relation_type=CanonicalRelationType.DISTINCT_FIELDS,
            status=ReuseRuleStatus.ACTIVE,
        )
    )

    issues = validate_reuse_rules(dossier)

    assert [issue.issue_type for issue in issues] == [ValidationIssueType.REUSE_CONFLICT]


def test_missing_role_and_unlinked_entity_are_diagnosed() -> None:
    requirement = DocumentRequirementRecord(
        doc_code="DOC-Z",
        doc_label="Role check",
        required_roles=(BusinessRole.SIGNATAIRE,),
    )
    dossier = DossierRecord(id="dossier-diagnostics")
    missing_role_issues = validate_document_requirement(
        dossier,
        requirement,
        include_unresolved_ambiguities=False,
    )

    dossier.assign_role(BusinessRole.SIGNATAIRE, RoleTargetType.PERSON, "missing-person")
    unlinked_issues = validate_required_entities_linked(dossier)

    assert [issue.issue_type for issue in missing_role_issues] == [
        ValidationIssueType.MISSING_ROLE
    ]
    assert [issue.issue_type for issue in unlinked_issues] == [
        ValidationIssueType.UNLINKED_REQUIRED_ENTITY
    ]


def test_sentinel_mapping_uses_the_csv_checklist() -> None:
    checklist_path = Path("docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv")
    with checklist_path.open(encoding="utf-8-sig", newline="") as handle:
        csv_codes = {row["doc_code"] for row in csv.DictReader(handle)}

    assert csv_codes == set(SENTINEL_CODES)
    assert set(SENTINEL_DOCUMENT_REQUIREMENTS) == csv_codes


@pytest.mark.parametrize("doc_code", SENTINEL_CODES)
def test_sentinel_document_requirement_is_covered_by_front_data_layer(doc_code: str) -> None:
    requirement = sentinel_requirement(doc_code)
    dossier = _satisfied_dossier(requirement)

    missing_definitions = [
        field_path
        for field_path in requirement.required_canonical_fields
        if canonical_definition(field_path) is None
    ]
    issues = validate_document_requirement(dossier, requirement)

    assert requirement.required_roles
    assert requirement.required_address_usages
    assert requirement.required_canonical_fields
    assert missing_definitions == []
    assert issues == ()


def test_legacy_alias_is_documentary_form_not_business_field() -> None:
    value = canonicalize_legacy_alias(
        "domiciliation.adresse_domiciliation_affichee",
        "1 rue du Test, 75000 Paris",
    )

    assert value.field_path == "domiciliation.adresse"
    assert value.source_field_path == "domiciliation.adresse_domiciliation_affichee"
    assert value.form_kind is FieldFormKind.DOCUMENTARY_ALIAS
    assert not value.is_business_field
    assert canonical_definition("domiciliation.adresse_domiciliation_affichee") is None


def _satisfied_dossier(requirement: DocumentRequirementRecord) -> DossierRecord:
    dossier = DossierRecord(id=f"dossier-{requirement.doc_code}")
    dossier.add_document_requirement(requirement)

    for role in sorted(
        {*requirement.required_roles, *requirement.required_entities},
        key=lambda item: item.value,
    ):
        if role in COMPANY_ROLES:
            company_id = f"company-{role.value}"
            if company_id not in dossier.companies:
                dossier.add_company(
                    CompanyRecord(
                        id=company_id,
                        denomination=f"Company {role.value}",
                    )
                )
            dossier.assign_role(role, RoleTargetType.COMPANY, company_id)
        else:
            person_id = f"person-{role.value}"
            if person_id not in dossier.persons:
                dossier.add_person(
                    PersonRecord(
                        id=person_id,
                        prenom="Alice",
                        nom=role.value.title(),
                    )
                )
            dossier.assign_role(role, RoleTargetType.PERSON, person_id)

    for usage in requirement.required_address_usages:
        dossier.add_address(
            AddressRecord(
                id=f"address-{usage.value}",
                usage=usage,
                display_value=f"Adresse {usage.value}",
            )
        )

    for field_path in requirement.required_canonical_fields:
        dossier.add_canonical_value(
            CanonicalFieldValue(
                field_path=_sample_field_path(field_path),
                value="sample",
                owner_object_type=FrontObjectType.DOSSIER,
            )
        )

    for ambiguity_key in requirement.unresolved_ambiguity_keys:
        dossier.resolve_ambiguity(ambiguity_key)

    return dossier


def _sample_field_path(field_path: str) -> str:
    sample = field_path.replace("{role}", "praticien").replace("{champ}", "nom")
    if sample.endswith(".*"):
        return sample[:-2] + ".sample"
    if sample.endswith("[]"):
        return sample[:-2] + "[0].sample"
    return sample
