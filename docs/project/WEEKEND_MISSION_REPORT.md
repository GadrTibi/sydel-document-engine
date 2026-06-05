# Rapport de mission week-end (autonome) — 2026-06-05 → retour Gad

> Pour Gad, à la reprise. Tout est sur **branches dédiées, rien sur `main`, aucune génération
> déclarée valide** (gate juridique respecté). Lis ce fichier en premier.

## TL;DR — ce qui est prêt, ce que tu dois faire
1. **SELARL = finie** (création + cession + SCM + **UI testable**), sur `review/selarl`. À toi : tester
   sur Streamlit (Cloud pointé sur `review/selarl`), valider, puis décider le merge `→ main`.
2. **Méthode A→Z capitalisée** : `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md` + commande
   `/type-entreprise`. Livrée à Naomi (prompt cockpit fourni).
3. **6 autres types ouverts** (SPFPL, SCM, SAS, SCI, SCP, EURL) sur `types/weekend-foundations` :
   modèles rangés + inventaire + cartographie tentative + **prompts NotebookLM prêts à envoyer** +
   statut/plan. **À toi : envoyer les `NOTEBOOKLM_PROMPTS.md` de chaque type au NotebookLM** ; les
   réponses débloquent la cartographie officielle puis la fondation.
4. **Nettoyage** : 3 clones obsolètes supprimés + junk local nettoyé. Voir §Nettoyage (1 clone + le
   sprawl docs laissés à ton arbitrage).

## ⚠️ Décisions / arbitrages qui t'attendent
- **[CANON] Quelle version fait foi ?** Le canon récent `Documents_a_generer_par_cas_V3.docx` est
  **SELARL-only**. Mais le **V1** (`Documents_a_generer_par_cas.docx`) **contenait une section SPFPL**
  (cession + apport, docs par cas) que V2/V3 ont **supprimée** — et le `case_catalog.py` de Codex la
  suit. → **Question n°1 : on repart du V1 (avec SPFPL/…) ou le V3 fait foi (et il faut re-sourcer les
  cas par type) ?** C'est le déblocage central pour tous les autres types.
- **[NotebookLM] À envoyer** : un fichier `docs/project/types/<TYPE>/NOTEBOOKLM_PROMPTS.md` par type,
  copiable tel quel. Priorité : établir la **liste des cas + la carte cas→documents** de chaque type.
- **[EURL]** : **aucun modèle** sur le Drive → il faut **demander les modèles EURL à Rafael** (prompt
  prêt dans `docs/project/types/EURL/`).
- **[Clone]** : `sydel-document-engine-clean` a **19 changements non commités** (rebuild front + docs
  potentiellement uniques) — **je ne l'ai pas supprimé**. À récupérer/arbitrer toi-même.
- **[Légacy .doc]** : 3 modèles SPFPL en `.doc` (non lisibles par l'outil) à reconvertir en `.docx` ou
  refournir tokenisés (listés dans `docs/project/types/SPFPL/STATUT.md`).

## État des branches
| Branche | Contenu | État |
|---|---|---|
| `review/selarl` | SELARL complète (création + cession + UI + bouton données de test) | testable, NO-GO merge sans toi |
| `types/weekend-foundations` | fondations + prompts des 6 types + ce rapport | review, rien sur main |
| `main` | inchangée (origin `5e0c72d`) | intacte, aucun déploiement |

## Par type (résumé — détail dans `docs/project/types/<TYPE>/` + `INDEX.md`)
| Type | Modèles | Backend Codex (à RE-VÉRIFIER) | Carte des cas | Prochaine étape |
|---|---|---|---|---|
| **SPFPL** | 33 (dont 3 `.doc` legacy) | substantiel (case_catalog SPFPL_CESSION/APPORT, lot_04/05, registry) | V1 oui / V3 non → **à trancher** | envoyer prompts → trancher canon → re-vérifier Codex |
| **SCM** | 12 | substantiel (statuts, pacte, RI, cession, satellites) | absente (sous-cas SELARL ≠ type autonome) | envoyer prompts → établir les cas SCM autonome |
| **SAS** | 7 | partiel (statuts_sas, satellites) ; recouvre SPFPL | absente | envoyer prompts (SAS pur vs SAS-SPFPL ?) |
| **SCI** | 7 | partiel (statuts_sci + IRIS) | absente | envoyer prompts |
| **SCP** | 6 | **rien** (Codex non démarré) | absente | envoyer prompts (sources minces : 1 modèle tokenisé) |
| **EURL** | **0** | rien | absente | **demander les modèles à Rafael** |

> Profondeur tenue : **fondation + prompts** (volontairement **pas de code moteur neuf** — le canon ne
> donne pas l'assemblage par cas, donc bâtir serait à l'aveugle). Le backend Codex existant est
> **inventorié mais NON re-vérifié** (zéro confiance tant que pas testé/validé).

## Comment reprendre (au retour)
1. Trancher la **question canon (V1 vs V3)** — c'est le déblocage.
2. Pour chaque type : **envoyer `NOTEBOOKLM_PROMPTS.md`** au NotebookLM → consigner les réponses.
3. Lancer **`/type-entreprise <TYPE>`** : il déroule le workflow (re-vérifie le backend Codex, bâtit
   la cartographie officielle, le moteur fidèle, l'UI tous-cas + bouton test, la vérif, le gate).
4. Tester chaque type sur Streamlit (Cloud pointé sur sa branche), valider, puis merge `→ main`.

## Nettoyage — fait & proposé
**Fait (sûr) :**
- Clones obsolètes supprimés : `_codex_worktrees_archive` (vide), `_TO_DELETE_…` (23 Mo, copie sans-git,
  docx tous dans git/régénérables), `sydel-track-b` (vide).
- Junk local : `artifacts/_*` temp, 18 `__pycache__`, 154 `.pyc`, caches pytest/ruff, dossiers basetemp.
- Gardés : `Notebooks/` (données), `sydel-document-engine` (original/install), `…-claude` (actif).

**Proposé (ton GO requis — je n'y ai pas touché) :**
- `sydel-document-engine-clean` : 19 changements non commités → **récupérer puis supprimer**, ou jeter si
  obsolète. (Travail non sauvegardé : à toi de voir.)
- **Sprawl docs committé** : 262 `.md` (dont 88 `docs/review/` = rapports d'audit Codex, 56
  `docs/project/`). Proposition : **archiver** les rapports d'audit superseded dans `docs/review/_archive/`
  et **consolider** les docs d'état (garder `04_LAST_STATE`, `JOURNAL_DECISIONS_*`, `WORKFLOW_*`,
  `PLAYBOOK_*`, les `types/`). À faire ensemble (jugement sur ce qui est courant vs historique).
- `.git` = 122 Mo (historique de docx binaires) : laissé tel quel (un nettoyage d'historique est risqué).

## Garanties
Rien sur `main`. Aucun déploiement. Aucune génération déclarée valide (gate juridique). Aucune question
métier posée au PM. Aucun travail non sauvegardé supprimé. Branche vérifiée avant chaque commit.
