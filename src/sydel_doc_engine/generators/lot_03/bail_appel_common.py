from __future__ import annotations

from datetime import date

from sydel_doc_engine.domain.models import CessionContext, DocumentGenerationContext
from sydel_doc_engine.generators.lot_05.spfpl_libelles import libelle_metier

DOCUMENT_CODE = "CODE-BAIL-APP-001"

SELARL_STRUCTURE = "SELARL"
SELAS_STRUCTURE = "SELAS"
SUPPORTED_BAIL_STRUCTURES = {SELARL_STRUCTURE, SELAS_STRUCTURE}

CABINET_DENTAIRE = "dentaire"
CABINET_MEDICAL = "medical"
SUPPORTED_CABINET_TYPES = {CABINET_DENTAIRE, CABINET_MEDICAL}


def required_text(value: str | None, field_name: str) -> str:
    # R10 (Rafael 2026-06-24) : une donnee manquante NE bloque PAS la generation -> on ecrit un
    # marqueur visible « (A COMPLETER : data) » SANS crochets (pour ne pas declencher le garde-fou
    # anti-placeholder source qui interdit les [ ]) au lieu de lever.
    if value is None or not value.strip():
        return f"(À COMPLÉTER : {libelle_metier(field_name)})"
    return value.strip()


def format_display_date(value: date | str | None, field_name: str) -> str:
    # KAN-2 @All : date absente -> marqueur metier, jamais lever.
    if value is None:
        return required_text(None, field_name)
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return required_text(value, field_name)


def required_cession(ctx: DocumentGenerationContext) -> CessionContext:
    if ctx.cession is None:
        raise ValueError(f"cession est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.cession


def required_structure(ctx: DocumentGenerationContext) -> str:
    return required_text(ctx.structure, "dossier.structure")


def require_cession_enabled(ctx: DocumentGenerationContext) -> None:
    if ctx.dossier_options is None or not ctx.dossier_options.cession:
        raise ValueError(f"dossier.options.cession doit etre vrai pour {DOCUMENT_CODE}.")


def cabinet_type(ctx: DocumentGenerationContext) -> str:
    cession = required_cession(ctx)
    value = required_text(cession.type_cabinet, "cession.type_cabinet").lower()
    if value not in SUPPORTED_CABINET_TYPES:
        supported = ", ".join(sorted(SUPPORTED_CABINET_TYPES))
        raise ValueError(
            f"cession.type_cabinet doit etre dans [{supported}] pour {DOCUMENT_CODE}."
        )
    return value


def validate_avenant_context(ctx: DocumentGenerationContext) -> None:
    structure = required_structure(ctx)
    if structure not in SUPPORTED_BAIL_STRUCTURES:
        supported = ", ".join(sorted(SUPPORTED_BAIL_STRUCTURES))
        raise ValueError(f"dossier.structure doit etre dans [{supported}] pour {DOCUMENT_CODE}.")
    require_cession_enabled(ctx)
    cabinet_type(ctx)


def validate_appel_fonds_context(ctx: DocumentGenerationContext) -> None:
    structure = required_structure(ctx)
    if structure != SELARL_STRUCTURE:
        raise ValueError(
            f"dossier.structure doit etre {SELARL_STRUCTURE} pour l'appel de fonds "
            f"{DOCUMENT_CODE}."
        )
    require_cession_enabled(ctx)
    # L'appel de fonds est un document COMMUN a toute cession (section « Si cession »
    # des Documents a generer par cas) : medical comme dentaire. On valide donc seulement
    # que le type de cabinet est connu et supporte, sans le restreindre au dentaire.
    cabinet_type(ctx)
