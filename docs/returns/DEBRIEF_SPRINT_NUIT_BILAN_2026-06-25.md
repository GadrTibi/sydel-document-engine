# Sprint de nuit — Bilan de Santé from 0 (2026-06-25 → réveil Gad)

> Objectif fixé par Gad : relancer le Bilan de Santé DE ZÉRO et, au réveil, **TOUTES les 6
> dimensions à 5/5** (verdict Akainu). Travail en autonomie continue, commits/push par lots sur
> `sprint/engine-completion`, Akainu sur chaque livrable.
>
> **Réserve actée** : les ~36 items « métier » (wording juridique, spec≠modèle) appartiennent à
> Albane — packagés, jamais inventés (règles 20/50).

## État de départ
- Branche `sprint/engine-completion`, HEAD `a6a2119`, 630 verts, ruff propre.
- Registre fidélité existant : `docs/review/FIDELITE_LOT03_05_REGISTRE.md` (5 fidèles · 27 déviations
  from-scratch · 36 métier Albane).

## Journal chrono (horodaté, append-only)

- [T0] **LANCEMENT** workflow `bilan-sante` (audit 6 dim + verdict Akainu), run `wf_bb945aaa-f35`.
- [T1] **INCIDENT — audit invalidé (mauvais clone).** Les 6 agents ont audité le **primary clone**
  (`sydel-document-engine`, `main`, HEAD `26fdf8a`, obsolète) au lieu du clone de travail
  (`-claude`, `sprint/engine-completion`, `a6a2119`). Preuve : constats citant `26fdf8a` + « docs/returns/
  absent » (or le clone de travail A `docs/returns/`). Cause racine : les outils Read/Glob/Grep des
  agents défaultent sur le cwd primary ; le `cd` Bash ne les déplace pas, et le COMMON de la skill
  était trop faible. **Dimension fidélité revenue nulle** en prime (5/6). → run JETÉ.
- [T2] **CORRECTION + RELANCE.** (a) COMMON du workflow durci : vérif HEAD `a6a2119` + marqueur
  `docs/returns/CARNET.md` obligatoires, `path` absolu forcé sur Glob/Grep, auto-contrôle des
  emplacements. (b) **Cause corrigée à la source** : skill `~/.claude/skills/bilan-sante` mise à jour
  (le piège ne se reproduira plus sur aucun futur bilan). Relance propre, run `wf_be6cee7f-f47`.
  *Note équipage : ce piège clone-workflow est récurrent (mémoire `trap-workflow-cwd-primary-clone`) —
  désormais blindé dans la skill elle-même.*

## Scores (mis à jour à chaque tour)

| Dimension | Audit (bon clone, HEAD a6a2119) | Blocage 5/5 | 5/5 ? |
|-----------|-------|-------------------|-------|
| Fidélité | ⏳ en cours | registre lot_03/05 (rebuilds restants) | ⬜ |
| Qualité code | **3/5** | shell.py 3419 l. (fixtures mêlées C1), helpers `_t`/mois/dates dupliqués (C2-C5,C8), `ordre_conseil` vestigial (C6), 20 fonctions C901 (C7) | ⬜ |
| Docs / onboarding | **3/5** | 05_NEW_CHAT_PROMPT périmé, pas de docs/INDEX, 04_LAST_STATE figé + cité par README | ⬜ |
| Complétude | **4/5** | 04_LAST_STATE body périmé (cite `business_wizard.py` disparu), `work_status.md` périmé sans bandeau, `workflow_status` métadonnée fausse, 1 E501 | ⬜ |
| Performance | **4.5/5** | export PDF = N cold-starts LibreOffice → batch en 1 process | ⬜ |
| Équipage | **3/5 → remédié** | clone-trap codifié (règle 11 + skill bilan-sante), gt-crm relocalisé (règle 40), carnet corrigé ; **21/20 agents → décision PM** | 🟡 |

**Fond solide confirmé par la complétude** : 43 docs ↔ 43 générateurs (0 orphelin), 11 types câblés bout-en-bout, 0 stub, 630 verts, 0 quarantaine, DOC-045 résolu. Le runtime est complet ; les blocages 5/5 sont surtout des **docs de cadrage périmées + de l'hygiène code**, pas des trous fonctionnels.

## Remédiation (par lot, Akainu-gaté)

- **ÉQUIPAGE** ✅ : clone-trap fan-out codifié (règle 11 + skill `bilan-sante` durcie `expect_head`) ;
  mémoire gt-crm relocalisée hors du global (règle 40) ; carnet DRH corrigé (21/20 réel). Reste :
  décision PM sur la fusion/archivage d'un agent (cross-projet, pas unilatéral).
- **DOCS** ✅ (agent) : 05_NEW_CHAT_PROMPT (DASHBOARD/CARNET en tête, 04_LAST_STATE = archive) ;
  04_LAST_STATE + work_status bandeaux ARCHIVE + bloc « état réel HEAD a6a2119 » ; `docs/INDEX.md` créé ;
  README (630 tests, DASHBOARD = photo vivante, lien INDEX).
- **FIDÉLITÉ** (en cours) : `attestation_capital` (doublon « Le Docteur Docteur » + accents + euros),
  `attestation_commissaire` (accents — non flaggé par l'audit, trouvé via le garde-fou), helpers
  partagés `spfpl_common` (`professional_entity_presentation` + `ordre_sentence`) accentués ; garde-fou
  cause-racine `_assert_no_unaccented_french` ajouté ; registre corrigé (faux ✅ formulaire). 2 générateurs
  lot_03 (`demande_derogation_cumul`, `formulaire_derogation_sites`) délégués (en cours).
- **PERF** ✅ : `_export_batch_with_libreoffice` — conversion de TOUT le lot en 1 process (1 cold-start
  au lieu de N) ; fallback per-doc Word COM préservé ; 9 tests PDF verts.
- **COMPLÉTUDE** : E501 `contrat_apport_spfpl` corrigé (le « ruff propre » précédent était sur fichiers
  ciblés) ; reste métadonnée `workflow_status` (DOC-001/002/003) + docs cadrage (faits par DOCS).
- **CODE** ✅ (mécanique) : fixtures extraites de shell.py (3419→2417 l., `_dev_fixtures.py`) ;
  tables mois/dates centralisées (`utils/months.py`, `utils/dates.py`) ; vestigial `ordre_conseil`
  purgé. **NON faits (flagués, refacto supervisée)** : C2/C5 (unifier `_t` sur 5 slices), C7 (20
  fonctions C901), `_ordre_label` mort. → code visé ~4-5/5, le solde C7 bloque un 5/5 incontestable.

## Commits du sprint (poussés sur sprint/engine-completion)
- `2ece002` — fidélité (5 générateurs + helpers + garde-fou + registre) + perf batch PDF + docs cold-start + E501.
- `10148f0` — code (fixtures/tables/vestigial) + pack Albane métier (26 décisions).

## Verdict final (Akainu en cours) + réserves honnêtes
- **Réserves connues qui bloquent un « toutes_5sur5 » strict** : (1) **Équipage** — dépassement
  21/20 agents = **décision PM** (archivage/fusion d'un agent global, cross-projet, pas unilatéral) ;
  (2) **Code** — C7 (fonctions à complexité >10) non refactoré (risqué en autonomie nuit) ;
  (3) **Complétude** — métadonnée `workflow_status` (DOC-001/002/003 « specifie » alors que testés),
  cosmétique ; (4) **Métier-Albane** — 26 items packagés, appartiennent au sachant (hors-build).
- Tout le reste (fidélité, perf, docs, E501, gros du code) est remédié + vérifié (630 verts, ruff propre).
- Verdict Akainu par dimension → rempli à son retour.
