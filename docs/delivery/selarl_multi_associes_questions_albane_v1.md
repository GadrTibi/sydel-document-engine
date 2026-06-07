# Statuts SELARL multi-associés complets — spec de sous-cas + questions pour Albane

> ⛔ ABANDONNÉ (décision Gad 2026-06-04) — SELARL reste unipersonnelle. Ce sous-cas (statuts SELARL
> multi-associés) n'est plus un objectif produit ; document conservé pour mémoire uniquement. Ne plus
> poser ces questions à Albane pour la SELARL. (La SELAS multi-actionnaire n'est pas concernée.)

**Statut : BLOQUÉ — en attente de la référence légale ligne-par-ligne d'Albane.**
Bloc « non codable sans Albane » du `SELARL_COMPLETION_PLAN_V1`. Ce document **ne code rien** :
il cadre le sous-cas et liste les **questions précises** à trancher avec Albane (via l'associé).
Tant que le wording pluriel n'est pas fourni et validé, **aucun code n'est écrit** (règle : on
n'invente pas de formulation juridique).

## 1. Ce qui est DÉJÀ couvert (ne pas redemander)
- **SELARL unipersonnelle** (associé unique) : statuts médecin (`DOC-017`) / dentiste (`DOC-016`)
  complets et générés. Wording singulier verrouillé.
- **Multi-associés PARTIAL** : `DOC-004` (PV) en sous-cas limité, et `DOC-016` dentiste en
  variante PARTIAL (apports / capital / répartition câblés) — **lock complet non revendiqué**.
- Le contexte de génération supporte déjà une **liste de N associés**
  (`build_generation_context` → `associes[]`, avec parts / apports / répartition).
- Hypothèse de travail actuelle du PARTIAL : **gérant unique + unanimité totale**.

## 2. Ce qui est BLOQUÉ (besoin du wording d'Albane)
Le passage de l'unipersonnel / PARTIAL au **multi-associés complet** change des **formulations
juridiques** que nous ne pouvons pas inventer. Périmètre bloqué :
1. **Préambule / comparution pluriels** : présenter 2..N comparants au lieu de l'associé unique.
2. **Bloc de signatures** pour N associés.
3. **Gérance multiple** (co-gérance) : nomination, pouvoirs, signatures de plusieurs gérants.
4. **Décisions collectives non unanimes** : quorum + règles de majorité (le PARTIAL suppose
   l'unanimité).
5. **Président de séance externe** (non-associé) : autorisé ? wording ?
6. **Associé absent / représenté** (pouvoir) : wording + impact quorum.

## 3. Où le wording devra s'insérer (repères techniques, pour après réponse)
- Générateurs statuts : `generators/lot_04/statuts_selarl_medecin.py`,
  `statuts_selarl_dentiste.py`, base commune `statuts_sel_exercice_common.py` /
  `statuts_sel_exercice_templates.py`.
- Spec texte de référence existante : `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.
- Contexte : `domain/models.py` (`Associe`, `GeranceContext`, `ReunionContext` /
  `ReunionPresident`), déjà multi-associés côté données.

## 4. QUESTIONS PRÉCISES POUR ALBANE
Pour chaque point : fournir le **texte exact** (référence ligne-par-ligne du modèle Word de
référence), pas une paraphrase.

### A. Comparution / préambule (2..N associés)
- A1. Texte exact d'introduction de la comparution quand il y a **plusieurs** associés (formule
  d'attaque, liaison entre comparants, ordre d'énumération).
- A2. Pour une **personne morale** associée (ex. holding) : bloc d'identification exact (forme,
  capital, RCS, représentant) ?
- A3. La mention « associé unique » devient quoi au pluriel (« les associés », « les soussignés ») ?
  Texte exact.

### B. Capital / apports / répartition
- B1. Tableau / phrase exacte de **répartition des parts** entre N associés (le PARTIAL en a une
  version — est-elle conforme ? sinon, wording cible).
- B2. Formule exacte des **apports en numéraire** par associé + total.

### C. Gérance
- C1. Cas **un seul gérant** parmi plusieurs associés : wording de nomination (déjà couvert ?).
- C2. Cas **plusieurs gérants (co-gérance)** : texte exact de nomination, étendue des pouvoirs
  (séparés / conjoints), et **bloc de signatures** des co-gérants.
- C3. Un gérant **non-associé** est-il permis en SELARL d'exercice ? Si oui, wording.

### D. Décisions collectives (AGE / AGO)
- D1. **Quorum** : règle exacte (texte) pour les décisions ordinaires et extraordinaires.
- D2. **Majorité** : seuils exacts (ex. majorité simple, 2/3, 3/4) par type de décision + wording.
- D3. Mention exacte quand un **vote n'est pas unanime** (PV : « pour / contre / abstention »,
  décompte par parts ?).

### E. Présidence de séance / représentation
- E1. **Président de séance** : doit-il être un associé ? Un **externe** est-il permis ? Wording.
- E2. **Associé absent représenté** (pouvoir / mandat) : texte exact du pouvoir + mention au PV +
  effet sur le quorum.

## 5. Livrable attendu d'Albane
Pour chaque question A→E : le **paragraphe Word exact** (ou la référence précise dans le modèle
maître), afin de l'intégrer **tel quel** dans les générateurs, sans reformulation. Dès réception et
validation PM, ce bloc passe de « bloqué » à « codable » et suit le cycle normal (spec canonique →
code → test → pack → revue).

## 6. Garde-fou
- Aucune de ces formulations n'est inventée côté Claude. Tant que A→E ne sont pas répondues, les
  statuts multi-associés complets restent **hors génération** (le front continue d'exposer
  uniquement l'unipersonnel + le PARTIAL borné, avec un statut honnête `hors_scope`).
