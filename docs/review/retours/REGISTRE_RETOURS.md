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

## Note de méthode
RAF-002, 003, 005, 006 recoupent le **bloc A** de `AUDIT_PARITE_SELARL_2026-06-19.md` (parité déjà
identifiée par notre propre audit, pas encore portée). RAF-001 est un **vrai bug** (non couvert par le
vert unitaire → dogfood requis). RAF-004 est une **feature neuve** (placeholder/légende d'exemple).

## Antériorité (pointeurs)
- Retours Rafael antérieurs (R1–R7 parité formulaire SELAS) : voir mémoire projet + locks `docs/review/`.
- Retours Albane (lots juridiques) : tracés dans les locks `docs/review/albane_*` (canal distinct ;
  à terme, fusionner ici la partie « parité/UX » pour une checklist unique).
