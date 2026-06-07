"""Socle des slices SPFPL (cession DOC-035 / apport DOC-036), patron SELARL.

SPFPL V1 = associe unique (le moteur bloque le multi-associes). Contexte moteur
mirroir du builder de test `test_lot_04_statuts_spfpl`. Le slice collecte les
champs cles, superpose un contexte de defaut valide, route vers le bon
generateur selon l'operation (cession / apport).
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
    Apport,
    ApportTitres,
    CapitalSouscription,
    CessionBanque,
    DepotFonds,
    DocumentGenerationContext,
    DossierOptions,
    ExerciceSocial,
    OperationSpfpl,
    Person,
    ProfessionalEntity,
    Signature,
    SocieteCible,
    SocieteSpfpl,
    SpfplConjoint,
    SpfplOrdre,
    SpfplPerson,
    SpfplRepresentant,
)
from sydel_doc_engine.front_app.field_derivations import (
    derive_gender_from_civilite,
    format_french_date,
    number_words_from_value,
    parse_french_date,
)

OPERATION_BY_STRUCTURE: dict[str, tuple[str, str]] = {
    "SPFPL cession": ("cession", "DOC-035"),
    "SPFPL apport": ("apport", "DOC-036"),
}


@dataclass(frozen=True)
class SpfplSlicePlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str = "front_app.spfpl_slice"


def _prefix(structure: str) -> str:
    return "spfpl_" + OPERATION_BY_STRUCTURE[structure][0]


def render_spfpl_form(structure: str) -> dict[str, object]:
    operation, _doc = OPERATION_BY_STRUCTURE[structure]
    prefix = _prefix(structure)
    is_apport = operation == "apport"
    st.subheader("Donnees a saisir")
    st.markdown(f"**Societe SPFPL ({operation})**")
    col_a, col_b = st.columns(2)
    denomination = _t(col_a, prefix, "denomination", "Denomination SPFPL")
    siege = _t(col_b, prefix, "siege", "Siege (adresse affichee)")
    col_c, col_d = st.columns(2)
    capital = _t(col_c, prefix, "capital_social", "Capital social")
    valeur_action = _t(col_d, prefix, "valeur_nominale_action", "Valeur nominale d'une action")

    st.markdown("**Actionnaire unique (chirurgien-dentiste, marie(e))**")
    col_e, col_f, col_g = st.columns(3)
    civilite = col_e.selectbox(
        "Civilite affichee",
        ("Docteur", "Monsieur", "Madame"),
        key=f"{prefix}_civilite",
    )
    prenom = _t(col_f, prefix, "prenom", "Prenom")
    prenoms = _t(col_g, prefix, "prenoms", "Prenoms complets (etat civil)")
    col_h, col_i = st.columns(2)
    nom = _t(col_h, prefix, "nom", "Nom")
    genre_label = col_i.selectbox(
        "Genre civil",
        ("Monsieur", "Madame"),
        key=f"{prefix}_genre_label",
    )
    col_j, col_k, col_l = st.columns(3)
    date_naissance = _t(col_j, prefix, "date_naissance", "Date de naissance (JJ/MM/AAAA)")
    ville_naissance = _t(col_k, prefix, "ville_naissance", "Ville de naissance")
    departement_naissance = _t(col_l, prefix, "departement_naissance", "Departement naissance")
    col_m, col_n = st.columns(2)
    nationalite = _t(col_m, prefix, "nationalite", "Nationalite")
    regime = _t(col_n, prefix, "regime_matrimonial", "Regime matrimonial")
    adresse = _t(st, prefix, "adresse", "Adresse personnelle (affichee)")

    st.markdown("Conjoint")
    col_o, col_p, col_q = st.columns(3)
    conjoint_civilite = col_o.selectbox(
        "Civilite conjoint",
        ("Madame", "Monsieur"),
        key=f"{prefix}_conjoint_civilite",
    )
    conjoint_prenom = _t(col_p, prefix, "conjoint_prenom", "Prenom conjoint")
    conjoint_nom = _t(col_q, prefix, "conjoint_nom", "Nom conjoint")

    st.markdown("Ordre")
    col_r, col_s, col_t = st.columns(3)
    ordre_departement = _t(col_r, prefix, "ordre_departement", "Departement ordre")
    numero_ordre = _t(col_s, prefix, "numero_ordre", "Numero ordre")
    numero_rpps = _t(col_t, prefix, "numero_rpps", "Numero RPPS")

    st.markdown("**Depot / titres apportes**")
    col_u, col_v = st.columns(2)
    banque_nom = _t(col_u, prefix, "banque_nom", "Banque")
    banque_adresse = _t(col_v, prefix, "banque_adresse", "Adresse banque")
    col_w, col_x, col_y = st.columns(3)
    apport_montant = _t(col_w, prefix, "apport_montant", "Montant de l'apport")
    apport_nb_parts = _i(col_x, prefix, "apport_nb_parts", "Nombre de parts apportees")
    apport_plage = _t(col_y, prefix, "apport_plage", "Plage de parts (ex: 41 a 100)")
    apport_valeur_globale = _t(st, prefix, "apport_valeur_globale", "Valeur globale apportee")

    st.markdown("**Societe cible**")
    col_z, col_aa = st.columns(2)
    cible_denomination = _t(col_z, prefix, "cible_denomination", "Denomination cible")
    cible_siege = _t(col_aa, prefix, "cible_siege", "Siege cible (affiche)")
    col_ab, col_ac = st.columns(2)
    cible_ville_rcs = _t(col_ab, prefix, "cible_ville_rcs", "RCS cible (ville)")
    cible_numero_rcs = _t(col_ac, prefix, "cible_numero_rcs", "Numero RCS cible")

    st.markdown("**Exercice / signature**")
    col_ad, col_ae, col_af = st.columns(3)
    exercice_debut = _t(col_ad, prefix, "exercice_debut", "Debut exercice")
    exercice_fin = _t(col_ae, prefix, "exercice_fin", "Fin exercice")
    date_cloture = _t(col_af, prefix, "date_cloture", "Cloture premier exercice")
    signature_lieu = _t(st, prefix, "signature_lieu", "Lieu de signature")
    signature_date = _date(prefix, "signature_date", "Date de signature")

    return {
        "structure": structure,
        "operation": operation,
        "is_apport": is_apport,
        "denomination": denomination,
        "siege": siege,
        "capital_social": capital,
        "valeur_nominale_action": valeur_action,
        "civilite": civilite,
        "prenom": prenom,
        "prenoms": prenoms or prenom,
        "nom": nom,
        "genre": derive_gender_from_civilite(genre_label),
        "date_naissance": date_naissance,
        "ville_naissance": ville_naissance,
        "departement_naissance": departement_naissance,
        "nationalite": nationalite,
        "regime_matrimonial": regime,
        "adresse": adresse,
        "conjoint_civilite": conjoint_civilite,
        "conjoint_prenom": conjoint_prenom,
        "conjoint_nom": conjoint_nom,
        "ordre_departement": ordre_departement,
        "numero_ordre": numero_ordre,
        "numero_rpps": numero_rpps,
        "banque_nom": banque_nom,
        "banque_adresse": banque_adresse,
        "apport_montant": apport_montant,
        "apport_nb_parts": apport_nb_parts,
        "apport_plage": apport_plage,
        "apport_valeur_globale": apport_valeur_globale,
        "cible_denomination": cible_denomination,
        "cible_siege": cible_siege,
        "cible_ville_rcs": cible_ville_rcs,
        "cible_numero_rcs": cible_numero_rcs,
        "exercice_debut": exercice_debut,
        "exercice_fin": exercice_fin,
        "date_cloture": date_cloture,
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
    }


def build_spfpl_plan(payload: dict[str, object]) -> SpfplSlicePlan:
    structure = str(payload["structure"])
    _operation, doc_code = OPERATION_BY_STRUCTURE[structure]
    blockers = _validate(payload)
    warnings = (
        f"{structure} V1 = associe unique (multi-associes bloque par le moteur).",
    )
    if blockers:
        return SpfplSlicePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=(doc_code,),
            blockers=blockers,
            warnings=warnings,
        )
    return SpfplSlicePlan(
        can_generate=True,
        status="ready",
        reason=f"Pret pour generation {structure} V1.",
        document_codes=(doc_code,),
        blockers=(),
        warnings=warnings,
    )


def _validate(payload: dict[str, object]) -> tuple[str, ...]:
    blockers: list[str] = []
    required = (
        ("denomination", "Denomination SPFPL requise."),
        ("siege", "Siege SPFPL requis."),
        ("capital_social", "Capital social requis."),
        ("valeur_nominale_action", "Valeur nominale d'une action requise."),
        ("prenom", "Prenom de l'actionnaire requis."),
        ("nom", "Nom de l'actionnaire requis."),
        ("date_naissance", "Date de naissance requise."),
        ("ville_naissance", "Ville de naissance requise."),
        ("departement_naissance", "Departement de naissance requis."),
        ("nationalite", "Nationalite requise."),
        ("regime_matrimonial", "Regime matrimonial requis."),
        ("adresse", "Adresse personnelle requise."),
        ("conjoint_prenom", "Prenom du conjoint requis."),
        ("conjoint_nom", "Nom du conjoint requis."),
        ("ordre_departement", "Departement ordre requis."),
        ("numero_ordre", "Numero ordre requis."),
        ("numero_rpps", "Numero RPPS requis."),
        ("banque_nom", "Banque requise."),
        ("banque_adresse", "Adresse banque requise."),
        ("apport_montant", "Montant de l'apport requis."),
        ("apport_plage", "Plage de parts apportees requise."),
        ("apport_valeur_globale", "Valeur globale apportee requise."),
        ("cible_denomination", "Denomination de la societe cible requise."),
        ("cible_siege", "Siege de la societe cible requis."),
        ("cible_ville_rcs", "RCS (ville) cible requis."),
        ("cible_numero_rcs", "Numero RCS cible requis."),
        ("exercice_debut", "Debut d'exercice requis."),
        ("exercice_fin", "Fin d'exercice requise."),
        ("date_cloture", "Cloture du premier exercice requise."),
        ("signature_lieu", "Lieu de signature requis."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    if int(payload.get("apport_nb_parts") or 0) < 1:
        blockers.append("Nombre de parts apportees requis et superieur a zero.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    return tuple(dict.fromkeys(blockers))


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    structure = str(payload["structure"])
    operation = str(payload["operation"])
    is_apport = bool(payload["is_apport"])
    capital = str(payload.get("capital_social") or "")
    nb_parts = int(payload.get("apport_nb_parts") or 0)
    valeur_action = str(payload.get("valeur_nominale_action") or "")

    founder = SpfplPerson(
        civilite_affichage=str(payload.get("civilite") or "Docteur"),
        prenom=str(payload.get("prenom") or ""),
        prenoms=str(payload.get("prenoms") or payload.get("prenom") or ""),
        nom=str(payload.get("nom") or ""),
        genre=payload.get("genre") or Gender.MASCULIN,
        profession="chirurgien-dentiste",
        profession_reglementee="chirurgiens-dentistes",
        date_naissance=str(payload.get("date_naissance") or ""),
        ville_naissance=str(payload.get("ville_naissance") or ""),
        departement_naissance=str(payload.get("departement_naissance") or ""),
        nationalite=str(payload.get("nationalite") or ""),
        situation_maritale="marie",
        regime_matrimonial=str(payload.get("regime_matrimonial") or ""),
        conjoint=SpfplConjoint(
            civilite_affichage=str(payload.get("conjoint_civilite") or "Madame"),
            prenom=str(payload.get("conjoint_prenom") or ""),
            nom=str(payload.get("conjoint_nom") or ""),
        ),
        adresse_personnelle=Address(adresse_affichee=str(payload.get("adresse") or "")),
        adresse_personnelle_affichee=str(payload.get("adresse") or ""),
        ordre=SpfplOrdre(
            professionnel="Ordre des chirurgiens-dentistes",
            departement=str(payload.get("ordre_departement") or ""),
            ville=str(payload.get("ordre_departement") or ""),
            numero=str(payload.get("numero_ordre") or ""),
            numero_rpps=str(payload.get("numero_rpps") or ""),
        ),
    )
    return DocumentGenerationContext(
        structure=structure,
        dossier_options=DossierOptions(
            apport=is_apport,
            cession=not is_apport,
            associe_unique=True,
        ),
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
        operation_spfpl=OperationSpfpl(type=operation),
        societe_spfpl=SocieteSpfpl(
            denomination=str(payload.get("denomination") or ""),
            forme_sociale="par actions simplifiee",
            capital_social=capital,
            capital_social_lettres=number_words_from_value(capital),
            valeur_nominale_action=valeur_action,
            valeur_nominale_action_lettres=number_words_from_value(valeur_action),
            siege=Address(adresse_affichee=str(payload.get("siege") or "")),
        ),
        actionnaire_unique=founder,
        apport=Apport(
            montant=str(payload.get("apport_montant") or ""),
            montant_lettres=(number_words_from_value(payload.get("apport_montant")) + " euros")
            if number_words_from_value(payload.get("apport_montant"))
            else str(payload.get("apport_montant") or ""),
        ),
        depot_fonds=DepotFonds(
            banque=CessionBanque(
                nom=str(payload.get("banque_nom") or ""),
                adresse_affichee=str(payload.get("banque_adresse") or ""),
            )
        ),
        apport_titres=ApportTitres(
            nb_parts=nb_parts,
            nb_parts_lettres=number_words_from_value(nb_parts),
            plage_parts=str(payload.get("apport_plage") or ""),
            valeur_globale=str(payload.get("apport_valeur_globale") or ""),
            valeur_nominale_action=valeur_action,
            valeur_nominale_action_lettres=number_words_from_value(valeur_action),
        ),
        societe_cible=SocieteCible(
            denomination=str(payload.get("cible_denomination") or ""),
            siege=Address(adresse_affichee=str(payload.get("cible_siege") or "")),
            ville_rcs=str(payload.get("cible_ville_rcs") or ""),
            numero_rcs=str(payload.get("cible_numero_rcs") or ""),
        ),
        capital_souscription=CapitalSouscription(
            nb_actions_total=600,
            valeur_nominale_action=valeur_action,
        ),
        exercice_social=ExerciceSocial(
            debut=str(payload.get("exercice_debut") or ""),
            fin=str(payload.get("exercice_fin") or ""),
            date_cloture_premier_exercice=str(payload.get("date_cloture") or ""),
        ),
        commissaire_aux_apports=ProfessionalEntity(
            denomination="CAA EXPERTISE",
            forme_sociale="SAS",
            capital_social="1 000 euros",
            siege=Address(adresse_affichee="1 rue Scheffer, 75016 Paris"),
            ville_rcs="Paris",
            numero_rcs="948 483 730",
            representant=SpfplRepresentant(
                civilite_affichage="Monsieur",
                prenom="Nabil",
                nom="Saidi",
            ),
        ),
        metadata={"front_slice": f"track_b_spfpl_{operation}_v1"},
    )


def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_spfpl_plan(payload)
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


def _t(container, prefix: str, field: str, label: str) -> str:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = ""
    return str(container.text_input(label, key=key)).strip()


def _i(container, prefix: str, field: str, label: str) -> int:
    key = f"{prefix}_{field}"
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
