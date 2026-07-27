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

## RÈGLES IMPOSÉES — le « code du bâtiment » (à étudier/questionner, défaut = appliquer)
Issues de la remise en question 2026-06-19. Toute exception doit être **justifiée et tracée**.

1. **Le gold fait foi : on dérive, on ne reconstruit pas.** Tout type dérive de la SELARL. Un écart
   non justifié = un bug de parité. On ne réécrit jamais un helper qui existe au gold — on le consomme.
2. **Couche partagée obligatoire.** Toute commodité de rendu (date, capital, adresse, mandataire…) vit
   dans `front_widgets.py`, jamais dupliquée par type. Envie de re-coder un helper = signal qu'il doit
   être partagé.
3. **Le vert unitaire ne suffit pas → dogfood obligatoire.** Avant « prêt », générer chaque conditionnel
   (régime, cession, apport…) dans l'UI réelle. Les fixtures pré-remplissent les champs et masquent les
   chemins « champ vide » (c'est ce qui a laissé passer le bug régime).
4. **Annoncer le niveau exact.** Jamais « c'est bon » flou. Toujours : documents-complet / parité-UX-
   complète / partiel (manque X, Y). Un « prêt » implicite fabrique des retours prévisibles.
5. **Matrice avant retours.** Avant de faire tester, diff le type contre le gold (la matrice) et fermer
   TOUS les trous connus → les retours du testeur sont du NEUF, pas du déjà-su.
6. **Un retour fait une fois = appliqué partout.** Le registre des retours : un retour sur un type
   devient une vérification sur tous les types concernés (pas seulement celui où il a été remonté).
7. **Ne pas inventer le métier.** Un écart qui touche le juridique (wording, 2e lieu d'une holding…)
   → question Albane, jamais deviné. Défaut documenté en attendant.
