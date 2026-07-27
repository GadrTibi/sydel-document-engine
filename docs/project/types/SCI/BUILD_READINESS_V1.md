# SCI — Build Readiness V1

Date : 2026-06-07
Auteur : analyste de constructibilite (lecture seule du code, aucune modif source)
Type : SCI (2 variantes : SCI, SCI IRIS) — capital VARIABLE, parts sociales civiles.

> Note de cadrage sur les chemins du prompt : plusieurs chemins cites dans la mission
> n'existent pas en l'etat (`project/source_documents/sci/`, `docs/project/types/SCI/NOTEBOOKLM_*`,
> `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`, `src/.../rendering/docx_template_fill.py`,
> generateurs `lot_01..05` au sens « SELARL livree »). Realite observee :
> - Modeles source SCI = `project/source_documents/lot_04/Modèle statuts SCI.docx` et
>   `…/Modèle statuts SCI IRIS.docx` (pas de repertoire `sci/` dedie).
> - Pas de synthese NotebookLM SCI. Source-of-truth metier = `project/source_truth/Documents_a_generer_par_cas.docx` (+ V3).
> - Recette canonique reelle = `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`.
> - Couche rendu = `src/sydel_doc_engine/rendering/docx_builder.py` (pas de `docx_template_fill.py`).
> - **Le moteur SCI / SCI IRIS / Lettre option IS EST DEJA CODE ET TESTE** (`WorkflowStatus.TESTE`).
>   Le chantier restant pour SCI n'est PAS le moteur des statuts, c'est le **front (slice Streamlit)**
>   et le branchement des **documents universels** au parcours SCI.

---

## 0. Etat synthetique

| Brique | Etat observe | Constructible maintenant ? |
|---|---|---|
| Moteur statuts SCI (DOC-020) | code + teste (`statuts_sci.py` → `statuts_civils_common.py`) | DEJA FAIT |
| Moteur statuts SCI IRIS (DOC-021) | code + teste (personne morale + quote-part exceptionnel) | DEJA FAIT |
| Moteur Lettre option IS (DOC-022) | code + teste (`lot_05/lettre_option_is.py`) | DEJA FAIT |
| Documents universels sur parcours SCI (DOC-001/002/003/004) | generateurs existants, **non cables au cas SCI** dans un slice | A CABLER (reuse) |
| Slice front SCI (Streamlit) | **inexistant** (seul `selarl_slice.py` existe) | A CONSTRUIRE |
| Personne morale associee cote socle | gere dans le moteur civils, **pas dans le socle front** | A ETENDRE (socle) |

Conclusion : SCI est **majoritairement deja construit au niveau moteur**. La readiness « produit »
depend d'un **slice front SCI** + branchement des documents universels, pas d'une re-ecriture des
statuts.

---

## 1. Inventaire des modeles source

Tous les modeles SCI vivent dans `project/source_documents/lot_04/` (et non dans un dossier `sci/`).

| Fichier source | Document juridique | Cas couvert | Tokenise ? |
|---|---|---|---|
| `Modèle statuts SCI.docx` (667 paragraphes, 0 table) | Statuts constitutifs d'une Societe Civile Immobiliere | Creation SCI, capital variable, associes personnes physiques 1-6 | OUI (placeholders `[…]`, ex. `[denomination_societe]`, `[forme_sociale]`, `[mention_capital_variable]`, `[capital_social]`, `[num_voie_siege]`…) |
| `Modèle statuts SCI IRIS.docx` (661 paragraphes, 1 table) | Statuts constitutifs SCI variante « IRIS » | Creation SCI IRIS : inclut **un associe personne morale** (`[denomination_societe_2]`) + **table de quote-part de resultat exceptionnel par groupe de parts** | OUI (memes placeholders + bloc `[nb_parts_lettres_societe_2]`, `[parts_debut_societe_2]`… et table « Groupe de parts / Quote-part du resultat exceptionnel ») |

Document associe au cas SCI mais physiquement dans un autre lot :
| `lot_05/lettre option IS.docx` | Lettre d'option pour l'impot sur les societes | Conditionnel SCI / SCI IRIS « Si IS » | OUI |

Constat de tokenisation : les deux modeles statuts SCI sont **deja tokenises** (placeholders entre
crochets) et **deja consommes** par le moteur (`statuts_civils_common.py`), qui valide d'ailleurs en
fin de rendu l'absence de tout `[`/`]` residuel. Aucun modele SCI a-tokeniser n'a ete trouve.

---

## 2. Cas couverts

Source metier : `project/source_truth/Documents_a_generer_par_cas.docx`, section « SCI » (par. 57-64).

- **Creation SCI** (physique, capital variable) — couvert.
- **Creation SCI IRIS** (avec associe personne morale + repartition resultat exceptionnel par groupe
  de parts) — couvert.
- **Multi-associes** : 1 a 6 associes (`MAX_ASSOCIES = 6`), apports/parts dynamiques par associe,
  numerotation de parts auto (`parts_debut`/`parts_fin`). Couvert pour les deux variantes.
- **Option IS** : conditionnel « Si IS » — couvert via DOC-022.

Cas **NON** couverts / hors source V1 (blocages explicites dans le code) :
- **SCI (non IRIS) avec associe personne morale** : explicitement **bloque** en V1
  (`_validate_sci` + `_validate_associes` levent une erreur ; commentaire « hors source observee V1 »).
  La personne morale n'est admise QUE pour SCI IRIS.
- **Cession de parts SCI**, **apport en nature**, **transformation**, **gerance personne morale en
  saisie** : aucun modele source SCI present → hors scope (non trouve).

---

## 3. Documents a generer (par variante)

Statuts retenus depuis la source-of-truth pour le cas SCI :

| Document | Code | Statut (cas) | Approche recommandee | Etat code |
|---|---|---|---|---|
| Statuts SCI | DOC-020 | systematique (SCI) | **template-fill** (le moteur reproduit la source paragraphe par paragraphe, n'insere que les blocs associes/apports/capital/signature) | DEJA TESTE |
| Statuts SCI IRIS | DOC-021 | systematique (SCI IRIS) | **template-fill** (idem + bloc table quote-part exceptionnel) | DEJA TESTE |
| Lettre option IS | DOC-022 | conditionnel (« Si IS », SCI et SCI IRIS) | **from-scratch** (pas un remplissage de la source : le generateur reconstruit la lettre ; la source `lettre option IS.docx` sert de reference de wording) | DEJA TESTE |
| Declaration sur l'honneur de non-condamnation | DOC-001 | systematique (univ.) | template-fill (generateur lot_01 existant, `grammar_variants`) | code existant, A CABLER au parcours SCI |
| Autorisation de domiciliation | DOC-002 | systematique (univ.) | template-fill (lot_01 existant) | code existant, A CABLER ; arbitrage rendu adresse encore note au catalogue |
| Procuration | DOC-003 | systematique (univ.) | template-fill (lot_01 existant) | code existant, A CABLER |
| PV nomination gerant | DOC-004 | systematique (univ., SCI ∈ `PV_NOMINATION_GERANT_STRUCTURES`) | from-scratch/mutualise (lot_02 existant, `dynamic_associates`) | code existant, A CABLER |

Notes de classement :
- « systematique (univ.) » = liste sous le bloc SCI de la source-of-truth (Declaration non-condamnation,
  Procuration, Autorisation de domiciliation, PV nomination gerant). SCI figure bien dans
  `PV_NOMINATION_GERANT_STRUCTURES` du catalogue ; SCI est **absent** de
  `DEMANDE_INSCRIPTION_ORDRE_STRUCTURES` (pas de demande d'inscription a l'ordre pour SCI) — coherent
  avec la source.
- « Lettre option IS » est un document **separe**, jamais injecte dans les statuts (catalogue
  DOC-022 : « Document dedie, non injecte dans les statuts civils »).
- Documents reglementaires SEL (ordre, regime communautaire, derogations, cession cabinet, bail,
  appel de fonds, SCM satellites) = **hors-creation SCI** : leurs listes de structures n'incluent pas
  SCI / SCI IRIS.

---

## 4. Wording EXACT deja disponible

Le wording statutaire SCI/SCI IRIS est **integralement disponible et fige** (les modeles sont la
source ; le moteur ne fait que substituer des variables). Exemples de wording confirme, repris tel
quel par le moteur (texte source non modifie) :

- En-tete : « Au Capital minimum et effectif de [capital_social] euros » / « Siège Social : … ».
- « LES SOUSSIGNES : » puis identite par associe :
  - physique : « Né/Née le … à … (…) » / « De nationalité … » / situation maritale / « Demeurant … ».
  - morale (IRIS) : forme juridique + « au capital de … » + « ayant son siège … » + « immatriculée au
    RCS de … sous le numéro … » + « Representée par … ».
- « Ont établi ainsi qu'il suit les statuts d'une [forme_sociale] devant exister entre eux. »
- ARTICLE 1 FORME, ARTICLE 2 OBJET (objet civil immobilier complet), ARTICLE 3 DENOMINATION,
  ARTICLE 6 APPORTS, ARTICLE 7 CAPITAL SOCIAL (« 7.1 Répartition du capital »), jusqu'aux ARTICLE 33
  (affectation/repartition des benefices), 34, 36 (immatriculation), et bloc signature.
- IRIS specifique (ARTICLE 33) : phrase d'amorce « Le résultat exceptionnel pour la période de
  référence … sera réparti de la façon suivante entre les différents groupes de parts : » suivie de la
  **table « Groupe de parts / Quote-part du résultat exceptionnel »** (4 lignes source), inseree par
  `_add_resultat_groupes_block`.
- Lettre option IS (from-scratch, wording fige dans le generateur) :
  - Objet : « Objet : Demande d'option pour le régime de l'impôt sur les sociétés »
  - « Fait à {lieu}, le {date} », « Madame, Monsieur, », corps « … opte pour le régime de l'Impôt sur
    les Sociétés … », tableau d'identification (Dénomination / Adresse / SIREN / répartition du
    capital), cloture « … l'assurance de notre parfaite considération. », signature « Le gérant ».

Le moteur expose un dictionnaire de substitution stable (`common_replacements`) : `[denomination_societe]`,
`[forme_sociale]`, `[mention_capital_variable]`, `[capital_social]`/`[capital_lettres]`,
`[capital_autorise]`/`[capital_autorise_lettres]`, `[nb_parts]`/`[nb_parts_lettres]`,
`[valeur_nominale_part]`, `[parts_debut]`/`[parts_fin]`, adresse de siege (`[num_voie_siege]`…),
`[ville_rcs]`, `[duree_societe]`, `[nom_banque]`/`[adresse_banque]`,
`[date_cloture_exercice_1]`, `[lieu_signature]`/`[date_signature]`.

---

## 5. NON TROUVE (a lever par tokenisation du modele PUIS Rafael — ne jamais inventer)

Aucune de ces zones ne doit etre comblee par du wording invente. Ordre impose : d'abord verifier dans
les modeles tokenises ; si absent → message a Rafael (via Gad), jamais une question au PM.

1. **SCI (non IRIS) avec associe personne morale** : pas de modele source → bloque en V1. Si Rafael
   confirme que ce cas existe, il faut un modele tokenise (ou confirmation que la variante IRIS est la
   seule porteuse de la personne morale). NON TROUVE en V1.
2. **Cession de parts SCI** (acte, agrement, PV) : aucun modele SCI present (les actes de cession
   existants visent SCM/SPFPL/cabinet, pas la SCI elle-meme). NON TROUVE.
3. **Apport en nature / immeuble a la SCI** (article apports en nature, etat descriptif) : la source
   statuts ne montre que des apports en numeraire. NON TROUVE pour la variante apport-immeuble.
4. **Genre/pluriel sur les statuts civils** : le moteur civils gere « Ne/Nee » par `Gender`, mais
   contrairement aux statuts SEL il **n'a pas** `grammar_variants=True` au catalogue (DOC-020/021).
   A confirmer avec Rafael si une couche genre/pluriel plus riche est attendue sur les statuts SCI.
5. **Wording exact du bloc personne morale en SCI IRIS au-dela de la repartition** (par ex. mentions
   conjoint/usufruit/nue-propriete deja presentes en ARTICLE 33) : present dans la source, mais toute
   variante non couverte par la source (ex. demembrement saisi par l'utilisateur) est NON TROUVE.

---

## 6. Besoins envers le SOCLE PARTAGE

Ce que SCI exige du socle commun (pour que le slice front et l'orchestration ne derivent pas) :

- **Substitution parts/actions** : SCI utilise « parts sociales » (jamais « actions »). Le moteur
  civils est deja oriente parts ; le socle front devra exposer le vocabulaire « parts » et la
  numerotation (debut/fin) par associe. Reutilisable depuis la mecanique SELARL (`CapitalContext`
  type_titre = « parts sociales »).
- **Gerant / president** : SCI a un **gerant** (pas de president). Le PV nomination gerant (DOC-004)
  existe et SCI est dans son scope ; le socle doit router SCI vers « gerant ». Pas de besoin
  « president » pour SCI.
- **Couche multi-associes** :
  - bloc « LES SOUSSIGNES » repete par associe — **deja gere** dans le moteur (`_add_associate_block`).
  - **repartition numerotee des parts** par associe (parts_debut/parts_fin, plage) — deja gere.
  - **PV d'AG** : non requis pour la *creation* SCI (la source ne liste pas de PV d'AG en creation,
    seulement PV nomination gerant). Pas de besoin de couche PV d'AG pour le scope creation.
- **Personne morale associee** : **besoin reel et specifique a SCI IRIS**. Le moteur le gere
  (`_add_morale_identity`, `_signature_label` morale, validations `_validate_sci_iris`). En revanche
  le **socle front** (slice + saisie) doit savoir saisir un associe personne morale (denomination,
  forme juridique, capital, siege, RCS ville+numero, representant civilite/prenom/nom/fonction). C'est
  le besoin de socle le plus structurant pour SCI IRIS. Le slice SELARL ne gere PAS la personne morale
  associee → extension necessaire.
- **Couche genre** : besoin minimal (Ne/Nee selon `Gender`) deja couvert par le moteur ; voir point 4
  pour une eventuelle couche plus riche a confirmer Rafael.
- **Registre** : SCI / SCI IRIS sont deja dans `ALL_STRUCTURES` du catalogue et chaque document a son
  `DocumentDefinition` (DOC-020/021/022) avec conditions et generateur lie. Pas de besoin de nouvelle
  entree registre ; eventuellement ajouter SCI/SCI IRIS aux structures des documents universels deja
  acquises au parcours (DOC-001/002/003 ont `ALL_STRUCTURES`, DOC-004 a SCI).
- **Slice front + deroulante auto-extensible** : **a construire** sur le patron `selarl_slice.py`
  (input dataclass figee, `validate_*`, `build_*_plan`, `selected_*_document_codes`,
  `build_generation_context`, `generate_*_dossier`). Besoin specifique : un **repeteur d'associes
  auto-extensible** (1 a 6) avec, par associe, le choix physique/morale et la quote-part de resultat
  exceptionnel pour IRIS. Le socle front existant (`front_data` : `BusinessRole`, `AddressUsage`,
  derivations, dedup) est reutilisable ; il faudra ajouter le role « associe personne morale » et
  l'usage d'adresse « siege associe morale ».

---

## 7. Bloquants de build

| # | Bloquant | Type | Effet | Action |
|---|---|---|---|---|
| B1 | Pas de slice front SCI | scope/build | SCI n'est pas pilotable par l'utilisateur final meme si le moteur marche | Construire `front_app/sci_slice.py` sur le patron SELARL (constructible immediatement, branche dediee, reversible) |
| B2 | Saisie « associe personne morale » absente du socle front | socle | SCI IRIS non saisissable cote UI sans cette brique | Etendre le socle front (role + adresse morale + representant) avant le slice IRIS |
| B3 | SCI + personne morale (non IRIS) sans source | canon/metier | cas bloque par le code ; reste flou | NE PAS coder ; message Rafael : ce cas existe-t-il ? sinon garder le blocage |
| B4 | Cession / apport en nature SCI sans modele | canon/metier | hors scope creation | NE PAS coder ; tokeniser un modele si fourni, puis Rafael |
| B5 | Couche genre/pluriel statuts civils non revendiquee (`grammar_variants=False`) | canon | risque de derive si on « ameliore » la grammaire sans source | Confirmer Rafael avant toute extension grammaticale des statuts SCI |
| B6 | Documents universels non cables au parcours SCI | build | un dossier SCI ne produit aujourd'hui que les statuts si on ne route pas DOC-001/002/003/004 | Cabler dans le slice SCI (reuse direct des generateurs lot_01/02) |

Decisions de scope par defaut (documentees, a confirmer cote metier si conteste) :
- V1 SCI = **creation uniquement** (SCI physiques + SCI IRIS avec 1 personne morale), option IS
  conditionnelle. Cession/apport/transformation = hors V1.
- Le moteur statuts n'est **pas** a refaire : il est teste. Le travail est **front + branchement**.

---

## Sources lues (preuve)

- `project/source_documents/lot_04/Modèle statuts SCI.docx`, `…/Modèle statuts SCI IRIS.docx`
- `project/source_documents/lot_05/lettre option IS.docx`
- `project/source_truth/Documents_a_generer_par_cas.docx` (section SCI, par. 57-64), `…_V3.docx`
- `src/sydel_doc_engine/generators/lot_04/statuts_sci.py`, `statuts_sci_iris.py`,
  `statuts_civils_common.py`
- `src/sydel_doc_engine/generators/lot_05/lettre_option_is.py`
- `src/sydel_doc_engine/registry/catalog.py` (DOC-020/021/022 + listes de structures)
- `src/sydel_doc_engine/domain/models.py` (StatutsCivils*, StatutsCivilsGroupeParts)
- `src/sydel_doc_engine/rendering/docx_builder.py` (helpers de rendu statuts)
- `src/sydel_doc_engine/front_app/selarl_slice.py`, `shell.py`, `src/sydel_doc_engine/front_data/`
- `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` (recette canonique reelle)
- Tests : `tests/unit/test_lot_04_statuts_civils.py` (SCI dynamic associates, IRIS morale + groupes),
  `tests/unit/test_lettre_option_is.py`
