"""Suite de CONFORMITÉ transverse — les retours client codifiés en assertions permanentes.

Principe : chaque retour client (Albane/Rafael) codifié ici est appliqué à CHAQUE
document de CHAQUE type d'entreprise (corpus généré par les slices front réels,
cf. ``_conformance_corpus``). Un retour codifié ne peut plus JAMAIS revenir
silencieusement sur aucun type (gate registre de propagation, règle 68 Q4).

Règles (détail : ``_conformance_rules``) :
  R1 tokens résiduels · R2 « numéro en cours » · R3 « Docteur » ≠ civilité ·
  R4 français accentué · R5 montants groupés · R6 élision « d'un » ·
  R7 double unité · R8 double répartition (acte) · R9 clause Ordre + département ·
  R10 nom de fichier statuts = « Statuts <dénomination>.docx » (Rafael 2026-07-07 —
  appliquée au NOM du document, cf. ``FILENAME_RULES``).

Marquage : les cellules (type × règle) ROUGES au constat initial (2026-07-07,
worklist = ``RAPPORT_INITIAL.md``) portent ``xfail(strict=True)`` — quand le fix
arrive, le xfail strict CASSE et on retire le marqueur. Les cellules vertes sont
des assertions DURES : toute régression future échoue immédiatement.
"""

from __future__ import annotations

import pytest
from _conformance_corpus import CORPUS_KEYS
from _conformance_rules import FILENAME_RULES, RULE_LABELS, RULES

# ---------------------------------------------------------------------------
# Cellules (type × règle) en échec au constat initial — worklist des fixes.
# Détail complet (doc × extrait) : tests/conformance/RAPPORT_INITIAL.md.
# ---------------------------------------------------------------------------

_REASON = "retour Albane 2026-07-07 — fix à venir"

# Fix-sprint 2026-07-07 : les 26 cellules initialement rouges (R2/R3/R4/R5/R6/R8/R9,
# cf. RAPPORT_INITIAL.md) sont TOUTES passées au VERT -> marqueurs retirés, assertions
# DURES permanentes. Y compris scm-R4 : les typos verbatim du modèle source SCM
# (« Associe », « repartis ») ont été corrigées sur insistance client (Rafael 2026-07-07,
# « tout le texte doit être correct » — supersede la fidélité au modèle).
KNOWN_FAILURES: dict[tuple[str, str], str] = {}


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
        # R10 (FILENAME_RULES) porte sur le NOM du document ; les autres sur le texte.
        subject = doc_name if rule_id in FILENAME_RULES else bundle[doc_name]
        for extract in rule(subject):
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
    "spfpl_cession_vn1": "Statuts SPFPL MARTIN.docx",
    "spfpl_apport": "contrat_apport_spfpl.docx",
    "sas": "attestation_capital_liste_souscripteurs_sas.docx",
    "sasu_holding": "Statuts MLG.docx",
    "sci": "lettre_option_is.docx",
    "sci_iris": "Statuts SCI IRIS EXEMPLE.docx",
    "scm": "reglement_interieur_scm.docx",
    "scs": "liste_souscripteurs_scs.docx",
    "micro_holding": "Statuts MA MICRO HOLDING.docx",
}


# ---------------------------------------------------------------------------
# R11 — une DNC PAR associé personne physique (règle de BUNDLE, Rafael 2026-07-09)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("type_key", CORPUS_KEYS)
def test_r11_dnc_par_associe(corpus: dict[str, dict[str, str]], type_key: str) -> None:
    """« Une déclaration de non-condamnation pour CHAQUE associé » (2 associés =
    2 documents), tous types. Compte les DNC du bundle contre le nombre d'associés
    personnes physiques du payload (table ``EXPECTED_DNC_PP``, alignée sur
    ``build_corpus``)."""
    from _conformance_corpus import EXPECTED_DNC_PP
    from _conformance_rules import R11_LABEL, rule_r11_dnc_par_associe

    assert set(EXPECTED_DNC_PP) == set(CORPUS_KEYS), (
        "EXPECTED_DNC_PP désaligné des types du corpus"
    )
    violations = rule_r11_dnc_par_associe(corpus[type_key], EXPECTED_DNC_PP[type_key])
    assert not violations, f"R11 — {R11_LABEL} ({type_key}) :\n" + "\n".join(violations)


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
