# Méga-sprint « tous les types » — tableau de bord (le Manifeste)

> **But.** Finir le moteur pour TOUS les types d'entreprise d'un coup, en **roulement parallèle** :
> pendant que le capitaine (Gad) colle les prompts dans NotebookLM, le Second (Jinbe) range les
> réponses précédentes ET lance les équipes de développement sur ce qui est déjà constructible.
> **Branche :** `sprint/engine-completion`. **Validation finale :** Rafael (groupée, à la fin).
> **Garde-fous durs :** aucun merge `main`, aucun déploiement, aucune écriture juridique inventée,
> aucun contact externe — sans GO Gad.

Types du sprint (EURL hors périmètre) : **SELAS · SPFPL · SCM · SCI · SCS · SCP · SAS**.

> ⚠️ **GOUVERNANCE CODEX (Gad, 2026-06-07).** Une grande partie de l'app a été bâtie par **Codex**
> depuis le seul doc « Documents à générer », **avant NotebookLM** : les moteurs par type
> (`statuts_*`, commits **mai 2026**) existent mais **ne sont pas validés**. **L'app ne garde QUE** ce
> que Claude Code + Gad ont **développé/validé ensemble** (réf. SELARL) ou de l'antérieur
> **explicitement validé**. Donc « le moteur existe / les tests passent » **≠ prêt** : chaque type
> passe une **passe d'audit de fidélité** (sortie Codex vs synthèse NotebookLM + modèle source +
> Rafael) avant câblage/livraison. Détail : [[governance-codex-suspect-until-validated]].

---

## Deux voies, en roulement

- **Voie A — NotebookLM (pilotée par Gad).** Gad colle les prompts d'un type, colle les réponses ;
  le Second donne **le pack suivant D'ABORD**, puis range (verbatim + synthèse). Règle codifiée :
  [[feedback-pipeline-pack-avant-rangement]].
- **Voie B — Développement (piloté par le Second, en arrière-plan).** Sur l'info DÉJÀ acquise, le
  Second lance des équipes. **Ordre imposé par les dépendances** (sinon collisions / drift) :
  - **B0 (sérialisé, en cours) — Socle partagé + tokenisation.** Tokeniser tous les modèles source
    (comble le NON TROUVÉ que NotebookLM ne donne pas) + bâtir UNE FOIS la couche commune :
    substitution (parts/actions, gérant/président), multi (LES SOUSSIGNÉS, répartition numérotée,
    PV d'AG), personne morale associée, couche genre, registre, slice front + déroulante auto-extensible.
  - **B0.5 (par type, AVANT câblage) — Audit de fidélité du moteur Codex.** Comparer la sortie du
    moteur existant au modèle source tokenisé + à la synthèse NotebookLM ; lister divergences. Garder
    ce qui est fidèle, **rebâtir le reste**. Aucun moteur Codex non audité ne passe en B1.
  - **B1 (parallélisé, après B0 + audit) — Une sous-équipe par type.** Câblage front + générateurs
    **validés** ; tout NON TROUVÉ ou divergence non tranchée est **parqué en TODO** → un message Rafael.
  - **Gate** : « fait » par type = passe **pré-shot UAT** + **validation Rafael**. Rien ne merge sur
    `main` ni ne se déploie sans GO Gad.

---

> ⚠️ **CORRECTION 2026-06-07.** Les « modèles manquants » signalés par les readiness B0 (Lettre option
> IS SCI, Liste dépenses .docx SCM, PV gérant…) étaient **FAUX** — l'audit B0 tournait sur le mauvais
> clone (main, `lot_01-05` seulement). **Tous les modèles sont présents** dans `project/source_documents/<type>/`.
> Seul réellement absent : modèle SELAS **multi « Reynaud »** (Gad l'a dans Downloads). Voir
> `_RAFAEL_PACKET_V1.md` + [[trap-false-missing-from-wrong-clone]].

> ✅ **MISE À JOUR 2026-06-08 (fin de nuit).** **Bundle de CRÉATION complet par type câblé selon le
> canon V1** (commits `98b2b9f` bundles + `87f50fb` conditionnels), plus seulement les statuts.
> Vérifié **end-to-end** (les tests génèrent chaque `.docx` + assert zéro placeholder `[`/`]`) :
> **suite 366 verts**. Conformité au canon = ✅ pour SELARL/SELAS/SPFPL(×2)/SCS/SCI/SCI IRIS/SAS.
> **2 groupes systématiques du canon tenus en réserve** (jamais abandonnés en silence) : **SCM 4
> satellites** (DOC-026/027/028/030) et **SPFPL note d'info** (DOC-037). ⚠️ **Correction 2026-06-08 :
> NotebookLM (synthèse SCM) dit que les satellites = « opérations DISTINCTES, hors bloc création »**
> → conflit canon (qui les liste) ↔ NotebookLM.
> ✅ **TRANCHÉ par RAFAEL 2026-06-08** : les 4 satellites SCM (pacte d'associés, liste dépenses
> communes, contrat frais communs, règlement intérieur) **FONT PARTIE du dossier SCM** (« il manque
> ces docs sur la SCM »). Le canon l'emporte sur la note NotebookLM. → **à CÂBLER dans la génération
> SCM** (générateurs Codex déjà fidèles, audit OK ; reste : collecte des données + bundle + tests).
> DOC-037 note SPFPL reste en attente Rafael (création vs après opération). Conditionnels OFF-par-défaut : régime communautaire (SELAS/SPFPL),
> option IS (SCI/SCI IRIS). Détail : `_RAPPORT_MATIN_2026-06-08.md` §0/§0bis.

## État par type

| Type | Voie A — NotebookLM | Voie B — Build | Bloquant / décision |
| :--- | :--- | :--- | :--- |
| SELARL | — (réf, fini) | **livré + mergé main** · re-audit fond+forme ✅ (`_SELARL_FIDELITY_RECHECK_V1.md`) : FOND fidèle (épinglé par test), FORME 95 % | durcissements à folder dans le fix systémique : footer médecin (pagination + « Statuts [dénom] ») ; tests dentiste + page de titre ; alignement dentiste (cosmétique) |
| SELAS | ✅ rangé (`6b6d413`) | **audit ✅** : FOND keep (verbatim, 0 invention) · FORME fix (footers/gras/centrage) · **incomplet** (unipersonnel) | **scope multi+PM+DG → GO Gad** ; tokeniser Reynaud |
| SPFPL | ✅ rangé (`915218c`) | **audit ✅** : FOND keep (0 invention) · FORME fix | toujours SPFPLAS ; Rafael (satellites apport) |
| SCM | ✅ rangé (`3d72507`) | **audit ✅** : FOND keep +2 fix · FORME fix **(⚠️ LOGO SYDEL perdu)** | carte cas→docs (Rafael) ; clé répartition dépenses |
| SCI | ✅ rangé (`736e89b`) | **audit ✅** : FOND fix (blocs réinjectés inventent ; plain-SCI wording croisé) · FORME fix | **PM en SCI standard : moteur bloque, NLM l'autorise → Rafael** ; Lettre option IS |
| SCS | ⏳ partiel (`d8980ec`) ; 11-13 attente NLM | **audit ✅** : FOND fix (blocs inventent/suppriment) · FORME fix (titre encadré perdu) | wording multi (modèle + Rafael) ; nature civile confirmée par audit |
| SCP | ⛔ **non commencé** (NLM) | readiness faite | **GO/NO-GO produit (Gad+Rafael)** — classé hors moteur courant au canon |
| SAS | ⛔ **non commencé** (NLM) | readiness faite | passe NLM jamais faite ; génération NO-GO sans Rafael |

### NotebookLM — reste à faire (limite journalière atteinte 2026-06-07)
- **SCS** : 3 prompts (11 PP-vs-société, 12 multi-commanditaires, 13 répartition apports/parts) —
  **non bloquants** (le wording multi vient du modèle source + Rafael).
- **SCP** : passe complète, **19 prompts** (dont 1 décisif « nature réelle de la SCP » + 3 Rafael).
  ⚠️ GO/NO-GO produit requis avant build.
- **SAS** : passe complète, **11 prompts**.
- **Reste donc : 2 types pleins (SCP, SAS) + le reliquat SCS (3).** Reprise à la réinitialisation NLM.

### Fix track (suite Voie B) — issu des audits de fidélité
**Cause racine commune (6 types + SELARL) :** rendu **from-scratch via `docx_builder`** au lieu de
préserver le modèle source → perte logo/footer/gras/centrage/tableaux + blocs réinjectés qui
inventent/suppriment/désaccentuent. **Fix systémique = préserver la source** (remplissage qui conserve
en-tête/footer/styles/tables nativement) + corriger les blocs dynamiques. Chantier à router proprement
(branche dédiée + plan + revue), preuve d'abord sur **1 type (SCM, cas logo)**.
- **SCM** : ✅ **logo SYDEL restauré** (`082ccdc`, vérifié : présent + 36 tests verts) ; reste 2 fix fond (« représentée par… » sur-spécifié) + reste forme.
- **SCI** : branche plain-SCI a un **wording croisé/inventé** (« Propriétaire de … parts … parts ») → réaligner sur le modèle ; désaccentuation des blocs réinjectés ; **PM en SCI standard** : moteur bloque alors que NLM autorise → Rafael.
- **SCS** : blocs réinjectés **inventent** (« SOIT AU TOTAL… ») / **suppriment** des clauses source ; **titre encadré « STATUTS » perdu** (le moteur n'itère pas les `tables` source).
- **SPFPL / SELAS** : restaurer la mise en forme source (footers/gras/centrage) ; SELAS reste **incomplet** (multi → Reynaud + Rafael).
- **SELARL (durcissement)** : footer médecin (pagination + « Statuts [dénom] ») ; tests dentiste + page de titre ; alignement dentiste.

---

## RÉUNION 2026-06-09 — Rafael × Albane × David (boss) — 1re validation humaine
Détail + routage : `_REUNION_2026-06-09_ALBANE_DAVID.md`.
- ✅ **Validation FONCTIONNELLE positive** (Albane + David) : génération docs/logos/variables/féminisation/
  pluralisation **OK constaté** ; ZIP + téléchargement par doc OK. Validation **juridique fine** = en cours.
- ✅ **Confirmé** : multi-associés **N (2/3/5+)** (listes dynamiques, le moteur adapte statuts/procurations/
  PV) ; **associé ≠ dirigeant** → distinguer **Président / DG / DG délégué** + champs dirigeant
  **conditionnels** (parents, DNC) ; **pas de mise à jour rétroactive** des dossiers historiques.
- 🔭 **Direction (à confirmer)** : **modèle unique « intelligent »** (conditions/arbres de décision) vs N
  modèles — partiellement notre approche. **Feature** : **base de données des personnes** (anti-sursaisie).
- 🩺 **Juridique → Rafael** (vague dans le débrief, attendre cas concrets) : intérêts de retard, clauses de
  cession, désignation dirigeants, infos parentales (DNC), variables mal injectées.
- **Roadmap dev next** : multi-associés N (généraliser, dont satellites SCM) ; rôles dirigeants
  (Président/DG/DG délégué) ; modèle unique dynamique. **Ne pas builder le vague** ; scoper d'abord.
- ✅ **LIVRÉ 2026-06-09 (lot constructible, `sprint/engine-completion`)** — journal MULTI-N-1 /
  DIRIGEANT-1 / DNC-COND-1 ; cadrage `_CADRAGE_LOT_REUNION_2026-06-09.md` ; plan `_PLAN_LOT_REUNION_2026-06-09.md` :
  - **A2** multi-associés **N prouvé** par tests à **3 et 5** (SCI, SCS, SCI IRIS, SELAS) ; verrou satellites SCM à 2.
  - **A1** bornes du repeater **nommées** (civils 1–2 → 6 ; SELAS 2 → 5), alignées sur le moteur.
  - **A3** sélecteur de **dirigeant** SELAS (case « Dirigeant » par associé physique ; rôle = « Président »
    seul, DG/DG délégué en attente wording Rafael ; jamais d'index moral transmis au moteur).
  - **A4** champs **DNC / filiation conditionnels** saisis **sous l'associé coché dirigeant** (défaut documenté).
  - **399 tests `tests/unit` verts**, lint propre, **zéro régression** SELARL / mono-associé.
  - **Reste FLAG Rafael** : wording DG/DG délégué · règle DNC (dirigeant seul vs tous) · satellites SCM >2 ·
    clauses « parts/gérant » des modèles SAS/SELAS. **A5 base de personnes** = ticket dédié (non démarré).

## Décisions RATIFIÉES (Rafael via Gad, 2026-06-07)

- **PÉRIMÈTRE V1 = CRÉATION UNIQUEMENT** pour tous les types (« que création »). Pas de cession /
  dissolution / transfert / entrée-sortie d'associé en V1. → allège massivement le build.
- **SELAS** : cible **confirmée** = **multi 2-5 + associé personne morale + DG** (supersede l'unipersonnel
  V1). Modèle = **Reynaud** (récupéré). ✅ **Décision Gad 2026-06-08** : face à la version SELAS du dossier
  Drive « Documents avec variables » (wording différent, 72,9 % de similarité), **on GARDE Reynaud** comme
  référence des statuts SELAS multi. Le générateur SELAS reste inchangé ; la version Drive n'est pas adoptée.
- **SCP** : **parquée, hors V1** (« tu n'as pas à t'occuper de ça »). Ne pas builder.
- **SCI standard + associé personne morale = AUTORISÉ** (Rafael, 2026-06-08) : « oui, une SCI classique
  peut avoir une autre société comme associée » (fréquent : SCI → micro-holding → SPFPL). ✅ **APPLIQUÉ
  2026-06-08** (`21e93e0`) : 3 verrous levés (moteur `_validate_sci` + `_validate_associes` + front),
  rendu via `_add_morale_identity` (= SCM/IRIS), test SCI+PM propre, 366 verts. **Reste : fidélité
  EXACTE du wording PM en SCI à confirmer Rafael/Albane** (pas de modèle source SCI-avec-PM observé).

### En attente Rafael (non bloquant — je build et je flague)
- **SPFPL** : correction vocabulaire PV « cession » rédigés en « apport » → « laisse moi checker ».

### Volet global (en attente GO Gad + coordination instance lead)
- Porter l'**INTEL GATE** dans la règle 20 (`~/.claude`), section « projets **avec associé** » (pas tous
  les projets) — pour qu'il vaille sur les autres projets Gad+Rafael (CRM…).

## Escalades métier (Rafael, groupées — jamais Gad)

- SELAS : wording multi/personne morale/DG (après modèle Reynaud).
- SPFPL : parcours apport (objet, report 150-0 B ter, conditions suspensives) après les 33 modèles.
- SCM : carte cas→docs, clé de répartition des dépenses, inscription Ordre SCM, pluriel (Albane).
- SCI : version canon qui fait foi, modèle « Lettre d'option IS ».
