"""Suite de CONFORMITÉ transverse — les retours client codifiés en assertions permanentes.

Principe : chaque retour client (Albane/Rafael) codifié ici est appliqué à CHAQUE
document de CHAQUE type d'entreprise (corpus généré par les slices front réels,
cf. ``_conformance_corpus``). Un retour codifié ne peut plus JAMAIS revenir
silencieusement sur aucun type (gate registre de propagation, règle 68 Q4).

Règles (détail : ``_conformance_rules``) :
  R1 tokens résiduels · R2 « numéro en cours » · R3 « Docteur » ≠ civilité ·
  R4 français accentué · R5 montants groupés · R6 élision « d'un » ·
  R7 double unité · R8 double répartition (acte) · R9 clause Ordre + département.

Marquage : les cellules (type × règle) ROUGES au constat initial (2026-07-07,
worklist = ``RAPPORT_INITIAL.md``) portent ``xfail(strict=True)`` — quand le fix
arrive, le xfail strict CASSE et on retire le marqueur. Les cellules vertes sont
des assertions DURES : toute régression future échoue immédiatement.
"""

from __future__ import annotations

import pytest
from _conformance_corpus import CORPUS_KEYS
from _conformance_rules import RULE_LABELS, RULES

# ---------------------------------------------------------------------------
# Cellules (type × règle) en échec au constat initial — worklist des fixes.
# Détail complet (doc × extrait) : tests/conformance/RAPPORT_INITIAL.md.
# ---------------------------------------------------------------------------

_REASON = "retour Albane 2026-07-07 — fix à venir"

# Fix-sprint 2026-07-07 : les 25 cellules initialement rouges (R2/R3/R4/R5/R6/R8/R9,
# cf. RAPPORT_INITIAL.md) sont passées au VERT (XPASS strict constaté) -> marqueurs
# retirés, ces cellules sont désormais des ASSERTIONS DURES permanentes.
# Seul reste xfail le verbatim source SCM (décision de fidélité à arbitrer avec Albane).
KNOWN_FAILURES: dict[tuple[str, str], str] = {
    ("scm", "R4"): (
        f"{_REASON} (pacte « Associe » + règlement « repartis » — verbatim source à arbitrer)"
    ),
}


def _cell_params():
    for type_key in CORPUS_KEYS:
        for rule_id in RULES:
            marks = []
            reason = KNOWN_FAILURES.get((type_key, rule_id))
            if reason is not None:
                marks.append(pytest.mark.xfail(strict=True, reason=reason))
            yield pytest.param(type_key, rule_id, id=f"{type_key}-{rule_id}", marks=marks)


@pytest.mark.parametrize(("type_key", "rule_id"), list(_cell_params()))
def test_conformite_transverse(
    corpus: dict[str, dict[str, str]], type_key: str, rule_id: str
) -> None:
    """Applique une règle transversale à CHAQUE document du bundle d'un type."""
    bundle = corpus[type_key]
    rule = RULES[rule_id]
    violations: list[str] = []
    for doc_name in sorted(bundle):
        for extract in rule(bundle[doc_name]):
            violations.append(f"({type_key} × {doc_name} × {rule_id}) {extract}")
    assert not violations, (
        f"{rule_id} — {RULE_LABELS[rule_id]} : {len(violations)} violation(s)\n"
        + "\n".join(violations)
    )


# ---------------------------------------------------------------------------
# Complétude du corpus : chaque type génère bien son bundle (document pivot
# présent + volume plausible). Si un slice casse, on le voit ICI, pas par des
# cellules de règles silencieusement vertes sur un bundle vide.
# ---------------------------------------------------------------------------

_PIVOT_DOC: dict[str, str] = {
    "selarl": "Statuts SELARL MARTIN.docx",
    "selarl_regime": "lettre_avertissement_conjoint.docx",
    "selarl_cession_medical": "acte_cession_cabinet_medical.docx",
    "selarl_cession_dentaire": "acte_cession_cabinet_dentaire.docx",
    "selarl_cession_scm": "acte_cession_parts_scm.docx",
    "selas_multi": "Statuts SELAS EXEMPLE.docx",
    "selas_multi_phys": "attestation_capital_souscripteurs_selas.docx",
    "selas_uni_medecin": "attestation_capital_souscripteurs_selas.docx",
    "selas_uni_dentiste": "attestation_capital_souscripteurs_selas.docx",
    "spfpl_cession": "acte_cession_parts_spfpl.docx",
    "spfpl_cession_vn1": "statuts_spfpl_cession.docx",
    "spfpl_apport": "contrat_apport_spfpl.docx",
    "sas": "attestation_capital_liste_souscripteurs_sas.docx",
    "sasu_holding": "statuts_sasu_holding.docx",
    "sci": "lettre_option_is.docx",
    "sci_iris": "statuts_sci_iris.docx",
    "scm": "reglement_interieur_scm.docx",
    "scs": "liste_souscripteurs_scs.docx",
    "micro_holding": "statuts_micro_holding.docx",
}


def test_corpus_couvre_tous_les_types(corpus: dict[str, dict[str, str]]) -> None:
    assert set(corpus) == set(CORPUS_KEYS)
    assert set(_PIVOT_DOC) == set(CORPUS_KEYS)
    for type_key in CORPUS_KEYS:
        bundle = corpus[type_key]
        expected_min = 1 if type_key == "spfpl_cession_vn1" else 5
        assert len(bundle) >= expected_min, (
            f"{type_key} : bundle anormalement réduit ({sorted(bundle)})"
        )
        assert _PIVOT_DOC[type_key] in bundle, (
            f"{type_key} : document pivot absent ({sorted(bundle)})"
        )
        for doc_name, text in bundle.items():
            assert text.strip(), f"{type_key} × {doc_name} : document vide"
