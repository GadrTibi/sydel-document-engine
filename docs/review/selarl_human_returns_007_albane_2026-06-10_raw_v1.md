# Retours humains 007 — Albane LALLEMAND (SYDEL, Direction Juridique) — 2026-06-10

> **Source canonique de ce lot.** Mail d'Albane du **10 juin 2026 18:28**, reçu EN DIRECT (Gad,
> 2026-06-11 : Rafael sorti du circuit par défaut — cf. mémoire `feedback-albane-direct-source`).
> Brut + pièces jointes dans `docs/review/albane_returns_2026-06-10/` (`.eml`, 2 modèles Word, 7 captures).
>
> ⚠️ **Rafael n'avait transcrit que la SECTION 1** (questionnaire + cession) → c'est le « ticket 35
> critères » déjà livré (commit `b781da3`/`e5f695c`). **La SECTION 2 « Sur les documents générés »,
> la demande de sauvegarde de dossier et les 2 modèles Word joints étaient PERDUS.** Ce lock rétablit
> l'intégralité du retour.

Cas testé : **SELARL dentiste unipersonnelle**, testé sur un homme (la sœur — cas femme — sera testée
au 2e contrôle après modifs).

---

## SECTION 1 — Questionnaire + cession  ✅ DÉJÀ LIVRÉ (lot 35 critères)
(Verbatim conservé dans le `.eml`. Correspond aux décisions SELARL-SAL-2, -MAT-1, -CESS-2/3, -LOC-1,
-OPT-1, -UI-1, -SCM-2, -AVB-1, -PRET-1 du journal.)

**Point résiduel de la section 1, NON couvert par le ticket Rafael :**
- **Sauvegarde / reprise de dossier** : « *ai-je un moyen de tout enregistrer (avec ma réf dossier) pour
  ne pas avoir à tout retaper ?* » → Albane bloquée a dû tout ressaisir. (Les blocages eux-mêmes —
  adresse banque, salariés — sont déjà corrigés.) **HORS lettre de mission → PARQUÉ au Manifeste**
  (Gad 2026-06-11) : Gad en discute avec son **associé Rafael** pour décider si on le construit quand
  même pour le client (SYDEL). Pas construit pour l'instant.

---

## SECTION 2 — « Sur les documents générés »  🆕 NON COUVERT PAR RAFAEL
(Albane a décoché la cession pour pouvoir générer ; retours sur les autres documents.)

### Statuts
1. Intitulé du doc = « **Statuts {dénomination}** » (mettre le nom d'office).
2. **Mise en page d'origine** : centrer l'entête, réduire sa taille, retirer les interlignes, cadre de
   statuts plus grand, espaces entre « le soussigné » et l'art. 1 ; **majuscule à « Société »** (2e ligne entête).
3. Page 1 : « marié avec Mme… » doit être **juste après l'adresse du domicile** (à la suite de la phrase du haut).
4. Page 1 : le **numéro d'inscription à l'ordre** est absent (le RPPS y est) → l'ajouter, **seulement si le champ du formulaire est rempli**.
5. Article 3 : **nom de la société en gras et centré**.
6. Article 7 : après « 1.000 » ajouter « **euros** » (en chiffres ET en lettres) ; idem article 8 « fixé à la somme de mille » → « euros ». [capture_3]
7. Avant-dernière page : « **fait à** » à gauche + nom du client en gras.
8. Dernière page : centrer la ligne « liste des actes accomplis… ».

### PV de nomination de gérant
9. Mise en forme entête : nom en gras, centré, **police 9**, pas d'interligne, espaces pour aérer.
10. ⚠️ **Le PV généré est un modèle MULTI-associés, pas associé unique.** Albane joint le **modèle
    associé unique simplifié** (`MODELE_PV_associe_unique_nomination_gerant.docx`) : « les associés » →
    « l'associé », « l'assemblée générale » → « l'associé unique », pas de texte sur les associés présents.
11. Ordre du jour en **tirets** (liste) pour ajouter une résolution facilement.

### Autorisation de domiciliation
12. Police **Roboto 10**, titre **11**. Le reste OK.

### Déclaration de non-condamnation
13. Espaces dans le cadre du haut (un avant le texte, un après).
14. « né à » : **enlever le point après la ville** + mettre le **département entre parenthèses**.
15. Retirer les interlignes (« je soussigné … de nationalité » ; entre les noms des parents), aérer, et
    placer le **rappel en italique en bas de page**.

### Demande d'inscription à l'ordre
16. En haut à gauche : **CP et ville en dessous** (pas sur la même ligne). [capture associée]
17. Nom de l'ordre **aligné**.
18. Aérer (espaces avant « objet », autour de « M. le Président », avant « Je vous prie d'agréer »).
19. Pouvoirs donnés à « M. Jordan ELBAZ » → **mettre le nom du conseiller** (→ **variable à ajouter**).
20. « Monsieur le Président » → « **Madame la Présidente** » si le président de l'ordre est une femme
    (vérifié à chaque fois) → **variable / case à cocher à ajouter**.

### Procuration
21. Aérer (espaces dans le cadre, comme le modèle).
22. ⚠️ **Modèle mis à jour (avril)** : sous l'adresse SYDEL, ajouter **RCS PARIS 788 531 432** (SIREN)
    + **téléphone 0153814303**. Modèle joint : `MODELE_Procuration_maj_SIREN_tel.docx`.

---

## Contexte fil antérieur (extrait utile, mai–juin 2026)
- Personne morale associée d'une SEL = **SELAS médecins uniquement**, associé = **société civile « micro
  holding »** (PAS une SPFPL). Modèle « micro holding » fourni par Albane (dans le fil).
- **Courriers de fin de création** (formalités après immatriculation) : à intégrer ; pas de nouvelles
  variables pour destinataires (champs libres) — juste nom/prénom client, nom SEL, siège, SIREN. Deux
  versions : « 1ère installation » (sans cession de fonds) et « normale » (tous autres cas).
- SELARL multi-associés = **abandonné** ; SELAS = N associés médecins.
- Siège social **identique au lieu d'exercice** = quasi systématique (case à cocher proposée par Albane).

---

## Mapping done / new (résumé)
- **Section 1** = ✅ livré (35 critères).
- **Section 2** = 🆕 22 points, aucun couvert. Majorité = **mise en page (FORME)** + 2 **modèles à
  remplacer** (PV uniperso, procuration MAJ) + qq **contenu/variables** (euros art 7/8, n° ordre dans
  statuts, titre « Statuts {dénom} », variable conseiller, case « Présidente »).
- **Save/reprise dossier** = ❓ décision Gad (nouvelle capacité, persistance).
