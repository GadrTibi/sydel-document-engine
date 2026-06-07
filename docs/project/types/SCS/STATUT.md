# SCS — Statut de fondation

Date : 2026-06-07
Branche : `sprint/engine-completion`
Décision dev courante : **NO-GO dev** (canon V1/V3 à trancher — voir bandeau de `CARTOGRAPHIE_TENTATIVE.md`).

> Note méthode : le prompt référence `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`, qui **n'existe pas**
> dans ce repo. Le workflow réel est `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`
> (méthode A→Z type d'entreprise), appuyé par `SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` et
> `REUSE_AUDIT_AGENT_PROTOCOL_V1.md`. Le plan de fondation ci-dessous s'appuie sur ce playbook.

## Ce que Codex a déjà fait pour la SCS dans `src/` (grep — à re-vérifier)

La SCS est **partiellement câblée dans le moteur** (contrairement à la SPFPL retirée). Trouvé :

| Emplacement | Contenu |
| --- | --- |
| `src/sydel_doc_engine/domain/case_catalog.py:14` | `SCS = "SCS"` dans l'enum `CaseType`. |
| `src/sydel_doc_engine/domain/case_catalog.py:337-339` | Doc `statuts_scs` / "Statuts SCS" / `Statuts_SCS_modele.docx`. |
| `src/sydel_doc_engine/domain/case_catalog.py:687-692` | 5 `DocumentOccurrence` SCS : `statuts_scs`, `declaration_non_condamnation`, `autorisation_domiciliation`, `procuration`, `pv_nomination_gerant` — **identiques à la carte V1**. |
| `src/sydel_doc_engine/registry/catalog.py:11,23,75-76` | `SCS` dans les listes de structures + `STATUTS_CIVILS_SCS_STRUCTURES`. |
| `src/sydel_doc_engine/registry/catalog.py:572-591` | `DocumentDefinition` DOC-019 « Statuts SCS », `generator_name=generate_statuts_scs`, lot 4, `source_path=project/source_documents/lot_04/Statuts_SCS_modele.docx`, `workflow_status=TESTE`, `dynamic_associates=True`, conditions « associes[] entre 1 et 6 ». |
| `src/sydel_doc_engine/generators/lot_04/statuts_scs.py` | Générateur `StatutsScsGenerator` → délègue à `generate_statuts_civil_docx(..., SCS_TEMPLATE)` (commun aux statuts civils). |
| `src/sydel_doc_engine/generators/lot_04/statuts_civils_common.py` | `SCS_TEMPLATE` + logique commune statuts civils (SCS/SCI/SCM). |
| `src/sydel_doc_engine/orchestrator/service.py:54,144,196` | Import du générateur + mapping `DOC-019 -> scs` + instanciation `StatutsScsGenerator()`. |

> À re-vérifier (grep, non exécuté en test ici) : que `generate_statuts_civil_docx` + `SCS_TEMPLATE`
> produisent réellement un DOCX SCS fidèle, et que `workflow_status=TESTE` est justifié par un test
> existant. Le présent ticket n'exécute **aucun test** et ne touche **aucun code**.

## Ce qui manque

1. **Décision canon V1/V3** (bloquant) — la SCS doit-elle exister comme type ? (prompt n.1).
2. **Sources NotebookLM** : aucune réponse capturée pour la SCS (fichier `NOTEBOOKLM_ANSWERS.md` vide).
3. **Retour humain associé (Rafael)** : pas de lock humain SCS (à comparer aux `*_HUMAN_REFERENCE_LOCK`).
4. **Réconciliation modèle ↔ moteur** : le moteur déclare `associes[] entre 1 et 6` / `dynamic_associates=True`,
   alors que les modèles décrivent des montages **2-3 associés à rôles fixes** (1 commandité + 1-2 commanditaires)
   et une distinction **personne physique vs société commanditaire** non reflétée. Drift à arbitrer.
5. **Modèles non sourcés** : `Statuts_SCSS_SYDEL_modele`, `SCS_modele_chenal_modele`, `RM_Sydel_SCS_modele`
   sont copiés dans `project/source_documents/scs/` mais **pas branchés au moteur** (le moteur n'utilise que
   `Statuts_SCS_modele.docx`). Décider s'ils deviennent des variantes générables.
6. **Capital variable vs fixe** : le modèle moteur est à capital variable ; les 2 autres à capital fixe. Non tranché.
7. **Rapport de mission** : ni câblé, ni classé (manuel ? généré ? hors carte V1 ?).
8. **Wording artefact** : « Société Civile Immobilière » résiduel dans le RM (à corriger côté métier).
9. **Documents transverses** : déclaration non condamnation / autorisation domiciliation / procuration /
   PV nomination gérant — à confirmer comme réutilisés du socle SELARL/global (audit de réutilisation non fait).

## Plan de fondation ordonné (cf. COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md)

> Tout reste en **NO-GO dev** tant que l'étape 1 n'est pas tranchée.

1. **Trancher le canon (prompt n.1)** — associé via Gad. Si V3 fait foi et retire la SCS → arrêter, classer
   la SCS « hors périmètre produit » (et décider du sort du code DOC-019 déjà présent). Si V1/sous-cas →
   continuer.
2. **Boucle NotebookLM** (Phase 2 playbook) — dérouler `NOTEBOOKLM_PROMPTS_V2.md`, capturer dans
   `NOTEBOOKLM_ANSWERS.md`, structurer un journal SCS. Boucler jusqu'à couverture suffisante
   (documents attendus, conditions, montages, wording, accords).
3. **Triangulation 3 sources** (Phase 1/2) — canon V1 + NotebookLM/modèles + retour associé. Tableau
   des contradictions et `non trouvé`.
4. **Audit de réutilisation** (`REUSE_AUDIT_AGENT_PROTOCOL_V1.md`) — classer chaque document
   `identique / reuse-check / adapter / no-go` vs SELARL/global (les 4 transverses sont a priori `reuse`).
5. **Matrice documentaire SCS** (Phase 3) — cas → documents → code → statut source/moteur/front → décision.
6. **Réconcilier moteur ↔ modèles** — corriger la définition DOC-019 (plage d'associés, rôles fixes,
   variante société commanditaire, capital fixe/variable) selon la matrice.
7. **Contrat métier-front** (Phase 4) — blocs de saisie : société, associé commandité, associé(s)
   commanditaire(s) personne/société, apports, parts ; dédup front.
8. **Plan de sprint + tickets bornés** (Phase 5) — `GO dev` seulement sur le 1er ticket prêt.
9. **Implémentation bornée → smoke → test associé → clôture canonique** (Phases 6-10).

## Sources de cette fiche

- `src/` (grep SCS, non exécuté en test).
- `project/source_truth/Documents_a_generer_par_cas{,_V2,_V3}.docx`.
- `project/source_documents/scs/*.docx`.
- `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`.
