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
    rename_dnc_with_signataire,
)
from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Apport,
    ApportTitres,
    CapitalContext,
    CapitalSouscripteur,
    CapitalSouscription,
    CessionBanque,
    CessionParts,
    Company,
    DecisionContext,
    DepotFonds,
    DirigeantNomine,
    DocumentGenerationContext,
    Domiciliation,
    DossierOptions,
    ExerciceSocial,
    OperationSpfpl,
    OperationTitres,
    OrdreAddress,
    OrdreProfessionnel,
    Person,
    ProfessionalEntity,
    RegimeCommunautaire,
    RegimeCommunautaireAvertissement,
    RegimeCommunautaireRenonciation,
    ReunionContext,
    ReunionPresident,
    Signature,
    SocieteCible,
    SocieteSpfpl,
    SpfplConjoint,
    SpfplDirigeant,
    SpfplOrdre,
    SpfplPerson,
    SpfplRepresentant,
)
from sydel_doc_engine.front_app import common_creation as cc
from sydel_doc_engine.front_app.address_oneline import (
    parse_address_full as _parse_address_full,
)
from sydel_doc_engine.front_app.associe_repeater import render_nationalite_selectbox
from sydel_doc_engine.front_app.field_derivations import (
    MATRIMONIAL_STATUS_PRESETS,
    accentuate_french_months,
    calculate_nominal_value,
    date_to_french_words,
    derive_gender_from_civilite,
    format_grouped_numeric_value,
    format_numeric_value,
    is_capital_divisible,
    matrimonial_status_value,
    number_words_from_value,
    regime_communautaire_from_status,
    regime_matrimonial_from_status,
    situation_display,
)
from sydel_doc_engine.front_app.front_widgets import (
    copyable_text_input,
    date_input_with_today,
    mandataire_inputs,
    seed_closing_date,
    seed_exercice_dates,
    seed_siege_from_perso,
    seed_signature_lieu,
    siege_same_as_perso_checkbox,
)

OPERATION_BY_STRUCTURE: dict[str, tuple[str, str]] = {
    "SPFPL cession": ("cession", "DOC-035"),
    "SPFPL apport": ("apport", "DOC-036"),
}

# Documents d'OPERATION apport (canon « Si apport ») — gates moteur sur
# dossier_options.apport : contrat d'apport (DOC-041) + attestation capital /
# liste des souscripteurs (DOC-042) + attestation du commissaire aux apports
# (DOC-043). Ils s'ajoutent au bundle de creation des que l'operation = apport.
SPFPL_APPORT_OPERATION_CODES: tuple[str, ...] = ("DOC-041", "DOC-042", "DOC-043")

# Documents d'OPERATION cession (canon « Si cession ») : note d'information (DOC-037),
# PV d'agrement (DOC-038 si la cible a UN associe reel / DOC-039 si PLUSIEURS), acte de
# cession de parts (DOC-040). Le PV depend du nombre d'associes REELS de la cible
# (hors holding acquereur, ajoute automatiquement comme personne morale).
SPFPL_CESSION_NOTE_CODE = "DOC-037"
SPFPL_CESSION_ACTE_PARTS_CODE = "DOC-040"
SPFPL_CESSION_PV_UNIQUE_CODE = "DOC-038"
SPFPL_CESSION_PV_PLUSIEURS_CODE = "DOC-039"

# Activite standard d'une SPFPL (societe de participations financieres de
# profession liberale) — boilerplate du type, pas une donnee de dossier.
_SPFPL_ACTIVITE = "participations financières de profession libérale"

# Champs d'une entite professionnelle (commissaire aux apports / evaluateur)
# collectee dans le sous-formulaire apport.
_ENTITY_FIELDS: tuple[str, ...] = (
    "denomination",
    "forme",
    "capital",
    "siege",
    "ville_rcs",
    "numero_rcs",
    "rep_civilite",
    "rep_prenom",
    "rep_nom",
)

# Bundle de creation SPFPL (canon, perimetre CREATION cablable) : statuts du type
# + tronc commun (DNC / domiciliation / procuration) + PV nomination gerant +
# demande d'inscription a l'ordre.
#
# Hors bundle automatique (exigent des donnees d'OPERATION non collectees a la
# creation du holding -> voir manques[]) :
#   - note d'information (DOC-037) : exige `associes_cible` = la repartition du
#     capital de la societe cible AVANT/APRES l'operation (roster d'associes de la
#     societe operationnelle), non saisie a la creation du holding.
#   - cession : PV agrement (DOC-038/039), acte cession parts/actions (DOC-040/029)
#     -> exigent associes_cible, prix en lettres, PV reunion d'agrement.
#   - apport : contrat apport (DOC-041), attestations capital / commissaire
#     (DOC-042/043) -> exigent l'identite du commissaire aux apports / evaluateur
#     et le detail des titres apportes en lettres.


def _creation_bundle_codes(
    statuts_code: str,
    *,
    regime_communautaire: bool = False,
) -> tuple[str, ...]:
    codes = [
        statuts_code,
        *cc.TRONC_COMMUN_CODES,
        cc.DOC_PV_NOMINATION_GERANT,
        cc.DOC_DEMANDE_INSCRIPTION_ORDRE,
    ]
    # Conditionnel canon « Si regime communautaire » (DOC-005 + DOC-006).
    if regime_communautaire:
        codes.extend(cc.REGIME_COMMUNAUTAIRE_CODES)
    return tuple(codes)


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
    # Parite gold (couche partagee) : pre-remplir exercice (1er janvier / 31 décembre)
    # + cloture « 31 décembre N+1 », modifiables.
    seed_exercice_dates(prefix)
    seed_closing_date(prefix)
    # Parite gold (RAF-003a) : recopie siege <- adresse perso si la case est cochee.
    seed_siege_from_perso(prefix)
    st.subheader("Donnees a saisir")
    st.markdown(f"**Societe SPFPL ({operation})**")
    denomination = _t(st, prefix, "denomination", "Denomination SPFPL")
    # §14.1 (retours Albane lot 2) : suppression du champ texte libre « Siege
    # (adresse affichee) » qui doublonnait la grille structuree ci-dessous.
    # L'adresse affichee est desormais DERIVEE de la grille (cf. _siege_display),
    # comme le formulaire SELARL de reference.
    # O24-03 : siege sur UNE ligne (parse interne -> num/voie/cp/ville exiges par la
    # domiciliation [num_voie_siege] et la procuration).
    siege_same_as_perso_checkbox(prefix)
    siege_ligne = _t(st, prefix, "siege", "Adresse du siège (N° et voie, CP Ville)")
    _siege_struct = _parse_address_full(siege_ligne)
    siege_num = _siege_struct.num_voie if _siege_struct else ""
    siege_voie = _siege_struct.voie if _siege_struct else ""
    siege_cp = _siege_struct.cp if _siege_struct else ""
    siege_ville = _siege_struct.ville if _siege_struct else ""
    # Parite gold : lieu de signature pre-rempli = ville du siege (anti double-saisie).
    seed_signature_lieu(prefix, siege_ville)
    col_c, col_d, col_dd = st.columns(3)
    # Capital en number_input (parite gold shell.py:1430) : interdit « 1000 » brut et
    # le « € » superflu. Stocke en chaine formatee pour l'aval.
    cap_key = f"{prefix}_capital_social"
    if cap_key not in st.session_state:
        st.session_state[cap_key] = 0
    capital = format_numeric_value(
        col_c.number_input(
            "Capital social (€)",
            min_value=0,
            step=100,
            key=cap_key,
            help="Montant numerique uniquement (ex : 330 000).",
        )
    )
    # Decision Gad 2026-06-18 : nombre d'actions VARIABLE (defaut 600), aligne sur
    # le patron SAS/SELAS. La valeur nominale n'est plus saisie librement : elle
    # est CALCULEE (capital / nb actions) et affichee en lecture seule.
    nb_actions = _i(col_d, prefix, "nb_actions_total", "Nombre d'actions")
    valeur_action = calculate_nominal_value(capital, nb_actions)
    col_dd.text_input(
        "Valeur nominale d'une action (calculee)",
        value=valeur_action,
        disabled=True,
    )
    ville_rcs = _t(st, prefix, "ville_rcs", "RCS SPFPL (ville)")

    st.markdown("**Actionnaire unique (chirurgien-dentiste, marie(e))**")
    st.caption(
        "Le titre « Docteur » est applique automatiquement (l'associe d'une SPFPL "
        "dentiste est necessairement docteur) ; la civilite ci-dessous est la "
        "civilite CIVILE (M. / Mme)."
    )
    # §14.2 (retours Albane lot 2) : « Docteur » n'est plus une valeur a choisir
    # (il etait melange avec la civilite civile et se propageait en titre dans les
    # satellites). On ne garde QUE la civilite civile M./Mme ; le genre en derive
    # (plus de double selecteur « Genre civil » redondant). Le titre pro « Docteur »
    # est injecte automatiquement cote moteur (build_generation_context).
    col_e, col_f, col_g = st.columns(3)
    civilite = col_e.selectbox(
        "Civilite (civile)",
        ("Monsieur", "Madame"),
        key=f"{prefix}_civilite",
    )
    prenom = _t(col_f, prefix, "prenom", "Prenom")
    prenoms = _t(col_g, prefix, "prenoms", "Prenoms complets (etat civil)")
    nom = _t(st, prefix, "nom", "Nom")
    col_j, col_k, col_l = st.columns(3)
    date_naissance = _t(col_j, prefix, "date_naissance", "Date de naissance (JJ/MM/AAAA)")
    ville_naissance = _t(col_k, prefix, "ville_naissance", "Ville de naissance")
    departement_naissance = _t(col_l, prefix, "departement_naissance", "Departement naissance")
    col_m, col_n = st.columns(2)
    # Parite gold : nationalite en deroulant (NATIONALITY_PRESETS + « Autre »).
    nationalite = render_nationalite_selectbox(prefix, container=col_m)
    # L6 (Gad 2026-06-24) : plus de case « Régime communautaire (...) ». L'actionnaire fondateur
    # SPFPL est marié (conjoint requis par la validation) -> on choisit le RÉGIME dans un MENU
    # (patron menu ratifié SELAS / LIVE-02). Le menu dérive le régime matrimonial ET le
    # déclencheur DOC-005/006 (communauté légale uniquement), via les mêmes helpers que la SELAS.
    _married_regimes = tuple(
        s for s in MATRIMONIAL_STATUS_PRESETS if matrimonial_status_value(s) == "marie"
    )
    regime_label = col_n.selectbox(
        "Regime matrimonial",
        _married_regimes,
        key=f"{prefix}_regime_label",
        help="« communauté légale » → renonciation + avertissement au conjoint.",
    )
    regime_communautaire = regime_communautaire_from_status(regime_label)
    regime = regime_matrimonial_from_status(regime_label, regime_communautaire)
    # O24-03 : adresse personnelle sur UNE ligne (parse interne -> num/voie/cp/ville
    # exiges par la DNC du president).
    st.caption("Adresse personnelle + filiation (déclaration de non-condamnation)")
    adresse_ligne = _t(st, prefix, "adresse", "Adresse personnelle (N° et voie, CP Ville)")
    _adresse_struct = _parse_address_full(adresse_ligne)
    adresse_num = _adresse_struct.num_voie if _adresse_struct else ""
    adresse_voie = _adresse_struct.voie if _adresse_struct else ""
    adresse_cp = _adresse_struct.cp if _adresse_struct else ""
    adresse_ville = _adresse_struct.ville if _adresse_struct else ""
    col_ae, col_af, col_ag = st.columns(3)
    nom_pere = _t(col_ae, prefix, "nom_pere", "Nom du pere")
    nom_mere = _t(col_af, prefix, "nom_mere", "Nom de la mere")
    with col_ag:
        decision_date = _date(prefix, "decision_date", "Date de decision (PV gerant)")

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
    ordre_conseil = _t(st, prefix, "ordre_conseil", "Conseil departemental")
    # O24-03 : adresse de l'ordre sur UNE ligne (parse interne -> ligne_1/cp/ville),
    # comme siege/perso/SELAS. Remplace les 3 champs separes ; alimente les MEMES cles
    # -> generateur DOC-034 et gold byte-identique inchanges.
    _ordre_struct = _parse_address_full(
        _t(st, prefix, "ordre_adresse", "Adresse de l'ordre (N° et voie, CP Ville)")
    )
    ordre_adresse_ligne_1 = (
        f"{_ordre_struct.num_voie} {_ordre_struct.voie}".strip() if _ordre_struct else ""
    )
    ordre_cp = _ordre_struct.cp if _ordre_struct else ""
    ordre_ville = _ordre_struct.ville if _ordre_struct else ""
    # Parite gold (Albane 2026-06-10) : « Madame la Presidente » si la presidente de
    # l'ordre est une femme (demande d'inscription a l'ordre).
    feminin_key = f"{prefix}_ordre_president_feminin"
    if feminin_key not in st.session_state:
        st.session_state[feminin_key] = False
    ordre_president_feminin = st.checkbox(
        "La présidente de l'ordre est une femme",
        key=feminin_key,
        help="Coché : « Madame la Présidente » au lieu de « Monsieur le Président ».",
    )
    # Parite gold (couche partagee) : conseiller/mandataire SYDEL editable.
    mandataire_prenom, mandataire_nom = mandataire_inputs(prefix)

    st.markdown("**Depot / titres apportes**")
    col_u, col_v = st.columns(2)
    banque_nom = _t(
        col_u, prefix, "banque_nom", "Banque", hint="ex : CIC CHAPEAU ROUGE BORDEAUX"
    )
    banque_adresse = _t(
        col_v, prefix, "banque_adresse", "Adresse banque", hint="ex : 5 place Bellecour, 69002 Lyon"
    )
    col_w, col_x, col_y = st.columns(3)
    apport_montant = _t(col_w, prefix, "apport_montant", "Montant de l'apport")
    apport_nb_parts = _i(col_x, prefix, "apport_nb_parts", "Nombre de parts apportees")
    apport_plage = _t(col_y, prefix, "apport_plage", "Plage de parts (ex: 41 a 100)")
    apport_valeur_globale = _t(st, prefix, "apport_valeur_globale", "Valeur globale apportee")

    st.markdown("**Societe cible**")
    col_z, col_aa2 = st.columns(2)
    cible_denomination = _t(col_z, prefix, "cible_denomination", "Denomination cible")
    cible_siege = _t(col_aa2, prefix, "cible_siege", "Siege cible (affiche)")
    col_ab, col_ac = st.columns(2)
    cible_ville_rcs = _t(col_ab, prefix, "cible_ville_rcs", "RCS cible (ville)")
    cible_numero_rcs = _t(col_ac, prefix, "cible_numero_rcs", "Numero RCS cible")
    col_ad2, col_ae2, col_af2 = st.columns(3)
    cible_forme = _t(col_ad2, prefix, "cible_forme", "Forme sociale cible")
    cible_profession = _t(col_ae2, prefix, "cible_profession", "Profession reglementee cible")
    cible_capital = _t(col_af2, prefix, "cible_capital", "Capital social cible")
    col_ag2, col_ah2 = st.columns(2)
    cible_nb_parts = _i(col_ag2, prefix, "cible_nb_parts", "Parts totales cible")
    cible_valeur_part = _t(col_ah2, prefix, "cible_valeur_part", "Valeur nominale part cible")

    # --- Operation apport (DOC-041 contrat + DOC-042/043 attestations) :
    # detail des titres apportes + organes de controle (commissaire aux apports
    # + evaluateur). Rendu UNIQUEMENT pour l'apport ; en cession ces champs
    # restent vides et ne sont pas lus.
    apport_nature_titres = "parts sociales"
    apport_valeur_par_titre = ""
    commissaire_fields = dict.fromkeys(_ENTITY_FIELDS, "")
    evaluateur_fields = dict.fromkeys(_ENTITY_FIELDS, "")
    if is_apport:
        st.markdown("**Apport en nature — detail & organes de controle**")
        col_at1, col_at2 = st.columns(2)
        apport_nature_titres = col_at1.selectbox(
            "Nature des titres apportes",
            ("parts sociales", "actions"),
            key=f"{prefix}_apport_nature_titres",
        )
        apport_valeur_par_titre = _t(
            col_at2, prefix, "apport_valeur_par_titre", "Valeur d'un titre apporte"
        )
        st.caption("Commissaire aux apports")
        commissaire_fields = _render_entity_inputs(prefix, "commissaire")
        st.caption("Evaluateur de l'apport")
        evaluateur_fields = _render_entity_inputs(prefix, "evaluateur")

    # --- Operation cession (DOC-037 note + DOC-038/039 PV agrement + DOC-040 acte) :
    # repartition des associes de la cible (avant/apres), parts cedees au holding, prix.
    cession_data: dict[str, object] = {"associes": []}
    if not is_apport:
        cession_data = _render_spfpl_cession_cible(prefix)

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
        "cession_data": cession_data,
        "denomination": denomination,
        # O24-03 : « siege » (affichage) derive du parse de la ligne unique.
        "siege": _siege_struct.adresse_affichee if _siege_struct else "",
        "siege_num": siege_num,
        "siege_voie": siege_voie,
        "siege_cp": siege_cp,
        "siege_ville": siege_ville,
        "ville_rcs": ville_rcs,
        "capital_social": capital,
        "nb_actions_total": nb_actions,
        # Valeur nominale CALCULEE (capital / nb actions), plus de saisie libre.
        "valeur_nominale_action": valeur_action,
        "civilite": civilite,
        # §14.2 : titre pro automatique (associe SPFPL dentiste = docteur). Plus de
        # « Docteur » dans la deroulante civilite ; le titre est pose ici.
        "titre_affichage": "Docteur",
        "prenom": prenom,
        "prenoms": prenoms or prenom,
        "nom": nom,
        # §14.2 : genre derive de la civilite CIVILE (M./Mme), plus de selecteur
        # « Genre civil » redondant.
        "genre": derive_gender_from_civilite(civilite),
        "date_naissance": date_naissance,
        "ville_naissance": ville_naissance,
        "departement_naissance": departement_naissance,
        "nationalite": nationalite,
        "regime_matrimonial": regime,
        # O24-03 : « adresse » (affichage) derivee du parse de la ligne unique.
        "adresse": _adresse_struct.adresse_affichee if _adresse_struct else "",
        "adresse_num": adresse_num,
        "adresse_voie": adresse_voie,
        "adresse_cp": adresse_cp,
        "adresse_ville": adresse_ville,
        "nom_pere": nom_pere,
        "nom_mere": nom_mere,
        "decision_date": decision_date,
        "conjoint_civilite": conjoint_civilite,
        "conjoint_genre": derive_gender_from_civilite(conjoint_civilite),
        "conjoint_prenom": conjoint_prenom,
        "conjoint_nom": conjoint_nom,
        "regime_communautaire": regime_communautaire,
        "ordre_departement": ordre_departement,
        "numero_ordre": numero_ordre,
        "numero_rpps": numero_rpps,
        "ordre_president_feminin": ordre_president_feminin,
        "mandataire_prenom": mandataire_prenom,
        "mandataire_nom": mandataire_nom,
        "ordre_conseil": ordre_conseil,
        "ordre_adresse_ligne_1": ordre_adresse_ligne_1,
        "ordre_cp": ordre_cp,
        "ordre_ville": ordre_ville,
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
        "cible_forme": cible_forme,
        "cible_profession": cible_profession,
        "cible_capital": cible_capital,
        "cible_nb_parts": cible_nb_parts,
        "cible_valeur_part": cible_valeur_part,
        "apport_nature_titres": apport_nature_titres,
        "apport_valeur_par_titre": apport_valeur_par_titre,
        **{f"commissaire_{k}": v for k, v in commissaire_fields.items()},
        **{f"evaluateur_{k}": v for k, v in evaluateur_fields.items()},
        "exercice_debut": exercice_debut,
        "exercice_fin": exercice_fin,
        "date_cloture": date_cloture,
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
    }


def build_spfpl_plan(payload: dict[str, object]) -> SpfplSlicePlan:
    structure = str(payload["structure"])
    operation, doc_code = OPERATION_BY_STRUCTURE[structure]
    regime_communautaire = bool(payload.get("regime_communautaire"))
    document_codes = _creation_bundle_codes(
        doc_code,
        regime_communautaire=regime_communautaire,
    )
    # Operation apport : le bundle de creation est complete par les documents
    # d'apport (contrat + 2 attestations), comme le canon « Si apport ».
    if operation == "apport":
        document_codes = document_codes + SPFPL_APPORT_OPERATION_CODES
    elif operation == "cession":
        # PV agrement : associe unique de la cible (<=1 associe reel) -> DOC-038,
        # sinon plusieurs associes -> DOC-039.
        cession_data = payload.get("cession_data") or {}
        nb_real = len(cession_data.get("associes") or [])  # type: ignore[arg-type]
        pv_code = (
            SPFPL_CESSION_PV_UNIQUE_CODE if nb_real <= 1 else SPFPL_CESSION_PV_PLUSIEURS_CODE
        )
        document_codes = document_codes + (
            SPFPL_CESSION_NOTE_CODE,
            pv_code,
            SPFPL_CESSION_ACTE_PARTS_CODE,
        )
    blockers = _validate(payload)
    warnings = [
        f"{structure} V1 = associe unique (multi-associes bloque par le moteur). Bundle de "
        "creation : statuts + tronc commun + PV gerant + demande ordre + note d'information.",
    ]
    if regime_communautaire:
        warnings.append("Regime communautaire actif : DOC-005 et DOC-006 seront generes.")
    warnings = tuple(warnings)
    if blockers:
        return SpfplSlicePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=document_codes,
            blockers=blockers,
            warnings=warnings,
        )
    return SpfplSlicePlan(
        can_generate=True,
        status="ready",
        reason=f"Pret pour generation {structure} V1 (bundle de creation).",
        document_codes=document_codes,
        blockers=(),
        warnings=warnings,
    )


def _validate(payload: dict[str, object]) -> tuple[str, ...]:
    blockers: list[str] = []
    required = (
        ("denomination", "Denomination SPFPL requise."),
        ("siege", "Siege SPFPL requis."),
        ("capital_social", "Capital social requis."),
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
    required += (
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
        ("ordre_conseil", "Conseil departemental de l'ordre requis (demande inscription)."),
        ("ordre_adresse_ligne_1", "Adresse de l'ordre requise (demande inscription)."),
        ("ordre_cp", "Code postal de l'ordre requis (demande inscription)."),
        ("ordre_ville", "Ville de l'ordre requise (demande inscription)."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    # Nombre d'actions VARIABLE (defaut 600) : doit etre >= 1 pour deriver une
    # valeur nominale coherente (capital / nb actions). Remplace l'ancien champ
    # « valeur nominale » en saisie libre (desormais calculee, non saisissable).
    # Dogfood 2026-06-22 : le « or 600 » NEUTRALISAIT cette garde (un 0 saisi devenait
    # 600 avant le test) -> 600 actions fantomes. On teste la valeur BRUTE.
    if int(payload.get("nb_actions_total") or 0) < 1:
        blockers.append("Nombre d'actions requis et superieur a zero.")
    # O24-05 (re-Akainu T4) : capital non divisible par le nb d'actions -> valeur nominale
    # fractionnaire (« 16.666... € ») dans le DOCX / lettres cassees. Garde partagee, meme
    # wording que civil/SAS/SELARL/SELAS.
    if not is_capital_divisible(payload.get("capital_social"), payload.get("nb_actions_total")):
        blockers.append(
            "Le capital social doit etre divisible par le nombre d'actions "
            "(la valeur nominale d'une action doit etre un nombre entier)."
        )
    if int(payload.get("apport_nb_parts") or 0) < 1:
        blockers.append("Nombre de parts apportees requis et superieur a zero.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    if payload.get("decision_date") is None:
        blockers.append("Date de decision requise (PV nomination gerant).")
    # Operation apport : les documents DOC-041/042/043 exigent le detail des
    # titres + les organes de controle (commissaire aux apports + evaluateur) +
    # la forme/capital de la cible (sinon le generateur leve `required_*`).
    if bool(payload.get("is_apport")):
        apport_required = (
            ("apport_valeur_par_titre", "Valeur d'un titre apporte requise (contrat d'apport)."),
            ("cible_forme", "Forme sociale de la cible requise (contrat d'apport)."),
            ("cible_capital", "Capital social de la cible requis (contrat d'apport)."),
            (
                "commissaire_denomination",
                "Denomination du commissaire aux apports requise (attestations).",
            ),
            ("commissaire_rep_nom", "Nom du representant du commissaire requis."),
            ("evaluateur_denomination", "Denomination de l'evaluateur de l'apport requise."),
            ("evaluateur_rep_nom", "Nom du representant de l'evaluateur requis."),
        )
        for field, message in apport_required:
            if not str(payload.get(field) or "").strip():
                blockers.append(message)
    if str(payload.get("operation") or "") == "cession":
        # Operation cession : repartition de la cible + prix + siege cible exiges par
        # la note d'info (DOC-037), le PV d'agrement (DOC-038/039) et l'acte (DOC-040).
        cd = payload.get("cession_data") or {}
        if not (cd.get("associes") or []):  # type: ignore[union-attr]
            blockers.append("Au moins un associe de la cible requis (cession).")
        if int(cd.get("nb_cedees") or 0) < 1:  # type: ignore[union-attr]
            blockers.append("Nombre de parts cedees au holding requis (cession).")
        if not str(cd.get("prix_unitaire") or "").strip():  # type: ignore[union-attr]
            blockers.append("Prix par part cedee requis (cession).")
        if not str(cd.get("cible_siege_num") or "").strip():  # type: ignore[union-attr]
            blockers.append("Siege structure de la cible requis (cession).")
        # Dogfood 2026-06-22 : la note d'info / le PV / l'acte exigent aussi la FORME
        # complete de la cible, son siege complet et l'identite de chaque associe cible
        # (sinon `required_*` leve a la generation alors que le plan disait « pret »).
        if not str(cd.get("cible_forme_complete") or "").strip():  # type: ignore[union-attr]
            blockers.append("Forme sociale complete de la cible requise (cession).")
        if not all(
            str(cd.get(field) or "").strip()  # type: ignore[union-attr]
            for field in ("cible_siege_voie", "cible_siege_cp", "cible_siege_ville")
        ):
            blockers.append("Adresse complete du siege de la cible requise (voie, CP, ville).")
        for index, associe in enumerate(cd.get("associes") or [], start=1):  # type: ignore[union-attr]
            data = associe or {}
            if not all(str(data.get(key) or "").strip() for key in ("civilite", "prenom", "nom")):
                blockers.append(
                    f"Associe cible {index} : civilite, prenom et nom requis (cession)."
                )
    return tuple(dict.fromkeys(blockers))


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    structure = str(payload["structure"])
    operation = str(payload["operation"])
    is_apport = bool(payload["is_apport"])
    capital = str(payload.get("capital_social") or "")
    nb_parts = int(payload.get("apport_nb_parts") or 0)
    # Nombre d'actions du capital : VARIABLE (defaut 600 = ancien codage en dur,
    # preserve la sortie byte-identique des dossiers existants). La valeur nominale
    # derive de capital / nb_actions ; on respecte une valeur deja calculee fournie
    # par le slice, sinon on la (re)calcule pour les appelants directs.
    nb_actions_total = int(payload.get("nb_actions_total") or 600)
    valeur_action = str(
        payload.get("valeur_nominale_action")
        or calculate_nominal_value(capital, nb_actions_total)
        or ""
    )
    # Detail des titres apportes (operation apport). La valeur globale est saisie ;
    # la valeur par titre est saisie (valeur d'un titre de la cible apporte). Les
    # versions « en lettres » sont DERIVEES, comme partout dans le slice. Le nombre
    # d'actions SPFPL attribuees en contrepartie = le nombre total d'actions du
    # holding (l'apporteur, associe unique, recoit toutes les actions).
    nature_titres = str(payload.get("apport_nature_titres") or "parts sociales")
    valeur_par_titre = str(payload.get("apport_valeur_par_titre") or "")
    valeur_globale = str(payload.get("apport_valeur_globale") or "")

    founder_genre = payload.get("genre") or Gender.MASCULIN
    founder = SpfplPerson(
        civilite_affichage=str(payload.get("civilite") or "Docteur"),
        prenom=str(payload.get("prenom") or ""),
        prenoms=str(payload.get("prenoms") or payload.get("prenom") or ""),
        nom=str(payload.get("nom") or ""),
        genre=founder_genre,
        profession="chirurgien-dentiste",
        profession_reglementee="chirurgiens-dentistes",
        profession_reglementee_pluriel="chirurgiens-dentistes",
        # LIVE-03 : date de naissance a saisie LIBRE -> re-accentue les mois avant
        # injection dans les statuts SPFPL (echo fidele du modele). Saisie ISO
        # (12/04/1984) intacte ; saisie textuelle (« 12 avril 1984 ») accentuee.
        date_naissance=accentuate_french_months(str(payload.get("date_naissance") or "")),
        ville_naissance=str(payload.get("ville_naissance") or ""),
        departement_naissance=str(payload.get("departement_naissance") or ""),
        nationalite=str(payload.get("nationalite") or ""),
        # O24-11 (MINEUR 2b) : statut ACCENTUE et accorde au genre (« marié »/
        # « mariée ») au lieu du « marie » nu — l'acte de cession d'actions SPFPL
        # rend cedant.situation_maritale verbatim. Le SPFPL dentiste est marie par
        # construction (conjoint requis), seul le genre varie.
        situation_maritale=situation_display("marie", founder_genre),
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
    cible_capital = str(payload.get("cible_capital") or "")
    nb_apportees = nb_parts
    regime_communautaire_actif = bool(payload.get("regime_communautaire"))
    # --- Operation cession : repartition de la cible + pricing (DOC-037/038/039/040).
    cession_data = payload.get("cession_data") or {}
    cession_associes_raw = cession_data.get("associes") or []  # type: ignore[union-attr]
    nb_cedees = int(cession_data.get("nb_cedees") or 0)  # type: ignore[union-attr]
    prix_unitaire_num = _parse_amount(cession_data.get("prix_unitaire"))  # type: ignore[union-attr]
    prix_total_num = prix_unitaire_num * nb_cedees
    associe_unique_cible = len(cession_associes_raw) <= 1
    if is_apport:
        cession_parts_obj = CessionParts(
            nb_parts=nb_apportees,
            nb_parts_lettres=number_words_from_value(nb_apportees),
            plage_parts=str(payload.get("apport_plage") or ""),
        )
    else:
        cession_parts_obj = CessionParts(
            nb_parts=nb_cedees,
            nb_parts_lettres=number_words_from_value(nb_cedees),
            plage_parts=str(cession_data.get("plage_cedee") or ""),  # type: ignore[union-attr]
            prix_unitaire=format_grouped_numeric_value(prix_unitaire_num),
            prix_unitaire_lettres=_euros_lettres(prix_unitaire_num),
            prix_total=format_grouped_numeric_value(prix_total_num),
            prix_total_lettres=_euros_lettres(prix_total_num),
            nombre_exemplaires_lettres="trois",
        )
    ctx = DocumentGenerationContext(
        structure=structure,
        dossier_options=DossierOptions(
            apport=is_apport,
            cession=not is_apport,
            # PV d'agrement : en cession, le « associe unique » reflete la CIBLE
            # (1 associe reel -> DOC-038 ; sinon DOC-039). En apport, sans effet.
            associe_unique=(True if is_apport else associe_unique_cible),
            regime_communautaire=regime_communautaire_actif,
        ),
        conjoint=(
            _conjoint_person(payload, adresse_perso) if regime_communautaire_actif else None
        ),
        regime_communautaire=(
            _regime_communautaire(payload) if regime_communautaire_actif else None
        ),
        personne_signataire=Person(
            genre=payload.get("genre") or Gender.MASCULIN,
            civilite=str(payload.get("civilite") or "Monsieur"),
            prenom=str(payload.get("prenom") or ""),
            nom=str(payload.get("nom") or ""),
            # §14.2 : titre PRO = « Docteur » automatique (et non la civilite civile
            # M./Mme), utilise par la demande d'inscription a l'ordre. L'associe
            # d'une SPFPL dentiste est necessairement docteur.
            titre_affichage=str(payload.get("titre_affichage") or "Docteur"),
            adresse_perso=adresse_perso,
            adresse_personnelle_affichee=adresse_perso.adresse_affichee,
            date_naissance=cc.parse_birth_date(payload.get("date_naissance")),
            ville_naissance=str(payload.get("ville_naissance") or ""),
            nationalite=str(payload.get("nationalite") or ""),
            nom_pere=str(payload.get("nom_pere") or ""),
            nom_mere=str(payload.get("nom_mere") or ""),
            fonction_dirigeant="président",
            qualification_principale="chirurgien-dentiste",
        ),
        signature=Signature(
            lieu=str(payload.get("signature_lieu") or ""),
            date=payload.get("signature_date"),
            nombre_exemplaires="trois",
        ),
        societe=Company(
            forme_sociale="SPFPL",
            forme_sociale_affichage="SPFPL",
            forme_sociale_abregee="SPFPL",
            forme_sociale_complete=(
                "société de participations financières de professions libérales"
            ),
            forme_sociale_libelle_long=(
                "Société de participations financières de professions libérales"
            ),
            denomination=str(payload.get("denomination") or ""),
            denomination_courte=str(payload.get("denomination") or ""),
            capital=capital,
            capital_social=capital,
            capital_variable=True,
            siege=siege_struct,
            ville_rcs=str(payload.get("ville_rcs") or payload.get("siege_ville") or ""),
        ),
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee=siege_struct.adresse_affichee,
        ),
        mandataire=cc.default_mandataire(
            prenom=str(payload.get("mandataire_prenom") or ""),
            nom=str(payload.get("mandataire_nom") or ""),
        ),
        ordre=_spfpl_ordre_professionnel(payload),
        capital=CapitalContext(
            nb_parts_total=nb_apportees,
            valeur_nominale_part=valeur_action,
            nb_parts_representees=nb_apportees,
            montant=capital,
            type_titre="actions",
        ),
        dirigeant_nomine=DirigeantNomine(
            genre=payload.get("genre") or Gender.MASCULIN,
            civilite_affichage=str(payload.get("civilite") or "Monsieur"),
            prenom=str(payload.get("prenom") or ""),
            nom=str(payload.get("nom") or ""),
            date_naissance=cc.parse_birth_date(payload.get("date_naissance")),
            ville_naissance=str(payload.get("ville_naissance") or ""),
            departement_naissance=str(payload.get("departement_naissance") or ""),
            nationalite=str(payload.get("nationalite") or ""),
            adresse_personnelle=adresse_perso,
            fonction_affichage="président",
            ref_associe_index=0,
        ),
        associes=[_spfpl_pv_associe(payload, nb_apportees)],
        # SCS2/SU4 (Albane 2026-06-25, propag. Q4) : date de decision (PV) = date de signature.
        decision=DecisionContext(date=_display_date(payload.get("signature_date"))),
        reunion=ReunionContext(
            date_lettres=date_to_french_words(payload.get("decision_date")),
            # Annee en lettres + heure : exigees par le PV d'agrement de cession.
            annee_lettres=_annee_lettres(payload.get("decision_date")),
            heure="10 heures",
            president=ReunionPresident(
                civilite_affichage=str(payload.get("civilite") or "Monsieur"),
                prenom=str(payload.get("prenom") or ""),
                nom=str(payload.get("nom") or ""),
                qualite="associé unique",
                civilite_president_seance=str(payload.get("civilite") or "Monsieur"),
                prenom_president_seance=str(payload.get("prenom") or ""),
                nom_personne_seance=str(payload.get("nom") or ""),
            ),
        ),
        cedant=founder if not is_apport else None,
        apporteur=founder if is_apport else None,
        operation_titres=OperationTitres(nb_titres=nb_apportees),
        operation_spfpl=OperationSpfpl(type=operation),
        societe_spfpl=SocieteSpfpl(
            denomination=str(payload.get("denomination") or ""),
            forme_sociale="par actions simplifiee",
            capital_social=capital,
            capital_social_lettres=number_words_from_value(capital),
            # Activite + profession : exiges par le contrat d'apport (DOC-041) et
            # l'attestation du commissaire (DOC-043). Boilerplate du type SPFPL
            # dentiste, pas une saisie de dossier.
            activite=_SPFPL_ACTIVITE,
            profession="chirurgien-dentiste",
            valeur_nominale_action=valeur_action,
            valeur_nominale_action_lettres=number_words_from_value(valeur_action),
            siege=siege_struct,
            ville_rcs=str(payload.get("ville_rcs") or payload.get("siege_ville") or ""),
            numero_rcs="en cours",
            dirigeant=SpfplDirigeant(fonction="Président"),
            representant=SpfplRepresentant(
                civilite_affichage=str(payload.get("civilite") or "Monsieur"),
                # Civilite courte (M./Mme) : exigee par l'acte de cession (DOC-040).
                civilite_courte=(
                    "Mme"
                    if str(payload.get("civilite") or "").strip().lower() == "madame"
                    else "M."
                ),
                prenom=str(payload.get("prenom") or ""),
                nom=str(payload.get("nom") or ""),
                fonction="Président",
            ),
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
            nature_titres=nature_titres,
            plage_parts=str(payload.get("apport_plage") or ""),
            valeur_par_titre=valeur_par_titre,
            valeur_par_titre_lettres=number_words_from_value(valeur_par_titre),
            valeur_globale=valeur_globale,
            valeur_globale_lettres=number_words_from_value(valeur_globale),
            nb_actions_attribuees=nb_actions_total,
            nb_actions_attribuees_lettres=number_words_from_value(nb_actions_total),
            valeur_nominale_action=valeur_action,
            valeur_nominale_action_lettres=number_words_from_value(valeur_action),
        ),
        societe_cible=SocieteCible(
            denomination=str(payload.get("cible_denomination") or ""),
            forme_sociale=str(payload.get("cible_forme") or ""),
            # Forme complete : exigee par l'acte de cession (DOC-040). Saisie au
            # sous-formulaire cession ; repli sur la forme courte sinon.
            forme_sociale_complete=str(
                cession_data.get("cible_forme_complete")  # type: ignore[union-attr]
                or payload.get("cible_forme")
                or ""
            ),
            profession_reglementee=str(payload.get("cible_profession") or ""),
            capital_social=cible_capital,
            capital_social_lettres=number_words_from_value(cible_capital),
            nb_parts_total=int(payload.get("cible_nb_parts") or 0),
            valeur_nominale_part=str(payload.get("cible_valeur_part") or ""),
            valeur_nominale_part_lettres=number_words_from_value(
                payload.get("cible_valeur_part")
            ),
            siege=Address(
                num_voie=str(cession_data.get("cible_siege_num") or ""),  # type: ignore[union-attr]
                voie=str(cession_data.get("cible_siege_voie") or ""),  # type: ignore[union-attr]
                cp=str(cession_data.get("cible_siege_cp") or ""),  # type: ignore[union-attr]
                ville=str(cession_data.get("cible_siege_ville") or ""),  # type: ignore[union-attr]
                # O24-03 : affichage derive du parse de la ligne unique (cession),
                # repli sur le champ « affiche » du bloc principal (apport / legacy).
                adresse_affichee=str(
                    cession_data.get("cible_siege_affiche")  # type: ignore[union-attr]
                    or payload.get("cible_siege")
                    or ""
                ),
            ),
            ville_rcs=str(payload.get("cible_ville_rcs") or ""),
            numero_rcs=str(payload.get("cible_numero_rcs") or ""),
        ),
        cession_parts=cession_parts_obj,
        associes_cible=(_build_associes_cible(payload) if not is_apport else []),
        capital_souscription=CapitalSouscription(
            nb_actions_total=nb_actions_total,
            valeur_nominale_action=valeur_action,
            # Apport SPFPL : le capital est constitue par l'apport EN NATURE des
            # titres de la cible (numeraire = 0). L'apporteur est l'unique
            # souscripteur et recoit toutes les actions.
            apports_nature_montant=valeur_globale,
            apports_numeraire_montant="0 euro",
            souscripteurs=[
                CapitalSouscripteur(
                    civilite_affichage="Docteur",
                    prenom=str(payload.get("prenom") or ""),
                    nom=str(payload.get("nom") or ""),
                    profession="chirurgien-dentiste",
                    adresse_personnelle_affichee=adresse_perso.adresse_affichee,
                    nb_actions=nb_actions_total,
                    qualite="actionnaire unique",
                )
            ],
        ),
        exercice_social=ExerciceSocial(
            # LIVE-03 : re-accentue les mois saisis librement (« 1er aout » -> « 1er août »)
            # EN AMONT du generateur, qui reste un echo fidele du modele. debut accentue
            # comme fin/cloture (oubli releve par re-Akainu T4).
            debut=accentuate_french_months(str(payload.get("exercice_debut") or "")),
            fin=accentuate_french_months(str(payload.get("exercice_fin") or "")),
            date_cloture_premier_exercice=accentuate_french_months(
                str(payload.get("date_cloture") or "")
            ),
        ),
        # Organes de controle de l'apport : SAISIS dans le sous-formulaire apport
        # (plus de valeurs en dur). Chaque dossier a son propre commissaire aux
        # apports et son evaluateur. None en cession (non lus).
        commissaire_aux_apports=(
            _professional_entity(payload, "commissaire") if is_apport else None
        ),
        evaluateur_apport=(
            _professional_entity(payload, "evaluateur") if is_apport else None
        ),
        metadata={"front_slice": f"track_b_spfpl_{operation}_v1"},
    )
    return ctx


def _conjoint_person(payload: dict[str, object], signataire_address: Address) -> Person:
    """Conjoint (renonciation DOC-005 + avertissement DOC-006).

    L'avertissement adresse le conjoint au domicile du foyer ; on reutilise
    l'adresse personnelle structuree de l'actionnaire, deja saisie.
    """
    return Person(
        genre=payload.get("conjoint_genre") or Gender.FEMININ,
        civilite=str(payload.get("conjoint_civilite") or "Madame"),
        prenom=str(payload.get("conjoint_prenom") or ""),
        nom=str(payload.get("conjoint_nom") or ""),
        adresse_perso=signataire_address,
        adresse_personnelle_affichee=signataire_address.adresse_affichee,
    )


def _regime_communautaire(payload: dict[str, object]) -> RegimeCommunautaire:
    """Mappe les saisies vers le contexte du conditionnel regime communautaire."""
    signature_date = payload.get("signature_date")
    return RegimeCommunautaire(
        avertissement=RegimeCommunautaireAvertissement(date_signature=signature_date),
        renonciation=RegimeCommunautaireRenonciation(
            lieu_signature=str(payload.get("signature_lieu") or ""),
            date_signature=signature_date,
            nombre_exemplaires_lettres="quatre",
        ),
        date_courrier_avertissement=signature_date,
        regime_matrimonial=str(payload.get("regime_matrimonial") or ""),
        qualite_renoncee="associé",
    )


def _render_entity_inputs(prefix: str, role: str) -> dict[str, str]:
    """Saisie d'une entite professionnelle (commissaire aux apports / evaluateur).

    Collecte les champs exiges par `professional_entity_presentation` (denomination,
    forme, capital, siege, RCS) + son representant (civilite / prenom / nom).
    """
    col_a, col_b, col_c = st.columns(3)
    denomination = _t(col_a, prefix, f"{role}_denomination", "Denomination")
    forme = _t(col_b, prefix, f"{role}_forme", "Forme sociale")
    capital = _t(col_c, prefix, f"{role}_capital", "Capital social")
    siege = _t(st, prefix, f"{role}_siege", "Siege (adresse affichee)")
    col_d, col_e = st.columns(2)
    ville_rcs = _t(col_d, prefix, f"{role}_ville_rcs", "RCS (ville)")
    numero_rcs = _t(col_e, prefix, f"{role}_numero_rcs", "Numero RCS")
    col_f, col_g, col_h = st.columns(3)
    rep_civilite = col_f.selectbox(
        "Civilite representant",
        ("Monsieur", "Madame"),
        key=f"{prefix}_{role}_rep_civilite",
    )
    rep_prenom = _t(col_g, prefix, f"{role}_rep_prenom", "Prenom representant")
    rep_nom = _t(col_h, prefix, f"{role}_rep_nom", "Nom representant")
    return {
        "denomination": denomination,
        "forme": forme,
        "capital": capital,
        "siege": siege,
        "ville_rcs": ville_rcs,
        "numero_rcs": numero_rcs,
        "rep_civilite": rep_civilite,
        "rep_prenom": rep_prenom,
        "rep_nom": rep_nom,
    }


def _professional_entity(payload: dict[str, object], role: str) -> ProfessionalEntity | None:
    """Construit une entite professionnelle (commissaire / evaluateur) du payload.

    Renvoie None si la denomination n'est pas saisie (le validateur apport bloque
    alors la generation avec un message explicite).
    """
    denomination = str(payload.get(f"{role}_denomination") or "")
    if not denomination:
        return None
    return ProfessionalEntity(
        denomination=denomination,
        forme_sociale=str(payload.get(f"{role}_forme") or ""),
        capital_social=str(payload.get(f"{role}_capital") or ""),
        siege=Address(adresse_affichee=str(payload.get(f"{role}_siege") or "")),
        ville_rcs=str(payload.get(f"{role}_ville_rcs") or ""),
        numero_rcs=str(payload.get(f"{role}_numero_rcs") or ""),
        representant=SpfplRepresentant(
            civilite_affichage=str(payload.get(f"{role}_rep_civilite") or ""),
            prenom=str(payload.get(f"{role}_rep_prenom") or ""),
            nom=str(payload.get(f"{role}_rep_nom") or ""),
        ),
    )


def _render_spfpl_cession_cible(prefix: str) -> dict[str, object]:
    """Sous-formulaire cession SPFPL : repartition des associes de la cible
    (avant/apres), parts cedees au holding, prix par part, forme complete de la cible.
    Alimente la note d'info (DOC-037), le PV d'agrement (DOC-038/039) et l'acte (DOC-040)."""
    st.markdown("**Cession — repartition de la cible & prix**")
    col_a, col_b, col_c = st.columns(3)
    nb_cedees = _i(col_a, prefix, "cession_nb_parts_cedees", "Parts cedees au holding")
    prix_unitaire = _t(
        col_b, prefix, "cession_prix_unitaire", "Prix par part", hint="ex : 1 000"
    )
    plage_cedee = _t(col_c, prefix, "cession_plage_cedee", "Plage parts cedees (ex: 41 a 100)")
    cible_forme_complete = _t(
        st,
        prefix,
        "cible_forme_complete",
        "Forme complete de la cible",
        hint="ex : societe d'exercice liberal a responsabilite limitee",
    )
    # O24-03 : siege de la cible sur UNE ligne (parse interne -> num/voie/cp/ville
    # exiges par l'acte/PV de cession). Remplace l'ancienne grille No/Voie/CP/Ville
    # ET le champ « Siege cible (affiche) » du bloc principal (double-saisie).
    cible_siege_ligne = _t(
        st, prefix, "cible_siege_cession", "Adresse du siège de la cible (N° et voie, CP Ville)"
    )
    _cible_struct = _parse_address_full(cible_siege_ligne)
    cible_siege_num = _cible_struct.num_voie if _cible_struct else ""
    cible_siege_voie = _cible_struct.voie if _cible_struct else ""
    cible_siege_cp = _cible_struct.cp if _cible_struct else ""
    cible_siege_ville = _cible_struct.ville if _cible_struct else ""
    cible_siege_affiche = _cible_struct.adresse_affichee if _cible_struct else ""
    nb_associes = int(
        st.number_input(
            "Nombre d'associes de la cible (hors holding acquereur)",
            min_value=1,
            max_value=6,
            step=1,
            key=f"{prefix}_cession_nb_associes",
        )
    )
    associes: list[dict[str, object]] = []
    for i in range(nb_associes):
        st.caption(f"Associe cible {i + 1}")
        c1, c2, c3 = st.columns(3)
        civ = c1.selectbox(
            "Civilite",
            ("Docteur", "Monsieur", "Madame"),
            key=f"{prefix}_cession_assoc_{i}_civ",
        )
        pre = _t(c2, prefix, f"cession_assoc_{i}_prenom", "Prenom")
        nom = _t(c3, prefix, f"cession_assoc_{i}_nom", "Nom")
        c4, c5, c6 = st.columns(3)
        avant = _i(c4, prefix, f"cession_assoc_{i}_avant", "Parts avant")
        apres = _i(c5, prefix, f"cession_assoc_{i}_apres", "Parts apres")
        plage = _t(c6, prefix, f"cession_assoc_{i}_plage", "Plage (ex: 1 a 10)")
        associes.append(
            {
                "civilite": civ,
                "prenom": pre,
                "nom": nom,
                "avant": avant,
                "apres": apres,
                "plage": plage,
            }
        )
    return {
        "nb_cedees": nb_cedees,
        "prix_unitaire": prix_unitaire,
        "plage_cedee": plage_cedee,
        "cible_forme_complete": cible_forme_complete,
        "cible_siege_num": cible_siege_num,
        "cible_siege_voie": cible_siege_voie,
        "cible_siege_cp": cible_siege_cp,
        "cible_siege_ville": cible_siege_ville,
        "cible_siege_affiche": cible_siege_affiche,
        "associes": associes,
    }


def _parse_amount(value: object) -> int:
    """Parse un montant saisi (« 1 000 », « 1000 ») en entier (espaces/insecables retires)."""
    raw = str(value or "").replace(" ", "").replace(" ", "").replace("\xa0", "")
    digits = "".join(c for c in raw if c.isdigit())
    return int(digits) if digits else 0


def _euros_lettres(amount: int) -> str:
    """Montant en lettres + « euros » (ex. 60000 -> « soixante mille euros »)."""
    lettres = number_words_from_value(amount)
    return f"{lettres} euros" if lettres else ""


def _annee_lettres(value: object) -> str:
    """Annee en lettres a partir d'une date (ex. 2026 -> « deux mille vingt-six »)."""
    if isinstance(value, date):
        return number_words_from_value(value.year)
    return ""


def _build_associes_cible(payload: dict[str, object]) -> list[object]:
    """Construit la liste AssocieCible (vendeurs/restants de la cible + holding
    acquereur en personne morale qui recoit les parts cedees)."""
    from sydel_doc_engine.domain.models import AssocieCible

    cession_data = payload.get("cession_data") or {}
    raw = cession_data.get("associes") or []  # type: ignore[union-attr]
    nb_cedees = int(cession_data.get("nb_cedees") or 0)  # type: ignore[union-attr]
    associes: list[object] = [
        AssocieCible(
            civilite_affichage=str(a.get("civilite") or "Docteur"),
            prenom=str(a.get("prenom") or ""),
            nom=str(a.get("nom") or ""),
            nb_parts_avant=int(a.get("avant") or 0),
            nb_parts_apres=int(a.get("apres") or 0),
            plage_parts=str(a.get("plage") or ""),
        )
        for a in raw
    ]
    # Le holding acquereur (personne morale) recoit les parts cedees.
    associes.append(
        AssocieCible(
            type="personne_morale",
            denomination=str(payload.get("denomination") or ""),
            nb_parts_avant=0,
            nb_parts_apres=nb_cedees,
            plage_parts=str(cession_data.get("plage_cedee") or ""),  # type: ignore[union-attr]
            est_present_ou_represente=False,
        )
    )
    return associes


def _spfpl_ordre_professionnel(payload: dict[str, object]) -> OrdreProfessionnel:
    ligne_1 = str(payload.get("ordre_adresse_ligne_1") or "")
    cp = str(payload.get("ordre_cp") or "")
    ville = str(payload.get("ordre_ville") or "")
    bloc = f"{ligne_1}\n{cp} {ville}"
    return OrdreProfessionnel(
        conseil_departemental_libelle=str(payload.get("ordre_conseil") or ""),
        departement_inscription=str(payload.get("ordre_departement") or ""),
        destinataire_appel=(
            "Madame la Présidente"
            if bool(payload.get("ordre_president_feminin"))
            else "Monsieur le Président"
        ),
        profession_signataire_affichee="chirurgien-dentiste",
        profession_ligne_destinataire="chirurgiens-dentistes",
        profession_reglementee_pluriel="chirurgiens-dentistes",
        adresse_affichee=bloc,
        adresse_bloc_affiche=bloc,
        adresse=OrdreAddress(
            ligne_1=str(payload.get("ordre_adresse_ligne_1") or ""),
            cp=str(payload.get("ordre_cp") or ""),
            ville=str(payload.get("ordre_ville") or ""),
        ),
    )


def _spfpl_pv_associe(payload: dict[str, object], nb_parts: int) -> object:
    from sydel_doc_engine.domain.models import Associe

    return Associe(
        genre=payload.get("genre") or Gender.MASCULIN,
        civilite_affichage=str(payload.get("civilite") or "Monsieur"),
        prenom=str(payload.get("prenom") or ""),
        nom=str(payload.get("nom") or ""),
        nb_parts=nb_parts,
        nb_parts_lettres=number_words_from_value(nb_parts),
        profession="chirurgien-dentiste",
        profession_reglementee="chirurgien-dentiste",
        qualite="associé unique",
    )


def _siege_display(payload: dict[str, object]) -> str:
    return (
        f"{payload.get('siege_num', '')} {payload.get('siege_voie', '')}, "
        f"{payload.get('siege_cp', '')} {payload.get('siege_ville', '')}"
    ).strip(" ,")


def _display_date(value) -> str | None:
    if value is None:
        return None
    return value.strftime("%d/%m/%Y")


def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_spfpl_plan(payload)
    if not plan.can_generate:
        raise ValueError(plan.reason)
    ctx = build_generation_context(payload)
    docx_paths = generate_docx_files_for_document_codes(ctx, output_dir, plan.document_codes)
    docx_paths = rename_dnc_with_signataire(docx_paths, ctx)  # O24-02 : DNC nommee par le dirigeant
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


def _t(container, prefix: str, field: str, label: str, hint: str | None = None) -> str:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = ""
    # O24-04 : tous les champs texte SPFPL passent par le helper « copier » partagé.
    return str(copyable_text_input(container, label, key=key, help=hint)).strip()


def _i(container, prefix: str, field: str, label: str) -> int:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date(prefix: str, field: str, label: str) -> date | None:
    # Consomme la couche de rendu partagee (front_widgets) au lieu de reimplementer
    # le helper localement (cause racine des ecarts de parite).
    return date_input_with_today(label, key=f"{prefix}_{field}", value=date.today())
