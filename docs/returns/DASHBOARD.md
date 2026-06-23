# DASHBOARD — Retours client (compteur de vitesse)

> Vue vivante de l'état des retours. Source de vérité détaillée : `CARNET.md`. MAJ manuelle à chaque jalon.
> Légende : ✅ traité · 🟡 traité partiel (propagation due) · ⬜ à faire · ❓ à clarifier · 🔴 défaut Akainu.

```
┌─ SYDEL · RETOURS CLIENT — compteur de vitesse ──────────────────────────
│
│   AKAINU OK (rien à redire) : O24-01 ✅ · O24-10 ✅   ·   LIVE-03 corrigé
│   EN DÉFAUT (à corriger)  [███████░░░░░░░░░░░░░░░░░]   7  ·  bloquant/majeur restants
│   VALIDÉ  (Rafael)     [░░░░░░░░░░░░░░░░░░░░░░░░]   0/21  ·   0%   ⚠ rien validé
│   BLOQUANT restants : O24-03 · O24-14   ·   MAJEUR : O24-05/07/11/12 + LIVE-02
│
│   ── ONGLET 24 (🔴 = défaut Akainu à corriger) ───────────────────────
│   ✅ 01 annexe Sydel — Akainu RIEN À REDIRE   ✅ 02 DNC nommée/dirigeant
│   🔴 03 adresses (ordre 3 champs + double siège + parser KO + propagation)
│   ⬜ 04 icône copier (décision UI)   🔴 05 valeur nominale (manque SELARL)
│   ✅ 06 pluri=multi   🔴 07 rôles (DG requalifié Président ; Président pas obligatoire)
│   ✅ 08 date+adresse 1×   ✅ 09 « (profession) »
│   ✅ 10 dérivation dentaire — Akainu RIEN À REDIRE   🔴 11 vendeur (régime+conjoint perdus)
│   🔴 12 case cabinet (test non-discriminant)   ✅ 13 CA non facultatif
│   🔴 14 acte+compromis CRASH génération   ✅ 15 acquéreur retiré
│
│   ── RETOURS LIVE ───────────────────────────────────────────────────
│   ✅ L1 situation=menu   🔴 L2 case régime (reste ailleurs)   🔴 L3 « aout » non accentué   ✅ L4 choix étape
│   ❓ L5 lettre renonciation   ❓ L6 « case à la fin »   → illisibles, clarif Rafael
│
│   RESTE : 03-propagation (7 types) · 04 icône copier · L5/L6 (clarif)
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
