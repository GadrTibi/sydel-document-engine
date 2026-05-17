# UI document occurrences V1

## Objet

Ce document formalise la logique d'occurrence documentaire a utiliser par l'UI et par
l'orchestrateur moteur.

Il ne modifie pas le wording juridique, ne cree pas de document canonique nouveau et
ne remplace pas les specs documentaires existantes. Il sert a distinguer :

- un document produit une seule fois ;
- un document produit une seule fois avec des blocs internes repetables ;
- un document produit plusieurs fois, une fois par entite metier.

## Sources lues

Sources projet :

- `AGENTS.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`

Specs et livrables delivery consultes pour le perimetre du ticket :

- PV nomination gerant : `lot_02_pv_nomination_gerant_*`
- statuts : `lot_04_statuts_*`
- liste des souscripteurs / capital : `lot_05_spfpl_*`, `lot_05_sas_satellites_*`
- cession SCM : `lot_05_scm_*`, `lot_04_statuts_scm_arbitrages_v1.md`
- cession cabinets : `lot_03_cession_cabinets_*`
- documents connexes du graphe : regime communautaire, demande d'inscription a l'ordre,
  bail / appel de fonds, derogations, option IS

## Definitions moteur

### `single_document`

Un document canonique est selectionne au plus une fois pour un dossier donne et produit
un seul fichier DOCX.

Regles :

- l'UI collecte les champs scalaires ou les roles uniques du document ;
- le moteur ne boucle pas sur une liste d'entites pour produire plusieurs fichiers ;
- les blocs conditionnels restent possibles, mais ils ne changent pas le nombre de fichiers ;
- le nom de sortie est celui du document canonique.

Exemples typiques : autorisation de domiciliation, demande d'inscription a l'ordre,
lettre option IS si elle etait sans liste interne.

### `single_document_with_repeated_block`

Un document canonique est selectionne au plus une fois pour un dossier donne, mais son
contenu contient un ou plusieurs blocs repetes depuis une liste canonique.

Regles :

- l'UI collecte une liste structuree : `associes[]`, `souscripteurs[]`,
  `statuts_civils.associes[]`, etc. ;
- le moteur produit un seul DOCX ;
- le moteur repete des paragraphes, lignes de tableau, signatures ou repartitions a
  l'interieur du document ;
- les validations de cardinalite, de coherence des totaux et de wording source doivent
  bloquer en cas d'ambiguite.

Exemples typiques : PV nomination gerant avec `associes[]`, statuts civils avec
associes dynamiques, attestation capital / liste des souscripteurs si la liste dynamique
est arbitree.

### `one_document_per_entity`

Un document canonique est selectionne une fois, puis produit N fichiers DOCX, un par
item d'une liste metier.

Regles :

- l'UI doit identifier la liste qui pilote la cardinalite de sortie ;
- chaque sortie doit porter une cle d'entite stable pour le nom de fichier et la trace ;
- le moteur doit pouvoir expliquer quelle entite a produit quel document ;
- cette strategie ne doit etre utilisee que si une source ou une spec le valide
  explicitement.

Etat V1 : aucun document consulte dans ce ticket n'autorise clairement cette strategie.
Les listes `associes[]`, `souscripteurs[]`, `cessionnaires[]` et `cedants[]`
(`cédants[]` dans les formulations metier) doivent
donc etre traitees comme blocs internes ou points ouverts, pas comme une generation
automatique d'un fichier par personne.

## Regle UI generale

L'UI ne doit pas demander "combien de documents ?" comme premiere question. Elle doit
d'abord identifier :

1. le document canonique selectionne par le dossier ;
2. la strategie d'occurrence du document ;
3. les listes metier utiles au contenu ;
4. les cas ou la liste reste bloquee ou manuelle faute de wording valide.

Une liste canonique ne signifie pas automatiquement "un fichier par item". Par defaut,
une liste comme `associes[]` ou `souscripteurs[]` alimente un bloc repetable dans un
document unique.

## Strategies par famille et document

| Famille / document | Strategie V1 | Entite repetable | Regle UI / moteur |
|---|---|---|---|
| DOC-001 Declaration de non-condamnation | `single_document` | aucune en V1 | Un document pour le signataire du contexte courant. Multi-signataires non arbitre. |
| DOC-002 Autorisation de domiciliation | `single_document` | aucune | Un document par dossier, avec `domiciliation.adresse_affichee`. |
| DOC-003 Procuration | `single_document` | aucune en V1 | Un document pour le signataire / dirigeant du contexte courant. Multi-mandants non arbitre. |
| PV nomination gerant | `single_document_with_repeated_block` | `associes[]` | Un PV unique ; la liste des associes presents / representes et les signatures sont repetees dans le document. |
| Demande d'inscription a l'ordre | `single_document` | aucune | Un document unique ; la derogation est un bloc manuel fourni ou bloquant. |
| Regime communautaire - lettre d'avertissement | `single_document` | aucune | Un document distinct du batch, pilote par un role unique `conjoint`. |
| Regime communautaire - lettre de renonciation | `single_document` | aucune | Un document distinct du batch ; pas de boucle multi-conjoints sourcee. |
| Statuts SAS | `single_document` en V1 | actionnaire / souscripteur unique | Les statuts restent limites a l'actionnaire unique ; multi-actionnaires ou multi-souscripteurs bloquent. |
| Statuts SEL d'exercice | `single_document` en V1, cible `single_document_with_repeated_block` | `associes[]` | La structure canonique est `associes[]`, mais les statuts multi-associes restent manuels/bloques en V1. |
| Statuts SPFPL | `single_document` en V1, cible `single_document_with_repeated_block` | associe fondateur / souscripteur | Les sources sont mono-associe ; extension multi-associes non automatisee sans arbitrage. |
| Statuts civils SCS / SCI / SCI IRIS | `single_document_with_repeated_block` | `statuts_civils.associes[]` | Un document de statuts par societe ; comparution, apports, parts et signatures peuvent repeter les associes. |
| Statuts SCM | `single_document_with_repeated_block` cible | `associes[]` | Un document statutaire SCM avec 1 a 6 associes ; satellites SCM exclus du generateur statuts. |
| Lettre option IS | `single_document_with_repeated_block` | `statuts_civils.associes[]` | Une lettre unique ; la table des associes est repetee dans le document. |
| Bail - avenant au contrat de bail | `single_document` | aucune liste de sortie | Un avenant unique si le contexte cession le rend eligible. |
| Appel de fonds SEL | `single_document` | aucune liste de sortie | Un document unique ; limite SELARL dentaire en V1. |
| Cession cabinets - acte medical | `single_document` | aucune liste de sortie | Un acte unique, selectionne par `type_cabinet=medical` et `etape=acte`. Roles vendeur/acquereur scalaires. |
| Cession cabinets - compromis medical | `single_document` | aucune liste de sortie | Un compromis unique, selectionne par `type_cabinet=medical` et `etape=compromis`. |
| Cession cabinets - acte dentaire | `single_document` | aucune liste de sortie | Un acte unique, selectionne par `type_cabinet=dentaire` et `etape=acte`. |
| Cession cabinets - compromis dentaire | `single_document` | aucune liste de sortie | Un compromis unique, selectionne par `type_cabinet=dentaire` et `etape=compromis`. |
| Derogations multi-sites / cumul | `single_document` ou formulaire a completer | aucune liste de sortie | Les documents restent des formulaires/document finalise selon mode explicite ; champs narratifs sensibles manuels. |
| SPFPL - note d'information | `single_document` | aucune liste de sortie | Un document unique par sous-batch SPFPL. |
| SPFPL - PV agrement associe unique | `single_document` | aucune | Un PV unique pour le cas associe unique. |
| SPFPL - PV agrement plusieurs associes | `single_document_with_repeated_block` | `associes_cible[]` | Un PV unique avec associes cibles repetes, si le contexte et le wording sont valides. |
| SPFPL - acte de cession de parts | `single_document_with_repeated_block` si repartition dynamique | associes de la societe cible | Un acte unique ; les repartitions internes peuvent repeter les associes. |
| SPFPL - contrat d'apport | `single_document` | aucune liste de sortie | Un contrat unique, hors double option cession/apport non arbitree. |
| SPFPL - attestation capital / liste souscripteurs | `single_document` en V1, cible `single_document_with_repeated_block` | `capital_souscription.souscripteurs[]` | Source V1 actionnaire unique ; liste dynamique multi-souscripteurs bloquee sans arbitrage. |
| SPFPL - designation commissaire aux apports | `single_document` | aucune | Un document unique si le commissaire est explicitement selectionne. |
| SAS - PV remuneration president | `single_document` | aucune | Un PV unique d'associe unique ; plusieurs associes bloquent. |
| SAS - attestation capital / liste souscripteurs | `single_document` en V1, cible `single_document_with_repeated_block` | `capital_souscription.souscripteurs[]` | Un seul document canonique ; multi-souscripteurs hors automatisation V1. |
| SCM cession - PV AGE cession part SCM | ambigu, spec requise | `associes[]` probable | Sources preparees seulement ; ne pas choisir entre bloc repetable et autre strategie avant spec. |
| SCM cession - Courrier SDE | ambigu, spec requise | aucune ou destinataire a confirmer | Sources preparees seulement ; strategie a fixer en spec. |
| SCM cession - acte de cession parts SCM | ambigu, spec requise | `cedants[]` / `cessionnaires[]` probables | Ne pas produire un document par cedant ou cessionnaire sans spec ; acte unique avec blocs internes probable mais non valide. |
| SCM satellites - pacte, liste depenses, contrat frais communs, reglement interieur | manuel / spec requise | a determiner | Hors generateur statuts SCM ; chaque satellite doit recevoir sa propre spec. |
| Acte de cession d'actions SPFPL | bloque / spec requise | a determiner | Source preparee recemment mais document non specifie ; occurrence a fixer avant automatisation. |

## Entites repetables et interpretation V1

| Entite | Interpretation V1 |
|---|---|
| `associes[]` | Liste interne prioritaire pour blocs repetables : PV, statuts civils, statuts SCM, option IS, certains PV SPFPL. Ne declenche pas un fichier par associe. |
| `souscripteurs[]` | Liste interne cible pour attestation capital / liste des souscripteurs. En V1 automatisee, souvent limitee a un seul souscripteur. |
| `cessionnaires[]` | Non stabilise dans les specs consultees. Ne doit pas piloter `one_document_per_entity` sans spec de cession dediee. |
| `cedants[]` / `cédants[]` | Non stabilise dans les specs consultees. Pour cession cabinets, le role actuel reste `cession.vendeur` scalaire ; pour SCM cession, spec requise. |
| `cession.exercices[]` | Bloc interne de cession cabinets, attendu sur trois exercices, pas occurrence de fichier. |
| `cession.salaries[]` | Conceptuellement repetable, mais reprise salaries reste manuelle / bloquante selon les arbitrages cession cabinets. |

## Cas manuels ou ambigus restants

- `one_document_per_entity` n'a aucun cas valide dans les specs lues ; toute utilisation future doit etre tranchee document par document.
- Les statuts SEL multi-associes restent hors automatisation V1 : `len(associes[]) >= 2` doit bloquer tant que le wording pluriel n'est pas valide.
- Les statuts SAS restent limites a l'actionnaire unique ; plusieurs actionnaires ou souscripteurs bloquent.
- Les statuts SPFPL et l'attestation capital SPFPL restent centres sur un associe / souscripteur unique en V1, sauf arbitrage specifique.
- Les listes dynamiques de souscripteurs pour SPFPL / SAS / SELAS / SCS restent a arbitrer ; elles doivent rester un bloc interne d'un document unique sauf decision contraire.
- Les documents SCM cession disposent de sources preparees, mais pas encore de spec : occurrence, roles `cedants[]` / `cessionnaires[]`, et frontiere avec les autres documents SCM restent a fixer.
- Les satellites SCM ne sont pas inclus dans les statuts SCM et doivent etre specifies separement.
- La clause SCM dans l'acte medical de cession cabinet reste conditionnelle et manuelle ; elle ne remplace pas la famille documentaire SCM.
- Les cessions cabinets gardent des roles scalaires vendeur / acquereur en V1 ; les multi-vendeurs ou multi-acquereurs ne sont pas sources.
- L'acte de cession d'actions SPFPL reste non specifie ; la preparation de source ne suffit pas a autoriser une strategie d'occurrence.
- Les documents marques ou traites comme formulaires a completer restent hors automatisation finalisee tant que le mode de rendu et les donnees narratives ne sont pas explicites.

## Regle de blocage a appliquer

Si l'UI detecte une cardinalite superieure a 1 sur une liste non arbitree, elle doit :

1. conserver les donnees saisies ;
2. afficher le document comme non automatisable V1 ;
3. signaler la spec ou l'arbitrage requis ;
4. ne pas transformer silencieusement la demande en plusieurs fichiers.

Cette regle evite de deduire une logique documentaire a partir de la seule presence
d'une liste metier.
