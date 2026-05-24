from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Final

from sydel_doc_engine.app.front_dossier_editor import (
    FrontDossierEditorView,
    build_front_dossier_editor_dossier,
    front_dossier_editor_profile,
)
from sydel_doc_engine.front_data.address_model import address_display_value
from sydel_doc_engine.front_data.document_status import build_document_status_summary
from sydel_doc_engine.front_data.dossier_flow import build_dossier_flow
from sydel_doc_engine.front_data.models import (
    AddressDisplaySource,
    AddressRecord,
    AddressUsage,
    BusinessRole,
    CanonicalFieldValue,
    CanonicalRelationType,
    CompanyRecord,
    DossierRecord,
    FieldFormKind,
    FrontObjectType,
    PersonRecord,
    ReuseRuleKind,
    ReuseRuleState,
    ReuseRuleStatus,
    RoleScope,
    RoleTargetType,
    address_ref,
)
from sydel_doc_engine.front_data.role_model import assign_explicit_role, role_ref

SELARL_CREATION_SIMPLE_PROFILE_KEY: Final = "selarl_creation_simple"
SUPPORTED_ENTRY_PROFILE_KEYS: Final[tuple[str, ...]] = (
    SELARL_CREATION_SIMPLE_PROFILE_KEY,
)

PERSON_MAIN_ID: Final = "person-praticien-principal"
COMPANY_MAIN_ID: Final = "company-societe-principale"
PERSONAL_ADDRESS_ID: Final = "address-adresse-personnelle"
REGISTERED_OFFICE_ADDRESS_ID: Final = "address-siege-social"
DOMICILIATION_ADDRESS_ID: Final = "address-domiciliation"
DOMICILIATION_REUSE_RULE_ID: Final = "reuse-address-siege-domiciliation"
ROLE_REUSE_RULE_PREFIX: Final = "reuse-role-praticien"


@dataclass(frozen=True)
class FrontDossierSimpleEntry:
    profile_key: str = SELARL_CREATION_SIMPLE_PROFILE_KEY
    dossier_unipersonnel: bool = True
    domiciliation_same_as_siege: bool = True
    civilite_affichage: str = ""
    genre: str = ""
    prenom: str = ""
    nom: str = ""
    fonction: str = "gerant"
    date_naissance: str = ""
    ville_naissance: str = ""
    departement_naissance: str = ""
    nationalite: str = ""
    nom_pere: str = ""
    nom_mere: str = ""
    adresse_personnelle: str = ""
    societe_denomination: str = ""
    societe_forme_sociale: str = "SELARL"
    societe_capital_social: str = ""
    societe_ville_rcs: str = ""
    siege_social: str = ""
    domiciliation: str = ""
    capital_titres_nombre_total: str = ""
    capital_titres_valeur_nominale: str = ""
    capital_repartition_associes: str = ""
    decision_date: str = ""
    reunion_date_lettres: str = ""
    reunion_heure: str = ""
    signature_lieu: str = ""
    signature_date: str = ""
    signature_nombre_exemplaires: str = ""


def front_dossier_entry_is_supported(profile_key_or_label: str) -> bool:
    try:
        profile = front_dossier_editor_profile(profile_key_or_label)
    except KeyError:
        return False
    return profile.key in SUPPORTED_ENTRY_PROFILE_KEYS


def build_front_dossier_entry_dossier(
    entry: FrontDossierSimpleEntry,
) -> DossierRecord:
    profile = front_dossier_editor_profile(entry.profile_key)
    if profile.key not in SUPPORTED_ENTRY_PROFILE_KEYS:
        raise ValueError(f"Unsupported data-entry profile: {profile.key}")

    dossier = build_front_dossier_editor_dossier(profile)
    dossier.metadata.update(
        {
            "front_editor_v1": True,
            "front_data_entry_v1": True,
            "placeholder_values": False,
            "dossier_unipersonnel": entry.dossier_unipersonnel,
            "domiciliation_same_as_siege": entry.domiciliation_same_as_siege,
        }
    )

    person = _add_person_if_present(dossier, entry)
    company = _add_company_if_present(dossier, entry)

    if person:
        _assign_person_roles(dossier, person, entry)
        _add_person_address_if_present(dossier, person, entry)
        _add_person_canonical_values(dossier, person, entry)
    if company:
        _assign_company_roles(dossier, company)
        _add_company_addresses_if_present(dossier, company, entry)
        _add_company_canonical_values(dossier, company, entry)

    _add_capital_and_signature_values(dossier, entry)
    return dossier


def build_front_dossier_entry_view(
    entry: FrontDossierSimpleEntry,
) -> FrontDossierEditorView:
    profile = front_dossier_editor_profile(entry.profile_key)
    dossier = build_front_dossier_entry_dossier(entry)
    flow = build_dossier_flow(dossier)
    status_summary = build_document_status_summary(
        dossier,
        lot_id=f"front-entry-{profile.key}",
        lot_label=profile.label,
    )
    return FrontDossierEditorView(
        profile=profile,
        dossier=dossier,
        flow=flow,
        status_summary=status_summary,
    )


def front_dossier_entry_object_rows(
    dossier: DossierRecord,
) -> tuple[dict[str, str], ...]:
    return (
        {"objet": "PersonRecord", "nombre": str(len(dossier.persons))},
        {"objet": "CompanyRecord", "nombre": str(len(dossier.companies))},
        {"objet": "AddressRecord", "nombre": str(len(dossier.addresses))},
        {"objet": "RoleAssignment", "nombre": str(len(dossier.role_assignments))},
        {"objet": "CanonicalFieldValue", "nombre": str(len(dossier.canonical_values))},
        {
            "objet": "ReuseRuleState active",
            "nombre": str(sum(1 for rule in dossier.reuse_rules.values() if rule.is_active)),
        },
    )


def front_dossier_entry_role_rows(
    dossier: DossierRecord,
) -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "role": assignment.role.value,
            "cible": assignment.target_id,
            "type": assignment.target_type.value,
            "portee": assignment.scope.value,
            "source regle": assignment.source_rule_id or "-",
        }
        for assignment in dossier.role_assignments.values()
    )


def front_dossier_entry_address_rows(
    dossier: DossierRecord,
) -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "usage": address.usage.value,
            "adresse": address_display_value(address) or "-",
            "source": address.display_source.value if address.display_source else "-",
            "regle source": address.source_rule_id or address.display_source_rule_id or "-",
        }
        for address in dossier.addresses.values()
    )


def _add_person_if_present(
    dossier: DossierRecord,
    entry: FrontDossierSimpleEntry,
) -> PersonRecord | None:
    if not _has_any_value(
        entry.civilite_affichage,
        entry.genre,
        entry.prenom,
        entry.nom,
        entry.date_naissance,
        entry.ville_naissance,
        entry.departement_naissance,
        entry.nationalite,
        entry.nom_pere,
        entry.nom_mere,
        entry.adresse_personnelle,
    ):
        return None
    return dossier.add_person(
        PersonRecord(
            id=PERSON_MAIN_ID,
            civilite_affichage=_clean(entry.civilite_affichage),
            genre=_clean(entry.genre),
            prenom=_clean(entry.prenom),
            nom=_clean(entry.nom),
            fonction=_clean(entry.fonction),
            metadata={"front_entry_v1": True},
        )
    )


def _add_company_if_present(
    dossier: DossierRecord,
    entry: FrontDossierSimpleEntry,
) -> CompanyRecord | None:
    if not _has_any_value(
        entry.societe_denomination,
        entry.societe_capital_social,
        entry.societe_ville_rcs,
        entry.siege_social,
        entry.domiciliation if not entry.domiciliation_same_as_siege else "",
    ):
        return None
    return dossier.add_company(
        CompanyRecord(
            id=COMPANY_MAIN_ID,
            denomination=_clean(entry.societe_denomination) or "",
            forme_sociale=_clean(entry.societe_forme_sociale),
            capital_social=_clean(entry.societe_capital_social),
            rcs_ville=_clean(entry.societe_ville_rcs),
            metadata={"front_entry_v1": True},
        )
    )


def _assign_person_roles(
    dossier: DossierRecord,
    person: PersonRecord,
    entry: FrontDossierSimpleEntry,
) -> None:
    assign_explicit_role(
        dossier,
        BusinessRole.PRATICIEN,
        person.id,
        assignment_id="role-praticien-principal",
        scope=RoleScope.DOSSIER,
        notes="Personne principale saisie dans la tranche V1.",
    )
    if not entry.dossier_unipersonnel:
        return

    _add_role_reuse_rule(
        dossier,
        BusinessRole.PRATICIEN,
        BusinessRole.ASSOCIE,
        "dossier_unipersonnel",
    )
    _add_role_reuse_rule(
        dossier,
        BusinessRole.PRATICIEN,
        BusinessRole.GERANT,
        "dossier_unipersonnel",
    )
    _add_role_reuse_rule(
        dossier,
        BusinessRole.PRATICIEN,
        BusinessRole.SIGNATAIRE,
        "dossier_unipersonnel",
    )
    assign_explicit_role(
        dossier,
        BusinessRole.ASSOCIE,
        person.id,
        target_type=RoleTargetType.PERSON,
        assignment_id="role-associe-unique",
        scope=RoleScope.OPERATION,
        scope_id="operation-creation",
        source_rule_id=_role_reuse_rule_id(BusinessRole.ASSOCIE),
        notes="Dossier unipersonnel : associe unique pointe vers le praticien.",
    )
    assign_explicit_role(
        dossier,
        BusinessRole.GERANT,
        person.id,
        assignment_id="role-gerant-principal",
        scope=RoleScope.DOSSIER,
        source_rule_id=_role_reuse_rule_id(BusinessRole.GERANT),
        notes="Dossier unipersonnel : gerant pointe vers le praticien.",
    )
    assign_explicit_role(
        dossier,
        BusinessRole.SIGNATAIRE,
        person.id,
        assignment_id="role-signataire-lot-v1",
        scope=RoleScope.LOT,
        scope_id="lot-documents-v1",
        source_rule_id=_role_reuse_rule_id(BusinessRole.SIGNATAIRE),
        notes="Dossier unipersonnel : signataire du lot V1 pointe vers le praticien.",
    )


def _assign_company_roles(dossier: DossierRecord, company: CompanyRecord) -> None:
    assign_explicit_role(
        dossier,
        BusinessRole.SOCIETE_PRINCIPALE,
        company.id,
        assignment_id="role-societe-principale",
        scope=RoleScope.DOSSIER,
        notes="Societe principale saisie dans la tranche V1.",
    )


def _add_person_address_if_present(
    dossier: DossierRecord,
    person: PersonRecord,
    entry: FrontDossierSimpleEntry,
) -> None:
    if not _clean(entry.adresse_personnelle):
        return
    dossier.add_address(
        AddressRecord(
            id=PERSONAL_ADDRESS_ID,
            usage=AddressUsage.ADRESSE_PERSONNELLE,
            display_value=_clean(entry.adresse_personnelle),
            display_source=AddressDisplaySource.MANUAL,
            owner_object_type=FrontObjectType.PERSON,
            owner_object_id=person.id,
            metadata={"front_entry_v1": True},
        )
    )


def _add_company_addresses_if_present(
    dossier: DossierRecord,
    company: CompanyRecord,
    entry: FrontDossierSimpleEntry,
) -> None:
    siege_value = _clean(entry.siege_social)
    if siege_value:
        dossier.add_address(
            AddressRecord(
                id=REGISTERED_OFFICE_ADDRESS_ID,
                usage=AddressUsage.SIEGE_SOCIAL,
                display_value=siege_value,
                display_source=AddressDisplaySource.MANUAL,
                owner_object_type=FrontObjectType.COMPANY,
                owner_object_id=company.id,
                metadata={"front_entry_v1": True},
            )
        )

    if entry.domiciliation_same_as_siege and siege_value:
        _add_domiciliation_reuse_rule(dossier)
        dossier.add_address(
            AddressRecord(
                id=DOMICILIATION_ADDRESS_ID,
                usage=AddressUsage.DOMICILIATION,
                display_value=siege_value,
                display_source=AddressDisplaySource.REUSE_RULE,
                display_source_rule_id=DOMICILIATION_REUSE_RULE_ID,
                owner_object_type=FrontObjectType.COMPANY,
                owner_object_id=company.id,
                source_address_id=REGISTERED_OFFICE_ADDRESS_ID,
                source_rule_id=DOMICILIATION_REUSE_RULE_ID,
                metadata={"front_entry_v1": True},
            )
        )
        return

    domiciliation_value = _clean(entry.domiciliation)
    if domiciliation_value:
        dossier.add_address(
            AddressRecord(
                id=DOMICILIATION_ADDRESS_ID,
                usage=AddressUsage.DOMICILIATION,
                display_value=domiciliation_value,
                display_source=AddressDisplaySource.MANUAL,
                owner_object_type=FrontObjectType.COMPANY,
                owner_object_id=company.id,
                metadata={"front_entry_v1": True},
            )
        )


def _add_person_canonical_values(
    dossier: DossierRecord,
    person: PersonRecord,
    entry: FrontDossierSimpleEntry,
) -> None:
    roles = [BusinessRole.PRATICIEN]
    if entry.dossier_unipersonnel:
        roles.extend(
            (
                BusinessRole.ASSOCIE,
                BusinessRole.GERANT,
                BusinessRole.SIGNATAIRE,
            )
        )
    for role in roles:
        role_path = role.value
        values = {
            "genre": entry.genre,
            "civilite_affichage": entry.civilite_affichage,
            "prenom": entry.prenom,
            "nom": entry.nom,
            "fonction": entry.fonction,
            "date_naissance": entry.date_naissance,
            "ville_naissance": entry.ville_naissance,
            "departement_naissance": entry.departement_naissance,
            "nationalite": entry.nationalite,
            "nom_pere": entry.nom_pere,
            "nom_mere": entry.nom_mere,
            "adresse_personnelle": entry.adresse_personnelle,
        }
        for suffix, value in values.items():
            _add_canonical_value(
                dossier,
                f"personne.{role_path}.{suffix}",
                value,
                owner_object_type=FrontObjectType.PERSON,
                owner_object_id=person.id,
            )


def _add_company_canonical_values(
    dossier: DossierRecord,
    company: CompanyRecord,
    entry: FrontDossierSimpleEntry,
) -> None:
    company_values = {
        "societe.societe_principale.denomination": entry.societe_denomination,
        "societe.societe_principale.forme_sociale": entry.societe_forme_sociale,
        "societe.societe_principale.capital_social": entry.societe_capital_social,
        "societe.societe_principale.rcs.ville": entry.societe_ville_rcs,
        "societe.societe_principale.siege.adresse": entry.siege_social,
        "forme_sociale": entry.societe_forme_sociale,
        "capital_social": entry.societe_capital_social,
    }
    for field_path, value in company_values.items():
        _add_canonical_value(
            dossier,
            field_path,
            value,
            owner_object_type=FrontObjectType.COMPANY,
            owner_object_id=company.id,
        )

    domiciliation_value = (
        entry.siege_social if entry.domiciliation_same_as_siege else entry.domiciliation
    )
    _add_canonical_value(
        dossier,
        "domiciliation.adresse",
        domiciliation_value,
        owner_object_type=FrontObjectType.ADDRESS,
        owner_object_id=DOMICILIATION_ADDRESS_ID,
        relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
    )


def _add_capital_and_signature_values(
    dossier: DossierRecord,
    entry: FrontDossierSimpleEntry,
) -> None:
    repartition = _capital_repartition_value(entry)
    values = {
        "capital.titres.nombre_total": entry.capital_titres_nombre_total,
        "capital.titres.valeur_nominale": entry.capital_titres_valeur_nominale,
        "capital.repartition_associes": repartition,
        "decision.date": entry.decision_date,
        "reunion.date_lettres": entry.reunion_date_lettres,
        "reunion.heure": entry.reunion_heure,
        "signature.lieu": entry.signature_lieu,
        "signature.date": entry.signature_date,
        "signature.nombre_exemplaires": entry.signature_nombre_exemplaires,
    }
    for field_path, value in values.items():
        _add_canonical_value(
            dossier,
            field_path,
            value,
            owner_object_type=FrontObjectType.DOSSIER,
            owner_object_id=dossier.id,
        )


def _add_canonical_value(
    dossier: DossierRecord,
    field_path: str,
    value: Any,
    *,
    owner_object_type: FrontObjectType,
    owner_object_id: str,
    relation_type: CanonicalRelationType = CanonicalRelationType.SAME_FIELD,
    form_kind: FieldFormKind = FieldFormKind.BUSINESS,
) -> None:
    cleaned = _clean(value)
    if cleaned == "":
        return
    dossier.add_canonical_value(
        CanonicalFieldValue(
            field_path=field_path,
            value=cleaned,
            owner_object_type=owner_object_type,
            owner_object_id=owner_object_id,
            relation_type=relation_type,
            form_kind=form_kind,
        )
    )


def _add_domiciliation_reuse_rule(dossier: DossierRecord) -> None:
    if DOMICILIATION_REUSE_RULE_ID in dossier.reuse_rules:
        return
    dossier.add_reuse_rule(
        ReuseRuleState(
            id=DOMICILIATION_REUSE_RULE_ID,
            source_ref=address_ref(AddressUsage.SIEGE_SOCIAL),
            target_ref=address_ref(AddressUsage.DOMICILIATION),
            relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
            label="domiciliation = siege social",
            kind=ReuseRuleKind.REFERENCE,
            status=ReuseRuleStatus.ACTIVE,
            explicit=True,
            allow_override=True,
            notes="Regle forte V2.1, tracee explicitement dans le DossierRecord.",
        )
    )


def _add_role_reuse_rule(
    dossier: DossierRecord,
    source_role: BusinessRole,
    target_role: BusinessRole,
    label: str,
) -> None:
    rule_id = _role_reuse_rule_id(target_role)
    if rule_id in dossier.reuse_rules:
        return
    dossier.add_reuse_rule(
        ReuseRuleState(
            id=rule_id,
            source_ref=role_ref(source_role),
            target_ref=role_ref(target_role),
            relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
            label=label,
            kind=ReuseRuleKind.REFERENCE,
            status=ReuseRuleStatus.ACTIVE,
            explicit=True,
            allow_override=False,
            notes="Role derive par option explicite de dossier unipersonnel.",
        )
    )


def _role_reuse_rule_id(target_role: BusinessRole) -> str:
    return f"{ROLE_REUSE_RULE_PREFIX}-{target_role.value}"


def _capital_repartition_value(entry: FrontDossierSimpleEntry) -> str:
    explicit_value = _clean(entry.capital_repartition_associes)
    if explicit_value:
        return explicit_value
    if not entry.dossier_unipersonnel:
        return ""
    total_parts = _clean(entry.capital_titres_nombre_total)
    full_name = _labels((entry.prenom, entry.nom))
    if total_parts and full_name:
        return f"{full_name} : {total_parts} parts"
    return ""


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _has_any_value(*values: object) -> bool:
    return any(_clean(value) for value in values)


def _labels(values: Iterable[object]) -> str:
    labels = tuple(_clean(value) for value in values if _clean(value))
    return " ".join(labels)
