---
description: Traiter une remarque/retour (Rafael, Albane, test live) selon le protocole gold-parity déterministe — propagation à tous les cas similaires + vérifications dans tous les sens.
---

# /retour-gold — traitement déterministe d'une remarque

Tu viens de recevoir une ou plusieurs remarques (collées par Gad ci-dessous, ou dans le
message courant). Applique **sans re-réfléchir à la méthode** le protocole
`docs/review/PROTOCOLE_RETOURS_GOLD.md`. Ne saute aucune phase.

Remarque(s) : $ARGUMENTS

## Déroulé imposé

1. **Phase 0 — INTAKE.** Consigne CHAQUE remarque dans
   `docs/review/retours/REGISTRE_RETOURS.md` (ID, source, date, cas d'origine, type, surface,
   scope attendu, statut=`ouvert`). Verbatim conservé.

2. **Phase 1 — CLASSIFY + GOLD-ANCHOR.** Pour chaque remarque : type, surface concrète
   (document/widget/règle), et ce que fait le gold SELARL ici.

3. **Phase 2 — SCOPE.** Liste TOUS les types/cas partageant la surface (le fix vaudra pour
   tout ce scope, pas seulement le cas d'origine). Types : SELARL, SCI, SCI IRIS, SCS, SCM,
   SAS, SPFPL cession, SPFPL apport, SELAS, SELAS uni médecin.

4. **Phase 3 — IMPLEMENT** sur la couche partagée (front_widgets / générateur unique /
   modèle canonique) pour propager par construction. Clone Claude uniquement.

5. **Phase 4 — VÉRIFIER DANS TOUS LES SENS** (toutes les cases) :
   - suite verte (`pytest -q --basetemp=artifacts/_audit_tmp/pt`) + `ruff check` ;
   - test de non-régression NEUF par remarque ;
   - zéro placeholder `[`/`]` dans les DOCX ;
   - accents/encodage sains (pas de mojibake) ;
   - logique conditionnelle (pas de donnée fantôme : ex. épouse si non marié communauté) ;
   - **propagation** : lance le workflow `audit-propagation-corrections` → la correction est
     dans TOUT le scope (vérif adversariale) ;
   - parité gold (SELARL byte-stable hors changement voulu).

6. **Phase 5 — REGISTER + CLORE.** Registre → `traité` + SHA + preuve. Règle transverse durable
   → la graver dans `docs/review/METHODE_PARITE_GOLD.md`.

## Vérification finale
Avant de rendre la main : relancer `audit-completude-types` + `audit-propagation-corrections`
et ne déclarer « parfait » que si les deux reviennent sans trou réel confirmé. Sinon : corriger
et re-vérifier. Ne jamais annoncer un test non lancé (règle 65).
