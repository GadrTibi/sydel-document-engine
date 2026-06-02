# SELAS reuse audit 001

Date : 2026-06-01

Ticket : `SELAS-REUSE-AUDIT-001`

Statut : `DONE - cadrage lecture seule`

Decision sprint : `NO-GO dev`

## Objet

Auditer ce qui peut etre reutilise depuis la SELARL et les registres globaux
pour le sprint SELAS, avant toute matrice documentaire finale et avant tout
developpement.

Cet audit ne modifie pas le moteur, ne modifie pas les sources DOCX, ne produit
aucun document SELAS et ne valide aucun wording juridique nouveau.

## Sources lues

### Pilotage sprint

- `AGENTS.md`
- `docs/project/PROJECT_CONTROL_TOWER_V1.md`
- `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`
- `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`
- `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`
- `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`
- `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`
- `docs/sprints/SPRINT_SELAS_V1.md`
- `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`

### Socle SELARL / global

- `docs/project/SELARL_CANONICAL_STATUS_V1.md`
- `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md`
- `docs/project/SELARL_PRODUCTION_FACTORY_V1.md`
- `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md`
- `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md`
- `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md`
- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md`

### Specs et registres documentaires

- `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`
- `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`
- `src/sydel_doc_engine/domain/case_catalog.py`
- `src/sydel_doc_engine/registry/catalog.py`

### Sources DOCX inspectees en lecture seule

- `project/source_documents/lot_04/Statuts_SELAS_medecin.docx`
- `project/source_truth/modele Statuts SELAS avec MH.docx`
- `project/source_documents/lot_02/Demande d_inscription à l_ordre - transforme.docx`
- `project/source_documents/lot_02/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx`
- `project/source_documents/lot_05/PV AGE cession part SCM - SELAS.docx`
- `project/source_documents/lot_05/Courrier SDE - SELAS.docx`

## Constat executif

Le sprint SELAS peut reutiliser le socle de methode SELARL, les roles globaux,
les adresses, la signature, le capital/titres et une partie des documents
universels.

La reutilisation juridique directe reste limitee. Les changements SELAS
`president`, `actions`, `actionnaires`, `statuts SELAS` et gouvernance par
actions rendent dangereux tout copier-coller SELARL.

Le premier perimetre raisonnable a preparer dans la matrice documentaire est :

- SELAS medecin associe unique ;
- documents courts universels en `reuse-check` ;
- demande a l'ordre en `reuse-check` fort ;
- statuts SELAS medecin en `adapter` sur source existante ;
- regime communautaire en `reuse-check` avec reserve ;
- cession, SCM, derogation, multi-actionnaires, micro-holding, actions de
  preference et directeur general en `no-go` ou `adapter` strict tant que les
  passages sources ne sont pas extraits et arbitres.

## Matrice de reutilisation documentaire

| Element | Source existante | Usage SELAS cible | Conditions identiques ? | Variables identiques ? | Decision | Risque | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-001` DNC | Lot 1 + SELARL LOCKED | DNC du president SELAS | A verifier : fonction dirigeant change | Partiellement : identite/filiation/signature communes | `reuse-check` | Moyen | Verifier si la source SELAS exige filiation et libelle president ; ne pas coder sans spec SELAS |
| `DOC-002` Domiciliation | Lot 1 + SELARL LOCKED | Autorisation domiciliation SELAS | Probablement oui si document neutre | Oui pour signataire/societe/siege/signature | `reuse-check` | Faible | Confirmer source SELAS ou source truth ; reutilisation technique probable |
| `DOC-003` Procuration | Lot 1 + SELARL LOCKED | Procuration du president SELAS | Non : fonction du signataire change | Majoritairement oui, sauf fonction dirigeant | `adapter` | Fort | Parametrer strictement `President`; interdire remplacement aveugle `Gerant -> President` |
| `DOC-004` PV nomination gerant | PV SELARL teste | Decision/PV nomination president SELAS | Non : gouvernance differente | Reuse partiel des roles/reunion/signature | `adapter` | Fort | Creer spec SELAS president avant code ; DG reste `no-go` |
| `DOC-034` Demande inscription ordre | Spec ordre couvre SELARL/SELAS | Demande ordre SELAS | Oui selon spec texte : overlay SELARL/SELAS identique | Oui : ordre, mandataire, societe, signataire | `reuse-check` | Moyen | Verifier source SELAS et pieces plans/devis ; lock humain absent |
| `DOC-005` Renonciation conjoint | Source SELAS presente + batch regime | Si regime communautaire | A verifier juridiquement pour SELAS | Oui pour conjoint/regime/apport/signature | `reuse-check` | Moyen | Ne pas extrapoler la revendication conjoint sans arbitrage ; verifier source SELAS |
| `DOC-006` Avertissement conjoint | Batch regime + SELARL reserve historique | Si regime communautaire | A verifier | Oui partiel | `no-go` provisoire | Fort | Garder reserve tant que source/decision SELAS pas explicite |
| `DOC-018` Statuts SELAS medecin | Source + spec statuts SEL | Statuts SELAS medecin associe unique | Non vs SELARL, oui comme document propre SELAS | Reuse global des packs statuts/capital/associes | `adapter` | Fort | Utiliser source SELAS dediee ; pas de fusion avec statuts SELARL |
| Statuts SELAS dentiste | NotebookLM indique priorite mais source repo non identifiee | Statuts SELAS dentiste | Non etabli | A verifier | `no-go` provisoire | Fort | Trouver source DOCX dentiste SELAS avant matrice generable |
| Attestation depot capital / liste souscripteurs | Sources attestation/liste souscripteurs ambiguës | Capital SELAS divise en actions | Non etabli | Capital/actions reutilisables en structure | `reuse-check` | Moyen | Identifier document canonique exact avant decision |
| Cession fonds liberal | Specs cession cabinet SELARL/SELAS existent cote moteur | SELAS si passage BNC vers societe | Non : cas ultra personnalise | Reuse roles cession seulement | `no-go` V1 simple | Fort | Garder manuel/hybride tant que sous-formulaire et origine propriete non arbitres |
| SCM cession `DOC-031` a `DOC-033` | Specs + sources SELAS/SELARL SCM | SELAS avec SCM | Partiellement ; overlays SELAS signales | Variables SCM reutilisables | `adapter` | Fort | A exclure du premier ticket ; preparer sous-cas dedie si priorise |
| Derogation / site distinct `DOC-013`/`DOC-014` | Specs derogations | SELAS deuxieme lieu ou derogation | Partiellement | Derogation/site reutilisables | `reuse-check` / `no-go generation` | Moyen | Afficher comme manuel ou conditionnel ; ne pas generer automatiquement en V1 simple |
| Multi-actionnaires | SELARL multi limite + registres `associes[]` | SELAS plusieurs actionnaires | Non : actions, votes, statuts, PV differents | Structure `associes[]` reutilisable, libelles a adapter | `no-go` V1 simple | Fort | Reporter apres associe unique ; actionnaires/personnes morales a specifier |
| Directeur General | Source raw signalee mais NotebookLM non trouve pour V1 | Nomination DG SELAS | Non etabli | Non etabli | `no-go` | Fort | Ne pas integrer au parcours V1 sans source/spec dediee |
| Actions de preference / micro-holding | Source `modele Statuts SELAS avec MH.docx` | SELAS avec personne morale/action pref | Non pour V1 simple | Champs candidats seulement | `no-go` V1 simple | Fort | Ticket separe avec arbitrage humain ; ne pas melanger au sprint simple |

## Matrice de reutilisation des variables et blocs

| Element | Source existante | Usage SELAS | Conditions identiques ? | Variables identiques ? | Decision | Risque | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Roles personne | Registre global V2.1 | Praticien, actionnaire, president, signataire, mandataire | Non : president/actionnaire a qualifier | Oui si roles explicites | `adapter` | Moyen | Utiliser `personne.president`, pas `gerant` ; pas de fusion silencieuse |
| Dossier unipersonnel | Contrat SELARL | Praticien = actionnaire unique = president = signataire | Oui seulement si option explicite | Oui par rattachement explicite | `reuse-check` | Moyen | Garder option explicite ; ne pas imposer hors unipersonnel |
| Adresses | Registre V2.1 | Domicile, siege, lieu exercice | Oui | Oui | `reuse-check` | Faible | Reutiliser les adresses rolees avec options explicites |
| Signature | Dictionnaire + registres | Signature lot/document | Oui | Oui | `identique` | Faible | Reutiliser lieu/date/email/tel signature si spec front le confirme |
| Capital/titres | Registre V2.1 + statuts SEL | Capital SELAS en actions | Non pour libelles | Structure oui | `adapter` | Moyen | Typer `actions`; verifier numerotation automatique/manuelle |
| Banque depot | Registre global + statuts | Depot capital SELAS | Oui partiel | Oui partiel | `reuse-check` | Moyen | Confirmer champs banque/adresse selon attestation/statuts |
| Ordre professionnel | Spec ordre | Dossier ordre SELAS | Oui selon overlay SELARL/SELAS | Oui | `reuse-check` | Moyen | Ajouter reserve plans/devis non tranchee |
| Regime communautaire | Batch regime | Conjoint SELAS | A verifier juridiquement | Oui structurellement | `reuse-check` | Moyen | Garder declencheur, mais bloquer automatisation complete si effet juridique non arbitre |
| Genre / accords | Dictionnaire + statuts specs | `ne/nee`, accords president/actionnaire | Partiel | Oui pour genre | `adapter` | Moyen | Ne pas inventer accords non source |
| Numerotation actions | Statuts SELAS source | Rangs actions | Non tranche | Champ candidat | `reuse-check` | Moyen | Decision humaine : automatique ou saisie juriste |

## Decisions de securite

- Aucune regle de remplacement automatique global `parts -> actions` ou
  `gerant -> president` ne doit etre acceptee comme mecanisme juridique.
- La SELARL sert de patron de methode et de tests, pas de source juridique
  SELAS.
- `DOC-018` existe comme statuts SELAS medecin, mais la source dentiste SELAS
  reste a identifier avant toute couverture medecin + dentiste.
- Le directeur general reste hors V1.
- Les actions de preference, micro-holding et multi-actionnaires restent hors
  premier ticket.
- Les documents de cession fonds, SCM et derogation doivent rester hors premier
  happy path SELAS, ou visibles comme conditionnels/manuels/bloques.

## Questions ouvertes a porter dans `SELAS-MATRIX-001`

1. Quelle source fait foi pour les statuts SELAS dentiste ?
2. La DNC du president doit-elle exiger la filiation complete en SELAS ?
3. La numerotation des actions est-elle calculee automatiquement ou saisie par
   le juriste ?
4. `DOC-006` avertissement conjoint doit-il rester reserve pour SELAS ou etre
   genere avec source SELAS explicite ?
5. Les plans/devis Ordre doivent-ils bloquer le parcours ou seulement apparaitre
   comme pieces attendues ?
6. Faut-il afficher `Actionnaire` dans l'interface ou conserver `Associe` comme
   terme transversal avec libelles documentaires adaptes ?
7. Le premier perimetre doit-il etre SELAS medecin uniquement, ou attendre la
   source SELAS dentiste avant sprint dev ?

## Recommandation

Passer a `SELAS-MATRIX-001` en lecture seule.

Objectif de la prochaine etape : produire une matrice documentaire SELAS
provisoire, classee par condition d'apparition et statut
`generable / reuse-check / adapter / manuel / reserve / no-go`, sans `GO dev`.

Premier ticket de developpement non autorise a ce stade.
