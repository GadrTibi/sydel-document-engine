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

1. **Pattern de sur-affirmation (récurrent, attrapé 3-4×).** Ma faute la plus coûteuse :
   déclarer « racine prouvée », « gold intact », « X verts déterministe » sur des bases
   insuffisantes. Akainu l'a relevé à répétition. **Correctif appliqué** : wording requalifié
   en « cause plausible + neutralisation par construction » ; preuves désormais structurelles
   (`pytest-randomly`) avant toute affirmation d'ordre-indépendance. Codifié en mémoire
   (`feedback-fixes-racine-pas-surface`).
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
| O24-04 | icône « copier » par champ | Streamlit n'a pas de copier natif → décision UI (approche `st-copy`) | build avec helper partagé **après** merge du lot retours |
| L5 / L6 | 2 retours live | **mini-screenshots illisibles** : sens inconnu | **question Rafael** — ne pas deviner (`QUESTIONS_RAFAEL.md`) |
| Sync registres | `CARNET`/`DASHBOARD` stale (23-06 17:48) | corrigés mais registres non mis à jour | synchroniser au statut réel (clôture) |
| Dettes Albane | wording figé « Inscription de la SELARL au Tableau » (2 compromis) ; PACS cession ; valeur nominale SPFPL cible ; salarié incomplet | arbitrage **métier** Albane, pas un bug | tracés dans `QUESTIONS_RAFAEL.md` |

---

## 7. Recommandation de manœuvre (ton GO requis)

1. **Merge** worktree `feat/propagation-q4-adresses` → `sprint/engine-completion`
   (fast-forward, 0 conflit) **après** convergence Akainu tour 10. _(Local, réversible — je le
   fais en autonomie une fois tour 10 OK.)_
2. **⚠️ DÉCISION PM — où déployer le staging.** J'ai découvert cette nuit que
   `sprint/engine-completion` **n'a jamais été poussé sur `origin`** (seul `origin/main`
   existe). Et un indice côté clone primaire (`26fdf8a "chore: trigger Streamlit main test
   deploy"`) suggère que **Streamlit Cloud déploie depuis `main`**. Conséquence : rendre le
   travail testable pourrait exiger de **toucher `main`** — ton garde-fou dur. **Je n'ai
   poussé RIEN.** Deux options à ton réveil :
   - **(a)** Streamlit watch `sprint/engine-completion` → je pousse cette branche (ne touche
     pas `main`, je peux le faire sans risque) — dis-moi juste « pousse engine-completion ».
   - **(b)** Streamlit watch `main` → il faut un merge `main` (PR + ton GO explicite). Je
     prépare la PR mais **je ne merge pas `main` sans toi**.
   → **Dis-moi quelle branche Streamlit surveille**, je pousse en conséquence.
3. **Message Rafael « à retester »** prêt à copier (je ne le contacte pas — c'est ton geste) —
   finalisé une fois le staging réellement déployé (sinon je l'enverrais sur du vide).
4. Puis **O24-04** (build) + clarif **L5/L6**.

_(Sections convergence / merge / O24-04 finalisées en bas de sprint.)_
</content>
</invoke>
