"""KAN-2 — Garde de conformité : générer le dossier SPFPL SANS AUCUN champ rempli.

Rafael (rejeté 2×) : « Tous les documents doivent pouvoir être générés, même si je ne remplis
AUCUN champ. » Un champ vide sort en MARQUEUR « (À COMPLÉTER : <libellé métier>) », JAMAIS une
valeur FAUSSE/inventée ni un chemin technique.

Ce garde génère les dossiers cession ET apport avec un payload VIDE FIDÈLE (les SÉLECTEURS
`operation`/`operation_spfpl_type`/`is_apport` restent — ce sont le TYPE de doc, pas des champs)
et asserte, sur TOUT le texte de TOUS les docx :

  * B1/B2/B3 : aucune valeur fausse affirmée — pas de « 600 »/« six cents » (nb d'actions inventé),
    pas de « célibataire » (statut matrimonial inventé), pas de « (0) »/« zéro (0) » titre affirmé,
    pas de civilité « Monsieur » inventée (les Monsieur/Madame LÉGITIMES sont whitelistés) ;
  * M1 : aucune profession d'INDIVIDU affirmée (« … de profession » / « , chirurgien-dentiste, ») —
    le boilerplate LÉGAL des statuts (« exercer la profession de … ») et l'Ordre sont légitimes ;
  * M2 : aucun marqueur technique — pas de point, underscore, chiffre d'index ni casse de token
    dans « (À COMPLÉTER : … ) » ; que des libellés métier lisibles.

Il attrape MÉCANIQUEMENT toute réintroduction d'un défaut de la classe (règle 68 §3 : convention
neuve -> règle de conformité le jour même) — la suite nominale ne les voyait pas.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
from docx import Document

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "tests" / "unit"))

import test_multi_type_front as mtf  # noqa: E402

from sydel_doc_engine.front_app import spfpl_slice  # noqa: E402

# Monsieur/Madame LÉGITIMES sur formulaire vide (pas des civilités inventées d'un signataire) :
# destinataire de l'Ordre, mandataire SYDEL hardcodé, civilités DÉFINITIONNELLES des parents.
_MONSIEUR_LEGITIMES = (
    "Monsieur le Président",
    "Madame la Présidente",
    "Monsieur Jordan",
    "fils de Monsieur",
    "fille de Monsieur",
    "et de Madame",
    "de Monsieur",  # « fils/fille de Monsieur … » coupé
)


def _empty_payload(structure: str) -> dict:
    full = mtf._spfpl_payload(structure)
    payload = {
        key: ("" if isinstance(value, str) else (value if isinstance(value, bool) else None))
        for key, value in full.items()
    }
    payload["structure"] = structure
    for selector in ("operation", "operation_spfpl_type", "is_apport"):
        if selector in full:
            payload[selector] = full[selector]
    payload["cession_data"] = {}
    payload["apport_data"] = {}
    return payload


def _all_text(structure: str, tmp_path: Path) -> str:
    out = tmp_path / structure.replace(" ", "_")
    out.mkdir(parents=True, exist_ok=True)
    generated = spfpl_slice.generate_dossier(_empty_payload(structure), out)
    assert generated.docx_paths, f"aucun document généré pour {structure} vide"
    chunks: list[str] = []
    for path in generated.docx_paths:
        chunks.extend(p.text for p in Document(str(path)).paragraphs)
    return "\n".join(chunks)


@pytest.mark.parametrize("structure", ["SPFPL cession", "SPFPL apport"])
def test_spfpl_dossier_generates_from_empty_form(structure: str, tmp_path: Path) -> None:
    text = _all_text(structure, tmp_path)

    # B1 : nombre d'actions du capital inventé « 600 » / « six cents ».
    assert "600 actions" not in text and "six cents" not in text.lower(), (
        f"{structure} vide : nombre d'actions FANTÔME affirmé (doit être un marqueur)"
    )
    # B2 : statut matrimonial inventé.
    assert "célibataire" not in text.lower(), (
        f"{structure} vide : « célibataire » inventé (doit être un marqueur)"
    )
    # B3 : quantité de titres affirmée à zéro dans un acte signable.
    assert "(0) actions" not in text and "(0) parts" not in text and "zéro (0)" not in text, (
        f"{structure} vide : quantité de titres « (0) » affirmée (doit être un marqueur)"
    )

    # B4 : civilité « Monsieur/Madame » inventée pour un signataire (hors cas légitimes).
    residual = text
    for legit in _MONSIEUR_LEGITIMES:
        residual = residual.replace(legit, "")
    assert "Monsieur" not in residual and "Madame" not in residual, (
        f"{structure} vide : civilité « Monsieur/Madame » inventée pour un signataire"
    )

    # M1 : profession d'INDIVIDU affirmée (descripteur d'identité), hors boilerplate légal.
    individu_profession = re.findall(
        r"(?<!la profession de )[Cc]hirurgiens?-[Dd]entistes? de profession", text
    ) + re.findall(r"\), [Cc]hirurgiens?-[Dd]entistes?, de nationalité", text)
    assert not individu_profession, (
        f"{structure} vide : profession d'individu « chirurgien-dentiste » affirmée "
        f"(le TYPE ne doit pas fuir sur une personne dont l'identité est un marqueur) : "
        f"{individu_profession[:3]}"
    )

    # M2 : marqueur technique (point / underscore / chiffre d'index / casse de token).
    marqueurs = re.findall(r"\(À COMPLÉTER : [^)]*\)", text)
    techniques = [
        m
        for m in marqueurs
        if ("." in m or "_" in m or re.search(r"\d", m) or re.search(r"[a-z][A-Z]{2}", m))
    ]
    assert not techniques, (
        f"{structure} vide : marqueur(s) TECHNIQUE(S) (doit être un libellé métier lisible) : "
        f"{sorted(set(techniques))[:5]}"
    )
