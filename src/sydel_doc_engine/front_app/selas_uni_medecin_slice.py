"""Slice front SELAS UNIPERSONNELLE medecin (DOC-018), patron SELARL uni.

Le generateur `StatutsSelasMedecinGenerator` (DOC-018) existait deja cote moteur
mais restait ORPHELIN : aucun parcours front ne l'exposait (audit retours Albane
lot 2, §17.1). Ce slice rebranche le cas comme un type NOMME dans la deroulante,
sur le modele des autres parcours SEL unipersonnels.

Strategie (faible risque, fidelite garantie) : on ne reconstruit PAS un contexte
SEL d'exercice a la main. On reutilise integralement le constructeur de contexte
SELARL unipersonnel (`selarl_slice.build_generation_context`), deja valide, qui
produit un contexte SEL d'exercice complet (associe unique, ordre, depot, exercice
social, capital en lettres, tronc commun...), PUIS on le transforme en SELAS
medecin : structure SELAS, forme sociale par actions, overlay `selas_medecin`,
titres = « actions », dirigeant President. Aucune regle metier inventee : le
wording des statuts vient du modele source `Statuts_SELAS_medecin.docx`, le reste
du contexte est strictement celui du parcours SELARL uni deja en production.

Bundle de creation = statuts SELAS medecin (DOC-018) + tronc commun (DNC /
domiciliation / procuration / demande ordre) + PV nomination du dirigeant, comme
les autres parcours de creation SEL.

Conditionnel canon SELAS « Si regime communautaire » : un toggle ajoute au bundle
la lettre de renonciation (DOC-005) + la lettre d'avertissement au conjoint
(DOC-006), exactement comme la SELARL le cable. Les deux generateurs existent et
sont enregistres pour la structure SELAS ; le contexte regime est produit par le
constructeur SELARL reutilise des que le toggle est actif.
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
from sydel_doc_engine.domain.models import DocumentGenerationContext, SpfplConjoint
from sydel_doc_engine.front_app import common_creation as cc
from sydel_doc_engine.front_app import selarl_slice
from sydel_doc_engine.front_app.associe_repeater import render_nationalite_selectbox
from sydel_doc_engine.front_app.field_derivations import (
    DEFAULT_TITRE_AFFICHAGE,
    calculate_nominal_value,
    derive_gender_from_civilite,
    format_numeric_value,
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
from sydel_doc_engine.front_app.selarl_slice import (
    PROFESSION_MEDECIN,
    SelarlSliceInput,
)

PREFIX = "selas_uni_medecin"
STRUCTURE = "SELAS uni medecin"
TYPE_KEY = "selas_uni_medecin_v1"

# Code statuts du cas (DOC-018) : statuts SELAS medecin from-scratch.
SELAS_UNI_MEDECIN_STATUTS_CODE = "DOC-018"

# Bundle de creation systematique (canon SELAS « docs a generer dans tous les
# cas ») = statuts DOC-018 + tronc commun (DNC / domiciliation / procuration) +
# PV nomination du dirigeant + demande d'inscription a l'ordre. Aligne sur les
# autres parcours de creation SEL (selas multi, SELARL).
SELAS_UNI_MEDECIN_BASE_CODES: tuple[str, ...] = (
    SELAS_UNI_MEDECIN_STATUTS_CODE,
    *cc.TRONC_COMMUN_CODES,
    cc.DOC_PV_NOMINATION_GERANT,
    cc.DOC_DEMANDE_INSCRIPTION_ORDRE,
)

# Bundle nominal (regime non communautaire) conserve sous l'ancien nom pour
# compatibilite : c'est le bundle de base sans conditionnel.
SELAS_UNI_MEDECIN_BUNDLE_CODES: tuple[str, ...] = SELAS_UNI_MEDECIN_BASE_CODES


def selected_document_codes(payload: dict[str, object]) -> tuple[str, ...]:
    """Codes du bundle SELAS uni medecin selon les conditionnels du canon.

    Base systematique + conditionnel « Si regime communautaire » (canon SELAS) :
    lettre de renonciation (DOC-005) + lettre d'avertissement (DOC-006), comme la
    SELARL le cable. Les deux generateurs existent et sont enregistres pour la
    structure SELAS (catalog `REGIME_COMMUNAUTAIRE_STRUCTURES`) ; le contexte
    regime est produit par le constructeur SELARL reutilise des que le toggle est
    actif. Aucun document existant n'est retire (additif)."""
    codes = list(SELAS_UNI_MEDECIN_BASE_CODES)
    if _is_regime_communautaire(payload):
        codes.extend(cc.REGIME_COMMUNAUTAIRE_CODES)
    return tuple(codes)


def _is_regime_communautaire(payload: dict[str, object]) -> bool:
    return bool(payload.get("regime_communautaire"))

# Wording SELAS (forme par actions) substitue a la forme SELARL portee par le
# constructeur de contexte reutilise. Verbatim du modele source SELAS medecin.
_SELAS_FORME_SOCIALE = "SELAS"
_SELAS_FORME_COMPLETE = "société d'exercice libéral par actions simplifiée"
_SELAS_FORME_LIBELLE_LONG = "Société d'exercice libéral par actions simplifiée"
# Duree du mandat du dirigeant SELAS uni : non bornee (President nomme pour une
# duree illimitee), comme la fixture de reference DOC-018.
_DUREE_MANDAT_PRESIDENT = "illimitée"


@dataclass(frozen=True)
class SelasUniMedecinPlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str = "front_app.selas_uni_medecin_slice"


def render_selas_uni_medecin_form() -> dict[str, object]:
    st.subheader("Donnees a saisir")
    # Parite gold (couche partagee) : exercice (1er janvier / 31 décembre) + cloture
    # « 31 décembre N+1 » pre-remplis, modifiables.
    seed_exercice_dates(PREFIX)
    seed_closing_date(PREFIX, field="exercice_cloture")
    # Parite gold (RAF-003a) : recopie siege <- adresse perso si la case est cochee.
    seed_siege_from_perso(PREFIX)
    st.markdown("**Societe (SELAS unipersonnelle medecin, vocabulaire actions)**")
    col_a, col_b = st.columns(2)
    denomination = _t(col_a, "denomination", "Denomination")
    # Capital en number_input (parite gold) : interdit « 1000 » brut et le « € ».
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
    col_c, col_d, col_e = st.columns(3)
    nb_actions = _i(col_c, "nb_actions_total", "Nombre total d'actions")
    valeur_action = calculate_nominal_value(capital, nb_actions)
    col_d.text_input(
        "Valeur nominale d'une action (calculee)",
        value=valeur_action,
        disabled=True,
    )
    duree = _t(col_e, "duree", "Duree de la societe (ex: 99 ans)") or "99 ans"
    col_f, col_g = st.columns(2)
    ville_rcs = _t(col_f, "ville_rcs", "RCS (ville)")
    lieu_exercice = _t(col_g, "lieu_exercice_adresse", "Adresse du lieu d'exercice")

    st.caption("Siege social (adresse structuree)")
    siege_same_as_perso_checkbox(PREFIX)
    col_sa, col_sb, col_sc, col_sd = st.columns(4)
    siege_num = _t(col_sa, "siege_num", "No")
    siege_voie = _t(col_sb, "siege_voie", "Voie")
    siege_cp = _t(col_sc, "siege_cp", "CP")
    siege_ville = _t(col_sd, "siege_ville", "Ville")
    # Parite gold : lieu de signature pre-rempli = ville du siege (anti double-saisie).
    seed_signature_lieu(PREFIX, siege_ville)

    st.markdown("Depot des fonds")
    col_h, col_i = st.columns(2)
    banque_nom = _t(col_h, "banque_nom", "Banque", hint="ex : CIC CHAPEAU ROUGE BORDEAUX")
    banque_adresse = _t(
        col_i,
        "banque_adresse",
        "Adresse banque (facultatif)",
        hint="ex : 5 place Bellecour, 69002 Lyon",
    )

    st.markdown("Exercice social")
    col_j, col_k, col_l = st.columns(3)
    exercice_debut = _t(col_j, "exercice_debut", "Debut (ex: 1er janvier)")
    exercice_fin = _t(col_k, "exercice_fin", "Fin (ex: 31 décembre)")
    exercice_cloture = _t(col_l, "exercice_cloture", "Cloture du 1er exercice")

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
    date_naissance = _date(col_p, "date_naissance", "Date de naissance")
    ville_naissance = _t(col_q, "ville_naissance", "Ville de naissance")
    departement_naissance = _t(col_r, "departement_naissance", "Departement naissance")
    col_s, col_t = st.columns(2)
    nationalite = render_nationalite_selectbox(PREFIX, container=col_s)
    titre_affichage = _t(col_t, "titre_affichage", "Titre (ex: Docteur)") or DEFAULT_TITRE_AFFICHAGE

    st.caption("Adresse personnelle (structuree)")
    col_u, col_v, col_w, col_x = st.columns(4)
    adresse_num = _t(col_u, "adresse_num", "No")
    adresse_voie = _t(col_v, "adresse_voie", "Voie")
    adresse_cp = _t(col_w, "adresse_cp", "CP")
    adresse_ville = _t(col_x, "adresse_ville", "Ville")

    st.caption("Situation matrimoniale (clause des statuts)")
    col_sm, col_rm = st.columns(2)
    situation_maritale = _t(
        col_sm, "situation_maritale", "Situation matrimoniale (ex: celibataire)"
    )
    regime_matrimonial = _t(
        col_rm, "regime_matrimonial", "Regime matrimonial (ex: separation de biens)"
    )
    # Conditionnel canon SELAS « Si regime communautaire » : ajoute la lettre de
    # renonciation (DOC-005) + la lettre d'avertissement (DOC-006) au bundle. Le
    # constructeur SELARL reutilise produit alors le contexte regime ; le conjoint
    # et le regime matrimonial deviennent requis (valide cote SELARL).
    regime_communautaire = _toggle(
        st,
        "regime_communautaire",
        "Regime communautaire (genere renonciation + avertissement conjoint)",
    )
    conjoint_civilite, conjoint_prenom, conjoint_nom = _render_conjoint()

    st.caption("Filiation + ordre professionnel (declaration / demande inscription)")
    col_y, col_z = st.columns(2)
    nom_pere = _t(col_y, "nom_pere", "Nom du pere")
    nom_mere = _t(col_z, "nom_mere", "Nom de la mere")
    col_aa, col_ab, col_ac = st.columns(3)
    ordre_conseil = _t(col_aa, "ordre_conseil", "Conseil departemental (ordre)")
    departement_ordre = _t(col_ab, "departement_ordre", "Departement ordre")
    numero_ordre = _t(col_ac, "numero_ordre", "Numero d'inscription")
    col_ad, col_ae, col_af = st.columns(3)
    numero_rpps = _t(col_ad, "numero_rpps", "Numero RPPS")
    ordre_ville = _t(col_ae, "ordre_ville", "Ville ordre")
    ordre_cp = _t(col_af, "ordre_cp", "CP ordre")
    ordre_adresse = _t(st, "ordre_adresse_ligne_1", "Adresse ordre")
    # Parite gold (Albane 2026-06-10) : « Madame la Presidente » si la presidente de
    # l'ordre est une femme (demande d'inscription a l'ordre, DOC-034).
    fem_key = f"{PREFIX}_ordre_president_feminin"
    if fem_key not in st.session_state:
        st.session_state[fem_key] = False
    ordre_president_feminin = st.checkbox(
        "La présidente de l'ordre est une femme",
        key=fem_key,
        help="Coché : « Madame la Présidente » au lieu de « Monsieur le Président ».",
    )
    # Parite gold (couche partagee) : conseiller/mandataire SYDEL editable.
    mandataire_prenom, mandataire_nom = mandataire_inputs(PREFIX)

    st.markdown("**Signature / decision**")
    col_ag, col_ah = st.columns(2)
    signature_lieu = _t(col_ag, "signature_lieu", "Lieu de signature")
    signature_date = _date(col_ah, "signature_date", "Date de signature")
    decision_date = _date(st, "decision_date", "Date de decision (PV nomination)")

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
        "ordre_conseil": ordre_conseil,
        "departement_ordre": departement_ordre,
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
        "decision_date": decision_date,
    }


def _render_conjoint() -> tuple[str, str, str]:
    """Saisie du conjoint (clause matrimoniale des statuts SELAS medecin).

    Le modele source DOC-018 porte les tokens conjoint (civilite / prenom / nom)
    de maniere INCONDITIONNELLE — `add_conjoint_replacements` les exige meme pour
    un associe non marie. On collecte donc toujours le conjoint pour ne pas bloquer
    la generation ; le wording de la clause distingue ensuite marie / non marie cote
    moteur. Aucune regle inventee : c'est le contrat du modele SEL d'exercice."""
    st.caption("Conjoint (clause matrimoniale des statuts — requis par le modele)")
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

    Profession = medecin (overlay SELARL medecin), unipersonnel. Le contexte
    produit est ensuite transforme en SELAS medecin par `build_generation_context`.
    """
    civilite = str(payload.get("civilite") or "Monsieur")
    denomination = str(payload.get("denomination") or "")
    conjoint_civilite = str(payload.get("conjoint_civilite") or "")
    return SelarlSliceInput(
        dossier_type_key=TYPE_KEY,
        # Reference dossier requise par la validation SELARL : derivee de la
        # denomination (parcours uni, pas de saisie de reference dediee).
        dossier_reference=denomination or TYPE_KEY,
        profession=PROFESSION_MEDECIN,
        dossier_unipersonnel=True,
        # Conditionnel canon SELAS « Si regime communautaire » : declenche DOC-005
        # / DOC-006 cote bundle ET le contexte regime cote constructeur SELARL
        # reutilise (validation conjoint + regime matrimonial heritee).
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
        ordre_conseil=str(payload.get("ordre_conseil") or ""),
        ordre_adresse_ligne_1=str(payload.get("ordre_adresse_ligne_1") or ""),
        ordre_cp=str(payload.get("ordre_cp") or ""),
        ordre_ville=str(payload.get("ordre_ville") or ""),
        signature_lieu=str(payload.get("signature_lieu") or ""),
        signature_date=payload.get("signature_date"),  # type: ignore[arg-type]
        # Regime communautaire (DOC-005/006) : sans cette date, le generateur de la
        # lettre de renonciation bloque (CODE-RC-001). L'adaptateur la defaulte sur la
        # date de signature, comme TOUS les autres types (SELAS pluri 1469/1627, SPFPL
        # 828, common_creation 303, SELARL natif data_entry 138). Sinon elle reste None.
        date_courrier_avertissement=payload.get("signature_date"),  # type: ignore[arg-type]
        decision_date=payload.get("decision_date"),  # type: ignore[arg-type]
        depot_banque_nom=str(payload.get("banque_nom") or ""),
        depot_banque_adresse=str(payload.get("banque_adresse") or ""),
        exercice_debut=str(payload.get("exercice_debut") or ""),
        exercice_fin=str(payload.get("exercice_fin") or ""),
        exercice_cloture_premier=str(payload.get("exercice_cloture") or ""),
        lieu_exercice_adresse=str(payload.get("lieu_exercice_adresse") or ""),
    )


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    """Contexte SELAS medecin (DOC-018) derive du contexte SELARL uni.

    On reutilise le constructeur SELARL uni (valide), puis on substitue UNIQUEMENT
    ce qui distingue une SELAS medecin d'une SELARL medecin : structure, forme
    sociale par actions, overlay `selas_medecin`, titres = actions, dirigeant
    President (duree de mandat illimitee). Le reste (associe unique, ordre, depot,
    exercice social, capital en lettres, tronc commun) est strictement identique au
    parcours SELARL deja en production -> aucune regle metier reinventee."""
    ctx = selarl_slice.build_generation_context(_to_selarl_input(payload))

    # Le constructeur SELARL n'attache le conjoint a l'associe que pour un associe
    # marie. Le modele SELAS medecin (DOC-018) exige les tokens conjoint de maniere
    # INCONDITIONNELLE (`add_conjoint_replacements`). On garantit donc le conjoint
    # sur l'associe representatif a partir de la saisie (toujours collectee), sans
    # changer le comportement SELARL.
    if ctx.associes and ctx.associes[0].conjoint is None:
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
        ctx.statuts_sel.overlay = "selas_medecin"

    if ctx.capital is not None:
        ctx.capital.type_titre = "actions"

    if ctx.dirigeant_nomine is not None:
        ctx.dirigeant_nomine.fonction_affichage = "président"
        ctx.dirigeant_nomine.duree_mandat = _DUREE_MANDAT_PRESIDENT

    ctx.metadata = {**(ctx.metadata or {}), "front_slice": "track_b_selas_uni_medecin_v1"}
    return ctx


def build_selas_uni_medecin_plan(payload: dict[str, object]) -> SelasUniMedecinPlan:
    # On delegue la validation a la couche SELARL uni (memes champs requis pour le
    # contexte SEL d'exercice), via une entree derivee.
    data = _to_selarl_input(payload)
    blockers = list(selarl_slice.validate_selarl_input(data))
    # Dogfood 2026-06-22 : le modele DOC-018 porte les tokens conjoint de maniere
    # INCONDITIONNELLE (add_conjoint_replacements les exige meme pour un non marie) ;
    # un conjoint vide passait la validation SELARL (conjoint requis seulement si marie)
    # puis crashait a la generation. On valide donc toujours la presence du conjoint.
    for field, name in (
        ("conjoint_civilite", "civilite du conjoint"),
        ("conjoint_prenom", "prenom du conjoint"),
        ("conjoint_nom", "nom du conjoint"),
    ):
        if not str(payload.get(field) or "").strip():
            blockers.append(f"SELAS medecin : {name} requis (le modele DOC-018 l'exige).")
    document_codes = selected_document_codes(payload)
    warnings_list = [
        "SELAS unipersonnelle medecin V1 : associe unique, vocabulaire actions. "
        "Bundle de creation : statuts DOC-018 + tronc commun + PV nomination.",
    ]
    if _is_regime_communautaire(payload):
        warnings_list.append(
            "Regime communautaire actif : DOC-005 (renonciation) et DOC-006 "
            "(avertissement conjoint) seront generes."
        )
    warnings = tuple(warnings_list)
    if blockers:
        return SelasUniMedecinPlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=document_codes,
            blockers=tuple(blockers),
            warnings=warnings,
        )
    return SelasUniMedecinPlan(
        can_generate=True,
        status="ready",
        reason="Pret pour generation SELAS unipersonnelle medecin V1 (bundle de creation).",
        document_codes=document_codes,
        blockers=(),
        warnings=warnings,
    )


def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_selas_uni_medecin_plan(payload)
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


def _t(container, field: str, label: str, hint: str | None = None) -> str:
    key = f"{PREFIX}_{field}"
    if key not in st.session_state:
        st.session_state[key] = ""
    return str(container.text_input(label, key=key, help=hint)).strip()


def _i(container, field: str, label: str) -> int:
    key = f"{PREFIX}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date(container, field: str, label: str) -> date | None:
    # Consomme la couche de rendu partagee (front_widgets) : ajoute le bouton
    # « Aujourd'hui » qui manquait ici, et unifie le rendu (cause racine des ecarts).
    return date_input_with_today(
        label, key=f"{PREFIX}_{field}", value=date.today(), container=container
    )


def _toggle(container, field: str, label: str) -> bool:
    key = f"{PREFIX}_{field}"
    if key not in st.session_state:
        st.session_state[key] = False
    return bool(container.checkbox(label, key=key))
