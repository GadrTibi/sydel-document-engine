from __future__ import annotations

from datetime import date

from sydel_doc_engine.domain.models import (
    AssocieCible,
    CessionParts,
    DocumentGenerationContext,
    SocieteCible,
    SocieteSpfpl,
    SpfplPerson,
)

DOCUMENT_CODE = "CODE-SPFPL-AGR-INFO-001"

SPFPL_CESSION_STRUCTURE = "SPFPL cession"
SPFPL_APPORT_STRUCTURE = "SPFPL apport"
OPERATION_CESSION = "cession"
OPERATION_APPORT = "apport"
SUPPORTED_NOTE_OPERATIONS = {OPERATION_CESSION, OPERATION_APPORT}


def required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value.strip()


def required_int(value: int | None, field_name: str) -> int:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


def format_display_date(value: date | str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return required_text(value, field_name)


def required_societe_spfpl(ctx: DocumentGenerationContext) -> SocieteSpfpl:
    if ctx.societe_spfpl is None:
        raise ValueError(f"societe_spfpl est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.societe_spfpl


def required_societe_cible(ctx: DocumentGenerationContext) -> SocieteCible:
    if ctx.societe_cible is None:
        raise ValueError(f"societe_cible est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.societe_cible


def required_cedant(ctx: DocumentGenerationContext) -> SpfplPerson:
    if ctx.cedant is None:
        raise ValueError(f"cedant est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.cedant


def required_apporteur(ctx: DocumentGenerationContext) -> SpfplPerson:
    if ctx.apporteur is None:
        raise ValueError(f"apporteur est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.apporteur


def required_cession_parts(ctx: DocumentGenerationContext) -> CessionParts:
    if ctx.cession_parts is None:
        raise ValueError(f"cession_parts est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.cession_parts


def validate_cession_context(ctx: DocumentGenerationContext) -> None:
    if ctx.structure != SPFPL_CESSION_STRUCTURE:
        raise ValueError(
            f"dossier.structure doit etre {SPFPL_CESSION_STRUCTURE} pour {DOCUMENT_CODE}."
        )
    if ctx.dossier_options is None or not ctx.dossier_options.cession:
        raise ValueError(f"dossier.options.cession doit etre vrai pour {DOCUMENT_CODE}.")
    operation_type = operation_spfpl_type(ctx)
    if operation_type != OPERATION_CESSION:
        raise ValueError(
            "operation_spfpl.type doit etre cession pour les PV d'agrement "
            f"{DOCUMENT_CODE}."
        )


def validate_associe_unique(ctx: DocumentGenerationContext, expected: bool) -> None:
    if ctx.dossier_options is None:
        raise ValueError(f"dossier.options est obligatoire pour {DOCUMENT_CODE}.")
    if ctx.dossier_options.associe_unique is not expected:
        attendu = "vrai" if expected else "faux"
        raise ValueError(
            f"dossier.options.associe_unique doit etre {attendu} pour {DOCUMENT_CODE}."
        )


def operation_spfpl_type(ctx: DocumentGenerationContext) -> str:
    if ctx.operation_spfpl is None:
        raise ValueError(f"operation_spfpl est obligatoire pour {DOCUMENT_CODE}.")
    operation_type = required_text(ctx.operation_spfpl.type, "operation_spfpl.type").lower()
    if operation_type not in SUPPORTED_NOTE_OPERATIONS:
        supported = ", ".join(sorted(SUPPORTED_NOTE_OPERATIONS))
        raise ValueError(
            f"operation_spfpl.type doit etre dans [{supported}] pour {DOCUMENT_CODE}."
        )
    return operation_type


def operation_party(ctx: DocumentGenerationContext) -> SpfplPerson:
    if operation_spfpl_type(ctx) == OPERATION_CESSION:
        return required_cedant(ctx)
    return required_apporteur(ctx)


def validate_note_context(ctx: DocumentGenerationContext) -> str:
    operation_type = operation_spfpl_type(ctx)
    if operation_type == OPERATION_CESSION:
        if ctx.structure != SPFPL_CESSION_STRUCTURE:
            raise ValueError(
                f"dossier.structure doit etre {SPFPL_CESSION_STRUCTURE} pour la note "
                f"{DOCUMENT_CODE}."
            )
        if ctx.dossier_options is None or not ctx.dossier_options.cession:
            raise ValueError(f"dossier.options.cession doit etre vrai pour {DOCUMENT_CODE}.")
    else:
        if ctx.structure != SPFPL_APPORT_STRUCTURE:
            raise ValueError(
                f"dossier.structure doit etre {SPFPL_APPORT_STRUCTURE} pour la note "
                f"{DOCUMENT_CODE}."
            )
        if ctx.dossier_options is None or not ctx.dossier_options.apport:
            raise ValueError(f"dossier.options.apport doit etre vrai pour {DOCUMENT_CODE}.")
    return operation_type


def person_display(person: SpfplPerson, field_name: str) -> str:
    return (
        f"{required_text(person.civilite_affichage, f'{field_name}.civilite_affichage')} "
        f"{required_text(person.prenom, f'{field_name}.prenom')} "
        f"{required_text(person.nom, f'{field_name}.nom')}"
    )


def person_signature(person: SpfplPerson, field_name: str) -> str:
    return (
        f"{required_text(person.prenom, f'{field_name}.prenom')} "
        f"{required_text(person.nom, f'{field_name}.nom')}"
    )


def company_siege_display(societe: SocieteSpfpl | SocieteCible, field_name: str) -> str:
    if societe.siege is None:
        raise ValueError(f"{field_name}.siege est obligatoire pour {DOCUMENT_CODE}.")
    if societe.siege.adresse_affichee:
        return societe.siege.adresse_affichee.strip()
    parts = [
        required_text(societe.siege.num_voie, f"{field_name}.siege.num_voie"),
        required_text(societe.siege.voie, f"{field_name}.siege.voie"),
        required_text(societe.siege.cp, f"{field_name}.siege.cp"),
        required_text(societe.siege.ville, f"{field_name}.siege.ville"),
    ]
    return f"{parts[0]} {parts[1]}, {parts[2]} {parts[3]}"


def associe_display_name(associe: AssocieCible, field_name: str) -> str:
    if associe.type == "personne_morale":
        return required_text(associe.denomination, f"{field_name}.denomination")
    return (
        f"{required_text(associe.civilite_affichage, f'{field_name}.civilite_affichage')} "
        f"{required_text(associe.prenom, f'{field_name}.prenom')} "
        f"{required_text(associe.nom, f'{field_name}.nom')}"
    )


def associe_signature_name(associe: AssocieCible, field_name: str) -> str:
    if associe.type == "personne_morale":
        return required_text(associe.denomination, f"{field_name}.denomination")
    return (
        f"{required_text(associe.prenom, f'{field_name}.prenom')} "
        f"{required_text(associe.nom, f'{field_name}.nom')}"
    )


def capital_after_lines(ctx: DocumentGenerationContext) -> list[str]:
    societe_cible = required_societe_cible(ctx)
    total = required_int(societe_cible.nb_parts_total, "societe_cible.nb_parts_total")
    if not ctx.associes_cible:
        raise ValueError(f"associes_cible est obligatoire pour {DOCUMENT_CODE}.")

    lines: list[str] = []
    total_after = 0
    for index, associe in enumerate(ctx.associes_cible):
        field_name = f"associes_cible[{index}]"
        nb_parts = required_int(associe.nb_parts_apres, f"{field_name}.nb_parts_apres")
        total_after += nb_parts
        part_label = "part sociale" if nb_parts == 1 else "parts sociales"
        details = (
            f"{associe_display_name(associe, field_name)}, titulaire de "
            f"{nb_parts} {part_label}"
        )
        if associe.numero_part_unique:
            details += f", numerotee {associe.numero_part_unique}"
        elif associe.plage_parts:
            details += f", numerotees de {associe.plage_parts}"
        lines.append(details)

    if total_after != total:
        raise ValueError(
            "La repartition apres operation doit correspondre a "
            f"societe_cible.nb_parts_total pour {DOCUMENT_CODE}."
        )
    return lines


def presence_lines(ctx: DocumentGenerationContext) -> list[str]:
    societe_cible = required_societe_cible(ctx)
    total = required_int(societe_cible.nb_parts_total, "societe_cible.nb_parts_total")
    lines: list[str] = []
    total_present = 0
    for index, associe in enumerate(ctx.associes_cible):
        if not associe.est_present_ou_represente:
            continue
        field_name = f"associes_cible[{index}]"
        nb_parts = required_int(associe.nb_parts_avant, f"{field_name}.nb_parts_avant")
        total_present += nb_parts
        part_label = "part" if nb_parts == 1 else "parts"
        lines.append(
            f"{associe_display_name(associe, field_name)} detenant {nb_parts} {part_label}"
        )

    if not lines:
        raise ValueError(
            "associes_cible presents ou representes est obligatoire pour "
            f"{DOCUMENT_CODE}."
        )
    if total_present != total:
        raise ValueError(
            "Les associes presents ou representes doivent disposer de la totalite des parts "
            f"pour {DOCUMENT_CODE}."
        )
    return lines
