"""Slice front SAS / SPFPL medecins (DOC-015), sur patron SELARL.

SAS V1 = SPFPL medecins, actionnaire unique, associe unique, marie(e) (le moteur
verrouille le wording non marie). Contexte moteur mirroir du builder de test
`test_statuts_sas`. Le slice collecte les champs cles et superpose un contexte de
defaut valide pour garantir une generation sans token residuel.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import streamlit as st

from sydel_doc_engine.app.ui_runtime import (
    GeneratedDossier,
    generate_docx_files_for_document_codes,
    generate_zip_file,
)
from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    CapitalSouscripteur,
    CapitalSouscription,
    CessionBanque,
    DepotFonds,
    DocumentGenerationContext,
    DossierOptions,
    ExerciceSocial,
    Person,
    Signature,
    SocieteSpfpl,
    SpfplConjoint,
    SpfplOrdre,
    SpfplPerson,
    StatutsPresident,
    StatutsSas,
)
from sydel_doc_engine.front_app.field_derivations import (
    derive_gender_from_civilite,
    format_french_date,
    number_words_from_value,
    parse_french_date,
)

STRUCTURE = "SAS"
DOC_CODE = "DOC-015"
PREFIX = "sas"


@dataclass(frozen=True)
class SasSlicePlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str = "front_app.sas_slice"


def render_sas_form() -> dict[str, object]:
    st.subheader("Donnees a saisir")
    st.markdown("**Societe (SPFPL medecins, forme SAS)**")
    col_a, col_b = st.columns(2)
    denomination = _t(col_a, "denomination", "Denomination")
    siege = _t(col_b, "siege", "Siege (adresse affichee)")
    col_c, col_d, col_e = st.columns(3)
    capital = _t(col_c, "capital_social", "Capital social")
    nb_actions = _i(col_d, "nb_actions_total", "Nombre total d'actions")
    valeur_action = _t(col_e, "valeur_nominale_action", "Valeur nominale d'une action")

    st.markdown("**Actionnaire unique / president (medecin, marie(e))**")
    col_f, col_g, col_h = st.columns(3)
    civilite = col_f.selectbox(
        "Civilite affichee",
        ("Docteur", "Monsieur", "Madame"),
        key=f"{PREFIX}_civilite",
    )
    prenom = _t(col_g, "prenom", "Prenom")
    nom = _t(col_h, "nom", "Nom")
    col_i, col_j = st.columns(2)
    genre_label = col_i.selectbox(
        "Genre civil",
        ("Monsieur", "Madame"),
        key=f"{PREFIX}_genre_label",
    )
    qualification = _t(col_j, "qualification_principale", "Qualification (ex: Medecin cardiologue)")
    col_k, col_l, col_m = st.columns(3)
    date_naissance = _t(col_k, "date_naissance", "Date de naissance (ex: 2 janvier 1980)")
    ville_naissance = _t(col_l, "ville_naissance", "Ville de naissance")
    departement_naissance = _t(col_m, "departement_naissance", "Departement naissance")
    col_n, col_o = st.columns(2)
    nationalite = _t(col_n, "nationalite", "Nationalite")
    regime = _t(col_o, "regime_matrimonial", "Regime matrimonial (ex: la communaute legale)")
    adresse_perso = _t(st, "adresse", "Adresse personnelle (affichee)")

    st.markdown("Conjoint")
    col_p, col_q, col_r = st.columns(3)
    conjoint_civilite = col_p.selectbox(
        "Civilite conjoint",
        ("Madame", "Monsieur"),
        key=f"{PREFIX}_conjoint_civilite",
    )
    conjoint_prenom = _t(col_q, "conjoint_prenom", "Prenom conjoint")
    conjoint_nom = _t(col_r, "conjoint_nom", "Nom conjoint")

    st.markdown("Ordre")
    col_s, col_t, col_u = st.columns(3)
    ordre_departement = _t(col_s, "ordre_departement", "Departement ordre")
    numero_ordre = _t(col_t, "numero_ordre", "Numero ordre")
    numero_rpps = _t(col_u, "numero_rpps", "Numero RPPS")

    st.markdown("**Depot / exercice / signature**")
    col_v, col_w = st.columns(2)
    banque_nom = _t(col_v, "banque_nom", "Banque depot")
    signature_lieu = _t(col_w, "signature_lieu", "Lieu de signature")
    col_x, col_y, col_z = st.columns(3)
    exercice_debut = _t(col_x, "exercice_debut", "Debut exercice")
    exercice_fin = _t(col_y, "exercice_fin", "Fin exercice")
    date_cloture = _t(col_z, "date_cloture", "Cloture premier exercice")
    signature_date = _date(PREFIX, "signature_date", "Date de signature")

    return {
        "denomination": denomination,
        "siege": siege,
        "capital_social": capital,
        "nb_actions_total": nb_actions,
        "valeur_nominale_action": valeur_action,
        "civilite": civilite,
        "prenom": prenom,
        "nom": nom,
        "genre": derive_gender_from_civilite(genre_label),
        "qualification_principale": qualification,
        "date_naissance": date_naissance,
        "ville_naissance": ville_naissance,
        "departement_naissance": departement_naissance,
        "nationalite": nationalite,
        "regime_matrimonial": regime,
        "adresse": adresse_perso,
        "conjoint_civilite": conjoint_civilite,
        "conjoint_prenom": conjoint_prenom,
        "conjoint_nom": conjoint_nom,
        "ordre_departement": ordre_departement,
        "numero_ordre": numero_ordre,
        "numero_rpps": numero_rpps,
        "banque_nom": banque_nom,
        "signature_lieu": signature_lieu,
        "exercice_debut": exercice_debut,
        "exercice_fin": exercice_fin,
        "date_cloture": date_cloture,
        "signature_date": signature_date,
    }


def build_sas_plan(payload: dict[str, object]) -> SasSlicePlan:
    blockers = _validate(payload)
    warnings = (
        "SAS V1 = SPFPL medecins, actionnaire unique marie(e). Wording feminin / non marie "
        "verrouille par la source (bloque par le moteur).",
    )
    if blockers:
        return SasSlicePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=(DOC_CODE,),
            blockers=blockers,
            warnings=warnings,
        )
    return SasSlicePlan(
        can_generate=True,
        status="ready",
        reason="Pret pour generation SAS / SPFPL medecins V1.",
        document_codes=(DOC_CODE,),
        blockers=(),
        warnings=warnings,
    )


def _validate(payload: dict[str, object]) -> tuple[str, ...]:
    blockers: list[str] = []
    required = (
        ("denomination", "Denomination requise."),
        ("siege", "Siege requis."),
        ("capital_social", "Capital social requis."),
        ("valeur_nominale_action", "Valeur nominale d'une action requise."),
        ("prenom", "Prenom de l'actionnaire requis."),
        ("nom", "Nom de l'actionnaire requis."),
        ("qualification_principale", "Qualification requise."),
        ("date_naissance", "Date de naissance requise."),
        ("ville_naissance", "Ville de naissance requise."),
        ("departement_naissance", "Departement de naissance requis."),
        ("nationalite", "Nationalite requise."),
        ("regime_matrimonial", "Regime matrimonial requis."),
        ("adresse", "Adresse personnelle requise."),
        ("conjoint_prenom", "Prenom du conjoint requis (actionnaire marie(e))."),
        ("conjoint_nom", "Nom du conjoint requis (actionnaire marie(e))."),
        ("ordre_departement", "Departement ordre requis."),
        ("numero_ordre", "Numero ordre requis."),
        ("numero_rpps", "Numero RPPS requis."),
        ("banque_nom", "Banque de depot requise."),
        ("signature_lieu", "Lieu de signature requis."),
        ("exercice_debut", "Debut d'exercice requis."),
        ("exercice_fin", "Fin d'exercice requise."),
        ("date_cloture", "Cloture du premier exercice requise."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    if int(payload.get("nb_actions_total") or 0) < 1:
        blockers.append("Nombre total d'actions requis et superieur a zero.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    return tuple(dict.fromkeys(blockers))


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    nb_actions = int(payload.get("nb_actions_total") or 0)
    capital = str(payload.get("capital_social") or "")
    profession = "medecin"
    actionnaire = SpfplPerson(
        civilite_affichage=str(payload.get("civilite") or "Docteur"),
        prenom=str(payload.get("prenom") or ""),
        nom=str(payload.get("nom") or ""),
        genre=payload.get("genre") or Gender.MASCULIN,
        profession=profession,
        qualification_principale=str(payload.get("qualification_principale") or ""),
        date_naissance=str(payload.get("date_naissance") or ""),
        ville_naissance=str(payload.get("ville_naissance") or ""),
        departement_naissance=str(payload.get("departement_naissance") or ""),
        nationalite=str(payload.get("nationalite") or ""),
        situation_maritale="Marie",
        regime_matrimonial=str(payload.get("regime_matrimonial") or ""),
        conjoint=SpfplConjoint(
            civilite_affichage=str(payload.get("conjoint_civilite") or "Madame"),
            prenom=str(payload.get("conjoint_prenom") or ""),
            nom=str(payload.get("conjoint_nom") or ""),
        ),
        adresse_personnelle_affichee=str(payload.get("adresse") or ""),
        ordre=SpfplOrdre(
            departement=str(payload.get("ordre_departement") or ""),
            numero=str(payload.get("numero_ordre") or ""),
            numero_rpps=str(payload.get("numero_rpps") or ""),
        ),
        nb_actions=nb_actions,
    )
    return DocumentGenerationContext(
        structure="SAS",
        dossier_options=DossierOptions(associe_unique=True),
        personne_signataire=Person(
            genre=payload.get("genre") or Gender.MASCULIN,
            civilite=str(payload.get("civilite") or "Monsieur"),
            prenom=str(payload.get("prenom") or ""),
            nom=str(payload.get("nom") or ""),
        ),
        signature=Signature(
            lieu=str(payload.get("signature_lieu") or ""),
            date=payload.get("signature_date"),
        ),
        statuts_sas=StatutsSas(type="spfpl_medecins", profession=profession),
        societe_spfpl=SocieteSpfpl(
            denomination=str(payload.get("denomination") or ""),
            capital_social=capital,
            capital_social_lettres=number_words_from_value(capital),
            nb_actions_total=nb_actions,
            nb_actions_total_lettres=number_words_from_value(nb_actions),
            valeur_nominale_action=str(payload.get("valeur_nominale_action") or ""),
            valeur_nominale_action_lettres=number_words_from_value(
                payload.get("valeur_nominale_action")
            )
            + " euros"
            if number_words_from_value(payload.get("valeur_nominale_action"))
            else str(payload.get("valeur_nominale_action") or ""),
            profession=profession,
            siege=Address(adresse_affichee=str(payload.get("siege") or "")),
        ),
        actionnaire_unique=actionnaire,
        president=StatutsPresident(
            ref_associe_index=0,
            civilite_affichage=str(payload.get("civilite") or "Docteur"),
            prenom=str(payload.get("prenom") or ""),
            nom=str(payload.get("nom") or ""),
            adresse_personnelle_affichee=str(payload.get("adresse") or ""),
            duree_mandat="illimitee",
        ),
        depot_fonds=DepotFonds(
            banque=CessionBanque(nom=str(payload.get("banque_nom") or "")),
            montant=capital,
        ),
        exercice_social=ExerciceSocial(
            debut=str(payload.get("exercice_debut") or ""),
            fin=str(payload.get("exercice_fin") or ""),
            date_cloture_premier_exercice=str(payload.get("date_cloture") or ""),
        ),
        capital_souscription=CapitalSouscription(
            nb_actions_total=nb_actions,
            valeur_nominale_action=str(payload.get("valeur_nominale_action") or ""),
            apports_numeraire_montant=capital,
            souscripteurs=[
                CapitalSouscripteur(
                    civilite_affichage=str(payload.get("civilite") or "Docteur"),
                    prenom=str(payload.get("prenom") or ""),
                    nom=str(payload.get("nom") or ""),
                    profession=profession,
                    adresse_personnelle_affichee=str(payload.get("adresse") or ""),
                    nb_actions=nb_actions,
                    qualite="actionnaire unique",
                )
            ],
        ),
        metadata={"front_slice": "track_b_sas_spfpl_medecins_v1"},
    )


def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_sas_plan(payload)
    if not plan.can_generate:
        raise ValueError(plan.reason)
    ctx = build_generation_context(payload)
    docx_paths = generate_docx_files_for_document_codes(ctx, output_dir, plan.document_codes)
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


def _t(container, field: str, label: str) -> str:
    key = f"{PREFIX}_{field}"
    if key not in st.session_state:
        st.session_state[key] = ""
    return str(container.text_input(label, key=key)).strip()


def _i(container, field: str, label: str) -> int:
    key = f"{PREFIX}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date(prefix: str, field: str, label: str) -> date | None:
    key = f"{prefix}_{field}"
    current = st.session_state.get(key)
    if isinstance(current, date):
        st.session_state[key] = format_french_date(current)
    elif current is None:
        st.session_state[key] = format_french_date(date.today())
    raw = st.text_input(label, key=key, placeholder="JJ/MM/AAAA")
    return parse_french_date(raw)
