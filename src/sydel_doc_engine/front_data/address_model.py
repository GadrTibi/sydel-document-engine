from __future__ import annotations

from dataclasses import dataclass

from sydel_doc_engine.front_data.models import (
    AddressDisplaySource,
    AddressRecord,
    AddressUsage,
    CanonicalRelationType,
    FrontObjectType,
)


@dataclass(frozen=True)
class AddressUsageDefinition:
    usage: AddressUsage
    label: str
    allowed_owner_types: frozenset[FrontObjectType] = frozenset()
    notes: str = ""


@dataclass(frozen=True)
class AddressReusePolicy:
    source_usage: AddressUsage
    target_usage: AddressUsage
    relation_type: CanonicalRelationType
    label: str
    requires_explicit_rule: bool = True
    standard_rule: bool = False
    allow_override: bool = True
    notes: str = ""


PERSON_OWNER = frozenset({FrontObjectType.PERSON})
COMPANY_OWNER = frozenset({FrontObjectType.COMPANY})
PERSON_OR_COMPANY_OWNER = frozenset({FrontObjectType.PERSON, FrontObjectType.COMPANY})
COMPANY_OR_DOSSIER_OWNER = frozenset({FrontObjectType.COMPANY, FrontObjectType.DOSSIER})
OPERATION_OWNER = frozenset({FrontObjectType.OPERATION})


ADDRESS_USAGE_DEFINITIONS: dict[AddressUsage, AddressUsageDefinition] = {
    AddressUsage.DOMICILE_PRATICIEN: AddressUsageDefinition(
        usage=AddressUsage.DOMICILE_PRATICIEN,
        label="Domicile du praticien",
        allowed_owner_types=PERSON_OWNER,
        notes="Adresse personnelle pivot du praticien ; distincte du siege et du cabinet.",
    ),
    AddressUsage.DOMICILE_CEDANT: AddressUsageDefinition(
        usage=AddressUsage.DOMICILE_CEDANT,
        label="Domicile du cedant",
        allowed_owner_types=PERSON_OWNER,
        notes="Adresse du vendeur/cedant personne physique dans une cession.",
    ),
    AddressUsage.ADRESSE_PERSONNELLE: AddressUsageDefinition(
        usage=AddressUsage.ADRESSE_PERSONNELLE,
        label="Adresse personnelle",
        allowed_owner_types=PERSON_OWNER,
        notes="Adresse personnelle rolee ; ne remplace pas automatiquement le domicile praticien.",
    ),
    AddressUsage.LIEU_EXERCICE: AddressUsageDefinition(
        usage=AddressUsage.LIEU_EXERCICE,
        label="Lieu d'exercice",
        allowed_owner_types=OPERATION_OWNER,
        notes="Adresse du cabinet ou du lieu principal d'exercice.",
    ),
    AddressUsage.SIEGE_SOCIAL: AddressUsageDefinition(
        usage=AddressUsage.SIEGE_SOCIAL,
        label="Siege social",
        allowed_owner_types=COMPANY_OWNER,
        notes="Siege de la societe rolee ; jamais deduit du lieu d'exercice sans option.",
    ),
    AddressUsage.DOMICILIATION: AddressUsageDefinition(
        usage=AddressUsage.DOMICILIATION,
        label="Domiciliation",
        allowed_owner_types=COMPANY_OR_DOSSIER_OWNER,
        notes="Forme documentaire du siege social, representee par une regle explicite.",
    ),
    AddressUsage.CABINET_CEDE: AddressUsageDefinition(
        usage=AddressUsage.CABINET_CEDE,
        label="Cabinet cede",
        allowed_owner_types=OPERATION_OWNER,
        notes="Adresse du cabinet objet de la cession.",
    ),
    AddressUsage.LOCAUX_LOUES: AddressUsageDefinition(
        usage=AddressUsage.LOCAUX_LOUES,
        label="Locaux loues",
        allowed_owner_types=OPERATION_OWNER,
        notes="Adresse des locaux du bail ; distincte du cabinet par defaut.",
    ),
    AddressUsage.BAILLEUR: AddressUsageDefinition(
        usage=AddressUsage.BAILLEUR,
        label="Adresse du bailleur",
        allowed_owner_types=PERSON_OR_COMPANY_OWNER,
        notes="Adresse de la partie bailleur, sans deduction depuis le vendeur.",
    ),
    AddressUsage.LOCATAIRE: AddressUsageDefinition(
        usage=AddressUsage.LOCATAIRE,
        label="Adresse du locataire",
        allowed_owner_types=PERSON_OR_COMPANY_OWNER,
        notes="Adresse de la partie locataire, sans deduction depuis la SEL.",
    ),
    AddressUsage.BANQUE: AddressUsageDefinition(
        usage=AddressUsage.BANQUE,
        label="Adresse de banque",
        allowed_owner_types=COMPANY_OWNER,
        notes="Adresse de la banque ou du depositaire, parametrable avec override.",
    ),
    AddressUsage.ORDRE: AddressUsageDefinition(
        usage=AddressUsage.ORDRE,
        label="Adresse du conseil de l'ordre",
        allowed_owner_types=COMPANY_OWNER,
        notes="Adresse de l'institution ordinale, distincte de l'inscrit.",
    ),
    AddressUsage.SCM: AddressUsageDefinition(
        usage=AddressUsage.SCM,
        label="Adresse SCM",
        allowed_owner_types=COMPANY_OWNER,
        notes="Adresse de la SCM standard ; peut reutiliser le lieu d'exercice via regle tracee.",
    ),
    AddressUsage.SCM_CEDEE: AddressUsageDefinition(
        usage=AddressUsage.SCM_CEDEE,
        label="Adresse SCM cedee",
        allowed_owner_types=COMPANY_OWNER,
        notes="Adresse de la SCM dont les parts sont cedees.",
    ),
    AddressUsage.CESSIONNAIRE_SCM: AddressUsageDefinition(
        usage=AddressUsage.CESSIONNAIRE_SCM,
        label="Adresse du cessionnaire SCM",
        allowed_owner_types=COMPANY_OWNER,
        notes="Adresse de la societe cessionnaire ; distincte de la SCM cedee par defaut.",
    ),
    AddressUsage.SPFPL: AddressUsageDefinition(
        usage=AddressUsage.SPFPL,
        label="Adresse SPFPL",
        allowed_owner_types=COMPANY_OWNER,
        notes="Siege ou adresse de la SPFPL beneficiaire.",
    ),
    AddressUsage.SOCIETE_CIBLE: AddressUsageDefinition(
        usage=AddressUsage.SOCIETE_CIBLE,
        label="Adresse societe cible",
        allowed_owner_types=COMPANY_OWNER,
        notes="Siege de la societe cible ou apportee.",
    ),
}


ADDRESS_REUSE_POLICIES: dict[tuple[AddressUsage, AddressUsage], AddressReusePolicy] = {
    (AddressUsage.SIEGE_SOCIAL, AddressUsage.DOMICILIATION): AddressReusePolicy(
        source_usage=AddressUsage.SIEGE_SOCIAL,
        target_usage=AddressUsage.DOMICILIATION,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        label="domiciliation_is_registered_office",
        standard_rule=True,
        notes="Albane confirme que la domiciliation est toujours le siege social.",
    ),
    (AddressUsage.LIEU_EXERCICE, AddressUsage.SIEGE_SOCIAL): AddressReusePolicy(
        source_usage=AddressUsage.LIEU_EXERCICE,
        target_usage=AddressUsage.SIEGE_SOCIAL,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        label="registered_office_is_exercise_place",
        notes="Option explicite seulement ; pas de fusion automatique.",
    ),
    (AddressUsage.LIEU_EXERCICE, AddressUsage.SCM): AddressReusePolicy(
        source_usage=AddressUsage.LIEU_EXERCICE,
        target_usage=AddressUsage.SCM,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        label="scm_address_is_exercise_place_standard",
        standard_rule=True,
        notes="Regle standard documentee par Albane, mais toujours tracee.",
    ),
    (AddressUsage.LIEU_EXERCICE, AddressUsage.CABINET_CEDE): AddressReusePolicy(
        source_usage=AddressUsage.LIEU_EXERCICE,
        target_usage=AddressUsage.CABINET_CEDE,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        label="transferred_cabinet_is_exercise_place",
        standard_rule=True,
        notes="Cas frequent dans les cessions, confirme par option de dossier.",
    ),
    (AddressUsage.LIEU_EXERCICE, AddressUsage.LOCAUX_LOUES): AddressReusePolicy(
        source_usage=AddressUsage.LIEU_EXERCICE,
        target_usage=AddressUsage.LOCAUX_LOUES,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        label="leased_premises_are_exercise_place",
        standard_rule=True,
        notes="Cas standard possible ; le bail reste distinct.",
    ),
    (AddressUsage.DOMICILE_PRATICIEN, AddressUsage.DOMICILE_CEDANT): AddressReusePolicy(
        source_usage=AddressUsage.DOMICILE_PRATICIEN,
        target_usage=AddressUsage.DOMICILE_CEDANT,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        label="practitioner_home_is_seller_home",
        standard_rule=True,
        notes="Parcours SELARL standard : vendeur/cedant = praticien BNC.",
    ),
    (AddressUsage.SCM_CEDEE, AddressUsage.CESSIONNAIRE_SCM): AddressReusePolicy(
        source_usage=AddressUsage.SCM_CEDEE,
        target_usage=AddressUsage.CESSIONNAIRE_SCM,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
        label="scm_sold_address_reused_for_scm_buyer",
        notes="Possible seulement apres confirmation ; distinct par defaut.",
    ),
}


def address_usage_definition(usage: AddressUsage) -> AddressUsageDefinition:
    return ADDRESS_USAGE_DEFINITIONS[usage]


def address_reuse_policy(
    source_usage: AddressUsage,
    target_usage: AddressUsage,
) -> AddressReusePolicy | None:
    return ADDRESS_REUSE_POLICIES.get((source_usage, target_usage))


def is_address_reuse_allowed(source_usage: AddressUsage, target_usage: AddressUsage) -> bool:
    if source_usage is target_usage:
        return True
    return address_reuse_policy(source_usage, target_usage) is not None


def parse_address_ref(ref: str) -> AddressUsage | None:
    if not ref.startswith("address:"):
        return None
    try:
        return AddressUsage(ref.removeprefix("address:"))
    except ValueError:
        return None


def has_decomposed_components(address: AddressRecord) -> bool:
    return any(
        (
            address.street_number,
            address.street_name,
            address.postal_code,
            address.city,
        )
    )


def compose_address_display(address: AddressRecord) -> str | None:
    street = " ".join(
        part for part in (address.street_number, address.street_name) if part
    ).strip()
    city_line = " ".join(part for part in (address.postal_code, address.city) if part).strip()
    parts = [part for part in (street, city_line) if part]
    if address.country and address.country != "France":
        parts.append(address.country)
    if not parts:
        return None
    return ", ".join(parts)


def address_display_value(address: AddressRecord) -> str | None:
    if address.display_value:
        return address.display_value
    return compose_address_display(address)


def is_display_derived_from_components(address: AddressRecord) -> bool:
    return address.display_source is AddressDisplaySource.COMPONENTS or (
        not address.display_value and has_decomposed_components(address)
    )
