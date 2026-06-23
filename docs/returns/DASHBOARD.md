# DASHBOARD — Retours client (compteur de vitesse)

> Vue vivante de l'état des retours. Source de vérité détaillée : `CARNET.md`. MAJ manuelle à chaque jalon.
> Légende : ✅ traité · 🟡 traité partiel (propagation due) · ⬜ à faire · ❓ à clarifier · 🔴 défaut Akainu.

```
┌─ SYDEL · RETOURS CLIENT — compteur de vitesse ──────────────────────────
│
│   CORRIGÉ (code)    [████████████████████░░░░]  18/21 · 86%
│   CONTRÔLE AKAINU   [██████████████░░░░░░░░░░]  12/21 · 57%  (6 en contrôle T3)
│   VALIDÉ  (Rafael)  [░░░░░░░░░░░░░░░░░░░░░░░░]   0/21 ·  0%  ⚠ rien validé
│   gate : CORRIGÉ ≥ AKAINU ≥ VALIDÉ — un retour ne passe Rafael qu'après Akainu OK
│   T3 (a152bf4, 550 verts) EN COURS : O24-03,11,14 + 05,12,LIVE-03
│   RESTE : propagation Q4 · O24-04 icône (décision) · L5/L6 (clarif Rafael)
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

## Jauges (définitions) — 3 barres progressives

Un retour avance de gauche à droite : **CORRIGÉ → CONTRÔLE AKAINU → VALIDÉ**. La barre de droite
ne peut jamais dépasser celle de gauche (gate).

- **CORRIGÉ (code)** = le fix est écrit + poussé sur la branche (tests verts). Ne dit rien de la qualité.
- **CONTRÔLE AKAINU** = l'auditeur adversarial (règle 66) a rendu **RIEN À REDIRE** sur ce retour,
  vérifié contre son **verbatim** par régénération réelle. C'est NOTRE gate qualité interne, AVANT
  de montrer quoi que ce soit à Rafael. Un retour avec un défaut Akainu ouvert n'y est PAS compté.
- **VALIDÉ (Rafael)** = Rafael a confirmé en retest réel. Reste à **0** par discipline (`traité ≠ validé`) :
  rien ne passe ici tant qu'il n'a pas reconfirmé, et seulement après Akainu OK.

## Reste à traiter (le « pourquoi 3 trucs »)

| # | Pourquoi ça reste | Action |
|---|---|---|
| O24-03 propagation | traité SELAS-only ; règle Q4 (Gad) = propager à tous les cas | build : adresses 1 ligne sur SELARL/SAS/SPFPL/SCI/SCS/SCM/SELAS-uni |
| O24-04 icône copier | Streamlit n'a pas de copier natif sur un champ → décision UI | trancher l'approche + build tous types |
| L5 / L6 | mini-screenshots **illisibles** : sens inconnu | question Rafael (`QUESTIONS_RAFAEL.md`) — ne pas deviner |
