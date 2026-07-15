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


def part_word(value: object, *, sociale: bool = False) -> str:
    """Accord en nombre du mot « part » (/« part sociale ») selon un NOMBRE DE PARTS.

    KAN-14 (Rafael 2026-07-15) : « Article 7 des statuts : lorsqu'un associé a 1 part,
    cela doit être rédigé au singulier. » Pendant exact de `euro_word` (né du même type
    de retour : « 10 euro »), pour que l'accord soit fait à UN endroit et pas réécrit
    localement dans chaque générateur (il l'était déjà ad hoc 4× côté SPFPL).

    Différence assumée avec `euro_word` : une PART est un objet dénombrable, donc le
    singulier ne vaut QUE pour exactement 1 (0 part**s**, 1 part, 2 parts) — alors qu'un
    MONTANT est une quantité continue et rend « 0 euro »/« 1,50 euro ». Ne pas
    factoriser les deux : ce sont deux règles françaises distinctes.

    Robuste aux formats de saisie (« 1 », « 1 000 »). Valeur illisible -> pluriel (cas le
    plus courant et le moins risqué), comme `euro_word`.
    """
    # « part sociale » s'accorde sur les DEUX mots (« parts sociales ») : un suffixe « s »
    # colle a la locution donnerait « part sociales ». Attrape par le test des le 1er jet.
    singulier, pluriel = ("part sociale", "parts sociales") if sociale else ("part", "parts")
    digits = re.sub(r"\D", "", str(value or "").split(",")[0])
    if not digits:
        return pluriel
    return singulier if abs(int(digits)) == 1 else pluriel


_ACCORD_EUROS_FIGURE: Final = re.compile(
    # « euros » pluriel precede — apres separateurs NEUTRES (espaces, insecables, « ) »,
    # « € ») — d'une quantite SINGULIERE : figure dont la partie entiere vaut 0 ou 1
    # (« 1 », « (1) », « 1 € », « 1,00 »). Le lookbehind negatif empeche de mordre la
    # QUEUE d'un nombre plus grand (« 21 euros », « 101 euros » : le « 1 » y est precede
    # d'un chiffre -> non singulier).
    r"(?<![\d   ][\d.,])(?<![0-9])([01](?:[.,]0+)?)"
    r"(\s*(?:€|\)| | )?\s*)euros\b"
)
_ACCORD_EUROS_LETTRES: Final = re.compile(
    # Mot « un »/« une » (mise en lettres du 1) directement suivi — via separateurs
    # neutres eventuels — de « euros » : « un euros » -> « un euro » ; « une euros ».
    r"\b(une?)(\s+)euros\b"
)


def accord_euros_apres_montant(text: str) -> str:
    """Corrige l'accord « euros » -> « euro » APRES un montant SINGULIER, sur un texte
    DEJA rendu (Rafael 2026-07-09, « partout = partout »).

    Cible les surfaces verbatim-modele dont l'unite « euros » est FIGEE dans le DOCX
    source (statuts SCI/SCS : « Au capital de [capital_social] euros ») : quand la valeur
    substituee vaut 0 ou 1, « 1 euros » est fautif -> « 1 euro ». On n'agit QUE sur un
    montant strictement singulier ; « 600 euros », « 21 euros », « 2,50 euros » restent
    intacts. La forme en lettres du 1 (« un euros » / « une euros ») est aussi accordee.
    Idempotent (« 1 euro » -> « 1 euro »). Ne touche jamais le pluriel.
    """
    text = _ACCORD_EUROS_FIGURE.sub(lambda m: f"{m.group(1)}{m.group(2)}euro", text)
    return _ACCORD_EUROS_LETTRES.sub(lambda m: f"{m.group(1)}{m.group(2)}euro", text)


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


# Partie entiere / decimale d'un montant nu (separateurs d'espace, insecables tolérés).
_MONTANT_PARTS_RE: Final = re.compile(r"(\d[\d\s\u00a0\u202f]*?)([.,]\d+)?$")


def _group_integer_part(text: str) -> str:
    """Groupe par 3 (espaces) la partie entiere d'un montant nu ; décimale préservée.

    « 1000 » -> « 1 000 » ; « 60000,50 » -> « 60 000,50 » ; idempotent
    (« 1 000 » -> « 1 000 ») ; « 600 » (< 4 chiffres) inchangé. Autonome (grammar reste
    sans dépendance sur field_derivations) ; même règle des 4 chiffres que
    ``field_derivations.group_montant`` (R5, Rafael 2026-07-09).
    """
    match = _MONTANT_PARTS_RE.fullmatch(text)
    if match is None:
        return text
    digits = re.sub(r"\D", "", match.group(1))
    if len(digits) < 4:
        return text
    grouped = f"{int(digits):,}".replace(",", " ")
    return grouped + (match.group(2) or "")


def montant_avec_euros(value: str | None) -> str:
    """Devise automatique d'un montant AFFICHE : « 1000 » -> « 1 000 euros ».

    Retour Rafael 2026-07-09 (transverse) : l'utilisateur ne redige JAMAIS « euros » —
    le moteur derive l'unite ET groupe les milliers (R5, seuil 4 chiffres). Idempotent
    et prudent :
    - montant nu purement numerique -> groupé + unité accordée (« 1 euro » / « 600
      euros » / « 1 000 euros ») ;
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
    grouped = _group_integer_part(text)
    return f"{grouped} {euro_word(grouped)}"


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


# ---------------------------------------------------------------------------
# Accord en GENRE d'une FONCTION / d'un mandat porte par une personne (Rafael
# 2026-07-09, reglement interieur SCM : « Madame Alice Martin, gerant » -> « gerante »).
# Meme classe grammaticale que ne/nee : on ACCORDE une fonction rendue pour une
# personne genree. Lexique par INTENTION (accord d'une fonction connue), JAMAIS une
# liste de tournures : chaque mot-fonction connu est accorde, au singulier comme au
# pluriel, dans les DEUX sens (idempotent). Un mot HORS lexique est laisse INTACT
# (aucune regex sur « -e/-ee » qui abimerait un mot inconnu). Multi-mots accordes mot
# a mot (« directeur general » -> « directrice generale »).
# ---------------------------------------------------------------------------
# KAN-23 (Rafael 2026-07-15) : « Le mot "gérant" ne doit JAMAIS être mis au féminin. Ce n'est pas
# correct. On parle toujours d'un gérant, même lorsqu'il s'agit d'une femme. » -> INVARIANT : les
# DEUX formes restent des cles (pour CORRIGER un « gérante » qui arriverait du front ou d'un
# modele), mais rendent TOUJOURS le masculin, quel que soit le genre de la personne.
# SUPERSEDE la demande INVERSE du meme Rafael le 2026-07-09 (reglement interieur SCM : « Madame
# Alice Martin, gerant » -> « gerante ») : le retour le plus recent prime (regle 68). Ne PAS
# reintroduire ces mots dans `_FONCTION_PAIRS_MF`.
_FONCTION_INVARIANTES_MF: Final = (
    ("gérant", "gérante"),
    ("cogérant", "cogérante"),
    ("co-gérant", "co-gérante"),
)

_FONCTION_PAIRS_MF: Final = (
    ("président", "présidente"),
    ("vice-président", "vice-présidente"),
    ("associé", "associée"),
    ("coassocié", "coassociée"),
    ("administrateur", "administratrice"),
    ("directeur", "directrice"),
    ("cofondateur", "cofondatrice"),
    ("fondateur", "fondatrice"),
    ("trésorier", "trésorière"),
    ("délégué", "déléguée"),
    ("adjoint", "adjointe"),
    ("général", "générale"),
)


def _build_fonction_maps() -> tuple[dict[str, str], dict[str, str]]:
    vers_feminin: dict[str, str] = {}
    vers_masculin: dict[str, str] = {}
    for masculin, feminin in _FONCTION_PAIRS_MF:
        # Les DEUX formes (masculin, feminin) sont des cles -> idempotent et
        # bidirectionnel : une fonction deja au bon genre reste intacte, une fonction
        # feminine attribuee a un homme redevient masculine.
        for forme in (masculin, feminin):
            vers_feminin[forme] = feminin
            vers_masculin[forme] = masculin
            # Pluriel regulier (+ s) : « presidents »/« presidentes », « associes »/« associees ».
            vers_feminin[forme + "s"] = feminin + "s"
            vers_masculin[forme + "s"] = masculin + "s"
    # KAN-23 : fonctions INVARIANTES (« gérant » & co) — les deux formes sont reconnues, mais
    # rendent TOUJOURS le masculin, y compris quand on demande le feminin. Un « gérante » qui
    # arriverait du front ou d'un modele est donc CORRIGE en « gérant ».
    for masculin, feminin_incorrect in _FONCTION_INVARIANTES_MF:
        for forme in (masculin, feminin_incorrect):
            vers_feminin[forme] = masculin
            vers_masculin[forme] = masculin
            vers_feminin[forme + "s"] = masculin + "s"
            vers_masculin[forme + "s"] = masculin + "s"
    return vers_feminin, vers_masculin


_FONCTION_VERS_FEMININ, _FONCTION_VERS_MASCULIN = _build_fonction_maps()
# KAN-23 : toutes les formes (masculin, feminin fautif, pluriels) des fonctions figees au
# masculin — sert au possessif (« son gérant », jamais « sa gérant »).
_FONCTIONS_INVARIABLES_CASEFOLD: Final[frozenset[str]] = frozenset(
    forme.casefold()
    for masculin, feminin in _FONCTION_INVARIANTES_MF
    for base in (masculin, feminin)
    for forme in (base, base + "s")
)
_FONCTION_TOKEN_RE: Final = re.compile(r"(\s+)")


def _accord_fonction_token(token: str, mapping: dict[str, str]) -> str:
    cible = mapping.get(token.casefold())
    if cible is None:
        return token
    # Preserve la MAJUSCULE initiale eventuelle (« Gérant » -> « Gérante »).
    if token[:1].isupper():
        return cible[:1].upper() + cible[1:]
    return cible


def accord_fonction(fonction: str | None, genre: Gender | None) -> str:
    """Accorde une FONCTION au genre d'une personne.

    « gérant » -> « gérante » au feminin ; masculin (ou genre absent) laisse la forme
    masculine. Idempotent et bidirectionnel (cf. ``_build_fonction_maps``). Un mot hors
    lexique est renvoye tel quel — on n'invente jamais de terminaison. Multi-mots
    accordes mot a mot (« directeur général » -> « directrice générale »)."""
    if not fonction:
        return fonction or ""
    mapping = _FONCTION_VERS_FEMININ if genre == Gender.FEMININ else _FONCTION_VERS_MASCULIN
    tokens = _FONCTION_TOKEN_RE.split(fonction)
    return "".join(_accord_fonction_token(token, mapping) for token in tokens)


# Termes (participes/adjectifs/pronoms) accordés au genre d'une personne dans les actes,
# au-dela des seules FONCTIONS (Albane SELARL 2026-07-10 : « inscrit » -> « inscrite »,
# « soussigné » -> « soussignée », « le cédant déclare qu'il » -> « qu'elle »). Codage par
# INTENTION (tout terme referant a la personne s'accorde), lexique explicite — jamais de
# regex de terminaison qui inventerait un feminin. Casse preservee, idempotent.
_TERMES_VERS_FEMININ: Final[dict[str, str]] = {
    "inscrit": "inscrite",
    "soussigné": "soussignée",
    "domicilié": "domiciliée",
    "marié": "mariée",
    "pacsé": "pacsée",
    "né": "née",
    "désigné": "désignée",
    "propriétaire": "propriétaire",  # invariant (explicite = « ne pas toucher »)
    "il": "elle",
    "celui": "celle",
    "lui-même": "elle-même",
    "ce dernier": "cette dernière",
    "le cédant": "la cédante",
    "un cédant": "une cédante",
    # Akainu SELARL 2026-07-12 (M2/M3) : adjectifs de qualite/nationalite et fonctions
    # accordes a la personne (declarations acte SCM « resident francais » ; demande ordre
    # « associe/praticien/exercant »). INTENTION : tout terme accorde a une personne genree.
    "résident": "résidente",
    "français": "française",
    "associé": "associée",
    "praticien": "praticienne",
    "exerçant": "exerçante",
    # Akainu SELARL ronde 2 (M2) : « en qualité de futur gérant » -> « future gérante »
    # (lettre d'avertissement au conjoint), accorde au genre du dirigeant signataire.
    "futur": "future",
}
_TERMES_VERS_MASCULIN: Final[dict[str, str]] = {v: k for k, v in _TERMES_VERS_FEMININ.items()}


def accord_terme_genre(terme: str | None, genre: Gender | None) -> str:
    """Accorde un TERME (participe/adjectif/pronom) au genre d'une personne : « inscrit »
    -> « inscrite », « soussigné » -> « soussignée », « il » -> « elle ». Idempotent,
    bidirectionnel, casse preservee. Mot hors lexique renvoye tel quel (aucune invention)."""
    if not terme:
        return terme or ""
    mapping = _TERMES_VERS_FEMININ if genre == Gender.FEMININ else _TERMES_VERS_MASCULIN
    cible = mapping.get(terme.lower())
    if cible is None:
        return terme
    if terme.isupper():
        return cible.upper()
    if terme[:1].isupper():
        return cible[:1].upper() + cible[1:]
    return cible


def accord_participe_e(mot: str | None, genre: Gender | None) -> str:
    """Accorde en genre un participe/adjectif se terminant par « -é » (« domicilié » ->
    « domiciliée », « désigné » -> « désignée »). Akainu batch2+3 M2 (2026-07-09) : coder
    l'INTENTION (tout le segment referant a une personne s'accorde), pas le seul mot fonction.
    Feminin + « -é » (pas deja « -ée ») -> +e ; sinon inchange (jamais d'invention)."""
    if not mot:
        return mot or ""
    if genre == Gender.FEMININ and mot.endswith("é"):
        return mot + "e"
    return mot


# Voyelles/h muet devant lesquels le possessif feminin reste « son » (« son associée »,
# « son école ») ; sinon feminin -> « sa » (« sa gérante », « sa présidente »).
_VOYELLES_ELISION = "aeiouyàâäéèêëîïôöûü"


def possessif_singulier(mot_suivant: str, genre: Gender | None) -> str:
    """« son »/« sa » accorde au MOT qu'il determine + a son initiale (Akainu M1 2026-07-09 :
    « son gérante » -> « sa gérante »). Masculin -> « son » ; feminin -> « sa » sauf devant
    une voyelle/h muet (« son associée »).

    KAN-23 (Rafael 2026-07-15) : « gérant » est INVARIABLEMENT masculin, meme pour une femme
    -> le possessif suit le MOT, pas la personne (« son gérant », jamais « sa gérant »). Sans
    cette garde, une gerante femme produirait « Représentée par sa gérant ».
    """
    if _fonction_invariable_masculine(mot_suivant):
        return "son"
    if genre == Gender.FEMININ and mot_suivant[:1].lower() not in _VOYELLES_ELISION:
        return "sa"
    return "son"


def _fonction_invariable_masculine(mot: str | None) -> bool:
    """Le mot est-il une fonction que KAN-23 fige au masculin (« gérant » & co) ?"""
    if not mot:
        return False
    premier = mot.strip().split(" ")[0].casefold()
    return premier in _FONCTIONS_INVARIABLES_CASEFOLD


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
