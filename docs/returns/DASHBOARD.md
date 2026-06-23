# DASHBOARD — Retours client (compteur de vitesse)

> Vue vivante de l'état des retours. Source de vérité détaillée : `CARNET.md`. MAJ manuelle à chaque jalon.
> Légende : ✅ traité · 🟡 traité partiel (propagation due) · ⬜ à faire · ❓ à clarifier · 🔴 défaut Akainu.

```
┌─ SYDEL · RETOURS CLIENT — compteur de vitesse ──────────────────────────
│
│   CORRIGÉS  [████████████████████████]  T1(10) + T2(5 MAJEUR) + T3(3 MAJEUR+résidus)
│   re-Akainu OK ✅ : O24-01,07,10 · LIVE-02   ·   re-Akainu T3 (6 items) EN COURS
│   T3 racine committé a152bf4 (550 verts) : O24-03,11,14 MAJEUR + 05,12,LIVE-03
│   VALIDÉ  (Rafael)     [░░░░░░░░░░░░░░░░░░░░░░░░]   0/21  ·   0%   ⚠ rien validé
│   RESTE : propagation Q4 (adresses tous types) · O24-04 icône · L5/L6 clarif
│
│   ── ONGLET 24 (✅=Akainu OK · 🟢=corrigé, re-Akainu en cours · ⬜=à faire) ──
│   ✅ 01 annexe Sydel (Akainu OK)        ✅ 02 DNC nommée/dirigeant
│   🟢 03 adresses 1 ligne (numéro requis)  ⬜ 04 icône copier (décision UI)
│   🟢 05 valeur nominale (+ SCM cédée)   ✅ 06 pluri=multi   ✅ 08 date+adresse 1×
│   ✅ 07 Président (racine, Akainu OK)    ✅ 09 « (profession) »
│   ✅ 10 dérivation dentaire (Akainu OK) 🟢 11 vendeur (régime+conjoint, PACS exclu)
│   🟢 12 case cabinet (édition préservée) ✅ 13 CA non facultatif
│   🟢 14 acte+compromis (salariés tolérés) ✅ 15 acquéreur retiré
│
│   ── RETOURS LIVE ───────────────────────────────────────────────────
│   ✅ L1 situation=menu   🟢 L2 case régime morte supprimée   🟢 L3 mois accentués   ✅ L4 choix étape
│   ❓ L5 lettre renonciation   ❓ L6 « case à la fin »   → illisibles, clarif Rafael
│
│   RESTE : propagation Q4 (adresses tous types) · 04 icône copier · L5/L6 (clarif)
│   GARDE-FOU : 0 validé tant que Rafael n'a pas reconfirmé (traité ≠ validé)
└──────────────────────────────────────────────────────────────────────────
```

## Jauges (définitions)

- **TRAITÉ** = fait + poussé + vérifié contre le verbatim par nous (gate règle 66 / Akainu en cours).
- **VALIDÉ** = Rafael a confirmé en retest. Reste à **0** par discipline (`traité ≠ validé`).
- **AKAINU** = retours passés à l'auditeur adversarial (règle 66).

## Reste à traiter (le « pourquoi 3 trucs »)

| # | Pourquoi ça reste | Action |
|---|---|---|
| O24-03 propagation | traité SELAS-only ; règle Q4 (Gad) = propager à tous les cas | build : adresses 1 ligne sur SELARL/SAS/SPFPL/SCI/SCS/SCM/SELAS-uni |
| O24-04 icône copier | Streamlit n'a pas de copier natif sur un champ → décision UI | trancher l'approche + build tous types |
| L5 / L6 | mini-screenshots **illisibles** : sens inconnu | question Rafael (`QUESTIONS_RAFAEL.md`) — ne pas deviner |
