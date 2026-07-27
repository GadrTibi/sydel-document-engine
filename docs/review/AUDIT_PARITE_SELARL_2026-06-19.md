# Audit de parité SELARL → autres types (2026-06-19)

> SELARL = référence « parfaite ». Audit lecture-seule (workflow `wi8j4ud4m`, 10 agents) : 42 features
> SELARL comparées à 9 types, croisées au canon + aux modèles source. Données brutes :
> `_audit_parite_findings.json` + `_audit_parite_gold.json`.

## Verdicts (375 comparaisons)
- **141 DÉJÀ CONFORMES** — la parité est déjà acquise (souvent via les générateurs partagés).
- **132 LÉGITIMEMENT DIFFÉRENTS** — différence normale pour le type (canon/modèle la justifie) → ne pas répliquer.
- **33 À RÉPLIQUER** — comportement SELARL validé, absent/différent sans raison légitime.
- **69 « à confirmer »** → après consolidation (~12 thèmes) et croisement aux sources : **quasi tous résolus**
  (consistance évidente que je fais, ou vérifiable dans les modèles). **0 vraie question Rafael.**

---

## A. JE FAIS — corrections de parité claires (sur GO Gad, sans déranger Rafael)
Toutes justifiées par la SELARL validée + zéro risque métier (UX/ergonomie/format/confort déjà ratifié).

| # | Parité à porter | Vers | Effort |
|---|---|---|---|
| 1 | **Conseiller/mandataire éditable** (défaut Jordan ELBAZ) — ratifié Albane 2026-06-10 | SAS, SCM, SCI IRIS, SCS (où le doc a un mandataire) | S |
| 2 | **Capital en `number_input` + format groupé « 1 000 »** (anti « 1000 » brut) | tous les types en saisie libre | S |
| 3 | **Nom de fichier « Statuts {dénomination}.docx »** — confort ratifié Albane | SELAS uni, SAS, SCM, SCI, SCI IRIS, SCS | S |
| 4 | **Lieu de signature = ville du siège** (pré-rempli, modifiable) | SELAS, SAS, SPFPL | S |
| 5 | **« Madame la Présidente »** (présidente de l'ordre femme) | SELAS, SPFPL, SCM (demande inscription ordre) | S |
| 6 | **Connecteur « de »/« du »** devant le département de l'ordre (R6) | SPFPL cession, SCM | S |
| 7 | **Bouton « Aujourd'hui »** sur toutes les dates | SPFPL cession (+ étendre où partiel) | S |
| 8 | **Nationalité en déroulant** (NATIONALITY_PRESETS + « Autre ») | SAS, SPFPL | S |
| 9 | **2e lieu d'exercice additif** (siège = lieu #1) | SELAS uni médecin | S |
| 10 | **Case « siège identique à l'adresse perso »** | SELAS uni, SPFPL | S |
| 11 | **Cadre STATUTS aéré** (marges de cellule, §2.1) | types à cadre STATUTS bordé | M |
| 12 | **Dates d'exercice pré-remplies** (1er janv / 31 déc / clôture N+1) | SELAS uni, SAS, SPFPL | S |
| 13 | **Durée figée 99 ans** (pas de saisie, cohérence §18.3) | SELAS uni médecin | S |

## B. À VÉRIFIER MOI-MÊME DANS LES SOURCES (je résous, pas de question)
- **Nombre d'exemplaires par type** (« trois » vs « quatre ») → **fidélité au modèle de chaque type** (le modèle fait foi ; pas de réplication aveugle vers 4).
- **« euros » après le capital dans les STATUTS** → uniquement si le modèle source ne le porte pas déjà (anti-doublon).
- **Régime communautaire DOC-005/006 pour SELAS uni médecin / SAS** → selon le canon « Si régime communautaire » (si l'associé peut être marié communauté).
- **Police Roboto footer statuts** → seulement si le modèle du type le prévoit (sinon fidélité).

## C. LÉGITIMEMENT DIFFÉRENT — on ne touche pas
- **Cession / SCM** (actes, compromis, bail, appel de fonds) pour SELAS uni / SPFPL → **hors création V1** (périmètre ratifié Rafael : création uniquement).
- **PV nomination gérant SCM** (co-gérants, durée indéterminée) → structure civile distincte de la SELARL.
- **Titre STATUTS bordé / non-bordé, saut de page annexe** → fidélité au modèle source (médecin table vs dentiste flux).
- **Profession libre** côté civils (SCM/SCI/SCS) → pas de table d'accents/pluriels (pas une profession réglementée à corpus figé).

## D. Questions Rafael
**Aucune.** Après consolidation + croisement aux sources, tout est soit de la parité évidente (bloc A),
soit vérifiable dans les modèles/canon (bloc B), soit légitimement différent (bloc C). Conforme à la
consigne « ne pas inventer de questions dont la réponse est dans le matériel ».
