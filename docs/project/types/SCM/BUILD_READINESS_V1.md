# SCM - BUILD READINESS V1 (analyse de constructibilite)

Date : 2026-06-07
Auteur : analyste constructibilite (lecture seule du code, aucune modification de code, aucune action Git)
Perimetre : type d'entreprise SCM du moteur Sydel (Python / python-docx / Streamlit).

## 0. Resume executif (a lire en premier)

**SCM n'est PAS un greenfield.** Contrairement au cadrage initial du ticket ("MVP = bloc
constitution seul", "11 modeles", "min 2 associes PP + SEL associee"), la couche MOTEUR de SCM est
deja LARGEMENT CONSTRUITE ET TESTEE :

- 7 generateurs SCM-natifs codes + 3 generateurs de cession SCM->SEL + 2 documents universels/mutualises ouverts a SCM ;
- catalogue (`registry/catalog.py`) : tous declares `WorkflowStatus.TESTE` ;
- 17 tests unitaires SCM verts (statuts + satellites + cession), lances cette session sur le seul perimetre SCM ;
- arbitrages metier V1 statuts CLOS (`lot_04_statuts_scm_arbitrages_v1.md`, "Aucun arbitrage SCM liste par ce ticket ne reste ouvert").

**Mais SCM n'a JAMAIS ete traite comme un sprint produit.** Le registre de statut canonique
(`COMPANY_TYPE_STATUS_REGISTRY_V1.md`) classe SCM en `INVENTAIRE_TECHNIQUE` (12 cas catalogue / 10
testes) et interdit explicitement de dire "SCM est terminee" tant qu'aucun sprint complet n'a
applique : NotebookLM + reuse + matrice + pack + retour humain. Concretement il manque :

1. **Aucune passe NotebookLM SCM** (aucun fichier `NOTEBOOKLM*` SCM ; seuls SELARL et SELAS en ont). Les 9 points ouverts de la spec satellites n'ont jamais ete leves par Rafael.
2. **SCM absent du front de production "clean" (Track B).** Le seul `DossierTypeOption` expose est `SELARL creation V1`. "SCM" dans le front n'existe que comme case a cocher SOUS SELARL (branche cession SCM->SEL), pas comme type creable.
3. **Borne dure "exactement 2 associes"** sur les 4 satellites de constitution, alors que les statuts SCM scalent de 1 a 6. Incoherence de perimetre a arbitrer.

**Note de cadrage divergente** : le ticket parle de "11 modeles" ; le repo expose 12 cas catalogue
SCM (dont 3 de cession qui se declenchent cote SELARL/SELAS, pas cote SCM). La cible MVP "bloc
constitution seul" = 5 documents SCM-natifs + 2 documents universels/mutualises. Voir sections 1-3.

---

## 1. Inventaire des modeles source (fichier -> document juridique + cas couvert)

Aucun repertoire `project/source_documents/scm` n'existe. Les sources SCM sont reparties dans
`project/source_documents/lot_04` (statuts) et `lot_05` (satellites + cession). Tous les fichiers
ci-dessous ont ete ouverts et identifies.

### 1.1 Constitution SCM (cote SCM)

| Fichier source | Document juridique | Cas | Etat tokenisation |
|---|---|---|---|
| `lot_04/Statuts SCM.docx` | Statuts constitutifs SCM | Creation SCM | Tokenise (`[denomination_societe]`, `[forme_sociale]`, multi-soussignes `_societe_1` / `_personne_2`, apports, parts) |
| `lot_05/Pacte d_associés SCM.docx` | Pacte d'associes (parts sociales SCM) | Creation SCM (option) | Tokenise (`[civilite_personne_1..2]`, `[denomination_societe]`, `[ville_rcs]`, `[numero_rcs]`) |
| `lot_05/REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx` | Reglement interieur SCM | Creation SCM (option) | Tokenise (`_societe_1` / `_societe_2`, `[titre_representant_societe_x]`, `[identite_representant_societe_x]`) ; 14 tables |
| `lot_05/CONTRAT FRAIS COMMUNS.docx` | Contrat d'exercice professionnel a frais communs | Creation SCM (option) | Tokenise (`_societe_1` / `_societe_2`, `[adresse_locaux]`) ; 1 table |
| `lot_05/Liste dépenses communes SCM.docx` | Liste/tableau des depenses communes SCM | Creation SCM (option) | Tokenise (`[denomination_societe]`, `[prenom_personne_1..2]`) ; 1 table. Source `.doc` ORIGINE convertie en `.docx` (les deux coexistent sur disque) |
| `lot_05/Liste dépenses communes SCM.doc` | Idem, version legacy `.doc` | Source legacy | A NE PAS coder directement (cf. spec) ; remplacee par le `.docx` ci-dessus |

### 1.2 Cession de parts SCM vers SEL (cote SELARL / SELAS, PAS cote SCM)

| Fichier source | Document juridique | Cas | Overlay |
|---|---|---|---|
| `lot_05/PV AGE cession part SCM.docx` | PV AGE de cession de parts SCM | Cession SCM->SEL | SELARL |
| `lot_05/PV AGE cession part SCM - SELAS.docx` | PV AGE de cession de parts SCM | Cession SCM->SEL | SELAS |
| `lot_05/Courrier SDE.docx` | Courrier SDE (enregistrement actes de cession) | Cession SCM->SEL | SELARL (4 exemplaires, pas de destinataire fiscal) |
| `lot_05/Courrier SDE - SELAS.docx` | Courrier SDE | Cession SCM->SEL | SELAS (destinataire fiscal, exemplaires variables) |
| `lot_05/Acte de cession des parts de la SCM à la SELARL - transforme.docx` | Acte de cession de parts SCM vers SEL | Cession SCM->SEL | SELARL (source transformee) |
| `lot_05/Acte_cession_parts_SCM_SEL_modele.docx` | Acte de cession de parts SCM vers SEL | Cession SCM->SEL | SELAS (source modele dediee) |

### 1.3 Documents transverses ouverts a SCM (mutualises)

| Fichier source | Document | Cas SCM |
|---|---|---|
| `lot_02/PV nomination gérant - transforme.docx` | PV nomination gerant | SCM dans `PV_NOMINATION_GERANT_STRUCTURES` |
| `lot_02/Demande d_inscription à l_ordre - transforme.docx` | Demande d'inscription a l'ordre | SCM dans `DEMANDE_INSCRIPTION_ORDRE_STRUCTURES` (uniquement avec donnees ordinales explicites) |
| `lot_01/*` (3 universels) | Declaration non-condamnation, autorisation domiciliation, procuration | SCM dans `ALL_STRUCTURES` (statut `SPECIFIE`, non implementes) |

Non present dans le repo mais cite par les specs : `Fiche de creation de SCM - transforme.docx`
(traitee comme support de collecte, hors generateur statuts).

---

## 2. Cas couverts

- **Creation SCM** (cible MVP) : statuts + 4 satellites optionnels (pacte, RI, contrat frais communs, liste depenses). Codes et testes.
- **Cession de parts SCM vers une SEL** : se declenche cote SELARL/SELAS (`dossier.options.scm_cession == true`), PAS comme parcours SCM. 3 documents x 2 overlays. Codes et testes.
- **Multi-associes** : statuts SCM = 1 a 6 associes, personnes physiques OU morales (incl. SEL associee). Satellites = EXACTEMENT 2 parties/associes (borne dure source).
- **Apport** : apports en numeraire par associe, controle de somme apports == capital et parts == nb_parts_total (bloquant si incoherent).
- **NON couverts en V1** : SCM > 2 associes pour les satellites ; associe historique personne morale au pacte ; locaux non dentaires au contrat frais communs ; formes juridiques differentes entre les 2 parties du RI ; cle de repartition autre que "temps d'occupation des salles de soin".

---

## 3. Documents a generer (statut + approche recommandee)

Statut : `systematique` (toujours produit pour le cas), `conditionnel` (selon option),
`hors-creation` (parcours cession, hors MVP constitution), `separe` (document distinct deja existant ailleurs).
Approche : `template-fill` (modele tokenise rempli), `from-scratch` (reconstruit en code), `a-tokeniser` (modele present, pas encore tokenise).

| Doc | DOC-id | Statut | Approche actuelle dans le code | Etat |
|---|---|---|---|---|
| Statuts SCM | DOC-025 | systematique (creation) | from-scratch avec reprise du source par index de paragraphes (`ASSOCIATE_SLICE`, `APPORT_SLICE`...) | CODE + TESTE. Dette : index de paragraphes en dur, fragile au changement de source |
| Pacte d'associes SCM | DOC-026 | conditionnel (`scm_satellites.pacte_associes`) | template-fill (`generate_from_template` + `TemplateBlock`) | CODE + TESTE. Borne 2 associes |
| Contrat frais communs | DOC-027 | conditionnel (`scm_satellites.contrat_frais_communs`) | template-fill | CODE + TESTE. Borne 2 parties, locaux dentaires figes |
| Reglement interieur SCM | DOC-028 | conditionnel (`scm_satellites.reglement_interieur`) | template-fill | CODE + TESTE. Borne 2 parties, formes juridiques identiques exigees |
| Liste depenses communes SCM | DOC-030 | conditionnel (`scm_satellites.liste_depenses_communes`) | template-fill | CODE + TESTE. Source `.docx` convertie OK, table figee, 2 signatures |
| PV nomination gerant | DOC-004 | systematique (creation, hors SAS) | mutualise | CODE + TESTE (mais sans UI/PDF/ZIP au niveau catalogue) |
| Demande inscription ordre | DOC-034 | conditionnel (donnees ordinales) | mutualise | CODE + TESTE |
| Declaration non-condamnation | DOC-001 | systematique (universel) | non implemente (`SPECIFIE`) | A IMPLEMENTER (commun a tous les types) |
| Autorisation domiciliation | DOC-002 | systematique (universel) | non implemente (`SPECIFIE`) | A IMPLEMENTER (arbitrage rendu adresse en suspens) |
| Procuration | DOC-003 | systematique (universel) | non implemente (`SPECIFIE`) | A IMPLEMENTER |
| PV AGE cession part SCM | DOC-031 | hors-creation (cession, cote SEL) | from-scratch + overlay SELARL/SELAS | CODE + TESTE |
| Courrier SDE cession SCM | DOC-032 | hors-creation (cession, cote SEL) | from-scratch + overlay | CODE + TESTE |
| Acte cession parts SCM->SEL | DOC-033 | hors-creation (cession, cote SEL) | from-scratch + overlay | CODE + TESTE |

**Recommandation d'approche** : pour SCM, le code existant respecte deja la doctrine "template-fill
quand le modele est tokenise" (les 4 satellites) et "from-scratch" la ou la reprise paragraphe par
paragraphe etait necessaire (statuts, cession). Aucun document SCM n'est "a-tokeniser" : tous les
modeles presents sont tokenises. Le travail restant n'est PAS de la generation moteur mais de
l'EXPOSITION FRONT + LEVEE NLM (sections 5-6).

---

## 4. Wording EXACT deja disponible (sources confirmees)

Le wording canonique SCM est deja stabilise dans les specs delivery (squelettes = extraits verbatim
des sources, "ne modifie aucun wording juridique source") :

- `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md` (arbitrages statuts, CLOS)
- `docs/delivery/lot_05_scm_satellites_spec_texte_v1.md` (squelettes texte verbatim : pacte, liste depenses, contrat frais communs, RI + listes de variables obligatoires par document)
- `docs/delivery/lot_05_scm_satellites_spec_canonique_v1.md`
- `docs/delivery/lot_05_scm_cession_block_spec_texte_v1.md` (wording cession)
- `docs/delivery/lot_05_scm_cession_block_resolution_v1.md` (decision "go code 6 docs", overlays SELARL/SELAS)
- `docs/delivery/lot_05_scm_cession_block_spec_canonique_v1.md`

Wording structurant deja confirme dans ces sources :
- Pacte : `PACTE D'ASSOCIES PORTANT SUR LES PARTS SOCIALES DE LA SOCIETE`, `LES SOUSSIGNEES`, 6 titres (I a VI), annexes 1 (statuts) et 2 (acte d'adhesion), clause tribunal de commerce.
- Liste depenses : en-tete societe + table fixe `DENOMINATION DE LA DEPENSE` / `AU PRORATA DES PARTS DE SCM` / `AU PRORATA CHIFFRE D'AFFAIRES` (15 lignes source avec marques `X`).
- Contrat frais communs : `CONTRAT D'EXERCICE PROFESSIONNEL A FRAIS COMMUNS`, articles 1 a 8, locaux dentaires decrits en dur, cle au temps d'occupation.
- RI : `REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS`, preambule + articles 1 a 10, `En quatre exemplaires`.
- Cession : overlays SELARL (4 exemplaires, sans destinataire fiscal) vs SELAS (destinataire fiscal, exemplaires variables) ; date de l'acte reste zone manuelle (source ne contient que `Le`).

---

## 5. NON TROUVE -> a lever par tokenisation PUIS Rafael (ne jamais inventer de wording)

La tokenisation est DEJA faite (tous les modeles SCM presents sont tokenises). Le NON TROUVE est
donc purement metier/juridique : ce sont les **9 points ouverts de la spec satellites** +
arbitrages cession, jamais leves par une passe NotebookLM/Rafael (aucune passe NLM SCM n'existe).

A confirmer par Rafael (via Gad) AVANT d'exposer SCM en production :
1. **Activation du batch satellites** : generation automatique vs selection explicite des satellites a produire.
2. **Borne "exactement 2 associes/parties"** : la confirmer comme regle V1 OU sourcer une version N (>2). Les 4 sources sont stabilisees sur 2 ; aucune version N n'est sourcee.
3. **Pacte** : confirmer les clauses sensibles (cession/preemption/non-concurrence) et le traitement des annexes (statuts en annexe 1, acte d'adhesion annexe 2).
4. **Liste depenses** : confirmer la table source (15 lignes), les marques `X` et les lignes sans marque (`Achat valide par la SCM`).
5. **Contrat frais communs** : confirmer la description FIXE des locaux dentaires et la cle de repartition "temps d'occupation des salles de soin".
6. **Reglement interieur** : confirmer le placeholder unique de forme sociale (impose 2 parties de meme forme), les clauses telephone, le nombre de "quatre exemplaires".
7. **Profession / titres** : confirmer les mentions `Docteur`, `praticien`, `cabinet dentaire` (specifiques au dentaire dans les sources) -> generalisables au medecin ou pas ?
8. **Coherence statuts <-> satellites** : confirmer les donnees communes a controler (numero_rcs, nb_parts_total, associes, parts).
9. **Cession** : roles exacts des personnes source `personne_1..4`, president de seance, date de l'acte (zone manuelle), credit-vendeur conditionnel.

Point ouvert n.1 de la spec (source `.doc` a convertir) = **RESOLU** : `Liste dépenses communes SCM.docx` existe sur disque.

---

## 6. Besoins envers le SOCLE PARTAGE

Ce que le type SCM exige de la couche commune (par rapport au patron SELARL) :

1. **Substitution parts/actions, gerant/president** : SCM = societe civile a PARTS et GERANT. Deja
   gere : `StatutsCivilsContext` (`nb_parts_total`, `valeur_nominale_part`, `parts.nb` par associe),
   `GeranceContext`. Le socle doit garantir que le vocabulaire "parts" / "gerant" (et non
   "actions" / "president") est porte par le type, comme pour SCS/SCI.

2. **Couche multi "LES SOUSSIGNES" / repartition numerotee / PV d'AG** :
   - Comparution multi-associes : DEJA en place dans `statuts_scm` (`_add_associate_block` boucle sur `associes[]`, separateur "ET", jusqu'a 6).
   - Repartition numerotee : `_add_capital_block` + controle de somme. Le PV AGE cession affiche `1° / 2° / 3°` (repartition numerotee) -> deja rendu cote cession.
   - **EXIGENCE SOCLE** : le bloc "LES SOUSSIGNEES" des satellites est aujourd'hui FIGE a 2 (helpers `_required_two_associes`, `required_two_parties`, `TWO_PARTIES = 2`). Pour un socle reellement multi-N, ces helpers devront etre generalises APRES arbitrage Rafael (point ouvert n.2). En l'etat, le socle multi-N existe cote statuts mais PAS cote satellites.

3. **Personne morale associee** : DEJA gere cote statuts (`_is_morale`, `_add_morale_identity`,
   `ScmRepresentant`, representant + fonction). SCM exige une SEL associee -> couvert par
   `type_personne == "personne_morale"` + `representant`. EXIGENCE : le socle doit exposer ce
   modele "associe personne morale avec representant" de facon stable (deja dans `StatutsCivilsAssocie`).
   Cote satellites, le pacte BLOQUE l'associe historique personne morale en V1 (point ouvert n.3).

4. **Couche genre** : SCM utilise `Gender` (Né/Née selon `associe.genre`) dans les statuts. Les
   satellites s'appuient sur `civilite_affichage` / `identite_affichee` (pas de derivation de genre
   complexe). EXIGENCE socle : derivation genre depuis civilite (deja dans `front_app.field_derivations.derive_gender_from_civilite`).

5. **Registre (catalog)** : SCM est DEJA cable dans `registry/catalog.py` (DOC-025 a DOC-033 pertinents)
   et `domain/case_catalog.py` (`CaseType.SCM`, occurrences, `DocumentAvailability.GENERATABLE`).
   EXIGENCE : aucune ; le registre porte deja SCM.

6. **Slice front + deroulante auto-extensible** : **MANQUANT.** Le front "clean" Track B
   (`front_app/shell.py` -> `render_clean_front`) n'expose QUE `SELARL creation V1`
   (`dossier_selection.CLEAN_DOSSIER_TYPE_OPTIONS`). Il n'existe AUCUN `scm_slice.py` equivalent a
   `selarl_slice.py`. EXIGENCES precises du socle pour exposer SCM :
   - un `DossierTypeOption` "SCM creation V1" dans `CLEAN_DOSSIER_TYPE_OPTIONS` ;
   - un `scm_slice.py` (sur le patron `selarl_slice.py`) qui mappe la saisie -> `DocumentGenerationContext` SCM puis appelle `generate_docx_files_for_document_codes` + `generate_zip_file` ;
   - une **deroulante auto-extensible d'associes** (le front SELARL gere des associes additionnels via `SelarlAdditionalAssocieInput` ; SCM doit reutiliser/generaliser ce composant pour 1 a 6 associes, et le brider a 2 pour les satellites tant que Rafael n'a pas tranche le point ouvert n.2) ;
   - selecteurs d'options satellites (`scm_satellites.pacte_associes`, etc.) + saisie des champs locaux (`pacte_associes.ville_tribunal`, `frais_communs.date_effet_contrat`, `reglement_interieur.*`, `locaux.adresse_affichee`, `praticiens[]`).

7. **PDF / ZIP / bundle** : `rendering/pdf_export.py`, `zip_bundle.py`, `bundle.py` existent et sont
   utilises par `ui_runtime`. EXIGENCE : brancher SCM dessus via le slice front (le moteur produit
   deja des DOCX valides).

Note : le ticket cite `rendering/docx_template_fill.py` -> ce fichier N'EXISTE PAS. Le template-fill
SCM passe par `generators/lot_05/scm_satellites_common.py::generate_from_template` +
`scm_satellites_templates.py`. Les helpers DOCX communs sont dans `rendering/docx_builder.py`.

---

## 7. Bloquants de build

### B1 - Decision de scope front (technique, decidable par l'equipe)
SCM n'est pas expose dans le front de production. Construire `scm_slice.py` + l'option de type est
constructible MAINTENANT sur branche dediee (le moteur et le wording sont prets). Non bloquant pour
le moteur ; bloquant pour livrer un parcours utilisateur SCM.

### B2 - Borne "2 associes" satellites vs "6 associes" statuts (METIER -> Rafael)
Incoherence de perimetre : les statuts acceptent 1-6 associes, les 4 satellites en exigent
exactement 2. Si un client SCM a 3 associes, les statuts se generent mais les satellites BLOQUENT.
A arbitrer (point ouvert n.2). Ne PAS lever en inventant une variante N : sourcer ou confirmer la borne 2.

### B3 - Passe NotebookLM SCM jamais faite (METIER -> Rafael)
Les 9 points ouverts (section 5) n'ont jamais ete confirmes par retour humain. Le registre canonique
interdit de declarer SCM "traite" sans cette passe. Bloquant pour passer SCM de
`INVENTAIRE_TECHNIQUE` a "type produit livre".

### B4 - Documents universels non implementes (DOC-001/002/003)
Declaration non-condamnation, autorisation domiciliation, procuration sont `SPECIFIE` (pas codes) et
systematiques pour TOUT type. DOC-002 a un arbitrage rendu d'adresse en suspens. Bloquant pour un
dossier de constitution SCM "complet". Transverse, pas propre a SCM.

### B5 - Dette technique statuts (technique, non bloquant)
`statuts_scm.py` reprend la source par index de paragraphes en dur
(`ASSOCIATE_SLICE = (25, 42)`, etc.). Toute reedition du DOCX source casse silencieusement le
mapping. A surveiller ; non bloquant tant que la source ne bouge pas.

### Ce qui N'EST PAS bloquant
- Tokenisation : faite. Wording satellites/cession : stabilise dans les specs delivery. Moteur :
  code + 17 tests verts. Registre : SCM cable.

---

## 8. Verification effectuee (perimetre nomme)

- 17 tests unitaires SCM verts, lances cette session sur le PERIMETRE SCM UNIQUEMENT
  (`test_statuts_scm.py`, `test_lot_05_scm_satellites.py`, `test_lot_05_scm_cession.py`,
  `--basetemp=artifacts/_audit_tmp/pt`). Suite globale NON relancee (hors scope audit).
- Tous les fichiers source SCM (section 1) ouverts et identifies via python-docx.
- Specs delivery SCM et registre de statut canonique relus.
- Aucun fichier de code modifie. Aucune action Git.
