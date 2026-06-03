from __future__ import annotations

from dataclasses import dataclass

from sydel_doc_engine.front_data.models import AddressUsage, BusinessRole, OperationType


@dataclass(frozen=True)
class FrontDataTestPrefillProfile:
    key: str
    case_type: str
    purpose: str
    expected_generable_doc_codes: tuple[str, ...]
    expected_reserve_doc_codes: tuple[str, ...] = ()
    expected_manual_doc_codes: tuple[str, ...] = ()
    orange_doc_codes: tuple[str, ...] = ()
    required_roles: tuple[BusinessRole, ...] = ()
    required_address_usages: tuple[AddressUsage, ...] = ()
    operation_types: tuple[OperationType, ...] = ()
    explicit_reuse_refs: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def status_document_codes(self) -> tuple[str, ...]:
        return tuple(
            dict.fromkeys(
                (
                    *self.expected_generable_doc_codes,
                    *self.expected_reserve_doc_codes,
                    *self.expected_manual_doc_codes,
                    *self.orange_doc_codes,
                )
            )
        )


SELARL_SIMPLE_PROFILE = FrontDataTestPrefillProfile(
    key="selarl_medecin_unipersonnelle_simple",
    case_type="SELARL",
    purpose="Happy path for DOC-001 to DOC-004 with one practitioner reused by explicit roles.",
    expected_generable_doc_codes=("DOC-001", "DOC-002", "DOC-003", "DOC-004"),
    required_roles=(
        BusinessRole.PRATICIEN,
        BusinessRole.ASSOCIE,
        BusinessRole.GERANT,
        BusinessRole.SIGNATAIRE,
        BusinessRole.SOCIETE_PRINCIPALE,
    ),
    required_address_usages=(
        AddressUsage.ADRESSE_PERSONNELLE,
        AddressUsage.SIEGE_SOCIAL,
        AddressUsage.DOMICILIATION,
        AddressUsage.LIEU_EXERCICE,
    ),
    operation_types=(OperationType.CREATION,),
    explicit_reuse_refs=(
        "role:praticien -> role:associe",
        "role:praticien -> role:gerant",
        "role:praticien -> role:signataire",
        "address:siege_social -> address:domiciliation",
    ),
)


SELARL_DENTISTE_PROFILE = FrontDataTestPrefillProfile(
    key="selarl_dentiste_regime_site",
    case_type="SELARL",
    purpose="Regime communautaire, site distinct and derogation visibility checks.",
    expected_generable_doc_codes=(
        "DOC-001",
        "DOC-002",
        "DOC-003",
        "DOC-004",
        "DOC-005",
        "DOC-006",
    ),
    expected_manual_doc_codes=("DOC-013", "DOC-014"),
    required_roles=SELARL_SIMPLE_PROFILE.required_roles,
    required_address_usages=SELARL_SIMPLE_PROFILE.required_address_usages,
    operation_types=(
        OperationType.CREATION,
        OperationType.REGIME_COMMUNAUTAIRE,
        OperationType.DEROGATION,
    ),
    explicit_reuse_refs=SELARL_SIMPLE_PROFILE.explicit_reuse_refs,
    notes=(
        "DOC-006 is generated with DOC-005 when the community property regime is active.",
        "DOC-013 and DOC-014 stay manual/non-generated.",
    ),
)


SELARL_CESSION_PROFILE = FrontDataTestPrefillProfile(
    key="selarl_medecin_cession_bail_financement",
    case_type="SELARL",
    purpose="Complex conditional blocks for cession, bail and financing.",
    expected_generable_doc_codes=("DOC-001", "DOC-002", "DOC-003", "DOC-004"),
    orange_doc_codes=("DOC-009",),
    required_roles=(
        *SELARL_SIMPLE_PROFILE.required_roles,
        BusinessRole.VENDEUR,
        BusinessRole.ACQUEREUR,
        BusinessRole.REPRESENTANT_PERSONNE_MORALE,
        BusinessRole.BAILLEUR,
        BusinessRole.LOCATAIRE,
        BusinessRole.CONJOINT,
        BusinessRole.BANQUE,
    ),
    required_address_usages=(
        *SELARL_SIMPLE_PROFILE.required_address_usages,
        AddressUsage.DOMICILE_CEDANT,
        AddressUsage.CABINET_CEDE,
        AddressUsage.LOCAUX_LOUES,
        AddressUsage.BAILLEUR,
        AddressUsage.LOCATAIRE,
        AddressUsage.BANQUE,
    ),
    operation_types=(
        OperationType.CREATION,
        OperationType.CESSION,
        OperationType.BAIL,
        OperationType.FINANCEMENT,
    ),
    explicit_reuse_refs=(
        *SELARL_SIMPLE_PROFILE.explicit_reuse_refs,
        "address:lieu_exercice -> address:cabinet_cede",
        "address:lieu_exercice -> address:locaux_loues",
    ),
    notes=(
        "DOC-009 remains orange: the prefill localizes cession/bail/financing data "
        "without pretending the global cession model is fully rebuilt.",
    ),
)


SCI_SIMPLE_PROFILE = FrontDataTestPrefillProfile(
    key="sci_simple",
    case_type="SCI",
    purpose="Legacy SCI happy path kept as a non-regression scenario.",
    expected_generable_doc_codes=("DOC-001", "DOC-003", "DOC-004"),
    orange_doc_codes=("DOC-002",),
    required_roles=(
        BusinessRole.ASSOCIE,
        BusinessRole.GERANT,
        BusinessRole.SIGNATAIRE,
        BusinessRole.SOCIETE_PRINCIPALE,
    ),
    required_address_usages=(
        AddressUsage.ADRESSE_PERSONNELLE,
        AddressUsage.SIEGE_SOCIAL,
        AddressUsage.DOMICILIATION,
    ),
    operation_types=(OperationType.CREATION,),
    explicit_reuse_refs=("address:siege_social -> address:domiciliation",),
    notes=(
        "The legacy business wizard can generate DOC-002 for SCI, while the "
        "current unit front_data requirement for DOC-002 is SEL-oriented and "
        "still asks for a praticien role.",
    ),
)


FRONT_DATA_TEST_PREFILL_PROFILES: dict[str, FrontDataTestPrefillProfile] = {
    profile.key: profile
    for profile in (
        SELARL_SIMPLE_PROFILE,
        SELARL_DENTISTE_PROFILE,
        SELARL_CESSION_PROFILE,
        SCI_SIMPLE_PROFILE,
    )
}


def front_data_test_prefill_profiles() -> tuple[FrontDataTestPrefillProfile, ...]:
    return tuple(FRONT_DATA_TEST_PREFILL_PROFILES.values())


def front_data_test_prefill_profile(key: str) -> FrontDataTestPrefillProfile:
    try:
        return FRONT_DATA_TEST_PREFILL_PROFILES[key]
    except KeyError as exc:
        raise KeyError(f"Unknown front_data test prefill profile: {key}") from exc
