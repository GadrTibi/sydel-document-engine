"""Donnees de TEST / prefill (developpement uniquement).

Fixtures de pre-remplissage du front Track B (bouton « Generer des donnees de test »).
Donnees fictives, sans aucune donnee reelle. Extrait de `shell.py` pour separer le code
de rendu UI de production des helpers de donnees de demonstration (refacto qualite C1,
bilan de sante 2026-06-26 ; aucun changement de comportement).
"""

from __future__ import annotations

import random
from datetime import date

import streamlit as st

from sydel_doc_engine.front_app.field_derivations import (
    MATRIMONIAL_STATUS_MARRIED_COMMUNAUTE,
    MATRIMONIAL_STATUS_PRESETS,
    NATIONALITY_PRESETS,
    format_french_date,
)
from sydel_doc_engine.front_app.selarl_slice import (
    PROFESSION_DENTISTE,
    PROFESSION_MEDECIN,
)
from sydel_doc_engine.scenarios.selarl import scm_cession_fixture

# Cle d'etat du dossier genere (copie locale du literal de shell.py : pur literal, evite
# un import circulaire shell <-> _dev_fixtures).
GENERATED_DOSSIER_STATE_KEY = "clean_generated_dossier"


def _prefill_random_selarl_data() -> None:
    person = random.choice(_test_people())
    company = random.choice(_test_companies())
    capital, parts = random.choice(((1000, 100), (2000, 200), (5000, 500), (10000, 1000)))
    # Respecte la profession deja choisie dans le wizard pour que la cession
    # preremplie soit coherente (medical vs dentaire) ; defaut Medecin.
    profession_label = st.session_state.get("selarl_profession") or "Medecin"
    if profession_label not in ("Medecin", "Chirurgien-dentiste"):
        profession_label = "Medecin"
    regime_communautaire = profession_label == "Chirurgien-dentiste" or random.choice(
        (False, True)
    )
    today_text = format_french_date(date.today())
    dossier_suffix = random.randint(1000, 9999)
    status = (
        MATRIMONIAL_STATUS_MARRIED_COMMUNAUTE
        if regime_communautaire
        else random.choice(
            tuple(
                item
                for item in MATRIMONIAL_STATUS_PRESETS
                if item != MATRIMONIAL_STATUS_MARRIED_COMMUNAUTE
            )
        )
    )

    profession_key = (
        PROFESSION_DENTISTE if profession_label == "Chirurgien-dentiste" else PROFESSION_MEDECIN
    )

    values = {
        "selarl_profession": profession_label,
        "selarl_dossier_unipersonnel": True,
        "selarl_cession": True,
        "selarl_scm": True,
        "selarl_dossier_reference": f"TEST-SELARL-{dossier_suffix}",
        "selarl_civilite": person["civilite"],
        "selarl_prenom": person["prenom"],
        "selarl_nom": person["nom"],
        "selarl_date_naissance": person["date_naissance"],
        "selarl_ville_naissance": person["ville_naissance"],
        "selarl_ville_naissance_article_au": False,
        "selarl_departement_naissance": person["departement_naissance"],
        "selarl_nationalite_choice": random.choice(NATIONALITY_PRESETS[:-1]),
        "selarl_nationalite_other": "",
        "selarl_situation_maritale": status,
        "selarl_numero_ordre": f"ORD-{random.randint(100000, 999999)}",
        "selarl_numero_rpps": str(random.randint(10000000000, 19999999999)),
        "selarl_nom_pere": person["nom_pere"],
        "selarl_nom_mere": person["nom_mere"],
        # O24-03 : adresse perso sur UNE ligne (le slice reparse num/voie/cp/ville).
        "selarl_adresse_ligne": (
            f"{person['adresse_num_voie']} {person['adresse_voie']}".strip()
            + f", {person['adresse_cp']} {person['adresse_ville']}"
        ),
        "selarl_denomination": f"SELARL {person['nom']}",
        "selarl_capital_social": capital,
        "selarl_nb_parts_total": parts,
        "selarl_ville_rcs": company["ville"],
        # O24-03 : siege sur UNE ligne (le slice reparse num/voie/cp/ville).
        "selarl_siege_ligne": (
            f"{company['numero']} {company['voie']}, {company['cp']} {company['ville']}"
        ),
        "selarl_departement_ordre": company["departement_ordre"],
        # O24-03 : adresse de l'ordre sur UNE ligne (le slice reparse ligne_1/cp/ville).
        "selarl_ordre_adresse_ligne": (
            f"{company['ordre_adresse']}, {company['ordre_cp']} {company['ville']}"
        ),
        "selarl_signature_lieu": company["ville"],
        "selarl_signature_date": today_text,
        "selarl_depot_banque_nom": random.choice(("BNP Paribas", "CIC", "Credit Agricole")),
        "selarl_depot_banque_adresse": company["banque_adresse"],
        "selarl_exercice_debut": "1er janvier",
        "selarl_exercice_fin": "31 décembre",
        "selarl_exercice_cloture_premier": f"31 décembre {date.today().year + 1}",
        "selarl_autre_lieu_exercice": False,
        "selarl_lieu_exercice_adresse": "",
        "selarl_second_lieu_exercice_nom": "",
        "selarl_second_lieu_exercice_adresse": "",
        "selarl_conjoint_civilite": "Madame",
        "selarl_conjoint_prenom": random.choice(("Claire", "Sophie", "Nadia")),
        "selarl_conjoint_nom": person["nom"],
    }
    values.update(_cession_prefill_values(profession_key))
    values.update(_scm_cession_prefill_values(person))
    st.session_state.update(values)
    st.session_state.pop(GENERATED_DOSSIER_STATE_KEY, None)


def _scm_associe_prefill_values(
    index: int,
    *,
    civilite: str,
    prenom: str,
    nom: str,
    ville: str,
    departement: str,
    naissance: str,
    adresse: str,
    apport: str,
    nb: int,
    debut: int,
    fin: int,
) -> dict[str, object]:
    """Cles session_state d'un associe SCM (personne physique) pour le prefill."""
    p = f"scm_associe_{index}"
    # Adresse perso sur UNE ligne (O24-03 : plus de num/voie/cp/ville separes ; le
    # slice reparse en interne). Nationalite deroulant (cle _choice) ; plus de parts
    # debut/fin (derivation cumulative). Profession conservee (SCM, §18.6).
    return {
        f"{p}_type": "personne_physique",
        f"{p}_civilite": civilite,
        f"{p}_prenom": prenom,
        f"{p}_nom": nom,
        f"{p}_date_naissance": naissance,
        f"{p}_ville_naissance": ville,
        f"{p}_departement_naissance": departement,
        f"{p}_nationalite_choice": "Française",
        f"{p}_situation_maritale": "celibataire",
        f"{p}_profession": "Medecin",
        f"{p}_adresse": adresse,
        # DNC par associe (Rafael 2026-07-09) : filiation requise pour CHAQUE associe.
        f"{p}_sig_nom_pere": f"Pierre {nom}",
        f"{p}_sig_nom_mere": f"Anne {nom}",
        f"{p}_apport_montant": apport,
        f"{p}_nb_titres": nb,
    }


def _prefill_scm_test_data() -> None:
    """Pre-remplit un dossier SCM de creation FICTIF et coherent (2 associes medecins).

    Donnees d'exemple uniquement (aucune donnee reelle). Somme des parts = total.
    """
    values: dict[str, object] = {
        "scm_denomination": "SCM DES DOCTEURS EXEMPLE",
        "scm_capital_social": 1000,
        "scm_nb_parts_total": 100,
        # O24-03 : siege sur UNE ligne (plus de num/voie/cp/ville separes).
        "scm_siege_adresse": "10 rue de la Paix, 75002 Paris",
        "scm_ville_rcs": "Paris",
        "scm_banque_nom": "BANQUE EXEMPLE",
        "scm_banque_adresse": "1 rue Banque, 75009 Paris",
        "scm_date_cloture_premier_exercice": "31 décembre 2026",
        "scm_signature_date": "15/05/2026",
        "scm_signataire_fonction": "gerant",
        "scm_signataire_titre": "Docteur",
        "scm_ordre_conseil": "Conseil departemental de l'Ordre des medecins",
        "scm_ordre_departement": "75",
        # O24-03 : adresse de l'ordre sur UNE ligne (le slice reparse ligne_1/cp/ville).
        "scm_ordre_adresse": "1 rue de l'Ordre, 75008 Paris",
        "scm_ordre_numero": "ORD-12345",
        "scm_nb_associes": 2,
        # Satellites SCM (pacte + liste depenses, generes a 2 associes).
        "scm_pacte_ville_tribunal": "Paris",
        "scm_societe_numero_rcs": "en cours de constitution",
        # Documents inter-SEL (R22-03/04) : contrat de frais communs + reglement interieur.
        # Actifs par defaut ; donnees FICTIVES de la SEL de chaque praticien + parametres.
        "scm_inter_sel_active": True,
        "scm_inter_sel_forme": "SELARL",
        "scm_inter_sel_titre": "Docteur",
        "scm_inter_sel_1_denomination": "SELARL DOCTEUR DURAND",
        "scm_inter_sel_1_capital": "1 000 euros",
        "scm_inter_sel_1_siege": "1 rue Exemple, 75000 Paris",
        "scm_inter_sel_1_ville_rcs": "Paris",
        "scm_inter_sel_1_numero_rcs": "900 000 011",
        "scm_inter_sel_1_telephone": "01 00 00 00 01",
        "scm_inter_sel_2_denomination": "SELARL DOCTEUR MARTIN",
        "scm_inter_sel_2_capital": "1 000 euros",
        "scm_inter_sel_2_siege": "2 rue Exemple, 69000 Lyon",
        "scm_inter_sel_2_ville_rcs": "Lyon",
        "scm_inter_sel_2_numero_rcs": "900 000 012",
        "scm_inter_sel_2_telephone": "04 00 00 00 02",
        "scm_inter_sel_locaux": "10 rue de la Paix, 75002 Paris",
        "scm_inter_sel_date_effet": "1er janvier 2027",
        "scm_inter_sel_seuil": "1 500 euros",
        "scm_inter_sel_annee_ref": "2027",
        "scm_inter_sel_date_fin_gestion": "31 décembre 2027",
        "scm_inter_sel_date_attribution": "1er janvier",
    }
    values.update(
        _scm_associe_prefill_values(
            0,
            civilite="Monsieur",
            prenom="Jean",
            nom="Durand",
            ville="Paris",
            departement="75",
            naissance="1 janvier 1980",
            adresse="1 rue Exemple, 75000 Paris",
            apport="700",
            nb=70,
            debut=1,
            fin=70,
        )
    )
    values.update(
        _scm_associe_prefill_values(
            1,
            civilite="Madame",
            prenom="Alice",
            nom="Martin",
            ville="Lyon",
            departement="69",
            naissance="2 février 1982",
            adresse="2 rue Exemple, 69000 Lyon",
            apport="300",
            nb=30,
            debut=71,
            fin=100,
        )
    )
    values.update(_civil_gerant_dnc_prefill("scm", 0))
    st.session_state.update(values)
    st.session_state.pop(GENERATED_DOSSIER_STATE_KEY, None)


def _civil_gerant_dnc_prefill(prefix: str, index: int) -> dict[str, object]:
    """Coche l'associe `index` comme gerant + sa DNC (filiation/adresse), saisies
    sous lui (reunion 2026-06-09). Donnees fictives. Le gerant designe alimente
    les cles signataire_* via _collect_gerant_sig."""
    # Adresse du gerant : plus saisie ici (§18.5), reprise de l'adresse personnelle
    # de l'associe. On ne pose que la filiation + la case dirigeant.
    p = f"{prefix}_associe_{index}"
    return {
        f"{p}_is_dirigeant": True,
        f"{p}_sig_nom_pere": "Pierre Durand",
        f"{p}_sig_nom_mere": "Anne Durand",
    }


def _civil_society_prefill(
    prefix: str,
    *,
    denomination: str,
    forme_sociale: str,
) -> dict[str, object]:
    """Cles societe + documents communs (hors identite du gerant) pour un dossier
    civil de test (fictif). La filiation/adresse du gerant est saisie sous lui."""
    # forme_sociale derivee (§18.1), valeur nominale calculee (§18.2), duree figee
    # (§18.3), lieu de signature = ville siege (§18.4) : ces champs ne sont plus des
    # widgets saisis -> plus de cle de prefill pour eux.
    del forme_sociale
    return {
        f"{prefix}_denomination": denomination,
        f"{prefix}_capital_social": 1000,
        f"{prefix}_nb_parts_total": 100,
        # O24-03 : siege sur UNE ligne (plus de num/voie/cp/ville separes).
        f"{prefix}_siege_adresse": "10 rue de la Paix, 75002 Paris",
        f"{prefix}_ville_rcs": "Paris",
        f"{prefix}_banque_nom": "BANQUE EXEMPLE",
        f"{prefix}_banque_adresse": "1 rue Banque, 75009 Paris",
        f"{prefix}_date_cloture_premier_exercice": "31 décembre 2026",
        f"{prefix}_signature_date": "15/05/2026",
        f"{prefix}_signataire_fonction": "gerant",
        f"{prefix}_signataire_titre": "Docteur",
    }


def _civil_pp_associe_prefill(
    prefix: str,
    index: int,
    *,
    civilite: str,
    prenom: str,
    nom: str,
    ville: str,
    departement: str,
    naissance: str,
    adresse: str,
    apport: str,
    nb: int,
    debut: int,
    fin: int,
    role: str | None = None,
) -> dict[str, object]:
    p = f"{prefix}_associe_{index}"
    # Adresse perso sur UNE ligne (O24-03 : plus de num/voie/cp/ville separes ; le
    # slice reparse en interne). parts debut/fin ne sont plus saisis (derivation
    # cumulative). Nationalite = deroulant (cle _choice).
    values: dict[str, object] = {
        f"{p}_type": "personne_physique",
        f"{p}_civilite": civilite,
        f"{p}_prenom": prenom,
        f"{p}_nom": nom,
        f"{p}_date_naissance": naissance,
        f"{p}_ville_naissance": ville,
        f"{p}_departement_naissance": departement,
        f"{p}_nationalite_choice": "Française",
        f"{p}_situation_maritale": "celibataire",
        f"{p}_profession": "Medecin",
        f"{p}_adresse": adresse,
        # DNC par associe (Rafael 2026-07-09) : filiation requise pour CHAQUE associe.
        f"{p}_sig_nom_pere": f"Pierre {nom}",
        f"{p}_sig_nom_mere": f"Anne {nom}",
        f"{p}_apport_montant": apport,
        f"{p}_nb_titres": nb,
    }
    if role is not None:
        values[f"{p}_role"] = role
    return values


def _civil_pm_associe_prefill(
    prefix: str,
    index: int,
    *,
    denomination: str,
    forme_juridique: str,
    capital: str,
    siege: str,
    numero_rcs: str,
    ville_rcs: str,
    rep_prenom: str,
    rep_nom: str,
    apport: str,
    nb: int,
    debut: int,
    fin: int,
) -> dict[str, object]:
    # Profession PM : widget SCM uniquement (§18.6) ; parts debut/fin derivees (§18.5).
    p = f"{prefix}_associe_{index}"
    values: dict[str, object] = {
        f"{p}_type": "personne_morale",
        f"{p}_denomination": denomination,
        f"{p}_forme_juridique": forme_juridique,
        f"{p}_capital_social": capital,
        f"{p}_siege": siege,
        f"{p}_numero_rcs": numero_rcs,
        f"{p}_ville_rcs": ville_rcs,
        f"{p}_rep_civilite": "Monsieur",
        f"{p}_rep_prenom": rep_prenom,
        f"{p}_rep_nom": rep_nom,
        f"{p}_rep_fonction": "gerant",
        f"{p}_apport_montant": apport,
        f"{p}_nb_titres": nb,
    }
    if prefix == "scm":
        values[f"{p}_profession"] = "Medecin"
    return values


def _commit_civil_prefill(values: dict[str, object]) -> None:
    st.session_state.update(values)
    st.session_state.pop(GENERATED_DOSSIER_STATE_KEY, None)


def _option_is_prefill(prefix: str) -> dict[str, object]:
    """Active l'option IS + le centre des impots (lettre DOC-022) dans les donnees de test.

    R22-05 (Rafael 2026-06-22) : la lettre d'option IS existe deja pour SCI / SCI IRIS mais
    n'etait pas demontree au bouton de test -> Rafael ne la voyait pas. On l'active ici. Le
    « Centre » n'est plus saisi (R22-07 : fige a « Centre des Finances Publiques »).
    """
    return {
        f"{prefix}_option_is": True,
        f"{prefix}_siren": "900 000 001",
        f"{prefix}_impots_service": "Service des impots des entreprises de Paris 8e",
        f"{prefix}_impots_adresse_ligne_1": "6 rue Paul Baudry",
        f"{prefix}_impots_adresse_ligne_2": "TSA 00001",
        # A7 (Albane 2026-07-09) : CP + Ville regroupes sur UNE ligne (`{prefix}_impots_cp_ville`) ;
        # l'ancienne saisie separee impots_cp / impots_ville n'existe plus au front.
        f"{prefix}_impots_cp_ville": "75008 Paris",
    }


def _prefill_sci_test_data() -> None:
    """SCI de creation fictive (2 associes physiques) + option IS (lettre DOC-022)."""
    values = _civil_society_prefill(
        "sci", denomination="SCI EXEMPLE", forme_sociale="societe civile immobiliere"
    )
    values["sci_nb_associes"] = 2
    values.update(_option_is_prefill("sci"))
    values.update(
        _civil_pp_associe_prefill(
            "sci", 0, civilite="Monsieur", prenom="Jean", nom="Durand", ville="Paris",
            departement="75", naissance="1 janvier 1980",
            adresse="1 rue Exemple, 75000 Paris", apport="400", nb=40, debut=1, fin=40,
        )
    )
    values.update(
        _civil_pp_associe_prefill(
            "sci", 1, civilite="Madame", prenom="Alice", nom="Martin", ville="Lyon",
            departement="69", naissance="2 février 1982",
            adresse="2 rue Exemple, 69000 Lyon", apport="600", nb=60, debut=41, fin=100,
        )
    )
    values.update(_civil_gerant_dnc_prefill("sci", 0))
    _commit_civil_prefill(values)


def _prefill_micro_holding_test_data() -> None:
    """Micro holding de creation fictive (1 associe physique = gerant) + option IS.

    Micro holding = societe civile A CAPITAL VARIABLE (Albane 2026-06-26), 1 associe
    minimum. Route 100 % vers le socle civil (`civil_statuts_slice`), prefixe
    « micro_holding ». L'associe unique est aussi le gerant. Le capital variable +
    la valeur nominale + la forme sociale sont DERIVES par le slice (pas de cle de
    prefill dediee) : on ne pose que les cles societe + l'associe + sa DNC de gerant.
    """
    values = _civil_society_prefill(
        "micro_holding",
        denomination="MICRO HOLDING EXEMPLE",
        forme_sociale="societe civile",
    )
    # 1 seul associe (societe civile a capital variable, 1..6 ; min = 1 pour micro holding).
    values["micro_holding_nb_associes"] = 1
    values.update(_option_is_prefill("micro_holding"))
    values.update(
        _civil_pp_associe_prefill(
            "micro_holding", 0, civilite="Monsieur", prenom="Jean", nom="Durand",
            ville="Paris", departement="75", naissance="1 janvier 1980",
            adresse="1 rue Exemple, 75000 Paris", apport="1000", nb=100, debut=1, fin=100,
        )
    )
    # L'associe unique (index 0) est aussi le gerant : on coche la case + sa DNC.
    values.update(_civil_gerant_dnc_prefill("micro_holding", 0))
    _commit_civil_prefill(values)


def _prefill_sci_iris_test_data() -> None:
    """SCI IRIS de creation fictive (1 societe associee + 1 associe physique)."""
    values = _civil_society_prefill(
        "sci_iris", denomination="SCI IRIS EXEMPLE",
        forme_sociale="societe civile immobiliere",
    )
    values["sci_iris_nb_associes"] = 2
    values.update(_option_is_prefill("sci_iris"))
    values.update(
        _civil_pm_associe_prefill(
            "sci_iris", 0, denomination="SEL EXEMPLE", forme_juridique="SELARL",
            capital="1 000 euros", siege="2 rue Pro, 75000 Paris",
            numero_rcs="900 000 001", ville_rcs="Paris", rep_prenom="Jean", rep_nom="Durand",
            apport="400", nb=40, debut=1, fin=40,
        )
    )
    values.update(
        _civil_pp_associe_prefill(
            "sci_iris", 1, civilite="Madame", prenom="Alice", nom="Martin", ville="Lyon",
            departement="69", naissance="2 février 1982",
            adresse="2 rue Exemple, 69000 Lyon", apport="600", nb=60, debut=41, fin=100,
        )
    )
    # Gerant SCI IRIS = associe physique (index 1 ; l'associe 0 est la personne morale).
    values.update(_civil_gerant_dnc_prefill("sci_iris", 1))
    _commit_civil_prefill(values)


def _prefill_scs_test_data() -> None:
    """SCS de creation fictive (1 commandite + 1 commanditaire)."""
    values = _civil_society_prefill(
        "scs", denomination="SCS EXEMPLE", forme_sociale="societe en commandite simple"
    )
    values["scs_nb_associes"] = 2
    values.update(
        _civil_pp_associe_prefill(
            "scs", 0, civilite="Monsieur", prenom="Jean", nom="Durand", ville="Paris",
            departement="75", naissance="1 janvier 1980",
            adresse="1 rue Exemple, 75000 Paris", apport="600", nb=60, debut=1, fin=60,
            role="commandite",
        )
    )
    values.update(
        _civil_pp_associe_prefill(
            "scs", 1, civilite="Madame", prenom="Alice", nom="Martin", ville="Lyon",
            departement="69", naissance="2 février 1982",
            adresse="2 rue Exemple, 69000 Lyon", apport="400", nb=40, debut=61, fin=100,
            role="commanditaire",
        )
    )
    # Gerant SCS = le commandite (associe 0).
    values.update(_civil_gerant_dnc_prefill("scs", 0))
    _commit_civil_prefill(values)


def _prefill_sas_test_data() -> None:
    """SAS (SPFPL medecins) de creation fictive — actionnaire unique masculin (V1)."""
    values: dict[str, object] = {
        "sas_denomination": "SPFPL MARTIN",
        # O24-03 : siege sur UNE ligne (le slice reparse num/voie/cp/ville).
        "sas_siege": "10 rue de la Paix, 75002 Paris",
        "sas_capital_social": 12000,
        "sas_nb_actions_total": 120,
        "sas_valeur_nominale_action": "100",
        "sas_apports_nature_montant": "10000",
        "sas_apports_numeraire_montant": "2000",
        "sas_civilite": "Monsieur",
        "sas_prenom": "Camille",
        "sas_nom": "Martin",
        "sas_genre_label": "Monsieur",
        "sas_qualification_principale": "Medecin cardiologue",
        # #8 : la date ISO de la DNC est derivee de cette UNIQUE date verbatim (parsable).
        "sas_date_naissance": "2 janvier 1980",
        "sas_ville_naissance": "Paris",
        "sas_departement_naissance": "75",
        "sas_nationalite_choice": "Française",
        "sas_regime_matrimonial": "la communaute legale",
        # O24-03 : adresse perso sur UNE ligne (le slice reparse num/voie/cp/ville).
        "sas_adresse": "5 rue Royale, 75008 Paris",
        "sas_nom_pere": "Pierre Martin",
        "sas_nom_mere": "Anne Martin",
        "sas_conjoint_civilite": "Madame",
        "sas_conjoint_prenom": "Alice",
        "sas_conjoint_nom": "Martin",
        "sas_ordre_departement": "Paris",
        "sas_numero_ordre": "12345",
        "sas_numero_rpps": "10000000001",
        "sas_cible_denomination": "SELARL CABINET MARTIN",
        "sas_cible_forme": "SELARL",
        "sas_cible_siege": "12 avenue des Ternes, 75017 Paris",
        "sas_cible_ville_rcs": "Paris",
        "sas_cible_numero_rcs": "900 000 001",
        "sas_apport_nb_parts": 50,
        "sas_banque_nom": "BANQUE EXEMPLE",
        "sas_signature_lieu": "Paris",
        "sas_exercice_debut": "1er janvier",
        "sas_exercice_fin": "31 décembre",
        "sas_date_cloture": "31 décembre 2026",
        "sas_signature_date": "14/05/2026",
    }
    _commit_civil_prefill(values)


def _prefill_sasu_holding_test_data() -> None:
    """SASU Holding de creation fictive (associe unique = president) — slice dedie.

    SASU Holding = SAS UNIPERSONNELLE generaliste (holding patrimoniale, PAS de
    profession reglementee), prefixe « sasu_holding ». Un clic = dossier coherent et
    generable (bundle 6 pieces : statuts + tronc commun + PV remuneration president +
    liste des souscripteurs). Capital == nb_actions * valeur nominale (1000 € / 100
    actions). Certaines cles (exercice, cloture, lieu de signature) sont aussi
    auto-seedees par le slice ; on les fixe quand meme pour la coherence du prefill.
    """
    p = "sasu_holding"
    values: dict[str, object] = {
        f"{p}_denomination": "SASU HOLDING EXEMPLE",
        f"{p}_forme_sociale": "Société par actions simplifiée unipersonnelle",
        # Siege sur UNE ligne (le slice reparse num/voie/cp/ville pour domiciliation/procuration).
        f"{p}_siege": "10 rue de la Paix, 75002 Paris",
        # Capital = number_input -> ENTIER (1000 € = 100 actions x 10 €).
        f"{p}_capital_social": 1000,
        f"{p}_nb_actions": 100,
        # Associe unique = president.
        f"{p}_civilite": "Monsieur",  # selectbox (Monsieur / Madame)
        f"{p}_prenom": "Jean",
        f"{p}_nom": "Durand",
        # Date de naissance : champ texte verbatim francais (re-accentue en aval).
        # #8 : la date ISO de la DNC est derivee de cette UNIQUE date verbatim (parsable).
        f"{p}_date_naissance": "2 janvier 1980",
        f"{p}_ville_naissance": "Paris",
        f"{p}_nationalite_choice": NATIONALITY_PRESETS[0],  # selectbox nationalite
        # Adresse perso sur UNE ligne (le slice reparse num/voie/cp/ville pour la DNC).
        f"{p}_adresse": "5 rue Royale, 75008 Paris",
        f"{p}_nom_pere": "Pierre Durand",
        f"{p}_nom_mere": "Anne Durand",
        # Depot / exercice / signature.
        f"{p}_banque_nom": "BANQUE EXEMPLE",
        f"{p}_signature_lieu": "Paris",
        f"{p}_exercice_debut": "1er janvier",
        f"{p}_exercice_fin": "31 décembre",
        f"{p}_date_cloture": f"31 décembre {date.today().year + 1}",
        f"{p}_signature_date": "15/05/2026",  # parse -> date
    }
    _commit_civil_prefill(values)


def _spfpl_prefill_values(prefix: str) -> dict[str, object]:
    """Dossier SPFPL de creation fictif (associe unique medecin), prefixe par parcours."""
    return {
        f"{prefix}_denomination": "SPFPL MARTIN",
        # O24-03 : siege sur UNE ligne (le slice reparse num/voie/cp/ville).
        f"{prefix}_siege": "10 rue de la Paix, 75002 Paris",
        f"{prefix}_capital_social": 60000,
        # Nombre d'actions VARIABLE (defaut 600) ; la valeur nominale est calculee
        # (60000 / 600 = 100) et affichee en lecture seule, plus de saisie libre.
        f"{prefix}_nb_actions_total": 600,
        f"{prefix}_ville_rcs": "Paris",
        # §14.2 : la civilite SPFPL est desormais la civilite CIVILE (M./Mme) ; le
        # titre « Docteur » est applique automatiquement (plus de selecteur
        # « Docteur » ni de selecteur « Genre civil » redondant).
        f"{prefix}_civilite": "Monsieur",
        f"{prefix}_prenom": "Camille",
        f"{prefix}_prenoms": "Camille Andre",
        f"{prefix}_nom": "Martin",
        f"{prefix}_date_naissance": "02/01/1980",
        f"{prefix}_ville_naissance": "Paris",
        f"{prefix}_departement_naissance": "75",
        f"{prefix}_nationalite_choice": "Française",
        f"{prefix}_regime_matrimonial": "la communaute legale",
        # O24-03 : adresse perso sur UNE ligne (le slice reparse num/voie/cp/ville).
        f"{prefix}_adresse": "5 rue Royale, 75008 Paris",
        f"{prefix}_nom_pere": "Pierre Martin",
        f"{prefix}_nom_mere": "Anne Martin",
        f"{prefix}_conjoint_civilite": "Madame",
        f"{prefix}_conjoint_prenom": "Alice",
        f"{prefix}_conjoint_nom": "Martin",
        f"{prefix}_ordre_departement": "Paris",
        f"{prefix}_numero_ordre": "12345",
        f"{prefix}_numero_rpps": "10000000001",
        f"{prefix}_ordre_conseil": "Conseil departemental",
        # O24-03 : adresse de l'ordre sur UNE ligne (le slice reparse ligne_1/cp/ville).
        f"{prefix}_ordre_adresse": "1 rue de l'Ordre, 75008 Paris",
        f"{prefix}_banque_nom": "BANQUE EXEMPLE",
        f"{prefix}_banque_adresse": "1 boulevard Haussmann, 75009 Paris",
        f"{prefix}_apport_montant": "60000",
        f"{prefix}_apport_nb_parts": 60,
        f"{prefix}_apport_plage": "41 a 100",
        # Fusion Rafael 2026-07-07 : « Valeur globale apportee » n'est plus saisie
        # (derivee de « Montant de l'apport ») ; « Siege cible (affiche) » supprime
        # (cession : sous-formulaire ; apport : ligne unique `*_cible_siege_cession`
        # seedee plus bas) -> plus de prefill de cles de widgets disparus.
        f"{prefix}_cible_denomination": "SELARL CABINET MARTIN",
        f"{prefix}_cible_ville_rcs": "Paris",
        f"{prefix}_cible_numero_rcs": "900 000 001",
        # Operation cession (DOC-037 note + DOC-038/039 PV + DOC-040 acte) :
        # repartition de la cible + prix + siege structure. 1 associe cible -> PV unique.
        f"{prefix}_cession_nb_parts_cedees": 60,
        f"{prefix}_cession_prix_unitaire": "1000",
        # Retour Albane 2026-07-07 : plus de prefill « plage cedee » / « parts apres » /
        # « plage » par associe — ces champs ne se saisissent plus (valeurs DERIVEES).
        f"{prefix}_cible_forme_complete": "societe d'exercice liberal a responsabilite limitee",
        # O24-03 : siege de la cible (cession) sur UNE ligne (le slice reparse les composants).
        f"{prefix}_cible_siege_cession": "12 avenue des Ternes, 75017 Paris",
        f"{prefix}_cession_nb_associes": 1,
        f"{prefix}_cession_assoc_0_civ": "Madame",
        f"{prefix}_cession_assoc_0_prenom": "Camille",
        f"{prefix}_cession_assoc_0_nom": "Martin",
        f"{prefix}_cession_assoc_0_avant": 100,
        f"{prefix}_cible_forme": "SELARL",
        f"{prefix}_cible_profession": "chirurgien-dentiste",
        f"{prefix}_cible_capital": "10000",
        f"{prefix}_cible_nb_parts": 100,
        f"{prefix}_cible_valeur_part": "100",
        # Operation apport (DOC-041 contrat + DOC-042/043 attestations) : detail
        # des titres apportes + organes de controle (commissaire + evaluateur).
        f"{prefix}_apport_nature_titres": "parts sociales",
        f"{prefix}_apport_valeur_par_titre": "1000",
        f"{prefix}_commissaire_denomination": "CAA EXPERTISE",
        f"{prefix}_commissaire_forme": "SAS",
        f"{prefix}_commissaire_capital": "1 000 euros",
        f"{prefix}_commissaire_siege": "1 rue Scheffer, 75016 Paris",
        f"{prefix}_commissaire_ville_rcs": "Paris",
        f"{prefix}_commissaire_numero_rcs": "948 483 730",
        f"{prefix}_commissaire_rep_civilite": "Monsieur",
        f"{prefix}_commissaire_rep_prenom": "Nabil",
        f"{prefix}_commissaire_rep_nom": "Saidi",
        f"{prefix}_evaluateur_denomination": "EVAL CONSEIL",
        f"{prefix}_evaluateur_forme": "SAS",
        f"{prefix}_evaluateur_capital": "1 000 euros",
        f"{prefix}_evaluateur_siege": "1 rue Scheffer, 75016 Paris",
        f"{prefix}_evaluateur_ville_rcs": "Paris",
        f"{prefix}_evaluateur_numero_rcs": "948 483 730",
        f"{prefix}_evaluateur_rep_civilite": "Madame",
        f"{prefix}_evaluateur_rep_prenom": "Eva",
        f"{prefix}_evaluateur_rep_nom": "Lemoine",
        f"{prefix}_exercice_debut": "1er janvier",
        f"{prefix}_exercice_fin": "31 décembre",
        f"{prefix}_date_cloture": "31 décembre 2026",
        f"{prefix}_signature_lieu": "Paris",
        f"{prefix}_signature_date": "14/05/2026",
    }


def _prefill_spfpl_cession_test_data() -> None:
    values = _spfpl_prefill_values("spfpl_cession")
    # Retour Albane 2026-07-07 : « Plage de parts » est un champ APPORT uniquement
    # (retire du parcours cession, ou la plage cedee est derivee) -> pas de prefill
    # d'une cle de widget qui n'existe plus sur ce parcours.
    values.pop("spfpl_cession_apport_plage")
    _commit_civil_prefill(values)


def _prefill_spfpl_apport_test_data() -> None:
    _commit_civil_prefill(_spfpl_prefill_values("spfpl_apport"))


def _selas_associe_prefill(
    index: int,
    *,
    civilite: str,
    prenoms: str,
    nom: str,
    ville: str,
    departement: str,
    nationalite_ordre: str,
    numero_ordre: str,
    numero_rpps: str,
    qualite: str,
    nb_actions: int,
    apport: str,
) -> dict[str, object]:
    p = f"selas_associe_{index}"
    return {
        f"{p}_type": "personne_physique",
        f"{p}_nb_actions": nb_actions,
        f"{p}_montant": apport,
        f"{p}_civilite": civilite,
        f"{p}_prenoms": prenoms,
        f"{p}_nom": nom,
        f"{p}_date_naissance": "1 janvier 1980",
        f"{p}_ville_naissance": ville,
        f"{p}_departement": departement,
        f"{p}_nationalite": "francaise",
        f"{p}_adresse": f"10 rue Exemple, {departement}000 {ville}",
        f"{p}_situation": "Célibataire",
        f"{p}_qualification": "Medecin generaliste",
        f"{p}_ordre_dep": nationalite_ordre,
        f"{p}_numero_ordre": numero_ordre,
        f"{p}_numero_rpps": numero_rpps,
        f"{p}_qualite": qualite,
        # DNC par associe (Rafael 2026-07-09) : filiation requise pour CHAQUE associe.
        f"{p}_sig_nom_pere": f"Pierre {nom}",
        f"{p}_sig_nom_mere": f"Anne {nom}",
    }


def _prefill_selas_test_data(
    profession: str = "médecin", profession_pluriel: str = "médecins"
) -> None:
    """SELAS multi de creation fictive (2 associes exercants, somme = total).

    La profession est parametrable : « médecin » par defaut (SELAS multi), ou
    « chirurgien-dentiste » pour le cas nomme SELAS dentiste pluripersonnelle —
    de sorte que les donnees de test basculent le moteur sur le bon corpus.
    R1 (2026-06-18) : la profession est desormais un menu deroulant ferme cote
    formulaire (cle `selas_profession_choice`) ; on seed cette cle pour rester
    coherent (la valeur DOIT etre une option exacte du menu)."""
    values: dict[str, object] = {
        "selas_denomination": "SELAS EXEMPLE",
        "selas_siege_adresse": "5 place du Centre, 69000 Lyon",
        "selas_profession_choice": profession,
        # Capital = number_input cote SELAS (parite gold) -> seed un ENTIER, pas une
        # chaine (sinon le widget number_input leve).
        "selas_capital_social": 1000,
        "selas_nb_actions_total": 100,
        "selas_valeur_nominale_action": "10",
        "selas_ville_rcs": "Lyon",
        "selas_adresse_lieu_exercice": "5 place du Centre, 69000 Lyon",
        "selas_banque_nom": "BANQUE EXEMPLE",
        "selas_banque_adresse": "1 rue Banque, 69009 Lyon",
        "selas_date_cloture": "31 décembre 2026",
        "selas_signature_lieu": "Lyon",
        "selas_signature_date": "15/05/2026",
        # DNC + identite du dirigeant : saisies SOUS l'associe coche dirigeant
        # (associe 0). La nationalite / le titre derivent de l'associe lui-meme.
        # DNC + identite du dirigeant : adresse et date sont reprises de l'associe
        # (saisies une seule fois, #8 / B4) ; seule la filiation reste propre ici.
        "selas_associe_0_is_dirigeant": True,
        "selas_associe_0_sig_nom_pere": "Pierre Durand",
        "selas_associe_0_sig_nom_mere": "Anne Durand",
        # R5/R6 (2026-06-18) : « Conseil departemental » retire du formulaire ;
        # le connecteur grammatical (« de » / « du ») le remplace pour l'accord.
        "selas_ordre_departement": "Rhone",
        "selas_ordre_connecteur": "du",
        "selas_ordre_adresse": "1 rue de l'Ordre, 69002 Lyon",  # O24-03 : ordre sur une ligne
        "selas_ordre_numero": "69-12345",
        "selas_nb_associes": 2,
    }
    values.update(
        _selas_associe_prefill(
            0, civilite="Monsieur", prenoms="Jean", nom="Durand", ville="Lyon",
            departement="69", nationalite_ordre="Rhone", numero_ordre="69-12345",
            numero_rpps="10100000001", qualite="associe exercant", nb_actions=60, apport="600",
        )
    )
    values.update(
        _selas_associe_prefill(
            1, civilite="Madame", prenoms="Alice", nom="Martin", ville="Paris",
            departement="75", nationalite_ordre="Paris", numero_ordre="75-67890",
            numero_rpps="10100000002", qualite="associee exercante", nb_actions=40, apport="400",
        )
    )
    _commit_civil_prefill(values)


def _prefill_selas_uni_medecin_test_data() -> None:
    """Retour Rafael 2026-06-25 (#4) : donnees de test SELAS UNIPERSONNELLE medecin.

    Un clic = dossier SELAS uni coherent et generable (associe unique = President, marie
    sous communaute pour demontrer la clause conjoint + DOC-005/006). Cles = `selas_uni_medecin_*`
    (prefixe du slice). Les dates sont seedees en objets `date` (widgets date_input)."""
    p = "selas_uni_medecin"
    values: dict[str, object] = {
        f"{p}_denomination": "SELAS EXEMPLE",
        f"{p}_capital_social": 1000,  # number_input -> entier
        f"{p}_nb_actions_total": 100,
        f"{p}_ville_rcs": "Lyon",
        f"{p}_lieu_exercice_adresse": "5 place du Centre, 69000 Lyon",
        f"{p}_siege": "5 place du Centre, 69000 Lyon",
        f"{p}_banque_nom": "BANQUE EXEMPLE",
        f"{p}_banque_adresse": "1 rue Banque, 69009 Lyon",
        f"{p}_exercice_debut": "1er janvier",
        f"{p}_exercice_fin": "31 décembre",
        f"{p}_exercice_cloture": "31 décembre 2026",
        f"{p}_civilite": "Monsieur",  # selectbox (Monsieur / Madame)
        f"{p}_prenom": "Jean",
        f"{p}_nom": "Durand",
        f"{p}_date_naissance": date(1980, 1, 1),
        f"{p}_ville_naissance": "Lyon",
        f"{p}_departement_naissance": "69",
        f"{p}_nationalite_choice": NATIONALITY_PRESETS[0],
        f"{p}_titre_affichage": "Docteur",
        f"{p}_adresse": "10 rue Exemple, 69000 Lyon",
        # Marie sous communaute -> demontre la clause conjoint + DOC-005/006.
        f"{p}_situation": MATRIMONIAL_STATUS_MARRIED_COMMUNAUTE,
        f"{p}_conjoint_civilite": "Madame",  # selectbox (Madame / Monsieur)
        f"{p}_conjoint_prenom": "Alice",
        f"{p}_conjoint_nom": "Durand",
        f"{p}_nom_pere": "Pierre Durand",
        f"{p}_nom_mere": "Anne Durand",
        # SU2 : destinataire ordre derive du departement + connecteur (« du Rhone »).
        f"{p}_departement_ordre": "Rhone",
        f"{p}_ordre_connecteur": "du",  # selectbox (de / du / des)
        f"{p}_numero_ordre": "69-12345",
        f"{p}_numero_rpps": "10100000001",
        f"{p}_ordre_adresse": "1 rue de l'Ordre, 69002 Lyon",
        f"{p}_signature_lieu": "Lyon",
        f"{p}_signature_date": date(2026, 5, 15),
    }
    _commit_civil_prefill(values)


def _prefill_selas_uni_dentiste_test_data() -> None:
    """Retour Rafael #5 : donnees de test SELAS UNIPERSONNELLE chirurgien-dentiste.

    Un clic = dossier SELAS uni dentiste coherent et generable (associe unique = President,
    marie sous communaute pour demontrer la clause conjoint + DOC-005/006). Cles =
    `selas_uni_dentiste_*` (prefixe du slice). Calque du prefill SELAS uni medecin."""
    p = "selas_uni_dentiste"
    values: dict[str, object] = {
        f"{p}_denomination": "SELAS EXEMPLE",
        f"{p}_capital_social": 1000,
        f"{p}_nb_actions_total": 100,
        f"{p}_ville_rcs": "Lyon",
        f"{p}_lieu_exercice_adresse": "5 place du Centre, 69000 Lyon",
        f"{p}_siege": "5 place du Centre, 69000 Lyon",
        f"{p}_banque_nom": "BANQUE EXEMPLE",
        f"{p}_banque_adresse": "1 rue Banque, 69009 Lyon",
        f"{p}_exercice_debut": "1er janvier",
        f"{p}_exercice_fin": "31 décembre",
        f"{p}_exercice_cloture": "31 décembre 2026",
        f"{p}_civilite": "Monsieur",
        f"{p}_prenom": "Jean",
        f"{p}_nom": "Durand",
        f"{p}_date_naissance": date(1980, 1, 1),
        f"{p}_ville_naissance": "Lyon",
        f"{p}_departement_naissance": "69",
        f"{p}_nationalite_choice": NATIONALITY_PRESETS[0],
        f"{p}_titre_affichage": "Docteur",
        f"{p}_adresse": "10 rue Exemple, 69000 Lyon",
        f"{p}_situation": MATRIMONIAL_STATUS_MARRIED_COMMUNAUTE,
        f"{p}_conjoint_civilite": "Madame",
        f"{p}_conjoint_prenom": "Alice",
        f"{p}_conjoint_nom": "Durand",
        f"{p}_nom_pere": "Pierre Durand",
        f"{p}_nom_mere": "Anne Durand",
        f"{p}_departement_ordre": "Rhone",
        f"{p}_ordre_connecteur": "du",
        f"{p}_numero_ordre": "69-12345",
        f"{p}_numero_rpps": "10100000001",
        f"{p}_ordre_adresse": "1 rue de l'Ordre, 69002 Lyon",
        f"{p}_signature_lieu": "Lyon",
        f"{p}_signature_date": date(2026, 5, 15),
    }
    _commit_civil_prefill(values)


# Boutons "donnees de test" par type (calques sur le bouton SELARL). Etendu type
# par type au fur et a mesure de la validation.
_TYPED_TEST_DATA_PREFILL = {
    "SCM": _prefill_scm_test_data,
    "SCI": _prefill_sci_test_data,
    "SCI IRIS": _prefill_sci_iris_test_data,
    "SCS": _prefill_scs_test_data,
    # Micro holding (Albane 2026-06-26) : societe civile a capital variable, socle civil.
    "MICRO_HOLDING": _prefill_micro_holding_test_data,
    "SAS": _prefill_sas_test_data,
    # SASU Holding (Albane 2026-06-29) : SAS unipersonnelle generaliste, slice dedie.
    "SASU_HOLDING": _prefill_sasu_holding_test_data,
    "SPFPL cession": _prefill_spfpl_cession_test_data,
    "SPFPL apport": _prefill_spfpl_apport_test_data,
    "SELAS": _prefill_selas_test_data,
    # Retour Rafael 2026-06-25 (#4) : bouton donnees de test SELAS unipersonnelle medecin.
    "SELAS uni medecin": _prefill_selas_uni_medecin_test_data,
    # Retour Rafael #5 : bouton donnees de test SELAS unipersonnelle dentiste.
    "SELAS uni dentiste": _prefill_selas_uni_dentiste_test_data,
}

# Prefill surchargeant le defaut par structure pour une cle de type precise.
# Retours Rafael 2026-06-23 : le cas SELAS pluripersonnelle unique (cle
# `selas_multi_v1`) utilise le prefill SELAS par defaut (medecin) ; la profession
# (dont chirurgien-dentiste) se choisit dans le formulaire. Plus de surcharge par cle.
_TYPED_TEST_DATA_PREFILL_BY_KEY: dict[str, object] = {}


def _cession_prefill_values(profession: str) -> dict[str, object]:
    """Cles du sous-formulaire cession (donnees de test FICTIVES, nouvelles cles).

    Le vendeur et l'acquereur sont repris automatiquement du dossier : seuls les
    champs specifiques a la cession sont preremplis ici. Un clic = cession
    testable et generable.
    """
    dentaire = profession == PROFESSION_DENTISTE
    year = date.today().year
    values: dict[str, object] = {
        "selarl_cession_meta_type_cabinet": "dentaire" if dentaire else "medical",
        "selarl_cession_meta_etape": "acte",
        "selarl_cession_vendeur_auto": True,
        "selarl_cession_vendeur_siren": "123 456 789",
        "selarl_cession_acquereur_numero_rcs": "900 000 001",
        "selarl_cession_acquereur_numero_siret": "900 000 001 00012",
        # Adresse cabinet : laissee vide -> reprise du siege social au rendu.
        "selarl_cession_cabinet_adresse": "",
        "selarl_cession_cabinet_telephone": "01 44 00 00 00",
        "selarl_cession_cabinet_origine_date": "01/01/2020",
        "selarl_cession_bail_date_bail": "01/09/2021",
        "selarl_cession_bail_date_effet": "01/09/2021",
        "selarl_cession_bail_duree": "six années",
        "selarl_cession_bail_loyer": "2 000",
        "selarl_cession_bail_descriptif": (
            "Les locaux sont composés d'une pièce principale de 80 m² avec "
            "jouissance de la salle d'attente et des toilettes."
        ),
        "selarl_cession_prix_total": "300 000",
        "selarl_cession_prix_total_lettres": "",
        "selarl_cession_prix_corporels": "50 000",
        "selarl_cession_prix_incorporels": "250 000",
        # §12.1 : champ « Banque » retire du questionnaire d'appel de fonds (nom
        # inconnu au remplissage) -> plus de seed de test pour cette cle.
        "selarl_cession_financement_destinataire_civilite": "Monsieur",
        "selarl_cession_financement_destinataire_prenom": "Louis",
        "selarl_cession_financement_destinataire_nom": "Bernard",
        "selarl_cession_financement_deblocage": "240 000",
        "selarl_cession_bailleur_civilite": "Monsieur",
        "selarl_cession_bailleur_prenom": "Paul",
        "selarl_cession_bailleur_nom": "Leroy",
        "selarl_cession_bailleur_adresse": "8 rue Victor Hugo, 69002 Lyon",
    }
    for index in range(3):
        values[f"selarl_cession_exercice_{index}_periode"] = str(year - 3 + index)
        values[f"selarl_cession_exercice_{index}_ca"] = f"2{index}0 000"
        values[f"selarl_cession_exercice_{index}_resultat"] = f"8{index} 000"
    if dentaire:
        values.update(
            {
                "selarl_cession_cabinet_precedent_civilite": "Monsieur",
                "selarl_cession_cabinet_precedent_prenom": "Henri",
                "selarl_cession_cabinet_precedent_nom": "Petit",
                "selarl_cession_cabinet_origine_prix": "150 000",
                "selarl_cession_salaries_aucun": False,
                "selarl_cession_salaries_nb": 2,
                "selarl_cession_salarie_0_civilite": "Madame",
                "selarl_cession_salarie_0_prenom": "Lea",
                "selarl_cession_salarie_0_nom": "Petit",
                "selarl_cession_salarie_0_poste": "assistante dentaire",
                "selarl_cession_salarie_1_civilite": "Monsieur",
                "selarl_cession_salarie_1_prenom": "Noe",
                "selarl_cession_salarie_1_nom": "Robert",
                "selarl_cession_salarie_1_poste": "",
            }
        )
    else:
        values.update(
            {
                "selarl_cession_cabinet_origine_mode": "Cabinet cree par le vendeur",
                "selarl_cession_financement_credit_actif": True,
                "selarl_cession_financement_credit_montant": "60 000",
                "selarl_cession_financement_credit_duree": "trois",
                "selarl_cession_financement_credit_taux": "5",
                "selarl_cession_financement_credit_majoration": "2",
                "selarl_cession_scm_clause_actif": True,
                "selarl_cession_financement_scm_parts": "10",
                "selarl_cession_acquereur_date_immatriculation": "15/01/2026",
                "selarl_cession_acquereur_date_inscription_ordre": "01/02/2026",
            }
        )
    return values


def _scm_cession_prefill_values(person: dict[str, str]) -> dict[str, object]:
    """Cles `selarl_cession_scm_*` : fixture SCM + cedant = la personne de test.

    §4.1 : prefill aussi le repeater des associes PRESENTS (3 par defaut, total
    cohérent avec le capital de la SCM) dont le cedant = la personne de test, plus
    le nombre de parts cedees. L'apres-cession est derive deterministe a la
    generation (cedant reduit + SEL acquereur entrante)."""
    payload = scm_cession_fixture().model_dump(by_alias=True)
    scm_cedee = payload.get("scm_cedee") or {}
    parts_cedees = payload.get("parts_cedees") or {}
    prix = payload.get("prix") or {}
    # SCM de demo : 300 parts (100 + 100 + 100) ; cession de 50 parts.
    nb_total = int(scm_cedee.get("nb_parts_total") or 300)
    nb_cedees = int(parts_cedees.get("nb") or 50)
    # Trois presents : le cedant (la personne de test) + deux co-associes de demo,
    # chacun 1/3 du capital, pour un total egal a nb_total.
    part = nb_total // 3
    reste = nb_total - 2 * part  # absorbe l'eventuel reste de division sur le 3e
    presents = [
        {
            "morale": False,
            "civilite": person["civilite"],
            "prenom": person["prenom"],
            "nom": person["nom"],
            "nb_parts": str(part),
            "plage": f"1 à {part}",  # N4 : « à » accentue
        },
        {
            "morale": False,
            "civilite": "Monsieur",
            "prenom": "Paul",
            "nom": "Bernard",
            "nb_parts": str(part),
            "plage": f"{part + 1} à {2 * part}",  # N4 : « à » accentue
        },
        {
            "morale": False,
            "civilite": "Madame",
            "prenom": "Anne",
            "nom": "Martin",
            "nb_parts": str(reste),
            "plage": f"{2 * part + 1} à {nb_total}",  # N4 : « à » accentue
        },
    ]
    values: dict[str, object] = {
        "selarl_cession_scm_cedee_denomination": scm_cedee.get("denomination") or "",
        "selarl_cession_scm_cedee_rcs_ville": scm_cedee.get("ville_rcs") or "",
        "selarl_cession_scm_cedee_numero_rcs": scm_cedee.get("numero_rcs") or "",
        "selarl_cession_scm_cedee_capital_social": scm_cedee.get("capital_social") or "",
        "selarl_cession_scm_cedee_nb_parts_total": str(nb_total),
        # N4 (Akainu n1, 2026-06-24) : prefill « plage_parts_total » retire (le widget est
        # desormais auto-calcule et desactive, sans key -> cette cle n'etait plus lue par personne).
        # Cedant = l'associe unique (ticket 2.13).
        "selarl_cession_scm_cedant_civilite": person["civilite"],
        "selarl_cession_scm_cedant_prenom": person["prenom"],
        "selarl_cession_scm_cedant_nom": person["nom"],
        # Parts cedees : le cedant cede les `nb_cedees` dernieres de sa tranche.
        "selarl_cession_scm_parts_nb": str(nb_cedees),
        "selarl_cession_scm_parts_plage": f"{part - nb_cedees + 1} à {part}",  # N4 : « à »
        "selarl_cession_scm_prix_global": prix.get("global") or "",
        "selarl_cession_scm_prix_global_lettres": prix.get("global_lettres") or "",
        # Repeater des presents.
        "selarl_cession_scm_presents_count": len(presents),
    }
    for index, present in enumerate(presents):
        values[f"selarl_cession_scm_present_{index}_morale"] = present["morale"]
        values[f"selarl_cession_scm_present_{index}_civilite"] = present["civilite"]
        values[f"selarl_cession_scm_present_{index}_prenom"] = present["prenom"]
        values[f"selarl_cession_scm_present_{index}_nom"] = present["nom"]
        values[f"selarl_cession_scm_present_{index}_nb_parts"] = present["nb_parts"]
        values[f"selarl_cession_scm_present_{index}_plage"] = present["plage"]
    return values


def _test_people() -> tuple[dict[str, str], ...]:
    return (
        {
            "civilite": "Monsieur",
            "prenom": "Jean",
            "nom": "Martin",
            "date_naissance": "12/04/1984",
            "ville_naissance": "Paris",
            "departement_naissance": "75",
            "nom_pere": "Pierre Martin",
            "nom_mere": "Anne Martin",
            "adresse_num_voie": "10",
            "adresse_voie": "rue des Tilleuls",
            "adresse_cp": "75011",
            "adresse_ville": "Paris",
        },
        {
            "civilite": "Madame",
            "prenom": "Camille",
            "nom": "Bernard",
            "date_naissance": "21/09/1978",
            "ville_naissance": "Lyon",
            "departement_naissance": "69",
            "nom_pere": "Laurent Bernard",
            "nom_mere": "Marie Bernard",
            "adresse_num_voie": "8",
            "adresse_voie": "avenue Victor Hugo",
            "adresse_cp": "69002",
            "adresse_ville": "Lyon",
        },
        {
            "civilite": "Monsieur",
            "prenom": "Thomas",
            "nom": "Durand",
            "date_naissance": "03/02/1981",
            "ville_naissance": "Nantes",
            "departement_naissance": "44",
            "nom_pere": "Alain Durand",
            "nom_mere": "Helene Durand",
            "adresse_num_voie": "14",
            "adresse_voie": "boulevard Saint-Felix",
            "adresse_cp": "44000",
            "adresse_ville": "Nantes",
        },
    )


def _test_companies() -> tuple[dict[str, str], ...]:
    return (
        {
            "numero": "20",
            "voie": "avenue du Siege",
            "cp": "75002",
            "ville": "Paris",
            "departement_ordre": "75, Paris",
            "ordre_adresse": "1 rue de l'Ordre",
            "ordre_cp": "75008",
            "banque_adresse": "30 boulevard Haussmann, 75009 Paris",
        },
        {
            "numero": "5",
            "voie": "place Bellecour",
            "cp": "69002",
            "ville": "Lyon",
            "departement_ordre": "69, Rhone",
            "ordre_adresse": "12 quai Jules Courmont",
            "ordre_cp": "69002",
            "banque_adresse": "7 cours de la Liberte, 69003 Lyon",
        },
        {
            "numero": "3",
            "voie": "rue Crebillon",
            "cp": "44000",
            "ville": "Nantes",
            "departement_ordre": "44, Loire-Atlantique",
            "ordre_adresse": "9 allee Baco",
            "ordre_cp": "44000",
            "banque_adresse": "2 rue de Strasbourg, 44000 Nantes",
        },
    )
