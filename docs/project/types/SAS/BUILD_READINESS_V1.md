# SAS — BUILD READINESS V1 (analyse de constructibilite)

Date : 2026-06-07
Auteur : analyse de constructibilite (lecture seule, aucun code modifie)
Type : SAS (en V1, exclusivement SPFPL Medecins par actions simplifiee — President / actions)
Statut produit actuel : `INVENTAIRE_TECHNIQUE` (cf. `docs/project/COMPANY_TYPE_STATUS_REGISTRY_V1.md`, 7 docs catalogues / 6 generables)

## 0. Constat de cadrage (lire d'abord — l'etat reel diverge du brief)

Le brief de mission supposait un greenfield (repertoire `project/source_documents/sas`, synthese
NotebookLM SAS, recette `WORKFLOW_TYPE_ENTREPRISE_V1.md`, rendu par `docx_template_fill.py`). La
realite du repo est differente, exactement comme pour SPFPL/SCI/SCM ; il faut la connaitre avant de
planifier :

1. **Aucun repertoire `project/source_documents/sas`.** Les sources SAS sont dispersees : le statut
   est dans `project/source_documents/lot_04/` (1 fichier), l'attestation capital dans
   `project/source_documents/lot_05/` (fichier partage avec SPFPL apport), et le **PV remuneration
   president n'est plus present sur disque** (voir B5). Inventaire complet en section 1.
2. **Le moteur SAS est DEJA code, branche dans l'orchestrateur et teste.** Trois generateurs SAS
   existent : statuts SAS (DOC-015), PV remuneration president (DOC-023), attestation capital / liste
   des souscripteurs (DOC-024). Statut catalogue = `WorkflowStatus.TESTE`
   (`src/sydel_doc_engine/registry/catalog.py`). Generateurs wires dans
   `src/sydel_doc_engine/orchestrator/service.py` (`DOC-015` -> `StatutsSasGenerator`, `DOC-023` ->
   `PvRemunerationPresidentGenerator`, `DOC-024` -> `AttestationCapitalListeSouscripteursSasGenerator`).
   Tests : `tests/unit/test_statuts_sas.py`, `tests/unit/test_lot_05_sas_satellites.py`.
3. **Le rendu n'est PAS du template-fill.** Il n'existe pas de `docx_template_fill.py`. Le projet
   genere les DOCX **from-scratch** via `src/sydel_doc_engine/rendering/docx_builder.py` (ADR-0004).
   Le DOCX source n'est jamais utilise comme gabarit d'execution (regle dure des specs). Pour SAS,
   l'approche "template-fill de preference" du brief ne s'applique pas : le patron est **from-scratch
   deterministe**, comme tous les autres types.
4. **Pas de synthese NotebookLM SAS** (`docs/project/types/SAS/NOTEBOOKLM_ANSWERS.md` /
   `NOTEBOOKLM_PROMPTS_V2.md` absents — le brief le confirme : NotebookLM pas encore ingere pour ce
   type). La phase NotebookLM (Rafael / NotebookLM) **n'a jamais ete faite** pour SAS.
5. **Pas de recette `WORKFLOW_TYPE_ENTREPRISE_V1.md`.** La recette canonique du projet est
   `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` (phases 0-10) + `COMPANY_TYPE_STATUS_REGISTRY_V1.md`.
6. **Pas de slice front SAS.** Le front clean (`src/sydel_doc_engine/front_app/`) n'expose QUE la
   SELARL : `front_app/dossier_selection.py` ne contient que `selarl_v1` ; `selarl_slice.py` / `shell.py`
   cables SELARL uniquement. C'est le vrai trou de constructibilite (identique au constat SPFPL).
7. **La "SAS" du moteur n'est pas une SAS generique.** En V1 c'est uniquement une **SPFPL de medecins
   par actions simplifiee** (President / actions, actionnaire unique = president). Le code verrouille
   ce perimetre : `statuts_sas.type == "spfpl_medecins"` et `profession == "medecin"` sont exiges
   (`_validate_sas_scope`, `_statuts_sas_enabled`). Toute SAS d'une autre profession ou une SAS
   commerciale generique n'est PAS couverte.

**Conclusion d'altitude.** Pour SAS, le travail constructible n'est pas "coder le moteur" (deja fait,
teste, from-scratch) — c'est : (a) faire la phase NotebookLM/Rafael pour valider le metier et lever
les `non trouve`, et (b) batir le **slice front SAS** sur le patron SELARL. Le moteur existant est une
**preuve technique**, pas une validation produit (regle du registre de statut).

## 1. Inventaire des modeles source (fichier -> document juridique + cas)

Sources recoupees avec le code, les specs canoniques (`docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md`,
`docs/delivery/lot_05_sas_satellites_spec_canonique_v1.md`) et le catalogue moteur.

| Fichier source | Document juridique | Cas couvert | Etat sur disque |
|---|---|---|---|
| `lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx` | Statuts d'une SPFPL de Medecins **par actions simplifiee unipersonnelle** (President / actions ; actionnaire unique = president ; condition suspensive inscription Ordre des Medecins) | Creation SAS (SPFPL medecins), actionnaire unique | **Present** (verifie : 344 775 octets) |
| `lot_05/Attestation sur le capital - apport - liste des souscripteurs.docx` | Attestation du President sur le capital + liste des souscripteurs (apport en nature de titres SEL + numeraire) | Creation SAS avec apport, souscripteur unique | **Present** (fichier partage : sert aussi de source SPFPL apport DOC-042, mais DOC canonique SAS distinct = DOC-024) |
| `source_import/raw_drive_dump/Creation SAS/PV remuneration president - transforme.docx` | PV des decisions de l'associe unique fixant l'**absence de remuneration** du President jusqu'a la cloture du 1er exercice | Creation SAS, associe unique, absence de remuneration | **ABSENT du disque** — `raw_drive_dump` nettoye ; chemin reference dans la spec et le catalogue mais introuvable (voir B5) |

Note importante : le nom de fichier `STATUTS_SAS_SPFPL_medecins_modele.docx` est juridiquement une
**SPFPL medecins** ; le catalogue le route sous `structure == SAS` (DOC-015), PAS sous SPFPL (qui ne
porte que les sources dentistes). C'est un choix de rangement assume (la SPFPL medecins vit sous le
chemin SAS, la SPFPLAS dentistes sous le chemin SPFPL). A confirmer au cadrage (voir B6).

Hors-SAS mais voisins (NE PAS confondre) : tous les statuts SELARL/SELAS, SCI/SCI IRIS/SCS, SCM ; le
bloc SPFPL dentistes (lot_04/lot_05) ; lot_01 universels ; lot_02 (PV gerant, inscription ordre,
regime communautaire) ; lot_03 (bail, appel fonds, cessions cabinet, derogations) ; `lettre_option_is`
(SCI / SCI IRIS uniquement, pas SAS).

## 2. Cas couverts par SAS

Confirme par les specs (`lot_04_statuts_sas_spec_canonique_v1`, `lot_05_sas_satellites_spec_canonique_v1`)
et le code (`statuts_sas.py`, `sas_satellites_common.py`, `orchestrator/service.py`) :

- **1 seul parcours canonique en V1** : **Creation d'une SPFPL de Medecins par actions simplifiee
  (SAS)**, **actionnaire unique** qui est aussi le **President**. Selectionne par `dossier.structure ==
  SAS` + `statuts_sas.type == spfpl_medecins` + `statuts_sas.profession == medecin` +
  `dossier.options.associe_unique == true` + `president.ref_associe_index == 0`.
- **Creation = systematique** : statuts SAS (DOC-015) + universels lot_01 (DNC, domiciliation,
  procuration via `structures = ALL`). Le catalogue case_catalog liste pour le cas SAS :
  `statuts_sas`, `declaration_non_condamnation`, `autorisation_domiciliation`, `procuration`,
  `attestation_capital_sas`, `pv_remuneration_president` (+ une 2e occurrence de l'attestation
  intitulee "Liste des souscripteurs").
- **Conditionnel apport** : l'attestation capital / liste des souscripteurs (DOC-024) n'est generee
  que si `dossier.options.apport == true` ET `capital_souscription.apports_nature_montant` non vide
  (`_sas_attestation_capital_enabled`). La source impose un bloc "Apports en nature" structurel.
- **Conditionnel absence de remuneration** : le PV remuneration president (DOC-023) n'est genere que
  si `remuneration_president.type == "absence_remuneration"` (`_sas_pv_remuneration_president_enabled`).
  Une remuneration positive/variable/differee n'est PAS couverte.

Cas NON couverts / hors V1 (a porter au front comme visibles non generes) :
- **SAS generique / commerciale** (non SPFPL) : explicitement hors source ;
- **SAS d'une autre profession** que medecin (ex. dentiste, infirmier...) : verrou code ;
- **Multi-actionnaires / multi-souscripteurs** : la source statuts est mono-actionnaire ; l'attestation
  source est mono-souscripteur ; les blocs "plusieurs soussignes", table d'apports dynamique,
  repartition dynamique des actions et signatures multiples ne sont pas sources ;
- **President distinct de l'actionnaire unique** : verrou code (`_validate_actionnaire_unique`) ;
- **President feminin** : le wording satellites V1 ne couvre QUE le president masculin
  (`actionnaire.genre != Gender.MASCULIN` -> erreur dans `validate_sas_satellite_scope`) ;
- **Remuneration positive** du president ;
- **Cession / apport hors creation** : pour SAS, il n'y a PAS de parcours cession en V1 (l'acte de
  cession d'actions DOC-029 appartient au chemin SPFPL cession dentistes, pas SAS — voir section 3).

## 3. Documents a generer (statut + approche)

Rappel approche : le projet genere **from-scratch** (ADR-0004) via `docx_builder.py`. "a-tokeniser"
ici = source DOCX deja inventoriee et generateur deja ecrit ; il reste a faire passer le **wording par
la validation Rafael/NotebookLM** (la tokenisation a deja eu lieu dans les specs). Les 3 generateurs
ci-dessous existent et sont `TESTE` cote moteur.

| Document (code) | Statut metier | Approche (rendu) | Etat moteur |
|---|---|---|---|
| Statuts SAS / SPFPL medecins (DOC-015) | **systematique** (creation) | from-scratch | code + teste, **actionnaire unique masculin**, profession medecin, marie uniquement |
| PV remuneration president (DOC-023) | **conditionnel** (associe_unique + `remuneration_president.type == absence_remuneration`) | from-scratch | code + teste ; **president masculin uniquement**, absence de remuneration uniquement |
| Attestation capital / liste des souscripteurs (DOC-024) | **conditionnel** (apport + 1 souscripteur + apport nature non vide) | from-scratch | code + teste ; **1 souscripteur uniquement**, bloc apport nature structurel |
| Declaration non condamnation (lot_01) | **systematique** (universel `structures = ALL`) | from-scratch | code + teste (transverse, partage tous types) |
| Autorisation domiciliation (lot_01) | **systematique** (universel) | from-scratch | code + teste (transverse) |
| Procuration (lot_01) | **systematique** (universel) | from-scratch | code + teste (transverse) |

Documents **separes / hors-creation SAS** ou a clarifier au cadrage front SAS :
- **PV nomination gerant (DOC-004)** : son `general_condition` est "dossiers **hors SAS** listes par la
  source de verite" et `PV_NOMINATION_GERANT_STRUCTURES` exclut SAS — donc **non applicable a SAS**
  (coherent : une SPFPLAS a un President, pas un gerant). A ne PAS proposer dans le parcours SAS.
- **Demande d'inscription a l'ordre (DOC-034)** : a verifier au cadrage si elle s'applique au parcours
  SAS / SPFPL medecins (non listee dans l'occurrence case_catalog SAS aujourd'hui).
- **Acte de cession d'ACTIONS (DOC-029)** : appartient au chemin **SPFPL cession (dentistes)**, PAS au
  chemin SAS. A ne pas confondre malgre le vocabulaire "actions".

## 4. Wording EXACT deja disponible (confirme par specs / sources / code)

Disponible sans nouvelle validation (deja tokenise + fige dans le code from-scratch et les specs
texte `lot_04_statuts_sas_spec_texte_v1.md` / `lot_05_sas_satellites_spec_texte_v1.md`) :

1. **Statuts SAS — cartouche** : `<denomination>` / "Société de Participations Financières de
   Profession Libérale de Médecins par actions simplifiée" / "Au capital de <capital_social>" /
   "Siège social : <adresse>" ; titre **STATUTS**.
2. **Statuts SAS — comparution** : "Le soussigné :" ... "Ci après dénommé l' « Associé Unique », ou
   l' « Actionnaire Unique »" ; phrase d'institution sous condition suspensive d'inscription au
   Tableau de l'Ordre des Medecins (texte integral fige dans `statuts_sas.py`).
3. **Statuts SAS — 27 articles** : Forme / Objet / Denomination / Siege / Duree / Apports / Capital
   social / Qualite des associes / Augmentation-reduction du capital / Cession et transmission des
   actions (clause d'agrement 3/4) / Comptes courants / President / Directeurs generaux / Conventions
   / Decisions d'actionnaires / Commissaires aux comptes / Exercice social / Affectation des benefices
   / Capitaux propres < 1/2 capital / Exclusion / Dissolution-liquidation / Transformation /
   Contestations / Condition suspensive / Ordre professionnel / Frais / Jouissance personnalite morale.
   Wording integral present dans `statuts_sas.py` (`_ARTICLE_10_PARAGRAPHS`,
   `_ARTICLES_13_TO_16_PARAGRAPHS`, `_ARTICLES_18_TO_27_PARAGRAPHS`).
4. **Statuts SAS — signature** : "Fait à <lieu>" / "Le" / nom du president, avec mention
   "Faire précéder de la mention « Bon pour acceptation des fonctions de Président »", puis ANNEXE
   "ETAT DES ENGAGEMENTS PRIS AVANT LA CONSTITUTION DE LA SOCIETE".
5. **PV remuneration president** : cartouche + titre encadre "PROCES-VERBAL DES DECISIONS / DE
   L'ASSOCIE UNIQUE / DU <date>" ; "DECISION UNIQUE" : absence de remuneration au titre du mandat
   jusqu'a la cloture du 1er exercice ; remboursement frais sur justificatifs ; "Fait à <lieu> en
   trois exemplaires". Wording fige dans `pv_remuneration_president.py`. **Reserve : le DOCX source
   n'est plus sur disque (B5)** — le wording vit dans le code et la spec, mais la fidelite ne peut plus
   etre recontrolee contre l'original.
6. **Attestation capital** : cartouche "Société par actions simplifiée au capital de ... euros" +
   "Société de Participations Financières de Profession Libérale de <profession>" ; titre
   **ATTESTATION** ; sous-titre **Liste des souscripteurs** ; corps (capital social, nombre d'actions,
   repartition a l'actionnaire unique, bloc "Apports en nature :", total apports nature, apports
   numeraire, certification par le President). Wording fige dans
   `attestation_capital_liste_souscripteurs_sas.py`.
7. **Roles canoniques entierement specifies** : `societe_spfpl`, `actionnaire_unique`, `president`,
   `capital_souscription`, `exercice_social`, `remuneration_president`, `apport_titres`,
   `societe_cible`, `depot_fonds`, `signature`. Modeles Pydantic presents dans
   `src/sydel_doc_engine/domain/models.py`.

Tous ces elements sont du wording **fige dans le code teste**. Ils n'exigent pas de nouvelle validation
Rafael SAUF si la phase NotebookLM revele une contradiction (voir section 5).

## 5. NON TROUVE -> a lever par tokenisation puis Rafael (jamais inventer)

Les points ci-dessous sont des arbitrages **metier / juridiques** non tranchables par le code. Ils
doivent passer par la phase NotebookLM (transcripts Albane / docs sources) PUIS, si absents ou
contradictoires, par un message a Rafael (jamais une question au PM, regle projets a associe).

1. **Nature exacte du document SAS** : le chemin source est "SAS" mais le texte vise une SPFPL de
   medecins par actions simplifiee. Confirmer que ce document EST bien le "statut SAS" attendu par le
   metier (point ouvert 1 des deux specs). **Non tranche.**
2. **President / actionnaire feminin** : la source utilise "il" / "Monsieur" / "Le Docteur" ; aucune
   variante feminine n'est sourcee. Le code bloque le genre feminin. Le wording feminin (accords,
   "Madame", "la Docteure"...) est **non source**.
3. **Situation matrimoniale autre que mariee** : la phrase source suppose un regime matrimonial + un
   conjoint ; le code n'accepte que `situation_maritale` commencant par "mari". Celibataire / divorce /
   PACS / veuf / sans conjoint = **non source** (point ouvert 4 spec statuts).
4. **Multi-actionnaires (statuts) et multi-souscripteurs (attestation)** : sources mono-personne. Les
   formes de comparution "plusieurs soussignes", table d'apports dynamique, repartition dynamique des
   actions, signatures multiples = **non sources** (point ouvert 3 spec statuts, point ouvert 6 spec
   satellites).
5. **Incoherences de vocabulaire dans la source statuts** : certains passages emploient "parts
   sociales", "gérant", "gérance", "parts" dans un document **par actions simplifiee** (ex. article 4
   "décision du gérant seul", article 10.3 "les parts de la Société"). Aucune correction de wording
   juridique ne doit etre faite sans validation (point ouvert 5 spec statuts). **A confirmer Rafael.**
6. **Alias `valeur_nominale_part`** (attestation) : la source emploie ce placeholder alors que le texte
   parle d'actions ; ne pas corriger le wording sans validation (point ouvert 8 spec satellites).
7. **Qualite affichee de l'associe / actionnaire** (`qualite_associe`) : le placeholder source doit
   etre fourni ou arbitre pour eviter une variation locale (point ouvert 4 spec satellites).
8. **Lieu de signature de l'attestation** : la source emploie `[ville_siege]` ; confirmer qu'il
   correspond a `signature.lieu` ou prevoir une saisie dediee (point ouvert 9 spec satellites).
9. **Remuneration positive du president** : la source ne couvre que l'absence de remuneration jusqu'a
   la cloture du 1er exercice. Toute remuneration positive / variable / differee = **non source**.
10. **Condition suspensive Ordre** : confirmer qu'elle s'applique a tous les dossiers SAS cibles
    (point ouvert 6 spec statuts).
11. **Attestation : variante numeraire-only** : la source impose un bloc apport en nature ; une
    attestation 100 % numeraire n'est pas sourcee (point ouvert 7 spec satellites).

## 6. Besoins envers le SOCLE PARTAGE (couche commune requise par SAS)

Ce que SAS exige du socle, au-dela de ce qui existe deja pour la SELARL :

1. **Slice front + deroulante auto-extensible (MANQUANT, c'est le coeur du build front).**
   - `front_app/dossier_selection.py` ne contient que `selarl_v1` (constante
     `CLEAN_DOSSIER_TYPE_OPTIONS`). Il faut y ajouter une entree `sas_spfpl_medecins_v1` (ou
     equivalent), dans une **deroulante auto-extensible** par type d'entreprise.
   - Il faut un `front_app/sas_slice.py` sur le patron de `selarl_slice.py` (`SasSliceInput` +
     `build_sas_plan` + `build_generation_context` + `generate_sas_dossier`), branche dans
     `front_app/shell.py` (aujourd'hui code en dur sur SELARL : `generate_selarl_dossier`, prefill
     SELARL, libelles "SELARL V1"). Le shell doit **router selon le type de dossier** au lieu d'appeler
     directement la slice SELARL.
2. **Couche "substitution parts/actions, gerant/president".** La SAS V1 = **President + actions**
   (alors que la SELARL = gerant + parts sociales). Le moteur SAS pose deja President/actions par role,
   mais le **front** SELARL est cable "gerant"/"parts sociales" en dur
   (`selarl_slice.build_generation_context`). Une slice SAS doit poser **President / actions**. C'est
   exactement la bascule de vocabulaire dirigeant + titres demandee par le brief.
3. **Couche multi "LES SOUSSIGNES" / repartition numerotee / PV d'AG.**
   - **NON requise pour le perimetre SAS V1** : tous les documents SAS V1 sont mono-actionnaire /
     mono-souscripteur (PV des decisions de **l'associe unique**, "Le soussigné" au singulier).
   - Le socle multi-associes / PV d'AG n'est donc PAS un prerequis du parcours SAS V1. Il ne le
     deviendrait que pour la variante multi-actionnaires (hors V1, non sourcee — section 5 pt 4).
4. **Personne morale associee.** **NON requise pour le perimetre SAS V1** : l'actionnaire unique est
   une personne physique (medecin). La couche personne morale associee existe ailleurs
   (`StatutsCivilsAssocie.type_personne == "personne_morale"`, `AssocieCible`) mais n'est pas mobilisee
   par SAS V1.
5. **Couche genre.** Existe deja (`domain/enums.Gender`, `field_derivations.derive_gender_from_civilite`,
   `utils/grammar.py`). **Attention** : le moteur SAS V1 est verrouille **masculin uniquement**
   (statuts + satellites). La couche genre n'est PAS branchee sur le wording SAS (dette feminin =
   section 5 pt 2). Une slice front SAS doit donc, en V1, soit borner a masculin, soit afficher le
   feminin comme bloque.
6. **Registre.** `registry/catalog.py` contient deja les 3 definitions SAS (DOC-015, DOC-023, DOC-024)
   avec conditions de selection ; `domain/case_catalog.py` liste les occurrences du cas SAS ;
   `orchestrator/service.py` cable les generateurs et leurs predicats d'activation
   (`_statuts_sas_enabled`, `_sas_pv_remuneration_president_enabled`, `_sas_attestation_capital_enabled`).
   Le registre est **pret** ; rien a ajouter cote moteur pour le perimetre V1 documente.
7. **Statut document front.** `front_data/document_status.py` (`build_document_status_for_code`),
   utilise par la slice SELARL pour afficher libelles/etats (generable / conditionnel / hors-V1 /
   bloque), sera reutilise par une slice SAS.
8. **Profession / Ordre des Medecins.** Le moteur exige les champs ordre (`departement`, `numero`,
   `numero_rpps`). La couche saisie front doit exposer ces champs Ordre des Medecins (existe deja en
   partie cote SELARL pour l'Ordre — a verifier la profession medecin).

Resume socle : le **moteur et le registre sont prets** ; le besoin reel est une **couche front SAS**
(slice + entree dans la deroulante de selection + routage shell + bascule **President/actions** +
champs Ordre des Medecins). C'est la meme couche que SELARL, a generaliser/dupliquer, pas a inventer.
La couche **multi-associes / PV d'AG / personne morale n'est PAS requise pour SAS V1** (mono-actionnaire).

## 7. Bloquants de build (decisions de scope / sources / canon)

| Code | Bloquant | Nature | Qui tranche |
|---|---|---|---|
| B1 | Phase NotebookLM SAS jamais faite (pas de `NOTEBOOKLM_ANSWERS.md`, NotebookLM pas ingere) | process / metier | Rafael via NotebookLM ; pilote Naomi/Codex |
| B2 | Statut produit = `INVENTAIRE_TECHNIQUE` : moteur teste mais type NON traite en sprint produit | gouvernance | playbook impose un sprint complet avant "traite" |
| B3 | Aucun slice front SAS ; shell cable SELARL en dur ; deroulante de selection ne contient que `selarl_v1` | technique (constructible) | a builder sur patron SELARL (pas de GO PM requis) |
| B4 | "SAS" = en realite SPFPL Medecins par actions simplifiee uniquement (pas de SAS generique) | scope metier | Rafael (le perimetre SAS attendu est-il bien la SPFPL medecins ?) |
| B5 | **Source DOCX du PV remuneration president introuvable** (`raw_drive_dump/Creation SAS/` nettoye) | source manquante | re-fournir le DOCX source (Rafael/Naomi) pour controle de fidelite ; le wording vit dans le code/spec mais l'original n'est plus verifiable |
| B6 | Rangement SPFPL medecins sous chemin SAS vs SPFPL dentistes sous chemin SPFPL | coherence canon | Rafael (taxonomie des types) |
| B7 | Wording verrouille **masculin uniquement** (statuts + satellites) ; feminin non source | wording juridique | Rafael (variante feminine) |
| B8 | Multi-actionnaires statuts + multi-souscripteurs attestation : non sources | scope / source | bloque V1, a sourcer puis Rafael |
| B9 | Incoherences de vocabulaire source ("gérant"/"parts" dans une SAS) non corrigeables sans validation | wording juridique | Rafael |

**Constructible immediatement, sans GO PM ni validation Rafael** (biais d'action) :
- B3 : slice front SAS perimetre V1 (= exactement ce que le moteur sait deja rendre et qui a un wording
  fige et teste : statuts SAS + universels lot_01 ; + attestation capital si apport ; + PV remuneration
  president si absence de remuneration ; actionnaire unique masculin medecin marie). Aucun wording
  nouveau, aucune regle metier inventee. C'est le patron SELARL applique a SAS, avec la bascule
  President/actions.

**Necessite la phase NotebookLM / Rafael AVANT generation reelle livrable** : tout ce qui touche
B4-B9 (nature SAS, PV source manquante a re-fournir, taxonomie, feminin, multi-*, vocabulaire). Ne pas
livrer ces variantes a Rafael avant validation.

## 8. Recommandation de sequence

1. Ouvrir le **sprint produit SAS** selon `COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` (phase 0, `NO-GO dev`).
2. Phase NotebookLM SAS (lever B1, B4-B9) — pilote Naomi, reponses Rafael, journal de sprint ; en
   priorite re-fournir le DOCX source du PV remuneration president (B5).
3. En parallele (constructible, reversible) : **builder le slice front SAS V1** sur le patron SELARL
   (lever B3), borne au wording deja fige (section 4) : actionnaire unique masculin medecin marie,
   bascule President/actions, champs Ordre des Medecins.
4. Triangulation 3 sources + matrice documentaire + audit reutilisation SELARL/global.
5. Smoke interne (ZIP + controle placeholders `[`/`]`) puis pack pour Rafael (phase 8).
6. Cloture canonique (`DONE` / `PARTIAL` / `BLOCKED`) + mise a jour du registre de statut.

Le moteur etant deja teste, le sprint SAS est principalement un sprint **front + validation metier**,
pas un sprint moteur — strictement comme le constat SPFPL.
