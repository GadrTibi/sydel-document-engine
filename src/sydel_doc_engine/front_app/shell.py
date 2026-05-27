from __future__ import annotations

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
    generate_selarl_dossier,
)

ARTIFACTS_DIR = Path("artifacts") / "track_b_selarl_v1"


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
    st.caption(
        "Perimetre actif : creation SELARL medecin ou chirurgien-dentiste, associe unique."
    )
    return dossier_type_by_label(selected_label)


def _render_data_entry_zone(dossier_type: DossierTypeOption) -> CleanDataEntry:
    st.subheader("Donnees a saisir")
    qualification = _render_qualification()
    praticien = _render_praticien(
        regime_communautaire=bool(qualification["regime_communautaire"])
    )
    societe = _render_societe()
    ordre_mandataire = _render_ordre_mandataire()
    generation_context = _render_generation_context(societe)
    conjoint = _render_conjoint(
        profession=qualification["profession"],
        regime_communautaire=qualification["regime_communautaire"],
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
    col_c.caption("Active DOC-005. DOC-006 reste reserve.")

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


def _render_societe() -> dict[str, object]:
    st.markdown("**Fiche Societe**")
    col_a, col_b = st.columns(2)
    denomination = col_a.text_input("Denomination sociale", key="selarl_denomination")
    capital_social = col_b.number_input(
        "Capital social (?)",
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
    col_h, col_i = st.columns(2)
    duree = col_h.text_input("Duree sociale", value="99 ans", key="selarl_duree")
    ville_rcs = col_i.text_input("RCS (ville)", key="selarl_ville_rcs")

    st.markdown("Siege social")
    adr_a, adr_b, adr_c, adr_d = st.columns(4)
    return {
        "denomination": denomination,
        "capital_social": format_numeric_value(capital_social),
        "duree": duree,
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
    col_a, col_b = st.columns(2)
    ordre_conseil = col_a.text_input(
        "Conseil departemental de l'ordre (libelle complet)",
        key="selarl_ordre_conseil",
        help="Exemple : Conseil departemental de l'Ordre des medecins de Paris.",
    )
    departement_ordre = col_b.text_input(
        "Departement d'inscription a l'ordre",
        key="selarl_departement_ordre",
        help="Exemple : 75, Paris ou le departement ordinal attendu par le dossier.",
    )
    col_c, col_d, col_e = st.columns(3)
    ordre_adresse_ligne_1 = col_c.text_input(
        "Adresse ordre",
        key="selarl_ordre_adresse_ligne_1",
    )
    ordre_cp = col_d.text_input("CP ordre", key="selarl_ordre_cp")
    ordre_ville = col_e.text_input("Ville ordre", key="selarl_ordre_ville")
    return {
        "ordre_conseil": ordre_conseil,
        "departement_ordre": departement_ordre,
        "ordre_adresse_ligne_1": ordre_adresse_ligne_1,
        "ordre_cp": ordre_cp,
        "ordre_ville": ordre_ville,
    }


def _render_generation_context(societe: dict[str, object]) -> dict[str, object]:
    st.markdown("**Generation**")
    col_a, col_b, col_c = st.columns(3)
    signature_lieu = col_a.text_input("Lieu de signature", key="selarl_signature_lieu")
    with col_b:
        signature_date = _date_input_with_today(
            "Date de signature",
            key="selarl_signature_date",
            value=date.today(),
        )
    signature_nombre_exemplaires = col_c.number_input(
        "Nombre d'exemplaires",
        min_value=1,
        step=1,
        value=2,
        key="selarl_signature_nombre_exemplaires",
    )
    col_d, col_f = st.columns(2)
    with col_d:
        decision_date = _date_input_with_today(
            "Date de decision",
            key="selarl_decision_date",
            value=date.today(),
        )
    reunion_heure = col_f.text_input("Heure de decision", key="selarl_reunion_heure")
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
        "signature_nombre_exemplaires": signature_nombre_exemplaires,
        "decision_date": decision_date,
        "reunion_heure": reunion_heure,
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
) -> dict[str, object]:
    if profession != PROFESSION_DENTISTE and not regime_communautaire:
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
        col_e, col_f = st.columns(2)
        qualite_renoncee = col_e.text_input(
            "Qualite renoncee",
            value="associe",
            key="selarl_qualite_renoncee",
        )
        with col_f:
            date_courrier_avertissement = _date_input_with_today(
                "Date courrier avertissement",
                key="selarl_date_courrier_avertissement",
                value=date.today(),
            )
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
        st.success(f"Dossier genere : {result.output_dir}")
        st.caption(f"ZIP : {result.zip_path}")
        for path in result.docx_paths:
            st.caption(f"DOCX : {path}")


def _output_dir(dossier_reference: str) -> Path:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", dossier_reference).strip("._")
    return ARTIFACTS_DIR / (slug or "selarl_v1")
