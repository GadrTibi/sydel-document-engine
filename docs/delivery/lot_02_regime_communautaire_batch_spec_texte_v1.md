# DAAT x SYDEL - SPEC TEXTE V1
## Batch `regime communautaire`

## 1. Objet

Stabiliser le texte canonique et les variantes textuelles du batch `regime communautaire`, sans coder.

Cette spec texte complete :
- `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md`

Elle vise a preparer un generateur deterministe qui :
- produit les deux lettres du batch quand le dossier est en regime communautaire ;
- conserve deux documents canoniques distincts ;
- isole les textes fixes, les variables, les overlays structurels et les points manuels ;
- ne transforme pas les variantes SELARL en corrections silencieuses.

## 2. Sources texte comparees

Sources majoritaires placees dans `source_documents` :
- renonciation source Lot 2 / SELAS / SPFPL, hash prefix `cd1cd16e4d224bd9` ;
- avertissement source Lot 2 / SELAS / SPFPL, hash prefix `e5ab70fea0303ae8`.

Variantes SELARL distinctes :
- renonciation SELARL, hash prefix `bfc15f04aee628cd` ;
- avertissement SELARL, hash prefix `b034c30291d20619`.

Decision texte V1 :
- le texte canonique de renonciation suit le groupe source Lot 2 / SELAS / SPFPL ;
- le texte canonique d'avertissement suit le groupe source Lot 2 / SELAS / SPFPL avec un overlay limite pour la mention manuscrite SELARL ;
- les differences SELARL restent documentees et devront etre relues humainement au premier rendu SELARL.

## 3. Texte source extrait

### 3.1 Renonciation - groupe source Lot 2 / SELAS / SPFPL

```text
A [lieu_signature]
Le [date_signature]
Objet : Lettre de renonciation à revendiquer la qualité d'associé
[civilite] [prenom] [nom],
Par courrier en date du [date_courrier], tu m’as fait part du projet de constitution de la société [denomination_societe], [forme_sociale_complete], à laquelle tu souhaites t'associer en apportant [apport_personne_1] ([apport_lettres_personne_1]) euros dépendant de notre [regime_matrimonial].
Je te notifie, par la présente, mon intention de renoncer à la faculté de devenir personnellement [qualite_associe] de cette société.
En tout état de cause, et conformément aux dispositions du Code civil, je déclare donner mon consentement à l'apport effectué par mon conjoint.
En [nombre_exemplaires_lettres] exemplaires
[prenom_conjoint] [nom_conjoint]
```

### 3.2 Renonciation - variante SELARL

```text
A [lieu_signature]
Le [date_signature]
Objet : Lettre de renonciation à revendiquer la qualité d'associé
[civilite] [prenom] [nom],
Par courrier en date du [date_du_jour], tu m’as fait part du projet de constitution de la société [denomination_societe], [forme_sociale_complete], à laquelle tu souhaites t'associer en apportant [apport_personne_1] ([apport_lettres_personne_1]) euros dépendant de notre communauté
Je te notifie, par la présente, mon intention de renoncer à la faculté de devenir personnellement associé de cette société.
En tout état de cause, et conformément aux dispositions du Code civil, je déclare donner mon consentement à l'apport effectué par mon conjoint.
En 2exemplaires
[prenom_conjoint] [nom_conjoint]
```

### 3.3 Avertissement - groupe source Lot 2 / SELAS / SPFPL

```text
[denomination_societe]
[forme_sociale]
Au capital de [capital_social] €
[num_voie_siege] [voie_siege]
[cp_siege] [ville_siege]
[civilite_conjoint] [nom_conjoint]
[num_voie_conjoint] [voie_conjoint]
[cp_conjoint] [ville_conjoint]
Le  [date_signature]
Objet : Lettre d'avertissement au conjoint en cas d'apport d'un bien commun.
[civilite_conjoint] [nom_conjoint],
En application des dispositions de l'article 1832-2 alinéa 1 er du Code civil, je t’informe par la présente que j'ai l'intention de faire apport à une Société dont les caractéristiques sont décrites ci-après :
[denomination_societe]
[forme_sociale]
Au capital de [capital_social] €
[num_voie_siege] [voie_siege]
[cp_siege] [ville_siege]
- d'une somme en numéraire de [montant_apport_lettres] ([montant_apport]) euros dépendant de notre communauté.
Fait en trois exemplaires
[civilite] [prenom] [nom]
Agissant en qualité de futur [fonction_dirigeant]
[civilite_conjoint] [nom_conjoint]
(Faire précéder de la mention « j’atteste avoir été informé de l’apport de [montant_apport] euros par [civilite] [prenom] [nom] à la [forme_sociale_abregee] [denomination_societe] »)
```

### 3.4 Avertissement - variante SELARL

La variante SELARL a le meme texte principal que le groupe source Lot 2 / SELAS / SPFPL. Seule la mention manuscrite differe :

```text
(Faire précéder de la mention « j’atteste avoir été informé de l’apport de [montant_apport] euros par [civilite] [prenom] [nom] à la Société [denomination_societe] »)
```

## 4. Texte canonique V1 - Lettre d'avertissement

### 4.1 Texte fixe principal

```text
{societe.denomination}
{societe.forme_sociale}
Au capital de {societe.capital_social} €
{societe.siege.num_voie} {societe.siege.voie}
{societe.siege.cp} {societe.siege.ville}
{conjoint.civilite_affichage} {conjoint.nom}
{conjoint.adresse.num_voie} {conjoint.adresse.voie}
{conjoint.adresse.cp} {conjoint.adresse.ville}
Le  {regime_communautaire.avertissement.date_signature}

Objet : Lettre d'avertissement au conjoint en cas d'apport d'un bien commun.

{conjoint.civilite_affichage} {conjoint.nom},

En application des dispositions de l'article 1832-2 alinéa 1 er du Code civil, je t’informe par la présente que j'ai l'intention de faire apport à une Société dont les caractéristiques sont décrites ci-après :

{societe.denomination}
{societe.forme_sociale}
Au capital de {societe.capital_social} €
{societe.siege.num_voie} {societe.siege.voie}
{societe.siege.cp} {societe.siege.ville}

- d'une somme en numéraire de {apport.montant_lettres} ({apport.montant}) euros dépendant de notre communauté.

Fait en trois exemplaires

{apporteur.civilite_affichage} {apporteur.prenom} {apporteur.nom}
Agissant en qualité de futur {apporteur.fonction_dirigeant}

{conjoint.civilite_affichage} {conjoint.nom}
{mention_manuscrite_instruction}
```

Regles de fidelite :
- le double espace source dans `Le  {date}` est conserve en V1 ;
- `alinea 1 er` conserve l'espacement source ;
- `Société` est une majuscule source dans le corps ;
- `Fait en trois exemplaires` est fixe en V1 ;
- `futur` est fixe en V1 et ne varie pas automatiquement selon le genre.

### 4.2 Overlay de mention manuscrite

SELARL :

```text
(Faire précéder de la mention « j’atteste avoir été informé de l’apport de {apport.montant} euros par {apporteur.civilite_affichage} {apporteur.prenom} {apporteur.nom} à la Société {societe.denomination} »)
```

SELAS / SPFPL cession / SPFPL apport :

```text
(Faire précéder de la mention « j’atteste avoir été informé de l’apport de {apport.montant} euros par {apporteur.civilite_affichage} {apporteur.prenom} {apporteur.nom} à la {societe.forme_sociale_abregee} {societe.denomination} »)
```

Regles :
- ne pas remplir une mention manuscrite a la place du conjoint ;
- rendre l'instruction comme texte source ;
- bloquer SELAS / SPFPL si `societe.forme_sociale_abregee` est absent ;
- ne pas exiger `societe.forme_sociale_abregee` pour SELARL.

## 5. Texte canonique V1 - Lettre de renonciation

### 5.1 Texte fixe principal

```text
A {regime_communautaire.renonciation.lieu_signature}
Le {regime_communautaire.renonciation.date_signature}

Objet : Lettre de renonciation à revendiquer la qualité d'associé

{apporteur.civilite_affichage} {apporteur.prenom} {apporteur.nom},

Par courrier en date du {regime_communautaire.date_courrier_avertissement}, tu m’as fait part du projet de constitution de la société {societe.denomination}, {societe.forme_sociale_complete}, à laquelle tu souhaites t'associer en apportant {apport.montant} ({apport.montant_lettres}) euros dépendant de notre {regime_communautaire.regime_matrimonial}.

Je te notifie, par la présente, mon intention de renoncer à la faculté de devenir personnellement {regime_communautaire.qualite_renoncee} de cette société.

En tout état de cause, et conformément aux dispositions du Code civil, je déclare donner mon consentement à l'apport effectué par mon conjoint.

En {regime_communautaire.renonciation.nombre_exemplaires_lettres} exemplaires

{conjoint.prenom} {conjoint.nom}
```

Regles de fidelite :
- la lettre conserve le tutoiement source ;
- `mon conjoint` reste fixe en V1 ;
- la qualite renoncee n'est pas derivee automatiquement de la structure ;
- la valeur `regime_communautaire.regime_matrimonial` permet de rendre `communaute` sans coder ce mot en dur ;
- la variante SELARL brute `En 2exemplaires` n'est pas retenue comme overlay automatique.

### 5.2 Resolution de la date du courrier

Regle V1 :
- si `regime_communautaire.date_courrier_avertissement` est fourni, utiliser cette date ;
- sinon, si les deux lettres sont produites ensemble, utiliser `regime_communautaire.avertissement.date_signature` ;
- sinon, bloquer la generation de la renonciation.

## 6. Variables texte attendues

### 6.1 Variables communes

- `dossier.structure`
- `dossier.options.regime_communautaire`
- `societe.denomination`
- `societe.forme_sociale`
- `societe.forme_sociale_complete`
- `societe.capital_social`
- `societe.siege.num_voie`
- `societe.siege.voie`
- `societe.siege.cp`
- `societe.siege.ville`
- `apport.montant`
- `apport.montant_lettres`
- `apporteur.civilite_affichage`
- `apporteur.prenom`
- `apporteur.nom`
- `conjoint.civilite_affichage`
- `conjoint.nom`

### 6.2 Variables propres a l'avertissement

- `conjoint.adresse.num_voie`
- `conjoint.adresse.voie`
- `conjoint.adresse.cp`
- `conjoint.adresse.ville`
- `regime_communautaire.avertissement.date_signature`
- `apporteur.fonction_dirigeant`
- `societe.forme_sociale_abregee` pour SELAS / SPFPL.

### 6.3 Variables propres a la renonciation

- `regime_communautaire.renonciation.lieu_signature`
- `regime_communautaire.renonciation.date_signature`
- `regime_communautaire.date_courrier_avertissement`
- `regime_communautaire.regime_matrimonial`
- `regime_communautaire.qualite_renoncee`
- `regime_communautaire.renonciation.nombre_exemplaires_lettres`
- `conjoint.prenom`

## 7. Variantes de genre et nombre

### 7.1 Genre

Variantes explicitement sourcees :
- aucune variante feminine explicite n'est fournie pour `futur [fonction_dirigeant]` ;
- aucune variante `ma conjointe` n'est fournie pour `mon conjoint` ;
- `[qualite_associe]` existe dans le groupe source Lot 2 / SELAS / SPFPL et doit porter la bonne qualite affichee.

Decision V1 :
- ne pas feminiser automatiquement `futur` ;
- ne pas varier automatiquement `mon conjoint` ;
- rendre `regime_communautaire.qualite_renoncee` tel que fourni.

### 7.2 Nombre

Variantes explicitement sourcees :
- `Fait en trois exemplaires` est fixe dans l'avertissement ;
- `En [nombre_exemplaires_lettres] exemplaires` est variable dans la renonciation ;
- `euros` est fixe au pluriel dans les deux lettres.

Decision V1 :
- ne pas ajouter de regle automatique `euro/euros` pour ce batch ;
- bloquer si `nombre_exemplaires_lettres` manque dans la renonciation ;
- conserver `Fait en trois exemplaires` pour l'avertissement.

## 8. Points manuels

Les elements suivants restent manuels ou fournis par contexte / referentiel :
- mention manuscrite effective du conjoint : le document imprime seulement l'instruction ;
- qualite renoncee : `associe`, `associee`, `actionnaire` ou autre valeur validee ;
- formes sociales complete, affichee et abregee ;
- dates de signature et date du courrier d'avertissement ;
- regime matrimonial affiche dans la renonciation ;
- fonction dirigeante affichee dans `futur [fonction_dirigeant]`.

Le generateur ne doit pas :
- inventer une mention manuscrite ;
- deduire une qualite juridique non fournie ;
- corriger `alinea 1 er`, `Le  [date]`, `mon conjoint` ou `futur` sans ticket explicite ;
- ajouter le prenom du conjoint dans l'avertissement, car la source ne le fait pas.

## 9. Regles de blocage avant generation

Le futur generateur doit bloquer si :
- la structure n'est pas SELARL, SELAS, SPFPL cession ou SPFPL apport ;
- `dossier.options.regime_communautaire` n'est pas vrai ;
- une variable commune obligatoire manque ;
- une variable propre au document demande manque ;
- la date du courrier d'avertissement ne peut pas etre resolue pour la renonciation ;
- la mention manuscrite SELAS / SPFPL ne peut pas etre rendue faute de `societe.forme_sociale_abregee` ;
- `regime_communautaire.qualite_renoncee` est absent.

Le futur generateur ne doit pas bloquer uniquement parce que :
- la structure est SELARL et `societe.forme_sociale_abregee` manque, car l'overlay SELARL n'en a pas besoin ;
- `conjoint.prenom` manque pour l'avertissement seul, car la source n'utilise pas ce prenom dans ce document.

## 10. Criteres avant implementation

Le ticket de code peut demarrer si :
- les deux documents sont generes dans le batch pour chaque structure couverte ;
- la selection SELARL / SELAS / SPFPL de la mention manuscrite est testee ;
- la renonciation utilise une date de courrier explicite ou, a defaut, la date de l'avertissement genere dans le meme batch ;
- les tests couvrent le blocage en cas de `qualite_renoncee` absente ;
- les tests couvrent le blocage en cas de `societe.forme_sociale_abregee` absente pour SELAS / SPFPL ;
- les tests verifient l'absence de placeholders residuels `[` / `]` ;
- aucun code Python ne modifie les autres generateurs documentaires.

## 11. Points ouverts restants

Points ouverts non bloquants pour `CODE-RC-001`, a garder visibles en revue humaine :

1. La variante SELARL de renonciation contient des valeurs fixes et `En 2exemplaires`; la V1 retient la source Lot 2 / SELAS / SPFPL pour eviter un overlay fonde sur une anomalie probable.
2. La source ne fournit pas de variante feminine de `futur`; toute variation `future` devra etre arbitree ou fournie comme libelle complet.
3. La source ne fournit pas de variante `ma conjointe`; `mon conjoint` reste fixe.
4. La source couvre un apport d'une somme en numeraire ; un apport d'un bien autre qu'une somme demanderait une nouvelle spec.
5. Les valeurs par defaut de `regime_matrimonial`, `qualite_renoncee` et formes sociales devront venir d'un referentiel ou du contexte dossier.

## 12. Statut de la spec texte

`SPEC-RC-001` est complet pour ouvrir le ticket suivant :

- `CODE-RC-001 | Implémenter le batch régime communautaire v1`

Le ticket de code devra rester limite a ce batch documentaire et ne devra modifier aucun wording juridique hors variables et overlays documentes ici.
