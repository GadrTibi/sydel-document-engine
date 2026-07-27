# Modèle Opérationnel de la boîte (Operating Model)

> Document de gouvernance. Point d'entrée unique (le **routeur existant**, pas un agent neuf) → classement déterministe → choix du workflow → pilotage A→Z avec gates → livraison « bonne du premier coup », sans impasse.
> Statut : **EN REVUE ADVERSARIALE — NON validé.** Une validation est posée par un réviseur (humain) APRÈS coup, jamais auto-déclarée par le doc audité (parité TRAITÉ ≠ VALIDÉ, r.65). Itérations : **v1→v5 sur 4 passes adversariales** — convergence nette (v1 = doublons de rôle + impasses structurels ; v5 = edge-cases résiduels). Réviseurs : Jinbe (tech lead) + Franky (`method-steward`). **En attente de sign-off Gad.**
> Décision Gad 2026-06-23 : **pas d'agent dispatcher** — on enrichit le routeur existant (règle 00 + hook routing-first) ; Vivi garde les retours, Franky la récurrence.
> **Vocabulaire de statut = liste FERMÉE de `docs/returns/METHODE.md` §3** : `NOUVEAU · TRIÉ · DISPATCHÉ · TRAITÉ · VALIDÉ · CLARIF · BLOQUÉ`. Aucun statut inventé. Un blocage métier = `BLOQUÉ` **+ attribut « re-ping daté »** (pas un nouveau statut).

---

## 0. Résumé exécutif

La boîte avait déjà ses **branches** (workflows) et son **point d'entrée** (routeur de phase `00` + hook routing-first qui s'injecte à chaque message), mais il leur manquait trois choses : une **grille de classement écrite** (aujourd'hui le routage est heuristique, signal→phase, sans tuple explicite), un **invariant anti-impasse** qui rende l'arrêt muet *structurellement* impossible, et des **gates Stage-Gate explicites** par workflow. Ce modèle ajoute **exactement ces trois pièces** — **aucun agent neuf** — et **nomme** tout le reste comme existant. Toute demande substantielle (retour, affaire neuve, bug, audit) est **classée** par le routeur (type ITIL + grille 3×3 sévérité×priorité), reçoit **exactement un owner et un état**, puis est **routée** vers l'un des quatre workflows. Une **micro-action** (lecture/question factuelle **sans écriture code, ni Git, ni décision produit**) **bypasse** le classement (conforme routeur 00). À chaque nœud de décision, une branche `{SINON}` **obligatoire** (défaut documenté + escalade non-bloquante d'une ligne + la file continue) rend l'impasse non-représentable. Chaque workflow est jalonné de **gates** (Go/Adjust, critères visibles) et fermé par une **DoD-checklist** courte = le « bon du premier coup ». Ownership tranché : **Approver produit unique = Gad** ; **veto métier/juridique = Albane**, jamais soumis à l'Approver produit.

---

## 1. Schéma du flux

```
   DEMANDE substantielle                     micro-action (lecture/question sans
   (retour, affaire, bug, audit)              écriture code NI Git NI décision
            │                                  produit) ──► réponse directe,
            ▼                                  AUCUN classement (routeur 00)
   ┌──────────────────────────────────────────────────────┐
   │  ROUTEUR  (règle 00 + hook routing-first — EXISTANT)  │  ◀ pièce NEUVE = la GRILLE 3×3 écrite
   │  1.CAPTER → 2.CLASSER (grille 3×3) → 2bis.AUTO-CONTRÔLE │     greffée ici (pas un agent)
   │  → 3.GATE actionnable → 4.ROUTER → 5.NOMMER 1 owner/   │
   │  1 état (+Approver/veto) → 6.INSCRIRE (file = Manifeste)│
   └───────────────────────────┬──────────────────────────┘
        ┌──────────────────┬────┴─────────────┬──────────────────┐
        ▼                  ▼                  ▼                   ▼
   ┌─────────┐        ┌──────────┐       ┌─────────┐         ┌─────────┐     (route latérale)
   │WF-RETOUR│        │WF-AFFAIRE│       │ WF-BUG  │         │WF-AUDIT │     signal méthode → Franky
   │ Change  │        │Service Req│      │Incident │         │ Problem │     (carnet DRH, hors file)
   │Vivi→Chop.│       │/type-     │      │ Chopper │         │ vigies  │
   │+docs/   │        │entreprise │      │+Sanji   │         │ /Law    │
   │returns/ │        │ Robin→Nami│      │ si prod │         │read-only│
   └────┬────┘        └────┬─────┘       └────┬────┘         └────┬────┘
        │  G1 G2 G3        │ G0…G4            │ G1 G2 G3          │ G1…G4 (+ré-injection)
        ▼                  ▼                  ▼                   ▼
   ┌────────────────────────────────────────────────────────────────────┐
   │  GATES Stage-Gate (Go/Adjust, borné K=2) + DoD + Poka-Yoke + Andon   │
   └───────────────────────────────┬────────────────────────────────────┘
                                   ▼
                            LIVRAISON vérifiée
                  (push branche dédiée ; merge main / déploiement = GO PM seul)

   À CHAQUE nœud ci-dessus : branche {SINON} OBLIGATOIRE → défaut documenté
   + escalade non-bloquante 1 ligne → la file CONTINUE.  (invariant anti-impasse, règle 12)
```

---

## 2. Le ROUTEUR + la grille 3×3

### 2.1 Pas d'agent — une grille écrite greffée au routeur existant

Le **point d'entrée et l'aiguillage de phase existent déjà** : routeur `00` + hook routing-first (qui injecte le routage à chaque message), opérés par **Jinbe** (main loop). Mais aujourd'hui ce routage est **heuristique** (signal→artefact), il ne produit pas de **tuple Type/Surface/P** explicite. La pièce **NEUVE** = la **grille 3×3 écrite** ci-dessous + l'**auto-contrôle** du classement (GATE 0), greffés au routeur. On n'ajoute **aucun** agent : la critique a montré qu'un dispatcher dédié (« Tom ») dupliquait Vivi (retours), Franky (récurrence) et le hook lui-même.

**Séquence de classement :** `1.CAPTER (verbatim + source + date + ID selon la convention canonique` `METHODE.md` `§1 : O24-NN/LIVE-NN/ALB-NN ; un préfixe d'affaire neuve serait à RATIFIER dans METHODE.md par Vivi, pas inventé ici) → 2.CLASSER (grille 3×3 → tuple Type/Surface/P) → 2bis.AUTO-CONTRÔLE (GATE 0) → 3.GATE actionnable → 4.ROUTER → 5.NOMMER owner+état (+Approver/veto) → 6.INSCRIRE dans la file (Manifeste).`

**Invariant load-bearing :** *toute demande a, à tout instant, exactement UN owner et UN état ; aucune ne touche un exécutant avant d'être complète et actionnable.*

**Exemption micro-action (reprise exacte du routeur 00).** Une **lecture / question factuelle SANS écriture code, NI Git (commit/branche/merge), NI décision produit** **bypasse** le classement : réponse directe, aucun routage. Un commit/push/merge n'est **jamais** une micro-action (r.11/60). On re-route dès qu'une écriture émerge.

**Frontières.** Le routeur **classe et aiguille** seulement ; il ne code pas, ne tranche aucune décision produit (Approver = Gad) ni métier (veto = Albane). Pour un **retour**, il constate « c'est un Change » et le passe **direct à Vivi**, qui applique sa grille fine (règle 68) — le routeur n'empiète pas sur le rulebook de Vivi. La **récurrence** : le routeur **détecte le candidat** (≥2 même cause) et le **passe à Franky** ; **Franky seul confirme et promeut** le Problem (R/A, règle des 2 occurrences) — le routeur ne classe jamais en Problem lui-même.

### 2.2 Axe 1 — TYPE (intake ITIL → workflow)

| Type ITIL | Signal Sydel | Branche cible | Owner d'entrée |
|---|---|---|---|
| **Change** | Retour/correction sur un doc ou type déjà livré | **WF-RETOUR** (`docs/returns/` + règle 68) | **Vivi** → Chopper |
| **Service Request** | Affaire neuve A→Z (nouveau type d'entreprise) | **WF-AFFAIRE** (`/type-entreprise`) | **Robin** → Nami |
| **Incident** | Un doc casse / génération KO / régression en prod | **WF-BUG** (`fix/…` ; Chopper si live, Sanji si prod) | **Chopper** |
| **Problem** | Retour **récurrent** (≥ 2 incidents même cause) → refonte de règle | **WF-AUDIT** (audit read-only + refonte canon) | une **vigie** / Law |

> Chaîne ITIL : **plusieurs Incidents → un Problem → un Change.** La récurrence (≥2 même cause) est détectée puis **promue par Franky** (`method-steward`, règle des 2 occurrences). Le routeur la **signale** ; il ne promeut pas lui-même. Quand un Problem accouche d'un Change/Incident actionnable, l'item dérivé **re-passe par le routeur** (GATE 0 + GATE 1, nouvel ID/owner/état) — §3.4.

### 2.3 Axe 2 — SURFACE (déclenche les volets design / sachant)

| Surface | Définition | Volet DESIGN | Volet SACHANT |
|---|---|---|---|
| **B — Backend pur** | Service, repo, migration, perf, tests, règle moteur sans rendu visible | **NON** (proportionnalité, routeur 00) | NON |
| **V — Surface visible** | Écran, formulaire, message, état, doc généré visible | **OUI** : `design-scope-auditor` amont si structurant, `ui-designer` aval systématique | NON (sauf wording légal) |
| **M — Métier/juridique** | Wording légal, genre/pluriel, durée, règle de droit, éligibilité | NON (sauf surface) | **OUI** : veto **Albane**, jamais soumis à l'Approver produit |

> Poka-Yoke : Surface=V **force** `ui-designer` aval ; Surface=M **force** le drapeau `à valider sachant` et **interdit** que Gad tranche le point métier.

### 2.4 Axe 3 — SÉVÉRITÉ × PRIORITÉ (grille 3×3 → P0..P3)

Sévérité = impact **technique** (objectif : nb de docs/types/users touchés, gold O/N, prod vivante O/N). Priorité/Urgence = jugement **métier** (Gad ; veto Albane sur un point juridique ; défaut « Moyenne » si flou). Un seul P par demande.

| Impact ↓ / Urgence → | **Haute** (client/prod bloqué, Albane attend) | **Moyenne** (dégradé, contournable) | **Basse** (cosmétique, confort) |
|---|---|---|---|
| **Élevé** (faux acte, génération KO, gold touché) | **P0** | **P1** | **P2** |
| **Moyen** (champ erroné non bloquant, UX cassée) | **P1** | **P2** | **P3** |
| **Faible** (libellé, accent, 1 champ) | **P2** | **P3** | **P3** |

- **P0** = **tête de file immédiate** : on traite le P0 **en priorité absolue, SANS figer les autres items batchables** (conforme règle 07 : on ne bloque jamais toute la file). Seul l'**acte irréversible** (E5) attend le GO PM.
- **P1** = tête de file courante · **P2** = file normale · **P3** = backlog / Manifeste P3.
- Un item en blocage métier Albane prend le statut **`BLOQUÉ`** (+ re-ping daté, §4.2 E2) et ne reçoit **pas** de P : gelé hors-grille **sans figer la file** jusqu'à arbitrage du sachant.

### 2.5 Table de routage complète (tuple → workflow + owner + volets)

| # | Type | Surface | P typique | → Workflow | Owner initial | Volets forcés |
|---|---|---|---|---|---|---|
| 1 | Change | V/B/M | P1–P3 | **WF-RETOUR** | **Vivi** (intake, R) → **Chopper** (fix, R) ; A Jinbe | si V→`ui-designer` ; si M→veto Albane ; grille 68 |
| 2 | Service Request | V (le plus souvent) | P2–P3 | **WF-AFFAIRE** | **Robin** puis impl | `design-scope-auditor` amont + `ui-designer` aval ; gate produit |
| 3 | Incident | B | **P0/P1** | **WF-BUG** | **Chopper** si live, sinon impl | règle 60 si base partagée ; GO PM si irréversible |
| 4 | Incident | V | **P0/P1** | **WF-BUG** + `ui-designer` aval | Chopper / impl | volet UI aval ; GO PM si irréversible |
| 5 | Incident (≥2 même cause) | — | P1 | **promotion → WF-AUDIT** | **Franky** (R/A : détecte+promeut) → ouvre WF-AUDIT (Robin R de la refonte, A Jinbe) | ADR de refonte ; canon |
| 6 | Problem | M | P1–P2 | **WF-AUDIT** | **Robin** + veto **Albane** | décision canon + journal de décisions |
| 7 | Change | B (pur, mécanique) | P2–P3 | **WF-BUG** (sprint-gov léger) | impl | aucun volet (proportionnalité) |
| 8 | signal **méthode** (façon de travailler, process, agent) | — | — | **route latérale → Franky** | **Franky** (R/A) | carnet DRH (r.45), hors file produit ; **critère** : porte sur *comment on travaille*, pas sur le produit ; **gate** : Franky confirme « méthode ≠ produit » avant d'absorber |

> Ownership inscrit à l'étape 5 : **Accountable produit = Gad** (Approver), **Responsible = owner du tableau**, **veto métier = Albane** (jamais soumis à l'Approver). Un seul Accountable par nœud (cf. §5.4, qui couvre TOUS les nœuds des SOP).

---

## 3. Catalogue des 4 workflows-SOP

Structure homogène : **pré-conditions bloquantes** (Poka-Yoke de démarrage, **chacune avec sa branche {SINON} nommée**) → **étapes** (owner · résultat vérifiable · échec « si… alors… ») → **gates** (critère + sign-off, branche Adjust **bornée K=2**) → **critère de sortie** + **maintenance**. Chaque nœud hérite de l'invariant `{SINON}` (§4, règle 12).

### 3.1 WF-RETOUR — Change *(englobe `docs/returns/` + règle 68 ; détail = `METHODE.md`)*

**Pré-conditions bloquantes (chacune avec son défaut) :** verbatim exact en main *(sinon → `CLARIF` + `QUESTIONS_RAFAEL`, file continue)* · `git branch` = branche de travail, jamais `main` *(sinon → STOP edit, `git-branch-steward`, r.11)* · base non partagée OU pas de suite DB en live *(sinon → ne lancer que des tests sans DB, r.60)* · périmètre de test nommé *(sinon → le nommer avant d'annoncer, r.65)* · `docs/returns/` à jour *(sinon → défaut : signaler 1 ligne + travailler sur l'état connu, ne pas recréer, file continue)*.

**Cycle de vie (statuts canoniques, `METHODE.md` §3) :** `NOUVEAU → TRIÉ → DISPATCHÉ → TRAITÉ → VALIDÉ` (+ `CLARIF`/`BLOQUÉ`). `CARNET.md`/`TRIAGE.md`/`VALIDES.md` sont des **fichiers**, pas des statuts.

| # | Étape | Owner (R) | Résultat vérifiable | Si échec → défaut OBLIGATOIRE + escalade |
|---|---|---|---|---|
| 1 | Intake verbatim (→ fichier `CARNET.md`), statut `NOUVEAU` | Vivi | ID stable + verbatim mot pour mot + champs schéma | ambigu → `CLARIF` + ligne `QUESTIONS_RAFAEL`, **file continue** |
| 2 | Triage 3 questions (→ `TRIAGE.md`), statut `TRIÉ` | Vivi | Q1 anticipable / Q2 écart / Q3 gold-métier tranchées | Q3=métier → `BLOQUÉ` (re-ping daté) + sachant, **on enchaîne** |
| 3 | Dispatch (dépendances ≥ `TRAITÉ`), statut `DISPATCHÉ` | Vivi→Chopper | Owner unique + verbatim transmis | dépendance non `TRAITÉ` → traiter la dépendance d'abord ; cet item attend **sans bloquer les autres** |
| 4 | Align : intention + critères d'acceptation | R Chopper, **A Jinbe**, C Robin | Intention reformulée + critères testables | règle produit neuve requise → **carte PM EN PARALLÈLE + défaut réversible documenté** ; **si la règle est structurante (aucun défaut réversible sûr)** → cet item seul passe `BLOQUÉ` (carte Gad, re-ping daté), **la file continue** ; ne jamais inventer un faux défaut |
| 5 | Fix minimal on-intent, statut reste `DISPATCHÉ` | Chopper | Diff minimal, aucune règle/lock touchée en silence | déborde → re-scoper, autre ticket |
| 6 | Test + **verbatim gate** | Chopper | Suite du périmètre nommé verte (r.65), ruff, hors-scope byte-identique, relu clause par clause | vert contre mauvaise interprétation → invalide, relire le verbatim |
| 7 | Revue fonctionnelle vs #4 | Zoro | aligné / dérive / régression / dette | dérive → retour #5, ne pas pousser ; **2e dérive même cause → re-scope (E3), pas de 3e tour** |
| 8 | Commit + push même session, statut `TRAITÉ` | Chopper | Commit réf. ID ; push branche dédiée ; jamais merge `main` | CI rouge infra transitoire → **1** relance (r.60) ; code → #5 |
| 9 | Message retest Rafael (court, froid, puces) | Jinbe | Bloc copiable, zéro code interne | n/a |
| 10 | Validé client → fichier `VALIDES.md`, statut `VALIDÉ` | Vivi | `VALIDÉ` **uniquement** sur mot explicite | pas de mot → reste `TRAITÉ`, jamais auto-valider |

**Accountable — handoff nommé :** **A = Vivi de #1 à #3** (intake/triage/dispatch, r.68) ; **A bascule à Jinbe à l'entrée de #4 (Align)** et le reste jusqu'à #8 (fix) ; **A revient à Vivi à #9** (suivi/validation). Un seul A à tout instant.
**Gates :** **G1 Triage** (après #2 ; sign-off **Vivi**) · **G2 Verbatim** (après #6 : relecture clause par clause + périmètre vert nommé + hors-scope byte-identique ; **sign-off Zoro** — gardien ≠ exécutant ; Chopper en C) · **G3 Validation client** (après #10 ; sign-off **Vivi** — **TRAITÉ ≠ VALIDÉ**). *Branche Adjust de chaque gate bornée K=2 (§5.1).*
**Critère de sortie :** l'item est `VALIDÉ` (G3). **Maintenance :** réviseurs Vivi + Franky ; règle 68.

### 3.2 WF-AFFAIRE — Service Request A→Z *(englobe `/type-entreprise` + `WORKFLOW_TYPE_ENTREPRISE_V1.md`)*

**Pré-conditions bloquantes (chacune avec son défaut) :** type cible nommé · branche `<type>/…` active, jamais `main` *(sinon → r.11)* · couche partagée SEL/commune non éditée en parallèle · modèles tokenisés en main · canon `Documents_a_generer_par_cas_V3.docx` + locks **lisibles** *(sinon illisible/manquant → E4 trou-de-source : remonter à Gad 1 ligne + `QUESTIONS_RAFAEL`, item `BLOQUÉ`, file continue)*.

| # | Phase | Owner (R) | Résultat vérifiable | Si échec → défaut OBLIGATOIRE + escalade |
|---|---|---|---|---|
| 0 | Cadrage & branche | Jinbe + Robin | Bloc routage PM ; carte périmètre (r.06) ; branche active | flou → carte PM + défaut de périmètre documenté, ne pas coder le flou |
| 1 | Sources | vigie | Modèles inventoriés/dédupliqués/rangés ; cas vérifiés **par le contenu** | doc manquant → message Rafael, jamais affirmer depuis le mauvais clone |
| 2 | Cartographie | Nami | Matrice **cas → documents** + variantes (genre, gérance, profession, régime, cession, SCM, dérogation, site) | variante non sourcée → open + défaut documenté |
| 3 | Moteur | Jinbe | 1 générateur/doc + `*_common.py` + fixtures/cas + `models.py` | paraphrase au lieu de template-fill → rejeter |
| 4 | Règles juridiques | Jinbe (NotebookLM/locks) | Règles tranchées ; coquilles inter-profession chassées ; durée société vs domiciliation | point non sourcé → `BLOQUÉ` (re-ping daté) + message Rafael, jamais inventer |
| 5 | Couche genre | Jinbe | `apply_gender_pairs` (paires exactes) ; préférences par personne | pluriel incertain → après Albane, pas d'initiative |
| 6 | UI Streamlit | Jinbe | Tous les cas du canon générables ; 1 clic données de test/cas ; garde-fou coché-sans-données ; messages FR métier | cas manuel = **WARNING**, pas blocker ; forme infidèle → template-fill |
| 7 | Vérification | Jinbe + Zoro | ruff + **suite COMPLÈTE** verte + génération via UI + création seule intacte + pré-shot UAT | **ne jamais croire l'auto-rapport d'un agent — revérifier** (r.65) |
| 8 | Gate juridique | Albane | Pack de passation ; génération **NO-GO** tant que wording non validé | non validé → NO-GO maintenu, item `BLOQUÉ` avec **re-ping daté** (§4.2 E2), on n'expose pas |
| 9 | Clôture | Brook | Journal décisions (codes, superseded) ; état + tickets ; leçons reversées | leçon non reversée → SOP non close |

**Gates :** **G0 Cadrage** (périmètre confirmé Gad) · **G1 Sources** (tous les cas du canon couverts ; Nami) · **G2a Fidélité genre/pluriel** (après #5, AVANT UI : paires de genre vérifiées, pluriel sourcé ou validé Albane ; **sign-off Zoro** — gardien ≠ exécutant ; Jinbe en C — risque de fidélité connu, gate dédié) · **G2b Moteur+UI** (suite complète verte + génération UI + création intacte + pré-shot UAT ; **Zoro**) · **G3 Juridique** (wording validé Albane OU NO-GO ; **veto Albane**, jamais soumis à Gad) · **G4 Merge/déploiement** (GO Gad ; **irréversible, jamais en autonomie**). *Adjust borné K=2.*
**Critère de sortie :** checklist « type fini » + G4 franchi **OU clôture partielle datée `LIVRÉ-SAUF-GÉNÉRATION`** (build complet ; génération gelée NO-GO en attente du veto Albane E2) — la SOP se clôt proprement sans rester ouverte ad vitam. **Maintenance :** réviseur Jinbe ; skill `/type-entreprise`.

### 3.3 WF-BUG — Incident *(s'appuie sur Chopper/`uat-fix-loop` + Sanji + règles 60/70)*

**Pré-conditions bloquantes (chacune avec son défaut) :** symptôme reproductible décrit *(sinon → `CLARIF`)* · sévérité + P posés par le routeur · branche `fix/<incident>` active, jamais `main` *(sinon → r.11)* · base partagée O/N → si live, aucune suite DB (r.60) · **si prod vivante** → fiche `prod-change-steward` requise avant tout déploiement (r.70).

| # | Étape | Owner (R) | Résultat vérifiable | Si échec → défaut OBLIGATOIRE + escalade |
|---|---|---|---|---|
| 1 | Triage incident : classe P + surface | **Jinbe** (routeur, A) → handoff R Chopper | Fiche sévérité/P/branche/owner | P0 → **tête de file immédiate** (pas de gel des autres, r.07) |
| 2 | Repro read-only : cause `file:line` | Chopper | Cause citée ; bug produit vs fixture distingués | non reproductible → `CLARIF` + état/écran exact (jamais « reboot » sans vérifier la chaîne de déploiement) |
| 3 | Align : comportement attendu + critère « réparé » | R Chopper, **A Jinbe**, C Robin | Attendu reformulé + critère | règle métier neuve requise → **carte PM EN PARALLÈLE OU `BLOQUÉ` (re-ping daté)** + défaut documenté, la file continue ; si structurante sans défaut sûr → item seul `BLOQUÉ`, file continue |
| 4 | Fix minimal | Chopper | Diff minimal, aucune règle/lock en silence | déborde → re-scoper |
| 5 | Test non-régression ciblé + cas du bug | Chopper | Module touché vert (périmètre nommé, r.65) + cas qui plantait passe + ruff ; hors-scope byte-identique | sous-ensemble → le dire ; rouge → #4 ; **rouge 2e fois même cause → re-scope (E3)** |
| 6 | Revue fonctionnelle | Zoro | aligné / pas de régression nouvelle | régression → #4 |
| 7 | **Si prod** : fiche GO/NO-GO | Sanji | Blast radius, migration expand→migrate→contract, fenêtre creuse, rollback **écrit prêt avant déploiement**, comms | rollback inconnu → **NO-GO** (r.70) |
| 8 | Commit + push `fix/…` | Chopper | Commit réf. incident ; CI verte ; **GO Gad avant merge `main`** | CI infra transitoire → **1** relance ; code → #4 |
| 9 | Vérif post-déploiement (si déployé) | Sanji + Gad | Smoke test parcours critiques + surveillance erreurs | erreur prod → **rollback immédiat**, pas de debug à chaud |
| 10 | Doc : registre dettes = incident résolu | Brook | Entrée datée ; récurrence → promotion Franky → WF-AUDIT | n/a |

**Gates :** **G1 Diagnostic** (cause `file:line` + bug-vs-fixture tranché ; **sign-off Zoro/vigie** — gardien ≠ exécutant ; Chopper en C) · **G2 Non-régression** (test ciblé vert nommé + aucune régression + ruff ; Zoro) · **G3 Prod** (si prod vivante : fiche GO/NO-GO + rollback prêt ; sign-off **Gad** ; sinon `n/a`). *Adjust borné K=2.*
**Critère de sortie :** incident résolu + poussé (+ déployé avec GO Gad si prod) + registre à jour. **Maintenance :** Chopper + Sanji ; règles 60/65/70.

### 3.4 WF-AUDIT — Problem / audit-only *(s'appuie sur les vigies / Law + règle 10 audit-only)*

**Pré-conditions bloquantes (chacune avec son défaut) :** périmètre d'audit nommé · mode **audit-only** confirmé (aucune édition de code, aucun patch — r.10) · branche d'origine notée, **restaurer avant de finir**, jamais sur `main` (r.11) · bon clone (chemins **absolus** vers `sydel-document-engine-claude`).

| # | Étape | Owner (R) | Résultat vérifiable | Si échec → défaut OBLIGATOIRE + escalade |
|---|---|---|---|---|
| 1 | Cadrage Problem : symptôme récurrent + Incidents liés | R Jinbe + Franky, **A Jinbe** | Liste des Incidents remontant au même Problem | un seul Incident isolé → pas un Problem, renvoyer en WF-BUG |
| 2 | Audit read-only ciblé | vigie / Law | Rapport **daté** : findings classés (confirmé/probable/assumption/open), aucune mutation | **besoin d'éditer du code détecté → défaut : fermer/suspendre l'audit (rapport partiel daté) + ouvrir un WF-BUG/WF-RETOUR pour la correction** ; jamais muter sous mode audit (r.10) |
| 3 | Recoupement des findings forts | Jinbe | Tout fait alarmant **revérifié soi-même** avant restitution | un sous-agent peut se tromper sur toute la ligne (r.65) |
| 4 | Cause racine (pas le symptôme) | Law + Jinbe | Règle/source défaillante identifiée | trou dans une source de vérité → **remonter à Gad immédiatement** |
| 5 | Reco de refonte de règle | Robin/Nami | intention / actuel / impact / sévérité / action (forme drift r.20) | reco qui change une règle produit → carte PM, ne pas trancher seul |
| 6 | **Ré-injection** : Problem → Change/Incident actionnable | Jinbe (routeur) | item dérivé **re-passe par le routeur** (GATE 0 + GATE 1 : nouvel ID, owner, état) | non re-passé → trou de traçabilité ITIL : forcer le ré-classement avant d'« ouvrir » |
| 7 | Dette si non traité maintenant | Brook | Entrées datées + pointeur | n/a |
| 8 | Restaurer branche + clôture | Jinbe | `git branch` = branche initiale ; repo pas sur `main` ; rapport rangé | laissé sur `main` → corriger avant de finir (r.11) |

**Gates :** **G0 Promotion** (récurrence ≥2 confirmée → Problem cadré ; **R/A Franky** ; à l'ouverture formelle de WF-AUDIT, A bascule à Jinbe — un seul A à tout instant) · **G1 Périmètre** (Problem ≠ Incident isolé ; R Jinbe+Franky, **A Jinbe**) · **G2 Intégrité audit** (rapport daté, zéro mutation, findings classés ; la vigie) · **G3 Recoupement** (tout finding fort revérifié à la main ; Jinbe) · **G4 Décision** (refonte présentée à Gad / Albane si métier) · **G5 Ré-injection** (tout dérivé actionnable re-passé par GATE 0/1 avec nouvel ID ; Jinbe). *Adjust borné K=2.*
**Critère de sortie :** rapport daté + dettes inscrites + dérivés ré-injectés (nouvel ID) + branche restaurée. **SOP read-only.** **Maintenance :** vigie + Franky ; règles 10/11/65.

---

## 4. Invariant anti-impasse + table d'escalade

### 4.1 L'invariant (règle globale `12-no-dead-end.md`, rappelé en tête du routeur 00)

```
## INVARIANT ANTI-IMPASSE (s'applique à CHAQUE nœud de décision de CHAQUE workflow)

Aucun nœud n'a le droit d'exister sans branche par défaut. Tout point où l'on choisit
(route, classement, gate, traitement, rebouclage) DOIT énumérer :
  (a) ses options nommées, ET
  (b) une branche {SINON} OBLIGATOIRE (jamais une alternative au STOP) :
      → poser un DÉFAUT documenté (le choix le plus sûr/réversible, écrit avec sa raison),
      → escalade NON-BLOQUANTE : UNE ligne au bon sachant (table d'escalade ci-dessous),
      → CONTINUER la file — ne jamais geler les autres items pour celui-ci.

Quatre interdits durs :
  1. Jamais router une demande INCOMPLÈTE : on la complète, ou on pose un défaut documenté.
     Une demande a, à tout instant, exactement UN owner et UN état.
  2. Jamais « escalade si ça tourne mal » : déclencheur = CONDITION MESURABLE
     — « si [symptôme précis] alors [action précise] vers [rôle nommé] avec l'état courant ».
  3. Jamais bloquer toute la file pour un item : flag 1 ligne (r.07) puis on enchaîne.
     Même un P0 se traite en tête de file SANS geler les autres items batchables.
  4. Tout REBOUCLAGE est BORNÉ K=2 sur la même cause — gate Go/Adjust ET retour d'étape
     interne (revue→fix, test rouge→fix). Au 2e échec identique → escalade (technique→E3
     re-scope/suspension ; produit→E1 ; métier→E2) ; l'item passe en état daté, la file
     continue. Jamais reboucler une 3e fois en silence.

Andon : tout agent qui voit un défaut STOPPE son item, flag 1 ligne, le pose en défaut+escalade
— il ne propage jamais le défaut en aval. Le redémarrage post-Andon appartient à Jinbe.
Une reprise PUREMENT TECHNIQUE (E3) ne remonte JAMAIS à Gad : si Jinbe est indisponible, l'item
reste BLOQUÉ-REPRISE daté dans la file, repris par le premier exécutant dispo / la prochaine session.
Le suppléant Gad est réservé aux reprises portant une décision PRODUIT (E1) ou un acte IRRÉVERSIBLE
(E5) — jamais une reprise technique. Aucun item n'est jamais propagé en aval ni perdu.

Exemption : une micro-action (lecture/question SANS écriture code NI Git NI décision produit)
n'est pas un nœud de workflow — réponse directe, pas de classement (routeur 00).
```

**Preuve d'absence d'impasse (taxinomie complète des attentes).** Tout état d'un agent est soit (a) une option nommée prise, soit (b) la branche `{SINON}`. Aucun troisième état ; un nœud sans `{SINON}` est *malformé par définition*. **Cas de l'agent mort/muet** (sous-agent background qui meurt sans rien flag) : ce n'est pas un 3ᵉ état toléré → **garde de vivacité (r.07)** : mtime des sorties surveillé ; au-delà du seuil de silence, **Jinbe reprend la main**, vérifie les édits laissés, reclasse l'item en option-prise ou `{SINON}`. L'item ne reste jamais gelé sans flag. Les **attentes** de la table §4.2 se rangent en deux classes, **aucune ne gèle jamais la file ni l'acte de build** :

- **Attentes BORNÉES à sortie terminante** — `E1` (clic Gad), `E4` (info introuvable), `E6` (CLARIF) : **jalon de bascule = la fin du lot courant OU le prochain commit groupé (le premier des deux)** — un événement qui se produit **forcément** dans le flux continu (r.07), pas une pause que r.07 élimine. À ce jalon sans réponse → le **défaut conservateur documenté** (marqué `à valider`) **devient effectif et l'item avance** ; le re-ping reste actif pour correction a posteriori. Sortie garantie par un événement inévitable.
- **Attentes légitimement NON-terminantes mais non-bloquantes** — `E2` (veto métier Albane, statut `BLOQUÉ`) et `E5` (irréversible) : par conception (r.20 / r.07) on **n'invente jamais** le juridique ni l'irréversible. L'item peut rester `BLOQUÉ` indéfiniment **sans que ce soit une impasse** : la file continue, le build continue, et rien n'est exposé en prod (G3 reste NO-GO). La **relance time-boxée** garantit le *non-oubli*, pas l'aboutissement. Ces attentes sont **nommées, owned (relance = Jinbe), datées** — pas des puits muets.

### 4.2 Table des chemins d'escalade (par type de blocage)

| # | Type de blocage | Condition de déclenchement (MESURABLE) | Destinataire (owner du déblocage) | Action (défaut + escalade) |
|---|---|---|---|---|
| **E1** | **Décision PRODUIT** (scope, priorité, UX, trade-off) | ≥ 2 options exclusives, aucune dérivable du déterministe ni d'une décision ratifiée | **Approver = Gad** (DACI). Relance = Jinbe. | **Carte cliquable** (r.06), reco en 1ʳᵉ. Défaut réversible posé EN PARALLÈLE, file continue. **Si aucun défaut réversible sûr (règle structurante)** → l'item seul attend (carte posée, re-ping daté) ; la file continue ; ne jamais inventer un faux défaut. |
| **E2** | **MÉTIER / JURIDIQUE** (wording, genre/pluriel, durée, droit, fidélité) | Info absente OU contradictoire **après épuisement des sources** (NotebookLM/corpus, canon, locks) | **Veto = Albane** (RAPID). **JAMAIS soumis à Gad** (r.20). Relance = Jinbe. | **Ne pas inventer.** Statut **`BLOQUÉ` + date de re-ping** ; **question au sachant : Albane via Gad** (canon `METHODE.md` §3 + §5.3 ; `QUESTIONS_RAFAEL.md` est réservé à la clarif PRODUIT E6, pas au veto métier). Défaut conservateur marqué `à valider`, **non exposé en prod**. Attente non-terminante mais **non-bloquante** : la file continue. |
| **E3** | **TECHNIQUE** (archi, branche/Git, outil, perf) | Blocage d'exécution sans surface produit ni juridique | **L'agent lui-même** (Jinbe), appuyé sur l'agent spécialisé | **Trancher soi-même** + annoncer 1 ligne (r.07). Jamais faire trancher Gad. Aucune escalade humaine. |
| **E4** | **INFO INTROUVABLE** (donnée/spec/source manquante) | Sources épuisées ET donnée introuvable, OU trou dans la source de vérité | **Défaut documenté** + `QUESTIONS_RAFAEL.md` ; trou de source → **remonter à Gad** | Défaut explicite + raison, file continue. **Sortie bornée** : au jalon, défaut conservateur tient. Trou de source = alerte 1 ligne immédiate, jamais contourner. |
| **E5** | **IRRÉVERSIBLE** (merge `main`, migration destructive, déploiement, contact externe) | L'action figure dans la liste irréversible de la r.07 | **GO PM = Gad** (+ Sanji/r.70 si prod) | **STOP avant l'acte uniquement** (jamais avant le build). Build sur branche/staging → prêt → GO PM. Attente non-terminante mais non-bloquante (le reste avance). |
| **E6** | **CLARIFICATION** (retour CLIENT illisible/ambigu) | Retour client non lisible (screenshot illisible, verbatim manquant) | **Rafael** via le carnet ; relance = Jinbe | Statut `CLARIF` + ligne `QUESTIONS_RAFAEL.md`. **Sortie bornée** : re-ping au jalon (point d'étape suivant) ; si toujours rien → **défaut conservateur documenté** (interprétation la plus sûre, marquée `à valider`). Item attend **sans bloquer les autres**. *(Un échec de CLASSEMENT interne — GATE 0 rouge persistant — n'est PAS un E6 : c'est un E3, Jinbe tranche le tuple par défaut + annonce ; jamais routé vers Rafael qui n'a pas le problème.)* |

> Branchement sur l'existant : la **règle 07** est le *moteur* de `{SINON}` ; `QUESTIONS_RAFAEL.md` le *réservoir* de clarif produit (E4/E6) ; le **veto métier E2** part à **Albane via Gad** (jamais dans `QUESTIONS_RAFAEL`) ; les **cartes 06** le *canal* d'E1/E5. **Préséance E2 > E6** : un retour à la fois illisible ET porteur d'un point métier → traiter d'abord le métier en E2 (Albane), E6 (Rafael) ne couvre que la lisibilité. L'impasse est **non-représentable** ; toute attente est nommée, owned, datée.

---

## 5. Système qualité : gates · DoD · poka-yoke/andon · ownership

### 5.1 Les 4 niveaux de gates

- **GATE 0 — Auto-contrôle du classement (NEUF).** Avant de router : le tuple Type/Surface/P est-il cohérent ? (un retour sur un doc livré n'est pas un « Incident » ; surface visible force le volet design ; point juridique force le drapeau sachant). Vert → on route. Rouge → reclasser **une fois** ; **si le tuple reste incohérent au 2ᵉ passage → E3 : Jinbe tranche par défaut conservateur NOMMÉ = `WF-AUDIT read-only` (zéro mutation, zéro risque) si simple doute, ou `Change / Surface=M / P1` si une action est requise** + annonce 1 ligne (échec de classement = interne, jamais une question à Rafael). L'item avance, la file continue. **Hook vs GATE 0 :** le hook routing-first pré-remplit un routage *signal→phase* (suggestion, **non-Accountable**) ; **GATE 0 (Jinbe) est le SEUL Accountable du tuple ITIL** ; en cas de divergence, GATE 0 fait foi.
- **GATE 1 — Intake (« demande actionnable »).** Binaire : verbatim · ID · Type · P · périmètre · dépendances · complétude. Vert → file (1 owner/1 état). Rouge → `CLARIF`/`BLOQUÉ` ou défaut documenté, ne descend pas.
- **GATE 2 — De phase (Stage-Gate Cooper).** Livrables + critères visibles → **Go / Adjust** par un **gardien du casting** (jamais l'exécutant). **Adjust borné : après K=2 Adjust sur la même phase → escalade** (litige produit→E1 carte Gad ; technique→E3 Jinbe tranche+annonce ; métier→E2). Pas de cycle Go/Adjust infini.
- **GATE 3 — De sortie (DoD-checklist, courte).** Étapes critiques cochées avant « fini ». **Sign-off DoD = le gardien fonctionnel Zoro** (jamais l'exécutant). **Borné : DoD refusée 2× sur le même critère → escalade (E1 si litige produit, E2 si infidélité métier non sourcée, E3 si simple mauvaise implémentation d'une règle déjà sourcée) ; pas de 3ᵉ reboucle silencieuse.**
- **GATE 4 — Adversarial (Akainu, règle 66).** Tout livrable passe l'auditeur méchant `adversarial-qa-auditor` **EN BOUCLE** : `fix → Akainu → fix → Akainu …` **jusqu'à `RIEN À REDIRE`** (ou nitpicks explicitement acceptés). **Un item n'est TRAITÉ que quand Akainu n'a plus rien à redire** ; un lot n'est « fini » que quand Akainu est content de TOUS les items. Borne anti-impasse (règle 12) : même défaut re-trouvé après fix → E3 re-scope, pas de 3ᵉ boucle à l'identique.

**DoD — WF-RETOUR :** fix relu clause par clause contre le verbatim · autres occurrences du même écart cherchées · suite ciblée réellement lancée, périmètre nommé, verte · `git branch` correcte · statut `TRAITÉ`, pas `VALIDÉ` jusqu'au mot de Rafael · trou de source → `SOURCES_DE_VERITE.md` · carnet re-montré avant l'item suivant.

**DoD — WF-AFFAIRE :** tous les DOC du périmètre génèrent (liste cochée) · parité gold vérifiée · genre/pluriel sourcé (G2a) · wording sourcé des modèles, sinon `QUESTIONS_RAFAEL.md` · suite **complète** verte (`--basetemp=artifacts/_audit_tmp/pt`) + ruff · conventions transverses (mois accentués) · existant byte-identique · `/release-readiness` si livrable PM, env nommé (r.67).

**DoD — WF-BUG :** cause `file:line` prouvée · test du cas qui plantait passe + non-régression ciblée verte (périmètre nommé) · ruff · si prod : fiche GO/NO-GO + rollback prêt · GO Gad avant merge `main` · registre dettes à jour.

**DoD — WF-AUDIT :** rapport daté, zéro mutation · findings classés · tout finding fort revérifié à la main · dérivés ré-injectés (nouvel ID, GATE 0/1) · branche d'origine restaurée, repo pas sur `main` · dettes inscrites.

### 5.2 Poka-Yoke — pré-conditions BLOQUANTES (mapping des règles)

| # | Pré-condition (action **impossible** si fausse) | Déclenche sur | Source |
|---|---|---|---|
| PY-1 | Bonne branche active ; jamais éditer sur `main` inattendue | tout edit/commit | r.**11** |
| PY-2 | Pas de suite DB en session live sur base partagée | PM/cobaye teste en réel | r.**60** |
| PY-3 | Périmètre de test nommé ; zéro résultat inféré | toute annonce « X verts » | r.**65** |
| PY-4 | Staging testable PM avant d'annoncer « en test » ; URL nommée | livrable destiné au PM | r.**67** |
| PY-5 | Fiche GO/NO-GO avant déploiement ; migration expand→migrate→contract | changement prod vivante | r.**70** |
| PY-6 | Verbatim ≠ paraphrase ; vérifier contre le mot client | tout fix retour | r.**65 + 68** |
| PY-7 | Demande non actionnable → ne descend pas (CLARIF ou défaut documenté) | gate intake | **§5.1** (neuf, r.12) |
| PY-8 | ≥ 2 occurrences du même écart → STOP patch, **Franky** ouvre un Problem | détection récurrence | chaîne ITIL + r.45 (Franky) |

### 5.3 Andon — stop-the-line

Tout agent **et** Jinbe peuvent stopper : signal → **STOP la propagation** + flag **1 ligne** (r.07/08), pose en défaut+escalade, puis **la file continue** (jamais de gel des autres items). **Reprise technique (E3) = Jinbe** ; si Jinbe indisponible → l'item reste `BLOQUÉ-REPRISE` daté, repris par le premier exécutant dispo / la prochaine session, **jamais routé vers Gad** (r.07 : technique ≠ PM). Gad n'est suppléant que pour une reprise portant une décision **produit (E1)** ou **irréversible (E5)**. **En mode audit-only (r.10)** : Andon = consigner le défaut dans le **rapport daté** + ouvrir un WF-BUG/WF-RETOUR — **jamais muter le code**.

| Signal Andon | Geste imposé | Vers qui |
|---|---|---|
| Dérive métier (règle produit changerait en silence) | STOP + flag, ne pas trancher seul | Robin (intent) ; Albane si juridique |
| Surface non ratifiée (écran/parcours neuf sans spec) | STOP build, pas de build silencieux | `design-scope-auditor` → `/design-brief` |
| Acte irréversible (merge `main`, migration, déploiement, contact externe) | STOP, GO PM obligatoire | Gad (Approver) |
| Branche `main` inattendue sous l'éditeur | STOP immédiat, ne rien éditer | `git-branch-steward` |
| Trou dans une source de vérité | STOP + alerte immédiate | Gad (jamais contourner) |
| Décision métier hors sources | `BLOQUÉ` (re-ping daté) + question au sachant | Albane via Gad (jamais inventer) |

### 5.4 Ownership — RACI / DACI / RAPID (couvre TOUS les nœuds des SOP)

**Invariants durs :** (1) un seul Accountable par nœud, un seul **Approver produit = Gad** ; (2) le **veto métier/juridique = Albane** (RAPID), **jamais soumis à l'Approver** ; (3) Driver ≠ Approver.

**RACI (exécution — tous les nœuds des 4 SOP) :**
- Classement/aiguillage/file → R/A **Jinbe** (routeur), C Vivi/Franky, I Gad
- Intake + triage + suivi retours → R/A **Vivi** (avant G1 et après G2 ; r.68)
- **Align / critères d'acceptation** (WF-RETOUR #4, WF-BUG #3) → R Chopper, **A Jinbe**, C Robin
- Fix technique retour/bug → R Chopper, **A Jinbe**
- **Triage incident** (WF-BUG #1) → R Jinbe (classe) puis handoff R→Chopper, **A Jinbe**
- **Cadrage Problem** (WF-AUDIT #1) → R Jinbe + Franky, **A Jinbe**
- **Promotion récurrence** (Incident→Problem) → **R/A Franky** (détecte+promeut) ; une fois WF-AUDIT ouvert, refonte → R Robin, **A Jinbe**
- Build type → R/A **Jinbe**, C Nami/Robin · Plan → R Nami, A Jinbe · Revue gate → **R Zoro**, A Jinbe · Git → R `git-branch-steward`, A Jinbe · Snapshot → R Brook · Méthode → **R/A Franky**. (Informed = Gad partout.)

**DACI (décisions produit) :** Périmètre/priorité → Driver Robin, **Approver Gad** · Go/Adjust litige de gate → Driver le gardien, **Approver Gad** · Choix produit/UX → Driver Robin (carte r.06), **Approver Gad** · Choix **technique** → Driver Jinbe, **Approver Jinbe** (décide ET annonce — r.07).

**RAPID (décisions à veto) :** Wording juridique / genre / pluriel / durée → Recommend Jinbe (extrait des modèles), Input NotebookLM, **Agree = Albane (veto)**, Decide Albane · Règle juridique d'un type → **Agree = Albane** · Mise en ligne prod → Perform Sanji, **Decide Gad** · Merge `main` → Input Zoro, **Decide Gad**.

> Le **veto métier (Albane)** ne remonte jamais à l'Approver produit (Gad) — chaîne séparée. Le **veto irréversible (Gad)** ne se délègue jamais à un agent.

---

## 6. Mapping sur l'existant

### 6.1 Ce qui EXISTE déjà (à nommer, pas à réinventer)

| Pièce | Source réutilisée |
|---|---|
| **Point d'entrée + aiguillage de phase** | routeur **00-phase-router** + **hook routing-first** (r.09) — fournissent l'entrée et le routage *signal→phase* ; ils ne produisent PAS encore le tuple ITIL (c'est le neuf) |
| **Capture + classement + suivi des RETOURS** | `returns-intake-organizer` (**Vivi**) + `docs/returns/*` + règle **68** — fonction **existante**, pas celle d'un dispatcher |
| **Détection + promotion récurrence (2 occurrences)** | `method-steward` (**Franky**) + règle **45** — fonction **existante**, pas celle d'un dispatcher |
| **WF-RETOUR** (Change) | Vivi + `docs/returns/*` + règle **68** |
| **WF-AFFAIRE** (Service Request) | skill `/type-entreprise` + `WORKFLOW_TYPE_ENTREPRISE_V1.md` |
| WF-BUG / GO PM | routeur **00** + `uat-fix-loop` (Chopper) + r.**60** ; prod → r.**70** + Sanji |
| Volet design | `design-scope-auditor` amont + `ui-designer` aval (routeur 00) |
| Gate fonctionnel | `functional-reviewer` (Zoro) via `/sprint-governance` |
| Cartes de décision PM | règle **06** + `AskUserQuestion` |
| Défaut documenté + non-blocage | règle **07** + `QUESTIONS_RAFAEL.md` |
| Veto métier Albane jamais soumis à l'Approver | règle **20** + mémoire `feedback-albane-direct-source` |
| Vocabulaire de statut (liste fermée) | `docs/returns/METHODE.md` §3 |
| Poka-Yoke épars | règles **11 / 60 / 65 / 67 / 70** |

### 6.2 Les 3 pièces NEUVES à créer (aucun agent)

1. **Invariant anti-impasse** — règle globale `~/.claude/rules/12-no-dead-end.md` (§4.1) + rappel en tête de `00-phase-router.md` + table d'escalade (§4.2). *Socle : tout en hérite.*
2. **Grille de classement 3×3 écrite** — greffée au routeur `00-phase-router.md` (§2.2–2.5) : la classification devient **explicite** (le routeur faisait du signal→phase, pas un tuple ITIL Type/Surface/P). Plus l'**auto-contrôle GATE 0** (§5.1).
3. **Gates Stage-Gate + DoD par workflow** — tableaux Go/Adjust (Adjust borné K=2) + DoD-checklists (§3, §5) intégrés à chaque SOP `WF-*` (`docs/returns/METHODE.md` pour WF-RETOUR, skill `/type-entreprise` pour WF-AFFAIRE, SOP dédiées pour WF-BUG/WF-AUDIT).

---

## 7. Plan de mise en place minimal

Pose sur la **branche de travail** du clone `sydel-document-engine-claude` — **jamais `main`** (r.11). Ordre :

1. **Invariant d'abord (socle).** Créer `~/.claude/rules/12-no-dead-end.md` (§4.1) + coller l'invariant + la table d'escalade (§4.2) **en tête de `00-phase-router.md`**. *Tout en hérite.*
2. **Grille de classement.** Greffer §2.2–2.5 + l'auto-contrôle GATE 0 au routeur 00 : *« demande substantielle → classer (grille 3×3) → router vers WF-* ; micro-action (sans écriture/Git/décision) → réponse directe »*. **Aucun agent créé.**
3. **Catalogue de workflows.** `docs/operations/workflows/` : `WF-BUG.md` + `WF-AUDIT.md` (SOP complètes, §3.3–3.4) ; WF-RETOUR/WF-AFFAIRE en **vue stage-gate** pointant vers `docs/returns/METHODE.md` et `WORKFLOW_TYPE_ENTREPRISE_V1.md`.
4. **Câblage qualité.** Gates en tête de `docs/returns/METHODE.md` (WF-RETOUR) et dans `/type-entreprise` (WF-AFFAIRE) ; Poka-Yoke (§5.2) en pré-conditions partagées.
5. **Ce document** = vue d'ensemble canonique ; les SOP `docs/operations/workflows/*` = détail exécutable.

**Décisions restant à Gad (1 ligne chacune) :** numéro de la règle anti-impasse (`12` proposé) · feu vert pour greffer la grille + l'invariant en tête du routeur 00 (changement **global**, tous projets) · « pose-les » → je crée les fichiers sur la branche de travail du clone `-claude`, jamais `main`. **Aucun blocage métier :** conception pure de dispositif process, rien d'irréversible, pas de sollicitation Albane requise.
```
