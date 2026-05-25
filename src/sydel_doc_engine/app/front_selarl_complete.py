from __future__ import annotations

from dataclasses import replace
from typing import Any, Final

from sydel_doc_engine.domain.case_catalog import (
    CaseInput,
    CaseType,
    DocumentAvailability,
    ExpectedDocument,
    get_expected_documents,
)
from sydel_doc_engine.front_data.canonical_mapping import sentinel_requirement
from sydel_doc_engine.front_data.models import (
    BusinessRole,
    DocumentRequirementRecord,
    DocumentRequirementStatus,
)
from sydel_doc_engine.front_data.unit_document_mode import unit_document_requirement

SELARL_FRONT_PROFILE_LABEL: Final = "SELARL complete"

SELARL_FRONT_RESERVE_DOC_CODES: Final[tuple[str, ...]] = ("DOC-006",)
SELARL_FRONT_MANUAL_DOC_CODES: Final[tuple[str, ...]] = ("DOC-013", "DOC-014")
SELARL_FRONT_COMPLEX_PENDING_DOC_CODES: Final[tuple[str, ...]] = (
    "DOC-007",
    "DOC-008",
    "DOC-009",
    "DOC-010",
    "DOC-011",
    "DOC-012",
    "DOC-031",
    "DOC-032",
    "DOC-033",
)
SELARL_FRONT_AUTO_DOC_CODES: Final[tuple[str, ...]] = (
    "DOC-001",
    "DOC-002",
    "DOC-003",
    "DOC-004",
    "DOC-034",
    "DOC-016",
    "DOC-017",
    "DOC-005",
    "DOC-007",
    "DOC-008",
    "DOC-009",
    "DOC-010",
    "DOC-011",
    "DOC-012",
    "DOC-031",
    "DOC-032",
    "DOC-033",
)
SELARL_FRONT_SUPPORTED_DOC_CODES: Final[tuple[str, ...]] = (
    *SELARL_FRONT_AUTO_DOC_CODES,
    *SELARL_FRONT_RESERVE_DOC_CODES,
    *SELARL_FRONT_MANUAL_DOC_CODES,
)


def selarl_front_conditions(
    *,
    profession: str,
    site_distinct: bool,
    scm_cession: bool,
    regime_communautaire: bool,
    derogation: bool,
    cession: bool,
    cabinet_type: str,
) -> dict[str, Any]:
    normalized_cabinet_type = cabinet_type.strip().lower()
    if not cession:
        normalized_cabinet_type = ""
    return {
        "profession": _normalized_profession(profession),
        "site_distinct": site_distinct,
        "scm_cession": scm_cession,
        "regime_communautaire": regime_communautaire,
        "derogation": derogation,
        "cession": cession,
        "cabinet_type": normalized_cabinet_type,
    }


def selarl_front_expected_documents(
    conditions: dict[str, Any],
) -> tuple[ExpectedDocument, ...]:
    return tuple(
        get_expected_documents(
            CaseInput(
                case_type=CaseType.SELARL,
                conditions=conditions,
            )
        )
    )


def selarl_front_document_codes(conditions: dict[str, Any]) -> tuple[str, ...]:
    return _dedupe(
        document.document_code
        for document in selarl_front_expected_documents(conditions)
        if document.document_code
    )


def selarl_front_auto_doc_codes(conditions: dict[str, Any]) -> tuple[str, ...]:
    selected = set(selarl_front_document_codes(conditions))
    return tuple(code for code in SELARL_FRONT_AUTO_DOC_CODES if code in selected)


def selarl_front_excluded_doc_codes(conditions: dict[str, Any]) -> tuple[str, ...]:
    selected = set(selarl_front_document_codes(conditions))
    return tuple(
        code
        for code in (*SELARL_FRONT_RESERVE_DOC_CODES, *SELARL_FRONT_MANUAL_DOC_CODES)
        if code in selected
    )


def selarl_front_manual_without_code_labels(conditions: dict[str, Any]) -> tuple[str, ...]:
    return tuple(
        document.document_label
        for document in selarl_front_expected_documents(conditions)
        if document.document_code is None
        and document.availability is DocumentAvailability.MANUAL_ONLY
    )


def selarl_front_requirement(doc_code: str) -> DocumentRequirementRecord:
    if doc_code == "DOC-016":
        return _statuts_dentiste_requirement()
    if doc_code in {"DOC-005", "DOC-006"}:
        return _regime_communautaire_requirement(doc_code)
    if doc_code in SELARL_FRONT_COMPLEX_PENDING_DOC_CODES:
        return _complex_pending_requirement(doc_code)
    if doc_code in {"DOC-034", "DOC-017", "DOC-033", "DOC-009"}:
        return sentinel_requirement(doc_code)
    return unit_document_requirement(doc_code)


def selarl_front_requirements(
    conditions: dict[str, Any],
) -> tuple[DocumentRequirementRecord, ...]:
    return tuple(
        selarl_front_requirement(code)
        for code in selarl_front_document_codes(conditions)
        if code in SELARL_FRONT_SUPPORTED_DOC_CODES
    )


def _statuts_dentiste_requirement() -> DocumentRequirementRecord:
    medecin_requirement = sentinel_requirement("DOC-017")
    return replace(
        medecin_requirement,
        doc_code="DOC-016",
        doc_label="Statuts SELARL chirurgien-dentiste",
        action_needed=(
            "Structurer capital, repartition, banque, ordre dentiste et seuils "
            "sans deduction."
        ),
    )


def _regime_communautaire_requirement(doc_code: str) -> DocumentRequirementRecord:
    label = (
        "Lettre de renonciation a revendiquer la qualite d'associe"
        if doc_code == "DOC-005"
        else "Lettre d'avertissement au conjoint en cas d'apport d'un bien commun"
    )
    return DocumentRequirementRecord(
        doc_code=doc_code,
        doc_label=label,
        required_roles=(BusinessRole.SIGNATAIRE, BusinessRole.CONJOINT),
        required_entities=(BusinessRole.SOCIETE_PRINCIPALE, BusinessRole.CONJOINT),
        required_canonical_fields=(
            "apport.numeraire.montant",
            "apport.numeraire.montant_lettres",
            "regime_communautaire.regime_matrimonial",
            "regime_communautaire.qualite_renoncee",
            "regime_communautaire.date_courrier_avertissement",
            "regime_communautaire.renonciation.lieu_signature",
            "regime_communautaire.renonciation.date_signature",
            "regime_communautaire.renonciation.nombre_exemplaires_lettres",
            "regime_communautaire.avertissement.date_signature",
            "personne.conjoint.civilite_affichage",
            "personne.conjoint.prenom",
            "personne.conjoint.nom",
            "personne.conjoint.adresse_personnelle",
        ),
        target_screen_blocks=("regime_communautaire", "capital_associes", "generation"),
        verdict="ORANGE",
        action_needed="Saisir conjoint, apport commun et dates de courrier/renonciation.",
    )


def _complex_pending_requirement(doc_code: str) -> DocumentRequirementRecord:
    base = unit_document_requirement(doc_code)
    return replace(
        base,
        status=DocumentRequirementStatus.CONTEXT_INCOMPLETE,
        action_needed=(
            "Document attendu par la SELARL complete, mais le sous-formulaire "
            "metier detaille reste a brancher avant generation utilisateur."
        ),
    )


def _normalized_profession(value: str) -> str:
    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in {"dentiste", "chirurgien_dentiste"}:
        return "chirurgien_dentiste"
    return "medecin"


def _dedupe(values: Any) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))
