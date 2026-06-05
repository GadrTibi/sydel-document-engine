# EURL — Cartographie tentative des cas → documents

> ╔══════════════════════════════════════════════════════════════════════════════╗
> ║  CARTE OFFICIELLE « CAS → DOCUMENTS » **MANQUANTE** POUR L'EURL.                ║
> ║  À CONFIRMER PAR NOTEBOOKLM / RAFAEL AVANT TOUTE IMPLÉMENTATION.                ║
> ║  Le canon `project/source_truth/Documents_a_generer_par_cas_V3.docx` est        ║
> ║  ENTIÈREMENT SELARL (SELARL ×23, EURL ×0). Aucun cas EURL n'y existe.            ║
> ║  Rien ci-dessous n'est ratifié. NE PAS coder sur cette base.                    ║
> ╚══════════════════════════════════════════════════════════════════════════════╝

## Pourquoi cette page existe

Il n'existe **aucun** des deux intrants nécessaires à une cartographie réelle :
1. **0 modèle EURL** tokenisé sur le Drive (cf. `INVENTAIRE_MODELES.md`).
2. **0 carte officielle** cas→documents pour l'EURL dans le canon (le canon est SELARL).

Cette page ne fait donc **que poser des hypothèses de travail** pour cadrer les questions
NotebookLM/Rafael. **Aucun cas, aucun document, aucun wording n'est inventé comme acquis.** Chaque
ligne est marquée `assumption` ou `open`.

## Regroupement PROBABLE par cas (hypothèses non ratifiées)

> Calque dérivé de la structure SELARL (type SEL de référence dans le projet) **par analogie
> uniquement**. L'EURL est une **société commerciale unipersonnelle (1 seul associé)** — pas une SEL.
> Donc la liste SELARL n'est probablement **PAS** transposable telle quelle. À confirmer entièrement.

| Cas probable | Documents qu'on POURRAIT s'attendre à trouver | Classification | Note |
|---|---|---|---|
| **Création EURL** | statuts EURL ; PV / décision de l'associé unique ; autorisation de domiciliation ; déclaration sur l'honneur de non-condamnation ; procuration ; (option IS ?) | `assumption` | Aucun modèle EURL présent ; libellés non confirmés. |
| **Régime matrimonial** | avertissement / renonciation du conjoint si bien commun apporté | `open` | Pertinence pour une EURL à confirmer (l'associé unique). |
| **Apport / cession de fonds** | acte d'apport ou de cession du fonds ; avenant de bail ; appel de fonds | `open` | Existe-t-il une opération d'apport/cession dans le périmètre EURL de Sydel ? Inconnu. |
| **Régime fiscal (IR/IS)** | lettre d'option à l'IS | `open` | Spécificité EURL (par défaut IR, option IS possible). Un `lettre option IS.docx` existe sur le Drive mais **non rattaché EURL** — à confirmer. |
| **Gérance** | acte de nomination du gérant (associé unique gérant vs gérant tiers) | `open` | Structure de gérance EURL à confirmer. |
| **Inscription Ordre / professions de santé** | demande d'inscription à l'Ordre, dérogations | `open` | L'EURL est-elle utilisée par Sydel pour des **professions de santé** (comme la SEL) ou pour une activité commerciale classique ? **Question structurante non tranchée.** |

## Ce qui est CONFIRMÉ (factuel, vérifiable dans le repo)

- L'EURL n'est **pas** dans l'enum `CaseType` (`src/sydel_doc_engine/domain/case_catalog.py` :
  SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI, SCM, SAS — **pas EURL**).
- Aucun modèle, aucune fixture, aucun générateur, aucune slice UI EURL n'existe dans `src/`.
- Le canon cas→documents est SELARL.

## Ce qu'il faut OBTENIR avant de cartographier pour de vrai

1. La **liste exhaustive des cas EURL** tels que Sydel les traite (création seule ? apport/cession ?
   transformation ? professions de santé ou commercial ?).
2. La **carte officielle cas → documents** par cas (l'équivalent EURL de
   `Documents_a_generer_par_cas_V3.docx`).
3. Les **modèles `.docx` tokenisés** correspondants.

Ces trois points sont portés par les prompts de `NOTEBOOKLM_PROMPTS.md`. Tant qu'ils ne sont pas
ratifiés, la phase 2 du workflow (cartographie) reste **bloquée**.
