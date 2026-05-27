# YB-S12-001 Review

Date : 2026-05-27

## PRE-FLIGHT PM

### A. Ce que le canon actuel dit encore

- Le repo recent est centre sur Track B SELARL V1, un front clean et une slice
  documentaire generable.
- Le front global existant utilise des roles, adresses typees, statuts
  documentaires et reuse rules explicites.
- Les docs de pilotage recommandent encore des suites de type
  `SELARL-COMPLETE-COMPLEX-SUBFORMS-001`, test utilisateur local ou revue pilote.
- Les documents manuels et reserves restent visibles mais hors generation.
- Le literal `USER-ONE-BUREAU` n'a pas ete trouve dans le repo. Le delta a
  toutefois traite ce point comme canon mono-bureau / mono-contexte implicite a
  reviser, car le parcours visible ne modelise pas encore plusieurs bureaux
  autorises avec contextes separes.

### B. Ce que le Boss change reellement

- Le centre produit devient `LEAD + ATELIER + RELANCE`.
- Le multi-bureaux est autorise avec contextes separes.
- Les relances sont explicites : `RELANCE_TELEPRO` et `RELANCE_BOSS`.
- `REFAIS_AG` devient un flow conserve, non un retour en prospection brute.
- La file atelier non attribuee est manuelle.
- Les tickets pilote/UAT/cobayes passent derriere la reconstruction Sprint 12.

### C. Contradictions majeures a absorber

- Ancien prochain ticket SELARL complet vs nouveau bridge PM Sprint 12.
- Pilote/UAT prets ou recommandes vs pause explicite jusqu'a rebuild.
- `USER-ONE-BUREAU` / mono-contexte implicite vs multi-bureaux autorise avec
  contextes strictement separes.
- Mono-parcours/mono-contexte visible vs multi-bureaux autorise mais separe.
- Documents/front orientes generation dossier vs modele operationnel
  Lead/Atelier/Relance.
- Relance non structuree vs deux etats visibles.
- REFAIS_AG anciennement assimilable a reprise/prospection vs statut atelier
  explicite.

### D. Nouveau canon Sprint 12 fige

- `LEAD + ATELIER + RELANCE`.
- Multi-bureaux separe.
- Dossier ouvert distinct du lead.
- `RELANCE_TELEPRO` et `RELANCE_BOSS`.
- `REFAIS_AG` historise, visible, non recycle en prospection brute.
- Atelier non attribue en file manuelle.
- Pas de role `chef telepro`, pas de logique speciale `interne / externe`.

### E. Mise en pause

- Pilote cobayes, Naomi, provisioning, launch et UAT reelle.
- Tout ticket design Claude.
- Toute production, hook ou cleanup gouvernance Phase 2/3.

## Delta canon ancien -> nouveau

### Canon conserve

- Travail repo-first, petite PR, memoire projet versionnee.
- Pas de code sans spec.
- Pas de modification du wording juridique.
- Documents manuels visibles mais hors automatisation.
- Roles, adresses typees et reuse rules explicites restent des fondations utiles.

### Canon remplace

- Le prochain axe n'est plus la suite pilote SELARL/subforms.
- Le modele mono-contexte doit etre remplace par multi-bureaux separes.
- Le flow pilote/UAT doit etre reconstruit apres les specs Sprint 12.
- La relance doit devenir un etat produit explicite.

### Canon differe

- Code produit Sprint 12.
- Rebuild pilote/UAT.
- Cobayes et launch.
- Extension UI concrete.

### Canon devenu faux

- Monday comme modele central.
- Dossier ouvert = simple lead.
- Vue metier fusionnee cross-bureau.
- Auto-attribution atelier de secours.
- Interne/externe comme statut produit special.
- Sarah/Ethan comme statuts systeme.
- Role `chef telepro` maintenant.
- `REFAIS_AG` renvoye en prospection brute.

## Verification

- Aucun fichier Python modifie.
- Aucun code produit lance.
- Aucun ticket pilote, design, production ou UAT lance.
- Branches pilote/cobaye locales ou distantes recherchees : aucune branche
  correspondante trouvee au pre-flight.
