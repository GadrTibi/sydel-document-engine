# SELAS multi — Cartographie de tokenisation (modèle « Reynaud »)

Date : 2026-06-07
Phase : tokenisation du modèle source (PAS de génération — le générateur SELAS multi sera bâti dans une phase ultérieure sur cette base).

## Fichiers

- **Source réelle (NE PAS committer brut)** : `C:/Users/Gad/Downloads/Statuts SELAS DU DR ISABELLE REYNAUD.docx` (541 paragraphes, 38 articles, 1 table décorative « STATUTS »).
- **Modèle neutralisé/tokenisé produit** : `project/source_documents/lot_04/Statuts_SELAS_multi_modele.docx` (541 paragraphes, 38 articles — structure identique au source ; aucune donnée réelle).
- **Script de tokenisation (artefact, non canonique)** : `artifacts/_reynaud_tokenize.py`.

## Caractéristiques structurantes de ce modèle (vs SELAS mono `Statuts_SELAS_medecin.docx`)

1. **Comparution MULTI** — en-tête « LES SOUSSIGNEES » avec **deux comparants** :
   - une **personne physique exerçante** (associée professionnelle) ;
   - une **personne morale associée non exerçante** (ici une Société Civile à capital variable).
2. **Article 15 — DIRECTEURS GENERAUX** présent (sous-sections 15-1 à 15-5), **générique** : le source ne nomme aucun DG concret (seul un Président est désigné). Aucune donnée réelle DG à tokeniser → voir « Divergences ».
3. **Capital en actions** avec **répartition entre deux associés** (table de répartition en paragraphes tabulés, pas en table Word) + ligne « Total des actions ».
4. **Président personne physique** désigné (Article 14).

## Index des blocs (index de paragraphe = 0-based, tel que python-docx)

| Bloc | Paras (0-based) | Contenu |
|---|---|---|
| En-tête société | 2–5 | Dénomination, forme (profession), capital, siège |
| Table déco « STATUTS » | (table 0) | Décorative, pas de données |
| **Comparution multi « LES SOUSSIGNEES »** | **14–19** | 14 = libellé ; **16–17 = personne physique 1** (état civil + ordre/RPPS) ; **19 = personne morale associée** |
| Art. 1 Forme | 22–30 | Profession tokenisée (para 24 boilerplate inchangé) |
| Art. 2 Objet | 33–39 | Profession tokenisée (35, 37) |
| Art. 3 Dénomination | 42–48 | 46 = dénomination ; 48 = mention légale (profession ×2) |
| Art. 4 Siège | 51–55 | 53 = adresse siège |
| Art. 5 Lieu d'exercice | 58–60 | 60 = adresse lieu d'exercice |
| Art. 6 Durée | 62–66 | Boilerplate (99 ans) inchangé |
| **Art. 7 Apports** | 68–80 | **72 = apport personne 1** ; **73 = apport personne morale** ; 75 = total ; 78 = banque |
| **Art. 8 Capital social + répartition** | 82–99 | 84 = capital lettres/chiffres ; 86 = nb actions / valeur nominale ; **88–89 = part personne 1** ; **92–93 = part personne morale** ; 95 = total actions |
| Art. 9 Qualité d'associé | 101–140 | 103 = profession pluriel ; reste boilerplate |
| Art. 10 Forme des actions | 142–149 | Boilerplate |
| Art. 11 Transmission des actions | 151–177 | Boilerplate |
| Art. 12 Droits/obligations | 179–187 | Boilerplate |
| Art. 13 Exclusion | 189–205 | Boilerplate |
| **Art. 14 Présidence** | 207–245 | 14-1 à 14-4 ; **221 = président (personne 1)** ; **222 = domicile président** ; 224 = « est nommée présidente » (gendré, inchangé) |
| **Art. 15 Directeurs Généraux** | 247–296 | **15-1 à 15-5, entièrement générique** (aucune donnée réelle) |
| Art. 16 Décisions sociales | 298–322 | Boilerplate |
| Art. 17 Conventions | 323–328 | Boilerplate |
| Art. 18 Responsabilité associé | 329–332 | Boilerplate |
| Art. 19 Non-concurrence | 334–337 | Boilerplate (durée 2 ans / rayon 2 km — voir Divergences) |
| Art. 20 Cessation d'activité | 338–351 | Boilerplate |
| Art. 21 Commissaires aux comptes | 352–369 | Boilerplate |
| Art. 22 Variation du capital | 370–375 | Boilerplate |
| Art. 23 Placement hors convention | 376–383 | Boilerplate |
| **Art. 24 Exercice social** | 385–390 | **389 = premier exercice clos (date)** |
| Art. 25 Comptes annuels | 392–395 | Boilerplate |
| Art. 26 Affectation résultats | 397–404 | Boilerplate |
| Art. 27 Capitaux propres | 406–415 | Boilerplate |
| Art. 28 Déontologie médicale | 417–425 | Boilerplate |
| Art. 29 Dissolution | 427–434 | Boilerplate |
| Art. 30 Liquidation | 436–441 | Boilerplate |
| Art. 31 Sanctions disciplinaires | 443–450 | Boilerplate |
| Art. 32 Communication au Conseil départemental | 452–473 | Boilerplate |
| Art. 33 Reprise des actes | 475–480 | Boilerplate |
| Art. 34 Condition suspensive / personnalité morale | 482–487 | Boilerplate |
| Art. 35 Conciliation | 488–491 | Boilerplate |
| Art. 36 Frais | 492–495 | Boilerplate |
| Art. 37 Pouvoirs | 497–500 | Boilerplate |
| Art. 38 Élection de domicile | 502–505 | Boilerplate |
| **Bloc signature** | 507–513 | **507 = lieu + date** ; **510 = signatures (personne 1 + personne morale)** ; 511–513 = mention « bon pour acceptation » (inchangé) |
| Annexe | 531–540 | Liste des actes (boilerplate ; mention « cabinet Sydel » conservée) |

## Placeholders introduits (46 distincts)

Convention indexée multi-associés (calquée sur le modèle SCM `Statuts SCM.docx` + consigne de la mission). Personne physique = `_personne_1` ; personne morale associée = `_associe_1`.

### Société
- `[denomination_societe]`
- `[profession_reglementee]`, `[profession_reglementee_pluriel]`
- `[capital_social]`, `[capital_lettres]`
- `[nb_actions]`, `[nb_actions_lettres]`
- `[valeur_nominale_action]`, `[valeur_nominale_action_lettres]`
- `[adresse_siege]`, `[adresse_lieu_exercice]`
- `[nom_banque]`, `[adresse_banque]`
- `[date_cloture_premier_exercice]`
- `[lieu_signature]`, `[date_signature]`

### Personne physique 1 (associée exerçante / présidente)
- `[civilite_personne_1]`, `[prenoms_personne_1]`, `[nom_personne_1]`
- `[qualification_principale_personne_1]`
- `[date_naissance_personne_1]`, `[ville_naissance_personne_1]`, `[departement_naissance_personne_1]`
- `[nationalite_personne_1]`, `[situation_maritale_personne_1]`
- `[adresse_personnelle_personne_1]`
- `[ordre_departemental_personne_1]`, `[numero_ordre_personne_1]`, `[numero_rpps_personne_1]`
- `[apport_personne_1]`, `[apport_lettres_personne_1]`
- `[nb_actions_personne_1]`, `[nb_actions_personne_1_lettres]`

### Personne morale associée 1 (associée non exerçante)
- `[denomination_societe_associe_1]`
- `[forme_sociale_associe_1]`
- `[capital_societe_associe_1]`
- `[adresse_siege_associe_1]`
- `[ville_rcs_associe_1]`, `[numero_rcs_associe_1]`
- `[civilite_representant_associe_1]`, `[prenoms_representant_associe_1]`, `[nom_representant_associe_1]`
- `[apport_associe_1]`, `[apport_lettres_associe_1]`
- `[nb_actions_associe_1]`, `[nb_actions_associe_1_lettres]`

## Notes pour la phase « générateur SELAS multi »

1. **Multiplicité réelle** : ce source a 1 personne physique + 1 personne morale. Le générateur multi devra **boucler sur N associés** (physiques et/ou morales). La convention indexée `_personne_N` / `_associe_N` est posée mais le **modèle ne contient qu'un exemplaire de chaque bloc** : la duplication des blocs comparution/apport/répartition pour N>2 est à concevoir au générateur, pas dans le modèle figé.
2. **Cohérence vocabulaire** : le SELAS mono (`Statuts_SELAS_medecin.docx`) emploie `[civilite]/[prenom]/[nom]` (non indexés), `[apport_personne_1]/[apport_lettres_personne_1]`, `[ordre_professionnel]`, `[ordre_departemental]`, `[numero_ordre]`, `[numero_rpps]`. **Divergence de nommage à arbitrer** côté générateur : aligner sur l'indexé `_personne_1` (choix de ce modèle) ou réutiliser le socle SELAS mono. À trancher techniquement à la construction du moteur (pas une décision métier).
3. **Genre** : le source est entièrement au féminin (« née », « associée exerçante », « nommée présidente »). Le wording gendré est **conservé tel quel** dans le modèle (non tokenisé). La gestion du genre (accord civilité) relève du moteur — voir le mécanisme `_CIVILS_FIX_SPEC_V1.md` / dérivation civilité existant.

## Divergences restantes (wording absent / non tokenisable du source — NE PAS inventer)

- **Article 15 (Directeurs Généraux)** : aucun DG concret nommé dans le source → aucun placeholder DG « personne » introduit. Si le moteur doit gérer des DG nommés, le **bloc de désignation DG nominatif est absent du modèle** et devra être rédigé/confirmé (NotebookLM / associé) avant d'être tokenisé.
- **Capital de la personne morale associée** : le source dit « **au capital minimum de 1.020 euros** » (capital **variable**). Tokenisé en `[capital_societe_associe_1]` mais la mention « minimum » / « variable » spécifique aux sociétés civiles à capital variable est **portée par `[forme_sociale_associe_1]`** (qui absorbe « Société Civile, à capital variable »). Si le moteur doit distinguer capital fixe vs variable pour l'associé morale, ce point est à préciser.
- **Forme sociale de l'associé morale** : ici « Société Civile à capital variable » — un seul cas observé. Pour d'autres formes d'associé morale (SPFPL, autre SEL…), le wording exact n'est pas dans ce source.
- **Non-concurrence (Art. 19)** : durée « 2 ans » et rayon « 2 kilomètres » laissés **en dur** (non tokenisés) — valeurs potentiellement métier/variables ; à confirmer si elles doivent devenir des champs.
- **Durée société (Art. 6)** : « 99 années » laissé en dur (standard, non tokenisé).
- **Annexe** : mention « cabinet Sydel » conservée (référence au cabinet émetteur, pas une donnée client).
