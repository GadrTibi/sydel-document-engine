from __future__ import annotations

from sydel_doc_engine.front_data import (
    AddressDisplaySource,
    AddressRecord,
    AddressUsage,
    CanonicalRelationType,
    DossierRecord,
    FrontObjectType,
    PersonRecord,
    ReuseRuleState,
    ReuseRuleStatus,
    ValidationIssueType,
    address_display_value,
    address_ref,
    canonical_definition,
    compose_address_display,
    sentinel_requirement,
    validate_address_records,
    validate_document_requirement,
    validate_reuse_rules,
)


def test_domiciliation_reuses_siege_social_through_explicit_rule() -> None:
    dossier = DossierRecord(id="dossier-domiciliation")
    dossier.add_address(
        AddressRecord(
            id="addr-siege",
            usage=AddressUsage.SIEGE_SOCIAL,
            display_value="1 rue du Siege, 75001 Paris",
        )
    )

    assert not dossier.is_address_usage_available(AddressUsage.DOMICILIATION)

    dossier.add_reuse_rule(
        _address_reuse_rule(
            "reuse-domiciliation-siege",
            AddressUsage.SIEGE_SOCIAL,
            AddressUsage.DOMICILIATION,
        )
    )

    assert dossier.is_address_usage_available(AddressUsage.DOMICILIATION)
    assert validate_reuse_rules(dossier) == ()


def test_siege_social_does_not_reuse_lieu_exercice_by_default() -> None:
    dossier = DossierRecord(id="dossier-siege-lieu")
    dossier.add_address(
        AddressRecord(
            id="addr-lieu",
            usage=AddressUsage.LIEU_EXERCICE,
            display_value="2 avenue du Cabinet, 69001 Lyon",
        )
    )

    assert not dossier.is_address_usage_available(AddressUsage.SIEGE_SOCIAL)

    dossier.add_reuse_rule(
        _address_reuse_rule(
            "reuse-siege-lieu",
            AddressUsage.LIEU_EXERCICE,
            AddressUsage.SIEGE_SOCIAL,
        )
    )

    assert dossier.is_address_usage_available(AddressUsage.SIEGE_SOCIAL)
    assert validate_reuse_rules(dossier) == ()


def test_scm_reuses_lieu_exercice_as_traceable_standard_rule() -> None:
    dossier = DossierRecord(id="dossier-scm-address")
    dossier.add_address(
        AddressRecord(
            id="addr-lieu",
            usage=AddressUsage.LIEU_EXERCICE,
            display_value="3 place du Cabinet, 33000 Bordeaux",
        )
    )
    dossier.add_reuse_rule(
        _address_reuse_rule(
            "reuse-scm-lieu",
            AddressUsage.LIEU_EXERCICE,
            AddressUsage.SCM,
        )
    )

    assert dossier.is_address_usage_available(AddressUsage.SCM)
    assert validate_reuse_rules(dossier) == ()


def test_scm_cedee_and_cessionnaire_scm_are_distinct_by_default() -> None:
    dossier = DossierRecord(id="dossier-scm-cession")
    dossier.add_address(
        AddressRecord(
            id="addr-scm-cedee",
            usage=AddressUsage.SCM_CEDEE,
            display_value="4 rue de la SCM, 45000 Orleans",
        )
    )

    assert not dossier.is_address_usage_available(AddressUsage.CESSIONNAIRE_SCM)

    dossier.add_reuse_rule(
        _address_reuse_rule(
            "reuse-scm-cessionnaire-confirmed",
            AddressUsage.SCM_CEDEE,
            AddressUsage.CESSIONNAIRE_SCM,
        )
    )

    assert dossier.is_address_usage_available(AddressUsage.CESSIONNAIRE_SCM)
    assert validate_reuse_rules(dossier) == ()


def test_domicile_siege_and_cabinet_do_not_merge_from_identical_text() -> None:
    same_text = "5 rue Commune, 75002 Paris"
    dossier = DossierRecord(id="dossier-no-fusion-address")
    dossier.add_address(
        AddressRecord(
            id="addr-domicile",
            usage=AddressUsage.DOMICILE_PRATICIEN,
            display_value=same_text,
        )
    )
    dossier.add_address(
        AddressRecord(
            id="addr-siege",
            usage=AddressUsage.SIEGE_SOCIAL,
            display_value=same_text,
        )
    )
    dossier.add_address(
        AddressRecord(
            id="addr-cabinet",
            usage=AddressUsage.CABINET_CEDE,
            display_value=same_text,
        )
    )

    assert {address.usage for address in dossier.addresses.values()} == {
        AddressUsage.DOMICILE_PRATICIEN,
        AddressUsage.SIEGE_SOCIAL,
        AddressUsage.CABINET_CEDE,
    }
    assert len(dossier.addresses) == 3


def test_display_address_is_derived_from_components_with_traceability() -> None:
    address = AddressRecord(
        id="addr-components",
        usage=AddressUsage.LIEU_EXERCICE,
        street_number="12",
        street_name="rue des Lilas",
        postal_code="75003",
        city="Paris",
        display_source=AddressDisplaySource.COMPONENTS,
        display_source_rule_id="display-from-components",
    )
    dossier = DossierRecord(id="dossier-components", addresses={address.id: address})

    assert compose_address_display(address) == "12 rue des Lilas, 75003 Paris"
    assert address_display_value(address) == "12 rue des Lilas, 75003 Paris"
    assert validate_address_records(dossier) == ()


def test_display_override_is_possible_for_legacy_document_shape() -> None:
    address = AddressRecord(
        id="addr-override",
        usage=AddressUsage.DOMICILIATION,
        street_number="12",
        street_name="rue des Lilas",
        postal_code="75003",
        city="Paris",
        display_value="12 rue des Lilas - 75003 PARIS",
        display_source=AddressDisplaySource.OVERRIDE,
        display_override_reason="Legacy DOC-002 display punctuation.",
        is_override=True,
    )
    dossier = DossierRecord(id="dossier-override", addresses={address.id: address})

    assert address_display_value(address) == "12 rue des Lilas - 75003 PARIS"
    assert validate_address_records(dossier) == ()


def test_bad_override_and_untraced_derivation_are_diagnosed() -> None:
    dossier = DossierRecord(id="dossier-address-diagnostics")
    dossier.add_address(
        AddressRecord(
            id="addr-untraced",
            usage=AddressUsage.LIEU_EXERCICE,
            street_number="12",
            street_name="rue des Lilas",
        )
    )
    dossier.add_address(
        AddressRecord(
            id="addr-bad-override",
            usage=AddressUsage.DOMICILIATION,
            display_value="Forme forcee",
            display_source=AddressDisplaySource.OVERRIDE,
            is_override=True,
        )
    )

    issue_types = [issue.issue_type for issue in validate_address_records(dossier)]

    assert ValidationIssueType.MISSING_ADDRESS_REUSE_SOURCE in issue_types
    assert ValidationIssueType.INCONSISTENT_ADDRESS_OVERRIDE in issue_types


def test_wrong_address_usage_for_party_is_diagnosed() -> None:
    dossier = DossierRecord(id="dossier-wrong-owner")
    dossier.add_person(PersonRecord(id="person-bank", prenom="Alice", nom="Banque"))
    dossier.add_address(
        AddressRecord(
            id="addr-bank",
            usage=AddressUsage.BANQUE,
            display_value="1 rue Banque, 75009 Paris",
            owner_object_type=FrontObjectType.PERSON,
            owner_object_id="person-bank",
        )
    )

    assert [issue.issue_type for issue in validate_address_records(dossier)] == [
        ValidationIssueType.WRONG_ADDRESS_USAGE
    ]


def test_address_reuse_without_registered_policy_is_rejected() -> None:
    dossier = DossierRecord(id="dossier-bad-address-reuse")
    dossier.add_reuse_rule(
        _address_reuse_rule(
            "reuse-bank-domiciliation",
            AddressUsage.BANQUE,
            AddressUsage.DOMICILIATION,
        )
    )

    assert [issue.issue_type for issue in validate_reuse_rules(dossier)] == [
        ValidationIssueType.ADDRESS_REUSE_FORBIDDEN
    ]


def test_doc_002_address_coverage_uses_domiciliation_siege_rule() -> None:
    dossier = DossierRecord(id="dossier-doc-002-address")
    dossier.add_address(
        AddressRecord(
            id="addr-siege",
            usage=AddressUsage.SIEGE_SOCIAL,
            display_value="1 rue du Siege, 75001 Paris",
        )
    )
    dossier.add_reuse_rule(
        _address_reuse_rule(
            "reuse-doc-002-domiciliation",
            AddressUsage.SIEGE_SOCIAL,
            AddressUsage.DOMICILIATION,
        )
    )

    assert _missing_address_usages(dossier, "DOC-002") == []
    assert canonical_definition("domiciliation.adresse_affichee") is not None
    assert canonical_definition("domiciliation.adresse_domiciliation_affichee") is None


def test_doc_033_address_coverage_keeps_scm_addresses_distinct() -> None:
    dossier = DossierRecord(id="dossier-doc-033-address")
    for usage in sentinel_requirement("DOC-033").required_address_usages:
        dossier.add_address(_address_for_usage(usage))

    assert _missing_address_usages(dossier, "DOC-033") == []
    assert (
        dossier.addresses_for_usage(AddressUsage.SCM_CEDEE)[0].id
        != dossier.addresses_for_usage(AddressUsage.CESSIONNAIRE_SCM)[0].id
    )


def test_doc_009_address_coverage_distinguishes_cabinet_locaux_parties_and_bank() -> None:
    dossier = DossierRecord(id="dossier-doc-009-address")
    for usage in (
        AddressUsage.DOMICILE_CEDANT,
        AddressUsage.LIEU_EXERCICE,
        AddressUsage.SIEGE_SOCIAL,
        AddressUsage.BAILLEUR,
        AddressUsage.LOCATAIRE,
        AddressUsage.BANQUE,
    ):
        dossier.add_address(_address_for_usage(usage))
    dossier.add_reuse_rule(
        _address_reuse_rule(
            "reuse-doc-009-cabinet",
            AddressUsage.LIEU_EXERCICE,
            AddressUsage.CABINET_CEDE,
        )
    )
    dossier.add_reuse_rule(
        _address_reuse_rule(
            "reuse-doc-009-locaux",
            AddressUsage.LIEU_EXERCICE,
            AddressUsage.LOCAUX_LOUES,
        )
    )

    assert _missing_address_usages(dossier, "DOC-009") == []
    assert canonical_definition("bail.bailleur.adresse") is not None
    assert canonical_definition("banque.{role}.adresse") is not None


def test_doc_025_address_coverage_reuses_lieu_for_scm_and_keeps_bank_explicit() -> None:
    dossier = DossierRecord(id="dossier-doc-025-address")
    for usage in (
        AddressUsage.LIEU_EXERCICE,
        AddressUsage.ADRESSE_PERSONNELLE,
        AddressUsage.SIEGE_SOCIAL,
        AddressUsage.BANQUE,
    ):
        dossier.add_address(_address_for_usage(usage))
    dossier.add_reuse_rule(
        _address_reuse_rule(
            "reuse-doc-025-scm",
            AddressUsage.LIEU_EXERCICE,
            AddressUsage.SCM,
        )
    )

    assert _missing_address_usages(dossier, "DOC-025") == []
    assert canonical_definition("scm.adresse") is not None
    assert canonical_definition("banque.{role}.adresse_affichee") is not None


def test_doc_034_order_address_mapping_is_explicit() -> None:
    assert canonical_definition("ordre.adresse") is not None
    assert canonical_definition("ordre.adresse_affichee") is not None
    assert canonical_definition("ordre.adresse.cp") is not None


def _address_reuse_rule(
    rule_id: str,
    source: AddressUsage,
    target: AddressUsage,
) -> ReuseRuleState:
    return ReuseRuleState(
        id=rule_id,
        source_ref=address_ref(source),
        target_ref=address_ref(target),
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        status=ReuseRuleStatus.ACTIVE,
        explicit=True,
    )


def _address_for_usage(usage: AddressUsage) -> AddressRecord:
    return AddressRecord(
        id=f"address-{usage.value}",
        usage=usage,
        display_value=f"Adresse {usage.value}",
    )


def _missing_address_usages(dossier: DossierRecord, doc_code: str) -> list[AddressUsage]:
    return [
        issue.address_usage
        for issue in validate_document_requirement(
            dossier,
            sentinel_requirement(doc_code),
            include_unresolved_ambiguities=False,
        )
        if issue.issue_type is ValidationIssueType.MISSING_TYPED_ADDRESS
        and issue.address_usage is not None
    ]
