# Workflow produit Sydel — rôles, voie juridique, base technique

Date : 2026-06-04. Ce document fixe **comment on travaille** sur Sydel (moteur de documents
juridiques). Il complète le `00-phase-router` global ; ici on cadre la spécificité **produit**.

> 🧭 **Recette de bout en bout pour outiller un type d'entreprise** (sources → cartographie → fidélité →
> règles → couches genre/nombre/PM → vérif → gate juridique → pièges) : **`PLAYBOOK_TYPE_ENTREPRISE_V1.md`**.
> Réutilisable SELARL **et SELAS**. Tout nouvel apprentissage de méthode s'y reverse (rule 45).

## 1. Rôles
- **Gad — capitaine, côté CODE / dev / orchestration.** Tranche le produit, le scope, la technique,
  les priorités, les merges. **Ne tranche PAS le contenu juridique** des documents et ne doit jamais
  être pris comme arbitre d'une règle de genre/pluriel/wording.
- **Claude — porte le juridique côté machine.** Cherche les règles dans le corpus source, encode,
  teste, génère. N'invente jamais de wording.
- **Rafael (l'associé)** — détient/centralise le savoir métier (a tokenisé les modèles, alimente le NotebookLM).
- **Albane** — sachant juridique externe (cabinet). Dernier recours pour une règle absente du corpus.

## 2. Source de vérité juridique (dans l'ordre)
1. `project/source_documents/` — modèles Word **tokenisés** (`[variable]`), par lot. Référence du
   wording ET de l'emplacement des variables.
2. `docs/delivery/*_spec_canonique_*` / `*_spec_texte_*` — specs par document (règles, variantes,
   arbitrages tranchés).
3. **NotebookLM** de l'équipe — infos compilées par l'associé + transcriptions des rendez-vous
   (plusieurs heures) avec Albane et les équipes.

## 3. Voie juridique (quand une règle est en doute)
```
Question de règle (genre / nombre / accord / variante / wording)
  └─> agent  sachant-juridique  (.claude/agents/) — LECTURE SEULE
        lit project/source_documents/ + docs/delivery/specs
        ├─ trouvé      -> réponse SOURCÉE (règle + citation verbatim + fichier §) , confiance confirmé/dérivé
        └─ absent      -> question d'escalade précise
                          -> Gad relaie -> NotebookLM -> associé (répond ou demande à Albane) -> Albane
```
Règle d'or : **jamais d'invention de wording.** Une règle `dérivée` (extrapolée d'un modèle frère)
n'est pas `confirmée` tant qu'elle n'est pas validée par le corpus ou la chaîne humaine.

## 4. Principe d'architecture (la « base solide »)

> ⛔ ABANDONNÉ (décision Gad 2026-06-04) — SELARL reste unipersonnelle. Le « multi-associés » évoqué
> ci-dessous n'est plus un objectif **pour la SELARL** (la couche nombre/pluriel reste pertinente pour
> la SELAS multi-actionnaire et les autres formes, pas pour la SELARL).

- ✅ **Une fonction (générateur) par document** + un moteur partagé + remplacement de tokens
  (`[variable]`). Déjà en place (`generators/lot_*` + `*_common.py`). **À conserver.**
- ⚠️ **Couche genre + nombre à consolider** : aujourd'hui `utils/grammar.py` ne couvre que 3 cas
  masculin/féminin singuliers ; **pas de système de pluriel/nombre**, et le multi-associés est câblé
  OFF en dur (`skip_personne_2_line=True`). Objectif cible : une couche **paramétrée et documentée**
  (genre × nombre × variante) que les générateurs consomment, alimentée par les règles du corpus.
  Priorisation retenue (2026-06-04, Capitaine) : couche **genre** en premier ; couche **nombre/pluriel** après le wording d'Albane.
- ⚠️ **Documentation des règles par fonction** : les specs existent (`docs/delivery/`) mais ne sont
  pas liées depuis le code. Cible : chaque générateur pointe vers sa spec + ses règles genre/nombre.

## 5. Cycle d'un document (ou d'une variante)
1. Règle/wording → **sachant-juridique** (sourcé) ; si absent → escalade (§3).
2. Spec de sous-cas si nouveau cas (règle projet : spec avant code).
3. Code : générateur (ou paramètre) fidèle au corpus, zéro invention.
4. Test + `generate_pack` (pack reproductible) + revue. **Revue `sachant-juridique` OBLIGATOIRE** (fidélité tokens vs modèle source) avant de marquer un document « fait » ; l'auto-rapport du générateur ne suffit pas.
5. MAJ des docs vivants (specs, journal, plan).

## 6. Ce qui est déjà livré (réf.)
Voir `SELARL_COMPLETION_PLAN_V1.md` : SELARL création + cession cabinet (DOC-007→012) + SCM
(DOC-031/033) câblés et générables sur `review/selarl`. **Couche genre faite** (2026-06-04, masc/fém,
323 tests verts). Reste :
- **statuts multi-associés** + **nombre/pluriel** : le wording (comparution « LES SOUSSIGNÉS », apports
  N, répartition N, signatures N, agrément/quorum) est **ABSENT du corpus ET du NotebookLM**
  (« NON TROUVÉ » ; les transcripts qualifient ces cas d'« ultra personnalisés / faits à la main ») →
  **escaladé à Rafael** (message 2026-06-04). **Ne pas inventer.**
- **règles de genre d'usage** (« Docteur » au féminin, article devant civilité) : idem escaladées à Rafael.
- formulaire UI cession/SCM (gated par la définition de « SELARL terminée », Q6 Gad).

> ⛔ ABANDONNÉ / SUPERSÉDÉ (décision Gad 2026-06-04) — SELARL reste unipersonnelle. La ligne D1
> ci-dessous (associé personne morale + multi-associés en SELARL) est **superseded** : elle n'oriente
> plus le produit. L'associé personne morale **en SELAS** via micro-holding n'est pas concerné.

**D1 tranché (2026-06-04, NotebookLM)** : une **personne morale PEUT être associée d'une SELARL** — le
canon « société associée » est **correct** (pas une dérive), et le multi-associés doit la gérer ; les
**champs** d'une PM sont connus, mais son **wording statuts** est « ultra personnalisé » (cf. Rafael).
