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
    CapitalContext,
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
from sydel_doc_engine.front_app.field_derivations import (
    date_to_french_words,
    derive_gender_from_civilite,
    format_french_date,
    number_words_from_value,
    parse_french_date,
)

OPERATION_BY_STRUCTURE: dict[str, tuple[str, str]] = {
    "SPFPL cession": ("cession", "DOC-035"),
    "SPFPL apport": ("apport", "DOC-036"),
}

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
    st.subheader("Donnees a saisir")
    st.markdown(f"**Societe SPFPL ({operation})**")
    col_a, col_b = st.columns(2)
    denomination = _t(col_a, prefix, "denomination", "Denomination SPFPL")
    siege = _t(col_b, prefix, "siege", "Siege (adresse affichee)")
    st.caption("Siege social (adresse structuree, pour la domiciliation / procuration)")
    col_sa, col_sb, col_sc, col_sd = st.columns(4)
    siege_num = _t(col_sa, prefix, "siege_num", "No")
    siege_voie = _t(col_sb, prefix, "siege_voie", "Voie")
    siege_cp = _t(col_sc, prefix, "siege_cp", "CP")
    siege_ville = _t(col_sd, prefix, "siege_ville", "Ville")
    col_c, col_d = st.columns(2)
    capital = _t(col_c, prefix, "capital_social", "Capital social")
    valeur_action = _t(col_d, prefix, "valeur_nominale_action", "Valeur nominale d'une action")
    ville_rcs = _t(st, prefix, "ville_rcs", "RCS SPFPL (ville)")

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
    st.caption("Adresse personnelle structuree + filiation (declaration de non-condamnation)")
    col_aa, col_ab, col_ac, col_ad = st.columns(4)
    adresse_num = _t(col_aa, prefix, "adresse_num", "No")
    adresse_voie = _t(col_ab, prefix, "adresse_voie", "Voie")
    adresse_cp = _t(col_ac, prefix, "adresse_cp", "CP")
    adresse_ville = _t(col_ad, prefix, "adresse_ville", "Ville")
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
    regime_key = f"{prefix}_regime_communautaire"
    if regime_key not in st.session_state:
        st.session_state[regime_key] = False
    regime_communautaire = st.checkbox(
        "Regime communautaire (ajoute lettre de renonciation + avertissement au conjoint)",
        key=regime_key,
    )

    st.markdown("Ordre")
    col_r, col_s, col_t = st.columns(3)
    ordre_departement = _t(col_r, prefix, "ordre_departement", "Departement ordre")
    numero_ordre = _t(col_s, prefix, "numero_ordre", "Numero ordre")
    numero_rpps = _t(col_t, prefix, "numero_rpps", "Numero RPPS")
    col_ra, col_rb, col_rc = st.columns(3)
    ordre_conseil = _t(col_ra, prefix, "ordre_conseil", "Conseil departemental")
    ordre_adresse_ligne_1 = _t(col_rb, prefix, "ordre_adresse_ligne_1", "Adresse ordre")
    ordre_cp = _t(col_rc, prefix, "ordre_cp", "CP ordre")
    ordre_ville = _t(st, prefix, "ordre_ville", "Ville ordre")

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
        "siege_num": siege_num,
        "siege_voie": siege_voie,
        "siege_cp": siege_cp,
        "siege_ville": siege_ville,
        "ville_rcs": ville_rcs,
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
        "exercice_debut": exercice_debut,
        "exercice_fin": exercice_fin,
        "date_cloture": date_cloture,
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
    }


def build_spfpl_plan(payload: dict[str, object]) -> SpfplSlicePlan:
    structure = str(payload["structure"])
    _operation, doc_code = OPERATION_BY_STRUCTURE[structure]
    regime_communautaire = bool(payload.get("regime_communautaire"))
    document_codes = _creation_bundle_codes(
        doc_code,
        regime_communautaire=regime_communautaire,
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
    if int(payload.get("apport_nb_parts") or 0) < 1:
        blockers.append("Nombre de parts apportees requis et superieur a zero.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    if payload.get("decision_date") is None:
        blockers.append("Date de decision requise (PV nomination gerant).")
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
    ctx = DocumentGenerationContext(
        structure=structure,
        dossier_options=DossierOptions(
            apport=is_apport,
            cession=not is_apport,
            associe_unique=True,
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
            titre_affichage=str(payload.get("civilite") or "Docteur"),
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
        mandataire=cc.default_mandataire(),
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
        decision=DecisionContext(date=_display_date(payload.get("decision_date"))),
        reunion=ReunionContext(
            date_lettres=date_to_french_words(payload.get("decision_date")),
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
            valeur_nominale_action=valeur_action,
            valeur_nominale_action_lettres=number_words_from_value(valeur_action),
            siege=siege_struct,
            ville_rcs=str(payload.get("ville_rcs") or payload.get("siege_ville") or ""),
            dirigeant=SpfplDirigeant(fonction="Président"),
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
            forme_sociale=str(payload.get("cible_forme") or ""),
            profession_reglementee=str(payload.get("cible_profession") or ""),
            capital_social=cible_capital,
            capital_social_lettres=number_words_from_value(cible_capital),
            nb_parts_total=int(payload.get("cible_nb_parts") or 0),
            valeur_nominale_part=str(payload.get("cible_valeur_part") or ""),
            valeur_nominale_part_lettres=number_words_from_value(
                payload.get("cible_valeur_part")
            ),
            siege=Address(adresse_affichee=str(payload.get("cible_siege") or "")),
            ville_rcs=str(payload.get("cible_ville_rcs") or ""),
            numero_rcs=str(payload.get("cible_numero_rcs") or ""),
        ),
        cession_parts=CessionParts(
            nb_parts=nb_apportees,
            nb_parts_lettres=number_words_from_value(nb_apportees),
            plage_parts=str(payload.get("apport_plage") or ""),
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


def _spfpl_ordre_professionnel(payload: dict[str, object]) -> OrdreProfessionnel:
    ligne_1 = str(payload.get("ordre_adresse_ligne_1") or "")
    cp = str(payload.get("ordre_cp") or "")
    ville = str(payload.get("ordre_ville") or "")
    bloc = f"{ligne_1}\n{cp} {ville}"
    return OrdreProfessionnel(
        conseil_departemental_libelle=str(payload.get("ordre_conseil") or ""),
        departement_inscription=str(payload.get("ordre_departement") or ""),
        destinataire_appel="Monsieur le Président",
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
    # Bouton « Aujourd'hui » (comme SELARL) : ecrit la date du jour AVANT que le
    # text_input soit instancie (sinon Streamlit interdit la modif post-widget).
    if st.button("Aujourd'hui", key=f"{key}_today"):
        st.session_state[key] = format_french_date(date.today())
    raw = st.text_input(label, key=key, placeholder="JJ/MM/AAAA")
    return parse_french_date(raw)
