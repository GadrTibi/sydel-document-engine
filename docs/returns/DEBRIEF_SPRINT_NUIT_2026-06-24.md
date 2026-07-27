# Debrief — sprint de nuit Akainu (23→24 juin 2026)

> Pour Gad, au réveil. Honnête, non complaisant. Vue courte d'abord, preuves ensuite.
> Branche de travail : worktree `feat/propagation-q4-adresses` (29 commits depuis `e609105`).
> ⚠️ RIEN poussé sur `main`. RIEN mergé sans ton GO.

---

## 1. TL;DR

Parti de l'état du 23-06 17:48 où un **sweep Akainu avait ré-ouvert 10 retours** (verdict
`AKAINU_VERDICT_2026-06-23.md` : **8 BLOQUANT + 16 MAJEUR** + 18 mineur + 18 nitpick). Mes
« traité » d'avant étaient **faux sur DOCX régénérés** — la machine produisait encore les
défauts. La nuit a servi à **re-corriger à la racine**, avec une boucle `fix → re-Akainu`
jusqu'à `RIEN À REDIRE`, en régénérant de vrais DOCX à chaque tour.

**Résultat au matin :**
- Suite : **594 tests verts**, ruff propre, **ordre-indépendance PROUVÉE** (ordres de collecte
  distincts via `pytest-randomly` — fini le faux-vert « N runs à ordre constant »).
- Les **8 BLOQUANT + 16 MAJEUR re-vérifiés un par un** ce matin : aucun non corrigé trouvé
  (détail § 3).
- **Gate de convergence (Akainu tour 10) : CONVERGENCE = OUI** (zéro BLOQUANT, zéro MAJEUR).
  Produit sain, lot retours intact, cession SELAS + golden-blocs + gold STATUTS reconfirmés
  par **régénération réelle**. Tour 10 a tout de même attrapé **2 MINEUR sur MA véracité
  chiffrée** (le pin `pytest-randomly` pointait `<4` mais la preuve a tourné sur 4.1.0 ; la
  docstring disait « 593 verts » au lieu de 594) — **corrigés + re-vérifiés** (commit `350c16f`),
  dernier run **594 verts** en ordre randomisé. C'est la **5ᵉ fois** que le gate attrape ce
  travers de sur-affirmation chiffrée chez moi : la leçon est prise (§ 4).
- **Le lot retours est donc TRAITÉ** (≠ VALIDÉ — toi/Rafael restez le juge final).

```
┌─ SYDEL · SPRINT DE NUIT — état au réveil ──────────────────────────────────
│
│   CORRIGÉ (code)    [████████████████████████]  19/21 · 90%   (reste O24-04, +L5/L6 clarif)
│   CONTRÔLE AKAINU   [██████████████████████░░]  ~19/21        (tour 10 = gate final)
│   VALIDÉ  (Rafael)  [░░░░░░░░░░░░░░░░░░░░░░░░]   0/21 ·  0%    ⚠ rien validé (normal)
│   gate : CORRIGÉ ≥ AKAINU ≥ VALIDÉ — Rafael est le juge final, pas moi
└────────────────────────────────────────────────────────────────────────────
```

---

## 2. Le parcours (29 commits, tours 1→9)

| Tour | Ce qu'Akainu a cassé (vrai bug document) | Fix racine |
|---|---|---|
| reopening | 10 retours ré-ouverts : mes « traité » étaient des garde-fous UI, pas des fixes — DOCX régénérés montraient encore les défauts | (point de départ) |
| T1-T3 | O24-03 adresses sur 1 ligne **non propagées** hors SELAS ; O24-05 capital indivisible (valeur nominale `3,3333 €`) ; O24-11 régime matrimonial perdu dans l'acte SCM ; LIVE-03 mois non accentués (`aout`, `decembre`) | **golden-bloc `address_oneline`** branché sur tous les types ; garde divisibilité capital ; helper d'accentuation des mois ; régime ré-accentué |
| T4-T5 | O24-12 saisie du cabinet **perdue** quand on coche « même adresse » ; O24-14 compromis qui **levait** sur champs partagés avec l'acte | **RE-SCOPE (règle 12)** : `manual_key` qui préserve la saisie ; le compromis tolère les champs d'acte partagés |
| T6 | O24-05 flakiness ~20 % sur le renommage des lettres de régime | `_rename_with_slug` rendu **idempotent** |
| T7 | Cession **SELAS qui ne se générait pas du tout** (`document est obligatoire` → crash ; SCM `variante_structure` ≠ `'selas'` → non-émission silencieuse) ; bundle ZIP qui plantait sous course FS | **câblage contexte SELAS** (TACHE A) ; retry FS borné dans `zip_bundle` |
| T8 | Acte médical figé sur le littéral « SELARL au capital de » → un acquéreur **SELAS affichait SELARL** ; flakiness racine (`random` global non seedé) | override token `[forme_sociale_acquereur]` (gold SELARL byte-identique) ; **`random.seed(0)` par test** |
| T9 | Mes propres **sur-affirmations** : « racine prouvée » (non reproduite en contrôle négatif), « gold line-by-line intact » (le test n'existait pas pour l'acte de cession), méthodo flakiness (« N runs à ordre constant » ne prouve rien) | `pytest-randomly` (ordre-indép. **réellement** prouvée, 4 ordres) ; wording requalifié honnêtement ; **test SELARL symétrique** ajouté (verrouille le claim byte-identique) ; nitpicks tracés |

**Lecture clé :** la boucle adversariale a **attrapé mes propres dérives** plusieurs fois
(extrapolations « numéro optionnel » / « PACS » que j'avais inventées → reculées au verbatim
exact ; sur-affirmations × 3-4). Le gate fonctionne **contre moi**, c'est sa valeur.

---

## 3. Vérification contre les sources de vérité (réponse à « as-tu halluciné ? »)

Tu avais raison de t'inquiéter. Voici **où et comment** j'ai confronté mon travail au réel
cette session (pas de mémoire, du regénéré) :

| Source de vérité | Ce que j'ai vérifié | Résultat |
|---|---|---|
| **Verbatim client** (`CARNET.md`) | chaque fix relu contre le mot exact du client, pas ma paraphrase | les fixes collent au verbatim ; mes 2 extrapolations passées (numéro optionnel, PACS) avaient été reculées |
| **Verdict Akainu 23-06** (8 BLOQ + 16 MAJ) | re-vérifié **les 24 défauts bloquant/majeur un par un** ce matin | tous couverts : O24-01 régen-propre · O24-07/10/LIVE-02 tests verts · O24-03/05/11/12/14/LIVE-03 commits + tour 10 |
| **DOCX régénérés** (O24-01) | régénéré SELAS-multi + SCI + SCI-IRIS + SCS cette session, scan des 2 chaînes interdites | **PURGÉ** sur les 4 (par `annexe_filter`, golden-bloc) |
| **Gold STATUTS** (`*_matches_source_docx_line_by_line`) | les changements front-only ne doivent pas toucher la sortie générateur | suite verte (tour 10 reconfirme) |
| **Ordre-indépendance** | suite sur 4 ordres de collecte distincts (`pytest-randomly` seeds 1/2/3 + défaut) | **594 verts × 4 ordres** |

**Désync documentaire trouvé** (à corriger, pas un bug produit) : `CARNET.md` ligne 47 et
`DASHBOARD.md` datent du 23-06 17:48 (avant les fixes de nuit) → ils listent encore des items
comme « ré-ouverts » alors qu'ils sont corrigés. **Synchronisation des registres = action de
clôture** (cf. § 6).

---

## 4. Auto-critique honnête (ce que je dois améliorer)

1. **Pattern de sur-affirmation (récurrent, constaté ~6× sur le sprint).** Ma faute la plus
   coûteuse : servir un fait/chiffre/preuve non re-vérifié — « racine prouvée », « gold intact »,
   « 593 verts » (réel 594), pin `pytest-randomly<4` (testé sur 4.1.0), et enfin
   « `sprint/engine-completion` jamais poussé » (FAUX — refspec local restreint à `main`, cf. § 7).
   **Nuance honnête** : les 5 premiers, c'est Akainu qui m'a rattrapé ; le 6ᵉ (staging), je l'ai
   attrapé **moi-même** via la sortie du `git push` — léger progrès, je commence à me reprendre
   avant qu'on me reprenne. **Correctif** : preuves structurelles (`pytest-randomly`), wording
   épistémique honnête, et désormais `git ls-remote` pour tout état distant. Codifié en mémoire
   (`feedback-preuve-avant-affirmation-chiffree`, `project-staging-deploy-channel`).
2. **Surface vs racine.** Mes premiers « traité » étaient des garde-fous UI, pas des fixes
   moteur — invisibles tant qu'on ne régénère pas le DOCX. **Leçon** : un retour n'est traité
   que prouvé sur **DOCX régénéré**, jamais sur la lecture du code.
3. **Méthodologie de preuve.** « 10 runs verts » à ordre constant ne prouvait pas
   l'ordre-indépendance. Il fallait randomiser l'ordre (`pytest-randomly`) — ce que j'aurais dû
   faire d'emblée pour une flakiness.
4. **Tenue des registres en temps réel.** J'ai corrigé sans mettre à jour `CARNET`/`DASHBOARD`
   au fil de l'eau → désync au matin. À l'avenir : synchroniser le registre **à chaque item
   clos**, pas en fin de lot.

---

## 5. État final par retour (TRAITÉ ≠ VALIDÉ — Rafael reste le juge)

| Retour | État | Note |
|---|---|---|
| O24-01 annexe Sydel | TRAITÉ (régen-propre, tous types) | golden-bloc `annexe_filter` |
| O24-02 DNC par dirigeant | TRAITÉ | tranché Rafael (1 DNC/dirigeant) |
| O24-03 adresses 1 ligne | TRAITÉ (propagé tous types) | golden-bloc `address_oneline` |
| **O24-04 icône copier** | **RESTE À FAIRE** | UI, tous types — § 6 |
| O24-05 valeur nominale auto | TRAITÉ | garde divisibilité capital |
| O24-06 pluri = multi | TRAITÉ | |
| O24-07 Président obligatoire | TRAITÉ | tests `zero_president_bloque` / `deux_presidents_bloque` |
| O24-08 date+adresse 1× | TRAITÉ | |
| O24-09 « (profession) » | TRAITÉ | |
| O24-10 menu dentaire/médical dérivé | TRAITÉ | test ligne 3207 |
| O24-11 vendeur = un associé | TRAITÉ | régime + conjoint ; PACS exclu (à confirmer Albane) |
| O24-12 case « même adresse cabinet » | TRAITÉ | saisie préservée (`manual_key`) |
| O24-13 CA non facultatif | TRAITÉ (RIEN À REDIRE dès le verdict) | |
| O24-14 acte + compromis ensemble | TRAITÉ | champs partagés tolérés |
| O24-15 acquéreur retiré | TRAITÉ (RIEN À REDIRE dès le verdict) | |
| LIVE-01 situation = régime SELARL | TRAITÉ | |
| LIVE-02 case régime communautaire | TRAITÉ | code mort supprimé + test négatif |
| LIVE-03 mois accentués | TRAITÉ (règle globale) | |
| LIVE-04 retrait choix étape | TRAITÉ | |
| **LIVE-05 lettre renonciation** | **BLOQUÉ** | mini-screenshot illisible → question Rafael |
| **LIVE-06 « case à la fin »** | **BLOQUÉ** | mini-screenshot illisible → question Rafael |

**VALIDÉ : 0** — normal et voulu (`traité ≠ validé`). Rien ne sort du carnet tant que Rafael
n'a pas retesté `sprint/engine-completion`.

---

## 6. Ce qui reste (et pourquoi)

| # | Sujet | Pourquoi ça reste | Action prévue |
|---|---|---|---|
| O24-04 | icône « copier » par champ | **non shippable à l'aveugle** (voir § 6bis) | ton greenlight + build vérifiable next session |
| L5 / L6 | 2 retours live | **mini-screenshots illisibles** : sens inconnu | **question Rafael** — ne pas deviner (`QUESTIONS_RAFAEL.md`) |
| Sync registres | `CARNET`/`DASHBOARD` stale (23-06 17:48) | corrigés mais registres non mis à jour | synchroniser au statut réel (fait en clôture, voir § 6ter) |
| Dettes Albane | wording figé « Inscription de la SELARL au Tableau » (2 compromis) ; PACS cession ; valeur nominale SPFPL cible ; salarié incomplet | arbitrage **métier** Albane, pas un bug | tracés dans `QUESTIONS_RAFAEL.md` |

### § 6bis — O24-04 (icône copier) : pourquoi je ne l'ai PAS shippé cette nuit

Verbatim client clair (« ajouter une icône copier à côté de chaque champ texte »). Mais en
l'investiguant cette nuit, **4 raisons dures** m'ont fait choisir de te le cadrer plutôt que de
le livrer en aveugle :

1. **Non testable sans déploiement.** Une icône « copier » est du **JS client-side** (clipboard).
   Streamlit `AppTest` (headless, ce qui fait tourner mes 594 tests) **ne peut pas** introspecter
   un bouton de copie (composant tiers en iframe, ou `components.v1.html`). Le livrer = livrer du
   code **invérifiable par la suite** → contraire à tout ce qu'on vient de faire cette nuit.
2. **Pas de point de passage unique.** **70 appels `st.text_input`** dispersés sur ~10 slices,
   **aucun helper central**. Le faire « tous types » = soit migrer 70 sites, soit créer un helper
   partagé et réécrire les 70 appels. Gros chantier transverse, à faire propre, pas à 5h.
3. **Nouvelle dépendance entanglée au déploiement.** Il faut un composant (`st-copy`) ou un hack
   `components.v1.html` → nouvelle dépendance. Or il n'y a **pas de `requirements.txt`** (deps via
   `pyproject`) et **le canal de déploiement n'est pas tranché** (§ 7). Ajouter une dép qui doit
   atteindre le bon environnement avant d'avoir tranché OÙ on déploie = mettre la charrue avant les
   bœufs.
4. **Scope UX = ta décision.** Une icône sur **chaque** champ de **tout** l'app est une décision
   d'agencement (risque d'encombrement). Le CARNET la tague d'ailleurs « décision UI ».

**Ma reco technique (prête à exécuter sur ton GO) :** helper partagé `copyable_text_field(label,
key, …)` qui enrobe `st.text_input` + un bouton de copie via `st.components.v1.html` (zéro dép
tierce, pas de risque Streamlit Cloud). Rollout progressif : d'abord les champs « sortie » (ceux
qu'on recopie vraiment), pas forcément les 70 d'un coup. **Vérification = manuelle sur le staging**
une fois le canal de déploiement tranché. → Dis « go O24-04 » + (champs ciblés ou tous) et je le
fais next session, vérifiable.

### § 6ter — Synchronisation des registres (fait en clôture)

`CARNET.md` / `DASHBOARD.md` dataient du 23-06 17:48 (avant les fixes de nuit) et listaient encore
des items comme « ré-ouverts ». **Synchronisés** au statut réel post-convergence (les 8 BLOQUANT +
16 MAJEUR re-vérifiés OK) — le détail par retour est le § 5 ci-dessus.

---

## 7. Manœuvre exécutée + ce qui reste

1. **Merge** `feat/propagation-q4-adresses` → `sprint/engine-completion` : **fait** (fast-forward,
   0 conflit, local).
2. **Staging poussé** (tranché par toi : Streamlit watch `sprint/engine-completion`).
   `origin/sprint/engine-completion` = `f01e3a4` → **Streamlit Cloud redéploie le lot convergé**.
   `origin/main` = `9c70b14` **intacte**.
   - ⚠️ **Correction honnête (à inscrire au passif § 4).** En cours de nuit j'avais écrit
     « `sprint/engine-completion` jamais poussé sur origin » — **c'était FAUX**. La branche existait
     (à `b2a57d4`, l'ancien état que Streamlit déployait) ; le **refspec de fetch de ce clone est
     restreint à `main`** (`+refs/heads/main:…`), donc mon local ne la voyait pas. Un
     `git ls-remote origin` l'aurait montré d'emblée. **6ᵉ instance** du travers « fait servi sans
     vérif complète » — corrigé, mémoire `project-staging-deploy-channel` mise à jour.
3. **Message Rafael « à retester »** (tu l'envoies — je ne contacte pas Rafael) :

   ```
   Lot retours onglet-24 + live retraité — à retester sur le staging.
   - Adresses sur une ligne (tous les types), valeur nominale calculée auto,
     cession SELAS (acte + compromis ensemble), mois accentués partout, etc.
   - Reboot l'app Streamlit pour charger la dernière version.
   - 2 points où j'ai besoin de ton avis (tes mini-captures étaient illisibles) :
     « lettre de renonciation » et « supprimer la case à la fin » — tu peux repréciser ?
   ```

4. Reste : **O24-04** (icône copier — § 6bis, sur ton greenlight) + **L5/L6** (clarif Rafael).
