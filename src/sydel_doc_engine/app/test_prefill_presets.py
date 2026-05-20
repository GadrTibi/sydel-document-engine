from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class BusinessTestPrefillPreset:
    key: str
    label: str
    case_type: str
    description: str
    widget_values: dict[str, object]


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
    ),
    BusinessTestPrefillPreset(
        key="selarl_dentiste_regime_site",
        label="SELARL chirurgien-dentiste + régime communautaire + site distinct",
        case_type="SELARL",
        description=(
            "Active le regime communautaire, le site distinct et la derogation "
            "pour voir DOC-006 avec reserve ainsi que DOC-013/DOC-014 manuels."
        ),
        widget_values=_selarl_dentiste_regime_site_values(),
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
    ),
    BusinessTestPrefillPreset(
        key="sci_simple",
        label="SCI simple",
        case_type="SCI",
        description="Cas SCI simple pour verifier la non-regression du parcours existant.",
        widget_values=_sci_simple_values(),
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
            "selarl_signataire_is_associe_1",
            "selarl_signataire_is_professional",
        }
    )
)
