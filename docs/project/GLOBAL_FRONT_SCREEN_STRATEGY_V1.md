# Strategie d'ecrans front global V1

Ticket : `GLOBAL-FRONT-ARCHITECTURE-001`

Statut : strategie globale, sans maquette detaillee et sans modification Streamlit.

## Intention

Le futur front doit guider un juriste ou un operateur par dossier complet, tout en gardant un mode de test document unitaire separe pour diagnostiquer le moteur.

L'entree se fait par type d'operation et famille documentaire, pas par liste brute de placeholders.

## Parcours dossier complet

### 1. Qualification et operation

Objectif : determiner le cadre metier avant toute saisie fine.

Contenu :

- famille : SEL, SPFPL, SCM, SCI, SAS, cession, apport, bail, regime communautaire, ordre ;
- structure : `SELARL`, `SELAS`, `SPFPL cession`, `SPFPL apport`, `SCS`, `SCI`, `SCI IRIS`, `SCM`, `SAS` ;
- profession : medecin, chirurgien-dentiste ou autre profession si source disponible ;
- type d'operation : creation, cession, apport, transformation, cession SCM, cession cabinet ;
- options dossier : unipersonnel, regime communautaire, SCM, site distinct, bail, financement, derogation.

Sortie :

- liste provisoire des documents attendus ;
- blocs de saisie actifs ;
- reutilisations possibles mais non appliquees sans regle.

### 2. Fiche personne

Objectif : saisir les personnes physiques une seule fois.

Contenu :

- fiche client / praticien ;
- autres associes personnes physiques ;
- conjoint ;
- mandataire ;
- signataire documentaire si distinct ;
- representant d'une personne morale ;
- vendeur, cedant, bailleur ou locataire personne physique si distinct.

Le bloc doit exposer les roles assignes a chaque personne, par exemple : praticien, associe unique, gerant, signataire.

### 3. Fiche societe

Objectif : creer les organisations rolees du dossier.

Contenu :

- societe principale en constitution ;
- SPFPL ;
- SCM ;
- SCM cedee ;
- societe cible ;
- societe associee personne morale ;
- banque ;
- conseil de l'ordre ;
- administration ou service d'enregistrement.

Le front doit afficher la societe principale comme objet central, mais ne doit pas assimiler toutes les societes du dossier a cette societe.

### 4. Blocs de parties

Objectif : relier les fiches aux roles contractuels ou documentaires.

Blocs possibles :

- associes et repartition ;
- gouvernance : gerant, president, representant ;
- signataires ;
- mandataires ;
- cession cabinet : vendeur, acquereur, representant acquereur ;
- cession SCM : cedant, SCM cedee, cessionnaire, representant ;
- bail : bailleur, locataire ;
- regime communautaire : conjoint ;
- SPFPL : cedant, apporteur, societe cible, associes cible, commissaire ou evaluateur.

Ce bloc doit montrer les reutilisations actives et les roles distincts.

### 5. Blocs d'adresses

Objectif : collecter les lieux une seule fois par usage.

Adresses pivot :

- domicile du praticien ;
- lieu d'exercice principal / cabinet ;
- siege social de la societe principale.

Adresses complementaires :

- domiciliation, derivee du siege ;
- SCM standard ;
- SCM cedee ;
- cessionnaire SCM ;
- locaux loues ;
- adresse du conseil de l'ordre ;
- banque ;
- tiers fiscal ou administratif.

Le front doit proposer les options de reutilisation connues : siege = lieu d'exercice, SCM = lieu d'exercice, domiciliation = siege.

### 6. Ordre et identifiants

Objectif : isoler les donnees ordinales et professionnelles.

Contenu :

- profession reglementee ;
- numero RPPS ;
- numero d'ordre ;
- departement ou ville ordinale ;
- conseil de l'ordre destinataire ;
- adresse ordinale ;
- inscrit concerne : personne physique, societe ou autre selon arbitrage futur.

Point ouvert : le modele final `ordre` par inscrit reste a arbitrer en interne.

### 7. Capital, titres et apports

Objectif : saisir les donnees financieres structurelles sans les confondre avec les prix de cession.

Contenu :

- capital social ;
- nombre total de parts ou actions ;
- valeur nominale ;
- repartition par associe ;
- apports en numeraire ;
- apports en nature ;
- droits financiers et droits de vote si necessaire ;
- actions de preference pour cas futur.

Point ouvert : calculs proposes, overrides et actions de preference doivent etre traites prudemment.

### 8. Financement

Objectif : isoler les donnees de banque et de pret.

Contenu :

- banque de depot ;
- adresse banque ;
- emprunt ou montant maximum ;
- pret pour cession ;
- credit-vendeur ;
- date ou conditions de financement si source documentee.

Les banques et tiers constants peuvent relever du parametrage cabinet/SYDEL avec override dossier.

### 9. Bail

Objectif : gerer le bail comme une famille de parties et de dates distincte.

Contenu :

- bailleur ;
- locataire ;
- date du bail ;
- dates d'effet ;
- locaux loues ;
- loyer, superficie, duree si le document le demande ;
- champ libre ou override pour le paragraphe locataire si la SCM rend le cas non standard.

Le locataire ne doit pas etre force a la SELARL en constitution.

### 10. Cession

Objectif : couvrir les cessions de cabinet, fonds liberal, parts, actions et parts SCM.

Contenu :

- type de cession : cabinet medical, cabinet dentaire, parts SCM, parts SPFPL, actions ;
- vendeur / cedant ;
- acquereur / cessionnaire ;
- representant ;
- cabinet ou fonds ;
- origine de propriete ;
- prix total, prix unitaire, composantes corporelles/incorporelles ;
- plage de parts ou actions ;
- conditions de financement ;
- salaries si cession dentaire.

Le parcours SELARL standard peut proposer praticien = vendeur/cedant et SEL = acquereur/cessionnaire, mais seulement via regles explicites.

### 11. SCM

Objectif : distinguer la SCM comme structure, la SCM cedee et les satellites SCM.

Contenu :

- SCM du dossier ;
- SCM cedee ;
- cessionnaire SCM ;
- associes SCM avant et apres cession ;
- parts cedees ;
- prix ;
- pacte, frais communs, reglement interieur, liste des depenses selon documents attendus.

L'adresse de la SCM standard peut etre liee au lieu d'exercice ; l'adresse SCM cedee et celle du cessionnaire restent distinctes par defaut.

### 12. SPFPL

Objectif : isoler les operations SPFPL sans les confondre avec SELAS ou micro-holding.

Contenu :

- type : cession ou apport ;
- societe SPFPL ;
- societe cible ;
- cedant ou apporteur ;
- associes cible ;
- parts ou actions ;
- commissaire aux apports ;
- evaluateur ;
- operation titres ;
- documents satellites attendus.

Le cas SELAS medecin avec micro-holding est hors perimetre immediat.

### 13. Documents attendus

Objectif : rendre visible la selection documentaire avant generation.

Contenu :

- documents attendus par cas ;
- statut : generable, manuel, non implemente, reserve, contexte incomplet ;
- champs manquants ;
- pieces manquantes ;
- raison d'exclusion ;
- lien vers test unitaire si utile ;
- avertissement si un document est manuel.

La liste doit venir du catalogue metier et du futur data layer, pas d'une liste de widgets.

### 14. Generation

Objectif : produire les sorties uniquement pour les documents generables et prets.

Actions :

- generer DOCX dossier ;
- produire PDF si backend disponible ;
- produire ZIP dossier ;
- telecharger les sorties ;
- afficher le manifeste et les erreurs ;
- conserver les documents manuels dans la checklist.

La generation ne vaut pas validation juridique.

## Mode document unitaire / test unitaire

Le mode document unitaire doit rester separe du parcours dossier complet.

Usage :

- tester un generateur `DOC-XXX` ;
- verifier les champs requis d'un document ;
- reproduire un bug ;
- diagnostiquer DOCX/PDF/ZIP ;
- construire un contexte minimal.

Non-usage :

- ne pas representer le parcours utilisateur principal ;
- ne pas remplacer le dossier complet ;
- ne pas prendre des decisions de reutilisation globale ;
- ne pas masquer les autres documents attendus.

## Difference dossier complet vs document unique

| Sujet | Parcours dossier complet | Mode document unitaire |
|---|---|---|
| Entree | operation, structure, options | code document |
| Source de donnees | fiches metier et roles | contexte minimal |
| Documents | liste attendue complete | un document choisi |
| Reutilisations | regles dossier visibles | valeurs directes ou prefill de test |
| Validation | dossier, documents, pieces, roles | champs requis du document |
| Sortie | DOCX/PDF/ZIP dossier | DOCX/PDF/ZIP local de test |
| Statut produit | parcours cible | outil de diagnostic |

## Ce que le prototype peut inspirer

Concepts a garder pour plus tard :

- separation entre Assistant metier, Document unitaire et Technique / diagnostic ;
- tableau des documents attendus avec statuts ;
- prefill de test explicite ;
- telechargements DOCX/PDF/ZIP ;
- mode technique YAML/JSON pour diagnostiquer le moteur.

Concepts a ne pas reprendre comme architecture :

- listes de champs codees pour un parcours SELARL ;
- dependance au `session_state` comme modele de donnees ;
- ecrans Streamlit actuels ;
- logique de reutilisation encodee dans les widgets ;
- generalisation depuis les cas SCI/SELARL du prototype.
