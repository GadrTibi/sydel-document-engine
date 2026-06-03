from __future__ import annotations

import random
import re
from datetime import date
from pathlib import Path

import streamlit as st

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
    SelarlAdditionalAssocieInput,
    generate_selarl_dossier,
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
    st.caption(
        "Perimetre actif : SELARL unipersonnelle de production, DOC-004 multi-associes "
        "limite ou statuts dentiste PARTIAL."
    )
    return dossier_type_by_label(selected_label)


def _prefill_random_selarl_data() -> None:
    person = random.choice(_test_people())
    company = random.choice(_test_companies())
    capital, parts = random.choice(((1000, 100), (2000, 200), (5000, 500), (10000, 1000)))
    profession_label = random.choice(("Medecin", "Chirurgien-dentiste"))
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

    values = {
        "selarl_profession": profession_label,
        "selarl_dossier_unipersonnel": True,
        "selarl_regime_communautaire": regime_communautaire,
        "selarl_derogation": False,
        "selarl_site_distinct": False,
        "selarl_cession": False,
        "selarl_scm": False,
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
    st.session_state.update(values)
    st.session_state.pop(GENERATED_DOSSIER_STATE_KEY, None)


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
    societe = _render_societe(
        multi_associes_simple=bool(
            qualification["multi_associes_doc004_limited"]
            or qualification["dentist_multi_associes_statuts_partial"]
        ),
        dentist_multi_associes_statuts_partial=bool(
            qualification["dentist_multi_associes_statuts_partial"]
        ),
        praticien=praticien,
    )
    ordre_mandataire = _render_ordre_mandataire()
    generation_context = _render_generation_context(societe)
    conjoint = _render_conjoint(
        profession=qualification["profession"],
        regime_communautaire=qualification["regime_communautaire"],
        situation_maritale=praticien["situation_maritale"],
    )
    return build_clean_data_entry(
        dossier_type,
        **qualification,
        **praticien,
        **societe,
        **ordre_mandataire,
        **generation_context,
        **conjoint,
    )


def _render_qualification() -> dict[str, object]:
    st.markdown("**Qualification**")
    profession_label = st.selectbox(
        "Profession",
        ("Medecin", "Chirurgien-dentiste"),
        key="selarl_profession",
    )
    case_options = [
        "SELARL unipersonnelle production",
        "SELARL multi-associes simple (limite DOC-004)",
    ]
    if profession_label == "Chirurgien-dentiste":
        case_options.append("SELARL dentiste multi-associes simple (PARTIAL statuts)")
    case_label = st.selectbox(
        "Cas SELARL",
        tuple(case_options),
        key="selarl_case_mode",
    )
    dentist_multi_associes_statuts_partial = "PARTIAL statuts" in case_label
    multi_associes_doc004_limited = case_label.startswith("SELARL multi-associes")
    multi_associes_simple = (
        multi_associes_doc004_limited or dentist_multi_associes_statuts_partial
    )
    col_a, col_b, col_c = st.columns(3)
    if multi_associes_simple:
        dossier_unipersonnel = False
        col_a.caption(
            "Plusieurs associes : DOC-004 + DOC-016 PARTIAL."
            if dentist_multi_associes_statuts_partial
            else "Plusieurs associes : DOC-004 uniquement."
        )
        col_b.caption("Gerant unique rattache au praticien.")
        col_c.caption(
            "Statuts multi-associes PARTIAL."
            if dentist_multi_associes_statuts_partial
            else "Statuts multi-associes non generes."
        )
        regime_communautaire = False
    else:
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
    if multi_associes_doc004_limited:
        st.info(
            "Sous-cas limite : DOC-004 uniquement, gerant unique, president choisi "
            "parmi les associes, unanimite totale."
        )
    if dentist_multi_associes_statuts_partial:
        st.info(
            "Sous-cas limite : DOC-004 et DOC-016 dentiste PARTIAL, gerant unique, "
            "president choisi parmi les associes, unanimite totale."
        )

    st.markdown("**Cas hors perimetre V1**")
    out_a, out_b, out_c, out_d = st.columns(4)
    derogation = out_a.checkbox("Derogation", value=False, key="selarl_derogation")
    site_distinct = out_b.checkbox("Site distinct", value=False, key="selarl_site_distinct")
    cession = out_c.checkbox("Cession", value=False, key="selarl_cession")
    scm = out_d.checkbox("SCM", value=False, key="selarl_scm")

    return {
        "dossier_reference": st.text_input(
            "Reference dossier",
            key="selarl_dossier_reference",
        ),
        "profession": (
            PROFESSION_DENTISTE if profession_label == "Chirurgien-dentiste" else PROFESSION_MEDECIN
        ),
        "dossier_unipersonnel": dossier_unipersonnel,
        "multi_associes_doc004_limited": multi_associes_doc004_limited,
        "dentist_multi_associes_statuts_partial": dentist_multi_associes_statuts_partial,
        "regime_communautaire": regime_communautaire,
        "derogation": derogation,
        "site_distinct": site_distinct,
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
    multi_associes_simple: bool,
    dentist_multi_associes_statuts_partial: bool,
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
    multi_associes_data: dict[str, object] = {
        "associe_principal_nb_parts": int(nb_parts_total),
        "additional_associes": (),
        "president_seance_associe_index": 0,
    }
    if multi_associes_simple:
        multi_associes_data = _render_multi_associes_simple_block(
            nb_parts_total=int(nb_parts_total),
            praticien=praticien,
            include_statuts=dentist_multi_associes_statuts_partial,
        )
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
            **multi_associes_data,
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
        **multi_associes_data,
        "ville_rcs": ville_rcs,
        "siege_num_voie": adr_a.text_input("Numero", key="selarl_siege_num_voie"),
        "siege_voie": adr_b.text_input("Voie", key="selarl_siege_voie"),
        "siege_cp": adr_c.text_input("Code postal", key="selarl_siege_cp"),
        "siege_ville": adr_d.text_input("Ville", key="selarl_siege_ville"),
    }


def _render_multi_associes_simple_block(
    *,
    nb_parts_total: int,
    praticien: dict[str, object],
    include_statuts: bool,
) -> dict[str, object]:
    st.markdown(
        "**Associes pour DOC-004 et DOC-016 PARTIAL**"
        if include_statuts
        else "**Associes pour DOC-004 limite**"
    )
    st.caption(
        "Tous les associes saisis ici sont reputes presents ou representes et "
        "detiennent ensemble la totalite des parts."
    )
    associes_count = st.number_input(
        "Nombre d'associes pour le sous-cas"
        if include_statuts
        else "Nombre d'associes pour DOC-004",
        min_value=2,
        max_value=6,
        step=1,
        value=2,
        key="selarl_doc004_associes_count",
    )
    principal_default = nb_parts_total if nb_parts_total > 0 else 1
    principal_parts = st.number_input(
        "Parts de l'associe 1 / gerant unique",
        min_value=1,
        step=1,
        value=principal_default,
        key="selarl_doc004_associe_1_parts",
    )
    additional_associes: list[SelarlAdditionalAssocieInput] = []
    for index in range(2, int(associes_count) + 1):
        col_a, col_b, col_c, col_d = st.columns(4)
        civilite = col_a.selectbox(
            f"Civilite associe {index}",
            ("Monsieur", "Madame"),
            key=f"selarl_doc004_associe_{index}_civilite",
        )
        prenom = col_b.text_input(
            f"Prenom associe {index}",
            key=f"selarl_doc004_associe_{index}_prenom",
        )
        nom = col_c.text_input(
            f"Nom associe {index}",
            key=f"selarl_doc004_associe_{index}_nom",
        )
        nb_parts = col_d.number_input(
            f"Parts associe {index}",
            min_value=1,
            step=1,
            value=1,
            key=f"selarl_doc004_associe_{index}_parts",
        )
        additional_associes.append(
            SelarlAdditionalAssocieInput(
                civilite=civilite,
                prenom=prenom,
                nom=nom,
                nb_parts=int(nb_parts),
            )
        )

    labels = [_associe_label(1, praticien.get("prenom"), praticien.get("nom"))]
    labels.extend(
        _associe_label(index, associe.prenom, associe.nom)
        for index, associe in enumerate(additional_associes, start=2)
    )
    president_index = st.selectbox(
        "President de seance",
        list(range(len(labels))),
        format_func=lambda index: labels[index],
        key="selarl_doc004_president_index",
    )
    return {
        "associe_principal_nb_parts": int(principal_parts),
        "additional_associes": tuple(additional_associes),
        "president_seance_associe_index": int(president_index),
    }


def _associe_label(index: int, prenom: object, nom: object) -> str:
    full_name = f"{prenom or ''} {nom or ''}".strip()
    return f"Associe {index}" if not full_name else f"Associe {index} - {full_name}"


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
            "qualite_renoncee": "associe",
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
    qualite_renoncee = "associe"
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
