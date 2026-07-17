from __future__ import annotations

from datetime import date

from sydel_doc_engine.domain.models import (
    Address,
    Apport,
    Company,
    DocumentGenerationContext,
    RegimeCommunautaire,
)
from sydel_doc_engine.generators.lot_05.spfpl_libelles import libelle_metier

DOCUMENT_CODE = "CODE-RC-001"

SELARL_STRUCTURE = "SELARL"
SELAS_STRUCTURE = "SELAS"
# SCS4 (Albane 2026-06-25) : la SCS reprend le bloc regime matrimonial de la SELAS
# pluri -> elle peut emettre le couple regime (DOC-005/006) per-associe marie.
SCS_STRUCTURE = "SCS"
SPFPL_CESSION_STRUCTURES = {"SPFPL cession", "SPFPL_CESSION"}
SPFPL_APPORT_STRUCTURES = {"SPFPL apport", "SPFPL_APPORT"}
SUPPORTED_STRUCTURES = (
    {SELARL_STRUCTURE, SELAS_STRUCTURE, SCS_STRUCTURE}
    | SPFPL_CESSION_STRUCTURES
    | SPFPL_APPORT_STRUCTURES
)


def validate_batch_enabled(ctx: DocumentGenerationContext) -> str:
    structure = required_text(ctx.structure, "dossier.structure")
    if structure not in SUPPORTED_STRUCTURES:
        supported = ", ".join(sorted(SUPPORTED_STRUCTURES))
        raise ValueError(f"dossier.structure doit etre dans [{supported}] pour {DOCUMENT_CODE}.")
    if ctx.dossier_options is None or not ctx.dossier_options.regime_communautaire:
        raise ValueError(
            f"dossier.options.regime_communautaire doit etre vrai pour {DOCUMENT_CODE}."
        )
    return structure


def required_text(value: str | None, field_name: str) -> str:
    # R10 (Rafael 2026-06-24) : une donnee manquante NE bloque PAS la generation -> on ecrit un
    # marqueur visible « (A COMPLETER : data) » SANS crochets (pour ne pas declencher le garde-fou
    # anti-placeholder source qui interdit les [ ]) au lieu de lever.
    if value is None or not value.strip():
        return f"(À COMPLÉTER : {libelle_metier(field_name)})"
    return value.strip()


def required_company(company: Company | None) -> Company:
    if company is None:
        raise ValueError(f"societe est obligatoire pour {DOCUMENT_CODE}.")
    return company


def required_apport(apport: Apport | None) -> Apport:
    if apport is None:
        raise ValueError(f"apport est obligatoire pour {DOCUMENT_CODE}.")
    return apport


def required_regime_communautaire(
    regime_communautaire: RegimeCommunautaire | None,
) -> RegimeCommunautaire:
    if regime_communautaire is None:
        raise ValueError(f"regime_communautaire est obligatoire pour {DOCUMENT_CODE}.")
    return regime_communautaire


def format_display_date(value: date | str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return required_text(value, field_name)


def company_capital_social(company: Company) -> str:
    return required_text(company.capital_social or company.capital, "societe.capital_social")


def company_forme_sociale(company: Company) -> str:
    return required_text(
        company.forme_sociale or company.forme_sociale_affichage,
        "societe.forme_sociale",
    )


def company_forme_sociale_complete(company: Company) -> str:
    return required_text(
        company.forme_sociale_complete or company.forme_sociale_libelle_long,
        "societe.forme_sociale_complete",
    )


def company_forme_sociale_abregee(company: Company) -> str:
    return required_text(company.forme_sociale_abregee, "societe.forme_sociale_abregee")


def required_address(address: Address | None, field_name: str) -> Address:
    if address is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    required_text(address.num_voie, f"{field_name}.num_voie")
    required_text(address.voie, f"{field_name}.voie")
    required_text(address.cp, f"{field_name}.cp")
    required_text(address.ville, f"{field_name}.ville")
    return address


def street_line(address: Address) -> str:
    return (
        f"{required_text(address.num_voie, 'adresse.num_voie')} "
        f"{required_text(address.voie, 'adresse.voie')}"
    )


def city_line(address: Address) -> str:
    return (
        f"{required_text(address.cp, 'adresse.cp')} "
        f"{required_text(address.ville, 'adresse.ville')}"
    )


def siege_social_inline(address: Address) -> str:
    """Adresse du siege sur UNE seule ligne, prefixee « Siège social : » (A2).

    Albane 2026-06-26 : dans l'entete societe des lettres de regime communautaire,
    l'adresse doit etre sur une seule ligne precedee de « Siège social : », comme
    dans le PV (qui compose « Siège social : <num voie cp ville> »), et SANS la
    mention « en cours d'immatriculation »."""
    num_voie = (address.num_voie or "").strip()
    voie = required_text(address.voie, "adresse.voie")
    cp = required_text(address.cp, "adresse.cp")
    ville = required_text(address.ville, "adresse.ville")
    inline = f"{num_voie} {voie} {cp} {ville}".strip()
    return f"Siège social : {inline}"
