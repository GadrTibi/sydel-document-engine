# SOCLE PARTAGE — Plan de la phase B0 (V1)

> ⚠️ **GOUVERNANCE — PROVENANCE CODEX (Gad, 2026-06-07, TRÈS IMPORTANT).** Les moteurs par type
> existants (`statuts_sci/scm/scs/sas/selas_medecin/spfpl_*`, commits **2026-05-14/15**) sont des
> **artefacts CODEX**, bâtis depuis le seul document « Documents à générer par cas » **AVANT NotebookLM**.
> Ils sont **SUSPECTS jusqu'à validation**. Dans ce plan, « moteur TESTÉ » signifie **testé par Codex
> sur son propre comportement**, PAS validé juridiquement — ne pas le lire comme « prêt à livrer ».
> **Règle dure** : l'application ne doit contenir QUE (a) ce que **Claude Code + Gad** ont développé/
> validé ensemble (réf. SELARL, 2026-06+), ou (b) du contenu de versions antérieures **explicitement
> validé**. **Conséquence build** : chaque type passe une **PASSE D'AUDIT DE FIDÉLITÉ** (sortie du
> moteur Codex vs synthèse NotebookLM + modèle source tokenisé + Rafael) AVANT câblage/livraison. On
> garde ce qui passe, on rebâtit le reste. **Aucun moteur Codex non validé ne ship.** Les vagues
> V-A/V-B/V-C ci-dessous sont re-cadrées en conséquence : ajouter une étape **audit-validation par
> type** avant tout « câblage front ».
>
> **Statut** : plan d'architecture. Daté 2026-06-07.
> **Source** : 7 rapports de constructibilité par type (SELAS, SPFPL, SCM, SCI, SCS, SCP, SAS) +
> lecture du code (`front_app/`, `domain/`, `registry/`, `utils/grammar.py`, `project/source_documents/`).
> **Portée** : ce document décrit le SOCLE COMMUN à bâtir **UNE SEULE FOIS** avant de lancer les équipes
> par type. Il ne décide aucune règle métier (cela reste Rafael) et n'autorise aucun merge `main` (GO Gad).
>
> **Garde-fou architecture (transverse, déjà tranché)** : le moteur réel est **from-scratch via
> `docx_builder`**, PAS `docx_template_fill.py`. Les statuts « approach: template-fill » des rapports
> SCI/SCS/SCM/SAS désignent une **substitution de variables dans un texte source tokenisé**, pas
> l'introduction d'un moteur template-fill. **Ne pas introduire `docx_template_fill.py`** (dérive).

---

## Constat d'ancrage (état réel du code, lecture seule)

- **Front = SELARL en dur.** `front_app/dossier_selection.py` n'expose qu'une seule option
  (`selarl_v1`). `front_app/shell.py` + `data_entry.py` câblent toute la saisie sur des clés
  `selarl_*` (profession, gérant/parts, multi-associés DOC-004). Tout type non-SELARL est
  **invisible au front**, même quand son moteur est testé.
- **Moteur multi-types prêt côté registre.** `CaseType` porte déjà SELARL, SELAS, SPFPL_CESSION,
  SPFPL_APPORT, SCS, SCI, SCM, SAS — **mais PAS SCP**. `catalog.py` + `case_catalog.py` modélisent les
  occurrences de ces types.
- **Couche genre minimale en place.** `utils/grammar.py` expose `subject_line`, `birth_label`,
  `filiation_label` par `Gender` ; `front_app/field_derivations.derive_gender_from_civilite` dérive
  le genre. Suffit pour Né/Née ; insuffisant pour les listes de termes féminins SELAS (Présidente…).
- **Personne morale associée : partiel.** `domain/models.py` a `Company` riche (forme, capital, RCS,
  représentant via `Person`), mais le `Associe`/repeater du **front** ne sait saisir qu'une personne
  physique. Le besoin morale est porté par SCI IRIS, SCM, SCS, SPFPL `associes_cible[]`.
- **Sources tokenisables présentes** dans `project/source_documents/lot_01..05` pour la quasi-totalité
  des types — **sauf** : modèle SELAS multi-associés (Reynaud) et modèle SCP. (Vérifié : seul
  `Statuts_SELAS_medecin.docx` mono existe ; aucun fichier Reynaud ni SCP.)

---

## 1. Besoins de socle — liste consolidée et dédupliquée (qui les demande)

Sept briques transverses ressortent. La colonne « Demandé par » liste les types qui en dépendent ;
« État socle » résume ce qui existe déjà vs ce qui manque.

| # | Brique de socle | Demandé par | État socle (réel) |
|---|---|---|---|
| **S1** | **Substitution vocabulaire dirigeant + titres** (Président/actions vs Gérant/parts) — paramétrable par type, **jamais** regex globale | SELAS, SPFPL, SAS (président/actions) ; SCI, SCS, SCM, SCP (gérant/parts) | Moteur le fait **par rôle** ; le **front SELARL câble `gérant`/`parts sociales` en dur**. À exposer comme paramètre de type. **Dette nommée** : `models.py Associe.nb_parts` / `CapitalContext.nb_parts_total` restent nommés « parts » même côté actions (SELAS) → normaliser vers titres/actions. |
| **S2** | **Couche multi « LES SOUSSIGNÉS »** : comparution N blocs + répartition numérotée des parts (plage début/fin par associé) + accord genre/nombre + signatures N | SELAS (2-5), SPFPL (`associes_cible[]`), SCM (statuts 1-6), SCI (1-6), SCS (1-6, rôles commandité/commanditaire), SCP (borne à sourcer) | **En construction côté SELARL** (`selarl_slice.additional_associes`, contrat TRACK_B_MULTI). SPFPL/SCM/SCS/SCI réutilisent **sans toucher**. **Piège dur** : satellites SCM **figés à 2 parties** (`TWO_PARTIES=2`) → la généralisation N attend l'arbitrage Rafael. |
| **S3** | **Personne morale associée** (forme + capital + siège + RCS + représentant + fonction) | SCI IRIS (besoin réel V1), SCM (statuts), SCS, SPFPL (`AssocieCible.type=='personne_morale'`, prêt moteur), SELAS (Q-C Rafael) | **GAP socle front** : le repeater d'associés ne saisit que des personnes physiques. Côté **moteur** : SPFPL/SCM/SCS/SCI gèrent déjà la morale ; **SELAS NON** (`models.py Associe` = physique seulement, pas de `forme_pm/rcs/representant`). |
| **S4** | **Couche genre par paires** (table de paires, jamais substitution globale) : Président/Présidente, Soussigné(e)(s), Associé(e)(s), Né(e) | SELAS (paires confirmées) ; SCI/SCS/SCP (Né/Née minimal) ; SPFPL (existe, non branché sur DOC-029, cédant masculin = dette) ; SAS (V1 **verrouillé masculin**) | Helpers `utils/grammar` + `derive_gender_from_civilite` **existants et réutilisables**. À enrichir d'une **table de termes féminins SELAS** (au-delà de Présidente). **Garde-fou** SELARL « associé suspect » à assouplir. SAS V1 : front doit **borner masculin** ou afficher féminin bloqué. |
| **S5** | **Registre / catalogue** (CaseType + DocumentOccurrence + catalog.py + lot_status + orchestrateur) | Tous | **PRÊT** pour SELARL/SELAS/SPFPL/SCM/SCI/SCS/SAS. **MANQUANT intégralement pour SCP** (pas de `CaseType.SCP`). Extension nécessaire pour le pack SELAS multi. |
| **S6** | **Slice front + routage par type** (`<type>_slice.py` sur patron `selarl_slice.py` + entrées `dossier_selection` + routage `shell.py`/`data_entry.py` aujourd'hui SELARL en dur) | Tous sauf SELARL (déjà fait) | **MANQUANT pour TOUS** (SELAS, SPFPL, SCM, SCI, SCS, SCP, SAS). **Cœur du build front.** Constructible immédiatement sur patron SELARL, réversible, **pas de GO PM** pour la brique technique. |
| **S7** | **Déroulante d'associés auto-extensible** (composant repeater 1→N réutilisable, réutilise `SelarlAdditionalAssocieInput`) + statut document front (`build_document_status_for_code`) + branchement PDF/ZIP/bundle | Tous les types multi-associés (SELAS, SPFPL, SCM, SCI, SCS, SCP) | Statut document + PDF/ZIP/bundle **existent**, à brancher via le slice. Le **repeater générique** est à extraire du SELARL pour être partagé (aujourd'hui SELARL-only). |

**Déduplication clé** : S6 (slice + routage) et S7 (repeater auto-extensible) sont **le même chantier
front transverse** demandé identiquement par 6 rapports sur 7. Le bâtir **génériquement une fois**
(et non type par type) est le principal gain de la phase B0.

---

## 2. Ordre de construction recommandé (sérialisé vs parallélisable)

### Phase B0 — SÉRIALISÉE (socle commun, une seule équipe, dans cet ordre)

1. **B0.1 — Normalisation vocabulaire moteur (S1, dette).** Renommer `nb_parts`/`nb_parts_total` vers
   une abstraction titres/actions paramétrable par type (parts vs actions). **Bloquant** car tous les
   types par actions (SELAS/SPFPL/SAS) héritent de ce nommage. À faire **avant** d'ouvrir les slices
   par actions, sinon dette propagée 3×.
2. **B0.2 — Extraction du repeater d'associés générique (S2 + S7).** Sortir
   `SelarlAdditionalAssocieInput` + le bloc multi-associés de `selarl_slice`/`data_entry` vers un
   composant front **partagé**, paramétré (borne N, vocabulaire parts/actions, rôle statutaire
   optionnel). Sérialisé car S6 en dépend.
3. **B0.3 — Saisie « personne morale associée » au socle front (S3).** Étendre le repeater pour saisir
   forme + capital + siège + RCS + représentant + fonction (le moteur sait déjà les consommer côté
   SCI/SCM/SCS/SPFPL). Sérialisé car SCI IRIS, SCM, SCS le réclament dès leur slice.
4. **B0.4 — Table de paires de genre étendue (S4).** Ajouter la table de termes féminins
   (Président/Présidente + liste SELAS à confirmer Rafael) et **assouplir le garde-fou « associé
   suspect »**. Le minimal Né/Née reste tel quel.
5. **B0.5 — Routage par type au shell + déroulante de sélection multi-types (S6).** Décâbler
   `shell.py`/`data_entry.py` du SELARL en dur ; faire de `dossier_selection` un vrai registre
   d'options ; router vers le bon `<type>_slice`. C'est l'**ouverture** qui rend les slices visibles.
6. **B0.6 — Extension registre pour SCP (S5).** Créer `CaseType.SCP` + occurrences + entrées catalog
   **vide/bloquées** (le contenu SCP dépend des bloquants amont — cf. §5), pour que SCP ne soit pas un
   trou dans le registre. (Faisable techniquement ; ne génère rien tant que B-SCP amont non levé.)

### Ensuite — PARALLÉLISABLE par équipe-type (une branche par type)

Une fois B0 livré, **chaque type avance en parallèle** sur sa propre branche, car il ne fait plus que :
`<type>_slice.py` (patron SELARL) + `DossierTypeOption` + câblage des documents au repeater partagé.

| Vague | Types | Pourquoi groupés |
|---|---|---|
| **V-A (prêts moteur, pas de blocage métier dur)** | **SCI, SCS, SCM** | Moteur statuts **TESTÉ** ; seul le front manque. Réutilisent S2/S3/S6/S7 directement. SCM limité aux satellites figés à 2 (cf. B2 métier). |
| **V-B (prêts moteur, attente NotebookLM)** | **SPFPL (cession + apport), SAS** | Moteur testé mais **passe NotebookLM jamais faite** → génération **NO-GO** tant que Rafael n'a pas validé ; le **slice front est constructible** en parallèle (réversible). |
| **V-C (attente source + Rafael)** | **SELAS multi 2-5** | Bloqué tant que le **modèle Reynaud n'est pas rapatrié+tokenisé** ET Q-B/C/D Rafael non tranchées. L'unipersonnel V1 codé devient **socle réutilisable**, pas livrable. |
| **V-D (bloqué amont, ne pas coder)** | **SCP** | Séquence obligatoire **B1(GO produit)→B2(source)→B3(NotebookLM)→build**. Ne **PAS** coder par analogie SCM. |

**Principe de sérialisation** : tout ce qui touche `models.py`, le repeater partagé, le routage shell
et le registre est **sérialisé en B0** (couche partagée → risque de collision). Tout ce qui est
`<type>_slice.py` + câblage documents est **parallélisable** (isolé par fichier/branche).

---

## 3. Plan de tokenisation

### 3.1 Répertoires sources présents (vérifiés sur disque)

`project/source_documents/lot_01..05` contient déjà la quasi-totalité des modèles. Priorité de
tokenisation = **prête / déjà tokenisée** d'abord, puis **à tokeniser depuis source présente**,
puis **source absente à rapatrier**.

| Priorité | Modèle source (chemin réel) | Type | État tokenisation |
|---|---|---|---|
| **Déjà tokenisé / moteur testé** | `lot_04/Modèle statuts SCI.docx`, `Modèle statuts SCI IRIS.docx` | SCI | TESTÉ — rien à refaire |
| | `lot_04/Statuts_SCS_modele.docx` | SCS | TESTÉ |
| | `lot_04/Statuts SCM.docx` + satellites `lot_05` (pacte/RI/frais communs/liste dépenses) | SCM | TESTÉ (satellites figés 2 parties) |
| | `lot_04/Statuts_SELAS_medecin.docx` (mono) | SELAS | Blocs déterministes codés (unipersonnel) |
| | `lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx` | SAS | TESTÉ (figé dans `statuts_sas.py`) |
| | `lot_04/Statuts_SPFPLAS_dentistes_cession.docx`, `Statuts SPFPLAS dentistes - apport.docx` + `lot_05` (note info, PV, actes, attestation, contrat apport) | SPFPL | TESTÉ |
| | `lot_01` (DNC, domiciliation, procuration), `lot_02` (PV gérant, inscription ordre, renonciation/avertissement conjoint) | Universels | Générateurs from-scratch existants |
| **À tokeniser (source présente, non faite)** | Attestation dépôt capital + liste souscripteurs SELAS (à identifier le DOCX canonique exact — **B5 SELAS**) | SELAS | `a-tokeniser` — **document canonique exact non identifié** |
| | Questionnaire Ordre médecin | SELAS | `a-tokeniser` (si fourni) |
| **SOURCE ABSENTE — à rapatrier AVANT toute tokenisation** | **Statuts SELAS médecin MULTI-ASSOCIÉS (Reynaud)** — confirmé absent du repo (seul le mono existe) | SELAS | **MANQUANT** — rapatrier le `.docx`, en **retirant toute valeur réelle patiente** avant versionnement (B9) |
| | **Statuts SELAS dentiste** | SELAS | **MANQUANT** — aucune source DOCX dans le repo (B4 SELAS) |
| | **Modèle Statuts SCP (« Modele Statuts SCP - transforme.docx »)** — référencé seulement dans un dump Drive non importé | SCP | **MANQUANT** — rapatriement requis avant tokenisation (B2 SCP) |

### 3.2 Règles de tokenisation (transverses)

- **Ne jamais versionner un `.docx` source contenant des données réelles** (Reynaud = données patiente
  réelles) : tokeniser en retirant les valeurs, ne committer que le modèle neutralisé.
- **Pas d'index de paragraphes en dur** quand évitable : dette connue sur `statuts_scm.py`
  (`ASSOCIATE_SLICE=(25,42)…`), `SCS_TEMPLATE` (`(14,18)/(43,58)…`) — casse silencieusement si le DOCX
  source est réédité. À documenter comme **dette technique non bloquante**, ne pas la propager aux
  nouveaux types.
- **Rendu from-scratch** (ADR-0004) : la tokenisation alimente la substitution de variables, jamais un
  moteur template-fill.

---

## 4. NON TROUVÉ → message Rafael groupé (par type)

> À transmettre à Rafael **groupé**, via Gad (jamais une question métier directe au PM). Avant relais :
> vérifier que la réponse n'est pas déjà dans le corpus tokenisé / NotebookLM / locks de retours humains.

### SELAS
- Q-B : gérer les **Directeurs Généraux** (présents art.15 Reynaud) ou hors premier jet ?
- Q-C : accepter **associé personne morale** + règle dure « majorité des droits de vote aux exerçants » ?
- Q-D : **Reynaud = LE modèle de référence ou un exemple** ? Manque variantes 2/3/4/5 associés + genres.
- Liste exacte des **termes féminins** au-delà de « Présidente ».
- Carte **associé vs actions** par article, validée sur statuts réels.
- **Plans/devis Ordre + attestation capital** : bloquants/obligatoires dans le pack V1 ?
- Modèle exact **questionnaire Ordre médecin**.
- **Filiation** dans la DNC du président : champ requis ?
- Titre exact **lettre renonciation conjoint** (régime communautaire).
- Nomination président **dans les statuts vs acte séparé** (sort de DOC-004 SELAS).
- Confirmer le **document canonique exact de l'attestation dépôt capital SELAS**.

### SPFPL
- Périmètre réel de l'**acte de cession d'ACTIONS** (DOC-029, codé sous réserves : cédant masculin,
  cible SELAS dentiste, paiement comptant, Yousign) — valider ou retirer de V1.
- **PV classés « cession » mais rédigés en « apport »** (parts apportées / contrat d'apport) :
  correction de formulation juridique à confirmer.
- **SPFPL médecins** sous route SPFPL **vs** route SAS (DOC-015) : périmètre à trancher.
- **PV « nomination gérant » (DOC-004)** routé vers une SPFPLAS qui a un **Président** : incohérence
  forme/document à lever.
- Libellé **« commissaire aux apports » vs « commissaire aux comptes »** (sources divergentes).
- Listes **multi-souscripteurs** (attestation) et **multi-associés** (statuts) : accords pluriel non
  sourcés → bloqués V1.

### SCM
- **Passe NotebookLM SCM jamais faite** : 9 points satellites jamais confirmés.
- **Incohérence borne 2 (satellites) vs 6 (statuts)** : un client SCM à 3 associés génère les statuts
  mais bloque les satellites — **ne pas inventer de variante N** sans arbitrage.
- Activation des satellites : **auto vs sélection explicite** ?
- Pacte : clauses sensibles (cession/préemption/non-concurrence) + annexes à confirmer.
- Liste dépenses : table source, marques X, lignes sans marque.
- Contrat frais communs : description fixe locaux dentaires + clé temps d'occupation.
- RI : placeholder unique forme sociale, clauses téléphone, 4 exemplaires.
- Mentions **Docteur/praticien/cabinet dentaire** généralisables au médecin ?

### SCI
- **SCI non-IRIS avec associé personne morale** : pas de modèle source → tokeniser si fourni puis Rafael.
- **Cession de parts SCI** (acte/agrément/PV) : aucun modèle SCI présent.
- **Apport en nature / immeuble** : source = apports numéraire seulement.
- Couche **genre/pluriel** statuts civils plus riche que Né/Née (`grammar_variants=False`) : confirmer.
- Variantes **démembrement usufruit/nue-propriété** au-delà de la source.

### SCS
- **Passe NotebookLM SCS jamais faite.**
- **Nature de la SCS attendue** : la source est **civile immobilière** ; une **SCS d'exercice
  professionnel** n'est pas sourcée.
- **Cession / transformation / dissolution / apport en nature** SCS : aucun modèle source.
- Couche **genre/pluriel** plus riche (`grammar_variants=False`) à confirmer.
- Règle métier sur **nombre d'exemplaires** et **cabinet mandataire** (valeurs non figées par source).

### SCP
- **Passe NotebookLM SCP jamais faite** : périmètre métier **intégralement** non validé (professions,
  nombre/borne d'associés, régime des parts, gérance, cession, règles ordinales, mentions obligatoires).
- Possibilité d'une **personne morale associée** : non sourcée.
- **Aucun wording disponible** : ne jamais inventer.

### SAS
- Confirmer que le chemin « SAS » correspond bien aux **statuts SPFPL médecins** attendus (pas de SAS
  générique).
- **Président/actionnaire féminin** : aucun wording féminin sourcé (code verrouillé masculin).
- **Situations matrimoniales** autres que marié(e) : non sourcées.
- Incohérences de vocabulaire source (« parts sociales »/« gérant » dans une SAS) : corriger ?
- **Multi-actionnaires / multi-souscripteurs** : non sourcés → bloqués V1.
- Condition suspensive **inscription Ordre** : applicable à tous les dossiers SAS ?
- Variante attestation **numéraire seul** (sans bloc apport en nature) : non sourcée.

---

## 5. Bloquants de SCOPE à remonter à Gad (décisions FONCTIONNELLES)

> Ce sont des arbitrages de **périmètre produit** qui appartiennent à Gad (pas du métier juridique
> Rafael, pas de la technique). À présenter en carte de décision cliquable.

1. **SELAS — cible V1 (déjà tranché, à confirmer).** Décision Gad 2026-06-05 : cible = **multi-associés
   2-5**, l'unipersonnel codé devient **socle réutilisable, pas livrable**. → Confirmer que ce statut
   tient : on ne livre PAS l'unipersonnel SELAS seul.

2. **SCP — GO/NO-GO produit (DUR, amont).** SCP est classé **« hors moteur courant »** par décision
   canonique (`13_SOURCE_ARBITRATION_DECISIONS_V1.md`) ET absent de la source-of-truth produit
   (`Documents_a_generer_par_cas` V1/V3). → **Décision produit/canon à lever par Gad + Rafael avant
   tout code SCP.** Tant que NO-GO, SCP reste hors vague de build (registre câblé vide en B0.6 seulement).

3. **Ordre de priorité des vagues de build.** Proposé : **V-A (SCI/SCS/SCM)** d'abord (moteur prêt,
   pas de NotebookLM bloquant), puis **V-B (SPFPL/SAS)** (slice front en parallèle, génération en
   attente NotebookLM), puis **V-C (SELAS multi)** (attend source Reynaud + Rafael). → Gad valide
   l'ordre ou repriorise.

4. **Périmètre « génération » vs « slice visible ».** Pour SPFPL/SAS/SELAS, le **slice front** est
   constructible et réversible sans GO PM, mais la **génération réelle reste NO-GO** tant que la passe
   NotebookLM (SPFPL/SAS/SELAS dentiste) n'est pas faite. → Confirmer qu'on accepte de **livrer des
   slices visibles « génération bloquée »** (UI en place, bouton désactivé) pendant l'attente métier.

5. **Rapatriement des sources manquantes.** Reynaud (SELAS multi), Statuts SELAS dentiste, Modèle SCP
   sont **absents du repo** (dump Drive non importé). → Décision Gad : qui rapatrie, et acceptation de
   la règle « jamais versionner le `.docx` réel avec données patiente » (neutralisation avant commit).

**Rappel garde-fou GO PM** : tout **merge sur `main`** de l'un de ces types, et toute **génération**
livrée à un utilisateur, restent soumis à GO Gad (génération SELAS/SPFPL/SAS/SCP = NO-GO sans validation
Rafael des points §4).

---

## Annexe — Constructible MAINTENANT sans GO PM (biais d'action)

Sur branche dédiée, réversible, sans toucher `main` ni générer pour un utilisateur :
- **B0.1 → B0.6** (tout le socle commun) — couche partagée, à sérialiser, mais 100 % constructible.
- **Slices front V-A (SCI/SCS/SCM)** dès B0 livré — moteur testé, pas de blocage métier dur sur la
  constitution (SCM hors variante satellites >2).
- **Slices front V-B (SPFPL/SAS)** avec **génération désactivée** en attendant NotebookLM.

À NE PAS construire : SELAS multi (source absente), SCP (GO produit absent), toute variante au-delà
des bornes sourcées (multi-souscripteurs, satellites SCM >2, cession/apport en nature sans modèle).
