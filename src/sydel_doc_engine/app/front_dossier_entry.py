from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Final

from sydel_doc_engine.app.front_dossier_editor import (
    FrontDossierEditorView,
    build_front_dossier_editor_dossier,
    front_dossier_editor_profile,
)
from sydel_doc_engine.app.front_selarl_complete import (
    selarl_front_conditions,
    selarl_front_manual_without_code_labels,
    selarl_front_requirements,
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
    OperationContext,
    OperationType,
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
ORDER_COMPANY_ID: Final = "company-ordre-professionnel"
ORDER_ADDRESS_ID: Final = "address-ordre-professionnel"
MANDATAIRE_PERSON_ID: Final = "person-mandataire-ordre"
CONJOINT_PERSON_ID: Final = "person-conjoint-regime"
BANQUE_COMPANY_ID: Final = "company-banque-depot"
BANQUE_ADDRESS_ID: Final = "address-banque-depot"
DOMICILIATION_REUSE_RULE_ID: Final = "reuse-address-siege-domiciliation"
ROLE_REUSE_RULE_PREFIX: Final = "reuse-role-praticien"


@dataclass(frozen=True)
class FrontDossierSimpleEntry:
    profile_key: str = SELARL_CREATION_SIMPLE_PROFILE_KEY
    dossier_unipersonnel: bool = True
    domiciliation_same_as_siege: bool = True
    profession: str = "medecin"
    site_distinct: bool = False
    scm_cession: bool = False
    regime_communautaire: bool = False
    derogation: bool = False
    cession: bool = False
    cabinet_type: str = ""
    civilite_affichage: str = ""
    genre: str = ""
    titre_affichage: str = ""
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
    signature_prestataire: str = ""
    ordre_conseil_departemental_libelle: str = ""
    ordre_destinataire_appel: str = ""
    ordre_profession_signataire_affichee: str = ""
    ordre_profession_ligne_destinataire: str = ""
    ordre_profession_reglementee_pluriel: str = ""
    ordre_adresse_ligne_1: str = ""
    ordre_adresse_cp: str = ""
    ordre_adresse_ville: str = ""
    ordre_numero: str = ""
    ordre_numero_rpps: str = ""
    ordre_derogation_mention_manuelle: str = ""
    mandataire_civilite_affichage: str = ""
    mandataire_prenom: str = ""
    mandataire_nom: str = ""
    mandataire_fonction: str = ""
    mandataire_cabinet: str = ""
    statuts_capital_social_lettres: str = ""
    statuts_societe_duree: str = "99 ans"
    statuts_apport_montant: str = ""
    statuts_apport_montant_lettres: str = ""
    statuts_nombre_titres_total_lettres: str = ""
    statuts_valeur_nominale_titre_lettres: str = ""
    statuts_associe_profession: str = ""
    statuts_associe_profession_reglementee: str = ""
    statuts_associe_profession_reglementee_pluriel: str = ""
    statuts_associe_qualification_principale: str = ""
    statuts_associe_titre_professionnel: str = ""
    statuts_associe_qualite: str = "associe unique"
    statuts_associe_situation_maritale: str = ""
    statuts_associe_regime_matrimonial: str = ""
    conjoint_civilite_affichage: str = ""
    conjoint_prenom: str = ""
    conjoint_nom: str = ""
    conjoint_adresse: str = ""
    depot_banque_nom: str = ""
    depot_banque_adresse: str = ""
    exercice_social_debut: str = ""
    exercice_social_fin: str = ""
    exercice_social_date_cloture_premier_exercice: str = ""
    exercice_lieu_principal_adresse: str = ""
    gerance_seuil_achat_materiel: str = ""
    gerance_seuil_emprunt: str = ""
    document_nombre_exemplaires_lettres: str = ""
    regime_apport_montant: str = ""
    regime_apport_montant_lettres: str = ""
    regime_matrimonial: str = ""
    regime_qualite_renoncee: str = ""
    regime_date_courrier_avertissement: str = ""
    regime_renonciation_lieu_signature: str = ""
    regime_renonciation_date_signature: str = ""
    regime_renonciation_nombre_exemplaires_lettres: str = ""
    regime_avertissement_date_signature: str = ""


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
    conditions = _entry_conditions(entry)
    dossier.metadata.update(
        {
            "front_editor_v1": True,
            "front_data_entry_v1": True,
            "placeholder_values": False,
            "dossier_unipersonnel": entry.dossier_unipersonnel,
            "domiciliation_same_as_siege": entry.domiciliation_same_as_siege,
            "selarl_conditions": conditions,
            "front_selarl_manual_without_code": selarl_front_manual_without_code_labels(
                conditions
            ),
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

    _add_order_if_present(dossier, entry)
    _add_mandataire_if_present(dossier, entry)
    _add_conjoint_if_present(dossier, entry)
    _add_banque_if_present(dossier, entry)
    _add_capital_and_signature_values(dossier, entry)
    _add_selarl_complete_values(dossier, entry)
    _sync_selarl_complete_requirements(dossier, conditions)
    _resolve_selarl_complete_ambiguities(dossier, entry)
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
            profession=_clean(_front_profession_label(entry)),
            fonction=_clean(entry.fonction),
            numero_rpps=_clean(entry.ordre_numero_rpps),
            numero_ordre=_clean(entry.ordre_numero),
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


def _add_order_if_present(dossier: DossierRecord, entry: FrontDossierSimpleEntry) -> None:
    if not _has_any_value(
        entry.ordre_conseil_departemental_libelle,
        entry.ordre_destinataire_appel,
        entry.ordre_adresse_ligne_1,
        entry.ordre_adresse_cp,
        entry.ordre_adresse_ville,
    ):
        return
    dossier.add_company(
        CompanyRecord(
            id=ORDER_COMPANY_ID,
            denomination=_clean(entry.ordre_conseil_departemental_libelle)
            or "Conseil de l'ordre",
            metadata={"front_entry_v1": True, "institution": "ordre"},
        )
    )
    assign_explicit_role(
        dossier,
        BusinessRole.ORDRE_PROFESSIONNEL,
        ORDER_COMPANY_ID,
        target_type=RoleTargetType.COMPANY,
        assignment_id="role-ordre-professionnel",
        scope=RoleScope.OPERATION,
        scope_id="operation-ordre",
        notes="Conseil de l'ordre saisi explicitement pour la SELARL complete.",
    )
    if _has_any_value(
        entry.ordre_adresse_ligne_1,
        entry.ordre_adresse_cp,
        entry.ordre_adresse_ville,
    ):
        dossier.add_address(
            AddressRecord(
                id=ORDER_ADDRESS_ID,
                usage=AddressUsage.ORDRE,
                display_value=_labels(
                    (
                        entry.ordre_adresse_ligne_1,
                        _labels((entry.ordre_adresse_cp, entry.ordre_adresse_ville)),
                    )
                ),
                street_name=_clean(entry.ordre_adresse_ligne_1),
                postal_code=_clean(entry.ordre_adresse_cp),
                city=_clean(entry.ordre_adresse_ville),
                display_source=AddressDisplaySource.MANUAL,
                owner_object_type=FrontObjectType.COMPANY,
                owner_object_id=ORDER_COMPANY_ID,
                metadata={"front_entry_v1": True},
            )
        )


def _add_mandataire_if_present(dossier: DossierRecord, entry: FrontDossierSimpleEntry) -> None:
    if not _has_any_value(
        entry.mandataire_civilite_affichage,
        entry.mandataire_prenom,
        entry.mandataire_nom,
        entry.mandataire_fonction,
        entry.mandataire_cabinet,
    ):
        return
    dossier.add_person(
        PersonRecord(
            id=MANDATAIRE_PERSON_ID,
            civilite_affichage=_clean(entry.mandataire_civilite_affichage),
            prenom=_clean(entry.mandataire_prenom),
            nom=_clean(entry.mandataire_nom),
            fonction=_clean(entry.mandataire_fonction),
            metadata={"front_entry_v1": True, "role": "mandataire"},
        )
    )
    assign_explicit_role(
        dossier,
        BusinessRole.MANDATAIRE,
        MANDATAIRE_PERSON_ID,
        target_type=RoleTargetType.PERSON,
        assignment_id="role-mandataire-ordre",
        scope=RoleScope.OPERATION,
        scope_id="operation-ordre",
        notes="Mandataire ordre saisi explicitement, sans derivation du signataire.",
    )


def _add_conjoint_if_present(dossier: DossierRecord, entry: FrontDossierSimpleEntry) -> None:
    if not _has_any_value(
        entry.conjoint_civilite_affichage,
        entry.conjoint_prenom,
        entry.conjoint_nom,
        entry.conjoint_adresse,
    ):
        return
    dossier.add_person(
        PersonRecord(
            id=CONJOINT_PERSON_ID,
            civilite_affichage=_clean(entry.conjoint_civilite_affichage),
            prenom=_clean(entry.conjoint_prenom),
            nom=_clean(entry.conjoint_nom),
            metadata={"front_entry_v1": True, "role": "conjoint"},
        )
    )
    assign_explicit_role(
        dossier,
        BusinessRole.CONJOINT,
        CONJOINT_PERSON_ID,
        target_type=RoleTargetType.PERSON,
        assignment_id="role-conjoint-regime",
        scope=RoleScope.DOSSIER,
        notes="Conjoint saisi explicitement pour regime communautaire.",
    )


def _add_banque_if_present(dossier: DossierRecord, entry: FrontDossierSimpleEntry) -> None:
    if not _has_any_value(entry.depot_banque_nom, entry.depot_banque_adresse):
        return
    dossier.add_company(
        CompanyRecord(
            id=BANQUE_COMPANY_ID,
            denomination=_clean(entry.depot_banque_nom) or "Banque de depot",
            metadata={"front_entry_v1": True, "role": "banque"},
        )
    )
    assign_explicit_role(
        dossier,
        BusinessRole.BANQUE,
        BANQUE_COMPANY_ID,
        target_type=RoleTargetType.COMPANY,
        assignment_id="role-banque-depot",
        scope=RoleScope.OPERATION,
        scope_id="operation-creation",
        notes="Banque de depot saisie explicitement pour statuts SEL.",
    )
    if _clean(entry.depot_banque_adresse):
        dossier.add_address(
            AddressRecord(
                id=BANQUE_ADDRESS_ID,
                usage=AddressUsage.BANQUE,
                display_value=_clean(entry.depot_banque_adresse),
                display_source=AddressDisplaySource.MANUAL,
                owner_object_type=FrontObjectType.COMPANY,
                owner_object_id=BANQUE_COMPANY_ID,
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
            "titre_affichage": entry.titre_affichage,
            "prenom": entry.prenom,
            "nom": entry.nom,
            "profession": _front_profession_label(entry),
            "fonction": entry.fonction,
            "date_naissance": entry.date_naissance,
            "ville_naissance": entry.ville_naissance,
            "departement_naissance": entry.departement_naissance,
            "nationalite": entry.nationalite,
            "nom_pere": entry.nom_pere,
            "nom_mere": entry.nom_mere,
            "adresse_personnelle": entry.adresse_personnelle,
            "numero_ordre": entry.ordre_numero,
            "numero_rpps": entry.ordre_numero_rpps,
            "qualification_principale": entry.statuts_associe_qualification_principale,
            "situation_maritale": entry.statuts_associe_situation_maritale,
            "regime_matrimonial": entry.statuts_associe_regime_matrimonial,
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


def _add_selarl_complete_values(
    dossier: DossierRecord,
    entry: FrontDossierSimpleEntry,
) -> None:
    for field_path, value in _selarl_complete_field_values(entry).items():
        _add_canonical_value(
            dossier,
            field_path,
            value,
            owner_object_type=FrontObjectType.DOSSIER,
            owner_object_id=dossier.id,
        )


def _selarl_complete_field_values(entry: FrontDossierSimpleEntry) -> dict[str, object]:
    profession_label = _front_profession_label(entry)
    profession_plural = (
        entry.ordre_profession_reglementee_pluriel
        or entry.statuts_associe_profession_reglementee_pluriel
        or _front_profession_plural(entry)
    )
    statuts_apport_montant = entry.statuts_apport_montant or entry.societe_capital_social
    statuts_apport_lettres = (
        entry.statuts_apport_montant_lettres or entry.statuts_capital_social_lettres
    )
    regime_apport_montant = entry.regime_apport_montant or statuts_apport_montant
    regime_apport_lettres = entry.regime_apport_montant_lettres or statuts_apport_lettres
    return {
        "dossier.conditions.profession": entry.profession,
        "dossier.options.site_distinct": entry.site_distinct,
        "dossier.options.scm_cession": entry.scm_cession,
        "dossier.options.regime_communautaire": entry.regime_communautaire,
        "dossier.options.derogation": entry.derogation,
        "dossier.options.cession": entry.cession,
        "dossier.options.cabinet_type": entry.cabinet_type,
        "ordre.professionnel": entry.ordre_conseil_departemental_libelle,
        "ordre.destinataire_appel": entry.ordre_destinataire_appel,
        "ordre.profession_signataire_affichee": (
            entry.ordre_profession_signataire_affichee or profession_label
        ),
        "ordre.profession_ligne_destinataire": (
            entry.ordre_profession_ligne_destinataire or profession_plural
        ),
        "ordre.profession_reglementee_pluriel": profession_plural,
        "ordre.adresse": _labels(
            (
                entry.ordre_adresse_ligne_1,
                _labels((entry.ordre_adresse_cp, entry.ordre_adresse_ville)),
            )
        ),
        "ordre.adresse.ligne_1": entry.ordre_adresse_ligne_1,
        "ordre.adresse.cp": entry.ordre_adresse_cp,
        "ordre.adresse.ville": entry.ordre_adresse_ville,
        "ordre.numero": entry.ordre_numero,
        "ordre.numero_rpps": entry.ordre_numero_rpps,
        "ordre.departement": entry.ordre_adresse_ville,
        "ordre.derogation_mention_manuelle": entry.ordre_derogation_mention_manuelle,
        "personne.mandataire.civilite_affichage": entry.mandataire_civilite_affichage,
        "personne.mandataire.prenom": entry.mandataire_prenom,
        "personne.mandataire.nom": entry.mandataire_nom,
        "personne.mandataire.fonction": entry.mandataire_fonction,
        "personne.mandataire.cabinet": entry.mandataire_cabinet,
        "statuts_sel.overlay": _statuts_overlay(entry),
        "statuts_sel.profession": _front_profession_key(entry),
        "societe.societe_principale.capital_social_lettres": (
            entry.statuts_capital_social_lettres
        ),
        "societe.societe_principale.duree": entry.statuts_societe_duree,
        "capital.titres.nombre_total_lettres": entry.statuts_nombre_titres_total_lettres,
        "capital.titres.valeur_nominale_lettres": (
            entry.statuts_valeur_nominale_titre_lettres
        ),
        "apport.numeraire.montant": statuts_apport_montant,
        "apport.numeraire.montant_lettres": statuts_apport_lettres,
        "personne.associe.profession_reglementee": (
            entry.statuts_associe_profession_reglementee or profession_label
        ),
        "personne.associe.profession_reglementee_pluriel": profession_plural,
        "personne.associe.titre_professionnel": (
            entry.statuts_associe_titre_professionnel or entry.titre_affichage
        ),
        "personne.associe.qualite": entry.statuts_associe_qualite,
        "personne.associe.conjoint.civilite_affichage": entry.conjoint_civilite_affichage,
        "personne.associe.conjoint.prenom": entry.conjoint_prenom,
        "personne.associe.conjoint.nom": entry.conjoint_nom,
        "statuts_civils.associes[0].prenom": entry.prenom,
        "statuts_civils.associes[0].nom": entry.nom,
        "statuts_civils.associes[0].nb_parts": entry.capital_titres_nombre_total,
        "statuts_civils.associes[0].apport.montant": statuts_apport_montant,
        "personne.conjoint.civilite_affichage": entry.conjoint_civilite_affichage,
        "personne.conjoint.prenom": entry.conjoint_prenom,
        "personne.conjoint.nom": entry.conjoint_nom,
        "personne.conjoint.adresse_personnelle": entry.conjoint_adresse,
        "banque.depot.nom": entry.depot_banque_nom,
        "banque.depot.adresse": entry.depot_banque_adresse,
        "banque.banque": entry.depot_banque_nom,
        "banque.banque.adresse": entry.depot_banque_adresse,
        "cession.financement.banque.nom": entry.depot_banque_nom,
        "exercice_social.debut": entry.exercice_social_debut,
        "exercice_social.fin": entry.exercice_social_fin,
        "exercice_social.date_cloture_premier_exercice": (
            entry.exercice_social_date_cloture_premier_exercice
        ),
        "exercice.lieu_principal.adresse": entry.exercice_lieu_principal_adresse,
        "gerance.seuil_achat_materiel": entry.gerance_seuil_achat_materiel,
        "gerance.seuil_emprunt": entry.gerance_seuil_emprunt,
        "document.nombre_exemplaires_lettres": (
            entry.document_nombre_exemplaires_lettres
            or entry.signature_nombre_exemplaires
        ),
        "document.signataire.prenom": entry.prenom,
        "document.signataire.nom": entry.nom,
        "signature.prestataire_signature_electronique": entry.signature_prestataire,
        "regime_communautaire.regime_matrimonial": entry.regime_matrimonial,
        "regime_communautaire.qualite_renoncee": entry.regime_qualite_renoncee,
        "regime_communautaire.date_courrier_avertissement": (
            entry.regime_date_courrier_avertissement
        ),
        "regime_communautaire.renonciation.lieu_signature": (
            entry.regime_renonciation_lieu_signature
        ),
        "regime_communautaire.renonciation.date_signature": (
            entry.regime_renonciation_date_signature
        ),
        "regime_communautaire.renonciation.nombre_exemplaires_lettres": (
            entry.regime_renonciation_nombre_exemplaires_lettres
        ),
        "regime_communautaire.avertissement.date_signature": (
            entry.regime_avertissement_date_signature
        ),
        "regime_communautaire.apport.montant": regime_apport_montant,
        "regime_communautaire.apport.montant_lettres": regime_apport_lettres,
    }


def _sync_selarl_complete_requirements(
    dossier: DossierRecord,
    conditions: dict[str, Any],
) -> None:
    dossier.document_requirements.clear()
    for operation_type in _operation_types_for_conditions(conditions):
        operation_id = f"operation-{operation_type.value}"
        if operation_id not in dossier.operation_contexts:
            dossier.add_operation_context(
                OperationContext(
                    id=operation_id,
                    operation_type=operation_type,
                    label=operation_type.value,
                )
            )
    for requirement in selarl_front_requirements(conditions):
        dossier.add_document_requirement(requirement)


def _resolve_selarl_complete_ambiguities(
    dossier: DossierRecord,
    entry: FrontDossierSimpleEntry,
) -> None:
    if _has_any_value(
        entry.ordre_conseil_departemental_libelle,
        entry.ordre_adresse_ligne_1,
        entry.ordre_adresse_cp,
        entry.ordre_adresse_ville,
    ):
        dossier.resolved_ambiguity_keys.add("ordre_model_per_inscrit")
    if _has_any_value(
        entry.mandataire_civilite_affichage,
        entry.mandataire_prenom,
        entry.mandataire_nom,
        entry.mandataire_fonction,
        entry.mandataire_cabinet,
    ):
        dossier.resolved_ambiguity_keys.add("mandataire_configurable")
    if not entry.derogation or _clean(entry.ordre_derogation_mention_manuelle):
        dossier.resolved_ambiguity_keys.add("derogation_manual_block")
    if entry.dossier_unipersonnel:
        dossier.resolved_ambiguity_keys.add("pluralite_associes_statuts_selarl")
        dossier.resolved_ambiguity_keys.add("associes_scm_one_to_six")
    if _has_any_value(entry.gerance_seuil_achat_materiel, entry.gerance_seuil_emprunt):
        dossier.resolved_ambiguity_keys.add("seuils_gerance")
    if _has_any_value(entry.statuts_apport_montant, entry.statuts_apport_montant_lettres):
        dossier.resolved_ambiguity_keys.add("apports_parts_per_associe")
    if _has_any_value(entry.depot_banque_nom, entry.depot_banque_adresse):
        dossier.resolved_ambiguity_keys.add("banque_depot_parametrage")


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


def _entry_conditions(entry: FrontDossierSimpleEntry) -> dict[str, Any]:
    return selarl_front_conditions(
        profession=entry.profession,
        site_distinct=entry.site_distinct,
        scm_cession=entry.scm_cession,
        regime_communautaire=entry.regime_communautaire,
        derogation=entry.derogation,
        cession=entry.cession,
        cabinet_type=entry.cabinet_type,
    )


def _operation_types_for_conditions(
    conditions: dict[str, Any],
) -> tuple[OperationType, ...]:
    operation_types = [OperationType.CREATION, OperationType.ORDRE]
    if conditions.get("regime_communautaire"):
        operation_types.append(OperationType.REGIME_COMMUNAUTAIRE)
    if conditions.get("derogation") or conditions.get("site_distinct"):
        operation_types.append(OperationType.DEROGATION)
    if conditions.get("cession"):
        operation_types.extend(
            (
                OperationType.CESSION,
                OperationType.BAIL,
                OperationType.FINANCEMENT,
            )
        )
    if conditions.get("scm_cession"):
        operation_types.append(OperationType.CESSION_PARTS_SCM)
    return tuple(dict.fromkeys(operation_types))


def _front_profession_key(entry: FrontDossierSimpleEntry) -> str:
    value = _clean(entry.profession).lower().replace("-", "_").replace(" ", "_")
    if value in {"chirurgien_dentiste", "dentiste"}:
        return "chirurgien_dentiste"
    return "medecin"


def _front_profession_label(entry: FrontDossierSimpleEntry) -> str:
    if _front_profession_key(entry) == "chirurgien_dentiste":
        return "chirurgien-dentiste"
    return "medecin"


def _front_profession_plural(entry: FrontDossierSimpleEntry) -> str:
    if _front_profession_key(entry) == "chirurgien_dentiste":
        return "chirurgiens-dentistes"
    return "medecins"


def _statuts_overlay(entry: FrontDossierSimpleEntry) -> str:
    if _front_profession_key(entry) == "chirurgien_dentiste":
        return "selarl_dentiste"
    return "selarl_medecin"


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _has_any_value(*values: object) -> bool:
    return any(_clean(value) for value in values)


def _labels(values: Iterable[object]) -> str:
    labels = tuple(_clean(value) for value in values if _clean(value))
    return " ".join(labels)
