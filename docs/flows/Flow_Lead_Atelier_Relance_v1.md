# Flow Lead / Atelier / Relance v1

Ticket source : `YB-S12-001`

Statut : canon fonctionnel a specifier en `YB-S12-003`, sans code produit.

## Objet

Ce flow remplace le modele implicite centre sur un pilote SELARL ou un tableau de
suivi unique. Le modele Sprint 12 est compose de trois blocs :

- `LEAD`
- `ATELIER`
- `RELANCE`

## Principes

- Le `LEAD` porte la qualification initiale et la prospection.
- L'`ATELIER` porte le traitement operationnel par bureau.
- La `RELANCE` porte les reprises visibles, avec deux etats distincts.
- Un dossier ouvert n'est pas un lead : c'est un contexte operationnel rattache
  au bureau et au traitement courant.

## Etats de relance

| Etat | Owner principal | Droits telepro | Notes |
|---|---|---|---|
| `RELANCE_TELEPRO` | Telepro / bureau concerne | Lecture + actions de relance autorisees par la future spec | Relance standard cote telepro. |
| `RELANCE_BOSS` | Boss de bureau ou atelier de bureau | Lecture seule + messagerie | Aucune modification structurante par telepro. |

## Transitions a specifier

`YB-S12-003` doit specifier :

- entree depuis lead qualifie vers atelier ;
- entree depuis atelier vers relance ;
- sortie de `RELANCE_TELEPRO` ;
- sortie de `RELANCE_BOSS` ;
- droits par role et bureau ;
- raisons visibles de blocage ou de reprise.

## Interdits Sprint 12

- Pas de retour au grand tableau Monday comme modele central.
- Pas de fusion cross-bureau dans une interface metier unique.
- Pas d'assimilation dossier ouvert = lead de prospection.
- Pas de role `chef telepro`.
