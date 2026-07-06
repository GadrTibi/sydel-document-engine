# REGISTRE DE PROPAGATION — conventions universelles × types

> **But** : outiller la règle 68 Q4 (le principe « propager à tous les cas » échouait en réactif/mémoriel).
> **Gate (règle 68)** : avant tout TRAITÉ d'un point de CONVENTION universelle, compléter la cellule
> `[convention][type]` + vérifier que chaque autre type porteur est `fait`/`à faire`. Cellule vide = pas TRAITÉ.
> **Légende** : ✅ fait (commit) · ⬜ à faire (déclencheur) · ➖ N/A (structure absente) · ❓ à vérifier (dette).
> Créé Gad 2026-07-06. Vivant : se complète au fil des fixes + du balayage.

## Types (colonnes)
SELARL-uni · SELARL-multi · SELAS-uni-med · SELAS-uni-dent · SELAS-pluri · SPFPL-cession · SPFPL-apport · SAS · SASU · SCI · SCM · SCS · SCI-IRIS · micro-holding

## Conventions (lignes) — état par type

| Convention | SELARL uni | SELARL multi | SELAS uni | SELAS pluri | SPFPL cess | SPFPL app | SAS | SASU | SCI | SCM | SCS | SCI-IRIS | micro |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Montant euro** « [lettres] euro(s) ([chiffres] €) » (capital art.8) | ➖ᵐ | ➖ᵐ | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ᵐ | ➖ | ➖ | ➖ | ➖ | ➖ |
| **Titre « Statuts [Nom] »** | ✅ | ✅ | ❓ | ❓ | ✅ | ✅ | ✅ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| **Case « même adresse »** (cible/exercice) | ➖ | ➖ | ✅(cession) | ✅(cession) | ✅(cession) | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |
| **Prénom usuel vs prénoms complets** (statuts) | ✅ | ➖ᵐ | ✅ | ➖ᵐ | ✅ | ✅ | ✅ | ✅ | ➖ | ➖ | ➖ | ➖ | ➖ |
| **Menu matrimonial complet + conjoint conditionnel** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❓ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Conjoint PACSÉ (wording)** | ❓ | ❓ | ❓ | ❓ | ⬜(flag Albane) | ⬜ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| **Département Ordre en NOM (pas numéro)** | ✅ | ✅ | ✅ | ✅ | ✅ | ➖(ville) | ✅ | ➖(pas d'Ordre) | ➖ | ➖ | ➖ | ➖ | ➖ |
| **Préposition de/du/des dept** | ➖faible | ➖faible | ➖faible | ➖faible | ✅(acte) | ➖faible | ➖faible | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |
| **Omission-si-vide (plages « numérotées de … »)** | ➖ | ➖ | ➖ | ➖ | ✅(PV) | ➖ | ➖ | ➖ | ➖ | ⬜? | ➖ | ➖ | ➖ |
| **Police Roboto 10** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Interligne simple (from-scratch)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ➖(inj) | ➖ | ➖ | ➖ | ➖ |
| **Majuscule liste soussigné** | ➖ | ➖ | ➖ | ➖ | ✅ | ✅ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |
| **Signature client à droite** (procuration/Ordre) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ➖ | ➖ | ➖ | ➖ |
| **Saut de page avant annexe** | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅(modèle) | ➖ᵐ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Adresse sur une ligne** (O24-03) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **DNC par dirigeant** (O24-02) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Attestation capital présente** (création) | ⬜(flag) | ⬜ | ✅ | ✅ | ✅ DOC-051 (critère Albane n°14) | ✅ | ✅ | ✅ | ⬜(flag) | ⬜ | ✅ | ⬜ | ⬜ |
| **Apport associé unique = capital** (uni) | ✅ | ➖ | ✅ | ➖ | ✅ | ✅ | ➖ | ✅ | ✅ | ✅ | ➖ | ✅ | ✅ |

> **Légende maj** : ✅ fait · ⬜ à faire (déclencheur) · ➖ N/A · ➖ᵐ forme dictée par le modèle ratifié (harmoniser = question Albane, pas dette code) · ➖faible risque négligeable (préposition « de » + nom de dept ne commençant quasi jamais par voyelle) · 🔧 fix en cours · ❓ non ré-audité.
> **Balayage 2026-07-06 (agent read-only, HEAD 4c12b79)** — 2 dettes RÉELLES trouvées :
> 1. **Département Ordre en NOM** (Albane 7.4) — **✅ RÉSOLU 2026-07-06 (2 tours Akainu → RIEN À REDIRE)**. Était siloé sur SPFPL cession seul. Propagé à **~14 surfaces** de sortie : statuts SAS/SELARL(dentiste)/SELARL-multi/SELAS-multi, `acte_cession_parts_spfpl`, `acte_cession_actions_spfpl` (cédant + SPFPL + cible), `contrat_apport_spfpl`, `acte_cession_parts_scm`, `spfpl_common` (ordre_sentence), `formulaire_derogation_sites_sel`, **cession_cabinets_common** (4 modèles cabinet, rattrapé par Akainu). Gardes ajoutées : test unitaire `departement_nom` + assertions d'intégration numéro→nom (acte parts + acte actions). NB : `[ville_ordre]` (templates médecin) = VILLE, non concerné ; `scm_cession_common:232` = validation pure (valeur jetée). `departement_naissance` jamais touché (pas d'over-reach).
> 2. **Saut de page avant annexe** absent du rendu SPFPL (`statuts_spfpl_common.py render_statuts_docx`) alors que SELARL/SELAS/SAS l'ont — traité avec prudence (pas de verbatim Albane explicite).
> **Candidat à vérifier** : omission-si-vide « numérotées de … inclus » (Albane 13) présente au PV agrément SPFPL seul ; surfaces SCM (`acte_cession_parts_scm.py:301`, `pv_age_cession_scm.py:226/338`) à confronter au verbatim si l'omission doit s'y propager.
