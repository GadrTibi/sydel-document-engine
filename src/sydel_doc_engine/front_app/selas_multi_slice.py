"""Slice front SELAS multi-associes (DOC-044), patron SELARL.

SELAS multi = SEL d'exercice par actions, 2 a 5 associes exercants/non exercants
(personne physique + personne morale), vocabulaire ACTIONS. Contexte moteur
mirroir du builder de test `test_lot_04_statuts_selas_multi`. Reutilise le
repeater generique en mode "exercice" (actions + qualite capital + ordre).
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
    Company,
    DocumentGenerationContext,
    Person,
    Signature,
    StatutsCivilsAssocie,
    StatutsSelasMultiContext,
    StatutsSelasMultiPresident,
)
from sydel_doc_engine.front_app.field_derivations import (
    derive_gender_from_civilite,
    format_french_date,
    number_words_from_value,
    parse_french_date,
)

STRUCTURE = "SELAS"
DOC_CODE = "DOC-044"
PREFIX = "selas"


@dataclass(frozen=True)
class SelasSlicePlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str = "front_app.selas_multi_slice"


def _count_key() -> str:
    return f"{PREFIX}_nb_associes"


def _associe_count() -> int:
    raw = st.session_state.get(_count_key(), 2)
    try:
        return max(2, min(5, int(raw)))
    except (TypeError, ValueError):
        return 2


def render_selas_form() -> dict[str, object]:
    st.subheader("Donnees a saisir")
    st.markdown("**Societe (SELAS d'exercice, vocabulaire actions)**")
    col_a, col_b = st.columns(2)
    denomination = _t(col_a, "denomination", "Denomination")
    siege = _t(col_b, "siege", "Siege (adresse affichee)")
    col_c, col_d = st.columns(2)
    profession = _t(col_c, "profession_reglementee", "Profession (ex: medecin)")
    profession_pluriel = _t(col_d, "profession_reglementee_pluriel", "Profession (pluriel)")
    col_e, col_f, col_g = st.columns(3)
    capital = _t(col_e, "capital_social", "Capital social")
    nb_actions = _i(col_f, "nb_actions_total", "Nombre total d'actions")
    valeur_action = _t(col_g, "valeur_nominale_action", "Valeur nominale d'une action")
    col_h, col_i = st.columns(2)
    ville_rcs = _t(col_h, "ville_rcs", "RCS (ville)")
    adresse_exercice = _t(col_i, "adresse_lieu_exercice", "Adresse lieu d'exercice")

    st.markdown("Depot des fonds")
    col_j, col_k = st.columns(2)
    banque_nom = _t(col_j, "banque_nom", "Banque")
    banque_adresse = _t(col_k, "banque_adresse", "Adresse banque")
    date_cloture = _t(st, "date_cloture", "Cloture du premier exercice")

    st.markdown("**Signature**")
    col_l, col_m = st.columns(2)
    signature_lieu = _t(col_l, "signature_lieu", "Lieu de signature")
    with col_m:
        signature_date = _date("signature_date", "Date de signature")

    associes = _render_selas_associes()

    return {
        "denomination": denomination,
        "siege": siege,
        "profession_reglementee": profession,
        "profession_reglementee_pluriel": profession_pluriel,
        "capital_social": capital,
        "nb_actions_total": nb_actions,
        "valeur_nominale_action": valeur_action,
        "ville_rcs": ville_rcs,
        "adresse_lieu_exercice": adresse_exercice,
        "banque_nom": banque_nom,
        "banque_adresse": banque_adresse,
        "date_cloture": date_cloture,
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
        "associes": associes,
    }


def _render_selas_associes() -> list[StatutsCivilsAssocie]:
    if _count_key() not in st.session_state:
        st.session_state[_count_key()] = 2
    nombre = _associe_count()
    st.markdown(f"**Associes ({nombre})** — 2 a 5, exercants / non exercants")
    cols = st.columns([1, 1, 3])
    if cols[0].button("Ajouter un associe", key=f"{PREFIX}_add"):
        st.session_state[_count_key()] = min(5, nombre + 1)
        st.rerun()
    if cols[1].button("Retirer un associe", key=f"{PREFIX}_remove"):
        st.session_state[_count_key()] = max(2, nombre - 1)
        st.rerun()
    cols[2].caption("Le premier associe physique est designe president par defaut.")

    associes: list[StatutsCivilsAssocie] = []
    for index in range(nombre):
        associes.append(_render_one_associe(index))
    return associes


def _render_one_associe(index: int) -> StatutsCivilsAssocie:
    prefix = f"{PREFIX}_associe_{index}"
    with st.expander(f"Associe {index + 1}", expanded=index == 0):
        type_key = f"{prefix}_type"
        if type_key not in st.session_state:
            st.session_state[type_key] = "personne_physique"
        type_personne = st.selectbox(
            "Type d'associe",
            ("personne_physique", "personne_morale"),
            key=type_key,
        )
        col_a, col_b = st.columns(2)
        nb_actions = _is(col_a, f"{prefix}_nb_actions", "Nombre d'actions")
        montant = _ts(col_b, f"{prefix}_montant", "Apport (montant)")
        if type_personne == "personne_morale":
            return _morale(prefix, nb_actions, montant)
        return _physique(prefix, nb_actions, montant)


def _physique(prefix: str, nb_actions: int, montant: str) -> StatutsCivilsAssocie:
    col_a, col_b, col_c = st.columns(3)
    civilite = col_a.selectbox(
        "Civilite",
        ("Madame", "Monsieur"),
        key=f"{prefix}_civilite",
    )
    prenoms = _ts(col_b, f"{prefix}_prenoms", "Prenom(s)")
    nom = _ts(col_c, f"{prefix}_nom", "Nom")
    col_d, col_e, col_f = st.columns(3)
    date_naissance = _ts(col_d, f"{prefix}_date_naissance", "Date naissance (ex: 1 janvier 1980)")
    ville_naissance = _ts(col_e, f"{prefix}_ville_naissance", "Ville naissance")
    departement = _ts(col_f, f"{prefix}_departement", "Departement naissance")
    col_g, col_h = st.columns(2)
    nationalite = _ts(col_g, f"{prefix}_nationalite", "Nationalite")
    profession = _ts(col_h, f"{prefix}_profession", "Profession (ex: Docteur)")
    adresse = _ts(st, f"{prefix}_adresse", "Adresse personnelle (affichee)")
    col_i, col_j = st.columns(2)
    situation = _ts(col_i, f"{prefix}_situation", "Situation matrimoniale")
    qualification = _ts(col_j, f"{prefix}_qualification", "Qualification principale")
    col_k, col_l, col_m = st.columns(3)
    ordre_dep = _ts(col_k, f"{prefix}_ordre_dep", "Departement ordre")
    numero_ordre = _ts(col_l, f"{prefix}_numero_ordre", "Numero ordre")
    numero_rpps = _ts(col_m, f"{prefix}_numero_rpps", "Numero RPPS")
    qualite = _ts(st, f"{prefix}_qualite", "Qualite au capital (ex: associee exercante)")

    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=derive_gender_from_civilite(civilite),
        civilite_affichage=civilite,
        prenom=prenoms,
        prenoms=prenoms,
        nom=nom,
        date_naissance=date_naissance or None,
        ville_naissance=ville_naissance or None,
        departement_naissance=departement or None,
        nationalite=nationalite or None,
        profession=profession or None,
        situation_maritale=situation or None,
        adresse_personnelle_affichee=adresse or None,
        qualification_principale=qualification or None,
        ordre_departemental=ordre_dep or None,
        numero_ordre=numero_ordre or None,
        numero_rpps=numero_rpps or None,
        qualite_capital=qualite or None,
        nb_actions=nb_actions or None,
        nb_actions_lettres=number_words_from_value(nb_actions) if nb_actions else None,
        apport=_apport(montant),
    )


def _morale(prefix: str, nb_actions: int, montant: str) -> StatutsCivilsAssocie:
    from sydel_doc_engine.domain.models import Address, StatutsCivilsRepresentant

    denomination = _ts(st, f"{prefix}_denomination", "Denomination (personne morale)")
    col_a, col_b = st.columns(2)
    forme = _ts(col_a, f"{prefix}_forme", "Forme juridique")
    capital = _ts(col_b, f"{prefix}_capital", "Capital social (affiche)")
    siege = _ts(st, f"{prefix}_siege", "Siege (affiche)")
    col_c, col_d = st.columns(2)
    numero_rcs = _ts(col_c, f"{prefix}_numero_rcs", "Numero RCS")
    ville_rcs = _ts(col_d, f"{prefix}_ville_rcs", "RCS (ville)")
    qualite = _ts(st, f"{prefix}_qualite", "Qualite au capital (ex: associee non exercante)")
    st.markdown("Representant legal")
    col_e, col_f, col_g = st.columns(3)
    rep_civilite = col_e.selectbox(
        "Civilite rep.",
        ("Monsieur", "Madame"),
        key=f"{prefix}_rep_civilite",
    )
    rep_prenom = _ts(col_f, f"{prefix}_rep_prenom", "Prenom rep.")
    rep_nom = _ts(col_g, f"{prefix}_rep_nom", "Nom rep.")

    return StatutsCivilsAssocie(
        type_personne="personne_morale",
        denomination=denomination or None,
        forme_juridique=forme or None,
        capital_social=capital or None,
        siege=Address(adresse_affichee=siege) if siege else None,
        numero_rcs=numero_rcs or None,
        ville_rcs=ville_rcs or None,
        representant=StatutsCivilsRepresentant(
            civilite_affichage=rep_civilite,
            prenom=rep_prenom or None,
            nom=rep_nom or None,
            fonction="gerant",
        ),
        qualite_capital=qualite or None,
        nb_actions=nb_actions or None,
        nb_actions_lettres=number_words_from_value(nb_actions) if nb_actions else None,
        apport=_apport(montant),
    )


def _apport(montant: str):
    from sydel_doc_engine.domain.models import StatutsCivilsApport

    return StatutsCivilsApport(
        montant=montant or None,
        montant_lettres=number_words_from_value(montant) if montant else None,
    )


def build_selas_plan(payload: dict[str, object]) -> SelasSlicePlan:
    blockers = _validate(payload)
    warnings = (
        "SELAS multi V1 : 2 a 5 associes, vocabulaire actions. Le moteur exige la coherence "
        "(somme des actions = total, au moins 2 associes).",
    )
    if blockers:
        return SelasSlicePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=(DOC_CODE,),
            blockers=blockers,
            warnings=warnings,
        )
    return SelasSlicePlan(
        can_generate=True,
        status="ready",
        reason="Pret pour generation SELAS multi V1.",
        document_codes=(DOC_CODE,),
        blockers=(),
        warnings=warnings,
    )


def _validate(payload: dict[str, object]) -> tuple[str, ...]:
    blockers: list[str] = []
    required = (
        ("denomination", "Denomination requise."),
        ("siege", "Siege requis."),
        ("profession_reglementee", "Profession requise."),
        ("profession_reglementee_pluriel", "Profession (pluriel) requise."),
        ("capital_social", "Capital social requis."),
        ("valeur_nominale_action", "Valeur nominale d'une action requise."),
        ("ville_rcs", "RCS (ville) requis."),
        ("adresse_lieu_exercice", "Adresse du lieu d'exercice requise."),
        ("banque_nom", "Banque requise."),
        ("banque_adresse", "Adresse banque requise."),
        ("date_cloture", "Cloture du premier exercice requise."),
        ("signature_lieu", "Lieu de signature requis."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    nb_actions_total = int(payload.get("nb_actions_total") or 0)
    if nb_actions_total < 1:
        blockers.append("Nombre total d'actions requis et superieur a zero.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    associes = payload.get("associes") or []
    if not isinstance(associes, list) or len(associes) < 2:
        blockers.append("SELAS multi requiert au moins 2 associes.")
    else:
        if not any(a.type_personne == "personne_physique" for a in associes):
            blockers.append("Au moins une personne physique (futur president) requise.")
        for idx, associe in enumerate(associes, start=1):
            if not _named(associe):
                blockers.append(f"Identite de l'associe {idx} requise.")
            if not associe.nb_actions:
                blockers.append(f"Nombre d'actions de l'associe {idx} requis.")
            if not str(associe.qualite_capital or "").strip():
                blockers.append(f"Qualite au capital de l'associe {idx} requise.")
            if associe.type_personne == "personne_physique":
                for field, name in (
                    ("date_naissance", "date de naissance"),
                    ("ville_naissance", "ville de naissance"),
                    ("nationalite", "nationalite"),
                    ("adresse_personnelle_affichee", "adresse"),
                    ("qualification_principale", "qualification"),
                    ("ordre_departemental", "departement ordre"),
                    ("numero_ordre", "numero ordre"),
                    ("numero_rpps", "numero RPPS"),
                ):
                    if not str(getattr(associe, field) or "").strip():
                        blockers.append(f"Associe {idx} : {name} requise.")
        if nb_actions_total:
            total = sum((a.nb_actions or 0) for a in associes)
            if total != nb_actions_total:
                blockers.append(
                    f"Somme des actions ({total}) != total declare ({nb_actions_total})."
                )
    return tuple(dict.fromkeys(blockers))


def _named(associe: StatutsCivilsAssocie) -> bool:
    if associe.type_personne == "personne_morale":
        return bool((associe.denomination or "").strip())
    return bool((associe.prenoms or associe.prenom or "").strip()) and bool(
        (associe.nom or "").strip()
    )


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    associes: list[StatutsCivilsAssocie] = list(payload.get("associes") or [])
    president_index = next(
        (i for i, a in enumerate(associes) if a.type_personne == "personne_physique"),
        0,
    )
    signataire_associe = associes[president_index] if associes else None
    signataire = Person(
        genre=(signataire_associe.genre if signataire_associe else None) or Gender.FEMININ,
        civilite=(signataire_associe.civilite_affichage if signataire_associe else "Madame"),
        prenom=(signataire_associe.prenom if signataire_associe else ""),
        nom=(signataire_associe.nom if signataire_associe else ""),
    )
    capital = str(payload.get("capital_social") or "")
    nb_actions_total = int(payload.get("nb_actions_total") or 0)
    valeur_action = str(payload.get("valeur_nominale_action") or "")

    return DocumentGenerationContext(
        structure="SELAS",
        personne_signataire=signataire,
        signature=Signature(
            lieu=str(payload.get("signature_lieu") or ""),
            date=payload.get("signature_date"),
        ),
        societe=Company(
            denomination=str(payload.get("denomination") or ""),
            forme_sociale="SELAS",
            siege=_address(str(payload.get("siege") or "")),
            ville_rcs=str(payload.get("ville_rcs") or ""),
        ),
        statuts_selas_multi=StatutsSelasMultiContext(
            profession_reglementee=str(payload.get("profession_reglementee") or ""),
            profession_reglementee_pluriel=str(
                payload.get("profession_reglementee_pluriel") or ""
            ),
            capital_social=capital,
            capital_social_lettres=number_words_from_value(capital),
            nb_actions_total=nb_actions_total,
            nb_actions_total_lettres=number_words_from_value(nb_actions_total),
            valeur_nominale_action=valeur_action,
            valeur_nominale_action_lettres=number_words_from_value(valeur_action),
            adresse_lieu_exercice=str(payload.get("adresse_lieu_exercice") or ""),
            banque_nom=str(payload.get("banque_nom") or ""),
            banque_adresse=str(payload.get("banque_adresse") or ""),
            date_cloture_premier_exercice=str(payload.get("date_cloture") or ""),
            associes=associes,
            president=StatutsSelasMultiPresident(ref_associe_index=president_index),
        ),
        metadata={"front_slice": "track_b_selas_multi_v1"},
    )


def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_selas_plan(payload)
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


def _address(adresse_affichee: str):
    from sydel_doc_engine.domain.models import Address

    return Address(adresse_affichee=adresse_affichee)


def _t(container, field: str, label: str) -> str:
    return _ts(container, f"{PREFIX}_{field}", label)


def _ts(container, key: str, label: str) -> str:
    if key not in st.session_state:
        st.session_state[key] = ""
    return str(container.text_input(label, key=key)).strip()


def _i(container, field: str, label: str) -> int:
    return _is(container, f"{PREFIX}_{field}", label)


def _is(container, key: str, label: str) -> int:
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date(field: str, label: str) -> date | None:
    key = f"{PREFIX}_{field}"
    current = st.session_state.get(key)
    if isinstance(current, date):
        st.session_state[key] = format_french_date(current)
    elif current is None:
        st.session_state[key] = format_french_date(date.today())
    raw = st.text_input(label, key=key, placeholder="JJ/MM/AAAA")
    return parse_french_date(raw)
