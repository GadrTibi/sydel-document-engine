"""Règles de conformité transversales client (R1..R10).

Chaque règle codifie un retour client (Albane/Rafael) en assertion PERMANENTE,
appliquée à CHAQUE document de CHAQUE type par ``test_conformite_transverse.py``.
Une règle prend le texte d'un document et retourne la liste des violations
(extraits contextualisés) — liste vide = document conforme à la règle.

Notes de périmètre (décisions consignées, cf. RAPPORT_INITIAL.md) :

* R4 étend le lexique de ``tests/unit/_accents.py`` SANS le modifier : la liste de
  base y est durcie par des tests unitaires existants ; l'étendre là-bas aurait
  changé le verdict de la suite verte. Les ajouts vivent donc ici.
* R6 : « de un euro / de un centime » interdits (élision « d'un » attendue —
  retour Albane n3 acte SPFPL). « à un euro » N'EST PAS codifié : la tournure est
  grammaticalement correcte en français (pas d'élision de « à ») — sans verbatim
  client prouvant le cas fautif, l'interdire produirait des faux positifs.
  Ambiguïté signalée, à trancher sur verbatim.
* R5 : détection des montants ≥ 5 chiffres NON groupés en contexte monétaire
  (« 60000 euros »), avec liste blanche par contexte (RPPS / RCS / SIREN / SIRET /
  numéro / téléphone) pour épargner les identifiants légitimes.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable

from _accents import MOTS_NON_ACCENTUES_INTERDITS

# ---------------------------------------------------------------------------
# Outils communs
# ---------------------------------------------------------------------------


def _extract(text: str, start: int, end: int, before: int = 60, after: int = 60) -> str:
    """Extrait contextualisé autour d'un match, aplati sur une ligne."""
    lo = max(0, start - before)
    hi = min(len(text), end + after)
    snippet = text[lo:hi].replace("\n", " ⏎ ")
    return f"…{snippet}…"


def _find_all(text: str, pattern: re.Pattern[str]) -> list[str]:
    return [_extract(text, m.start(), m.end()) for m in pattern.finditer(text)]


def _ascii_fold(value: str) -> str:
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")


# ---------------------------------------------------------------------------
# R1 — tokens résiduels
# ---------------------------------------------------------------------------

_R1_BRACKETS = re.compile(r"[\[\]]")


def rule_r1_tokens(text: str) -> list[str]:
    """Aucun ``[`` / ``]`` résiduel ; aucun marqueur « (À COMPLÉTER … » (données complètes)."""
    violations = _find_all(text, _R1_BRACKETS)
    if "À COMPLÉTER" in text:
        idx = text.index("À COMPLÉTER")
        violations.append(_extract(text, idx, idx + len("À COMPLÉTER")))
    folded = _ascii_fold(text).upper()
    if "A COMPLETER" in folded:
        idx = folded.index("A COMPLETER")
        violations.append(_extract(text, idx, idx + len("A COMPLETER")))
    return violations


# ---------------------------------------------------------------------------
# R2 — « sous le numéro en cours » (retour récurrent 6×)
# ---------------------------------------------------------------------------

_R2 = re.compile(r"sous le num[ée]ro en cours")


def rule_r2_numero_en_cours(text: str) -> list[str]:
    """« sous le numéro en cours » interdit (RCS non attribué ≠ numéro « en cours »)."""
    return _find_all(text, _R2)


# ---------------------------------------------------------------------------
# R3 — « Docteur » n'est pas une civilité
# ---------------------------------------------------------------------------

_R3 = re.compile(
    r"soussignée?[\s,]+Docteur\b|Président,\s+Docteur\b"
    # R3 durci (Rafael 2026-07-07, siloing attestation pluripersonnelle) : les slots
    # de repartition / d'apport des attestations souscripteurs rendent la civilite
    # CIVILE — « attribuées au Dr X » et « Le Docteur X a fait un apport » interdits.
    r"|attribuées? au Dr\b"
    r"|Le Docteur [^\n]{1,80} a fait"
)


def rule_r3_docteur_civilite(text: str) -> list[str]:
    """« soussigné(e) Docteur » / « Président, Docteur » / « attribuées au Dr X » /
    « Le Docteur X a fait … » interdits.

    La civilité est Monsieur/Madame ; « le Docteur X » comme TITRE ne reste permis
    que là où le modèle source le porte verbatim (statuts art. 6/8, acte « Dr X
    détenant »), jamais dans les slots de civilité (R3 durci Rafael 2026-07-07).
    """
    return _find_all(text, _R3)


# ---------------------------------------------------------------------------
# R4 — linter français non accentué (lexique de base + extensions client)
# ---------------------------------------------------------------------------

# Extensions au lexique de tests/unit/_accents.py (mots sans ambiguïté fautive
# en minuscule/Capitalisé ; les intitulés légaux TOUT-EN-CAPITALES ne matchent pas).
MOTS_SUPPLEMENTAIRES: tuple[str, ...] = (
    # nationalité
    "francais", "Francais", "francaise", "Francaise", "francaises",
    # situation matrimoniale (les formes « marie/mariee » sont contextuelles, cf. regex)
    "celibataire", "Celibataire", "celibataires",
    "pacse", "pacsee", "Pacse", "Pacsee", "pacses", "pacsees",
    "divorcee", "Divorcee", "divorcees",  # masculin « divorce » = nom légitime, exclu
    # réparti (participe ; « repartir » = repartir ailleurs, jamais dans ces actes)
    "reparti", "repartie", "repartis", "reparties", "Reparti", "Repartie",
    # époux / épouse
    "epoux", "epouse", "Epoux", "Epouse",
)

# « marié(e) » sans accent : contextuel pour épargner le prénom « Marie ».
# - minuscule : suivi d'un espace + avec/sous, ou d'une ponctuation.
# - Capitalisé (début de ligne de comparution) : uniquement suivi de avec/sous.
_R4_MARIE = (
    re.compile(r"\bmariee?(?=[.,;]| (?:avec|sous)\b)"),
    re.compile(r"\bMariee?(?= (?:avec|sous)\b)"),
)

_R4_HEURE = re.compile(r"\ba \d+\s*heure")

# Faux positifs de la liste de BASE (constat conformité 2026-07-07) : « acquise » /
# « acquises » sont du français CORRECT (participe d'acquérir, sans accent) — les
# garder flaguerait « parts souscrites ou acquises » dans la moitié des statuts.
# Exclusion locale ; le nettoyage de tests/unit/_accents.py appartient au fix-sprint.
_FAUX_POSITIFS_BASE = frozenset({"acquise", "acquises"})

_R4_WORDS = tuple(
    dict.fromkeys(
        tuple(m for m in MOTS_NON_ACCENTUES_INTERDITS if m not in _FAUX_POSITIFS_BASE)
        + MOTS_SUPPLEMENTAIRES
    )
)
_R4_WORD_PATTERNS = {mot: re.compile(rf"\b{re.escape(mot)}\b") for mot in _R4_WORDS}


def rule_r4_francais_accentue(text: str) -> list[str]:
    """Texte français intégralement accentué (lexique _accents.py + extensions)."""
    violations: list[str] = []
    for mot, pattern in _R4_WORD_PATTERNS.items():
        match = pattern.search(text)
        if match:
            violations.append(f"« {mot} » : {_extract(text, match.start(), match.end())}")
    for pattern in _R4_MARIE:
        for match in pattern.finditer(text):
            violations.append(
                f"« marié » sans accent : {_extract(text, match.start(), match.end())}"
            )
    match = _R4_HEURE.search(text)
    if match:
        violations.append(f"« a NN heures » (à) : {_extract(text, match.start(), match.end())}")
    return violations


# ---------------------------------------------------------------------------
# R5 — groupement des montants (« 60000 » interdit en contexte monétaire)
# ---------------------------------------------------------------------------

# Run de ≥ 5 chiffres : jamais une partie d'un nombre groupé (un nombre groupé n'a
# jamais 5 chiffres consécutifs) ; le lookbehind à 2 caractères écarte la QUEUE d'un
# nombre groupé partiel (« 123 45678 ») sans écarter « de 60000 » (espace seul).
_R5_DIGITS = re.compile(r"(?<!\d)(?<!\d[\s.,\u00a0\u202f])(\d{5,})(?!\d)")
_R5_MONEY_AFTER = re.compile(r"^\s?(?:€|euros?\b)")
_R5_MONEY_BEFORE = re.compile(
    r"(?:capital(?: social)?(?: de| est fixé à| fixé à)|somme de|prix(?: global| total)?"
    r"(?: de| est fixé à| fixé à)?|apporte|apport de|montant de|fixée? à|s['’]élève à)\s*$",
    re.IGNORECASE,
)
_R5_WHITELIST = re.compile(
    r"(?:RPPS|RCS|SIREN|SIRET|RIB|IBAN|n°\s*|num[ée]ro|t[ée]l[ée]phone|t[ée]l\.?)"
    r"[^\n]{0,25}$",
    re.IGNORECASE,
)


def rule_r5_montants_groupes(text: str) -> list[str]:
    """Un montant ≥ 5 chiffres non groupé adjacent à un marqueur monétaire est interdit.

    Liste blanche par contexte : identifiants (RPPS 11 chiffres, SIREN/RCS, numéros,
    téléphone) exclus via le contexte AMONT.
    """
    violations: list[str] = []
    for match in _R5_DIGITS.finditer(text):
        start, end = match.span(1)
        before = text[max(0, start - 45) : start]
        after = text[end : end + 12]
        if _R5_WHITELIST.search(before):
            continue
        monetary = bool(_R5_MONEY_AFTER.search(after)) or bool(_R5_MONEY_BEFORE.search(before))
        if monetary:
            violations.append(_extract(text, start, end))
    return violations


# ---------------------------------------------------------------------------
# R6 — élision « d'un » (« de un euro » interdit)
# ---------------------------------------------------------------------------

_R6 = re.compile(r"\b[dD]e un (?:euro|centime)")


def rule_r6_elision(text: str) -> list[str]:
    """« de un euro » / « de un centime » interdits (élision « d'un » attendue)."""
    return _find_all(text, _R6)


# ---------------------------------------------------------------------------
# R7 — double unité / double titre
# ---------------------------------------------------------------------------

_R7 = re.compile(r"euros? euros?\b|d['’]euro euros?\b|Dr Docteur\b|Docteur Docteur\b")


def rule_r7_double_unite(text: str) -> list[str]:
    """« euro euro », « euros euros », « d'euro euros », « Dr Docteur »,
    « Docteur Docteur » interdits."""
    return _find_all(text, _R7)


# ---------------------------------------------------------------------------
# R8 — double bloc de répartition dans un même acte de cession
# ---------------------------------------------------------------------------

_R8_BLOC_A = "réparti à ce jour comme suit"
_R8_BLOC_B = "actuellement détenu comme suit"


def rule_r8_double_repartition(text: str) -> list[str]:
    """« réparti à ce jour comme suit » ET « actuellement détenu comme suit » dans le
    MÊME document interdits (Albane : un seul bloc de répartition)."""
    if _R8_BLOC_A in text and _R8_BLOC_B in text:
        ia = text.index(_R8_BLOC_A)
        ib = text.index(_R8_BLOC_B)
        return [
            f"bloc 1 : {_extract(text, ia, ia + len(_R8_BLOC_A))}",
            f"bloc 2 : {_extract(text, ib, ib + len(_R8_BLOC_B))}",
        ]
    return []


# ---------------------------------------------------------------------------
# R9 — clause Ordre : le Conseil départemental doit porter un département
# ---------------------------------------------------------------------------

_R9 = re.compile(
    r"communiqué au Conseil départemental de l['’]Ordre(?!\s+(?:de|du|des|d['’]))"
)


def rule_r9_ordre_departement(text: str) -> list[str]:
    """« communiqué au Conseil départemental de l'Ordre » doit porter un nom de
    département (« de l'Ordre de <Nom> »), pas se terminer sans."""
    return _find_all(text, _R9)


# ---------------------------------------------------------------------------
# R10 — nom de fichier des statuts : « Statuts <dénomination>.docx »
# ---------------------------------------------------------------------------

# Retour Rafael 2026-07-07 : « TOUS les documents de statuts doivent être nommés
# "Statuts [Nom de la société]" ». Règle de NOM DE FICHIER (pas de contenu) : tout
# document dont le nom logique contient « statuts » doit s'appeler
# « Statuts <dénomination>.docx » (helper partagé ``statuts_output_filename``).
# Elle reçoit donc le NOM du document, pas son texte (cf. ``FILENAME_RULES``).
_R10_OK = re.compile(r"^Statuts \S.*\.docx$")


def rule_r10_nom_fichier_statuts(doc_name: str) -> list[str]:
    """Un document de statuts est nommé « Statuts <dénomination>.docx »."""
    if "statuts" not in doc_name.casefold():
        return []
    if _R10_OK.match(doc_name):
        return []
    return [f"nom de fichier « {doc_name} » — attendu « Statuts <dénomination>.docx »"]


# ---------------------------------------------------------------------------
# Registre des règles
# ---------------------------------------------------------------------------

RULES: dict[str, Callable[[str], list[str]]] = {
    "R1": rule_r1_tokens,
    "R2": rule_r2_numero_en_cours,
    "R3": rule_r3_docteur_civilite,
    "R4": rule_r4_francais_accentue,
    "R5": rule_r5_montants_groupes,
    "R6": rule_r6_elision,
    "R7": rule_r7_double_unite,
    "R8": rule_r8_double_repartition,
    "R9": rule_r9_ordre_departement,
    "R10": rule_r10_nom_fichier_statuts,
}

# Règles appliquées au NOM DE FICHIER du document (les autres reçoivent le texte).
FILENAME_RULES: frozenset[str] = frozenset({"R10"})

RULE_LABELS: dict[str, str] = {
    "R1": "tokens résiduels ([ ] / À COMPLÉTER)",
    "R2": "« sous le numéro en cours » interdit",
    "R3": "« Docteur » n'est pas une civilité",
    "R4": "français non accentué",
    "R5": "montants ≥ 5 chiffres non groupés",
    "R6": "élision « d'un euro » manquante",
    "R7": "double unité / double titre",
    "R8": "double bloc de répartition (acte)",
    "R9": "clause Ordre sans département",
    "R10": "nom de fichier statuts ≠ « Statuts <dénomination>.docx »",
}
