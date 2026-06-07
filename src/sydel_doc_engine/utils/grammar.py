from __future__ import annotations

from sydel_doc_engine.domain.enums import Gender


def subject_line(genre: Gender) -> str:
    return "Je soussignée" if genre == Gender.FEMININ else "Je soussigné"


def birth_label(genre: Gender) -> str:
    return "Née le" if genre == Gender.FEMININ else "Né le"


def filiation_label(genre: Gender) -> str:
    return "fille de Monsieur" if genre == Gender.FEMININ else "fils de Monsieur"


def apply_gender_pairs(
    text: str,
    genre: Gender,
    pairs: list[tuple[str, str]],
) -> str:
    """Accorde un texte en genre par remplacement de chaînes EXACTES et ancrées.

    Chaque paire est `(forme_masculin, forme_feminin)`. Selon `genre` :

    - `Gender.FEMININ`  -> remplace chaque `forme_masculin` par sa `forme_feminin` ;
    - `Gender.MASCULIN` -> remplace chaque `forme_feminin` par sa `forme_masculin`.

    Le remplacement est **bidirectionnel** : un modèle figé au féminin (ex. acte
    dentaire « née le ») redevient masculin pour un homme, et un modèle figé au
    masculin (ex. statuts « LE SOUSSIGNE ») devient féminin pour une femme.

    GARDE-FOU : on ne fait JAMAIS de regex sur les terminaisons « -é/-ée ». On
    remplace uniquement les chaînes littérales fournies, pilotées par le `genre`
    de la BONNE personne du contexte (vendeur, représentant, associé,
    signataire...). Une forme déjà dans le bon genre, ou absente du texte, est
    laissée intacte. Si une paire a ses deux formes égales (rien à accorder),
    elle est ignorée pour éviter tout remplacement parasite.

    Le remplacement est **idempotent** et sûr même quand la forme source est un
    préfixe de la cible (ex. « Je soussigné » ⊂ « Je soussignée ») : on protège
    d'abord les occurrences déjà dans le bon genre avant de remplacer, pour ne
    pas re-accorder « Je soussignée » en « Je soussignéee ». Réappliquer la
    fonction sur un texte déjà accordé ne le modifie plus.

    Args:
        text: le texte source (après remplissage des tokens éventuel).
        genre: genre cible (celui de la personne décrite par les formes).
        pairs: liste de couples `(masculin, feminin)` de chaînes exactes.

    Returns:
        Le texte accordé au genre demandé.
    """
    rendered = text
    for index, (masculin, feminin) in enumerate(pairs):
        if masculin == feminin:
            continue
        source, target = (masculin, feminin) if genre == Gender.FEMININ else (feminin, masculin)
        rendered = _replace_to_target(rendered, source, target, index)
    return rendered


def _replace_to_target(text: str, source: str, target: str, index: int) -> str:
    """Remplace `source` par `target` de façon idempotente et sûre.

    Deux cas de chevauchement préfixe à gérer (l'une des formes est sous-chaîne
    de l'autre) :

    - `source` ⊂ `target` (ex. masc « Je soussigné » dans fém « Je soussignée ») :
      remplacer naïvement `source` re-toucherait les `target` déjà corrects. On
      masque d'abord les `target` présents par un jeton neutre, on remplace
      `source` -> `target`, puis on restaure les jetons.
    - `target` ⊂ `source` (ex. fém « Je soussignée » contient masc « Je
      soussigné ») : on remplace directement la chaîne `source` complète (le
      match porte sur la forme la plus longue, donc non ambigu).

    Dans tous les cas, réappliquer la fonction sur un texte déjà accordé est sans
    effet (idempotent).
    """
    if source not in text:
        return text
    if target in source:
        # target est un préfixe/sous-chaîne de source : match direct non ambigu.
        return text.replace(source, target)
    # source ⊂ target (ou disjoints) : on protège les target déjà présents.
    sentinel = f"\x00GENDER_PAIR_{index}\x00"
    protected = text.replace(target, sentinel)
    protected = protected.replace(source, target)
    return protected.replace(sentinel, target)
