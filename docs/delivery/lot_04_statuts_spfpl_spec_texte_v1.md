# DAAT x SYDEL - SPEC TEXTE V1
## Lot 04 - Statuts SPFPL

## 1. Objet

Stabiliser le texte canonique et les variantes textuelles de la famille `Statuts SPFPL`, sans coder.

Cette spec texte complete :
- `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md`

Elle vise a preparer de futurs generateurs deterministes pour :
- les statuts SPFPL cession ;
- les statuts SPFPL apport.

Cette spec ne modifie aucun wording juridique source. Les formulations divergentes ou suspectes sont conservees comme constats ou transformees en points ouverts bloquants avant code.

## 2. Sources lues

Memoire projet et referentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_04_statuts_preparation_v1.md`
- `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md`

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Sources Lot 04 lues :
- `project/source_documents/lot_04/Statuts_SPFPLAS_dentistes_cession.docx`
- `project/source_documents/lot_04/Statuts SPFPLAS dentistes - apport.docx`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : generation DOCX propre from-scratch pour les futurs tickets code ;
- ADR-0005 : mode Codex repo-first.

## 3. Perimetre texte V1

Chemins couverts :
- `SPFPL_CESSION` pour les statuts issus de `Statuts_SPFPLAS_dentistes_cession.docx` ;
- `SPFPL_APPORT` pour les statuts issus de `Statuts SPFPLAS dentistes - apport.docx`.

Hors perimetre :
- statuts SEL, statuts civils, statuts SAS ;
- note d'information, PV d'agrement, acte de cession, contrat d'apport et attestations SPFPL deja traites en Lot 05 ;
- adaptation multi-associes non sourcee ;
- correction juridique ou orthographique des sources.

Decision texte V1 :
- le texte canonique est une famille a deux overlays ;
- le tronc commun est d'abord structurel ;
- le wording source de chaque overlay prime sur toute tentative d'harmonisation ;
- les articles communs ne doivent pas etre deduplices par similarite sans revue humaine.

## 4. Tronc commun structurel

Les deux statuts suivent la meme architecture generale :

```text
{societe_spfpl.denomination}
{societe_spfpl.libelle_forme_et_capital}
Siege social : {societe_spfpl.siege.adresse_affichee}

STATUTS

Le soussigne :
{associes[0].identite_statuts}

FORME - OBJET - DENOMINATION SOCIALE - SIEGE SOCIAL - DUREE
ARTICLE 1 - FORME
ARTICLE 2 - OBJET
ARTICLE 3 - DENOMINATION
ARTICLE 4 - SIEGE SOCIAL
ARTICLE 5 - DUREE
ARTICLE 6 - APPORTS
ARTICLE 7 - COMPTES COURANTS
ARTICLE 8 - CAPITAL SOCIAL
ARTICLE 9 - QUALITE D'ASSOCIE
ARTICLE 10 - MODIFICATIONS DU CAPITAL SOCIAL
ARTICLE 11 - LIBERATION ET REPRESENTATION DES ACTIONS
ARTICLE 12 - FORME DES ACTIONS
ARTICLE 13 - DROITS ET OBLIGATIONS ATTACHES AUX ACTIONS
ARTICLE 14 - INDIVISIBILITE DES ACTIONS
ARTICLE 15 - CESSION - TRANSMISSION DES ACTIONS
ARTICLE 16 - NULLITE DES CESSIONS D'ACTIONS
ARTICLE 17 - LOCATION DES ACTIONS
ARTICLE 18 - EXCLUSION D'UN ASSOCIE
ARTICLE 19 - LE PRESIDENT
ARTICLE 20 - DIRECTEURS GENERAUX
ARTICLE 21 - COMMISSAIRES AUX COMPTES
ARTICLE 22 - CONVENTIONS ENTRE LA SOCIETE ET LES DIRIGEANTS
ARTICLE 23 - DECISIONS COLLECTIVES
ARTICLE 24 - DECISIONS COLLECTIVES ORDINAIRES
ARTICLE 25 - DECISIONS COLLECTIVES EXTRAORDINAIRES
ARTICLE 26 - DROIT DE COMMUNICATION, D'INFORMATION ET DE CONTROLE DES ASSOCIES
ARTICLE 27 - EXERCICE SOCIAL - COMPTES SOCIAUX
ARTICLE 28 - COMPTES ANNUELS
ARTICLE 29 - AFFECTATION ET REPARTITION DES RESULTATS
ARTICLE 30 - CAPITAUX PROPRES INFERIEURS A LA MOITIE DU CAPITAL SOCIAL
ARTICLE 31 - PAIEMENT DES DIVIDENDES - ACOMPTES
ARTICLE 32 - TRANSFORMATION DE LA SOCIETE
ARTICLE 33 - DISSOLUTION - LIQUIDATION
ARTICLE 34 - DECES, INTERDICTION, FAILLITE D'UN ASSOCIE
ARTICLE 35 - CONTESTATIONS
ARTICLE 36 - CONDITION SUSPENSIVE
ARTICLE 37 - DECLARATION ORDINALE DE LA SITUATION DE LA SOCIETE
ARTICLE 38 - NOMINATION DU PRESIDENT
ARTICLE 39 - ACTES PASSES POUR LA SOCIETE EN FORMATION
ARTICLE 40 - PUBLICITE - POUVOIRS
Signature
ANNEXE 1
```

Regle de fidelite :
- cette architecture ne vaut pas autorisation de reecrire les articles ;
- les titres ci-dessus normalisent seulement la lecture de la structure ;
- les titres source presentent parfois des espaces, tirets ou collages differents, qui devront etre conserves ou corriges uniquement sur validation.

## 5. Overlay texte cession

Source :
- `project/source_documents/lot_04/Statuts_SPFPLAS_dentistes_cession.docx`

### 5.1 En-tete cession

Structure source :

```text
{societe_spfpl.denomination}
Societe de Participations Financieres de Profession Liberale de Chirurgiens-Dentistes par actions simplifiee
Au capital de {societe_spfpl.capital_social}
Siege social : {societe_spfpl.siege.adresse_affichee}
STATUTS
```

Points de fidelite :
- le libelle de forme est fixe dans la source ;
- `capital_social` est affiche sans `euros` dans l'en-tete source ;
- la source utilise `Chirurgiens-Dentistes` dans l'en-tete.

### 5.2 Comparution cession

Structure source :

```text
Le soussigne :
- {associes[0].civilite_affichage} {associes[0].prenoms} {associes[0].nom}
{associes[0].profession} de profession
Ne le {associes[0].date_naissance} a {associes[0].ville_naissance} ({associes[0].departement_naissance})
Demeurant {associes[0].adresse_personnelle_affichee}
{associes[0].situation_maritale} sous le regime de {associes[0].regime_matrimonial} avec {associes[0].conjoint.civilite_affichage} {associes[0].conjoint.prenom} {associes[0].conjoint.nom}
De nationalite {associes[0].nationalite}
Inscrit au tableau de l'Ordre des Chirurgiens-Dentistes de {ordre.departemental} sous le n {ordre.numero} et sous le numero RPPS {ordre.numero_rpps}
```

Points de fidelite :
- la source cession emploie `[prenoms]` dans la comparution et l'article 38, mais `[prenom]` dans certains autres blocs ;
- le conjoint et le regime matrimonial sont explicites dans la source cession.

### 5.3 Article 1 cession

Decision texte :
- conserver l'article 1 de la source cession comme overlay cession ;
- ne pas remplacer automatiquement le libelle fixe par `[forme_sociale]`.

Constat :
- la source cession decrit une SPFPL constituee sous forme de Societe par Actions Simplifiee ;
- elle ne decompose pas les bases legales en liste comme la source apport.

### 5.4 Article 6 cession - apports en numeraire

Structure source :

```text
A la constitution de la Societe, le soussigne fait les apports suivants :
- Le Docteur {associes[0].prenom} {associes[0].nom}, associe unique, apporte {apport_numeraire.montant_lettres}
Ci{apport_numeraire.montant}
Total des apports{apport_numeraire.montant}
au credit du compte ouvert aupres de la banque {apport_numeraire.banque.nom} sise {apport_numeraire.banque.adresse_affichee}.
```

Regles :
- ce bloc est propre a l'overlay cession ;
- la banque est une donnee fournie, pas une constante ;
- la ponctuation et l'espacement source autour de `Ci` et `Total des apports` doivent etre relus avant code.

### 5.5 Article 8 cession - capital social

Structure source :

```text
Le capital social est fixe a la somme de {societe_spfpl.capital_social} ({societe_spfpl.capital_social_lettres}) euros, divise en {capital_souscription.nb_actions_total} actions de {capital_souscription.valeur_nominale_action} ({capital_souscription.valeur_nominale_action_lettres}) chacune, entierement libere et attribue en totalite a l'associe unique :
- Le Docteur {associes[0].prenom} {associes[0].nom} ... {capital_souscription.nb_actions_total} actions
Total des actions composant le capital social ... {capital_souscription.nb_actions_total} actions
```

Regle :
- la source V1 ne couvre que l'associe unique ;
- toute liste multi-associes doit rester bloquee sans arbitrage.

### 5.6 Article 27 cession

Structure source :

```text
Chaque exercice social a une duree d'une annee, qui commence le {exercice_social.debut} et finit le {exercice_social.fin}.
Par exception, le premier exercice commencera le jour de l'immatriculation de la Societe au Registre du commerce et des societes et se terminera le {exercice_social.premier_exercice_fin}.
```

Regle :
- cession conserve trois variables distinctes : debut, fin, premier exercice.

### 5.7 Signature et annexe cession

Structure source :

```text
Fait a {signature.lieu}
Le
{associes[0].civilite_affichage} {associes[0].prenom} {associes[0].nom}
"Bon pour acceptation des fonctions de President"

ANNEXE 1
ETAT DES ENGAGEMENTS PRIS AVANT
LA CONSTITUTION DE LA SOCIETE
Ouverture d'un compte bancaire aupres de la Banque en vue du depot du capital social
Signature d'une lettre de mission avec le cabinet Sydel pour la creation de la Societe
Paiement de l'acompte des honoraires du cabinet Sydel pour la creation de la Societe
```

Regle :
- ne pas injecter automatiquement `signature.date` apres `Le` sans validation ;
- les engagements repris sont un bloc annexe source, pas une liste libre a enrichir.

## 6. Overlay texte apport

Source :
- `project/source_documents/lot_04/Statuts SPFPLAS dentistes - apport.docx`

### 6.1 En-tete apport

Structure source :

```text
{societe_spfpl.denomination}
Societe par actions simplifieesau capital de {societe_spfpl.capital_social} euros
Societe de Participations Financieres de Profession Liberale de dentistes
Siege social : {societe_spfpl.siege.adresse_affichee}
STATUTS
```

Points de fidelite :
- la source contient `simplifieesau` sans espace visible ;
- ne pas corriger ce libelle sans validation juridique ou redactionnelle.

### 6.2 Comparution apport

Structure source :

```text
Le soussigne :
- {associes[0].civilite_affichage} {associes[0].prenom} {associes[0].nom}
{associes[0].profession} de profession
Ne le {associes[0].date_naissance} a {associes[0].ville_naissance} ({associes[0].departement_naissance})
Demeurant {associes[0].adresse_personnelle_affichee}
{associes[0].situation_maritale}
De nationalite {associes[0].nationalite}
Inscrit au tableau de l'Ordre des {ordre.profession_reglementee} de {ordre.ville} sous le n {ordre.numero} et sous le numero RPPS {ordre.numero_rpps}
```

Points de fidelite :
- le conjoint n'est pas detaille dans la source apport ;
- l'ordre est rendu via profession reglementee et ville d'ordre, pas via departement ordinal.

### 6.3 Article 1 apport

Decision texte :
- conserver l'article 1 de la source apport comme overlay apport ;
- ne pas remplacer automatiquement les bases legales detaillees par le bloc cession.

Constat :
- l'article 1 apport parametre la forme sociale avec `{societe_spfpl.forme_sociale}` ;
- il liste l'ordonnance du 8 fevrier 2023, le Code de commerce, le Code de la Sante publique et le Code de deontologie medicale.

### 6.4 Article 6 apport - apports en nature

Structure source :

```text
A la constitution de la Societe, le soussigne a fait les apports suivants :
Apports en nature
{associes[0].civilite_affichage} {associes[0].prenom} {associes[0].nom} fait apport de {apport_titres.nb_parts_lettres} ({apport_titres.nb_parts}) parts numerotees de {apport_titres.plage_parts} de la societe d'exercice liberal a responsabilite limitee de chirurgiens-dentistes denommee "{societe_cible.denomination}", ayant son siege {societe_cible.siege.adresse_affichee}, immatriculee au RCS de {societe_cible.ville_rcs} sous le n {societe_cible.numero_rcs} pour une valeur de :
{apport_titres.valeur_globale} EUR
Total des apports en nature {apport_titres.valeur_globale} EUR
Le rapport du Commissaire aux apports charge de controler l'evaluation des apports en nature est annexe aux presents statuts.
Le transfert de la propriete des parts se realisera au jour de l'immatriculation de la SPFPL.
Apports en numeraire
Neant
Total des apports realises {apport_titres.valeur_globale} EUR
```

Regles :
- `apport_titres.plage_parts` mappe l'alias source `[plage_parts_cedees]`, malgre son nom cession ;
- le commissaire aux apports est requis par le texte ;
- aucune conversion en apport numerique ne doit etre inventee.

### 6.5 Article 8 apport - capital social

Structure source :

```text
Le capital social est fixe a la somme de {apport_titres.valeur_globale} EUR {apport_titres.valeur_globale} euros, divise en {capital_souscription.nb_actions_total} actions de {capital_souscription.valeur_nominale_action} ({capital_souscription.valeur_nominale_action_lettres}) chacune, entierement libere et attribue comme suit :
- Le Docteur {associes[0].prenom} {associes[0].nom} ... {capital_souscription.nb_actions_total} actions
Total des actions composant le capital social ... {capital_souscription.nb_actions_total} actions
```

Point de fidelite :
- la source repete `montant_apports_nature` en chiffres puis en lettres attendues mais non separees ; ne pas corriger sans validation.

### 6.6 Article 27 apport

Structure source :

```text
Chaque exercice social a une duree d'une annee, qui commence le1er janvier et finit le 31 decembre.
Par exception, le premier exercice commencera le jour de l'immatriculation de la Societe au Registre du commerce et des societes et se terminera le {exercice_social.premier_exercice_fin}.
```

Regle :
- conserver l'exercice fixe de l'overlay apport ;
- ne pas reprendre les variables `debut_exercice` et `date_cloture_exercice_1` de la source cession.

### 6.7 Signature et annexe apport

Structure source :

```text
Fait a {signature.lieu}
Le {signature.date}
{associes[0].civilite_affichage} {associes[0].prenom} {associes[0].nom}
"Bon pour acceptation des fonctions de President"

ANNEXE 1
ETAT DES ENGAGEMENTS PRIS AVANT
LA CONSTITUTION DE LA SOCIETE
Nomination d'un commissaire aux apports
```

Regle :
- contrairement a la cession, la date de signature est sourcee par `[date_signature]` ;
- l'annexe apport ne doit pas reprendre les engagements bancaires et SYDEL de la source cession sans validation.

## 7. Blocs associes dynamiques

### 7.1 Source V1 mono-associe

Les deux sources utilisent un associe unique dans :
- la comparution ;
- l'article 6 ;
- l'article 8 ;
- l'article 38 ;
- la signature.

Texte source equivalent :

```text
- Le Docteur {associes[0].prenom} {associes[0].nom} ... {capital_souscription.nb_actions_total} actions
Total des actions composant le capital social ... {capital_souscription.nb_actions_total} actions
```

### 7.2 Extension multi-associes

La source de verite indique que les statuts peuvent comporter plusieurs associes.

Decision texte V1 :
- aucune forme multi-associes SPFPL n'est validee par les deux DOCX lus ;
- le futur generateur doit bloquer si `associes[].length > 1` tant qu'une table de rendu multi-associes n'est pas fournie ;
- les accords `associe unique`, `soussignes`, `totalite a l'associe unique` et signatures multiples ne doivent pas etre deduits automatiquement.

## 8. Variables texte et aliases

### 8.1 Communes aux deux overlays

| Alias source | Variable texte canonique | Note |
|---|---|---|
| `[denomination_societe]` | `societe_spfpl.denomination` | SPFPL en constitution |
| `[capital_social]` | `societe_spfpl.capital_social` | en-tete et capital |
| `[adresse_siege]` | `societe_spfpl.siege.adresse_affichee` | adresse complete source |
| `[civilite]` | `associes[0].civilite_affichage` | source mono-associe |
| `[prenom]` | `associes[0].prenom` | source apport et blocs cession |
| `[prenoms]` | `associes[0].prenoms` ou `associes[0].prenom` | cession uniquement, a arbitrer |
| `[nom]` | `associes[0].nom` | commun |
| `[profession]` | `associes[0].profession` | commun |
| `[date_naissance]` | `associes[0].date_naissance` | commun |
| `[ville_naissance]` | `associes[0].ville_naissance` | commun |
| `[departement_naissance]` | `associes[0].departement_naissance` | commun |
| `[adresse_personnelle]` | `associes[0].adresse_personnelle_affichee` | commun |
| `[situation_maritale]` | `associes[0].situation_maritale` | commun, detail variable selon overlay |
| `[nationalite]` | `associes[0].nationalite` | commun |
| `[numero_ordre]` | `ordre.numero` | commun |
| `[numero_rpps]` | `ordre.numero_rpps` | commun |
| `[nb_actions]` | `capital_souscription.nb_actions_total` | commun |
| `[lieu_signature]` | `signature.lieu` | commun |

### 8.2 Cession

| Alias source | Variable texte canonique | Note |
|---|---|---|
| `[capital_lettres]` | `societe_spfpl.capital_social_lettres` | capital cession |
| `[valeur_nominale_action]` | `capital_souscription.valeur_nominale_action` | cession |
| `[valeur_nominale_action_lettres]` | `capital_souscription.valeur_nominale_action_lettres` | cession |
| `[montant_apport]` | `apport_numeraire.montant` | apport en numeraire |
| `[montant_apport_lettres]` | `apport_numeraire.montant_lettres` | apport en numeraire |
| `[nom_banque]` | `apport_numeraire.banque.nom` | banque de depot |
| `[adresse_banque]` | `apport_numeraire.banque.adresse_affichee` | banque de depot |
| `[regime_matrimonial]` | `associes[0].regime_matrimonial` | comparution |
| `[civilite_conjoint]` | `associes[0].conjoint.civilite_affichage` | comparution |
| `[prenom_conjoint]` | `associes[0].conjoint.prenom` | comparution |
| `[nom_conjoint]` | `associes[0].conjoint.nom` | comparution |
| `[ordre_departemental]` | `ordre.departemental` | cession |
| `[debut_exercice]` | `exercice_social.debut` | cession |
| `[fin_exercice]` | `exercice_social.fin` | cession |
| `[date_cloture_exercice_1]` | `exercice_social.premier_exercice_fin` | cession |

### 8.3 Apport

| Alias source | Variable texte canonique | Note |
|---|---|---|
| `[forme_sociale]` | `societe_spfpl.forme_sociale` | article 1 et responsabilite president |
| `[profession_reglementee]` | `ordre.profession_reglementee` | comparution |
| `[ville_ordre]` | `ordre.ville` | comparution |
| `[nb_parts_apportees]` | `apport_titres.nb_parts` | apport en nature |
| `[nb_parts_apportees_lettres]` | `apport_titres.nb_parts_lettres` | apport en nature |
| `[plage_parts_cedees]` | `apport_titres.plage_parts` | alias source a confirmer |
| `[denomination_societe_cedee]` | `societe_cible.denomination` | societe cible apportee |
| `[ville_rcs_societe_cedee]` | `societe_cible.ville_rcs` | societe cible apportee |
| `[numero_rcs_societe_cedee]` | `societe_cible.numero_rcs` | societe cible apportee |
| `[montant_apports_nature]` | `apport_titres.valeur_globale` | valeur globale de l'apport |
| `[valeur_nominale_part]` | `capital_souscription.valeur_nominale_action` | alias source divergent |
| `[valeur_nominale_part_lettres]` | `capital_souscription.valeur_nominale_action_lettres` | alias source divergent |
| `[fin_exercice]` | `exercice_social.premier_exercice_fin` | premier exercice apport |
| `[date_signature]` | `signature.date` | apport uniquement |

## 9. Elements manuels

Doivent etre fournis ou valides hors texte fixe :
- adresse complete du siege ;
- profession affichee ;
- libelle ordinal et ville/departement ordinal ;
- situation matrimoniale et conjoint ;
- banque de depot pour cession ;
- commissaire aux apports et rapport annexe pour apport ;
- premier exercice social ;
- date de signature cession si elle doit etre remplie ;
- contenu exact des annexes ;
- liste multi-associes si elle est demandee.

Restent hors automatisation V1 :
- correction des anomalies de source ;
- ajout d'une date de signature cession ;
- harmonisation des articles 1, 23 ou 27 entre cession et apport ;
- adaptation du texte a plusieurs associes ;
- ajout ou retrait de clauses ordinales.

## 10. Regles de fidelite avant generation

Le futur generateur doit :
- selectionner un seul overlay : cession ou apport ;
- reconstruire un DOCX propre from-scratch ;
- conserver les articles source de l'overlay selectionne ;
- remplacer uniquement les zones variables specifiees ;
- bloquer si un placeholder source resterait visible ;
- bloquer si une correction de wording est necessaire mais non validee ;
- bloquer si plusieurs associes sont presents sans spec multi-associes.

Le futur generateur ne doit pas :
- prendre un DOCX source comme template d'execution ;
- corriger `simplifieesau`, `c_m`, `1cr`, `l'objet <lesdites` ou toute autre anomalie visible sans validation ;
- transformer `[plage_parts_cedees]` en wording cession dans l'overlay apport ;
- copier l'annexe cession dans l'apport ou inversement ;
- coder `Sydel` comme constante si l'annexe devient parametree.

## 11. Criteres avant implementation

Un ticket de code peut demarrer si :
- les deux documents cibles sont explicitement retenus ou le ticket limite a un seul overlay ;
- le comportement de la date de signature cession est tranche ;
- le comportement multi-associes est tranche ou bloque explicitement ;
- les anomalies source a conserver sont listees ;
- les champs `associes[]`, `societe_spfpl`, `capital_souscription`, `apport_numeraire`, `apport_titres`, `societe_cible`, `ordre`, `exercice_social` et `signature` sont disponibles dans le contexte ou mappes ;
- les tests futurs couvrent les overlays cession et apport si les deux sont codes ;
- les tests verifient l'absence de placeholders residuels ;
- les tests verifient que l'overlay non selectionne n'apparait pas dans le document produit ;
- aucune formulation juridique n'est modifiee hors decision documentee.

## 12. Points ouverts

1. **Multi-associes SPFPL** : aucune forme texte multi-associes n'est sourcee pour ces deux statuts ; bloquer ou arbitrer avant code.
2. **Date de signature cession** : la source cession affiche seulement `Le`; confirmer si ce champ doit rester manuel.
3. **Alias `[prenoms]`** : confirmer le mapping avec `associes[0].prenom` ou un champ separe `prenoms`.
4. **Alias `[plage_parts_cedees]` dans l'apport** : conserver comme alias source, mais confirmer avant code.
5. **Article 1 apport** : la source apport contient `[forme_sociale]` et des bases legales detaillees ; ne pas remplacer par l'article 1 cession.
6. **Article 23** : les differences de decisions collectives et de proces-verbal entre cession et apport doivent etre conservees ou arbitrees.
7. **Anomalies source apport** : plusieurs anomalies visibles doivent etre relues avant toute correction.
8. **Annexes** : les annexes 1 ne portent pas les memes engagements ; valider les contenus avant automatisation.
9. **Commissaire aux apports** : l'apport suppose un rapport annexe ; le role doit venir du contexte ou d'un referentiel valide.
10. **Wording ordinal** : les libelles Ordre / Chirurgiens-Dentistes / profession reglementee ne doivent pas etre generalises sans source.

## 13. Statut de la spec texte

`SPEC-STATUTS-SPFPL-001` stabilise la spec texte V1 des statuts SPFPL cession et apport, sans code Python.

La prochaine etape recommandee est un arbitrage metier sur les points ouverts 1, 2, 6, 7 et 8 avant tout ticket de code statuts SPFPL.
