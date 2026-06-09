# Itinéraire d'implémentation — Lot post-réunion 2026-06-09

> Auteur : Nami (technical-planner). Carte d'implémentation. AUCUN code modifié ici.
> Branche cible : `sprint/engine-completion` (clone `sydel-document-engine-claude`).
> Cadrage source : `_CADRAGE_LOT_REUNION_2026-06-09.md`. Ordre imposé : A2 → A1 → A3 → A4.
> Hors lot : A5 (base de personnes) = ticket dédié séparé. B (wording DG/DG délégué, etc.) = FLAG Rafael.

---

## 0. État vérifié de l'existant (lu dans le code)

- Repeater civils (SCI/SCI IRIS/SCS/SCM) : `associe_repeater.py:69-90`, `RepeaterConfig.nb_max=6`
  (`:43`), `nb_min` réglé par type au call site `civil_statuts_slice.py:173-183`
  (`nb_min=1` pour SCI/SCM, `2` pour SCI IRIS/SCS).
- Repeater SELAS : NON partagé — slice maison `selas_multi_slice.py:252-269`, borné `2..5`
  (`_associe_count` `:95-100`).
- Générateurs : itération réelle `for associe in data.associes` — civils `statuts_civils_common.py`
  (cadrage `:80-82`), SELAS `statuts_selas_multi.py:213/278/305/339`.
- Président SELAS : résolu par `ref_associe_index` sinon `physiques[0]`
  (`statuts_selas_multi.py:373-403`). Côté front, l'index est forcé au 1er physique
  (`selas_multi_slice.py:539-543`, puis `:650`, `:682`).
- SAS : actionnaire unique, président = `ref_associe_index=0` figé (`sas_slice.py:429`).
- DNC/filiation : collectée pour un **signataire unique implicite** — civils
  `civil_statuts_slice.py:212-246` (`_render_common_docs_form`), SELAS
  `selas_multi_slice.py:167-214` (`_render_common_docs_form`). Le signataire = 1er physique
  (`civil_statuts_slice.py:511-518` `_signataire_associe`).
- Modèle de données déjà prêt : `StatutsSelasMultiPresident.ref_associe_index`
  (`models.py:714`), `StatutsPresident.ref_associe_index` (`models.py:457`),
  `DirigeantNomine.fonction_affichage` + `ref_associe_index` (`models.py:824-825`).
- Tests : `tests/unit/test_multi_type_front.py` — fixtures **à 2 associés** partout
  (`_civil_base`, `_selas_payload`). Prefill UI SELAS = 2 associés (`shell.py:642-695`).

---

## 1. A2 — Preuve multi-N (3 et 5 associés) — PRIORITAIRE

**Nature : VÉRIFICATION par test. Aucun code applicatif touché.** On prouve que le socle
déjà câblé tient à 3 et 5. Si un test casse → on a trouvé un vrai bug ; on STOP et on remonte
avant de « corriger » (pas d'invention).

### 1.1 Tests générateurs/plan (niveau `build_*_plan` + `generate_dossier`)
Fichier : `tests/unit/test_multi_type_front.py` (mêmes helpers `_pp`/`_pm`/`_civil_base`/`_selas_payload`).

Helper à ajouter (factorise N associés en gardant somme parts = total / somme actions = total) :
- `_split_parts(n, total)` → renvoie liste `(nb, debut, fin)` couvrant `1..total` sans trou.
- `_split_actions(n, total)` → idem pour les actions SELAS.

Tests civils à 3 associés (somme parts = `nb_parts_total`, somme apports = `capital_social`) :
- `test_sci_three_associes_generates_clean` — SCI, 3×PP, parts 100, capital 1000.
  Asserts : `plan.can_generate is True` ; `plan.document_codes == ("DOC-020","DOC-001","DOC-002","DOC-003","DOC-004")` ;
  `_assert_bundle_clean(... {"statuts_sci.docx"})` ; les 3 noms (`Durand`/`Martin`/`Petit`)
  présents dans le texte des `statuts_sci.docx` ; texte du `pv_nomination_gerant.docx` liste les 3.
- `test_scs_three_associes_generates_clean` — SCS, ≥1 `commandite` + ≥1 `commanditaire` parmi 3
  (sinon le validateur `civil_statuts_slice.py:434-437` bloque). Asserts identiques + présence des 3.
- `test_sci_iris_three_associes_generates_clean` — SCI IRIS, 1×PM + 2×PP (contrainte
  `:392-395` : ≥1 morale). Asserts : groupes de résultat IRIS produits sans `[`/`]`
  (`_apply_iris_result_groups` `:858-877` itère sur N — le prouver à 3).

Tests civils à 5 associés :
- `test_sci_five_associes_generates_clean` — SCI, 5×PP, parts/apports cohérents, 5 noms présents.
- (SCM volontairement ABSENT à 3/5 — voir §1.3.)

Tests SELAS multi à 3 et 5 (borne moteur = 5) :
- `test_selas_three_associes_generates_clean` — 3 associés (≥1 PP exerçante), somme actions = total.
  Asserts : `plan.can_generate is True` ; `document_codes == ("DOC-044","DOC-001","DOC-002","DOC-003","DOC-004","DOC-034")` ;
  bundle clean ; les 3 comparutions présentes dans `statuts_selas_multi.docx`.
- `test_selas_five_associes_generates_clean` — 5 associés (borne max). Mêmes asserts.
  Note : ne PAS dépasser 5 (le générateur lève `statuts_selas_multi.py:354-357`).

### 1.2 Test front AppTest multi-N (preuve UI bout-en-bout)
Calqué sur `test_front_routes_to_sci_slice_and_generates` (`:794-897`). Le repeater civil ajoute
un associé via le bouton `key="{prefix}_add"` (`associe_repeater.py:77`). Procédure :
- `test_front_sci_three_associes_generates` :
  1. sélectionner « SCI creation V1 », `app.run`.
  2. cliquer le bouton `sci_add` une fois (2→3) : `next(b for b in app.button if str(b.key)=="sci_add").click()` ; `app.run`.
  3. remplir société + les **3** blocs associés (clés `sci_associe_0_*`, `_1_*`, `_2_*` ;
     champs : `prenom/nom/date_naissance/ville_naissance/departement_naissance/nationalite/
     situation_maritale/profession/adresse/apport_montant` en texte ; `nb_titres/parts_debut/
     parts_fin` en number) + `sci_nb_parts_total`. Sommes cohérentes.
  4. vérifier `generate_button.disabled is False` et aucun caption « Blocage », puis générer ;
     `"Telecharger statuts_sci.docx"` et le ZIP dans les `download_button`.
- `test_front_selas_three_associes_generates` : idem avec bouton `selas_add`, clés `selas_associe_*`
  (champs SELAS : `nb_actions/montant/civilite/prenoms/nom/date_naissance/ville_naissance/
  departement/nationalite/profession/adresse/situation/qualification/ordre_dep/numero_ordre/
  numero_rpps/qualite` cf. `selas_multi_slice.py:283-315`) + champs société + `_render_common_docs_form`.

> Garde live-DB : ces tests AppTest n'ouvrent AUCUNE connexion DB (génération DOCX en `tmp_path`,
> `monkeypatch` de `shell.ARTIFACTS_DIR`). Sûrs en session live.

### 1.3 Ce que A2 NE doit PAS prouver (le borner explicitement dans le test)
- **SCM à 3/5** : les satellites (DOC-026 pacte, DOC-030 liste dépenses) sont **verrouillés à
  exactement 2** (`civil_statuts_slice.py:99-104` `_scm_satellites_pair_active`). Ajouter un test
  de **non-régression du verrou** : `test_scm_three_associes_drops_satellites` → SCM à 3 associés,
  assert `"DOC-026" not in plan.document_codes and "DOC-030" not in plan.document_codes`
  (le bundle de base reste généré proprement). NE PAS tester une SCM 3/5 « complète » → FLAG Rafael.

**Sortie A2 :** si tout est vert → le socle multi-N est prouvé, on enchaîne. Si rouge → bug réel
détecté, STOP + remontée (ne pas patcher le générateur sans cadrage).

---

## 2. A1 — Harmoniser bornes / UX du repeater par type — LÉGER

Objectif : cohérence des bornes et libellés, **zéro changement de comportement de génération**.

Fichiers :
- `civil_statuts_slice.py:173-183` : les `nb_min` sont déjà fixés par type. Harmonisation =
  rendre la borne **explicite et nommée** (constante `CIVIL_NB_MIN_BY_STRUCTURE`) plutôt
  qu'un ternaire en ligne, et passer un libellé de caption par type. SCI IRIS reste `nb_min=2`,
  SCS reste `nb_min=2` (≥1 commandité + ≥1 commanditaire — sinon validateur `:434-437`).
- `associe_repeater.py:83-85` : la caption générique « Entre {min} et {max} associes » suffit ;
  option : injecter un libellé d'unité déjà présent (`config.titre_unite`). Pas de refonte.
- `selas_multi_slice.py:95-100` + `:256` : borne `2..5` dédiée. Harmonisation = remplacer les
  littéraux `2`/`5` par des constantes nommées `SELAS_NB_MIN=2` / `SELAS_NB_MAX=5` **alignées
  sur** le générateur (`statuts_selas_multi.py` `MIN_ASSOCIES`/`MAX_ASSOCIES` — à importer ou
  dupliquer en commentaire référencé). Le caption `:264` (« 1er physique = président par défaut »)
  sera **modifié par A3** — ne pas le réécrire ici, juste le laisser.

Tests A1 (légers, sur le plan, pas de génération) :
- `test_selas_repeater_bounds` : `_associe_count` clamp `1→2` et `9→5`.
- `test_civil_repeater_nb_min_by_structure` : pour chaque structure, le `RepeaterConfig.nb_min`
  passé correspond à la table attendue (SCI=1, SCM=1, SCI IRIS=2, SCS=2).

Risque A1 : changer un `nb_min` casserait une fixture. → ne PAS changer les valeurs, seulement
les **nommer**. Les tests A2 (qui partent à 2) restent verts.

---

## 3. A3 — UI sélection du dirigeant — DÉBLOQUE A4

Le modèle de données sait déjà pointer n'importe quel associé (`ref_associe_index`,
`models.py:457/714/825`). Il manque l'UI pour **choisir** + le câblage front→contexte.

### 3.1 SELAS (`selas_multi_slice.py`)
- **UI — case dirigeant + rôle, dans `_render_one_associe` (`:272-289`)** : pour chaque associé
  **personne physique uniquement** (le président SELAS doit être PP, contrainte moteur
  `statuts_selas_multi.py:387-391`), ajouter :
  - `st.checkbox("Dirigeant", key=f"{prefix}_is_dirigeant")` ;
  - `st.selectbox("Rôle", ("Président",), key=f"{prefix}_role_dirigeant")` — **liste limitée à
    « Président »** tant que Rafael n'a pas livré le wording DG / DG délégué (voir §5). Ne PAS
    proposer DG/DG délégué dans le selectbox (sinon on promettrait une clause inexistante).
- **Collecte de l'index choisi** : dans `_render_selas_associes` (`:252-269`), après la boucle,
  dériver `president_index` = premier index dont `st.session_state[f"{PREFIX}_associe_{i}_is_dirigeant"]`
  est vrai ET associé PP ; défaut = 1er physique (comportement actuel, `:539-543`). Stocker dans le
  payload : `payload["president_index"]` (nouvelle clé), renvoyée par `render_selas_form`.
- **Passage au générateur** : dans `build_generation_context` (`:537`), remplacer le calcul forcé
  `president_index = next(... PP ..., 0)` (`:539-542`) par la lecture de `payload["president_index"]`
  (fallback = même `next(...)`). Cet index alimente déjà `DirigeantNomine.ref_associe_index` (`:650`),
  `StatutsSelasMultiPresident(ref_associe_index=...)` (`:682`) et le bloc `ReunionPresident` (`:657-664`).
  → un seul point d'injection, le reste suit.
- **Caption** `:264` : remplacer « 1er physique = président par défaut » par « Cochez le dirigeant ;
  à défaut, le 1er associé physique est président ».

### 3.2 SAS (`sas_slice.py`)
- SAS V1 = **actionnaire unique** (`dossier_options associe_unique=True`, `:371`). Il n'y a qu'un
  associé → **pas de sélecteur pertinent**. A3 sur SAS = **no-op fonctionnel**.
  Action : NE PAS ajouter de case dirigeant SAS dans ce lot. Laisser `ref_associe_index=0` (`:429`).
  Le tracer comme tel dans le plan pour éviter une fausse attente. (Le multi-associé SAS sort du
  périmètre V1.)

### 3.3 Stockage session_state — convention
Clés par associé, alignées sur le préfixe existant : `f"{prefix}_is_dirigeant"` (bool),
`f"{prefix}_role_dirigeant"` (str). Aucune clé globale mutable → compatible reruns Streamlit
(le repeater seed déjà ses clés, `associe_repeater.py:64-66` / `selas_multi_slice.py:276-277`).

### 3.4 Tests A3
- `test_selas_president_defaults_to_first_physique` : payload sans `president_index` → contexte
  pointe l'index du 1er PP (non-régression du défaut actuel).
- `test_selas_president_selectable` : payload `president_index=2` (un PP en 3e position) →
  `ctx.dirigeant_nomine.ref_associe_index == 2`, `ctx.statuts_selas_multi.president.ref_associe_index == 2`,
  et le PV/comparutions nomment ce dirigeant. Génération clean.
- `test_selas_president_must_be_physique` : si l'index pointé est une PM → la génération lève
  (déjà géré moteur `statuts_selas_multi.py:387-391`) ; prouver que le front retombe sur le 1er PP
  OU bloque proprement (au choix d'implémentation — défaut recommandé : retomber sur 1er PP, ne
  jamais générer un dirigeant moral).
- Test AppTest : cocher `selas_associe_1_is_dirigeant` et vérifier que le dossier généré nomme
  bien le 2e associé comme président.

---

## 4. A4 — Champs dirigeant conditionnels — MÉCANIQUE constructible, RÈGLE = FLAG Rafael

Aujourd'hui DNC + filiation (nom père/mère, adresse structurée, date naissance) sont collectés
pour un **signataire unique** : `_render_common_docs_form` (civils `:212-246`, SELAS `:167-214`).

**DÉFAUT DOCUMENTÉ retenu (cadrage §3, en attente Rafael §7) : conditionner la collecte des
champs lourds sur « associé coché dirigeant ».** Si Rafael tranche « tout associé », on élargira
la condition — c'est un paramètre, pas une refonte.

### 4.1 Mécanique (SELAS, le cas qui porte la DNC)
- Aujourd'hui les champs DNC sont saisis dans un bloc « Président / signataire » **séparé** des
  associés (`selas_multi_slice.py:167-214`), et le contexte signataire est bâti depuis ces champs
  `payload["signataire_*"]` (`:553-587`). Le `signataire_associe` (identité, ville naissance) vient
  déjà de l'associé président (`:539-543`).
- **Changement A4 (mécanique)** : déplacer la **collecte conditionnelle** des champs DNC/filiation
  **dans le bloc associé**, rendu UNIQUEMENT si `f"{prefix}_is_dirigeant"` est coché. Concrètement :
  - dans `_render_one_associe` (`:272-289`), après la case « Dirigeant » (A3), si cochée, afficher
    un sous-bloc : nom père, nom mère, adresse structurée (num/voie/cp/ville), nationalité, date
    de naissance ISO — les champs aujourd'hui dans `_render_common_docs_form` (`:171-204`).
  - `build_generation_context` lit ces champs **depuis l'associé dirigeant** (via `president_index`)
    au lieu de `payload["signataire_*"]` globaux. Mapping inchangé en aval (`Person`, `DirigeantNomine`).
- **Compat mono-associé / non-régression** : conserver `_render_common_docs_form` comme **fallback**
  tant que la migration n'est pas totale. Règle de lecture : si l'associé dirigeant porte les champs
  DNC → les utiliser ; sinon retomber sur `payload["signataire_*"]`. Ainsi les fixtures existantes
  (qui remplissent `signataire_*`) restent vertes. **C'est le point de rupture n°1 — voir §6.**
- **Validation** : `_validate_common_docs` (`:499-526`) doit cibler les champs **du dirigeant
  coché** quand ils existent, sinon les `signataire_*`. Ne pas exiger DNC pour les associés
  non-dirigeants (c'est précisément l'objectif A4).

### 4.2 Civils (SCI/SCM/…)
Même principe mais : les types civils ont un **gérant** signataire (1er physique,
`civil_statuts_slice.py:511-518`). A4 civils = optionnel pour ce lot ; si embarqué, appliquer la
**même mécanique** (case dirigeant/gérant → champs DNC conditionnels) avec le même fallback
`signataire_*`. Recommandation : faire SELAS d'abord (porte la DNC explicite), civils ensuite si
le temps le permet, sinon les laisser sur le bloc signataire actuel (pas de régression).

### 4.3 Tests A4
- `test_selas_dnc_collected_for_dirigeant_only` : 3 associés, seul l'index dirigeant porte
  nom père/mère → génération clean, DNC nomme le bon dirigeant ; les non-dirigeants n'exigent pas
  ces champs (plan `can_generate is True` sans les remplir pour eux).
- `test_selas_dnc_fallback_signataire_fields` : payload « ancien style » (`signataire_*` remplis,
  pas de champs portés par l'associé) → toujours vert (non-régression).
- `test_selas_mono_dirigeant_unchanged` : 2 associés, 1 dirigeant → bundle et DNC identiques à
  l'attendu actuel (`document_codes` inchangés, DOCX clean).

### 4.4 FLAG Rafael (bloquant pour fermer A4, pas pour le construire)
La **règle de déclenchement** (DNC = dirigeant seul vs tout associé) reste à confirmer
(`_RAFAEL_PACKET_V1.md` §7). Construire avec le défaut « dirigeant coché », laisser un point ouvert.

---

## 5. Ce qui reste FLAG Rafael (NE PAS construire dans ce lot)

Déjà tracé dans `_RAFAEL_PACKET_V1.md` (le re-pointer, ne pas dupliquer la décision) :
- §6 — **wording DG / DG délégué** : aucun modèle source ne le porte. A3 limite le selectbox de
  rôle à « Président ». Ne rien rédiger. (Cadrage §B, §3 pièges de fidélité.)
- §7 — **DNC : dirigeant seul vs tout associé** : paramètre de A4 (défaut « dirigeant coché »).
- §1 — **satellites SCM ≠ 2 associés** : verrou conservé (A2 §1.3 prouve la non-régression).
- §3 — **clauses « parts sociales » / « gérant »** dans modèles SAS/SELAS en actions : fidélité,
  NE PAS corriger (décision Rafael). Aucune étape de ce plan ne les touche.
- §4/§5/§8 — intérêts de retard, clauses de cession, variables mal injectées : hors lot.

A5 (base de personnes) : ticket dédié séparé, hors de ce lot.

---

## 6. Points de rupture potentiels + couverture

| # | Risque | Où | Couverture |
| :- | :- | :- | :- |
| 1 | A4 casse le **mono-associé / signataire actuel** en déplaçant la DNC dans l'associé | `selas_multi_slice.py:167-214` + `:553-587` | **Fallback obligatoire** vers `payload["signataire_*"]` ; test `test_selas_dnc_fallback_signataire_fields` + `test_selas_mono_dirigeant_unchanged` |
| 2 | A3 change le président par défaut et **régresse le défaut 1er-physique** | `selas_multi_slice.py:539-543` → lecture `president_index` | `test_selas_president_defaults_to_first_physique` (payload sans index) |
| 3 | Index dirigeant pointe une **personne morale** → génération lève | `statuts_selas_multi.py:387-391` | `test_selas_president_must_be_physique` ; défaut = retomber sur 1er PP |
| 4 | A1 modifie un `nb_min` et **casse une fixture à 2** | `civil_statuts_slice.py:173-183` | Ne changer que les **noms** (constantes), pas les valeurs ; A2 (fixtures à 2) reste vert |
| 5 | Test multi-N à 6 (civils) ou >5 (SELAS) **dépasse la borne moteur** | `statuts_selas_multi.py:354-357` ; `MAX_ASSOCIES=6` civils | Tests bornés à 5 (SELAS) / 5 (civils) ; clamp prouvé par `test_selas_repeater_bounds` |
| 6 | SCM à N **génère des satellites cassés** (modèles à 2) | `civil_statuts_slice.py:99-104` | `test_scm_three_associes_drops_satellites` (verrou conservé) |
| 7 | **SELARL (référence)** régressé par effet de bord | chemin SELARL historique (`slice_module is None`, test `:69-75`) | SELARL n'est PAS touché par ce lot (slices typés séparés) ; `test_selarl_option_unchanged` + `test_registry_exposes_all_ready_types` restent verts |
| 8 | SAS : ajout d'un sélecteur dirigeant non pertinent (actionnaire unique) | `sas_slice.py` | A3 = **no-op SAS** documenté §3.2 ; aucun changement SAS |

**Garantie non-régression SELARL :** ne modifier AUCUN fichier du chemin SELARL ni
`common_creation.py` de façon comportementale (A1 ne fait que nommer des constantes). Lancer la
suite unit complète (périmètre nommé ci-dessous) avant tout push.

---

## 7. Commande de test exacte (Windows, périmètre ciblé)

Périmètre touché = `tests/unit/test_multi_type_front.py` (A2/A3/A4) + tests générateurs SELAS/civils
si A2 révèle un besoin. Trap Windows connu : `--basetemp`.

Périmètre lot (rapide, à itérer pendant le build) :

```
python -m pytest tests/unit/test_multi_type_front.py --basetemp=artifacts/_audit_tmp/pt -q
```

Avant push (non-régression unit complète, hors intégration/DB — sûr en session live) :

```
python -m pytest tests/unit --basetemp=artifacts/_audit_tmp/pt -q
```

- Lancer depuis la racine du clone `sydel-document-engine-claude` (chemins relatifs des fixtures
  AppTest : `AppTest.from_file("src/sydel_doc_engine/front_app/app.py")`).
- **NE PAS** lancer `pytest` global non filtré ni `tests/integration` en session live (garde
  base partagée) — les tests ci-dessus génèrent du DOCX en `tmp_path`, aucune DB.
- Annoncer le résultat en **nommant le périmètre** (« X verts sur `tests/unit` — intégration non
  relancée »), jamais « tout vert » sur un sous-ensemble.

---

## 8. Ordre d'exécution récapitulé

1. **A2** — écrire tests 3/5 associés (générateurs + AppTest) + test verrou satellites SCM.
   Vert → socle prouvé. Rouge → STOP + remontée (bug réel, pas d'invention).
2. **A1** — nommer les bornes (constantes civils + SELAS), libellés ; tests bornes. Zéro changement
   de valeur.
3. **A3** — case « Dirigeant » + rôle (« Président » seul) par associé PP SELAS ; `president_index`
   payload → `build_generation_context`. SAS = no-op. Tests sélecteur + défaut.
4. **A4** — DNC/filiation conditionnelle par dirigeant coché (SELAS) avec **fallback signataire_*** ;
   validation ciblée. Tests fallback + mono-associé. Défaut documenté ; règle finale = FLAG Rafael §7.

Chaque étape : commit local (gratuit), un seul push groupé en fin de lot (économie CI).
