# Questions en attente pour Rafael / Albane — refonte SELAS (onglet 24)

> Points où un arbitrage **métier / wording d'acte** est nécessaire. Politique (Gad 2026-06-22) :
> on NE bloque PAS et on NE demande PAS à Gad — on applique le **défaut le plus simple / sûr** ci-dessous,
> on accumule ici, Rafael/Albane tranchent plus tard, on rajuste au besoin.

| # | Question | Défaut appliqué (réversible) |
|---|---|---|
| #9 | En retirant le champ « profession » (garder « qualification »), la comparution doit-elle **garder le titre « Docteur »** (« Docteur Médecin généraliste… ») ou **ne montrer que la qualification** (« Médecin généraliste… ») ? | **Titre « Docteur » conservé et dérivé** → output de l'acte INCHANGÉ ; seul le champ disparaît du formulaire. |
| #2 ✅ TRANCHÉ (Rafael 2026-06-23) | DNC par dirigeant ou une seule ? | **RÉPONDU : une DNC PAR dirigeant** (Président + chaque DG / DG Associé). Implémenté (`4622b8a`). |
| Appel de fonds (DOC-008) | En cession de cabinet **SELAS**, faut-il générer un **appel de fonds** comme en SELARL ? | **Non inscrit** au plan SELAS (le moteur le restreint à la SELARL). |
| #12 | La case « siège = lieu d'exercice » remplace l'ancienne « siège = adresse président » : on garde uniquement « = lieu d'exercice », ou les deux ? Et le **lieu d'exercice** reste 1 champ libre (parsé vers le siège structuré) — faut-il le **restructurer en 4 champs** (No/Voie/CP/Ville) ? | « = lieu d'exercice » **remplace** « = président » ; lieu d'exercice **reste 1 champ** parsé best-effort. |
| B3 (technique) | Le champ libre « Siège (adresse affichée) » est redondant avec les 4 champs structurés (SELAS uni est propre). Le retirer changerait la validation « Siège requis ». | **Conservé** pour l'instant (retrait = dette technique, sans impact métier). |
