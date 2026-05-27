# Flow REFAIS_AG v2

Ticket source : `YB-S12-001`

Statut : canon fonctionnel a specifier en `YB-S12-004`, sans code produit.

## Definition

`REFAIS_AG` signifie que l'atelier invalide la qualification telepro initiale.

Ce n'est pas un simple retour en prospection. C'est un etat atelier explicite
avec historique conserve.

## Regles canonisees

1. L'atelier invalide la qualification telepro initiale.
2. Le statut atelier reste explicitement `REFAIS_AG`.
3. La telepro voit toujours que c'est une ancienne fiche refaitagee.
4. La fiche ne retourne pas dans la prospection brute.
5. La suite doit passer par le modele Sprint 12 `LEAD + ATELIER + RELANCE`.

## Visibilite minimale

| Zone | Information visible |
|---|---|
| Atelier | Statut `REFAIS_AG`, raison de refaitage, bureau concerne, owner courant. |
| Telepro | Ancienne fiche refaitagee, historique de qualification invalidee, etat de relance si applicable. |
| Boss de bureau | Contexte bureau, etat de relance, decision attendue. |

## Points a specifier dans YB-S12-004

- liste exacte des raisons `REFAIS_AG` ;
- transitions autorisees depuis `REFAIS_AG` ;
- lien entre `REFAIS_AG` et `RELANCE_TELEPRO` ;
- niveau de lecture ou action cote telepro ;
- trace d'historique minimale ;
- criteres empechant le retour prospection brute.
