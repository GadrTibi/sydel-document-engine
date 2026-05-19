# Spec UI wizard SELARL V1

Ticket source : `SELARL-PILOT-PROTOCOL-001`

## Objet

Décrire le parcours cible du pilote SELARL, écran par écran, sans modifier l'UI dans ce ticket.

Le parcours doit aider un juriste à qualifier un dossier SELARL, comprendre les documents attendus et voir les champs manquants avant génération.

## Écran 1 — Nouveau dossier SELARL

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

## Écran 2 — Société

Objectif : saisir la SELARL en création ou cible du dossier.

Blocs :

- dénomination ;
- forme sociale ;
- capital ;
- nombre total de parts ;
- valeur nominale ;
- ville RCS ;
- siège social ;
- adresse de domiciliation si différente ou si champ libre requis.

Règles :

- proposer `L'adresse de domiciliation est le siège social` ;
- conserver un champ libre `Adresse de domiciliation affichée` pour respecter la décision V1 de `DOC-002` ;
- ne pas afficher des champs de cession ou de SCM sur cet écran.

## Écran 3 — Professionnel principal / gérant

Objectif : saisir la personne principale et éviter la double saisie gérant / signataire / associé.

Blocs :

- identité ;
- naissance ;
- nationalité ;
- filiation si les documents communs la demandent ;
- adresse personnelle ;
- profession ;
- ordre professionnel ;
- RPPS / numéro d'ordre ;
- fonction cible : `Gérant / professionnel principal`.

Règles :

- proposer `Le gérant est le professionnel principal` ;
- proposer `Le signataire est le professionnel principal` ;
- ne pas utiliser le libellé `Dirigeant / pharmacien` ;
- tout champ d'adresse doit être qualifié.

## Écran 4 — Associés

Objectif : saisir les associés et la répartition du capital utile aux statuts et au PV.

Blocs :

- nombre d'associés ;
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

- `Le signataire est le premier associé` ;
- `Copier depuis professionnel principal` ;
- `Choisir le gérant parmi les associés`.

## Écran 5 — Conditions spécifiques

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
- l'emprunt PV reste une option du `DOC-004`, pas un document séparé.

## Écran 6 — Documents attendus

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

Règles :

- ne pas transformer cette liste en formulaires document par document ;
- ne pas afficher `PV d'autorisation d'emprunt` comme document autonome ;
- afficher le formulaire site distinct CD94 comme manuel ;
- afficher le formulaire multi-sites SEL comme manuel / hors génération pilote si la vraie V2 ne fournit pas ses variables ;
- afficher Dérogation SEL BNC comme manuel ;
- afficher Dérogation cumul SELARL BNC comme manuel, même si `DOC-014` existe côté moteur.

## Écran 7 — Génération

Objectif : lancer la génération seulement quand le contexte est prêt.

Actions :

- générer DOCX ;
- générer ZIP dossier ;
- générer PDF optionnel si backend local disponible.

Règles :

- bouton génération actif uniquement s'il existe au moins un document générable prêt ;
- ZIP inclut uniquement les sorties produites et le manifeste ;
- PDF reste optionnel ;
- documents manuels restent listés comme pièces attendues hors automatisation.

## Écarts UI actuelle vs cible SELARL

| Écart | Constat actuel | Cible SELARL |
|---|---|---|
| Logique de saisie | Le formulaire part des documents prêts `DOC-001` à `DOC-004`. | Le formulaire part du processus SELARL et de ses conditions. |
| Libellé dirigeant | `Dirigeant / pharmacien` visible dans l'UI Streamlit. | `Gérant / professionnel principal` pour SELARL. |
| Double saisie | Signataire, dirigeant et associé peuvent être saisis séparément sans lien UX. | Cases de réutilisation et copie depuis source. |
| Adresse ambiguë | Plusieurs champs courts `Numero`, `Voie`, `Code postal`, `Ville` sans toujours rappeler le contexte. | Labels qualifiés : siège, personnelle, cabinet, bailleur, banque, SCM, etc. |
| Documents contextualisés | Documents attendus affichés, mais beaucoup restent `Contexte incomplet pour génération V2`. | Documents regroupés par blocs métier avec champs manquants lisibles. |
| PV emprunt | Checkbox UI `PV avec autorisation d'emprunt` peut être interprétée comme un document. | Option conditionnelle du PV nomination gérant seulement. |
| Cession SELARL | Le formulaire ne collecte pas encore les champs cession, bail, banque et cabinet. | Bloc cession complet conditionné par `cession = oui`. |
| SCM cession | Le formulaire ne collecte pas encore les champs SCM cession. | Bloc SCM distinct de la cession de cabinet. |
| Régime communautaire | Champs conjoint/apport absents du pilote assistant. | Bloc régime matrimonial / conjoint. |
| Dérogation | Le catalogue V1 exposait `DOC-013` et `DOC-014` comme formulaires à compléter. | Dans le pilote SELARL vérifié, le formulaire multi-sites est hors génération faute de variables V2 et `Dérogation cumul SELARL BNC` est manuel. |
| Lettre d'avertissement conjoint | Le moteur expose `DOC-006` comme générable. | L'écran doit afficher une réserve source V2 : le document ne figure pas parmi les sources fournies. |
| Documents à retirer du pilote | Aucun document autonome d'autorisation d'emprunt ne doit être ajouté. | Ne montrer que les documents SELARL attendus par la V2. |

## Critères d'acceptation UI futur

- L'écran 1 permet de reproduire la sélection SELARL du catalogue.
- Aucun champ UI ne s'appelle seulement `adresse`.
- Le signataire, le gérant et l'associé 1 peuvent être liés sans double saisie.
- Les documents manuels sont visibles mais exclus de la génération.
- `DOC-013` et `DOC-014` ne sont pas envoyés à la génération dans le pilote SELARL vérifié sans arbitrage juriste.
- Les champs manquants sont regroupés par bloc métier.
- Aucun document hors flux SELARL pilote n'est affiché.
