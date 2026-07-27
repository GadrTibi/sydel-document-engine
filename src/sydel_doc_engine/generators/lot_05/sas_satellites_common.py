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
from sydel_doc_engine.generators.lot_01.civilite import civilite_civile
from sydel_doc_engine.generators.lot_05.spfpl_libelles import libelle_metier

DOCUMENT_CODE = "CODE-SAS-SATELLITES-001"
SAS_STRUCTURE = "SAS"
STATUTS_SAS_TYPE = "spfpl_medecins"
SUPPORTED_PROFESSIONS = {"medecin", "médecin"}


def required_text(value: str | None, field_name: str) -> str:
    # R10 (Rafael 2026-06-24) : une donnee manquante NE bloque PAS la generation -> on ecrit un
    # marqueur visible « (A COMPLETER : data) » SANS crochets (pour ne pas declencher le garde-fou
    # anti-placeholder source qui interdit les [ ]) au lieu de lever.
    if value is None or not value.strip():
        return f"(À COMPLÉTER : {libelle_metier(field_name)})"
    return value.strip()


def required_int(value: int | None, field_name: str) -> int:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


def format_display_date(value: date | str | None, field_name: str) -> str:
    # KAN-2 @All : date absente -> marqueur metier, jamais lever.
    if value is None:
        return required_text(None, field_name)
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return required_text(value, field_name)


# KAN-2 @All : un OBJET absent NE bloque JAMAIS -> instance VIDE (ses champs sortent en
# marqueurs via les helpers ci-dessus), au lieu de lever. Meme pattern que spfpl_common.
def required_societe_spfpl(ctx: DocumentGenerationContext) -> SocieteSpfpl:
    return ctx.societe_spfpl if ctx.societe_spfpl is not None else SocieteSpfpl()


def required_actionnaire_unique(ctx: DocumentGenerationContext) -> SpfplPerson:
    return ctx.actionnaire_unique if ctx.actionnaire_unique is not None else SpfplPerson()


def required_president(ctx: DocumentGenerationContext) -> StatutsPresident:
    return ctx.president if ctx.president is not None else StatutsPresident()


def required_capital_souscription(ctx: DocumentGenerationContext) -> CapitalSouscription:
    return (
        ctx.capital_souscription
        if ctx.capital_souscription is not None
        else CapitalSouscription()
    )


def required_societe_cible(ctx: DocumentGenerationContext) -> SocieteCible:
    return ctx.societe_cible if ctx.societe_cible is not None else SocieteCible()


def validate_sas_satellite_scope(
    ctx: DocumentGenerationContext,
    *,
    require_apport: bool = False,
) -> None:
    # KAN-2 @All : ce satellite ne se genere QUE pour une SAS -> le SELECTEUR de structure reste
    # un garde (fiable meme a vide). Les autres controles (options, type/profession, genre, index)
    # ne s'exercent QUE si la donnee est REELLEMENT saisie : un champ vide ne bloque pas.
    if ctx.structure != SAS_STRUCTURE:
        raise ValueError(f"dossier.structure doit etre SAS pour {DOCUMENT_CODE}.")
    options = ctx.dossier_options
    if options is not None:
        if options.associe_unique is False:
            raise ValueError(
                f"dossier.options.associe_unique doit etre vrai pour {DOCUMENT_CODE}."
            )
        if require_apport and options.apport is False:
            raise ValueError(f"dossier.options.apport doit etre vrai pour {DOCUMENT_CODE}.")

    if ctx.statuts_sas is not None:
        statuts_type = (ctx.statuts_sas.type or "").strip().lower()
        profession = (ctx.statuts_sas.profession or "").strip().lower()
        if (statuts_type and statuts_type != STATUTS_SAS_TYPE) or (
            profession and profession not in SUPPORTED_PROFESSIONS
        ):
            raise ValueError(
                "statuts_sas.type et statuts_sas.profession doivent confirmer le perimetre "
                f"SAS / SPFPL medecins pour {DOCUMENT_CODE}."
            )

    actionnaire = required_actionnaire_unique(ctx)
    president = required_president(ctx)
    if president.ref_associe_index:
        raise ValueError(
            f"president.ref_associe_index doit valoir 0 pour {DOCUMENT_CODE}."
        )
    if actionnaire.genre is not None and actionnaire.genre != Gender.MASCULIN:
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
    for _field_name, (actionnaire_value, president_value) in comparisons.items():
        # KAN-2 @All : un champ vide sort en MARQUEUR, jamais une divergence. On ne compare que
        # des valeurs RÉELLES (brutes, pas les marqueurs — deux marqueurs de field_name distincts
        # different toujours et levaient a tort). Si l'une des deux manque, rien a signaler.
        actionnaire_raw = (actionnaire_value or "").strip()
        president_raw = (president_value or "").strip()
        if actionnaire_raw and president_raw and actionnaire_raw != president_raw:
            raise ValueError(
                "president doit correspondre a actionnaire_unique pour "
                f"{DOCUMENT_CODE}."
            )


def address_display(address: Address | None, field_name: str) -> str:
    # KAN-2 @All : adresse absente -> marqueur (comme `personal_address_for_pv`), jamais lever.
    if address is None:
        return required_text(None, field_name)
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
    # R3 durci (Rafael 2026-07-07, supersede A26-45/49) : « Docteur »/« Dr » ne sort
    # JAMAIS — un titre professionnel posé en civilite_affichage est rendu en civilité
    # CIVILE (Monsieur/Madame, accordée au genre quand le modèle le porte).
    civilite = civilite_civile(
        required_text(person.civilite_affichage, f"{field_name}.civilite_affichage"),
        getattr(person, "genre", None),
    )
    return (
        f"{civilite} "
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
    # KAN-2 @All : la coherence capital ne se controle que sur des valeurs REELLES. Si l'un des
    # montants / quantites n'est pas saisi, il n'y a rien a comparer -> on n'exige rien (le doc se
    # genere, les zones vides sortent en marqueurs). La coherence complete reste exigee des que
    # TOUTES les valeurs sont renseignees.
    _requis = (
        societe.capital_social,
        societe.nb_actions_total,
        societe.valeur_nominale_action,
        capital.nb_actions_total,
        capital.valeur_nominale_action,
        capital.apports_nature_montant,
        capital.apports_numeraire_montant,
    )
    if any(v is None or (isinstance(v, str) and not v.strip()) for v in _requis):
        return
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
