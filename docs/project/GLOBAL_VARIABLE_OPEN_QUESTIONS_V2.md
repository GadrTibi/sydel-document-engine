# Questions humaines ouvertes - variables globales V2

Statut : version courte apres integration des reponses humaines disponibles.

Objectif : retirer les questions fermees par la reponse d'Albane et ne conserver que les arbitrages internes ou les sujets a remettre en backlog documentaire. Aucune relance client n'est requise pour figer le registre canonique global V2.1.

## Synthese

- Questions V1 initiales : 10.
- Questions fermees par arbitrage humain : 4.
- Questions encore ouvertes mais arbitrables en interne : 5.
- Question basculee en backlog documentaire futur : 1.

## A. Questions resolues

### A-001 - Roles personne et non-fusion silencieuse

Questions V1 fermees : Q-001.

Decision V2.1 : une fiche personne peut alimenter plusieurs roles, mais les roles restent explicites. `Praticien`, `associe`, `gerant`, `signataire`, `mandataire`, `vendeur`, `cedant`, `acquereur`, `cessionnaire`, `bailleur` et `locataire` ne fusionnent jamais par proximite de libelle.

Regle retenue : reutilisation seulement via option ou contexte documente, par exemple `Dossier unipersonnel` pour Praticien = associe unique = gerant = signataire.

### A-002 - Adresses pivots du dossier SEL

Questions V1 fermees : Q-002.

Decision V2.1 : trois adresses pivots sont retenues pour l'architecture front :

- adresse de domicile du praticien ;
- adresse du lieu d'exercice / cabinet ;
- adresse du siege social.

Regle retenue : les formes affichees peuvent etre derivees depuis des composants, mais chaque adresse reste typee par role.

### A-003 - Domiciliation et siege social

Questions V1 fermees : Q-003.

Decision V2.1 : la domiciliation correspond au siege social. Elle ne doit pas devenir une quatrieme adresse concurrente dans le front global.

Regle retenue : le siege social peut etre le domicile, le lieu d'exercice ou une adresse manuelle, mais ce choix doit etre explicite.

### A-004 - Parties de cession SELARL / SCM / fonds liberal

Questions V1 fermees : Q-004.

Decision V2.1 : dans le parcours SELARL standard, le vendeur ou cedant du fonds liberal ou des parts de SCM est le praticien personne physique exercant en BNC. L'acquereur ou cessionnaire est la SEL en cours de constitution.

Regle retenue : les roles restent distincts dans le schema, meme lorsqu'ils pointent vers la meme fiche personne ou societe.

## B. Questions encore ouvertes mais a arbitrer en interne

### B-001 - Ordre professionnel et identifiants

Question V1 concernee : Q-005.

Reste a arbitrer : modele final `ordre` par inscrit, notamment personne physique, societe inscrite, departement ordinal, numero RPPS et numero d'ordre. Aucun besoin de relance client avant architecture front.

### B-002 - Capital, titres, apports et prix

Question V1 concernee : Q-006.

Reste a arbitrer : niveau de calcul propose par le front, gestion des overrides, distinction parts/actions et cas d'actions de preference. Le modele SELAS + micro-holding confirme que ce sujet doit rester prudent.

### B-003 - Signataire, mandataire et representant

Question V1 concernee : Q-007.

Reste a arbitrer : signataire par document, mandataire de formalites et representant de personne morale. Albane confirme l'existence de representants pour les personnes morales, mais ne valide pas une fusion mandataire/signataire.

### B-004 - Dates homonymes

Question V1 concernee : Q-008.

Reste a arbitrer : prefill eventuel depuis une date dossier tout en conservant les dates juridiques distinctes : signature, decision, PV, bail, effet, jouissance, limite de realisation.

### B-005 - Champs tiers et constantes locales

Question V1 concernee : Q-010.

Reste a arbitrer : separation entre champs dossier et parametrage cabinet/SYDEL pour banque, depot des fonds, impots, service d'enregistrement et prestataire de signature electronique.

## C. Backlog documentaire futur

### C-001 - Variables spec-only et template-only

Question V1 concernee : Q-009.

Decision V2.1 : ne pas integrer massivement ces champs au front global. Les traiter par famille documentaire lors des tickets de reconstruction ou de revue.

### C-002 - SELAS medecin avec associe personne morale micro-holding

Source : `project/source_truth/modele Statuts SELAS avec MH.docx`.

Decision V2.1 : cas futur hors perimetre SELARL standard. Il necessite un ticket separe avant toute implementation ou extension UI.

### C-003 - Bail et locataire selon presence d'une SCM

Decision V2.1 : Albane signale que le paragraphe locataire varie selon la presence d'une SCM et pourrait rester en champ libre. Ce point doit revenir dans un ticket documentaire bail/cession, pas dans le gel du registre global.
