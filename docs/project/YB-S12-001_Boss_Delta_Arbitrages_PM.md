# YB-S12-001 Boss Delta - Arbitrages PM

Statut : arbitrages PM figes pour Sprint 12.

## Decisions non rouvertes

| Sujet | Arbitrage PM Sprint 12 |
|---|---|
| Modele central | `LEAD + ATELIER + RELANCE`, pas Monday. |
| Nature du dossier ouvert | Le dossier ouvert est un contexte operationnel, pas un lead de prospection. |
| Relance | Deux etats visibles : `RELANCE_TELEPRO` et `RELANCE_BOSS`. |
| Relance boss | Telepro lecture seule, messagerie autorisee, aucune modification structurante. |
| REFAIS_AG | Atelier invalide la qualification telepro initiale ; statut atelier conserve `REFAIS_AG`; ancienne fiche refaitagee visible cote telepro ; pas de retour prospection brute. |
| Atelier non attribue | File manuelle a attribuer ; aucune auto-attribution fallback. |
| Multi-bureaux | Autorise pour users autorises ; contextes separes par bureau ; pas de vue metier fusionnee cross-bureau. |
| Interne / externe | Pas de logique produit speciale ; bureaux independants. |
| Sarah / Ethan / autres | Contextes atelier sur bureaux concernes ; pas de statut systeme special. |
| Chef telepro | Pas maintenant ; ramene a boss de bureau ou atelier de bureau. |

## Mise en pause explicite

- Le pilote cobayes, Naomi, provisioning, launch et UAT reelle sont en pause tant
  que le bridge Boss Delta n'est pas absorbe.
- Les branches pilote/cobaye eventuelles ne doivent pas etre touchees dans ce
  bridge.
- Aucun ticket design Claude ne doit etre lance.

## Ordre de tickets impose

1. `YB-S12-001` Boss Delta Bridge.
2. `YB-S12-002` Multi-contextes multi-bureaux.
3. `YB-S12-003` Modele multi-blocs Lead / Atelier / Relance.
4. `YB-S12-004` REFAIS_AG + relance telepro.
5. `YB-S12-005` Relance boss.
6. `YB-S12-006` Affectation atelier par bureau.
7. `YB-S12-007` Rebuild pilote / UAT.
