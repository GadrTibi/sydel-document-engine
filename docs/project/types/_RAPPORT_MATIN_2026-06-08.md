# Rapport du matin — nuit du 2026-06-07 → 08 (état FINAL)

> Branche `sprint/engine-completion` (clone `-claude`). **Rien sur `main`, rien déployé, zéro donnée
> réelle versionnée.** Suite complète **366 verts** (PYTHONPATH forcé sur le bon clone, ordre
> déterministe). Tout est réversible et soumis à ta validation. Bar honnête : **bâti +
> auto-vérifié techniquement end-to-end** ; la **justesse juridique** reste la revue Rafael/Albane
> (que tu avais prévue). Ce rapport remplace la version de 01:11 (qui datait d'avant les bundles).

## 0. LE point que tu attends : « quel document générer par cas » (canon = `Documents_a_generer_par_cas` V1)

Chaque type émet désormais **le bundle de création complet du canon**, pas seulement les statuts.
Vérifié **end-to-end** : les tests génèrent réellement chaque `.docx` et vérifient (a) le set de
fichiers attendu, (b) **zéro placeholder résiduel** (`[`/`]`) dans paragraphes + tableaux + footers.

| Type | Bundle CRÉATION imposé par le canon | Câblé & généré propre | Conformité |
| :--- | :--- | :--- | :--- |
| **SELARL** (réf, sur `main`) | DNC, domic, procuration, PV gérant, inscription ordre, statuts (médecin/dentiste) · *cond.* régime | idem | ✅ conforme |
| **SELAS** (DOC-044 multi) | DNC, domic, proc, PV gérant, inscription ordre, statuts · *cond.* régime | idem (+ toggle régime) | ✅ conforme |
| **SPFPL cession** (DOC-035) | DNC, domic, proc, PV gérant, inscription ordre, statuts, **note d'info** · *cond.* régime | tout sauf **note d'info** | ⚠️ note d'info en réserve |
| **SPFPL apport** (DOC-036) | idem cession (statuts apport) + **note d'info** · *cond.* régime | tout sauf **note d'info** | ⚠️ note d'info en réserve |
| **SCS** (DOC-019) | DNC, domic, proc, PV gérant, statuts | idem | ✅ conforme |
| **SCI** (DOC-020) | DNC, domic, proc, PV gérant, statuts · *cond.* « Si IS » lettre option IS | idem (+ toggle option IS) | ✅ conforme |
| **SCI IRIS** (DOC-021) | idem SCI (statuts IRIS) · *cond.* option IS | idem (+ toggle option IS) | ✅ conforme |
| **SCM** (DOC-025) | DNC, domic, proc, PV gérant, inscription ordre, statuts, **pacte + liste dépenses + contrat frais communs + RI** | tout sauf **les 4 satellites** | ⚠️ 4 satellites en réserve |
| **SAS** (DOC-015) | DNC, domic, proc, statuts, attestation capital, PV rémunération président (pas de PV gérant ni inscription ordre) | idem | ✅ conforme |

**Conditionnels du canon, câblés en triple verrou (front + moteur + bundle), OFF par défaut :**
« Si régime communautaire » → renonciation (DOC-005) + avertissement conjoint (DOC-006) pour SELAS +
SPFPL ; « Si IS » → lettre option IS (DOC-022) pour SCI/SCI IRIS. OFF = bundle de base inchangé ;
ON sans la saisie requise = **bloqué** (jamais de doc partiel). Conforme au canon, qui ne liste ces
conditionnels que là (pas de fuite vers SCS/SCM/SAS).

## 0bis. Ce qui N'EST PAS câblé — et POURQUOI (jamais abandonné en silence)

Le canon liste **systématiquement** ces docs ; je ne les ai **pas** mis dans le bundle car leur
mise en service dépend d'un arbitrage que je ne peux pas trancher seul. Les **générateurs existent**
(bâtis par Codex, **non audités** → notre gouvernance interdit de les livrer tant qu'ils ne sont pas
vérifiés). Statut : **prêts à auditer puis câbler derrière un toggle OFF dès confirmation.**

1. **SCM — 4 satellites** : pacte d'associés (DOC-026), contrat à frais communs (DOC-027), règlement
   intérieur (DOC-028), liste des dépenses communes (DOC-030). Ce qu'il faut pour les fermer :
   (a) **Rafael** — sont-ils produits **systématiquement à la création** d'une SCM, ou sont-ce des
   actes distincts ? (le canon dit systématique ; à confirmer côté pratique) ; (b) audit de fidélité
   du générateur Codex ; (c) le modèle « liste dépenses » est un `.doc` ancien format (à reconvertir).
2. **SPFPL — note d'information (DOC-037)** : le canon la liste pour cession ET apport. Le code l'a
   écartée en jugeant qu'elle exige le **roster de la société cible** (donnée d'opération non saisie
   à la création du holding). À trancher : (a) **Rafael** — la note est-elle générable à la création
   ou attend-elle l'opération ? (b) audit de fidélité du générateur Codex.

→ Ces 2 points partent dans le **paquet Rafael** (métier, groupé — jamais toi sur le métier) et
l'audit de fidélité des générateurs est lancé en parallèle (constructif, sans décision métier).

## 1. Ce qui est FAIT cette nuit (tout commité, 30 commits sur la branche)
| Lot | Commit | Vérif |
| :--- | :--- | :--- |
| SCI/SCS/SCM fond + Reynaud tokenisé + **SELAS multi** (DOC-044) + **front 9 types** + footer SELARL + correctifs PASSE 2 | `f80ac31`→`eb30ace` | suite 356 |
| **Bundle de CRÉATION complet par type selon le canon** (plus seulement les statuts) | `98b2b9f` | suite 356 + e2e |
| INTEL GATE étape 0 (source incomplète = alerte immédiate) | `f9bc6c8` | docs |
| **Conditionnels canon** (régime communautaire + option IS), triple verrou | `87f50fb` | **suite 366** + e2e |

## 2. PASSE 2 — re-vérification (10 vérificateurs indépendants, lecture seule, double méthode)
**5 FIDÈLES, 5 PARTIELS (corrigés en `eb30ace`), 0 NON-fidèle. Zéro droit inventé, zéro placeholder
résiduel.** Détail : `_PASSE2_VERIFICATION_REPORT.md`.

## 3. Ce qui t'attend (toi / Rafael) — AUCUN n'est un bug code
1. **UAT du front** : teste-le en live (les 9 types dans la déroulante, bundle complet par type).
   ⚠️ Livraison métier SPFPL/SAS/SELAS = **NO-GO tant que Rafael n'a pas validé** (front câblé, gated).
2. **Paquet Rafael (métier, groupé)** : les 2 réserves ci-dessus (satellites SCM, note d'info SPFPL)
   + les arbitrages déjà listés dans `_RAFAEL_PACKET_V1.md` (PM en SCI standard, vocabulaire
   cession/apport, genre/DG SELAS…).
3. **Défauts du MODÈLE SOURCE** (moteur fidèle, c'est le `.docx` qui a un résidu) : SAS Art.4 + SELAS
   multi Art.4/23 « parts/gérant » dans un acte en actions/Président → corriger le modèle ou confirmer.

## 4. Dette technique restante (déterministe, planifiable — non bloquante)
- Généraliser un **test ligne-par-ligne** par type (seul SELARL médecin l'a → la CI ne verrouille pas
  encore la fidélité fine des autres).
- TAB→espace sur certains totaux (SCI/IRIS/SAS) ; footer SELARL pages paires/première (limite python-docx).
- **Consolider les deux clones** (l'editable install pointe vers `main` → toute vérif force
  `PYTHONPATH=…/-claude/src`). À régler proprement post-sprint.

## Verdict global
**Le moteur génère, pour chaque type V1, le bundle de création conforme au canon — sauf 2 groupes
de docs explicitement tenus en réserve (satellites SCM, note d'info SPFPL), faute d'arbitrage métier
et d'audit Codex, jamais abandonnés en silence.** Le front expose les 9 types. Reste : ta **validation
métier (Rafael)** + ton **UAT** + de la dette cosmétique. Conforme à ton cadrage (« avant revue Albane
et affinage »).
