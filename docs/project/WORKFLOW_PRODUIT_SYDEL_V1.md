# Workflow produit Sydel — rôles, voie juridique, base technique

Date : 2026-06-04. Ce document fixe **comment on travaille** sur Sydel (moteur de documents
juridiques). Il complète le `00-phase-router` global ; ici on cadre la spécificité **produit**.

## 1. Rôles
- **Gad — capitaine, côté CODE / dev / orchestration.** Tranche le produit, le scope, la technique,
  les priorités, les merges. **Ne tranche PAS le contenu juridique** des documents et ne doit jamais
  être pris comme arbitre d'une règle de genre/pluriel/wording.
- **Claude — porte le juridique côté machine.** Cherche les règles dans le corpus source, encode,
  teste, génère. N'invente jamais de wording.
- **Rafael (l'associé)** — détient/centralise le savoir métier (a tokenisé les modèles, alimente le NotebookLM).
- **Alban** — sachant juridique externe (cabinet). Dernier recours pour une règle absente du corpus.

## 2. Source de vérité juridique (dans l'ordre)
1. `project/source_documents/` — modèles Word **tokenisés** (`[variable]`), par lot. Référence du
   wording ET de l'emplacement des variables.
2. `docs/delivery/*_spec_canonique_*` / `*_spec_texte_*` — specs par document (règles, variantes,
   arbitrages tranchés).
3. **NotebookLM** de l'équipe — infos compilées par l'associé + transcriptions des rendez-vous
   (plusieurs heures) avec Alban et les équipes.

## 3. Voie juridique (quand une règle est en doute)
```
Question de règle (genre / nombre / accord / variante / wording)
  └─> agent  sachant-juridique  (.claude/agents/) — LECTURE SEULE
        lit project/source_documents/ + docs/delivery/specs
        ├─ trouvé      -> réponse SOURCÉE (règle + citation verbatim + fichier §) , confiance confirmé/dérivé
        └─ absent      -> question d'escalade précise
                          -> Gad relaie -> NotebookLM -> associé (répond ou demande à Alban) -> Alban
```
Règle d'or : **jamais d'invention de wording.** Une règle `dérivée` (extrapolée d'un modèle frère)
n'est pas `confirmée` tant qu'elle n'est pas validée par le corpus ou la chaîne humaine.

## 4. Principe d'architecture (la « base solide »)
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
(DOC-031/033) câblés et générables sur `review/selarl`. Reste : couche genre/nombre + statuts
multi-associés (wording présent dans le corpus, à dériver via le sachant-juridique) + formulaire UI.
