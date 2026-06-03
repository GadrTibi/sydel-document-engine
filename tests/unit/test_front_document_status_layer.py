from __future__ import annotations

import inspect

import sydel_doc_engine.front_data.document_status as document_status
from sydel_doc_engine.front_data import (
    AddressRecord,
    AddressUsage,
    BusinessRole,
    CanonicalFieldValue,
    DocumentLotStatus,
    DocumentStatus,
    DocumentStatusReasonType,
    DossierBlockId,
    DossierRecord,
    FrontObjectType,
    PersonRecord,
    RoleScope,
    RoleTargetType,
    build_document_lot_status,
    build_document_status,
    build_document_status_for_code,
    sentinel_requirement,
)
from sydel_doc_engine.front_data.models import CompanyRecord, DocumentRequirementRecord

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


def test_doc_002_is_generable_when_domiciliation_and_siege_are_ready() -> None:
    requirement = sentinel_requirement("DOC-002")
    dossier = _satisfied_dossier(requirement)

    status = build_document_status(dossier, requirement)

    assert status.status is DocumentStatus.GENERABLE
    assert status.is_ready_for_generation
    assert status.why_not_generable() == ()


def test_document_status_detects_blocked_missing_data() -> None:
    requirement = sentinel_requirement("DOC-002")
    dossier = DossierRecord(id="dossier-doc-002-missing")
    dossier.add_document_requirement(requirement)

    status = build_document_status(dossier, requirement)

    assert status.status is DocumentStatus.BLOCKED_MISSING_DATA
    assert BusinessRole.SIGNATAIRE in status.missing_roles
    assert AddressUsage.DOMICILIATION in status.missing_address_usages
    assert "signature.date" in status.missing_canonical_fields


def test_document_status_detects_blocked_unresolved_ambiguity() -> None:
    requirement = sentinel_requirement("DOC-034")
    dossier = _satisfied_dossier(
        requirement,
        resolve_ambiguities=False,
        extra_fields=(
            "personne.praticien.numero_ordre",
            "personne.praticien.numero_rpps",
        ),
    )

    status = build_document_status(dossier, requirement)

    assert status.status is DocumentStatus.BLOCKED_UNRESOLVED_AMBIGUITY
    assert "mandataire_configurable" in status.unresolved_ambiguity_keys
    assert "ordre_model_per_inscrit" in status.unresolved_ambiguity_keys


def test_manual_documents_are_visible_but_never_ready_for_generation() -> None:
    doc_013 = build_document_status_for_code("DOC-013")
    doc_014 = build_document_status_for_code("DOC-014")

    assert doc_013.status is DocumentStatus.MANUAL_ONLY
    assert doc_014.status is DocumentStatus.MANUAL_ONLY
    assert not doc_013.is_ready_for_generation
    assert not doc_014.is_ready_for_generation
    assert any(
        reason.reason_type is DocumentStatusReasonType.MANUAL_ONLY
        for reason in doc_013.reasons
    )


def test_doc_006_has_no_source_reserve_by_default() -> None:
    status = build_document_status_for_code("DOC-006")

    assert status.status is DocumentStatus.EXPECTED
    assert not status.is_ready_for_generation
    assert not any(
        reason.reason_type is DocumentStatusReasonType.RESERVE
        for reason in status.reasons
    )


def test_document_lot_ready_partial_and_blocked_statuses() -> None:
    doc_002_requirement = sentinel_requirement("DOC-002")
    doc_002_status = build_document_status(
        _satisfied_dossier(doc_002_requirement),
        doc_002_requirement,
    )
    doc_006_status = build_document_status_for_code("DOC-006")
    doc_013_status = build_document_status_for_code("DOC-013")
    doc_034_requirement = sentinel_requirement("DOC-034")
    blocked_dossier = DossierRecord(id="dossier-doc-034-blocked")
    blocked_dossier.add_document_requirement(doc_034_requirement)
    doc_034_status = build_document_status(blocked_dossier, doc_034_requirement)

    ready_lot = build_document_lot_status("lot-ready", "Lot ready", (doc_002_status,))
    partial_lot = build_document_lot_status(
        "lot-partial",
        "Lot partial",
        (doc_002_status, doc_006_status, doc_013_status),
    )
    blocked_lot = build_document_lot_status("lot-blocked", "Lot blocked", (doc_034_status,))

    assert ready_lot.status is DocumentLotStatus.READY
    assert partial_lot.status is DocumentLotStatus.PARTIAL
    assert blocked_lot.status is DocumentLotStatus.BLOCKED
    assert partial_lot.manual_document_codes == ("DOC-013",)
    assert partial_lot.reserve_document_codes == ()
    assert blocked_lot.blocked_document_codes == ("DOC-034",)


def test_doc_034_status_keeps_structured_order_and_mandate_blockages() -> None:
    requirement = sentinel_requirement("DOC-034")
    dossier = DossierRecord(id="dossier-doc-034-status")
    dossier.add_document_requirement(requirement)

    status = build_document_status(dossier, requirement)
    block_ids = {reason.block_id for reason in status.reasons}

    assert status.status is DocumentStatus.BLOCKED_MISSING_DATA
    assert DossierBlockId.ORDER_IDENTIFIERS in block_ids
    assert DossierBlockId.ORDER_MANDATE in block_ids
    assert BusinessRole.MANDATAIRE in status.missing_roles
    assert AddressUsage.ORDRE in status.missing_address_usages
    assert "personne.mandataire.*" in status.missing_canonical_fields


def test_doc_009_status_keeps_cession_bail_financing_and_origin_reasons() -> None:
    requirement = sentinel_requirement("DOC-009")
    dossier = DossierRecord(id="dossier-doc-009-status")
    dossier.add_document_requirement(requirement)

    status = build_document_status(dossier, requirement)
    block_ids = {reason.block_id for reason in status.reasons}

    assert status.status is DocumentStatus.BLOCKED_MISSING_DATA
    assert DossierBlockId.CESSION_CABINET in block_ids
    assert DossierBlockId.BAIL in block_ids
    assert DossierBlockId.FINANCING in block_ids
    assert DossierBlockId.CESSION_ORIGIN in block_ids
    assert DossierBlockId.CESSION_EXERCISES in block_ids
    assert "origine_propriete_libre" in status.unresolved_ambiguity_keys
    assert "cession.exercices[]" in status.missing_canonical_fields


def test_document_status_layer_has_no_streamlit_dependency() -> None:
    source = inspect.getsource(document_status).lower()

    assert "streamlit" not in source


def _satisfied_dossier(
    requirement: DocumentRequirementRecord,
    *,
    resolve_ambiguities: bool = True,
    extra_fields: tuple[str, ...] = (),
) -> DossierRecord:
    dossier = DossierRecord(id=f"dossier-{requirement.doc_code}")
    dossier.add_document_requirement(requirement)

    roles = sorted(
        {*requirement.required_roles, *requirement.required_entities},
        key=lambda item: item.value,
    )
    for role in (role for role in roles if role in COMPANY_ROLES):
        _add_company_role(dossier, role, requirement.doc_code)
    for role in (role for role in roles if role not in COMPANY_ROLES):
        _add_person_role(dossier, role, requirement.doc_code)

    for usage in requirement.required_address_usages:
        dossier.add_address(
            AddressRecord(
                id=f"address-{usage.value}",
                usage=usage,
                display_value=f"Adresse {usage.value}",
            )
        )

    for field_path in (*requirement.required_canonical_fields, *extra_fields):
        dossier.add_canonical_value(
            CanonicalFieldValue(
                field_path=_sample_field_path(field_path),
                value="sample",
                owner_object_type=FrontObjectType.DOSSIER,
            )
        )

    if resolve_ambiguities:
        for ambiguity_key in requirement.unresolved_ambiguity_keys:
            dossier.resolve_ambiguity(ambiguity_key)

    return dossier


def _add_company_role(
    dossier: DossierRecord,
    role: BusinessRole,
    doc_code: str,
) -> None:
    company_id = f"company-{role.value}"
    if company_id not in dossier.companies:
        dossier.add_company(CompanyRecord(id=company_id, denomination=f"Company {role.value}"))
    dossier.assign_role(
        role,
        RoleTargetType.COMPANY,
        company_id,
        scope=RoleScope.OPERATION,
        document_code=doc_code,
    )


def _add_person_role(
    dossier: DossierRecord,
    role: BusinessRole,
    doc_code: str,
) -> None:
    person_id = f"person-{role.value}"
    if person_id not in dossier.persons:
        dossier.add_person(PersonRecord(id=person_id, prenom="Alice", nom=role.value.title()))
    represented_target_type = None
    represented_target_id = None
    represented_role = None
    if role is BusinessRole.REPRESENTANT_PERSONNE_MORALE:
        represented_target_type = RoleTargetType.COMPANY
        represented_target_id = _represented_company_id(dossier)
        represented_role = BusinessRole.CESSIONNAIRE
    dossier.assign_role(
        role,
        RoleTargetType.PERSON,
        person_id,
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
    raise AssertionError("representative role requires a company role in the test setup")


def _sample_field_path(field_path: str) -> str:
    sample = field_path.replace("{role}", "praticien").replace("{champ}", "nom")
    if sample.endswith(".*"):
        return sample[:-2] + ".sample"
    if sample.endswith("[]"):
        return sample[:-2] + "[0].sample"
    return sample
