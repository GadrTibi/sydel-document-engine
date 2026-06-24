# DASHBOARD — Retours client (compteur de vitesse)

> Vue vivante de l'état des retours. Source de vérité détaillée : `CARNET.md`. MAJ manuelle à chaque jalon.
> Légende : ✅ traité · 🟡 traité partiel (propagation due) · ⬜ à faire · ❓ à clarifier · 🔴 défaut Akainu.

```
┌─ SYDEL · RETOURS CLIENT — compteur de vitesse (post-convergence T10) ─────
│
│   CORRIGÉ (code)    [███████████████████████░]  20/21 · 95%
│   CONTRÔLE AKAINU   [███████████████████████░]  20/21 · 95%  ✅ L6 RIEN À REDIRE
│   VALIDÉ  (Rafael)  [░░░░░░░░░░░░░░░░░░░░░░░░]   0/21 ·  0%  ⚠ rien validé (normal)
│   gate : CORRIGÉ ≥ AKAINU ≥ VALIDÉ — un retour ne passe Rafael qu'après Akainu OK
│   Akainu : convergence T10 + L6 (SPFPL) RIEN À REDIRE (2026-06-24). 594 verts.
│   RESTE : O24-04 icône copier UNIQUEMENT (cadré Gad, § 6bis debrief)
│
│   ── ONGLET 24 (✅=Akainu OK · ⬜=à faire) ──────────────────────────────
│   ✅ 01 annexe Sydel (régen-propre tous types)   ✅ 02 DNC nommée/dirigeant
│   ✅ 03 adresses 1 ligne (propagé tous types)     ⬜ 04 icône copier (cadré Gad)
│   ✅ 05 valeur nominale (+ SCM cédée)   ✅ 06 pluri=multi   ✅ 08 date+adresse 1×
│   ✅ 07 Président (racine, Akainu OK)    ✅ 09 « (profession) »
│   ✅ 10 dérivation dentaire (Akainu OK)  ✅ 11 vendeur (régime+conjoint, PACS exclu)
│   ✅ 12 case cabinet (édition préservée) ✅ 13 CA non facultatif
│   ✅ 14 acte+compromis (salariés tolérés) ✅ 15 acquéreur retiré
│
│   ── RETOURS LIVE ───────────────────────────────────────────────────
│   ✅ L1 situation=menu   ✅ L2 case régime morte supprimée   ✅ L3 mois accentués   ✅ L4 choix étape
│   ✅ L5+L6 case « Régime communautaire » SPFPL → menu (Akainu RIEN À REDIRE)
│
│   RESTE : O24-04 icône copier UNIQUEMENT (cadré Gad, ton « go » attendu)
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
| O24-04 icône copier | non shippable à l'aveugle (non testable headless + dép + scope UX) | greenlight Gad + build vérifiable (`DEBRIEF_SPRINT_NUIT_2026-06-24.md` § 6bis) |
| L5 / L6 | mini-screenshots **illisibles** : sens inconnu | question Rafael (`QUESTIONS_RAFAEL.md`) — ne pas deviner |
