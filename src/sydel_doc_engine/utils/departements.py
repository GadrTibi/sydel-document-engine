from __future__ import annotations

# Mapping numero -> nom des departements francais (metropole + DROM + Corse 2A/2B).
# Source : liste officielle INSEE des departements. Utilise pour rendre le NOM du
# departement (« Seine-et-Marne ») la ou un champ porte le NUMERO (« 77 »).
#
# Retour Albane (7.4 / 9.2, 2026-07-06) : les statuts SPFPL et la demande d'inscription
# a l'Ordre rendaient « de 77 » au lieu de « de Seine-et-Marne ». Le champ
# `ordre.departement` / `ordre.departement_inscription` porte le NUMERO ; ce helper le
# convertit en NOM. Passthrough si la valeur est deja un nom (robustesse).

_DEPARTEMENTS: dict[str, str] = {
    "01": "Ain",
    "02": "Aisne",
    "03": "Allier",
    "04": "Alpes-de-Haute-Provence",
    "05": "Hautes-Alpes",
    "06": "Alpes-Maritimes",
    "07": "Ardèche",
    "08": "Ardennes",
    "09": "Ariège",
    "10": "Aube",
    "11": "Aude",
    "12": "Aveyron",
    "13": "Bouches-du-Rhône",
    "14": "Calvados",
    "15": "Cantal",
    "16": "Charente",
    "17": "Charente-Maritime",
    "18": "Cher",
    "19": "Corrèze",
    "2A": "Corse-du-Sud",
    "2B": "Haute-Corse",
    "21": "Côte-d'Or",
    "22": "Côtes-d'Armor",
    "23": "Creuse",
    "24": "Dordogne",
    "25": "Doubs",
    "26": "Drôme",
    "27": "Eure",
    "28": "Eure-et-Loir",
    "29": "Finistère",
    "30": "Gard",
    "31": "Haute-Garonne",
    "32": "Gers",
    "33": "Gironde",
    "34": "Hérault",
    "35": "Ille-et-Vilaine",
    "36": "Indre",
    "37": "Indre-et-Loire",
    "38": "Isère",
    "39": "Jura",
    "40": "Landes",
    "41": "Loir-et-Cher",
    "42": "Loire",
    "43": "Haute-Loire",
    "44": "Loire-Atlantique",
    "45": "Loiret",
    "46": "Lot",
    "47": "Lot-et-Garonne",
    "48": "Lozère",
    "49": "Maine-et-Loire",
    "50": "Manche",
    "51": "Marne",
    "52": "Haute-Marne",
    "53": "Mayenne",
    "54": "Meurthe-et-Moselle",
    "55": "Meuse",
    "56": "Morbihan",
    "57": "Moselle",
    "58": "Nièvre",
    "59": "Nord",
    "60": "Oise",
    "61": "Orne",
    "62": "Pas-de-Calais",
    "63": "Puy-de-Dôme",
    "64": "Pyrénées-Atlantiques",
    "65": "Hautes-Pyrénées",
    "66": "Pyrénées-Orientales",
    "67": "Bas-Rhin",
    "68": "Haut-Rhin",
    "69": "Rhône",
    "70": "Haute-Saône",
    "71": "Saône-et-Loire",
    "72": "Sarthe",
    "73": "Savoie",
    "74": "Haute-Savoie",
    "75": "Paris",
    "76": "Seine-Maritime",
    "77": "Seine-et-Marne",
    "78": "Yvelines",
    "79": "Deux-Sèvres",
    "80": "Somme",
    "81": "Tarn",
    "82": "Tarn-et-Garonne",
    "83": "Var",
    "84": "Vaucluse",
    "85": "Vendée",
    "86": "Vienne",
    "87": "Haute-Vienne",
    "88": "Vosges",
    "89": "Yonne",
    "90": "Territoire de Belfort",
    "91": "Essonne",
    "92": "Hauts-de-Seine",
    "93": "Seine-Saint-Denis",
    "94": "Val-de-Marne",
    "95": "Val-d'Oise",
    "971": "Guadeloupe",
    "972": "Martinique",
    "973": "Guyane",
    "974": "La Réunion",
    "976": "Mayotte",
}


def _normalize_code(value: str) -> str:
    """Normalise un code departement en cle du mapping.

    Accepte « 77 », « 7 » (-> « 07 »), « 2A »/« 2a », « 971 »… On retire les
    espaces, on met les lettres Corse en majuscule, et on pad a 2 chiffres pour
    les codes purement numeriques < 10 (« 1 » -> « 01 »).
    """
    cleaned = value.strip().upper()
    if cleaned in _DEPARTEMENTS:
        return cleaned
    if cleaned.isdigit() and len(cleaned) == 1:
        return cleaned.zfill(2)
    return cleaned


def departement_nom(value: str | None) -> str:
    """Convertit un NUMERO de departement en NOM (« 77 » -> « Seine-et-Marne »).

    - Numero connu (metropole, Corse 2A/2B, DROM) -> nom officiel INSEE.
    - Valeur deja un nom (ex. « Seine-et-Marne », « Rhône ») -> renvoyee telle
      quelle (passthrough robuste : on ne detruit jamais un nom deja correct).
    - Numero inconnu / valeur vide -> renvoyee telle quelle (jamais de perte
      silencieuse ni d'exception ; l'appelant reste maitre de la validation).
    """
    if value is None:
        return ""
    cleaned = value.strip()
    if not cleaned:
        return cleaned
    return _DEPARTEMENTS.get(_normalize_code(cleaned), cleaned)
