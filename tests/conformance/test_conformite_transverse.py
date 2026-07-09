"""Suite de CONFORMITÉ transverse — les retours client codifiés en assertions permanentes.

Principe : chaque retour client (Albane/Rafael) codifié ici est appliqué à CHAQUE
document de CHAQUE type d'entreprise (corpus généré par les slices front réels,
cf. ``_conformance_corpus``). Un retour codifié ne peut plus JAMAIS revenir
silencieusement sur aucun type (gate registre de propagation, règle 68 Q4).

Règles (détail : ``_conformance_rules``) :
  R1 tokens résiduels · R2 « numéro en cours » · R3 « Docteur » ≠ civilité ·
  R4 français accentué · R5 montants groupés (seuil abaissé à 4 chiffres, Rafael
  2026-07-09 : « 1000 » -> « 1 000 ») · R6 élision « d'un » · R7 double unité ·
  R8 double répartition (acte) · R9 clause Ordre + département · R10 nom de fichier
  statuts = « Statuts <dénomination>.docx » (Rafael 2026-07-07 — appliquée au NOM du
  document, cf. ``FILENAME_RULES``) · R12 majuscule en tête de phrase.

R13 (accord euro/euros — Rafael 2026-07-09) tourne sur un corpus SÉPARÉ « montant
unitaire = 1 € » (``build_corpus_cap1``) : cf. ``test_r13_accord_euro`` plus bas. Un
montant singulier suivi de « euros » (« 1 euros ») échoue sur TOUS les types à la fois.

Marquage : les cellules (type × règle) ROUGES au constat initial (2026-07-07,
worklist = ``RAPPORT_INITIAL.md``) portent ``xfail(strict=True)`` — quand le fix
arrive, le xfail strict CASSE et on retire le marqueur. Les cellules vertes sont
des assertions DURES : toute régression future échoue immédiatement.
"""

from __future__ import annotations

import pytest
from _conformance_corpus import CORPUS_CAP1_KEYS, CORPUS_KEYS
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
# R11 — une DNC PAR GÉRANT personne physique (règle de BUNDLE)
# Albane (Direction Juridique) + Rafael 2026-07-09 : DNC = gérants uniquement, supersede
# le retour Rafael du matin « 1 DNC par associé ».
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("type_key", CORPUS_KEYS)
def test_r11_dnc_par_gerant(corpus: dict[str, dict[str, str]], type_key: str) -> None:
    """« Une déclaration de non-condamnation par GÉRANT » (Albane 2026-07-09 —
    supersede « 1 DNC par associé » du matin), tous types. Compte les DNC du bundle
    contre le nombre de GÉRANTS personnes physiques du payload (table
    ``EXPECTED_DNC_GERANTS``, alignée sur ``build_corpus``)."""
    from _conformance_corpus import EXPECTED_DNC_GERANTS
    from _conformance_rules import R11_LABEL, rule_r11_dnc_par_gerant

    assert set(EXPECTED_DNC_GERANTS) == set(CORPUS_KEYS), (
        "EXPECTED_DNC_GERANTS désaligné des types du corpus"
    )
    violations = rule_r11_dnc_par_gerant(corpus[type_key], EXPECTED_DNC_GERANTS[type_key])
    assert not violations, f"R11 — {R11_LABEL} ({type_key}) :\n" + "\n".join(violations)


# ---------------------------------------------------------------------------
# R13 — accord euro/euros après un montant SINGULIER (Rafael 2026-07-09)
# ---------------------------------------------------------------------------
#
# « si montant = 1 -> 1 euro, si 100 -> 100 euros » : PARTOUT, tous types, tous
# documents. Appliquée au corpus « montant unitaire = 1 € » (``build_corpus_cap1``) :
# tout « 1 euros » / « (1) euros » / « un euros » / « 0 euros » (accord singulier faux)
# est une VIOLATION. Un spot silo-é (hardcodé Python OU figé dans un modèle source)
# échoue ICI, sur TOUS les types concernés à la fois (gate registre, règle 68 Q4).


@pytest.mark.parametrize("type_key", CORPUS_CAP1_KEYS)
def test_r13_accord_euro(corpus_cap1: dict[str, dict[str, str]], type_key: str) -> None:
    """Aucun « 1 euros » (montant singulier + pluriel) sur AUCUN document, cap 1 €."""
    from _conformance_rules import R13_LABEL, rule_r13_accord_euro

    bundle = corpus_cap1[type_key]
    violations: list[str] = []
    for doc_name in sorted(bundle):
        for extract in rule_r13_accord_euro(bundle[doc_name]):
            violations.append(f"({type_key} × {doc_name} × R13) {extract}")
    assert not violations, (
        f"R13 — {R13_LABEL} : {len(violations)} violation(s)\n" + "\n".join(violations)
    )


# ---------------------------------------------------------------------------
# R15 — accord en genre de la FONCTION d'une personne (Rafael 2026-07-09)
# ---------------------------------------------------------------------------
#
# Le corpus transverse (``_pp`` -> tous masculins) ne porte pas de représentante
# féminine : R15 y est vraie mais VACUE. Ce test cible la LOGIQUE de la règle (par
# INTENTION) pour garantir ses dents : « Madame <Nom>, <fonction masculine> » flaguée,
# forme féminine / « Monsieur » / fonction non accolée non flaguées.


def test_r15_flague_madame_fonction_masculine() -> None:
    from _conformance_rules import rule_r15_accord_fonction

    assert rule_r15_accord_fonction("Représentée par Madame Alice Martin, gérant")
    assert rule_r15_accord_fonction("Madame Claire Bernard, président")
    assert rule_r15_accord_fonction("Mme Alice Martin, associé de la société")
    assert rule_r15_accord_fonction("Madame Eva Roux, directeur")


def test_r15_ne_flague_pas_les_cas_legitimes() -> None:
    from _conformance_rules import rule_r15_accord_fonction

    # Forme féminine correcte.
    assert not rule_r15_accord_fonction("Représentée par Madame Alice Martin, gérante")
    assert not rule_r15_accord_fonction("Madame Alice Martin, présidente")
    assert not rule_r15_accord_fonction("Madame Alice Martin, associée")
    # Homme -> masculin légitime.
    assert not rule_r15_accord_fonction("Représentée par Monsieur Jean Durand, gérant")
    # Fonction NON accolée au nom (autre segment de virgule) -> hors périmètre.
    assert not rule_r15_accord_fonction("Madame Alice Martin, née le 1er janvier 1980, gérante")


def test_corpus_cap1_couvre_les_types(corpus_cap1: dict[str, dict[str, str]]) -> None:
    """Le corpus cap1 couvre exactement ``CORPUS_CAP1_KEYS`` (bundles non vides)."""
    assert set(corpus_cap1) == set(CORPUS_CAP1_KEYS)
    for type_key in CORPUS_CAP1_KEYS:
        bundle = corpus_cap1[type_key]
        assert bundle, f"{type_key} : bundle cap1 vide"
        for doc_name, text in bundle.items():
            assert text.strip(), f"{type_key} × {doc_name} : document cap1 vide"


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
