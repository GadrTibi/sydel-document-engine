# Journal de décisions — SELARL (V1, 2026-06-05)

Décisions produit/métier **ratifiées**, à code stable. Source de vérité durable (ne pas enterrer en chat).
Les décisions de **méthode / comportement d'agent** vont au bilan DRH (`method-steward`), pas ici.

| Code | Décision | Source | Statut |
|---|---|---|---|
| **SELARL-SCOPE-1** | La SELARL est **UNIPERSONNELLE**. Multi-associés + associé personne morale **ABANDONNÉS**. | Gad 2026-06-04 | acté |
| **SELARL-D1** | Une personne morale **peut** être associée d'une SELARL (le canon « société associée » est correct légalement, NotebookLM). **Mais hors périmètre V1** (cf. SCOPE-1). | NotebookLM 2026-06-04 | acté → **superseded** par SCOPE-1 pour la V1 |
| **SELARL-DUR-1** | Durée de la **SOCIÉTÉ** (statuts art. 6) = « **99 ans** », **figée en dur** (pas une variable). | retour humain 006 (02/06) | appliqué |
| **SELARL-DUR-2** | **Autorisation de domiciliation** = « pour une **durée indéterminée** ». L'amendement « 99 ans » (03/06) était **ERRONÉ** (contredisait la source humaine primaire du 31/05). | Retours humains 31/05 | appliqué |
| **SELARL-ORIG-1** | **Origine de propriété** (cession) décrit le **VENDEUR** (créé par défaut, ou acheté). Cas complexes → relecture humaine (garde-fou). | NotebookLM 2026-06-05 | appliqué |
| **SELARL-SAL-1** | **Reprise des salariés** (cession) : 0 → « Néant. » ; 1..N → liste nom/prénom/poste. | NotebookLM 2026-06-05 | appliqué |
| **SELARL-CV-1** | **Crédit-vendeur** : unité = **années**. Taux 5 % conservé tel quel (fixe/variable non tranché). | NotebookLM 2026-06-05 | appliqué (taux = dette mineure) |
| **SELARL-AF-1** | **Appel de fonds** = **COMMUN à toute cession** (médical + dentaire). Le « dentaire-only » était une **dérive du canon**. | canon « Si cession » + NotebookLM (coquilles) | appliqué |
| **SELARL-GENRE-1** | « **Docteur** » invariant (« le Docteur », même au féminin) ; « la Docteure » = préférence par personne, **future**. Couche genre (soussigné/né/associé) appliquée. | Rafael 2026-06-04 | appliqué |
| **SELARL-FID-1** | **Fidélité** : remplissage de template du modèle source tokenisé, jamais de paraphrase/invention ; corrections = lock humain. Cas complexes/« ultra personnalisés » → garde + relecture humaine. | ADR-0004 | en vigueur |

## Lot post-réunion 2026-06-09 (multi-type : SCI / SCI IRIS / SCS / SELAS)
1re validation humaine (Albane + David). Constructible **livré et testé** ; juridique fin = en attente
des cas concrets de Rafael (cf. `_RAFAEL_PACKET_V1.md`, `_REUNION_2026-06-09_ALBANE_DAVID.md`).

| Code | Décision | Source | Statut |
|---|---|---|---|
| **MULTI-N-1** | Les types multi-associés (SCI, SCI IRIS, SCS, SELAS) gèrent **N associés** (bornes nommées : civils 1–2 → 6 ; SELAS 2 → 5) ; statuts / PV / annexes s'adaptent. Prouvé par tests à 3 et 5. | Réunion 2026-06-09 | appliqué (`sprint/engine-completion`) |
| **DIRIGEANT-1** | **Associé ≠ dirigeant** : case « Dirigeant » par associé physique → choix du président (SELAS). Rôle limité à **« Président »** ; **DG / DG délégué = en attente wording Rafael** (aucun modèle source ne le porte → pas d'invention). | Réunion 2026-06-09 | appliqué (président) / **open** (DG) |
| **DNC-COND-1** | Les champs **DNC + filiation** ne sont demandés **que pour l'associé coché dirigeant** (saisis sous lui, plus de bloc signataire séparé). **Défaut documenté** : « dirigeant coché ». Règle exacte (dirigeant seul vs tout associé) = **en attente Rafael**. | Réunion 2026-06-09 | appliqué (défaut) / **open** (règle) |
| **NO-RETRO-1** | **Pas de mise à jour rétroactive** des dossiers historiques : produire les bons docs **à la création** (aligné V1 = création). | Réunion 2026-06-09 | acté |
| **SCM-SAT-N** | Satellites SCM (pacte DOC-026 + liste dépenses DOC-030) **verrouillés à exactement 2 associés** (modèles bâtis pour 2) ; à N>2 ils disparaissent, le bundle de base reste propre. Généraliser = **FLAG Rafael**. | Rafael 2026-06-08 + plan | acté (verrou testé) |

## Dettes mineures (non bloquantes)
- Champ `CessionValidations.salaries_dentaire_deux_valides` non enforced → à retirer lors d'un nettoyage.
- Appel de fonds : préposition « exploité **au** » + « **Cher Monsieur** » figé — **non sourcés** (NotebookLM/Rafael si on veut peaufiner ; cosmétique).
- `date_entree_jouissance` (dentaire) : commentaire « à confirmer côté métier » préexistant.

## Périmètre livré (réf.)
SELARL **unipersonnelle** : création (statuts médecin/dentiste, PV gérant, autorisation, déclaration, procuration, demande ordre, régime communautaire) + cession (cabinet médical/dentaire acte+compromis, parts SCM, avenant bail, appel de fonds commun). 325 tests verts sur `review/selarl`.
