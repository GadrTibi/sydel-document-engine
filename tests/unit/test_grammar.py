from __future__ import annotations

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.utils.grammar import (
    apply_gender_pairs,
    birth_label,
    filiation_label,
    subject_line,
)


def test_subject_line_masculin() -> None:
    assert subject_line(Gender.MASCULIN) == "Je soussigné"


def test_subject_line_feminin() -> None:
    assert subject_line(Gender.FEMININ) == "Je soussignée"


def test_birth_label_and_filiation_label_feminin() -> None:
    assert birth_label(Gender.FEMININ) == "Née le"
    assert filiation_label(Gender.FEMININ) == "fille de Monsieur"


_PAIRS = [
    ("Je soussigné", "Je soussignée"),
    ("né le", "née le"),
    ("LE SOUSSIGNE\xa0:", "LA SOUSSIGNÉE\xa0:"),
]


def test_apply_gender_pairs_masculin_to_feminin() -> None:
    # Genre feminin : chaque forme masculine devient sa forme feminine.
    source = "LE SOUSSIGNE\xa0: Je soussigné, né le 02/01/1980."

    rendered = apply_gender_pairs(source, Gender.FEMININ, _PAIRS)

    assert rendered == "LA SOUSSIGNÉE\xa0: Je soussignée, née le 02/01/1980."


def test_apply_gender_pairs_feminin_to_masculin() -> None:
    # Genre masculin : chaque forme feminine redevient sa forme masculine
    # (sens inverse, ex. modele dentaire fige au feminin pour un homme).
    source = "LA SOUSSIGNÉE\xa0: Je soussignée, née le 10/03/1975."

    rendered = apply_gender_pairs(source, Gender.MASCULIN, _PAIRS)

    assert rendered == "LE SOUSSIGNE\xa0: Je soussigné, né le 10/03/1975."


def test_apply_gender_pairs_leaves_correct_gender_untouched() -> None:
    # Une forme deja dans le bon genre n'est pas modifiee.
    masculine = "Je soussigné, né le 02/01/1980."
    feminine = "Je soussignée, née le 10/03/1975."

    assert apply_gender_pairs(masculine, Gender.MASCULIN, _PAIRS) == masculine
    assert apply_gender_pairs(feminine, Gender.FEMININ, _PAIRS) == feminine


def test_apply_gender_pairs_does_not_touch_invariant_forms() -> None:
    # GARDE-FOU : aucune regex de terminaison. Avec les paires reelles ancrees
    # de la cession (vendeur), les formes invariantes/voulues du modele
    # (« désigné », « soussigné de première part ») ne sont jamais accordees.
    cession_vendeur_pairs = [
        ("né le ", "née le "),
        ("Inscrit au tableau", "Inscrite au tableau"),
        ("inscrit au tableau", "inscrite au tableau"),
    ]
    invariant = (
        "Ci-après désigné «\xa0le vendeur\xa0» ou le soussigné de première part. "
        "Le vendeur cède, ci-après plus amplement désigné, exploité au siège."
    )

    assert apply_gender_pairs(invariant, Gender.FEMININ, cession_vendeur_pairs) == invariant
    assert apply_gender_pairs(invariant, Gender.MASCULIN, cession_vendeur_pairs) == invariant
