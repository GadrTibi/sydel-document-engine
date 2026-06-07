# Track B SELARL multi-associes front contract V1

> ⛔ ABANDONNÉ (décision Gad 2026-06-04) — SELARL reste unipersonnelle. Ce contrat de front
> multi-associés SELARL n'est plus un objectif produit ; document conservé pour mémoire uniquement.
> Le code correspondant (sous-cas multi DOC-004 + dentiste PARTIAL) a été retiré du front et des
> générateurs. (La SELAS multi-actionnaire n'est pas concernée.)

Ticket : `TRACK-B-SELARL-MULTI-ASSOCIES-SOURCE-CONTRACT-006`

Statut : contrat source uniquement. Aucun code, aucun front, aucun generateur et aucun wording juridique ne sont modifies par ce document.

## 1. Sources et hierarchie

Hierarchie appliquee :

1. retour humain le plus recent fourni par l'utilisateur : `C:\Users\Gad\Downloads\Retours humains .docx` ;
2. arbitrages et locks SELARL deja actes ;
3. specs de livraison et sources DOCX repo ;
4. code existant uniquement comme verification d'etat.

Sources lues ou verifiees pour ce contrat :

- `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md` ;
- `docs/project/SELARL_PRODUCTION_FACTORY_V1.md` ;
- `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md` ;
- `docs/review/track_b_selarl_dentist_line_by_line_lock_003_report_v1.md` ;
- `docs/review/track_b_selarl_medecin_line_by_line_lock_004_report_v1.md` ;
- `docs/review/track_b_selarl_medecin_regime_communautaire_005_report_v1.md` ;
- `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md` ;
- `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md` ;
- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` ;
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md` ;
- `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md` ;
- `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md` ;
- `docs/delivery/lot_05_scm_cession_block_spec_canonique_v1.md` ;
- `docs/delivery/lot_05_scm_cession_block_resolution_v1.md` ;
- source Lot 02 du PV de nomination de gerant dans `project/source_documents/lot_02/` ;
- sources statuts SELARL dentiste et medecin dans `project/source_documents/lot_04/` ;
- sources cession cabinet et cession SCM deja referencees par les specs Lot 03 / Lot 05 ;
- modeles front/data et domaine existants en verification seulement.

## 2. Perimetre exact du contrat

Ce contrat couvre la famille de donnees et de decisions necessaire pour preparer :

- SELARL de creation a plusieurs associes ;
- president de seance rattache a un associe existant ;
- nomination d'un gerant unique dans un contexte multi-associes ;
- cadrage du futur modele multi-gerants sans l'implementer ;
- liens de readiness avec cession medicale/dentaire et cession SCM.

Ce contrat ne couvre pas une generation complete multi-associes de tout le pack SELARL. Les statuts `DOC-016` et `DOC-017` restent verrouilles sur les cas unipersonnels actuellement lockes. Les sources actuelles ne donnent pas encore un lock humain suffisant pour rendre les statuts multi-associes article par article.

## 3. Variantes incluses et exclues

Variantes incluses dans le contrat de source :

- multi-associes simple : au moins deux associes, tous presents ou representes, repartition de parts explicite, un gerant unique, pas de cession, pas de SCM, pas de derogation, pas de site distinct ;
- president de seance choisi parmi les associes existants ;
- rattachement du gerant unique a un associe existant quand c'est le cas.

Variantes exclues de l'implementation directe par ce ticket :

- plusieurs gerants nommes ;
- president de seance non associe ;
- associe represente par mandataire avec pouvoir detaille non source ;
- vote non unanime, abstention, opposition ou quorum partiel ;
- statuts SELARL multi-associes `DOC-016` / `DOC-017` ;
- cession medicale ou dentaire ;
- cession SCM ;
- derogation, site distinct, SELAS, SPFPL, SCI, SCM de creation ;
- `DOC-006`, `DOC-013`, `DOC-014` et documents marques manuels ou reserves.

## 4. Donnees a collecter

### 4.1 Associes

La saisie cible doit etre structuree en `associes[]`, sans alias documentaire implicite du type `personne_1`.

Par associe :

- identifiant stable front, par exemple `associe_id` ;
- `genre` ;
- `civilite_affichage` ;
- `prenom` ;
- `nom` ;
- `profession` ou `profession_reglementee` si le document l'exige ;
- adresse personnelle si un document l'exige ;
- situation matrimoniale, regime matrimonial et conjoint uniquement si le document active un bloc conjoint ;
- `nb_parts` ;
- `est_present_ou_represente` ;
- role optionnel : gerant nomme, president de seance, signataire.

### 4.2 Capital et parts

Donnees minimales :

- `capital_social` ;
- `nb_parts_total` ;
- `valeur_nominale_part` ;
- repartition des parts par associe.

Regle : la somme des `associes[].nb_parts` doit etre egale a `nb_parts_total`. Si ce controle echoue, la generation doit bloquer.

### 4.3 President de seance

Donnees minimales :

- `president_seance_ref_associe_id` si le dossier compte au moins deux associes ;
- derivation des variables documentaires :
  - `civilite_president_seance` ;
  - `prenom_president_seance` ;
  - `nom_personne_seance`.

Regle : pour un associe unique, le president peut etre derive de l'associe unique comme aujourd'hui. Pour plusieurs associes, le choix doit etre explicite parmi les associes existants. Aucun choix arbitraire ne doit etre invente.

### 4.4 Gerance

Donnees minimales pour le sous-cas source-suffisant :

- `dirigeant_nomine` unique ;
- lien optionnel `ref_associe_index` ou futur `ref_associe_id` quand le gerant est un associe ;
- identite complete du gerant si elle n'est pas derivee d'un associe existant.

Donnees a prevoir, mais non codables sans source complementaire :

- `gerants[]` ;
- ordre d'affichage des gerants ;
- resolution de nomination multi-gerants ;
- signatures et pouvoirs associes a plusieurs gerants.

## 5. Donnees a deriver

Derivations autorisees :

- `valeur_nominale_part = capital_social / nb_parts_total`, si division exacte et format conforme au moteur ;
- `nb_parts_representees = somme des parts des associes presents ou representes` ;
- libelle `Nomination du gerant` si un seul gerant ;
- libelle `Nomination des gerants` uniquement quand une source multi-gerants est validee ;
- variables president de seance depuis l'associe selectionne ;
- identite du gerant depuis l'associe selectionne quand le gerant est rattache a un associe.

Derivations interdites :

- choisir automatiquement le president parmi plusieurs associes ;
- deduire un mandataire ou un representant absent des sources ;
- deduire plusieurs gerants depuis une liste d'associes ;
- corriger le wording des statuts multi-associes sans reference humaine.

## 6. Donnees conditionnelles

Donnees conditionnelles autorisees :

- conjoint et regime communautaire uniquement si le bloc communautaire est actif ;
- date du courrier d'avertissement uniquement si `DOC-005` est actif ;
- donnees ordinales si `DOC-034` ou un document ordinal les exige ;
- donnees de cession uniquement si un sous-formulaire cession dedie est actif et source.

Donnees conditionnelles a bloquer sans source :

- president de seance externe aux associes ;
- plusieurs gerants ;
- pouvoirs de representation detaillee ;
- cession medicale/dentaire ;
- cession SCM ;
- clauses de vote hors unanimite.

## 7. Regles metier-front

### 7.1 Nombre d'associes

Le modele front peut preparer une liste de 2 a 6 associes, car les specs statuts SEL mentionnent une cible source de 1 a 6 associes. Toutefois, la generation des statuts multi-associes doit rester bloquee tant que le texte pluriel n'est pas verrouille.

Sous-cas source-suffisant : plusieurs associes pour `DOC-004` uniquement, avec tous les associes presents ou representes et disposant ensemble de la totalite des parts sociales.

### 7.2 Repartition des parts

Regles :

- chaque associe doit avoir un nombre de parts strictement positif ;
- la somme des parts doit correspondre au total ;
- les parts representees doivent correspondre au total pour rendre la formule humaine actuelle d'unanimite ;
- si un associe est absent non represente, le rendu doit bloquer faute de source de quorum/vote partiel.

### 7.3 President de seance

Regles :

- associe unique : rattachement automatique autorise ;
- plusieurs associes : selection obligatoire dans `associes[]` ;
- president externe : NO-GO faute de source ;
- les variables `civilite_president_seance`, `prenom_president_seance`, `nom_personne_seance` sont des sorties derivees, pas des champs a retaper si le president est un associe.

### 7.4 Un ou plusieurs gerants

Regles :

- gerant unique : GO limite si son identite est derivee ou saisie explicitement ;
- plusieurs gerants : NO-GO tant que la resolution, la presentation, les signatures et les pouvoirs multi-gerants ne sont pas verrouilles ;
- le modele actuel expose `dirigeant_nomine` au singulier. Un futur `gerants[]` devra etre ajoute proprement avant toute generation multi-gerants.

### 7.5 Resolution, vote et pouvoirs

La reference humaine PV autorise le rendu suivant seulement dans un cadre unanime :

- les associes presents ou representes disposent ensemble de la totalite des parts sociales ;
- l'ensemble est habilite a prendre des decisions ;
- le president rappelle l'ordre du jour ;
- la resolution est adoptee a l'unanimite ;
- les pouvoirs sont donnes au porteur d'un original pour les formalites.

Hors de ce cadre, le moteur doit bloquer.

## 8. Documents impactes

| Document | Impact multi-associes | Statut source |
|---|---|---|
| `DOC-004` PV nomination gerant | Liste `associes[]`, parts detenues, president de seance, ordre du jour, vote, pouvoirs | GO limite pour un gerant unique et unanimite totale |
| `DOC-016` statuts dentiste | Soussignes, apports, capital, repartition, signatures, articles associes | NO-GO multi-associes : lock actuel unipersonnel |
| `DOC-017` statuts medecin | Soussignes, apports, capital, repartition, signatures, articles associes | NO-GO multi-associes : lock actuel unipersonnel source-level |
| `DOC-001` DNC | Potentielle repetition par dirigeant ou associe selon decision | OPEN GAP : aucune regle source multi-associes |
| `DOC-002` domiciliation | Pas de delta evident lie au nombre d'associes | Pas d'impact direct identifie |
| `DOC-003` procuration | Signataire et pouvoirs potentiellement multi-signataires | OPEN GAP : aucune regle source multi-associes |
| `DOC-005` renonciation associe | Conjoint et communaute potentiellement par associe | GO seulement pour le cas communautaire deja locke ; multi-associes non source |
| `DOC-034` demande ordre | Donnees ordinales et praticiens multiples potentielles | PARTIAL : pas de lock multi-praticiens dans ce contrat |
| Cession cabinet | Donnees vendeur/acquereur/cabinet/bail/prix | NO-GO dans ce contrat, sous-formulaire dedie requis |
| Cession SCM `DOC-031` a `DOC-033` | Roles SCM, president, repartitions avant/apres, cessionnaire | NO-GO dans ce contrat, bloc SCM separe malgre sources existantes |

## 9. Matrice de readiness

Cette matrice juge la readiness pour une future implementation Track B limitee, pas pour une generation complete de tout le pack SELARL multi-associes.

| Sous-cas | Decision | Sources suffisantes | Risque | Raison |
|---|---|---|---|---|
| Multi-associes simple | GO limite | Oui pour `DOC-004`; non pour les statuts | Moyen | Le PV humain et la spec PV portent deja les associes presents/representes, les parts detenues, l'unanimite et les pouvoirs. Les statuts multi-associes restent bloques. |
| President de seance distinct | GO limite | Oui si le president est un associe existant | Moyen | Les variables president existent et peuvent etre derivees d'un associe selectionne. President externe non source. |
| Plusieurs gerants | NO-GO | Non | Eleve | Le libelle pluriel existe, mais le modele, la resolution, les signatures et les pouvoirs multi-gerants ne sont pas verrouilles. |
| Cession medicale/dentaire | NO-GO | Non pour ce contrat | Eleve | Les specs existent, mais elles documentent de nombreuses donnees et anomalies source. Il faut un sous-formulaire cession dedie, hors famille president/gerance. |
| Cession SCM | NO-GO pour ce contrat | Sources documentaires oui, contrat front SELARL non | Eleve | Le bloc SCM a une resolution source propre, mais il exige roles `personne_1` a `personne_4`, repartitions avant/apres, cessionnaire, cedant, credit-vendeur et validations dediees. |

## 10. Recommandation unique

Le meilleur prochain sous-cas a implementer en priorite est :

**multi-associes simple limite a `DOC-004`, avec president de seance selectionne parmi les associes existants, un gerant unique et unanimite totale.**

Pourquoi :

- c'est le plus petit delta source-suffisant apres les locks unipersonnels ;
- il reutilise directement le texte humain du PV sans inventer les statuts multi-associes ;
- il cree la structure `associes[]`, la validation de repartition des parts et la selection explicite du president, qui seront necessaires aux sous-cas suivants ;
- il evite de melanger les chantiers cession, SCM et multi-gerants.

Les statuts `DOC-016` et `DOC-017` doivent rester bloques en multi-associes tant qu'une reference humaine multi-associes n'a pas verrouille le wording article par article.

## 11. OPEN GAPS

1. Texte humain complet pour statuts SELARL multi-associes dentiste et medecin : soussignes, apports, capital, repartition, signatures et accords.
2. Regle documentaire sur `DOC-001` en multi-associes : document par gerant, par associe, ou par representant legal.
3. Regle documentaire sur `DOC-003` en multi-associes : signataire unique ou signatures multiples.
4. Portee multi-praticiens de `DOC-034`.
5. President de seance externe aux associes.
6. Associe absent ou represente par mandataire detaille.
7. Vote non unanime, quorum partiel, abstention ou opposition.
8. Plusieurs gerants : modele `gerants[]`, resolution, ordre d'affichage, signatures, pouvoirs.
9. Regime communautaire par associe dans un dossier multi-associes.
10. Interaction entre multi-associes et cession medicale/dentaire.
11. Interaction entre multi-associes et cession SCM.
12. Extension au site distinct, derogations et documents reserves/manuels.

## 12. Verrou de fin

Ce contrat autorise seulement une suite de travail bornee et sourcee sur `DOC-004`. Il ne de-verrouille pas les statuts multi-associes, ne valide pas plusieurs gerants et ne transforme pas les specs cession en sous-formulaires Track B.
