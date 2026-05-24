# Architecture front globale V1

Ticket : `GLOBAL-FRONT-ARCHITECTURE-001`

Statut : cadrage produit et donnees, sans implementation UI.

## Objet

Ce document definit l'architecture metier cible du nouveau front global a partir du registre canonique global V2.1. Il ne modifie ni l'UI existante, ni les generateurs, ni le moteur DOCX/PDF/ZIP.

Le front actuel reste un prototype et un bac a sable. Il ne sert pas de modele d'architecture globale.

## Sources directrices

- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`
- `docs/project/GLOBAL_VARIABLE_IDENTITY_MATRIX_V1.csv`
- `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V2.md`
- `docs/review/global_variable_identity_audit_001_report_v1.md`
- `docs/review/global_human_answers_integration_001_report_v1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `src/sydel_doc_engine/registry/catalog.py`
- `project/source_truth/albane_reponse_mail_selarl_v1.md`
- `project/source_truth/notebooklm_selarl_10_prompts_v1.md`
- `project/source_truth/Documents_a_generer_par_cas_V3.docx`

## Principes cibles

Le front global doit etre construit autour d'objets metier stables, pas autour des champs du prototype.

Les objets pivots sont :

- `Dossier / Matter / Operation`
- `Person`
- `Organization / Company`
- `Address`
- `RoleAssignment`
- `DocumentRequirement`
- `FieldDefinition`
- `ReuseRule`
- `ValidationIssue`
- `SupportingEvidence`

Le principe central est le suivant : une fiche metier peut etre reutilisee dans plusieurs roles, mais le role reste explicite. La reutilisation cree un lien trace, pas une fusion de sens.

## Entites metier canoniques

### Dossier / Matter / Operation

Le dossier est l'enveloppe de travail. Il porte le type d'operation, la famille documentaire, les options metier et la liste des documents attendus.

Champs structurants :

- type d'operation : constitution SEL, cession, apport, SCM, SPFPL, SCI, SAS, etc. ;
- structure cible : `SELARL`, `SELAS`, `SPFPL cession`, `SPFPL apport`, `SCS`, `SCI`, `SCI IRIS`, `SCM`, `SAS` ;
- profession et contexte ordinal ;
- options dossier : regime communautaire, site distinct, derogation, cession, apport, bail, SCM, cession SCM, dossier unipersonnel ;
- statut de saisie, statut de revue et statut de generation.

Le dossier ne doit pas contenir directement tous les champs documentaires. Il orchestre les objets rolees, les documents attendus et les validations.

### Person

Une personne est une fiche d'identite reutilisable. Elle n'est jamais equivalent a un role juridique par elle-meme.

Exemples de personnes :

- praticien ;
- associe personne physique ;
- gerant ;
- president ;
- signataire ;
- mandataire ;
- vendeur / cedant ;
- bailleur ou locataire personne physique ;
- conjoint ;
- representant d'une personne morale.

La meme personne peut alimenter plusieurs roles si une `ReuseRule` ou une option de dossier l'autorise, par exemple `Dossier unipersonnel`.

### Organization / Company

Une societe ou organisation est une fiche d'entite morale rolee.

Exemples :

- SEL en constitution ;
- SELAS ;
- SPFPL ;
- SCM existante ;
- SCM cedee ;
- societe cible ;
- societe civile micro-holding future ;
- banque ;
- administration fiscale ;
- conseil de l'ordre ;
- bailleur personne morale.

La denomination, le capital, le RCS et le siege doivent rester rolees. Une SEL en constitution, une SCM cedee, une SPFPL et une micro-holding ne se fusionnent pas parce qu'elles apparaissent dans le meme dossier.

### Address

Une adresse est un objet distinct, type par usage. Elle peut etre stockee en composants et exposee sous forme affichee.

Usages cibles :

- domicile du praticien ;
- lieu d'exercice principal / cabinet ;
- siege social d'une societe rolee ;
- domiciliation, egale au siege social ;
- adresse de la SCM standard, reutilisable depuis le lieu d'exercice selon regle ;
- adresse de la SCM cedee ;
- adresse du cessionnaire SCM ;
- locaux loues ;
- conseil de l'ordre ;
- banque ;
- administration ou service d'enregistrement.

Le front doit demander une seule fois une adresse seulement quand l'usage est effectivement unique. Quand deux usages peuvent coincider, le front propose une reutilisation explicite.

### RoleAssignment

Un role assignment relie une personne ou une organisation a un role dans un dossier, un document ou une operation.

Exemples :

- `personne.praticien` pointe vers la fiche Person du client ;
- `personne.associe[0]` pointe vers le praticien si `Dossier unipersonnel` est actif ;
- `personne.signataire` pointe vers le praticien pour un document donne ;
- `societe.acquereur` pointe vers la SEL en constitution dans une cession SELARL standard ;
- `societe.scm_cession.cessionnaire` pointe vers la SEL en constitution seulement si la regle est activee.

Le role assignment est l'outil principal pour eviter les doubles saisies sans perdre les distinctions juridiques.

### DocumentRequirement

Un document attendu est une occurrence issue du type de dossier et des conditions metier.

Il porte :

- code canonique `DOC-XXX` quand le document existe dans le moteur ;
- libelle source ;
- famille documentaire et lot ;
- statut : generable, manuel, non implemente, contexte incomplet, reserve ;
- champs requis ;
- issues bloquantes ou non bloquantes ;
- liens vers les pieces justificatives.

Cette couche distingue le dossier complet du document unitaire. Elle ne decide pas seule de fusionner les donnees.

### FieldDefinition

Un champ est une definition canonique issue du registre global.

Il porte :

- chemin canonique, par exemple `personne.{role}.prenom` ;
- type metier : texte, date, montant, adresse, identifiant, option, collection ;
- role ou scope attendu ;
- forme : composee, decomposée, affichee, calculee ;
- statut de stabilite ;
- sources documentaires observees.

Le front doit consommer des `FieldDefinition`, pas des placeholders bruts de templates.

### ReuseRule

Une regle de reutilisation formalise un lien entre une source et une cible.

Exemples stables V2.1 :

- `Dossier unipersonnel` : praticien = associe unique = gerant = signataire ;
- domiciliation = siege social ;
- siege social = lieu d'exercice uniquement via option explicite ;
- SCM standard = lieu d'exercice ;
- vendeur / cedant du fonds liberal = praticien BNC dans le parcours SELARL standard ;
- acquereur / cessionnaire = SEL en constitution dans le parcours SELARL standard.

Une reutilisation ne supprime jamais les roles. Elle cree une reference, un prefill ou une synchronisation controlee.

### ValidationIssue

Une validation issue represente un probleme de saisie, de coherence ou de couverture documentaire.

Types :

- champ obligatoire manquant ;
- conflit entre deux roles ;
- reutilisation possible mais non confirmee ;
- document manuel ;
- document non implemente ;
- contexte incomplet ;
- piece justificative manquante ;
- override sensible a relire.

### SupportingEvidence

Les pieces justificatives ne sont pas le coeur du moteur documentaire, mais le front global doit prevoir leur statut.

Exemples :

- pieces ordinales ;
- plans ou devis de travaux ;
- justificatifs bancaires ;
- bail et avenants ;
- attestations de depot ;
- pieces d'identite ;
- justificatifs SCM ou RCS.

Cette couche doit rester separee de la generation. Une piece peut bloquer la revue du dossier sans bloquer la generation d'un document de test.

## Relations principales

| Source | Relation | Cible |
|---|---|---|
| `Dossier` | contient | `DocumentRequirement[]` |
| `Dossier` | reference | `Person[]`, `Organization[]`, `Address[]` |
| `RoleAssignment` | relie | `Person` ou `Organization` a un role |
| `Address` | appartient a | une personne, une organisation ou un usage dossier |
| `ReuseRule` | derive ou reference | un champ, une adresse, une personne ou une societe vers un autre role |
| `DocumentRequirement` | consomme | `FieldDefinition[]` et `RoleAssignment[]` |
| `ValidationIssue` | cible | dossier, document, champ, role, adresse ou piece |
| `SupportingEvidence` | rattache | dossier, operation, document ou tiers |

## Donnees saisies une seule fois

Les donnees suivantes doivent etre saisies une seule fois par fiche metier, puis reutilisees par roles explicites :

- identite du praticien : civilite d'affichage, genre, prenom, nom, naissance, nationalite, profession ;
- identifiants professionnels du praticien : RPPS, ordre, departement ordinal, profession reglementee ;
- adresse de domicile du praticien ;
- fiche de la societe principale : denomination, forme, capital, siege, RCS quand disponible ;
- adresse du lieu d'exercice principal ;
- donnees de signature par defaut : lieu, date, nombre d'exemplaires si le dossier l'impose ;
- associes et repartition du capital quand ils sont structurellement communs ;
- SCM existante quand elle est citee dans plusieurs documents ;
- banque de depot ou tiers parametrables quand ils sont effectivement communs au dossier.

Ces donnees peuvent avoir des overrides documentaires, mais l'override doit etre localise et trace.

## Donnees reutilisees via regles explicites

Les reutilisations suivantes sont autorisees seulement si le contexte ou l'utilisateur les confirme :

| Regle | Source | Cible | Condition |
|---|---|---|---|
| Dossier unipersonnel | praticien | associe unique, gerant, signataire | option dossier active |
| Domiciliation = siege | siege social societe principale | domiciliation affichee | regle V2.1 stable |
| Siege = lieu d'exercice | lieu d'exercice principal | siege social | option explicite |
| SCM standard = lieu d'exercice | lieu d'exercice principal | adresse SCM | cas standard documente |
| Cession SELARL standard | praticien BNC | vendeur / cedant | parcours SELARL standard |
| Cession SELARL standard | SEL en constitution | acquereur / cessionnaire | parcours SELARL standard |
| Adresse composee -> affichee | composants adresse | adresse affichee | transformation controlee |
| Montant chiffres -> lettres | montant numerique | montant en lettres | transformation controlee avec override |

## Donnees qui restent distinctes

Les donnees suivantes restent distinctes meme si les libelles sont proches :

- praticien, associe, gerant, president, signataire, mandataire et representant ;
- vendeur, cedant, bailleur, locataire, acquereur et cessionnaire ;
- associe personne morale et representant de cette personne morale ;
- domicile du praticien, lieu d'exercice, siege social, adresse de domiciliation, locaux loues, adresse SCM, adresse SCM cedee et adresse cessionnaire SCM ;
- societe principale, SPFPL, SCM, societe cible, societe cedee, societe apporteuse et micro-holding future ;
- civilite d'affichage et genre grammatical ;
- date de signature, date de decision, date de PV, date de bail, date d'effet, date de jouissance et date limite de realisation ;
- capital social, apports, prix de cession, prix unitaire, prix global, montant de pret et credit-vendeur ;
- parts sociales, actions et actions de preference.

## Eviter les doubles saisies sans fusionner trop tot

Le front doit privilegier quatre mecanismes :

1. Créer d'abord les fiches metier : personne, societe, adresse, operation.
2. Assigner ensuite les roles par `RoleAssignment`.
3. Proposer les reutilisations sous forme de regles visibles et reversibles.
4. Afficher les conflits et overrides comme des `ValidationIssue`, jamais comme des corrections silencieuses.

La matrice d'identite globale sert a orienter ces regles :

- `SAME_FIELD` : un seul champ canonique ;
- `SAME_DATA_DIFFERENT_SHAPE` : une source metier avec plusieurs formes ;
- `EXPLICIT_REUSE_ONLY` : prefill ou lien uniquement via regle ;
- `DISTINCT_FIELDS` : champs separes ;
- `UNCERTAIN_REQUIRES_HUMAN_DECISION` : pas de decision automatique.

## Position sur le prototype actuel

Le prototype Streamlit n'est pas detruit. Il reste utile pour diagnostiquer le moteur, tester un document unitaire et verifier la generation DOCX/PDF/ZIP locale.

Il ne doit pas etre generalise :

- ses widgets ne sont pas une source canonique ;
- son `session_state` ne doit pas devenir le modele global ;
- ses parcours SELARL et SCI ne doivent pas imposer l'architecture future ;
- ses prefill de test ne doivent pas etre confondus avec des donnees metier reelles.

La migration future doit reprendre les concepts qui ont prouve leur utilite, pas copier l'implementation.

## Limites V1

Cette architecture est suffisante pour lancer le rebuild front data-first. Elle n'est pas suffisante pour :

- modifier un generateur ;
- modifier le wording juridique ;
- ajouter un mode Projet / filigrane ;
- implementer le cas SELAS medecin avec micro-holding ;
- automatiser les documents signales comme manuels ;
- trancher les calculs de capital, actions de preference ou droits financiers.
