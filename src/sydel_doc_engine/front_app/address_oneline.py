"""Golden bloc — saisie d'adresse sur UNE ligne (retour client O24-03).

« Toutes les adresses doivent etre redigees sur une ligne, pas de champ separe pour la
rue, la voie, etc. » Ce module porte le PARSER PARTAGE (un champ texte unique -> Address
structuree num_voie/voie/cp/ville exigee par les generateurs : DNC DOC-001, domiciliation
via [num_voie_siege], regime communautaire, ordre...). Appele par TOUS les types
(propagation Q4, regle 68). Loi golden-bloc : appele comme un service, JAMAIS copie
(cf. docs/operations/GOLDEN_BLOCS.md).
"""

from __future__ import annotations

import re
from typing import Any

import streamlit as st

from sydel_doc_engine.domain.models import Address

_CP_RE = re.compile(r"\b(\d{5})\b")


def parse_address_full(text: str) -> Address | None:
    """Parse une adresse saisie sur UNE LIGNE -> Address structuree complete.

    O24-03 (onglet 24) : « Toutes les adresses doivent etre redigees sur une ligne, pas
    de champ separe pour la rue, la voie, etc.. » La saisie reste UNE ligne mais les
    generateurs (DOC-001 DNC, domiciliation via [num_voie_siege], regime communautaire,
    ordre) exigent num_voie/voie/cp/ville separes -> on parse en interne.

    Robustesse (re-Akainu 2026-06-23, MAJEUR O24-03) : le code postal francais fait
    EXACTEMENT 5 chiffres et clot la chaine (CP + ville en fin). On retient donc le
    DERNIER groupe de 5 chiffres comme CP, ce qui immunise les voies contenant une
    annee (« avenue du 8 Mai 1945 » : 1945 = 4 chiffres, jamais pris pour un CP ;
    « rue du 11 Novembre 1918 » idem). num_voie/voie = tout ce qui precede le CP,
    ville = tout ce qui suit. Le suffixe bis/ter/quater est detache du numero, en
    minuscules OU majuscules. Exemples acceptes :
      « 12 rue de la Paix, 75001 Paris »   « 12, rue de la Paix, 75001 Paris »
      « 12 rue de la Paix 75001 Paris »    « 10 avenue du 8 Mai 1945, 33700 Merignac »
      « 12 BIS rue de la Paix 75001 Paris » -> num_voie=« 12 BIS ».
    -> num_voie/voie / cp=75001 / ville=Paris.

    Validite : num_voie ET voie ET cp ET ville requis (sinon None -> la validation
    « adresse requise » s'applique). Le numero de tete est REQUIS, en coherence avec
    les validateurs (siege_num / signataire_adresse_num obligatoires pour la
    domiciliation et la DNC). Le cas « lieu-dit / place sans numero » est un arbitrage
    metier en attente d'Albane (docs/review/QUESTIONS_RAFAEL.md) : tant qu'il n'est pas
    tranche, on garde le comportement historique (numero requis) — pas d'extrapolation."""
    raw = (text or "").strip()
    if not raw:
        return None
    # CP francais = DERNIER groupe de 5 chiffres ; voie avant, ville apres.
    cp_matches = list(_CP_RE.finditer(raw))
    if not cp_matches:
        return None
    last = cp_matches[-1]
    cp = last.group(1)
    before = raw[: last.start()].strip().rstrip(",").strip()
    ville = raw[last.end():].strip().lstrip(",").strip()
    # Numero de tete detache de la voie, separateur espace OU virgule ; suffixe
    # bis/ter/quater insensible a la casse (« 12 BIS » comme « 12 bis »).
    m = re.match(r"(\d+\s*(?:bis|ter|quater|[a-z])?)[\s,]+(.*)", before, re.IGNORECASE)
    if m:
        num_voie, voie = m.group(1).strip(), m.group(2).strip()
    else:
        # Complement d'adresse AVANT le numero (nom de residence / batiment / lieu-dit) :
        # « Maison Blanche 14 boulevard Carabacel ». Bug Albane 2026-07-08 : le parseur
        # exigeait un chiffre EN TETE -> toute adresse a complement etait rejetee (None)
        # et bloquait la generation (« adresse/CP/ville requis ») alors qu'elle etait
        # saisie. On capte le PREMIER numero de voie et on garde le complement COLLE au
        # numero (num_voie) : ordre d'origine preserve, zero perte (le complement doit
        # figurer dans l'adresse). Regression nulle sur les adresses commencant deja par
        # un chiffre (branche `if m` ci-dessus, inchangee).
        m2 = re.match(r"(.+?\d+\s*(?:bis|ter|quater|[a-z])?)[\s,]+(.+)", before, re.IGNORECASE)
        if m2:
            num_voie, voie = m2.group(1).strip(), m2.group(2).strip()
        else:
            num_voie, voie = "", before
    if not (num_voie and voie and cp and ville):
        return None
    return Address(
        num_voie=num_voie,
        voie=voie,
        cp=cp,
        ville=ville,
        adresse_affichee=f"{num_voie} {voie}, {cp} {ville}",
    )


def oneline_address_field(
    container: Any,
    *,
    key: str,
    label: str = "Adresse (N° et voie, CP Ville)",
    default: str = "",
    hint: str | None = "ex : 12 rue de la Paix, 75001 Paris",
) -> Address | None:
    """Rend UN champ texte d'adresse sur une ligne et renvoie le parse (Address | None).

    Helper de rendu PARTAGE (propagation Q4) : un seul text_input + parse_address_full,
    a la place des anciens champs separes No / Voie / CP / Ville. Seede `default` si la
    cle n'est pas encore renseignee. Renvoie None si l'adresse est incomplete : le slice
    appelant applique alors sa validation « adresse requise » comme avant."""
    if default and not st.session_state.get(key):
        st.session_state[key] = default
    raw = container.text_input(label, key=key, help=hint)
    return parse_address_full(raw)
