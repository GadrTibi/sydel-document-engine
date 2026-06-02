# SELAS tickets 001

Date : 2026-06-01

Ticket : `SELAS-TICKETS-001`

Statut : `DONE - cadrage lecture seule`

Decision sprint : `NO-GO dev`

## Objet

Transformer le cadrage SELAS en backlog de tickets ordonnes, sans coder et sans
valider de wording juridique.

Ce livrable s'appuie sur :

- `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` ;
- `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md` ;
- `docs/sprints/SPRINT_SELAS_MATRIX_001.md` ;
- `docs/sprints/SPRINT_SELAS_FRONT_CONTRACT_001.md`.

Il ne donne aucun `GO dev`. Il prepare les arbitrages a demander a Gad et
identifie le plus petit futur ticket qui pourrait devenir codable.

## Perimetre candidat maintenu

Le seul parcours candidat pour un futur premier developpement reste :

```text
SELAS medecin, actionnaire unique, president unique, creation simple,
sans cession, sans SCM, sans derogation, sans site distinct,
sans directeur general, sans micro-holding, sans actions de preference,
hors multi-actionnaires.
```

Tout autre cas reste hors premier sprint dev ou en ticket separe.

## Regle de priorisation

Les tickets sont classes en quatre familles :

1. `ARBITRAGE` : decision Gad requise avant tout code.
2. `SPEC` : ecriture ou verrouillage documentaire requis avant tout code.
3. `DEV CANDIDAT` : ticket potentiellement codable apres arbitrage et spec.
4. `RESERVE` : cas connu, mais exclu du premier parcours SELAS simple.

Un ticket `DEV CANDIDAT` ne devient codable que si :

- le perimetre exact est valide par Gad ;
- la source ou spec documentaire est identifiee ;
- les champs front sont figes ;
- les blocages visibles sont acceptes ;
- les tests attendus sont decrits.

## Backlog ordonne

| Ordre | Ticket | Famille | Statut | Objet | Dependances | Sortie attendue |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `SELAS-ARBITRAGE-SCOPE-001` | `ARBITRAGE` | `READY` | Valider que le premier parcours dev est uniquement `SELAS medecin actionnaire unique president unique` | Matrice + contrat front | Decision Gad ecrite : `GO cadrage dev limite` ou maintien `NO-GO dev` |
| 2 | `SELAS-SPEC-PRESIDENT-001` | `SPEC` | `READY` | Specifier le role `President` SELAS dans les documents candidats | Arbitrage scope | Spec roles president/actionnaire/signataire, sans DG |
| 3 | `SELAS-SPEC-PROCURATION-001` | `SPEC` | `READY` | Verrouiller l'adaptation SELAS de `DOC-003` procuration | Spec president | Decision document separe ou parametre strict `President` |
| 4 | `SELAS-SPEC-DNC-PRESIDENT-001` | `SPEC` | `READY` | Verrouiller `DOC-001` DNC president et la question filiation | Spec president | Champs requis DNC SELAS, filiation oui/non |
| 5 | `SELAS-SPEC-STATUTS-MEDECIN-AU-001` | `SPEC` | `READY` | Verrouiller `DOC-018` statuts SELAS medecin actionnaire unique | Arbitrage scope | Spec statuts simple, actions, president, source citee |
| 6 | `SELAS-SPEC-DECISION-PRESIDENT-001` | `SPEC` | `READY` | Creer la spec canonique Decision/PV nomination president SELAS | Spec president + statuts | Code canonique ou nouveau document a definir |
| 7 | `SELAS-SPEC-CAPITAL-ACTIONS-001` | `SPEC` | `READY` | Arbitrer capital, actions, valeur nominale et numerotation | Statuts medecin | Numerotation calculee/saisie, controles capital |
| 8 | `SELAS-SPEC-ORDRE-001` | `SPEC` | `READY` | Confirmer reutilisation `DOC-034` et pieces Ordre SELAS | Contrat front | Plans/devis bloquants ou simples pieces attendues |
| 9 | `SELAS-SPEC-REGIME-COMMUNAUTAIRE-001` | `SPEC` | `READY` | Arbitrer `DOC-005` et reserve `DOC-006` pour SELAS | Audit reuse | Decision : `DOC-005` seul, `DOC-006` reserve ou inclus |
| 10 | `SELAS-FRONT-SCHEMA-001` | `DEV CANDIDAT` | `BLOCKED` | Ajouter le schema front SELAS simple, sans generation | Tickets specs 2 a 9 | UI collecte champs + blocages, aucun DOCX |
| 11 | `SELAS-FRONT-BLOCKERS-001` | `DEV CANDIDAT` | `BLOCKED` | Afficher les messages de blocage des cas hors V1 | Front schema | Blocages visibles pour dentiste, multi-actionnaires, DG, SCM, cession, etc. |
| 12 | `SELAS-DOC001-DNC-PRESIDENT-001` | `DEV CANDIDAT` | `BLOCKED` | Brancher ou adapter `DOC-001` pour DNC president | Spec DNC + front schema | DOCX DNC president + tests |
| 13 | `SELAS-DOC002-DOMICILIATION-001` | `DEV CANDIDAT` | `BLOCKED` | Verifier et brancher `DOC-002` domiciliation SELAS | Spec front + source neutralite | DOCX domiciliation + tests |
| 14 | `SELAS-DOC003-PROCURATION-PRESIDENT-001` | `DEV CANDIDAT` | `BLOCKED` | Adapter `DOC-003` procuration avec fonction president | Spec procuration | DOCX procuration president + controle anti-gerant |
| 15 | `SELAS-DOC018-STATUTS-MEDECIN-AU-001` | `DEV CANDIDAT` | `BLOCKED` | Implementer statuts SELAS medecin actionnaire unique | Spec statuts + capital/actions | DOCX statuts + tests wording actions/president |
| 16 | `SELAS-DECISION-PRESIDENT-001` | `DEV CANDIDAT` | `BLOCKED` | Implementer Decision/PV nomination president SELAS | Spec decision president | DOCX decision/PV + tests |
| 17 | `SELAS-DOC034-ORDRE-001` | `DEV CANDIDAT` | `BLOCKED` | Brancher la demande d'inscription a l'Ordre pour SELAS | Spec ordre | DOCX ordre + affichage pieces attendues |
| 18 | `SELAS-DOC005-RENONCIATION-CONJOINT-001` | `DEV CANDIDAT` | `BLOCKED` | Brancher `DOC-005` si regime communautaire | Spec regime communautaire | DOCX conditionnel ou blocage explicite |
| 19 | `SELAS-SMOKE-HAPPY-PATH-001` | `DEV CANDIDAT` | `BLOCKED` | Tester le happy path SELAS medecin simple | Docs candidats implementes | Pack DOCX + ZIP sans mentions SELARL/gerant/parts |
| 20 | `SELAS-HUMAN-REVIEW-001` | `ARBITRAGE` | `BLOCKED` | Soumettre le pack SELAS simple a revue humaine | Smoke happy path | Retours juriste/associe, corrections ou validation |

## Tickets reserves hors premier parcours

| Ticket | Statut | Raison |
| --- | --- | --- |
| `SELAS-SOURCES-DENTISTE-001` | `RESERVE` | Source statuts SELAS chirurgien-dentiste non identifiee |
| `SELAS-MULTI-ACTIONNAIRES-001` | `RESERVE` | Actions, votes, droits financiers, accords et PV pluriel non verrouilles |
| `SELAS-DIRECTEUR-GENERAL-001` | `RESERVE` | Directeur General non trouve dans NotebookLM V1 |
| `SELAS-MICRO-HOLDING-001` | `RESERVE` | Personne morale et actions de preference hors V1 simple |
| `SELAS-ACTIONS-PREFERENCE-001` | `RESERVE` | Droits derogatoires a specifier dans un sprint separe |
| `SELAS-CESSION-FONDS-001` | `RESERVE` | Redaction ultra personnalisee, origine de propriete complexe |
| `SELAS-SCM-001` | `RESERVE` | Sous-parcours dedie requis, variables SCM nombreuses |
| `SELAS-DEROGATION-SITE-DISTINCT-001` | `RESERVE` | Formulaires/pieces ordinales a traiter hors happy path |
| `SELAS-ATTESTATION-CAPITAL-001` | `RESERVE` | Document canonique exact a identifier avant promesse produit |

## Premier ticket pouvant devenir codable

Le plus petit ticket futur pouvant recevoir un `GO dev` borne est :

```text
SELAS-FRONT-SCHEMA-001
```

Mais seulement apres les arbitrages/specs suivants :

1. `SELAS-ARBITRAGE-SCOPE-001` ;
2. `SELAS-SPEC-PRESIDENT-001` ;
3. `SELAS-SPEC-CAPITAL-ACTIONS-001` ;
4. `SELAS-SPEC-ORDRE-001` ;
5. `SELAS-SPEC-REGIME-COMMUNAUTAIRE-001`, au moins pour savoir si le bloc est
   affiche comme generable, reserve ou bloque.

Ce ticket front serait plus sur que commencer par un document, car il peut
afficher le parcours et les blocages sans produire de wording juridique.

## Criteres du futur `SELAS-FRONT-SCHEMA-001`

Le ticket ne devra pas generer de DOCX. Il devra seulement :

- proposer le type de dossier `SELAS` ;
- limiter la profession active a `medecin` ;
- imposer actionnaire unique et president unique ;
- collecter les blocs Qualification, Fiche Client, Roles, Societe, Adresses,
  Capital/actions, Ordre, Regime communautaire et Signature ;
- afficher les documents candidats et reserves ;
- bloquer les cas hors V1 simple avec les messages du contrat front ;
- conserver le sprint en `NO-GO generation` tant que les specs documentaires ne
  sont pas codees et testees.

## Questions a envoyer a Gad avant dev

1. Confirme-t-on le premier parcours `SELAS medecin actionnaire unique president
   unique` uniquement ?
2. Le premier ticket codable doit-il etre le schema front sans generation ?
3. La DNC president doit-elle exiger la filiation complete ?
4. La procuration SELAS doit-elle etre un document separe ou un parametre du
   `DOC-003` existant ?
5. La Decision/PV president doit-elle recevoir un nouveau code canonique ?
6. La numerotation des actions est-elle calculee automatiquement ou saisie ?
7. Les plans/devis Ordre sont-ils bloquants ?
8. `DOC-006` reste-t-il reserve pour SELAS ?
9. L'interface doit-elle afficher `Actionnaire` ou garder `Associe` comme terme
   transversal hors documents ?

## Decision de sortie

`SELAS-TICKETS-001` est suffisant pour demander un arbitrage Gad sur le premier
ticket codable.

Le sprint reste en `NO-GO dev`.

Prochaine etape recommandee : `SELAS-GO-DEV-FIRST-TICKET-001`, limite a une
decision Gad sur le premier ticket, sans code tant que ce `GO dev` n'est pas
donne.
