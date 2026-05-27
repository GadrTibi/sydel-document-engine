# Specification fonctionnelle

Statut : spec fonctionnelle vivante, initialisee par YB-S12-001.

## Canon Sprint 12

Le produit cible prioritaire repose sur trois blocs operationnels :

1. `LEAD`
2. `ATELIER`
3. `RELANCE`

Le dossier ouvert est un contexte operationnel distinct. Il ne doit pas etre
ramene a un lead de prospection simple.

## Relance

Deux etats sont visibles :

- `RELANCE_TELEPRO`
- `RELANCE_BOSS`

En `RELANCE_BOSS` :

- la telepro lit le dossier ;
- la telepro peut utiliser la messagerie ;
- la telepro ne modifie pas les donnees structurantes ;
- le boss de bureau ou l'atelier de bureau portent la suite de traitement.

## REFAIS_AG

`REFAIS_AG` signifie que l'atelier invalide la qualification telepro initiale.

Regles :

- le statut atelier reste explicitement `REFAIS_AG` ;
- la telepro voit toujours que la fiche vient d'un ancien refaitage ;
- la fiche ne retourne pas en prospection brute ;
- la suite passe par le flow de relance/traitement defini dans Sprint 12.

## Multi-bureaux

Un utilisateur autorise peut acceder a plusieurs bureaux.

Regles :

- chaque bureau a son contexte strictement separe ;
- aucune vue metier unique ne fusionne plusieurs bureaux ;
- `interne / externe` n'est pas un statut produit special ;
- Sarah, Ethan et autres noms propres sont des contextes atelier de bureau, pas
  des statuts systeme.

## Atelier non attribue

Un atelier non attribue va dans une file manuelle a attribuer.

Il n'y a aucune auto-attribution de secours dans le canon Sprint 12.

## Roles

Pas de role `chef telepro` maintenant.

Les responsabilites sont ramenees a :

- boss de bureau ;
- atelier de bureau ;
- telepro selon etat et droits.

## Pause pilote

Le pilote cobayes, Naomi, provisioning, launch et UAT reelle sont suspendus tant
que les tickets `YB-S12-002` a `YB-S12-006` ne sont pas absorbes.
