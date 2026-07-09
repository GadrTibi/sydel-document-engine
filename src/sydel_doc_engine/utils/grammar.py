from __future__ import annotations

import re
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Final

from sydel_doc_engine.domain.enums import Gender

# ---------------------------------------------------------------------------
# Fonctions PURES nombre -> mots (deplacees de front_app.field_derivations le
# 2026-07-06, re-architecture « containment » de la mise en lettres monetaire).
#
# But du deplacement : centraliser le batisseur monetaire (`monetary_words_from_value`)
# AUPRES du SEUL point de composition « lettres + euro » (`montant_lettres_avec_unite`,
# plus bas), sans que `number_words_from_value` (reste dans field_derivations) ait a
# etre decimal-aware globalement (cause de doubles-euros en cascade : prix, civils,
# apport/capital SEL). `field_derivations` RE-IMPORTE ces fonctions pour que tous les
# imports/tests existants continuent de marcher. grammar NE DOIT PAS importer
# field_derivations (pas d'import circulaire).
# ---------------------------------------------------------------------------

_SMALL_NUMBERS: Final = {
    0: "zero",
    1: "un",
    2: "deux",
    3: "trois",
    4: "quatre",
    5: "cinq",
    6: "six",
    7: "sept",
    8: "huit",
    9: "neuf",
    10: "dix",
    11: "onze",
    12: "douze",
    13: "treize",
    14: "quatorze",
    15: "quinze",
    16: "seize",
}
_TENS: Final = {
    20: "vingt",
    30: "trente",
    40: "quarante",
    50: "cinquante",
    60: "soixante",
}


def _decimal_from_value(value: object) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return None
        cleaned = cleaned.replace(" ", " ").replace(" ", "")
        cleaned = cleaned.replace(",", ".")
        cleaned = re.sub(r"[^0-9.-]", "", cleaned)
        if not cleaned:
            return None
        try:
            return Decimal(cleaned)
        except InvalidOperation:
            return None
    return None


def format_numeric_value(value: object) -> str:
    number = _decimal_from_value(value)
    if number is None:
        return str(value).strip() if value is not None else ""
    if number == number.to_integral_value():
        return str(int(number))
    return format(number.normalize(), "f")


def _invariable_before_mille(words: str) -> str:
    """« quatre-vingts » et « cents » sont INVARIABLES devant « mille » (adjectif numéral).

    Akainu 2026-06-26 : « trois cents mille » / « quatre-vingts mille » étaient fautifs ->
    « trois cent mille » / « quatre-vingt mille ». NB : on ne touche QUE devant « mille » ;
    devant « millions »/« milliards » (substantifs) le « s » reste (« deux cents millions »).
    """
    if words.endswith("vingts"):
        return words[:-1]
    if words.endswith("cents"):
        return words[:-1]
    return words


def integer_to_french_words(value: int) -> str:
    if value < 0:
        return "moins " + integer_to_french_words(abs(value))
    if value < 17:
        return _SMALL_NUMBERS[value]
    if value < 20:
        return "dix-" + _SMALL_NUMBERS[value - 10]
    if value < 100:
        return _two_digit_words(value)
    if value < 1000:
        return _hundreds_words(value)
    if value < 1_000_000:
        thousands, remainder = divmod(value, 1000)
        prefix = (
            "mille"
            if thousands == 1
            else f"{_invariable_before_mille(integer_to_french_words(thousands))} mille"
        )
        return prefix if remainder == 0 else f"{prefix} {integer_to_french_words(remainder)}"
    if value < 1_000_000_000:
        millions, remainder = divmod(value, 1_000_000)
        prefix = (
            "un million"
            if millions == 1
            else f"{integer_to_french_words(millions)} millions"
        )
        return prefix if remainder == 0 else f"{prefix} {integer_to_french_words(remainder)}"
    # Palier milliard (Akainu 2026-06-26) : sans lui, 1 000 000 000 rendait « mille millions »
    # au lieu de « un milliard » (capital variable micro holding = 10x un capital >= 100 M).
    milliards, remainder = divmod(value, 1_000_000_000)
    prefix = (
        "un milliard"
        if milliards == 1
        else f"{integer_to_french_words(milliards)} milliards"
    )
    return prefix if remainder == 0 else f"{prefix} {integer_to_french_words(remainder)}"


def _two_digit_words(value: int) -> str:
    if value < 70:
        ten, unit = divmod(value, 10)
        ten_value = ten * 10
        if unit == 0:
            return _TENS[ten_value]
        if unit == 1:
            return f"{_TENS[ten_value]} et un"
        return f"{_TENS[ten_value]}-{_SMALL_NUMBERS[unit]}"
    if value < 80:
        remainder = value - 60
        if remainder == 11:
            return "soixante et onze"
        return f"soixante-{integer_to_french_words(remainder)}"
    remainder = value - 80
    if remainder == 0:
        return "quatre-vingts"
    return f"quatre-vingt-{integer_to_french_words(remainder)}"


def _hundreds_words(value: int) -> str:
    hundred, remainder = divmod(value, 100)
    if hundred == 1:
        prefix = "cent"
    else:
        prefix = f"{_SMALL_NUMBERS[hundred]} cent"
    if remainder == 0:
        return prefix + ("s" if hundred > 1 else "")
    return f"{prefix} {integer_to_french_words(remainder)}"


def monetary_words_from_value(value: object) -> str:
    """Mise en LETTRES monetaire francaise d'un montant en euros, unite INCLUSE.

    Formes standard (Albane 7.5, 2026-07-06) :
    - entier N            -> « <N mots> euro » (N<2) / « euros » (N>=2)
      (ex. 1 -> « un euro », 100 -> « cent euros »)
    - centimes 0,0X       -> « <X mots> centime d'euro » / « centimes d'euro »
      (ex. 0,01 -> « un centime d'euro », 0,50 -> « cinquante centimes d'euro »)
    - mixte X,YY          -> « <X mots> euro(s) et <YY mots> centime(s) »
      (ex. 2,50 -> « deux euros et cinquante centimes »)

    Le montant est arrondi au centime (2 decimales). Une valeur illisible -> "".

    SEUL batisseur de la phrase monetaire complete. Appele UNIQUEMENT au point de
    composition `montant_lettres_avec_unite` (branche decimale) et par les surfaces
    7.5 qui ont besoin de « un centime d'euro ». `number_words_from_value`
    (field_derivations) ne l'appelle PLUS (revert 2026-07-06 : il rend la FIGURE pour
    un decimal, ce qui evite les doubles-euros a la recomposition « lettres + euro »).
    """
    number = _decimal_from_value(value)
    if number is None:
        return ""
    negatif = number < 0
    number = abs(number).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    euros = int(number)
    centimes = int((number - euros) * 100)

    if centimes == 0:
        phrase = f"{integer_to_french_words(euros)} {'euro' if euros < 2 else 'euros'}"
    elif euros == 0:
        # Purement centimes : « un centime d'euro » / « cinquante centimes d'euro ».
        unite = "centime d’euro" if centimes < 2 else "centimes d’euro"
        phrase = f"{integer_to_french_words(centimes)} {unite}"
    else:
        # Mixte : « deux euros et cinquante centimes » (l'unite « euro(s) » reste le
        # noyau, les centimes se declinent en « centime(s) » sans repeter « d'euro »).
        euro_part = f"{integer_to_french_words(euros)} {'euro' if euros < 2 else 'euros'}"
        centime_part = (
            f"{integer_to_french_words(centimes)} "
            f"{'centime' if centimes < 2 else 'centimes'}"
        )
        phrase = f"{euro_part} et {centime_part}"

    return f"moins {phrase}" if negatif else phrase


def _has_real_decimal(value: object) -> bool:
    """True si le montant porte une partie décimale NON NULLE (ex. « 0,01 », « 2,50 »).

    Une décimale « ,00 » ou absente -> False (montant entier). Robuste aux formats
    « 0,01 », « 0.01 », « 1 000,50 », « 100 € ». Sert à distinguer, à la COMPOSITION,
    un montant dont les lettres portent déjà leur unité (« un centime d'euro ») d'un
    entier dont l'unité « euro(s) » doit être accolée à part.
    """
    raw = str(value or "")
    sep = "," if "," in raw else ("." if "." in raw else None)
    if sep is None:
        return False
    fractional = re.sub(r"\D", "", raw.split(sep, 1)[1])
    return bool(fractional) and int(fractional) != 0


def euro_word(value: object) -> str:
    """Accord en nombre du mot « euro » selon un MONTANT.

    Règle française : « euro » au singulier pour un montant strictement inférieur
    à 2 (0 euro, 1 euro, 1,50 euro) ; « euros » au pluriel à partir de 2.

    Robuste aux formats de saisie : « 10 », « 1 000 », « 10,00 », « 100 € ». On
    raisonne sur la PARTIE ENTIÈRE (avant la virgule décimale française), tous
    séparateurs/symboles retirés. Si la valeur est illisible, on renvoie le
    pluriel (cas le plus courant et le moins risqué).

    NB : fonction d'accord PURE (jamais vide) -> utilisable sans risque sur une
    ligne « figure + unité » (« parts de 1 euro »). La suppression de l'unité pour
    un DÉCIMAL (« un centime d'euro », unité déjà dans les lettres) est gérée par
    `montant_lettres_avec_unite`, PAS ici.
    """
    integer_part = re.sub(r"\D", "", str(value or "").split(",")[0])
    if not integer_part:
        # Aucun chiffre exploitable -> pluriel par defaut (cas le plus courant).
        return "euros"
    return "euro" if abs(int(integer_part)) < 2 else "euros"


def montant_lettres_avec_unite(lettres: str, figure: object) -> str:
    """Compose « <lettres> <unité euro> » sans espace parasite — anti double-euro.

    SEUL point de COMPOSITION de la valeur nominale (et de tout montant en lettres
    suivi de son unité). C'est le SEUL endroit qui produit la phrase monétaire
    décimale « un centime d'euro » (containment, re-architecture 2026-07-06). Deux
    cas :

    - figure ENTIÈRE -> `lettres` porte les mots SEULS (« cent ») ; on accole
      l'unité accordée : « cent » + « euros » -> « cent euros » (byte-identique
      au rendu historique `[lettres] [euro_nominal_word]`).
    - figure DÉCIMALE réelle (Albane 7.5, 2026-07-06) -> on IGNORE `lettres` (qui
      ne porte plus que la FIGURE depuis le revert de `number_words_from_value`) et
      on CALCULE la phrase monétaire complète DEPUIS LA FIGURE via
      `monetary_words_from_value` : « 0,01 » -> « un centime d'euro », « 2,50 » ->
      « deux euros et cinquante centimes ». Aucune unité accolée en plus (pas de
      « un centime d'euro euro » ni d'espace parasite).

    Localiser la phrase monétaire ICI (au lieu de `number_words_from_value`) évite
    les doubles-euros en cascade sur les surfaces qui composent « lettres + euro »
    séparément (prix, civils, apport/capital SEL) : là, `number_words_from_value`
    rend désormais la FIGURE, et le template accole « euro(s) » proprement.

    `str.strip()` neutralise tout résidu d'espace.
    """
    if _has_real_decimal(figure):
        return monetary_words_from_value(figure).strip()
    return f"{lettres} {euro_word(figure)}".strip()


# Montant purement numerique (groupes d'espaces / insecables / separateur decimal
# FR ou point) : seul candidat a l'ajout automatique d'unite (jamais de devinette
# sur du texte libre). Unite deja presente (« euros », « euro », « € ») -> passthrough.
_MONTANT_NU_RE: Final = re.compile(r"\d[\d\s  ]*(?:[.,]\d+)?")
_UNITE_EURO_FIN_RE: Final = re.compile(r"(?:euros?|€)\s*$", re.IGNORECASE)


def montant_avec_euros(value: str | None) -> str:
    """Devise automatique d'un montant AFFICHE : « 1 000 » -> « 1 000 euros ».

    Retour Rafael 2026-07-09 (transverse) : l'utilisateur ne redige JAMAIS
    « euros » — le moteur derive l'unite. Idempotent et prudent :
    - montant nu purement numerique -> unite accordee accolée (« 1 euro » /
      « 600 euros ») ;
    - unite deja presente (« 1 000 euros », « 600 € ») -> INTACT (pas de doublon) ;
    - texte non purement numerique (marqueur « (À COMPLÉTER : …) », plage, vide)
      -> INTACT : dans le doute, on ne touche pas.
    """
    text = (value or "").strip()
    if not text:
        return text
    if _UNITE_EURO_FIN_RE.search(text):
        return text
    if _MONTANT_NU_RE.fullmatch(text) is None:
        return text
    return f"{text} {euro_word(text)}"


def capitalize_first(value: str) -> str:
    """Capitalise la 1re lettre en préservant le reste (« célibataire » ->
    « Célibataire », « chirurgien-dentiste » -> « Chirurgien-dentiste »).

    N'utilise PAS ``str.capitalize()`` (qui abaisserait le reste). Rafael
    2026-07-09 (R12) : chaque élément d'un bloc liste d'identité commence par
    une MAJUSCULE — même règle que 7.2 (Albane) côté SPFPL/SELAS.
    """
    if not value:
        return value
    return value[0].upper() + value[1:]


def subject_line(genre: Gender) -> str:
    return "Je soussignée" if genre == Gender.FEMININ else "Je soussigné"


def birth_label(genre: Gender) -> str:
    return "Née le" if genre == Gender.FEMININ else "Né le"


def filiation_label(genre: Gender) -> str:
    return "fille de Monsieur" if genre == Gender.FEMININ else "fils de Monsieur"


def apply_gender_pairs(
    text: str,
    genre: Gender,
    pairs: list[tuple[str, str]],
) -> str:
    """Accorde un texte en genre par remplacement de chaînes EXACTES et ancrées.

    Chaque paire est `(forme_masculin, forme_feminin)`. Selon `genre` :

    - `Gender.FEMININ`  -> remplace chaque `forme_masculin` par sa `forme_feminin` ;
    - `Gender.MASCULIN` -> remplace chaque `forme_feminin` par sa `forme_masculin`.

    Le remplacement est **bidirectionnel** : un modèle figé au féminin (ex. acte
    dentaire « née le ») redevient masculin pour un homme, et un modèle figé au
    masculin (ex. statuts « LE SOUSSIGNE ») devient féminin pour une femme.

    GARDE-FOU : on ne fait JAMAIS de regex sur les terminaisons « -é/-ée ». On
    remplace uniquement les chaînes littérales fournies, pilotées par le `genre`
    de la BONNE personne du contexte (vendeur, représentant, associé,
    signataire...). Une forme déjà dans le bon genre, ou absente du texte, est
    laissée intacte. Si une paire a ses deux formes égales (rien à accorder),
    elle est ignorée pour éviter tout remplacement parasite.

    Le remplacement est **idempotent** et sûr même quand la forme source est un
    préfixe de la cible (ex. « Je soussigné » ⊂ « Je soussignée ») : on protège
    d'abord les occurrences déjà dans le bon genre avant de remplacer, pour ne
    pas re-accorder « Je soussignée » en « Je soussignéee ». Réappliquer la
    fonction sur un texte déjà accordé ne le modifie plus.

    Args:
        text: le texte source (après remplissage des tokens éventuel).
        genre: genre cible (celui de la personne décrite par les formes).
        pairs: liste de couples `(masculin, feminin)` de chaînes exactes.

    Returns:
        Le texte accordé au genre demandé.
    """
    rendered = text
    for index, (masculin, feminin) in enumerate(pairs):
        if masculin == feminin:
            continue
        source, target = (masculin, feminin) if genre == Gender.FEMININ else (feminin, masculin)
        rendered = _replace_to_target(rendered, source, target, index)
    return rendered


def _replace_to_target(text: str, source: str, target: str, index: int) -> str:
    """Remplace `source` par `target` de façon idempotente et sûre.

    Deux cas de chevauchement préfixe à gérer (l'une des formes est sous-chaîne
    de l'autre) :

    - `source` ⊂ `target` (ex. masc « Je soussigné » dans fém « Je soussignée ») :
      remplacer naïvement `source` re-toucherait les `target` déjà corrects. On
      masque d'abord les `target` présents par un jeton neutre, on remplace
      `source` -> `target`, puis on restaure les jetons.
    - `target` ⊂ `source` (ex. fém « Je soussignée » contient masc « Je
      soussigné ») : on remplace directement la chaîne `source` complète (le
      match porte sur la forme la plus longue, donc non ambigu).

    Dans tous les cas, réappliquer la fonction sur un texte déjà accordé est sans
    effet (idempotent).
    """
    if source not in text:
        return text
    if target in source:
        # target est un préfixe/sous-chaîne de source : match direct non ambigu.
        return text.replace(source, target)
    # source ⊂ target (ou disjoints) : on protège les target déjà présents.
    sentinel = f"\x00GENDER_PAIR_{index}\x00"
    protected = text.replace(target, sentinel)
    protected = protected.replace(source, target)
    return protected.replace(sentinel, target)


# Voyelles d'elision (sans « h » : dans une valeur-nombre-en-lettres, le seul mot a « h »
# initial est « huit/huitieme » = h ASPIRE -> « de huit »). « onze/onzieme » = exception
# francaise (« de onze »). Helper partage lot_04 (statuts SEL art.8) + lot_05 (actes/attestations).
_VOYELLES_ELISION = "aeiouàâäéèêëîïôöùûü"
_NO_ELISION_PREFIXES = ("onze", "onziem", "huit", "huitiem", "huitain", "onzain")


def elision_de(value: str) -> str:
    """« de <value> » avec elision correcte : « d’ » (apostrophe courbe U+2019) devant voyelle,
    « de » devant consonne, « h » aspire (« huit ») et l'exception « onze ». PORTEE : valeurs
    NUMERIQUES en lettres (valeur nominale, montant). Les modeles collent « d’ » au placeholder
    (« d’[valeur] ») ; « cent euros » -> « de cent euros », « un euro » -> « d’un euro »,
    « onze/huit euros » -> « de onze/huit euros », « 100 » -> « de 100 »."""
    cleaned = (value or "").strip()
    low = cleaned.lower()
    voyelle = bool(low) and low[0] in _VOYELLES_ELISION and not low.startswith(_NO_ELISION_PREFIXES)
    return f"d’{cleaned}" if voyelle else f"de {cleaned}"
