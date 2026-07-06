"""Slice front SELAS UNIPERSONNELLE chirurgien-dentiste (DOC-046), patron SELAS uni medecin.

Retour Rafael #5 : « la SELAS unipersonnelle dentiste = la pluripersonnelle dentiste
mais avec un seul associe ». Ce slice est le CLONE STRUCTUREL du slice SELAS uni medecin
(`selas_uni_medecin_slice`), avec la seule difference de profession (chirurgien-dentiste)
et de generateur de statuts (DOC-046, blocs dentiste).

Strategie (faible risque, fidelite garantie) : on ne reconstruit PAS un contexte SEL
d'exercice a la main. On reutilise integralement le constructeur de contexte SELARL
unipersonnel (`selarl_slice.build_generation_context`) avec `profession=chirurgien_dentiste`
(overlay SELARL dentiste, qualification/profession/ordre dentiste), PUIS on le transforme
en SELAS dentiste : structure SELAS, forme par actions, overlay `selas_dentiste`,
titres = « actions », dirigeant President. Aucune regle metier inventee : le wording des
statuts vient du modele source dentiste pluri uni-fie ; le reste du contexte est
strictement celui du parcours SELARL uni dentiste deja en production.

Bundle de creation = statuts SELAS dentiste (DOC-046) + tronc commun (DNC /
domiciliation / procuration / demande ordre) + PV nomination du dirigeant, comme les
autres parcours de creation SEL. Conditionnel canon SELAS « Si regime communautaire » :
ajoute DOC-005 + DOC-006, exactement comme la SELAS uni medecin le cable.
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
from sydel_doc_engine.domain.models import DocumentGenerationContext, SpfplConjoint
from sydel_doc_engine.front_app import common_creation as cc
from sydel_doc_engine.front_app import selarl_slice
from sydel_doc_engine.front_app._field_inputs import text_input_prefixed
from sydel_doc_engine.front_app.address_oneline import (
    parse_address_full as _parse_address_full,
)
from sydel_doc_engine.front_app.associe_repeater import render_nationalite_selectbox
from sydel_doc_engine.front_app.field_derivations import (
    DEFAULT_TITRE_AFFICHAGE,
    MATRIMONIAL_STATUS_PRESETS,
    accentuate_french_months,
    calculate_nominal_value,
    derive_gender_from_civilite,
    format_numeric_value,
    matrimonial_status_value,
    regime_communautaire_from_status,
    regime_matrimonial_from_status,
    situation_display,
)
from sydel_doc_engine.front_app.front_widgets import (
    date_input_freeform,
    date_input_with_today,
    mandataire_inputs,
    seed_closing_date,
    seed_exercice_dates,
    seed_siege_from_perso,
    seed_signature_lieu,
    siege_same_as_perso_checkbox,
)
from sydel_doc_engine.front_app.selarl_slice import (
    PROFESSION_DENTISTE,
    SelarlSliceInput,
)
from sydel_doc_engine.front_app.selas_uni_attestation import (
    attach_attestation_to_ctx,
    selas_uni_bundle_codes,
)

PREFIX = "selas_uni_dentiste"
STRUCTURE = "SELAS uni dentiste"
TYPE_KEY = "selas_uni_dentiste_v1"

# Code statuts du cas (DOC-046) : statuts SELAS dentiste from-scratch (blocs dentiste).
SELAS_UNI_DENTISTE_STATUTS_CODE = "DOC-046"

# Bundle de creation systematique (canon SELAS « docs a generer dans tous les cas ») =
# statuts DOC-046 + tronc commun (DNC / domiciliation / procuration) + PV nomination du
# dirigeant + demande d'inscription a l'ordre. Aligne sur la SELAS uni medecin.
SELAS_UNI_DENTISTE_BASE_CODES: tuple[str, ...] = (
    SELAS_UNI_DENTISTE_STATUTS_CODE,
    *cc.TRONC_COMMUN_CODES,
    cc.DOC_PV_NOMINATION_GERANT,
    cc.DOC_DEMANDE_INSCRIPTION_ORDRE,
)

SELAS_UNI_DENTISTE_BUNDLE_CODES: tuple[str, ...] = SELAS_UNI_DENTISTE_BASE_CODES


def selected_document_codes(payload: dict[str, object]) -> tuple[str, ...]:
    """Codes du bundle SELAS uni dentiste selon les conditionnels du canon.

    Base systematique + conditionnel « Si regime communautaire » (canon SELAS) :
    lettre de renonciation (DOC-005) + lettre d'avertissement (DOC-006), comme la
    SELAS uni medecin le cable. Aucun document existant n'est retire (additif)."""
    codes = list(SELAS_UNI_DENTISTE_BASE_CODES)
    # ANO-045 : attestation souscripteurs SELAS (DOC-045). Un unipersonnel a un unique
    # associe physique detenant toutes les actions -> toujours attestable. Insere juste
    # apres les statuts, avant le conditionnel regime communautaire.
    codes = list(selas_uni_bundle_codes(tuple(codes), payload))
    if _is_regime_communautaire(payload):
        codes.extend(cc.REGIME_COMMUNAUTAIRE_CODES)
    return tuple(codes)


def _is_regime_communautaire(payload: dict[str, object]) -> bool:
    return bool(payload.get("regime_communautaire"))


# Wording SELAS (forme par actions) substitue a la forme SELARL portee par le
# constructeur de contexte reutilise. Verbatim du modele source SELAS dentiste.
_SELAS_FORME_SOCIALE = "SELAS"
_SELAS_FORME_COMPLETE = "société d'exercice libéral par actions simplifiée"
_SELAS_FORME_LIBELLE_LONG = "Société d'exercice libéral par actions simplifiée"
# Duree du mandat du dirigeant SELAS uni : non bornee (President nomme pour une duree
# illimitee), comme la SELAS uni medecin.
_DUREE_MANDAT_PRESIDENT = "illimitée"


@dataclass(frozen=True)
class SelasUniDentistePlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str = "front_app.selas_uni_dentiste_slice"


def render_selas_uni_dentiste_form() -> dict[str, object]:
    st.subheader("Donnees a saisir")
    seed_exercice_dates(PREFIX)
    seed_closing_date(PREFIX, field="exercice_cloture")
    seed_siege_from_perso(PREFIX)
    st.markdown("**Societe (SELAS unipersonnelle dentiste, vocabulaire actions)**")
    col_a, col_b = st.columns(2)
    denomination = _t(col_a, "denomination", "Denomination")
    cap_key = f"{PREFIX}_capital_social"
    if cap_key not in st.session_state:
        st.session_state[cap_key] = 0
    capital = format_numeric_value(
        col_b.number_input(
            "Capital social (€)",
            min_value=0,
            step=100,
            key=cap_key,
            help="Montant numerique uniquement (ex : 330 000).",
        )
    )
    col_c, col_d = st.columns(2)
    nb_actions = _i(col_c, "nb_actions_total", "Nombre total d'actions")
    valeur_action = calculate_nominal_value(capital, nb_actions)
    col_d.text_input(
        "Valeur nominale d'une action (calculee)",
        value=valeur_action,
        disabled=True,
    )
    # Duree FORCEE a « 99 ans » (champ retire) comme tous les autres types SEL.
    duree = "99 ans"
    col_f, col_g = st.columns(2)
    ville_rcs = _t(col_f, "ville_rcs", "RCS (ville)")
    lieu_exercice = _t(col_g, "lieu_exercice_adresse", "Adresse du lieu d'exercice")

    siege_same_as_perso_checkbox(PREFIX)
    siege_ligne = _t(st, "siege", "Adresse du siège (N° et voie, CP Ville)")
    _siege_struct = _parse_address_full(siege_ligne)
    siege_num = _siege_struct.num_voie if _siege_struct else ""
    siege_voie = _siege_struct.voie if _siege_struct else ""
    siege_cp = _siege_struct.cp if _siege_struct else ""
    siege_ville = _siege_struct.ville if _siege_struct else ""
    seed_signature_lieu(PREFIX, siege_ville)

    st.markdown("Depot des fonds")
    col_h, col_i = st.columns(2)
    banque_nom = _t(col_h, "banque_nom", "Banque", hint="ex : CIC CHAPEAU ROUGE BORDEAUX")
    banque_adresse = _t(
        col_i,
        "banque_adresse",
        "Adresse banque",
        hint="ex : 5 place Bellecour, 69002 Lyon",
    )

    # Retour Rafael 2026-07-01 : exercice/cloture pre-remplis et recurrents -> volet replie.
    with st.expander(
        "Exercice comptable et clôture (pré-rempli — modifier si besoin)", expanded=False
    ):
        col_j, col_k, col_l = st.columns(3)
        exercice_debut = date_input_freeform(
            "Début de l'exercice comptable (ex : 1er janvier)",
            key=f"{PREFIX}_exercice_debut", container=col_j,
        )
        exercice_fin = date_input_freeform(
            "Fin de l'exercice comptable (ex : 31 décembre)",
            key=f"{PREFIX}_exercice_fin", container=col_k,
        )
        exercice_cloture = date_input_freeform(
            "Date de clôture du 1er exercice (ex : 31 décembre 2028)",
            key=f"{PREFIX}_exercice_cloture", container=col_l,
        )

    st.markdown("**Associe unique / President**")
    col_m, col_n, col_o = st.columns(3)
    civilite = col_m.selectbox(
        "Civilite (civile)",
        ("Monsieur", "Madame"),
        key=f"{PREFIX}_civilite",
    )
    prenom = _t(col_n, "prenom", "Prenom(s)")
    nom = _t(col_o, "nom", "Nom")
    col_p, col_q, col_r = st.columns(3)
    date_naissance = _date(col_p, "date_naissance", "Date de naissance", seed=False)
    ville_naissance = _t(col_q, "ville_naissance", "Ville de naissance")
    departement_naissance = _t(col_r, "departement_naissance", "Departement naissance")
    col_s, col_t = st.columns(2)
    nationalite = render_nationalite_selectbox(PREFIX, container=col_s)
    titre_affichage = _t(col_t, "titre_affichage", "Titre (ex: Docteur)") or DEFAULT_TITRE_AFFICHAGE

    adresse_ligne = _t(st, "adresse", "Adresse personnelle (N° et voie, CP Ville)")
    _adresse_struct = _parse_address_full(adresse_ligne)
    adresse_num = _adresse_struct.num_voie if _adresse_struct else ""
    adresse_voie = _adresse_struct.voie if _adresse_struct else ""
    adresse_cp = _adresse_struct.cp if _adresse_struct else ""
    adresse_ville = _adresse_struct.ville if _adresse_struct else ""

    # MEME DEROULE que la SELAS uni medecin : UN SEUL champ « Situation matrimoniale »
    # (menu preset) ; regime matrimonial + regime de la communaute DERIVES du libelle.
    situation_label = st.selectbox(
        "Situation matrimoniale",
        MATRIMONIAL_STATUS_PRESETS,
        key=f"{PREFIX}_situation",
    )
    situation_maritale = situation_display(
        matrimonial_status_value(situation_label),
        derive_gender_from_civilite(civilite),
    )
    regime_communautaire = regime_communautaire_from_status(situation_label)
    regime_matrimonial = regime_matrimonial_from_status(
        situation_label, regime_communautaire
    )
    if regime_communautaire:
        st.caption("Regime de la communaute : DOC-005 et DOC-006 seront generes.")
    # Champs conjoint affiches pour un associe MARIE ET desormais PACSE (Albane 6.3/7.3,
    # RATIFIE 2026-07-06 : « pacsé avec {partenaire} » a la comparution). Autres statuts -> aucun.
    situation_norm = situation_maritale.lower().replace("é", "e")
    is_marie_ou_pacse = "marie" in situation_norm or "pacse" in situation_norm
    if is_marie_ou_pacse:
        conjoint_civilite, conjoint_prenom, conjoint_nom = _render_conjoint()
    else:
        conjoint_civilite = conjoint_prenom = conjoint_nom = ""

    st.caption("Filiation + ordre professionnel (declaration / demande inscription)")
    col_y, col_z = st.columns(2)
    nom_pere = _t(col_y, "nom_pere", "Nom du pere")
    nom_mere = _t(col_z, "nom_mere", "Nom de la mere")
    col_ab, col_ac = st.columns(2)
    departement_ordre = _t(col_ab, "departement_ordre", "Departement ordre")
    numero_ordre = _t(col_ac, "numero_ordre", "Numero d'inscription")
    connecteur_departement = str(
        st.selectbox(
            "Connecteur avant le departement (de / du / des)",
            ("de", "du", "des"),
            key=f"{PREFIX}_ordre_connecteur",
            help="S'affiche dans « Conseil departemental ... <departement> » : "
            "« de Paris » / « du Rhone » / « des Hauts de Seine ».",
        )
    )
    numero_rpps = _t(st, "numero_rpps", "Numero RPPS")
    _ordre_struct = _parse_address_full(
        _t(st, "ordre_adresse", "Adresse de l'ordre (N° et voie, CP Ville)")
    )
    ordre_adresse = (
        f"{_ordre_struct.num_voie} {_ordre_struct.voie}".strip() if _ordre_struct else ""
    )
    ordre_cp = _ordre_struct.cp if _ordre_struct else ""
    ordre_ville = _ordre_struct.ville if _ordre_struct else ""
    fem_key = f"{PREFIX}_ordre_president_feminin"
    if fem_key not in st.session_state:
        st.session_state[fem_key] = False
    ordre_president_feminin = st.checkbox(
        "La présidente de l'ordre est une femme",
        key=fem_key,
        help="Coché : « Madame la Présidente » au lieu de « Monsieur le Président ».",
    )
    mandataire_prenom, mandataire_nom = mandataire_inputs(PREFIX)

    st.markdown("**Signature**")
    col_ag, col_ah = st.columns(2)
    signature_lieu = _t(col_ag, "signature_lieu", "Lieu de signature")
    signature_date = _date(col_ah, "signature_date", "Date de signature")
    # SU4/SCS2 (Albane) : la date du PV de decision = la date de signature dans TOUS les
    # cas ; le champ « Date de decision » dedie etait mort (jamais lu, derive de
    # signature_date plus bas). Supprime (#8 onglet 24 — champ trompeur).

    return {
        "denomination": denomination,
        "capital_social": capital,
        "nb_actions_total": nb_actions,
        "valeur_nominale_action": valeur_action,
        "duree": duree,
        "ville_rcs": ville_rcs,
        "lieu_exercice_adresse": lieu_exercice,
        "siege_num": siege_num,
        "siege_voie": siege_voie,
        "siege_cp": siege_cp,
        "siege_ville": siege_ville,
        "banque_nom": banque_nom,
        "banque_adresse": banque_adresse,
        "exercice_debut": exercice_debut,
        "exercice_fin": exercice_fin,
        "exercice_cloture": exercice_cloture,
        "civilite": civilite,
        "prenom": prenom,
        "nom": nom,
        "date_naissance": date_naissance,
        "ville_naissance": ville_naissance,
        "departement_naissance": departement_naissance,
        "nationalite": nationalite,
        "titre_affichage": titre_affichage,
        "adresse_num": adresse_num,
        "adresse_voie": adresse_voie,
        "adresse_cp": adresse_cp,
        "adresse_ville": adresse_ville,
        "nom_pere": nom_pere,
        "nom_mere": nom_mere,
        "situation_maritale": situation_maritale,
        "regime_matrimonial": regime_matrimonial,
        "regime_communautaire": regime_communautaire,
        "conjoint_civilite": conjoint_civilite,
        "conjoint_prenom": conjoint_prenom,
        "conjoint_nom": conjoint_nom,
        "departement_ordre": departement_ordre,
        "connecteur_departement": connecteur_departement,
        "ordre_president_feminin": ordre_president_feminin,
        "mandataire_prenom": mandataire_prenom,
        "mandataire_nom": mandataire_nom,
        "numero_ordre": numero_ordre,
        "numero_rpps": numero_rpps,
        "ordre_ville": ordre_ville,
        "ordre_cp": ordre_cp,
        "ordre_adresse_ligne_1": ordre_adresse,
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
    }


def _render_conjoint() -> tuple[str, str, str]:
    """Saisie du conjoint (clause matrimoniale des statuts) — associe MARIE uniquement."""
    st.caption("Conjoint (clause matrimoniale des statuts — associe marie)")
    col_a, col_b, col_c = st.columns(3)
    civilite = col_a.selectbox(
        "Civilite conjoint",
        ("Madame", "Monsieur"),
        key=f"{PREFIX}_conjoint_civilite",
    )
    prenom = _t(col_b, "conjoint_prenom", "Prenom conjoint")
    nom = _t(col_c, "conjoint_nom", "Nom conjoint")
    return civilite, prenom, nom


def _to_selarl_input(payload: dict[str, object]) -> SelarlSliceInput:
    """Construit l'entree du constructeur SELARL uni (reutilise tel quel).

    Profession = chirurgien-dentiste (overlay SELARL dentiste), unipersonnel. Le
    contexte produit est ensuite transforme en SELAS dentiste par
    `build_generation_context`.
    """
    civilite = str(payload.get("civilite") or "Monsieur")
    denomination = str(payload.get("denomination") or "")
    conjoint_civilite = str(payload.get("conjoint_civilite") or "")
    return SelarlSliceInput(
        dossier_type_key=TYPE_KEY,
        dossier_reference=denomination or TYPE_KEY,
        profession=PROFESSION_DENTISTE,
        dossier_unipersonnel=True,
        regime_communautaire=bool(payload.get("regime_communautaire")),
        civilite=civilite,
        genre=derive_gender_from_civilite(civilite),
        prenom=str(payload.get("prenom") or ""),
        nom=str(payload.get("nom") or ""),
        titre_affichage=str(payload.get("titre_affichage") or DEFAULT_TITRE_AFFICHAGE),
        date_naissance=payload.get("date_naissance"),  # type: ignore[arg-type]
        ville_naissance=str(payload.get("ville_naissance") or ""),
        departement_naissance=str(payload.get("departement_naissance") or ""),
        nationalite=str(payload.get("nationalite") or ""),
        nom_pere=str(payload.get("nom_pere") or ""),
        nom_mere=str(payload.get("nom_mere") or ""),
        situation_maritale=str(payload.get("situation_maritale") or ""),
        regime_matrimonial=str(payload.get("regime_matrimonial") or ""),
        conjoint_civilite=conjoint_civilite,
        conjoint_genre=(
            derive_gender_from_civilite(conjoint_civilite) if conjoint_civilite else Gender.FEMININ
        ),
        conjoint_prenom=str(payload.get("conjoint_prenom") or ""),
        conjoint_nom=str(payload.get("conjoint_nom") or ""),
        adresse_num_voie=str(payload.get("adresse_num") or ""),
        adresse_voie=str(payload.get("adresse_voie") or ""),
        adresse_cp=str(payload.get("adresse_cp") or ""),
        adresse_ville=str(payload.get("adresse_ville") or ""),
        numero_ordre=str(payload.get("numero_ordre") or ""),
        numero_rpps=str(payload.get("numero_rpps") or ""),
        departement_ordre=str(payload.get("departement_ordre") or ""),
        ordre_president_feminin=bool(payload.get("ordre_president_feminin")),
        mandataire_prenom=str(payload.get("mandataire_prenom") or ""),
        mandataire_nom=str(payload.get("mandataire_nom") or ""),
        denomination=str(payload.get("denomination") or ""),
        capital_social=str(payload.get("capital_social") or ""),
        duree=str(payload.get("duree") or "99 ans"),
        nb_parts_total=int(payload.get("nb_actions_total") or 0),
        siege_num_voie=str(payload.get("siege_num") or ""),
        siege_voie=str(payload.get("siege_voie") or ""),
        siege_cp=str(payload.get("siege_cp") or ""),
        siege_ville=str(payload.get("siege_ville") or ""),
        ville_rcs=str(payload.get("ville_rcs") or ""),
        ordre_adresse_ligne_1=str(payload.get("ordre_adresse_ligne_1") or ""),
        ordre_cp=str(payload.get("ordre_cp") or ""),
        ordre_ville=str(payload.get("ordre_ville") or ""),
        signature_lieu=str(payload.get("signature_lieu") or ""),
        signature_date=payload.get("signature_date"),  # type: ignore[arg-type]
        date_courrier_avertissement=payload.get("signature_date"),  # type: ignore[arg-type]
        decision_date=payload.get("signature_date"),  # type: ignore[arg-type]
        depot_banque_nom=str(payload.get("banque_nom") or ""),
        depot_banque_adresse=str(payload.get("banque_adresse") or ""),
        exercice_debut=accentuate_french_months(str(payload.get("exercice_debut") or "")),
        exercice_fin=accentuate_french_months(str(payload.get("exercice_fin") or "")),
        exercice_cloture_premier=accentuate_french_months(
            str(payload.get("exercice_cloture") or "")
        ),
        lieu_exercice_adresse=str(payload.get("lieu_exercice_adresse") or ""),
    )


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    """Contexte SELAS dentiste (DOC-046) derive du contexte SELARL uni dentiste.

    On reutilise le constructeur SELARL uni (valide) avec la profession dentiste, puis
    on substitue UNIQUEMENT ce qui distingue une SELAS d'une SELARL : structure, forme
    par actions, overlay `selas_dentiste`, titres = actions, dirigeant President (duree
    de mandat illimitee). Le reste (associe unique, ordre dentiste, depot, exercice,
    capital en lettres, clause matrimoniale, tronc commun) est strictement celui du
    parcours SELARL dentiste deja en production -> aucune regle metier reinventee."""
    ctx = selarl_slice.build_generation_context(_to_selarl_input(payload))

    if (
        ctx.associes
        and ctx.associes[0].conjoint is None
        and payload.get("conjoint_civilite")
    ):
        ctx.associes[0].conjoint = SpfplConjoint(
            civilite_affichage=str(payload.get("conjoint_civilite") or ""),
            prenom=str(payload.get("conjoint_prenom") or ""),
            nom=str(payload.get("conjoint_nom") or ""),
        )

    ctx.structure = "SELAS"
    ctx.societe.forme_sociale = _SELAS_FORME_SOCIALE
    ctx.societe.forme_sociale_affichage = _SELAS_FORME_SOCIALE
    ctx.societe.forme_sociale_abregee = _SELAS_FORME_SOCIALE
    ctx.societe.forme_sociale_complete = _SELAS_FORME_COMPLETE
    ctx.societe.forme_sociale_libelle_long = _SELAS_FORME_LIBELLE_LONG

    if ctx.statuts_sel is not None:
        ctx.statuts_sel.overlay = "selas_dentiste"

    if ctx.ordre is not None:
        ctx.ordre.destinataire_sans_mention_ordre = True
        ctx.ordre.connecteur_departement = str(
            payload.get("connecteur_departement") or "de"
        )

    if ctx.capital is not None:
        ctx.capital.type_titre = "actions"

    if ctx.dirigeant_nomine is not None:
        ctx.dirigeant_nomine.fonction_affichage = "président"
        ctx.dirigeant_nomine.duree_mandat = _DUREE_MANDAT_PRESIDENT

    ctx.metadata = {
        **(ctx.metadata or {}),
        "front_slice": "track_b_selas_uni_dentiste_v1",
    }

    # ANO-045 : construit et attache les objets requis par l'attestation souscripteurs
    # (DOC-045) — le constructeur SELARL reutilise ne les produit pas. No-op si non
    # attestable (jamais le cas pour un unipersonnel valide).
    ctx = attach_attestation_to_ctx(ctx, payload)
    return ctx


def build_selas_uni_dentiste_plan(payload: dict[str, object]) -> SelasUniDentistePlan:
    data = _to_selarl_input(payload)
    blockers = list(selarl_slice.validate_selarl_input(data))
    is_marie = "marie" in str(payload.get("situation_maritale") or "").lower().replace("é", "e")
    # La validation SELARL FORCE le conjoint pour la profession dentiste (regle native
    # SELARL : `data.profession == PROFESSION_DENTISTE`). En SELAS uni, le conjoint n'est
    # requis QUE pour un associe MARIE (meme gate que le formulaire + retour Rafael #2,
    # aligne sur la SELAS uni medecin) : la clause matrimoniale des statuts rend juste
    # « celibataire » sans conjoint pour un non-marie. On retire donc, pour un non-marie,
    # les bloqueurs conjoint « ... requis(e) pour les statuts. » herites du chemin SELARL.
    if not is_marie:
        _conjoint_statuts_blockers = {
            "Civilite du conjoint requise pour les statuts.",
            "Prenom du conjoint requis pour les statuts.",
            "Nom du conjoint requis pour les statuts.",
        }
        blockers = [b for b in blockers if b not in _conjoint_statuts_blockers]
    if is_marie:
        for field, name in (
            ("conjoint_civilite", "civilite du conjoint"),
            ("conjoint_prenom", "prenom du conjoint"),
            ("conjoint_nom", "nom du conjoint"),
        ):
            if not str(payload.get(field) or "").strip():
                blockers.append(f"SELAS dentiste : {name} requis pour un associe marie.")
    document_codes = selected_document_codes(payload)
    warnings_list = [
        "SELAS unipersonnelle dentiste V1 : associe unique, vocabulaire actions. "
        "Bundle de creation : statuts DOC-046 + tronc commun + PV nomination.",
    ]
    if _is_regime_communautaire(payload):
        warnings_list.append(
            "Regime communautaire actif : DOC-005 (renonciation) et DOC-006 "
            "(avertissement conjoint) seront generes."
        )
    warnings = tuple(warnings_list)
    if blockers:
        return SelasUniDentistePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=document_codes,
            blockers=tuple(blockers),
            warnings=warnings,
        )
    return SelasUniDentistePlan(
        can_generate=True,
        status="ready",
        reason="Pret pour generation SELAS unipersonnelle dentiste V1 (bundle de creation).",
        document_codes=document_codes,
        blockers=(),
        warnings=warnings,
    )


def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_selas_uni_dentiste_plan(payload)
    if not plan.can_generate:
        raise ValueError(plan.reason)
    ctx = build_generation_context(payload)
    docx_paths = generate_docx_files_for_document_codes(ctx, output_dir, plan.document_codes)
    docx_paths = rename_dnc_with_signataire(docx_paths, ctx)  # DNC nommee par le dirigeant
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


def _t(container, field: str, label: str, hint: str | None = None) -> str:
    # C2 : helper canonique partage (front_app/_field_inputs). Comportement inchange.
    return text_input_prefixed(container, PREFIX, field, label, hint)


def _i(container, field: str, label: str) -> int:
    key = f"{PREFIX}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date(container, field: str, label: str, *, seed: bool = True) -> date | None:
    # seed=False pour une NAISSANCE (pas de pre-remplissage au jour) — m1 Akainu 29/06.
    return date_input_with_today(
        label, key=f"{PREFIX}_{field}", value=date.today(), container=container, seed=seed
    )
