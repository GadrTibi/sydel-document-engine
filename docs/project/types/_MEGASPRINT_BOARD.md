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

## État par type

| Type | Voie A — NotebookLM | Voie B — Build | Bloquant / décision |
| :--- | :--- | :--- | :--- |
| SELARL | — (réf, fini) | **livré + mergé main** | — |
| SELAS | ✅ rangé (`6b6d413`) | readiness en cours | **scope multi+PM+DG vs V1 unique → GO Gad** ; tokeniser Reynaud (Downloads) |
| SPFPL | ✅ rangé (`915218c`) | readiness en cours | toujours SPFPLAS ; tokeniser 33 modèles ; Rafael (apport) |
| SCM | ✅ rangé (`3d72507`) | readiness en cours | carte cas→docs (Rafael) ; clé répartition dépenses |
| SCI | prompts donnés (collage en cours) | readiness en cours | canon V1 vs V2/V3 ; modèle Lettre option IS (Rafael) |
| SCS | à venir | readiness en cours | canon V1 only |
| SCP | à venir | readiness en cours | — |
| SAS | à venir | readiness en cours | — |

---

## Décisions fonctionnelles en attente (Gad uniquement)

- **SELAS scope** : multi 2-5 + personne morale associée + DG **supersede** le périmètre V1
  « actionnaire unique ». À ratifier **avant** de figer le build SELAS (pas avant le socle B0).

## Escalades métier (Rafael, groupées — jamais Gad)

- SELAS : wording multi/personne morale/DG (après modèle Reynaud).
- SPFPL : parcours apport (objet, report 150-0 B ter, conditions suspensives) après les 33 modèles.
- SCM : carte cas→docs, clé de répartition des dépenses, inscription Ordre SCM, pluriel (Albane).
- SCI : version canon qui fait foi, modèle « Lettre d'option IS ».
