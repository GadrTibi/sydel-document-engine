# Rapport QA - GLOBAL-FRONT-ARCHITECTURE-QA-001

Date : 2026-05-24

Statut : QA documentaire et architecture, sans modification de Python, des generateurs, du moteur DOCX/PDF/ZIP ou de l'UI.

## 1. Objet du controle

Ce rapport verifie que l'architecture du nouveau front global couvre des documents sentinelles representatifs du moteur, sans trou de modelisation et sans fusion abusive de variables.

Le controle porte sur l'architecture produit et donnees uniquement. Il ne valide pas les maquettes, ne recode pas le front et ne modifie aucun generateur.

## 2. Etat Git initial

Commandes executees :

- `git status --short --branch`
- `git branch -vv`
- `git log --oneline -10`

Constat initial :

- branche active : `main`
- dernier commit initial : `92f4e0e docs: add global front architecture v1`
- branche locale en avance de 4 commits sur `origin/main`
- element non suivi deja present et laisse hors perimetre : `docs/docssource_truth/`

## 3. Sources utilisees

Sources d'architecture front :

- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`
- `docs/project/GLOBAL_FRONT_RULES_V1.md`
- `docs/project/GLOBAL_FRONT_SCREEN_STRATEGY_V1.md`
- `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md`

Sources registre et audit :

- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`
- `docs/project/GLOBAL_VARIABLE_IDENTITY_MATRIX_V1.csv`

Sources metier :

- `project/source_truth/Documents_a_generer_par_cas_V3.docx`
- `project/source_truth/notebooklm_selarl_10_prompts_v1.md`
- `project/source_truth/albane_reponse_mail_selarl_v1.md`

Sources moteur et documentaires :

- `src/sydel_doc_engine/registry/catalog.py`
- templates DOCX des sentinelles dans `project/source_documents/`
- specs delivery pertinentes dans `docs/delivery/`, notamment Lot 1, Lot 2 ordre, Lot 3 cession, Lot 4 statuts SEL/SCM et Lot 5 SPFPL/SCM cession.

Memoire projet relue selon `AGENTS.md` :

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- ADR applicables `0001`, `0002`, `0003`, `0005`

## 4. Methode

Pour chaque document sentinelle, le controle a croise :

- l'entree du registre moteur ;
- les placeholders extraits du template DOCX pertinent ;
- les variables et points ouverts des specs delivery ;
- les regles du registre canonique global V2.1 ;
- les objets front et les blocs d'ecran prevus par l'architecture V1.

La matrice d'identite comporte 142 rapprochements classes :

- `SAME_FIELD` : 16
- `SAME_DATA_DIFFERENT_SHAPE` : 30
- `EXPLICIT_REUSE_ONLY` : 16
- `DISTINCT_FIELDS` : 15
- `UNCERTAIN_REQUIRES_HUMAN_DECISION` : 65

Le controle a retenu `DOC-041` plutot que `DOC-039`, car le contrat d'apport SPFPL teste mieux les roles apporteur / societe cible / evaluateur / commissaire. Il a retenu `DOC-025` plutot que `DOC-020`, car les statuts SCM testent la pluralite d'associes, les personnes morales et les anomalies de repartition.

## 5. Verdict global

Verdict global : ORANGE maitrisable.

L'architecture V1 couvre les sentinelles au niveau objet : les roles, adresses, documents attendus, reutilisations explicites, validations et overrides sont presents. Aucun document sentinelle ne revele un trou de modelisation rouge.

Le niveau orange vient de la couche data a construire : plusieurs documents exigent des sous-structures detaillees qui ne doivent pas etre improvisees dans l'UI. Ces sous-structures doivent entrer dans `FRONT-DATA-LAYER-001`, puis etre renforcees par `FRONT-ROLE-MODEL-001` et `FRONT-ADDRESS-MODEL-001`.

Synthese :

| Verdict | Documents |
|---|---|
| VERT | `DOC-002`, `DOC-033` |
| ORANGE | `DOC-034`, `DOC-017`, `DOC-009`, `DOC-041`, `DOC-025` |
| ROUGE | Aucun |

Conclusion de demarrage : le rebuild front peut commencer, mais uniquement par la couche de donnees front. Un demarrage direct par ecrans visibles risquerait de recreer les confusions du prototype.

## 6. Fiches de controle sentinelles

### DOC-002 - Autorisation de domiciliation

Roles requis :

- signataire ;
- praticien ou dirigeant principal ;
- societe principale.

Entites et adresses requises :

- `Person` praticien/signataire ;
- `Organization` societe principale ;
- `Address` siege social et domiciliation ;
- lieu et date de signature.

Montants / dates sensibles :

- capital social ;
- date de signature.

Champs canoniques V2.1 correspondants :

- `personne.{role}.civilite_affichage`
- `personne.{role}.prenom`
- `personne.{role}.nom`
- `societe.{role}.denomination`
- `societe.{role}.capital_social`
- `societe.{role}.siege.adresse`
- `domiciliation.adresse`
- `signature.lieu`
- `signature.date`

Objet front porteur :

- `Person` pour le signataire ;
- `Organization / Company` pour la societe principale ;
- `Address` pour siege/domiciliation ;
- `ReuseRule` pour domiciliation = siege ;
- `DocumentRequirement` pour le besoin `DOC-002`.

Ecran / bloc cible :

- Fiche Client ;
- Fiche societe ;
- Blocs d'adresses ;
- Documents attendus ;
- Generation.

Reutilisations explicites possibles :

- domiciliation = siege social ;
- signataire = praticien si `Dossier unipersonnel` ou regle explicite ;
- adresse composee vers adresse affichee.

Points ambigus :

- le champ legacy `domiciliation.adresse_domiciliation_affichee` doit devenir une forme affichee/override, pas une nouvelle adresse metier ;
- les composants `num_voie_siege`, `voie_siege`, `cp_siege`, `ville_siege` et la forme affichee doivent rester relies mais tracables.

Verdict : VERT.

Action :

- mapper le legacy de domiciliation dans `FRONT-DATA-LAYER-001`.

### DOC-034 - Demande d'inscription a l'ordre

Roles requis :

- signataire inscrit ;
- societe a inscrire ;
- mandataire ;
- ordre professionnel.

Entites et adresses requises :

- `Person` signataire ;
- `Organization` societe principale ;
- `Organization` conseil de l'ordre ;
- `Person` ou `Organization` mandataire ;
- adresse personnelle du signataire ;
- adresse ordinale affichee ou composee ;
- lieu et date de signature.

Montants / dates sensibles :

- date de signature ;
- mention de derogation si l'option dossier est active.

Champs canoniques V2.1 correspondants :

- `personne.{role}.prenom`
- `personne.{role}.nom`
- `personne.{role}.profession`
- `personne.{role}.adresse_personnelle`
- `societe.{role}.denomination`
- `ordre.professionnel`
- `ordre.adresse`
- `personne.mandataire.*`
- `signature.lieu`
- `signature.date`
- `dossier.options.derogation`

Objet front porteur :

- `Person` pour signataire et mandataire personne physique ;
- `Organization / Company` pour societe et conseil de l'ordre ;
- `Address` pour adresse personnelle et adresse ordre ;
- `RoleAssignment` pour separer signataire, mandataire et inscrit ;
- `ValidationIssue` pour derogation manquante ou mandataire absent.

Ecran / bloc cible :

- Fiche Client ;
- Fiche societe ;
- Bloc ordre / identifiants ;
- Documents attendus ;
- Generation.

Reutilisations explicites possibles :

- signataire = praticien si regle active ;
- mandataire depuis configuration SYDEL, mais jamais comme constante magique ;
- adresse ordre affichee construite depuis composants si disponibles.

Points ambigus :

- le modele ordinal par inscrit reste ouvert en V2.1 ;
- le mandataire peut etre configure ou saisi ;
- la mention de derogation doit bloquer si l'option est active et que le texte manuel manque ;
- le cas SCM exige des donnees ordinales explicites.

Verdict : ORANGE.

Action :

- definir les sous-champs `ordre` et `mandataire` dans `FRONT-DATA-LAYER-001`, puis verrouiller les roles dans `FRONT-ROLE-MODEL-001`.

### DOC-017 - Statuts SELARL medecin

Roles requis :

- praticien ;
- associe(s) ;
- gerant ;
- signataire ;
- banque de depot ;
- ordre professionnel.

Entites et adresses requises :

- `Organization` SELARL ;
- `Person` associes ;
- `Person` gerant/signataire ;
- `Organization` banque ;
- `Organization` ordre ;
- siege social ;
- adresse personnelle de l'associe ;
- adresse banque.

Montants / dates sensibles :

- capital social et capital en lettres ;
- nombre total de parts ;
- valeur nominale ;
- seuil d'achat de materiel ;
- seuil d'emprunt de gerance ;
- date de cloture du premier exercice ;
- date de signature ;
- nombre d'exemplaires.

Champs canoniques V2.1 correspondants :

- `societe.{role}.denomination`
- `societe.{role}.forme_sociale`
- `societe.{role}.capital_social`
- `capital.titres.nombre_total`
- `capital.titres.valeur_nominale`
- `capital.repartition_associes`
- `personne.{role}.*`
- `personne.{role}.numero_ordre`
- `personne.{role}.numero_rpps`
- `banque.{role}`
- `signature.*`

Objet front porteur :

- `Dossier / Operation` pour la constitution SELARL medecin ;
- `Organization` pour la SELARL ;
- `Person` + `RoleAssignment` pour praticien, associe, gerant, signataire ;
- `FieldDefinition` pour capital, seuils et banque ;
- `ReuseRule` pour `Dossier unipersonnel`.

Ecran / bloc cible :

- Qualification ;
- Fiche Client ;
- Fiche societe ;
- Capital & associes ;
- Bloc ordre ;
- Generation.

Reutilisations explicites possibles :

- praticien = associe unique = gerant = signataire si `Dossier unipersonnel` ;
- siege = lieu d'exercice seulement via option ;
- montant chiffres vers lettres via derivation controlee.

Points ambigus :

- le moteur V1 du document est limite a l'associe unique ;
- la ligne `personne_2` de la source medecin est non canonique ;
- la pluralite d'associes, les seuils de gerance et la banque doivent etre structures sans deduction implicite.

Verdict : ORANGE.

Action :

- faire porter par `FRONT-DATA-LAYER-001` les collections capital/associes, les seuils et les champs banque, puis faire confirmer les roles par `FRONT-ROLE-MODEL-001`.

### DOC-033 - Acte de cession des parts de la SCM vers SEL

Roles requis :

- cedant praticien BNC ;
- conjoint du cedant si requis ;
- societe cessionnaire ;
- representant de la cessionnaire ;
- SCM cedee ;
- associes de la SCM cedee ;
- signataires.

Entites et adresses requises :

- `Person` cedant ;
- `Person` conjoint ;
- `Organization` SEL cessionnaire ;
- `Person` representant cessionnaire ;
- `Organization` SCM cedee ;
- domicile cedant ;
- siege cessionnaire ;
- siege SCM cedee.

Montants / dates sensibles :

- nombre de parts cedees ;
- plage de parts ;
- prix unitaire ;
- prix global ;
- credit-vendeur montant/duree/taux ;
- capital de la cessionnaire ;
- capital et total de parts de la SCM cedee ;
- nombre d'exemplaires.

Champs canoniques V2.1 correspondants :

- `scm_cession.{champ}`
- `scm_cession.scm_cedee.*`
- `scm_cession.cessionnaire.*`
- `scm_cession.cedant.*`
- `cession.parts.nombre`
- `cession.parts.plage`
- `cession.prix.total`
- `cession.prix.unitaire`
- `signature.*`

Objet front porteur :

- `Operation` SCM cession ;
- `Person` pour cedant, conjoint, representant ;
- `Organization` pour cessionnaire et SCM cedee ;
- `Address` typee pour domicile, siege cessionnaire, siege SCM cedee ;
- `ValidationIssue` pour credit-vendeur incomplet, representant ambigu ou total de parts incoherent.

Ecran / bloc cible :

- Bloc SCM ;
- Bloc cession ;
- Bloc parties ;
- Blocs d'adresses ;
- Generation.

Reutilisations explicites possibles :

- cedant = praticien BNC dans le parcours SELARL standard ;
- cessionnaire = SEL en constitution dans le parcours SELARL standard ;
- adresse SCM standard = lieu d'exercice seulement lorsque le cas standard est confirme.

Points ambigus :

- representant cessionnaire a confirmer ;
- credit-vendeur conditionnel ;
- adresse SCM cedee distincte de l'adresse cessionnaire par defaut, malgre l'alias historique source.

Verdict : VERT.

Action :

- encoder les roles et adresses SCM distincts dans `FRONT-ROLE-MODEL-001` / `FRONT-ADDRESS-MODEL-001`.

### DOC-009 - Acte de cession d'un cabinet medical

Roles requis :

- vendeur/praticien BNC ;
- conjoint vendeur ;
- societe acquereur ;
- representant acquereur ;
- bailleur/locataire selon bail ;
- signataires vendeur et acquereur.

Entites et adresses requises :

- `Person` vendeur ;
- `Person` conjoint ;
- `Organization` acquereur ;
- `Person` representant acquereur ;
- operation de cession cabinet ;
- adresse vendeur ;
- adresse exercice vendeur ;
- adresse cabinet ;
- adresse locaux loues ;
- siege acquereur.

Montants / dates sensibles :

- prix total ;
- prix elements corporels ;
- prix elements incorporels ;
- credit-vendeur montant/duree/taux/majoration ;
- dates de bail, debut, fin, reconductions ;
- date immatriculation acquereur ;
- date inscription ordre acquereur ;
- chiffres d'affaires et resultats des trois exercices ;
- nombre de pages/exemplaires.

Champs canoniques V2.1 correspondants :

- `cession.cabinet.adresse`
- `cession.cabinet.prix_composantes`
- `cession.vendeur.*`
- `cession.acquereur.*`
- `cession.financement.*`
- `cession.prix.*`
- `bail.parties`
- `bail.dates`
- `signature.*`

Objet front porteur :

- `Dossier / Operation` cession cabinet ;
- `Person` et `Organization` rolees ;
- `Address` typee par usage ;
- `FieldDefinition` pour prix, bail, exercices et financement ;
- `ValidationIssue` pour origine de propriete ou financement incomplet.

Ecran / bloc cible :

- Bloc cession ;
- Bloc bail ;
- Bloc financement ;
- Bloc parties ;
- Blocs d'adresses ;
- Documents attendus ;
- Generation.

Reutilisations explicites possibles :

- vendeur = praticien BNC dans le parcours SELARL standard ;
- acquereur = SEL en constitution dans le parcours SELARL standard ;
- adresse cabinet = lieu d'exercice seulement via regle explicite ;
- locaux loues = lieu d'exercice seulement via regle explicite.

Points ambigus :

- origine de propriete peut rester libre selon les arbitrages ;
- exercices financiers et bail sont couverts par `FieldDefinition` mais meritent des sous-blocs data explicites ;
- locataire du bail n'est pas toujours la SELARL ;
- adresse cabinet, locaux loues et siege doivent rester distincts par defaut.

Verdict : ORANGE.

Action :

- ajouter dans `FRONT-DATA-LAYER-001` des sous-structures `cession.exercices[]`, `cession.bail`, `cession.prix`, `cession.financement` et `cession.cabinet.origine`.

### DOC-041 - Contrat d'apport SEL vers SPFPL

Roles requis :

- apporteur ;
- societe SPFPL beneficiaire ;
- societe cible/apportee ;
- dirigeant president ou gerant ;
- evaluateur de l'apport ;
- commissaire aux apports ;
- conjoint si requis ;
- signataire.

Entites et adresses requises :

- `Person` apporteur ;
- `Organization` SPFPL ;
- `Organization` societe cible/apportee ;
- `Person` dirigeant ;
- `Person` ou `Organization` evaluateur ;
- `Person` ou `Organization` commissaire ;
- domicile apporteur ;
- siege SPFPL ;
- siege societe apportee.

Montants / dates sensibles :

- nombre d'actions ;
- nombre de parts apportees ;
- plage de parts ;
- valeur globale d'apport ;
- valeur par part ;
- capital social ;
- capital de la societe apportee ;
- valeur nominale d'action ;
- date de signature ;
- nombre d'exemplaires.

Champs canoniques V2.1 correspondants :

- `spfpl.operation.type`
- `apport_titres.*`
- `commissaire_aux_apports.{champ}`
- `societe_spfpl.*`
- `societe_cible.*`
- `personne.{role}.*`
- `capital.titres.*`
- `signature.*`

Objet front porteur :

- `Operation` SPFPL apport ;
- `Organization` SPFPL et societe cible ;
- `Person` apporteur et dirigeant ;
- `RoleAssignment` pour evaluateur et commissaire ;
- `SupportingEvidence` si rapport ou pieces d'evaluation sont suivis ;
- `ValidationIssue` pour valeur fixe source ou commissaire non selectionne.

Ecran / bloc cible :

- Bloc SPFPL ;
- Capital / titres / apports ;
- Fiche societe ;
- Fiche Client ;
- Generation.

Reutilisations explicites possibles :

- apporteur = praticien ou associe uniquement via role explicite ;
- societe cible distincte de la SPFPL ;
- evaluateur/commissaire depuis configuration ou saisie, mais jamais fixes silencieusement.

Points ambigus :

- source nommee avec evaluateur/commissaire fixes vs variante parametrable ;
- libelle commissaire aux apports a confirmer dans certains cadrages ;
- plusieurs champs SPFPL restent classes `UNCERTAIN_REQUIRES_HUMAN_DECISION` dans la matrice.

Verdict : ORANGE.

Action :

- modeliser `apport_titres`, `societe_cible`, `evaluateur` et `commissaire_aux_apports` comme roles explicites et bloquer les valeurs fixes non confirmees.

### DOC-025 - Statuts SCM

Roles requis :

- associes SCM personnes physiques ou morales ;
- representant de personne morale ;
- signataires ;
- banque de depot.

Entites et adresses requises :

- `Organization` SCM ;
- `Person` associe physique ;
- `Organization` associe personne morale ;
- `Person` representant ;
- `Organization` banque ;
- siege SCM ;
- adresse personnelle associe personne physique ;
- siege associe personne morale ;
- adresse banque.

Montants / dates sensibles :

- capital social ;
- capital en lettres ;
- nombre de parts ;
- valeur nominale ;
- apports par associe ;
- lieu de signature.

Champs canoniques V2.1 correspondants :

- `statuts_civils.associes[]`
- `societe.{role}.*`
- `capital.titres.nombre_total`
- `capital.titres.valeur_nominale`
- `capital.repartition_associes`
- `apport.numeraire.montant`
- `banque.{role}`
- `signature.*`

Objet front porteur :

- `Organization` SCM ;
- `Person` / `Organization` pour associes ;
- `RoleAssignment` pour representant ;
- `FieldDefinition` pour parts/apports/capital ;
- `ValidationIssue` pour repartition incoherente ou valeur source heritee.

Ecran / bloc cible :

- Bloc SCM ;
- Fiche societe ;
- Capital & associes ;
- Blocs d'adresses ;
- Generation.

Reutilisations explicites possibles :

- associe personne morale + representant lies par role, sans fusion ;
- montant chiffres vers lettres par derivation controlee ;
- signataires depuis associes si la regle documentaire le confirme.

Points ambigus :

- la source legacy duplique `nb_parts_personne_2` pour deux lignes ;
- les statuts SCM exigent 1 a 6 associes avec parts/apports explicites ;
- satellites SCM hors statuts doivent rester documents distincts.

Verdict : ORANGE.

Action :

- definir `associes[]` SCM avec parts/apports par ligne et validation de somme dans `FRONT-DATA-LAYER-001`.

## 7. Principaux trous ou points a renforcer

Aucun trou rouge d'objet front n'a ete identifie. Les renforcements necessaires sont :

1. Modele `ordre` par inscrit et par structure : `DOC-034` montre qu'il faut separer profession affichee, destinataire, adresse ordinale et derogation.
2. Role model fin : signataire, mandataire, representant, cedant, cessionnaire, apporteur, evaluateur et commissaire ne doivent jamais etre fusionnes.
3. Address model fin : siege, domiciliation, lieu d'exercice, cabinet, locaux loues, SCM cedee, cessionnaire SCM, ordre et banque doivent etre des usages distincts.
4. Capital / titres / apports : `DOC-017`, `DOC-025` et `DOC-041` exigent une structure explicite de repartition, apports, parts/actions, montants chiffres/lettres et overrides.
5. Cession cabinet : `DOC-009` exige des sous-blocs explicites pour origine de propriete, bail, exercices financiers, prix et financement.
6. SPFPL apport : `DOC-041` exige que les tiers evaluateur/commissaire soient rolees et non repris de valeurs fixes source.
7. Legacy aliases : plusieurs placeholders historiques doivent devenir des aliases documentaires ou formes affichees, pas des champs metier concurrents.

## 8. Peut-on demarrer le rebuild du front ?

Oui, mais par `FRONT-DATA-LAYER-001` seulement.

Le registre V2.1 et l'architecture V1 suffisent pour demarrer :

- le modele `Person`, `Organization`, `Address`, `RoleAssignment` ;
- les documents attendus via `DocumentRequirement` ;
- les champs via `FieldDefinition` ;
- les reutilisations explicites via `ReuseRule` ;
- les issues via `ValidationIssue`.

Ils ne suffisent pas pour demarrer directement une UI visible complete, ni pour modifier les generateurs. Les sentinelles orange doivent devenir des criteres d'acceptation data layer.

## 9. Recommandations

1. Demarrer `FRONT-DATA-LAYER-001` en integrant le CSV `docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv` comme checklist de couverture.
2. Dans `FRONT-DATA-LAYER-001`, ajouter explicitement les sous-blocs `ordre`, `capital`, `cession`, `bail`, `apport_titres`, `scm_cession` et `statuts_civils.associes[]`.
3. Lancer ensuite `FRONT-ROLE-MODEL-001` avant tout ecran visible, car les sentinelles montrent que le risque principal est la fusion abusive de roles.
4. Lancer `FRONT-ADDRESS-MODEL-001` avant de traiter les blocs adresses, car les coincidences d'adresses sont frequentes mais non absolues.
5. Garder le prototype actuel comme outil de diagnostic uniquement ; ne pas le generaliser.

## 10. Tests

Aucun fichier Python n'a ete modifie. Aucun `ruff` ou `pytest` n'est requis pour ce ticket.

Validation attendue de ce ticket :

- relecture documentaire ;
- controle du diff ;
- verification que seuls des fichiers docs/CSV et pilotage sont modifies.
