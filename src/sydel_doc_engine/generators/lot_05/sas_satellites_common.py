from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    CapitalSouscription,
    DocumentGenerationContext,
    SocieteCible,
    SocieteSpfpl,
    SpfplPerson,
    StatutsPresident,
)

DOCUMENT_CODE = "CODE-SAS-SATELLITES-001"
SAS_STRUCTURE = "SAS"
STATUTS_SAS_TYPE = "spfpl_medecins"
SUPPORTED_PROFESSIONS = {"medecin", "médecin"}


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


def required_actionnaire_unique(ctx: DocumentGenerationContext) -> SpfplPerson:
    if ctx.actionnaire_unique is None:
        raise ValueError(f"actionnaire_unique est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.actionnaire_unique


def required_president(ctx: DocumentGenerationContext) -> StatutsPresident:
    if ctx.president is None:
        raise ValueError(f"president est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.president


def required_capital_souscription(ctx: DocumentGenerationContext) -> CapitalSouscription:
    if ctx.capital_souscription is None:
        raise ValueError(f"capital_souscription est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.capital_souscription


def required_societe_cible(ctx: DocumentGenerationContext) -> SocieteCible:
    if ctx.societe_cible is None:
        raise ValueError(f"societe_cible est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.societe_cible


def validate_sas_satellite_scope(
    ctx: DocumentGenerationContext,
    *,
    require_apport: bool = False,
) -> None:
    if ctx.structure != SAS_STRUCTURE:
        raise ValueError(f"dossier.structure doit etre SAS pour {DOCUMENT_CODE}.")
    if ctx.dossier_options is None:
        raise ValueError(f"dossier.options est obligatoire pour {DOCUMENT_CODE}.")
    if not ctx.dossier_options.associe_unique:
        raise ValueError(
            f"dossier.options.associe_unique doit etre vrai pour {DOCUMENT_CODE}."
        )
    if require_apport and not ctx.dossier_options.apport:
        raise ValueError(f"dossier.options.apport doit etre vrai pour {DOCUMENT_CODE}.")

    if ctx.statuts_sas is None:
        raise ValueError(f"statuts_sas est obligatoire pour {DOCUMENT_CODE}.")
    statuts_type = required_text(ctx.statuts_sas.type, "statuts_sas.type").lower()
    profession = required_text(ctx.statuts_sas.profession, "statuts_sas.profession").lower()
    if statuts_type != STATUTS_SAS_TYPE or profession not in SUPPORTED_PROFESSIONS:
        raise ValueError(
            "statuts_sas.type et statuts_sas.profession doivent confirmer le perimetre "
            f"SAS / SPFPL medecins pour {DOCUMENT_CODE}."
        )

    actionnaire = required_actionnaire_unique(ctx)
    president = required_president(ctx)
    if president.ref_associe_index != 0:
        raise ValueError(
            f"president.ref_associe_index doit valoir 0 pour {DOCUMENT_CODE}."
        )
    if actionnaire.genre != Gender.MASCULIN:
        raise ValueError(
            "Le wording source SAS satellites V1 ne couvre que le president masculin "
            f"pour {DOCUMENT_CODE}."
        )
    validate_president_is_actionnaire_unique(actionnaire, president)


def validate_president_is_actionnaire_unique(
    actionnaire: SpfplPerson,
    president: StatutsPresident,
) -> None:
    comparisons = {
        "civilite_affichage": (actionnaire.civilite_affichage, president.civilite_affichage),
        "prenom": (actionnaire.prenom, president.prenom),
        "nom": (actionnaire.nom, president.nom),
    }
    for field_name, (actionnaire_value, president_value) in comparisons.items():
        if required_text(actionnaire_value, f"actionnaire_unique.{field_name}") != required_text(
            president_value,
            f"president.{field_name}",
        ):
            raise ValueError(
                "president doit correspondre a actionnaire_unique pour "
                f"{DOCUMENT_CODE}."
            )


def address_display(address: Address | None, field_name: str) -> str:
    if address is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if address.adresse_affichee:
        return address.adresse_affichee.strip()
    return (
        f"{required_text(address.num_voie, f'{field_name}.num_voie')} "
        f"{required_text(address.voie, f'{field_name}.voie')}, "
        f"{required_text(address.cp, f'{field_name}.cp')} "
        f"{required_text(address.ville, f'{field_name}.ville')}"
    )


def personal_address_for_pv(person: SpfplPerson, field_name: str) -> str:
    address = person.adresse_personnelle
    if address is None:
        return required_text(
            person.adresse_personnelle_affichee,
            f"{field_name}.adresse_personnelle_affichee",
        )
    if address.adresse_affichee:
        return address.adresse_affichee.strip()
    return (
        f"{required_text(address.num_voie, f'{field_name}.adresse_personnelle.num_voie')} "
        f"{required_text(address.voie, f'{field_name}.adresse_personnelle.voie')}, "
        f"{required_text(address.ville, f'{field_name}.adresse_personnelle.ville')} "
        f"{required_text(address.cp, f'{field_name}.adresse_personnelle.cp')}"
    )


def person_name(person: SpfplPerson | StatutsPresident, field_name: str) -> str:
    return (
        f"{required_text(person.civilite_affichage, f'{field_name}.civilite_affichage')} "
        f"{required_text(person.prenom, f'{field_name}.prenom')} "
        f"{required_text(person.nom, f'{field_name}.nom')}"
    )


def person_signature(person: SpfplPerson | StatutsPresident, field_name: str) -> str:
    return (
        f"{required_text(person.prenom, f'{field_name}.prenom')} "
        f"{required_text(person.nom, f'{field_name}.nom')}"
    )


def euro_amount(value: str | None, field_name: str) -> Decimal:
    raw_value = required_text(value, field_name)
    normalized = (
        raw_value.lower()
        .replace("euros", "")
        .replace("euro", "")
        .replace("€", "")
        .replace("\u00a0", "")
        .replace(" ", "")
        .replace(",", ".")
        .strip()
    )
    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError(
            f"{field_name} doit etre un montant numerique pour {DOCUMENT_CODE}."
        ) from exc


def validate_capital_consistency(
    societe: SocieteSpfpl,
    capital: CapitalSouscription,
) -> None:
    capital_social = euro_amount(societe.capital_social, "societe_spfpl.capital_social")
    nb_actions_societe = required_int(
        societe.nb_actions_total,
        "societe_spfpl.nb_actions_total",
    )
    nb_actions_capital = required_int(
        capital.nb_actions_total,
        "capital_souscription.nb_actions_total",
    )
    if nb_actions_societe != nb_actions_capital:
        raise ValueError(
            "capital_souscription.nb_actions_total doit etre coherent avec "
            f"societe_spfpl.nb_actions_total pour {DOCUMENT_CODE}."
        )

    valeur_societe = euro_amount(
        societe.valeur_nominale_action,
        "societe_spfpl.valeur_nominale_action",
    )
    valeur_capital = euro_amount(
        capital.valeur_nominale_action,
        "capital_souscription.valeur_nominale_action",
    )
    if valeur_societe != valeur_capital:
        raise ValueError(
            "capital_souscription.valeur_nominale_action doit etre coherente avec "
            f"societe_spfpl.valeur_nominale_action pour {DOCUMENT_CODE}."
        )
    if valeur_capital * Decimal(nb_actions_capital) != capital_social:
        raise ValueError(
            "Le nombre d'actions et la valeur nominale doivent correspondre au capital "
            f"social pour {DOCUMENT_CODE}."
        )

    apports_total = euro_amount(
        capital.apports_nature_montant,
        "capital_souscription.apports_nature_montant",
    ) + euro_amount(
        capital.apports_numeraire_montant,
        "capital_souscription.apports_numeraire_montant",
    )
    if apports_total != capital_social:
        raise ValueError(
            "Les apports en nature et en numeraire doivent correspondre au capital "
            f"social pour {DOCUMENT_CODE}."
        )
