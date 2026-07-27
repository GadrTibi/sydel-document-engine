# SCP — BUILD READINESS V1 (analyse de constructibilite)

Date : 2026-06-07
Auteur : analyste de constructibilite (lecture seule du code, aucune modification de code, aucune action Git)
Type : SCP (Societe Civile Professionnelle) — societe civile a PARTS et GERANT, exercice en commun d'une profession liberale reglementee.

> **Note de cadrage sur les chemins du prompt (a lire d'abord).** Plusieurs chemins/hypotheses de la
> mission n'existent pas dans ce repo, et l'ecart est cette fois MAXIMAL :
> - `project/source_documents/scp` : **n'existe pas**. Aucun fichier `scp` n'est range dans le moteur.
> - `docs/project/types/SCP/NOTEBOOKLM_ANSWERS.md` / `NOTEBOOKLM_PROMPTS_V2.md` : **absents** (le repertoire `docs/project/types/SCP/` n'existait pas avant ce rapport).
> - `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md` : **absent**. La recette canonique reelle est
>   `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` (+ `COMPANY_TYPE_STATUS_REGISTRY_V1.md`).
> - `src/sydel_doc_engine/rendering/docx_template_fill.py` : **n'existe pas**. Le projet genere les DOCX
>   **from-scratch** via `src/sydel_doc_engine/rendering/docx_builder.py` (ADR-0004), jamais par remplissage
>   du DOCX source utilise comme gabarit d'execution. La doctrine "template-fill de preference" du brief ne
>   s'applique donc PAS a ce projet.
> - Generateurs `lot_01..05` au sens "SELARL livree" : existent pour SELARL/SELAS/SCM/SCI/SPFPL, **pas pour SCP**.

---

## 0. Resume executif — SCP est un GREENFIELD REEL, et de surcroit explicitement EXCLU

Contrairement a SCM, SPFPL et SCI (dont le MOTEUR etait deja code et teste, seul le front manquait),
**SCP n'a AUCUNE brique existante dans ce repo** et est **canoniquement classe "hors moteur courant"**.

Faits verifies cette session :

1. **Pas de `CaseType.SCP`.** L'enum `domain/case_catalog.py` (l. 9-17) ne connait que SELARL, SELAS,
   SPFPL_CESSION, SPFPL_APPORT, SCS, SCI, SCM, SAS. **SCP n'y figure pas.**
2. **Aucun generateur, aucune entree catalogue, aucun test SCP.** Recherche sur tout `src/` : aucune
   occurrence de SCP comme type traite (les seules occurrences "SCP" du repo sont des MENTIONS — un
   rappel d'article du Code de la sante publique dans une derogation, et les docs d'import qui EXCLUENT SCP).
3. **Aucun modele source SCP dans le repo.** Le seul fichier SCP jamais reference
   (`Creation SCP/Modele Statuts SCP - transforme.docx`, cite par `docs/delivery/lot_04_statuts_preparation_v1.md` l.89)
   vit dans un dump Drive (`project/source_import/raw_drive_dump/Creation SCP/...`) **qui n'est pas present** :
   le dump du repo ne contient que `création scm`, `Création SCS`, `Création SELARL`, `Création SPFPL`.
   Aucun `.doc`/`.docx` contenant "scp" n'existe nulle part dans le repo (recherche exhaustive faite).
4. **Decision canonique : SCP = "hors moteur courant".** Inscrit noir sur blanc dans
   `docs/project/13_SOURCE_ARBITRATION_DECISIONS_V1.md` (l.16-23 et tableau l.58), repris par
   `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md` (l.64) et `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md` (l.114).
5. **SCP absent de la source-of-truth produit.** Ni `project/source_truth/Documents_a_generer_par_cas.docx`
   ni sa V3 ne mentionnent SCP ni "societe civile professionnelle" (verifie par extraction texte+tables).
   SCP n'est donc **pas** dans la matrice "documents a generer par cas" du produit.
6. **Pas de statut dans le registre.** `docs/project/COMPANY_TYPE_STATUS_REGISTRY_V1.md` liste 8 types ;
   SCP n'y est meme pas en `NON_TRAITE` — il est hors registre, car decide hors moteur.

**Conclusion d'altitude.** Pour SCM/SPFPL/SCI, "construire" voulait dire "batir le slice front sur un
moteur deja teste". **Pour SCP, il n'y a rien a brancher : il faudrait creer le type de zero** (source,
tokenisation, NotebookLM, modele Pydantic, generateur from-scratch, catalogue, registre, slice front) —
**ET d'abord LEVER une decision produit/canon qui exclut SCP du moteur courant**. SCP n'est pas
"constructible maintenant" : c'est **bloque en amont** (B1, B2 ci-dessous). Tant que (a) la decision
"hors moteur courant" n'est pas explicitement revisee par Rafael/Gad et (b) le modele source SCP n'est pas
rapatrie dans le repo, **aucun code SCP ne doit etre ecrit** — ce serait inventer un type non sourced et
non valide metier.

---

## 1. Inventaire des modeles source (fichier -> document juridique + cas couvert)

**Aucun modele source SCP n'est present dans le repo.** Il n'existe donc pas d'inventaire a dresser.

| Element | Etat observe |
|---|---|
| Repertoire `project/source_documents/scp` | inexistant |
| Modeles SCP dans `lot_01..05` | aucun (les lots contiennent SELARL/SELAS/SCM/SCI/SCS/SPFPL/SAS uniquement) |
| `Creation SCP/Modele Statuts SCP - transforme.docx` (cite par les specs) | **absent du repo** ; reference a un dump Drive non importe |
| `Creation SCP/Declaration sur l_honneur de non condamnation - transforme.docx` (cite par `11_SOURCE_DUPLICATES_REPORT_V1.md` l.42) | **absent du repo** ; marque "SCP hors perimetre" |
| Tout autre `.docx`/`.doc` contenant "scp" | aucun (recherche exhaustive) |

Mentions de "SCP" trouvees dans le repo, **qui ne sont PAS des modeles SCP** (a ne pas confondre) :
- `docs/delivery/lot_03_derogations_spec_texte_v1.md` l.397 : citation de l'article R.4113-3 CSP
  ("...ne peut cumuler... en SCP") — c'est du wording d'une **derogation SELARL/medecin**, pas un doc SCP.
- `docs/project/10/11/12/13_*.md` : SCP cite uniquement pour le **classer hors moteur courant**.
- `src/.../generators/lot_04/statuts_sel_exercice_templates.py` : occurrence "SCP" dans un wording
  d'exercice SEL (a verifier au cadrage, mais ce n'est pas un type SCP creable).

**Consequence build :** la phase 0 du playbook (rapatriement + tokenisation des sources) n'a meme pas son
intrant. Sans le DOCX source SCP dans le repo, rien de SCP n'est tokenisable ni codable.

---

## 2. Cas couverts

**Aucun cas SCP n'est couvert par le moteur.** Zero generateur, zero entree catalogue, zero test.

Cas qu'un type SCP DEVRAIT theoriquement couvrir (par analogie SCM/SCS — societe civile a parts/gerant),
**a confirmer entierement par source + Rafael, rien n'est sourced ici** :
- Creation SCP (statuts constitutifs, profession liberale reglementee, 2+ associes praticiens).
- Eventuels satellites (PV nomination gerant, demande d'inscription a l'ordre, declaration non-condamnation,
  procuration) — transverses, deja codes pour d'autres types mais **non cables a un cas SCP** (qui n'existe pas).
- Cession de parts SCP — **non source, non decide**.

Tant que la source SCP n'est pas dans le repo et que NotebookLM/Rafael n'a pas valide le perimetre,
**ces cas restent hypothetiques** : ne pas les coder.

---

## 3. Documents a generer (statut + approche recommandee)

Rappel doctrine projet : rendu **from-scratch** (`docx_builder.py`, ADR-0004). "template-fill" du brief
ne s'applique pas. "a-tokeniser" = modele present mais pas encore tokenise — **ici aucun modele n'est present**.

| Document | Statut | Approche recommandee | Etat reel |
|---|---|---|---|
| Statuts SCP | systematique (creation) — **a confirmer** | from-scratch (apres tokenisation du modele source) | **A TOKENISER d'abord**, mais **modele source ABSENT du repo** -> non constructible |
| Eventuels satellites SCP (pacte, RI, frais communs…) | inconnu | inconnu | **non source, non decide** -> ne pas coder |
| Declaration non-condamnation | systematique (universel) | from-scratch (DOC-001) | generateur universel existe ; **non cable a un cas SCP** (cas inexistant) |
| Autorisation domiciliation | systematique (universel) | from-scratch (DOC-002) | idem ; arbitrage rendu adresse en suspens (transverse) |
| Procuration | systematique (universel) | from-scratch (DOC-003) | idem |
| PV nomination gerant | conditionnel | from-scratch (DOC-004) | generateur existe ; SCP n'est pas dans `PV_NOMINATION_GERANT_STRUCTURES` |
| Demande inscription a l'ordre | conditionnel | from-scratch (DOC-034) | generateur existe ; SCP non cable |

**Recommandation d'approche :** identique a tous les types de ce projet -> **from-scratch deterministe via
`docx_builder.py`**, JAMAIS template-fill du DOCX source. Mais pour SCP la question d'approche est
**prematuree** : il n'y a ni source a tokeniser, ni decision de scope. Le seul travail "reutilisable"
serait, le jour ou SCP serait ratifie, de cabler les documents universels (DOC-001/002/003) deja codes.

---

## 4. Wording EXACT deja disponible

**Aucun wording SCP confirme n'est disponible.** Il n'existe :
- aucune synthese NotebookLM SCP ;
- aucune spec delivery SCP (`docs/delivery/` ne contient rien de SCP) ;
- aucun modele source SCP tokenise.

Le seul texte contenant la chaine "SCP" et qui soit du wording valide est une **citation d'article**
(R.4113-3 CSP) dans une derogation SELARL — **ce n'est pas du wording de document SCP** et ne peut servir
de base a aucun document SCP.

=> **Rien a reutiliser.** Tout wording SCP devra etre tokenise depuis un modele source (absent) puis
valide par Rafael. Ne JAMAIS inventer de wording juridique SCP.

---

## 5. NON TROUVE -> a lever par tokenisation du modele PUIS Rafael (ne jamais inventer)

Pour SCP, le "NON TROUVE" n'est pas une liste de points fins : **c'est la totalite du type**. Sequence
imposee (et bloquee en amont) :

1. **Modele source SCP absent du repo.** Intrant n.1 manquant. A rapatrier (`Modele Statuts SCP - transforme.docx`
   + eventuelle declaration non-condamnation SCP) depuis le Drive vers le repo AVANT toute tokenisation.
   Tant que ce fichier n'est pas dans le repo, **aucune tokenisation n'est possible**.
2. **Tokenisation jamais faite** (corollaire du point 1).
3. **Aucune passe NotebookLM SCP.** Le perimetre metier SCP (profession(s) concernee(s), nombre d'associes,
   regime des parts, gerance, cession, regles ordinales, mentions obligatoires) est **integralement non valide**.
4. **Decision "hors moteur courant" a lever.** Cf. section 7, B1.

Reflexe projet-a-associe (regle 20) : sur tout doute metier SCP, **epuiser d'abord les sources** (modele
source une fois rapatrie, NotebookLM, transcripts Albane) ; si absent/contradictoire, rediger un **message
pour Rafael** (jamais une question metier au PM) — et ne pas faire relayer une question dont la reponse
serait deja dans la source SCP une fois celle-ci importee.

---

## 6. Besoins envers le SOCLE PARTAGE (couche commune requise par CE type)

Profil SCP attendu : **societe civile a PARTS sociales + GERANT** (comme SCM/SCS), exercice EN COMMUN
d'une profession liberale par PLUSIEURS praticiens associes. Sous cette hypothese (a confirmer par source),
les besoins socle seraient proches de SCM/SCS. Le socle existe deja en grande partie ; ce qui manque est
le **cablage SCP** (impossible tant que le type n'existe pas). Detail :

1. **Substitution parts/actions, gerant/president.** EXIGENCE : vocabulaire "parts sociales" + "gerant"
   (PAS "actions"/"president"). DEJA porte par le socle civils (`StatutsCivilsContext`, `GeranceContext`,
   utilises par SCM/SCS/SCI). Reutilisable tel quel pour SCP. **Manquant : un type SCP qui s'en serve.**

2. **Couche multi "LES SOUSSIGNES" / repartition numerotee / PV d'AG.** EXIGENCE forte : SCP = exercice
   en commun, donc PLUSIEURS associes praticiens (comparution multi, repartition numerotee des parts,
   PV d'AG). Le socle a deja : comparution multi-associes (boucle `associes[]`, separateur "ET" — cf.
   `statuts_scm`), repartition numerotee + controle de somme, PV d'AG (cote SPFPL/cession). Reutilisable.
   **Le nombre d'associes SCP (borne min/max) n'est pas source -> a fixer par Rafael, ne pas inventer.**

3. **Personne morale associee.** EXIGENCE : a confirmer si une SCP peut compter une personne morale
   associee. Le socle sait le faire (`StatutsCivilsAssocie` / `_is_morale` / representant, cf. SCM/SCI IRIS).
   Reutilisable SI la source SCP le prevoit — **non source aujourd'hui**.

4. **Couche genre.** EXIGENCE : Ne/Nee + accords selon civilite des praticiens. DEJA en place
   (`domain/enums.Gender`, `front_app/field_derivations.derive_gender_from_civilite`, `utils/grammar.py`).
   Reutilisable tel quel.

5. **Registre (catalogue + lot_status).** EXIGENCE : ajouter `CaseType.SCP`, les `DocumentOccurrence`
   SCP, les definitions `registry/catalog.py` + cablage `registry/lot_status.py` et orchestrateur.
   **MANQUANT integralement** (c'est la creation du type). A ne faire qu'apres source + NotebookLM.

6. **Slice front + deroulante auto-extensible d'associes.** EXIGENCE : un `DossierTypeOption` "SCP creation"
   dans `front_app/dossier_selection.py` (qui n'expose AUJOURD'HUI que `selarl_v1`), un `scp_slice.py` sur
   le patron `selarl_slice.py` (mapping saisie -> `DocumentGenerationContext` -> `generate_docx_files_for_document_codes`
   + `generate_zip_file`), routage dans `shell.py` (aujourd'hui cable SELARL en dur), et une **deroulante
   auto-extensible d'associes** (generaliser le composant additionnel SELARL pour N praticiens). **MANQUANT
   integralement.** Note : ce besoin de socle "selecteur de type + routage shell + saisie multi-associes
   generique" est COMMUN a SCM/SPFPL/SCI/SCP — il devrait etre construit une fois, generiquement, pas
   re-duplique par type.

7. **PDF / ZIP / bundle.** `rendering/pdf_export.py`, `zip_bundle.py`, `bundle.py` existent (utilises par
   `ui_runtime`). Reutilisables ; rien de specifique SCP a ajouter cote rendu bundle.

Resume socle : **le socle est largement pret** (vocabulaire parts/gerant, multi-associes, genre, bundle).
Ce qui manque pour SCP est entierement du **cablage type-specifique** (CaseType, generateur, catalogue,
slice) — et ce cablage est **bloque tant que la source et la decision de scope ne sont pas levees**.

---

## 7. Bloquants de build

| Code | Bloquant | Nature | Qui tranche | Constructible maintenant ? |
|---|---|---|---|---|
| **B1** | SCP classe **"hors moteur courant"** par decision canonique (`13_SOURCE_ARBITRATION_DECISIONS_V1.md`, repris par `10`/`12`). SCP absent de la source-of-truth produit (`Documents_a_generer_par_cas` V1/V3). | **decision produit / canon** | Rafael (perimetre) + Gad (scope/priorisation) | NON — bloquant amont dur |
| **B2** | **Modele source SCP absent du repo.** Le DOCX statuts SCP (et la declaration SCP) ne sont reference que dans un dump Drive non importe. Sans intrant, ni tokenisation ni codage. | source / ops | rapatriement Drive -> repo (technique), puis tokenisation | NON — pas d'intrant |
| **B3** | **Aucune passe NotebookLM SCP.** Perimetre metier integralement non valide (professions, nombre d'associes, parts, gerance, cession, ordinal). | process / metier | Rafael via NotebookLM ; pilote Naomi/Codex | NON tant que B1/B2 ouverts |
| **B4** | **Type inexistant cote moteur** : pas de `CaseType.SCP`, pas de generateur, pas de catalogue, pas de tests, pas de slice front. | technique (creation de zero) | equipe code APRES B1-B3 | NON tant que B1-B3 ouverts |
| **B5** | Documents universels (DOC-001/002/003) non cables a SCP — mais cela presuppose un cas SCP. Transverse, secondaire. | technique | equipe code, apres B4 | NON (depend de B4) |

**Ce qui N'EST PAS constructible maintenant :** absolument tout SCP (moteur, slice, catalogue). A la
difference de SCM/SPFPL/SCI, il n'y a **aucun butin technique a exposer** et **aucun wording confirme**.

**Ce qui serait constructible le jour ou B1+B2+B3 seraient leves :** le type complet, en suivant le
playbook (`COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`) phase 0 -> 10, en reutilisant massivement le socle civils
(parts/gerant, multi-associes, genre, bundle) et le patron de slice SELARL.

**Recommandation anti-derive (pour les equipes de code qui suivront) :** ne PAS commencer a coder SCP "par
analogie SCM". SCP est explicitement hors moteur courant et sans source dans le repo. Toute ligne de code
SCP ecrite avant la levee de B1 (decision Rafael/Gad de reintegrer SCP) + B2 (source rapatriee) + B3
(NotebookLM) serait un type **invente, non sourced, non valide** — exactement ce que le registre de statut
et les regles produit interdisent. Sequence obligatoire : **B1 (GO produit) -> B2 (source) -> B3 (NotebookLM)
-> B4 (build moteur from-scratch + catalogue) -> slice front -> pack Rafael -> cloture canonique.**

---

## 8. Verification effectuee (perimetre nomme)

- Enum `CaseType` lu (`domain/case_catalog.py` l.9-17) : **pas de SCP** confirme.
- Recherche exhaustive "SCP" sur tout le repo : seules des MENTIONS (citation CSP, docs d'import qui
  excluent SCP) ; **aucun type/generateur/test SCP**.
- Recherche exhaustive de tout `.doc`/`.docx` contenant "scp" : **zero fichier**.
- Arbre du dump `project/source_import/raw_drive_dump/` liste : contient scm/SCS/SELARL/SPFPL, **pas SCP**.
- `13_SOURCE_ARBITRATION_DECISIONS_V1.md`, `12_SOURCE_PLACEMENT_PLAN_V1.md`, `10_SOURCE_IMPORT_MANIFEST_V1.md`
  relus : SCP **"hors moteur courant"** confirme.
- `Documents_a_generer_par_cas.docx` et `_V3.docx` : extraction texte+tables, **aucune mention SCP / societe
  civile professionnelle**.
- `COMPANY_TYPE_STATUS_REGISTRY_V1.md` relu : SCP **absent du registre** (8 types, pas SCP).
- Patron de reference relu : `front_app/dossier_selection.py` (n'expose que `selarl_v1`), `selarl_slice.py`
  (imports `domain.models` + `ui_runtime`, rendu via le socle), rapports soeurs SCM/SPFPL/SCI.
- **Aucun fichier de code modifie. Aucune action Git.** Seul ce rapport a ete ecrit.
