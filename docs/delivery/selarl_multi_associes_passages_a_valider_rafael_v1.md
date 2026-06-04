# STATUTS SELARL MULTI-ASSOCIÉS — 4 passages pluriels dérivés (à valider Rafael)

> ## ⚠️ STATUT : DÉRIVÉ — NE PAS GÉNÉRER AVANT VALIDATION RAFAEL / ALBANE
> Aucun wording ci-dessous n'a été inventé. Chaque proposition est **dérivée** (a) du wording SELARL
> unipersonnel existant (médecin / chirurgien-dentiste) et (b) de la forme plurielle d'un modèle frère
> ratifié (SCP, SCS, SCI, PV SELARL plusieurs associés). Tant que Rafael (et Albane le cas échéant) n'a
> pas validé, **ces blocs ne doivent pas être branchés dans le moteur de génération**.
>
> Convention de tokens : par associé, suffixe `_associe_1 … _associe_N` ; borne `[nombre_associes]` (N).

---

## ENDROIT 1 — COMPARUTION

**En-tête (remplace « LE SOUSSIGNE : ») :** `LES SOUSSIGNES :`

**Bloc identité, RÉPÉTÉ pour chaque associé i = 1..N — variante MÉDECINS** (dérivée du modèle médecin) :
```
[civilite_associe_i] [prenom_associe_i] [nom_associe_i], [profession], né le [date_naissance_associe_i] à [ville_naissance_associe_i] ([departement_naissance_associe_i]), de nationalité [nationalite_associe_i], demeurant [adresse_personnelle_associe_i], inscrit au tableau du Conseil départemental de [ville_ordre_associe_i] sous le numéro national [numero_ordre_associe_i] et sous le numéro RPPS [numero_rpps_associe_i], [situation_maritale_associe_i].
```
**Variante CHIRURGIENS-DENTISTES** (dérivée du modèle dentiste) :
```
[civilite_associe_i] [prenom_associe_i] [nom_associe_i], [profession], né le [date_naissance_associe_i] à [ville_naissance_associe_i] ([departement_naissance_associe_i]), de nationalité [nationalite_associe_i], demeurant [adresse_personnelle_associe_i], [situation_maritale_associe_i] sous le régime de [regime_matrimonial_associe_i] avec [civilite_conjoint_associe_i] [prenom_conjoint_associe_i] [nom_conjoint_associe_i].
Inscrit au Tableau de l'ordre départemental des [profession_reglementee_pluriel] de [ordre_departemental_associe_i] sous le numéro RPPS [numero_rpps_associe_i].
```
**Phrase de clôture** (remplace « il a décidé d'instituer ») :
- MÉDECINS : `Ont établi ainsi qu'il suit les statuts de la Société d'exercice libéral à responsabilité limitée de médecins qu'ils ont décidé d'instituer entre eux :`
- DENTISTES : `Ont établi ainsi qu'il suit les statuts de la [forme_sociale_complete] de [profession_reglementee] qu'ils ont décidé d'instituer entre eux :`

**Article 1 – Forme** : dentiste = inchangé (déjà générique). Médecin : `Il est formé entre les soussignés, une [forme_sociale_complete] (SELARL), qui existera entre les propriétaires des parts ci-après créées…`

*Source : SCP (en-tête + bloc répété + clôture), SCS (« décidé d'instituer entre eux », « formé entre les soussignés »). Reste = wording unipersonnel d'origine.*

---

## ENDROIT 2 — ARTICLE 7 : APPORTS
```
ARTICLE 7 – APPORTS
Les associés effectuent les apports en numéraire suivants, qui sont intégralement libérés :
```
**Bloc RÉPÉTÉ par associé i** — MÉDECINS : `Dr [prenom_associe_i] [nom_associe_i] apporte à la Société la somme de [apport_lettres_associe_i] euros, ci  [apport_associe_i] €` · DENTISTES : `[civilite_associe_i] [prenom_associe_i] [nom_associe_i] apporte à la Société la somme de [apport_lettres_associe_i], ci  [apport_associe_i]`
**Total + dépôt :**
```
Total des apports en numéraire :  [capital_social] euros
Ces sommes ont été intégralement déposées par les associés conformément à la loi, au crédit d'un compte ouvert au nom de la société en formation dans les livres de la banque [nom_banque] [adresse_banque].
```
*Source : SCP Art. 6.1 + SCI Art. 6 (énumération + Total) ; libellé Total du dentiste. « par les associés » dérivé du « par l'associé unique » dentiste.*

---

## ENDROIT 3 — ARTICLE 8 : CAPITAL & RÉPARTITION
```
ARTICLE 8 – CAPITAL SOCIAL
Le capital social est fixé à la somme de [capital_lettres] euros ([capital_social] €).
Il est divisé en [nb_parts_total] parts de [valeur_nominale_part] euro chacune, entièrement souscrites et libérées dans les conditions exposées ci-dessus et attribuées aux associés de la manière suivante :
```
**Bloc RÉPÉTÉ par associé i** (forme PV SELARL plusieurs associés) :
```
-  le Docteur [prenom_associe_i] [nom_associe_i], titulaire de [nb_parts_lettres_associe_i] parts sociales, numérotées de [numero_part_debut_associe_i] à [numero_part_fin_associe_i],  [nb_parts_associe_i] parts
```
**Total :** `Total du nombre de parts composant le capital social :  [nb_parts_total] parts`

*Source : PV SELARL plusieurs associés (« titulaire de N parts, numérotées de … »), SCP (plages), ligne Total du dentiste. Supprime « associée unique ».*

---

## ENDROIT 4 — SIGNATURES
```
Fait à [lieu_signature], le [date_signature]
En [nombre_exemplaires_lettres] exemplaires
```
**Bloc signataire RÉPÉTÉ par associé i :** `[prenom_associe_i] [nom_associe_i]` + `(Faire précéder de la mention « Lu et approuvé »)`

*Source : SCP + SCS (empilement « Lu et approuvé » par signataire), ligne « exemplaires » du médecin.*

---

# ❓ QUESTIONS DE VALIDATION — À TRANSMETTRE À RAFAEL

**Comparution** — 1. Clôture « décidé d'instituer entre eux » (fidèle SELARL) ou « convenu de constituer entre eux » (SCP) ? · 2. Médecin Art.1 « formé entre les soussignés » ou « formé par les soussignés » ? · 3. Régime matrimonial/conjoint (dentiste) : obligatoire par associé ou conditionnel (célibataire / sans communauté) ? · 4. Désignation du gérant : traitée ailleurs, rien à ajouter en comparution — confirmer.

**Apports (art.7)** — 5. Ligne Total : « Total des apports en numéraire : » (dentiste) ou « SOIT AU TOTAL » (SCP/SCI) ? · 6. Somme des apports par associé = capital social (100 % numéraire) ? · 7. Préfixe « Dr » systématique (médecin) ou `[civilite_associe_i]` (dentiste) ? · 8. **Apports en nature/industrie** : à prévoir ? (NON couvert par les sources — non dérivable sans wording) · 9. Dépôt « par les associés » en bloc, ou nominatif par associé ?

**Capital & répartition (art.8)** — 10. **Numérotation des parts** « numérotées de X à Y » (PV SELARL/SCP) ou sans numéros (comme l'unipersonnel actuel) ? · 11. « le Docteur [nom] » ou « [civilite] [nom] » dans la liste ? · 12. **Associé personne morale (SPFPL) admis dès la constitution ?** Si oui, ajouter un bloc identité personne morale (dérivable du PV/SCS). · 13. Libellé Total parts : dentiste ou SCP ? · 14. Concordance parts/plages contiguës — confirmer le principe.

**Signatures** — 15. Garder « En N exemplaires » (médecin) ou exemplaire numérique unique (dentiste) ? — par modèle. · 16. Unifier les tokens signataire sur `[prenom_associe_i]/[nom_associe_i]` ? · 17. Ordre des signatures = ordre comparution/répartition ? · 18. Signature personne morale (représentant légal) — seulement si Q12 = oui.

**Transverse (important)** — Clause d'**agrément multi-associés** (cession de parts entre associés / à des tiers) : **aucun wording d'agrément multi n'a été dérivé** (les extraits ne le couvraient pas). Si Rafael veut une clause d'agrément adaptée au multi, fournir le wording d'agrément SELARL + la forme plurielle frère. **Signalé, non inventé.**

---

*Sources verbatim : médecin (statuts SELARL médecins) ; dentiste (statuts SELARL chirurgien dentiste) ; SCP (`Modèle Statuts SCP`) ; SCS (`Statuts_SCS_modele`) ; SCI (`Modèle statuts SCI`) ; PV SELARL plusieurs associés (`lot_05`). Généré 2026-06-04, chemin B (dérivation + validation humaine).*
