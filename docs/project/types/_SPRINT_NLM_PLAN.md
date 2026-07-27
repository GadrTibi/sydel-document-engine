# Sprint NotebookLM — plan de passage des 6 types

> **Date :** 2026-06-07 · **Branche :** `sprint/engine-completion`
> **But.** Cadrer l'ordre de passage NotebookLM pour les 6 types restants à bâtir (moteur + UI), à
> partir des `NOTEBOOKLM_PROMPTS_V2.md` réellement créés sous `docs/project/types/<TYPE>/`.
> **Méthode de relais.** Coller **un seul prompt à la fois** dans NotebookLM, attendre la réponse, la
> coller dans le `NOTEBOOKLM_ANSWERS.md` du type concerné ; le Second la range ensuite dans le canon.
> **Garde-fou.** NotebookLM TOUJOURS avant Rafael. Ne JAMAIS poser une question métier à Gad
> (rule 20 — projet avec associé métier Rafael). Une info absente/contradictoire → message Rafael.

---

## 1. Ordre de passage

| # | Type | Prompts | Question / point bloquant en tête |
|---|------|:------:|-----------------------------------|
| 1 | **SELAS** | 16 | **Arbitrage Gad/produit (hors NotebookLM)** : le nouveau besoin « 2 à 5 associés + personne morale associée + DG » **contredit** le périmètre V1 « actionnaire unique » déjà ratifié. À trancher AVANT de tokeniser/coder : (a) V1 uni remplacée ou complétée par le multi ? (b) personne morale associée dans le périmètre V1 ? (c) DG en V1 ? (d) le cas Reynaud est-il LE modèle de référence ? Les prompts P-A préparent la matière, ils ne tranchent pas le périmètre. |
| 2 | **SPFPL** | 12 | **Prompt 1 BLOQUANT** : quelle version du canon « Documents à générer par cas » fait foi (la section SPFPL a été supprimée dans des versions ultérieures) + lever l'ambiguïté **parts vs actions** (forme de la SPFPL, et titres de la SEL sous-jacente). Ne pas coder avant sa réponse. |
| 3 | **SCM** | 18 | **Prompt 1 — carte officielle des cas absente du canon (100 % SELARL)** : envoyer le groupe « Cas → documents » EN PREMIER ; prompt 1 [Rafael] (NotebookLM ne l'a probablement pas) demande la carte « cas → documents » SCM. Sans cette carte, ni moteur ni UI. |
| 4 | **SCI** | 13 | **Prompt 1 BLOQUANT** : le bloc SCI du canon existe en V1 mais a **disparu en V2/V3** — trancher la version qui fait foi + confirmer le maintien de la SCI au périmètre Sydel. Modèle manquant « Lettre d'option IS » (prompt 10 → Rafael). |
| 5 | **SAS** | 11 | **Prompts 1-2 — aucune carte cas → documents SAS** (canon 100 % SELARL, 0 occurrence SAS/SASU/SPFPL) : toute cartographie actuelle est inférée, non ratifiée. Établir l'existence/le contenu de la carte + le périmètre (profession ; SELAS « exercice » vs SPFPL « holding »). |
| 6 | **SCP** | 19 | **Prompt 1 décisif (AVANT tout le reste)** : trancher ce qu'EST réellement le « SCP » de nos dossiers — société civile **professionnelle d'exercice** ou société civile **de portefeuille/patrimoniale** (l'objet du modèle ressemble à une société de participations). Tant que le type n'est pas identifié, ni moteur ni UI. |

---

## 2. Total des prompts

**89 prompts** au total sur les 6 types :

- SELAS : 16 (P-A 7 · P-B 3 · P-C 4 · P-D 2)
- SPFPL : 12 (Cas→docs 3 · Wording 6 · Genre/pluriel 1 · Multi 2)
- SCM : 18 (Cas→docs 7 · Wording 7 · Genre/pluriel 3 · Multi 1)
- SCI : 13 (Cas→docs 5 · Wording 5 · Genre/pluriel 2 · Multi 1)
- SAS : 11 (Cas→docs 4 · Wording 4 · Genre/pluriel 1 · Multi 2)
- SCP : 19 (Cas→docs 6 · Wording 9 · Genre/pluriel 3 · Multi 1)

> Note : plusieurs prompts sont taggés **[Rafael]** (filets de secours / modèles manquants) à n'envoyer
> que si NotebookLM reste muet — ils sont comptés dans les totaux ci-dessus.

---

## 3. Capture des réponses

Un fichier de capture vide a été créé par type — le PM y colle les réponses, le Second les range :

- `docs/project/types/SELAS/NOTEBOOKLM_ANSWERS.md`
- `docs/project/types/SPFPL/NOTEBOOKLM_ANSWERS.md`
- `docs/project/types/SCM/NOTEBOOKLM_ANSWERS.md`
- `docs/project/types/SCI/NOTEBOOKLM_ANSWERS.md`
- `docs/project/types/SAS/NOTEBOOKLM_ANSWERS.md`
- `docs/project/types/SCP/NOTEBOOKLM_ANSWERS.md`

Source de chaque jeu de prompts : `docs/project/types/<TYPE>/NOTEBOOKLM_PROMPTS_V2.md`.
