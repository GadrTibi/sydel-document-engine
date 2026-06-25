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


# (label, fonction de generation -> GeneratedDossier, fragment du nom de fichier statuts,
#  resolveur du modele source)
_CASES = [
    pytest.param(
        lambda d: css.generate_dossier(
            _civil_base("SCI", "sci", [_pp("Jean", "Durand", 100, 1, 100, 1000)]), d
        ),
        "statuts_sci.docx",
        lambda: _source("Modèle statuts SCI", exclude="IRIS"),
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
        "statuts_sci_iris.docx",
        lambda: _source("SCI IRIS"),
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
        "statuts_scs.docx",
        lambda: _source("SCS"),
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
        "statuts_scm.docx",
        lambda: _source("Statuts SCM"),
        id="SCM",
    ),
    pytest.param(
        lambda d: sas_slice.generate_dossier(_sas_payload(), d),
        "statuts_sas",
        lambda: _source("SAS", "medecins"),
        id="SAS",
    ),
    pytest.param(
        lambda d: spfpl_slice.generate_dossier(_spfpl_payload("SPFPL cession"), d),
        "statuts_spfpl_cession",
        lambda: _source("SPFPLAS", "cession"),
        id="SPFPL-cession",
    ),
    pytest.param(
        lambda d: spfpl_slice.generate_dossier(_spfpl_payload("SPFPL apport"), d),
        "statuts_spfpl_apport",
        lambda: _source("SPFPLAS", "apport"),
        id="SPFPL-apport",
    ),
    pytest.param(
        lambda d: selas_multi_slice.generate_dossier(_selas_payload(), d),
        "statuts_selas_multi",
        lambda: _source("SELAS", "multi"),
        id="SELAS-multi",
    ),
]


@pytest.mark.parametrize("generate, statuts_name, source_resolver", _CASES)
def test_statuts_source_headings_all_present(
    tmp_path: Path, generate, statuts_name: str, source_resolver
) -> None:
    generated = generate(tmp_path)
    statuts_path = _gen_statuts(generated, statuts_name)

    source_headings = _headings(source_resolver())
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

# Marqueurs (substring) des lignes du modele LEGITIMEMENT absentes du rendu, par type, avec raison.
# Une ligne source manquante n'echoue PAS si elle contient l'un de ces marqueurs. Tout le RESTE
# du corps statique doit apparaitre verbatim.
_BODY_ALLOWLIST: dict[str, tuple[str, ...]] = {
    # O24-01 (Rafael) : lignes d'annexe « lettre de mission » + « acompte des honoraires » du
    # cabinet Sydel, supprimees de TOUS les statuts a la demande du client.
    "statuts_sci.docx": ("lettre de mission", "acompte des honoraires"),
    "statuts_sci_iris.docx": ("lettre de mission", "acompte des honoraires"),
    "statuts_spfpl_cession": ("lettre de mission", "acompte des honoraires"),
    "statuts_selas_multi": ("lettre de mission", "acompte des honoraires"),
    # SCM : O24-01 + « ci- 510 € » = valeur d'EXEMPLE du modele (montant reinjecte dynamiquement) ;
    # « Faire preceder » / « Lu et approuve » = artefact du modele source SCM (texte de la mention
    # de signature DUPLIQUE dans un meme paragraphe), rendu de-duplique cote sortie.
    "statuts_scm.docx": (
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


@pytest.mark.parametrize("generate, statuts_name, source_resolver", _CASES)
def test_statuts_source_body_lines_present(
    tmp_path: Path, generate, statuts_name: str, source_resolver
) -> None:
    generated = generate(tmp_path)
    statuts_path = _gen_statuts(generated, statuts_name)
    output = _normalized_full_text(statuts_path)
    allow = _BODY_ALLOWLIST.get(statuts_name, ())
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
    doc = Document(_gen_statuts(generated, "statuts_sci_iris.docx"))
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
