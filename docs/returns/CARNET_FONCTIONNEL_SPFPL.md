# CARNET — Ticket fonctionnel « Retours par cas » (SPFPL cession dentiste + transverse) — 2026-07-06

> **Source** : Doc Google (onglet fonctionnel), reçu Gad 2026-07-06. **Verbatim** : [`_ticket_fonctionnel_spfpl_verbatim.md`](_ticket_fonctionnel_spfpl_verbatim.md).
> **Cas central** : SPFPL par cession de dentiste (questionnaire + statuts + note d'info + demande Ordre + acte cession + PV + attestation) + points transverses (unipersonnelle apport, plages, prénom).
> **Statut** ∈ `a_faire · partiel · fait` · **Validé** (client) ∈ `⬜ · ✅`.
> Cartographie vérifiée (workflow `ticket-fonctionnel-spfpl-map`, 6 lecteurs, HEAD c524970) : **35 points**.

## Synthèse triage (35 points)

- **FAIT / conforme (6)** : 10 (domiciliation validée), 9.1 (mise en forme demande Ordre validée), 9.3 (de/du/des demande Ordre déjà présent), 6.7 (doublon adresse cible), 7.3-partiel (comparution marié), 12.1 (acte = token-replacement sur modèle — à re-vérifier vs « illisible », flag).
- **BUILDABLE (19)** → exécution 5 fix agents parallèles :
  - **FRONT** (spfpl_slice) : 6.1 case même adresse cible, 6.2 « Société cible (SEL) », 6.5 profession cible préremplie, 6.6 champ profession associé unique, 8.2-label « à la holding ».
  - **STATUTS** (statuts_spfpl + demande Ordre + helper dept) : 6.8 titre « Statuts [Nom] », 7.1 prénom (pas prénoms complets), 7.2 majuscule liste soussigné, 7.5 art.8 euro, 7.4 dept NOM pas numéro, 9.2 dept nom demande Ordre.
  - **ACTE** (acte_cession_parts + modèle) : 12.2 identité acquéreur forme complète, 12.3 euro capital, 12.4 de/du/des, 12.5 0 part + doublon répartition, 12.6 prix singulier, 12.7 paiement « par le moyen ».
  - **NOTE+PV+ATTEST** (note/pv/service) : 8.2-logic variable parts cédées, 13 PV plage supprimée si vide, 11 attestation capital SPFPL cession.
  - **TRANSVERSE §1** : apport associé unique supprimé (SELARL/SELAS uni + civils uni).
- **MÉTIER / BONUS (7)** → flags Albane (`QUESTIONS_RAFAEL.md`, tracé 2026-07-06) : 3 greffe/RCS auto (bonus, data), 4 lisibilité questionnaire (design UI), 6.4 import Kbis (bonus API), 6.3/7.3 conjoint **pacsé** (wording), 8.1 note d'info mise en forme (reformatage lourd), 9.4 supprimer « Conseil départemental » ?, 12.1 acte « illisible » (écart à investiguer).

## Critères d'acceptation client (18) — voir verbatim §14.

## Notes de contexte (recoupements avec le travail SPFPL récent)
- Menu matrimonial complet SPFPL (situation + conjoint conditionnel) DÉJÀ fait (commit 7bb1f91) → 6.3/7.3 = reste le cas PACSÉ (wording, flag).
- Acte de cession de PARTS branché `mentions_conjoint` DÉJÀ fait → 12.x = mise en forme + euro + 0 part + prix.
- « euro » art.8 SELAS fait (mise en forme 2.3) → 7.5 = même pattern pour SPFPL.
- Plages de parts SCM (N4) fait → 13/§2 = même principe (omettre si vide) pour le PV SPFPL.
