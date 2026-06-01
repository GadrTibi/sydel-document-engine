# Spec UI wizard SELARL V1

Ticket source : `SELARL-PILOT-PROTOCOL-001`

## Objet

Décrire le parcours cible du pilote SELARL, écran par écran, sans modifier l'UI dans ce ticket.

Le parcours doit aider un juriste à qualifier un dossier SELARL, comprendre les documents attendus et voir les champs manquants avant génération.

## Écran 1 — Qualification

Objectif : qualifier le dossier sans demander de détails documentaires.

Champs :

- profession : médecin / chirurgien-dentiste ;
- site distinct : oui / non ;
- SCM cession : oui / non ;
- régime communautaire : oui / non ;
- dérogation : oui / non ;
- cession : oui / non ;
- si cession : cabinet médical / cabinet dentaire / aucun.

Règles :

- `type de cabinet` est affiché seulement si `cession = oui` ;
- si `cession = non`, la valeur est `aucun` ;
- les documents attendus sont recalculés à chaque changement ;
- les documents manuels sont visibles plus tard, mais jamais envoyés à la génération.

## Écran 2 — Fiche Client / Praticien

Objectif : saisir le Praticien avant la société et éviter la double saisie gérant / signataire / associé.

Blocs :

- identité ;
- naissance ;
- nationalité ;
- filiation si les documents communs la demandent ;
- adresse personnelle ;
- profession exercée ;
- ordre professionnel ;
- RPPS / numéro d'ordre ;
- conseil de l'ordre ;
- lieu d'exercice si applicable ;
- fonction cible : `Gérant` lorsque le Praticien exerce le mandat social.

Règles :

- proposer l'option pivot `Dossier unipersonnel` pour les dossiers où le Praticien est aussi associé unique, gérant et signataire ;
- ne dériver aucun rôle depuis le Praticien quand `Dossier unipersonnel` est inactif ;
- garder les liens individuels gérant / signataire comme options explicites si le dossier n'est pas unipersonnel ;
- ne pas utiliser le libellé banni ;
- tout champ d'adresse doit être qualifié.

## Écran 3 — Fiche Société

Objectif : saisir la SELARL en création ou cible du dossier, après la Fiche Client.

Blocs :

- dénomination ;
- forme sociale ;
- capital social ;
- ville RCS si utile ;
- siège social ;
- adresse de domiciliation si différente ou si champ libre requis.

Règles :

- proposer `L'adresse de domiciliation est le siège social` ;
- conserver un champ libre `Adresse de domiciliation affichée` pour respecter la décision V1 de `DOC-002` ;
- ne pas afficher des champs de cession ou de SCM sur cet écran ;
- ne pas assimiler automatiquement siège social, cabinet, lieu d'exercice et domiciliation.

## Écran 4 — Capital & Associés

Objectif : saisir les associés et la répartition du capital utile aux statuts et au PV.

Blocs :

- nombre d'associés ;
- nombre total de parts ;
- valeur nominale ;
- associé 1 ;
- associé 2 si nécessaire ;
- parts détenues ;
- total des parts ;
- choix du gérant parmi les associés.

Cas simples V1 :

- associé unique ;
- deux associés si le document cible le supporte ;
- blocage explicite si la cardinalité saisie dépasse le périmètre automatisé d'un document.

Mécanismes de déduplication :

- `Dossier unipersonnel` comme raccourci contrôlé : Praticien = associé unique = gérant = signataire ;
- options individuelles explicites hors dossier unipersonnel, sans activation par défaut ;
- `Choisir le gérant parmi les associés`.

## Écran 5 — Contexte & scénarios métier

Objectif : collecter uniquement les blocs activés par l'écran 1.

Blocs conditionnels :

- régime communautaire : conjoint, régime, apport concerné, date et signature ;
- SCM cession : SCM cédée, cédant, cessionnaire, associés SCM, prix, enregistrement ;
- dérogation : documents attendus, mais pas de saisie générative pilote pour `DOC-013` / `DOC-014` tant que la vraie V2 ne fournit pas les variables ou marque le document à remplir à la main ;
- cession : vendeur, acquéreur, cabinet, prix, financement ;
- cabinet médical / dentaire : champs propres au type de cabinet ;
- bail : bailleur, locaux, dates, acceptation ;
- banque / financement : banque, adresse de banque, emprunt PV si actif.

Règles :

- chaque bloc inactif est masqué et non bloquant ;
- les documents de dérogation SELARL restent manuels dans le pilote vérifié : formulaire multi-sites non fourni en variables V2, `Dérogation SEL BNC` manuelle, `Dérogation cumul SELARL BNC` manuelle ;
- l'emprunt PV reste une option du `DOC-004`, pas un document séparé ;
- le mandataire reste un sujet de formalité si un document ou une variable l'exige, sans devenir l'axe UX central du parcours ;
- ne pas activer `mandataire = signataire` par défaut ;
- ne pas déduire automatiquement vendeur / locataire, siège / lieu d'exercice / cabinet, vendeur / Praticien ou cédant SCM / Praticien.

## Écran 6 — Documents & génération

Objectif : donner un contrôle métier avant génération.

Afficher trois groupes :

- documents générables ;
- documents manuels ;
- documents non implémentés ou hors contexte ;
- champs manquants par document.

Pour chaque document :

- nom métier ;
- `DOC-XXX` si connu ;
- statut ;
- bloc qui l'a déclenché ;
- champs manquants ;
- note de prudence si formulaire à compléter.

Actions :

- générer DOCX ;
- générer ZIP dossier ;
- générer PDF optionnel si backend local disponible.

Règles :

- ne pas transformer cette liste en formulaires document par document ;
- ne pas afficher `PV d'autorisation d'emprunt` comme document autonome ;
- afficher le formulaire site distinct CD94 comme manuel ;
- afficher le formulaire multi-sites SEL comme manuel / hors génération pilote si la vraie V2 ne fournit pas ses variables ;
- afficher Dérogation SEL BNC comme manuel ;
- afficher Dérogation cumul SELARL BNC comme manuel, même si `DOC-014` existe côté moteur.
- bouton génération actif uniquement s'il existe au moins un document générable prêt ;
- ZIP inclut uniquement les sorties produites et le manifeste ;
- PDF reste optionnel ;
- documents manuels restent listés comme pièces attendues hors automatisation.

Le rendu Streamlit SELARL a été réaligné par `SELARL-UI-REALIGN-001`. Il consomme désormais les titres d'écrans, champs visibles et projections de réutilisation issus du schéma et de `business_wizard.py`. Il ne doit toutefois pas être poussé ou redéployé avant `SELARL-SMOKE-REALISTIC-001`.

## Écarts UI actuelle vs cible SELARL

| Écart | Constat actuel | Cible SELARL |
|---|---|---|
| Logique de saisie | Le formulaire part des documents prêts `DOC-001` à `DOC-004`. | Le formulaire part du processus SELARL et de ses conditions. |
| Ordre du parcours | Corrigé par `SELARL-UI-REALIGN-001` : la Fiche Client précède la Fiche Société. | Qualification, Fiche Client / Praticien, Fiche Société, Capital & Associés, Contexte & scénarios métier, Documents & génération. |
| Libellé personne | Corrigé par `SELARL-WORDING-REALIGN-001`. | `Fiche Client` pour l'écran personne et `Gérant` pour le rôle juridique SELARL. |
| Double saisie | Corrigé par `SELARL-UI-REALIGN-001` : `Dossier unipersonnel` est exposé dans la qualification et verrouille le cas pivot. | `Dossier unipersonnel` pour le cas pivot, puis options explicites de copie hors défaut. |
| Adresse ambiguë | Plusieurs champs courts `Numero`, `Voie`, `Code postal`, `Ville` sans toujours rappeler le contexte. | Labels qualifiés : siège, personnelle, cabinet, bailleur, banque, SCM, etc. |
| Documents contextualisés | Documents attendus affichés, mais beaucoup restent `Contexte incomplet pour génération V2`. | Documents regroupés par blocs métier avec champs manquants lisibles. |
| PV emprunt | Corrigé : l'emprunt est affiché comme option du `DOC-004`, pas comme document autonome. | Option conditionnelle du PV nomination gérant seulement. |
| Cession SELARL | Le bloc cession, bail et banque est conditionné par `cession = oui`. | Bloc cession complet conditionné par `cession = oui`. |
| SCM cession | Le bloc SCM reste distinct et la SELARL cessionnaire est une option explicite. | Bloc SCM distinct de la cession de cabinet. |
| Régime communautaire | Le bloc conjoint/apport est conditionné par régime communautaire. | Bloc régime matrimonial / conjoint. |
| Dérogation | Le catalogue V1 exposait `DOC-013` et `DOC-014` comme formulaires à compléter. | Dans le pilote SELARL vérifié, le formulaire multi-sites est hors génération faute de variables V2 et `Dérogation cumul SELARL BNC` est manuel. |
| Lettre d'avertissement conjoint | Le moteur expose `DOC-006` comme générable. | L'écran doit le générer avec `DOC-005` quand le régime communautaire est actif ; la réserve historique est levée par la source DOCX Lot 2. |
| Documents à retirer du pilote | Aucun document autonome d'autorisation d'emprunt ne doit être ajouté. | Ne montrer que les documents SELARL attendus par la V2. |

## Critères d'acceptation UI réaligné

- L'écran 1 permet de reproduire la sélection SELARL du catalogue.
- Aucun champ UI ne s'appelle seulement `adresse`.
- `Dossier unipersonnel` permet de lier Praticien, associé unique, gérant et signataire sans double saisie.
- Quand `Dossier unipersonnel` est inactif, aucun lien Praticien / associé / gérant / signataire n'est imposé.
- Les documents manuels sont visibles mais exclus de la génération.
- `DOC-013` et `DOC-014` ne sont pas envoyés à la génération dans le pilote SELARL vérifié sans arbitrage juriste.
- Les champs manquants sont regroupés par bloc métier.
- Aucun document hors flux SELARL pilote n'est affiché.
