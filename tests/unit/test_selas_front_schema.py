from __future__ import annotations

from sydel_doc_engine.front_data import (
    AddressDisplaySource,
    AddressRecord,
    AddressUsage,
    BusinessRole,
    CanonicalRelationType,
    CanonicalFieldValue,
    CompanyRecord,
    DocumentRequirementStatus,
    DossierBlockId,
    DossierRecord,
    FlowStatus,
    FrontObjectType,
    PersonRecord,
    ReuseRuleState,
    ReuseRuleStatus,
    RoleScope,
    RoleTargetType,
    assign_explicit_role,
    address_ref,
    build_selas_front_schema,
    build_selas_schema_dossier,
    is_role_reuse_allowed,
    validate_document_requirement,
    validate_role_assignments,
    ValidationIssueType,
)


def test_selas_front_schema_is_common_backbone_without_generation() -> None:
    schema = build_selas_front_schema()

    assert schema.structure == "SELAS"
    assert schema.generation_enabled is False
    assert schema.active_professions == ("medecin",)
    assert schema.candidate_document_codes == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-034",
        "DOC-018",
    )
    assert "DOC-005" not in schema.candidate_document_codes
    assert "DOC-006" not in schema.candidate_document_codes
    assert "SELAS-DECISION-PRESIDENT" not in schema.candidate_document_codes
    assert "SELAS-DECISION-PRESIDENT" in schema.reserved_document_codes
    assert "DOC-006" not in schema.reserved_document_codes
    assert schema.pack_readiness.generation_enabled is False
    assert schema.pack_readiness.ready_document_codes == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-034",
        "DOC-018",
    )
    assert schema.pack_readiness.conditional_document_codes == ("DOC-005", "DOC-006")
    assert schema.pack_readiness.active_conditional_document_codes == ()
    assert schema.pack_readiness.reserved_document_codes == (
        "SELAS-DECISION-PRESIDENT",
        "SELAS-STATUTS-DENTISTE",
        "SELAS-ATTESTATION-CAPITAL",
    )
    assert schema.pack_readiness.active_pack_document_codes == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-034",
        "DOC-018",
    )
    assert {
        "directeur_general",
        "multi_actionnaires",
        "chirurgien_dentiste",
    }.issubset({case.key for case in schema.blocked_cases})


def test_selas_schema_uses_actionnaire_and_president_roles_without_gerant() -> None:
    requirements = {
        requirement.doc_code: requirement
        for requirement in build_selas_front_schema().candidate_document_requirements
    }

    statuts = requirements["DOC-018"]

    assert BusinessRole.ACTIONNAIRE in statuts.required_roles
    assert BusinessRole.PRESIDENT in statuts.required_roles
    assert all(
        BusinessRole.GERANT not in requirement.required_roles
        for requirement in requirements.values()
    )


def test_selas_reserved_documents_include_decision_president_and_capital_gaps() -> None:
    reserved = {
        requirement.doc_code: requirement
        for requirement in build_selas_front_schema().reserved_document_requirements
    }

    assert reserved["SELAS-DECISION-PRESIDENT"].status is (
        DocumentRequirementStatus.NOT_IMPLEMENTED
    )
    assert reserved["SELAS-STATUTS-DENTISTE"].status is (
        DocumentRequirementStatus.NOT_IMPLEMENTED
    )
    assert reserved["SELAS-ATTESTATION-CAPITAL"].status is (
        DocumentRequirementStatus.NOT_IMPLEMENTED
    )
    assert "absorbee par les statuts V1" in (
        reserved["SELAS-DECISION-PRESIDENT"].action_needed
    )
    assert BusinessRole.PRESIDENT in reserved["SELAS-DECISION-PRESIDENT"].required_roles


def test_selas_dnc_president_requires_president_signataire_and_filiation() -> None:
    requirements = {
        requirement.doc_code: requirement
        for requirement in build_selas_front_schema().candidate_document_requirements
    }
    dnc = requirements["DOC-001"]

    assert dnc.required_roles == (BusinessRole.PRESIDENT, BusinessRole.SIGNATAIRE)
    assert dnc.required_address_usages == (AddressUsage.ADRESSE_PERSONNELLE,)
    assert "personne.president.nom_pere" in dnc.required_canonical_fields
    assert "personne.president.nom_mere" in dnc.required_canonical_fields
    assert "personne.president.nationalite" in dnc.required_canonical_fields
    assert "personne.president.adresse_personnelle" in dnc.required_canonical_fields
    assert "signature.lieu" in dnc.required_canonical_fields
    assert "signature.date" in dnc.required_canonical_fields
    assert "personne.president.lieu_naissance" not in dnc.required_canonical_fields
    assert "selas_dnc_filiation_president" not in dnc.unresolved_ambiguity_keys
    assert BusinessRole.GERANT not in dnc.required_roles


def test_selas_dnc_readiness_blocks_missing_filiation() -> None:
    requirement = next(
        requirement
        for requirement in build_selas_front_schema().candidate_document_requirements
        if requirement.doc_code == "DOC-001"
    )
    dossier = DossierRecord(id="selas-dnc-president")
    dossier.add_person(PersonRecord(id="person-president", prenom="Alice", nom="Martin"))
    dossier.add_address(
        AddressRecord(
            id="address-president",
            usage=AddressUsage.ADRESSE_PERSONNELLE,
            display_value="12 rue des Lilas, 75008 Paris",
            display_source=AddressDisplaySource.MANUAL,
            owner_object_type=FrontObjectType.PERSON,
            owner_object_id="person-president",
        )
    )
    assign_explicit_role(dossier, BusinessRole.PRESIDENT, "person-president")
    assign_explicit_role(
        dossier,
        BusinessRole.SIGNATAIRE,
        "person-president",
        scope=RoleScope.DOCUMENT,
        document_code="DOC-001",
    )
    for field_path in (
        "personne.president.genre",
        "personne.president.civilite_affichage",
        "personne.president.prenom",
        "personne.president.nom",
        "personne.president.date_naissance",
        "personne.president.nationalite",
        "personne.president.adresse_personnelle",
        "signature.lieu",
        "signature.date",
    ):
        dossier.add_canonical_value(CanonicalFieldValue(field_path=field_path, value="x"))

    issues = validate_document_requirement(dossier, requirement)

    assert {
        issue.field_path
        for issue in issues
        if issue.field_path is not None
    } == {"personne.president.nom_pere", "personne.president.nom_mere"}


def test_selas_doc002_requires_president_siege_and_explicit_reuse_rule() -> None:
    requirements = {
        requirement.doc_code: requirement
        for requirement in build_selas_front_schema().candidate_document_requirements
    }
    domiciliation = requirements["DOC-002"]

    assert domiciliation.required_roles == (
        BusinessRole.PRESIDENT,
        BusinessRole.SIGNATAIRE,
        BusinessRole.SOCIETE_PRINCIPALE,
    )
    assert domiciliation.required_address_usages == (
        AddressUsage.SIEGE_SOCIAL,
        AddressUsage.DOMICILIATION,
    )
    assert domiciliation.required_reuse_rules == (
        "address:siege_social -> address:domiciliation",
    )
    assert "personne.president.genre" in domiciliation.required_canonical_fields
    assert "personne.president.civilite_affichage" in (
        domiciliation.required_canonical_fields
    )
    assert "societe.societe_principale.capital_social" in (
        domiciliation.required_canonical_fields
    )
    assert "societe.societe_principale.siege.adresse.num_voie" in (
        domiciliation.required_canonical_fields
    )
    assert "signature.lieu" in domiciliation.required_canonical_fields
    assert "signature.date" in domiciliation.required_canonical_fields
    assert "domiciliation.adresse" not in domiciliation.required_canonical_fields
    assert "signature.*" not in domiciliation.required_canonical_fields
    assert domiciliation.status is DocumentRequirementStatus.EXPECTED
    assert BusinessRole.GERANT not in domiciliation.required_roles


def test_selas_doc002_blocks_distinct_domiciliation_without_reuse_rule() -> None:
    requirement = next(
        requirement
        for requirement in build_selas_front_schema().candidate_document_requirements
        if requirement.doc_code == "DOC-002"
    )
    dossier = _selas_doc002_dossier(manual_distinct_domiciliation=True)

    issues = validate_document_requirement(dossier, requirement)

    assert [
        issue.issue_type
        for issue in issues
    ] == [ValidationIssueType.MISSING_ADDRESS_REUSE_SOURCE]
    assert issues[0].source_ref == "address:siege_social"
    assert issues[0].target_ref == "address:domiciliation"


def test_selas_doc002_ready_with_explicit_siege_domiciliation_reuse() -> None:
    requirement = next(
        requirement
        for requirement in build_selas_front_schema().candidate_document_requirements
        if requirement.doc_code == "DOC-002"
    )
    dossier = _selas_doc002_dossier(active_domiciliation_reuse=True)

    assert validate_document_requirement(dossier, requirement) == ()


def test_selas_doc034_requires_order_mandataire_and_signature_fields() -> None:
    requirements = {
        requirement.doc_code: requirement
        for requirement in build_selas_front_schema().candidate_document_requirements
    }
    ordre = requirements["DOC-034"]

    assert ordre.required_roles == (
        BusinessRole.SIGNATAIRE,
        BusinessRole.MANDATAIRE,
        BusinessRole.SOCIETE_PRINCIPALE,
        BusinessRole.ORDRE_PROFESSIONNEL,
    )
    assert ordre.required_address_usages == (
        AddressUsage.ORDRE,
        AddressUsage.ADRESSE_PERSONNELLE,
    )
    assert {
        "personne.signataire.titre_affichage",
        "personne.signataire.prenom",
        "personne.signataire.nom",
        "personne.signataire.adresse_personnelle",
        "societe.societe_principale.denomination",
        "ordre.conseil_departemental_libelle",
        "ordre.destinataire_appel",
        "ordre.profession_signataire_affichee",
        "ordre.profession_ligne_destinataire",
        "ordre.profession_reglementee_pluriel",
        "ordre.adresse.ligne_1",
        "ordre.adresse.cp",
        "ordre.adresse.ville",
        "mandataire.civilite_affichage",
        "mandataire.prenom",
        "mandataire.nom",
        "mandataire.fonction",
        "mandataire.cabinet",
        "signature.lieu",
        "signature.date",
        "dossier.options.derogation",
    }.issubset(set(ordre.required_canonical_fields))
    assert "mandataire_configurable" not in ordre.unresolved_ambiguity_keys
    assert "selas_ordre_pieces_plans_devis" in ordre.unresolved_ambiguity_keys
    assert BusinessRole.PRESIDENT not in ordre.required_roles
    assert BusinessRole.GERANT not in ordre.required_roles


def test_selas_doc003_and_doc018_are_no_longer_waiting_for_old_readiness_locks() -> None:
    requirements = {
        requirement.doc_code: requirement
        for requirement in build_selas_front_schema().candidate_document_requirements
    }

    procuration = requirements["DOC-003"]
    statuts = requirements["DOC-018"]

    assert procuration.unresolved_ambiguity_keys == ()
    assert statuts.unresolved_ambiguity_keys == ()
    assert {
        "societe.societe_principale.forme_sociale_complete",
        "capital.type_titre",
        "capital.actions.nombre_total",
        "capital.actions.valeur_nominale",
        "capital.actions.repartition_actionnaires",
        "banque_depot.nom",
        "ordre.numero_rpps",
        "signature.prestataire_signature_electronique",
    }.issubset(set(statuts.required_canonical_fields))
    assert "selas_actions_numbering" not in statuts.unresolved_ambiguity_keys
    assert "selas_capital_attestation" not in statuts.unresolved_ambiguity_keys


def test_selas_regime_communautaire_adds_doc005_and_doc006_candidates() -> None:
    schema = build_selas_front_schema(regime_communautaire=True)
    requirements = {
        requirement.doc_code: requirement
        for requirement in schema.candidate_document_requirements
    }

    assert "DOC-005" in schema.candidate_document_codes
    assert "DOC-006" in schema.candidate_document_codes
    assert schema.pack_readiness.active_conditional_document_codes == (
        "DOC-005",
        "DOC-006",
    )
    assert schema.pack_readiness.active_pack_document_codes == (
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-034",
        "DOC-018",
        "DOC-005",
        "DOC-006",
    )
    assert "DOC-006" not in schema.reserved_document_codes
    assert requirements["DOC-005"].status is DocumentRequirementStatus.CONTEXT_INCOMPLETE
    assert requirements["DOC-006"].status is DocumentRequirementStatus.CONTEXT_INCOMPLETE
    assert BusinessRole.CONJOINT in requirements["DOC-005"].required_roles
    assert BusinessRole.CONJOINT in requirements["DOC-006"].required_roles
    assert BusinessRole.GERANT not in requirements["DOC-005"].required_roles
    assert BusinessRole.GERANT not in requirements["DOC-006"].required_roles
    assert "dossier.options.regime_communautaire" in (
        requirements["DOC-005"].required_canonical_fields
    )
    assert "regime_communautaire.qualite_renoncee" in (
        requirements["DOC-005"].required_canonical_fields
    )
    assert "societe.societe_principale.forme_sociale_abregee" in (
        requirements["DOC-006"].required_canonical_fields
    )
    assert "personne.conjoint.adresse.cp" in (
        requirements["DOC-006"].required_canonical_fields
    )


def test_selas_flow_blocks_readiness_without_creating_generation() -> None:
    dossier = build_selas_schema_dossier()
    flow = build_selas_front_schema().flow
    generation = flow.validation_for_block(DossierBlockId.GENERATION_READINESS)

    assert dossier.metadata["generation_enabled"] is False
    assert generation.status is FlowStatus.BLOCKED
    assert BusinessRole.ACTIONNAIRE in generation.missing_roles
    assert BusinessRole.PRESIDENT in generation.missing_roles
    assert "capital.actions.nombre_total" in generation.missing_canonical_fields
    assert "selas_actions_numbering" not in generation.unresolved_ambiguity_keys
    assert "selas_capital_attestation" not in generation.unresolved_ambiguity_keys
    assert "selas_statuts_medecin_source_lock" not in (
        generation.unresolved_ambiguity_keys
    )


def test_praticien_reuse_is_explicit_for_selas_actionnaire_and_president() -> None:
    dossier = DossierRecord(id="selas-person-reuse")
    dossier.add_person(PersonRecord(id="person-praticien", prenom="Alice", nom="Martin"))

    assert is_role_reuse_allowed(BusinessRole.PRATICIEN, BusinessRole.ACTIONNAIRE)
    assert is_role_reuse_allowed(BusinessRole.PRATICIEN, BusinessRole.PRESIDENT)

    assign_explicit_role(dossier, BusinessRole.PRATICIEN, "person-praticien")
    assign_explicit_role(
        dossier,
        BusinessRole.ACTIONNAIRE,
        "person-praticien",
        target_type=RoleTargetType.PERSON,
        scope=RoleScope.OPERATION,
    )
    assign_explicit_role(dossier, BusinessRole.PRESIDENT, "person-praticien")
    assign_explicit_role(
        dossier,
        BusinessRole.SIGNATAIRE,
        "person-praticien",
        scope=RoleScope.DOCUMENT,
        document_code="DOC-018",
    )

    assert validate_role_assignments(dossier) == ()


def _selas_doc002_dossier(
    *,
    active_domiciliation_reuse: bool = False,
    manual_distinct_domiciliation: bool = False,
) -> DossierRecord:
    dossier = DossierRecord(id="selas-doc002-domiciliation")
    dossier.add_person(PersonRecord(id="person-president", prenom="Alice", nom="Martin"))
    dossier.add_company(
        CompanyRecord(
            id="company-selas",
            denomination="MARTIN MEDECINE",
            forme_sociale="SELAS",
            capital_social="1 000",
        )
    )
    dossier.add_address(
        AddressRecord(
            id="address-siege",
            usage=AddressUsage.SIEGE_SOCIAL,
            display_value="10 rue du Siege, 75008 Paris",
            display_source=AddressDisplaySource.MANUAL,
            owner_object_type=FrontObjectType.COMPANY,
            owner_object_id="company-selas",
        )
    )
    if manual_distinct_domiciliation:
        dossier.add_address(
            AddressRecord(
                id="address-domiciliation-distincte",
                usage=AddressUsage.DOMICILIATION,
                display_value="44 avenue Distincte, 75009 Paris",
                display_source=AddressDisplaySource.MANUAL,
                owner_object_type=FrontObjectType.COMPANY,
                owner_object_id="company-selas",
            )
        )
    if active_domiciliation_reuse:
        dossier.add_reuse_rule(
            ReuseRuleState(
                id="reuse-siege-domiciliation",
                source_ref=address_ref(AddressUsage.SIEGE_SOCIAL),
                target_ref=address_ref(AddressUsage.DOMICILIATION),
                relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
                status=ReuseRuleStatus.ACTIVE,
            )
        )
    assign_explicit_role(dossier, BusinessRole.PRESIDENT, "person-president")
    assign_explicit_role(
        dossier,
        BusinessRole.SIGNATAIRE,
        "person-president",
        scope=RoleScope.DOCUMENT,
        document_code="DOC-002",
    )
    assign_explicit_role(
        dossier,
        BusinessRole.SOCIETE_PRINCIPALE,
        "company-selas",
        target_type=RoleTargetType.COMPANY,
    )
    for field_path in (
        "personne.president.genre",
        "personne.president.civilite_affichage",
        "personne.president.prenom",
        "personne.president.nom",
        "societe.societe_principale.denomination",
        "societe.societe_principale.capital_social",
        "societe.societe_principale.siege.adresse.num_voie",
        "societe.societe_principale.siege.adresse.voie",
        "societe.societe_principale.siege.adresse.cp",
        "societe.societe_principale.siege.adresse.ville",
        "signature.lieu",
        "signature.date",
    ):
        dossier.add_canonical_value(CanonicalFieldValue(field_path=field_path, value="x"))
    return dossier
