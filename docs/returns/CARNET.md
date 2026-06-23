# CARNET — retours client actifs

> **File active des retours NON validés.** Un retour reste ici tant que `Validé ≠ ✅`.
> Schéma & règles de classement : [`METHODE.md`](METHODE.md). Triage détaillé : [`TRIAGE.md`](TRIAGE.md).
> Historique : [`JOURNAL.md`](JOURNAL.md). Carte : [`README.md`](README.md).
>
> **Statut** (nous) ∈ `NOUVEAU · TRIÉ · DISPATCHÉ · TRAITÉ · VALIDÉ · CLARIF · BLOQUÉ`.
> **Validé** (client) ∈ `⬜ · ✅`. Verbatim = mot exact du client.

## Onglet 24 — `O24` (« ne parle que de la SELAS »)

| ID | Verbatim exact | Périmètre | Dépend de | Statut | Validé |
|---|---|---|---|---|---|
| O24-01 | « Supprimer : Signature d'une lettre de mission … / Paiement de l'acompte des honoraires du cabinet Sydel … dans l'annexe de tous les statuts de tous les cas » | tous types | — | TRAITÉ | ⬜ |
| O24-02 | « Dans tous les cas où il y a une déclaration de non condamnation, elle doit être générée d'office pour chaque dirigeant uniquement. Le nom du document doit intégrer le nom du dirigeant … » | tous types | — | DISPATCHÉ | ⬜ |
| O24-03 | « Toutes les adresses doivent être rédigées sur une ligne, pas de champ séparé pour la rue, la voie, etc.. » | SELAS (UI) | — | TRAITÉ | ⬜ |
| O24-04 | « Ajouter une icone "copier" à côté de chaque champ texte pour copier le texte contenu à l'intérieur d'un champ » | SELAS (UI) | — | TRIÉ | ⬜ |
| O24-05 | « la valeur nominale d'une part/action doit être calculée automatiquement et affichée dans le champ concerné » | tous types | — | TRAITÉ | ⬜ |
| O24-06 | « pluripersonnelle et multi associé veut dire la meme chose » | SELAS | — | TRAITÉ | ⬜ |
| O24-07 | « soit président (un seul), soit directeur général (un seul), soit directeur général associé (plusieurs) — non cumulatives » | SELAS | — | TRAITÉ | ⬜ |
| O24-08 | « la date de naissance apparait deux fois → une seule fois ; l'adresse apparait aussi deux fois → une seule fois » | SELAS | — | TRAITÉ | ⬜ |
| O24-09 | « supprimer le champ profession → laisser "qualification principale" et mentionner "(profession)" dans le nom du champ » | SELAS | — | TRAITÉ | ⬜ |
| O24-10 | « menu cession cabinet "dentaire"/"médical" → supprimer ce champ, cela va de soi selon le cas » | SELAS (cession) | — | TRAITÉ | ⬜ |
| O24-11 | « cession → vendeur : supprimer "le vendeur est l'associé unique" … à la place, choisir l'un des associés et reprendre toutes ses informations » | SELAS (cession) | — | TRAITÉ | ⬜ |
| O24-12 | « adresse du cabinet → ajouter une case : "même adresse que le lieu d'exercice" et reporter les données si cochée. » | SELAS (cession) | O24-03 | TRAITÉ | ⬜ |
| O24-13 | « Le CA ne doit pas être facultatif — mm chose pour les exercices » | SELAS (cession) | — | TRAITÉ | ⬜ |
| O24-14 | « Ajouter le fait de remplir à la fois l'acte ainsi que le compromis de cession en meme temps » | SELAS (cession) | — | TRAITÉ | ⬜ |
| O24-15 | « Retirer le champ acquéreur » | SELAS (cession) | — | TRAITÉ | ⬜ |

> `O24-12` corrigé : la case est désormais sur l'adresse du **cabinet** (cession), conforme au verbatim ; le faux essai sur le siège a été retiré (O24-03).

## Retours live Rafael — `LIVE`

| ID | Verbatim / sens exact | Source | Dépend de | Statut | Validé |
|---|---|---|---|---|---|
| LIVE-01 | « pour la situation matrimoniale de l'associé — mets le même que le régime matrimonial sur la SELARL » (communauté → conjoint + docs) | live 23-06 | — | TRAITÉ | ⬜ |
| LIVE-02 | « Supprime le champ à cocher "marié sous un régime communautaire" » | live 23-06 | — | TRAITÉ | ⬜ |
| LIVE-03 | « decembre → décembre » (+ règle globale mois accentués) | live 23-06 | — | TRAITÉ | ⬜ |
| LIVE-04 | Cession : retirer le CHOIX acte/compromis (menu Étape) — découle de O24-14 | live 23-06 | O24-14 | TRAITÉ | ⬜ |
| LIVE-05 | « ajoute lettre de renonciation » *(réf. mini-screenshot illisible)* | live 23-06 | — | CLARIF | ⬜ |
| LIVE-06 | « supprimer cette case à la fin, ne sert à rien » *(réf. mini-screenshot illisible)* | live 23-06 | — | CLARIF | ⬜ |

## Synthèse machine-lisible

- **Reste à faire** (Statut ≠ TRAITÉ/VALIDÉ) : `O24-02` (DISPATCHÉ, à généraliser), `O24-04` ; `LIVE-05`/`LIVE-06` (CLARIF).
- **En attente validation Rafael** (TRAITÉ, `Validé = ⬜`) : O24-01/03/05/06/07/08/09/10/11/12/13/14/15 + LIVE-01/02/03/04.
- **VALIDÉ** : aucun → le carnet reste plein (Rafael doit retester `sprint/engine-completion`).
