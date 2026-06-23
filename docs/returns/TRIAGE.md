# TRIAGE — classement des retours (les 3 questions)

> Application de la grille (`METHODE.md` §5, règle 68) à chaque retour.
> **Q1 ANTICIPABLE ?** (nos sources couvraient-elles ?) · **Q2 NOUVEAUTÉ / ÉCART ?** · **Q3 BLOC-GOLD / MÉTIER ?**

## Verdict d'ensemble onglet 24

**Tout l'onglet 24 est BLOC-GOLD — aucune décision métier (Albane) requise.** Ce sont des corrections
de formulaire / fidélité à une intention déjà ratifiée. La majorité étaient **ANTICIPABLES** par parité
stricte au gold SELARL : c'est là le vrai trou (cf. `SOURCES_DE_VERITE.md`) — la SELAS a dérivé du gold.

| ID | Q1 anticipable ? | Q2 | Q3 | Note |
|---|---|---|---|---|
| O24-01 | OUI (gold sans annexe Sydel) | ÉCART | BLOC-GOLD | annexe Sydel à ne jamais réintroduire |
| O24-02 | OUI (pattern DNC du gold) | ÉCART | BLOC-GOLD | nom du dirigeant dans le fichier ; tous types |
| O24-03 | OUI partiel (gold ordre = 1 ligne ; perso/siège structurés = drift) | ÉCART | BLOC-GOLD | fusionner les champs ; parser pour les générateurs |
| O24-04 | NON (préférence UI client) | NOUVEAUTÉ | BLOC-GOLD | rendu Streamlit pur, pas de métier |
| O24-05 | OUI (valeur dérivable) | ÉCART | BLOC-GOLD | bug `value=`+`key=` qui figeait l'affichage |
| O24-06 | OUI partiel | NOUVEAUTÉ (vocabulaire) | BLOC-GOLD | un seul cas SELAS multi |
| O24-07 | OUI (corpus rôles) | ÉCART (DGA manquant) | BLOC-GOLD | non-cumul, bornes |
| O24-08 | OUI (anti double-saisie gold) | ÉCART | BLOC-GOLD | date + adresse saisies 1× |
| O24-09 | OUI partiel | ÉCART | BLOC-GOLD | label « (profession) » |
| O24-10 | OUI (dérivable de la profession) | ÉCART | BLOC-GOLD | menu retiré |
| O24-11 | OUI (multi-associés) | ÉCART | BLOC-GOLD | vendeur sélectionnable |
| O24-12 | NON (commodité UI client) | NOUVEAUTÉ | BLOC-GOLD | case sur le CABINET, dépend de O24-03 |
| O24-13 | OUI partiel | ÉCART | BLOC-GOLD | CA + exercices requis |
| O24-14 | NON partiel | NOUVEAUTÉ | BLOC-GOLD | acte ET compromis ensemble |
| O24-15 | OUI (acquéreur = la société) | ÉCART | BLOC-GOLD | champ retiré |

## Retours live

| ID | Q1 | Q2 | Q3 | Note |
|---|---|---|---|---|
| LIVE-01 | OUI (gold SELARL porte le menu régime) | ÉCART | BLOC-GOLD | situation = menu, comme SELARL |
| LIVE-02 | OUI | ÉCART | BLOC-GOLD | case régime retirée |
| LIVE-03 | OUI (convention sortie) | ÉCART | BLOC-GOLD | mois accentués (règle globale posée) |
| LIVE-04 | OUI | ÉCART | BLOC-GOLD | découle de O24-14 |
| LIVE-05 | — | — | — | **CLARIF** : screenshot illisible, sens à confirmer |
| LIVE-06 | — | — | — | **CLARIF** : screenshot illisible, sens à confirmer |

## Conséquences actionnables du triage

1. **Trou de source confirmé** → la SELAS aurait dû être bâtie par **parité stricte au gold SELARL** ;
   le drift a généré la majorité de ces retours. Action : audit de parité SELAS↔gold avant de rouvrir le dev
   (noté dans `SOURCES_DE_VERITE.md`).
2. **Aucune question Albane** sur ce lot : 100 % bloc-gold, traitable en autonomie.
3. **LIVE-05 / LIVE-06** : seuls vrais bloquants d'info → clarification Rafael (screenshots).
