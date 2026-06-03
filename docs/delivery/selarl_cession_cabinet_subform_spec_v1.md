# Spec de sous-cas — Cession de cabinet (front SELARL) — V1

Bloc 1 du `SELARL_COMPLETION_PLAN_V1`. But : câbler le **sous-formulaire front** de cession de
cabinet pour rendre générables `DOC-007`..`DOC-012` (+ bail/appel de fonds), **sans toucher au
wording des générateurs** (déjà validés). Spec AVANT code (règle projet).

## Documents visés et conditions (orchestrateur, déjà en place)
- `DOC-009`/`DOC-010` (acte/compromis cabinet **médical**) ; `DOC-011`/`DOC-012` (acte/compromis
  **dentaire**) → `_cession_cabinet_enabled` : `dossier_options.cession=True` + `cession.etape ∈
  {compromis, acte}` + `cession.type_cabinet ∈ {medical, dentaire}`.
- `DOC-007` (avenant bail) → `cession`. `DOC-008` (appel de fonds) → SELARL + `type_cabinet=dentaire`.
- Le générateur unique `cession_cabinets_common.generate_cession_cabinet_docx(ctx, out,
  CessionCabinetVariant(etape, type_cabinet))` produit les 4 actes ; bail/appel via `bail_appel_common`.

## Données à saisir (sous-formulaire), mappées au contexte
Modèle cible : `domain/models.py` → `DocumentGenerationContext.cession: CessionContext`. Sections :
1. **Qualification cession** : `etape` (compromis|acte), `type_cabinet` (medical|dentaire),
   options bail / appel de fonds / financement. → `dossier_options.cession=True`.
2. **Vendeur / cédant** (`CessionVendeur`) : civilité, genre, prénom, nom, profession (+ adresse si
   distincte). NB règle métier déjà actée : vendeur = praticien BNC dans le parcours SELARL standard
   (réutilisation possible depuis le praticien, à confirmer — voir `GLOBAL_CANONICAL_FIELD_REGISTRY`).
3. **Acquéreur** = la SEL en constitution (réutiliser la société du dossier).
4. **Cabinet cédé** (`CessionCabinet`) : dénomination/adresse, nature fonds libéral, adresse locaux,
   superficie, origine de propriété (description, date, prix, précédent propriétaire), années
   d'acquisition de patientèle.
5. **Prix / financement** (`CessionFinancement`) : montant, banque, prêt, crédit-vendeur, destinataire.
6. **Bail** (si option) : données avenant. **Appel de fonds** (si dentaire) : données `appel_fond_sel`.
7. **Validations sensibles** (`CessionValidations`) : cases à cocher (mentions bail médical, origine
   compromis médical, date réalisation, ligne contrats travail médical, 2 salariés dentaire) — ce sont
   des garde-fous métier exigés par les générateurs ; à exposer comme cases explicites.

## À coder (étapes, dans `front_app/`)
1. `SelarlSliceInput` : ajouter les champs cession (ou un sous-objet) ci-dessus.
2. `build_generation_context` : assembler `ctx.cession` (CessionContext complet) +
   `dossier_options.cession=True` (+ flags bail/financement).
3. `selected_selarl_document_codes` : ajouter DOC-007..012 selon `etape`/`type_cabinet`/options.
4. Sous-formulaire dans `front_app/shell.py` (zone « Cession de cabinet », visible si option cochée).
5. Scénario `selarl_medecin_cession_acte` (+ dentaire) dans `scenarios/selarl.py`.
6. Tests `tests/unit/test_clean_front_app.py` (cas cession) + `generate_pack` smoke.

## Garde-fous
- Réutiliser les générateurs tels quels (pas de wording inventé).
- Lire les champs EXACTS dans `domain/models.py` (CessionContext et sous-modèles) + les `required_*`
  de `cession_cabinets_common.py` au moment de coder, pour ne rien oublier.
- Bloc à sérialiser (touche `SelarlSliceInput` + `build_generation_context` partagés).

## Questions métier à confirmer (non bloquantes pour démarrer le câblage)
- Vendeur/cédant : réutilise-t-on automatiquement le praticien, ou saisie distincte ?
- Acquéreur : toujours la SEL du dossier ?
(Ces réponses viennent d'Albane via l'associé ; en attendant, exposer les champs en saisie explicite.)
