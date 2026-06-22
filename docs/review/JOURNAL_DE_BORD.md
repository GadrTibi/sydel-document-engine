# Journal de bord — Sydel Document Engine

> Le **« backlog » complet** voulu par Gad (2026-06-22) : un journal **chronologique horodaté
> unique** qui capture TOUT — chaque action/implémentation, chaque **question posée à Rafael**,
> chaque **réponse de Rafael**, chaque décision — pour **rejouer l'histoire du projet** et
> **remonter** quand Rafael a fait une connerie.
>
> **Sources croisées** (ce journal les unifie, il ne les remplace pas) :
> - `git log` = chronologie exacte des implémentations (horodatée, faisant foi pour les actions code) ;
> - `docs/review/retours/REGISTRE_RETOURS.md` = détail des remarques Rafael/Albane + statut + SHA ;
> - mémoire privée `rafael-collaboration-grievances` = les conneries de Rafael (G1/G2/G3), HORS repo.

## Règle de tenue (codifiée — appliquée systématiquement)
À chaque **action significative**, **question à Rafael**, **réponse de Rafael**, ou **décision**,
j'ajoute UNE ligne ici : `- [AAAA-MM-JJ HH:MM] [TYPE] description (réf : SHA / fichier)`.
- TYPE ∈ `ACTION` (code/commit) · `Q-RAFAEL` (question posée) · `R-RAFAEL` (réponse reçue) ·
  `DÉCISION` · `AUDIT` · `INCIDENT` (connerie/erreur, Rafael ou nous) · `MÉTHODE` (règle codifiée).
- Heure exacte pour les commits (git) ; approximative (`~`) pour les échanges non horodatés.
- Append-only : on ne réécrit pas l'histoire, on ajoute.

---

## 2026-06-22 — session retours R22 + audits

- [~10:00] **R-RAFAEL** Rafael répond au lot précédent : « toute la première page du document - oui ajuste » (réponse R22-06 + accents).
- [10:24] **ACTION** RAF-004 : exemples de réponse attendue (`help=`) sur les champs à risque, tous types (`6934b2d`).
- [11:03] **ACTION** SPFPL cession : note DOC-037 + PV agrément DOC-038/039 + acte DOC-040 (`28c96ad`).
- [11:20] **ACTION** SCM inter-SEL : contrat frais communs DOC-027 + règlement DOC-028 (`e859a2c`).
- [~11:30] **Q-RAFAEL → R-RAFAEL** batch de 6 remarques reçu (SELARL accents + conjoint fantôme ; SCM 2 docs manquants ; SCI option IS ; SCI IRIS mise en forme + [centre_impots]). Consigné REGISTRE_RETOURS R22-01→07.
- [11:50] **ACTION** R22-03/04 : SCM frais communs + règlement générés par défaut + champs visibles (`c2d3498`).
- [11:58] **ACTION** R22-05/07 : option IS démontrée au bouton SCI/IRIS + centre des impôts figé « Centre des Finances Publiques » (`e994127`).
- [12:11] **ACTION** R22-02 : pas de conjoint fantôme quand le cédant n'est pas marié (helper partagé `mentions_conjoint`, 2 actes de cession) (`c197875`).
- [12:20] **ACTION** R22-01 : accents « composés d'une pièce » (descriptif local cession) (`08542f3`).
- [12:23] **DÉCISION** R22-06 d'abord bloqué « précisions Rafael » : moteur déjà structuré, from-scratch ratifié → besoin du pointeur exact (`8123de9`). Puis Rafael précise « toute la première page ».
- [12:36] **MÉTHODE** garde-fou « périmètre exact, zéro extrapolation » gravé (validation Rafael avant tout choix neuf non sourcé) (`5e6edb7`).
- [13:32] **ACTION** R22-06 : statuts civils respectent la mise en forme de la 1re page source (en-tête centré, « LES SOUSSIGNES » gras+souligné, comparution gras) — moteur partagé, 4 types civils (`ae53bb8`).
- [13:33] **ACTION** untrack + gitignore des scripts repro `_audit_*.py` d'agents (`991f314`).
- [13:42 / 13:49] **MÉTHODE** Phase 6 RESTITUTION : format message retest Rafael (court/froid/puces/copier-collable ; reboot Streamlit = action de GAD) (`6c57dce`, `79e7936`).
- [~13:00→14:00] **AUDIT** 3 audits read-only lancés (opus, fan-out 10 types + vérif adversariale) :
  - cohérence inter-docs (`w767ud7w7`) → **fini** : « bloquant SCM » = **FAUX POSITIF vérifié** (source utilise `[adresse_locaux]` pour la partie 2, spec confirme) ; 4 « majeur » à recouper.
  - dogfood robustesse (`wrb1xv6kq`) → **fini** : 7 bloquants + 11 majeurs (asymétrie front/générateur + divisibilité + 0-passant).
  - propagation des corrections (`wbr7yj7cl`) → **fini** : 6/15 corrections ont des trous de code (R22-02 incomplet sur SPFPL ; ALB-numéro-ordre ; etc.).
- [13:59] **ACTION** garde de divisibilité capital/parts partagée → ferme 2 bloquants + 2 majeurs sur 4 types (`ec45978`). Bug confirmé empiriquement avant fix (règle 65).
- [~14:00] **INCIDENT (nous)** la passe propagation montre que R22-02 n'avait PAS été propagé aux statuts/apport SPFPL (mon sous-scopage) → à compléter.
- [14:04] **MÉTHODE** création de ce journal de bord (demande Gad : tracer la totale, rejouer l'histoire, remonter les conneries Rafael).
- [~14:20] **R-RAFAEL** batch 2026-06-22b : (1) `courrier_sde_cession_scm` retirer surlignage/rouge ; (2) « compromis cession cabinet médical manquant ».
- [~14:30] **MÉTHODE** RÈGLE ABSOLUE gravée (global 07 + mémoire) : traiter en continu jusqu'à épuisement, sans pause ni « je continue ? ».
- [~14:40] **ACTION** R22b-01 : rouge + surlignages retirés du courrier SDE (générateur + 3 tests inversés). 509 verts.
- [~14:45] **INCIDENT (Rafael)** R22b-02 « compromis médical manquant » = NON-BUG vérifié (DOC-010 généré quand étape=compromis ; testé en acte = G2 test partiel).
- [~15:00] **INCIDENT (Rafael) — G4** Rafael a demandé par mail à **Albane + David (clients)** de tester la SCM AVANT que le fix soit confirmé prêt/déployé côté dev (Streamlit pas rebooté → ancienne version cassée). Exposition prématurée du décideur + de la direction juridique, sans coordination dev. Noté en mémoire grievances G4.
- [~15:05] **ACTION** 3 bloquants dogfood civils corrigés (capital=0, banque_adresse, associé PM sans représentant) (`912b89e`). 512 verts.

## Conneries / incidents Rafael (résumé — détail dans la mémoire privée)
- **G1** (2026-06-22) : nouvelle remarque sur la SELARL « validée 100 % » et socle de tous les types (confirmé par Rafael : nouvelle remarque, pas régression).
- **G2** : ne teste pas réellement — preuve : 4 docs sur 7 produits non remarqués (docs non téléchargés).
- **G3** : source de vérité incomplète (NotebookLM caché) → 1er travail entièrement refait. Voir `rafael-collaboration-grievances`.

## Antérieur (2026-06-19 et avant)
Chronologie exacte dans `git log` (vague parité gold-anchored : 7 règles imposées `1d8ae1d`,
couche partagée `front_widgets`, consommation par tous les types `9f726dc`→`f5baf27`). Retours
antérieurs Rafael/Albane : `REGISTRE_RETOURS.md` + locks `docs/review/albane_*`.
