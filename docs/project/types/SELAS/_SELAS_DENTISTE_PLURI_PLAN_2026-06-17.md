# Plan — SELAS dentiste pluripersonnelle (lot retours Rafael 2026-06-17)

> Source : lock 008 `docs/review/albane_returns_2026-06-17/` (doc Rafael + 4 modèles).
> Findings **vérifiés à la main** (pas seulement sous-agent). Branche `sprint/engine-completion`.

## Verdict du lot
- **Toutes les « corrections V2 »** (textuelles + 15 points du PV) = **DÉJÀ FAITES** (le doc Rafael décrivait un état moteur plus ancien). Vérifié : 15/15 items PV OK, 3 corrections textuelles déjà en place (sous-agent + génération réelle).
- Le **seul vrai chantier neuf** = **SELAS dentiste pluripersonnelle** (4 modèles joints).
- **SELARL multi-associés** (tickets V3) = **GATÉ** : contredit SELARL-SCOPE-1 (uniperso) ET Albane elle-même (05/06 « laissons tomber la SELARL à plusieurs associés »). GO Gad de construire, mais **question de confirmation Albane en attente** avant build (probable artefact Rafael).

## ✅ Déjà livré dans ce lot
- **Bug genre SELAS multi corrigé** : `statuts_selas_multi.py` — « née »/« Inscrite » figés au féminin → accord par `associe.genre` (`_associe_est_feminin`). Test masculin ajouté (`test_..._masculin_accorde_ne_et_inscrit`). Défaut de fidélité pré-existant sur du SELAS déjà livré.

## Reste à construire (priorisé, vérifié)
1. **P0 — Statuts SELAS dentiste pluripersonnelle.** Le moteur génère depuis un **corpus médecin** (`Statuts_SELAS_multi_modele.docx`, 38 articles, « DEONTOLOGIE MEDICALE », « ASSOCIE MEDECIN »…), **≠** du nouveau modèle dentiste (`MODELE_statuts_SELAS_dentiste_pluripersonnelle.docx`, 32 articles, structure/wording propres, art. 19 Président / art. 20 DG / art. 32 signature élec). → **tokeniser le nouveau modèle dentiste** en source dédiée + brancher (paramétrer la source par profession). La **mécanique N-associés est réutilisable** (comparution/apports/répartition/président/signature dynamiques). Corriger au passage : élision « du Ille et Vilaine » → « d'Ille-et-Vilaine » ; rendre `qualification_principale` optionnelle (médecin-spécifique) ; aligner la clause « marié sous le régime de… » sur la règle V2.
2. **P0 — Attestation capital / liste des souscripteurs SELAS.** **Absente du catalogue SELAS** (vérifié : `case_catalog.py` ne la liste que pour SPFPL_APPORT + SAS). Le générateur SPFPL `attestation_capital_liste_souscripteurs.py` est **mono-souscripteur** (`_unique_souscripteur` lève si ≠1, « actionnaire unique »). Le modèle SELAS exige **N souscripteurs en numéraire** (répartition + apport par associé). → nouveau générateur multi-souscripteurs numéraire SELAS + occurrence catalogue SELAS.
3. **P1 — PV nominations dirigeants (Président + DG).** Le PV actuel fait **UNE** nomination ; le modèle en fait **DEUX** (PREMIÈRE = Président, DEUXIÈME = Directeur Général) + bloc signatures **2 colonnes** (« Bon pour acceptation des fonctions de Président / de Directeur Général »), vocabulaire **« actions »** (≠ « parts »). Le wording DG est **désormais fourni** → lever le verrou DG de `selas_multi_slice.py` (l.297-320 « DG : à venir »).
4. **P2 — Bornes associés 1 à 6** (actuel `SELAS_NB_MIN=2 / MAX=5`). Cas **1 associé** = router vers le générateur uniperso (`statuts_selas_medecin.py`) ? à trancher. 6 associés = vérifier l'injection dynamique des blocs source.
5. **P3 — Procuration SELAS** : **déjà fidèle** (structure-agnostique, `fonction_dirigeant="Président"`, RCS/tél SYDEL présents). Rien — au plus retirer une virgule cosmétique.

## Garde-fous
- Fidélité : tokeniser/reproduire le modèle source verbatim, jamais inventer le wording juridique. Cas DG : wording pris du modèle fourni.
- ⚠️ Conflit procuration RCS/tél (round1 ajouter vs round2 retirer) — confirmer côté Albane avant de défaire (cf. message confirmations).
- Reprise à froid de ce chantier → ce fichier + lock 008 + `JOURNAL_DECISIONS_SELARL_V1.md`.
