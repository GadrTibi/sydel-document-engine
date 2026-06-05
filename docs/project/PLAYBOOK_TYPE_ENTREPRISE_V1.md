# Playbook — Développer un type d'entreprise dans Sydel (V1, 2026-06-04)

> ➡️ **ÉLARGI par [`WORKFLOW_TYPE_ENTREPRISE_V1.md`](WORKFLOW_TYPE_ENTREPRISE_V1.md)** (le workflow A→Z
> définitif, **interface Streamlit comprise**, piloté par la commande **`/type-entreprise`**). Ce
> playbook reste le **résumé des principes** ; pour **dérouler** un nouveau type, suis le workflow.

**Recette réutilisable** pour outiller un type d'entreprise (SELARL, SELAS, SPFPL, SCI, SCS, SCP…).
But : **ne pas re-découvrir à chaque type** ce qu'on a appris. S'applique à **tout** type — SELARL en
cours **et SELAS de Naomi**. Mis en dur ici exprès. Complète `WORKFLOW_PRODUIT_SYDEL_V1.md`.

> Méta-règle : tout nouvel apprentissage de méthode pendant un type se reverse **ici** (rule 45 —
> codifier sans qu'on le demande), pour que le type suivant parte plus vite.

> ⛔ ABANDONNÉ pour la SELARL (décision Gad 2026-06-04) — La **SELARL reste unipersonnelle** : les
> couches/variantes « multi-associés » et « personne morale associée » évoquées ci-dessous **ne
> s'appliquent pas à la SELARL**. Elles **restent valables** pour la **SELAS** (multi-actionnaire,
> micro-holding) et les autres types (SCP/SCI/SCS/SPFPL).

## 0. Sources (avant tout code)
- Récupérer les modèles tokenisés du type dans le Drive **« Documents avec variables »** (toutes structures).
- **Dédupliquer** (un seul exemplaire par document) + **ranger par structure** dans `project/source_documents/lot_*` (du plus courant au moins courant).
- ⚠️ **Vérifier qu'on a TOUS les cas en lisant le CONTENU, pas le nom de fichier** : unipersonnel **ET** multi-associés. Le multi est souvent le cas courant ; certains modèles « unipersonnels » sont en fait des **multi adaptés** (comparution au singulier mais gouvernance déjà plurielle). Si un cas/fichier manque → **message Rafael** (demander le fichier, ne pas inventer).

## 1. Cartographie
- Inventaire « documents à générer par cas » (canon `Documents_a_generer_par_cas_V*`).
- Cartographier les **variantes** : genre, nombre/pluriel (multi-associés), **personne morale associée**, gérance (mono/co), régime communautaire, cession (cabinet + parts SCM), dérogations, site distinct.

## 2. Fidélité (règle d'or)
- Reconstruire par **REMPLISSAGE DE TEMPLATE** du modèle source tokenisé (`rendering/docx_template_fill.py`) ; **JAMAIS** de paraphrase du wording juridique.
- **Un générateur par document** + moteur partagé + sécurité anti-token-résiduel.
- Une règle **`dérivée`** (extrapolée d'un modèle frère) **n'est pas `confirmée`** tant qu'un humain n'a pas validé.

## 3. Règles juridiques (chaîne d'escalade)
`source_documents` → **NotebookLM** → **Rafael** (qui décide **seul** s'il sollicite **Albane**). **Claude ne contacte jamais Albane.**
- **Jamais inventer.** NotebookLM « NON TROUVÉ » → **message pour Rafael**.
- **Les réponses humaines ne sont PAS parole d'évangile** : analyser, signaler les imprécisions/sur-généralisations, préférer une **variable/préférence par personne** à une règle figée (ex. « le Docteur » = préférence par défaut, pas règle universelle ; « la Docteure » possible).

## 4. Couches transverses
- **Genre** : paires de chaînes **EXACTES** pilotées par le genre de la **bonne personne** ; **JAMAIS de regex de terminaison** (`-é/-ée`). Helper `utils/grammar.apply_gender_pairs`.
- **Nombre / pluriel (multi-associés)** : la **gouvernance** est souvent déjà plurielle dans le modèle ; seuls **4 endroits** sont à pluraliser → comparution (« LES SOUSSIGNÉS » + N), apports (art. 7, N + total), répartition (art. 8, tableau N), signatures (N). Wording à **dériver des modèles frères pluriels** (SCP/SCI/SCS + PV « plusieurs associés ») puis **valider Rafael**.
- **Personne morale associée** : collecter les **champs** (dénomination, forme, capital, RCS, SIREN, nb parts, représentant légal) ; le **wording statuts** est « ultra personnalisé » → **zone à valider/personnaliser**, pas inventer.

## 5. Vérification (avant de marquer « fait »)
- Tests **masculin ET féminin**, cas **uni ET multi**.
- **Revue `sachant-juridique` OBLIGATOIRE** (fidélité tokens vs modèle source). **Ne jamais se fier à l'auto-rapport** d'un agent/générateur : vérifier soi-même (ruff + pytest + ouvrir le DOCX généré).

## 6. Gate juridique (livraison)
- La **génération de documents reste NO-GO** tant qu'une **revue humaine** n'a pas tranché les points ouverts → **Pack de passation** (points formatés pour Rafael/Albane). La fondation technique peut être GO indépendamment.

## 7. Pièges techniques (Windows)
- pytest : `--basetemp` **hors repo** ; console cp1252 → `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` + **glob** pour les noms de fichiers **accentués** (ne pas hardcoder « Modèle… »).
- editable install : pointe vers le **repo d'origine** — `pyproject` `pythonpath=["src"]` met le clone courant en tête ; toute vérif hors pytest doit `sys.path.insert(0, "<clone>/src")`.
- **Plusieurs clones** sur la machine : **1 session Claude = 1 dossier** (éviter les collisions Git/fichiers entre sessions parallèles).

## 8. Sécurité Git / sessions
- 1 sprint = 1 branche dédiée (`<type>/...`), jamais `main` sans review du capitaine.
- Sessions parallèles (ex. SELARL + cockpit Naomi) = **dossiers séparés** ; ne pas éditer la **couche SEL partagée** depuis deux sessions en même temps (risque de collision, déjà constaté SELARL × SELAS).
