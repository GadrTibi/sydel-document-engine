# Méthode de classement des retours — le rulebook

> **But** : classer chaque retour de manière déterministe, professionnelle, vérifiable à la machine.
> Personne n'improvise le classement : on applique CES règles. Propriétaire : Vivi (`returns-intake-organizer`).
> Complète la règle globale `~/.claude/rules/68-returns-triage-gate.md`.
> Inspiré des bonnes idées de Task Master AI (source unique versionnée, statut grep-able, dépendances
> explicites, IDs hiérarchiques) — **sans** sa génération IA qui reformulerait le verbatim.

## 1. Identifiant (ID) — convention stable

- `O24-NN` : retour de l'**onglet 24** (NN = ordre dans l'onglet, ex. `O24-12`).
- `LIVE-NN` : retour **live** de Rafael (NN = ordre de réception ; la date va dans `Source`).
- `ALB-NN` : retour / arbitrage d'**Albane** (métier ou juridique).
- Sous-point : `O24-12.1`, `O24-12.2` quand un retour se découpe en corrections distinctes.
- **Un ID ne change jamais et ne se réutilise jamais.** (les anciens `#12` / `L1` = `O24-12` / `LIVE-01`.)

## 2. Schéma stable d'un retour (un retour = une ligne, mêmes champs partout)

| Champ | Règle de remplissage |
|---|---|
| **ID** | cf. §1 |
| **Source** | `onglet 24` / `live Rafael (JJ-MM)` / `Albane (JJ-MM)` |
| **Verbatim** | mot pour mot, **jamais paraphrasé** (sinon ce n'est plus la spec) |
| **Statut** | un mot du vocabulaire FERMÉ §3 |
| **Validé** | ⬜ ou ✅ (§4) |
| **Triage** | verdicts Q1 / Q2 / Q3 (§5), détaillés dans `TRIAGE.md` |
| **Dépend de** | IDs bloquants (§6), vide si aucun |
| **Périmètre** | types / surfaces touchés (ex. `SELAS`, `tous types`, `cession`) |

## 3. Vocabulaire de statut — liste FERMÉE, grep-able

Un seul mot, en MAJUSCULES, vérifiable par un agent sans interprétation :

| Statut | Sens |
|---|---|
| `NOUVEAU` | capturé verbatim, pas encore trié |
| `TRIÉ` | grille de triage remplie, pas encore confié |
| `DISPATCHÉ` | confié au traitement (Chopper / tech lead) |
| `TRAITÉ` | fait + poussé + **vérifié contre le verbatim** — en attente validation |
| `VALIDÉ` | confirmé par le client → quitte le carnet vers `VALIDES.md` |
| `CLARIF` | bloqué sur une clarification (verbatim ambigu / illisible) |
| `BLOQUÉ` | bloqué sur une décision métier (Albane) |

**Transitions autorisées** : `NOUVEAU → TRIÉ → DISPATCHÉ → TRAITÉ → VALIDÉ`.
Depuis n'importe quel état on peut basculer en `CLARIF` ou `BLOQUÉ`, puis revenir.

## 4. Deux axes ORTHOGONAUX : Statut (nous) vs Validé (client)

- **Statut** = où on en est *de notre côté*.
- **Validé** = le client a confirmé, ou non. Axe séparé, jamais déduit du statut.
- **Règle dure** : `Validé = ✅` est posé UNIQUEMENT sur un mot explicite de Rafael. Jamais par nous, jamais par un test vert, jamais par « ça me semble bon ».
- Un retour quitte `CARNET.md` pour `VALIDES.md` **seulement** quand `Validé = ✅`.

## 5. Grille de triage — les 3 questions (règle 68)

Pour chaque retour, réponse consignée dans `TRIAGE.md` :

1. **Q1 — ANTICIPABLE ?** Nos sources de vérité (`SOURCES_DE_VERITE.md`) couvraient-elles le point ?
   `OUI` → trou de source à combler (l'inscrire dans `SOURCES_DE_VERITE.md`), pas juste un fix.
   `NON` → retour genuinement neuf.
2. **Q2 — NOUVEAUTÉ ou ÉCART ?** `NOUVEAUTÉ` = intention métier inédite. `ÉCART` = on s'était trompé
   vs une intention déjà ratifiée → **chercher les autres occurrences du même écart**.
3. **Q3 — BLOC-GOLD ou MÉTIER ?** `BLOC-GOLD` = dérivable du déterministe → dispatchable.
   `MÉTIER` = dépasse les sources → `Statut = BLOQUÉ` + question au sachant (Albane via Gad). Jamais inventer.

## 6. Dépendances explicites

- `Dépend de : O24-03` quand un retour ne peut être traité avant un autre.
- **Avant de dispatcher** un retour, vérifier que toutes ses dépendances sont au moins `TRAITÉ`.
- Exemple réel : `O24-12` (case « adresse cabinet = lieu d'exercice ») **dépend de** `O24-03`
  (adresses sur une ligne) — inutile de câbler la copie tant que l'adresse n'est pas en une ligne.

## 7. Cadence (non négociable)

- Tout nouveau retour → **INTAKE immédiat** (ID + verbatim), même flou.
- **Re-montrer le carnet COMPLET** avant de traiter l'item suivant.
- Vérification clause par clause contre le **verbatim**, jamais contre la paraphrase d'un workflow.

## 8. Où vit quoi

`CARNET.md` (file active) · `TRIAGE.md` (classements) · `JOURNAL.md` (historique daté) ·
`VALIDES.md` (archive validée) · `SOURCES_DE_VERITE.md` (corpus de référence). Carte : `README.md`.
