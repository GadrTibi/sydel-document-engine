# Flow Contextes MultiBureaux v2

Ticket source : `YB-S12-001`

Statut : canon fonctionnel a specifier en `YB-S12-002`, sans code produit.

## Definition

Le multi-bureaux est autorise pour les users autorises, mais les contextes sont
strictement separes par bureau.

## Regles

1. Un user autorise peut acceder a plusieurs bureaux.
2. Chaque bureau garde son contexte metier separe.
3. Une interface metier ne fusionne pas plusieurs bureaux dans une vue unique de
   travail.
4. Les transitions Lead / Atelier / Relance sont evaluees dans le contexte du
   bureau courant.
5. `interne / externe` n'est pas une logique produit speciale.
6. Sarah, Ethan ou autres noms propres designent des contextes atelier sur les
   bureaux concernes, pas des statuts systeme.

## UI / produit

Le futur front peut proposer un selecteur de bureau ou de contexte, mais ne doit
pas afficher une vue metier fusionnee cross-bureau pour agir sur les dossiers.

## Points a specifier dans YB-S12-002

- modele des users autorises multi-bureaux ;
- separation des donnees par bureau ;
- droits de lecture/ecriture par bureau ;
- comportement de changement de bureau ;
- garde-fous contre les actions sur le mauvais contexte ;
- traces d'audit minimales.
