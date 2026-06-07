"""Bibliothèque de scénarios SELARL figés (cas type, données fictives réalistes).

Chaque scénario produit un `SelarlSliceInput` déterministe, passé tel quel au
pipeline validé `front_app.selarl_slice.generate_selarl_dossier`. C'est la
"boussole reproductible" du pack : même scénario + même commit → même documents.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sydel_doc_engine.domain.models import BailContext, CessionContext, ScmCessionContext
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
        "situation_maritale": "marié" if is_married else "célibataire",
        "regime_matrimonial": (
            "régime de communauté"
            if regime_communautaire
            else "séparation de biens"
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
        "exercice_fin": "31 décembre",
        "exercice_cloture_premier": "31 décembre 2026",
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
                "profession": "médecin",
                "date_naissance": "1975-03-10",
                "ville_naissance": "Lyon",
                "departement_naissance": "69",
                "cp_naissance": "69002",
                "pays_naissance": "France",
                "nationalite": "française",
                "adresse_affichee": "4 rue Victor Hugo, 69002 Lyon",
                "adresse_exercice_affichee": "10 rue du Cabinet, 75008 Paris",
                "numero_siren": "123 456 789",
                "numero_ordre": "ORD-123",
                "numero_rpps": "10101010101",
                "ordre_departemental": "Paris",
                "situation_maritale": "marié",
                "regime_matrimonial": "communauté réduite aux acquêts",
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
                "date_immatriculation": "2026-01-15",
                "date_inscription_ordre": "2026-02-01",
                "representant": {
                    "civilite_affichage": "Docteur",
                    "genre": "feminin",
                    "prenom": "Alice",
                    "nom": "Moreau",
                    "fonction": "gérante",
                },
            },
            "cabinet": {
                "nature_fonds_liberal": "médecin généraliste",
                "denomination_ou_adresse_affichee": "Cabinet médical de Wagram",
                "adresse_affichee": "10 rue du Cabinet, 75008 Paris",
                "adresse_locaux_affichee": "10 rue du Cabinet, 75008 Paris",
                "telephone": "01 44 00 00 00",
                "superficie_local": "80",
                # Origine de propriete (regle NotebookLM) : decrit le VENDEUR ;
                # defaut "cree" si le praticien n'a pas achete son cabinet.
                "origine_propriete_mode": "cree",
                "date_origine_propriete": "2020-01-01",
                "annees_acquisition_patientele": "2020",
                "prix_origine_propriete": "120 000",
                "precedent_proprietaire": {
                    "civilite_affichage": "Docteur",
                    "prenom": "Paul",
                    "nom": "Bernard",
                },
            },
            "bail_professionnel": {
                "date_bail": "2021-01-01",
                "duree": "six années",
                "date_debut": "2021-01-01",
                "date_fin": "2027-01-01",
                "date_reconduction_1": "2027-01-01",
                "date_reconduction_2": "2033-01-01",
                "loyer_mensuel": "2 000",
                "activite_autorisee_affichee": "activité médicale et paramédicale",
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
                "banque": {"nom": "BANQUE EXEMPLE"},
                "destinataire": {
                    "civilite_affichage": "Monsieur",
                    "prenom": "Louis",
                    "nom": "Bernard",
                },
                "montant_deblocage": "240 000",
                "pret": {"montant": "240 000", "taux": "4 %", "duree": "sept ans"},
                "credit_vendeur": {
                    "actif": True,
                    "montant": "60 000",
                    # Regle NotebookLM : unite du credit-vendeur = ANNEES
                    # (« Trois ans »). Le modele rend « [duree_credit_vendeur] ans ».
                    "duree": "trois",
                    "taux": "5",
                    "majoration_interet_retard": "2",
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


def _bail_avenant_medecin() -> BailContext:
    """Avenant au bail pour la cession médicale (exemple lot_03 adapté, locataire médecin)."""
    return BailContext.model_validate(
        {
            "date_avenant": "2026-05-26",
            "date_signature_origine": "2021-09-01",
            "societe_en_cours_immatriculation": True,
            "bailleur_accepte_changement_locataire": True,
            "bailleur": {
                "civilite_affichage": "Monsieur",
                "prenom": "Paul",
                "nom": "Leroy",
                "profession": "bailleur",
                "date_naissance": "1970-01-05",
                "ville_naissance": "Lyon",
                "nationalite": "française",
                "adresse_affichee": "8 rue Victor Hugo, 69002 Lyon",
            },
            "locataire": {
                "civilite_affichage": "Docteur",
                "civilite_courte": "Docteur",
                "prenom": "Jean",
                "nom": "Durand",
                "profession": "médecin",
                "date_naissance": "1975-03-10",
                "ville_naissance": "Lyon",
                "nationalite": "française",
                "adresse_affichee": "4 rue Victor Hugo, 69002 Lyon",
            },
        }
    )


def _cession_cabinet_dentaire_acte() -> CessionContext:
    """Cession de cabinet dentaire (étape acte) + champs appel de fonds — données type."""
    return CessionContext.model_validate(
        {
            "type_cabinet": "dentaire",
            "etape": "acte",
            "vendeur": {
                "civilite_affichage": "Docteur",
                "genre": "masculin",
                "prenom": "Camille",
                "nom": "Martin",
                "profession": "chirurgien-dentiste",
                "date_naissance": "1984-06-20",
                "ville_naissance": "Paris",
                "departement_naissance": "75",
                "cp_naissance": "75007",
                "pays_naissance": "France",
                "nationalite": "française",
                "adresse_affichee": "4 rue du Bac, 75007 Paris",
                "adresse_exercice_affichee": "12 avenue des Ternes, 75017 Paris",
                "numero_siren": "321 654 987",
                "numero_ordre": "ORD-456",
                "numero_rpps": "20202020202",
                "ordre_departemental": "Paris",
                "situation_maritale": "marié",
                "regime_matrimonial": "communauté réduite aux acquêts",
                "conjoint": {"civilite_affichage": "Madame", "prenom": "Sophie", "nom": "Martin"},
            },
            "acquereur": {
                "denomination_societe": "SELARL CABINET MARTIN",
                "forme_sociale": "SELARL",
                "capital_social": "10 000",
                "siege": {"adresse_affichee": "12 avenue des Ternes, 75017 Paris"},
                "rcs_ville": "Paris",
                "numero_rcs": "888 777 666",
                "numero_siret": "888 777 666 00013",
                "representant": {
                    "civilite_affichage": "Docteur",
                    "genre": "masculin",
                    "prenom": "Camille",
                    "nom": "Martin",
                    "fonction": "gérant",
                },
            },
            "cabinet": {
                "nature_fonds_liberal": "chirurgien-dentiste",
                "denomination_ou_adresse_affichee": "Cabinet dentaire des Ternes",
                "adresse_affichee": "12 avenue des Ternes, 75017 Paris",
                "adresse_locaux_affichee": "12 avenue des Ternes, 75017 Paris",
                "telephone": "01 45 00 00 00",
                "superficie_local": "90",
                "description_origine_propriete": "Origine de propriété validée manuellement.",
                "date_origine_propriete": "2019-01-01",
                "annees_acquisition_patientele": "2019",
                "prix_origine_propriete": "150 000",
                "precedent_proprietaire": {
                    "civilite_affichage": "Docteur",
                    "prenom": "Henri",
                    "nom": "Petit",
                },
            },
            "bail_professionnel": {
                "date_bail": "2021-09-01",
                "duree": "six années",
                "date_debut": "2021-09-01",
                "date_fin": "2027-09-01",
                "date_reconduction_1": "2027-09-01",
                "date_reconduction_2": "2033-09-01",
                "loyer_mensuel": "2 500",
                "activite_autorisee_affichee": "activité dentaire et paramédicale",
            },
            "exercices": [
                {"periode": "2023", "chiffre_affaires": "260 000", "resultat": "100 000"},
                {"periode": "2024", "chiffre_affaires": "270 000", "resultat": "105 000"},
                {"periode": "2025", "chiffre_affaires": "280 000", "resultat": "110 000"},
            ],
            "prix": {
                "total": "350 000",
                "total_lettres": "trois cent cinquante mille euros",
                "elements_corporels": "60 000",
                "elements_corporels_lettres": "soixante mille euros",
                "elements_incorporels": "290 000",
                "elements_incorporels_lettres": "deux cent quatre-vingt-dix mille euros",
            },
            "financement": {
                "banque": {"nom": "BANQUE EXEMPLE"},
                "destinataire": {
                    "civilite_affichage": "Monsieur",
                    "prenom": "Louis",
                    "nom": "Bernard",
                },
                "montant_deblocage": "150 000",
                "pret": {"montant": "280 000", "taux": "4 %", "duree": "sept ans"},
            },
            "scm": {"actif": False},
            "salaries": [
                {"civilite_affichage": "Madame", "prenom": "Léa", "nom": "Petit"},
                {"civilite_affichage": "Monsieur", "prenom": "Noé", "nom": "Robert"},
            ],
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


def _bail_avenant_dentaire() -> BailContext:
    """Avenant au bail pour la cession dentaire (exemple lot_03, locataire chirurgien-dentiste)."""
    return BailContext.model_validate(
        {
            "date_avenant": "2026-05-26",
            "date_signature_origine": "2021-09-01",
            "societe_en_cours_immatriculation": True,
            "bailleur_accepte_changement_locataire": True,
            "bailleur": {
                "civilite_affichage": "Monsieur",
                "prenom": "Paul",
                "nom": "Leroy",
                "profession": "bailleur",
                "date_naissance": "1970-01-05",
                "ville_naissance": "Lyon",
                "nationalite": "française",
                "adresse_affichee": "8 rue Victor Hugo, 69002 Lyon",
            },
            "locataire": {
                "civilite_affichage": "Docteur",
                "civilite_courte": "Docteur",
                "prenom": "Camille",
                "nom": "Martin",
                "profession": "chirurgien-dentiste",
                "date_naissance": "1984-06-20",
                "ville_naissance": "Paris",
                "nationalite": "française",
                "adresse_affichee": "4 rue du Bac, 75007 Paris",
            },
        }
    )


def _scm_cession_selarl() -> ScmCessionContext:
    """Cession de parts de SCM par une SELARL (exemple lot_05 adapté en variante SELARL)."""
    return ScmCessionContext.model_validate(
        {
            "variante_structure": "selarl",
            "scm_cedee": {
                "denomination": "SCM CABINET CENTRAL",
                "forme_juridique": "Societe Civile de Moyens",
                "capital_social": "3 000",
                "siege": {"adresse_affichee": "12 rue des Soins, 75008 Paris"},
                "ville_rcs": "Paris",
                "numero_rcs": "900 111 222",
                "nb_parts_total": 300,
                "valeur_nominale_part": "10",
                "plage_parts_total": "1 a 300",
                "cogerants": [
                    "Monsieur Paul Bernard",
                    "Monsieur Jean Dupont",
                    "Madame Anne Martin",
                ],
            },
            "cessionnaire": {
                "denomination": "SELARL CABINET DUPONT",
                "forme_juridique": "SELARL",
                "capital_social": "10 000",
                "siege": {"adresse_affichee": "20 avenue des Praticiens, 75008 Paris"},
                "ville_rcs": "Paris",
                "representant": {
                    "civilite_affichage": "Monsieur",
                    "civilite_courte": "M.",
                    "prenom": "Jean",
                    "nom": "Dupont",
                    "fonction": "gerant",
                },
            },
            "cedant": {
                "civilite_affichage": "Monsieur",
                "prenom": "Jean",
                "nom": "Dupont",
                "profession": "chirurgien-dentiste",
                "profession_reglementee_pluriel": "chirurgiens-dentistes",
                "date_naissance": "1er janvier 1980",
                "ville_naissance": "Paris",
                "departement_naissance": "75",
                "nationalite": "francaise",
                "adresse_affichee": "1 rue du Cedant, 75008 Paris",
                "situation_maritale": "marie",
                "ordre": {"departemental": "Paris", "numero": "12345"},
                "numero_rpps": "10000000001",
                "conjoint": {"civilite_affichage": "Madame", "prenom": "Claire", "nom": "Dupont"},
            },
            "agrement": {
                "date_pv": "15 mai 2026",
                "date_pv_lettres": "deux mille vingt-six, le quinze mai",
                "delai_mois": "3",
                "date_limite": "15 aout 2026",
            },
            "associes_presents": [
                {"civilite_affichage": "Monsieur", "prenom": "Paul", "nom": "Bernard",
                 "parts": {"nb": 100, "plage": "1 a 100"}},
                {"civilite_affichage": "Monsieur", "prenom": "Jean", "nom": "Dupont",
                 "parts": {"nb": 100, "plage": "101 a 200"}},
                {"civilite_affichage": "Madame", "prenom": "Anne", "nom": "Martin",
                 "parts": {"nb": 100, "plage": "201 a 300"}},
            ],
            "associes_avant_cession": [
                {"civilite_affichage": "Monsieur", "prenom": "Paul", "nom": "Bernard",
                 "parts": {"nb": 100, "plage": "1 a 100"}},
                {"civilite_affichage": "Monsieur", "prenom": "Jean", "nom": "Dupont",
                 "parts": {"nb": 100, "plage": "101 a 200"}},
                {"civilite_affichage": "Madame", "prenom": "Anne", "nom": "Martin",
                 "parts": {"nb": 100, "plage": "201 a 300"}},
            ],
            "associes_apres_cession": [
                {"civilite_affichage": "Monsieur", "prenom": "Paul", "nom": "Bernard",
                 "parts": {"nb": 100, "plage": "1 a 100"}},
                {"civilite_affichage": "Monsieur", "prenom": "Jean", "nom": "Dupont",
                 "parts": {"nb": 50, "plage": "101 a 150"}},
                {"type_personne": "personne_morale", "denomination": "SELARL CABINET DUPONT",
                 "forme_juridique": "SELARL", "parts": {"nb": 50, "plage": "151 a 200"}},
                {"civilite_affichage": "Madame", "prenom": "Anne", "nom": "Martin",
                 "parts": {"nb": 100, "plage": "201 a 300"}},
            ],
            "signataires_pv": ["M. Jean Dupont", "M. Paul Bernard", "Mme Anne Martin"],
            "parts_cedees": {"nb": 50, "plage": "151 a 200"},
            "prix": {
                "unitaire": "100",
                "unitaire_lettres": "cent",
                "global": "5 000",
                "global_lettres": "cinq mille",
            },
            "paiement_mode": "pret_bancaire",
            "credit_vendeur": {"actif": False},
            "enregistrement": {
                "service": "SERVICE DEPARTEMENTAL DE L'ENREGISTREMENT",
                "centre_finances_publiques": "Centre des finances publiques de Paris",
                "adresse_service": "6 rue Paganini",
                "cp_ville_service": "75020 Paris",
                "nombre_exemplaires": "3",
                "montant_droits": "150",
            },
            "signataire_sde": {"prenom": "Sarah", "nom": "Durand"},
            "nombre_exemplaires_lettres": "trois",
            "prestataire_signature_electronique": "DocuSign",
            "date_acte_affichee": "15 mai 2026",
            "representant_cessionnaire_confirme": True,
        }
    )


def _cession_cabinet_medical_compromis() -> CessionContext:
    """Compromis de cession médical (DOC-010) : étape compromis, sans crédit-vendeur ni SCM
    (réservés à l'acte médical par les règles métier des générateurs)."""
    base = _cession_cabinet_medical_acte()
    financement = base.financement.model_copy(update={"credit_vendeur": None})
    return base.model_copy(
        update={"etape": "compromis", "financement": financement, "scm": None}
    )


def _cession_cabinet_dentaire_compromis() -> CessionContext:
    """Compromis de cession dentaire (DOC-012) — mêmes données que l'acte, étape compromis,
    sans les salariés (la reprise des contrats de travail est réservée à l'acte dentaire
    par les règles métier des générateurs)."""
    return _cession_cabinet_dentaire_acte().model_copy(
        update={"etape": "compromis", "salaries": []}
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
        "bail": _bail_avenant_medecin,
    },
    "selarl_dentiste_cession_cabinet_dentaire": {
        "profession": PROFESSION_DENTISTE,
        "cession": _cession_cabinet_dentaire_acte,
        "bail": _bail_avenant_dentaire,
    },
    "selarl_dentiste_cession_scm": {
        "profession": PROFESSION_DENTISTE,
        "scm_cession": _scm_cession_selarl,
    },
    "selarl_medecin_cession_compromis_medical": {
        "profession": PROFESSION_MEDECIN,
        "cession": _cession_cabinet_medical_compromis,
        "bail": _bail_avenant_medecin,
    },
    "selarl_dentiste_cession_compromis_dentaire": {
        "profession": PROFESSION_DENTISTE,
        "cession": _cession_cabinet_dentaire_compromis,
        "bail": _bail_avenant_dentaire,
    },
}


def cession_fixture_for_profession(profession: str) -> tuple[CessionContext, BailContext]:
    """Fixture cession (acte) + avenant bail adaptee a la profession du praticien.

    Reutilisee par le front pour (a) prereremplir le sous-formulaire cession et
    (b) fournir un `CessionContext` complet et valide a fusionner avec les
    saisies utilisateur. Medecin -> cabinet medical, chirurgien-dentiste ->
    cabinet dentaire.
    """
    if profession == PROFESSION_DENTISTE:
        return _cession_cabinet_dentaire_acte(), _bail_avenant_dentaire()
    return _cession_cabinet_medical_acte(), _bail_avenant_medecin()


def scm_cession_fixture() -> ScmCessionContext:
    """Fixture de cession de parts de SCM par une SELARL (DOC-031/032/033)."""
    return _scm_cession_selarl()


def build_selarl_scenario(key: str) -> SelarlSliceInput:
    if key not in SELARL_SCENARIOS:
        raise KeyError(
            f"Scénario inconnu : {key}. Disponibles : {', '.join(SELARL_SCENARIOS)}"
        )
    spec = dict(SELARL_SCENARIOS[key])
    cession_factory = spec.pop("cession", None)
    bail_factory = spec.pop("bail", None)
    scm_cession_factory = spec.pop("scm_cession", None)
    dossier_type = dossier_type_by_label(SELARL_DOSSIER_LABEL)
    kwargs = _base_kwargs(**spec)
    if cession_factory is not None:
        kwargs["cession_context"] = (
            cession_factory() if callable(cession_factory) else cession_factory
        )
    if bail_factory is not None:
        kwargs["bail_context"] = bail_factory() if callable(bail_factory) else bail_factory
    if scm_cession_factory is not None:
        kwargs["scm_cession_context"] = (
            scm_cession_factory() if callable(scm_cession_factory) else scm_cession_factory
        )
    return build_clean_data_entry(dossier_type, **kwargs)
