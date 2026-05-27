# YB-S12-001 Boss Delta - Cadrage canonique

Statut : source de cadrage session, capturee dans le repo pendant le bridge YB-S12-001.

Note : les fichiers `YB-S12-001_Boss_Delta_Cadrage_Canonique.md` et
`YB-S12-001_Boss_Delta_Arbitrages_PM.md` n'etaient pas presents sur disque au
pre-flight. Cette capture reprend le canon explicite fourni dans la mission
utilisateur afin que le repo dispose d'une trace durable. Si une piece jointe
complete est fournie plus tard, elle doit remplacer cette capture sans rouvrir
les arbitrages deja tranches.

## Canon Sprint 12

1. Le modele prioritaire devient `LEAD + ATELIER + RELANCE`.
2. Le grand tableau Monday ne redevient pas le modele central.
3. Un dossier ouvert n'est pas un simple lead de prospection.
4. Deux etats de relance doivent etre visibles : `RELANCE_TELEPRO` et
   `RELANCE_BOSS`.
5. En `RELANCE_BOSS`, la telepro est en lecture seule, peut utiliser la
   messagerie, mais ne modifie pas la structure du dossier.
6. `REFAIS_AG` invalide la qualification telepro initiale cote atelier, conserve
   explicitement le statut atelier `REFAIS_AG`, reste visible comme ancienne
   fiche refaitagee cote telepro et ne retourne pas en prospection brute.
7. Un atelier non attribue part dans une file manuelle a attribuer. Aucune
   auto-attribution de secours n'est retenue maintenant.
8. Le multi-bureaux est autorise pour les users autorises, avec contextes
   strictement separes par bureau et sans fusion de vues cross-bureau dans une
   seule interface metier.
9. Il n'y a pas de logique produit speciale `interne / externe` : ce sont des
   bureaux independants.
10. Sarah, Ethan et les autres sont des contextes atelier sur les bureaux
    concernes, sans statut systeme special.
11. Il n'y a pas de role `chef telepro` maintenant : ce besoin est ramene a
    `boss de bureau` ou `atelier de bureau`.

## Hors scope associe

- Aucun code produit metier dans YB-S12-001.
- Aucun nouveau sprint feature.
- Aucun nouveau travail Claude Design.
- Aucune production.
- Aucun hook.
- Aucun cleanup gouvernance Phase 2/3.
- Aucun cobaye, Naomi, provisioning ou launch.
- Aucune UAT reelle.
- Aucune refonte UI hors cadrage documentaire.
