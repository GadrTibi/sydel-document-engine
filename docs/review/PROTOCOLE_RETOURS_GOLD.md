# Protocole RETOUR-GOLD — traitement déterministe d'une remarque

> But : quand Gad amène une remarque (Rafael / Albane / test live), il y a **une seule
> marche à suivre**, exécutée **sans re-réfléchir** à la méthode, avec des **vérifications
> dans tous les sens** pour que le résultat soit *parfait*. Ce document est le cerveau ;
> les workflows `audit-completude-types` et `audit-propagation-corrections` sont les bras.

## Principe fondateur (la règle d'or)

**Une remarque faite à UN endroit est une remarque faite à TOUS les endroits similaires.**
La SELARL validée est le *gold*. Tout type DÉRIVE du gold par différence justifiée. Un fix se
pose sur la **couche partagée** (front_widgets / générateur / modèle) pour se propager *par
construction*, jamais par recopie. Si on doit copier, c'est que la couche partagée manque —
on la crée.

## Les 6 phases (toujours dans cet ordre)

### Phase 0 — INTAKE (consigner avant de toucher au code)
- Chaque remarque → une ligne dans `docs/review/retours/REGISTRE_RETOURS.md` :
  `ID | source | date | cas d'origine | type | surface | scope attendu | statut`.
- `type` ∈ {bug, doc-manquant, champ-manquant, wording, mise-en-forme, logique-conditionnelle, encodage}.
- Verbatim de la remarque conservé (jamais reformuler une exigence métier).

### Phase 1 — CLASSIFY + GOLD-ANCHOR
- Identifier la **surface concrète** touchée (document(s), widget, règle).
- Regarder ce que fait le **gold SELARL** sur cette surface. Le gold est la référence ;
  si le gold est lui-même fautif (ex. mention d'épouse fantôme), le fix part DU gold.

### Phase 2 — SCOPE (propagation)
- Lister **TOUS** les types/cas partageant la surface = `scope attendu`.
  Types : SELARL, SCI, SCI IRIS, SCS, SCM, SAS, SPFPL cession, SPFPL apport, SELAS, SELAS uni médecin.
- Un doc partagé (tronc commun, satellite) → le fix vaut pour tous ses consommateurs.

### Phase 3 — IMPLEMENT sur la couche partagée
- Poser le fix au niveau le plus **commun** possible (front_widgets, générateur unique,
  modèle canonique). Différence par type = seulement si **justifiée métier**.
- Aucun wording juridique inventé ; il s'extrait des modèles source ou se confirme (registre).

### Phase 4 — VÉRIFIER DANS TOUS LES SENS (le cœur « c'est parfait »)
Cocher **toutes** les cases, pas une de moins :
1. **Suite verte** : `pytest -q --basetemp=artifacts/_audit_tmp/pt` + `ruff check`.
2. **Test de non-régression NEUF** par remarque (le bug ne peut pas revenir muet).
3. **Zéro placeholder** : aucun `[` / `]` résiduel dans les DOCX générés.
4. **Encodage / accents** : aucun accent cassé (mojibake), NFC cohérent.
5. **Logique conditionnelle** : aucune donnée fantôme (ex. épouse si non marié communauté).
6. **Propagation vérifiée** : relancer `audit-propagation-corrections` → la correction est
   présente dans **tout** le scope attendu (vérif adversariale des trous).
7. **Parité gold** : SELARL byte-stable là où on n'a pas voulu la changer.
8. **Canon à jour** : spec / matrice de parité / registre mis à jour si une règle a bougé.

### Phase 5 — REGISTER + CLORE
- `REGISTRE_RETOURS.md` : statut → `traité` + commit SHA + preuve de vérif (les cases Phase 4).
- Si la remarque révèle une règle transverse durable → la graver dans
  `METHODE_PARITE_GOLD.md` (les règles imposées) pour qu'elle devienne un invariant audité.

## Garde-fous (anti-rechute appris)
- **Pas d'opt-in silencieux sur un livrable attendu.** Si le canon dit « ça fait partie du
  dossier », le document se génère et ses champs sont VISIBLES — pas caché derrière une case
  décochée (leçon SCM frais communs / règlement, 2026-06-22 : Rafael « je ne vois pas les champs »).
- **Recouper toute affirmation forte d'un sous-agent** avant de la servir (règle 65).
- **Ne jamais annoncer un test non lancé.** Périmètre nommé.
- **Travailler dans le clone Claude** (`sydel-document-engine-claude`, `sprint/engine-completion`),
  jamais le clone primary.

## Invocation
- Commande : `/retour-gold` (colle les remarques → je déroule les 6 phases).
- Workflows de vérif réutilisables : `audit-completude-types`, `audit-propagation-corrections`.
