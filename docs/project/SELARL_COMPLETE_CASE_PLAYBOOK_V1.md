# SELARL complete case playbook V1

Ticket source : `SELARL-COMPLETE-CASE-PLAYBOOK-001`

Date : 2026-05-25

## Objectif

Ce document fige la cible "SELARL complete" avant de coder la suite.

Le besoin utilisateur est clair : ne plus rester sur un test limite a quatre
documents, mais obtenir une forme SELARL finale, propre, et reproductible pour
les autres cas.

La reponse technique doit rester conforme aux garde-fous du projet :

- ne pas modifier les generateurs sans ticket documentaire dedie ;
- ne pas modifier le moteur DOCX/PDF/ZIP ;
- ne pas inventer un wording juridique ;
- ne pas envoyer en generation les documents marques manuels dans la source ;
- avancer par adaptateur front, readiness, smoke et revue humaine.

## Realite actuelle

### Ce que le moteur sait deja generer

Le registre moteur contient deja les generateurs SELARL suivants :

| Bloc | Documents moteur |
| --- | --- |
| Commun | `DOC-001`, `DOC-002`, `DOC-003` |
| SELARL base | `DOC-004`, `DOC-034` |
| Statuts SELARL | `DOC-016`, `DOC-017` |
| Regime communautaire | `DOC-005`, `DOC-006` |
| Bail et financement | `DOC-007`, `DOC-008` |
| Cession cabinet medical | `DOC-009`, `DOC-010` |
| Cession cabinet dentaire | `DOC-011`, `DOC-012` |
| SCM cession | `DOC-031`, `DOC-032`, `DOC-033` |
| Derogations moteur | `DOC-013`, `DOC-014` existent cote moteur mais restent manuels dans le flux SELARL verifie |

Conclusion : le blocage n'est pas un manque global du moteur. Le moteur est
plus avance que la surface utilisateur actuelle.

### Ce que le nouveau front genere vraiment

Le nouveau front global reste volontairement limite au profil :

`SELARL creation simple`

Les actions de generation visibles utilisent actuellement :

```text
FRONT_GENERATION_SUPPORTED_DOC_CODES = DOC-001, DOC-002, DOC-003, DOC-004
FRONT_GENERATION_CONDITIONAL_DOC_CODES = DOC-005, DOC-006
FRONT_GENERATION_EXCLUDED_DOC_CODES = DOC-013, DOC-014
```

Le mode document unitaire V1 est lui aussi limite a :

```text
UNIT_DOCUMENT_V1_SUPPORTED_CODES = DOC-001, DOC-002, DOC-003, DOC-004
```

Le wizard historique garde le meme plafond fonctionnel :

```text
BUSINESS_WIZARD_CONTEXT_READY_DOCUMENT_IDS = DOC-001, DOC-002, DOC-003, DOC-004
```

Donc l'utilisateur a raison : aujourd'hui, depuis le parcours visible, on est
encore sur un pilote quatre documents. Le reste peut etre connu du catalogue ou
du moteur, mais n'est pas branche proprement dans la generation front.

## Definition de "SELARL complete"

Une SELARL complete ne veut pas dire "generer tout ce qui a un generateur".
Cela veut dire :

1. afficher un parcours unique, simple et lisible ;
2. demander toutes les donnees necessaires au dossier SELARL choisi ;
3. calculer les documents attendus selon les conditions du dossier ;
4. generer les documents autorises par la source et suffisamment mappes ;
5. afficher les documents manuels comme manuels, sans les envoyer au moteur ;
6. sortir DOCX puis ZIP, et PDF seulement si le backend local est disponible ;
7. produire des blocages explicites si un document attendu n'est pas pret.

La surface principale cible reste strictement :

1. Type de dossier
2. Donnees a saisir
3. Generation

Tout debug, tableau technique, mapping, statut interne ou mode unitaire doit
rester cache dans un mode equipe.

## Parcours SELARL final cible

La saisie SELARL doit suivre ce fil metier, meme si l'UI visible reste compacte :

| Ordre | Etape metier | Role |
| --- | --- | --- |
| 1 | Qualification | Profession, dossier unipersonnel, regime communautaire, site distinct, SCM cession, derogation, cession, type de cabinet |
| 2 | Fiche Client / Praticien | Identite, naissance, nationalite, filiation, adresse personnelle, fonction |
| 3 | Fiche Societe | Denomination, forme, capital, RCS, siege, domiciliation |
| 4 | Capital et Associes | Associe unique ou liste, parts, valeur nominale, dirigeant nomme, decision |
| 5 | Scenarios metier | Ordre, mandataire, conjoint, bail, cession, financement, SCM, signature |
| 6 | Generation | Documents prets, documents bloques, documents manuels, DOCX, ZIP, PDF si disponible |

Le front peut grouper visuellement les champs pour rester simple, mais le
modele de donnees doit garder ces blocs distincts.

## Matrice SELARL complete

| Condition | Document | Code | Statut source SELARL | Statut moteur | Statut front actuel | Decision finale |
| --- | --- | --- | --- | --- | --- | --- |
| Tous dossiers | Declaration non-condamnation | `DOC-001` | Generable | Branche | Branche | Garder dans le pack de base |
| Tous dossiers | Autorisation domiciliation | `DOC-002` | Generable | Branche | Branche | Garder dans le pack de base |
| Tous dossiers | Procuration | `DOC-003` | Generable | Branche | Branche | Garder dans le pack de base |
| SELARL base | PV nomination gerant | `DOC-004` | Generable | Branche | Branche | Garder dans le pack de base |
| SELARL base | Demande inscription ordre | `DOC-034` | Generable | Branche | Non branche front generation | A brancher dans adaptateur SELARL complet |
| Chirurgien-dentiste | Statuts SELARL chirurgien-dentiste | `DOC-016` | Generable | Branche | Non branche front generation | A brancher si profession dentiste |
| Medecin | Statuts SELARL medecin | `DOC-017` | Generable | Branche | Non branche front generation | A brancher si profession medecin |
| Site distinct | Formulaire site distinct CD94 avec la SEL | Aucun code | Manuel | Hors moteur | Non branche | Afficher manuel seulement |
| SCM cession | PV AGE cession part SCM | `DOC-031` | Generable | Branche | Non branche front generation | A brancher si SCM cession |
| SCM cession | Courrier SDE cession SCM | `DOC-032` | Generable | Branche | Non branche front generation | A brancher si SCM cession |
| SCM cession | Acte cession parts SCM vers SELARL | `DOC-033` | Generable | Branche | Non branche front generation | A brancher si SCM cession |
| Regime communautaire | Lettre renonciation associe | `DOC-005` | Generable | Branche | Non branche front generation | A brancher si regime communautaire |
| Regime communautaire | Lettre avertissement conjoint | `DOC-006` | Generable | Branche | Genere si regime communautaire | A produire avec `DOC-005` |
| Derogation | Formulaire multi-sites SEL | `DOC-013` | Manuel pour pilote SELARL | Branche moteur | Exclu front generation | Rester manuel sans arbitrage |
| Derogation | Derogation SEL BNC | Aucun code | Manuel | Hors moteur | Non branche | Rester manuel |
| Derogation | Demande derogation cumul SELARL BNC | `DOC-014` | Manuel | Branche moteur | Exclu front generation | Rester manuel sans arbitrage |
| Cession | Avenant contrat de bail | `DOC-007` | Generable | Branche | Non branche front generation | A brancher si cession |
| Cession | Appel de fonds SEL | `DOC-008` | Generable | Branche | Non branche front generation | A brancher si cession |
| Cabinet medical | Acte cession cabinet medical | `DOC-009` | Generable | Branche | Non branche front generation | A brancher si cession medicale |
| Cabinet medical | Compromis cession cabinet medical | `DOC-010` | Generable | Branche | Non branche front generation | A brancher si cession medicale |
| Cabinet dentaire | Acte cession cabinet dentaire | `DOC-011` | Generable | Branche | Non branche front generation | A brancher si cession dentaire |
| Cabinet dentaire | Compromis cession cabinet dentaire | `DOC-012` | Generable | Branche | Non branche front generation | A brancher si cession dentaire |
| Emprunt PV | Autorisation emprunt | Aucun code autonome | Branche du `DOC-004` | Dans contexte PV | Non document separe | Ne jamais afficher comme document distinct |

## Garde-fous non negociables

### Documents manuels

Les documents suivants ne doivent pas entrer dans la generation automatique
SELARL sans arbitrage explicite :

- formulaire site distinct CD94 sans code moteur ;
- `DOC-013` formulaire multi-sites SEL ;
- Derogation SEL BNC sans code moteur ;
- `DOC-014` demande derogation cumul SELARL BNC.

Meme si `DOC-013` et `DOC-014` existent cote moteur, la source SELARL verifiee
les maintient hors generation pilote.

### `DOC-006` regime communautaire

Correction 2026-06-01 : l'ancienne reserve `DOC-006` est levee. La source DOCX
Lot 2 existe et le batch regime communautaire couvre les deux lettres. Le front
doit donc generer `DOC-005` et `DOC-006` quand le regime communautaire est actif.

Il ne doit pas generer `DOC-006` hors regime communautaire.

### Reutilisations explicites

Les reutilisations suivantes restent opt-in :

- Praticien = associe unique = gerant = signataire seulement si
  `Dossier unipersonnel` est actif ;
- siege social = domiciliation seulement si la regle est active ;
- SELARL en creation = acquereur cabinet seulement si l'utilisateur le choisit ;
- SELARL en creation = cessionnaire SCM seulement si l'utilisateur le choisit ;
- signataire = mandataire ordre seulement si l'utilisateur le choisit.

Aucune relation vendeur, locataire, cabinet, lieu d'exercice, SCM ou mandataire
ne doit etre deduite silencieusement.

## Strategie de simplification UX

La forme finale ne doit pas ajouter une grande table visible de documents.

Dans la vue principale :

- bloc `Type de dossier` : choix SELARL et conditions essentielles ;
- bloc `Donnees a saisir` : formulaire guide par blocs, avec champs manquants
  seulement quand ils bloquent ;
- bloc `Generation` : bouton DOCX, bouton ZIP apres DOCX, PDF si disponible,
  et trois listes courtes : prets, bloques, manuels.

Dans le debug cache :

- matrice documents ;
- details des champs canoniques ;
- details du `DocumentGenerationContext` ;
- diagnostics de readiness ;
- statut par lot ;
- liens vers les artefacts.

## Prochain ticket unique recommande

### `SELARL-COMPLETE-CONTEXT-ADAPTER-001`

Objectif : etendre le nouveau front SELARL depuis le pilote quatre documents
vers un adaptateur de contexte complet, sans modifier les generateurs ni le
moteur DOCX/PDF/ZIP.

Perimetre :

- remplacer la constante de generation front limitee a `DOC-001` a `DOC-004`
  par une selection SELARL conditionnelle issue du catalogue ;
- construire un `DocumentGenerationContext` complet pour les familles deja
  generables cote moteur ;
- ajouter les requirements front manquants pour `DOC-005` a `DOC-012`,
  `DOC-016`, `DOC-017`, `DOC-031`, `DOC-032`, `DOC-033`, `DOC-034` ;
- garder `DOC-013`, `DOC-014` et les documents sans code en manuel ;
- generer `DOC-006` uniquement si le regime communautaire est actif ;
- ne pas changer le texte juridique ;
- ne pas modifier les generateurs.

Livrables attendus :

- tests unitaires de selection documentaire par scenario SELARL ;
- tests unitaires de readiness par document ;
- tests d'adaptateur contexte pour au moins six scenarios ;
- rapport court listant documents prets, reserves, manuels et bloques.

Scenarios minimum :

- SELARL medecin simple ;
- SELARL chirurgien-dentiste simple ;
- SELARL avec regime communautaire ;
- SELARL avec cession cabinet medical ;
- SELARL avec cession cabinet dentaire ;
- SELARL avec SCM cession ;
- SELARL avec derogation, en verifiant que les documents restent manuels.

## Sequence complete apres ce ticket

1. `SELARL-COMPLETE-CONTEXT-ADAPTER-001` : adaptateur et readiness complete.
2. `SELARL-COMPLETE-UI-SURFACE-001` : rendre la surface finale sans bruit.
3. `SELARL-COMPLETE-SMOKE-001` : generer les packs DOCX/ZIP par scenario.
4. `SELARL-COMPLETE-JURIST-REVIEW-001` : revue humaine des rendus.
5. `REPLICATION-NEXT-CASE-001` : appliquer la recette au cas suivant.

## Mode d'emploi pour reproduire sur les autres cas

La methode SELARL devient la recette standard.

### 1. Figer la source

Pour chaque cas :

- identifier la source de verite ;
- lister les arbitrages humains superieurs a la source brute ;
- documenter les contradictions ;
- classer chaque document en generable, reserve, manuel, non implemente.

### 2. Construire la matrice documentaire

La matrice doit contenir :

- condition d'apparition ;
- libelle utilisateur ;
- code `DOC-XXX` ou absence de code ;
- statut source ;
- statut moteur ;
- statut front ;
- decision finale.

Aucun ticket d'UI ne doit demarrer sans cette matrice.

### 3. Construire le schema de saisie

Le formulaire doit partir du processus, pas des generateurs.

Pour chaque champ :

- label utilisateur qualifie ;
- chemin canonique ;
- bloc metier ;
- condition d'affichage ;
- document consommateur ;
- regle de reutilisation eventuelle.

### 4. Definir les reutilisations

Toute reutilisation doit etre explicite :

- source ;
- cible ;
- option visible ou regle conditionnelle ;
- conflit possible ;
- consequence sur les documents.

Pas de fusion silencieuse de roles, personnes ou adresses.

### 5. Brancher l'adaptateur contexte

Le front doit transformer le dossier saisi en contexte moteur complet.

Le ticket doit rester limite a l'adaptateur et aux tests, sauf si une
spec documentaire autorise explicitement une modification de generateur.

### 6. Brancher la readiness

Chaque document attendu doit etre dans un des statuts suivants :

- pret ;
- bloque par donnees manquantes ;
- reserve ;
- manuel ;
- non implemente ;
- contexte incomplet.

Le bouton de generation ne doit jamais etre la premiere source de verite du
blocage. Le front doit expliquer le blocage avant l'appel moteur.

### 7. Garder une surface utilisateur minimale

Le premier ecran utilisateur doit rester :

1. type de dossier ;
2. donnees a saisir ;
3. generation.

Les tableaux et diagnostics vivent uniquement dans le mode equipe.

### 8. Smoke complet avant generalisation

Pour chaque cas, generer au minimum :

- le scenario simple ;
- chaque condition documentaire majeure ;
- un scenario mixte realiste ;
- le ZIP du dossier ;
- le PDF seulement si le backend est disponible.

### 9. Revue humaine

Un cas ne devient "final" qu'apres revue humaine des rendus.

Avant cette revue, l'etat correct est :

`candidat final technique`

et non :

`final juridiquement valide`

## Definition of done SELARL complete

La SELARL sera consideree complete quand :

- le front selectionne tous les documents attendus selon les conditions ;
- les documents moteur autorises sont generables depuis le parcours principal ;
- les documents manuels sont visibles comme manuels et exclus du moteur ;
- `DOC-006` est gere comme document conditionnel du regime communautaire ;
- DOCX et ZIP sortent pour tous les scenarios de smoke ;
- les blocages sont comprehensibles sans debug ;
- la surface principale reste limitee a type de dossier, saisie, generation ;
- les rendus ont ete revus humainement.

