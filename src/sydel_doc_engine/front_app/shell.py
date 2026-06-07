from __future__ import annotations

import random
import re
from datetime import date
from pathlib import Path

import streamlit as st

from sydel_doc_engine.domain.models import (
    BailContext,
    CessionContext,
    ScmCessionContext,
)
from sydel_doc_engine.front_app.data_entry import (
    CleanDataEntry,
    build_clean_data_entry,
)
from sydel_doc_engine.front_app.dossier_selection import (
    DossierTypeOption,
    dossier_type_by_label,
    dossier_type_labels,
)
from sydel_doc_engine.front_app.field_derivations import (
    MATRIMONIAL_STATUS_PRESETS,
    NATIONALITY_PRESETS,
    calculate_nominal_value,
    derive_gender_from_civilite,
    format_french_date,
    format_numeric_value,
    matrimonial_status_value,
    parse_french_date,
    regime_matrimonial_from_status,
)
from sydel_doc_engine.front_app.generation import (
    CleanGenerationPlan,
    build_clean_generation_plan,
)
from sydel_doc_engine.front_app.selarl_slice import (
    PROFESSION_DENTISTE,
    PROFESSION_MEDECIN,
    generate_selarl_dossier,
)
from sydel_doc_engine.scenarios.selarl import (
    cession_fixture_for_profession,
    scm_cession_fixture,
)

ARTIFACTS_DIR = Path("artifacts") / "track_b_selarl_v1"
GENERATED_DOSSIER_STATE_KEY = "clean_generated_dossier"
DOCX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def render_clean_front() -> None:
    st.title("SYDEL Track B")
    st.caption(
        "Front clean Track B : slice SELARL V1 bornee, sans ecrans legacy ni outils internes."
    )
    dossier_type = _render_dossier_type_selection()
    data_entry = _render_data_entry_zone(dossier_type)
    generation_plan = build_clean_generation_plan(dossier_type, data_entry)
    _render_generation_zone(data_entry, generation_plan)


def _render_dossier_type_selection() -> DossierTypeOption:
    st.subheader("Type de dossier")
    selected_label = st.selectbox(
        "Type de dossier",
        dossier_type_labels(),
        key="clean_dossier_type",
    )
    if st.button("Generer des donnees de test", key="clean_generate_test_data"):
        _prefill_random_selarl_data()
        st.success("Donnees de test coherentes pre-remplies.")
    st.caption("Perimetre actif : SELARL unipersonnelle de production.")
    return dossier_type_by_label(selected_label)


def _prefill_random_selarl_data() -> None:
    person = random.choice(_test_people())
    company = random.choice(_test_companies())
    capital, parts = random.choice(((1000, 100), (2000, 200), (5000, 500), (10000, 1000)))
    # Respecte la profession deja choisie dans le wizard pour que la cession
    # preremplie soit coherente (medical vs dentaire) ; defaut Medecin.
    profession_label = st.session_state.get("selarl_profession") or "Medecin"
    if profession_label not in ("Medecin", "Chirurgien-dentiste"):
        profession_label = "Medecin"
    regime_communautaire = profession_label == "Chirurgien-dentiste" or random.choice(
        (False, True)
    )
    today_text = format_french_date(date.today())
    dossier_suffix = random.randint(1000, 9999)
    status = (
        "Marie(e)"
        if regime_communautaire
        else random.choice(tuple(item for item in MATRIMONIAL_STATUS_PRESETS if item != "Marie(e)"))
    )

    profession_key = (
        PROFESSION_DENTISTE if profession_label == "Chirurgien-dentiste" else PROFESSION_MEDECIN
    )

    values = {
        "selarl_profession": profession_label,
        "selarl_dossier_unipersonnel": True,
        "selarl_regime_communautaire": regime_communautaire,
        "selarl_cession": True,
        "selarl_scm": True,
        "selarl_dossier_reference": f"TEST-SELARL-{dossier_suffix}",
        "selarl_civilite": person["civilite"],
        "selarl_prenom": person["prenom"],
        "selarl_nom": person["nom"],
        "selarl_date_naissance": person["date_naissance"],
        "selarl_ville_naissance": person["ville_naissance"],
        "selarl_ville_naissance_article_au": False,
        "selarl_departement_naissance": person["departement_naissance"],
        "selarl_nationalite_choice": random.choice(NATIONALITY_PRESETS[:-1]),
        "selarl_nationalite_other": "",
        "selarl_situation_maritale": status,
        "selarl_numero_ordre": f"ORD-{random.randint(100000, 999999)}",
        "selarl_numero_rpps": str(random.randint(10000000000, 19999999999)),
        "selarl_nom_pere": person["nom_pere"],
        "selarl_nom_mere": person["nom_mere"],
        "selarl_adresse_num_voie": person["adresse_num_voie"],
        "selarl_adresse_voie": person["adresse_voie"],
        "selarl_adresse_cp": person["adresse_cp"],
        "selarl_adresse_ville": person["adresse_ville"],
        "selarl_denomination": f"SELARL {person['nom']}",
        "selarl_capital_social": capital,
        "selarl_nb_parts_total": parts,
        "selarl_ville_rcs": company["ville"],
        "selarl_siege_num_voie": company["numero"],
        "selarl_siege_voie": company["voie"],
        "selarl_siege_cp": company["cp"],
        "selarl_siege_ville": company["ville"],
        "selarl_departement_ordre": company["departement_ordre"],
        "selarl_ordre_adresse_ligne_1": company["ordre_adresse"],
        "selarl_ordre_cp": company["ordre_cp"],
        "selarl_ordre_ville": company["ville"],
        "selarl_signature_lieu": company["ville"],
        "selarl_signature_date": today_text,
        "selarl_decision_date": today_text,
        "selarl_depot_banque_nom": random.choice(("BNP Paribas", "CIC", "Credit Agricole")),
        "selarl_depot_banque_adresse": company["banque_adresse"],
        "selarl_exercice_debut": "1er janvier",
        "selarl_exercice_fin": "31 decembre",
        "selarl_exercice_cloture_premier": "31 decembre 2026",
        "selarl_autre_lieu_exercice": False,
        "selarl_lieu_exercice_adresse": "",
        "selarl_conjoint_civilite": "Madame",
        "selarl_conjoint_prenom": random.choice(("Claire", "Sophie", "Nadia")),
        "selarl_conjoint_nom": person["nom"],
    }
    values.update(_cession_prefill_values(profession_key))
    values.update(_scm_cession_prefill_values())
    st.session_state.update(values)
    st.session_state.pop(GENERATED_DOSSIER_STATE_KEY, None)


def _cession_prefill_values(profession: str) -> dict[str, object]:
    """Cles `selarl_cession_*` prereremplies depuis la fixture scenario adaptee.

    Source unique de verite : la meme fixture que `_render_cession_form` utilise
    comme base. Un clic = cession testable et generable.
    """
    cession, _bail = cession_fixture_for_profession(profession)
    payload = cession.model_dump(by_alias=True)
    vendeur = payload.get("vendeur") or {}
    acquereur = payload.get("acquereur") or {}
    siege = acquereur.get("siege") or {}
    cabinet = payload.get("cabinet") or {}
    bail = payload.get("bail_professionnel") or {}
    prix = payload.get("prix") or {}
    financement = payload.get("financement") or {}
    banque = financement.get("banque") or {}
    pret = financement.get("pret") or {}
    credit = financement.get("credit_vendeur") or {}

    prefill: dict[str, object] = {
        "selarl_cession_meta_type_cabinet": payload.get("type_cabinet") or "medical",
        "selarl_cession_meta_etape": payload.get("etape") or "acte",
        "selarl_cession_vendeur_civilite": vendeur.get("civilite_affichage") or "",
        "selarl_cession_vendeur_prenom": vendeur.get("prenom") or "",
        "selarl_cession_vendeur_nom": vendeur.get("nom") or "",
        "selarl_cession_vendeur_numero_ordre": vendeur.get("numero_ordre") or "",
        "selarl_cession_vendeur_numero_rpps": vendeur.get("numero_rpps") or "",
        "selarl_cession_vendeur_adresse": vendeur.get("adresse_affichee") or "",
        "selarl_cession_acquereur_denomination": acquereur.get("denomination_societe") or "",
        "selarl_cession_acquereur_rcs_ville": acquereur.get("rcs_ville") or "",
        "selarl_cession_acquereur_numero_rcs": acquereur.get("numero_rcs") or "",
        "selarl_cession_acquereur_siege": siege.get("adresse_affichee") or "",
        "selarl_cession_cabinet_nature": cabinet.get("nature_fonds_liberal") or "",
        "selarl_cession_cabinet_denomination": (
            cabinet.get("denomination_ou_adresse_affichee") or ""
        ),
        "selarl_cession_cabinet_adresse": cabinet.get("adresse_affichee") or "",
        "selarl_cession_bail_duree": bail.get("duree") or "",
        "selarl_cession_bail_loyer": bail.get("loyer_mensuel") or "",
        "selarl_cession_bail_activite": bail.get("activite_autorisee_affichee") or "",
        "selarl_cession_prix_total": prix.get("total") or "",
        "selarl_cession_prix_total_lettres": prix.get("total_lettres") or "",
        "selarl_cession_prix_corporels": prix.get("elements_corporels") or "",
        "selarl_cession_prix_incorporels": prix.get("elements_incorporels") or "",
        "selarl_cession_financement_banque": banque.get("nom") or "",
        "selarl_cession_financement_deblocage": financement.get("montant_deblocage") or "",
        "selarl_cession_financement_pret_montant": pret.get("montant") or "",
        "selarl_cession_financement_credit_actif": bool(credit.get("actif")),
        "selarl_cession_financement_credit_montant": credit.get("montant") or "",
        "selarl_cession_financement_credit_duree": credit.get("duree") or "",
        "selarl_cession_financement_credit_taux": credit.get("taux") or "",
    }
    for index, exercice in enumerate(payload.get("exercices") or []):
        prefill[f"selarl_cession_exercice_{index}_periode"] = exercice.get("periode") or ""
        prefill[f"selarl_cession_exercice_{index}_ca"] = exercice.get("chiffre_affaires") or ""
        prefill[f"selarl_cession_exercice_{index}_resultat"] = exercice.get("resultat") or ""
    for index, salarie in enumerate(payload.get("salaries") or []):
        prefill[f"selarl_cession_salarie_{index}_civilite"] = (
            salarie.get("civilite_affichage") or ""
        )
        prefill[f"selarl_cession_salarie_{index}_prenom"] = salarie.get("prenom") or ""
        prefill[f"selarl_cession_salarie_{index}_nom"] = salarie.get("nom") or ""
    return prefill


def _scm_cession_prefill_values() -> dict[str, object]:
    """Cles `selarl_cession_scm_*` prereremplies depuis la fixture SCM."""
    payload = scm_cession_fixture().model_dump(by_alias=True)
    scm_cedee = payload.get("scm_cedee") or {}
    cedant = payload.get("cedant") or {}
    parts_cedees = payload.get("parts_cedees") or {}
    prix = payload.get("prix") or {}
    return {
        "selarl_cession_scm_cedee_denomination": scm_cedee.get("denomination") or "",
        "selarl_cession_scm_cedee_rcs_ville": scm_cedee.get("ville_rcs") or "",
        "selarl_cession_scm_cedee_numero_rcs": scm_cedee.get("numero_rcs") or "",
        "selarl_cession_scm_cedant_civilite": cedant.get("civilite_affichage") or "",
        "selarl_cession_scm_cedant_prenom": cedant.get("prenom") or "",
        "selarl_cession_scm_cedant_nom": cedant.get("nom") or "",
        "selarl_cession_scm_parts_plage": parts_cedees.get("plage") or "",
        "selarl_cession_scm_prix_global": prix.get("global") or "",
        "selarl_cession_scm_prix_global_lettres": prix.get("global_lettres") or "",
    }


def _test_people() -> tuple[dict[str, str], ...]:
    return (
        {
            "civilite": "Monsieur",
            "prenom": "Jean",
            "nom": "Martin",
            "date_naissance": "12/04/1984",
            "ville_naissance": "Paris",
            "departement_naissance": "75",
            "nom_pere": "Pierre Martin",
            "nom_mere": "Anne Martin",
            "adresse_num_voie": "10",
            "adresse_voie": "rue des Tilleuls",
            "adresse_cp": "75011",
            "adresse_ville": "Paris",
        },
        {
            "civilite": "Madame",
            "prenom": "Camille",
            "nom": "Bernard",
            "date_naissance": "21/09/1978",
            "ville_naissance": "Lyon",
            "departement_naissance": "69",
            "nom_pere": "Laurent Bernard",
            "nom_mere": "Marie Bernard",
            "adresse_num_voie": "8",
            "adresse_voie": "avenue Victor Hugo",
            "adresse_cp": "69002",
            "adresse_ville": "Lyon",
        },
        {
            "civilite": "Monsieur",
            "prenom": "Thomas",
            "nom": "Durand",
            "date_naissance": "03/02/1981",
            "ville_naissance": "Nantes",
            "departement_naissance": "44",
            "nom_pere": "Alain Durand",
            "nom_mere": "Helene Durand",
            "adresse_num_voie": "14",
            "adresse_voie": "boulevard Saint-Felix",
            "adresse_cp": "44000",
            "adresse_ville": "Nantes",
        },
    )


def _test_companies() -> tuple[dict[str, str], ...]:
    return (
        {
            "numero": "20",
            "voie": "avenue du Siege",
            "cp": "75002",
            "ville": "Paris",
            "departement_ordre": "75, Paris",
            "ordre_adresse": "1 rue de l'Ordre",
            "ordre_cp": "75008",
            "banque_adresse": "30 boulevard Haussmann, 75009 Paris",
        },
        {
            "numero": "5",
            "voie": "place Bellecour",
            "cp": "69002",
            "ville": "Lyon",
            "departement_ordre": "69, Rhone",
            "ordre_adresse": "12 quai Jules Courmont",
            "ordre_cp": "69002",
            "banque_adresse": "7 cours de la Liberte, 69003 Lyon",
        },
        {
            "numero": "3",
            "voie": "rue Crebillon",
            "cp": "44000",
            "ville": "Nantes",
            "departement_ordre": "44, Loire-Atlantique",
            "ordre_adresse": "9 allee Baco",
            "ordre_cp": "44000",
            "banque_adresse": "2 rue de Strasbourg, 44000 Nantes",
        },
    )


def _ordre_label(profession_label: str, ville: str) -> str:
    profession = (
        "chirurgiens-dentistes" if profession_label == "Chirurgien-dentiste" else "médecins"
    )
    return f"Conseil departemental de l'Ordre des {profession} de {ville}"


def _render_data_entry_zone(dossier_type: DossierTypeOption) -> CleanDataEntry:
    st.subheader("Donnees a saisir")
    qualification = _render_qualification()
    praticien = _render_praticien(
        regime_communautaire=bool(qualification["regime_communautaire"])
    )
    societe = _render_societe(praticien=praticien)
    ordre_mandataire = _render_ordre_mandataire()
    generation_context = _render_generation_context(societe)
    conjoint = _render_conjoint(
        profession=qualification["profession"],
        regime_communautaire=qualification["regime_communautaire"],
        situation_maritale=praticien["situation_maritale"],
    )
    cession_context, bail_context = _render_cession_form(
        bool(qualification["cession"]),
        str(qualification["profession"]),
    )
    scm_cession_context = _render_scm_cession_form(bool(qualification["scm"]))
    return build_clean_data_entry(
        dossier_type,
        **qualification,
        **praticien,
        **societe,
        **ordre_mandataire,
        **generation_context,
        **conjoint,
        cession_context=cession_context,
        bail_context=bail_context,
        scm_cession_context=scm_cession_context,
    )


def _render_qualification() -> dict[str, object]:
    st.markdown("**Qualification**")
    profession_label = st.selectbox(
        "Profession",
        ("Medecin", "Chirurgien-dentiste"),
        key="selarl_profession",
    )
    col_a, col_b, col_c = st.columns(3)
    dossier_unipersonnel = col_a.checkbox(
        "Dossier unipersonnel",
        value=True,
        key="selarl_dossier_unipersonnel",
    )
    regime_communautaire = col_b.checkbox(
        "Documents regime de la communaute",
        value=False,
        key="selarl_regime_communautaire",
    )
    col_c.caption("Active DOC-005 et DOC-006.")

    st.markdown("**Operations complementaires**")
    out_a, out_b = st.columns(2)
    cession = out_a.checkbox("Cession", value=False, key="selarl_cession")
    scm = out_b.checkbox("SCM", value=False, key="selarl_scm")

    return {
        "dossier_reference": st.text_input(
            "Reference dossier",
            key="selarl_dossier_reference",
        ),
        "profession": (
            PROFESSION_DENTISTE if profession_label == "Chirurgien-dentiste" else PROFESSION_MEDECIN
        ),
        "dossier_unipersonnel": dossier_unipersonnel,
        "regime_communautaire": regime_communautaire,
        "cession": cession,
        "scm": scm,
    }


def _render_praticien(*, regime_communautaire: bool) -> dict[str, object]:
    st.markdown("**Fiche Client / Praticien**")
    civilite = st.selectbox("Civilite", ("Monsieur", "Madame"), key="selarl_civilite")
    col_d, col_e = st.columns(2)
    prenom = col_d.text_input("Prenom", key="selarl_prenom")
    nom = col_e.text_input("Nom", key="selarl_nom")
    col_f, col_g, col_h = st.columns(3)
    with col_f:
        date_naissance = _date_input_with_today(
            "Date de naissance",
            key="selarl_date_naissance",
            value=date(1990, 1, 1),
        )
    ville_naissance = col_g.text_input("Ville de naissance", key="selarl_ville_naissance")
    ville_naissance_article_au = col_g.checkbox(
        "au",
        key="selarl_ville_naissance_article_au",
        help="Affiche 'ne au ...' au lieu de 'ne a ...' dans la DNC.",
    )
    departement_naissance = col_h.text_input(
        "Departement naissance",
        key="selarl_departement_naissance",
    )
    col_i, col_j = st.columns(2)
    nationalite_choice = col_i.selectbox(
        "Nationalite",
        NATIONALITY_PRESETS,
        key="selarl_nationalite_choice",
    )
    nationalite = (
        col_i.text_input("Nationalite autre", key="selarl_nationalite_other")
        if nationalite_choice == "Autre"
        else nationalite_choice.lower()
    )
    situation_maritale_label = col_j.selectbox(
        "Situation matrimoniale",
        MATRIMONIAL_STATUS_PRESETS,
        key="selarl_situation_maritale",
    )
    numero_ordre = st.text_input("Numero Ordre", key="selarl_numero_ordre")
    col_m, col_n, col_o = st.columns(3)
    numero_rpps = col_m.text_input("Numero RPPS", key="selarl_numero_rpps")
    nom_pere = col_n.text_input("Nom du pere", key="selarl_nom_pere")
    nom_mere = col_o.text_input("Nom de la mere", key="selarl_nom_mere")

    st.markdown("Adresse personnelle")
    adr_a, adr_b, adr_c, adr_d = st.columns(4)
    return {
        "civilite": civilite,
        "genre": derive_gender_from_civilite(civilite),
        "prenom": prenom,
        "nom": nom,
        "date_naissance": date_naissance,
        "ville_naissance": ville_naissance,
        "ville_naissance_article_au": ville_naissance_article_au,
        "departement_naissance": departement_naissance,
        "nationalite": nationalite,
        "nom_pere": nom_pere,
        "nom_mere": nom_mere,
        "situation_maritale": matrimonial_status_value(situation_maritale_label),
        "regime_matrimonial": regime_matrimonial_from_status(
            situation_maritale_label,
            regime_communautaire,
        ),
        "numero_ordre": numero_ordre,
        "numero_rpps": numero_rpps,
        "adresse_num_voie": adr_a.text_input("No", key="selarl_adresse_num_voie"),
        "adresse_voie": adr_b.text_input("Voie", key="selarl_adresse_voie"),
        "adresse_cp": adr_c.text_input("CP", key="selarl_adresse_cp"),
        "adresse_ville": adr_d.text_input("Ville", key="selarl_adresse_ville"),
    }


def _render_societe(
    *,
    praticien: dict[str, object],
) -> dict[str, object]:
    st.markdown("**Fiche Societe**")
    col_a, col_b = st.columns(2)
    denomination = col_a.text_input("Denomination sociale", key="selarl_denomination")
    capital_social = col_b.number_input(
        "Capital social (€)",
        min_value=0,
        step=100,
        value=0,
        key="selarl_capital_social",
        help="Montant numerique uniquement.",
    )
    nb_parts_total = st.number_input(
        "Nombre total de parts",
        min_value=0,
        step=1,
        value=0,
        key="selarl_nb_parts_total",
    )
    valeur_nominale_part = calculate_nominal_value(capital_social, nb_parts_total)
    if valeur_nominale_part:
        st.caption(f"Valeur nominale calculee : {valeur_nominale_part} EUR")
    else:
        st.caption("Valeur nominale calculee automatiquement apres capital et parts.")
    ville_rcs = st.text_input("RCS (ville)", key="selarl_ville_rcs")

    st.markdown("Siege social")
    siege_same_as_personal = st.checkbox(
        "identique a l'adresse personnelle",
        value=False,
        key="selarl_siege_same_as_personal",
    )
    if siege_same_as_personal:
        return {
            "denomination": denomination,
            "capital_social": format_numeric_value(capital_social),
            "duree": "99 ans",
            "nb_parts_total": int(nb_parts_total),
            "valeur_nominale_part": valeur_nominale_part,
            "ville_rcs": ville_rcs,
            "siege_num_voie": str(praticien.get("adresse_num_voie") or ""),
            "siege_voie": str(praticien.get("adresse_voie") or ""),
            "siege_cp": str(praticien.get("adresse_cp") or ""),
            "siege_ville": str(praticien.get("adresse_ville") or ""),
        }
    adr_a, adr_b, adr_c, adr_d = st.columns(4)
    return {
        "denomination": denomination,
        "capital_social": format_numeric_value(capital_social),
        "duree": "99 ans",
        "nb_parts_total": int(nb_parts_total),
        "valeur_nominale_part": valeur_nominale_part,
        "ville_rcs": ville_rcs,
        "siege_num_voie": adr_a.text_input("Numero", key="selarl_siege_num_voie"),
        "siege_voie": adr_b.text_input("Voie", key="selarl_siege_voie"),
        "siege_cp": adr_c.text_input("Code postal", key="selarl_siege_cp"),
        "siege_ville": adr_d.text_input("Ville", key="selarl_siege_ville"),
    }


def _render_ordre_mandataire() -> dict[str, object]:
    st.markdown("**Ordre professionnel**")
    col_a, _ = st.columns(2)
    departement_ordre = col_a.text_input(
        "Departement d'inscription a l'ordre",
        key="selarl_departement_ordre",
        help="Exemple : Paris, Loire-Atlantique ou le departement ordinal attendu par le dossier.",
    )
    col_c, col_d, col_e = st.columns(3)
    ordre_adresse_ligne_1 = col_c.text_input(
        "Adresse ordre",
        key="selarl_ordre_adresse_ligne_1",
    )
    ordre_cp = col_d.text_input("CP ordre", key="selarl_ordre_cp")
    ordre_ville = col_e.text_input("Ville ordre", key="selarl_ordre_ville")
    return {
        "departement_ordre": departement_ordre,
        "ordre_adresse_ligne_1": ordre_adresse_ligne_1,
        "ordre_cp": ordre_cp,
        "ordre_ville": ordre_ville,
    }


def _render_generation_context(societe: dict[str, object]) -> dict[str, object]:
    st.markdown("**Generation**")
    col_a, col_b = st.columns(2)
    signature_lieu = col_a.text_input("Lieu de signature", key="selarl_signature_lieu")
    with col_b:
        signature_date = _date_input_with_today(
            "Date de signature",
            key="selarl_signature_date",
            value=date.today(),
        )
    decision_date = _date_input_with_today(
        "Date de decision",
        key="selarl_decision_date",
        value=date.today(),
    )
    col_g, col_h = st.columns(2)
    depot_banque_nom = col_g.text_input("Banque depot", key="selarl_depot_banque_nom")
    depot_banque_adresse = col_h.text_input(
        "Adresse banque",
        key="selarl_depot_banque_adresse",
    )
    col_j, col_k, col_l = st.columns(3)
    exercice_debut = col_j.text_input("Debut exercice", key="selarl_exercice_debut")
    exercice_fin = col_k.text_input("Fin exercice", key="selarl_exercice_fin")
    exercice_cloture_premier = col_l.text_input(
        "Cloture premier exercice",
        key="selarl_exercice_cloture_premier",
    )
    autre_lieu_exercice = st.checkbox(
        "Autre lieu d'exercice ?",
        value=False,
        key="selarl_autre_lieu_exercice",
    )
    lieu_exercice_adresse = ""
    if autre_lieu_exercice:
        siege_display = _siege_display(societe)
        if "selarl_lieu_exercice_adresse" not in st.session_state:
            st.session_state["selarl_lieu_exercice_adresse"] = siege_display
        lieu_exercice_adresse = st.text_input(
            "Adresse du lieu d'exercice",
            key="selarl_lieu_exercice_adresse",
        )
    return {
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
        "signature_nombre_exemplaires": "quatre",
        "decision_date": decision_date,
        "depot_banque_nom": depot_banque_nom,
        "depot_banque_adresse": depot_banque_adresse,
        "exercice_debut": exercice_debut,
        "exercice_fin": exercice_fin,
        "exercice_cloture_premier": exercice_cloture_premier,
        "lieu_exercice_adresse": lieu_exercice_adresse,
    }


def _date_input_with_today(label: str, *, key: str, value: date) -> date | None:
    current_value = st.session_state.get(key)
    if isinstance(current_value, date):
        st.session_state[key] = format_french_date(current_value)
    elif current_value is None:
        st.session_state[key] = format_french_date(value)

    button_col, input_col = st.columns([1, 3])
    if button_col.button("Aujourd'hui", key=f"{key}_today"):
        st.session_state[key] = format_french_date(date.today())
    raw_value = input_col.text_input(
        label,
        key=key,
        placeholder="JJ/MM/AAAA",
    )
    parsed = parse_french_date(raw_value)
    if str(raw_value).strip() and parsed is None:
        input_col.caption("Format attendu : JJ/MM/AAAA")
    return parsed


def _siege_display(societe: dict[str, object]) -> str:
    return (
        f"{societe.get('siege_num_voie', '')} "
        f"{societe.get('siege_voie', '')}, "
        f"{societe.get('siege_cp', '')} "
        f"{societe.get('siege_ville', '')}"
    ).strip(" ,")


def _render_conjoint(
    *,
    profession: str,
    regime_communautaire: bool,
    situation_maritale: object,
) -> dict[str, object]:
    is_married = "marie" in str(situation_maritale).casefold()
    if profession != PROFESSION_DENTISTE and not regime_communautaire and not is_married:
        return {
            "conjoint_civilite": "",
            "conjoint_genre": derive_gender_from_civilite("Madame"),
            "conjoint_prenom": "",
            "conjoint_nom": "",
            "qualite_renoncee": "associé",
            "date_courrier_avertissement": None,
        }

    st.markdown("**Conjoint**")
    col_a, col_c, col_d = st.columns(3)
    conjoint_civilite = col_a.selectbox(
        "Civilite conjoint",
        ("Madame", "Monsieur"),
        key="selarl_conjoint_civilite",
    )
    conjoint_prenom = col_c.text_input("Prenom conjoint", key="selarl_conjoint_prenom")
    conjoint_nom = col_d.text_input("Nom conjoint", key="selarl_conjoint_nom")
    qualite_renoncee = "associé"
    date_courrier_avertissement = None
    if regime_communautaire:
        date_courrier_avertissement = date.today()
    return {
        "conjoint_civilite": conjoint_civilite,
        "conjoint_genre": derive_gender_from_civilite(conjoint_civilite),
        "conjoint_prenom": conjoint_prenom,
        "conjoint_nom": conjoint_nom,
        "qualite_renoncee": qualite_renoncee,
        "date_courrier_avertissement": date_courrier_avertissement,
    }


CESSION_TYPE_LABELS: dict[str, str] = {"medical": "medical", "dentaire": "dentaire"}
CESSION_ETAPE_LABELS: dict[str, str] = {"acte": "acte", "compromis": "compromis"}


def _cession_default_type(profession: str) -> str:
    return "dentaire" if profession == PROFESSION_DENTISTE else "medical"


def _seed_default(key: str, default: object) -> None:
    if key not in st.session_state:
        st.session_state[key] = default


def _cession_text(
    container: object,
    label: str,
    *,
    section: str,
    field: str,
    default: str,
) -> str:
    key = f"selarl_cession_{section}_{field}"
    _seed_default(key, default)
    value = container.text_input(label, key=key)
    return str(value).strip()


def _render_cession_form(cession: bool, profession: str) -> tuple[
    CessionContext | None, BailContext | None
]:
    """Sous-formulaire de saisie CESSION (cabinet medical / dentaire).

    Retourne (None, None) si la cession n'est pas demandee. Sinon, construit un
    `CessionContext` complet et valide en fusionnant les saisies sur la fixture
    scenario adaptee a la profession (medical / dentaire), ainsi que l'avenant
    de bail associe (DOC-007). Les champs profonds non exposes restent ceux de
    la fixture, garantissant une generation sans token residuel ; les valeurs de
    test prerempissent les cles, l'utilisateur peut editer.
    """
    if not cession:
        return None, None

    st.markdown("**Cession de cabinet**")
    base_cession, base_bail = cession_fixture_for_profession(profession)
    payload = base_cession.model_dump(by_alias=True)

    with st.expander("Type & etape", expanded=True):
        col_a, col_b = st.columns(2)
        type_default = _cession_default_type(profession)
        type_options = tuple(CESSION_TYPE_LABELS)
        type_key = "selarl_cession_meta_type_cabinet"
        _seed_default(type_key, type_default)
        type_cabinet = col_a.selectbox(
            "Type de cabinet",
            type_options,
            key=type_key,
        )
        etape_key = "selarl_cession_meta_etape"
        _seed_default(etape_key, "acte")
        etape = col_b.selectbox(
            "Etape",
            tuple(CESSION_ETAPE_LABELS),
            key=etape_key,
        )
    payload["type_cabinet"] = type_cabinet
    payload["etape"] = etape

    vendeur = payload.setdefault("vendeur", {})
    with st.expander("Vendeur"):
        col_a, col_b, col_c = st.columns(3)
        vendeur["civilite_affichage"] = _cession_text(
            col_a, "Civilite", section="vendeur", field="civilite",
            default=str(vendeur.get("civilite_affichage") or ""),
        )
        vendeur["prenom"] = _cession_text(
            col_b, "Prenom", section="vendeur", field="prenom",
            default=str(vendeur.get("prenom") or ""),
        )
        vendeur["nom"] = _cession_text(
            col_c, "Nom", section="vendeur", field="nom",
            default=str(vendeur.get("nom") or ""),
        )
        col_d, col_e = st.columns(2)
        vendeur["numero_ordre"] = _cession_text(
            col_d, "Numero Ordre", section="vendeur", field="numero_ordre",
            default=str(vendeur.get("numero_ordre") or ""),
        )
        vendeur["numero_rpps"] = _cession_text(
            col_e, "Numero RPPS", section="vendeur", field="numero_rpps",
            default=str(vendeur.get("numero_rpps") or ""),
        )
        vendeur["adresse_affichee"] = _cession_text(
            st, "Adresse personnelle (affichee)", section="vendeur", field="adresse",
            default=str(vendeur.get("adresse_affichee") or ""),
        )

    acquereur = payload.setdefault("acquereur", {})
    with st.expander("Acquereur (societe)"):
        acquereur["denomination_societe"] = _cession_text(
            st, "Denomination societe", section="acquereur", field="denomination",
            default=str(acquereur.get("denomination_societe") or ""),
        )
        col_a, col_b = st.columns(2)
        acquereur["rcs_ville"] = _cession_text(
            col_a, "RCS (ville)", section="acquereur", field="rcs_ville",
            default=str(acquereur.get("rcs_ville") or ""),
        )
        acquereur["numero_rcs"] = _cession_text(
            col_b, "Numero RCS", section="acquereur", field="numero_rcs",
            default=str(acquereur.get("numero_rcs") or ""),
        )
        siege = acquereur.setdefault("siege", {}) or {}
        siege["adresse_affichee"] = _cession_text(
            st, "Siege (adresse affichee)", section="acquereur", field="siege",
            default=str(siege.get("adresse_affichee") or ""),
        )
        acquereur["siege"] = siege

    cabinet = payload.setdefault("cabinet", {})
    with st.expander("Cabinet"):
        cabinet["nature_fonds_liberal"] = _cession_text(
            st, "Nature du fonds liberal", section="cabinet", field="nature",
            default=str(cabinet.get("nature_fonds_liberal") or ""),
        )
        cabinet["denomination_ou_adresse_affichee"] = _cession_text(
            st, "Denomination ou adresse", section="cabinet", field="denomination",
            default=str(cabinet.get("denomination_ou_adresse_affichee") or ""),
        )
        cabinet["adresse_affichee"] = _cession_text(
            st, "Adresse cabinet", section="cabinet", field="adresse",
            default=str(cabinet.get("adresse_affichee") or ""),
        )

    bail = payload.setdefault("bail_professionnel", {}) or {}
    with st.expander("Bail professionnel"):
        col_a, col_b = st.columns(2)
        bail["duree"] = _cession_text(
            col_a, "Duree du bail", section="bail", field="duree",
            default=str(bail.get("duree") or ""),
        )
        bail["loyer_mensuel"] = _cession_text(
            col_b, "Loyer mensuel", section="bail", field="loyer",
            default=str(bail.get("loyer_mensuel") or ""),
        )
        bail["activite_autorisee_affichee"] = _cession_text(
            st, "Activite autorisee", section="bail", field="activite",
            default=str(bail.get("activite_autorisee_affichee") or ""),
        )
    payload["bail_professionnel"] = bail

    exercices = list(payload.get("exercices") or [])
    with st.expander("Exercices (3)"):
        for index in range(3):
            existing = exercices[index] if index < len(exercices) else {}
            col_a, col_b, col_c = st.columns(3)
            periode = _cession_text(
                col_a, f"Periode {index + 1}", section="exercice", field=f"{index}_periode",
                default=str(existing.get("periode") or ""),
            )
            ca = _cession_text(
                col_b, f"CA {index + 1}", section="exercice", field=f"{index}_ca",
                default=str(existing.get("chiffre_affaires") or ""),
            )
            resultat = _cession_text(
                col_c, f"Resultat {index + 1}", section="exercice", field=f"{index}_resultat",
                default=str(existing.get("resultat") or ""),
            )
            if index < len(exercices):
                exercices[index] = {
                    "periode": periode,
                    "chiffre_affaires": ca,
                    "resultat": resultat,
                }
    payload["exercices"] = exercices

    prix = payload.setdefault("prix", {}) or {}
    with st.expander("Prix"):
        col_a, col_b = st.columns(2)
        prix["total"] = _cession_text(
            col_a, "Prix total", section="prix", field="total",
            default=str(prix.get("total") or ""),
        )
        prix["total_lettres"] = _cession_text(
            col_b, "Prix total (lettres)", section="prix", field="total_lettres",
            default=str(prix.get("total_lettres") or ""),
        )
        col_c, col_d = st.columns(2)
        prix["elements_corporels"] = _cession_text(
            col_c, "Elements corporels", section="prix", field="corporels",
            default=str(prix.get("elements_corporels") or ""),
        )
        prix["elements_incorporels"] = _cession_text(
            col_d, "Elements incorporels", section="prix", field="incorporels",
            default=str(prix.get("elements_incorporels") or ""),
        )
    payload["prix"] = prix

    financement = payload.setdefault("financement", {}) or {}
    with st.expander("Financement"):
        banque = financement.setdefault("banque", {}) or {}
        banque["nom"] = _cession_text(
            st, "Banque", section="financement", field="banque",
            default=str(banque.get("nom") or ""),
        )
        financement["banque"] = banque
        col_a, col_b = st.columns(2)
        financement["montant_deblocage"] = _cession_text(
            col_a, "Montant deblocage", section="financement", field="deblocage",
            default=str(financement.get("montant_deblocage") or ""),
        )
        pret = financement.setdefault("pret", {}) or {}
        pret["montant"] = _cession_text(
            col_b, "Montant pret", section="financement", field="pret_montant",
            default=str(pret.get("montant") or ""),
        )
        financement["pret"] = pret
        credit_default = financement.get("credit_vendeur") or {}
        credit_key = "selarl_cession_financement_credit_actif"
        _seed_default(credit_key, bool(credit_default.get("actif")))
        credit_actif = st.checkbox("Credit-vendeur", key=credit_key)
        if credit_actif:
            col_c, col_d, col_e = st.columns(3)
            credit = {
                "actif": True,
                "montant": _cession_text(
                    col_c, "Montant credit-vendeur", section="financement",
                    field="credit_montant",
                    default=str(credit_default.get("montant") or ""),
                ),
                "duree": _cession_text(
                    col_d, "Duree credit-vendeur (annees)", section="financement",
                    field="credit_duree",
                    default=str(credit_default.get("duree") or ""),
                ),
                "taux": _cession_text(
                    col_e, "Taux credit-vendeur", section="financement",
                    field="credit_taux",
                    default=str(credit_default.get("taux") or ""),
                ),
                "majoration_interet_retard": str(
                    credit_default.get("majoration_interet_retard") or ""
                ),
            }
            financement["credit_vendeur"] = credit
        else:
            financement["credit_vendeur"] = None
    payload["financement"] = financement

    if type_cabinet == "dentaire":
        salaries = list(payload.get("salaries") or [])
        with st.expander("Salaries (cabinet dentaire)"):
            for index in range(max(2, len(salaries))):
                existing = salaries[index] if index < len(salaries) else {}
                col_a, col_b, col_c = st.columns(3)
                civilite = _cession_text(
                    col_a, f"Civilite salarie {index + 1}", section="salarie",
                    field=f"{index}_civilite",
                    default=str(existing.get("civilite_affichage") or ""),
                )
                prenom = _cession_text(
                    col_b, f"Prenom salarie {index + 1}", section="salarie",
                    field=f"{index}_prenom",
                    default=str(existing.get("prenom") or ""),
                )
                nom = _cession_text(
                    col_c, f"Nom salarie {index + 1}", section="salarie",
                    field=f"{index}_nom",
                    default=str(existing.get("nom") or ""),
                )
                if index < len(salaries):
                    salaries[index] = {
                        "civilite_affichage": civilite,
                        "prenom": prenom,
                        "nom": nom,
                        "poste": existing.get("poste"),
                    }
        payload["salaries"] = salaries

    cession_context = CessionContext.model_validate(payload)
    return cession_context, base_bail


def _render_scm_cession_form(scm: bool) -> ScmCessionContext | None:
    """Sous-formulaire de cession de parts de SCM standalone (DOC-031/032/033).

    Plus court que la cession de cabinet : reutilise la fixture SCM comme base
    complete et expose les champs cles. Retourne None si non demande.
    """
    if not scm:
        return None

    st.markdown("**Cession de parts de SCM**")
    base = scm_cession_fixture()
    payload = base.model_dump(by_alias=True)

    scm_cedee = payload.setdefault("scm_cedee", {}) or {}
    with st.expander("SCM cedee", expanded=True):
        scm_cedee["denomination"] = _cession_text(
            st, "Denomination SCM", section="scm_cedee", field="denomination",
            default=str(scm_cedee.get("denomination") or ""),
        )
        col_a, col_b = st.columns(2)
        scm_cedee["ville_rcs"] = _cession_text(
            col_a, "RCS (ville)", section="scm_cedee", field="rcs_ville",
            default=str(scm_cedee.get("ville_rcs") or ""),
        )
        scm_cedee["numero_rcs"] = _cession_text(
            col_b, "Numero RCS", section="scm_cedee", field="numero_rcs",
            default=str(scm_cedee.get("numero_rcs") or ""),
        )
    payload["scm_cedee"] = scm_cedee

    cedant = payload.setdefault("cedant", {}) or {}
    with st.expander("Cedant"):
        col_a, col_b, col_c = st.columns(3)
        cedant["civilite_affichage"] = _cession_text(
            col_a, "Civilite", section="scm_cedant", field="civilite",
            default=str(cedant.get("civilite_affichage") or ""),
        )
        cedant["prenom"] = _cession_text(
            col_b, "Prenom", section="scm_cedant", field="prenom",
            default=str(cedant.get("prenom") or ""),
        )
        cedant["nom"] = _cession_text(
            col_c, "Nom", section="scm_cedant", field="nom",
            default=str(cedant.get("nom") or ""),
        )
    payload["cedant"] = cedant

    parts_cedees = payload.setdefault("parts_cedees", {}) or {}
    prix = payload.setdefault("prix", {}) or {}
    with st.expander("Parts cedees & prix"):
        col_a, col_b = st.columns(2)
        plage = _cession_text(
            col_a, "Plage parts cedees", section="scm_parts", field="plage",
            default=str(parts_cedees.get("plage") or ""),
        )
        parts_cedees["plage"] = plage
        prix["global"] = _cession_text(
            col_b, "Prix global", section="scm_prix", field="global",
            default=str(prix.get("global") or ""),
        )
        prix["global_lettres"] = _cession_text(
            st, "Prix global (lettres)", section="scm_prix", field="global_lettres",
            default=str(prix.get("global_lettres") or ""),
        )
    payload["parts_cedees"] = parts_cedees
    payload["prix"] = prix

    return ScmCessionContext.model_validate(payload)


def _render_generation_zone(data_entry: CleanDataEntry, plan: CleanGenerationPlan) -> None:
    st.subheader("Generation")
    for warning in plan.warnings:
        st.info(warning)
    if plan.can_generate:
        st.success(plan.reason)
    else:
        st.warning(plan.reason)
    if plan.blockers:
        for blocker in plan.blockers[:8]:
            st.caption(f"Blocage : {blocker}")
        if len(plan.blockers) > 8:
            st.caption(f"{len(plan.blockers) - 8} autres champs requis.")

    st.markdown("Documents")
    for row in plan.document_rows:
        st.caption(f"{row.doc_code} - {row.label} - {row.status} : {row.message}")

    if plan.front_data_scope:
        st.caption("Fondations front_data utilisees : " + " | ".join(plan.front_data_scope))

    if st.button(
        "Generer le dossier",
        key="clean_generate_dossier",
        disabled=not plan.can_generate,
        type="primary",
    ):
        try:
            result = generate_selarl_dossier(
                data_entry,
                _output_dir(data_entry.dossier_reference),
            )
        except Exception as exc:
            st.error(f"Generation bloquee par le moteur : {exc}")
            return
        st.session_state[GENERATED_DOSSIER_STATE_KEY] = {
            "output_dir": str(result.output_dir),
            "zip_path": str(result.zip_path),
            "docx_paths": [str(path) for path in result.docx_paths],
        }

    generated_dossier = st.session_state.get(GENERATED_DOSSIER_STATE_KEY)
    if isinstance(generated_dossier, dict):
        _render_generated_dossier_downloads(generated_dossier)


def _output_dir(dossier_reference: str) -> Path:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", dossier_reference).strip("._")
    return ARTIFACTS_DIR / (slug or "selarl_v1")


def _render_generated_dossier_downloads(generated_dossier: dict[str, object]) -> None:
    output_dir = generated_dossier.get("output_dir", "")
    zip_path = Path(str(generated_dossier.get("zip_path", "")))
    docx_paths = [
        Path(str(path))
        for path in generated_dossier.get("docx_paths", [])
        if isinstance(path, str)
    ]

    st.success(f"Dossier genere : {output_dir}")
    st.caption(f"ZIP : {zip_path}")
    if zip_path.is_file():
        st.download_button(
            "Telecharger le dossier ZIP",
            data=zip_path.read_bytes(),
            file_name=zip_path.name,
            mime="application/zip",
            key="clean_download_zip",
            type="primary",
            on_click="ignore",
        )
    else:
        st.error("ZIP genere introuvable sur le serveur.")

    for index, path in enumerate(docx_paths):
        st.caption(f"DOCX : {path}")
        if not path.is_file():
            st.error(f"DOCX genere introuvable : {path.name}")
            continue
        st.download_button(
            f"Telecharger {path.name}",
            data=path.read_bytes(),
            file_name=path.name,
            mime=DOCX_MIME_TYPE,
            key=f"clean_download_docx_{index}",
            on_click="ignore",
        )
