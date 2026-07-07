# CHECKLIST MAÎTRE — PV d'agrément cession SPFPL (DOC-038 associé unique · DOC-039 plusieurs associés)

> Code : `generators/lot_05/pv_agrement_cession_spfpl_associe_unique.py` /
> `pv_agrement_cession_spfpl_plusieurs_associes.py`, socle partagé `pv_agrement_common.py`.
> Sélection par `dossier.options.associe_unique` (true → DOC-038, false → DOC-039). SPFPL cession uniquement.
> Un fix sur le socle touche LES DEUX ; un fix sur une variante doit être balayé sur l'autre.
> S'ajoute à `_transverse.md`.

## Attentes cumulées

- [x] Plage de parts « numérotées de … à … inclus » : entièrement OMISE si non renseignée — jamais de phrase incomplète — Albane 13 (2026-07-06) — statut : **fait** (PV SPFPL ✅ registre « omission-si-vide » ; groupe NOTE+PV+ATTEST)
- [ ] Propagation de l'omission-si-vide aux surfaces SCM (`acte_cession_parts_scm.py:301`, `pv_age_cession_scm.py:226/338` rendent encore « (À COMPLÉTER) ») — balayage registre 2026-07-06 — statut : **pas fait** (flag Albane : le principe est-il universel ? basse priorité tracée)
- [ ] Plage de parts AUTO-DÉDUITE de la répartition (20 parts → « 1 à 20 »), plus de saisie texte libre — **Albane 2026-07-07** — statut : **contradiction résolue → à faire**. Les plages SPFPL sont en **texte libre** « écho fidèle de la saisie » (convention Rafael, N4 2026-06-24 + SP3 tracé « défaut = fidèle à la saisie ») ; **le 07-07 prime** : dériver la plage automatiquement comme SCM/SELARL (`_assign_cumulative_part_ranges`), supprimer la saisie manuelle
- [ ] Accent « numérotées de 41 **à** 100 » (jamais « a ») — SP3/N4 (Akainu 2026-06-25) + 07-07 « accents partout » — statut : **partiel → absorbé par l'auto-déduction ci-dessus** (les plages auto-calculées sont accentuées depuis `c609a33` ; le texte libre échoit la saisie brute — disparaît si la saisie manuelle tombe)
- [x] Totalité des parts présente ou représentée (DOC-039) — spec lot 5 — statut : **fait** (structurel)
- [x] Wording cession conservé (pas de formule apport) — arbitrage V1 — statut : **fait**
- [ ] Interligne PV à 0 (désignation société en-tête, désignation client, chaque décision d'AG) + espace entre la 1re décision et le texte suivant — mise en forme 1.4 (2026-07-03, « pour les PV ») — statut : **à vérifier** (le groupe C du lot visait le tronc ; confirmer que les PV d'agrément SPFPL ont bien reçu 1.4 — sinon propager)
- [ ] Transverse 07-07 sur le doc régénéré : montants « lettres (chiffres) euros » groupés, « Docteur » ≠ civilité, élision « d'un » — statut : **à vérifier** (aucun passage dédié tracé sur DOC-038/039)

## Rappels

- Le PV cite la répartition/les parts cédées : toute évolution de la **répartition unique** (07-07, cf. `acte_cession_parts.md`) et de l'auto-déduction des plages doit être régénérée ici aussi (cohérence acte ↔ PV).
- Cousins PV hors périmètre direct mais mêmes conventions : DOC-031 (PV AGE cession SCM — items A26-75→81 traités lots 2026-06-26) et DOC-004 (PV nomination — interligne/tirets/espaces A26-26/27, traités).
