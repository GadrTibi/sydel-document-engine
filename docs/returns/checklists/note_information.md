# CHECKLIST MAÎTRE — Note d'information SPFPL (DOC-037)

> Code : `generators/lot_05/note_information.py` — générateur UNIQUE partagé
> **SPFPL cession ET SPFPL apport** (wording tranché par `operation_spfpl.type`).
> Un fix doit être régénéré/diffé sur les DEUX opérations.
> S'ajoute à `_transverse.md`.

## Attentes cumulées

- [ ] 8.1 Reprendre la mise en forme du MODÈLE D'ORIGINE (`NOTE D'INFORMATION.docx`) — la note générée doit être lisible, proche du modèle — Albane 2026-07-06 — statut : **pas fait** (classé BUILDABLE lourd le 2026-07-06 : rebuild token-replacement à mener ; le générateur actuel ne reproduit pas la forme du modèle)
- [x] 8.2 Variable « il prévoit d'acquérir X parts » = **parts cédées à la holding** (PAS le nombre d'actions de la SPFPL) — Albane 2026-07-06 — statut : **fait** (corrigé en code ; avait été re-flaggé à tort)
- [x] 8.2-label Libellé front « parts cédées **à la** holding » (pas « au holding ») — Albane 2026-07-06 — statut : **fait** (groupe FRONT)
- [ ] Montants : « LETTRES (chiffres) euros » + chiffres groupés par 3 + élision « d'un » — **Albane 2026-07-07 (transverse)** — statut : **à vérifier** sur la note régénérée (aucun passage dédié fait sur ce doc ; balayer lors du rebuild 8.1)
- [ ] « Docteur » ≠ civilité — **Albane 2026-07-07 (transverse)** — statut : **à vérifier** lors du rebuild 8.1 (le corpus from-scratch de la note peut porter le titre)
- [ ] Accents / orthographe irréprochables — SP3 (2026-06-25) + 07-07 — statut : **à vérifier** (la note fait partie des générateurs from-scratch lot_05 listés au registre fidélité `docs/review/FIDELITE_LOT03_05_REGISTRE.md` — rebuild token-replacement = le fix racine)
- [x] Wording cession vs apport correctement tranché par `operation_spfpl.type` — spec lot 5 — statut : **fait** (structurel, testé)

## Rappels

- Le rebuild 8.1 est le **prérequis** des vérifs transverses (montants/Docteur/accents) : les traiter dans le même chantier, contre le modèle source, pas en rustines sur le from-scratch actuel.
- Après rebuild : régénérer cession ET apport + diff golden (règle byte-neutralité).
