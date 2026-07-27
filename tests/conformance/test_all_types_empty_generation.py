"""KAN-2 @All — Garde de conformité : TOUT type de document se génère SANS AUCUN champ.

Verbatim (Rafael, rejeté 2×) : « Tous les documents doivent pouvoir être générés, même si je ne
remplis AUCUN champ dans le générateur. » Champ vide -> marqueur « (À COMPLÉTER : <libellé> ) »,
JAMAIS un crash, JAMAIS une valeur inventée.

CE GARDE EST L'ORACLE @All. Il génère, pour CHAQUE structure atteignable au front, un dossier à
partir d'un payload VIDE FIDÈLE — c.-à-d. exactement ce que le vrai front Streamlit envoie quand
l'opérateur ne touche à rien :

    * nombre  = 0     (``st.number_input`` non touché pose 0, PAS None) ;
    * texte   = ""    ;
    * date    = None  ;
    * booléen / enum / sélecteur de routage = conservés (c'est le TYPE de doc, pas un champ saisi).

C'est la LEÇON CLÉ des rejets : un helper qui ne traite que ``None`` comme vide laisse fuir le 0
(« divisé en zéro (0) actions », « composé de 0 parts », « la somme de 0 euros »). Vider fidèlement
(nombres=0) est donc ce qui fait apparaître les leaks — d'où ce garde.

Pour chaque structure, il asserte sur TOUT le texte de TOUS les docx (paragraphes ET cellules) :

  * aucun CRASH (le dossier se génère, des docx sont produits) ;
  * aucune QUANTITÉ chiffrée affirmée (« N actions/parts/titres », « (0) … », « 0 actions ») ;
  * aucun « zéro » (mise en lettres d'une quantité nulle) ;
  * aucun « 0 euros » affirmé — HORS le boilerplate structurel de l'apport SPFPL (numéraire nul
    par construction : le capital de la holding est constitué par l'apport EN NATURE des titres) ;
  * aucune civilité INVENTÉE (« Je soussigné Monsieur … » alors que rien n'est saisi) — seules
    restent les civilités STRUCTURELLES / boilerplate (filiation père=Monsieur / mère=Madame ;
    salutation du courrier à l'Ordre « Monsieur le Président » ; mandataire du cabinet par défaut) ;
  * aucun MARQUEUR TECHNIQUE dans « (À COMPLÉTER : …) » — que des libellés métier lisibles, jamais
    un point, un underscore, un chiffre d'index ni une casse de token.

Couvre les 13 familles (14 cas, SELARL et SPFPL comptant deux variantes chacun) : SAS, SASU_HOLDING,
SELAS multi + uni dentiste + uni médecin, SPFPL cession + apport, SCI, SCI IRIS, SCM, SCS,
MICRO_HOLDING, SELARL uni + multi.
"""

from __future__ import annotations

import re
import sys
from datetime import date, datetime
from enum import Enum
from pathlib import Path

import pytest
from docx import Document
from pydantic import BaseModel

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT / "tests" / "unit"))

import test_multi_type_front as mtf  # noqa: E402
import test_sasu_holding_plan as sasu_tests  # noqa: E402

from sydel_doc_engine.domain.models import (  # noqa: E402
    StatutsCivilsAssocie,
    StatutsCivilsParts,
)
from sydel_doc_engine.front_app import (  # noqa: E402
    civil_statuts_slice as css,
)
from sydel_doc_engine.front_app import (  # noqa: E402
    sas_slice,
    sasu_holding_slice,
    selas_multi_slice,
    spfpl_slice,
)
from sydel_doc_engine.front_app import (  # noqa: E402
    selas_uni_dentiste_slice as sud,
)
from sydel_doc_engine.front_app import (  # noqa: E402
    selas_uni_medecin_slice as sum_,
)
from sydel_doc_engine.front_app.civil_statuts_slice import CIVIL_TYPE_BY_STRUCTURE  # noqa: E402
from sydel_doc_engine.front_app.field_derivations import (  # noqa: E402
    DEFAULT_MANDATAIRE_NOM,
    DEFAULT_MANDATAIRE_PRENOM,
)
from sydel_doc_engine.front_app.selarl_slice import (  # noqa: E402
    SelarlSliceInput,
    generate_selarl_dossier,
)

# --------------------------------------------------------------------------- #
# Recette d'un payload VIDE FIDÈLE (nombres=0, textes="", dates=None)
# --------------------------------------------------------------------------- #

# Clés à préserver même « à vide » : ce sont des SÉLECTEURS de routage / discriminants (le TYPE de
# document ou de personne, l'accord de genre), pas des champs saisis par l'opérateur.
_SELECTEURS = frozenset(
    {
        "structure",
        "operation",
        "operation_spfpl_type",
        "is_apport",
        "statuts_type",
        "type_personne",
        "role_statutaire",
        "genre",
        "type",
    }
)


def _empty(value: object, key: str | None = None) -> object:
    """Vide FIDÈLEMENT une valeur selon son type (miroir de ce que pose un front non rempli)."""
    if key in _SELECTEURS:
        return value
    if isinstance(value, bool) or isinstance(value, Enum):
        return value
    if isinstance(value, str):
        return ""
    if isinstance(value, (int, float)):
        return 0
    if isinstance(value, (date, datetime)):
        return None
    if value is None:
        return None
    if isinstance(value, BaseModel):
        return value.model_copy(
            update={
                name: _empty(getattr(value, name), name)
                for name in value.__class__.model_fields
            }
        )
    if isinstance(value, dict):
        return {sub_key: _empty(sub_value, sub_key) for sub_key, sub_value in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)(_empty(item) for item in value)
    return value


def _empty_payload(builder_result: dict) -> dict:
    return {key: _empty(value, key) for key, value in builder_result.items()}


def _civil_empty(structure: str, nb_associes: int) -> dict:
    # Payload civil minimal : le sélecteur `structure` + `statuts_type` + N associés VIDES
    # (`StatutsCivilsAssocie()` = tous champs à leur défaut « non rempli »).
    return {
        "structure": structure,
        "statuts_type": CIVIL_TYPE_BY_STRUCTURE[structure][0],
        "associes": [StatutsCivilsAssocie() for _ in range(nb_associes)],
    }


def _selarl_empty(multi: bool) -> SelarlSliceInput:
    # SELARL : l'entrée est un `SelarlSliceInput` (tous champs à leur défaut vide/0/None). En multi,
    # un membre additionnel VIDE (nb_parts=0) — le vrai front pose 0 sur ce `number_input`.
    if multi:
        return SelarlSliceInput(
            dossier_type_key="selarl_v1",
            dossier_unipersonnel=False,
            membres_additionnels=(StatutsCivilsAssocie(parts=StatutsCivilsParts(nb=0)),),
        )
    return SelarlSliceInput(dossier_type_key="selarl_v1")


# (label, callable(output_dir) -> liste de chemins docx). SCS / SCI IRIS / SCM utilisent 2
# associés : SCS/SCI IRIS l'exigent (bloc régime / personne morale IRIS), et SCM à 2 associés
# exerce les SATELLITES (pacte + liste des dépenses) — là où vit le leak « composé de 0 parts ».
_CAS: tuple[tuple[str, object], ...] = (
    ("SAS", lambda out: sas_slice.generate_dossier(_empty_payload(mtf._sas_payload()), out)),
    (
        "SASU_HOLDING",
        lambda out: sasu_holding_slice.generate_dossier(_empty_payload(sasu_tests._payload()), out),
    ),
    (
        "SELAS multi",
        lambda out: selas_multi_slice.generate_dossier(_empty_payload(mtf._selas_payload()), out),
    ),
    (
        "SELAS uni dentiste",
        lambda out: sud.generate_dossier(_empty_payload(mtf._selas_uni_payload()), out),
    ),
    (
        "SELAS uni medecin",
        lambda out: sum_.generate_dossier(_empty_payload(mtf._selas_uni_medecin_payload()), out),
    ),
    (
        "SPFPL cession",
        lambda out: spfpl_slice.generate_dossier(
            _empty_payload(mtf._spfpl_payload("SPFPL cession")), out
        ),
    ),
    (
        "SPFPL apport",
        lambda out: spfpl_slice.generate_dossier(
            _empty_payload(mtf._spfpl_payload("SPFPL apport")), out
        ),
    ),
    ("SCI", lambda out: css.generate_dossier(_civil_empty("SCI", 1), out)),
    ("SCI IRIS", lambda out: css.generate_dossier(_civil_empty("SCI IRIS", 2), out)),
    ("SCM", lambda out: css.generate_dossier(_civil_empty("SCM", 2), out)),
    ("SCS", lambda out: css.generate_dossier(_civil_empty("SCS", 2), out)),
    ("MICRO_HOLDING", lambda out: css.generate_dossier(_civil_empty("MICRO_HOLDING", 1), out)),
    ("SELARL uni", lambda out: generate_selarl_dossier(_selarl_empty(multi=False), out)),
    ("SELARL multi", lambda out: generate_selarl_dossier(_selarl_empty(multi=True), out)),
)


# --------------------------------------------------------------------------- #
# Lecture du texte + assertions par CONCEPT
# --------------------------------------------------------------------------- #


def _all_text(paths) -> str:
    lines: list[str] = []
    for path in paths:
        document = Document(str(path))
        lines.extend(p.text for p in document.paragraphs)
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    lines.extend(p.text for p in cell.paragraphs)
    return "\n".join(lines)


# Quantité de titres AFFIRMÉE en chiffres — on code le CONCEPT « quantité de titres », au
# SINGULIER comme au pluriel (« 600 actions », « 0 part », « 1 titre », « 102 000 titres »).
_TITRES = r"(?:actions?|parts?(?:\s+sociales?)?|titres?)"
_QUANTITE_CHIFFREE = re.compile(rf"\b\d[\d\s]*\s+{_TITRES}\b")
# « (0) actions » / « 0 part » explicitement nuls (singulier + pluriel).
_ZERO_QUANTITE = re.compile(rf"\(0\)\s*{_TITRES}|(?<!\d)0\s+{_TITRES}\b")
# « zéro » (mise en lettres d'une quantité nulle) — aucun acte à vide ne doit l'affirmer.
_ZERO_LETTRES = re.compile(r"\bz[ée]ro\b", re.IGNORECASE)
# Montant NUL affirmé — on code l'UNITÉ monétaire (« euro(s) », symbole « € », code « EUR »),
# pas la seule tournure « euros » (un « 10 euros » n'est pas touché grâce au lookbehind).
_ZERO_EUROS = re.compile(r"(?<!\d)0\s*(?:€|EUR\b|euros?\b)")
# Boilerplate LÉGITIME : dans un APPORT SPFPL, le numéraire est structurellement nul (le capital
# est constitué par l'apport EN NATURE des titres) -> « Apports en numéraire : 0 euro » est correct.
_APPORT_NUMERAIRE_NUL = "Apports en numéraire : 0 euro"
# Marqueur métier ; un marqueur TECHNIQUE (point / underscore / chiffre d'index / casse de token)
# est un défaut (le client relit « (À COMPLÉTER : associes_cible0.prenom ) » sans comprendre).
_MARQUEUR = re.compile(r"\(À COMPLÉTER : ([^)]*)\)")


def _marqueurs_techniques(text: str) -> list[str]:
    return [
        match.group(0)
        for match in _MARQUEUR.finditer(text)
        if (
            "." in match.group(1)
            or "_" in match.group(1)
            or re.search(r"\d", match.group(1))
            or re.search(r"[a-z][A-Z]{2}", match.group(1))
        )
    ]


def _civilites_inventees(text: str) -> list[str]:
    """Civilités « Monsieur »/« Madame » qui ne relèvent PAS d'un usage STRUCTUREL légitime.

    Whitelist explicite et raisonnée (règle 68 : l'exception se whiteliste, elle ne se devine pas) :
      * FILIATION — « fils/fille de Monsieur <père> et de Madame <mère> » : le père est toujours
        Monsieur, la mère toujours Madame (structurel, pas une civilité du client saisie) ;
      * SALUTATION du courrier à l'Ordre — « Monsieur le Président » / « Madame la Présidente »
        (adresse conventionnelle du destinataire, avec bascule de genre à l'UI) ;
      * MANDATAIRE du cabinet par défaut — « Monsieur <Jordan ELBAZ> » (constante métier
        DEFAULT_MANDATAIRE, le clerc qui effectue les formalités, jamais le client).
    Toute autre occurrence = civilité INVENTÉE pour le client (dont on n'a rien saisi) -> défaut.
    """
    prenom = re.escape(DEFAULT_MANDATAIRE_PRENOM)
    nom = re.escape(DEFAULT_MANDATAIRE_NOM)
    suspects: list[str] = []
    # Pas de \b de FIN : une civilité collée à un token (« Monsieur0000 », « Madame_____ ») est
    # justement le cas qui fuyait — on veut l'attraper (règle 68 §3 : coder le concept, pas la
    # tournure « bien espacée »).
    for match in re.finditer(r"\b(?:Monsieur|Madame|Mesdames|Messieurs)", text):
        before = text[max(0, match.start() - 4) : match.start()]
        after = text[match.end() : match.end() + 60]
        if after.startswith(("_", "/")):  # blanc de formulaire (« Monsieur____ ») / alternative
            continue  # « Madame/Monsieur____ » de l'Acte d'Adhésion = modèle blanc à remplir main
        if before.endswith(("de ", "De ")):  # filiation père/mère
            continue
        if re.match(r"\s+(?:le Président|la Présidente)", after):  # salutation courrier Ordre
            continue
        if re.match(rf"\s+{prenom}\s+{nom}", after):  # mandataire du cabinet par défaut
            continue
        suspects.append(text[max(0, match.start() - 20) : match.end() + 25].strip())
    return suspects


def _signature_blancs(paths) -> list[str]:
    """Blanc silencieux : ancre de signature NUE (« Fait à » / « Le » suivi de RIEN) ou adresse
    aux sous-champs vides (« demeurant au ,, »). Un champ absent doit sortir en MARQUEUR, jamais
    laisser une étiquette pendante. « Le » nu est TOLÉRÉ dans les STATUTS (fidélité modèle
    ratifiée : « Le » suivi du signataire, date volontairement absente). Couvre la classe qui a
    récidivé et qu'aucun autre test mécanique ne verrouille (KAN-36 = pagination seule)."""
    problems: list[str] = []
    for path in paths:
        name = path.name.lower()
        is_statuts = "statuts" in name  # « Le » nu ratifié (suivi du signataire)
        # L'Acte d'Adhésion (annexe du pacte SCM) est un FORMULAIRE blanc à remplir à la main :
        # « Fait à » / « Le » nus y sont fidèles au modèle source (non-défaut, confirmé Akainu).
        is_pacte_annexe = "pacte" in name
        document = Document(str(path))
        units = [p.text for p in document.paragraphs]
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    units.extend(p.text for p in cell.paragraphs)
        for unit in units:
            stripped = unit.strip()
            if stripped in ("Fait à", "Fait à,") and not is_pacte_annexe:
                problems.append(f"{path.name}: « Fait à » nu")
            elif stripped in ("Le", "le") and not is_statuts and not is_pacte_annexe:
                problems.append(f"{path.name}: « Le » nu")
            if re.search(r",\s*,", unit):  # adresse aux sous-champs vides
                problems.append(f"{path.name}: adresse nue {stripped[:40]!r}")
    return problems


@pytest.mark.parametrize("label,generate", _CAS, ids=[label for label, _ in _CAS])
def test_type_generates_from_empty_form(label: str, generate, tmp_path: Path) -> None:
    out = tmp_path / re.sub(r"[^\w]+", "_", label)
    out.mkdir(parents=True, exist_ok=True)

    # (1) aucun CRASH + des documents produits.
    generated = generate(out)
    paths = list(generated.docx_paths)
    assert paths, f"{label} à vide : aucun document généré"

    text = _all_text(paths)

    # (2) aucune quantité de titres CHIFFRÉE / nulle affirmée (marqueur attendu).
    quantite = _QUANTITE_CHIFFREE.findall(text) + _ZERO_QUANTITE.findall(text)
    assert not quantite, (
        f"{label} à vide : quantité de titres affirmée (marqueur attendu) : "
        f"{sorted(set(quantite))[:4]}"
    )

    # (3) aucun « zéro » en toutes lettres (« divisé en zéro (…) actions »).
    zero = _ZERO_LETTRES.findall(text)
    assert not zero, f"{label} à vide : « zéro » affirmé en toutes lettres (marqueur attendu)"

    # (4) aucun « 0 euros » affirmé, hors le boilerplate structurel de l'apport SPFPL (num. nul).
    euros = [
        line
        for line in text.splitlines()
        if _ZERO_EUROS.search(line) and _APPORT_NUMERAIRE_NUL not in line
    ]
    assert not euros, f"{label} à vide : « 0 euros » affirmé (marqueur attendu) : {euros[:2]}"

    # (5) aucune civilité INVENTÉE pour le client (restent filiation / salutation / mandataire).
    civilites = _civilites_inventees(text)
    assert not civilites, (
        f"{label} à vide : civilité INVENTÉE (marqueur attendu) : {sorted(set(civilites))[:3]}"
    )

    # (6) aucun marqueur TECHNIQUE : que des libellés métier lisibles.
    techniques = _marqueurs_techniques(text)
    assert not techniques, (
        f"{label} à vide : marqueur(s) TECHNIQUE(S) (libellé métier attendu) : "
        f"{sorted(set(techniques))[:4]}"
    )

    # (7) aucun BLANC de signature (« Fait à »/« Le » nu) ni adresse « ,, » — le champ absent sort
    # en marqueur ; « Le » nu reste toléré dans les statuts (fidélité ratifiée).
    blancs = _signature_blancs(paths)
    assert not blancs, (
        f"{label} à vide : blanc silencieux de signature (marqueur attendu) : "
        f"{sorted(set(blancs))[:4]}"
    )
