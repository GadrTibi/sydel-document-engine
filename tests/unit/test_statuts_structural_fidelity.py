"""Verrou de fidelite STRUCTURELLE par type.

Garantit que TOUTES les en-tetes d'articles/titres (ARTICLE..., TITRE...) du MODELE
SOURCE apparaissent dans les statuts generes, en nombre exact et accents preserves.

Niveau de garantie : structure complete (aucun article supprime / renomme / desaccentue
dans son titre, aucun article en trop ou en moins). Ce verrou COMPLETE — il ne remplace
pas — le verrou ligne-par-ligne complet que seul SELARL medecin possede aujourd'hui
(`test_lot_04_statuts_sel_exercice.py`). Combine aux tests de generation propre
(`test_multi_type_front.py` : zero placeholder residuel + set de fichiers exact par type),
il protege chaque type contre la regression #1 signalee a l'audit : une clause/un article
perdu, ajoute ou altere par les blocs reinjectes.

Il ne prouve PAS l'egalite ligne-par-ligne du CORPS des articles (une paraphrase a
l'interieur d'un article ne serait pas attrapee ici) — c'est le perimetre du verrou
ligne-par-ligne, a generaliser type par type.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pytest
from docx import Document

# Payloads representatifs deja valides par les tests de generation propre.
from test_multi_type_front import (  # type: ignore[import-not-found]
    _civil_base,
    _pm,
    _pp,
    _sas_payload,
    _selas_payload,
    _spfpl_payload,
)

from sydel_doc_engine.front_app import (
    civil_statuts_slice as css,
)
from sydel_doc_engine.front_app import (
    sas_slice,
    selas_multi_slice,
    spfpl_slice,
)

_LOT4 = Path("project/source_documents/lot_04")
_HEADING_RE = re.compile(r"^\s*(ARTICLE|TITRE)\b", re.IGNORECASE)

# Transformations d'en-tetes INTENTIONNELLES, sanctionnees par retour client, par type de
# statuts. Le rendu remplace l'en-tete SOURCE (cle) par sa version transformee (valeur) ; le
# verrou de fidelite verifie donc la presence de la VERSION TRANSFORMEE, pas du verbatim source.
# Tout le reste des en-tetes doit rester verbatim.
# NB cles : depuis R10 (Rafael 2026-07-07), les fichiers statuts portent la DENOMINATION
# (« Statuts <denomination>.docx ») — plusieurs cas partagent le meme nom (SAS et SPFPL
# rendent tous « Statuts SPFPL MARTIN.docx ») -> les dicts sont keyes par CASE_KEY (id du
# cas parametrique), plus par nom de fichier.
_HEADING_TRANSFORMS: dict[str, dict[str, str]] = {
    # ST7g (Albane 2026-06-26) : les titres a casse cassee du modele medecin (art. 16/17/22)
    # sont mis en MAJUSCULES integrales (cf. _SELAS_MEDECIN_BROKEN_TITLE_SOURCES du generateur).
    "SELAS-multi": {
        "ARTICLE 16 – des DECISIONS sociales": "ARTICLE 16 – DES DECISIONS SOCIALES",
        "ARTICLE 17 - CONVENTIONS ENTRE leS DIRIgerantS ou les associes et la societe": (
            "ARTICLE 17 - CONVENTIONS ENTRE LES DIRIGERANTS OU LES ASSOCIES ET LA SOCIETE"
        ),
        "ARTICLE 22 – variation du capital": "ARTICLE 22 – VARIATION DU CAPITAL",
    },
}


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def _source(*tokens: str, exclude: str | None = None) -> Path:
    for path in _LOT4.glob("*.docx"):
        name = _nfc(path.name).upper()
        if all(t.upper() in name for t in tokens) and (
            exclude is None or exclude.upper() not in name
        ):
            return path
    raise FileNotFoundError(f"modele source introuvable pour {tokens}")


def _headings(path: Path) -> list[str]:
    out: list[str] = []
    for para in Document(path).paragraphs:
        text = _nfc(para.text).strip()
        if _HEADING_RE.match(text) and "[" not in text:
            out.append(re.sub(r"\s+", " ", text))
    return out


def _gen_statuts(generated, name_part: str) -> Path:
    for path in generated.docx_paths:
        if name_part in path.name:
            return path
    raise FileNotFoundError(f"statuts {name_part} absent du dossier genere")


# (fonction de generation -> GeneratedDossier, fragment du nom de fichier statuts,
#  resolveur du modele source, case_key = cle des dicts transforms/allowlist)
# R10 (Rafael 2026-07-07) : TOUS les fichiers statuts portent la denomination du payload
# (« Statuts <denomination>.docx », helper partage statuts_output_filename).
_CASES = [
    pytest.param(
        lambda d: css.generate_dossier(
            _civil_base("SCI", "sci", [_pp("Jean", "Durand", 100, 1, 100, 1000)]), d
        ),
        "Statuts SCI EXEMPLE.docx",
        lambda: _source("Modèle statuts SCI", exclude="IRIS"),
        "SCI",
        id="SCI",
    ),
    pytest.param(
        lambda d: css.generate_dossier(
            _civil_base(
                "SCI IRIS",
                "sci_iris",
                [_pm(40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
            ),
            d,
        ),
        "Statuts SCI IRIS EXEMPLE.docx",
        lambda: _source("SCI IRIS"),
        "SCI-IRIS",
        id="SCI-IRIS",
    ),
    pytest.param(
        lambda d: css.generate_dossier(
            _civil_base(
                "SCS",
                "scs",
                [
                    _pp("Jean", "Durand", 60, 1, 60, 600, role="commandite"),
                    _pp("Alice", "Martin", 40, 61, 100, 400, role="commanditaire"),
                ],
            ),
            d,
        ),
        "Statuts SCS EXEMPLE.docx",
        lambda: _source("SCS"),
        "SCS",
        id="SCS",
    ),
    pytest.param(
        lambda d: css.generate_dossier(
            _civil_base(
                "SCM",
                "scm",
                [_pm(70, 1, 70, 700), _pp("Alice", "Martin", 30, 71, 100, 300)],
            ),
            d,
        ),
        "Statuts SCM EXEMPLE.docx",
        lambda: _source("Statuts SCM"),
        "SCM",
        id="SCM",
    ),
    pytest.param(
        lambda d: sas_slice.generate_dossier(_sas_payload(), d),
        "Statuts SPFPL MARTIN.docx",
        lambda: _source("SAS", "medecins"),
        "SAS",
        id="SAS",
    ),
    pytest.param(
        lambda d: spfpl_slice.generate_dossier(_spfpl_payload("SPFPL cession"), d),
        "Statuts SPFPL MARTIN.docx",
        lambda: _source("SPFPLAS", "cession"),
        "SPFPL-cession",
        id="SPFPL-cession",
    ),
    pytest.param(
        lambda d: spfpl_slice.generate_dossier(_spfpl_payload("SPFPL apport"), d),
        "Statuts SPFPL MARTIN.docx",
        lambda: _source("SPFPLAS", "apport"),
        "SPFPL-apport",
        id="SPFPL-apport",
    ),
    pytest.param(
        lambda d: selas_multi_slice.generate_dossier(_selas_payload(), d),
        # ST1 (Albane 2026-06-26) : le fichier statuts porte desormais la denomination
        # (« Statuts SELAS EXEMPLE.docx »), comme les autres types nommes (cf. SCS).
        "Statuts SELAS EXEMPLE.docx",
        lambda: _source("SELAS", "multi"),
        "SELAS-multi",
        id="SELAS-multi",
    ),
]


@pytest.mark.parametrize("generate, statuts_name, source_resolver, case_key", _CASES)
def test_statuts_source_headings_all_present(
    tmp_path: Path, generate, statuts_name: str, source_resolver, case_key: str
) -> None:
    generated = generate(tmp_path)
    statuts_path = _gen_statuts(generated, statuts_name)

    transforms = _HEADING_TRANSFORMS.get(case_key, {})
    # On applique les transformations sanctionnees a l'en-tete SOURCE avant comparaison : le
    # rendu doit porter la version transformee (ST7g : MAJUSCULES), pas le verbatim a casse cassee.
    source_headings = [transforms.get(h, h) for h in _headings(source_resolver())]
    generated_headings = _headings(statuts_path)
    generated_set = set(generated_headings)

    missing = [h for h in source_headings if h not in generated_set]
    assert not missing, (
        f"{statuts_name} : en-tetes du modele source absentes du genere : {missing}"
    )
    # Aucun article en trop ni en moins : le nombre d'en-tetes coincide.
    assert len(generated_headings) == len(source_headings), (
        f"{statuts_name} : {len(generated_headings)} en-tetes generees "
        f"vs {len(source_headings)} au modele source"
    )


# --- Verrou ligne-par-ligne du CORPS (chantier fidelite, Bilan 2026-06-24) -----------------
# Generalise a tous les types statuts le verrou ligne-par-ligne que seul SELARL medecin avait.
# Toute ligne de corps STATIQUE du modele (sans placeholder [...]) doit apparaitre dans le rendu
# -> attrape une clause perdue ou PARAPHRASEE a l'interieur d'un article (invisible au verrou
# en-tetes). Les lignes intentionnellement absentes (blocs reinjectes dynamiquement, ou lignes
# supprimees par decision client) sont allowlistees PAR TYPE avec raison.

# Marqueurs (substring) des lignes du modele LEGITIMEMENT absentes du rendu, par CASE_KEY (cf.
# note _HEADING_TRANSFORMS : les noms de fichiers R10 ne sont plus uniques), avec raison.
# Une ligne source manquante n'echoue PAS si elle contient l'un de ces marqueurs. Tout le RESTE
# du corps statique doit apparaitre verbatim.
_BODY_ALLOWLIST: dict[str, tuple[str, ...]] = {
    # O24-01 (Rafael) : lignes d'annexe « lettre de mission » + « acompte des honoraires » du
    # cabinet Sydel, supprimees de TOUS les statuts a la demande du client.
    "SCI": ("lettre de mission", "acompte des honoraires"),
    "SCI-IRIS": ("lettre de mission", "acompte des honoraires"),
    # KAN-3 (Albane 2026-07-13) : le tiret solo en tete du 1er alinea de l'art. 10 (« - Le
    # capital social peut etre augmente… », numId upperRoman dans le modele) est RETIRE a la
    # demande d'Albane -> la ligne SOURCE avec tiret n'apparait plus verbatim (sa version sans
    # tiret est presente). Retour ratifie qui supersede la fidelite modele (regle 68).
    "SPFPL-cession": (
        "lettre de mission",
        "acompte des honoraires",
        "Le capital social peut être augmenté ou réduit",
    ),
    # KAN-3 (Albane 2026-07-13) — divergences RATIFIEES vs modele apport (regle 68) :
    #  · art. 10 : tiret solo retire (comme cession) ;
    #  · art. 22 : typo source « l'objet <lesdites conventions » corrigee en « desdites » ;
    #  · art. 23 : ligne modele fusionnant l'intro et le 1er item (« … suivantes : Approbation
    #    des comptes annuels … ») SCINDEE en intro + item puce (mise en page coherente).
    "SPFPL-apport": (
        "Le capital social peut être augmenté ou réduit",
        "lesdites conventions",
        "prendre les décisions suivantes : Approbation des comptes annuels",
        # KAN-3 / gate Akainu M1 (2026-07-16) : l'art. 23 « decisions collectives » du MODELE
        # SOURCE apport fusionnait les decisions en 7 puces a la ponctuation cassee (« ; » colles,
        # derniere en « ; »). Le fix les a scindees en 11 puces PROPRES, alignees sur la cession
        # ratifiee (le ticket demandait « il manque des puces »). Le modele source est donc
        # SUPERSEDE sur ces 4 lignes fusionnees (code = verite, cf. migration-models-stale-code).
        "Nomination des Commissaires aux comptes;",
        "actif; Dissolution et liquidation",
        "actions ; Augmentation des engagements des associés;",
        "dirigeants ; Modification des statuts, sauf transfert du siège social ;",
    ),
    # ST7g (Albane 2026-06-26) : titres art. 16/17/22 a casse cassee RENDUS en MAJUSCULES
    # integrales (transformation sanctionnee, cf. _HEADING_TRANSFORMS) -> la ligne SOURCE a casse
    # cassee n'apparait plus verbatim (sa version MAJUSCULES est presente, verifiee par le verrou
    # d'en-tetes). Marqueurs = segments distinctifs de la casse source.
    # DOUBLON-PRESIDENT (Albane 2026-06-26) : la DESIGNATION NOMINATIVE du president (« est
    # nomme(e) president(e) ... ») et le paragraphe de REMUNERATION qui suit ont ete RETIRES du
    # statut a la demande d'Albane (le PV de nomination reste le seul a nommer nominativement le
    # dirigeant ; pas de doublon). La clause GENERIQUE de gerance reste presente et verifiee.
    "SELAS-multi": (
        "lettre de mission",
        "acompte des honoraires",
        "des DECISIONS sociales",
        "ENTRE leS DIRIgerantS",
        "variation du capital",
        "est nommée présidente de la Société et ce pour une durée illimitée",
        "Sa rémunération sera fixée ultérieurement",
    ),
    # SCM : O24-01 + « ci- 510 € » = valeur d'EXEMPLE du modele (montant reinjecte dynamiquement) ;
    # « Faire preceder » / « Lu et approuve » = artefact du modele source SCM (texte de la mention
    # de signature DUPLIQUE dans un meme paragraphe), rendu de-duplique cote sortie.
    "SCM": (
        "lettre de mission",
        "acompte des honoraires",
        "ci- 510",
        "Faire précéder",
        "Lu et approuvé",
    ),
}


def _normalized_full_text(path: Path) -> str:
    parts: list[str] = []
    document = Document(path)
    for para in document.paragraphs:
        parts.append(para.text)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    parts.append(para.text)
    return re.sub(r"\s+", " ", _nfc("\n".join(parts)))


def _static_body_lines(path: Path) -> list[str]:
    out: list[str] = []
    for para in Document(path).paragraphs:
        text = re.sub(r"\s+", " ", _nfc(para.text).strip())
        if text and "[" not in text and "]" not in text:
            out.append(text)
    return out


@pytest.mark.parametrize("generate, statuts_name, source_resolver, case_key", _CASES)
def test_statuts_source_body_lines_present(
    tmp_path: Path, generate, statuts_name: str, source_resolver, case_key: str
) -> None:
    generated = generate(tmp_path)
    statuts_path = _gen_statuts(generated, statuts_name)
    output = _normalized_full_text(statuts_path)
    allow = _BODY_ALLOWLIST.get(case_key, ())
    missing = [
        line
        for line in _static_body_lines(source_resolver())
        if line not in output and not any(marker in line for marker in allow)
    ]
    assert not missing, (
        f"{statuts_name} : {len(missing)} ligne(s) de corps du modele perdues/paraphrasees "
        f"(non rendues, non allowlistees) : {missing[:8]}"
    )


def test_statuts_civil_first_page_formatting_matches_source(tmp_path: Path) -> None:
    # R22-06 (Rafael 2026-06-22, « toute la première page ») : la 1re page des statuts
    # civils doit respecter la mise en forme de la source -> en-tete CENTRE, « LES
    # SOUSSIGNES » gras+souligne, identite du comparant en gras. Le moteur partage les
    # aplatissait en justifie Normal.
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    generated = css.generate_dossier(
        _civil_base(
            "SCI IRIS",
            "sci_iris",
            [_pm(40, 1, 40, 400), _pp("Alice", "Martin", 60, 41, 100, 600)],
        ),
        tmp_path,
    )
    doc = Document(_gen_statuts(generated, "Statuts SCI IRIS EXEMPLE.docx"))
    paras = [p for p in doc.paragraphs if p.text.strip()]

    def find(prefix: str):
        return next(p for p in paras if _nfc(p.text).strip().startswith(prefix))

    # En-tete CENTRE (forme sociale, capital, siege).
    assert find("Au Capital").alignment == WD_ALIGN_PARAGRAPH.CENTER
    assert find("Siège Social").alignment == WD_ALIGN_PARAGRAPH.CENTER
    # « LES SOUSSIGNES » en gras + souligne.
    soussignes = find("LES SOUSSIGNES")
    assert any(r.bold for r in soussignes.runs)
    assert any(r.underline for r in soussignes.runs)
    # Identite du comparant (ligne de nom) en gras.
    assert any(r.bold for r in find("SEL IRIS").runs)
