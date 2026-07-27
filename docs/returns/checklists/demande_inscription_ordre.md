# CHECKLIST MAÎTRE — Demande d'inscription à l'Ordre (DOC-034)

> Code : `generators/lot_02/demande_inscription_ordre.py` — générateur UNIQUE partagé
> **SELARL · SELAS · SPFPL cession · SPFPL apport · SCM** (5 types).
> Tout fix se propage automatiquement aux 5 — vérifier la byte-neutralité des 4 autres.
> S'ajoute à `_transverse.md`.

## Attentes cumulées

- [x] Mise en forme : **VALIDÉE par Albane** (« C'est juste parfait :) » A26 §8 ; « mise en forme VALIDÉE » 9.1, 2026-07-06) — **ne pas dégrader** ; toute retouche = régression à prouver nulle
- [x] 9.2 Destinataire : département de l'Ordre en NOM (« Seine-et-Marne », jamais « 77 ») — Albane 2026-07-06 — statut : **fait** (propagation 2 tours Akainu, registre 2026-07-06)
- [x] 9.3 Préposition de/du/des devant le département (« de Seine-et-Marne / du Jura / des Bouches-du-Rhône ») — Albane 2026-07-06 — statut : **fait** (déjà présent au moment de la cartographie)
- [x] Ordre des mots destinataire : « Conseil départemental de l'Ordre des {profession} **de** {département} » (profession PUIS département) — SU2/R5, tranché Rafael 2026-07-01 « comme les modèles » — statut : **fait** (commit `fc91f6f`, Akainu RIEN À REDIRE ; apostrophe typographique U+2019 uniforme = décision assumée). NB : la **contradiction interne Albane** (02/06 « garder de l'Ordre » ⟂ 25/06 « supprimer de l'Ordre », tracée SU2) est **close** par cet arbitrage — ne pas rouvrir sans nouveau verbatim
- [ ] 9.4 Champ « Conseil départemental » : supprimer s'il est inutile ; garder un seul champ « Département de l'Ordre (nom, ex. Seine-et-Marne) » — Albane 2026-07-06 — statut : **pas fait / à vérifier** (rebasculé BUILDABLE le 2026-07-06 : champ MORT, zéro consommateur → suppression à exécuter ou à confirmer faite)
- [x] Signature du client à droite — mise en forme 1.5 (2026-07-03) — statut : **fait**
- [x] Mention de dérogation manuelle si `dossier.options.derogation` — spec lot 2 — statut : **fait** (structurel)
- [x] SCM : accepté uniquement avec données ordinales explicites — spec lot 2 — statut : **fait** (structurel)
- [ ] Transverse 07-07 (« Docteur » ≠ civilité, accents, élision) — statut : **à vérifier** par régénération sur les 5 types (doc validé : ne toucher QUE si un défaut réel est prouvé sur la sortie)

## Rappels

- Document **VALIDÉ client** : la charge de la preuve s'inverse — on ne touche que sur verbatim explicite, et on re-prouve le byte-identique sur ce qui n'est pas visé.
- Porté par 5 types dont SCM : un fix testé sur SPFPL doit être régénéré sur SELARL/SELAS/SCM aussi.
