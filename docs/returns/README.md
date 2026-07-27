# Bureau des retours client — `docs/returns/`

> Hub unique de la **chaîne des retours** : collecte → classe → dispatche → suit.
> Propriétaire : agent **Vivi** (`returns-intake-organizer`). Règle : `~/.claude/rules/68-returns-triage-gate.md`.

## La carte (ça c'est là, ça c'est là)

| Fichier | Rôle | Qui écrit |
|---|---|---|
| [`METHODE.md`](METHODE.md) | **Le rulebook** : IDs, schéma stable, vocabulaire de statut, dépendances, double axe traité/validé. Comment on classe — sans improviser. | tech lead / Vivi |
| [`CARNET.md`](CARNET.md) | **File active** : tous les retours NON validés, un par ligne, état courant. Source de vérité du « reste à faire ». | Vivi + tech lead |
| [`TRIAGE.md`](TRIAGE.md) | **Classement** de chaque retour : les 3 questions (anticipable ? nouveauté ? bloc-gold ?) + verdict. | Vivi |
| [`JOURNAL.md`](JOURNAL.md) | **Historique daté** : qui a fait quoi, quand. On n'efface jamais. | tech lead |
| [`VALIDES.md`](VALIDES.md) | **Archive** : retours sortis du carnet UNIQUEMENT après validation client. | Vivi |
| [`SOURCES_DE_VERITE.md`](SOURCES_DE_VERITE.md) | **Corpus de référence** consulté AVANT tout triage (gold, modèles, NotebookLM, specs). Base du test d'anticipabilité. | tech lead |

## Les 2 lois

1. **TRAITÉ ≠ VALIDÉ.** « Traité » = fait + poussé par nous. « Validé » = le client (Rafael) a confirmé. Un retour sort du carnet **seulement** quand il est VALIDÉ.
2. **Verbatim = spec, machine = découverte.** On vérifie chaque retour clause par clause contre le **mot exact du client**, jamais contre la paraphrase d'un workflow / bloc-gold.

## Le flux (comme une petite entreprise)

```
  RETOUR CLIENT (verbatim)
        │
        ▼
  [INTAKE]   Vivi note le verbatim exact dans CARNET.md            → état NOUVEAU
        │
        ▼
  [TRIAGE]   Vivi répond aux 3 questions dans TRIAGE.md
        │     Q1 anticipable ?  Q2 nouveauté/écart ?  Q3 bloc-gold/métier ?
        ▼
  [DISPATCH] → bloc-gold : Chopper / tech lead implémente          → état DISPATCHÉ
             → décision métier : question au sachant (Albane via Gad)
        │
        ▼
  [TRAITÉ]   fix poussé, vérifié contre le verbatim                → état TRAITÉ (en attente validation)
        │
        ▼
  [VALIDÉ]   Rafael confirme → déplacé dans VALIDES.md             → sort du carnet actif
```

## Cadence imposée

Avant de traiter le retour suivant, on **re-montre le carnet complet** (tous items, tous états). Jamais sauter.
