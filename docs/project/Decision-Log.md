# Decision Log

## YB-S12-001 - Boss Delta Bridge

Date : 2026-05-27

Statut : PM canonise, sans code produit.

### Decisions

1. Le nouveau canon Sprint 12 est `LEAD + ATELIER + RELANCE`.
2. Le grand tableau Monday ne redevient pas le modele central.
3. Un dossier ouvert n'est pas assimile a un lead de prospection.
4. Les relances visibles sont separees en `RELANCE_TELEPRO` et `RELANCE_BOSS`.
5. En `RELANCE_BOSS`, la telepro est lecture seule, sauf messagerie autorisee.
6. `REFAIS_AG` ne retourne pas en prospection brute et conserve son historique
   visible cote telepro.
7. Les ateliers non attribues passent par une file manuelle.
8. Le multi-bureaux est autorise uniquement avec contextes strictement separes
   par bureau.
9. `interne / externe` n'est pas un axe produit special : chaque bureau reste un
   bureau independant.
10. Sarah, Ethan et autres personnes nommees ne creent pas de statut systeme.
11. Aucun role `chef telepro` n'est introduit maintenant.

### Consequences

- Les anciens points de canon centres sur un pilote SELARL, un utilisateur a
  contexte unique, ou un prochain test cobaye sont suspendus.
- Le projet repart en cadrage Sprint 12 avant tout code.
- Les prochains tickets doivent absorber les contextes multi-bureaux, les blocs
  Lead/Atelier/Relance, puis les cas REFAIS_AG et relance boss.
