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
from collections.abc import Callable, Iterable

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

# R3 UNIVERSELLE (Gad 2026-07-09, remise en question) : ne plus lister des PHRASES
# precises (« soussigne Docteur », « au Dr X »…) — chaque nouvelle formulation du meme
# defaut passait au vert (appel_fond « de Docteur X » non liste -> livre a Albane). La LOI
# est : « Docteur » n'est PAS une civilite, Rafael veut « supprime PARTOUT » (07-07 bis +
# 09-07). Donc on interdit le MOT « Docteur » et l'abreviation « Dr » comme titre-devant-nom
# dans TOUTE sortie generee. Defaut = interdit ; toute exception legale reelle = whitelistee
# EXPLICITEMENT ci-dessous (aucune a ce jour). Une nouvelle tournure ne peut plus fuir.
_R3 = re.compile(
    r"\bDocteurs?\b"  # le mot, sous toutes ses formes
    r"|\bDr\b\.?\s+[A-ZÉÈ]"  # « Dr X » / « Dr. X » (abreviation devant un nom propre)
)

# Contextes ou « Docteur » reste LEGITIME = titre professionnel en PROSE (pas une
# civilite). Whitelist EXPLICITE et raisonnee (jamais une liste de phrases a attraper) :
# marqueurs de l'annuaire telephonique du reglement SCM ou le modele source ratifie porte
# « le Docteur <identite> » (message repondeur / rotation) — Rafael 2026-07-09 : « garde
# Docteur UNIQUEMENT pour ca ». Un match dont l'extrait contient l'un de ces marqueurs est
# le titre-pro-en-prose de l'annuaire, autorise ; partout ailleurs « Docteur » reste interdit.
_R3_WHITELIST: tuple[str, ...] = ("joindre", "en charge du message")


def rule_r3_docteur_civilite(text: str) -> list[str]:
    """« Docteur » / « Dr <Nom> » interdits dans TOUTE sortie (loi universelle).

    « Docteur » n'est pas une civilité (Rafael 2026-07-07 puis 2026-07-09 : « supprimé
    partout »). La civilité est Monsieur/Madame ; le titre professionnel « Docteur » ne
    doit apparaître nulle part dans les documents générés. Règle par INTENTION (le mot),
    pas par formulation — sinon une nouvelle tournure fuit (leçon appel_fond 2026-07-09).
    """
    hits = _find_all(text, _R3)
    return [h for h in hits if not any(w in h for w in _R3_WHITELIST)]


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

# Run de ≥ 4 chiffres (Rafael 2026-07-09, live SCS : « 1000 euros » doit sortir
# « 1 000 euros » — seuil abaissé de 5 à 4 chiffres). Un montant correctement groupé n'a
# jamais 4 chiffres consécutifs (« 1 000 » porte un espace) ; le lookbehind à 2 caractères
# écarte la QUEUE d'un nombre groupé partiel (« 12 3456 ») sans écarter « de 1000 ».
_R5_DIGITS = re.compile(r"(?<!\d)(?<!\d[\s.,\u00a0\u202f])(\d{4,})(?!\d)")
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
# Le seuil à 4 chiffres croise les ANNÉES (19xx/20xx) : une année n'est JAMAIS un
# montant à grouper (« le 31 décembre 2026 »). On l'épargne SAUF si une unité monétaire
# la suit directement (jamais le cas d'une date).
_R5_ANNEE = re.compile(r"^(?:19|20)\d{2}$")


def rule_r5_montants_groupes(text: str) -> list[str]:
    """Un montant ≥ 4 chiffres non groupé adjacent à un marqueur monétaire est interdit.

    Liste blanche par contexte : identifiants (RPPS 11 chiffres, SIREN/RCS, numéros,
    téléphone) exclus via le contexte AMONT ; les années (19xx/20xx) épargnées sauf si
    l'unité monétaire les suit directement (jamais le cas d'une date).
    """
    violations: list[str] = []
    for match in _R5_DIGITS.finditer(text):
        digits = match.group(1)
        start, end = match.span(1)
        before = text[max(0, start - 45) : start]
        after = text[end : end + 12]
        if _R5_WHITELIST.search(before):
            continue
        money_after = bool(_R5_MONEY_AFTER.search(after))
        # Une année (19xx/20xx) sans unité monétaire directe -> date, pas un montant.
        if _R5_ANNEE.match(digits) and not money_after:
            continue
        monetary = money_after or bool(_R5_MONEY_BEFORE.search(before))
        if monetary:
            violations.append(_extract(text, start, end))
    return violations


# ---------------------------------------------------------------------------
# R6 — élision « d'un » (« de un euro » interdit)
# ---------------------------------------------------------------------------

# R6 UNIVERSELLE (audit règles 2026-07-09) : « de un » est TOUJOURS fautif en français
# (« un » commence par une voyelle -> élision « d'un » obligatoire), pas seulement devant
# « euro/centime ». On code l'INTENTION (élision manquante) et non la liste euro/centime,
# sinon « de un euro » corrigé mais « de une part » / « de un associé » fuiraient.
_R6 = re.compile(r"\b[dD]e une? \b")


def rule_r6_elision(text: str) -> list[str]:
    """« de un … » / « de une … » interdits : élision « d'un »/« d'une » obligatoire
    (« un »/« une » commencent par une voyelle). Règle par INTENTION, pas liste de mots."""
    return _find_all(text, _R6)


# ---------------------------------------------------------------------------
# R7 — double unité / double titre
# ---------------------------------------------------------------------------

# Rafael 2026-07-09 (lettre avertissement conjoint SPFPL apport) : la double unité
# AUTOUR d'une parenthèse échappait au motif adjacent — « soixante mille euros
# (60 000) euros » et « (soixante mille euros) euros » sont désormais couverts.
_R7 = re.compile(
    r"euros? euros?\b|d['’]euro euros?\b|Dr Docteur\b|Docteur Docteur\b"
    r"|euros?\s*\([\d\s  .,]+\)\s*euros?\b"
    r"|euros?\)\s*euros?\b"
)


def rule_r7_double_unite(text: str) -> list[str]:
    """« euro euro », « euros euros », « d'euro euros », « Dr Docteur »,
    « Docteur Docteur », « euros (60 000) euros », « (… euros) euros » interdits."""
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
# R11 — une DNC PAR GÉRANT personne physique (règle de BUNDLE)
# ---------------------------------------------------------------------------

# Retour Albane (Direction Juridique) + Rafael 2026-07-09 : la déclaration de
# non-condamnation ne se génère QUE pour les GÉRANTS (dirigeants), PAS pour les
# associés non-gérants. Ça SUPERSEDE le retour Rafael du matin « 1 DNC par associé »
# (Rafael a confirmé « Albane a raison »). Règle de BUNDLE (pas de texte) : elle reçoit
# les NOMS des documents d'un bundle + le nombre attendu de GÉRANTS personnes physiques,
# et vérifie que le compte de DNC est exact. Ne figure pas dans RULES (signature
# différente) — appliquée par ``test_r11_dnc_par_gerant``.
#   - civils (SCI / SCI IRIS / SCM / SCS / micro holding), SELARL : 1 gérant.
#   - SELAS : les gérants = les dirigeants (Président + chaque DG / DG Associé).
#   - unipersonnels (SAS, SASU, SELAS uni, SPFPL, SELARL uni) : l'associé unique EST
#     gérant → 1 DNC.
_R11_DNC_PREFIX = "declaration_non_condamnation"


def rule_r11_dnc_par_gerant(
    doc_names: Iterable[str], nb_gerants_pp: int
) -> list[str]:
    """Le bundle porte EXACTEMENT une DNC par GÉRANT personne physique."""
    dnc = sorted(
        name
        for name in doc_names
        if name.startswith(_R11_DNC_PREFIX) and name.endswith(".docx")
    )
    if len(dnc) == nb_gerants_pp:
        return []
    return [
        f"{len(dnc)} DNC générée(s) ({', '.join(dnc) or 'aucune'}) "
        f"pour {nb_gerants_pp} gérant(s) personne physique"
    ]


R11_LABEL = "nb de DNC ≠ nb de gérants personnes physiques"


# ---------------------------------------------------------------------------
# R12 — majuscule en début de paragraphe (Rafael 2026-07-09)
# ---------------------------------------------------------------------------

# Un paragraphe qui commence par une minuscule (latin accentué compris) = violation,
# HORS listes/tirets/plages connues (verbatim Rafael). Concrètement :
#   - listes/tirets : le marqueur « - » est DANS le texte des items (ils ne commencent
#     pas par une lettre minuscule) ; les marqueurs alphabétiques « a) / b) » sont
#     exclus explicitement ;
#   - CONTINUATION de phrase : une minuscule est légitime quand le paragraphe
#     précédent n'a PAS terminé sa phrase (fin sans « . ! ? … » — identités de type
#     DNC « demeurant / fils de », retours à la ligne en milieu de phrase des modèles,
#     énumérations après « : » ou « , »). On ne flague donc qu'une minuscule qui OUVRE
#     une phrase (après un paragraphe terminé par une ponctuation finale) ;
#   - continuations connues même après ponctuation : « la somme de … » (apports
#     SCS/SCM, suite de « - X apporte, ») et les renvois comptables « ci- / ci<TAB> » ;
#   - plage connue : « sous réserve des interdictions légales … » — VERBATIM du modèle
#     source des statuts SEL (typo du modèle, byte-locké ; correction = décision
#     Albane, cf. rapport Rafael 2026-07-09).
_R12_MINUSCULE = re.compile(r"^[a-zà-öø-ÿœ]")
_R12_FIN_DE_PHRASE = re.compile(r"[.!?…]\s*[»\"')]*\s*$")
_R12_EXCEPTIONS = (
    re.compile(r"^la somme de "),
    re.compile(r"^ci[-\s ]"),
    re.compile(r"^[a-z]\)"),  # marqueur d'énumération « a) / b) »
    re.compile(r"^sous réserve des interdictions légales"),  # modèle SEL verbatim
    # Énumérations SANS tiret des modèles sources (items de liste verbatim dont
    # l'item précédent finit par un point) : pacte SCM (bloc adhésion « Déclare : »)
    # et actes de cession de cabinet (liste des éléments cédés).
    re.compile(r"^avoir pris connaissance des termes du pacte"),  # pacte SCM verbatim
    re.compile(r"^les dossiers, archives et informations"),  # actes cession verbatim
)


def rule_r12_majuscule_debut(text: str) -> list[str]:
    """Chaque paragraphe qui OUVRE une phrase commence par une MAJUSCULE (hors
    listes/tirets, continuations de phrase et plages connues des modèles)."""
    violations: list[str] = []
    offset = 0
    previous = ""
    for line in text.split("\n"):
        stripped = line.lstrip(" \t  ")
        starts_sentence = not previous or bool(_R12_FIN_DE_PHRASE.search(previous))
        if (
            stripped
            and starts_sentence
            and _R12_MINUSCULE.match(stripped)
            and not any(pattern.match(stripped) for pattern in _R12_EXCEPTIONS)
        ):
            start = offset + (len(line) - len(stripped))
            violations.append(_extract(text, start, min(start + 40, len(text))))
        if stripped:
            previous = stripped
        offset += len(line) + 1
    return violations


# ---------------------------------------------------------------------------
# R13 — accord euro/euros après un montant SINGULIER (Rafael 2026-07-09)
# ---------------------------------------------------------------------------
#
# « si montant = 1 -> 1 euro, si 100 -> 100 euros » : PARTOUT, tous types, tous
# documents. Appliquée au corpus « montant unitaire = 1 € » (``build_corpus_cap1``) :
# tout « 1 euros » (accord singulier faux), « (1) euros », « un/une euros », « 0 euros »
# (« zéro euro » est singulier en français) est une VIOLATION. « 1 euro » est attendu.
# Le lookbehind écarte la QUEUE d'un nombre plus grand (« 21 euros », « 101 euros »,
# « 1 000 euros » = mille euros -> pluriel légitime, jamais flagués).
_R13_FIGURE = re.compile(r"(?<![\d   ][\d.,])(?<![0-9])([01](?:[.,]0+)?)(?:\s*[)€  ]?\s*)euros\b")
_R13_LETTRES = re.compile(r"\b(une?)\s+euros\b")


def rule_r13_accord_euro(text: str) -> list[str]:
    """Aucun montant singulier (0/1, « un »/« une ») suivi de « euros » (pluriel)."""
    violations = _find_all(text, _R13_FIGURE)
    violations += _find_all(text, _R13_LETTRES)
    return violations


R13_LABEL = "accord euro/euros — « 1 euros » (montant singulier) interdit"


# ---------------------------------------------------------------------------
# R14 — adresse de résidence précédée de « au » (Rafael/Albane 2026-07-09)
# ---------------------------------------------------------------------------
#
# Retour Rafael/Albane 2026-07-09 : « Demeurant [adresse] » -> « Demeurant au
# [adresse] », « il faut adapter à chaque adresse ». Convention UNIVERSELLE : la
# procuration portait déjà « demeurant au » ; statuts, PV, actes, attestations et
# lettre IS ne l'avaient pas. On code l'INTENTION (l'adresse postale de résidence est
# introduite par « au »), JAMAIS une liste de tournures (leçon R3 2026-07-09). Signal
# opérationnel : un « [Dd]emeurant » suivi DIRECTEMENT d'un numéro de voie (chiffre)
# sans « au » = violation. « demeurant à <Ville> » (ville seule, sans numéro de voie)
# reste légitime et n'est jamais flaguée — aucun chiffre ne suit « demeurant » (pas de
# whitelist à écrire). Limite documentée : une adresse à complément NON numérique
# (« Résidence Les Tilleuls, 4 … ») garde « au » par défaut (exigence client) mais
# échappe à CETTE détection ; cas rare, byte-vérifié à la génération.
_R14 = re.compile(r"\b[Dd]emeurant\s+\d")


def rule_r14_demeurant_au(text: str) -> list[str]:
    """« Demeurant <numéro> … » interdit : l'adresse de résidence doit être précédée
    de « au » (« Demeurant au <numéro> … »). Règle par INTENTION (adresse postale
    introduite par « au »), pas liste de tournures. « demeurant à <Ville> » (ville
    seule) reste légitime — aucun chiffre ne suit « demeurant »."""
    return _find_all(text, _R14)


R14_LABEL = "adresse de résidence non précédée de « au » (« Demeurant <numéro> »)"


# ---------------------------------------------------------------------------
# R15 — accord en genre de la FONCTION d'une personne (Rafael 2026-07-09)
# ---------------------------------------------------------------------------
#
# Retour Rafael 2026-07-09 (règlement intérieur SCM) : « Représentée par Madame Alice
# Martin, gérant » -> « gérante ». Convention UNIVERSELLE : une FONCTION rendue pour
# une personne FÉMININE s'accorde au féminin (même classe que né/née). On code
# l'INTENTION (« Madame <Nom>, <fonction au masculin> » = accord manquant), JAMAIS une
# liste de tournures (leçon R3 2026-07-09). Signal : une civilité féminine
# (« Madame »/« Mme »), suivie du nom puis d'une virgule, puis d'une fonction au
# MASCULIN directement = violation. Un homme (« Monsieur <Nom>, gérant ») est LÉGITIME
# et n'est jamais flagué (le motif n'ancre que « Madame »/« Mme » — aucune whitelist à
# écrire). Les formes féminines (« gérante », « présidente », « associée ») échappent
# au motif par la frontière de mot (« gérant\b » ne mord pas « gérante »). La fenêtre
# ne franchit jamais la 1re virgule : seule la fonction ACCOLÉE au nom est visée.
_R15_FONCTION_MASC = (
    r"(?:co-?g[ée]rant|vice-pr[ée]sident|cog[ée]rant|g[ée]rant|pr[ée]sident|associé"
    r"|administrateur|directeur|cofondateur|fondateur|tr[ée]sorier)"
)
_R15 = re.compile(r"\b(?:Madame|Mme)\b[^,\n]{0,40},\s*" + _R15_FONCTION_MASC + r"\b")

# Akainu batch2+3 M1/M2 (2026-07-09) : coder l'INTENTION COMPLÈTE — dans un segment
# « Représentée par … Madame/Mme … », TOUS les termes accordés au représentant féminin
# doivent l'être, pas seulement la fonction. On flag les FUITES masculines résiduelles :
# « domicilié » (participe non accordé, attendu « domiciliée ») et « son <fonction féminine
# à initiale consonne> » (possessif non accordé, attendu « sa gérante »). Segment = une
# ligne « Représentée par … » (les représentés d'un même acte sont sur des lignes distinctes).
_R15_REPR_FEMININ = re.compile(r"Repr[ée]sent[ée]e? par\b[^\n]*\b(?:Madame|Mme)\b[^\n]*")
_R15_DOMICILIE_MASC = re.compile(r"\bdomicilié\b(?!e)")
_R15_SON_FONCTION_FEM = re.compile(
    r"\bson\s+(?:g[ée]rante|pr[ée]sidente|directrice|tr[ée]sori[èe]re|cog[ée]rante"
    r"|administratrice|cofondatrice|fondatrice)\b"
)


def rule_r15_accord_fonction(text: str) -> list[str]:
    """Accord en genre COMPLET du segment « Représentée par … » pour une représentante
    féminine : fonction, participe « domicilié(e) » ET possessif « son/sa ». Règle par
    INTENTION (tout le segment s'accorde), pas liste de tournures — leçon Akainu 2026-07-09
    (« son gérante »/« gérante … domicilié » fuyaient l'ancienne R15). « Monsieur … gérant »
    (masculin) reste légitime."""
    violations = _find_all(text, _R15)
    for segment in _R15_REPR_FEMININ.finditer(text):
        seg = segment.group(0)
        if _R15_DOMICILIE_MASC.search(seg) or _R15_SON_FONCTION_FEM.search(seg):
            violations.append(_extract(text, segment.start(), segment.end()))
    return violations


R15_LABEL = "accord en genre de la fonction (« Madame <Nom>, gérant » interdit)"


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
    # NB : R11 est portée par le chantier DNC parallèle (2026-07-09) — numérotation
    # réservée, ne pas réutiliser.
    "R12": rule_r12_majuscule_debut,
    # R13 tourne sur le corpus cap1 séparé (test_r13_accord_euro), pas ici.
    "R14": rule_r14_demeurant_au,
    "R15": rule_r15_accord_fonction,
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
    "R12": "paragraphe commençant par une minuscule",
    "R14": "adresse de résidence non précédée de « au »",
    "R15": "accord en genre de la fonction (« Madame <Nom>, gérant »)",
}
