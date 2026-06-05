# Cartographie TENTATIVE des cas SCI (V1)

> ## ⚠️ CARTE OFFICIELLE cas→documents MANQUANTE — à confirmer NotebookLM/Rafael
>
> Le canon `project/source_truth/Documents_a_generer_par_cas_V3.docx` est **entièrement SELARL**
> (**vérifié : 23 mentions « SELARL », 0 mention « SCI »**). **Il n'existe AUCUNE carte officielle
> « cas SCI → documents »** dans les sources actuelles.
>
> Le regroupement ci-dessous est une **hypothèse de travail dérivée** (par analogie SEL + lecture du
> contenu des modèles). **`dérivé` ≠ `confirmé`.** Rien ci-dessous ne doit servir de base de génération
> tant que la liste des cas SCI et la carte cas→documents ne sont pas **confirmées par NotebookLM puis
> Rafael**. **Ne rien inventer au-delà de ce tableau** (pas de wording, pas de cas supplémentaire).

## Regroupement PROBABLE par cas (hypothèse, NON ratifié)

### Cas A — Création SCI (hypothèse principale)

| Document (modèle `sci/…`) | Spécifique SCI ? | Condition probable (à confirmer) |
|---|---|---|
| `Déclaration sur l_honneur de non condamnation - transforme.docx` | non (transverse « tous les cas ») | toujours, par dirigeant |
| `Autorisation de domiciliation - transforme.docx` | non (transverse « tous les cas ») | si siège domicilié chez un associé |
| `Procuration.docx` | non (transverse « tous les cas ») | si mandat pour les formalités |
| `Modèle statuts SCI.docx` | **oui** | SCI standard (par défaut) |
| `Modèle statuts SCI IRIS.docx` | **oui** | variante « IRIS » (personne morale associée / démembrement / quote-part) — **mutuellement exclusif** avec les statuts SCI standard ? *à confirmer* |
| `PV nomination gérant - transforme.docx` | non (identique à la version SELARL) | nomination du gérant (toujours ?) |

### Cas B — Option IS (sous-cas / option, hypothèse)

| Document | Spécifique SCI ? | Condition probable |
|---|---|---|
| `lettre option IS.docx` | non (partagé, `DOC-022`) | **si** la SCI opte pour l'impôt sur les sociétés |

### Variantes transverses pressenties (à confirmer)

- **Capital fixe vs variable** : `[mention_capital_variable]` présent dans les deux statuts → variante de saisie.
- **Nombre d'associés** : tokens `[…_personne_1..3]` → **plafond apparent de 3** associés personnes physiques ; comportement au-delà de 3 = **ouvert**.
- **Personne morale associée** : géré uniquement par la variante IRIS (`[…_societe_2]`).
- **Genre** : `[civilite]` / `[civilite_personne_n]` présents → couche genre à appliquer (cf. workflow Phase 5), wording exact des paires **à confirmer**.

## Ce qui N'EST PAS établi (et qu'on n'invente pas)

- La **liste exhaustive et officielle des cas SCI** (création seule ? cession de parts de SCI ?
  changement de gérant hors création ? régime communautaire ? dissolution ?). Le Drive ne contient
  qu'un dossier « Création SCI » → **rien ne prouve qu'il n'y a qu'un cas**, ni que ce cas est complet.
- Les **conditions exactes** de chaque document (obligatoire vs conditionnel, exclusivités).
- Le **sens métier de « IRIS »** et sa relation aux statuts SCI standard.
- L'existence éventuelle de **documents SCI manquants** (un cas peut exiger un document non fourni dans
  le Drive — piège déjà vu sur d'autres types).

➡️ Toutes ces inconnues sont formulées en questions prêtes à envoyer dans `NOTEBOOKLM_PROMPTS.md`.
