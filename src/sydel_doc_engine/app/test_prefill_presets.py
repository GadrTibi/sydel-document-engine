from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from sydel_doc_engine.app.business_wizard import (
    BusinessAssociateInput,
    BusinessWizardInput,
)
from sydel_doc_engine.front_data.document_status import (
    DocumentStatusSummary,
    build_document_lot_status,
    build_document_status,
)
from sydel_doc_engine.front_data.dossier_flow import build_dossier_flow
from sydel_doc_engine.front_data.models import (
    AddressRecord,
    AddressUsage,
    BusinessRole,
    CanonicalFieldValue,
    CanonicalRelationType,
    CompanyRecord,
    DossierRecord,
    FrontObjectType,
    OperationContext,
    PersonRecord,
    ReuseRuleKind,
    ReuseRuleState,
    ReuseRuleStatus,
    RoleScope,
    RoleTargetType,
    address_ref,
)
from sydel_doc_engine.front_data.test_prefill_presets import (
    FrontDataTestPrefillProfile,
    front_data_test_prefill_profile,
)
from sydel_doc_engine.front_data.unit_document_mode import unit_document_requirement


@dataclass(frozen=True)
class BusinessTestPrefillPreset:
    key: str
    label: str
    case_type: str
    description: str
    widget_values: dict[str, object]
    front_data_profile: FrontDataTestPrefillProfile


SELARL_FORME_AFFICHAGE: Final = (
    "Societe d'exercice liberal a responsabilite limitee"
)
SELARL_FORME_LONGUE: Final = (
    "societe d'exercice liberal a responsabilite limitee"
)


def business_test_prefill_presets() -> tuple[BusinessTestPrefillPreset, ...]:
    return BUSINESS_TEST_PREFILL_PRESETS


def business_test_prefill_labels() -> tuple[str, ...]:
    return tuple(preset.label for preset in BUSINESS_TEST_PREFILL_PRESETS)


def business_test_prefill_by_label(label: str) -> BusinessTestPrefillPreset:
    for preset in BUSINESS_TEST_PREFILL_PRESETS:
        if preset.label == label:
            return preset
    raise KeyError(f"Scenario de test inconnu: {label}")


def business_test_prefill_widget_keys() -> tuple[str, ...]:
    return BUSINESS_TEST_PREFILL_WIDGET_KEYS


def business_test_prefill_front_data_profile(
    label: str,
) -> FrontDataTestPrefillProfile:
    return business_test_prefill_by_label(label).front_data_profile


def business_test_prefill_input(label: str) -> BusinessWizardInput:
    preset = business_test_prefill_by_label(label)
    if preset.case_type == "SELARL":
        return _selarl_input_from_widget_values(preset.widget_values)
    if preset.case_type == "SCI":
        return _sci_input_from_widget_values(preset.widget_values)
    raise ValueError(f"Unsupported test prefill case type: {preset.case_type}")


def business_test_prefill_front_dossier(label: str) -> DossierRecord:
    preset = business_test_prefill_by_label(label)
    data = business_test_prefill_input(label)
    dossier = DossierRecord(
        id=f"prefill-{preset.key}",
        label=preset.label,
        structure=preset.case_type,
        metadata={
            "test_prefill": True,
            "fictitious_data": True,
            "front_data_profile": preset.front_data_profile.key,
        },
    )
    for doc_code in preset.front_data_profile.status_document_codes:
        dossier.add_document_requirement(unit_document_requirement(doc_code))
    for operation_type in preset.front_data_profile.operation_types:
        dossier.add_operation_context(
            OperationContext(
                id=f"operation-{operation_type.value}",
                operation_type=operation_type,
            )
        )

    if preset.case_type == "SELARL":
        _populate_selarl_front_dossier(dossier, data, preset.widget_values)
    else:
        _populate_sci_front_dossier(dossier, data)

    return dossier


def business_test_prefill_status_summary(label: str) -> DocumentStatusSummary:
    preset = business_test_prefill_by_label(label)
    dossier = business_test_prefill_front_dossier(label)
    lot_id = f"prefill-{preset.key}"
    statuses = tuple(
        _status_for_prefill_document(dossier, doc_code, lot_id=lot_id)
        for doc_code in preset.front_data_profile.status_document_codes
    )
    return DocumentStatusSummary(
        documents=statuses,
        lots=(build_document_lot_status(lot_id, preset.label, statuses),),
    )


def _status_for_prefill_document(
    dossier: DossierRecord,
    doc_code: str,
    *,
    lot_id: str,
):
    single_doc_dossier = _single_document_view(dossier, doc_code)
    requirement = single_doc_dossier.document_requirements[doc_code]
    return build_document_status(
        single_doc_dossier,
        requirement,
        flow=build_dossier_flow(single_doc_dossier),
        lot_id=lot_id,
    )


def _single_document_view(dossier: DossierRecord, doc_code: str) -> DossierRecord:
    return DossierRecord(
        id=f"{dossier.id}-{doc_code}",
        label=dossier.label,
        structure=dossier.structure,
        persons=dict(dossier.persons),
        companies=dict(dossier.companies),
        addresses=dict(dossier.addresses),
        role_assignments=dict(dossier.role_assignments),
        operation_contexts=dict(dossier.operation_contexts),
        document_requirements={doc_code: dossier.document_requirements[doc_code]},
        canonical_values=dict(dossier.canonical_values),
        reuse_rules=dict(dossier.reuse_rules),
        resolved_ambiguity_keys=set(dossier.resolved_ambiguity_keys),
        metadata=dict(dossier.metadata),
    )


def _selarl_input_from_widget_values(
    values: dict[str, object],
) -> BusinessWizardInput:
    dossier_unipersonnel = _bool_value(values.get("condition_selarl_dossier_unipersonnel"))
    gerant_from_praticien = dossier_unipersonnel or _bool_value(
        values.get("selarl_gerant_is_professional")
    )
    signataire_from_praticien = dossier_unipersonnel or _bool_value(
        values.get("selarl_signataire_is_professional")
    )
    associes = _selarl_associes_from_widget_values(
        values,
        copy_first_from_praticien=(
            dossier_unipersonnel
            or _bool_value(values.get("selarl_copy_associe_1_from_professional"))
            or _bool_value(values.get("selarl_signataire_is_associe_1"))
        ),
    )
    dirigeant = _selarl_praticien_values(values) if gerant_from_praticien else values
    domiciliation = _text(values, "selarl_domiciliation_adresse_affichee")
    if not domiciliation and _bool_value(values.get("selarl_domiciliation_is_registered_office")):
        domiciliation = _address_display(
            _text(values, "selarl_societe_num"),
            _text(values, "selarl_societe_voie"),
            _text(values, "selarl_societe_cp"),
            _text(values, "selarl_societe_ville"),
        )

    return BusinessWizardInput(
        structure="SELARL",
        profession=_text(values, "condition_selarl_profession") or None,
        site_distinct=_bool_value(values.get("condition_selarl_site_distinct")),
        scm_cession=_bool_value(values.get("condition_selarl_scm_cession")),
        regime_communautaire=_bool_value(
            values.get("condition_selarl_regime_communautaire")
        ),
        derogation=_bool_value(values.get("condition_selarl_derogation")),
        cession=_bool_value(values.get("condition_selarl_cession")),
        cabinet_type=_optional_text(values, "condition_selarl_cabinet_type"),
        nombre_associes=len(associes),
        personne_genre=_text(values, "selarl_personne_genre"),
        personne_civilite=_text(values, "selarl_personne_civilite"),
        personne_prenom=_text(values, "selarl_personne_prenom"),
        personne_nom=_text(values, "selarl_personne_nom"),
        personne_date_naissance=_text(values, "selarl_personne_date_naissance"),
        personne_nationalite=_text(values, "selarl_personne_nationalite"),
        personne_nom_pere=_text(values, "selarl_personne_nom_pere"),
        personne_nom_mere=_text(values, "selarl_personne_nom_mere"),
        personne_fonction_dirigeant=_text(values, "selarl_personne_fonction"),
        personne_adresse_num_voie=_text(values, "selarl_personne_num"),
        personne_adresse_voie=_text(values, "selarl_personne_voie"),
        personne_adresse_cp=_text(values, "selarl_personne_cp"),
        personne_adresse_ville=_text(values, "selarl_personne_ville"),
        societe_forme_sociale=_text(values, "selarl_societe_forme_sociale"),
        societe_forme_sociale_affichage=_text(
            values,
            "selarl_societe_forme_sociale_affichage",
        ),
        societe_forme_sociale_libelle_long=_text(
            values,
            "selarl_societe_forme_sociale_libelle_long",
        ),
        societe_denomination=_text(values, "selarl_societe_denomination"),
        societe_capital_social=_text(values, "selarl_societe_capital_social"),
        societe_capital_variable=True,
        societe_siege_num_voie=_text(values, "selarl_societe_num"),
        societe_siege_voie=_text(values, "selarl_societe_voie"),
        societe_siege_cp=_text(values, "selarl_societe_cp"),
        societe_siege_ville=_text(values, "selarl_societe_ville"),
        societe_ville_rcs=_text(values, "selarl_societe_ville_rcs"),
        domiciliation_adresse_affichee=domiciliation,
        associes=associes,
        dirigeant_genre=_text(dirigeant, "selarl_personne_genre", "selarl_dirigeant_genre"),
        dirigeant_civilite_affichage=_text(
            dirigeant,
            "selarl_personne_civilite",
            "selarl_dirigeant_civilite",
        ),
        dirigeant_prenom=_text(
            dirigeant,
            "selarl_personne_prenom",
            "selarl_dirigeant_prenom",
        ),
        dirigeant_nom=_text(dirigeant, "selarl_personne_nom", "selarl_dirigeant_nom"),
        dirigeant_date_naissance=_text(
            dirigeant,
            "selarl_personne_date_naissance",
            "selarl_dirigeant_date_naissance",
        ),
        dirigeant_ville_naissance=_text(
            dirigeant,
            "selarl_personne_ville_naissance",
        ),
        dirigeant_departement_naissance=_text(
            dirigeant,
            "selarl_personne_departement_naissance",
        ),
        dirigeant_nationalite=_text(
            dirigeant,
            "selarl_personne_nationalite",
            "selarl_dirigeant_nationalite",
        ),
        dirigeant_fonction_affichage="gerant" if gerant_from_praticien else _text(
            values,
            "selarl_dirigeant_fonction",
        ),
        dirigeant_adresse_num_voie=_text(
            dirigeant,
            "selarl_personne_num",
            "selarl_dirigeant_num",
        ),
        dirigeant_adresse_voie=_text(
            dirigeant,
            "selarl_personne_voie",
            "selarl_dirigeant_voie",
        ),
        dirigeant_adresse_cp=_text(
            dirigeant,
            "selarl_personne_cp",
            "selarl_dirigeant_cp",
        ),
        dirigeant_adresse_ville=_text(
            dirigeant,
            "selarl_personne_ville",
            "selarl_dirigeant_ville",
        ),
        capital_nb_parts_total=_optional_int(values.get("selarl_capital_nb_parts_total")),
        capital_valeur_nominale_part=_text(
            values,
            "selarl_capital_valeur_nominale_part",
        ),
        decision_date=_text(values, "selarl_decision_date"),
        reunion_date_lettres=_text(values, "selarl_reunion_date_lettres"),
        reunion_heure=_text(values, "selarl_reunion_heure"),
        signature_lieu=_text(values, "selarl_signature_lieu"),
        signature_date=_text(values, "selarl_signature_date"),
        signature_nombre_exemplaires=_text(
            values,
            "selarl_signature_nombre_exemplaires",
        ),
        emprunt_actif=_bool_value(values.get("selarl_emprunt_actif")),
        emprunt_montant_max=_text(values, "selarl_emprunt_montant_max"),
        bien_adresse_num_voie=_text(values, "selarl_bien_num"),
        bien_adresse_voie=_text(values, "selarl_bien_voie"),
        bien_adresse_cp=_text(values, "selarl_bien_cp"),
        bien_adresse_ville=_text(values, "selarl_bien_ville"),
        selarl_signataire_is_associe_1=_bool_value(
            values.get("selarl_signataire_is_associe_1")
        ),
        selarl_dossier_unipersonnel=dossier_unipersonnel,
        selarl_gerant_is_professional=gerant_from_praticien and not dossier_unipersonnel,
        selarl_signataire_is_professional=(
            signataire_from_praticien and not dossier_unipersonnel
        ),
        selarl_mandataire_is_signataire=_bool_value(
            values.get("selarl_mandataire_is_signataire")
        ),
        selarl_company_is_acquirer=_bool_value(values.get("selarl_company_is_acquirer")),
        selarl_company_is_scm_transferee=_bool_value(
            values.get("selarl_company_is_scm_transferee")
        ),
        selarl_domiciliation_is_registered_office=_bool_value(
            values.get("selarl_domiciliation_is_registered_office")
        ),
    )


def _sci_input_from_widget_values(values: dict[str, object]) -> BusinessWizardInput:
    associe_count = _optional_int(values.get("business_associe_count")) or 0
    associes = tuple(
        BusinessAssociateInput(
            genre=_text(values, f"associe_genre_{index}"),
            civilite_affichage=_text(values, f"associe_civilite_{index}"),
            prenom=_text(values, f"associe_prenom_{index}"),
            nom=_text(values, f"associe_nom_{index}"),
            nb_parts=_optional_int(values.get(f"associe_parts_{index}")),
            est_present_ou_represente=_bool_value(
                values.get(f"associe_present_{index}", True)
            ),
        )
        for index in range(associe_count)
    )

    return BusinessWizardInput(
        structure="SCI",
        sci_iris=_text(values, "condition_sci_variant") == "SCI IRIS",
        option_is=_bool_value(values.get("condition_option_is")),
        nombre_associes=associe_count,
        personne_genre=_text(values, "business_personne_genre"),
        personne_civilite=_text(values, "business_personne_civilite"),
        personne_prenom=_text(values, "business_personne_prenom"),
        personne_nom=_text(values, "business_personne_nom"),
        personne_date_naissance=_text(values, "business_personne_date_naissance"),
        personne_nationalite=_text(values, "business_personne_nationalite"),
        personne_nom_pere=_text(values, "business_personne_nom_pere"),
        personne_nom_mere=_text(values, "business_personne_nom_mere"),
        personne_fonction_dirigeant=_text(values, "business_personne_fonction"),
        personne_adresse_num_voie=_text(values, "business_personne_num"),
        personne_adresse_voie=_text(values, "business_personne_voie"),
        personne_adresse_cp=_text(values, "business_personne_cp"),
        personne_adresse_ville=_text(values, "business_personne_ville"),
        societe_forme_sociale=_text(values, "business_societe_forme_sociale"),
        societe_forme_sociale_affichage=_text(
            values,
            "business_societe_forme_sociale_affichage",
        ),
        societe_forme_sociale_libelle_long=_text(
            values,
            "business_societe_forme_sociale_libelle_long",
        ),
        societe_denomination=_text(values, "business_societe_denomination"),
        societe_capital_social=_text(values, "business_societe_capital_social"),
        societe_capital_variable=_bool_value(
            values.get("business_societe_capital_variable", True)
        ),
        societe_siege_num_voie=_text(values, "business_societe_num"),
        societe_siege_voie=_text(values, "business_societe_voie"),
        societe_siege_cp=_text(values, "business_societe_cp"),
        societe_siege_ville=_text(values, "business_societe_ville"),
        societe_ville_rcs=_text(values, "business_societe_ville_rcs"),
        domiciliation_adresse_affichee=_text(
            values,
            "business_domiciliation_adresse_affichee",
        ),
        associes=associes,
        dirigeant_genre=_text(values, "business_dirigeant_genre"),
        dirigeant_civilite_affichage=_text(values, "business_dirigeant_civilite"),
        dirigeant_prenom=_text(values, "business_dirigeant_prenom"),
        dirigeant_nom=_text(values, "business_dirigeant_nom"),
        dirigeant_date_naissance=_text(values, "business_dirigeant_date_naissance"),
        dirigeant_ville_naissance=_text(values, "business_dirigeant_ville_naissance"),
        dirigeant_departement_naissance=_text(
            values,
            "business_dirigeant_departement_naissance",
        ),
        dirigeant_nationalite=_text(values, "business_dirigeant_nationalite"),
        dirigeant_fonction_affichage=_text(values, "business_dirigeant_fonction"),
        dirigeant_adresse_num_voie=_text(values, "business_dirigeant_num"),
        dirigeant_adresse_voie=_text(values, "business_dirigeant_voie"),
        dirigeant_adresse_cp=_text(values, "business_dirigeant_cp"),
        dirigeant_adresse_ville=_text(values, "business_dirigeant_ville"),
        capital_nb_parts_total=_optional_int(values.get("business_capital_nb_parts_total")),
        capital_valeur_nominale_part=_text(
            values,
            "business_capital_valeur_nominale_part",
        ),
        decision_date=_text(values, "business_decision_date"),
        reunion_date_lettres=_text(values, "business_reunion_date_lettres"),
        reunion_heure=_text(values, "business_reunion_heure"),
        signature_lieu=_text(values, "business_signature_lieu"),
        signature_date=_text(values, "business_signature_date"),
        signature_nombre_exemplaires=_text(
            values,
            "business_signature_nombre_exemplaires",
        ),
        emprunt_actif=_bool_value(values.get("business_emprunt_actif")),
        emprunt_montant_max=_text(values, "business_emprunt_montant_max"),
        bien_adresse_num_voie=_text(values, "business_bien_num"),
        bien_adresse_voie=_text(values, "business_bien_voie"),
        bien_adresse_cp=_text(values, "business_bien_cp"),
        bien_adresse_ville=_text(values, "business_bien_ville"),
    )


def _populate_selarl_front_dossier(
    dossier: DossierRecord,
    data: BusinessWizardInput,
    values: dict[str, object],
) -> None:
    praticien = PersonRecord(
        id="person-praticien",
        civilite_affichage=data.personne_civilite or None,
        genre=data.personne_genre or None,
        prenom=data.personne_prenom or None,
        nom=data.personne_nom or None,
        profession=data.profession,
        fonction=data.personne_fonction_dirigeant or None,
        numero_rpps=_optional_text(values, "selarl_numero_rpps"),
        numero_ordre=_optional_text(values, "selarl_numero_ordre"),
    )
    dossier.add_person(praticien)
    for role in (BusinessRole.PRATICIEN, BusinessRole.ASSOCIE, BusinessRole.GERANT):
        dossier.assign_role(role, RoleTargetType.PERSON, praticien.id)
    dossier.assign_role(
        BusinessRole.SIGNATAIRE,
        RoleTargetType.PERSON,
        praticien.id,
        scope=RoleScope.LOT,
        scope_id="prefill-simple-documents",
    )

    company = _add_main_company(dossier, data)
    _add_common_front_addresses(dossier, data, praticien.id, company.id)
    _add_selarl_lieu_exercice(dossier, values)
    _add_domiciliation_reuse_rule(dossier, "prefill-selarl-siege-domiciliation")
    _populate_common_canonical_values(dossier, data)
    dossier.resolve_ambiguity("legacy_domiciliation_display_alias")

    if data.cession:
        _populate_cession_front_data(dossier, data, values, company.id, praticien.id)


def _populate_sci_front_dossier(
    dossier: DossierRecord,
    data: BusinessWizardInput,
) -> None:
    signataire = PersonRecord(
        id="person-signataire",
        civilite_affichage=data.personne_civilite or None,
        genre=data.personne_genre or None,
        prenom=data.personne_prenom or None,
        nom=data.personne_nom or None,
        fonction=data.personne_fonction_dirigeant or None,
    )
    gerant = PersonRecord(
        id="person-gerant",
        civilite_affichage=data.dirigeant_civilite_affichage or None,
        genre=data.dirigeant_genre or None,
        prenom=data.dirigeant_prenom or None,
        nom=data.dirigeant_nom or None,
        fonction=data.dirigeant_fonction_affichage or None,
    )
    dossier.add_person(signataire)
    dossier.add_person(gerant)
    dossier.assign_role(
        BusinessRole.SIGNATAIRE,
        RoleTargetType.PERSON,
        signataire.id,
        scope=RoleScope.LOT,
        scope_id="prefill-simple-documents",
    )
    dossier.assign_role(BusinessRole.GERANT, RoleTargetType.PERSON, gerant.id)
    for index, associe in enumerate(data.associes):
        person_id = f"person-associe-{index + 1}"
        person = PersonRecord(
            id=person_id,
            civilite_affichage=associe.civilite_affichage or None,
            genre=associe.genre or None,
            prenom=associe.prenom or None,
            nom=associe.nom or None,
        )
        dossier.add_person(person)
        dossier.assign_role(BusinessRole.ASSOCIE, RoleTargetType.PERSON, person.id)

    company = _add_main_company(dossier, data)
    _add_common_front_addresses(dossier, data, signataire.id, company.id)
    _add_address_from_parts(
        dossier,
        "address-gerant",
        AddressUsage.ADRESSE_PERSONNELLE,
        data.dirigeant_adresse_num_voie,
        data.dirigeant_adresse_voie,
        data.dirigeant_adresse_cp,
        data.dirigeant_adresse_ville,
        owner_type=FrontObjectType.PERSON,
        owner_id=gerant.id,
    )
    _add_domiciliation_reuse_rule(dossier, "prefill-sci-siege-domiciliation")
    _populate_common_canonical_values(dossier, data)
    dossier.resolve_ambiguity("legacy_domiciliation_display_alias")


def _populate_cession_front_data(
    dossier: DossierRecord,
    data: BusinessWizardInput,
    values: dict[str, object],
    company_id: str,
    praticien_id: str,
) -> None:
    vendeur = PersonRecord(id="person-vendeur", nom=_text(values, "selarl_cession_cession_vendeur"))
    conjoint = PersonRecord(id="person-conjoint", prenom="Jeanne", nom="Durand")
    dossier.add_person(vendeur)
    dossier.add_person(conjoint)
    dossier.assign_role(
        BusinessRole.VENDEUR,
        RoleTargetType.PERSON,
        vendeur.id,
        scope=RoleScope.OPERATION,
        scope_id="operation-cession",
    )
    dossier.assign_role(BusinessRole.CONJOINT, RoleTargetType.PERSON, conjoint.id)
    dossier.assign_role(
        BusinessRole.ACQUEREUR,
        RoleTargetType.COMPANY,
        company_id,
        scope=RoleScope.OPERATION,
        scope_id="operation-cession",
    )
    dossier.assign_role(
        BusinessRole.REPRESENTANT_PERSONNE_MORALE,
        RoleTargetType.PERSON,
        praticien_id,
        scope=RoleScope.OPERATION,
        scope_id="operation-cession",
        represented_target_type=RoleTargetType.COMPANY,
        represented_target_id=company_id,
        represented_role=BusinessRole.ACQUEREUR,
    )

    bailleur = CompanyRecord(
        id="company-bailleur",
        denomination=_text(values, "selarl_bail_bail_bailleur") or "__bailleur_test__",
    )
    banque = CompanyRecord(
        id="company-banque",
        denomination=_text(values, "selarl_banque_banque_banque") or "__banque_test__",
    )
    dossier.add_company(bailleur)
    dossier.add_company(banque)
    dossier.assign_role(
        BusinessRole.BAILLEUR,
        RoleTargetType.COMPANY,
        bailleur.id,
        scope=RoleScope.OPERATION,
        scope_id="operation-bail",
    )
    dossier.assign_role(
        BusinessRole.LOCATAIRE,
        RoleTargetType.PERSON,
        vendeur.id,
        scope=RoleScope.OPERATION,
        scope_id="operation-bail",
    )
    dossier.assign_role(
        BusinessRole.BANQUE,
        RoleTargetType.COMPANY,
        banque.id,
        scope=RoleScope.OPERATION,
        scope_id="operation-financement",
    )

    _add_display_address(
        dossier,
        "address-vendeur",
        AddressUsage.DOMICILE_CEDANT,
        _text(values, "selarl_cession_cession_adresse_vendeur"),
        owner_type=FrontObjectType.PERSON,
        owner_id=vendeur.id,
    )
    _add_display_address(
        dossier,
        "address-cabinet-cede",
        AddressUsage.CABINET_CEDE,
        _text(values, "selarl_cession_cession_adresse_cabinet"),
    )
    _add_display_address(
        dossier,
        "address-locaux-loues",
        AddressUsage.LOCAUX_LOUES,
        _text(values, "selarl_cession_cession_adresse_locaux"),
    )
    _add_display_address(
        dossier,
        "address-bailleur",
        AddressUsage.BAILLEUR,
        _text(values, "selarl_bail_bail_adresse_bailleur"),
        owner_type=FrontObjectType.COMPANY,
        owner_id=bailleur.id,
    )
    _add_display_address(
        dossier,
        "address-locataire",
        AddressUsage.LOCATAIRE,
        _text(values, "selarl_bail_bail_adresse_locataire"),
        owner_type=FrontObjectType.PERSON,
        owner_id=vendeur.id,
    )
    _add_display_address(
        dossier,
        "address-banque",
        AddressUsage.BANQUE,
        _text(values, "selarl_banque_banque_adresse_banque"),
        owner_type=FrontObjectType.COMPANY,
        owner_id=banque.id,
    )
    _add_address_reuse_rule(
        dossier,
        "prefill-lieu-exercice-cabinet",
        AddressUsage.LIEU_EXERCICE,
        AddressUsage.CABINET_CEDE,
    )
    _add_address_reuse_rule(
        dossier,
        "prefill-lieu-exercice-locaux",
        AddressUsage.LIEU_EXERCICE,
        AddressUsage.LOCAUX_LOUES,
    )

    _add_canonical_value(
        dossier,
        "cession.cabinet.adresse",
        _text(values, "selarl_cession_cession_adresse_cabinet"),
    )
    _add_canonical_value(
        dossier,
        "cession.cabinet.prix_composantes",
        _text(values, "selarl_cession_cession_activite"),
    )
    _add_canonical_value(
        dossier,
        "cession.vendeur.identite",
        _text(values, "selarl_cession_cession_vendeur"),
    )
    _add_canonical_value(dossier, "cession.acquereur.identite", data.societe_denomination)
    _add_canonical_value(
        dossier,
        "cession.financement.modalites",
        _text(values, "selarl_banque_banque_pret"),
    )
    _add_canonical_value(
        dossier,
        "cession.prix.total",
        _text(values, "selarl_cession_cession_prix"),
    )
    _add_canonical_value(dossier, "cession.exercices[0].periode", "2024")
    _add_canonical_value(dossier, "bail.parties", _text(values, "selarl_bail_bail_bailleur"))
    _add_canonical_value(dossier, "bail.dates", _text(values, "selarl_bail_bail_conditions"))


def _add_main_company(
    dossier: DossierRecord,
    data: BusinessWizardInput,
) -> CompanyRecord:
    company = CompanyRecord(
        id="company-principale",
        denomination=data.societe_denomination or "__societe_test__",
        forme_sociale=data.societe_forme_sociale or None,
        capital_social=data.societe_capital_social or None,
    )
    dossier.add_company(company)
    dossier.assign_role(
        BusinessRole.SOCIETE_PRINCIPALE,
        RoleTargetType.COMPANY,
        company.id,
    )
    return company


def _add_common_front_addresses(
    dossier: DossierRecord,
    data: BusinessWizardInput,
    person_id: str,
    company_id: str,
) -> None:
    _add_address_from_parts(
        dossier,
        "address-personnelle",
        AddressUsage.ADRESSE_PERSONNELLE,
        data.personne_adresse_num_voie,
        data.personne_adresse_voie,
        data.personne_adresse_cp,
        data.personne_adresse_ville,
        owner_type=FrontObjectType.PERSON,
        owner_id=person_id,
    )
    _add_address_from_parts(
        dossier,
        "address-siege",
        AddressUsage.SIEGE_SOCIAL,
        data.societe_siege_num_voie,
        data.societe_siege_voie,
        data.societe_siege_cp,
        data.societe_siege_ville,
        owner_type=FrontObjectType.COMPANY,
        owner_id=company_id,
    )
    _add_display_address(
        dossier,
        "address-domiciliation",
        AddressUsage.DOMICILIATION,
        data.domiciliation_adresse_affichee,
    )


def _add_selarl_lieu_exercice(
    dossier: DossierRecord,
    values: dict[str, object],
) -> None:
    _add_display_address(
        dossier,
        "address-lieu-exercice",
        AddressUsage.LIEU_EXERCICE,
        _text(values, "selarl_adresse_lieu_exercice"),
    )


def _populate_common_canonical_values(
    dossier: DossierRecord,
    data: BusinessWizardInput,
) -> None:
    _add_canonical_value(dossier, "personne.signataire.genre", data.personne_genre)
    _add_canonical_value(
        dossier,
        "personne.signataire.civilite_affichage",
        data.personne_civilite,
    )
    _add_canonical_value(dossier, "personne.signataire.prenom", data.personne_prenom)
    _add_canonical_value(dossier, "personne.signataire.nom", data.personne_nom)
    _add_canonical_value(
        dossier,
        "personne.signataire.date_naissance",
        data.personne_date_naissance,
    )
    _add_canonical_value(
        dossier,
        "personne.signataire.nationalite",
        data.personne_nationalite,
    )
    _add_canonical_value(dossier, "personne.signataire.nom_pere", data.personne_nom_pere)
    _add_canonical_value(dossier, "personne.signataire.nom_mere", data.personne_nom_mere)
    _add_canonical_value(dossier, "personne.signataire.fonction", data.personne_fonction_dirigeant)
    _add_canonical_value(
        dossier,
        "personne.signataire.adresse_personnelle",
        _address_display(
            data.personne_adresse_num_voie,
            data.personne_adresse_voie,
            data.personne_adresse_cp,
            data.personne_adresse_ville,
        ),
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.denomination",
        data.societe_denomination,
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.forme_sociale",
        data.societe_forme_sociale,
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.capital_social",
        data.societe_capital_social,
    )
    _add_canonical_value(
        dossier,
        "societe.societe_principale.siege.adresse",
        _address_display(
            data.societe_siege_num_voie,
            data.societe_siege_voie,
            data.societe_siege_cp,
            data.societe_siege_ville,
        ),
    )
    _add_canonical_value(dossier, "domiciliation.adresse", data.domiciliation_adresse_affichee)
    _add_canonical_value(dossier, "capital.titres.nombre_total", data.capital_nb_parts_total)
    _add_canonical_value(
        dossier,
        "capital.titres.valeur_nominale",
        data.capital_valeur_nominale_part,
    )
    _add_canonical_value(dossier, "capital.repartition_associes", data.associes)
    _add_canonical_value(
        dossier,
        "personne.gerant.civilite_affichage",
        data.dirigeant_civilite_affichage,
    )
    _add_canonical_value(dossier, "personne.gerant.prenom", data.dirigeant_prenom)
    _add_canonical_value(dossier, "personne.gerant.nom", data.dirigeant_nom)
    _add_canonical_value(
        dossier,
        "personne.gerant.date_naissance",
        data.dirigeant_date_naissance,
    )
    _add_canonical_value(dossier, "personne.gerant.nationalite", data.dirigeant_nationalite)
    _add_canonical_value(
        dossier,
        "personne.gerant.adresse_personnelle",
        _address_display(
            data.dirigeant_adresse_num_voie,
            data.dirigeant_adresse_voie,
            data.dirigeant_adresse_cp,
            data.dirigeant_adresse_ville,
        ),
    )
    _add_canonical_value(dossier, "decision.date", data.decision_date)
    _add_canonical_value(dossier, "reunion.date_lettres", data.reunion_date_lettres)
    _add_canonical_value(dossier, "reunion.heure", data.reunion_heure)
    _add_canonical_value(dossier, "signature.lieu", data.signature_lieu)
    _add_canonical_value(dossier, "signature.date", data.signature_date)
    _add_canonical_value(
        dossier,
        "signature.nombre_exemplaires",
        data.signature_nombre_exemplaires,
    )


def _add_address_from_parts(
    dossier: DossierRecord,
    address_id: str,
    usage: AddressUsage,
    num_voie: str,
    voie: str,
    cp: str,
    ville: str,
    *,
    owner_type: FrontObjectType | None = None,
    owner_id: str | None = None,
) -> None:
    _add_display_address(
        dossier,
        address_id,
        usage,
        _address_display(num_voie, voie, cp, ville),
        owner_type=owner_type,
        owner_id=owner_id,
    )


def _add_display_address(
    dossier: DossierRecord,
    address_id: str,
    usage: AddressUsage,
    display_value: str,
    *,
    owner_type: FrontObjectType | None = None,
    owner_id: str | None = None,
) -> None:
    if not display_value:
        return
    dossier.add_address(
        AddressRecord(
            id=address_id,
            usage=usage,
            display_value=display_value,
            owner_object_type=owner_type,
            owner_object_id=owner_id,
        )
    )


def _add_domiciliation_reuse_rule(dossier: DossierRecord, rule_id: str) -> None:
    _add_address_reuse_rule(
        dossier,
        rule_id,
        AddressUsage.SIEGE_SOCIAL,
        AddressUsage.DOMICILIATION,
    )


def _add_address_reuse_rule(
    dossier: DossierRecord,
    rule_id: str,
    source_usage: AddressUsage,
    target_usage: AddressUsage,
) -> None:
    dossier.add_reuse_rule(
        ReuseRuleState(
            id=rule_id,
            source_ref=address_ref(source_usage),
            target_ref=address_ref(target_usage),
            relation_type=CanonicalRelationType.EXPLICIT_REUSE_ONLY,
            label=f"Test prefill: {source_usage.value} -> {target_usage.value}",
            kind=ReuseRuleKind.REFERENCE,
            status=ReuseRuleStatus.ACTIVE,
            explicit=True,
        )
    )


def _add_canonical_value(
    dossier: DossierRecord,
    field_path: str,
    value: object,
) -> None:
    if value in (None, "", ()):
        return
    dossier.add_canonical_value(CanonicalFieldValue(field_path=field_path, value=value))


def _selarl_praticien_values(values: dict[str, object]) -> dict[str, object]:
    return values


def _selarl_associes_from_widget_values(
    values: dict[str, object],
    *,
    copy_first_from_praticien: bool,
) -> tuple[BusinessAssociateInput, ...]:
    count = _optional_int(values.get("selarl_associe_count")) or 1
    if _bool_value(values.get("condition_selarl_dossier_unipersonnel")):
        count = 1
    associes: list[BusinessAssociateInput] = []
    for index in range(count):
        derived = index == 0 and copy_first_from_praticien
        associes.append(
            BusinessAssociateInput(
                genre=(
                    _text(values, "selarl_personne_genre")
                    if derived
                    else _text(values, f"selarl_associe_genre_{index}")
                ),
                civilite_affichage=(
                    _text(values, "selarl_personne_civilite")
                    if derived
                    else _text(values, f"selarl_associe_civilite_{index}")
                ),
                prenom=(
                    _text(values, "selarl_personne_prenom")
                    if derived
                    else _text(values, f"selarl_associe_prenom_{index}")
                ),
                nom=(
                    _text(values, "selarl_personne_nom")
                    if derived
                    else _text(values, f"selarl_associe_nom_{index}")
                ),
                nb_parts=_optional_int(values.get(f"selarl_associe_parts_{index}")),
                est_present_ou_represente=_bool_value(
                    values.get(f"selarl_associe_present_{index}", True)
                ),
            )
        )
    return tuple(associes)


def _bool_value(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    text = str(value).strip().casefold()
    return text in {"oui", "true", "1"}


def _optional_int(value: object) -> int | None:
    if isinstance(value, int):
        return value
    if value is None or value == "":
        return None
    return int(value)


def _optional_text(values: dict[str, object], key: str) -> str | None:
    value = _text(values, key)
    return value or None


def _text(values: dict[str, object], *keys: str) -> str:
    for key in keys:
        value = values.get(key)
        if value is not None:
            return str(value)
    return ""


def _address_display(num_voie: str, voie: str, cp: str, ville: str) -> str:
    street = " ".join(part.strip() for part in (num_voie, voie) if part.strip())
    locality = " ".join(part.strip() for part in (cp, ville) if part.strip())
    return ", ".join(part for part in (street, locality) if part)


def _common_selarl_values(
    *,
    profession: str,
    site_distinct: bool,
    scm_cession: bool,
    regime_communautaire: bool,
    derogation: bool,
    cession: bool,
    cabinet_type: str | None,
    denomination: str,
    praticien_prenom: str,
    praticien_nom: str,
    siege_num: str,
    siege_voie: str,
    siege_cp: str,
    siege_ville: str,
    rcs_ville: str,
    capital: str,
    nb_parts: int,
    valeur_part: str,
    signature_lieu: str,
    signature_date: str,
) -> dict[str, object]:
    values: dict[str, object] = {
        "condition_selarl_profession": profession,
        "condition_selarl_site_distinct": _bool_select(site_distinct),
        "condition_selarl_scm_cession": _bool_select(scm_cession),
        "condition_selarl_regime_communautaire": _bool_select(regime_communautaire),
        "condition_selarl_derogation": _bool_select(derogation),
        "condition_selarl_cession": _bool_select(cession),
        "condition_selarl_dossier_unipersonnel": True,
        "selarl_personne_genre": "masculin",
        "selarl_personne_civilite": "Docteur",
        "selarl_personne_prenom": praticien_prenom,
        "selarl_personne_nom": praticien_nom,
        "selarl_personne_date_naissance": "1985-04-03",
        "selarl_personne_ville_naissance": "Lyon",
        "selarl_personne_departement_naissance": "Rhone",
        "selarl_personne_nationalite": "francaise",
        "selarl_personne_nom_pere": f"Paul {praticien_nom}",
        "selarl_personne_nom_mere": "Anne Bernard",
        "selarl_personne_fonction": "Gerant",
        "selarl_personne_num": "8",
        "selarl_personne_voie": "avenue Victor Hugo",
        "selarl_personne_cp": "69002",
        "selarl_personne_ville": "Lyon",
        "selarl_numero_rpps": "10101234567",
        "selarl_numero_ordre": "69-12345",
        "selarl_adresse_conseil_ordre": (
            "Conseil departemental de l'ordre, 10 rue du Conseil, 69002 Lyon"
        ),
        "selarl_adresse_lieu_exercice": f"{siege_num} {siege_voie}, {siege_cp} {siege_ville}",
        "selarl_societe_denomination": denomination,
        "selarl_societe_forme_sociale": "SELARL",
        "selarl_societe_forme_sociale_affichage": SELARL_FORME_AFFICHAGE,
        "selarl_societe_forme_sociale_libelle_long": SELARL_FORME_LONGUE,
        "selarl_societe_capital_social": capital,
        "selarl_societe_ville_rcs": rcs_ville,
        "selarl_societe_num": siege_num,
        "selarl_societe_voie": siege_voie,
        "selarl_societe_cp": siege_cp,
        "selarl_societe_ville": siege_ville,
        "selarl_domiciliation_is_registered_office": True,
        "selarl_domiciliation_adresse_affichee": (
            f"{siege_num} {siege_voie}, {siege_cp} {siege_ville}"
        ),
        "selarl_capital_nb_parts_total": nb_parts,
        "selarl_capital_valeur_nominale_part": valeur_part,
        "selarl_associe_count": 1,
        "selarl_associe_parts_0": nb_parts,
        "selarl_associe_present_0": True,
        "selarl_decision_date": "2026-05-20",
        "selarl_reunion_date_lettres": "vingt mai deux mille vingt-six",
        "selarl_reunion_heure": "10 heures",
        "selarl_signature_lieu": signature_lieu,
        "selarl_signature_date": signature_date,
        "selarl_signature_nombre_exemplaires": "3",
        "selarl_emprunt_actif": False,
        "selarl_mandataire_is_signataire": False,
    }
    if cabinet_type is not None:
        values["condition_selarl_cabinet_type"] = cabinet_type
    return values


def _selarl_simple_medecin_values() -> dict[str, object]:
    return _common_selarl_values(
        profession="medecin",
        site_distinct=False,
        scm_cession=False,
        regime_communautaire=False,
        derogation=False,
        cession=False,
        cabinet_type=None,
        denomination="SELARL DU PARC MONCEAU",
        praticien_prenom="Camille",
        praticien_nom="Martin",
        siege_num="14",
        siege_voie="rue de Lisbonne",
        siege_cp="75008",
        siege_ville="Paris",
        rcs_ville="Paris",
        capital="5 000 euros",
        nb_parts=500,
        valeur_part="10 euros",
        signature_lieu="Paris",
        signature_date="2026-05-20",
    )


def _selarl_dentiste_regime_site_values() -> dict[str, object]:
    values = _common_selarl_values(
        profession="chirurgien_dentiste",
        site_distinct=True,
        scm_cession=False,
        regime_communautaire=True,
        derogation=True,
        cession=False,
        cabinet_type=None,
        denomination="SELARL SOURIRE RIVE GAUCHE",
        praticien_prenom="Adrien",
        praticien_nom="Moreau",
        siege_num="22",
        siege_voie="avenue du Maine",
        siege_cp="75015",
        siege_ville="Paris",
        rcs_ville="Paris",
        capital="8 000 euros",
        nb_parts=800,
        valeur_part="10 euros",
        signature_lieu="Paris",
        signature_date="2026-05-20",
    )
    values.update(
        {
            "selarl_regime_regime_conjoint": "Madame Elise Moreau",
            "selarl_regime_regime_apport": "Apport en numeraire de 8 000 euros",
        }
    )
    return values


def _selarl_medecin_cession_bail_financement_values() -> dict[str, object]:
    values = _common_selarl_values(
        profession="medecin",
        site_distinct=False,
        scm_cession=False,
        regime_communautaire=False,
        derogation=False,
        cession=True,
        cabinet_type="medical",
        denomination="SELARL MEDICALE DES ARCADES",
        praticien_prenom="Nicolas",
        praticien_nom="Leroy",
        siege_num="18",
        siege_voie="rue des Arcades",
        siege_cp="75012",
        siege_ville="Paris",
        rcs_ville="Paris",
        capital="10 000 euros",
        nb_parts=1000,
        valeur_part="10 euros",
        signature_lieu="Paris",
        signature_date="2026-05-20",
    )
    values.update(
        {
            "selarl_company_is_acquirer": True,
            "selarl_cession_cession_vendeur": "Docteur Jean Durand",
            "selarl_cession_cession_adresse_vendeur": (
                "6 rue du Cedant, 75011 Paris"
            ),
            "selarl_cession_cession_adresse_exercice_vendeur": (
                "3 rue du Cabinet Medical, 75012 Paris"
            ),
            "selarl_cession_cession_adresse_cabinet": (
                "3 rue du Cabinet Medical, 75012 Paris"
            ),
            "selarl_cession_cession_adresse_locaux": (
                "3 rue du Cabinet Medical, 75012 Paris"
            ),
            "selarl_cession_cession_acquereur": "SELARL MEDICALE DES ARCADES",
            "selarl_cession_cession_prix": "120 000 euros",
            "selarl_cession_cession_activite": (
                "Cabinet medical exploite depuis 2016, patientele locale stable"
            ),
            "selarl_bail_bail_bailleur": "SCI DES ARCADES",
            "selarl_bail_bail_adresse_bailleur": (
                "40 boulevard du Bailleur, 75008 Paris"
            ),
            "selarl_bail_bail_locataire": "Docteur Jean Durand",
            "selarl_bail_bail_adresse_locataire": (
                "6 rue du Cedant, 75011 Paris"
            ),
            "selarl_bail_bail_conditions": (
                "Bail professionnel du 1er janvier 2024, loyer mensuel 2 000 euros"
            ),
            "selarl_banque_banque_banque": "Banque Fictive de Paris",
            "selarl_banque_banque_adresse_banque": (
                "1 boulevard Haussmann, 75009 Paris"
            ),
            "selarl_banque_banque_pret": "Pret de 100 000 euros sur 84 mois",
            "selarl_banque_banque_credit_vendeur": (
                "Credit vendeur de 20 000 euros sur 24 mois"
            ),
            "selarl_emprunt_actif": True,
            "selarl_emprunt_montant_max": "250 000 euros",
            "selarl_bien_num": "3",
            "selarl_bien_voie": "rue du Cabinet Medical",
            "selarl_bien_cp": "75012",
            "selarl_bien_ville": "Paris",
        }
    )
    return values


def _sci_simple_values() -> dict[str, object]:
    return {
        "condition_sci_variant": "SCI simple",
        "condition_option_is": "Non",
        "business_societe_forme_sociale": "SCI",
        "business_societe_forme_sociale_affichage": "Societe civile immobiliere",
        "business_societe_forme_sociale_libelle_long": "societe civile immobiliere",
        "business_societe_denomination": "SCI DES TILLEULS",
        "business_societe_capital_social": "1 000 euros",
        "business_societe_capital_variable": True,
        "business_societe_ville_rcs": "Paris",
        "business_societe_num": "10",
        "business_societe_voie": "rue des Tilleuls",
        "business_societe_cp": "75016",
        "business_societe_ville": "Paris",
        "business_personne_genre": "masculin",
        "business_personne_civilite": "Monsieur",
        "business_personne_prenom": "Jean",
        "business_personne_nom": "Durand",
        "business_personne_date_naissance": "1990-02-03",
        "business_personne_nationalite": "francaise",
        "business_personne_nom_pere": "Pierre Durand",
        "business_personne_nom_mere": "Anne Martin",
        "business_personne_fonction": "Gerant",
        "business_personne_num": "12",
        "business_personne_voie": "rue des Lilas",
        "business_personne_cp": "75008",
        "business_personne_ville": "Paris",
        "business_associe_count": 2,
        "associe_genre_0": "feminin",
        "associe_civilite_0": "Madame",
        "associe_prenom_0": "Alice",
        "associe_nom_0": "Durand",
        "associe_parts_0": 60,
        "associe_present_0": True,
        "associe_genre_1": "masculin",
        "associe_civilite_1": "Monsieur",
        "associe_prenom_1": "Bruno",
        "associe_nom_1": "Martin",
        "associe_parts_1": 40,
        "associe_present_1": True,
        "business_dirigeant_genre": "feminin",
        "business_dirigeant_civilite": "Madame",
        "business_dirigeant_prenom": "Claire",
        "business_dirigeant_nom": "Bernard",
        "business_dirigeant_date_naissance": "1985-04-03",
        "business_dirigeant_ville_naissance": "Lyon",
        "business_dirigeant_departement_naissance": "Rhone",
        "business_dirigeant_nationalite": "francaise",
        "business_dirigeant_fonction": "gerant",
        "business_dirigeant_num": "22",
        "business_dirigeant_voie": "avenue des Fleurs",
        "business_dirigeant_cp": "69002",
        "business_dirigeant_ville": "Lyon",
        "business_domiciliation_adresse_affichee": (
            "10 rue des Tilleuls, 75016 Paris"
        ),
        "business_capital_nb_parts_total": 100,
        "business_capital_valeur_nominale_part": "10 euros",
        "business_decision_date": "2026-05-20",
        "business_reunion_date_lettres": "vingt mai deux mille vingt-six",
        "business_reunion_heure": "10 heures",
        "business_signature_lieu": "Paris",
        "business_signature_date": "2026-05-20",
        "business_signature_nombre_exemplaires": "3",
        "business_emprunt_actif": False,
    }


def _bool_select(value: bool) -> str:
    return "Oui" if value else "Non"


BUSINESS_TEST_PREFILL_PRESETS: Final[tuple[BusinessTestPrefillPreset, ...]] = (
    BusinessTestPrefillPreset(
        key="selarl_medecin_unipersonnelle_simple",
        label="SELARL médecin unipersonnelle simple",
        case_type="SELARL",
        description=(
            "Cas par defaut pour generer DOC-001 a DOC-004 avec un praticien "
            "associe unique, gerant et signataire."
        ),
        widget_values=_selarl_simple_medecin_values(),
        front_data_profile=front_data_test_prefill_profile(
            "selarl_medecin_unipersonnelle_simple"
        ),
    ),
    BusinessTestPrefillPreset(
        key="selarl_dentiste_regime_site",
        label="SELARL chirurgien-dentiste + régime communautaire + site distinct",
        case_type="SELARL",
        description=(
            "Active le regime communautaire, le site distinct et la derogation "
            "pour voir DOC-005/DOC-006 generes ainsi que DOC-013/DOC-014 manuels."
        ),
        widget_values=_selarl_dentiste_regime_site_values(),
        front_data_profile=front_data_test_prefill_profile("selarl_dentiste_regime_site"),
    ),
    BusinessTestPrefillPreset(
        key="selarl_medecin_cession_bail_financement",
        label="SELARL médecin + cession cabinet médical + bail + financement",
        case_type="SELARL",
        description=(
            "Active la cession de cabinet medical, le bail, la banque et "
            "l'emprunt DOC-004 avec donnees coherentes de test."
        ),
        widget_values=_selarl_medecin_cession_bail_financement_values(),
        front_data_profile=front_data_test_prefill_profile(
            "selarl_medecin_cession_bail_financement"
        ),
    ),
    BusinessTestPrefillPreset(
        key="sci_simple",
        label="SCI simple",
        case_type="SCI",
        description="Cas SCI simple pour verifier la non-regression du parcours existant.",
        widget_values=_sci_simple_values(),
        front_data_profile=front_data_test_prefill_profile("sci_simple"),
    ),
)

BUSINESS_TEST_PREFILL_WIDGET_KEYS: Final[tuple[str, ...]] = tuple(
    sorted(
        {
            key
            for preset in BUSINESS_TEST_PREFILL_PRESETS
            for key in preset.widget_values
        }
        | {
            "business_bien_cp",
            "business_bien_num",
            "business_bien_ville",
            "business_bien_voie",
            "business_emprunt_montant_max",
            "selarl_copy_associe_1_from_professional",
            "selarl_dirigeant_civilite",
            "selarl_dirigeant_cp",
            "selarl_dirigeant_date_naissance",
            "selarl_dirigeant_fonction",
            "selarl_dirigeant_genre",
            "selarl_dirigeant_nationalite",
            "selarl_dirigeant_nom",
            "selarl_dirigeant_num",
            "selarl_dirigeant_prenom",
            "selarl_dirigeant_ville",
            "selarl_dirigeant_voie",
            "selarl_gerant_choice",
            "selarl_gerant_is_professional",
            "selarl_associe_civilite_0",
            "selarl_associe_civilite_1",
            "selarl_associe_genre_0",
            "selarl_associe_genre_1",
            "selarl_associe_nom_0",
            "selarl_associe_nom_1",
            "selarl_associe_parts_1",
            "selarl_associe_prenom_0",
            "selarl_associe_prenom_1",
            "selarl_associe_present_1",
            "selarl_signataire_is_associe_1",
            "selarl_signataire_is_professional",
        }
    )
)
