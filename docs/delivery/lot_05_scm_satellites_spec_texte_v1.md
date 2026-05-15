# DAAT x SYDEL - SPEC TEXTE V1
## Batch satellites SCM

## 1. Objet

Stabiliser le texte canonique et les variantes textuelles des satellites SCM avant tout codage.

Cette spec texte complète :
- `docs/delivery/lot_05_scm_satellites_spec_canonique_v1.md`

Elle couvre uniquement :
- le pacte d'associés SCM ;
- la liste des dépenses communes SCM ;
- le contrat de frais communs ;
- le règlement intérieur SCM.

Elle ne modifie aucun wording juridique source. Les formulations ambiguës sont conservées comme constats ou transformées en points ouverts bloquants avant code.

## 2. Sources lues

Mémoire projet et référentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md` en lecture seule
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md` en lecture seule
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_05_scm_satellites_preparation_v1.md`
- `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md`
- `docs/delivery/lot_05_scm_satellites_spec_canonique_v1.md`

Source de vérité métier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Sources documentaires lues :
- `project/source_documents/lot_05/Pacte d_associes SCM.docx`
- `project/source_documents/lot_05/Liste depenses communes SCM.doc`
- `project/source_documents/lot_05/CONTRAT FRAIS COMMUNS.docx`
- `project/source_documents/lot_05/REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx`

ADR applicables :
- ADR-0001 : source de vérité documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : génération DOCX propre from-scratch pour les futurs tickets code ;
- ADR-0005 : mode Codex repo-first.

Blocage explicite `.doc` :
- `Liste depenses communes SCM.doc` est une source legacy `.doc` ;
- le texte a été inventorié en lecture seule, mais la mise en page Word et la table doivent être converties ou remplacées avant automatisation ;
- aucun code ne doit être lancé sur cette source tant qu'une source DOCX propre ou une conversion validée n'existe pas.

## 3. Périmètre texte V1

Chemin couvert :
- `SCM`, limité aux quatre satellites inventoriés.

Hors périmètre :
- statuts SCM ;
- documents universels ;
- PV nomination gérant ;
- demande d'inscription à l'ordre ;
- fiche de création SCM ;
- cessions de parts SCM ;
- toute réécriture juridique.

Décision texte V1 :
- conserver les documents comme quatre textes indépendants ;
- ne pas généraliser les formulations vers un nombre dynamique de parties ;
- ne pas corriger les incohérences ou maladresses source sans validation métier ;
- documenter les blocages plutôt que produire une variante locale.

## 4. Pacte d'associés SCM

### 4.1 Structure texte source

Structure visible :
- titre `PACTE D'ASSOCIES` ;
- comparution de deux associés historiques ;
- présence de la société SCM ;
- rappel préalable ;
- Titre I : objet, définitions, déclarations ;
- Titre II : cessions de titres ;
- Titre III : gouvernance ;
- Titre IV : départ d'un associé ;
- Titre V : droit d'information ;
- Titre VI : stipulations spécifiques ;
- dispositions générales ;
- règlement des différends ;
- signatures ;
- Annexe 1 statuts ;
- Annexe 2 acte d'adhésion.

### 4.2 Squelette texte V1

Le squelette ci-dessous décrit les zones variables et l'ordre des blocs. Il ne remplace pas le texte juridique source complet.

```text
PACTE D'ASSOCIES
PORTANT SUR LES PARTS SOCIALES
DE LA SOCIETE {societe.denomination}

LES SOUSSIGNEES :

{associes[0].civilite_affichage} {associes[0].prenom} {associes[0].nom}

ET

{associes[1].civilite_affichage} {associes[1].prenom} {associes[1].nom}

Tous associés de la société {societe.denomination}

En présence de la société :

- {societe.forme_juridique} {societe.denomination}
{societe.forme_juridique}
Au capital de {societe.capital_social}
Siège social : {societe.siege.adresse_affichee}
Immatriculée au RCS de {societe.ville_rcs} sous le n°{societe.numero_rcs}

IL A ETE PREALABLEMENT RAPPELE CE QUI SUIT :

Le capital social de la Société est composé, à la date de signature du Pacte, de {societe.nb_parts_total} parts sociales.

TITRE I - OBJET - DEFINITIONS - DECLARATIONS
...
TITRE II - MODALITES RELATIVES AUX CESSIONS DE TITRES DE LA SOCIETE
...
TITRE III - GOUVERNANCE DE LA SOCIETE
...
TITRE IV - DEPART D'UN ASSOCIE
...
TITRE V - DROIT D'INFORMATION
...
TITRE VI - STIPULATIONS SPECIFIQUES
...
TITRE VI - DISPOSITIONS GENERALES
...

Les Parties conviennent que tout litige qui n'aurait pu être réglé par la voie de la conciliation [...] sera de la compétence exclusive du Tribunal de Commerce de {pacte_associes.ville_tribunal}.

Fait à {signature.lieu}
Le {signature.date}
en autant d'exemplaires que de Parties.

{associes[0].civilite_affichage} {associes[0].prenom} {associes[0].nom}
{associes[1].civilite_affichage} {associes[1].prenom} {associes[1].nom}

Annexe 1
Statuts de la société {societe.denomination}

Annexe 2
Acte d'Adhésion au pacte d'associés de la {societe.forme_juridique} {societe.denomination}
```

### 4.3 Variables texte obligatoires

- `societe.denomination`
- `societe.forme_juridique`
- `societe.capital_social`
- `societe.siege.adresse_affichee`
- `societe.ville_rcs`
- `societe.numero_rcs`
- `societe.nb_parts_total`
- `associes[0].civilite_affichage`
- `associes[0].prenom`
- `associes[0].nom`
- `associes[1].civilite_affichage`
- `associes[1].prenom`
- `associes[1].nom`
- `pacte_associes.ville_tribunal`
- `signature.lieu`
- `signature.date`

### 4.4 Blocs et limites

Blocs fixes :
- définitions ;
- cession et préemption ;
- gouvernance ;
- départ d'un associé ;
- droit d'information ;
- clauses de non-sollicitation et non-concurrence ;
- dispositions générales ;
- annexes.

Blocs conditionnels non automatisés en V1 :
- plus de deux associés historiques ;
- associé historique personne morale ;
- suppression ou modification des clauses de cession, préemption ou non-concurrence ;
- annexe statuts remplie automatiquement.

Règle texte :
- le futur rendu doit bloquer si le dossier impose une adaptation juridique non prévue par la source.

## 5. Liste dépenses communes SCM

### 5.1 Structure texte source

Structure visible :
- en-tête société ;
- mention de société en cours d'immatriculation ;
- tableau `DENOMINATION DE LA DEPENSE` ;
- colonnes `AU PRORATA DES PARTS DE SCM` et `AU PRORATA CHIFFRE D'AFFAIRES` ;
- signatures de deux personnes.

### 5.2 Squelette texte V1

```text
{societe.denomination}
{societe.forme_juridique} au capital de {societe.capital_social}
Siège social : {societe.siege.adresse_affichee}
En cours d'immatriculation au RCS de {societe.ville_rcs}

DENOMINATION DE LA DEPENSE
AU PRORATA DES PARTS DE SCM
AU PRORATA CHIFFRE D'AFFAIRES

Loyer et charges locatives d'eau, gaz, électricité | X |
Téléphone | X |
Assurance de biens mobiliers, immobiliers et du personnel de l'association | X |
Frais d'entretien, de réparation des locaux | X |
Salaires et charges sociales du personnel de la SCM | X |
Frais d'honoraires versés par la SCM à des tiers (comptable) | X |
Frais de gestions comptables et fiscales | X |
Frais afférents aux disposition obligatoires de fonctionnement [...] | X |
Frais d'entretien et de réparation du mobilier | X |
Produits consommables, fournitures de bureau, consommables clinique | X |
Frais afférents au logiciel professionnel ou autres frais de maintenance et au matériel informatique | X |
Frais de prothèse | X | X
Frais de cadeaux, réception, représentation au personnel | X |
Achat validé par la SCM | | |
Pressing | X |

{associes[0].prenom} {associes[0].nom}
{associes[1].prenom} {associes[1].nom}
```

### 5.3 Variables texte obligatoires

- `societe.denomination`
- `societe.forme_juridique`
- `societe.capital_social`
- `societe.siege.adresse_affichee`
- `societe.ville_rcs`
- `associes[0].prenom`
- `associes[0].nom`
- `associes[1].prenom`
- `associes[1].nom`

### 5.4 Blocs et limites

Blocs fixes :
- tableau des dépenses ;
- marques `X` source ;
- deux signatures.

Blocage texte :
- le document ne doit pas être codé tant que la source `.doc` n'est pas convertie ou remplacée ;
- aucune reconstruction de tableau à partir du seul extrait texte ne vaut validation de mise en page.

Blocs conditionnels non automatisés en V1 :
- lignes de dépenses dynamiques ;
- clés de répartition différentes ;
- ajout de signataires.

## 6. Contrat frais communs

### 6.1 Structure texte source

Structure visible :
- titre `CONTRAT D'EXERCICE PROFESSIONNEL A FRAIS COMMUNS` ;
- comparution de deux sociétés ;
- article 1 : exercice à frais communs dans les locaux ;
- article 2 : locaux, matériel et dépenses communes ;
- tableau de dépenses au prorata du temps d'occupation des salles de soin ;
- dépenses professionnelles personnelles ;
- article 3 : durée indéterminée et prise d'effet ;
- article 4 : interdiction d'exercer ;
- article 5 : remplacement ;
- article 6 : départ et documents patients ;
- article 7 : conciliation ordinale et tribunal ;
- article 8 : absence de contre-lettre ;
- signature.

### 6.2 Squelette texte V1

```text
CONTRAT D'EXERCICE PROFESSIONNEL
A FRAIS COMMUNS

ENTRE LES SOUSSIGNES :

{parties_frais_communs[0].societe.denomination}
{parties_frais_communs[0].societe.forme_juridique}
Au capital de {parties_frais_communs[0].societe.capital_social}
Siège social : {parties_frais_communs[0].societe.siege.adresse_affichee}
Immatriculée au RCS de {parties_frais_communs[0].societe.ville_rcs} sous le numéro {parties_frais_communs[0].societe.numero_rcs}
Représentée par {parties_frais_communs[0].representant.civilite_affichage} {parties_frais_communs[0].representant.prenom} {parties_frais_communs[0].representant.nom} en qualité de {parties_frais_communs[0].representant.fonction}, domicilié en cette qualité audit siège.

ET

{parties_frais_communs[1].societe.denomination}
{parties_frais_communs[1].societe.forme_juridique} au capital de {parties_frais_communs[1].societe.capital_social}
Ayant son siège au {locaux.adresse_affichee}
Immatriculée au RCS de {parties_frais_communs[1].societe.ville_rcs} sous le numéro {parties_frais_communs[1].societe.numero_rcs}
Représentée par son {parties_frais_communs[1].representant.fonction}, {parties_frais_communs[1].representant.civilite_affichage} {parties_frais_communs[1].representant.prenom} {parties_frais_communs[1].representant.nom}, domicilié en cette qualité audit siège.

IL A ETE CONVENU ET ARRETE CE QUI SUIT :

Article 1 - Les soussignés décident d'exercer leur profession à frais communs dans un cabinet sis {locaux.adresse_affichee}.

Article 2 - [...]
Le local professionnel mis en commun est situé {locaux.adresse_affichee}, composé d'une entrée, salle d'attente, deux pièces à usage de cabinet dentaire, WC, pièce à usage de stérilisation, lesquels sont loués par bail professionnel.

[Table des dépenses communes source]

Article 3 - Le présent contrat est conclu pour une durée indéterminée à compter du {frais_communs.date_effet_contrat}.

Articles 4 à 8 [...]

A {signature.lieu}, le {signature.date}
```

### 6.3 Variables texte obligatoires

- `parties_frais_communs[0].societe.denomination`
- `parties_frais_communs[0].societe.forme_juridique`
- `parties_frais_communs[0].societe.capital_social`
- `parties_frais_communs[0].societe.siege.adresse_affichee`
- `parties_frais_communs[0].societe.ville_rcs`
- `parties_frais_communs[0].societe.numero_rcs`
- `parties_frais_communs[0].representant.civilite_affichage`
- `parties_frais_communs[0].representant.prenom`
- `parties_frais_communs[0].representant.nom`
- `parties_frais_communs[0].representant.fonction`
- `parties_frais_communs[1].societe.denomination`
- `parties_frais_communs[1].societe.forme_juridique`
- `parties_frais_communs[1].societe.capital_social`
- `parties_frais_communs[1].societe.ville_rcs`
- `parties_frais_communs[1].societe.numero_rcs`
- `parties_frais_communs[1].representant.civilite_affichage`
- `parties_frais_communs[1].representant.prenom`
- `parties_frais_communs[1].representant.nom`
- `parties_frais_communs[1].representant.fonction`
- `locaux.adresse_affichee`
- `frais_communs.date_effet_contrat`
- `signature.lieu`
- `signature.date`

### 6.4 Blocs et limites

Blocs fixes :
- articles 1 à 8 ;
- description des locaux ;
- table des dépenses communes ;
- dépenses personnelles ;
- conciliation ordinale ;
- contre-lettre.

Blocs conditionnels non automatisés en V1 :
- plus de deux parties ;
- locaux non dentaires ou description différente ;
- répartition des frais autre que temps d'occupation des salles de soin ;
- partie 2 dont le siège ne correspond pas aux locaux.

Règle texte :
- le futur rendu doit bloquer si la description fixe des locaux ou la clé de répartition ne correspond pas au dossier.

## 7. Règlement intérieur SCM

### 7.1 Structure texte source

Structure visible :
- titre `REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS` ;
- comparution de deux sociétés ;
- préambule ;
- article 1 : objet et durée du règlement intérieur ;
- article 2 : déontologie et exercice ;
- article 3 : gestion du cabinet ;
- article 4 : moyens mis en commun ;
- article 5 : absence des associés ;
- article 6 : assurance ;
- article 7 : exclusion ;
- article 8 : litiges ;
- article 9 : communication ;
- article 10 : clauses particulières ;
- autonomie des clauses ;
- signature en quatre exemplaires.

### 7.2 Squelette texte V1

```text
REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS
{societe.denomination}

ENTRE LES SOUSSIGNEES :

{parties_frais_communs[0].societe.denomination}
{parties_frais_communs[0].societe.forme_juridique}
Au capital social de {parties_frais_communs[0].societe.capital_social}
Sise {parties_frais_communs[0].societe.siege.adresse_affichee}
Immatriculée au RCS de {parties_frais_communs[0].societe.ville_rcs} sous le numéro {parties_frais_communs[0].societe.numero_rcs}
Représentée par le {parties_frais_communs[0].representant.titre_affichage} {parties_frais_communs[0].representant.identite_affichee}, {parties_frais_communs[0].representant.fonction}

D'UNE PART

{parties_frais_communs[1].societe.denomination}
{parties_frais_communs[1].societe.forme_juridique}
Au capital social de {parties_frais_communs[1].societe.capital_social}
Sise {parties_frais_communs[1].societe.siege.adresse_affichee}
Immatriculée au RCS de {parties_frais_communs[1].societe.ville_rcs} sous le numéro {parties_frais_communs[1].societe.numero_rcs}
Représentée par le {parties_frais_communs[1].representant.titre_affichage} {parties_frais_communs[1].representant.identite_affichee}, {parties_frais_communs[1].representant.fonction}

D'UNE AUTRE PART

IL A ETE CONVENU ET ARRETE CE QUI SUIT :

PREAMBULE
...

ARTICLE 1 - OBJET ET DUREE DU REGLEMENT INTERIEUR
...

ARTICLE 2 - DEONTOLOGIE - EXERCICE
...

ARTICLE 4 - MOYENS MIS EN COMMUN
Les contractants se sont mis d'accord pour l'utilisation en commun des locaux situés {locaux.adresse_affichee}
...
Toute dépense de la société qualifiée de "dépense commune" nécessite l'accord de tous les associés lorsque ladite dépense excède la somme de {reglement_interieur.seuil_depense_commune}.
...
Il est annexé à ce règlement le tableau de répartition des charges entre associés pour l'année {reglement_interieur.annee_reference_charges}.
...
La "gestion administrative" [...] sera effectuée conjointement par chacun des cogérants jusqu'au {reglement_interieur.date_fin_gestion_administrative}.
Il sera attribué, chaque année au {reglement_interieur.date_attribution_responsabilites}, à chacun des cogérants, des responsabilités bien définies.

ARTICLE 10 - CLAUSES PARTICULIERES
...
Pour joindre le Docteur {praticiens[0].identite_affichee} composez le n° {praticiens[0].telephone}
Pour joindre le Docteur {praticiens[1].identite_affichee} composez le n° {praticiens[1].telephone}
...

Fait à {signature.lieu}
Le {signature.date}

En quatre exemplaires

Pour la {parties_frais_communs[0].societe.denomination}
Le {parties_frais_communs[0].representant.titre_affichage} {parties_frais_communs[0].representant.identite_affichee}

Pour la {parties_frais_communs[1].societe.denomination}
Le {parties_frais_communs[1].representant.titre_affichage} {parties_frais_communs[1].representant.identite_affichee}
```

### 7.3 Variables texte obligatoires

- `societe.denomination`
- `parties_frais_communs[0].societe.denomination`
- `parties_frais_communs[0].societe.forme_juridique`
- `parties_frais_communs[0].societe.capital_social`
- `parties_frais_communs[0].societe.siege.adresse_affichee`
- `parties_frais_communs[0].societe.ville_rcs`
- `parties_frais_communs[0].societe.numero_rcs`
- `parties_frais_communs[0].representant.titre_affichage`
- `parties_frais_communs[0].representant.identite_affichee`
- `parties_frais_communs[0].representant.fonction`
- `parties_frais_communs[1].societe.denomination`
- `parties_frais_communs[1].societe.forme_juridique`
- `parties_frais_communs[1].societe.capital_social`
- `parties_frais_communs[1].societe.siege.adresse_affichee`
- `parties_frais_communs[1].societe.ville_rcs`
- `parties_frais_communs[1].societe.numero_rcs`
- `parties_frais_communs[1].representant.titre_affichage`
- `parties_frais_communs[1].representant.identite_affichee`
- `parties_frais_communs[1].representant.fonction`
- `locaux.adresse_affichee`
- `reglement_interieur.seuil_depense_commune`
- `reglement_interieur.annee_reference_charges`
- `reglement_interieur.date_fin_gestion_administrative`
- `reglement_interieur.date_attribution_responsabilites`
- `praticiens[0].identite_affichee`
- `praticiens[0].telephone`
- `praticiens[1].identite_affichee`
- `praticiens[1].telephone`
- `signature.lieu`
- `signature.date`

### 7.4 Blocs et limites

Blocs fixes :
- préambule ;
- clauses de déontologie ;
- moyens mis en commun ;
- dépenses communes et personnelles ;
- absence, assurance, exclusion et litiges ;
- communication ;
- clauses particulières de temps partiel, part sociale et rupture d'association ;
- autonomie des clauses ;
- signature en quatre exemplaires.

Blocs conditionnels non automatisés en V1 :
- parties ou praticiens au-delà de deux ;
- formes sociales différentes entre les deux parties ;
- suppression des clauses de départ ou de téléphone ;
- profession ou titre autre que les formules source ;
- répartition des charges différente.

Règle texte :
- le futur rendu doit bloquer si le contexte nécessite une adaptation métier du règlement intérieur.

## 8. Variables partagées entre les satellites

Variables communes :
- `societe.denomination`
- `societe.forme_juridique`
- `societe.capital_social`
- `societe.siege.adresse_affichee`
- `societe.ville_rcs`
- `signature.lieu`
- `signature.date`

Variables à maintenir cohérentes avec les statuts SCM :
- `societe.numero_rcs`
- `societe.nb_parts_total`
- `associes[]`
- `associes[].parts.nb`
- données de représentants lorsque les associés sont des personnes morales.

Variables locales au batch :
- `parties_frais_communs[]`
- `praticiens[]`
- `locaux.adresse_affichee`
- `pacte_associes.ville_tribunal`
- `frais_communs.date_effet_contrat`
- `reglement_interieur.*`

## 9. Éléments manuels

Éléments qui doivent venir du contexte ou d'une saisie contrôlée :
- satellites à produire ;
- deux associés historiques du pacte ;
- deux parties aux frais communs et au règlement intérieur ;
- représentants, titres et fonctions ;
- identités et téléphones des praticiens ;
- adresse des locaux ;
- ville du tribunal compétent ;
- date d'effet du contrat ;
- seuil de dépense commune ;
- année de référence des charges ;
- dates de gestion administrative ;
- lieu et date de signature ;
- confirmation des nombres d'exemplaires ;
- validation des tables de dépenses ;
- conversion ou remplacement de la source `.doc`.

Le moteur ne doit pas inventer ces valeurs.

## 10. Règles de blocage texte

Un futur générateur doit bloquer si :
- le dossier n'est pas `SCM` ;
- le satellite demandé n'est pas explicitement activé ;
- la liste des dépenses communes est demandée sans source DOCX propre ou conversion validée ;
- le dossier contient plus de deux associés, parties ou praticiens pour un document limité à deux ;
- les parties du règlement intérieur ont des formes sociales différentes alors que la source utilise un seul placeholder ;
- le contrat frais communs nécessite une description de locaux différente ;
- les tables de dépenses doivent être modifiées ;
- une clause juridique doit être ajoutée, supprimée ou réécrite ;
- les données de statuts SCM et de satellites divergent ;
- le rendu final conserverait un placeholder `[` ou `]` ;
- le rendu final corrigerait une anomalie source sans note de validation.

## 11. Critères avant implémentation

Un ticket de code pourra démarrer seulement si :
- il cible explicitement un satellite ou le batch complet ;
- la source `.doc` est convertie ou exclue du ticket de code ;
- la limite V1 à deux associés ou deux parties est confirmée ;
- les clauses sensibles sont validées comme applicables au dossier type ;
- les tables de dépenses sont validées comme fixes ;
- les tests futurs couvrent les blocages principaux ;
- les tests futurs vérifient l'absence de placeholders résiduels ;
- aucun wording juridique n'est modifié silencieusement.

## 12. Points ouverts

1. **Source `.doc`** : conversion ou remplacement obligatoire de `Liste depenses communes SCM.doc` avant code.
2. **Activation du batch** : génération automatique ou sélection explicite des satellites à arbitrer.
3. **Nombre de parties** : les quatre sources sont stabilisées sur deux personnes ou deux parties ; aucune version N n'est sourceée.
4. **Pacte** : confirmer les clauses sensibles et le traitement des annexes.
5. **Liste dépenses** : confirmer la table source, les marques `X` et les lignes sans marque.
6. **Contrat frais communs** : confirmer la description fixe des locaux dentaires et la clé au temps d'occupation.
7. **Règlement intérieur** : confirmer le placeholder unique de forme sociale, les clauses de téléphone et le nombre de quatre exemplaires.
8. **Profession / titres** : confirmer les mentions `Docteur`, `praticien`, `cabinet dentaire` et autres formulations professionnelles.
9. **Cohérence statuts** : confirmer les données communes à contrôler entre statuts SCM et satellites.

## 13. Statut de la spec texte

`SPEC-SCM-SATELLITES-001` stabilise la spec texte V1 des satellites SCM sans code Python.

La prochaine étape recommandée est un arbitrage métier sur les points ouverts 1, 2, 3, 4, 6, 7 et 8 avant tout ticket de code.
