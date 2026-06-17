# Message à Rafael — arbitrage des 4 sujets « hors-build » du ticket Albane lot 2

> Rafael tranche build vs Albane. Le reste (~47 corrections) part sans lui.

> **MAJ retour Rafael (2026-06-17)** :
> - **§16 (édition des modèles) → CLOS, rien à construire.** Albane parle de retoucher les
>   documents **générés**, *a posteriori, dans Word* — pas d'un éditeur intégré au logiciel.
>   Or les sorties sont déjà des .docx éditables : aucune dev. (Sur-interprétation de ma part.)
> - **§15 (export/import du formulaire) → PARQUÉ.** Item flou même pour Rafael ; on ne le
>   construit pas tant qu'Albane n'a pas exprimé un besoin concret. Pas à la roadmap pour l'instant.
> - **Restent réellement ouverts** : les **nouvelles formes** (§17 : micro-holding, SARL famille,
>   SELAS uni dentiste — modèle manquant) et les **2 questions métier** (SPFPL dentistes-only ?,
>   wording avenant locataire). Ces questions-là, elles, sont pertinentes.

---

Rafa,

Albane vient de me déposer un colis de 21 points sur le paillasson, façon grève des éboueurs : j'ai déjà sorti les sacs qui puaient vraiment (les bugs, les « euros » fantômes, les dates qui se prennent pour la date du jour), j'enchaîne le reste tout seul. Mais y a **4 trucs qui dépassent le code** — soit ça touche au scope (donc à ta pomme), soit c'est du juridique pur (donc Albane). À toi de dire « on construit » / « demande à Albane » / « on verra plus tard ». Sérieux à partir d'ici :

## 1. Nouvelles formes sociales demandées
- **Société civile micro-holding** : nouveau parcours, mais il réutilise quasi tout de la SCI (statuts + les mêmes docs que la SCI + une lettre d'option à l'IS). **Faisable vite.**
- **SARL de famille** : même esprit + lettre d'option à l'IR — **mais** c'est une SARL *commerciale*, et on n'a **aucun** générateur SARL aujourd'hui. Donc nettement plus de boulot que la micro-holding.
- **SELAS unipersonnelle** : la version **médecin** existe déjà côté moteur, juste à rebrancher au menu (je le fais, c'est gratuit). La version **dentiste**, il me **manque le modèle Word source** — si on la veut, il faut ce modèle (→ Albane).

→ **À trancher** : on ajoute micro-holding + SARL de famille ? Et on demande à Albane le modèle SELAS uni dentiste ?

## 2. Le client veut éditer les modèles lui-même (§16)
Il veut pouvoir **modifier les modèles Word, changer les variables, voire le formulaire** sans repasser par moi. Ce n'est pas un patch : ça **change la nature de l'outil** (vrai chantier produit/archi).

→ **Décision David** : on s'engage là-dessus, et à quelle priorité ?

## 3. Export / import du formulaire (§15)
Exporter un formulaire vierge → le remplir hors-outil (Word) → le réimporter → remplissage auto des champs. Utile (filet anti-bug de saisie) mais c'est du **dev dédié**.

→ **À trancher** : on le met à la roadmap ou pas ?

## 4. Deux questions purement métier (pour Albane, si tu valides)
- **SPFPL** « apport » et « cession » : ça concerne **uniquement les dentistes**, ou aussi les médecins ? (je dois libeller les parcours correctement — là c'est ambigu, et il y a déjà un « SPFPL SAS médecin » à côté).
- **Avenant au bail**, la phrase « a pour locataire ___ » : Albane a proposé soit **« le Dr [Nom] »** soit **« M./Mme [Nom] »** — laquelle elle veut ?

---

Le reste du ticket (les bugs de données, les formulaires à simplifier, la nationalité en déroulant, la valeur nominale auto-calculée, l'aération, le courrier de cession SCM…) : **je m'en occupe, j'ai besoin de personne.**
