# SCS — Cartographie tentative (cas → documents)

Date : 2026-06-07
Branche : `sprint/engine-completion`
Statut : **tentative** — à confirmer par NotebookLM + retour associé (Rafael). Aucune décision dev ici.

---

> ## ⚠️ BANDEAU : canon V1 vs V3 à trancher (bloquant)
>
> La SCS **figure dans le canon V1** (`project/source_truth/Documents_a_generer_par_cas.docx`)
> mais a été **entièrement RETIRÉE des canons V2 et V3**
> (`..._V2.docx`, `..._V3.docx`) — vérifié : zéro occurrence de « SCS » dans V2 et V3.
>
> C'est **exactement le précédent SPFPL** : un type présent en V1, absent des versions récentes du canon.
> Le canon V3 se réorganise autour de la SELARL (cas « dans tous les cas », « Si SELARL », « Si SCM
> cession », « Si régime communautaire »…) et **ne traite plus la SCS comme une structure autonome**.
>
> **Question à trancher AVANT tout dev SCS :** quelle version du canon fait foi pour la SCS ?
> - (A) V1 fait foi → la SCS est un type à part entière à générer (5 documents, voir ci-dessous) ;
> - (B) V3 fait foi → la SCS est **hors périmètre produit** (retirée volontairement) → NO-GO dev ;
> - (C) la SCS n'apparaît qu'en **sous-cas** d'un autre montage (ex. holding commanditaire d'une SEL) → cadrer le rattachement.
>
> Tant que ce point n'est pas tranché par l'associé (via Gad), le statut reste **NO-GO dev**.
> C'est le **prompt n.1** de `NOTEBOOKLM_PROMPTS_V2.md`.

---

## Carte officielle V1 (source de vérité historique)

Section `SCS` du canon V1 (`Documents_a_generer_par_cas.docx`), recopiée fidèlement :

| Document V1 | Modèle source cité par le canon V1 |
| --- | --- |
| Statuts SCS | `Statuts_SCS_modele.docx` |
| Déclaration sur l'honneur de non condamnation | `Déclaration sur l'honneur de non condamnation.docx` |
| Autorisation de domiciliation | `Autorisation de domiciliation.docx` |
| Procuration | `Procuration.docx` |
| PV nomination gérant | `PV nomination gérant.docx` |

Le canon V1 précise aussi (section « La liste des souscripteurs ») :
**« Cela concerne les SPFPL, SELAS et SCS »** → une *liste des souscripteurs* peut être attendue pour la SCS.
À confirmer (présente dans la carte V1 « cas → documents » uniquement de façon indirecte).

Note : les 4 documents communs (déclaration non condamnation, autorisation de domiciliation,
procuration, PV nomination gérant) sont **transverses** et déjà traités côté SELARL / global → fort
potentiel de réutilisation (voir `STATUT.md`).

## Regroupement par cas probable (à confirmer NotebookLM)

La SCS distingue toujours deux rôles d'associés (art. L.222-1 C. com., rappelé dans le RM) :
- **associé commandité** : gère, responsabilité indéfinie et solidaire (≈ le gérant) ;
- **associé commanditaire** : apporteur/investisseur, responsabilité limitée à ses apports.
Minimum **2 associés** : au moins 1 commandité + au moins 1 commanditaire.

Les 3 modèles de statuts correspondent à **3 montages distincts** (cf. INVENTAIRE) :

### Cas 1 — SCS « simple » 2 personnes physiques, capital variable
- Modèle : `Statuts_SCS_modele.docx` (= modèle moteur actuel DOC-019).
- Commandité = personne physique ; commanditaire = personne physique.
- Documents probables : Statuts SCS + les 4 transverses (V1).

### Cas 2 — SCS avec holding commanditaire (capital fixe)
- Modèle : `Statuts_SCSS_SYDEL_modele.docx`.
- Commandité = personne physique ; commanditaire = **société** (micro-holding).
- C'est le montage décrit dans le **rapport de mission** (`RM_Sydel_SCS_modele`) :
  « vous serez l'associé commandité… votre société micro holding sera l'associé commanditaire ».
- Documents probables : Statuts SCS (variante holding) + 4 transverses + **rapport de mission** + éventuelle liste des souscripteurs.

### Cas 3 — SCS mixte (société + 2 personnes physiques)
- Modèle : `SCS_modele_chenal_modele.docx`.
- Commandité = personne physique ; commanditaires = 1 société + 1 personne physique.
- Variante à 3 associés du cas 2.

### Document transverse possible — Rapport de mission SCS
- Modèle : `RM_Sydel_SCS_modele.docx`.
- N'est **pas** dans la carte V1 « cas → documents ». C'est un livrable de **conseil patrimonial**
  (pas un acte de constitution). À classer : document métier additionnel (probablement « manuel » ou
  hors carte officielle) — à confirmer avec l'associé.
- ⚠️ wording : contient un résidu « Société Civile Immobilière » (copier-coller depuis un RM SCI) à corriger.

## Écart détecté entre les modèles et le moteur actuel

Le moteur (`registry/catalog.py`, DOC-019) décrit la SCS comme :
`dynamic_associates=True`, `associes[] entre 1 et 6`, « roles commandite et commanditaire explicites »,
`workflow_status=TESTE`. Or les modèles de statuts décrivent des montages **2 à 3 associés à rôles fixes**
(1 commandité + 1-2 commanditaires), pas une plage libre 1–6. À réconcilier (cf. `STATUT.md`).

## Sources lues pour cette cartographie

- `project/source_truth/Documents_a_generer_par_cas.docx` (V1) — section SCS.
- `project/source_truth/Documents_a_generer_par_cas_V2.docx` (V2) — SCS absente.
- `project/source_truth/Documents_a_generer_par_cas_V3.docx` (V3) — SCS absente.
- 4 modèles `project/source_documents/scs/*.docx`.
- Moteur : `src/sydel_doc_engine/registry/catalog.py`, `domain/case_catalog.py`,
  `generators/lot_04/statuts_scs.py`.
