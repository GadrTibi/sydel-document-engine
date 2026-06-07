---
description: Développer un type d'entreprise de A à Z dans Sydel (moteur + interface Streamlit) en suivant le workflow définitif — sourcing, cartographie, moteur fidèle, couches genre, UI testable tous-cas, vérification, gate juridique. S'arrête aux jalons PM/juridique.
---

Tu pilotes le développement d'un **type d'entreprise** dans Sydel, de A à Z, **interface Streamlit
comprise**. Le type visé est `$ARGUMENTS` (ex. `SPFPL`, `SCM`, `SCI`, `SAS`). S'il est vide, demande-le.

## Source de vérité
Déroule **`docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`** — c'est le mode d'emploi détaillé (phases 0→9,
recette UI, pièges, checklist de clôture). La **SELARL** en est l'implémentation de référence : à chaque
phase, copie/adapte les fichiers `Réf. SELARL` cités là-bas. Ne réinvente pas ce qui est déjà résolu.

## Règles dures (toutes phases — NON négociables)
- **Fidélité** : remplissage de template du modèle tokenisé (`rendering/docx_template_fill.py`), JAMAIS
  de paraphrase. `dérivé` ≠ `confirmé`.
- **Escalade** : sources → **NotebookLM** (toujours AVANT Rafael) → **message Rafael** (jamais Albane en
  direct, jamais une question métier au PM). Réponses humaines ≠ parole d'évangile.
- **Vérification** : suite **COMPLÈTE** verte (jamais un sous-ensemble), ruff clean, **0 token résiduel**,
  masculin ET féminin, tous les cas. **Ne jamais croire l'auto-rapport d'un agent** — revérifie toi-même.
- **Git** : 1 type = 1 branche `<type>/…`. **`git branch --show-current` AVANT chaque edit/commit.**
  `add` explicite (pas de `git add -A` aveugle). **Merge `main` + déploiement = geste PM uniquement.**
- **Couche partagée** : ne pas éditer la couche SEL/commune depuis deux sessions en parallèle.

## Déroulé (s'arrête aux 🚦 jalons)
0. **Cadrage & branche** — bloc de routage PM ; 🚦 confirmer le périmètre au PM (carte cliquable si choix) ;
   créer la branche `<type>/…` via `git-branch-steward` ; vérifier la branche courante.
1. **Sources** — `Explore` : inventorier/dédupliquer/ranger les modèles tokenisés dans
   `project/source_documents/lot_*` ; lire le canon `Documents_a_generer_par_cas_V3.docx` + locks de
   retours humains. Vérifier les cas par le **contenu** ; cas manquant → 🚦 message Rafael.
2. **Cartographie** — produire la **matrice cas → documents** (le backlog) + les variantes (genre,
   gérance, profession, régime, cession, SCM, dérogation, site distinct).
3. **Moteur** — un générateur par document (`generators/lot_*`) + `*_common.py` + anti-token-résiduel ;
   **scénarios/fixtures par cas** (`scenarios/<type>.py`, réutilisés par le bouton test en phase 6) ;
   modèles `domain/models.py`.
4. **Règles juridiques** — appliquer ce que NotebookLM/locks tranchent ; chasser les **coquilles
   inter-profession** ; ne pas confondre durée société (figée) vs domiciliation (indéterminée) ; points
   non sourcés → 🚦 message Rafael.
5. **Couche genre** — `utils/grammar.apply_gender_pairs` (paires exactes, jamais de regex de terminaison),
   pilotée par la bonne personne ; préférences par personne = variables. (Nombre/pluriel : après Albane.)
6. **Interface Streamlit** (LE gros morceau) — copier l'archi slice de la SELARL :
   `front_app/app.py → shell.py → <type>_slice.py`. Pour CHAQUE cas : checkbox + `_render_<cas>_form()`
   bâti sur la fixture (→ contexte Pydantic toujours valide) + câblage (`…_context`, codes, génération) +
   garde-fou (coché sans données = bloqué) + **étendre le bouton « Generer des donnees de test »** pour
   préremplir ce cas depuis la fixture. **Standard : tous les cas du canon générables depuis l'UI, 1 clic
   de données de test, 0 token résiduel.** **Messages UI en français métier (zéro code interne type
   DOC-0xx) ; un cas manuel/hors-scope = WARNING, pas blocker. Fidélité de FORME : un générateur
   from-scratch reproduit logo (header, helper `docx_builder.add_header_logo`) + alignements +
   puces/tirets + gras/souligné du modèle — sinon préférer le template-fill.**
7. **Vérification** — toi-même : ruff + suite complète verte + génération **via le chemin UI** sans token
   résiduel + création seule intacte + revue fidélité (`functional-reviewer`/`sachant-juridique`) +
   **passe pré-shot UAT** (relire chaque doc à côté du modèle : logo, alignements, puces/tirets,
   gras/souligné, **noms de personnes complets**, messages métier). Vérifie la branche, `add` explicite,
   push sur `<type>/…`.
8. **Gate juridique** — génération **NO-GO** tant que Rafael/Albane n'a pas validé le wording ; produire le
   **Pack de passation** (points épuisés côté NotebookLM) ; 🚦 tests sur la branche `<type>/…` (Streamlit
   Cloud pointé sur cette branche, **pas** un merge `main`).
9. **Clôture** — journal de décisions (codes `<TYPE>-…`, superseded marqué), état courant + tickets,
   **reverser les nouvelles leçons dans `WORKFLOW_TYPE_ENTREPRISE_V1.md`** (méta-règle) ; 🚦 merge `main` +
   déploiement laissés au PM.

## Sortie attendue à chaque jalon 🚦
Une **carte de décision** courte au PM (périmètre, points Rafael, go/no-go tests, merge), jamais une
question métier. À la fin : la **checklist de clôture « type fini »** du workflow, cochée et vérifiée.
