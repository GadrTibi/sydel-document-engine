# Plan — SELAS dentiste pluripersonnelle (lot retours Rafael 2026-06-17)

> Source : lock 008 `docs/review/albane_returns_2026-06-17/` (doc Rafael + 4 modèles).
> Findings **vérifiés à la main** (pas seulement sous-agent). Branche `sprint/engine-completion`.

## ✅✅ LIVRÉ — 2026-06-17 (chantier SELAS dentiste pluripersonnelle bouclé)
**Suite complète : 432 verts · ruff propre repo-wide.** Commits sur `sprint/engine-completion` :
- `78b894e` — **Attestation capital / liste des souscripteurs SELAS** (DOC-045), N souscripteurs en numéraire, accord en genre, câblé catalogue + orchestrator + registry.
- `ab15e78` — **Statuts SELAS dentiste** : corpus dentiste dédié (`Statuts_SELAS_dentiste_pluri_modele.docx`), sélection source + index par profession (`_SelasProfile`) ; médecin **byte-identique** préservé.
- `d11f479` — **PV nominations dirigeants** : multi-dirigeants (Président + Directeur Général), une décision/dirigeant (ordinaux dynamiques), signatures 2 colonnes, vocabulaire « actions » ; **verrou DG levé** dans le slice (champ additif `dirigeants_nomines`, mode mono SELARL/civils inchangé).
- `ee2a4ca` — fix genre comparution SELAS multi (« né/née », « Inscrit/Inscrite »).
- bornes **SELAS multi 2→6** associés (le cas 1 associé = flux uniperso existant `statuts_selas_medecin`).
- Procuration SELAS : **déjà fidèle**, rien à faire (P3).

### ⚠️ Points de fidélité à confirmer avec Albane (relevés, NON inventés)
1. **PV — titre « EXTRAORDINAIRE »** : le modèle dit « ASSEMBLÉE GÉNÉRALE EXTRAORDINAIRE » mais un test existant (chemin SCI/parts) interdit « EXTRAORDINAIRE » → titre laissé « ASSEMBLÉE GÉNÉRALE » (partagé). À trancher si la SELAS doit dire « EXTRAORDINAIRE ».
2. **PV — clause matrimoniale dans la phrase de nomination** : le modèle montre « marié sous le régime de… » dans l'identité du dirigeant ; le slice ne collecte pas cette donnée → non rendue (champ additif `identite_phrase` en place pour la porter plus tard sans refonte).
3. **Attestation — token « apport en nature »** du modèle = en réalité montant **numéraire** par souscripteur (capital SELAS = numéraire) → calculé `nb_actions × valeur_nominale`.
4. **Cas 1 associé SELAS dentiste** : routé vers l'uniperso ; vérifier qu'un uniperso DENTISTE existe (sinon gap mineur).

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
