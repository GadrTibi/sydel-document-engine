# INTEL GATE — porte d'accès aux sources de vérité (V1)

> **Quand l'appliquer :** AVANT de poser/transmettre la moindre question à une **source de vérité**
> (NotebookLM, Rafael, plus tard Albane), et **obligatoirement dans tout workflow** qui transmet ou
> questionne une de ces sources. But : ne jamais demander ce qu'on a déjà, ni la mauvaise question à
> la mauvaise source. (Né de 3 ratés 2026-06-07 où Gad « passait pour un con » devant Rafael.)

## Le gate — 4 étapes, dans l'ordre, AVANT toute question

**1. INVENTAIRE D'ABORD (a-t-on déjà la réponse ?)**
Chercher dans nos propres actifs avant de demander à qui que ce soit :
- modèles : `find project/source_documents -iname "*<mot>*"` (tous dossiers, `.doc` ET `.docx`) ;
- docs/specs : `grep` dans `docs/` ; code : `grep` dans `src/`.
→ Si la réponse y est : **STOP, on l'utilise.** On ne demande pas.

**2. CLASSER LA QUESTION (de quel type est-elle ?)**
| Type de besoin | Source = | Action |
| :--- | :--- | :--- |
| **Wording / texte** d'un document (comparution, articles, accords…) | **le modèle `.docx`** | **l'extraire soi-même** (python-docx). JAMAIS demander à un humain de recopier un doc qu'on tient. |
| **Règle / pratique métier** non écrite dans un modèle (quels cas, quand tel doc, usage cabinet) | **Rafael** (ou NotebookLM si c'est sourçable dans le corpus) | poser, court, métier |
| **Décision de périmètre / produit** (garder SCP ? scope SELAS ? quels cas en V1 ?) | **Gad** | jamais Rafael |
| **Validation humaine / juridique** hors corpus | Rafael → (Albane via Rafael) | seulement après 1 et 2 |

**3. BONNE QUESTION À LA BONNE SOURCE**
Ne demander QUE ce qui est (a) absent de nos actifs (étape 1) ET (b) du domaine de cette source
(étape 2). Ne jamais router du **wording** vers un humain ; ne jamais router une **décision de scope**
vers Rafael.

**4. PAS DE BATCH NON MÛRI**
Ne rien faire relayer à Gad avant d'avoir passé 1→3. Prévenir Gad **avant** toute transmission à une
source externe ; lui soumettre les **décisions** à lui, jamais en vrac à Rafael.

## Contrôle (le gate a-t-il été respecté ?)
- Si la source répond « **c'est dans les docs / pas pour moi / trop technique** » → le gate a été **sauté**.
- Avant d'affirmer qu'un doc/modèle « manque » : l'avoir cherché soi-même (`find`) sur le **bon clone**.

## Liens
Opérationnalise la règle globale `~/.claude/rules/20-product-alignment.md` (volet « associé métier »).
Mémoires liées : `feedback-extract-from-models-not-rafael`, `feedback-no-rafael-relay-build-first`,
`trap-false-missing-from-wrong-clone`. À invoquer dans `WORKFLOW_TYPE_ENTREPRISE_V1` (phase recueil).
