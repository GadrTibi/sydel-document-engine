# SELAS — Build readiness V1 (analyse de constructibilité)

Date : 2026-06-07
Auteur : analyste de constructibilité (lecture seule du code, aucun fichier de code modifié)
Décision globale : **GO build sur branche dédiée (socle + statuts multi)** ; **NO-GO génération / merge** tant que Rafael n'a pas tranché la revue juridique.
Branche de référence du butin SELAS : `origin/naomie/selas/recup-codex` (PAS encore mergée sur `main`).

> AVERTISSEMENT MÉTHODE — Les chemins annoncés dans le brief de mission n'existent pas sur `main` :
> il n'y a ni `docs/project/types/SELAS/NOTEBOOKLM_ANSWERS.md`, ni `NOTEBOOKLM_PROMPTS_V2.md`, ni
> `WORKFLOW_TYPE_ENTREPRISE_V1.md`, ni `rendering/docx_template_fill.py`. La matière SELAS réelle vit
> sur la branche `naomie/selas/recup-codex` (specs `docs/sprints/SPRINT_SELAS_*`, journal NotebookLM,
> cartographie Reynaud, `front_data/selas_schema.py`). La recette canonique est `docs/project/02_CODEX_WORKFLOW.md`
> (+ `COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`). L'architecture de rendu est **from-scratch** (`rendering/docx_builder.py`
> + blocs de texte codés), **PAS template-fill** : la préférence « template-fill » du brief ne correspond pas
> au moteur réel — voir §3.

---

## 0. Constat de divergence de branches (à traiter AVANT tout build)

Le travail SELAS le plus avancé n'est pas sur `main`. Il est sur `origin/naomie/selas/recup-codex`,
qui contient ~70 fichiers / +8 793 lignes en un snapshot (`4b0c106`) :

- **Code** : `front_data/selas_schema.py` (554 l.), rôle `ACTIONNAIRE`, validation, +84 l. orchestrateur
  (sélection pack V1 + garde-fous), `generators/lot_04/statuts_selas_medecin.py`, adaptation procuration/DNC, registre.
- **Tests** : `tests/unit/test_selas_front_schema.py` (483 l.) + `test_orchestrator_service.py` → 118 tests verts (sous-ensemble).
- **Specs** : ~25 docs `docs/sprints/SPRINT_SELAS_*` (matrice, roadmap A→P, contrat front, reuse audit, triple-source, human-review pack).
- **Journal NotebookLM** : `SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` rempli (8 réponses structurées) — sur `main` ce fichier est VIDE.

Sur `main`, SELAS existe déjà partiellement (et plus ancien) : `CaseType.SELAS`, `DOC-018` au registre
(statut `TESTE`), `StatutsSelasMedecinGenerator` branché dans l'orchestrateur, occurrences SELAS dans
`domain/case_catalog.py`. Mais le socle front/data SELAS (`selas_schema.py`) et le journal NotebookLM
**n'y sont pas**.

ATTENTION : `recup-codex` a aussi divergé sur des docs non-SELAS (supprime de nombreux rapports de revue
SELARL, réécrit `01_EXECUTION_BOARD.md` / `04_LAST_STATE.md`). Un merge naïf vers `main` régresserait
le canon SELARL. La réconciliation doit être **sélective** (cherry-pick du butin SELAS), pas un merge brut.

**Bloquant de build n°1** : décider de la stratégie de réconciliation `recup-codex` → `main` (cherry-pick
SELAS uniquement vs merge). C'est une décision technique (à prendre par le Second, pas par le PM), mais elle
conditionne toute reprise propre.

---

## 1. Inventaire des modèles source (fichier → document juridique + cas couvert)

### Sources DOCX SELAS DÉJÀ dans le repo (`project/source_documents/`, `project/source_truth/`)
| Fichier | Document juridique | Cas couvert | Tokenisé ? |
|---|---|---|---|
| `lot_04/Statuts_SELAS_medecin.docx` | Statuts SELAS médecin | Création, associé unique (V1) | OUI → `DOC-018` from-scratch |
| `lot_02/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx` | Renonciation associé conjoint (régime communautaire) | Conditionnel communauté → `DOC-005` | OUI (variante SELAS) |
| `lot_05/Courrier SDE - SELAS.docx` | Courrier SDE cession SCM | Conditionnel SCM → `DOC-032` | OUI (variante SELAS) |
| `lot_05/PV AGE cession part SCM - SELAS.docx` | PV AGE cession parts SCM | Conditionnel SCM → `DOC-031` | OUI (variante SELAS) |
| `project/source_truth/modele Statuts SELAS avec MH.docx` | Statuts SELAS + micro-holding / actions de préférence | Cas complexe — `no-go V1` | NON (lu globalement seulement) |

### Modèles source SELAS PAS dans le repo (à rapatrier + tokeniser) — BLOQUANT TOKENISATION
| Fichier | Emplacement | Document juridique | Cas couvert | Action |
|---|---|---|---|---|
| `Statuts SELAS DU DR ISABELLE REYNAUD.docx` | `C:/Users/Gad/Downloads/` | Statuts SELAS médecins **multi-associés** (38 articles) | **Multi-associés 2-5, dont 1 personne morale, présidence + DG** | NE JAMAIS versionner le `.docx` réel (données patiente réelles). Tokeniser → ne versionner que le modèle tokenisé. Cartographie déjà faite : `SPRINT_SELAS_MULTI_CARTOGRAPHIE_REYNAUD_001.md` |
| `modele Statuts SELAS avec MH.docx` | `C:/Users/Gad/Downloads/` (+ copie repo `source_truth`) | Statuts SELAS avec micro-holding | Actions de préférence / personne morale | Hors V1 ; à tokeniser seulement quand le cas MH sera ouvert |

> Aucun `.docx` SELAS dédié n'existe pour : statuts SELAS **dentiste**, PV/décision **président** séparé,
> attestation de dépôt de capital SELAS, questionnaire Ordre médecin. → voir §5 (NON TROUVÉ).

---

## 2. Cas couverts

| Cas | Statut constructibilité | Source |
|---|---|---|
| Création SELAS médecin, **associé unique, président unique** | Codé sur `recup-codex` (DOC-001/002/003/034/018), smoke OK, en attente revue humaine | `ROADMAP_TO_COMPLETION_001` |
| Création SELAS médecin **multi-associés (2-5)** | **Nouvelle cible validée Gad 2026-06-05** ; cadrage fait (cartographie Reynaud), code NON fait, dépend de Rafael (DG / personne morale) | `REPRISE_MULTI_ASSOCIES_001`, `MULTI_CARTOGRAPHIE_REYNAUD_001` |
| Régime communautaire (conjoint) | Conditionnel codé (DOC-005/006), effet juridique SELAS **non tranché** | matrice + log NotebookLM |
| SCM (cession parts) | Sources SELAS présentes (DOC-031/032/033), `adapter` hors V1 simple | matrice |
| Cession cabinet / fonds (passage BNC) | `manuel` / `no-go V1` — rédaction ultra-personnalisée | matrice + log Q6 |
| Dérogation / site distinct | `manuel` / `reserve` | matrice |
| SELAS dentiste | `no-go` — source statuts dentiste introuvable | matrice |
| Directeur général | `no-go` — non trouvé NotebookLM ; PRÉSENT dans le cas réel Reynaud → Q-B Rafael | matrice + Reynaud |
| Associé personne morale | `no-go V1` actuel ; PRÉSENT dans Reynaud → Q-C Rafael | Reynaud |
| Micro-holding / actions de préférence | `no-go V1` — sprint séparé | matrice |

**Tension de scope à signaler** : la cible a basculé de l'unipersonnel (V1 codée) vers le **multi-associés
2-5** (Gad, 2026-06-05). L'unipersonnel est « rangé, pas supprimé » comme base réutilisable. Le pack codé
sur `recup-codex` est donc un socle, pas la cible produit finale.

---

## 3. Documents à générer (statut + approche recommandée)

> RÈGLE D'APPROCHE — le moteur Sydel est **from-scratch** : chaque générateur reconstruit le DOCX via
> `rendering/docx_builder.py` (`new_document()` + helpers de style) à partir de blocs de texte codés
> (ex. `STATUTS_SELAS_MEDECIN_BLOCKS` dans `statuts_sel_exercice_templates.py`). Il n'existe PAS de
> couche « template-fill » qui chargerait le `.docx` source et remplacerait des balises. Donc « approche
> recommandée » = **from-scratch (conforme au moteur)** dès qu'un modèle est tokenisé en blocs ; « à-tokeniser »
> = modèle présent mais blocs pas encore extraits. Ne pas introduire de template-fill : ce serait une dérive
> architecturale par rapport au reste du moteur.

| Document | Code | Statut | Approche recommandée | État build |
|---|---|---|---|---|
| Déclaration de non-condamnation (président) | DOC-001 | systématique | from-scratch (générateur Lot 1 existant) | codé, SELAS-safe à revalider ; **filiation président non tranchée** |
| Autorisation de domiciliation | DOC-002 | systématique | from-scratch (Lot 1 existant) | codé ; neutralité SELAS à confirmer |
| Procuration (président) | DOC-003 | systématique | from-scratch (Lot 1 existant, adapté président) | codé `adapter` ; wording « président » à verrouiller |
| Demande d'inscription à l'Ordre | DOC-034 | systématique | from-scratch (existant, overlay SELAS) | codé `DONE_PARTIAL_QA` ; pièces ordinales à confirmer |
| Statuts SELAS médecin (associé unique) | DOC-018 | systématique (si médecin) | from-scratch (`STATUTS_SELAS_MEDECIN_BLOCKS`) | codé `TESTE`/`DONE_PARTIAL_QA` ; cible multi à refaire |
| Statuts SELAS médecin **multi-associés** | (à créer) | systématique (nouvelle cible) | **à-tokeniser** (Reynaud) puis from-scratch sur couche multi | NON codé ; dépend Rafael Q-B/Q-C + couche SEL partagée |
| Lettre de renonciation conjoint | DOC-005 | conditionnel (communauté) | from-scratch (source SELAS tokenisée) | codé ; effet juridique SELAS à arbitrer |
| Lettre d'avertissement conjoint | DOC-006 | conditionnel (communauté) | from-scratch | codé MAIS marqué `réserve` dans la matrice → incohérence à trancher |
| Décision / PV nomination président séparé | (proche DOC-004) | conditionnel / réservé | from-scratch | **réservé** : nomination absorbée dans les statuts V1 ; rouvrir si Rafael exige acte séparé |
| Attestation dépôt capital + liste souscripteurs | (à définir) | systématique (selon Q4 Rafael) | **à-tokeniser** (source canonique exacte à identifier) | réservé ; document canonique pas identifié |
| Statuts SELAS dentiste | (à définir) | hors-création V1 | à-tokeniser (source manquante) | bloqué — pas de source |
| Plans locaux / devis matériel (Ordre) | hors DOC-XXX | conditionnel (pièce à fournir) | hors-création (pièce uploadée, pas générée) | bloquant/obligatoire selon Q3 Rafael |
| Questionnaire Ordre médecin | (à définir) | conditionnel (profession=médecin) | à-tokeniser (modèle à fournir par Rafael, Q5) | non sourcé |
| Cession cabinet/fonds (DOC-009..012) | DOC-009/010/011/012 | hors-création (cas cession) | from-scratch existant mais `manuel`/`no-go V1` | hors happy path |
| SCM (DOC-031/032/033) | DOC-031/032/033 | conditionnel (SCM) — séparé | from-scratch existant, overlay SELAS | hors V1 simple |
| Avenant bail (DOC-007), Appel de fonds (DOC-008), Dérogations (DOC-013) | — | conditionnel / réservé | from-scratch existant | hors V1 |

---

## 4. Wording EXACT déjà disponible (confirmé)

### Confirmé par la boucle NotebookLM (matière exploratoire, sourcing faible — à re-valider Rafael)
- **Forme sociale** : « Société d'exercice libéral par actions simplifiée » (statuts), abrégé « SELAS ».
- **Gouvernance** : rôle **Président** (jamais « Gérant » en SELAS).
- **Capital** : **actions** (jamais « parts sociales ») ; « cession d'actions » (jamais « cession de parts »).
- **Numérotation actions V1** : « 1 à N » suffit (Q6) ; pas d'alphanumérique spécial.
- **Genre dirigeant** : le titre s'adapte → « **Présidente** » pour une femme (Q1) ; genre = donnée obligatoire ; accords par table de paires (PAS de substitution globale de chaînes).
- **Lexique personnes** : « **associé** » pour les personnes (Q2, confirmé par le cas réel Reynaud : ≈177 occurrences « associé » ≫ « actionnaire ») — donc NE PAS remplacer « associé » par « actionnaire » dans les statuts.

### Confirmé par le code déjà écrit (`recup-codex`, déterministe, testé)
- Blocs de texte des statuts SELAS médecin associé unique : `STATUTS_SELAS_MEDECIN_BLOCKS` (`statuts_sel_exercice_templates.py`), avec contrôle de cohérence capital = nb actions × valeur nominale.
- Overlay `selas_medecin`, structure `SELAS`, titre de capital « actions » (`title_type="actions"`).
- Tokens cartographiés pour le multi (Reynaud) : `denomination_sociale`, `forme_sociale`, `objet_social`, `siege_social_adresse`, `lieu_exercice`, `duree_annees`, `capital_montant`, `nombre_actions_total`, `valeur_nominale_action`, et bloc associé répété `associe[i].*` (voir cartographie).

### Paires de genre confirmées (réutilisées de SELARL, jamais de regex de terminaison)
Président/Présidente, Soussigné(e)(s), Associé(e)(s), Né(e).

---

## 5. NON TROUVÉ → à lever par tokenisation du modèle PUIS Rafael (ne JAMAIS inventer)

### Points pour Rafael (déjà packagés : `PACK_PASSATION_NOTEBOOKLM_SELAS_2026-06-05.md` + `REPRISE_MULTI_ASSOCIES_001`)
- **Q-B** : gère-t-on les **Directeurs Généraux** (présents art. 15 Reynaud) ou hors premier jet ?
- **Q-C** : accepte-t-on un **associé personne morale** (Société Civile dans Reynaud) ou médecins physiques seulement ? + inscrire la règle dure « majorité des droits de vote aux exerçants » comme garde-fou moteur ?
- **Q-D** : Reynaud est-il LE modèle de référence du multi ou un exemple ? Il manque des modèles 2/3/4/5 associés + variantes de genre pour figer la trame.
- **a** : wording féminin exact au-delà de « Présidente » (liste des termes à accorder).
- **b** : carte « associé vs actions » par article, validée sur les vrais statuts.
- **c** : plans/devis Ordre + attestation capital → confirmés bloquants/obligatoires du pack V1 ?
- **d** : fournir / valider le modèle exact du **questionnaire Ordre médecin**.
- Filiation dans la **DNC du président** (champ de saisie requis ?).
- **Titre exact** de la lettre de renonciation conjoint (régime communautaire).
- Nomination du président **dans les statuts** vs **acte séparé** (tranche le sort de DOC-004 SELAS).
- Assouplir le **garde-fou anti-régression** qui traite « associé » comme suspect (le cas réel confirme « associé »).

### À lever d'abord par TOKENISATION (avant même Rafael)
- Modèle exact des **statuts SELAS dentiste** : aucune source DOCX dans le repo → tokeniser dès qu'un modèle est fourni.
- **Attestation de dépôt de capital SELAS / liste des souscripteurs** : document canonique exact non identifié (famille DOC-024/DOC-042 à ne pas confondre).
- Trame multi-associés 2-5 : tokeniser le **Reynaud tokenisé** (cartographie faite, valeurs réelles à retirer).

### Hors V1 (non trouvés, déjà bloqués par garde-fous code)
Démembrement nue-propriété/usufruit, seuils de blocage/majorité par défaut, clause d'agrément des héritiers, libération partielle du capital (1/2, 1/4), apports en industrie. Ne PAS inventer ; rester `no-go`.

---

## 6. Besoins envers le SOCLE PARTAGÉ (couche SEL commune)

Ce que **CE type (SELAS multi-associés)** exige du socle, avec l'état actuel :

| Besoin socle | Pourquoi SELAS l'exige | État actuel | Action |
|---|---|---|---|
| **Substitution parts → actions** (vocabulaire capital) | SELAS = actions, jamais parts sociales | `statuts_sel_exercice_common` gère déjà `title_type="actions"` ; MAIS `domain/models.py` `Associe.nb_parts` / `CapitalContext.nb_parts_total` restent nommés « parts » | adapter le modèle de capital pour porter « actions » proprement (champs neutres `nombre_titres` existent déjà côté `CapitalContext` étendu) |
| **Substitution gérant → président** (rôle dirigeant) | SELAS = président | `DirigeantNomine.fonction_affichage` paramétrable (défaut « gérant ») ; rôle `ACTIONNAIRE` ajouté côté `recup-codex` | brancher `fonction_affichage="Président"` + accord genre Présidente |
| **Couche multi « LES SOUSSIGNÉS »** (comparution N blocs + accord genre/nombre) | Reynaud = comparution multi-associés | **EN CONSTRUCTION sur la session SELARL** (couche SEL partagée) : `selarl_slice.py` porte déjà `additional_associes`, `multi_associes_doc004_limited`, validations multi ; contrat `TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md` existe | SELAS **réutilise** cette couche, **sans la toucher** depuis la session SELAS (coordination, pas parallèle aveugle) |
| **Répartition numérotée** (apports N lignes + tableau répartition + signatures N) | 4 ancrages Reynaud (comparution, apports art.7, répartition art.8, signatures) | partiellement présent côté SELARL multi | réutiliser les ancrages SELARL ; ajouter garde-fou « majorité droits de vote aux exerçants » (dépend Q-C Rafael) |
| **PV d'AG** (décisions collectives multi) | SELAS pluripersonnelle → PV assemblée vs décision associé unique | générateurs PV existants (gérant) ; pas de PV président SELAS multi | spec PV/décision président SELAS (dépend nomination dans statuts vs acte séparé) |
| **Personne morale associée** | Reynaud : 1 associé = Société Civile | `Associe` (models.py) = personne physique uniquement (pas de `forme_pm`/`rcs`/`representant`) | **gap socle** : ajouter le support personne morale dans le modèle associé — dépend Q-C Rafael |
| **Couche genre** (paires, jamais regex) | Présidente, Associé(e)(s), Né(e), accords par associé | helpers `utils/grammar` existants côté SELARL | réutiliser ; assouplir garde-fou anti-régression « associé » |
| **Registre** (catalogue documentaire) | DOC-018 SELAS + futurs docs multi | `registry/catalog.py` porte DOC-018 (`TESTE`) ; `case_catalog.py` modélise toutes les occurrences SELAS | étendre pour le pack multi |
| **Slice front + déroulante auto-extensible** | saisie N associés (2-5) | front prod `front_app/` = SELARL-only ; `selas_schema.py` (socle SELAS front/data) est sur `recup-codex`, PAS branché dans le front Streamlit | construire la slice SELAS dans `front_app/` (réutiliser le pattern `selarl_slice.py` + déroulante `additional_associes`) ; le `selas_schema.py` fournit le contrat data |

**Synthèse socle** : l'essentiel de la couche multi est en cours côté **SELARL** (couche SEL partagée).
SELAS doit **réutiliser sans dupliquer**. Deux vrais gaps socle propres à SELAS : (1) **personne morale associée**
dans le modèle `Associe` ; (2) **slice front Streamlit SELAS** (le socle data `selas_schema.py` existe mais
n'est pas câblé à une UI). Le reste = paramétrage/branchement de briques existantes.

---

## 7. Bloquants de build (décisions de scope, modèles manquants, canon ambigu)

| # | Bloquant | Type | Qui tranche | Réversible ? |
|---|---|---|---|---|
| 1 | Réconciliation `recup-codex` → `main` (cherry-pick SELAS vs merge ; recup-codex régresse le canon SELARL) | technique | Second (toi) | oui — sur branche |
| 2 | Cible produit = multi-associés 2-5 (l'unipersonnel V1 codé devient socle, pas livrable) | scope produit | déjà tranché Gad 2026-06-05 | n/a |
| 3 | Génération SELAS = NO-GO tant que Rafael n'a pas validé les points juridiques (Q-B/C/D + a/b/c/d + filiation/titre/PV) | métier/juridique | Rafael via Gad | n/a |
| 4 | Modèle statuts SELAS dentiste : source DOCX absente | source manquante | à fournir (Rafael/Gad) puis tokeniser | oui |
| 5 | Attestation dépôt capital SELAS : document canonique exact non identifié | source/canon ambigu | identifier source puis tokeniser | oui |
| 6 | Trame multi 2/3/4/5 : Reynaud = 1 seul exemple (Q-D) ; manque variantes | source/représentativité | Rafael via Gad | oui |
| 7 | Support **personne morale associée** absent du modèle `Associe` | technique (dépend Q-C) | Second, après Q-C | oui — sur branche |
| 8 | Incohérence DOC-006 (codé mais marqué « réserve » dans la matrice) ; libellé DOC-002 (« autorisation » vs « attestation ») ; CRLF mixte `procuration.py` ; doublons macOS `.DS_Store`/dossiers `…2`/`…3` dans artefacts | hygiène technique | Second | oui |
| 9 | Tokeniser le Reynaud sans jamais versionner le `.docx` réel (données patiente réelles) | discipline données | Second | oui |

**Ce qui est constructible MAINTENANT, sans GO Rafael (sur branche dédiée, réversible)** :
- réconciliation propre du butin SELAS, hygiène (CRLF, doublons, libellés, incohérence DOC-006) ;
- tokenisation du Reynaud → modèle tokenisé versionné + extraction des blocs ;
- branchement de la slice front Streamlit SELAS (réutilisation `selarl_slice` + `selas_schema`) en mode
  cadrage (génération désactivée, `SELAS_FRONT_SCHEMA_GENERATION_ENABLED = False`) ;
- ajout du support personne morale au modèle, derrière garde-fou (si Q-C va dans ce sens).

**Ce qui reste NO-GO tant que Rafael n'a pas tranché** : activer la **génération** des statuts multi
(wording, accords, DG, personne morale, garde-fou majorité exerçants), et tout **merge sur `main`**.

---

## Pointeurs de fichiers (chemins absolus)
- Branche butin : `origin/naomie/selas/recup-codex`
- Journal NotebookLM (rempli) : `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` (sur recup-codex)
- Matrice : `docs/sprints/SPRINT_SELAS_MATRIX_001.md`
- Roadmap A→P : `docs/sprints/SPRINT_SELAS_ROADMAP_TO_COMPLETION_001.md`
- Contrat front : `docs/sprints/SPRINT_SELAS_FRONT_CONTRACT_001.md`
- Cartographie Reynaud : `docs/sprints/SPRINT_SELAS_MULTI_CARTOGRAPHIE_REYNAUD_001.md`
- Reprise multi-associés (décision Gad) : `docs/sprints/SPRINT_SELAS_REPRISE_MULTI_ASSOCIES_001.md`
- Pack Rafael : `naomie/worklog/PACK_PASSATION_NOTEBOOKLM_SELAS_2026-06-05.md`
- Audit butin : `naomie/worklog/AUDIT_SELAS_BUTIN_4b0c106_2026-06-04.md`
- Socle data SELAS : `src/sydel_doc_engine/front_data/selas_schema.py` (recup-codex)
- Générateur statuts SELAS : `src/sydel_doc_engine/generators/lot_04/statuts_selas_medecin.py`
- Couche from-scratch : `src/sydel_doc_engine/rendering/docx_builder.py`, `generators/lot_04/statuts_sel_exercice_common.py` + `_templates.py`
- Modèle multi SELARL (socle partagé) : `src/sydel_doc_engine/front_app/selarl_slice.py`, `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md`
- Modèles source à rapatrier : `C:/Users/Gad/Downloads/Statuts SELAS DU DR ISABELLE REYNAUD.docx`, `C:/Users/Gad/Downloads/modele Statuts SELAS avec MH.docx`
