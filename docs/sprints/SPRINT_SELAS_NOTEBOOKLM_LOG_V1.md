# Sprint SELAS - journal NotebookLM V1

Date d'ouverture : 2026-06-01

## Objet

Ce journal doit recevoir les reponses NotebookLM donnees par Naomie pendant le
sprint SELAS.

Regle : Naomie colle la reponse brute dans Codex. Codex ne laisse pas la reponse
dans le chat seulement ; il la restructure ici avant de passer au prompt
suivant.

## Statut global

| Sujet | Statut | Note |
| --- | --- | --- |
| Prompt 01 - Inventaire documentaire | FAIT | Reponse NotebookLM importee le 2026-06-01 ; sources non citees ou vides, donc matiere utile mais non validante |
| Prompt 02 - Differences SELARL / SELAS | FAIT | Reponse NotebookLM importee le 2026-06-01 ; differences utiles mais sources non citees |
| Prompt 03 - Gouvernance et statuts | FAIT | Reponse NotebookLM importee le 2026-06-01 ; gouvernance utile mais sources non citees |
| Prompt 04 - Variables et donnees | FAIT | Reponse NotebookLM importee le 2026-06-01 ; blocs de donnees utiles mais sources non citees |
| Prompt 05 - Reutilisation SELARL | FAIT | Reponse NotebookLM importee le 2026-06-01 ; reuse utile mais sources non citees |
| Prompt 06 - Cas conditionnels | FAIT | Reponse NotebookLM importee le 2026-06-01 ; cas dangereux utiles mais sources non citees |
| Prompt 07 - Recette / validation humaine | FAIT | Reponse NotebookLM importee le 2026-06-01 ; recette utile mais sources non citees |

## Template de reponse structuree

Copier ce bloc pour chaque reponse NotebookLM.

```text
## Reponse NotebookLM SELAS NN

Date :
Prompt utilise :
Source NotebookLM / indices cites :

### Synthese fiable

### Documents identifies

| Document | Condition | Statut | Source | Incertitude |
| --- | --- | --- | --- | --- |

### Conditions et exclusions

### Variables / donnees a saisir

### Differences SELARL / SELAS

### Reutilisation possible

| Element | Decision provisoire | Justification | Verification requise |
| --- | --- | --- | --- |

### Contradictions

### Informations non trouvees

### Impact sur le sprint

### Prochain prompt recommande
```

## Reponses NotebookLM

## Reponse NotebookLM SELAS 01

Date : 2026-06-01
Prompt utilise : Prompt 01 - Inventaire documentaire SELAS
Source NotebookLM / indices cites : la reponse ne cite pas de source exploitable ;
les champs `Source` sont vides pour les documents listes. Cette reponse doit
etre traitee comme un inventaire exploratoire, pas comme une validation
juridique ou documentaire.

### Synthese fiable

NotebookLM identifie un noyau de documents SELAS autour des statuts, de la
gouvernance, des formalites, de l'ordre professionnel, du depot de capital, des
cessions, de la SCM, des derogations, du regime communautaire et des
questionnaires professionnels.

La valeur principale de cette reponse est de confirmer les axes a investiguer.
La fiabilite reste limitee car aucune source precise n'est citee et plusieurs
points sont marques `non trouve`.

### Documents identifies

| Document | Condition | Statut | Source | Incertitude |
| --- | --- | --- | --- | --- |
| Statuts SELAS | Creation de SELAS | Toujours | Non citee | Le contenu varie fortement selon la profession, notamment medecin/dentiste |
| PV de nomination du president | Si le president n'est pas nomme directement dans les statuts | Conditionnel | Non citee | Basculer strictement de `gerant` a `president` |
| Procuration ou mandat | Formalites faites par le cabinet | Toujours | Non citee | Document dit commun a toutes les professions, a verifier |
| Declaration de non-condamnation | Formalite greffe | Toujours | Non citee | Incertitude indiquee `non trouve` |
| Demande d'inscription a l'Ordre | Professions reglementees | Toujours | Non citee | Variantes possibles selon le departement, exemple formulaire 94 |
| Attestation de depot de capital | Constitution et blocage des fonds | Toujours | Non citee | Incertitude indiquee `non trouve` |
| Acte de cession de fonds liberal | Si le praticien etait en BNC et vend son activite a la societe | Conditionnel | Non citee | Redaction personnalisee, souvent finalisee manuellement |
| Acte de cession de parts de SCM | Si le praticien est membre d'une SCM | Conditionnel | Non citee | Identification de la SCM et de ses associes actuels requise |
| Avenant au bail | En cas de cession de fonds et transfert du bail | Conditionnel | Non citee | Peut etre redige par le bailleur ou l'agence |
| Demande de derogation exercice sur site distinct | Si deuxieme lieu d'exercice professionnel | Conditionnel | Non citee | Identifie comme `cas numero 2`, a confirmer |
| Acte de renonciation a la qualite d'associe du conjoint | Praticien marie sous regime de communaute | Conditionnel | Non citee | Incertitude indiquee `non trouve` |
| Lettre d'avertissement au conjoint | Praticien marie sous regime de communaute | Conditionnel | Non citee | Incertitude indiquee `non trouve` |
| Questionnaire specifique par profession a l'Ordre | Selon profession | Conditionnel | Non citee | Non requis pour les dentistes selon la reponse, a verifier |

### Conditions et exclusions

- Toujours selon NotebookLM : statuts SELAS, procuration/mandat, DNC, demande
  d'inscription a l'Ordre, depot de capital.
- Conditionnel selon NotebookLM : PV de nomination du president, cession de
  fonds liberal, cession de parts de SCM, avenant au bail, derogation site
  distinct, regime communautaire, questionnaire professionnel.
- Les documents de cession de fonds sont signales comme complexes et souvent
  finalises manuellement : a proteger avant toute automatisation.
- La variation profession medecin/dentiste est un axe critique pour les statuts
  et les documents d'ordre.

### Variables / donnees a saisir

La reponse ne donne pas encore une liste de variables structuree. Donnees
mentionnees ou deduites comme a verifier :

- profession ;
- departement ou ordre competent ;
- president nomme dans les statuts ou hors statuts ;
- existence d'un exercice BNC anterieur ;
- existence d'une SCM ;
- bail a transferer ;
- deuxieme lieu d'exercice ;
- regime matrimonial communautaire ;
- associes minoritaires ;
- seuils de limitation de pouvoirs du president ;
- origine de propriete en cas de cession de fonds ;
- pieces ordinales.

### Differences SELARL / SELAS

- Gouvernance : `gerant` SELARL ne doit pas etre transpose sans controle ; la
  SELAS appelle au moins le role `president`.
- Capital : la reponse souleve implicitement les actions et droits de vote,
  distincts des parts sociales.
- Statuts : la profession et la forme SELAS peuvent modifier fortement le
  contenu.
- PV : le document proche du PV de nomination gerant doit etre adapte ou bloque
  tant que le wording president n'est pas valide.

### Reutilisation possible

| Element | Decision provisoire | Justification | Verification requise |
| --- | --- | --- | --- |
| DOC-001 DNC | reuse-check | Document attendu en SELAS et deja traite cote SELARL | Verifier source SELAS et wording exact |
| DOC-003 procuration | reuse-check | NotebookLM le presente comme commun | Verifier source et absence de wording SELARL |
| DOC-004 PV nomination gerant | adapter/no-go | Fonction proche mais role SELAS different | Comparer president/gerant et conditions de nomination |
| DOC-005/DOC-006 regime communautaire | reuse-check/no-go | Documents cites pour conjoint communaute | Verifier si les sources couvrent SELAS et quelle piece reste reservee |
| DOC-034 demande d'inscription a l'Ordre | reuse-check | Demande d'ordre citee comme attendue | Verifier overlays SELAS, profession et departement |
| Statuts SELAS | adapter/no-go | Source/spec semble exister mais variations fortes | Lire sources statuts SELAS et distinguer profession/sous-cas |
| Cession fonds / SCM / bail | no-go provisoire | Complexite et personnalisation signalees | Sources et arbitrages requis avant toute automatisation |

### Contradictions

- La reponse classe certains documents comme `toujours` sans citer la source.
- Le depot de capital est cite comme document toujours attendu, mais aucune
  source ou spec projet n'est encore rattachee dans la reponse.
- La demande d'inscription a l'Ordre est citee comme toujours attendue pour les
  professions reglementees, mais NotebookLM signale aussi des variantes
  departementales.
- Le questionnaire par profession est dit non requis pour les dentistes, mais
  aucune source n'est citee.

### Informations non trouvees

- Sources exactes des documents.
- Source ou statut exact de l'attestation de depot de capital.
- Liste de variables structuree.
- Statut manuel/reserve precis des cessions, bail et SCM.
- Regles de gouvernance SELAS detaillees.
- Presence ou absence du directeur general en V1.
- Seuils de limitation de pouvoirs du president.
- Pieces ordinales bloquantes.

### Impact sur le sprint

Le sprint reste en Phase 3 - NOTEBOOKLM / `NO-GO dev`.

Prompt 01 apporte un premier inventaire mais il n'est pas suffisant pour lancer
l'audit de reutilisation ni la matrice documentaire finale, car les sources ne
sont pas citees. Il faut maintenant cibler les differences SELARL / SELAS pour
eviter une transposition abusive du travail SELARL.

### Prochain prompt recommande

Prompt 02 - Differences SELARL / SELAS.

## Reponse NotebookLM SELAS 02

Date : 2026-06-01
Prompt utilise : Prompt 02 - Differences SELARL / SELAS
Source NotebookLM / indices cites : la reponse indique etre basee sur les
sources NotebookLM, mais les champs `Source` sont vides. Cette reponse est donc
une matiere d'analyse utile, sans valeur de validation juridique ou documentaire.

### Synthese fiable

NotebookLM confirme les grands axes de difference entre SELARL et SELAS :
direction, nature du capital, terminologie des porteurs de droits, modele de
statuts, formalisme des decisions, ordre professionnel et regime communautaire.

Le point le plus sensible est la transposition du travail SELARL : les termes
`gerant`, `parts sociales` et certains PV ou actes de cession ne peuvent pas
etre recopies tels quels vers la SELAS.

### Documents identifies

| Document | Condition | Statut | Source | Incertitude |
| --- | --- | --- | --- | --- |
| PV de nomination / decision de nomination | Selon nomination dans les statuts et nombre d'associes | Conditionnel | Non citee | Transformer `gerant` en `president`, verifier le formalisme SELASU / SELAS pluripersonnelle |
| Statuts SELAS | Creation SELAS | Toujours | Non citee | Articles differents non listes exhaustivement |
| Procuration | Formalites | Toujours ou a verifier | Non citee | Mentions de signature impactees par `president` |
| Demande d'inscription a l'ordre | Profession reglementee | Toujours ou conditionnel selon cas ordinal | Non citee | Aucune preuve d'un document different uniquement parce que SELAS |
| Regime communautaire / renonciation conjoint | Mariage sous regime de communaute | Conditionnel | Non citee | Effet exact de la SELAS sur la revendication du conjoint non trouve |
| Actes de cession | Si cession de titres ou fonds | Conditionnel | Non citee | `cession de parts` vs `cession d'actions` a traiter avec prudence |

### Conditions et exclusions

- Le role de dirigeant change : `gerant` en SELARL, `president` en SELAS.
- Le directeur general n'est pas trouve pour les SELAS unipersonnelles dans la
  reponse.
- Le capital passe de `parts sociales` a `actions`.
- La reponse ne confirme pas une obligation de remplacer partout `associe` par
  `actionnaire`, notamment dans l'interface.
- Le formalisme varie selon associe unique ou pluralite d'associes.
- Les contraintes ordinales semblent transverses mais doivent refleter la forme
  sociale choisie.
- Le regime communautaire reste une condition transverse selon la reponse, mais
  l'effet juridique precis en SELAS n'est pas trouve.

### Variables / donnees a saisir

- forme sociale : SELARL ou SELAS ;
- role du dirigeant : gerant / president / directeur general eventuel ;
- nomination du president dans les statuts ou par acte separe ;
- nombre d'associes / actionnaires ;
- associe unique ou pluralite ;
- nature du capital : parts sociales / actions ;
- numerotation des actions ;
- profession et ordre competent ;
- regime matrimonial ;
- option communaute ;
- documents ordinaux complementaires.

### Differences SELARL / SELAS

| Sujet | Difference indiquee | Impact documentaire | Non trouve / verification |
| --- | --- | --- | --- |
| Gerant / president / directeur general | SELARL = gerant ; SELAS = president | PV de nomination, statuts, procuration, signatures, front | Directeur general non trouve pour SELAS unipersonnelle |
| Parts sociales / actions | SELARL = parts sociales ; SELAS = actions | Article capital, actes de cession, variables capital/titres | Numerotation des actions non detaillee |
| Associe / actionnaire | `associe` reste parfois terme generique ; SELAS repose techniquement sur actionnaires | Wording UI et documents a verrouiller | Pas d'instruction de remplacement systematique dans le front |
| Statuts | Modeles distincts SELARL / SELAS | Choix de modele selon forme sociale et profession | Liste exhaustive des articles differents non trouvee |
| PV ou decisions | Associe unique = formalisme plus leger ; plusieurs associes = PV assemblee | Titre et resolutions a adapter | Aucun PV uniquement SELAS identifie |
| Ordre professionnel | Contraintes ordinales transverses mais forme sociale a mentionner | Demande d'inscription a l'ordre | Pas de preuve d'un document different uniquement pour SELAS |
| Regime communautaire | Condition liee au mariage / communaute | Lettre de renonciation ou document conjoint | Effet specifique SAS/SELAS sur qualite d'associe du conjoint non trouve |

### Reutilisation possible

| Element | Decision provisoire | Justification | Verification requise |
| --- | --- | --- | --- |
| DOC-004 PV nomination gerant | adapter/no-go | Role `gerant` incompatible avec `president` sans adaptation | Source PV president SELAS et conditions de nomination |
| Statuts SELARL medecin/dentiste | no-go pour copie directe | Modele distinct SELAS, articles differents non listes | Source statuts SELAS et analyse article par article |
| Variables capital SELARL | adapter | `parts sociales` devient `actions` | Numerotation, valeur nominale, droits de vote, wording |
| Modele de roles front | adapter | Role dirigeant commun mais libelle juridique change | Mapping gerant/president/DG eventuel |
| DOC-034 ordre | reuse-check | Ordre professionnel semble transverse | Overlay forme sociale SELAS et profession |
| DOC-005/DOC-006 regime communautaire | reuse-check/no-go | Condition communaute citee comme transverse | Effet juridique propre aux SAS/SELAS non trouve |

### Contradictions

- La reponse annonce une comparaison selon les sources, mais ne cite aucune
  source.
- Elle distingue techniquement `actionnaire`, tout en disant que `associe` reste
  souvent generique dans les fiches de saisie.
- Elle dit que l'ordre professionnel applique des contraintes similaires, mais
  mentionne des documents complementaires sans les relier a une source.
- Elle indique une lettre de renonciation en regime communautaire, tout en
  signalant que l'effet specifique SELAS/SAS n'est pas trouve.

### Informations non trouvees

- Source precise de chaque difference.
- Directeur general en SELAS unipersonnelle.
- Regle de numerotation des actions.
- Instruction explicite `associe` / `actionnaire` pour le front et les documents.
- Liste exhaustive des articles differents entre statuts SELARL et SELAS.
- Document PV propre uniquement a la SELAS.
- Document ordinal different uniquement parce que la forme est SELAS.
- Effet juridique de la SELAS sur la revendication du conjoint en regime
  communautaire.

### Impact sur le sprint

Le sprint reste en Phase 3 - NOTEBOOKLM / `NO-GO dev`.

Prompt 02 confirme que la SELAS ne peut pas etre traitee comme une simple
declinaison lexicale de la SELARL. Les zones a creuser avant toute reutilisation
sont la gouvernance, les statuts, les actions, le formalisme des decisions et le
regime communautaire.

### Prochain prompt recommande

Prompt 03 - Gouvernance et statuts SELAS.

## Reponse NotebookLM SELAS 03

Date : 2026-06-01
Prompt utilise : Prompt 03 - Gouvernance et statuts SELAS
Source NotebookLM / indices cites : la reponse indique etre basee sur les
sources fournies, mais les champs `Source` sont vides ou `-`. Cette reponse est
donc une matiere d'analyse utile, sans valeur de validation juridique ou
documentaire.

### Synthese fiable

NotebookLM isole les sujets structurants de la gouvernance SELAS : president,
directeur general non trouve, actionnaires, decisions collectives, capital,
actions, signature et annexes ordinales.

La reponse confirme un sous-cas simple V1 plausible : SELAS / SELASU avec
president associe ou actionnaire unique, capital simple et decision de l'associe
unique. Les cas a bloquer provisoirement sont les tiers non exercants, personnes
morales complexes, droits de vote ou majorites derogatoires, numerotation
complexe des actions et dossiers ordinaux sans plans/devis lorsque ces pieces
sont exigees.

### Documents identifies

| Document | Condition | Statut | Source | Incertitude |
| --- | --- | --- | --- | --- |
| Statuts SELAS | Creation SELAS | Toujours | Non citee | Articles et clauses detaillees non cites |
| PV de nomination / decision president | Selon nomination du president et forme associe unique/pluralite | Conditionnel | Non citee | Forme exacte de l'acte et source president a confirmer |
| Procuration | Formalites | Toujours ou a verifier | Non citee | Signature par president a confirmer dans source |
| Fiche societe / liste des actionnaires | Constitution du dossier | A traiter | Non citee | `associe` vs `actionnaire` a arbitrer |
| PV d'assemblee ou decision de l'associe unique | Selon pluralite d'actionnaires | Conditionnel | Non citee | Quorum/majorite et clauses derogatoires non trouves |
| Attestation de depot de capital | Constitution avec capital | A verifier | Non citee | Statut documentaire et source non confirmes |
| Registre des mouvements de titres | Actions / mouvements de titres | A verifier | Non citee | Presence dans perimetre creation non confirmee |
| Dossier d'inscription a l'Ordre | Profession reglementee | A verifier | Non citee | Plans et devis peuvent etre bloquants selon Ordre |

### Conditions et exclusions

- President : dirigeant obligatoire selon la reponse ; remplace `gerant`.
- Directeur general : non trouve dans les sources de la reponse.
- Actionnaires : capital detenu par des actionnaires ; les fiches de saisie
  peuvent encore employer `associe` par defaut.
- Decisions : `decision` en associe/actionnaire unique ; `PV d'assemblee` en
  pluralite.
- Capital : montant a fixer des la creation.
- Actions : nombre d'actions et valeur nominale gerables en cas simple.
- Signature : signature electronique apres validation des projets selon la
  reponse.
- Annexes : plans des locaux et devis de materiel peuvent etre exiges par
  certains Ordres.
- Cas a bloquer provisoirement : tiers non exercants, personnes morales
  complexes, clauses de majorite derogatoires, droits de vote specifiques,
  numerotation complexe des actions, dossier ordinal sans pieces exigees.

### Variables / donnees a saisir

- president : civilite, prenom, nom, accord de genre ;
- directeur general : non trouve, a ne pas activer sans source ;
- actionnaires : identite complete, regime matrimonial ;
- decisions collectives : date de reunion, quorum, majorite ;
- capital : montant en euros ;
- actions : nombre d'actions, valeur nominale ;
- signature : e-mail du signataire, numero de portable ;
- annexes ordre : plans PDF, devis de materiel ;
- DNC president : filiation complete a verifier, signalee comme question
  ouverte.

### Differences SELARL / SELAS

- Le role `gerant` ne doit pas etre reutilise tel quel : le role SELAS est
  `president`.
- Les porteurs du capital sont presentes comme `actionnaires`, meme si le front
  ou les fiches peuvent utiliser `associe`.
- Les statuts SELAS doivent gerer capital en actions, non en parts sociales.
- Le formalisme de decision depend du nombre d'actionnaires.
- Les droits specifiques ou clauses derogatoires semblent hors sous-cas simple.

### Reutilisation possible

| Element | Decision provisoire | Justification | Verification requise |
| --- | --- | --- | --- |
| Modele role dirigeant | adapter | `president` remplace `gerant` | Source SELAS et mapping front/document |
| DOC-004 PV nomination gerant | adapter/no-go | L'acte proche existe mais role et titre changent | Source PV/decision president SELAS |
| Statuts SELARL | no-go copie directe | Gouvernance, capital et actions divergent | Source statuts SELAS et analyse article par article |
| Capital / valeur nominale | adapter | Logique montant/valeur peut etre reutilisable, mais vocabulaire change | Actions, droits de vote et numerotation |
| Signature | reuse-check | Donnees e-mail/telephone peuvent etre transverses | Source signature et statut dans le flux cabinet |
| Annexes ordre | reuse-check/no-go | Pieces ordinales transverses possibles | Liste exacte par profession/ordre |

### Contradictions

- La reponse parle de sources fournies mais ne cite aucune source precise.
- Le president est presente comme obligatoire, mais la source exacte n'est pas
  fournie.
- Le capital est dit mis a jour automatiquement lors des augmentations, alors
  que le sprint SELAS en est encore a la creation.
- Le registre des mouvements de titres est cite sans confirmation de son statut
  dans le dossier de creation.
- Les plans/devis sont presentes comme possibles exigences ordinales, mais sans
  precision par ordre ou profession.

### Informations non trouvees

- Source precise de chaque regle de gouvernance.
- Directeur general pour SELAS unipersonnelle.
- Seuils d'emprunt ou d'achat de materiel pour limitation des pouvoirs du
  president.
- Droits derogatoires et dissociation actions / droits aux benefices.
- Informations minimales pour actionnaires minoritaires conjoint/enfants.
- Decision UI `associe` vs `actionnaire`.
- Filiation complete requise pour la DNC du president.
- Statut exact de l'attestation de depot de capital et du registre des mouvements
  de titres dans la creation SELAS.

### Impact sur le sprint

Le sprint reste en Phase 3 - NOTEBOOKLM / `NO-GO dev`.

Prompt 03 permet de mieux cerner le plus petit cas SELAS V1 possible :
president/actionnaire unique, capital simple, actions simples, decision de
l'associe unique, sans directeur general, sans droits derogatoires, sans
personnes morales complexes et sans cession complexe.

Avant toute matrice ou audit de reutilisation, il faut maintenant obtenir une
liste structuree des donnees utilisateur a demander, avec obligation,
conditionnalite et reutilisation SELARL possible.

### Prochain prompt recommande

Prompt 04 - Variables et donnees a demander.

## Reponse NotebookLM SELAS 04

Date : 2026-06-01
Prompt utilise : Prompt 04 - Variables et donnees a demander
Source NotebookLM / indices cites : la reponse indique etre fondee sur les
sources, mais ne donne pas de source ou indice source par donnee. Cette reponse
est donc une base de structuration, sans valeur de validation juridique ou
documentaire.

### Synthese fiable

NotebookLM presente les donnees SELAS comme tres proches de la SELARL, avec des
ajustements terminologiques critiques :

- `president` au lieu de `gerant` ;
- `actions` au lieu de `parts` ;
- `actionnaire` a verifier face au terme generique `associe`.

La reponse structure les donnees en huit blocs : client/praticien, societe,
gouvernance, capital/actions, siege/exercice, ordre professionnel, conjoint /
regime communautaire et signature.

### Documents identifies

| Document | Condition | Statut | Source | Incertitude |
| --- | --- | --- | --- | --- |
| Statuts SELAS | Creation SELAS | Toujours | Non citee | Variables proches SELARL mais wording SELAS a verifier |
| DNC president | Dirigeant personne physique | Toujours ou a verifier | Non citee | Filiation complete non confirmee |
| PV de nomination / decision president | Selon nomination du president | Conditionnel | Non citee | Wording president et forme decision/PV a verifier |
| Attestation de depot de capital | Constitution avec depot | A verifier | Non citee | Banque nom/adresse citee, statut documentaire non confirme |
| Fiche societe | Constitution dossier | A traiter | Non citee | Fiscalite, capital, repartition, forme SELAS |
| Dossier Ordre | Profession reglementee | A verifier | Non citee | Plans/devis obligatoires selon conseil departemental, source non citee |
| Regime communautaire / renonciation conjoint | Mariage communaute | Conditionnel | Non citee | Effet SELAS sur conjoint non tranche |
| Procuration / Ordre | Mandataire / juriste | A verifier | Non citee | Initiales mandataire citees comme donnee interne |

### Conditions et exclusions

- La majorite des donnees sont presentees comme reutilisables depuis SELARL, mais
  cela reste a verifier par audit de reutilisation.
- Les droits de vote et droits financiers sont conditionnels si derogatoires au
  capital.
- Les autres lieux d'exercice declenchent une demande de derogation selon la
  reponse.
- Plans des locaux et devis materiel peuvent etre obligatoires selon les
  exigences du Conseil Departemental de l'Ordre.
- Le conjoint est conditionnel si mariage sous regime de communaute.
- Les relances automatiques de pieces manquantes sont mentionnees comme question,
  hors generation documentaire directe a ce stade.

### Variables / donnees a saisir

| Bloc | Donnee | Obligation selon reponse | Document concerne | Reutilisation SELARL indiquee |
| --- | --- | --- | --- | --- |
| Client / praticien | Nom et prenom | Obligatoire | Tous les actes | Reutilisable |
| Client / praticien | Date et lieu de naissance | Obligatoire | Statuts, DNC | Reutilisable |
| Client / praticien | Nationalite | Obligatoire | Statuts | Reutilisable |
| Client / praticien | Adresse de domicile | Obligatoire | Fiche client, etat civil | Reutilisable |
| Client / praticien | Sexe | Obligatoire | Accords de genre | Reutilisable |
| Client / praticien | Numero de securite sociale | Obligatoire | Fiche client | Reutilisable |
| Client / praticien | Numero de portable | Obligatoire | Signature electronique | Reutilisable |
| Societe | Denomination sociale | Obligatoire | Tous les actes | Reutilisable |
| Societe | Forme sociale | Obligatoire | Tous les actes | Champ existant |
| Societe | Objet social / profession | Obligatoire | Statuts | Reutilisable |
| Societe | Fiscalite IS/IR | Obligatoire | Fiche societe | Reutilisable |
| Societe | Date de cloture de l'exercice | Obligatoire | Statuts | Reutilisable |
| Gouvernance | Identite du president | Obligatoire | PV de nomination, statuts | Reutilisable avec changement `gerant` -> `president` |
| Gouvernance | Identite des actionnaires | Obligatoire | Statuts, repartition | Reutilisable avec changement `associe` -> `actionnaire` |
| Gouvernance | Qualite de l'actionnaire | Obligatoire | Statuts / gouvernance | Reutilisable |
| Capital / actions | Montant du capital social | Obligatoire | Statuts, attestation de depot | Reutilisable |
| Capital / actions | Nombre d'actions | Obligatoire | Statuts | Reutilisable avec changement `parts` -> `actions` |
| Capital / actions | Valeur nominale de l'action | Obligatoire | Calcul capital | Reutilisable |
| Capital / actions | Repartition du capital | Obligatoire | Statuts, fiche societe | Reutilisable |
| Capital / actions | Droits de vote et financiers | Conditionnel | Statuts | Reutilisable a verifier |
| Capital / actions | Banque de depot nom/adresse | Obligatoire | Attestation capital | Reutilisable |
| Siege / exercice | Adresse du siege social | Obligatoire | Statuts, Kbis | Reutilisable |
| Siege / exercice | Autres lieux d'exercice | Conditionnel | Derogation multi-sites | Reutilisable |
| Ordre professionnel | Numero RPPS | Obligatoire | Statuts, dossier Ordre | Reutilisable |
| Ordre professionnel | Numero d'inscription a l'Ordre | Obligatoire | Fiche client | Reutilisable |
| Ordre professionnel | Lieu d'inscription de l'Ordre | Obligatoire | Envoi dossier | Reutilisable |
| Ordre professionnel | Plans des locaux et devis materiel | Obligatoire selon Ordre | Dossier Ordre | Reutilisable a verifier |
| Conjoint / regime communautaire | Statut matrimonial | Obligatoire | Etat civil | Reutilisable |
| Conjoint / regime communautaire | Regime matrimonial | Obligatoire | Regime communautaire | Reutilisable |
| Conjoint / regime communautaire | Nom du conjoint | Conditionnel | Renonciation / conjoint | Reutilisable |
| Signature | E-mail de signature | Obligatoire | Signature electronique | Reutilisable |
| Signature | Initiales du mandataire / juriste | Obligatoire | Procuration et Ordre | Reutilisable |

### Differences SELARL / SELAS

- Les donnees de gouvernance doivent basculer de `gerant` a `president`.
- Les donnees de capital doivent basculer de `parts` a `actions`.
- L'identite des porteurs du capital est presentee comme `actionnaires`, avec un
  risque de vocabulaire si l'interface garde `associes`.
- Les droits de vote / droits financiers derogatoires sont conditionnels et
  risquent de sortir du cas simple V1.
- Le regime communautaire est repris comme transverse, mais l'effet propre de la
  SELAS n'est toujours pas valide.

### Reutilisation possible

| Element | Decision provisoire | Justification | Verification requise |
| --- | --- | --- | --- |
| Etat civil praticien | reuse-check | Donnees classiques deja SELARL | Verifier filiation DNC president et champs exacts |
| Societe / denomination / siege | reuse-check | Donnees probablement transverses | Verifier statuts SELAS et ordre |
| Gouvernance SELARL | adapter | Role dirigeant change | Mapping president / gerant et source president |
| Capital SELARL | adapter | Logique reutilisable mais `actions` remplace `parts` | Wording statuts, numerotation, droits |
| Ordre professionnel | reuse-check | Donnees RPPS/ordre transverses probables | Source SELAS et profession |
| Regime communautaire | reuse-check/no-go | Donnees conjoint reutilisables en apparence | Effet SELAS sur renonciation conjoint |
| Signature electronique | reuse-check | Donnees e-mail/telephone probablement transverses | Confirmer flux signature dans scope moteur |
| Initiales mandataire | reuse-check | Donnee interne deja proche | Verifier usage exact procuration/ordre SELAS |

### Contradictions

- La reponse annonce une liste exhaustive selon les sources, mais aucune source
  n'est citee par donnee.
- Des donnees sont marquees obligatoires pour tous les actes alors que leur
  obligation peut dependre du document, du sous-cas ou de l'Ordre.
- Plans/devis sont dits obligatoires selon l'Ordre, mais sans identifier l'Ordre
  ou la profession concernes.
- Les droits de vote et financiers sont indiques reutilisables alors qu'ils sont
  aussi potentiellement derogatoires et dangereux pour V1.
- Banque de depot est rattachee a une attestation de capital dont le statut
  documentaire reste a confirmer dans le sprint.

### Informations non trouvees

- Source precise de chaque donnee obligatoire.
- Regle de numerotation des actions.
- Decision V1 sur actions de preference / droits non proportionnels.
- Bloc filiales et participations.
- Filiation DNC du president.
- Regle de relance des pieces ordinales manquantes.
- Decision UI definitive `associe` / `actionnaire`.
- Statut exact de l'attestation de depot de capital dans le moteur.

### Impact sur le sprint

Le sprint reste en Phase 3 - NOTEBOOKLM / `NO-GO dev`.

Prompt 04 donne une premiere base de formulaire SELAS, mais il ne suffit pas a
ouvrir un audit ou un ticket de dev sans confrontation aux sources et au travail
SELARL existant. La prochaine etape logique est d'identifier les documents SELAS
identiques ou proches de la SELARL, avec decision `identique`, `reuse-check`,
`adapter` ou `no-go`.

### Prochain prompt recommande

Prompt 05 - Documents deja proches de SELARL.

## Reponse NotebookLM SELAS 05

Date : 2026-06-01
Prompt utilise : Prompt 05 - Documents deja proches de SELARL
Source NotebookLM / indices cites : la reponse se refere aux rendez-vous et
documents de travail du NotebookLM, mais les champs `Source` du tableau sont
vides. Cette reponse est donc une base de comparaison et de tri de risque, sans
valeur de validation juridique ou documentaire.

### Synthese fiable

NotebookLM identifie plusieurs documents SELAS proches des documents SELARL :
procuration, statuts, DNC, demande d'inscription a l'Ordre, attestation de
domiciliation, PV de nomination et attestation sur le capital.

Le message central est prudent : certains documents appartiennent a un socle
transversal, mais la SELAS n'est pas une simple copie de la SELARL. Les statuts,
la gouvernance et les titres de capital imposent des adaptations fortes.

Attention : la reponse propose un "levier de transformation automatique" par
remplacement de chaines (`parts` -> `actions`, `gerant` -> `president`). Dans le
cadre du projet, cela doit etre traite comme un risque et non comme une regle de
generation validee : aucun wording juridique ne doit etre modifie par simple
substitution globale sans source et spec.

### Documents identifies

| Document | Condition | Statut | Source | Incertitude |
| --- | --- | --- | --- | --- |
| Procuration SELAS | Formalites / mandat | Adapter | Non citee | `gerant` -> `president`, mandataire par defaut a verifier |
| Statuts SELAS | Creation SELAS | Adapter | Non citee | Statuts tres differents, clauses ordinales et actions a verifier |
| DNC president | Dirigeant personne physique | Reuse-check | Non citee | Filiation et fonction president a verifier |
| Demande d'inscription a l'Ordre | Profession reglementee | Reuse-check | Non citee | Formulaire departemental et forme SELAS a verifier |
| Attestation de domiciliation | Siege / domiciliation | Identique selon reponse | Non citee | Neutralite juridique a confirmer par source |
| PV de nomination president | Nomination dirigeant | Adapter | Non citee | Modalites unipersonnel/pluripersonnel et role president |
| Attestation sur le capital | Depot de capital | Reuse-check | Non citee | Division en actions et variables de titres a verifier |

### Conditions et exclusions

- Procuration : proche SELARL, mais risque eleve si le role dirigeant reste
  `gerant`.
- Statuts : proche seulement sur certains champs de dossier ; pas reutilisable
  par copie directe.
- DNC : document centre sur la personne physique, probablement reutilisable apres
  verification de la fonction et de la filiation.
- Ordre : informations professionnelles transverses, mais forme sociale et
  departement peuvent changer le formulaire.
- Domiciliation : presentee comme quasi identique, mais a confirmer.
- PV nomination : acte proche, mais gouvernance differente.
- Capital : montant et banque proches ; division en actions a controler.

### Variables / donnees a saisir

- praticien / president : identite complete ;
- mandataire ;
- siege social ;
- objet social ;
- date de cloture ;
- clauses ordinales par profession ;
- filiation DNC si requise ;
- RPPS / ordre / departement ;
- proprietaire des murs ou titre de domiciliation ;
- date de reunion ou decision ;
- associe unique ou pluralite ;
- banque, agence, montant du capital ;
- nombre d'actions et variables de titres.

### Differences SELARL / SELAS

- Le vocabulaire de gouvernance change : `gerant` ne doit pas survivre dans les
  documents SELAS visant le president.
- Les statuts sont indiques comme tres differents malgre des champs communs.
- Les titres de capital changent : `parts sociales` / `cession de parts` vers
  `actions` / `cession d'actions`.
- La demande d'ordre doit mentionner la forme SELAS.
- Le PV de nomination doit tenir compte du role president et du formalisme
  associe unique / pluralite.

### Reutilisation possible

| Element | Decision provisoire | Justification | Verification requise |
| --- | --- | --- | --- |
| Procuration SELARL | adapter | Mandat et identite proches, gouvernance differente | Source procuration SELAS, role president, mandataire |
| Statuts SELARL | adapter/no-go | Champs communs mais base documentaire differente | Source statuts SELAS, analyse article par article |
| DNC SELARL | reuse-check | Centree sur personne physique | Fonction president, filiation, source greffe |
| Demande Ordre SELARL | reuse-check | Donnees pro transverses | Forme SELAS, profession, departement |
| Attestation domiciliation | identique provisoire / reuse-check | Reponse indique document neutre | Source et absence de wording SELARL |
| PV nomination gerant | adapter | Date/reunion proches mais role change | Source PV president/decision SELAS |
| Attestation capital | reuse-check | Banque/montant proches | Actions, titres, source attestation |

### Contradictions

- La reponse classe l'attestation de domiciliation en `identique`, mais ne cite
  aucune source.
- Elle presente les substitutions de chaines comme levier automatique, alors que
  les statuts sont aussi decrits comme tres differents.
- Elle signale un risque critique de copie pour les statuts tout en les classant
  `adapter`, ce qui impose une analyse source avant reuse.
- Elle parle d'un "pot commun" pour procuration et DNC, mais la procuration est
  aussi classee a risque eleve a cause du role president.

### Informations non trouvees

- Sources precises de chaque classification.
- Source de la procuration SELAS.
- Source du PV ou de la decision president SELAS.
- Source de l'attestation sur le capital SELAS.
- Statut exact de l'attestation de domiciliation comme document identique.
- Regles de filiation DNC president.
- Regles de formulaire Ordre par departement et profession.
- Clauses specifiques aux actions de preference.

### Impact sur le sprint

Le sprint reste en Phase 3 - NOTEBOOKLM / `NO-GO dev`.

Prompt 05 confirme que la reutilisation SELARL devra etre auditee document par
document. Les decisions provisoires issues de NotebookLM ne suffisent pas a
lancer l'audit formel ni une matrice finale, car les sources ne sont pas citees.
Le prochain prompt doit isoler les cas conditionnels et dangereux avant de
preparer l'audit de reutilisation et la matrice.

### Prochain prompt recommande

Prompt 06 - Cas conditionnels et blocages.

## Reponse NotebookLM SELAS 06

Date : 2026-06-01
Prompt utilise : Prompt 06 - Cas conditionnels et blocages
Source NotebookLM / indices cites : la reponse se refere aux ateliers d'audit et
de cartographie, mais les champs `Source` du tableau sont vides ou `-`. Cette
reponse est donc une base de tri des risques, sans valeur de validation
juridique ou documentaire.

### Synthese fiable

NotebookLM classe les principaux cas conditionnels SELAS :

- regime communautaire ;
- cession de cabinet / fonds liberal ;
- SCM ;
- derogation / site distinct ;
- multi-actionnaires ;
- directeur general ;
- origine de propriete.

La reponse aide a distinguer un cas simple V1 d'un perimetre dangereux. Les
propositions `automatisable`, `automatisable via API` ou `hybride` restent
provisoires : elles ne valent ni source recue, ni spec, ni `GO dev`.

### Documents identifies

| Document | Condition | Statut | Source | Incertitude |
| --- | --- | --- | --- | --- |
| Lettre d'avertissement conjoint | Mariage + regime communaute | Automatisable selon reponse | Non citee | Effet propre SELAS toujours non valide |
| Acte de renonciation conjoint | Mariage + regime communaute | Automatisable selon reponse | Non citee | Source SELAS et wording a verifier |
| Acte de cession de fonds liberal | Passage BNC vers societe | Hybride / brouillon Word | Non citee | Redaction personnalisee, risque juridique fort |
| Avenant au bail | Cession de fonds / transfert bail | Hybride / a verifier | Non citee | Redacteur et source non confirmes |
| Acte de cession de parts SCM | Praticien membre d'une SCM | Automatisable via API selon reponse | Non citee | API Pappers non validee dans moteur, source/conditions a cadrer |
| Demande de derogation a l'Ordre | Deuxieme lieu d'exercice | Conditionnel UI | Non citee | Forme exacte et donnees par Ordre a verifier |
| Statuts / PV assemblee | Multi-actionnaires | Dangereux / vigilance | Non citee | Accords, numerotation actions, droits de vote/financiers |
| Directeur general | Non trouve | Non trouve | Non citee | Ne pas activer sans source |
| Clauses d'origine de propriete | Fonds rachete | Manuel selon reponse | Non citee | Rédaction automatique dangereuse |

### Conditions et exclusions

- Regime communautaire : declenche par mariage + communaute ; peut rendre le
  bloc conjoint obligatoire selon la reponse.
- Cession cabinet/fonds : declenchee par passage BNC vers societe ; redaction
  personnalisee, a exclure du cas simple.
- SCM : declenchee par appartenance a une SCM ; donnees SCM et associes requis.
- Derogation / site distinct : declenchee par deuxieme lieu d'exercice ; champ
  cache par defaut suggere pour ne pas alourdir le parcours.
- Multi-actionnaires : declenche par plus d'un actionnaire ; vigilance sur
  accords, genre, pluriel, numerotation et droits.
- Directeur general : non trouve ; doit rester bloque.
- Origine de propriete : fonds rachete et non cree ; manuel selon reponse.

### Variables / donnees a saisir

- conjoint : nom, regime matrimonial ;
- cession fonds : prix, cédant, cessionnaire, origine de propriete ;
- SCM : Siren SCM, capital SCM, liste des associes SCM ;
- site distinct : adresse secondaire, forme d'exercice ;
- multi-actionnaires : repartition du capital, droits de vote, droits
  financiers, numerotation des actions ;
- origine de propriete : details de l'acte d'achat initial ;
- pieces Ordre : plans et devis, si rendus bloquants par arbitrage.

### Differences SELARL / SELAS

- Multi-actionnaires SELAS semble plus sensible que le cas simple : actions,
  numerotation, droits de vote et droits financiers peuvent diverger du capital.
- Les cessions doivent distinguer cession de fonds, cession de parts SCM et
  eventuelle logique d'actions SELAS.
- Le directeur general reste proprement non trouve : pas de reprise par analogie.
- Les clauses d'origine de propriete ne doivent pas etre generees par simple case
  ou substitution.

### Reutilisation possible

| Element | Decision provisoire | Justification | Verification requise |
| --- | --- | --- | --- |
| Regime communautaire | reuse-check/no-go | Cas standardise selon reponse | Source SELAS, effet conjoint, wording |
| Cession cabinet/fonds | no-go / manuel | Redaction personnalisee et origine de propriete complexe | Source, spec et arbitrage humain |
| SCM | no-go provisoire | Automatisation API evoquee mais non cadree | Source SCM, API, donnees, RGPD/fiabilite |
| Site distinct / derogation | reuse-check | Cas deja connu cote SELARL/ordre | Source SELAS, formulaire exact, UI conditionnelle |
| Multi-actionnaires | no-go provisoire | Accords, actions, droits et numerotation complexes | Sous-cas borne et source statuts |
| Directeur general | no-go | Non trouve | Source explicite requise |
| Origine de propriete | manuel/no-go | Redaction automatique dangereuse | Decision humaine et source detaillee |

### Contradictions

- La reponse classe le regime communautaire en `automatisable`, mais les prompts
  precedents signalaient que l'effet juridique propre SELAS/SAS n'etait pas
  trouve.
- La SCM est dite `automatisable via API`, mais aucune source projet ne valide
  l'appel API ni les donnees recuperees.
- Le prompt demandait les documents a remplir a la main ; la reponse identifie
  surtout origine de propriete comme manuel, mais ne donne pas de liste complete
  des documents manuels.
- Les seuils de pouvoirs sont mentionnes dans les questions, mais pas resolus
  dans le tableau.

### Informations non trouvees

- Sources exactes par cas.
- Liste complete des documents manuels SELAS.
- Decision V1 sur blocage des fonds non pure creation.
- Regles de numerotation des actions en demembrement ou droits derogatoires.
- Blocage obligatoire ou non des plans/devis dans le formulaire.
- Seuils par defaut de limitation des pouvoirs du president.
- Workflow de relecture humaine avant signature.
- Conditions exactes d'automatisation SCM/API.

### Impact sur le sprint

Le sprint reste en Phase 3 - NOTEBOOKLM / `NO-GO dev`.

Prompt 06 clarifie le perimetre prudent :

- cas simple V1 possible : creation SELAS simple, president/actionnaire unique,
  capital simple, sans DG, sans droits derogatoires, sans cession, sans SCM ;
- cas a bloquer ou cadrer : cession, origine de propriete, SCM/API,
  multi-actionnaires, DG, actions complexes, droits derogatoires ;
- cas a verifier : regime communautaire, site distinct, pieces ordinales.

La prochaine etape NotebookLM doit porter sur la recette et la validation
humaine afin de savoir quels scenarios tester, quels documents relire et quels
points de wording juridique surveiller.

### Prochain prompt recommande

Prompt 07 - Recette et validation humaine.

## Reponse NotebookLM SELAS 07

Date : 2026-06-01
Prompt utilise : Prompt 07 - Recette et validation humaine
Source NotebookLM / indices cites : la reponse indique etre basee exclusivement
sur les besoins et processus decrits dans les sources, mais ne cite pas de
source precise par scenario ou document. Cette reponse est donc une base de
recette, sans valeur de validation juridique ou documentaire.

### Synthese fiable

NotebookLM propose un protocole de validation SELAS autour de :

- un scenario simple minimal de creation ex nihilo ;
- des scenarios conditionnels ;
- des comparaisons ligne par ligne ;
- des revues humaines par associe ou juriste ;
- des points de wording sensibles ;
- des criteres de sprint complet.

La reponse confirme un axe de recette important : le moteur devra prouver
l'absence de termes SELARL residuels (`gerant`, `parts`) et la bonne adaptation
aux termes SELAS (`president`, `actions`). Elle ne suffit pas encore a valider le
perimetre, car les sources restent non citees et certains criteres sont
quantitatifs ou produits sans preuve source, notamment `90 % des situations
courantes`.

### Documents identifies

| Document | Condition | Statut | Source | Incertitude |
| --- | --- | --- | --- | --- |
| Statuts SELAS | Scenario simple medecin/dentiste | A comparer ligne par ligne | Non citee | Modele source SELAS a identifier |
| PV de nomination president | Nomination dirigeant | A comparer ligne par ligne | Non citee | Decision associe unique vs PV assemblee |
| Procuration | Formalites | A comparer ligne par ligne | Non citee | Mandataire et role president |
| DNC president | Dirigeant personne physique | Dans lot complet | Non citee | Filiation non trouvee |
| Demande a l'Ordre | Profession reglementee | Dans lot complet | Non citee | Pieces ordinales et variantes profession/departement |
| Documents regime communautaire | Mariage communaute | Scenario conditionnel | Non citee | Effet SELAS sur conjoint a verifier |
| Demande de derogation | Deuxieme lieu d'exercice | Scenario conditionnel | Non citee | Formulaire exact a verifier |
| Acte cession parts SCM | Membre d'une SCM | Scenario conditionnel | Non citee | Source et donnees SCM a cadrer |
| Cession fonds liberal | Cession / achat fonds | Revue humaine / brouillon | Non citee | Redaction ultra-personnalisee |
| Clauses origine de propriete | Achat fonds | Revue humaine / manuel | Non citee | Source et details acte initial requis |

### Conditions et exclusions

- Scenario simple minimal : praticien medecin ou dentiste, installation seule,
  associe/actionnaire unique, capital 1 000 euros, siege defini.
- Scenarios conditionnels : regime communautaire, multi-associes/actionnaires,
  deuxieme lieu d'exercice, membre SCM, origine de propriete achat vs creation.
- Documents a revue humaine : cession de fonds liberal, repartition derogatoire,
  origine de propriete complexe.
- Points wording sensibles : feminisation, pluralisation, numerotation des
  actions, dates.
- Directeur general : non trouve.
- Nombre d'exemplaires en lettres : non trouve.

### Variables / donnees a saisir

- profession : medecin ou dentiste ;
- identite complete praticien / president ;
- capital : exemple 1 000 euros dans le scenario ;
- siege social ;
- regime matrimonial ;
- nombre d'actionnaires ;
- deuxieme lieu d'exercice ;
- appartenance SCM ;
- origine de propriete : creation ou achat ;
- cession fonds : donnees a revue humaine ;
- droits financiers / droits de vote derogatoires ;
- sexe du praticien pour feminisation ;
- date de reunion, possiblement date du jour par defaut ;
- numerotation des actions.

### Differences SELARL / SELAS

- Le scenario minimal doit verifier `president` au lieu de `gerant`.
- Le scenario minimal doit verifier `actions` au lieu de `parts`.
- Les statuts doivent porter `Societe d'exercice liberal par actions simplifiee`.
- L'article capital doit etre exprime en actions.
- Le PV doit nommer un president.
- L'attestation sur le capital doit verifier la division en actions.

### Reutilisation possible

| Element | Decision provisoire | Justification | Verification requise |
| --- | --- | --- | --- |
| Scenario simple SELARL | adapter | Meme logique de lot, mais role/titres changent | Sources SELAS et expected docs |
| Tests wording anti-regression | reuse-check | Controle des termes residuels utile | Liste termes interdits SELAS |
| Tests feminisation/pluralisation | reuse-check | Deja critique cote SELARL | Cas SELAS et wording source |
| Smoke DOCX/ZIP | reuse-check | Sortie exploitable attendue | Liste exacte documents SELAS |
| Revue humaine cession/origine | no-go dev | Cas complexes non automatisables sans source | Spec et arbitrage |

### Contradictions

- La reponse demande de comparer les sorties SELAS avec les modeles SELARL
  existants, alors que les prompts precedents rappellent que les statuts SELAS
  peuvent avoir une base documentaire differente.
- Le critere `90 % des situations courantes` est propose sans source ni mesure.
- Le lot complet minimal inclut la demande a l'Ordre, mais les variantes
  departement/profession et pieces ordinales restent non sourcees.
- La reponse mentionne la readiness signature electronique, mais le scope moteur
  documentaire ne valide pas encore un flux de signature.

### Informations non trouvees

- Sources exactes des scenarios de test.
- Source du seuil `90 %`.
- Role directeur general.
- Obligation de generer le nombre d'exemplaires en lettres.
- Liste exacte des documents du lot minimal SELAS par profession.
- Source de la DNC president et filiation.
- Source des controles de plans/devis et blocage Ordre.
- Workflow de relecture humaine exact avant signature.

### Impact sur le sprint

Le sprint reste en Phase 3 - NOTEBOOKLM / `NO-GO dev`.

Les prompts 01 a 07 donnent une couverture exploratoire utile :

- inventaire documentaire ;
- differences SELARL / SELAS ;
- gouvernance et statuts ;
- variables et donnees ;
- reutilisation SELARL ;
- cas conditionnels et dangereux ;
- recette et revue humaine.

Mais la couverture reste insuffisante pour passer a l'audit de reutilisation ou
a la matrice finale, car les reponses NotebookLM ne citent presque jamais les
sources exploitables. Le prochain prompt doit donc cibler explicitement les
sources/indices par document et par regle, avant tout audit formel.

### Prochain prompt recommande

Prompt de suivi libre - sources et indices exacts.

## Reponse NotebookLM SELAS 08

Date : 2026-06-01
Prompt utilise : Prompt de suivi libre - sources et indices exacts
Source NotebookLM / indices cites : la reponse cite des documents NotebookLM
nommes, notamment `Texte colle`, `Besoins Sydel (juridique).pdf` et `Notre job
- Sydel.pdf`. Les champs d'indice exact contiennent toutefois plusieurs valeurs
illisibles ou vides (`",,"`, `,`, vide), donc la reponse apporte des indices de
source mais pas encore des citations precises.

### Synthese fiable

NotebookLM rattache les principaux points SELAS a trois sources ou indices
sources :

- `Texte colle` ;
- `Besoins Sydel (juridique).pdf` ;
- `Notre job - Sydel.pdf`.

Les points `directeur general`, filiation DNC, actions de preference, blocage
plans/devis et numerotation detaillee des actions restent a arbitrer ou a
source-verifier.

### Documents identifies

| Document | Condition | Statut | Source | Incertitude |
| --- | --- | --- | --- | --- |
| Liste documents SELAS | Creation SELAS | Source trouvee selon NotebookLM | `Texte colle`; `Besoins Sydel (juridique).pdf` | 62 documents annonces, liste exhaustive non reproduite |
| Statuts SELAS medecin | Profession medecin | Source trouvee selon NotebookLM | `Notre job - Sydel.pdf`; `Texte colle` | Modele exact et clauses a extraire |
| Statuts SELAS dentiste | Profession dentiste | Source trouvee selon NotebookLM | `Notre job - Sydel.pdf`; `Texte colle` | Modele exact et priorite V1 a confirmer |
| PV / decision nomination president | Nomination hors statuts | Indice seulement | `Texte colle`; `Besoins Sydel (juridique).pdf` | Source exacte et wording a confirmer |
| Procuration SELAS | Formalites | Source trouvee selon NotebookLM | `Texte colle` | Doit mentionner president |
| DNC president | Dirigeant personne physique | Indice seulement | `Besoins Sydel (juridique).pdf`; `Texte colle` | Filiation non trouvee |
| Demande d'inscription a l'Ordre | SELAS / Ordre | Source trouvee selon NotebookLM | `Texte colle` | Variantes modeles 94/transverses a confirmer |
| Attestation domiciliation | Domiciliation | Source trouvee selon NotebookLM | `Texte colle` | Source exacte vide, statut fusionne a confirmer |
| Attestation depot capital | Depot capital | Source trouvee selon NotebookLM | `Texte colle`; `Besoins Sydel (juridique).pdf` | Role actions / banque / montant |
| Regime communautaire | Mariage + communaute | Source trouvee selon NotebookLM | `Texte colle` | Effet juridique propre SELAS non tranche |
| Cession fonds liberal | Passage BNC vers SEL | Source trouvee selon NotebookLM | `Notre job - Sydel.pdf`; `Texte colle` | Redaction ultra-personnalisee |
| SCM | Membre SCM | Source trouvee selon NotebookLM | `Notre job - Sydel.pdf`; `Texte colle` | API/automatisation non validee |
| Site distinct / derogation | Deuxieme lieu | Source trouvee selon NotebookLM | `Texte colle` | `Cas numero 2` a confirmer |
| Multi-actionnaires | Plusieurs actionnaires | Source trouvee selon NotebookLM | `Texte colle` | Formalisme, pluriel, numerotation |
| Documents a remplir a la main | Origine propriete / tiers cessions | Source trouvee selon NotebookLM | `Notre job - Sydel.pdf`; `Texte colle` | Liste complete non extraite |
| Pieces plans/devis | Ordre / premiere installation | Source trouvee selon NotebookLM | `Texte colle` | Caractere bloquant non tranche |
| Validation humaine | Brouillon Word / relecture juriste | Source trouvee selon NotebookLM | `Texte colle` | Workflow exact a definir |

### Conditions et exclusions

- Le directeur general SELAS est explicitement non trouve.
- La filiation DNC president est un indice seulement : non confirmee comme champ
  de saisie.
- Les documents a remplir a la main concernent au moins l'origine de propriete
  complexe et certains tiers de cession, mais la liste exhaustive reste a
  construire.
- Les plans/devis sont cites comme requis par certains Ordres, mais le caractere
  bloquant UI reste a arbitrer.

### Variables / donnees a saisir

- type de statuts : medecin / dentiste ;
- president ;
- actions et numerotation ;
- conjoint / regime communautaire ;
- cession fonds ;
- SCM ;
- site distinct ;
- multi-actionnaires ;
- pieces ordinales ;
- filiation DNC : non trouvee ;
- directeur general : non trouve.

### Differences SELARL / SELAS

- Le president SELAS est source par `Texte colle`, mais pas encore par une
  citation precise.
- Les actions / numerotation des actions sont rattachees a `Texte colle` et
  `Besoins Sydel (juridique).pdf`.
- Les statuts medecin/dentiste SELAS sont rattaches a `Notre job - Sydel.pdf` et
  `Texte colle`.
- Les documents communs restent a auditer : un rattachement source NotebookLM ne
  vaut pas reutilisation automatique.

### Reutilisation possible

| Element | Decision provisoire | Justification | Verification requise |
| --- | --- | --- | --- |
| Sources NotebookLM SELAS | reuse-check | Les documents sources sont maintenant nommes | Extraire passages/pages ou verifier dans sources repo |
| Statuts medecin/dentiste | adapter/no-go | Sources nommees, modeles distincts | Analyse source SELAS article par article |
| Procuration / DNC / Ordre | reuse-check | Sources ou indices nommes | Comparaison avec existant SELARL |
| Regime communautaire | reuse-check/no-go | Source nommee mais effet SELAS non tranche | Arbitrage juridique |
| Cession / SCM / site distinct | no-go provisoire | Sources nommees mais complexite forte | Specs et decisions humaines |

### Contradictions

- Plusieurs lignes sont marquees `Source trouvee`, mais l'indice exact est vide
  ou illisible.
- `Liste des documents SELAS` annonce 62 documents, alors que la liste detaillee
  n'est pas fournie dans cette reponse.
- `Attestation domiciliation` est marque source trouvee mais sans source exacte
  lisible dans la colonne correspondante.
- `DNC et filiation` confirme la DNC obligatoire tout en indiquant que la
  filiation n'est pas explicitement mentionnee.

### Informations non trouvees

- Directeur general SELAS.
- Filiation DNC president.
- Numerotation automatique ou manuelle des actions.
- Blocage plans/devis dans l'interface.
- Actions de preference / droits derogatoires en V1.
- Passages exacts, pages ou extraits source exploitables.
- Liste complete des 62 documents SELAS.

### Impact sur le sprint

Le sprint reste en Phase 3 - NOTEBOOKLM / `NO-GO dev`.

Cette reponse ameliore le niveau de couverture NotebookLM : les sources
principales sont identifiees par nom. Elle ne suffit pas pour un `GO dev`, mais
elle est suffisante pour preparer l'etape suivante de cadrage en lecture seule :
audit de reutilisation SELARL/global, avec reserve explicite sur les passages
source a verifier.

### Prochain prompt recommande

Aucun nouveau prompt NotebookLM general avant audit. Prochaine etape recommandee
: preparer `SELAS-REUSE-AUDIT-001` en lecture seule, sans developpement, sans
matrice finale et sans `GO dev`.

## Reponse NotebookLM SELAS 09

Date : 2026-06-02
Prompt utilise : verification des questions de revue humaine du pack SELAS V1
Source NotebookLM / indices cites : reponse avec sources/indices partiellement
illisibles (``,`,`,`) ; utile comme pre-check, mais non validante sans retour
Gad / associe / juriste.

### Synthese fiable

NotebookLM confirme que le perimetre V1 limite a SELAS medecin, unipersonnel,
President unique et creation simple est coherent.

La reponse renforce deux points de vigilance :

- plans et devis Ordre : presentes comme bloquants ;
- attestation sur le capital : presentee comme document obligatoire.

Elle ne tranche pas plusieurs questions sensibles :

- nomination President dans les statuts ou acte separe ;
- purge de `associe` au profit de `actionnaire` ;
- titre exact de la renonciation conjoint en SELAS ;
- filiation complete dans la DNC President.

### Documents identifies

| Document | Condition | Statut | Source | Incertitude |
| --- | --- | --- | --- | --- |
| Statuts SELAS medecin | Creation SELAS V1 | Dans pack | Sources NotebookLM illisibles | Acte separe President et wording `associe` a confirmer |
| Decision/PV President | Si nomination hors statuts ou choix outil | A confirmer | Indice outil | Faut-il le generer systematiquement en V1 ? |
| DNC President | Formalite dirigeant | Dans pack | DNC obligatoire, filiation non trouvee | Filiation a confirmer humainement |
| Demande Ordre | Profession reglementee | Dans pack | Plans/devis presentes comme bloquants | Blocage UI a arbitrer |
| Attestation capital / liste souscripteurs | Creation SELAS | A arbitrer | Attestation capital presentee comme obligatoire | Document distinct liste souscripteurs a confirmer |
| Renonciation conjoint | Regime communautaire | Dans pack conditionnel | Terme `associe` non tranche | Titre SELAS a confirmer |

### Conditions et exclusions

- V1 medecin unipersonnel : coherent selon NotebookLM.
- Plans/devis : a traiter comme point potentiellement bloquant pour Ordre.
- Apports en nature / materiel : question ouverte, car l'exclusion peut reduire
  la couverture des premieres installations.
- Attestation capital / liste souscripteurs : a arbitrer avant cloture.

### Variables / donnees a saisir

NotebookLM signale que des variables manquent probablement dans la fiche client
standard. La reponse propose de lister ces champs ensuite, mais cette liste n'a
pas encore ete fournie.

Variables ou blocs confirmes comme sensibles :

- plans des locaux ;
- devis materiel ;
- filiation DNC ;
- donnees de capital / souscripteurs ;
- genre du President pour feminisation ;
- donnees utiles aux actes de nomination si acte separe.

### Differences SELARL / SELAS

- Remplacement critique : `Gerant` vers `President`.
- Remplacement critique : `parts sociales` vers `actions`.
- Le terme `associe` reste ambigu dans certaines sources ou echanges.
- La feminisation `President` / `Presidente` est signalee comme point a gerer.

### Reutilisation possible

| Element | Decision provisoire | Justification | Verification requise |
| --- | --- | --- | --- |
| Pack V1 medecin unipersonnel | reuse-check valide en V1 | Tres coherent selon NotebookLM | Validation humaine officielle |
| Plans/devis Ordre | adapter/front-blocking possible | Bloquant selon NotebookLM | Arbitrage Gad/juriste sur blocage UI |
| Attestation capital | no-go provisoire / a ajouter selon arbitrage | Obligatoire selon NotebookLM | Source canonique exacte et document distinct liste souscripteurs |
| DNC filiation | reuse-check prudent | Non trouve dans NotebookLM | Confirmer greffe/juriste |
| Feminisation President | adapter possible | Point sensible signale | Verifier cas feminin dans pack ou ticket correctif |

### Contradictions

- NotebookLM indique un acte de nomination separe prevu dans l'outil, alors que
  la V1 actuelle absorbe la nomination President dans les statuts.
- NotebookLM signale `associe` comme terme parfois present, mais confirme aussi
  que le vocabulaire SELAS doit etre adapte.
- NotebookLM indique l'attestation capital comme obligatoire, alors que la V1
  actuelle l'a reservee faute de source canonique exacte.

### Informations non trouvees

- Filiation DNC President.
- Titre SELAS exact de la renonciation conjoint.
- Statut distinct obligatoire ou non de la liste des souscripteurs.
- Regle finale d'acte separe President en V1.

### Impact sur le sprint

Le pack de revue humaine doit etre enrichi avec un pre-check NotebookLM.

Impact concret :

- ajouter `NOTEBOOKLM_PRECHECK.md` au pack de revue ;
- ajouter une question de revue sur la feminisation `President` / `Presidente` ;
- porter en priorite humaine les plans/devis Ordre et l'attestation capital /
  liste souscripteurs.

Le sprint reste en `NO-GO cloture SELAS V1` tant que la revue humaine n'est pas
revenue.

### Prochain prompt recommande

Pas de nouveau prompt NotebookLM pour l'instant.

Prochaine etape : transmettre le pack de revue humaine enrichi a Gad / associe /
juriste, puis classer le retour humain.
