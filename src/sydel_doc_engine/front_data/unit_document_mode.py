from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from sydel_doc_engine.domain.case_catalog import (
    CATALOG_DOCUMENTS,
    CatalogDocument,
    DocumentAvailability,
)
from sydel_doc_engine.front_data.canonical_mapping import (
    SENTINEL_DOCUMENT_REQUIREMENTS,
)
from sydel_doc_engine.front_data.document_status import (
    DocumentStatus,
    DocumentStatusRecord,
    build_document_status,
)
from sydel_doc_engine.front_data.dossier_flow import DossierFlow, build_dossier_flow
from sydel_doc_engine.front_data.models import (
    AddressUsage,
    BusinessRole,
    DocumentRequirementRecord,
    DocumentRequirementStatus,
    DossierRecord,
)


class UnitDocumentScopeStatus(StrEnum):
    SUPPORTED = "supported"
    OUT_OF_SCOPE_V1 = "out_of_scope_v1"
    MANUAL_ONLY = "manual_only"
    NOT_IMPLEMENTED = "not_implemented"
    CONTEXT_INCOMPLETE = "context_incomplete"
    GENERABLE_WITH_RESERVE = "generable_with_reserve"


@dataclass(frozen=True)
class UnitDocumentPlan:
    doc_code: str
    doc_label: str
    requirement: DocumentRequirementRecord
    status_record: DocumentStatusRecord
    scope_status: UnitDocumentScopeStatus
    scope_reasons: tuple[str, ...] = ()
    flow: DossierFlow | None = None

    @property
    def is_in_v1_scope(self) -> bool:
        return self.scope_status is UnitDocumentScopeStatus.SUPPORTED

    @property
    def is_generation_allowed(self) -> bool:
        return self.is_in_v1_scope and self.status_record.is_ready_for_generation

    @property
    def required_roles(self) -> tuple[BusinessRole, ...]:
        return _unique((*self.requirement.required_roles, *self.requirement.required_entities))

    @property
    def required_address_usages(self) -> tuple[AddressUsage, ...]:
        return self.requirement.required_address_usages

    @property
    def required_canonical_fields(self) -> tuple[str, ...]:
        return self.requirement.required_canonical_fields

    def explain_blockers(self) -> tuple[str, ...]:
        messages: list[str] = []
        if self.scope_status is not UnitDocumentScopeStatus.SUPPORTED:
            messages.extend(self.scope_reasons)
        messages.extend(reason.message for reason in self.status_record.why_not_generable())
        return tuple(dict.fromkeys(message for message in messages if message))


@dataclass(frozen=True)
class UnitDocumentPreparation:
    plan: UnitDocumentPlan
    dossier: DossierRecord | None

    @property
    def ready_for_generation(self) -> bool:
        return self.plan.is_generation_allowed

    @property
    def missing_roles(self) -> tuple[BusinessRole, ...]:
        return self.plan.status_record.missing_roles

    @property
    def missing_address_usages(self) -> tuple[AddressUsage, ...]:
        return self.plan.status_record.missing_address_usages

    @property
    def missing_canonical_fields(self) -> tuple[str, ...]:
        return self.plan.status_record.missing_canonical_fields


UNIT_DOCUMENT_V1_SUPPORTED_CODES: tuple[str, ...] = (
    "DOC-001",
    "DOC-002",
    "DOC-003",
    "DOC-004",
)

UNIT_DOCUMENT_V1_EXCLUSIONS: dict[str, str] = {
    "DOC-033": (
        "Hors perimetre V1 : cession SCM encore dependante de roles, prix, "
        "representant personne morale et adresses distinctes."
    ),
    "DOC-034": (
        "Hors perimetre V1 : ordre, mandataire, derogation et pieces ordinales "
        "restent orange dans le flow global."
    ),
}

_CATALOG_BY_CODE: dict[str, CatalogDocument] = {
    document.document_code: document
    for document in CATALOG_DOCUMENTS
    if document.document_code is not None
}


UNIT_DOCUMENT_V1_REQUIREMENTS: dict[str, DocumentRequirementRecord] = {
    "DOC-001": DocumentRequirementRecord(
        doc_code="DOC-001",
        doc_label="Declaration sur l'honneur de non-condamnation",
        required_roles=(BusinessRole.SIGNATAIRE,),
        required_address_usages=(AddressUsage.ADRESSE_PERSONNELLE,),
        required_entities=(BusinessRole.SIGNATAIRE,),
        required_canonical_fields=(
            "personne.signataire.genre",
            "personne.signataire.civilite_affichage",
            "personne.signataire.prenom",
            "personne.signataire.nom",
            "personne.signataire.date_naissance",
            "personne.signataire.nationalite",
            "personne.signataire.nom_pere",
            "personne.signataire.nom_mere",
            "personne.signataire.adresse_personnelle",
            "signature.lieu",
            "signature.date",
        ),
        target_screen_blocks=("document_unitaire", "fiche_personne", "signature"),
        verdict="VERT",
        action_needed="Porte par la fiche signataire et la signature.",
    ),
    "DOC-002": DocumentRequirementRecord(
        doc_code="DOC-002",
        doc_label="Autorisation de domiciliation",
        required_roles=(
            BusinessRole.SIGNATAIRE,
            BusinessRole.PRATICIEN,
            BusinessRole.SOCIETE_PRINCIPALE,
        ),
        required_address_usages=(AddressUsage.SIEGE_SOCIAL, AddressUsage.DOMICILIATION),
        required_entities=(
            BusinessRole.SIGNATAIRE,
            BusinessRole.PRATICIEN,
            BusinessRole.SOCIETE_PRINCIPALE,
        ),
        required_canonical_fields=(
            "personne.signataire.civilite_affichage",
            "personne.signataire.prenom",
            "personne.signataire.nom",
            "societe.societe_principale.denomination",
            "societe.societe_principale.capital_social",
            "societe.societe_principale.siege.adresse",
            "domiciliation.adresse",
            "signature.lieu",
            "signature.date",
        ),
        target_screen_blocks=(
            "document_unitaire",
            "fiche_personne",
            "fiche_societe",
            "adresses",
            "signature",
        ),
        possible_reuse_rules=("address:siege_social -> address:domiciliation",),
        unresolved_ambiguity_keys=("legacy_domiciliation_display_alias",),
        verdict="VERT",
        action_needed="Domiciliation portee par une adresse typee, pas par un alias.",
    ),
    "DOC-003": DocumentRequirementRecord(
        doc_code="DOC-003",
        doc_label="Procuration",
        required_roles=(BusinessRole.SIGNATAIRE, BusinessRole.SOCIETE_PRINCIPALE),
        required_address_usages=(AddressUsage.ADRESSE_PERSONNELLE, AddressUsage.SIEGE_SOCIAL),
        required_entities=(BusinessRole.SIGNATAIRE, BusinessRole.SOCIETE_PRINCIPALE),
        required_canonical_fields=(
            "personne.signataire.civilite_affichage",
            "personne.signataire.prenom",
            "personne.signataire.nom",
            "personne.signataire.fonction",
            "personne.signataire.adresse_personnelle",
            "societe.societe_principale.forme_sociale",
            "societe.societe_principale.denomination",
            "societe.societe_principale.siege.adresse",
            "signature.lieu",
            "signature.date",
        ),
        target_screen_blocks=(
            "document_unitaire",
            "fiche_personne",
            "fiche_societe",
            "adresses",
            "signature",
        ),
        verdict="VERT",
        action_needed="Mandataire SYDEL conserve comme constante documentaire du generateur.",
    ),
    "DOC-004": DocumentRequirementRecord(
        doc_code="DOC-004",
        doc_label="PV nomination gerant",
        required_roles=(
            BusinessRole.SIGNATAIRE,
            BusinessRole.ASSOCIE,
            BusinessRole.GERANT,
            BusinessRole.SOCIETE_PRINCIPALE,
        ),
        required_address_usages=(AddressUsage.ADRESSE_PERSONNELLE, AddressUsage.SIEGE_SOCIAL),
        required_entities=(
            BusinessRole.SIGNATAIRE,
            BusinessRole.ASSOCIE,
            BusinessRole.GERANT,
            BusinessRole.SOCIETE_PRINCIPALE,
        ),
        required_canonical_fields=(
            "societe.societe_principale.denomination",
            "societe.societe_principale.forme_sociale",
            "societe.societe_principale.capital_social",
            "societe.societe_principale.siege.adresse",
            "capital.titres.nombre_total",
            "capital.titres.valeur_nominale",
            "capital.repartition_associes",
            "personne.gerant.civilite_affichage",
            "personne.gerant.prenom",
            "personne.gerant.nom",
            "personne.gerant.date_naissance",
            "personne.gerant.nationalite",
            "personne.gerant.adresse_personnelle",
            "decision.date",
            "reunion.date_lettres",
            "reunion.heure",
            "signature.lieu",
            "signature.date",
            "signature.nombre_exemplaires",
        ),
        target_screen_blocks=(
            "document_unitaire",
            "fiche_societe",
            "capital_associes",
            "fiche_personne",
            "signature",
        ),
        verdict="VERT",
        action_needed="Cas simple seulement ; les variantes capital restent hors rebuild global.",
    ),
}


def unit_document_v1_supported_codes() -> tuple[str, ...]:
    return UNIT_DOCUMENT_V1_SUPPORTED_CODES


def unit_document_requirement(doc_code: str) -> DocumentRequirementRecord:
    if doc_code in UNIT_DOCUMENT_V1_REQUIREMENTS:
        return UNIT_DOCUMENT_V1_REQUIREMENTS[doc_code]
    if doc_code in SENTINEL_DOCUMENT_REQUIREMENTS:
        return SENTINEL_DOCUMENT_REQUIREMENTS[doc_code]
    catalog_document = _CATALOG_BY_CODE.get(doc_code)
    if catalog_document:
        return _requirement_from_catalog(catalog_document)
    return DocumentRequirementRecord(
        doc_code=doc_code,
        doc_label=doc_code,
        status=DocumentRequirementStatus.CONTEXT_INCOMPLETE,
        action_needed="Document absent du catalogue et du perimetre unitaire V1.",
    )


def build_unit_document_plan(
    doc_code: str,
    dossier: DossierRecord | None = None,
) -> UnitDocumentPlan:
    requirement = unit_document_requirement(doc_code)
    flow = (
        build_dossier_flow(dossier, document_codes=(doc_code,))
        if dossier and doc_code in dossier.document_requirements
        else None
    )
    status_record = build_document_status(dossier, requirement, flow=flow)
    scope_status = _scope_status_for(doc_code, status_record)
    return UnitDocumentPlan(
        doc_code=doc_code,
        doc_label=requirement.doc_label,
        requirement=requirement,
        status_record=status_record,
        scope_status=scope_status,
        scope_reasons=_scope_reasons_for(doc_code, scope_status),
        flow=flow,
    )


def prepare_unit_document_generation(
    doc_code: str,
    dossier: DossierRecord | None,
) -> UnitDocumentPreparation:
    if dossier and doc_code not in dossier.document_requirements:
        dossier.add_document_requirement(unit_document_requirement(doc_code))
    return UnitDocumentPreparation(
        plan=build_unit_document_plan(doc_code, dossier),
        dossier=dossier,
    )


def list_unit_document_v1_plans(
    doc_codes: Iterable[str] | None = None,
) -> tuple[UnitDocumentPlan, ...]:
    codes = tuple(doc_codes or UNIT_DOCUMENT_V1_SUPPORTED_CODES)
    return tuple(build_unit_document_plan(code) for code in codes)


def unit_document_requirement_rows(doc_code: str) -> tuple[dict[str, str], ...]:
    plan = build_unit_document_plan(doc_code)
    requirement = plan.requirement
    return (
        {
            "categorie": "roles",
            "valeurs": ", ".join(role.value for role in plan.required_roles),
        },
        {
            "categorie": "adresses",
            "valeurs": ", ".join(
                usage.value for usage in requirement.required_address_usages
            ),
        },
        {
            "categorie": "champs canoniques",
            "valeurs": ", ".join(requirement.required_canonical_fields),
        },
        {
            "categorie": "statut data-layer",
            "valeurs": plan.status_record.status.value,
        },
        {
            "categorie": "perimetre unitaire V1",
            "valeurs": plan.scope_status.value,
        },
    )


def _scope_status_for(
    doc_code: str,
    status_record: DocumentStatusRecord,
) -> UnitDocumentScopeStatus:
    if doc_code in UNIT_DOCUMENT_V1_SUPPORTED_CODES:
        return UnitDocumentScopeStatus.SUPPORTED
    if status_record.status is DocumentStatus.MANUAL_ONLY:
        return UnitDocumentScopeStatus.MANUAL_ONLY
    if status_record.status is DocumentStatus.NOT_IMPLEMENTED:
        return UnitDocumentScopeStatus.NOT_IMPLEMENTED
    if status_record.status is DocumentStatus.CONTEXT_INCOMPLETE:
        return UnitDocumentScopeStatus.CONTEXT_INCOMPLETE
    if status_record.status is DocumentStatus.GENERABLE_WITH_RESERVE:
        return UnitDocumentScopeStatus.GENERABLE_WITH_RESERVE
    return UnitDocumentScopeStatus.OUT_OF_SCOPE_V1


def _scope_reasons_for(
    doc_code: str,
    scope_status: UnitDocumentScopeStatus,
) -> tuple[str, ...]:
    if scope_status is UnitDocumentScopeStatus.SUPPORTED:
        return ("Document inclus dans le perimetre unitaire V1.",)
    if doc_code in UNIT_DOCUMENT_V1_EXCLUSIONS:
        return (UNIT_DOCUMENT_V1_EXCLUSIONS[doc_code],)
    if scope_status is UnitDocumentScopeStatus.MANUAL_ONLY:
        return ("Document manuel visible, hors generation automatique.",)
    if scope_status is UnitDocumentScopeStatus.NOT_IMPLEMENTED:
        return ("Document non implemente dans le moteur, hors generation unitaire.",)
    if scope_status is UnitDocumentScopeStatus.CONTEXT_INCOMPLETE:
        return ("Contexte ou mapping incomplet, hors generation unitaire V1.",)
    if scope_status is UnitDocumentScopeStatus.GENERABLE_WITH_RESERVE:
        return (
            "Document techniquement generable avec reserve, visible mais hors "
            "perimetre de generation unitaire V1.",
        )
    return ("Document hors perimetre prudent du mode unitaire V1.",)


def _requirement_from_catalog(
    catalog_document: CatalogDocument,
) -> DocumentRequirementRecord:
    return DocumentRequirementRecord(
        doc_code=catalog_document.document_code or catalog_document.document_key,
        doc_label=catalog_document.document_label,
        status=_requirement_status_from_catalog(catalog_document.availability),
        action_needed=catalog_document.notes or "",
    )


def _requirement_status_from_catalog(
    availability: DocumentAvailability,
) -> DocumentRequirementStatus:
    if availability is DocumentAvailability.MANUAL_ONLY:
        return DocumentRequirementStatus.MANUAL_ONLY
    if availability is DocumentAvailability.NOT_IMPLEMENTED:
        return DocumentRequirementStatus.NOT_IMPLEMENTED
    if availability is DocumentAvailability.NEEDS_MAPPING:
        return DocumentRequirementStatus.CONTEXT_INCOMPLETE
    return DocumentRequirementStatus.EXPECTED


def _unique(items: Iterable[object]) -> tuple:
    return tuple(dict.fromkeys(items))
