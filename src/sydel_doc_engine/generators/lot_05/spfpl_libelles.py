"""Libellés MÉTIER des marqueurs « (À COMPLÉTER : … ) » des documents SPFPL.

KAN-2 / M1 (Rafael 2026-07-15, motif n°1 des rejets successifs) : un marqueur exposé au
client qui relit son acte doit porter un LIBELLÉ MÉTIER lisible (« prénom de l'associé unique »,
« numéro RPPS », « valeur nominale d'une action »), JAMAIS un chemin technique
(« actionnaire_unique.prenom », « CESSION_PARTS.PRIX_TOTAL_LETTRES »).

`libelle_metier` traduit le `field_name` technique (chemin d'objet, éventuellement en
MAJUSCULES de token ou indexé « souscripteurs0 ») en libellé métier. Un libellé DÉJÀ humain
(passé tel quel par un appelant, ex. `quantite_titres(value, "nombre de parts cédées")`) traverse
inchangé. Toute traduction est appliquée UNIQUEMENT au moment où le marqueur est produit
(valeur absente) — la sortie NOMINALE (champ rempli) est byte-identique.

Un chemin non répertorié tombe sur un repli sûr (séparateurs remplacés par des espaces) : le
marqueur reste lisible et surtout ne contient JAMAIS de point, d'underscore ni de MAJUSCULES de
token — la garantie que la garde de conformité vérifie.
"""

from __future__ import annotations

# Libellés des chemins techniques -> libellé métier lisible par le client.
# Clé = `field_name` NORMALISÉ (minuscules, index numériques retirés). Cf. `_normalize_key`.
_LIBELLES: dict[str, str] = {
    # --- Personne physique (associé unique / cédant / apporteur) --------------------------
    "actionnaire_unique.prenom": "prénom de l'associé unique",
    "actionnaire_unique.prenoms": "prénoms de l'associé unique",
    "actionnaire_unique.nom": "nom de l'associé unique",
    "actionnaire_unique.date_naissance": "date de naissance de l'associé unique",
    "actionnaire_unique.ville_naissance": "ville de naissance de l'associé unique",
    "actionnaire_unique.departement_naissance": "département de naissance de l'associé unique",
    "actionnaire_unique.nationalite": "nationalité de l'associé unique",
    "actionnaire_unique.profession": "profession de l'associé unique",
    "actionnaire_unique.situation_maritale": "situation matrimoniale de l'associé unique",
    "actionnaire_unique.regime_matrimonial": "régime matrimonial de l'associé unique",
    "actionnaire_unique.civilite_affichage": "civilité de l'associé unique",
    "actionnaire_unique.adresse_personnelle_affichee": "adresse personnelle de l'associé unique",
    "actionnaire_unique.adresse_personnelle.num_voie": "numéro de voie de l'associé unique",
    "actionnaire_unique.adresse_personnelle.voie": "voie de l'adresse de l'associé unique",
    "actionnaire_unique.adresse_personnelle.cp": "code postal de l'associé unique",
    "actionnaire_unique.adresse_personnelle.ville": "ville de l'associé unique",
    "actionnaire_unique.ordre.departement": "département de l'Ordre de l'associé unique",
    "actionnaire_unique.ordre.ville": "ville de l'Ordre de l'associé unique",
    "actionnaire_unique.ordre.numero": "numéro d'inscription à l'Ordre de l'associé unique",
    "actionnaire_unique.ordre.numero_rpps": "numéro RPPS de l'associé unique",
    "actionnaire_unique.conjoint.civilite_affichage": "civilité du conjoint",
    "actionnaire_unique.conjoint.prenom": "prénom du conjoint",
    "actionnaire_unique.conjoint.nom": "nom du conjoint",
    "cedant.prenom": "prénom du cédant",
    "cedant.nom": "nom du cédant",
    "cedant.date_naissance": "date de naissance du cédant",
    "cedant.ville_naissance": "ville de naissance du cédant",
    "cedant.departement_naissance": "département de naissance du cédant",
    "cedant.nationalite": "nationalité du cédant",
    "cedant.profession": "profession du cédant",
    "cedant.situation_maritale": "situation matrimoniale du cédant",
    "cedant.civilite_affichage": "civilité du cédant",
    "cedant.adresse_personnelle_affichee": "adresse personnelle du cédant",
    "cedant.ordre.departement": "département de l'Ordre du cédant",
    "cedant.ordre.numero_rpps": "numéro RPPS du cédant",
    "cedant.conjoint.civilite_affichage": "civilité du conjoint du cédant",
    "cedant.conjoint.prenom": "prénom du conjoint du cédant",
    "cedant.conjoint.nom": "nom du conjoint du cédant",
    "apporteur.prenom": "prénom de l'apporteur",
    "apporteur.nom": "nom de l'apporteur",
    "apporteur.date_naissance": "date de naissance de l'apporteur",
    "apporteur.ville_naissance": "ville de naissance de l'apporteur",
    "apporteur.departement_naissance": "département de naissance de l'apporteur",
    "apporteur.nationalite": "nationalité de l'apporteur",
    "apporteur.profession": "profession de l'apporteur",
    "apporteur.situation_maritale": "situation matrimoniale de l'apporteur",
    "apporteur.civilite_affichage": "civilité de l'apporteur",
    "apporteur.adresse_personnelle_affichee": "adresse personnelle de l'apporteur",
    "apporteur.adresse_personnelle.num_voie": "numéro de voie de l'apporteur",
    "apporteur.adresse_personnelle.voie": "voie de l'adresse de l'apporteur",
    "apporteur.adresse_personnelle.cp": "code postal de l'apporteur",
    "apporteur.adresse_personnelle.ville": "ville de l'apporteur",
    "apporteur.ordre.departement": "département de l'Ordre de l'apporteur",
    "apporteur.ordre.numero": "numéro d'inscription à l'Ordre de l'apporteur",
    "apporteur.ordre.numero_rpps": "numéro RPPS de l'apporteur",
    "apporteur.conjoint.civilite_affichage": "civilité du conjoint de l'apporteur",
    "apporteur.conjoint.prenom": "prénom du conjoint de l'apporteur",
    "apporteur.conjoint.nom": "nom du conjoint de l'apporteur",
    # --- SPFPL (holding) ------------------------------------------------------------------
    "societe_spfpl.denomination": "dénomination de la SPFPL",
    "societe_spfpl.capital_social": "capital social de la SPFPL",
    "societe_spfpl.capital_social_lettres": "capital social de la SPFPL en toutes lettres",
    "societe_spfpl.valeur_nominale_action_lettres": (
        "valeur nominale d'une action en toutes lettres"
    ),
    "societe_spfpl.ville_rcs": "ville du RCS de la SPFPL",
    "societe_spfpl.siege.num_voie": "numéro de voie du siège de la SPFPL",
    "societe_spfpl.siege.voie": "voie du siège de la SPFPL",
    "societe_spfpl.siege.cp": "code postal du siège de la SPFPL",
    "societe_spfpl.siege.ville": "ville du siège de la SPFPL",
    # --- Société cible (SEL) --------------------------------------------------------------
    "societe_cible.denomination": "dénomination de la société cible",
    "societe_cible.forme_sociale": "forme juridique de la société cible",
    "societe_cible.forme_sociale_complete": "forme juridique complète de la société cible",
    "societe_cible.profession_reglementee": "profession réglementée de la société cible",
    "societe_cible.capital_social": "capital social de la société cible",
    "societe_cible.capital_social_lettres": "capital social de la société cible en toutes lettres",
    "societe_cible.valeur_nominale_part": "valeur nominale d'une part de la société cible",
    "societe_cible.valeur_nominale_part_lettres": (
        "valeur nominale d'une part de la société cible en toutes lettres"
    ),
    "societe_cible.numero_rcs": "numéro RCS de la société cible",
    "societe_cible.ville_rcs": "ville du RCS de la société cible",
    "societe_cible.siege.num_voie": "numéro de voie du siège de la société cible",
    "societe_cible.siege.voie": "voie du siège de la société cible",
    "societe_cible.siege.cp": "code postal du siège de la société cible",
    "societe_cible.siege.ville": "ville du siège de la société cible",
    # --- Apport (opération) ---------------------------------------------------------------
    "apport.montant": "montant de l'apport",
    "apport.montant_lettres": "montant de l'apport en toutes lettres",
    "apport_titres.plage_parts": "plage de parts apportées",
    "apport_titres.valeur_globale": "valeur globale de l'apport",
    "apport_titres.valeur_globale_lettres": "valeur globale de l'apport en toutes lettres",
    "apport_titres.valeur_par_titre": "valeur d'un titre apporté",
    "apport_titres.valeur_par_titre_lettres": "valeur d'un titre apporté en toutes lettres",
    "apport_titres.valeur_nominale_action_lettres": (
        "valeur nominale d'une action en toutes lettres"
    ),
    # --- Cession (opération) --------------------------------------------------------------
    "cession_parts.nb_parts_lettres": "nombre de parts cédées en toutes lettres",
    "cession_parts.prix_unitaire": "prix par part cédée",
    "cession_parts.prix_unitaire_lettres": "prix par part cédée en toutes lettres",
    "cession_parts.prix_total": "prix total de cession",
    "cession_parts.prix_total_lettres": "prix total de cession en toutes lettres",
    # --- Capital / souscripteurs (attestation de capital) ---------------------------------
    "capital_souscription.valeur_nominale_action": "valeur nominale d'une action",
    "capital_souscription.apports_nature_montant": "montant des apports en nature",
    "capital_souscription.president.prenom": "prénom du président",
    "capital_souscription.president.nom": "nom du président",
    "capital_souscription.president.adresse_personnelle_affichee": (
        "adresse personnelle du président"
    ),
    "capital_souscription.souscripteurs.prenom": "prénom du souscripteur",
    "capital_souscription.souscripteurs.nom": "nom du souscripteur",
    # --- Associés de la cible (répartition) -----------------------------------------------
    "associes_cible.prenom": "prénom de l'associé de la société cible",
    "associes_cible.nom": "nom de l'associé de la société cible",
    "associes_cible.denomination": "dénomination de la société acquéreuse",
    # --- Organes de contrôle de l'apport --------------------------------------------------
    "commissaire_aux_apports.denomination": "dénomination du commissaire aux apports",
    "commissaire_aux_apports.forme_sociale": "forme juridique du commissaire aux apports",
    "commissaire_aux_apports.capital_social": "capital social du commissaire aux apports",
    "commissaire_aux_apports.numero_rcs": "numéro RCS du commissaire aux apports",
    "commissaire_aux_apports.ville_rcs": "ville du RCS du commissaire aux apports",
    "commissaire_aux_apports.siege.num_voie": "numéro de voie du commissaire aux apports",
    "commissaire_aux_apports.siege.voie": "voie du siège du commissaire aux apports",
    "commissaire_aux_apports.siege.cp": "code postal du commissaire aux apports",
    "commissaire_aux_apports.siege.ville": "ville du commissaire aux apports",
    "commissaire_aux_apports.representant.civilite_affichage": (
        "civilité du représentant du commissaire aux apports"
    ),
    "commissaire_aux_apports.representant.prenom": (
        "prénom du représentant du commissaire aux apports"
    ),
    "commissaire_aux_apports.representant.nom": "nom du représentant du commissaire aux apports",
    "evaluateur_apport.denomination": "dénomination de l'évaluateur de l'apport",
    "evaluateur_apport.forme_sociale": "forme juridique de l'évaluateur de l'apport",
    "evaluateur_apport.capital_social": "capital social de l'évaluateur de l'apport",
    "evaluateur_apport.numero_rcs": "numéro RCS de l'évaluateur de l'apport",
    "evaluateur_apport.ville_rcs": "ville du RCS de l'évaluateur de l'apport",
    "evaluateur_apport.siege.num_voie": "numéro de voie de l'évaluateur de l'apport",
    "evaluateur_apport.siege.voie": "voie du siège de l'évaluateur de l'apport",
    "evaluateur_apport.siege.cp": "code postal de l'évaluateur de l'apport",
    "evaluateur_apport.siege.ville": "ville de l'évaluateur de l'apport",
    # --- Représentant de la SPFPL (acte de cession) ---------------------------------------
    "representant.prenom": "prénom du représentant de la SPFPL",
    "representant.nom": "nom du représentant de la SPFPL",
    "representant.civilite_affichage": "civilité du représentant de la SPFPL",
    # --- Banque / dépôt des fonds ---------------------------------------------------------
    "depot_fonds.banque.nom": "nom de la banque",
    "depot_fonds.banque.adresse_affichee": "adresse de la banque",
    # --- Dates / lieux / réunion ----------------------------------------------------------
    "signature.lieu": "lieu de signature",
    "signature.date": "date de signature",
    "decision.date": "date de la décision",
    "reunion.date_lettres": "date de la réunion en toutes lettres",
    "reunion.annee_lettres": "année de la réunion en toutes lettres",
    "exercice_social.debut": "début de l'exercice social",
    "exercice_social.fin": "fin de l'exercice social",
    "exercice_social.date_cloture_premier_exercice": (
        "date de clôture du premier exercice"
    ),
    "date": "date",
}


def _normalize_key(field_name: str) -> str:
    """Chemin technique -> clé normalisée : minuscules + index numériques retirés.

    « SOCIETE_CIBLE.CAPITAL_SOCIAL » et « associes_cible0.nom » -> « societe_cible.capital_social »
    / « associes_cible.nom ». Les crochets d'index éventuels sont retirés.
    """
    raw = field_name.replace("[", "").replace("]", "").strip()
    segments = []
    for segment in raw.split("."):
        segment = segment.strip().rstrip("0123456789").lower()
        segments.append(segment)
    return ".".join(segments)


def _fallback(field_name: str) -> str:
    """Repli sûr : un chemin non répertorié reste lisible et surtout SANS point / underscore /
    MAJUSCULES de token (garantie de la garde de conformité)."""
    cleaned = field_name.replace("[", "").replace("]", "").replace("_", " ").replace(".", " ")
    return " ".join(cleaned.lower().split())


def libelle_metier(field_name: str) -> str:
    """Traduit un `field_name` technique en libellé MÉTIER lisible (KAN-2 / M1).

    Un libellé DÉJÀ humain (espaces, pas de séparateur technique) traverse inchangé — les
    appelants qui passent déjà un intitulé métier (`quantite_titres`) ne sont pas réécrits.
    """
    fn = field_name.strip()
    if " " in fn and "." not in fn and "_" not in fn:
        return fn
    key = _normalize_key(fn)
    if key in _LIBELLES:
        return _LIBELLES[key]
    return _fallback(fn)
