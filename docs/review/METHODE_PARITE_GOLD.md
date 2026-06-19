# Méthode « Gold-anchored parity » — la SELARL fait foi

> Statut : méthode de travail ratifiée (Gad, 2026-06-19). S'applique à **tous** les types d'entreprise.
> Raison d'être : les formulaires front sont construits **par type** et ont dérivé du gold SELARL →
> bugs + écarts UX que Rafael a dû remonter alors que « normalement on a tout ce qu'il faut ».
> Cette méthode supprime la cause : on ne reconstruit plus, on **dérive du gold**.

## Principe
La **SELARL** est la référence validée (le « gold »). Aucun autre type n'est *reconstruit* : il est
**dérivé du gold par différence justifiée**. Un écart avec la SELARL n'est légitime que s'il est
**justifié** (le canon ou Albane rend le type différent). Sinon, l'écart est un **bug de parité** à
corriger en réutilisant *exactement* la structure et la manière de faire de la SELARL.

## Règle des documents partagés
Pour un document généré à la fois par la SELARL et par un autre type :
- S'il n'est **pas censé différer** → **réutiliser exactement** le même générateur + le même
  sous-formulaire (pas de réécriture parallèle). C'est déjà le cas des générateurs ; ça doit le devenir
  des sous-formulaires.
- S'il diffère → la différence doit être **tracée et justifiée** (canon/Albane), jamais implicite.

## Les trois artefacts durables
1. **Répertoire de retours** (`docs/review/retours/REGISTRE_RETOURS.md`) — chaque retour (Rafael,
   Albane) = une entrée structurée. Un retour fait une fois = **appliqué à tous les types concernés**,
   pas seulement celui où il a été remonté.
2. **Matrice de parité gold↔type** — pour chaque (document × champ × commodité) : identique au gold ? /
   écart justifié ? / à porter. C'est le worklist concret, généré par diff du gold.
3. **Ce document** (la méthode) + le workflow corrigé ci-dessous.

## Le workflow corrigé « faire / corriger un type »
1. Charger le répertoire de retours + générer la matrice de parité (diff vs gold SELARL).
2. Documents partagés non-différents → réutiliser **exactement** l'implémentation SELARL.
3. Porter chaque commodité SELARL dont l'absence n'est **pas** justifiée.
4. **Dogfood** : générer chaque conditionnel (régime communautaire, cession, apport, option IS…) dans
   l'UI réelle, pas seulement en test unitaire. Le vert unitaire ne suffit pas — les fixtures
   pré-remplissent les données et masquent les chemins « champ vide » qu'un vrai utilisateur déclenche.
5. Seulement alors : « prêt à tester ».

## Changement de comportement (Claude / Jinbe)
- Ne plus déclarer un type « prêt » sur du vert unitaire seul → **dogfooder** chaque conditionnel.
- **Diff systématique contre le gold** avant de reconstruire quoi que ce soit.
- Quand j'envoie un type à tester, **annoncer son niveau exact** (documents-complet vs parité-UX-complète) —
  jamais « prêt » implicite. (C'est ce qui a rendu les retours Rafael prévisibles.)
