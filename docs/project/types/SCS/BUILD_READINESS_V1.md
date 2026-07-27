# SCS — Build Readiness V1 (analyse de constructibilite)

Date : 2026-06-07
Auteur : analyste de constructibilite (lecture seule du code ; aucune modif de code ; aucune action Git)
Type : SCS = **Societe en Commandite Simple** (civile / objet immobilier), capital VARIABLE,
parts sociales, roles **commandite / commanditaire**, 1 a 6 associes.

> Note de cadrage sur les chemins du prompt : plusieurs chemins cites dans la mission n'existent
> pas en l'etat. Realite observee :
> - **Modele source SCS** = `project/source_documents/lot_04/Statuts_SCS_modele.docx` (il n'existe
>   AUCUN repertoire `project/source_documents/scs/`). C'est le SEUL modele SCS-natif du repo.
> - **Aucune synthese NotebookLM SCS** : ni `docs/project/types/SCS/NOTEBOOKLM_ANSWERS.md`, ni
>   `..._PROMPTS_V2.md`, ni aucun fichier `NOTEBOOKLM*` nulle part dans le repo. NLM jamais ingere
>   pour ce type (conforme au cadrage). Source-of-truth metier = `project/source_truth/Documents_a_generer_par_cas.docx`.
> - **Recette canonique reelle** = `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` (il n'y a pas de
>   `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`).
> - **Couche rendu** = `src/sydel_doc_engine/rendering/docx_builder.py` (pas de `docx_template_fill.py`).
>   Le `lot_01..05` "SELARL livree" n'est pas une arborescence de generateurs dediee SELARL : ce sont
>   les lots de documents, partages entre types.
> - **Le moteur des statuts SCS EST DEJA CODE ET TESTE** (`DOC-019`, `WorkflowStatus.TESTE`,
>   `generators/lot_04/statuts_scs.py` -> `statuts_civils_common.py`, `SCS_TEMPLATE`). Le chantier
>   restant pour SCS n'est PAS le moteur des statuts : c'est le **front (slice Streamlit)** + le
>   branchement des **documents universels** (DOC-001/002/003) + la **levee NLM/Rafael** des points metier.

---

## 0. Etat synthetique (a lire en premier)

| Brique | Etat observe | Constructible maintenant ? |
|---|---|---|
| Moteur statuts SCS (DOC-019) | code + teste (`statuts_scs.py` -> `statuts_civils_common.py`, `SCS_TEMPLATE`) | DEJA FAIT |
| PV nomination gerant (DOC-004) | code + teste, SCS dans `PV_NOMINATION_GERANT_STRUCTURES` | DEJA FAIT (a cabler au parcours SCS) |
| Declaration non-condamnation (DOC-001) | generateur existant, `WorkflowStatus.SPECIFIE` (pas branche/teste catalogue) | A CABLER / A FINIR (universel, transverse) |
| Autorisation domiciliation (DOC-002) | generateur existant, `SPECIFIE` (arbitrage rendu adresse note) | A CABLER / A FINIR (universel) |
| Procuration (DOC-003) | generateur existant, `SPECIFIE` | A CABLER / A FINIR (universel) |
| Slice front SCS (Streamlit) | **inexistant** (seul `selarl_slice.py` existe ; `dossier_selection` n'expose que `SELARL creation V1`) | A CONSTRUIRE |
| Saisie "associe personne morale" au socle front | geree dans le moteur civils ; **pas dans le socle front** | A ETENDRE (socle) |
| Passe NotebookLM SCS | **jamais faite** (aucun fichier NLM) | A LEVER (Rafael via Gad) |

Conclusion : **SCS n'est PAS un greenfield au niveau moteur.** Les statuts SCS sont code + testes
(2 tests SCS-specifiques verts cette session, voir section 8). La readiness "produit" depend d'un
**slice front SCS** + branchement des 3 documents universels + une **passe NLM/Rafael** sur quelques
points metier — pas d'une re-ecriture des statuts.

---

## 1. Inventaire des modeles source (fichier -> document juridique + cas)

Le SCS n'a **qu'un seul** modele source natif. Il vit dans `lot_04` (pas de dossier `scs/`).

| Fichier source | Document juridique | Cas couvert | Tokenise ? |
|---|---|---|---|
| `project/source_documents/lot_04/Statuts_SCS_modele.docx` (289 paragraphes, 0 table) | **Statuts constitutifs d'une Societe en Commandite Simple** (par. 19 : "les statuts d'une Societe en commandite simple qu'ils ont decide d'instituer entre eux") ; objet **civil immobilier** (acquisition/administration/gestion d'immeubles, art. 2) ; **capital variable** (art. 7-8) | Creation SCS : associes commandites + commanditaires, 1-6 associes, eventuel associe personne morale dans la repartition | OUI — placeholders `[...]` : `[denomination_societe]`, `[forme_sociale]`, `[capital_social]`, `[capital_lettres]`, `[capital_social_maximal]`, `[adresse_siege]`, `[ville_rcs]`, `[duree_societe]`, `[civilite/prenom/nom/date_naissance/...personne_1..2]`, `[apport(_commanditaire)_(lettres_)personne_x]`, `[total_apports_commandites]`, `[nb_parts(_lettres)_personne_x]`, `[plage_parts_personne_x]`, `[denomination_societe_associe_1]` / `[parts_societe_associe_1]`, `[valeur_nominale_part(_lettres)]`, `[qualite_associe_personne_2]` |

Documents transverses qui s'appliquent AUSSI au cas SCS mais qui vivent dans d'autres lots (catalogue,
section 6) : `lot_01/declaration_non_condamnation_transforme.docx`, `lot_01/autorisation_domiciliation_transforme.docx`,
`lot_01/procuration_transforme.docx` (universels), `lot_02/PV nomination gerant - transforme.docx`.

Constat de tokenisation : le modele SCS est **deja tokenise** ET **deja consomme** par le moteur
(`statuts_civils_common.generate_statuts_civil_docx` valide en fin de rendu l'absence de tout `[`/`]`
residuel). **Aucun modele SCS a-tokeniser.** Le SCS ne dispose d'aucun autre modele natif (pas de PV
specifique SCS, pas d'acte de cession SCS, pas de satellite SCS).

---

## 2. Cas couverts

Source metier : `project/source_truth/Documents_a_generer_par_cas.docx` (bloc SCS) + arbitrages
`docs/delivery/lot_04_statuts_civils_arbitrages_v1.md` (section 8 : perimetre V1 = SCS/SCI/SCI IRIS/SCM
comme 4 statuts civils distincts, non fusionnables).

- **Creation SCS** (objet civil immobilier, capital variable) — COUVERT (moteur teste).
- **Multi-associes 1 a 6** (`MAX_ASSOCIES = 6`), apports/parts/numerotation dynamiques par associe — COUVERT.
- **Roles commandite / commanditaire** : OBLIGATOIRES et explicites ; le code refuse de generer si
  un role manque (`_validate_scs`), et le role n'est JAMAIS deduit du rang dans `associes[]`
  (regle d'arbitrage explicite) — COUVERT.
- **Associe personne morale dans la repartition du capital** (`[denomination_societe_associe_1]`) :
  modele de donnees `type_personne = personne_morale` + representant — COUVERT cote moteur
  (`_add_morale_identity`, `_signature_label` morale) si le dossier fournit les donnees.
- **Apports separes commandite vs commanditaire** + total commandites + controle de somme
  (apports == capital, parts == nb_parts_total) — COUVERT.
- **Signature "Lu et approuve"** en grille (specificite SCS vs SCI/SCI IRIS) — COUVERT (`add_statuts_signature_grid`).

Cas **NON couverts / hors source V1** (aucun modele SCS present) :
- **Cession de parts SCS**, **transformation**, **dissolution**, **apport en nature** : aucun modele
  source -> hors scope (non trouve). Les actes de cession existants visent SCM/SPFPL/cabinet, pas la SCS.
- **PV d'AG SCS** (autres que nomination gerant) : aucun modele SCS.
- **SCS professionnelle / inscription a l'ordre** : SCS est **absent** de
  `DEMANDE_INSCRIPTION_ORDRE_STRUCTURES` (coherent : la source SCS est une SCS civile immobiliere,
  pas une structure d'exercice professionnel). Pas de demande d'inscription a l'ordre en V1.

---

## 3. Documents a generer (statut + approche recommandee)

Statut : `systematique` (toujours produit pour le cas), `conditionnel` (selon option), `hors-creation`
(hors MVP constitution), `separe` (document distinct). Approche : `template-fill` (modele tokenise
rempli), `from-scratch` (reconstruit en code), `a-tokeniser` (modele present, pas tokenise).

| Document | Code | Statut (cas creation SCS) | Approche actuelle dans le code | Etat |
|---|---|---|---|---|
| Statuts SCS | DOC-019 | systematique | **template-fill** : le moteur reproduit la source paragraphe par paragraphe et n'insere en code QUE 4 blocs (associes `associate_slice=(14,18)`, apports `apport_slice=(43,58)`, capital `capital_slice=(63,76)`, signatures `append_signatures_after=253`) | CODE + TESTE |
| PV nomination gerant | DOC-004 | systematique (SCS dans `PV_NOMINATION_GERANT_STRUCTURES`) | mutualise/from-scratch (`lot_02`, `dynamic_associates`) | CODE + TESTE ; A CABLER au parcours SCS |
| Declaration non-condamnation | DOC-001 | systematique (universel, `ALL_STRUCTURES`) | template-fill (`lot_01`, `grammar_variants=True`) | generateur existe ; `WorkflowStatus.SPECIFIE` au catalogue ; A CABLER / FINIR |
| Autorisation domiciliation | DOC-002 | systematique (universel, `ALL_STRUCTURES`) | template-fill (`lot_01`) | generateur existe ; `SPECIFIE` ; arbitrage rendu adresse note ; A CABLER / FINIR |
| Procuration | DOC-003 | systematique (universel, `ALL_STRUCTURES`) | template-fill (`lot_01`) | generateur existe ; `SPECIFIE` ; A CABLER / FINIR |

Aucun document SCS n'est `a-tokeniser` (le seul modele SCS est deja tokenise). Aucun document SCS
n'est `conditionnel` natif (pas de satellites SCS sources). Aucun document SCS `hors-creation` n'a de
modele (cession/transformation = non trouve, section 5).

**Recommandation d'approche** : ne PAS reecrire les statuts SCS (template-fill, teste). Le travail
restant est : (a) construire le slice front SCS ; (b) cabler DOC-004 au parcours SCS ; (c) finir +
cabler les 3 universels DOC-001/002/003 (chantier transverse, pas propre a SCS). Reutiliser
`statuts_civils_common` tel quel (ne pas dupliquer).

---

## 4. Wording EXACT deja disponible (sources confirmees)

Le wording statutaire SCS est **integralement disponible et fige** : le modele EST la source, et le
moteur ne fait que substituer des variables (texte source non modifie, controle anti-placeholder en
sortie). Wording confirme, repris verbatim par le moteur :

- En-tete : `Au capital minimal de [capital_social] et effectif de [capital_social]`, `Siege social : [adresse_siege]`, `En cours d'immatriculation au RCS de [ville_rcs]`.
- Comparution : `LES SOUSSIGNES :` puis identite par associe (physique : `Ne/Nee le ... a ... (...)`, `De nationalite ...`, situation maritale, `Demeurant ...` ; morale : forme + `au capital de ...` + `ayant son siege ...` + `immatriculee au RCS de ... sous le numero ...` + `Representee par ...`).
- `Ont etabli ainsi qu'il suit les statuts d'une Societe en commandite simple qu'ils ont decide d'instituer entre eux :`
- TITRE I a fin : ARTICLE 1 Forme (`une Societe en commandite simple regie par le Code du commerce...`), ARTICLE 2 Objet (civil immobilier complet), ARTICLE 6 Apports (bloc commandites / commanditaires, `Le montant total verse par le commandite est de [total_apports_commandites]`), ARTICLE 7 Capital social (variable, maximal/minimal/effectif), ARTICLE 8 Variabilite, jusqu'aux articles gerance (16-19, `gerant`, `gerant personne morale` art. 17), decisions collectives (21-23), exercice/comptes/resultats (24-26).
- Specificite SCS confirmee par la spec texte (`lot_04_statuts_civils_spec_texte_v1.md`, section 4) : distinction commandites/commanditaires, responsabilite indefinie et solidaire des commandites, capital variable avec maximal, qualite associe dans la repartition, gerance personne morale ; signature SCS = mention `Lu et approuve` (arbitrage section 7).

Specs delivery qui figent et tracent ce wording (a citer comme source, ne pas reinventer) :
- `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md` (structure texte SCS verbatim, section 4) ;
- `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` ;
- `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md` (ARBITRAGE-STATUTS-CIVILS-001, CLOS pour les 4 statuts civils).

Dictionnaire de substitution stable (`_ResolvedStatutsCivil.common_replacements`) commun aux 3 statuts
civils : `[denomination_societe]`, `[forme_sociale]`, `[mention_capital_variable]`, `[capital_social]`/`[capital_lettres]`,
`[capital_social_maximal]`/`[capital_social_maximal_lettres]`, `[nb_parts(_total)]`/`[nb_parts(_total)_lettres]`,
`[valeur_nominale_part(_lettres)]`, `[plage_parts_total]`, `[parts_debut]`/`[parts_fin]`, adresse siege
(`[num_voie_siege]`...), `[ville_rcs]`, `[duree_societe]`, `[nom_banque]`/`[adresse_banque]`,
`[date_cloture_exercice_1]`, `[lieu_signature]`/`[date_signature]`, `[nombre_exemplaires_lettres]`,
`[denomination_cabinet_mandataire]`.

---

## 5. NON TROUVE -> a lever par tokenisation du modele PUIS Rafael (ne jamais inventer de wording)

La tokenisation des statuts SCS est DEJA faite (modele unique tokenise). Le NON TROUVE est donc soit
"pas de modele du tout" (a tokeniser si Rafael fournit une source), soit purement metier/juridique.
Ordre impose : verifier d'abord les sources/modeles ; si absent -> message Rafael via Gad, JAMAIS une
question au PM, JAMAIS de wording invente.

1. **Aucune passe NotebookLM SCS** : aucun fichier NLM n'existe. Les questions obligatoires du
   playbook (sections A-H de `COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`) n'ont jamais ete posees pour SCS.
   A lever par une passe NLM puis retour Rafael. **Bloquant pour declarer SCS "type produit livre".**
2. **Cession de parts SCS / transformation / dissolution** : aucun modele source SCS -> NON TROUVE.
   Ne pas coder. Si Rafael fournit un modele, le tokeniser PUIS coder.
3. **Apport en nature / immeuble a la SCS** : la source ne montre que des apports en numeraire (art. 6).
   Variante apport-immeuble = NON TROUVE.
4. **Profession / nature exacte de la SCS attendue** : le modele source est une SCS **civile
   immobiliere** (objet immobilier). Si le besoin metier vise une SCS d'exercice professionnel
   (medecin/dentiste), la source ne le porte pas -> NON TROUVE ; a confirmer Rafael (sinon garder le
   cadre civil immobilier de la source).
5. **Couche genre/pluriel sur les statuts SCS** : le moteur gere `Ne/Nee` via `Gender`, mais DOC-019
   a `grammar_variants=False` au catalogue (contrairement aux universels DOC-001/002/003 en
   `grammar_variants=True`). A confirmer Rafael si une couche genre/pluriel plus riche est attendue
   sur les statuts SCS. Ne pas "ameliorer" la grammaire sans source.
6. **Nombre d'exemplaires / mandataire** : `[nombre_exemplaires_lettres]` et
   `[denomination_cabinet_mandataire]` sont des champs requis du template SCS (`_validate_template_fields`
   branche SCS). Leurs valeurs metier (combien d'exemplaires ? quel cabinet mandataire ?) sont des
   donnees dossier a fournir ; si une regle fixe existe cote metier, elle est NON TROUVE en l'etat.

---

## 6. Besoins envers le SOCLE PARTAGE

Ce que SCS exige de la couche commune (pour que le slice front + l'orchestration ne derivent pas) :

1. **Substitution parts/actions, gerant/president** : SCS = societe civile a **parts sociales** et
   **gerant** (jamais "actions" ni "president"). Le moteur civils est deja oriente parts/gerant
   (`StatutsCivilsContext.nb_parts_total`, `valeur_nominale_part`, `GeranceContext`, PV nomination
   **gerant** DOC-004). EXIGENCE socle : le slice front SCS doit router vers le vocabulaire
   "parts" + "gerant" et la numerotation debut/fin par associe. Reutilisable depuis la mecanique
   parts existante (ne PAS exposer "actions"/"president" pour SCS).

2. **Couche multi "LES SOUSSIGNES" / repartition numerotee / PV d'AG** :
   - Comparution multi-associes "LES SOUSSIGNES" : DEJA gere dans le moteur
     (`_add_associate_block` boucle sur `associes[]`, 1 a 6).
   - Repartition numerotee des parts (plage debut/fin par associe) : DEJA gere
     (`_add_capital_block`, `_first_part_number`/`_last_part_number`).
   - **Specificite SCS** : le socle multi doit porter le **role statutaire** (commandite /
     commanditaire) par associe (`role_statutaire`) ET le rendu en DEUX sous-groupes pour les apports
     ("Associes commandites :" / "Associes commanditaires :"). C'est present cote moteur
     (`_associes_by_role`) ; le socle FRONT devra exposer ce choix de role par associe.
   - **PV d'AG** : non requis pour la *creation* SCS (la source ne liste pas de PV d'AG en creation,
     hormis PV nomination gerant). Pas de besoin de couche PV d'AG generique pour le scope creation SCS.

3. **Personne morale associee** : besoin reel (ligne `[denomination_societe_associe_1]` de la source
   SCS). DEJA gere cote moteur (`_is_morale`, `_add_morale_identity`, `_signature_label` morale,
   `ScmRepresentant`/`representant`). EXIGENCE socle FRONT : savoir saisir un associe personne morale
   (denomination, forme juridique, capital, siege, RCS ville+numero, representant
   civilite/prenom/nom/fonction). Le slice SELARL ne gere PAS l'associe personne morale -> extension
   du socle front necessaire (besoin partage avec SCI IRIS / SCM).

4. **Couche genre** : besoin minimal (Ne/Nee selon `Gender`) deja couvert par le moteur via
   `derive_gender_from_civilite` (`front_app.field_derivations`). Pas de derivation complexe requise
   par les statuts SCS au-dela de ca (voir point 5 de la section NON TROUVE pour une eventuelle couche
   plus riche a confirmer Rafael).

5. **Registre (catalog)** : SCS est DEJA cable :
   - `domain/enums.CaseType.SCS = "SCS"` ;
   - `registry/catalog` : `ALL_STRUCTURES`, `PV_NOMINATION_GERANT_STRUCTURES` et
     `STATUTS_CIVILS_SCS_STRUCTURES` contiennent "SCS" ; DOC-019 declare avec
     `generator_name="generate_statuts_scs"`, `source_path=".../Statuts_SCS_modele.docx"`,
     `workflow_status=WorkflowStatus.TESTE` ;
   - `domain/case_catalog` : `CaseType.SCS` avec occurrences `statuts_scs`,
     `declaration_non_condamnation`, `autorisation_domiciliation`, `procuration`,
     `pv_nomination_gerant` ; `statuts_scs` = `DocumentAvailability.GENERATABLE`.
   EXIGENCE : aucune nouvelle entree registre pour les statuts. (Eventuellement verifier que les
   universels exposent bien SCS quand on les finira — ils sont en `ALL_STRUCTURES`, donc OK.)

6. **Slice front + deroulante auto-extensible** : **MANQUANT.** Le front "clean"
   (`dossier_selection.CLEAN_DOSSIER_TYPE_OPTIONS`) n'expose QUE `SELARL creation V1`. Il n'existe
   AUCUN `scs_slice.py` equivalent a `selarl_slice.py`. EXIGENCES precises du socle pour exposer SCS :
   - un `DossierTypeOption` "SCS creation V1" dans `CLEAN_DOSSIER_TYPE_OPTIONS` (structure="SCS") ;
   - un `front_app/scs_slice.py` sur le patron `selarl_slice.py` (input dataclass figee, `validate_*`,
     `build_*_plan`, `selected_*_document_codes`, `build_generation_context` -> `DocumentGenerationContext`
     SCS, puis `generate_docx_files_for_document_codes` + `generate_zip_file` de `app/ui_runtime`) ;
   - une **deroulante d'associes auto-extensible** (1 a 6) avec, PAR associe : choix physique/morale,
     **role commandite/commanditaire**, apport, parts (nb + nb_lettres + plage), donnees personne morale
     + representant si morale. (Le slice SELARL gere des associes additionnels ; SCS doit
     reutiliser/generaliser ce composant ET ajouter le selecteur de role statutaire.) ;
   - saisie des champs SCS specifiques requis par le template : `total_apports_commandites`,
     `capital_maximal`/`capital_maximal_lettres`, `valeur_nominale_part_lettres`, `plage_parts_totale`,
     `duree_societe`, `nombre_exemplaires_lettres`, `denomination_cabinet_mandataire`.

7. **PDF / ZIP / bundle** : `rendering/pdf_export.py`, `zip_bundle.py`, `bundle.py` existent et sont
   utilises par `app/ui_runtime`. EXIGENCE : brancher SCS dessus via le slice front (le moteur produit
   deja un DOCX SCS valide).

Note : le ticket cite `rendering/docx_template_fill.py` -> ce fichier N'EXISTE PAS. Le template-fill
SCS passe par `generators/lot_04/statuts_civils_common.py::generate_statuts_civil_docx` + `SCS_TEMPLATE`.
Les helpers DOCX communs sont dans `rendering/docx_builder.py`.

---

## 7. Bloquants de build

| # | Bloquant | Type | Effet | Action |
|---|---|---|---|---|
| B1 | Pas de slice front SCS ; `dossier_selection` n'expose que SELARL | scope/build (technique) | SCS non pilotable par l'utilisateur final meme si le moteur marche | Construire `front_app/scs_slice.py` + `DossierTypeOption` SCS, sur le patron SELARL. **Constructible MAINTENANT** sur branche dediee, reversible (le moteur + le wording sont prets). |
| B2 | Saisie "associe personne morale" + "role commandite/commanditaire" absente du socle front | socle (technique) | SCS avec personne morale associee, et le choix de role par associe, non saisissables cote UI | Etendre le socle front (role statutaire par associe ; saisie personne morale + representant). Besoin partage avec SCI IRIS / SCM. |
| B3 | Passe NotebookLM SCS jamais faite (9+ points du playbook non leves) | metier -> Rafael | Interdit de declarer SCS "type produit livre" sans triangulation 3 sources | Lancer la passe NLM (prompts du playbook), structurer le journal, puis retour Rafael via Gad. |
| B4 | Documents universels DOC-001/002/003 en `WorkflowStatus.SPECIFIE` (pas branches/testes catalogue) | build (transverse) | un dossier SCS "complet" ne sort aujourd'hui que les statuts (+ PV gerant) si on ne finit/route pas les universels | Finir + cabler DOC-001/002/003 dans le slice SCS (reuse direct des generateurs `lot_01`). DOC-002 a un arbitrage rendu adresse en suspens. Transverse, pas propre a SCS. |
| B5 | Nature de la SCS (civile immobiliere vs exercice professionnel) | canon/metier -> Rafael | risque de derive si on adapte le wording a un usage non source | NE PAS adapter le wording sans source ; confirmer Rafael (sinon garder le cadre civil immobilier de la source). |
| B6 | Cession / transformation / apport en nature SCS sans modele | canon/metier -> Rafael | hors scope creation | NE PAS coder ; tokeniser un modele si Rafael en fournit un, puis coder. |
| B7 | Dette technique : `SCS_TEMPLATE` reprend la source par **index de paragraphes en dur** (`associate_slice=(14,18)`, `apport_slice=(43,58)`, `capital_slice=(63,76)`, `append_signatures_after=253`) | technique (non bloquant) | toute reedition du DOCX source SCS casse silencieusement le mapping (les slices ne correspondraient plus) | A surveiller ; non bloquant tant que la source ne bouge pas. Un test de garde (verifier la structure attendue de la source) reduirait le risque. |

### Ce qui N'EST PAS bloquant
- Tokenisation : faite (modele SCS unique deja tokenise). Wording statuts : fige dans la source +
  specs delivery. Moteur statuts SCS : code + 2 tests SCS verts. Registre : SCS cable (enum, catalog,
  case_catalog). PV nomination gerant (DOC-004) : code + teste, SCS deja dans son scope.

---

## 8. Verification effectuee (perimetre nomme)

- **Tests** : `tests/unit/test_lot_04_statuts_civils.py`, filtre SCS uniquement
  (`-k "scs or SCS or commandit"`, `--basetemp=artifacts/_audit_tmp/pt`) -> **2 passed, 3 deselected**
  cette session. Les 2 tests SCS couvrent (a) le rejet si commandite OU commanditaire manque, (b) le
  rendu des roles + la mention `Lu et approuve`. **Perimetre SCS UNIQUEMENT ; suite globale NON
  relancee** (hors scope audit, et garde base/CI).
- **Modele source SCS** ouvert et identifie via python-docx (289 paragraphes, 0 table) -> Statuts SCS,
  objet civil immobilier, capital variable, commandites/commanditaires.
- **Catalogue / case_catalog / enums** relus : SCS cable, DOC-019 = TESTE, DOC-001/002/003 = SPECIFIE,
  DOC-004 = TESTE, SCS absent de `DEMANDE_INSCRIPTION_ORDRE_STRUCTURES`.
- **Specs delivery civils** (arbitrages CLOS, spec texte, spec canonique) relues : wording SCS fige,
  4 statuts civils non fusionnables.
- **Front** : `dossier_selection.py` (seul SELARL expose), `selarl_slice.py` (patron) confirmes ;
  aucun `scs_slice.py`.
- **Confirme absent** : tout fichier `NOTEBOOKLM*` ; tout `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md` ;
  tout `rendering/docx_template_fill.py` ; tout repertoire `project/source_documents/scs/`.
- **Aucun fichier de code modifie. Aucune action Git.**

---

## Sources lues (preuve)

- `project/source_documents/lot_04/Statuts_SCS_modele.docx` (ouvert via python-docx)
- `src/sydel_doc_engine/generators/lot_04/statuts_scs.py`,
  `src/sydel_doc_engine/generators/lot_04/statuts_civils_common.py` (`SCS_TEMPLATE`, validations SCS)
- `src/sydel_doc_engine/registry/catalog.py` (DOC-019 + `ALL_STRUCTURES`/`PV_NOMINATION_GERANT_STRUCTURES`/`STATUTS_CIVILS_SCS_STRUCTURES`)
- `src/sydel_doc_engine/domain/case_catalog.py` (`CaseType.SCS`, occurrences), `src/sydel_doc_engine/domain/enums.py`
- `src/sydel_doc_engine/generators/lot_01/declaration_non_condamnation.py` (universel)
- `src/sydel_doc_engine/front_app/selarl_slice.py`, `src/sydel_doc_engine/front_app/dossier_selection.py`
- `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`, `..._spec_texte_v1.md`, `..._spec_canonique_v1.md`
- `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` (recette canonique reelle)
- `docs/project/types/SCI/BUILD_READINESS_V1.md`, `docs/project/types/SCM/BUILD_READINESS_V1.md` (siblings)
- Tests : `tests/unit/test_lot_04_statuts_civils.py` (SCS commandite/commanditaire + Lu et approuve)
