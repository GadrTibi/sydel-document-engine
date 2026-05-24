# Modele d'objets front global V1

Ticket : `GLOBAL-FRONT-ARCHITECTURE-001`

Statut : modele conceptuel, sans code Python.

## Vue d'ensemble

Le modele front global repose sur des fiches metier reutilisables et des roles explicites. Il doit eviter deux erreurs symetriques :

- redemander la meme donnee dans chaque document ;
- fusionner trop tot des roles juridiquement distincts.

## Person

### Role metier

Une `Person` represente une personne physique connue du dossier. Elle n'est pas un role par elle-meme.

### Champs principaux

- identifiant interne ;
- civilite d'affichage ;
- genre grammatical ;
- prenom ;
- nom ;
- date de naissance ;
- ville, departement ou pays de naissance ;
- nationalite ;
- profession ;
- fonction ;
- identifiants professionnels : RPPS, numero d'ordre, departement ordinal ;
- situation matrimoniale ;
- adresse personnelle principale ;
- contacts utiles si le front les integre plus tard.

### Relations

- peut porter plusieurs `RoleAssignment` ;
- peut posseder une ou plusieurs `Address` typees ;
- peut representer une `Organization` via un role de representant ;
- peut etre liee a un conjoint ;
- peut etre source ou cible d'une `ReuseRule`.

### Exemples

- le praticien client ;
- le gerant ;
- l'associe unique ;
- le signataire d'un document ;
- le mandataire des formalites ;
- le cedant des parts SCM ;
- le representant d'une societe civile micro-holding future.

### Risques de confusion

- confondre praticien et associe sans option ;
- confondre signataire et mandataire ;
- confondre gerant, president et representant ;
- deduire le genre depuis la civilite sans validation ;
- reutiliser le domicile du praticien comme siege sans regle explicite.

## Organization / Company

### Role metier

Une `Organization` represente une personne morale, une societe en constitution ou un tiers institutionnel.

### Champs principaux

- identifiant interne ;
- denomination ;
- forme sociale ;
- statut : en constitution, existante, tierce, administration, ordre, banque ;
- capital social ;
- RCS : numero et ville ;
- SIREN / SIRET si disponible ;
- profession ou ordre concerne si applicable ;
- siege social ;
- representant personne physique ;
- attributs specifiques selon famille : SCM, SPFPL, SEL, micro-holding, banque, conseil de l'ordre.

### Relations

- peut porter plusieurs `RoleAssignment` ;
- possede une ou plusieurs `Address` ;
- peut avoir des `Person` associees, dirigeants, representants ou signataires ;
- peut etre partie a une cession, un bail, un apport ou un depot de capital ;
- peut etre rattachee a des `DocumentRequirement`.

### Exemples

- SELARL en constitution ;
- SELAS ;
- SCM cedee ;
- SCM cessionnaire si distincte ;
- SPFPL ;
- societe cible ;
- banque de depot ;
- conseil de l'ordre ;
- societe civile micro-holding future.

### Risques de confusion

- confondre societe principale et societe cible ;
- confondre SCM standard et SCM cedee ;
- confondre SEL en constitution et SPFPL ;
- traiter une micro-holding comme une SPFPL sans ticket dedie ;
- reutiliser le siege d'une societe pour une autre par proximite de nom.

## Address

### Role metier

Une `Address` represente un lieu type par usage. Elle peut etre composee et/ou affichee.

### Champs principaux

- identifiant interne ;
- usage : domicile, siege, lieu d'exercice, cabinet, locaux loues, SCM, ordre, banque, fiscalite ;
- numero de voie ;
- voie ;
- complement ;
- code postal ;
- ville ;
- pays ;
- adresse affichee ;
- mode de production : saisie composee, saisie libre, derivee, importee ;
- source de reutilisation si derivee.

### Relations

- appartient a une `Person`, une `Organization` ou un usage de dossier ;
- peut etre source ou cible d'une `ReuseRule` ;
- peut etre consommee par un `DocumentRequirement` ;
- peut produire des formes affichees via une `FieldDefinition`.

### Exemples

- domicile du praticien ;
- lieu d'exercice principal ;
- siege de la SEL en constitution ;
- adresse de domiciliation ;
- adresse de la SCM cedee ;
- adresse du cessionnaire SCM ;
- adresse du conseil de l'ordre ;
- adresse de la banque.

### Risques de confusion

- transformer la domiciliation en quatrieme adresse concurrente alors qu'elle correspond au siege social ;
- imposer siege = lieu d'exercice sans option ;
- confondre adresse des locaux loues et adresse du cabinet ;
- confondre adresse vendeur et adresse exercice vendeur ;
- perdre les composants en ne stockant qu'une forme libre.

## RoleAssignment

### Role metier

Un `RoleAssignment` est le lien explicite entre une fiche et son role juridique ou documentaire.

### Champs principaux

- identifiant interne ;
- role canonique ;
- scope : dossier, operation, document, lot ;
- cible : `Person` ou `Organization` ;
- statut : confirme, propose, derive, override, a verifier ;
- source de la regle ;
- documents impactes ;
- notes de revue.

### Relations

- pointe vers une `Person` ou une `Organization` ;
- peut etre cree par une `ReuseRule` ;
- peut generer des `ValidationIssue` ;
- est consomme par des `DocumentRequirement`.

### Exemples

- praticien du dossier ;
- associe unique ;
- gerant ;
- signataire de la procuration ;
- mandataire ;
- vendeur du fonds liberal ;
- acquereur du cabinet ;
- cessionnaire des parts SCM ;
- bailleur ;
- locataire ;
- representant d'une personne morale.

### Risques de confusion

- croire que deux roles ayant la meme fiche cible sont fusionnes ;
- oublier qu'un document peut avoir son propre signataire ;
- rendre le mandataire identique au signataire par defaut ;
- appliquer un role global alors que le document exige un role local.

## Dossier / Matter / Operation

### Role metier

Le `Dossier` porte le contexte operationnel et pilote les documents attendus.

### Champs principaux

- identifiant dossier ;
- type d'operation ;
- structure cible ;
- profession ;
- options metier ;
- etape du dossier ;
- fiches personnes, societes et adresses ;
- documents attendus ;
- regles de reutilisation actives ;
- validations et pieces.

### Relations

- contient `DocumentRequirement[]` ;
- reference `Person[]`, `Organization[]`, `Address[]` ;
- active `ReuseRule[]` ;
- consolide `ValidationIssue[]` ;
- rattache `SupportingEvidence[]`.

### Exemples

- creation SELARL medecin unipersonnelle ;
- creation SELARL chirurgien-dentiste avec regime communautaire ;
- cession de cabinet medical vers SEL ;
- cession de parts SCM vers SEL ;
- operation SPFPL cession ;
- constitution SCI.

### Risques de confusion

- utiliser le lot documentaire comme type de dossier ;
- utiliser un document unitaire comme dossier complet ;
- confondre option de selection documentaire et champ juridique ;
- changer la profession apres saisie sans invalider les documents impactes.

## DocumentRequirement

### Role metier

Un `DocumentRequirement` represente un document attendu dans un dossier donne.

### Champs principaux

- code `DOC-XXX` si disponible ;
- libelle canonique ;
- libelle source ;
- famille ;
- lot ;
- statut : generable, manuel, non implemente, reserve, contexte incomplet ;
- conditions d'apparition ;
- champs requis ;
- champs optionnels ;
- pieces utiles ;
- erreurs bloquantes ;
- mode de generation cible : dossier complet ou test unitaire.

### Relations

- appartient a un `Dossier` ;
- consomme des `FieldDefinition` ;
- consomme des `RoleAssignment` ;
- produit ou reference des `ValidationIssue` ;
- peut exiger des `SupportingEvidence`.

### Exemples

- `DOC-001` declaration de non-condamnation ;
- `DOC-034` demande d'inscription a l'ordre ;
- `DOC-007` avenant au bail ;
- formulaire de derogation a completer a la main ;
- document non implemente ou hors perimetre.

### Risques de confusion

- afficher un document manuel comme generable ;
- masquer un document attendu parce qu'il n'est pas automatisable ;
- confondre document attendu et document pret a generer ;
- creer un contexte incomplet silencieux.

## FieldDefinition

### Role metier

Une `FieldDefinition` decrit un champ canonique utilisable par le front.

### Champs principaux

- chemin canonique ;
- libelle front ;
- description metier ;
- type ;
- role ou owner ;
- cardinalite ;
- forme : composant, affichee, calculee, libre ;
- statut de stabilite ;
- relation matrix : `SAME_FIELD`, `SAME_DATA_DIFFERENT_SHAPE`, `EXPLICIT_REUSE_ONLY`, `DISTINCT_FIELDS`, `UNCERTAIN_REQUIRES_HUMAN_DECISION` ;
- sources observees ;
- documents consommateurs.

### Relations

- peut appartenir a un objet metier ;
- peut etre requis par un `DocumentRequirement` ;
- peut etre derive par une `ReuseRule` ;
- peut generer une `ValidationIssue`.

### Exemples

- `personne.{role}.prenom` ;
- `personne.{role}.genre` ;
- `societe.{role}.siege.cp` ;
- `signature.date` ;
- `cession.prix.total` ;
- `capital.titres.valeur_nominale` ;
- `ordre.numero`.

### Risques de confusion

- reprendre un placeholder source comme champ canonique ;
- rendre global un champ template-only ;
- confondre forme affichee et composants ;
- utiliser un champ stable hors de son role.

## ReuseRule

### Role metier

Une `ReuseRule` explicite une reutilisation, une derivation ou une synchronisation controlee.

### Champs principaux

- identifiant ;
- libelle ;
- source ;
- cible ;
- type : reference, copie initiale, derivation, formatage, calcul ;
- condition d'activation ;
- activation par defaut ;
- comportement si inactif ;
- possibilite d'override ;
- justification source ;
- niveau de risque.

### Relations

- agit sur `Person`, `Organization`, `Address` ou `FieldDefinition` ;
- cree ou met a jour des `RoleAssignment` ;
- peut declencher des `ValidationIssue`.

### Exemples

- `dossier_unipersonnel` ;
- `domiciliation_is_registered_office` ;
- `registered_office_is_exercise_place` ;
- `sel_is_acquirer` ;
- `sel_is_scm_transferee` ;
- `vendor_is_praticien_standard` ;
- `address_components_to_display`.

### Risques de confusion

- activer une regle parce qu'elle est souvent vraie ;
- transformer une suggestion en valeur juridique ;
- effacer un override local lors d'une mise a jour source ;
- synchroniser deux roles qui doivent diverger.

## ValidationIssue

### Role metier

Une `ValidationIssue` rend visible un probleme au lieu de le corriger silencieusement.

### Champs principaux

- identifiant ;
- severite : info, warning, blocking ;
- scope : dossier, document, champ, role, adresse, piece ;
- message ;
- cause ;
- action attendue ;
- statut : ouvert, resolu, accepte, reporte ;
- source de detection ;
- trace de resolution.

### Relations

- appartient a un `Dossier` ;
- peut viser un `DocumentRequirement` ;
- peut viser un `FieldDefinition`, un `RoleAssignment`, une `Address` ou une `SupportingEvidence`.

### Exemples

- numero RPPS manquant pour une demande d'ordre ;
- siege social derive du lieu d'exercice mais option non confirmee ;
- date de signature differente de la date de decision ;
- document manuel attendu ;
- piece ordinale manquante.

### Risques de confusion

- bloquer une generation de test unitaire pour une piece non necessaire ;
- laisser passer une incoherence qui touche un document juridique ;
- confondre alerte produit et validation juridique.

## SupportingEvidence

### Role metier

Une `SupportingEvidence` represente une piece ou preuve utile au dossier.

### Champs principaux

- identifiant ;
- categorie ;
- libelle ;
- fichier ou reference externe ;
- statut : attendu, recu, valide, manquant, non requis ;
- portee : dossier, operation, document, ordre, banque ;
- caractere bloquant ;
- responsable ;
- date de reception ;
- notes de revue.

### Relations

- appartient a un `Dossier` ;
- peut etre exigee par un `DocumentRequirement` ;
- peut generer une `ValidationIssue`.

### Exemples

- plans ou devis pour l'ordre ;
- attestation de depot de capital ;
- bail initial ;
- Kbis ou justificatif RCS ;
- pieces d'identite ;
- documents SCM.

### Risques de confusion

- faire dependre la generation DOCX d'une piece utile seulement pour l'envoi ;
- masquer une piece bloquante pour l'ordre ;
- confondre piece justificative et variable documentaire.

## Regle de modelisation finale

Le front global doit stocker les faits metier sous forme d'objets et les usages sous forme de roles. Les documents ne doivent consommer que des roles, des champs canoniques et des regles explicites.
