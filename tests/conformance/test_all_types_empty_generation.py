"""KAN-2 @All — Garde de conformité : TOUT type de document se génère SANS AUCUN champ.

Verbatim (Rafael, rejeté 2×) : « Tous les documents doivent pouvoir être générés, même si je ne
remplis AUCUN champ dans le générateur. » Re-scopé @All le 2026-07-27 : le comportement livré pour
SPFPL doit valoir pour TOUTES les structures.

Ce garde généralise `test_spfpl_empty_generation` à toutes les familles : pour chaque structure, il
construit un payload VIDE FIDÈLE (le SÉLECTEUR `structure` reste — c'est le TYPE de doc, pas un
champ ; les vraies opérations/flags nécessaires au routage restent) et asserte, sur TOUT le texte
de TOUS les docx (paragraphes ET cellules) :

  * aucun CRASH (le dossier se génère, docx produits) ;
  * aucun MARQUEUR TECHNIQUE dans « (À COMPLÉTER : …) » — pas de point, underscore, chiffre d'index
    ni casse de token ; que des libellés métier lisibles ;
  * aucune QUANTITÉ chiffrée affirmée (« N actions/parts/titres », « (0) … ») ni « six cents ».

Le détail fin (blancs signature, statut matrimonial, civilité, profession) reste couvert
structure-par-structure par les gardes dédiés ; ici on verrouille MÉCANIQUEMENT le contrat @All :
« ça génère, à vide, sans crash ni valeur fausse », pour ne jamais régresser (règle 68 §3).

SPFPL a déjà son garde exhaustif (`test_spfpl_empty_generation`) : on ne le duplique pas ici.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
from docx import Document

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT / "tests" / "unit"))

import test_multi_type_front as mtf  # noqa: E402

# (structure, module du slice, nom du builder de payload dans test_multi_type_front)
# Structures à builder disponible. Les familles sans builder (civils / sasu / selarl) sont
# ajoutées après recensement de leur point d'entrée empty-gen (agents KAN-2 @All).
_CAS: tuple[tuple[str, str, str], ...] = (
    ("SAS", "sas_slice", "_sas_payload"),
    ("SELAS", "selas_multi_slice", "_selas_payload"),
    ("SELAS uni dentiste", "selas_uni_dentiste_slice", "_selas_uni_payload"),
    ("SELAS uni medecin", "selas_uni_medecin_slice", "_selas_uni_medecin_payload"),
)

# Sélecteurs de routage à préserver même « à vide » (ce sont le TYPE/flux, pas des champs saisis).
_SELECTEURS = ("structure", "operation", "operation_spfpl_type", "is_apport")


def _empty_payload(structure: str, builder: str) -> dict:
    full = getattr(mtf, builder)()
    payload = {
        key: ("" if isinstance(value, str) else (value if isinstance(value, bool) else None))
        for key, value in full.items()
    }
    payload["structure"] = structure
    for selector in _SELECTEURS:
        if selector in full:
            payload[selector] = full[selector]
    # Sous-dictionnaires d'opération : vidés, jamais None (le routage lit .get sur eux).
    for bag in ("cession_data", "apport_data"):
        if bag in full:
            payload[bag] = {}
    return payload


def _all_units(structure: str, builder: str, slice_module: str, tmp_path: Path) -> list[str]:
    mod = __import__(f"sydel_doc_engine.front_app.{slice_module}", fromlist=["generate_dossier"])
    out = tmp_path / structure.replace(" ", "_")
    out.mkdir(parents=True, exist_ok=True)
    generated = mod.generate_dossier(_empty_payload(structure, builder), out)
    assert generated.docx_paths, f"aucun document généré pour {structure} à vide"
    units: list[str] = []
    for path in generated.docx_paths:
        doc = Document(str(path))
        units.extend(p.text for p in doc.paragraphs)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    units.extend(p.text for p in cell.paragraphs)
    return units


@pytest.mark.parametrize("structure,slice_module,builder", _CAS)
def test_type_generates_from_empty_form(
    structure: str, slice_module: str, builder: str, tmp_path: Path
) -> None:
    units = _all_units(structure, builder, slice_module, tmp_path)
    text = "\n".join(units)

    # Aucun marqueur TECHNIQUE : que des libellés métier lisibles.
    marqueurs = re.findall(r"\(À COMPLÉTER : [^)]*\)", text)
    techniques = [
        m
        for m in marqueurs
        if ("." in m or "_" in m or re.search(r"\d", m) or re.search(r"[a-z][A-Z]{2}", m))
    ]
    assert not techniques, (
        f"{structure} à vide : marqueur(s) TECHNIQUE(S) (libellé métier attendu) : "
        f"{sorted(set(techniques))[:5]}"
    )

    # Aucune quantité de titres chiffrée affirmée (doit être un marqueur), ni nombre en lettres.
    quantite = re.findall(r"\b\d[\d\s]*\s+(?:actions|parts|titres)\b", text)
    assert not quantite, (
        f"{structure} à vide : quantité de titres CHIFFRÉE affirmée (marqueur attendu) : "
        f"{quantite[:3]}"
    )
    assert "(0) actions" not in text and "(0) parts" not in text and "(0) titres" not in text, (
        f"{structure} à vide : quantité « (0) » affirmée (marqueur attendu)"
    )
    assert "six cents" not in text.lower(), (
        f"{structure} à vide : nombre affirmé « six cents » (marqueur attendu)"
    )
