from __future__ import annotations

from datetime import date
from typing import Any

from sydel_doc_engine.front_app.dossier_selection import DossierTypeOption
from sydel_doc_engine.front_app.field_derivations import (
    DEFAULT_MANDATAIRE_CABINET,
    DEFAULT_MANDATAIRE_CIVILITE,
    DEFAULT_MANDATAIRE_FONCTION,
    DEFAULT_MANDATAIRE_NOM,
    DEFAULT_MANDATAIRE_PRENOM,
    DEFAULT_PRESTATAIRE_SIGNATURE_ELECTRONIQUE,
    DEFAULT_SEUIL_ACHAT_MATERIEL,
    DEFAULT_SEUIL_EMPRUNT,
    DEFAULT_TITRE_AFFICHAGE,
    calculate_nominal_value,
    date_to_french_words,
    derive_gender_from_civilite,
    format_numeric_value,
    number_words_from_value,
    parse_french_date,
    regime_matrimonial_from_status,
)
from sydel_doc_engine.front_app.selarl_slice import SelarlSliceInput

CleanDataEntry = SelarlSliceInput

_NUMERIC_TEXT_FIELDS = (
    "capital_social",
    "valeur_nominale_part",
    "seuil_achat_materiel",
    "seuil_emprunt",
)
_DATE_FIELDS = (
    "date_naissance",
    "signature_date",
    "decision_date",
    "date_courrier_avertissement",
)


def build_clean_data_entry(
    dossier_type: DossierTypeOption,
    **values: Any,
) -> CleanDataEntry:
    normalized = dict(values)

    legacy_company_label = normalized.pop("company_label", "")
    normalized.pop("client_label", None)
    normalized.pop("internal_note", None)
    if legacy_company_label and not normalized.get("denomination"):
        normalized["denomination"] = legacy_company_label
    for legacy_conjoint_address_key in (
        "conjoint_adresse_num_voie",
        "conjoint_adresse_voie",
        "conjoint_adresse_cp",
        "conjoint_adresse_ville",
    ):
        normalized.pop(legacy_conjoint_address_key, None)

    for key, value in tuple(normalized.items()):
        if isinstance(value, str):
            normalized[key] = value.strip()
    for key in _NUMERIC_TEXT_FIELDS:
        if key in normalized:
            normalized[key] = format_numeric_value(normalized[key])
    for key in _DATE_FIELDS:
        if key in normalized:
            normalized[key] = parse_french_date(normalized[key])

    _derive_hidden_values(normalized)

    return CleanDataEntry(
        dossier_type_key=dossier_type.key,
        **normalized,
    )


def _derive_hidden_values(values: dict[str, Any]) -> None:
    _set_default(values, "genre", derive_gender_from_civilite(str(values.get("civilite", ""))))
    _set_default(
        values,
        "conjoint_genre",
        derive_gender_from_civilite(str(values.get("conjoint_civilite", "Madame"))),
    )
    _set_default(values, "titre_affichage", DEFAULT_TITRE_AFFICHAGE)
    values["valeur_nominale_part"] = calculate_nominal_value(
        values.get("capital_social"),
        values.get("nb_parts_total"),
    )
    _set_default(
        values,
        "capital_social_lettres",
        number_words_from_value(values.get("capital_social")),
    )
    _set_default(
        values,
        "nb_parts_total_lettres",
        number_words_from_value(values.get("nb_parts_total")),
    )
    _set_default(
        values,
        "valeur_nominale_part_lettres",
        number_words_from_value(values.get("valeur_nominale_part")),
    )
    _set_default(
        values,
        "regime_matrimonial",
        regime_matrimonial_from_status(
            str(values.get("situation_maritale", "")),
            bool(values.get("regime_communautaire")),
        ),
    )
    _set_default(values, "reunion_date_lettres", date_to_french_words(values.get("decision_date")))

    values["duree"] = "99 ans"
    values["signature_nombre_exemplaires"] = "4"
    values["qualite_renoncee"] = "associé"

    exemplaires_words = number_words_from_value(values.get("signature_nombre_exemplaires"))
    if exemplaires_words:
        values["signature_nombre_exemplaires"] = exemplaires_words

    _set_default(values, "mandataire_civilite", DEFAULT_MANDATAIRE_CIVILITE)
    _set_default(values, "mandataire_prenom", DEFAULT_MANDATAIRE_PRENOM)
    _set_default(values, "mandataire_nom", DEFAULT_MANDATAIRE_NOM)
    _set_default(values, "mandataire_fonction", DEFAULT_MANDATAIRE_FONCTION)
    _set_default(values, "mandataire_cabinet", DEFAULT_MANDATAIRE_CABINET)
    _set_default(
        values,
        "prestataire_signature_electronique",
        DEFAULT_PRESTATAIRE_SIGNATURE_ELECTRONIQUE,
    )
    _set_default(values, "seuil_achat_materiel", DEFAULT_SEUIL_ACHAT_MATERIEL)
    _set_default(values, "seuil_emprunt", DEFAULT_SEUIL_EMPRUNT)

    if values.get("regime_communautaire"):
        values["date_courrier_avertissement"] = date.today()
    else:
        values["date_courrier_avertissement"] = None


def _set_default(values: dict[str, Any], key: str, default: Any) -> None:
    value = values.get(key)
    if value is None or (isinstance(value, str) and not value.strip()):
        values[key] = default
