# Registre des retours (Rafael · Albane) — checklist vivante

> Chaque retour est saisi **une fois** et appliqué à **tous les types concernés**.
> Méthode : `../METHODE_PARITE_GOLD.md`. Un retour « parité » porté sur un type doit l'être sur tous.

## Légende
- **Type** : `bug` (bloque la génération) · `parité` (existe sur le gold SELARL, manque ailleurs) ·
  `UX` (idée neuve, n'existe nulle part) · `métier` (à valider Albane).
- **Statut** : `ouvert` / `en cours` / `fait` / `bloqué`.

## Retours Rafael — SELAS pluripersonnelle (2026-06-19)

| id | type | retour | portée | statut |
|----|------|--------|--------|--------|
| RAF-001 | bug | Régime communautaire bloquait (CODE-RC-001, date d'avertissement absente) → **vérifié : c'était la SELAS UNI MÉDECIN** (adaptateur SELARL oubliait la date), pas la pluri (immune). **Corrigé** + test non-régression (HEAD `7053de6`). | SELAS uni médecin | **fait** |
| RAF-002 | parité | Valeur nominale d'action visible mais non modifiable (calculée) | SELAS pluri | **déjà fait** (disabled=True, l.281-287) |
| RAF-003a | parité | Case « siège = adresse perso » (pure front, clone gold shell.py:1453-1469) | SELAS pluri | en cours |
| RAF-003b | parité/moteur | 2e lieu d'exercice → **SCOPE-BREAKER** : le générateur SELAS code « lieu unique » en dur → moteur + template + **modèle Albane à vérifier** | SELAS pluri | **reporté (ticket séparé)** |
| RAF-004 | UX neuf | Exemple de réponse à côté de chaque champ → **feature neuve transverse** (n'existe sur aucun type) | tous types | **reporté (GO PM scope/pattern)** |
| RAF-005 | parité | Bouton « Aujourd'hui » sur toutes les dates → déjà là sauf `date_cloture` (contourne le helper) | SELAS pluri | en cours (1 champ) |
| RAF-006 | parité | Clôture 1er exercice pré-remplie + modifiable → **porter le gold `31 décembre N+1`** (arbitrage : Rafael dit « +1 an glissant », défaut = gold) | SELAS pluri | en cours |
| ANO-008 | bug | DOC-008 (appel de fonds) annoncé au plan SELAS mais jamais généré (gate moteur SELARL-only) — incohérence du câblage cession | SELAS | ouvert |
| ANO-045 | à vérifier | DOC-045 (attestation capital SELAS) : orphelin (aucun bundle) selon un agent, livré selon Robin → à recouper | SELAS | ouvert |

## Retours Rafael — batch 2026-06-22 (SELARL / SCM / SCI / SCI IRIS)

> Traité via le protocole `../PROTOCOLE_RETOURS_GOLD.md` (commande `/retour-gold`).
> Verbatim conservé ; scope = tous les cas similaires, pas seulement le cas d'origine.

| id | type | retour (verbatim) | surface / scope attendu | statut |
|----|------|--------|--------|--------|
| R22-01 | encodage | SELARL : « ne pas oublier les accents "composés d'une pièce" » | texte libre rendu verbatim (descriptif du local, cession) | **traité** (descriptif prefill accentué « composés d'une pièce principale de 80 m² ») . **Accent sur données structurées (nationalité, situation) = NON décidé seul → à faire VALIDER par Rafael avant tout (Gad 2026-06-22 : aucune initiative, on n'invente rien).** |
| R22-02 | logique-conditionnelle | SELARL : ne pas mentionner de prétendue épouse quand le client n'est PAS marié sous communauté ; ex. `acte_cession_parts_scm` supprimer « divorcé avec Madame Claire Dupont » (personne jamais mentionnée) | clause conjoint/situation maritale → **TOUS** les docs qui affichent un conjoint | **traité** (helper partagé `mentions_conjoint` ; gardé sur les 2 actes de cession SCM+SPFPL ; statuts SAS = marié-only par design ; statuts SPFPL gardé sur présence conjoint ; +2 tests) |
| R22-03 | doc-manquant | SCM : « il manque le document Contrat frais communs — il n'est pas généré » + « je ne vois pas de champs correspondants » | DOC-027 + champs inter-SEL **visibles** (mon opt-in décoché = mauvais cap) | **traité** `c2d3498` (visible + actif par défaut, 504 verts) |
| R22-04 | doc-manquant | SCM : « il manque le document règlement intérieur de la scté civile de moyens — il n'est pas généré » + pas de champs | DOC-028 + champs inter-SEL visibles | **traité** `c2d3498` |
| R22-05 | champ-manquant | SCI : « inclure l'option IS et donc le document lettre option IS correspondant » | option IS SCI (déjà câblée `OPTION_IS_STRUCTURES`) → activée au bouton de test SCI + SCI IRIS | **traité** (prefill option IS, lettre DOC-022 démontrée) |
| R22-06 | mise-en-forme | SCI IRIS : « statuts : respecter la mise en forme du texte du document source » → Rafael précise : **« toute la première page »** | moteur de rendu civil PARTAGÉ (SCI/SCI IRIS/SCS/SCM) | **traité** : le moteur préserve désormais l'alignement + gras + souligné de la SOURCE sur l'en-tête/comparution (en-tête centré, « LES SOUSSIGNES » gras+souligné, identité comparant en gras) au lieu d'aplatir en justifié. +1 test fidélité. Profite aux 4 types civils |
| R22-07 | wording | SCI IRIS : remplacer la variable `[centre_impots]` par « Centre des Finances Publiques » (toujours le même, pas besoin de variable) | tout doc/type utilisant `[centre_impots]` (lettre DOC-022, tous types) | **traité** (figé générateur + champ retiré) |

## Retours Rafael — batch 2026-06-22b (cession)

| id | type | retour (verbatim) | surface / scope | statut |
|----|------|--------|--------|--------|
| R22b-01 | mise-en-forme | `courrier_sde_cession_scm` → « retirer tout surlignage ou couleur rouge sur le texte » | générateur courrier SDE (rouge montant + 2 surlignages jaunes ; rouge nulle part ailleurs) | **traité** : rouge + surlignages retirés, imports nettoyés, 3 tests inversés (assertent l'absence) |
| R22b-02 | doc-manquant (présumé) | « il manque le compromis de cession d'un cabinet médical dans les doc générés » | sélection cession SELARL (étape acte/compromis) | **NON-BUG vérifié** : `selected_selarl_document_codes` retourne **DOC-010** pour (compromis, medical) + test front le génère. Le compromis se génère quand **étape = compromis** ; Rafael a testé en « acte » (défaut). Cas G2 (test partiel) → expliquer, pas de fix |

## Note de méthode
RAF-002, 003, 005, 006 recoupent le **bloc A** de `AUDIT_PARITE_SELARL_2026-06-19.md` (parité déjà
identifiée par notre propre audit, pas encore portée). RAF-001 est un **vrai bug** (non couvert par le
vert unitaire → dogfood requis). RAF-004 est une **feature neuve** (placeholder/légende d'exemple).

## Antériorité (pointeurs)
- Retours Rafael antérieurs (R1–R7 parité formulaire SELAS) : voir mémoire projet + locks `docs/review/`.
- Retours Albane (lots juridiques) : tracés dans les locks `docs/review/albane_*` (canal distinct ;
  à terme, fusionner ici la partie « parité/UX » pour une checklist unique).
