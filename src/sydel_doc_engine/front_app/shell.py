from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import streamlit as st

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.front_app.data_entry import (
    CleanDataEntry,
    build_clean_data_entry,
)
from sydel_doc_engine.front_app.dossier_selection import (
    DossierTypeOption,
    dossier_type_by_label,
    dossier_type_labels,
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
    praticien = _render_praticien()
    societe = _render_societe()
    ordre_mandataire = _render_ordre_mandataire()
    generation_context = _render_generation_context()
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
        "Regime communautaire",
        value=False,
        key="selarl_regime_communautaire",
    )
    col_c.caption("DOC-005 seulement si regime communautaire actif.")

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


def _render_praticien() -> dict[str, object]:
    st.markdown("**Fiche Client / Praticien**")
    col_a, col_b, col_c = st.columns(3)
    civilite = col_a.text_input("Civilite", key="selarl_civilite")
    genre_label = col_b.selectbox("Genre", ("Masculin", "Feminin"), key="selarl_genre")
    titre_affichage = col_c.text_input("Titre affichage", key="selarl_titre_affichage")
    col_d, col_e = st.columns(2)
    prenom = col_d.text_input("Prenom", key="selarl_prenom")
    nom = col_e.text_input("Nom", key="selarl_nom")
    col_f, col_g, col_h = st.columns(3)
    date_naissance = col_f.date_input(
        "Date de naissance",
        value=date(1990, 1, 1),
        key="selarl_date_naissance",
    )
    ville_naissance = col_g.text_input("Ville de naissance", key="selarl_ville_naissance")
    departement_naissance = col_h.text_input(
        "Departement naissance",
        key="selarl_departement_naissance",
    )
    col_i, col_j = st.columns(2)
    nationalite = col_i.text_input("Nationalite", key="selarl_nationalite")
    situation_maritale = col_j.text_input(
        "Situation matrimoniale",
        key="selarl_situation_maritale",
    )
    col_k, col_l = st.columns(2)
    regime_matrimonial = col_k.text_input(
        "Regime matrimonial",
        key="selarl_regime_matrimonial",
    )
    numero_ordre = col_l.text_input("Numero Ordre", key="selarl_numero_ordre")
    col_m, col_n, col_o = st.columns(3)
    numero_rpps = col_m.text_input("Numero RPPS", key="selarl_numero_rpps")
    nom_pere = col_n.text_input("Nom du pere", key="selarl_nom_pere")
    nom_mere = col_o.text_input("Nom de la mere", key="selarl_nom_mere")

    st.markdown("Adresse personnelle")
    adr_a, adr_b, adr_c, adr_d = st.columns(4)
    return {
        "civilite": civilite,
        "genre": Gender.FEMININ if genre_label == "Feminin" else Gender.MASCULIN,
        "prenom": prenom,
        "nom": nom,
        "titre_affichage": titre_affichage,
        "date_naissance": date_naissance,
        "ville_naissance": ville_naissance,
        "departement_naissance": departement_naissance,
        "nationalite": nationalite,
        "nom_pere": nom_pere,
        "nom_mere": nom_mere,
        "situation_maritale": situation_maritale,
        "regime_matrimonial": regime_matrimonial,
        "numero_ordre": numero_ordre,
        "numero_rpps": numero_rpps,
        "adresse_num_voie": adr_a.text_input("No", key="selarl_adresse_num_voie"),
        "adresse_voie": adr_b.text_input("Voie", key="selarl_adresse_voie"),
        "adresse_cp": adr_c.text_input("CP", key="selarl_adresse_cp"),
        "adresse_ville": adr_d.text_input("Ville", key="selarl_adresse_ville"),
    }


def _render_societe() -> dict[str, object]:
    st.markdown("**Fiche Societe**")
    col_a, col_b, col_c = st.columns(3)
    denomination = col_a.text_input("Denomination", key="selarl_denomination")
    capital_social = col_b.text_input("Capital social", key="selarl_capital_social")
    capital_social_lettres = col_c.text_input(
        "Capital social en lettres",
        key="selarl_capital_social_lettres",
    )
    col_d, col_e, col_f, col_g = st.columns(4)
    nb_parts_total = col_d.number_input(
        "Nombre de parts",
        min_value=0,
        step=1,
        value=0,
        key="selarl_nb_parts_total",
    )
    nb_parts_total_lettres = col_e.text_input(
        "Nombre de parts en lettres",
        key="selarl_nb_parts_total_lettres",
    )
    valeur_nominale_part = col_f.text_input(
        "Valeur nominale",
        key="selarl_valeur_nominale_part",
    )
    valeur_nominale_part_lettres = col_g.text_input(
        "Valeur nominale en lettres",
        key="selarl_valeur_nominale_part_lettres",
    )
    col_h, col_i = st.columns(2)
    duree = col_h.text_input("Duree sociale", value="99 ans", key="selarl_duree")
    ville_rcs = col_i.text_input("Ville RCS", key="selarl_ville_rcs")

    st.markdown("Siege social")
    adr_a, adr_b, adr_c, adr_d = st.columns(4)
    return {
        "denomination": denomination,
        "capital_social": capital_social,
        "capital_social_lettres": capital_social_lettres,
        "duree": duree,
        "nb_parts_total": int(nb_parts_total),
        "nb_parts_total_lettres": nb_parts_total_lettres,
        "valeur_nominale_part": valeur_nominale_part,
        "valeur_nominale_part_lettres": valeur_nominale_part_lettres,
        "ville_rcs": ville_rcs,
        "siege_num_voie": adr_a.text_input("No siege", key="selarl_siege_num_voie"),
        "siege_voie": adr_b.text_input("Voie siege", key="selarl_siege_voie"),
        "siege_cp": adr_c.text_input("CP siege", key="selarl_siege_cp"),
        "siege_ville": adr_d.text_input("Ville siege", key="selarl_siege_ville"),
    }


def _render_ordre_mandataire() -> dict[str, object]:
    st.markdown("**Ordre et mandataire**")
    col_a, col_b = st.columns(2)
    ordre_conseil = col_a.text_input(
        "Conseil departemental de l'ordre",
        key="selarl_ordre_conseil",
    )
    departement_ordre = col_b.text_input(
        "Departement d'inscription",
        key="selarl_departement_ordre",
    )
    col_c, col_d, col_e = st.columns(3)
    ordre_adresse_ligne_1 = col_c.text_input(
        "Adresse ordre",
        key="selarl_ordre_adresse_ligne_1",
    )
    ordre_cp = col_d.text_input("CP ordre", key="selarl_ordre_cp")
    ordre_ville = col_e.text_input("Ville ordre", key="selarl_ordre_ville")
    col_f, col_g, col_h = st.columns(3)
    mandataire_civilite = col_f.text_input(
        "Civilite mandataire",
        value="Monsieur",
        key="selarl_mandataire_civilite",
    )
    mandataire_prenom = col_g.text_input(
        "Prenom mandataire",
        value="Jordan",
        key="selarl_mandataire_prenom",
    )
    mandataire_nom = col_h.text_input(
        "Nom mandataire",
        value="ELBAZ",
        key="selarl_mandataire_nom",
    )
    col_i, col_j = st.columns(2)
    mandataire_fonction = col_i.text_input(
        "Fonction mandataire",
        value="gerant",
        key="selarl_mandataire_fonction",
    )
    mandataire_cabinet = col_j.text_input(
        "Cabinet mandataire",
        value="SYDEL",
        key="selarl_mandataire_cabinet",
    )
    return {
        "ordre_conseil": ordre_conseil,
        "departement_ordre": departement_ordre,
        "ordre_adresse_ligne_1": ordre_adresse_ligne_1,
        "ordre_cp": ordre_cp,
        "ordre_ville": ordre_ville,
        "mandataire_civilite": mandataire_civilite,
        "mandataire_prenom": mandataire_prenom,
        "mandataire_nom": mandataire_nom,
        "mandataire_fonction": mandataire_fonction,
        "mandataire_cabinet": mandataire_cabinet,
    }


def _render_generation_context() -> dict[str, object]:
    st.markdown("**Generation**")
    col_a, col_b, col_c = st.columns(3)
    signature_lieu = col_a.text_input("Lieu de signature", key="selarl_signature_lieu")
    signature_date = col_b.date_input(
        "Date de signature",
        value=date.today(),
        key="selarl_signature_date",
    )
    signature_nombre_exemplaires = col_c.text_input(
        "Nombre d'exemplaires",
        key="selarl_signature_nombre_exemplaires",
    )
    col_d, col_e, col_f = st.columns(3)
    decision_date = col_d.date_input(
        "Date decision",
        value=date.today(),
        key="selarl_decision_date",
    )
    reunion_date_lettres = col_e.text_input(
        "Date reunion en lettres",
        key="selarl_reunion_date_lettres",
    )
    reunion_heure = col_f.text_input("Heure reunion", key="selarl_reunion_heure")
    col_g, col_h, col_i = st.columns(3)
    depot_banque_nom = col_g.text_input("Banque depot", key="selarl_depot_banque_nom")
    depot_banque_adresse = col_h.text_input(
        "Adresse banque",
        key="selarl_depot_banque_adresse",
    )
    prestataire_signature_electronique = col_i.text_input(
        "Prestataire signature electronique",
        key="selarl_prestataire_signature_electronique",
    )
    col_j, col_k, col_l = st.columns(3)
    exercice_debut = col_j.text_input("Debut exercice", key="selarl_exercice_debut")
    exercice_fin = col_k.text_input("Fin exercice", key="selarl_exercice_fin")
    exercice_cloture_premier = col_l.text_input(
        "Cloture premier exercice",
        key="selarl_exercice_cloture_premier",
    )
    col_m, col_n, col_o = st.columns(3)
    lieu_exercice_adresse = col_m.text_input(
        "Lieu exercice",
        key="selarl_lieu_exercice_adresse",
    )
    seuil_achat_materiel = col_n.text_input(
        "Seuil achat materiel",
        key="selarl_seuil_achat_materiel",
    )
    seuil_emprunt = col_o.text_input("Seuil emprunt", key="selarl_seuil_emprunt")
    return {
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
        "signature_nombre_exemplaires": signature_nombre_exemplaires,
        "prestataire_signature_electronique": prestataire_signature_electronique,
        "decision_date": decision_date,
        "reunion_date_lettres": reunion_date_lettres,
        "reunion_heure": reunion_heure,
        "depot_banque_nom": depot_banque_nom,
        "depot_banque_adresse": depot_banque_adresse,
        "exercice_debut": exercice_debut,
        "exercice_fin": exercice_fin,
        "exercice_cloture_premier": exercice_cloture_premier,
        "lieu_exercice_adresse": lieu_exercice_adresse,
        "seuil_achat_materiel": seuil_achat_materiel,
        "seuil_emprunt": seuil_emprunt,
    }


def _render_conjoint(
    *,
    profession: str,
    regime_communautaire: bool,
) -> dict[str, object]:
    st.markdown("**Conjoint**")
    if profession != PROFESSION_DENTISTE and not regime_communautaire:
        st.caption("Non requis pour la generation active.")
    col_a, col_b, col_c, col_d = st.columns(4)
    conjoint_civilite = col_a.text_input("Civilite conjoint", key="selarl_conjoint_civilite")
    conjoint_genre_label = col_b.selectbox(
        "Genre conjoint",
        ("Feminin", "Masculin"),
        key="selarl_conjoint_genre",
    )
    conjoint_prenom = col_c.text_input("Prenom conjoint", key="selarl_conjoint_prenom")
    conjoint_nom = col_d.text_input("Nom conjoint", key="selarl_conjoint_nom")
    col_e, col_f = st.columns(2)
    qualite_renoncee = col_e.text_input(
        "Qualite renoncee",
        value="associe",
        key="selarl_qualite_renoncee",
    )
    date_courrier_avertissement = col_f.date_input(
        "Date courrier avertissement",
        value=date.today(),
        key="selarl_date_courrier_avertissement",
    )
    return {
        "conjoint_civilite": conjoint_civilite,
        "conjoint_genre": (
            Gender.MASCULIN if conjoint_genre_label == "Masculin" else Gender.FEMININ
        ),
        "conjoint_prenom": conjoint_prenom,
        "conjoint_nom": conjoint_nom,
        "qualite_renoncee": qualite_renoncee,
        "date_courrier_avertissement": date_courrier_avertissement
        if regime_communautaire
        else None,
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
