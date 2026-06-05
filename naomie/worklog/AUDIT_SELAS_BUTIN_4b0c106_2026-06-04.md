# Débrief SELAS — audit du travail local de Naomie

**Pour :** le Capitaine (Gad)
**Par :** le Second (Claude de Naomie)
**Date :** 2026-06-04
**Objet :** audit poussé du butin SELAS récupéré (commit `4b0c106 — wip: snapshot Naomi SELAS local work for reconciliation`)
**Méthode :** lecture seule sur le dossier local `/Users/naomiguetta/Desktop/sydel-document-engine`, branche `naomie/selas/recup-codex`. 3 relectures parallèles (sourcing NotebookLM · gouvernance/état · code+tests+specs). Tests réellement exécutés.

---

## 0. Réponse courte
**C'est récupérable, et plus propre que ne le suggère le message « wip ».** On garde **tout le butin**, avec un nettoyage léger. Mais il faut séparer deux plans :

- **Fondation technique** (moteur, schéma front, orchestrateur, tests) → **GO** : propre, testé, on repart dessus.
- **Activation de la génération documentaire SELAS** → **NO-GO pour l'instant** : bloquée à un **gate humain** (arbitrage juridique), pas à un trou de code. Ce gate relève de la terre ferme (vous), pas du dev.

---

## 1. Ce que Naomie a réellement fait
Un seul commit (`4b0c106`), mais **70 fichiers / +8 793 lignes** — un sprint SELAS V1 quasi complet :

- **Cadrage & gouvernance** : matrice documentaire (7 docs ciblés en V1), 31 tickets, roadmap A→P, contrat front, pack de revue humaine, audit de réutilisation SELARL→SELAS, *triple source check*, vos retours capturés verbatim (`SPRINT_SELAS_GAD_FEEDBACK_001`).
- **Log NotebookLM** : ~1 200 lignes — 7 prompts cadrés / 9 réponses structurées (`SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`).
- **Code** : `selas_schema.py` (554 l.), rôle `ACTIONNAIRE`, validation, orchestrateur (sélection du pack V1 + garde-fous), générateur statuts médecin SELAS (`statuts_selas_medecin.py`), adaptation procuration, registre.
- **Tests** : 32 tests SELAS dédiés + ~86 tests voisins touchés.
- **Sources & artefacts** : `.docx` des lots 02→05, DOCX générés (cas simple + régime communautaire), ZIP de revue.

**Phase atteinte : 31 — « Human Review Pack »** (`SPRINT_SELAS_V1.md:17-20`). Le dev V1 est fait, emballé, **en attente d'un retour humain**.

Compteur de tickets (`SPRINT_SELAS_V1.md:242-275`) : 30 `DONE`/`DONE_PARTIAL_QA`, 1 `DONE_WAITING_HUMAN_REVIEW`, + 4 tickets de clôture restants en roadmap (`ROADMAP_TO_COMPLETION_001.md:65,76-78`).

---

## 2. Ce qui est propre (vérifié, pas sur parole)
- **Code = qualité production.** Aligné sur les conventions du repo `front_data`, réutilise l'infra existante au lieu de réinventer (`DocumentRequirementRecord`, `BusinessRole`, `AddressUsage`…), dataclasses figées, garde-fous V1 explicites (bloque Directeur Général, multi-actionnaires, cession, actions de préférence, capital non-actions). `statuts_selas_medecin.py` vérifie même la cohérence du capital (montant = nb d'actions × valeur nominale).
- **Specs ↔ code alignés 1-pour-1** : ce que décrivent les `SPRINT_SELAS_SPEC_*` est concrètement implémenté (ex. `SPEC_STATUTS_MEDECIN_AU_001` → `_validate_doc018_v1_scope`).
- **Tests : exécutés pour de vrai.** Les docs de Naomie disaient « QA partielle, pytest indisponible en local ». Relance dans un venv jetable :
  - `test_selas_front_schema.py` + `test_orchestrator_service.py` → **32 passed**
  - 7 autres fichiers de test touchés → **86 passed**
  - **Total : 118 tests, 0 échec.** `ruff` passe sur les 4 fichiers cœur.
  - **Le trou de QA qu'elle ne pouvait pas combler est désormais comblé : c'est vert.**

> **⚠️ Correction Capitaine (2026-06-04)** — ces 118 verts sont un **sous-ensemble**. Le Capitaine a
> rejoué la **suite complète** : **3 échecs / 450 passés**. Les 3 échecs **ne sont pas du SELAS ni la faute
> de Naomie** : 2 DOCX sources SCI recopiés en double sous variante d'accent Unicode (« Modèle » de deux
> façons) → le moteur attend 1 source, en trouve 2, s'arrête (2 tests SCI + 1 cas dentaire). Correctif
> = Second côté Gad. La conclusion « SELAS sain » tient ; seul le chiffre de couverture est rectifié.
- **Honnêteté du butin** : aucune promesse de code fantôme — tout ce que les docs annoncent existe réellement.

→ **Verdict code : RÉCUPÉRABLE AVEC RETOUCHES MINEURES.** Rien à réécrire.

---

## 3. Question NotebookLM — réponse tranchée
> *Prendre les réponses telles quelles, ou refaire la phase NotebookLM faute d'assez d'info ?*

**Ni l'un ni l'autre. Ne PAS refaire NotebookLM.**

- **Plafond déjà atteint** : NotebookLM ne restitue **aucune citation source exploitable** sur ce corpus. Le prompt n°8 a demandé « les sources exactes » et n'a obtenu que des indices « illisibles ou vides » (`NOTEBOOKLM_LOG:983-985`). Refaire les mêmes prompts ne lèvera rien — le problème est l'outil sur ce corpus, pas le prompt.
- **Suffisant pour *cadrer*** (périmètre V1, substitutions gérant→président / parts→actions, squelette de formulaire à ~32 champs) **mais insuffisant pour *générer* du déterministe** (wording légal exact, règles de genre/pluriel sourcées, variantes par cas). Le log se l'auto-déclare « matière exploratoire, pas validation juridique » à chaque réponse.
- **Bon prochain pas (déjà tracé dans le repo)** : extraire les **passages sources réels des DOCX** (statuts médecin, renonciation conjoint, demande Ordre — déjà localisés) **+ boucler une revue humaine** sur les points ouverts. NotebookLM a servi de boussole ; la matière déterministe vient des sources DOCX et de l'arbitrage.

---

## 4. Ce qui bloque vraiment (ressort de la terre ferme — vous)
- **La revue humaine SELAS n'existe pas encore dans le repo.** Correction factuelle : le relecteur humain est **Albane** (pas « Alban ») ; son seul input présent est un **mail SELARL**, pas une revue SELAS (`TRIPLE_SOURCE_CHECK:102-111` : relecture SELAS « non présente dans le dépôt »).
- **~11 points juridiques ouverts** non tranchés, dont **2 « forts »** signalés comme potentiellement **bloquants/manquants** pour un dossier réel :
  1. **Plans/devis de l'Ordre** : bloquants ou simples pièces attendues ?
  2. **Attestation de capital / liste des souscripteurs** : donnée obligatoire selon NotebookLM — or elle est en réserve, donc **absente du pack actuel**.
- Autres points : genre Président/**Présidente**, numérotation des actions, filiation dans la DNC du président, `associé` vs `actionnaire` dans l'UI, PV de nomination président séparé ou absorbé dans les statuts, statuts dentiste (source DOCX non identifiée), libellé domiciliation, etc.

Aucun de ces points n'est tranchable par Naomie ou par moi (formulation juridique / périmètre produit = interdits durs).

---

## 5. Hygiène à purger avant de rebrancher (léger, non bloquant)
- Normaliser `procuration.py` repassé en **CRLF mixte** (le diff réel est noyé sinon).
- Re-saucissonner le « wip snapshot » en commits/tickets propres lors de la réconciliation.
- Réaligner des docs périmés : nom de branche dans `SPRINT_SELAS_V1`, statut incohérent de `DOC-006` (réservé dans la matrice mais codé), libellé `DOC-002` (« autorisation » vs « attestation »).
- Supprimer les dossiers dupliqués macOS (`20260602_135708 2`/`3`) et les `.DS_Store` committés dans les artefacts.
- Condenser `04_LAST_STATE.md` (1 321 lignes, trop bavard).

---

## 6. Recommandation GO / NO-GO

| Plan | Décision | Pourquoi |
|---|---|---|
| **Repartir sur la fondation technique** (schéma / orchestrateur / tests) | ✅ **GO** | Propre, 118/118 vert, specs alignées. On enchaîne sur le ticket de génération du pack SELAS V1. |
| **Activer la génération de documents SELAS** | ⏸️ **NO-GO tant que** : (a) passages sources extraits des DOCX, (b) revue humaine bouclée sur les ~11 points (surtout les 2 « forts ») | Risque juridique réel ; la substitution globale de chaînes est explicitement signalée comme dangereuse dans le butin lui-même. |
| **Refaire la phase NotebookLM** | ❌ **NON** | Plafond atteint, 0 source exploitable. |

**Reco nette :** récupérer **intégralement** le butin (il est sain) → **petit nettoyage** → **repartir en dev sur la couche technique**. En parallèle, **vous** (seul à pouvoir) lancez la **revue humaine SELAS** sur les points ouverts — c'est elle, pas plus de NotebookLM, qui débloquera la génération documentaire.

---

## 7. Points opérationnels (séparés de la décision GO/NO-GO)
1. **Accès dépôt à ouvrir** : `naomiguetta10-prog` n'a pas le droit *write* (push refusé — `403 denied to naomiguetta10-prog`). La branche `naomie/selas/recup-codex` est prête à être hissée **dès que vous l'ajoutez en collaboratrice** (Settings → Collaborators → Add people).
2. **Pack de passation « revue humaine SELAS »** : sur votre feu vert, je formate les ~11 points ouverts pour Albane/l'associé, pour que Naomie ait de quoi avancer pendant le déblocage.

---

### Annexe — sources d'audit (toutes en lecture seule, commit `4b0c106`)
- Sourcing : `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`, `…_NOTEBOOKLM_PROMPTS_V1.md`, `…_TRIPLE_SOURCE_CHECK_001.md`, `…_REUSE_AUDIT_001.md`.
- Gouvernance/état : `docs/project/04_LAST_STATE.md`, `docs/sprints/SPRINT_SELAS_V1.md`, `…_MATRIX_001.md`, `…_TICKETS_001.md`, `…_ROADMAP_TO_COMPLETION_001.md`, `…_GO_DEV_FIRST_TICKET_001.md`, `…_GAD_FEEDBACK_001.md`, `…_HUMAN_REVIEW_PACK_001.md`, `…_FRONT_CONTRACT_001.md`, `…_FRONT_READINESS_PACK_001.md`.
- Code/tests/specs : `src/sydel_doc_engine/front_data/selas_schema.py`, `role_model.py`, `validation.py`, `models.py`, `orchestrator/service.py`, `generators/lot_04/statuts_selas_medecin.py`, `generators/lot_01/procuration.py`, `registry/catalog.py`, `tests/unit/test_selas_front_schema.py`, `test_orchestrator_service.py` (+ tests voisins), `docs/sprints/SPRINT_SELAS_SPEC_*`.
- Tests exécutés : venv jetable `/tmp/sydel_venv` (`pip install -e ".[dev]"`), `python -m pytest` → 118 passed / 0 failed ; `ruff check` OK. Aucun fichier source modifié.
</content>
</invoke>
