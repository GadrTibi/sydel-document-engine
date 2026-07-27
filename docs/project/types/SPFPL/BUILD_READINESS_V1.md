# SPFPL — BUILD READINESS V1 (analyse de constructibilite)

Date : 2026-06-07
Auteur : analyse de constructibilite (lecture seule, aucun code modifie)
Type : SPFPL (toujours SPFPLAS — President / actions)
Statut produit actuel : `INVENTAIRE_TECHNIQUE` (cf. `docs/project/COMPANY_TYPE_STATUS_REGISTRY_V1.md`)

## 0. Constat de cadrage (lire d'abord — l'etat reel diverge du brief)

Le brief de mission supposait un greenfield ("33 modeles rapatries", repertoire
`project/source_documents/spfpl`, synthese NotebookLM SPFPL, recette
`WORKFLOW_TYPE_ENTREPRISE_V1.md`, rendu par `docx_template_fill.py`). La realite du
repo est differente et il faut la connaitre avant de planifier :

1. **Aucun repertoire `project/source_documents/spfpl`.** Les sources SPFPL sont
   dispersees dans `project/source_documents/lot_04/` (statuts) et
   `project/source_documents/lot_05/` (satellites cession / apport). Inventaire complet en section 1.
2. **Le moteur SPFPL est DEJA code, branche dans l'orchestrateur et teste.** Tous les
   generateurs SPFPL existent (statuts cession/apport, note d'information, PV d'agrement
   x2, acte de cession de parts, acte de cession d'actions, contrat d'apport, attestation
   capital, attestation commissaire). Statut catalogue = `WorkflowStatus.TESTE`
   (`src/sydel_doc_engine/registry/catalog.py`, DOC-035/036, DOC-037..043, DOC-029).
   Tests : `tests/unit/test_lot_04_statuts_spfpl.py`, `test_lot_05_spfpl_core.py`,
   `test_lot_05_spfpl_agrement_info.py`, `test_lot_05_acte_cession_actions.py`.
3. **Le rendu n'est PAS du template-fill.** Il n'existe pas de `docx_template_fill.py`.
   Le projet genere les DOCX **from-scratch** via `src/sydel_doc_engine/rendering/docx_builder.py`
   (ADR-0004). Le DOCX source n'est jamais utilise comme gabarit d'execution (regle dure des specs).
   => Pour SPFPL, l'approche "template-fill de preference" du brief ne s'applique pas : le
   patron est **from-scratch deterministe**, comme tous les autres types.
4. **Pas de synthese NotebookLM SPFPL** (`docs/project/types/SPFPL/NOTEBOOKLM_ANSWERS.md` /
   `NOTEBOOKLM_PROMPTS_V2.md` absents). La phase NotebookLM (Rafael / NotebookLM) **n'a jamais ete faite** pour SPFPL.
5. **Pas de recette `WORKFLOW_TYPE_ENTREPRISE_V1.md`.** La recette canonique du projet est
   `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` (phases 0-10) + `COMPANY_TYPE_STATUS_REGISTRY_V1.md`.
6. **Pas de slice front SPFPL.** Le front clean (`src/sydel_doc_engine/front_app/`) n'expose
   QUE la SELARL (`dossier_selection.py` ne contient que `selarl_v1` ;
   `selarl_slice.py`/`shell.py` cables SELARL uniquement). C'est le vrai trou de constructibilite.

**Conclusion d'altitude.** Pour SPFPL, le travail constructible n'est pas "coder le moteur"
(deja fait, teste, from-scratch) — c'est : (a) faire la phase NotebookLM/Rafael pour valider le
metier et lever les `non trouve`, et (b) batir le **slice front SPFPL** sur le patron SELARL.
Le moteur existant est une **preuve technique**, pas une validation produit (regle du registre de statut).

## 1. Inventaire des modeles source (fichier -> document juridique + cas)

Sources lues directement (extraction texte des DOCX) + recoupees avec les specs canoniques.

### Statuts (lot_04)

| Fichier | Document juridique | Cas | Forme confirmee |
|---|---|---|---|
| `lot_04/Statuts_SPFPLAS_dentistes_cession.docx` | Statuts SPFPLAS chirurgiens-dentistes, constitution par apport en **numeraire** | SPFPL cession, associe unique | SAS / President / actions ("par actions simplifiee", `Au capital de [capital_social]`) |
| `lot_04/Statuts SPFPLAS dentistes - apport.docx` | Statuts SPFPLAS dentistes, constitution par apport en **nature** de titres d'une SEL | SPFPL apport, associe unique | SAS / President / actions ("Societe par actions simplifiees", `[forme_sociale]` parametre) |
| `lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx` | Statuts SPFPLAS **medecins** par actions simplifiee | Code SAS (DOC-015), **PAS** route SPFPL | SAS / President / actions (rattache structure `SAS`, profession medecin) |

Note : `STATUTS_SAS_SPFPL_medecins_modele.docx` est juridiquement une SPFPL medecins mais le
catalogue le route sous `structure == SAS` (DOC-015), pas sous SPFPL. A trancher au cadrage SPFPL
medecins (voir bloquant B4).

### Satellites cession / apport (lot_05)

| Fichier | Document juridique | Cas |
|---|---|---|
| `lot_05/NOTE D'INFORMATION.docx` | Note d'information (constitution SPFPL + acquisition/apport des titres de la cible) | cession ET apport (double formule source) |
| `lot_05/PV SELARL agrément cession SPFPL - SELARL 1 associé - transforme.docx` | PV de l'associe unique de la cible : agrement SPFPL + modif statuts | SPFPL cession, associe unique |
| `lot_05/PV SELARL agrément cession SPFPL - SELARL plusieurs associés - transforme.docx` | PV d'AGE de la cible : agrement SPFPL + modif statuts | SPFPL cession, plusieurs associes |
| `lot_05/Acte_cession_SPFPL_tiers_part_modele.docx` | Acte de cession de **parts** (titre source "Cession de parts") | SPFPL cession |
| `lot_05/Acte_cession_SPFPL_tiers_modele.docx` | Acte de cession d'**actions** (titre source "Cession d'actions") | SPFPL cession (variante actions) |
| `lot_05/Contrat d_apport SEL SPFPL.docx` | Contrat d'apport en nature de titres SEL vers SPFPL | SPFPL apport |
| `lot_05/Attestation sur le capital - apport - liste des souscripteurs.docx` | Attestation capital + liste des souscripteurs (President) | SPFPL apport (et reutilisee comme satellite SAS DOC-024) |
| `lot_05/attestation nomination commissaire aux apports - transforme.docx` | Acte de designation d'un commissaire aux apports | SPFPL apport |

Hors-SPFPL mais voisins (NE PAS confondre) : tout le bloc SCM (`Statuts SCM`, `Pacte`, `Reglement
interieur`, `Liste depenses`, `PV AGE cession part SCM`, `Courrier SDE`, `Acte cession parts SCM`),
SCI/SCI IRIS/SCS, statuts SELARL/SELAS, lot_01 (universels), lot_02 (PV gerant, inscription ordre,
regime communautaire), lot_03 (bail, appel de fonds, cessions cabinet, derogations).

## 2. Cas couverts par SPFPL

Confirme par les specs (`lot_04_statuts_spfpl_spec_canonique_v1`, `lot_05_spfpl_spec_canonique_v1`,
`lot_05_spfpl_arbitrages_v1`) et le catalogue moteur :

- **2 parcours canoniques** : `SPFPL cession` (constitution numeraire + acquisition de titres) et
  `SPFPL apport` (constitution par apport en nature de titres SEL). Selectionnes par
  `dossier.structure` + `operation_spfpl.type` (`cession` | `apport`) + `dossier.options.cession/apport`.
- **Creation = systematique** : statuts + note d'information + (cession) PV d'agrement + acte de
  cession de parts ; (apport) contrat d'apport + attestation capital + designation commissaire.
- **Variante associe unique vs plusieurs associes** : PV d'agrement (PV associe unique vs PV d'AGE).
  Pilote par `dossier.options.associe_unique`.
- **Variante parts vs actions** (cession) : acte de cession de **parts** (source confirmee) vs acte de
  cession d'**actions** (source `Acte_cession_SPFPL_tiers_modele.docx` ; codee DOC-029 mais sous fortes
  reserves de scope — cedant masculin uniquement, cible SELAS dentiste, paiement comptant, Yousign).
- **Statuts toujours mono-associe en V1** (les deux DOCX statuts sont mono-associe ; multi-associes
  statuts SPFPL bloque cote moteur, cf. `statuts_spfpl_common.validate_common_statuts_context`).
- **Personne morale associee** : geree dans `associes_cible[]` via `type == "personne_morale"`
  (`spfpl_common.associe_display_name`), pour les listes de repartition de la cible. Mais **PAS** comme
  fondateur/souscripteur de la SPFPL en V1.

Cas NON couverts / hors V1 (a porter au front comme visibles non generes) : multi-associes des
statuts SPFPL ; liste dynamique de plusieurs souscripteurs sur l'attestation capital ; combinaison
simultanee cession+apport dans un meme dossier ; profession medecin sous route SPFPL (route SAS aujourd'hui).

## 3. Documents a generer (statut + approche)

Rappel approche : le projet genere **from-scratch** (ADR-0004) via `docx_builder.py`. "a-tokeniser"
ici = source DOCX deja inventoriee, generateur deja ecrit ; il reste a faire passer le **wording par la
validation Rafael/NotebookLM** (pas de retokenisation technique necessaire, la tokenisation a deja eu
lieu dans les specs). Tous les generateurs ci-dessous existent et sont `TESTE` cote moteur.

| Document (code) | Statut metier | Approche (rendu) | Etat moteur |
|---|---|---|---|
| Statuts SPFPL cession (DOC-035) | systematique (cession) | from-scratch | code + teste, mono-associe |
| Statuts SPFPL apport (DOC-036) | systematique (apport) | from-scratch | code + teste, mono-associe |
| Note d'information SPFPL (DOC-037) | systematique (cession & apport) | from-scratch | code + teste ; wording cession/apport arbitre |
| PV agrement cession - associe unique (DOC-038) | conditionnel (cession + associe_unique) | from-scratch | code + teste |
| PV agrement cession - plusieurs associes (DOC-039) | conditionnel (cession + !associe_unique) | from-scratch | code + teste |
| Acte de cession de parts SPFPL (DOC-040) | conditionnel (cession, nature != actions) | from-scratch | code + teste |
| Acte de cession d'actions SPFPL (DOC-029) | conditionnel (cession, nature == actions) | from-scratch | code + teste MAIS scope tres reserve (voir B5) |
| Contrat d'apport SEL->SPFPL (DOC-041) | conditionnel (apport) | from-scratch | code + teste ; exige evaluateur + commissaire |
| Attestation capital / liste souscripteurs SPFPL (DOC-042) | conditionnel (apport) | from-scratch | code + teste ; **1 souscripteur uniquement** |
| Attestation nomination commissaire aux apports (DOC-043) | conditionnel (apport) | from-scratch | code + teste ; exige commissaire selectionne |

Documents **separes / hors-creation SPFPL** mais qui apparaissent dans un dossier SPFPL via les lots
transverses (a confirmer au cadrage front SPFPL) :
- universels lot_01 (DNC, domiciliation, procuration) — `structures = ALL`, donc applicables a SPFPL ;
- PV nomination gerant (DOC-004) et demande d'inscription a l'ordre (DOC-034) — catalogue les liste
  pour `SPFPL cession`/`SPFPL apport` ; **mais** une SPFPLAS a un President, pas un gerant : le PV
  "nomination gerant" sur SPFPL est un **point a trancher metier** (incoherence forme/document) ;
- regime communautaire (DOC-005/006) — liste pour SPFPL cession/apport (conditionnel
  `regime_communautaire == true`).

## 4. Wording EXACT deja disponible (confirme par specs / sources)

Disponible sans nouvelle validation (deja tokenise + arbitre dans les specs) :

1. **Note d'information** — squelette canonique complet figé dans
   `docs/delivery/lot_05_spfpl_spec_texte_v1.md` (sec. 4.2), variables `note_information.operation_phrase`
   / `note_information.operation_nom` ; valeurs arbitrees (`lot_05_spfpl_arbitrages_v1` sec. 4.1) :
   cession -> `d'acquerir` / `cession` ; apport -> `de recevoir en apport en nature` / `apport`.
   La double formule source `acquerir/de recevoir en apport en nature` ne doit JAMAIS etre rendue telle quelle.
2. **PV agrement** — titres exacts confirmes par lecture source :
   `PROCES-VERBAL DE L'ASSOCIE UNIQUE DU [date_pv]` (variante associe unique) et
   `PROCES-VERBAL DE L'ASSEMBLEE GENERALE EXTRAORDINAIRE DU [date_pv]` (variante plusieurs associes) ;
   en-tete cible : denomination / forme / `Au capital de ... €` / `Siège social` / `Immatriculée au RCS de ... sous le n° ...`.
3. **Acte de cession de parts** — titre source `Cession de parts` ; acte d'actions -> `Cession d'actions`.
4. **Attestation capital** — titre `ATTESTATION`, sous-titre `Liste des souscripteurs`, en-tete SPFPLAS
   "Societe par actions simplifiee au capital de ... euros / Societe de Participations Financieres de
   Profession Liberale de [profession]".
5. **Contrat d'apport** — titre `Contrat d'apport`, comparution `Entre les soussignes`.
6. **Designation commissaire** — titre `Acte de designation d'un commissaire aux apports`.
7. Roles canoniques entierement specifies (sec. 5 du spec canonique) : `societe_spfpl`, `societe_cible`,
   `cedant`, `apporteur`, `associes_cible[]`, `cession_parts`, `apport_titres`, `reunion`,
   `capital_souscription`, `evaluateur_apport`, `commissaire_aux_apports`. Modeles Pydantic presents
   dans `src/sydel_doc_engine/domain/models.py` (lignes 362-578).

Tous ces elements sont du wording **confirme** (source tokenisee + arbitrage documente). Ils n'exigent
pas de nouvelle validation Rafael SAUF si la phase NotebookLM revele une contradiction (voir section 5).

## 5. NON TROUVE -> a lever par tokenisation puis Rafael (jamais inventer)

Les points ci-dessous sont des arbitrages **metier / juridiques** non tranchables par le code. Ils
doivent passer par la phase NotebookLM (transcripts Albane / docs sources) PUIS, si absents ou
contradictoires, par un message a Rafael (jamais une question au PM, regle projets a associe).

1. **Acte de cession d'ACTIONS** (`Acte_cession_SPFPL_tiers_modele.docx`) : classe "bloquant" dans
   `lot_05_spfpl_arbitrages_v1` (source DOCX confirmee depuis, mais codee DOC-029 sous des reserves
   tres fortes — cedant masculin uniquement, cible limitee au wording SELAS chirurgien-dentiste,
   paiement comptant cheque de banque, agrement unanime, Yousign). Le perimetre reel cession d'actions
   SPFPL (variantes de paiement, genre du cedant, type de cible) est **non valide metier**.
2. **PV d'agrement classes "cession" mais rediges en "apport"** : les deux PV sources emploient le
   vocabulaire d'apport (`parts apportees`, `contrat d'apport`). Arbitrage V1 = corriger vers wording
   cession (documente dans `lot_05_spfpl_arbitrages_v1` sec. 4.1), MAIS cette correction de wording
   juridique reste **a confirmer par Rafael** (c'est une modification de formulation legale).
3. **Liste dynamique de plusieurs souscripteurs** (attestation capital) : source mono-actionnaire ;
   les accords singulier/pluriel et la structure multi-souscripteurs ne sont pas couverts par une
   source. Bloque en V1.
4. **Statuts SPFPL multi-associes** : les deux DOCX statuts sont mono-associe ; la source de verite
   rappelle 1 a 6 associes possibles. Formes de comparution / repartition / signatures multi-associes
   **non sourcees**.
5. **SPFPL medecins vs dentistes** : seules les sources dentistes existent en route SPFPL ; la SPFPL
   medecins est rangee sous SAS (DOC-015). Savoir si SPFPL doit couvrir les medecins (et avec quel
   wording d'ordre/profession) est **non tranche**.
6. **PV "nomination gerant" sur une SPFPLAS** : incoherence forme (President) vs document (gerant). Le
   catalogue route DOC-004 vers SPFPL ; a confirmer si ce document s'applique reellement a une SPFPLAS.
7. **Libelle "commissaire aux apports" vs "comm. aux comptes"** : la source de verite dit "comm. aux
   comptes", les DOCX disent "commissaire aux apports". Arbitrage V1 retient commissaire aux apports
   (`lot_05_spfpl_arbitrages_v1` sec. 4.2), **sous reserve de validation metier**.
8. **Choix evaluateur / commissaire** : entites fixes dans les sources, a fournir par saisie ; pas de
   referentiel valide. Reste manuel V1 mais le **catalogue des intervenants** n'est pas source.

## 6. Besoins envers le SOCLE PARTAGE (couche commune requise par SPFPL)

Ce que SPFPL exige du socle, au-dela de ce qui existe deja pour la SELARL :

1. **Slice front + deroulante auto-extensible (MANQUANT, c'est le coeur du build front).**
   - `front_app/dossier_selection.py` ne contient que `selarl_v1`. Il faut y ajouter
     `spfpl_cession` et `spfpl_apport` (ou une entree SPFPL avec sous-choix operation).
   - Il faut un `front_app/spfpl_slice.py` sur le patron de `selarl_slice.py`
     (`SpfplSliceInput` + `build_spfpl_plan` + `build_generation_context` + `generate_spfpl_dossier`),
     branche dans `front_app/shell.py` (aujourd'hui code en dur sur SELARL :
     `generate_selarl_dossier`, prefill SELARL, libelles "SELARL V1").
   - Le shell doit router selon le type de dossier au lieu d'appeler directement la slice SELARL.
2. **Couche "substitution parts/actions, gerant/president".** SPFPLAS = President + actions. Le socle
   doit savoir basculer le vocabulaire titres (`parts sociales` vs `actions`) et dirigeant
   (`gerant` vs `president`). Le moteur le fait deja localement par role (`apport_titres.nature_titres`,
   `societe_spfpl.dirigeant.fonction`), mais le **front** SELARL est cable "gerant"/"parts" en dur
   (`fonction_dirigeant="gérant"`, `type_titre="parts sociales"` dans `selarl_slice.build_generation_context`).
   Une slice SPFPL doit poser President/actions.
3. **Couche multi "LES SOUSSIGNES" / repartition numerotee / PV d'AG.**
   - Le moteur a deja la **repartition numerotee** et les listes presents/representes :
     `spfpl_common.capital_before_lines/capital_after_lines/presence_lines` (avec plages de parts,
     numero de part unique, controle d'integrite de la totalite des parts).
   - Le moteur a deja le **PV d'AG** (variante plusieurs associes, DOC-039) avec liste des presents.
   - **Manquant cote front** : la saisie auto-extensible de `associes_cible[]` (N associes de la cible,
     avant/apres, plage/numero) — la SELARL a un equivalent partiel (`additional_associes` /
     `_render_multi_associes_simple_block`) qui peut servir de patron mais doit etre adapte au modele
     `AssocieCible` (avant/apres operation, personne morale).
4. **Personne morale associee.** Le modele `AssocieCible.type == "personne_morale"` et
   `associe_display_name`/`associe_signature_name` existent (moteur). Le **front** SELARL ne sait saisir
   que des personnes physiques ; une slice SPFPL doit pouvoir saisir une personne morale dans la
   repartition de la cible.
5. **Couche genre.** Existe deja (`domain/enums.Gender`, `field_derivations.derive_gender_from_civilite`,
   `utils/grammar.py`). SPFPL la reutilise telle quelle. **Attention** : DOC-029 (cession actions) est
   code "cedant masculin uniquement" — la couche genre n'y est pas encore branchee (dette).
6. **Registre.** `registry/catalog.py` contient deja toutes les definitions SPFPL avec conditions de
   selection. `registry/lot_status.py` et l'orchestrateur (`orchestrator/service.py`) cablent les
   generateurs. Le registre est **pret** ; rien a ajouter cote moteur pour le perimetre V1 documente.
7. **Statut document front.** `front_data/document_status.py` (`build_document_status_for_code`) est
   utilise par la slice SELARL pour afficher les libelles/etats ; une slice SPFPL le reutilisera pour
   afficher generables / conditionnels / hors-V1 / bloques.

Resume socle : le **moteur et le registre sont prets** ; le besoin reel est une **couche front SPFPL**
(slice + selection + routage shell + saisie multi-associes cible + personne morale + bascule
President/actions). C'est la meme couche que SELARL, a generaliser/dupliquer, pas a inventer.

## 7. Bloquants de build (decisions de scope / sources / canon)

| Code | Bloquant | Nature | Qui tranche |
|---|---|---|---|
| B1 | Phase NotebookLM SPFPL jamais faite (pas de `NOTEBOOKLM_ANSWERS.md`) | process / metier | Rafael via NotebookLM ; pilote Naomi/Codex |
| B2 | Statut produit = `INVENTAIRE_TECHNIQUE` : moteur teste mais type NON traite en sprint produit | gouvernance | playbook impose sprint complet avant "traite" |
| B3 | Aucun slice front SPFPL ; shell cable SELARL en dur | technique (constructible) | a builder sur patron SELARL (pas de GO PM requis) |
| B4 | SPFPL medecins range sous SAS (DOC-015), pas sous SPFPL | scope metier | Rafael (perimetre SPFPL medecins) |
| B5 | Acte cession d'ACTIONS (DOC-029) code sous reserves fortes non validees metier | scope metier / juridique | Rafael (variantes paiement/genre/cible) |
| B6 | PV "nomination gerant" route vers SPFPL alors que SPFPLAS = President | coherence canon | Rafael (le document s'applique-t-il ?) |
| B7 | Correction wording PV "cession" rediges en "apport" (arbitrage V1 non confirme humain) | wording juridique | Rafael |
| B8 | Multi-associes statuts + multi-souscripteurs attestation : non sources | scope / source | bloque V1, a sourcer puis Rafael |

**Constructible immediatement, sans GO PM ni validation Rafael** (biais d'action) :
- B3 : slice front SPFPL cession + apport, perimetre mono-associe (= exactement ce que le moteur sait
  deja rendre et qui a un wording confirme : statuts + note d'information + PV associe unique + acte
  cession parts pour cession ; statuts + note + contrat apport + attestation capital + commissaire pour
  apport). Aucun wording nouveau, aucune regle metier inventee. C'est le patron SELARL applique a SPFPL.

**Necessite la phase NotebookLM / Rafael AVANT generation reelle livrable** : tout ce qui touche
B4-B8 (medecins, actions, PV gerant, correction wording PV, multi-*). Ne pas livrer ces variantes a
Rafael avant validation.

## 8. Recommandation de sequence

1. Ouvrir le **sprint produit SPFPL** selon `COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` (phase 0, `NO-GO dev`).
2. Phase NotebookLM SPFPL (lever B1, B4-B8) — pilote Naomi, reponses Rafael, journal de sprint.
3. En parallele (constructible, reversible) : **builder le slice front SPFPL mono-associe** sur le
   patron SELARL (lever B3), borne au wording deja confirme (section 4).
4. Triangulation 3 sources + matrice documentaire + audit reutilisation SELARL/global.
5. Smoke interne (ZIP + controle placeholders) puis pack pour Rafael (phase 8).
6. Cloture canonique (`DONE` / `PARTIAL` / `BLOCKED`) + mise a jour du registre de statut.

Le moteur etant deja teste, le sprint SPFPL est principalement un sprint **front + validation metier**,
pas un sprint moteur.
