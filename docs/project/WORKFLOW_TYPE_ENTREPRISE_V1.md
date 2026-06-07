# Workflow — Développer un type d'entreprise de A à Z dans Sydel (V1)

**Le mode d'emploi définitif** pour outiller un nouveau type d'entreprise (SPFPL, SCM, SCI, SAS, SCP,
EURL…), **moteur ET interface Streamlit comprise**, jusqu'à un produit testable et fidèle.

> **La SELARL est le premier type fait de A à Z** (création + cession + SCM + UI + bouton de test).
> Ce workflow **capitalise** ce cap : les prochains types doivent être **simples et parfaits** parce que
> les problèmes durs sont déjà résolus. La SELARL sert d'**implémentation de référence** : à chaque
> phase, « Réf. SELARL » pointe le fichier réel à copier/adapter.

> **Méta-règle (rule 45).** Tout nouvel apprentissage de méthode pendant un type **se reverse ICI**
> (sans qu'on le demande), pour que le type suivant parte encore plus vite. Ce doc **remplace et
> élargit** `PLAYBOOK_TYPE_ENTREPRISE_V1.md` (gardé comme résumé des principes).

> **MAJ 2026-06-07 — leçons du 1ᵉʳ round UAT Rafael (SELARL) intégrées** : ① fidélité de **mise en
> forme** + **logo header** (le from-scratch les perdait), ② **messages UI en français métier** (un cas
> manuel = **warning, pas blocker**), ③ **complétude des clauses nommées** (mettre le nom des personnes,
> ex. conjoint), ④ **passe « pré-shot UAT »** avant livraison. Objectif : boucle UAT quasi vide.

> **Exécution.** Ce workflow est piloté par la commande **`/type-entreprise <TYPE>`**
> (`.claude/commands/type-entreprise.md`), qui déroule les phases ci-dessous avec les bons agents et
> s'arrête aux jalons PM / juridique. On peut aussi le suivre à la main.

---

## Principes non négociables (valent à TOUTES les phases)

1. **Fidélité.** On reconstruit par **remplissage de template** du modèle source tokenisé
   (`rendering/docx_template_fill.py`) ; **jamais** de paraphrase du wording juridique. `dérivé` ≠
   `confirmé` tant qu'un humain n'a pas validé.
2. **Escalade des règles.** `project/source_documents/` → **NotebookLM** → **Rafael** (qui décide seul
   s'il sollicite **Albane**). **NotebookLM TOUJOURS avant Rafael.** **Claude ne contacte jamais
   Albane.** **Ne JAMAIS poser une question métier/juridique au PM (Gad)** : épuiser les sources, puis
   message pour Rafael (être CERTAIN avant de faire relayer). Les réponses humaines **ne sont pas
   parole d'évangile** : analyser, signaler les imprécisions, préférer une **variable** à une règle fausse.
3. **Vérification.** **Suite COMPLÈTE verte** (jamais un sous-ensemble), ruff clean, **0 token résiduel**
   dans les DOCX générés, masculin ET féminin, **tous les cas**. **Ne jamais croire l'auto-rapport** d'un
   agent : revérifier soi-même.
4. **Discipline Git.** 1 type = 1 branche dédiée `<type>/...`. **Vérifier `git branch --show-current`
   AVANT tout edit/commit** (un agent d'audit peut laisser le repo sur `main`). `add` **explicite** des
   fichiers visés (pas de `git add -A` aveugle). **Merge sur `main` = geste PM**, jamais en autonomie.
5. **Couche partagée.** La couche SEL/commune est partagée (SELARL × SELAS de Naomi…) : **ne pas
   l'éditer depuis deux sessions en parallèle** ; 1 session = 1 dossier.

---

## Phase 0 — Cadrage & branche
**Objectif :** savoir ce qu'on construit et où.
- Produire le **bloc de routage PM** (`05-pm-routing-block`) ; confirmer le **périmètre** au PM si une
  intention est nouvelle/modifiée (carte de décision cliquable).
- Créer la **branche dédiée** `<type>/<ticket>` (via `git-branch-steward`). Vérifier la branche courante.
- **Sortie :** branche prête, périmètre confirmé.

## Phase 1 — Sources (le butin)
**Objectif :** réunir les modèles tokenisés et le canon, sans rien inventer.
- Récupérer les **modèles `.docx` tokenisés** du type (Drive « Documents avec variables », toutes
  structures). **Dédupliquer** (un seul exemplaire/document) et **ranger par structure** dans
  `project/source_documents/lot_*` (du plus courant au moins courant).
- Charger le **canon** `project/source_truth/Documents_a_generer_par_cas_V3.docx` (carte cas → documents).
- Charger les éventuels **locks de retours humains** (`*_HUMAN_REFERENCE_LOCK_*`, `*_human_returns_*`).
- ⚠️ **Vérifier qu'on a TOUS les cas en lisant le CONTENU, pas le nom de fichier.** Si un cas/fichier
  manque → **message Rafael** (jamais inventer).
- **Agents :** l'agent **built-in** `Explore` (inventaire — ce n'est pas un agent custom du projet),
  `git-branch-steward`.
- **Sortie :** corpus rangé + canon lu.

## Phase 2 — Cartographie des cas
**Objectif :** la liste exhaustive de ce qu'il faut générer (= le backlog).
- Depuis le canon, **énumérer TOUS les cas** du type et les **documents par cas**. Pour une SEL typique :
  création (statuts, PV nomination, autorisation domiciliation, déclaration, procuration, demande
  ordre), **régime communautaire** (renonciation, avertissement), **cession** (commune : avenant bail,
  appel de fonds ; cabinet médical acte+compromis ; cabinet dentaire acte+compromis ; **parts SCM** :
  PV AGE + courrier SDE + acte), **dérogation**, **site distinct**.
- Cartographier les **variantes** : genre, nombre/pluriel, gérance/présidence, profession (médecin /
  chirurgien-dentiste …).
- **Sortie :** une **matrice cas → documents** (tableau). C'est le plan de charge.
- **Réf. SELARL :** `docs/project/JOURNAL_DECISIONS_SELARL_V1.md` (périmètre livré) + la matrice cession.

## Phase 3 — Moteur (génération fidèle)
**Objectif :** chaque document se génère fidèlement depuis le modèle.
- **Un générateur par document** dans `generators/lot_*/` + un module **partagé** `*_common.py` ;
  remplissage via `fill_docx_template` ; **sécurité anti-token-résiduel** (lève si un `[token]` reste).
- **⚠️ FIDÉLITÉ DE MISE EN FORME — PRÉFÉRER le template-fill (leçon UAT Rafael).** La fidélité, ce
  n'est pas que le wording : c'est aussi la **mise en forme**. Le **template-fill préserve
  AUTOMATIQUEMENT** la forme du modèle (logo, alignements, puces/tirets, gras/souligné, positionnement,
  images). Un générateur **from-scratch** doit **REPRODUIRE TOUT** ce que contient le modèle d'origine —
  pas seulement le texte : **logo du header**, **alignements** (bloc à droite, montant centré),
  **puces/tirets** des listes, **gras/souligné** (objets, titres), positionnement (signataire à droite…),
  et **toutes les images embarquées** (`word/media/`). Le from-scratch SELARL en avait perdu plusieurs →
  autant de remarques UAT 100 % évitables. **Si from-scratch : ouvrir le modèle d'origine et lister sa
  forme AVANT de coder.**
- **Logo SYDEL** : il vit dans le **header des modèles d'origine** ; tout from-scratch l'oublie. Helper
  partagé prêt : `rendering/docx_builder.add_header_logo(document, alignment=…)` (asset
  `assets/logo_sydel.png`, extrait du modèle). À appeler après `new_document()` dans **chaque** générateur
  from-scratch (alignement selon le modèle/retour : appel de fonds = droite, courrier SDE = gauche).
- **Ranger par lot logique** : la cession de **cabinet** vit dans son lot (réf. SELARL `lot_03`), la
  cession de parts d'une **société satellite** (SCM) dans **son propre lot** (réf. `lot_05`) — pas
  mélangées.
- **Déclarer les codes documents** (`DOC-0xx`) + leur mapping `code → générateur` dans le **registre**
  (`registry/` + le slice) — étape **obligatoire** pour qu'un cas soit sélectionnable.
- Écrire les **scénarios/fixtures par cas** dans `scenarios/<type>.py` : des contextes Pydantic
  **complets et valides**. **Ils seront RÉUTILISÉS** comme source unique du bouton « données de test »
  de l'UI (Phase 6) — ne pas dupliquer les données ailleurs.
- **Modèles de données** (`domain/models.py`) : un `…Context` par grand cas (ex. `CessionContext` et ses
  sous-modèles) ; champs requis vs optionnels explicites.
- **Réf. SELARL :** `generators/lot_01..05/`, `generators/lot_03/*_common.py`,
  `rendering/docx_template_fill.py`, `scenarios/selarl.py`, `domain/models.py`.
- **Agents :** build dédié + revue. **Sortie :** tous les docs générables par scénario.

## Phase 4 — Règles juridiques (escalade, anti-coquille)
**Objectif :** le wording est juste, sans invention.
- Pour tout doute : sources → **NotebookLM** → message **Rafael**. Cf. principe 2.
- **Pièges déjà rencontrés** (à vérifier systématiquement) :
  - **Coquilles inter-profession** : des mentions d'une profession fuient dans la trame d'une autre (ex.
    « cabinet **dentaire** » dans un document **médical**) → **purger**.
  - **Durée** : la **durée de la SOCIÉTÉ** (statuts) est **figée** (99 ans pour la SELARL — retour
    humain) ; la **durée de la DOMICILIATION** est **« indéterminée »** (source primaire). **Ne pas
    confondre** les deux.
  - **Origine de propriété** (cession) : décrit le **VENDEUR** (créé par défaut, ou acheté), pas
    l'acquéreur.
  - **Unités** (crédit-vendeur en **années**…), **salariés 0/1/N** (« Néant. » si 0).
  - Un document « commun à toute cession » (ex. **appel de fonds**) ne doit pas être restreint à une
    profession à cause d'une coquille figée → vérifier contre le canon (« Si cession » = commun).
- **Sortie :** points juridiques tranchés (NotebookLM) ou listés pour Rafael.

## Phase 5 — Couches transverses
**Objectif :** genre (et nombre, plus tard) corrects partout.
- **Genre** : `utils/grammar.apply_gender_pairs(texte, genre, paires)` — **paires de chaînes EXACTES**,
  **JAMAIS de regex de terminaison** (`-é/-ée`), pilotées par le genre de **la bonne personne**.
- **Genre par personne** : certaines préférences sont **par personne** (« le Docteur » / « la
  Docteure ») → **variable**, pas règle universelle.
- **Nombre / pluriel** : seulement **après validation Albane** ; la gouvernance est souvent déjà
  plurielle dans le modèle, seuls ~4 endroits sont à pluraliser (comparution, apports, répartition,
  signatures).
- **Réf. SELARL :** `utils/grammar.py`.

## Phase 6 — Interface Streamlit (LE gros morceau)
**Objectif :** **tous les cas du canon générables depuis l'UI**, en un clic de données de test.
**Standard « parfait » :** cocher un cas → un sous-formulaire de saisie → génération réelle ; et le
bouton « données de test » préremplit **tout** (1 clic = dossier complet testable, 0 token résiduel).

**Architecture de la slice (à copier de la SELARL) :**
- `front_app/app.py` → appelle `render_clean_front()`.
- `front_app/shell.py` : le wizard —
  `_render_dossier_type_selection()` (contient le **bouton « Generer des donnees de test »** →
  `_prefill_random_selarl_data()`), puis `_render_data_entry_zone()` (qualification → sous-formulaires
  par cas) puis `_render_generation_zone()`.
- `front_app/<type>_slice.py` : le **modèle d'entrée** (`…SliceInput`), `validate_<type>_input()`,
  `selected_<type>_document_codes()`, `build_generation_context()`.

**Pour CHAQUE cas (recette) :**
1. Une **checkbox/sélecteur** de qualification (ex. « Cession », « SCM », « Régime communautaire »).
2. Un **`_render_<cas>_form(...) -> <Cas>Context | None`** : si non coché → `None` ; sinon des sections
   repliables (`st.expander`) qui exposent les **champs clés éditables**, **bâties SUR la fixture
   scénario** (Phase 3) et **fusionnées** → un `…Context` Pydantic **toujours valide** (les champs
   profonds non exposés viennent de la fixture → 0 token résiduel garanti).
3. **Câbler** : le contexte est passé à `…SliceInput.<cas>_context` ; la condition `… is not None`
   sélectionne les codes documents du cas ; `build_generation_context` le passe au moteur.
4. **Garde-fou** : cas coché **sans** données → **bloqué** (pas de génération muette).
5. **Étendre le bouton « données de test »** : il préremplit **les clés de CE cas** depuis la **fixture
   scénario** (helper public `…_fixture_for_*`), en respectant la profession choisie. **Conserver le
   libellé exact du bouton** et tout le préremplissage existant.
6. **Messages UI en FRANÇAIS MÉTIER, jamais en jargon dev (leçon UAT Rafael).** Aucun code interne
   (`DOC-013`, « périmètre V1 »…) visible par l'utilisateur. Un cas **hors scope / manuel** (formulaire
   « à remplir à la main ») = un **warning informatif CLAIR**, **PAS un blocker** qui empêche de générer
   le reste du dossier. Réserver les **blockers** aux **vraies données manquantes** (cas coché sans
   données). Réf. SELARL : dérogation/site distinct → warnings (pas blockers) dans `validate_selarl_input`.

**Réf. SELARL :** `front_app/shell.py` (`_render_cession_form`, `_render_scm_cession_form`,
`_prefill_random_selarl_data`), `front_app/selarl_slice.py`
(`selected_selarl_document_codes`, `validate_selarl_input`, `build_generation_context`),
`scenarios/selarl.py` (`cession_fixture_for_profession`, `scm_cession_fixture`).
**Garde-fou anti-legacy :** les sous-formulaires ne rendent leurs `expander` que si le cas est coché
(sinon test « pas d'écran legacy » cassé).

## Phase 7 — Vérification (jamais l'auto-rapport)
**Objectif :** prouver, soi-même, que tout marche.
- `ruff check src tests` → 0 erreur.
- `pytest` **suite COMPLÈTE** (`--basetemp` **hors repo**, cf. pièges) → **tout vert** (chiffres). Ajouter
  des tests : codes documents par cas, génération **via le chemin UI** (slice → contexte → DOCX) **sans
  token résiduel**, **création seule intacte**, masculin/féminin.
- Générer et **ouvrir les DOCX** des cas clés (preuve), vérifier « 0 crochet `[` résiduel ».
- **Revue de fidélité** (`functional-reviewer` / agent `sachant-juridique`) vs modèle source.
- **🔎 Passe « PRÉ-SHOT UAT » (l'œil de Rafael, AVANT Rafael)** : relis chaque doc généré comme l'associé
  le ferait en test, **à côté du modèle d'origine**, et coche : **logo** présent + bien placé ?
  **alignements** (droite/centre) conformes ? **puces/tirets** sur les listes ? **gras/souligné** sur les
  objets/titres ? **noms de personnes COMPLETS** dans les clauses (ex. conjoint dans « marié à … ») ?
  **messages en français métier** (zéro code interne) ? Tout ce qui se **voit à l'œil** doit matcher le
  modèle. But : que Rafael n'ait **rien** à remonter en mise en forme — la boucle UAT doit être quasi vide.
- **Vérifier la BRANCHE** (`git branch --show-current`) **avant** de committer ; `add` explicite ; push
  sur la branche du type (pas `main`).

## Phase 8 — Gate juridique (livraison)
**Objectif :** ne pas livrer un wording non validé.
- La **génération reste NO-GO** tant que **Rafael/Albane** n'a pas validé le wording des nouveaux
  documents. La **fondation technique + l'UI** peuvent être GO indépendamment (preview/test).
- Produire un **Pack de passation** : points juridiques **épuisés côté NotebookLM**, formulés pour Rafael.
- **Tests sur la branche du type** (Streamlit Cloud pointé sur la branche `<type>/…`, **pas** un merge sur
  `main`) → boucle de correction live si besoin.

## Phase 9 — Journal de décisions & clôture
**Objectif :** rien d'enterré en chat, prêt pour le type suivant.
- Consigner les **décisions ratifiées** dans le **journal de décisions** avec des **codes stables**
  (`<TYPE>-…`), ancienne décision marquée `superseded`.
- Mettre à jour l'**état courant** + le **registre des tickets**.
- **Reverser les nouvelles leçons ICI** (méta-règle).
- **Merge `<type>/… → main` + déploiement = geste PM** (après validation des tests sur la branche).
- **Réf. SELARL :** `docs/project/JOURNAL_DECISIONS_SELARL_V1.md`.

---

## Pièges techniques (Windows / Git) — déjà payés, ne pas re-payer
- **pytest** : `--basetemp` **hors repo** ; console cp1252 → `sys.stdout.reconfigure(encoding='utf-8',
  errors='replace')` + **glob** pour les noms de fichiers **accentués** (ne pas hardcoder « Modèle… »).
- **editable install** pointe vers le repo voisin : `pyproject` `pythonpath=["src"]` couvre **pytest** ;
  toute vérif **hors pytest** (génération directe) doit forcer `PYTHONPATH=<clone>/src`. `scripts/` peut
  ne pas exister dans le clone courant — vérifier le chemin du script avant de l'appeler.
- **From-scratch vs template-fill** : certains générateurs **construisent** le document (paragraphes en
  dur) au lieu de remplir le modèle — la durée/le wording peut alors être **codé dans le générateur**, pas
  dans le `.docx`. Vérifier **où** vit réellement le texte avant de « corriger le modèle ».
- **Plusieurs clones** sur la machine : 1 session = 1 dossier ; ne pas éditer la couche partagée à deux.
- **Incident branche** : un agent d'audit (go/no-go) peut laisser le repo sur `main` → on committe au
  mauvais endroit. **Toujours `git branch --show-current` avant edit/commit** ; les agents qui inspectent
  Git doivent **restaurer** la branche.

## Checklist de clôture « type fini »
- [ ] Tous les cas du canon **cartographiés** (matrice cas → documents).
- [ ] Tous les documents **générés fidèlement** par scénario (0 token résiduel), masculin **et** féminin.
- [ ] **Tous les cas générables depuis l'UI** + **bouton données de test** qui préremplit tout (1 clic).
- [ ] Garde-fous : cas coché sans données = bloqué ; pas de génération muette.
- [ ] `ruff` clean + **suite complète verte** (chiffres), **vérifiée soi-même**, sur la **bonne branche**.
- [ ] **Revue de fidélité** faite (pas d'auto-rapport).
- [ ] **Passe pré-shot UAT** faite : logo, alignements, puces/tirets, gras/souligné, noms de personnes
      complets, messages en français métier — conformes au modèle d'origine (rien à récolter en UAT).
- [ ] **From-scratch** : tout générateur from-scratch reproduit la mise en forme + le logo du modèle
      (sinon → template-fill).
- [ ] **Décisions ratifiées** au journal (codes stables) ; leçons reversées dans ce workflow.
- [ ] **Gate juridique** : points pour Rafael épuisés côté NotebookLM ; génération NO-GO tant que non
      validée par l'humain.
- [ ] Merge `main` + déploiement **laissés au PM**.
