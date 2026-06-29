"""Slice front SASU Holding (DOC-048), nouveau type — modele officiel Albane 2026-06-29.

SASU Holding = SAS UNIPERSONNELLE, holding patrimoniale GENERALISTE (objet participations,
PAS de profession reglementee). DISTINCTE de la « SAS / SPFPL medecins » du moteur (DOC-015,
conservee, chemin `sas_slice`). L'acte est unipersonnel : un seul associe = le president,
aucun bloc repetitif. Le slice collecte societe + associe unique + nb actions + banque +
exercice + signature, et emet le contexte dedie `statuts_sasu_holding`.

Bundle de creation = 6 pieces (canon Albane) : statuts (DOC-048) + tronc commun (DNC /
domiciliation / procuration) + PV remuneration president (DOC-049) + liste des souscripteurs
(DOC-050). Les 2 satellites ont leurs PROPRES generateurs GENERALISTES, byte-fideles aux
modeles Albane (`docs/review/albane_sas_2026-06-29/`), DISTINCTS des generateurs SPFPL medecins
DOC-023 / DOC-024 (conserves, verrouilles SPFPL medecins). Genre libre, pas de profession.
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
    rename_dnc_with_signataire,
)
from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Company,
    DocumentGenerationContext,
    Domiciliation,
    DossierOptions,
    ExerciceSocial,
    Person,
    Signature,
    StatutsSasuHoldingContext,
)
from sydel_doc_engine.front_app import common_creation as cc
from sydel_doc_engine.front_app._field_inputs import text_input_prefixed
from sydel_doc_engine.front_app.address_oneline import (
    parse_address_full as _parse_address_full,
)
from sydel_doc_engine.front_app.associe_repeater import render_nationalite_selectbox
from sydel_doc_engine.front_app.field_derivations import (
    accentuate_french_months,
    derive_gender_from_civilite,
    format_numeric_value,
    number_words_from_value,
)
from sydel_doc_engine.front_app.front_widgets import (
    date_input_with_today,
    mandataire_inputs,
    seed_closing_date,
    seed_exercice_dates,
    seed_siege_from_perso,
    seed_signature_lieu,
    siege_same_as_perso_checkbox,
)

STRUCTURE = "SASU_HOLDING"
DOC_CODE = "DOC-048"
PREFIX = "sasu_holding"

# Bundle de creation SASU Holding (canon Albane 2026-06-29) = 6 pieces : statuts (DOC-048) +
# tronc commun (DNC / domiciliation / procuration) + PV remuneration president (DOC-049) +
# liste des souscripteurs (DOC-050). Les 2 satellites ont leurs generateurs GENERALISTES
# dedies (byte-fideles aux modeles Albane), DISTINCTS des DOC-023 / DOC-024 SPFPL medecins.
SASU_HOLDING_DOC_STATUTS = "DOC-048"
SASU_HOLDING_DOC_PV_REMUNERATION = "DOC-049"
SASU_HOLDING_DOC_LISTE_SOUSCRIPTEURS = "DOC-050"
SASU_HOLDING_BUNDLE_CODES: tuple[str, ...] = (
    SASU_HOLDING_DOC_STATUTS,
    *cc.TRONC_COMMUN_CODES,
    SASU_HOLDING_DOC_PV_REMUNERATION,
    SASU_HOLDING_DOC_LISTE_SOUSCRIPTEURS,
)


@dataclass(frozen=True)
class SasuHoldingSlicePlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str = "front_app.sasu_holding_slice"


def render_sasu_holding_form() -> dict[str, object]:
    st.subheader("Donnees a saisir")
    # Parite gold : pre-remplir exercice (1er janvier / 31 décembre) + cloture « 31 décembre
    # N+1 », recopie siege <- adresse perso si la case est cochee. Seede AVANT les widgets.
    seed_exercice_dates(PREFIX)
    seed_closing_date(PREFIX)
    seed_siege_from_perso(PREFIX)

    st.markdown("**Societe (SASU Holding generaliste)**")
    col_a, col_b = st.columns(2)
    denomination = _t(col_a, "denomination", "Denomination")
    forme_sociale = _t(
        col_b,
        "forme_sociale",
        "Forme sociale",
        hint="ex : Société par actions simplifiée unipersonnelle",
    )
    # Siege sur UNE ligne -> display ET composants num/voie/cp/ville (domiciliation,
    # procuration). Case « siege = adresse perso » comme les autres slices.
    siege_same_as_perso_checkbox(PREFIX)
    siege_ligne = _t(st, "siege", "Adresse du siège (N° et voie, CP Ville)")
    _siege_struct = _parse_address_full(siege_ligne)
    siege = _siege_struct.adresse_affichee if _siege_struct else ""
    siege_num = _siege_struct.num_voie if _siege_struct else ""
    siege_voie = _siege_struct.voie if _siege_struct else ""
    siege_cp = _siege_struct.cp if _siege_struct else ""
    siege_ville = _siege_struct.ville if _siege_struct else ""
    # Lieu de signature pre-rempli = ville du siege (anti double-saisie).
    seed_signature_lieu(PREFIX, siege_ville)

    col_c, col_d = st.columns(2)
    cap_key = f"{PREFIX}_capital_social"
    if cap_key not in st.session_state:
        st.session_state[cap_key] = 0
    capital = format_numeric_value(
        col_c.number_input(
            "Capital social (€)",
            min_value=0,
            step=100,
            key=cap_key,
            help="Montant numerique uniquement (ex : 1 000).",
        )
    )
    nb_actions = _i(col_d, "nb_actions", "Nombre d'actions")

    st.markdown("**Associe unique (= president)**")
    col_e, col_f, col_g = st.columns(3)
    civilite = col_e.selectbox(
        "Civilite affichee",
        ("Monsieur", "Madame"),
        key=f"{PREFIX}_civilite",
    )
    prenom = _t(col_f, "prenom", "Prenom")
    nom = _t(col_g, "nom", "Nom")
    col_h, col_i, col_j = st.columns(3)
    # Date de naissance : selecteur calendrier + « Aujourd'hui ». Saisie verbatim aval
    # (re-accentuee). seed=False.
    date_input_with_today(
        "Date de naissance (ex: 2 janvier 1980)",
        key=f"{PREFIX}_date_naissance",
        value=date.today(),
        container=col_h,
        seed=False,
    )
    date_naissance = str(st.session_state.get(f"{PREFIX}_date_naissance") or "").strip()
    ville_naissance = _t(col_i, "ville_naissance", "Ville de naissance")
    nationalite = render_nationalite_selectbox(PREFIX, container=col_j)
    # Adresse personnelle sur UNE ligne -> display ET composants (DNC).
    adresse_ligne = _t(st, "adresse", "Adresse personnelle (N° et voie, CP Ville)")
    _adresse_struct = _parse_address_full(adresse_ligne)
    adresse_perso = _adresse_struct.adresse_affichee if _adresse_struct else ""
    adresse_num = _adresse_struct.num_voie if _adresse_struct else ""
    adresse_voie = _adresse_struct.voie if _adresse_struct else ""
    adresse_cp = _adresse_struct.cp if _adresse_struct else ""
    adresse_ville = _adresse_struct.ville if _adresse_struct else ""
    st.caption("Filiation de l'associé président (déclaration de non-condamnation)")
    col_k, col_l, col_m = st.columns(3)
    nom_pere = _t(col_k, "nom_pere", "Nom du pere")
    nom_mere = _t(col_l, "nom_mere", "Nom de la mere")
    with col_m:
        date_naissance_iso = _date(PREFIX, "date_naissance_iso", "Date naissance (JJ/MM/AAAA)")

    # Conseiller / mandataire SYDEL editable (parite gold).
    mandataire_prenom, mandataire_nom = mandataire_inputs(PREFIX)

    st.markdown("**Depot / exercice / signature**")
    col_n, col_o = st.columns(2)
    banque_nom = _t(col_n, "banque_nom", "Banque depot", hint="ex : HSBC")
    signature_lieu = _t(col_o, "signature_lieu", "Lieu de signature")
    col_p, col_q, col_r = st.columns(3)
    exercice_debut = _t(col_p, "exercice_debut", "Debut exercice")
    exercice_fin = _t(col_q, "exercice_fin", "Fin exercice")
    date_cloture = _t(col_r, "date_cloture", "Cloture premier exercice")
    signature_date = _date(PREFIX, "signature_date", "Date de signature")

    return {
        "denomination": denomination,
        "forme_sociale": forme_sociale,
        "siege": siege,
        "siege_num": siege_num,
        "siege_voie": siege_voie,
        "siege_cp": siege_cp,
        "siege_ville": siege_ville,
        "capital_social": capital,
        "nb_actions": nb_actions,
        "civilite": civilite,
        "prenom": prenom,
        "nom": nom,
        "genre": derive_gender_from_civilite(civilite),
        "date_naissance": date_naissance,
        "date_naissance_iso": date_naissance_iso,
        "ville_naissance": ville_naissance,
        "nationalite": nationalite,
        "adresse": adresse_perso,
        "adresse_num": adresse_num,
        "adresse_voie": adresse_voie,
        "adresse_cp": adresse_cp,
        "adresse_ville": adresse_ville,
        "nom_pere": nom_pere,
        "nom_mere": nom_mere,
        "mandataire_prenom": mandataire_prenom,
        "mandataire_nom": mandataire_nom,
        "banque_nom": banque_nom,
        "signature_lieu": signature_lieu,
        "exercice_debut": exercice_debut,
        "exercice_fin": exercice_fin,
        "date_cloture": date_cloture,
        "signature_date": signature_date,
    }


def build_sasu_holding_plan(payload: dict[str, object]) -> SasuHoldingSlicePlan:
    blockers = _validate(payload)
    warnings = (
        "SASU Holding = SAS unipersonnelle generaliste (associe unique = president). "
        "Bundle (6 pieces) : statuts + tronc commun (DNC / domiciliation / procuration) + "
        "PV remuneration president + liste des souscripteurs (modeles Albane generalistes).",
    )
    if blockers:
        return SasuHoldingSlicePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=SASU_HOLDING_BUNDLE_CODES,
            blockers=blockers,
            warnings=warnings,
        )
    return SasuHoldingSlicePlan(
        can_generate=True,
        status="ready",
        reason="Pret pour generation SASU Holding V1 (bundle de creation).",
        document_codes=SASU_HOLDING_BUNDLE_CODES,
        blockers=(),
        warnings=warnings,
    )


def _validate(payload: dict[str, object]) -> tuple[str, ...]:
    blockers: list[str] = []
    required = (
        ("denomination", "Denomination requise."),
        ("forme_sociale", "Forme sociale requise."),
        ("siege", "Siege requis."),
        ("capital_social", "Capital social requis."),
        ("prenom", "Prenom de l'associe requis."),
        ("nom", "Nom de l'associe requis."),
        ("date_naissance", "Date de naissance requise."),
        ("ville_naissance", "Ville de naissance requise."),
        ("nationalite", "Nationalite requise."),
        ("adresse", "Adresse personnelle requise."),
        ("banque_nom", "Banque de depot requise."),
        ("signature_lieu", "Lieu de signature requis."),
        ("exercice_debut", "Debut d'exercice requis."),
        ("exercice_fin", "Fin d'exercice requise."),
        ("date_cloture", "Cloture du premier exercice requise."),
        ("siege_num", "No de voie du siege requis (domiciliation)."),
        ("siege_voie", "Voie du siege requise (domiciliation)."),
        ("siege_cp", "Code postal du siege requis (domiciliation)."),
        ("siege_ville", "Ville du siege requise (domiciliation)."),
        ("adresse_num", "No de voie personnel requis (declaration)."),
        ("adresse_voie", "Voie personnelle requise (declaration)."),
        ("adresse_cp", "Code postal personnel requis (declaration)."),
        ("adresse_ville", "Ville personnelle requise (declaration)."),
        ("nom_pere", "Nom du pere requis (declaration)."),
        ("nom_mere", "Nom de la mere requis (declaration)."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    if int(payload.get("nb_actions") or 0) < 1:
        blockers.append("Nombre d'actions requis et superieur a zero.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    if payload.get("date_naissance_iso") is None:
        blockers.append("Date de naissance (JJ/MM/AAAA) requise (declaration).")
    return tuple(dict.fromkeys(blockers))


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    capital = str(payload.get("capital_social") or "")
    nb_actions = int(payload.get("nb_actions") or 0)
    genre = payload.get("genre") or Gender.MASCULIN
    forme_sociale = str(payload.get("forme_sociale") or "")
    qualite_associe = "Associé unique et Président"
    fonction_dirigeant = "Président"

    siege_struct = Address(
        num_voie=str(payload.get("siege_num") or ""),
        voie=str(payload.get("siege_voie") or ""),
        cp=str(payload.get("siege_cp") or ""),
        ville=str(payload.get("siege_ville") or ""),
        adresse_affichee=str(payload.get("siege") or "") or _siege_display(payload),
    )
    adresse_perso = Address(
        num_voie=str(payload.get("adresse_num") or ""),
        voie=str(payload.get("adresse_voie") or ""),
        cp=str(payload.get("adresse_cp") or ""),
        ville=str(payload.get("adresse_ville") or ""),
        adresse_affichee=str(payload.get("adresse") or ""),
    )
    # `Person.date_naissance` est typee `date` stricte. On porte la vraie date ISO : le
    # statuts (`_french_date`) la rend « né le 1 janvier 1990 » et la DNC consomme la meme
    # date — une seule source, pas de double saisie. (La saisie verbatim « 1er janvier 1990 »
    # reste affichee au front mais n'est pas reinjectee : le rendu francais est derive de la
    # date ISO, donc identique.)
    associe = Person(
        genre=genre,
        civilite=str(payload.get("civilite") or "Monsieur"),
        prenom=str(payload.get("prenom") or ""),
        nom=str(payload.get("nom") or ""),
        titre_affichage=str(payload.get("civilite") or "Monsieur"),
        adresse_perso=adresse_perso,
        adresse_personnelle_affichee=adresse_perso.adresse_affichee,
        date_naissance=payload.get("date_naissance_iso"),
        ville_naissance=str(payload.get("ville_naissance") or ""),
        nationalite=str(payload.get("nationalite") or ""),
        nom_pere=str(payload.get("nom_pere") or ""),
        nom_mere=str(payload.get("nom_mere") or ""),
        fonction_dirigeant=fonction_dirigeant,
    )
    return DocumentGenerationContext(
        structure="SASU_HOLDING",
        dossier_options=DossierOptions(associe_unique=True),
        personne_signataire=associe,
        signature=Signature(
            lieu=str(payload.get("siege_ville") or payload.get("signature_lieu") or ""),
            date=payload.get("signature_date"),
            nombre_exemplaires="trois",
        ),
        societe=Company(
            # Forme ABREGEE « SAS » pour les satellites (procuration « de la SAS <denom> »,
            # domiciliation) — modele Albane (gate Akainu M1). La forme LONGUE
            # (« Societe par actions simplifiee unipersonnelle ») n'est portee que par les
            # statuts via statuts_sasu_holding.forme_sociale.
            forme_sociale="SAS",
            forme_sociale_affichage="SAS",
            denomination=str(payload.get("denomination") or ""),
            denomination_courte=str(payload.get("denomination") or ""),
            capital=capital,
            capital_social=capital,
            siege=siege_struct,
            ville_rcs=str(payload.get("siege_ville") or ""),
        ),
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee=siege_struct.adresse_affichee,
        ),
        mandataire=cc.default_mandataire(
            prenom=str(payload.get("mandataire_prenom") or ""),
            nom=str(payload.get("mandataire_nom") or ""),
        ),
        exercice_social=ExerciceSocial(
            debut=accentuate_french_months(str(payload.get("exercice_debut") or "")),
            fin=accentuate_french_months(str(payload.get("exercice_fin") or "")),
            date_cloture_premier_exercice=accentuate_french_months(
                str(payload.get("date_cloture") or "")
            ),
        ),
        statuts_sasu_holding=StatutsSasuHoldingContext(
            forme_sociale=forme_sociale,
            capital_social=capital,
            capital_social_lettres=number_words_from_value(capital),
            nb_actions=nb_actions,
            nom_banque=str(payload.get("banque_nom") or ""),
            qualite_associe=qualite_associe,
            fonction_dirigeant=fonction_dirigeant,
        ),
        metadata={"front_slice": "sasu_holding_v1"},
    )


def _siege_display(payload: dict[str, object]) -> str:
    return (
        f"{payload.get('siege_num', '')} {payload.get('siege_voie', '')}, "
        f"{payload.get('siege_cp', '')} {payload.get('siege_ville', '')}"
    ).strip(" ,")


def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_sasu_holding_plan(payload)
    if not plan.can_generate:
        raise ValueError(plan.reason)
    ctx = build_generation_context(payload)
    docx_paths = generate_docx_files_for_document_codes(ctx, output_dir, plan.document_codes)
    docx_paths = rename_dnc_with_signataire(docx_paths, ctx)
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


def _t(container, field: str, label: str, hint: str | None = None) -> str:
    return text_input_prefixed(container, PREFIX, field, label, hint)


def _i(container, field: str, label: str) -> int:
    key = f"{PREFIX}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date(prefix: str, field: str, label: str) -> date | None:
    return date_input_with_today(label, key=f"{prefix}_{field}", value=date.today())


__all__ = [
    "STRUCTURE",
    "DOC_CODE",
    "SASU_HOLDING_BUNDLE_CODES",
    "SasuHoldingSlicePlan",
    "render_sasu_holding_form",
    "build_sasu_holding_plan",
    "build_generation_context",
    "generate_dossier",
]
