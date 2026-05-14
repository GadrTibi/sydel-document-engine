from __future__ import annotations

from datetime import date

from sydel_doc_engine.domain.models import (
    Company,
    CompanyInscriptionOrdre,
    Contact,
    DerogationContext,
    DerogationRole,
    DocumentGenerationContext,
    Person,
)

DOCUMENT_CODE = "CODE-DEROG-CORE-001"

FORMULAIRE_A_COMPLETER_MODE = "formulaire_a_completer"
MULTI_SITES_SEL = "multi_sites_sel"
CUMUL_SEL_BNC = "cumul_sel_bnc"
SUPPORTED_DEROGATION_STRUCTURES = {"SELARL", "SELAS"}

MANUAL_BLANK = "........................................................"


def required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value.strip()


def format_display_date(value: date | str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return required_text(value, field_name)


def optional_display_date(value: date | str | None) -> str:
    if value is None:
        return MANUAL_BLANK
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return value.strip() or MANUAL_BLANK


def require_derogation_context(
    ctx: DocumentGenerationContext,
    expected_type: str,
) -> DerogationContext:
    if ctx.dossier_options is None or not ctx.dossier_options.derogation:
        raise ValueError(f"dossier.options.derogation doit etre vrai pour {DOCUMENT_CODE}.")
    if ctx.derogation is None:
        raise ValueError(f"derogation est obligatoire pour {DOCUMENT_CODE}.")
    if ctx.derogation.type != expected_type:
        raise ValueError(f"derogation.type doit etre {expected_type} pour {DOCUMENT_CODE}.")
    if ctx.derogation.mode_rendu != FORMULAIRE_A_COMPLETER_MODE:
        raise ValueError(
            "derogation.mode_rendu doit etre formulaire_a_completer pour "
            f"{DOCUMENT_CODE}."
        )
    return ctx.derogation


def require_structure(ctx: DocumentGenerationContext, *, selarl_only: bool = False) -> str:
    structure = required_text(ctx.structure, "dossier.structure")
    supported = {"SELARL"} if selarl_only else SUPPORTED_DEROGATION_STRUCTURES
    if structure not in supported:
        allowed = ", ".join(sorted(supported))
        raise ValueError(f"dossier.structure doit etre dans [{allowed}] pour {DOCUMENT_CODE}.")
    return structure


def require_company(ctx: DocumentGenerationContext) -> Company:
    if ctx.societe is None:
        raise ValueError(f"societe est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.societe


def require_company_inscription(company: Company) -> CompanyInscriptionOrdre:
    if company.inscription_ordre is None:
        raise ValueError(f"societe.inscription_ordre est obligatoire pour {DOCUMENT_CODE}.")
    return company.inscription_ordre


def require_role(role: DerogationRole | None, field_name: str) -> DerogationRole:
    if role is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    required_text(role.prenom, f"{field_name}.prenom")
    required_text(role.nom, f"{field_name}.nom")
    return role


def require_contact(contact: Contact | None, field_name: str) -> Contact:
    if contact is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return contact


def require_person_contact(person: Person) -> Contact:
    return require_contact(person.contact, "personne_signataire.contact")
