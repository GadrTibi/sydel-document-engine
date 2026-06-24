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
| O24-02 | « Dans tous les cas où il y a une déclaration de non condamnation, elle doit être générée d'office pour chaque dirigeant uniquement. Le nom du document doit intégrer le nom du dirigeant … » | tous types | — | TRAITÉ | ⬜ |
| O24-03 | « Toutes les adresses doivent être rédigées sur une ligne, pas de champ séparé pour la rue, la voie, etc.. » | **tous types (UX)** | — | TRAITÉ (propagé tous types, golden-bloc `address_oneline`) | ⬜ |
| O24-04 | « Ajouter une icone "copier" à côté de chaque champ texte pour copier le texte contenu à l'intérieur d'un champ » | **tous types (UI)** | — | TRAITÉ | ⬜ |
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
| LIVE-05 | « ajoute lettre de renonciation » | live 23-06 | LIVE-06 | TRAITÉ | ⬜ |
| LIVE-06 | « supprimer cette case à la fin, ne sert à rien » | live 23-06 | — | TRAITÉ | ⬜ |

> **L5 + L6 = UN seul point** (clarifié Gad 2026-06-24) : « ajoute lettre de renonciation » n'était pas une demande séparée, c'est le **texte entre parenthèses** de la case à supprimer = « **Régime communautaire (ajoute lettre de renonciation + avertissement au conjoint)** ». Cette case survivait sur le **formulaire SPFPL** (retirée de SELAS par LIVE-02). Remplacée par un **menu « Régime matrimonial »** (4 régimes mariés) qui dérive le régime + le déclencheur DOC-005/006 (communauté légale). Gate Akainu = RIEN À REDIRE (régénération réelle 4 régimes). Commit `aa00fc6`.

## Retours 2026-06-24 (batch N — Rafael/Albane) — `N`

| # | verbatim | périmètre | statut | validé |
|---|---|---|---|---|
| N1 | « le capital doit être divisible / la valeur nominale doit être un entier → enlever ça » (la valeur nominale PEUT être décimale, partout) | tous types | TRAITÉ (figure décimale rendue ; **lettres décimale flaggée Albane** = interim figure 2×). Gate Akainu (3 boucles). | ⬜ |
| N2 | « il y a deux fois la date de décision, enlever un des deux » | tous types (champ date partagé) | TRAITÉ (libellé calendrier replié `label_visibility=collapsed` + test). Gate Akainu. | ⬜ |
| N3 | « fais en sorte que tous les montants en lettres soient écrits automatiquement » | tous types | TRAITÉ (déjà auto, 46 sites, 0 manuel). | ⬜ |
| N4 | « calcule automatiquement la plage de parts » | SCM cession (+ statuts) | TRAITÉ (plages présents/cédées/total auto ; **accent « 1 a/à N » flaggé Albane** ; sous-ens. SPFPL = convention Rafael). Gate Akainu **RIEN À REDIRE**. | ⬜ |
| N5 | « j'ai fait le test avec deux associés et en cours de test j'en ai ajouté un qui a supprimé les champs des deux précédents » (Albane) | tous formulaires multi-associés (SELAS, civil/SCI/SCM, SELARL) | TRAITÉ (st.rerun prématuré retiré des 3 repeaters + 3 tests de régression). Gate Akainu **RIEN À REDIRE**. | ⬜ |
| N6 | « Ajouter l'en-tête Statuts. Aérer entre les associés. Remettre les tirets dans la liste de l'article 1. Faire démarrer l'annexe sur une nouvelle page. » | statuts SELAS (médecin + dentiste) | TRAITÉ pt1 (en-tête) + pt3 (**tirets systémiques** via style Word, 25 puces) + pt4 (annexe nouvelle page) + tests ; **pt2 aération flaggée Rafael**. Gate Akainu **RIEN À REDIRE**. | ⬜ |

> Batch N = retours du 2026-06-24 (postérieurs aux 21 O24+LIVE). Tous **Akainu-gatés** (boucle règle 66 close cette session, commits N5 `a951935`, N4 `3b6a159`, N6 `7d47287`+test). Flags métier non bloquants tracés dans `QUESTIONS_RAFAEL.md` (lettres décimale N1, accent plages N4, aération N6).

## Synthèse machine-lisible

- **Reste à faire (constructible)** : **AUCUN** — les 21 retours sont TRAITÉS. `O24-04` (icône copier
  tous types) traité 2026-06-24, gate Akainu RIEN À REDIRE ; reste seulement la **validation visuelle
  du copier réel** par Gad/Rafael sur le staging (JS client, non testable en headless).
- **Règle de propagation (Q4 triage, Gad 2026-06-23)** : un retour universel se propage à TOUS les cas concernés ; O24-01/02/03/05 propagés ; O24-06→15 = SELAS-pluri structurel (pas de propagation).
- **✅ CONVERGENCE Akainu (tour 10, 2026-06-24)** : les défauts ré-ouverts par le verdict 23-06
  (`AKAINU_VERDICT_2026-06-23.md` : 8 bloquant + 16 majeur) sont **tous re-corrigés à la racine et
  re-vérifiés** (sprint de nuit, 29 commits, HEAD `44f7dda`). Gate tour 10 = **CONVERGENCE OUI**
  (0 bloquant, 0 majeur ; 2 mineur de véracité doc corrigés). Suite **594 verts**, ordre-indépendance
  prouvée. Détail : `DEBRIEF_SPRINT_NUIT_2026-06-24.md`.
- **TRAITÉ (≠ validé), en attente retest Rafael** : **les 21** (O24-01→15 + LIVE-01→06) **+ le batch N (N1→N6, 2026-06-24, Akainu-gaté règle 66)**.
- **VALIDÉ** : aucun → le carnet reste plein (Rafael doit retester une fois le canal de déploiement
  tranché — voir DEBRIEF § 7).
