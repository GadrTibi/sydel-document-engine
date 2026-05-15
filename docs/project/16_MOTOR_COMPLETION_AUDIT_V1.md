# Audit de cloture du moteur documentaire V1

Ticket : `CLOSE-MOTOR-AUDIT-001`

Date : 2026-05-15

## Objet

Ce document cloture l'etat du moteur documentaire apres integration des dernieres vagues visibles dans `origin/main`.

Il se limite a qualifier :

- ce qui est couvert par le moteur documentaire ;
- ce qui reste explicitement manuel ou legacy ;
- ce qui sort de la cloture moteur et passe dans les prochains chantiers ;
- si le moteur peut etre considere `feature complete` pour la V1.

Il ne modifie aucun wording juridique et ne vaut pas validation juridique des rendus.

## Sources lues

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/project/15_REMAINING_SCOPE_AUDIT_V1.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/04_LAST_STATE.md`
- `project/source_truth/Documents_a_generer_par_cas.docx`

Verification complementaire, sans modification de code :

- `src/sydel_doc_engine/registry/catalog.py`
- `src/sydel_doc_engine/orchestrator/service.py`

## Definition de couverture retenue

Un document est considere couvert par le moteur seulement si :

1. il dispose d'un generateur deterministe ;
2. il est reference dans le catalogue moteur ;
3. il est branche dans le registre de generateurs de l'orchestrateur ;
4. sa selection est conditionnee par le contexte dossier quand necessaire.

Un generateur present mais non branche n'est donc pas considere comme une couverture moteur complete.

## 1. Couverture moteur constatee

### 1.1 Tronc commun universel

Le tronc commun est couvert pour toutes les structures referencees :

| ID | Document | Couverture |
|---|---|---|
| `DOC-001` | Declaration sur l'honneur de non-condamnation | genere, catalogue, orchestre |
| `DOC-002` | Autorisation de domiciliation | genere, catalogue, orchestre |
| `DOC-003` | Procuration | genere, catalogue, orchestre |

### 1.2 Documents mutualisables branches

| ID | Document ou famille | Structures / conditions |
|---|---|---|
| `DOC-004` | PV nomination gerant | hors SAS selon le catalogue |
| `DOC-005` | Lettre de renonciation a revendiquer la qualite d'associe | option regime communautaire |
| `DOC-006` | Lettre d'avertissement au conjoint | option regime communautaire |
| `DOC-007` | Avenant contrat de bail | SELARL / SELAS avec cession |
| `DOC-008` | Appel de fonds SEL | SELARL avec cession dentaire |
| `DOC-009` | Acte de cession cabinet medical | SELARL / SELAS avec cession medicale |
| `DOC-010` | Compromis de cession cabinet medical | SELARL / SELAS avec cession medicale |
| `DOC-011` | Acte de cession cabinet dentaire | SELARL / SELAS avec cession dentaire |
| `DOC-012` | Compromis de cession cabinet dentaire | SELARL / SELAS avec cession dentaire |
| `DOC-013` | Formulaire derogation multi-sites SEL | formulaire a completer |
| `DOC-014` | Demande derogation cumul SELARL-BNC | formulaire a completer |
| `DOC-022` | Lettre option IS | SCI / SCI IRIS avec option IS |

### 1.3 Statuts branches

| ID | Document | Couverture |
|---|---|---|
| `DOC-015` | Statuts SAS / SPFPL medecins | SAS, perimetre source limite |
| `DOC-016` | Statuts SELARL chirurgien-dentiste | SELARL, associe unique V1 |
| `DOC-017` | Statuts SELARL medecin | SELARL, associe unique V1 |
| `DOC-018` | Statuts SELAS medecin | SELAS, associe unique V1 |
| `DOC-019` | Statuts SCS | SCS |
| `DOC-020` | Statuts SCI | SCI |
| `DOC-021` | Statuts SCI IRIS | SCI IRIS |
| `DOC-025` | Statuts SCM | SCM |

### 1.4 Satellites et documents specifiques branches

| ID | Document | Couverture |
|---|---|---|
| `DOC-023` | PV remuneration president SAS | SAS, associe unique, absence de remuneration |
| `DOC-024` | Attestation capital / liste des souscripteurs SAS | SAS, associe unique, apport |
| `DOC-026` | Pacte d'associes SCM | SCM, option satellites SCM |
| `DOC-027` | Contrat d'exercice professionnel a frais communs | SCM, option satellites SCM |
| `DOC-028` | Reglement interieur de la SCM | SCM, option satellites SCM |
| `DOC-029` | Acte de cession d'actions SPFPL a un tiers | SPFPL cession, option cession actions |
| `DOC-030` | Liste des depenses communes SCM | SCM, option satellites SCM |

## 2. Couvert partiellement ou non cloture dans le moteur

Les elements suivants existent dans le depot sous forme de generateurs ou de preparations, mais ne sont pas clos comme couverture moteur complete au sens strict ci-dessus.

| Document ou famille | Etat constate | Traitement |
|---|---|---|
| Demande d'inscription a l'ordre | generateur present, mais pas de `DOC-xxx` catalogue/orchestrateur constate | chantier d'alignement registre |
| Statuts SPFPL cession / apport | generateurs presents, mais pas de branchement catalogue/orchestrateur constate | chantier d'alignement registre |
| Note d'information SPFPL | generateur present, branchement non constate | chantier d'alignement registre |
| PV agrement cession SPFPL associe unique / plusieurs associes | generateurs presents, branchement non constate | chantier d'alignement registre |
| Acte de cession de parts SPFPL | generateur present, branchement non constate | chantier d'alignement registre |
| Contrat d'apport SPFPL | generateur present, branchement non constate | chantier d'alignement registre |
| Attestation capital SPFPL / commissaire aux apports | generateurs presents, branchement non constate | chantier d'alignement registre |
| Cession SCM SELARL / SELAS | sources preparees et spec de blocage disponible | arbitrage puis code ou blocage explicite |

## 3. Manuel ou legacy explicite

Les elements ci-dessous ne doivent pas etre integres automatiquement dans la cloture moteur V1 sans decision separee.

| Element | Qualification |
|---|---|
| Formulaire de declaration prealable de site distinct CD94 avec la SEL | marque a remplir a la main dans la source de verite |
| Derogation SEL BNC complete | indiquee comme a remplir a la main ; `DOC-014` ne couvre que la demande ciblee SELARL-BNC en formulaire a completer |
| `DOC-013` multi-sites SEL | volontairement produit comme formulaire a completer, pas comme acte finalise |
| `DOC-014` cumul SELARL-BNC | volontairement produit comme formulaire a completer, avec zones narratives sensibles |
| Demande de derogation cumul SELARL salariee | source legacy `.doc`, conversion bloquee ; traitement manuel specifie |
| Zones narratives sensibles non structurees | restent manuelles ou bloquantes tant qu'une spec n'encadre pas le wording |
| Validation juridique fine des rendus | hors tests automatises ; requiert revue humaine |

## 4. Prochains chantiers hors cloture moteur

Ces sujets ne doivent pas bloquer la redaction de la cloture, mais empechent de qualifier l'ensemble produit comme complet.

| Chantier | Raison |
|---|---|
| Alignement catalogue / orchestrateur des generateurs deja presents | plusieurs generateurs existent mais ne sont pas selectionnables par le moteur |
| Resolution de la cession SCM | `ARBITRAGE-SCM-CESSION-RESOLVE-001` reste READY |
| Blocage ou implementation cession SCM | `CODE-SCM-CESSION-BLOCK-001` reste READY |
| PDF | sortie cible V1 historique, non integree comme flux final moteur |
| ZIP dossier | sortie cible V1 historique, non integree comme flux final moteur |
| Streamlit V0 | explicitement bloque et hors ticket |
| Revue juridique / visuelle globale | les tests et smoke DOCX ne valent pas validation metier finale |

## 5. Decision feature complete V1

Statut retenu : **non feature complete V1**.

Raison :

- le moteur DOCX deterministe couvre un perimetre large et structure, avec `DOC-001` a `DOC-030` constates dans le catalogue ou les generateurs ;
- toutefois plusieurs documents inventories dans la source de verite ont encore un ecart entre generateur present et branchement moteur ;
- la cession SCM reste un chantier ouvert, au minimum a bloquer explicitement ou a resoudre par arbitrage ;
- PDF, ZIP dossier et Streamlit restent hors flux final ;
- la validation juridique fine reste humaine.

Conclusion operationnelle :

- le socle moteur DOCX est cloturable comme etat technique intermediaire ;
- le moteur ne doit pas etre annonce comme `feature complete V1` tant que les exclusions et prochains chantiers ci-dessus ne sont pas soit traites, soit explicitement sortis du perimetre V1 par decision metier.

