# DAAT x SYDEL - ARBITRAGES V1
## Famille `cession cabinets medical / dentaire` - ARBITRAGE-CESSION-001

## 1. Objet

Ce document ferme les arbitrages V1 possibles avant une future vague de code sur la famille documentaire `cession cabinets`.

Il complete :
- `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md` ;
- `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.

Il ne modifie aucun wording juridique source. Les decisions ci-dessous sont des decisions de production documentaire V1 : elles fixent ce que le futur moteur peut generer, ce qu'il doit laisser en saisie humaine, et ce qu'il doit encore bloquer.

## 2. Sources relues

Memoire projet :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`

Specs :
- `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`
- `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : generation DOCX propre from-scratch pour un futur ticket code ;
- ADR-0005 : mode Codex repo-first.

Observation source de verite :
- les branches SELARL et SELAS listent chacune les documents `acte` et `compromis` pour cabinet medical ;
- les branches SELARL et SELAS listent chacune les documents `acte` et `compromis` pour cabinet dentaire ;
- la source de verite ne precise pas une generation simultanee obligatoire de l'acte et du compromis.

## 3. Regle de lecture V1

Le futur code doit respecter trois principes :
- ne pas fusionner des documents juridiques distincts sous pretexte de similarite ;
- determiner les roles par le contexte juridique de la clause, pas uniquement par le nom technique d'un placeholder source ;
- bloquer une generation quand une anomalie source peut changer le sens juridique du document.

## 4. Points tranches

### 4.1 Acte vs compromis

Decision V1 :
- conserver quatre documents canoniques distincts :
  - `LOT03-CESSION-ACTE-MEDICAL` ;
  - `LOT03-CESSION-COMPROMIS-MEDICAL` ;
  - `LOT03-CESSION-ACTE-DENTAIRE` ;
  - `LOT03-CESSION-COMPROMIS-DENTAIRE` ;
- piloter la selection par une etape explicite `dossier.cession.etape in {acte, compromis}` ;
- ne pas produire automatiquement acte et compromis ensemble si l'etape n'est pas fournie.

Consequence pour le code :
- `dossier.options.cession == true` ne suffit pas ;
- `dossier.cession.etape` est obligatoire ;
- si le besoin metier est de produire les deux documents, le dossier doit le demander explicitement par deux generations ou par une future liste d'etapes explicitement arbitree.

### 4.2 Medical vs dentaire

Decision V1 :
- conserver des variantes medicales et dentaires separees ;
- ne pas appliquer une clause dentaire a un document medical ;
- ne pas appliquer une clause medicale a un document dentaire ;
- les clauses d'accessibilite et de conciliation dentaires restent propres aux documents dentaires.

Consequence pour le code :
- `dossier.cession.type_cabinet` est obligatoire ;
- `medical` et `dentaire` doivent etre testes separement ;
- tout residu de wording contraire au type de cabinet doit bloquer, sauf validation metier explicite.

### 4.3 SELARL vs SELAS

Decision V1 :
- la source de verite rattache les memes quatre documents de cession aux branches SELARL et SELAS ;
- la generation peut donc etre eligible pour `dossier.structure in {SELARL, SELAS}` ;
- le futur code ne doit toutefois pas inventer de wording SELAS specifique.

Consequence pour le code :
- les champs variables de forme sociale de l'acquereur doivent porter la structure ;
- si une source contient un residu non parametre propre a SELARL alors que le dossier est SELAS, la generation doit bloquer.

### 4.4 Placeholders vendeur / acquereur

Decision V1 :
- les placeholders portant `vendeur` dans une zone qui decrit clairement l'acquereur ou son representant sont traites comme des erreurs techniques de placeholder ;
- dans ces zones, le mapping cible est le role juridique visible dans la clause :
  - vendeur -> `cession.vendeur.*` ;
  - societe acquereur -> `cession.acquereur.*` ;
  - representant de l'acquereur -> `cession.acquereur.representant.*`.

Consequence pour le code :
- le mapping ne doit pas recopier aveuglement `cession.vendeur.*` dans le bloc representant acquereur ;
- chaque correction de mapping doit etre couverte par un test ciblant le role rendu ;
- si le contexte de la clause ne permet pas d'identifier le role avec certitude, la generation doit bloquer.

### 4.5 Credit-vendeur

Decision V1 :
- le credit-vendeur est un bloc conditionnel de l'acte medical uniquement ;
- le bloc est desactive par defaut ;
- la mention source d'instruction `Ajouter en cas de CV` ne doit jamais etre rendue ;
- aucun bloc credit-vendeur n'est cree pour les documents dentaires en V1.

Consequence pour le code :
- si `cession.financement.credit_vendeur.actif == false`, le bloc est absent ;
- si `cession.financement.credit_vendeur.actif == true`, les champs montant, duree, taux et majoration d'interet de retard sont obligatoires ;
- toute demande de credit-vendeur hors acte medical bloque la generation en V1.

### 4.6 Taux de pret du compromis dentaire

Decision V1 :
- le taux source fixe `5 %` du compromis dentaire est conserve comme wording source V1 ;
- le compromis dentaire ne requiert pas `cession.financement.pret.taux` tant qu'aucune validation metier ne transforme ce taux en variable.

Consequence pour le code :
- le compromis medical utilise les variables montant, taux et duree de pret ;
- le compromis dentaire utilise le montant du pret et conserve le taux source fixe.

### 4.7 Chiffres d'affaires et resultats

Decision V1 :
- le futur modele utilise `cession.exercices[]` avec exactement trois lignes structurees ;
- les anomalies de placeholders repetes ou de periodes fixes melangees ne sont pas reproduites comme logique metier.

Consequence pour le code :
- chaque ligne doit contenir `periode`, `chiffre_affaires` et `resultat` ;
- la generation bloque si les trois exercices ne sont pas complets ;
- les periodes affichees viennent du contexte dossier, pas d'annees fixes codees en dur.

### 4.8 Signatures

Decision V1 :
- chaque document conserve son mode de signature source ;
- les images de signature restent optionnelles quand le document source prevoit des placeholders image ;
- les mentions manuscrites restent explicites et propres au document qui les prevoit ;
- aucune signature electronique effective n'est automatisee en V1.

Consequence pour le code :
- `signature.lieu` et `signature.date` sont les champs communs attendus quand la zone de signature contient lieu/date ;
- les mentions `Lu et approuve` ne sont rendues que pour les documents sources qui les prevoient ;
- la convention de preuve / signature electronique est un texte source a rendre quand elle existe, pas une integration technique de signature.

## 5. Points a laisser manuels en V1

Ces points ne doivent pas etre deduits automatiquement. Ils peuvent etre fournis par le contexte dossier, saisis humainement, ou traites hors generation initiale.

### 5.1 Origine de propriete et bail

Rester manuel en V1 :
- description de l'origine de propriete ;
- date ou annees d'acquisition / creation ;
- precedent proprietaire ;
- details du bail ;
- activite autorisee par le bail ;
- loyer, duree, dates et reconductions.

### 5.2 Prix, pret et prorata

Rester manuel en V1 :
- prix total en chiffres et en lettres ;
- repartition corporels / incorporels ;
- conditions de pret quand elles sont variables ;
- prorata d'exploitation si des montants detailles doivent etre ajoutes ;
- verification metier de l'arithmetique du prix si le projet veut l'imposer.

### 5.3 Salaries

Decision V1 :
- `cession.salaries[]` reste une liste repetable fournie par contexte ;
- aucun document ne doit imposer globalement deux salaries dans le modele ;
- l'acte medical ne doit pas rendre la ligne incomplete `De reprendre les contrats de travail de`.

Rester manuel en V1 :
- decision de reprendre ou non des salaries ;
- identite des salaries repris ;
- adaptation eventuelle du wording si le nombre de salaries differe de la source dentaire.

### 5.4 SCM

Decision V1 :
- la clause SCM de l'acte medical reste conditionnelle et manuelle ;
- elle ne doit pas etre activee automatiquement par le seul type `medical` ;
- elle ne remplace pas la famille documentaire SCM separee.

Rester manuel en V1 :
- activation de la clause SCM ;
- nombre de parts ;
- coherence avec les documents SCM separes du dossier.

### 5.5 Signatures, exemplaires et annexes

Rester manuel en V1 :
- images de signature si utilisees ;
- mentions manuscrites ;
- nombre de pages ;
- nombre d'exemplaires quand la source utilise un placeholder ;
- liste et contenu des annexes.

Decision V1 :
- les annexes titrees peuvent etre listees ;
- aucun contenu d'annexe n'est genere automatiquement faute de source annexe detaillee.

## 6. Points reellement bloquants restants

Les points suivants bloquent la generation automatique complete tant qu'une validation metier ou textuelle n'est pas ajoutee.

### 6.1 Mentions dentaires dans les sources medicales

Blocage :
- les formulations dentaires presentes dans des blocs medicaux, notamment autour du bail, ne doivent pas etre corrigees automatiquement ;
- elles ne doivent pas non plus etre rendues dans un document medical sans validation.

Decision requise :
- confirmer si la source medicale doit etre conservee telle quelle ;
- ou fournir le wording medical corrige a substituer.

### 6.2 Origine de propriete du compromis medical

Blocage :
- le compromis medical semble designer le representant acquereur comme proprietaire dans le bloc origine de propriete ;
- ce point peut changer le role juridique de la clause.

Decision requise :
- confirmer le role a afficher dans ce bloc ;
- ou fournir le texte corrige.

### 6.3 Titre anormal de realisation dans les compromis

Blocage :
- le titre source `[date_origine_propriete] PREVUE DE REALISATION` semble utiliser une variable incoherente.

Decision requise :
- confirmer la variable attendue, probablement une date limite ou date prevue de realisation ;
- ou valider le maintien du wording source.

### 6.4 Placeholders ambigus hors contexte clair

Blocage :
- les erreurs de placeholders vendeur/acquereur sont tranchees seulement lorsque le contexte de clause identifie clairement le role juridique ;
- si le role n'est pas clair, le code ne doit pas choisir.

Decision requise :
- fournir le mapping de role exact pour la zone concernee.

### 6.5 Ligne incomplete sur contrats de travail dans l'acte medical

Blocage :
- la ligne `De reprendre les contrats de travail de` est incomplete et ne peut pas etre rendue automatiquement.

Decision requise :
- supprimer explicitement la ligne dans la version codee ;
- ou fournir le wording complet et ses variables.

### 6.6 Variantes de nombre de salaries dans l'acte dentaire

Blocage :
- l'acte dentaire source vise deux salaries nommes ;
- le modele V1 est repetable, mais le wording pour zero, un ou plus de deux salaries n'est pas source.

Decision requise :
- limiter le rendu automatique a deux salaries fournis ;
- ou fournir un wording validant les autres nombres ;
- ou laisser la clause hors generation.

## 7. Synthese de classement

### Tranche

- quatre documents canoniques distincts ;
- selection par `dossier.cession.etape` explicite ;
- separation stricte medical / dentaire ;
- eligibilite SELARL / SELAS sous reserve d'absence de residu non parametre ;
- mapping des roles vendeur / acquereur par contexte de clause ;
- credit-vendeur conditionnel uniquement sur acte medical ;
- taux fixe `5 %` conserve pour le compromis dentaire ;
- trois exercices rendus depuis `cession.exercices[]` ;
- signatures rendues selon le mode source du document.

### A laisser manuel en V1

- origine de propriete detaillee ;
- bail et activite autorisee ;
- prix, repartition et conditions financieres variables ;
- activation et contenu du credit-vendeur ;
- salaries repris ;
- clause SCM ;
- signatures, mentions manuscrites, pages, exemplaires variables ;
- annexes detaillees.

### Reellement bloquant

- mentions dentaires dans des sources medicales ;
- role incoherent dans l'origine de propriete du compromis medical ;
- titre anormal `[date_origine_propriete] PREVUE DE REALISATION` ;
- placeholders vendeur/acquereur ambigus hors contexte clair ;
- ligne incomplete de reprise des contrats de travail dans l'acte medical ;
- wording non source pour un nombre de salaries dentaire different de deux.

## 8. Critere avant futur code

Un futur ticket de code peut demarrer si le generateur respecte les decisions tranchees et bloque explicitement les points reellement bloquants ci-dessus.

Le code ne doit pas corriger le wording juridique. Toute correction textuelle medicale, dentaire, salarie ou SCM doit etre fournie par une validation metier explicite avant implementation.
