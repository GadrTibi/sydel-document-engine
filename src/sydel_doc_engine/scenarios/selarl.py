"""Bibliothèque de scénarios SELARL figés (cas type, données fictives réalistes).

Chaque scénario produit un `SelarlSliceInput` déterministe, passé tel quel au
pipeline validé `front_app.selarl_slice.generate_selarl_dossier`. C'est la
"boussole reproductible" du pack : même scénario + même commit → même documents.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sydel_doc_engine.domain.models import CessionContext
from sydel_doc_engine.front_app.data_entry import build_clean_data_entry
from sydel_doc_engine.front_app.dossier_selection import dossier_type_by_label
from sydel_doc_engine.front_app.selarl_slice import (
    PROFESSION_DENTISTE,
    PROFESSION_MEDECIN,
    SelarlSliceInput,
)

SELARL_DOSSIER_LABEL = "SELARL creation V1"


def _base_kwargs(
    profession: str,
    *,
    regime_communautaire: bool = False,
    married_separation: bool = False,
) -> dict[str, Any]:
    """Données type d'un dossier SELARL unipersonnel (fictives mais réalistes)."""
    is_married = regime_communautaire or married_separation
    kwargs: dict[str, Any] = {
        "dossier_reference": "SCENARIO-SELARL-001",
        "profession": profession,
        "dossier_unipersonnel": True,
        "regime_communautaire": regime_communautaire,
        "civilite": "Monsieur",
        "prenom": "Jean",
        "nom": "Martin",
        "date_naissance": date(1984, 4, 12),
        "ville_naissance": "Paris",
        "departement_naissance": "75",
        "nationalite": "française",
        "nom_pere": "Pierre Martin",
        "nom_mere": "Anne Martin",
        "adresse_num_voie": "10",
        "adresse_voie": "rue Test",
        "adresse_cp": "75001",
        "adresse_ville": "Paris",
        "situation_maritale": "marie" if is_married else "celibataire",
        "regime_matrimonial": (
            "regime de communaute"
            if regime_communautaire
            else "separation de biens"
            if married_separation
            else ""
        ),
        "numero_ordre": "ORD-123",
        "numero_rpps": "10000000001",
        "departement_ordre": "75",
        "denomination": "SELARL MARTIN",
        "capital_social": "1000",
        "nb_parts_total": 100,
        "valeur_nominale_part": "10",
        "siege_num_voie": "20",
        "siege_voie": "avenue du Siege",
        "siege_cp": "75002",
        "siege_ville": "Paris",
        "ville_rcs": "Paris",
        "ordre_adresse_ligne_1": "1 rue de l'Ordre",
        "ordre_cp": "75008",
        "ordre_ville": "Paris",
        "signature_lieu": "Paris",
        "signature_date": date(2026, 5, 26),
        "decision_date": date(2026, 5, 26),
        "depot_banque_nom": "Banque Test",
        "depot_banque_adresse": "30 boulevard Banque, 75009 Paris",
        "exercice_debut": "1er janvier",
        "exercice_fin": "31 decembre",
        "exercice_cloture_premier": "31 decembre 2026",
    }
    if profession == PROFESSION_DENTISTE or regime_communautaire or married_separation:
        kwargs.update(
            {
                "conjoint_civilite": "Madame",
                "conjoint_prenom": "Claire",
                "conjoint_nom": "Martin",
            }
        )
    return kwargs


def _cession_cabinet_medical_acte() -> CessionContext:
    """Cession de cabinet médical (étape acte) — données type (exemple lot_03 validé)."""
    return CessionContext.model_validate(
        {
            "type_cabinet": "medical",
            "etape": "acte",
            "vendeur": {
                "civilite_affichage": "Docteur",
                "genre": "masculin",
                "prenom": "Jean",
                "nom": "Durand",
                "profession": "medecin",
                "date_naissance": "1975-03-10",
                "ville_naissance": "Lyon",
                "departement_naissance": "69",
                "nationalite": "francaise",
                "adresse_affichee": "4 rue Victor Hugo, 69002 Lyon",
                "adresse_exercice_affichee": "10 rue du Cabinet, 75008 Paris",
                "numero_siren": "123 456 789",
                "numero_ordre": "ORD-123",
                "numero_rpps": "10101010101",
                "ordre_departemental": "Paris",
                "situation_maritale": "marie",
                "regime_matrimonial": "communaute reduite aux acquets",
                "conjoint": {"civilite_affichage": "Madame", "prenom": "Claire", "nom": "Durand"},
            },
            "acquereur": {
                "denomination_societe": "SELARL CABINET DURAND",
                "forme_sociale": "SELARL",
                "capital_social": "10 000",
                "siege": {"adresse_affichee": "20 avenue de Wagram, 75017 Paris"},
                "rcs_ville": "Paris",
                "numero_rcs": "999 888 777",
                "numero_siret": "999 888 777 00012",
                "representant": {
                    "civilite_affichage": "Docteur",
                    "genre": "feminin",
                    "prenom": "Alice",
                    "nom": "Moreau",
                    "fonction": "gerante",
                },
            },
            "cabinet": {
                "nature_fonds_liberal": "medecin generaliste",
                "adresse_affichee": "10 rue du Cabinet, 75008 Paris",
                "adresse_locaux_affichee": "10 rue du Cabinet, 75008 Paris",
                "telephone": "01 44 00 00 00",
                "superficie_local": "80 m2",
                "description_origine_propriete": "Origine de propriete validee manuellement.",
                "date_origine_propriete": "2020-01-01",
                "annees_acquisition_patientele": "2020",
                "prix_origine_propriete": "120 000 euros",
                "precedent_proprietaire": {
                    "civilite_affichage": "Docteur",
                    "prenom": "Paul",
                    "nom": "Bernard",
                },
            },
            "bail_professionnel": {
                "date_bail": "2021-01-01",
                "duree": "six annees",
                "date_debut": "2021-01-01",
                "date_fin": "2027-01-01",
                "loyer_mensuel": "2 000 euros",
                "activite_autorisee_affichee": "activite medicale et paramedicale",
            },
            "exercices": [
                {"periode": "2023", "chiffre_affaires": "210 000", "resultat": "80 000"},
                {"periode": "2024", "chiffre_affaires": "220 000", "resultat": "85 000"},
                {"periode": "2025", "chiffre_affaires": "230 000", "resultat": "90 000"},
            ],
            "prix": {
                "total": "300 000",
                "total_lettres": "trois cent mille euros",
                "elements_corporels": "50 000",
                "elements_corporels_lettres": "cinquante mille euros",
                "elements_incorporels": "250 000",
                "elements_incorporels_lettres": "deux cent cinquante mille euros",
            },
            "financement": {
                "pret": {"montant": "240 000", "taux": "4 %", "duree": "sept ans"},
                "credit_vendeur": {
                    "actif": True,
                    "montant": "60 000",
                    "duree": "vingt-quatre mois",
                    "taux": "3 %",
                    "majoration_interet_retard": "2 points",
                },
            },
            "scm": {"actif": True, "nb_parts_a_ceder": "10"},
            "date_limite_realisation": "2026-09-30",
            "validations": {
                "mentions_bail_medical_validees": True,
                "origine_compromis_medical_validee": True,
                "date_realisation_compromis_validee": True,
                "ligne_contrats_travail_medical_supprimee": True,
                "salaries_dentaire_deux_valides": True,
            },
        }
    )


# clé de scénario -> paramètres du cas
SELARL_SCENARIOS: dict[str, dict[str, Any]] = {
    "selarl_medecin_simple": {"profession": PROFESSION_MEDECIN},
    "selarl_dentiste_simple": {"profession": PROFESSION_DENTISTE},
    "selarl_medecin_regime_communautaire": {
        "profession": PROFESSION_MEDECIN,
        "regime_communautaire": True,
    },
    "selarl_medecin_cession_cabinet_medical": {
        "profession": PROFESSION_MEDECIN,
        "cession": _cession_cabinet_medical_acte,
    },
}


def build_selarl_scenario(key: str) -> SelarlSliceInput:
    if key not in SELARL_SCENARIOS:
        raise KeyError(
            f"Scénario inconnu : {key}. Disponibles : {', '.join(SELARL_SCENARIOS)}"
        )
    spec = dict(SELARL_SCENARIOS[key])
    cession_factory = spec.pop("cession", None)
    dossier_type = dossier_type_by_label(SELARL_DOSSIER_LABEL)
    kwargs = _base_kwargs(**spec)
    if cession_factory is not None:
        kwargs["cession_context"] = (
            cession_factory() if callable(cession_factory) else cession_factory
        )
    return build_clean_data_entry(dossier_type, **kwargs)
