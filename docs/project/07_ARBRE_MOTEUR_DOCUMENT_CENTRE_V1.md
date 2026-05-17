# DAAT x SYDEL — Arbre logique du moteur documentaire V3

## Objet
Ce document décrit **l'arbre logique du moteur**, centré sur les **documents**.

Principes :
- le tronc démarre par les **documents universels** ;
- on **split seulement quand le document suivant change** ;
- on **recoupe** vers un même nœud quand plusieurs chemins réutilisent le même document ;
- les **variables UI** sont volontairement laissées de côté dans cette version ;
- les **conditions métier** importantes restent visibles (`si régime communautaire`, `si cession`, etc.).

## Légende
- trait plein = continuité normale du moteur
- trait pointillé = branche conditionnelle / optionnelle
- un même nœud peut être rejoint par plusieurs chemins
- les structures se **déduisent du chemin**, elles ne pilotent pas le graphe au départ

## Vue Mermaid

```mermaid
flowchart LR

classDef core fill:#0f172a,stroke:#0f172a,color:#fff;
classDef doc fill:#e0f2fe,stroke:#0284c7,color:#0c4a6e;
classDef cond fill:#fef3c7,stroke:#d97706,color:#7c2d12;
classDef end fill:#dcfce7,stroke:#16a34a,color:#14532d;
classDef warn fill:#fee2e2,stroke:#dc2626,color:#7f1d1d;

A([Début dossier]):::core --> U1[DOC-001\nDéclaration de non-condamnation]:::doc --> U2[DOC-002\nAutorisation de domiciliation]:::doc --> U3[DOC-003\nProcuration]:::doc

U3 --> SPLIT1{Le document suivant change-t-il ?}:::cond

%% SAS branch
SPLIT1 -->|Oui : branche SAS| SAS1[Statuts SAS]:::doc --> SAS2[Attestation sur le capital\n/ Liste des souscripteurs]:::doc --> SAS3[PV rémunération président]:::doc --> END_SAS([Sortie moteur SAS]):::end

%% Non-SAS shared branch
SPLIT1 -->|Oui : branche hors SAS| G1[PV nomination gérant]:::doc

%% Shared order branch
G1 --> SPLIT2{Demande d'inscription à l'ordre ?}:::cond
SPLIT2 -->|Oui| O1[Demande d'inscription à l'ordre]:::doc
SPLIT2 -->|Non| N1[Suite sans ordre]:::cond

%% SELARL
O1 --> SELARL_STAT{Statuts SELARL ?}:::cond
SELARL_STAT --> SELARL_DENT[Statuts SELARL\nchirurgien-dentiste]:::doc
SELARL_STAT --> SELARL_MED[Statuts SELARL\nmédecin]:::doc
SELARL_DENT --> SELARL_END([Sortie moteur SELARL]):::end
SELARL_MED --> SELARL_END
SELARL_DENT -. si site distinct .-> SELARL_SITE[Formulaire site distinct\nà remplir à la main]:::warn -.-> SELARL_END
SELARL_MED -. si site distinct .-> SELARL_SITE
SELARL_DENT -. si SCM cession .-> SELARL_SCM1[PV cession parts SCM]:::doc --> SELARL_SCM2[Courrier SDE]:::doc --> SELARL_SCM3[Acte cession SCM → SELARL]:::doc -.-> SELARL_END
SELARL_MED -. si SCM cession .-> SELARL_SCM1
SELARL_DENT -. si régime communautaire .-> REG1[Lettre de renonciation]:::doc --> REG2[Lettre d'avertissement]:::doc -.-> SELARL_END
SELARL_MED -. si régime communautaire .-> REG1
SELARL_DENT -. si dérogation .-> DER1[Formulaire dérogation SEL]:::doc -.-> SELARL_END
SELARL_MED -. si dérogation .-> DER1
SELARL_DENT -. si dérogation cumul SELARL-BNC .-> DER2[Demande dérogation\nSELARL-BNC]:::doc -.-> SELARL_END
SELARL_MED -. si dérogation cumul SELARL-BNC .-> DER2
SELARL_DENT -. si cession .-> CESS1[Avenant contrat de bail]:::doc --> CESS2[Appel de fond SEL]:::doc -.-> SELARL_CAB{Type de cabinet ?}:::cond
SELARL_MED -. si cession .-> CESS1
SELARL_CAB --> CESS_MED1[Acte cession cabinet médical]:::doc --> CESS_MED2[Compromis cabinet médical]:::doc -.-> SELARL_END
SELARL_CAB --> CESS_DEN1[Acte cession cabinet dentaire]:::doc --> CESS_DEN2[Compromis cabinet dentaire]:::doc -.-> SELARL_END

%% SELAS
O1 --> SELAS_STAT[Statuts SELAS médecin]:::doc --> SELAS_END([Sortie moteur SELAS]):::end
SELAS_STAT -. si régime communautaire .-> REG1
SELAS_STAT -. si SCM .-> SELAS_SCM1[PV AGE cession part SCM]:::doc --> SELAS_SCM2[Courrier SDE SELAS]:::doc --> SELAS_SCM3[Acte cession parts SCM → SEL]:::doc -.-> SELAS_END
SELAS_STAT -. si cession .-> SELAS_C1[Avenant contrat de bail]:::doc -.-> SELAS_CAB{Type de cabinet ?}:::cond
SELAS_CAB --> SELAS_MED1[Acte cession cabinet médical]:::doc --> SELAS_MED2[Compromis cabinet médical]:::doc -.-> SELAS_END
SELAS_CAB --> SELAS_DEN1[Acte cession cabinet dentaire]:::doc --> SELAS_DEN2[Compromis cabinet dentaire]:::doc -.-> SELAS_END
SELAS_STAT -. si dérogation multi-sites .-> DER1
SELAS_STAT -. si dérogation cumul salariée .-> SELAS_DER2[Demande dérogation\ncumul salariée]:::doc -.-> SELAS_END

%% SPFPL cession
O1 --> SPF_C_STAT[Statuts SPFPL cession]:::doc --> SPF_C_NOTE[Note d'information]:::doc --> SPF_C_END([Sortie moteur SPFPL cession]):::end
SPF_C_STAT -. si régime communautaire .-> REG1
SPF_C_NOTE -. si plusieurs associés .-> SPF_C_AGR_P[PV agrément cession\nplusieurs associés]:::doc -.-> SPF_C_END
SPF_C_NOTE -. si associé unique .-> SPF_C_AGR_U[PV agrément cession\nassocié unique]:::doc -.-> SPF_C_END
SPF_C_NOTE --> SPF_C_ACTE1[Acte de cession de parts]:::doc -.-> SPF_C_END
SPF_C_NOTE -. point ouvert .-> SPF_C_ACTE2[Acte de cession d'actions\nsource à confirmer]:::warn -.-> SPF_C_END

%% SPFPL apport
O1 --> SPF_A_STAT[Statuts SPFPL apport]:::doc --> SPF_A_NOTE[Note d'information]:::doc --> SPF_A_END([Sortie moteur SPFPL apport]):::end
SPF_A_STAT -. si régime communautaire .-> REG1
SPF_A_NOTE --> SPF_A_C1[Contrat d'apport]:::doc --> SPF_A_C2[Attestation sur le capital]:::doc --> SPF_A_C3[Attestation nomination\ncommissaire aux apports]:::doc -.-> SPF_A_END

%% SCM
O1 --> SCM_STAT[Statuts SCM]:::doc --> SCM_P1[Pacte d'associés SCM]:::doc --> SCM_P2[Liste dépenses communes]:::doc --> SCM_P3[Contrat frais communs]:::doc --> SCM_P4[Règlement intérieur SCM]:::doc --> SCM_END([Sortie moteur SCM]):::end

%% SCS
N1 --> SCS_STAT[Statuts SCS]:::doc --> SCS_END([Sortie moteur SCS]):::end

%% SCI / SCI IRIS
N1 --> SCI_STAT{Statuts SCI ?}:::cond
SCI_STAT --> SCI1[Statuts SCI]:::doc --> SCI_END([Sortie moteur SCI]):::end
SCI_STAT --> SCI2[Statuts SCI IRIS]:::doc --> SCI_END
SCI1 -. si option IS .-> SCI_IS[Lettre option IS]:::doc -.-> SCI_END
SCI2 -. si option IS .-> SCI_IS

%% Recoupe visuelle des lettres régime communautaire
REG2 -. réutilisé par plusieurs chemins .-> REG_END([Bloc régime communautaire terminé]):::end

```

## Lecture métier

### 1) Tronc commun
Le moteur commence par les trois documents présents dans tous les cas :
- DOC-001 — Déclaration de non-condamnation
- DOC-002 — Autorisation de domiciliation
- DOC-003 — Procuration

### 2) Premier split utile
Le premier vrai split intervient quand le document suivant change :
- **SAS** bifurque directement vers son bloc propre ;
- **hors SAS** passe par **PV nomination gérant**.

### 3) Nœuds de recoupe importants
Les nœuds à mutualiser côté moteur sont surtout :
- **PV nomination gérant**
- **Demande d'inscription à l'ordre**
- **bloc régime communautaire**
- **bloc cession cabinet** (médical / dentaire)
- **statuts**, avec variantes documentaires

### 4) Ce que ce document n'essaie pas encore de montrer
Pas encore dans cette version :
- la couche détaillée des **variables** ;
- l'arbre des **questions UI** ;
- le mapping exact **nœud documentaire → pack de variables**.

Ces couches viendront après validation de l'arbre documentaire.

## Points ouverts à garder visibles
- **SPFPL cession — Acte de cession d'actions** : mentionné dans le référentiel, mais source exacte à confirmer.
- **Liste des souscripteurs** : la règle générale la cite pour SPFPL / SELAS / SCS ; la place exacte dans l'arbre moteur devra être confirmée document par document.
- certains éléments sont explicitement **à remplir à la main** et restent hors automatisation initiale.

## Consolidation runtime RECONCILE-MOTOR-CLOSE-001

L'arbre ci-dessus reste le graphe documentaire de lecture metier. La
reconciliation finale du moteur ferme l'ecart runtime en exposant tous les
generateurs documentaires disponibles dans le catalogue et l'orchestrateur.

Etat runtime DOCX V1 apres reconciliation :

- `DOC-001` a `DOC-004` : socle universel et PV nomination gerant.
- `DOC-034` : demande d'inscription a l'ordre.
- `DOC-005` a `DOC-014` : regime communautaire, bail/appel, cession cabinets et derogations coeur.
- `DOC-015`, `DOC-035`, `DOC-036`, `DOC-016` a `DOC-021`, `DOC-025` : statuts SAS, SPFPL, SEL, SCS, SCI, SCI IRIS et SCM.
- `DOC-022` a `DOC-024` : option IS et satellites SAS.
- `DOC-037` a `DOC-043` : documents SPFPL specifiques restaures dans le runtime.
- `DOC-026` a `DOC-030` : satellites SCM et acte actions SPFPL.
- `DOC-031` a `DOC-033` : bloc cession SCM.

Les exclusions V1 restent volontaires : UI, PDF, ZIP, recette finale, revue
juridique/visuelle humaine, documents a remplir a la main et sources legacy non
converties ou non specifiees.
