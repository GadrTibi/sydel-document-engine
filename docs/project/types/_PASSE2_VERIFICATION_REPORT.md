# PASSE 2 — Rapport de vérification de fidélité (re-vérification totale)

> Daté **2026-06-08**. Dépôt vérifié : `C:/Users/Gad/Desktop/Sydel/sydel-document-engine-claude`.
> `PYTHONPATH=…/sydel-document-engine-claude/src` (clone `-claude` confirmé via `sydel_doc_engine.__file__`
> pour chaque type). **Tâche LECTURE SEULE** : aucun fichier source / canon / git modifié ; seuls des
> artefacts d'audit jetables sous `artifacts/_audit_tmp/`. Ce rapport est le seul fichier écrit.
>
> Méthode commune (2 contrôles indépendants par type) : (1) diff paragraphe-par-paragraphe du DOCX
> généré vs modèle source tokenisé après substitution des placeholders (python-docx, normalisation
> espaces/nbsp), détection wording inventé / clause manquante / placeholder résiduel / duplication /
> désaccentuation ; (2) contrôle vocabulaire+blocs (forme correcte parts/gérant vs actions/Président,
> présence comparution / apports / capital / répartition / signatures / annexe). Accents lus en **UTF-8
> réel** via python-docx (la console cp1252 affiche du mojibake — ignoré).

---

## 1. Suite de tests complète (dernière exécution PASSE 2)

```
cd C:/Users/Gad/Desktop/Sydel/sydel-document-engine-claude
PYTHONPATH=…/src python -m pytest tests/ -q --basetemp=…/artifacts/_audit_tmp/pt_passe2_final
→ 356 passed in 32.14s
```

**356 passed / 0 failed.** Suite globale verte. (Les échecs ponctuels observés par les vérificateurs
par type étaient des artefacts Windows : `PermissionError`/`ZipBundleError` en teardown ou sur basetemp
custom long-path — disparus en run global avec basetemp dédié. Aucun échec réel lié à la fidélité.)

---

## 2. Tableau par type

| Type | Fidèle | Wording inventé | Divergences principales | Tests (périmètre) |
| :--- | :--- | :--- | :--- | :--- |
| **SELARL médecin** | **OUI** | Aucun | Aucune de fond. Région articles **byte-identique** au source après substitution (311/311 paras). Désaccentuation `médecin`/`française` = donnée de **fixture de test**, pas le moteur (le source porte `[profession]`/`[nationalite]`). | `-k selarl` : 43 passed. Inclut le test ligne-par-ligne `test_statuts_selarl_medecin_matches_source_docx_line_by_line`. |
| **SELARL dentiste** | **OUI** | 1 normalisation : mot `euros` ajouté à l'en-tête capital (absent du source dentiste, présent `€` chez le médecin). Aucune clause juridique fabriquée. | 258 blocs vs 258 paras source (1:1). 7 divergences toutes **délibérées** (paramétrisations + décision Rafael `99 ans` figée). 1 écart structurel : **relocalisation** clause matrimoniale (identité → ligne ordre/RPPS), contenu mot-pour-mot identique. | `-k selarl_dentiste` : 3 passed ; lot_04 : 18 passed. **Pas** de test ligne-par-ligne (≠ médecin). |
| **SELAS mono** | **PARTIEL** | Aucun | **Défaut de rendu réel** sur la ligne d'identité associé : `de la la communauté légale` (double article) + `du Ordre` (élision manquante). Cause : connecteurs codés en dur en collision avec les helpers. Conjoint sans prénom (`Madame Martin`) = fidèle au source. Δ 255 vs 256 paras = 2e lieu d'exercice optionnel omis (légitime). | `-k selas` : 18 passed. **Aucun test ne couvre ces 2 fautes de rendu.** Pas de test ligne-par-ligne. |
| **SELAS multi** | **OUI** | Aucun | 259 paras source ↔ 259 générés (0 clause perdue, 0 duplication). Token-mapping mineur : profession en comparution rend `associe.profession` (`Docteur`) au lieu de `[profession_reglementee]` (`médecin`) du source — donnée de contexte, squelette préservé. Boilerplate `parts/gérant` + `DIRIgerantS` = **défauts du DOCX source** recopiés fidèlement. | `-k selas_multi` : 4 passed ; sélecteur élargi : 18 passed. |
| **SPFPL cession** | **OUI** | Aucun | Transcription fidèle (369 blocs). Diff squelette bidirectionnel 0/0. Vocabulaire actions+Président conforme (actions 94=94, gérant 0/0). Unique `parts sociales` = clause légale verbatim source (Art. 9-III). Duplication unique = présente 2× dans le source (Art. 19/19-1). | `-k spfpl` : 3 passed (cession+apport+blocage). |
| **SPFPL apport** | **PARTIEL** | Aucun | **2 bannières de partition omises** (titres organisationnels `FORME-OBJET-…` et `ADMINISTRATION-…`, sévérité faible, aucune clause de droit perdue : 6/8 bannières rendues). **1 déviation délibérée** : Art. 6 substitue le siège de la société cible (SELARL) au lieu de `[adresse_siege]` SPFPL du source — juridiquement plus correct, à confirmer métier. `gérant`/`parts sociales` résiduels = fidèles au source. | `-k spfpl` : 31 passed ; sous-ensemble apport : 6 passed. Ratio similarité difflib 0.9947. |
| **SCM** | **OUI** | Aucun | Vocabulaire SCM correct (parts+gérant, société civile de moyens). Divergences = 2 drops cosmétiques (points de conduite, wrapper « Faire précéder de la mention ») + 3 **correctifs de défauts source** (montant fantôme `510 €`, placeholder de parts mal câblé, date vide) + 1 adaptation genre légitime + 1 artefact source reproduit (`1200euros` sans espace). | `-k scm` : 37 passed. |
| **SCI standard** | **PARTIEL** | Aucun | **Désaccentuation** du wording **statique** injecté par le moteur dans le bloc comparution (`Ne le`/` a `/`De nationalite` vs source `Né le`/`à`/`De nationalité`). TAB→espace sur les totaux. **Fuite d'un marqueur éditorial source** `A RETIRER SI LA SOCIETE EST A L'IR` dans la sortie client. Corps clausier (37 articles) fidèle, accents intacts. Ancien wording SCS croisé = **confirmé absent** (corrigé avant cette passe). | `-k sci` : 15 passed. Les tests ne couvrent **pas** les accents. |
| **SCI IRIS** | **PARTIEL** | **2 cas** : (a) bloc identité **personne morale** (`ayant son siège … immatriculée au RCS … sous le numéro …` / `Représentée par … gérant`) — squelette **absent du modèle source tokenisé**, généré en dur par `_add_morale_identity`/`_signature_label` ; fonctionnellement requis (source attend `[denomination_societe_2]`) mais wording non présent dans la source de vérification → à valider sur le `.docx` original. (b) libellé tableau `Parts 1 à 40` au lieu de `Parts numérotées de [debut] à [fin]` (mot `numérotées` supprimé). | **Désaccentuation qui CONTREDIT la fix-spec `_CIVILS_FIX_SPEC_V1.md` (2026-06-07)** : `Numerotees de 1 a 40`, `Nee le … a Paris`, `De nationalite francaise` — la SCI IRIS n'a pas reçu le traitement accents appliqué à SCI/SCS. **Duplication** de la date de signature (`A Paris, le …` ×2 : chemin source 626 + réinjection). En-tête tableau `Quote-part de résultat` vs source `du résultat`. TAB→espace. | `-k sci` : 15 passed. Les tests ne couvrent **pas** accents ni duplication date. |
| **SCS** | **PARTIEL** | Aucun | **Désaccentuation** mention signature `Lu et approuve` (vs source `Lu et approuvé`) + perte guillemets/parenthétique. **Reformatage** du bloc comparution : identité normalisée multi-associés au lieu de la prose source `marié avec / épouse` du couple (mini-désaccentuations moteur `Ne le`/`De nationalite`/`Demeurant`). Corps clausier accentué fidèle. Vocabulaire SCS correct (commandité/commanditaire, parts+gérant). | `-k scs` : 3 passed. |
| **SAS** | **PARTIEL** | Aucun | Au plan textuel **fidèle** (220/221 paras, 0 wording inventé, vocabulaire actions+Président conforme). **Réserve métier héritée** : Art. 4 contient `parts sociales` + `gérant seul` (forme parts/gérant) dans un acte SAS — **défaut du DOCX source** propagé fidèlement (src=1/gen=1), pas une invention. Réserve de forme : tabulations + découpage ANNEXE non reproduits à l'identique. | `-k sas` : 20 passed. |

---

## 3. Liste consolidée des points à arbitrer (métier — Rafael / Albane)

> Aucun de ces points n'est tranchable côté technique seul (règle 20 : ne pas inventer de règle
> produit). Plusieurs recoupent les points déjà ouverts dans `_RAFAEL_PACKET_V1.md`.

### A. Défauts hérités du DOCX SOURCE (le moteur est fidèle, c'est le modèle qui est en cause)
1. **Résidu SELARL/parts dans SAS Art. 4** — `parts sociales` + `gérant seul` dans un acte SAS (forme
   en actions+Président). Corriger le **modèle source** (`STATUTS_SAS_SPFPL_medecins_modele.docx`) ou
   confirmer que c'est voulu ? *(sévérité moyenne-haute — sortie client juridiquement incohérente)*
2. **Résidu parts/gérant dans SELAS multi** — `parts sociales`/`gérant` (Art. 4, 23) + casse OCR
   `DIRIgerantS` (titre Art. 17, = `DIRIGEANTS` déformé) dans `Statuts_SELAS_multi_modele.docx`.
   Corriger la source.
3. **Marqueur éditorial SCI** — `A RETIRER SI LA SOCIETE EST A L'IR` (fin Art. 31 du modèle SCI) fuit
   dans le document client. Retirer ou conditionner ? *(instruction interne non destinée au client)*
4. **Artefacts de mise en forme source** — `1200euros` sans espace (SCM page de garde) ; en-tête
   capital dentiste sans `euros`/`€`. Le moteur reproduit / normalise. À nettoyer côté modèles si gênant.

### B. Décisions produit / vocabulaire (recoupent `_RAFAEL_PACKET_V1.md`)
5. **Genre masculin / mixte SELAS** — SELAS mono rend `de la la communauté` / `du Ordre` (défaut de
   rendu, voir §4) ; au-delà du correctif technique, **harmonisation genre/accord** à confirmer pour la
   famille SELAS (mono vs multi). Lié au scope SELAS multi 2-5 + personne morale + DG du paquet Rafael.
6. **DG nominatif (SELAS multi)** — token-mapping profession en comparution : afficher la
   `profession_reglementee` **commune** (`médecin`, fidèle au source) ou la **profession individuelle**
   de chaque associé (`Docteur`, choix actuel, arguablement plus correct multi-professions) ?
7. **Vocabulaire cession / apport SPFPL** — déjà ouvert au paquet (« PV nommés cession au wording
   apport »). Plus, sur **SPFPL apport** : le **swap de siège** Art. 6 (siège société cible SELARL au
   lieu du siège SPFPL `[adresse_siege]` du source) — juridiquement défendable, à confirmer plutôt que
   trancher seul.
8. **PM en SCI standard** — déjà ouvert au paquet (NotebookLM autorise la personne morale en SCI, le
   moteur bloque par prudence via `_validate_sci`). Le code d'identité morale partagé existe mais n'est
   pas déclenché en SCI simple. **Confirmer pour débloquer** + valider le wording d'identité morale.
9. **Wording identité morale (SCI IRIS)** — le squelette `ayant son siège … immatriculée au RCS …
   sous le numéro … / Représentée par … gérant` **n'existe pas** dans le modèle source tokenisé. À
   valider sur le `.docx` original / NotebookLM **avant de figer** (lié au point 8).
10. **Relocalisation clause matrimoniale (SELARL dentiste)** — déplacée de la ligne identité vers la
    ligne ordre/RPPS (contenu identique, paragraphe d'accueil différent du choix médecin). Acceptable
    ou exiger la fidélité paragraphe-par-paragraphe stricte du médecin ?

---

## 4. Dette technique pure (corrigeable sans arbitrage métier — hors scope de cette passe lecture seule)

> Ces points ne sont **pas** des questions métier : ce sont des correctifs déterministes à planifier
> sur branche dédiée. Listés ici pour ne pas les perdre.

- **SELAS mono — défaut de rendu (priorité haute)** : `de la la communauté légale` + `du Ordre` sur la
  ligne d'identité **nominative** de l'associé. Correctif : aligner le SELAS mono sur le token composite
  `[situation_matrimoniale_statuts]` déjà utilisé par les blocs SELARL (qui rend la clause complète sans
  collision) + gérer l'élision `de l'Ordre`. **Non couvert par les tests** → ajouter une assertion.
- **SCI IRIS — désaccentuation contredisant `_CIVILS_FIX_SPEC_V1.md`** : la fix-spec (2026-06-07) a
  réaccentué SCI/SCS mais **pas** SCI IRIS. Réaccentuer `_add_physical_identity`, branche IRIS de
  `_add_capital_block`, `_add_resultat_groupes_block` (`Numérotées`/`Née`/`nationalité`/`à`).
- **SCI IRIS — duplication date de signature** : `signature_slice=(629,636)` ne couvre pas la ligne
  date source (para 626) → double rendu. Corriger le slice pour englober la ligne date.
- **SCI standard / SCS — désaccentuation des chaînes statiques en dur** du bloc comparution
  (`Ne le`/` a `/`De nationalite`/`Demeurant`) + `Lu et approuve` (SCS). Réaccentuer.
- **TAB→espace** sur les totaux (SCI, SCI IRIS) et tabulations d'alignement (SAS) non reproduites.
- **Gouvernance fidélité** : seul **SELARL médecin** possède un test de comparaison **ligne-par-ligne**
  au source (`test_statuts_selarl_medecin_matches_source_docx_line_by_line`). Les autres types
  (dentiste, SELAS mono/multi, SCI/IRIS, SCS, SAS, SPFPL) n'ont que des assertions ciblées → la fidélité
  **n'est pas verrouillée par la CI**. Recommandation : généraliser un test ligne-par-ligne par type.

---

## 5. VERDICT GLOBAL (honnête)

**Suite complète : 356/356 verte.** Aucun échec réel. Les défauts ci-dessous sont **fonctionnels /
cosmétiques** et, pour la plupart, **non couverts par les tests existants** — la CI verte ne les attrape
donc pas.

**Bilan par type : 5 FIDÈLES, 5 PARTIELS, 0 NON-fidèle.**

### Fidèle et livrable techniquement (5)
- **SELARL médecin** — fidélité byte-identique, verrouillée par un test ligne-par-ligne. Référence du moteur.
- **SELARL dentiste** — quasi-parfait (1:1), seules divergences délibérées + 1 normalisation `euros` défendable.
- **SELAS multi** — 259=259, 0 clause perdue ; les résidus parts/gérant sont des défauts **source**, pas moteur.
- **SPFPL cession** — transcription fidèle, vocabulaire actions+Président propre.
- **SCM** — fidèle, divergences = correctifs de défauts source + cosmétique.

> Sur ces 5, **aucun wording juridique inventé, aucun placeholder résiduel, aucune clause manquante**.
> Le moteur est un assembleur déterministe de blocs + substitution ; il ne forge pas de texte.

### Fidèles SOUS RÉSERVE (5 PARTIELS — répartition de la cause)
- **Cause métier / source (ne bloque pas le moteur, à arbitrer)** :
  - **SAS** — fidèle au texte ; la seule réserve est le résidu parts/gérant **du modèle source** (Art. 4).
  - **SPFPL apport** — fidélité 0.9947 ; 2 bannières omises (sévérité faible) + 1 déviation siège à confirmer.
- **Cause dette technique pure (corrigeable sans métier)** :
  - **SELAS mono** — défaut de rendu réel `la la` / `du Ordre` sur une ligne **nominative** → sévérité
    moyenne-haute en sortie client. **Le seul PARTIEL avec un défaut visible immédiat.** Correctif évident.
  - **SCI IRIS** — désaccentuation contredisant la fix-spec + duplication date + 1 wording identité
    morale **à valider métier**. Le plus chargé en dette.
  - **SCI standard / SCS** — désaccentuation de chaînes statiques + fuite marqueur `A RETIRER` (SCI).

### Ligne de fond
- **Techniquement livrable en l'état** : les 5 fidèles + (SAS, SPFPL apport) une fois leurs réserves
  **métier** confirmées (le moteur n'a rien à corriger sur ces deux-là, c'est la source / une décision).
- **À corriger avant livraison client** : **SELAS mono** (défaut de rendu nominatif) et **SCI IRIS**
  (désaccentuation + duplication date) — dette **technique** déterministe, pas un blocage métier.
- **Cosmétique / à planifier** : réaccentuation SCI/SCS, TAB→espace, fuite marqueur éditorial SCI,
  généralisation des tests ligne-par-ligne.
- **Aucun type n'invente de droit** : tous les écarts sont soit des paramétrisations délibérées, soit
  des défauts hérités du DOCX source recopiés fidèlement, soit de la dette d'accent/mise en forme dans
  les blocs réinjectés en dur. **Zéro placeholder résiduel sur les 10 types.**
