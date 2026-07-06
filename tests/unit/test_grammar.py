from __future__ import annotations

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.utils.grammar import (
    apply_gender_pairs,
    birth_label,
    euro_word,
    filiation_label,
    montant_lettres_avec_unite,
    subject_line,
)


def test_euro_word_singulier_sous_deux() -> None:
    # « euro » au singulier pour 0 et 1 (montant < 2).
    assert euro_word("0") == "euro"
    assert euro_word("1") == "euro"
    assert euro_word(1) == "euro"


def test_euro_word_pluriel_des_deux() -> None:
    # « euros » au pluriel a partir de 2 (le bug remonte par Rafael : « 10 euro »).
    assert euro_word("2") == "euros"
    assert euro_word("10") == "euros"
    assert euro_word("100") == "euros"
    assert euro_word("1 000") == "euros"  # separateur de milliers tolere
    assert euro_word("10,00") == "euros"  # decimale francaise toleree


def test_euro_word_illisible_defaut_pluriel() -> None:
    # Valeur non parsable -> pluriel (cas le plus courant, le moins risque).
    assert euro_word("") == "euros"
    assert euro_word(None) == "euros"


def test_euro_word_reste_pur_meme_sur_decimal() -> None:
    # euro_word est un accord PUR (jamais vide) : sur une valeur decimale il rend « euro(s) »
    # selon la partie entiere, utilisable sans risque sur une ligne « figure + unite ».
    # La suppression de l'unite pour un decimal est le role de montant_lettres_avec_unite.
    assert euro_word("0,01") == "euro"  # partie entiere 0 -> singulier
    assert euro_word("2,50") == "euros"


def test_montant_lettres_avec_unite_entier_byte_identique() -> None:
    # ENTIER : mots nus + unite accordee -> byte-identique au rendu historique.
    assert montant_lettres_avec_unite("un", "1") == "un euro"
    assert montant_lettres_avec_unite("cent", "100") == "cent euros"
    assert montant_lettres_avec_unite("dix", "10") == "dix euros"
    # Une decimale « ,00 » n'est PAS une vraie decimale -> accord entier normal.
    assert montant_lettres_avec_unite("deux", "2,00") == "deux euros"


def test_montant_lettres_avec_unite_decimal_pas_de_double_euro() -> None:
    # DECIMAL (Albane 7.5) : la phrase monetaire est calculee DEPUIS LA FIGURE, l'arg
    # `lettres` est IGNORE (containment 2026-07-06). On l'assert avec la phrase historique
    # comme lettres (retro-compat) puis avec la FIGURE nue comme lettres (vrai front).
    assert montant_lettres_avec_unite("un centime d’euro", "0,01") == "un centime d’euro"
    assert (
        montant_lettres_avec_unite("cinquante centimes d’euro", "0,50")
        == "cinquante centimes d’euro"
    )
    assert (
        montant_lettres_avec_unite("deux euros et cinquante centimes", "2,50")
        == "deux euros et cinquante centimes"
    )
    # Aucun double « euro » ni espace parasite quel que soit le cas.
    for lettres, fig in (
        ("un centime d’euro", "0,01"),
        ("deux euros et cinquante centimes", "2,50"),
    ):
        rendu = montant_lettres_avec_unite(lettres, fig)
        assert "euro euro" not in rendu
        assert "  " not in rendu


def test_montant_lettres_avec_unite_calcule_depuis_la_figure() -> None:
    # Containment 2026-07-06 : c'est le SEUL point qui produit la phrase monetaire decimale,
    # et il la CALCULE depuis la FIGURE (arg `lettres` ignore sur un decimal). Le front pose
    # desormais la FIGURE dans le slot lettres (`number_words_from_value(decimal)` = figure) :
    # on prouve que le rendu est bien la phrase monetaire, PAS la figure nue.
    assert montant_lettres_avec_unite("0,01", "0,01") == "un centime d’euro"
    assert montant_lettres_avec_unite("0,5", "0,50") == "cinquante centimes d’euro"
    assert montant_lettres_avec_unite("2,5", "2,50") == "deux euros et cinquante centimes"
    assert (
        montant_lettres_avec_unite("1500,5", "1500,50")
        == "mille cinq cents euros et cinquante centimes"
    )
    # ENTIER : mots nus + unite accordee (byte-identique), l'arg `lettres` est UTILISE ici.
    assert montant_lettres_avec_unite("cent", "100") == "cent euros"
    assert montant_lettres_avec_unite("un", "1") == "un euro"


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
