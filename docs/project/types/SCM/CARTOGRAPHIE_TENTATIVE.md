# SCM — Cartographie TENTATIVE des cas (V1)

> ## ⚠️ CARTE OFFICIELLE « cas → documents » **MANQUANTE**
> Le canon `project/source_truth/Documents_a_generer_par_cas_V3.docx` est **entièrement SELARL**.
> La SCM n'y figure **que comme sous-cas d'une cession de SELARL** (« Si SCM » / « Si SCM Cession » :
> cession de parts de SCM **vers** la SELARL — `PV AGE cession part SCM`, `Courrier SDE`,
> `Acte de cession des parts de la SCM à la SELARL`). **Il n'existe AUCUNE carte « créer une SCM »
> en tant que type d'entreprise autonome.**
>
> **Tout regroupement ci-dessous est PROBABLE (`dérivé`), reconstruit à partir des seuls modèles
> Drive — pas du canon. À CONFIRMER par NotebookLM puis Rafael avant tout code.** Voir
> `NOTEBOOKLM_PROMPTS.md` (bloc 1 = obtenir la liste officielle des cas SCM).

---

## Ce dont on dispose réellement

- **11 modèles tokenisés** (cf. `INVENTAIRE_MODELES.md`) issus du dossier Drive « création scm ».
- **Aucune liste de cas**, aucune règle « tel cas → tels documents », aucun retour humain (lock) propre
  à la SCM.

## Regroupement PROBABLE par cas (hypothèse de travail — NON ratifiée)

> Légende statut : `dérivé` = déduit des modèles, jamais confirmé.

### Cas A — « Création d'une SCM » (hypothèse principale) — `dérivé`
Documents qui semblent constitutifs d'une SCM nouvelle :
| Document (modèle) | Rôle présumé |
|---|---|
| `Statuts SCM.docx` | Acte constitutif. |
| `PV nomination gerant SCM.docx` | Nomination du gérant. |
| `Autorisation de domiciliation SCM.docx` | Domiciliation du siège (commun). |
| `Declaration non condamnation SCM.docx` | Déclaration de non-condamnation (commun). |
| `Procuration SCM.docx` | Mandat formalités (commun). |
| `Fiche de creation SCM.docx` | Fiche récap interne (à confirmer : livrable client ou outil interne ?). |

**Ouvert :** demande d'inscription à l'ordre ? (présente pour la SELARL ; **absente** du dossier Drive
SCM — ne pas l'ajouter sans confirmation). Régime communautaire / conjoint ? (lettres de renonciation
et d'avertissement **absentes** du dossier SCM).

### Cas B — « Conventions entre associés / fonctionnement » (hypothèse) — `dérivé`
Documents qui organisent la vie de la SCM et le partage des frais :
| Document (modèle) | Rôle présumé |
|---|---|
| `Pacte d_associes SCM.docx` | Pacte d'associés. |
| `Reglement interieur SCM.docx` | Règlement intérieur (dépenses communes, responsabilités). |
| `Contrat frais communs SCM.docx` | Répartition des frais communs entre les SEL des associés. |
| `Liste depenses communes SCM.doc` | Annexe liste des dépenses communes (`.doc` legacy). |

**Ouvert :** ce cas est-il **toujours** émis avec la création, ou **optionnel** (« si pacte »,
« si contrat de frais communs ») ? Combien d'associés (les modèles supposent **2** associés/2 sociétés ;
le `variables.csv` Drive descend jusqu'à `_societe_3` → possibilité de 3) ?

### Cas C — « Bail » (hypothèse) — `dérivé`
| Document (modèle) | Rôle présumé |
|---|---|
| `Avenant contrat de bail SCM.docx` | Avenant au bail (changement de locataire vers la SCM). |

**Ouvert :** condition d'émission (« si la SCM reprend un bail existant » ?). Recouvre la trame de
l'avenant de bail SELARL → **doublon de couche partagée** probable.

### Cas D — « Cession de parts de SCM » — **déjà cartographié côté SELARL**, PAS un cas SCM autonome
Le canon traite ce cas **dans le dossier SELARL** (`PV AGE cession part SCM`, `Courrier SDE`,
`Acte de cession des parts de la SCM à la SELARL`). Codex l'a déjà implémenté dans `lot_05`
(structures `SELARL`/`SELAS`). **À ne PAS recréer sous le type SCM** : risque de doublon. À clarifier
avec Rafael si une cession de parts de SCM existe **hors** contexte SELARL/SELAS.

---

## Divergence détectée avec le code existant (à arbitrer)

Codex a **déjà** posé dans `src/.../domain/case_catalog.py` (lignes ~701-713) un `CaseType.SCM`
listant : `statuts_scm`, `declaration_non_condamnation`, `autorisation_domiciliation`, `procuration`,
`pv_nomination_gerant`, `demande_inscription_ordre`, `pacte_associes_scm`, `liste_depenses_communes_scm`,
`contrat_frais_communs_scm`, `reglement_interieur_scm`.

- Cette liste est une **extrapolation Codex**, **NON adossée au canon** (aucune carte SCM dans
  `Documents_a_generer_par_cas_V3.docx`).
- Elle inclut `demande_inscription_ordre` **alors que ce modèle est ABSENT du dossier Drive SCM** →
  signal d'invention possible.
- Elle ne distingue pas obligatoire vs optionnel, ni le nombre d'associés.

**→ Cette liste sert d'hypothèse à challenger, pas de vérité.** La carte officielle doit venir de
NotebookLM/Rafael (bloc 1 des prompts).
