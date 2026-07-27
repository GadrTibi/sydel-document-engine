# SOURCES DE VÉRITÉ — corpus de référence

> Base du **test d'anticipabilité** (`METHODE.md` Q1). Avant de classer un retour « nouveauté »,
> on vérifie ici si une source le couvrait déjà. Si oui → c'est un **trou de source à combler**.

## Les sources, par autorité

| Source | Ce qu'elle fait foi | Où |
|---|---|---|
| **Gold SELARL validé** | Référence de parité : tout autre type dérive par différence justifiée | générateurs `lot_04`, tests `test_lot_04_*` |
| **Corpus tokenisé / modèles .docx** | Wording exact des actes (verbatim juridique) | modèles source du client |
| **NotebookLM / transcripts Albane** | Règles métier/genre/pluriel/durée/légal | hors repo (NotebookLM) |
| **Specs ratifiées / journal de décisions** | Décisions produit déjà tranchées | `docs/review/`, journaux de décision |
| **Retours validés** | Ce que Rafael a explicitement confirmé | `VALIDES.md` |

## Ordre de consultation (INTEL GATE)

1. **NotebookLM / corpus tokenisé** d'abord (jamais sauté).
2. **Gold SELARL** (parité).
3. **Specs / journaux** ratifiés.
4. **Locks de retours** humains validés.
→ Info présente : l'utiliser. Absente/contradictoire : `BLOQUÉ` + question au sachant (jamais inventer).

## Trous de source identifiés (à combler)

- **2026-06-23 — Parité SELAS ↔ gold SELARL.** La majorité des retours de l'onglet 24 (adresses,
  valeur nominale, DNC par dirigeant, rôles, anti double-saisie, menu cession dérivé) étaient
  **ANTICIPABLES** : ils corrigent un **drift de la SELAS par rapport au gold SELARL**. La SELAS
  aurait dû être bâtie par parité stricte. **Action** : audit de parité SELAS↔gold (champ par champ,
  doc par doc) avant de rouvrir le dev — pour que ces écarts ne reviennent jamais un par un.
- **Machine = découverte, pas spec.** Le workflow bloc-gold a produit une paraphrase (« siège = lieu
  d'exercice » au lieu de « cabinet = lieu d'exercice ») qui a causé un faux. La source d'exécution
  reste le **verbatim client**, jamais la sortie machine. (cf. mémoire `feedback-machine-decouverte-pas-spec`.)
