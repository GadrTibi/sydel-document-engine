# DAAT x SYDEL — SPEC TEXTE V1
## Famille `PV nomination gérant`

## 1. Objet

Formaliser le texte canonique générateur-friendly du document `PV nomination gérant`, sans coder.

Cette spec texte complète la spec canonique :
- `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`

Elle vise à préparer un générateur déterministe qui :
- ne dépend pas de `personne_1` / `personne_2` comme vérité métier ;
- isole le texte fixe ;
- isole les blocs répétables `associes[]` ;
- isole les variantes singulier/pluriel et masculin/féminin ;
- documente les conditions et points ouverts avant implémentation.

## 2. Sources lues

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`
- `project/source_documents/lot_02/PV nomination gérant - transforme.docx`

ADR applicables :
- ADR-0001 : source de vérité documentaire
- ADR-0002 : moteur par document canonique
- ADR-0004 : génération DOCX propre from-scratch
- ADR-0005 : mode Codex repo-first

## 3. Texte source extrait du DOCX

Le modèle source contient les blocs textuels suivants :

```text
[denomination_societe]
[forme_sociale] à capital variable
Au capital minimum et effectif de [capital_social] euros
Siège social : [num_voie_siege] [voie_siege] [cp_siege] [ville_siege]
En cours d’immatriculation au RCS de [ville_rcs]
PROCES-VERBAL DES DECISIONS
 DE L’ASSEMBLEE GENERALE EXTRAORDINAIRE
 DU [date_decision]
Le [date_reunion_lettres] à [heure_reunion]
Les associés de la société civile immobilière [denomination_societe], à capital variable, au capital minimum de [capital_social] euros, divisé en [nb_parts] parts de [valeur_nominale_part] euro chacune, se sont réunis ce jour au siège de la société.
Associés présents ou représentés :
[civilite_personne_1] [prenom_personne_1] [nom_personne_1], représentant [nb_parts_personne_1] parts,
[civilite_personne_2] [prenom_personne_2] [nom_personne_2], représentant [nb_parts_personne_2] parts,
Les associés présents représentent [nb_parts] parts, soit la totalité du capital.
A l’issue de la signature des statuts, les associés se sont réunis pour prendre les décisions suivantes :
Nomination du gérant ;
Autorisation de  contracter un emprunt pour l’achat d’un bien immobilier sis [num_voie_bien] [voie_bien], [cp_bien] [ville_bien] ;
Pouvoir.
PREMIERE DECISION
L’assemblée générale extraordinaire décide de désigner en qualité de gérant pour une durée indéterminée :
[civilite_personne_2] [prenom_personne_2] [nom_personne_2], née le [date_naissance_personne_2] à [ville_naissance_personne_2] ([departement_naissance_personne_2]), de nationalité [nationalite_personne_2], demeurant [num_voie_perso_personne_2] [voie_perso_personne_2], [cp_perso_personne_2] [ville_perso_personne_2].
Cette résolution, soumise au vote est adoptée à l’unanimité des voix présentes.
DEUXIEME DECISION
L’assemblée générale extraordinaire, décide de contracter un emprunt d’un montant maximum de [montant_emprunt] euros pour l’acquisition d’un bien immobilier sis [num_voie_bien] [voie_bien], [cp_bien] [ville_bien].
Cette résolution, soumise au vote est adoptée à l’unanimité des voix présentes.
TROISIEME DECISION
L’assemblée générale extraordinaire confère tous les pouvoirs au porteur d’un original à l’effet de procéder aux formalités d’enregistrement au greffe du Tribunal de Commerce.
Cette résolution, soumise au vote est adoptée à l’unanimité des voix présentes.
De tout ce qui a été décidé, il a été dressé le présent procès-verbal qui a été signé après lecture par les associés.
L’ordre du jour étant épuisé et personne ne demandant plus la parole, la séance est levée.
Fait à [lieu_signature] en [nombre_exemplaires] exemplaires
[prenom_personne_1] [nom_personne_1]
[prenom_personne_2] [nom_personne_2]
Faire précéder la signature de la mention « Bon pour acceptation des fonctions de [fonction_dirigeant] »
```

## 4. Décisions de canonisation texte

### 4.1 Ce qui reste fixe en V1

Les formulations suivantes sont conservées comme texte fixe canonique, sauf condition explicitée plus bas :

- `PROCES-VERBAL DES DECISIONS`
- `DE L’ASSEMBLEE GENERALE EXTRAORDINAIRE`
- `DU {decision.date}`
- `Le {reunion.date_lettres} à {reunion.heure}`
- `Associés présents ou représentés :`
- `PREMIERE DECISION`
- `L’assemblée générale extraordinaire décide de désigner en qualité de {dirigeant_nomine.fonction_affichage} pour une durée indéterminée :`
- `Cette résolution, soumise au vote est adoptée à l’unanimité des voix présentes.`
- bloc pouvoirs, selon le texte source exact :
  `L’assemblée générale extraordinaire confère tous les pouvoirs au porteur d’un original à l’effet de procéder aux formalités d’enregistrement au greffe du Tribunal de Commerce.`
- `De tout ce qui a été décidé, il a été dressé le présent procès-verbal qui a été signé après lecture par les associés.`
- `L’ordre du jour étant épuisé et personne ne demandant plus la parole, la séance est levée.`
- `Faire précéder la signature de la mention « Bon pour acceptation des fonctions de {dirigeant_nomine.fonction_affichage} »`

### 4.2 Ce qui est générateur-friendly, mais à validation juridique implicite interdite

Les lignes qui contiennent dans la source un libellé trop spécifique à une SCI sont paramétrées, sans changer la fonction du bloc :

- `[forme_sociale] à capital variable` devient `{societe.forme_sociale_affichage}{societe.capital_variable_mention}`
- `Les associés de la société civile immobilière ...` devient une phrase pilotée par `{societe.forme_sociale_libelle_long}`

La généralisation est nécessaire pour la famille mutualisée, mais elle doit rester visible en revue : elle ne constitue pas une amélioration de wording juridique, seulement une extraction du libellé de forme sociale.

## 5. Structure canonique du document

### Bloc A — En-tête société

Texte canonique :

```text
{societe.denomination}
{societe.forme_sociale_affichage}{societe.capital_variable_mention}
Au capital minimum et effectif de {societe.capital_social} euros
Siège social : {societe.siege.num_voie} {societe.siege.voie} {societe.siege.cp} {societe.siege.ville}
En cours d’immatriculation au RCS de {societe.ville_rcs}
```

Règles :
- `societe.capital_variable_mention` vaut ` à capital variable` si le dossier est à capital variable.
- La ligne `Au capital minimum et effectif de ...` conserve le wording source pour la V1.
- Si une structure non capital variable doit être couverte, le wording alternatif `Au capital de ...` doit être validé avant ajout.
- La mention `En cours d’immatriculation au RCS de ...` est conservée comme V1 ; le cas d’une société déjà immatriculée reste hors V1.

### Bloc B — Titre et réunion

Texte canonique :

```text
PROCES-VERBAL DES DECISIONS
 DE L’ASSEMBLEE GENERALE EXTRAORDINAIRE
 DU {decision.date}

Le {reunion.date_lettres} à {reunion.heure}
```

Règles :
- pas de variante de titre en V1 ;
- pas de dépendance à la forme sociale en V1 ;
- `decision.date` peut être numérique ou déjà formatée, selon la future règle de formatage transverse.

### Bloc C — Introduction de l’assemblée

Texte canonique pluriel, cas source :

```text
Les associés de la {societe.forme_sociale_libelle_long} {societe.denomination}, {societe.capital_variable_formule_intro}, au capital minimum de {societe.capital_social} euros, divisé en {capital.nb_parts_total} parts de {capital.valeur_nominale_part} euro chacune, se sont réunis ce jour au siège de la société.
```

Variante singulier :

```text
L’associé de la {societe.forme_sociale_libelle_long} {societe.denomination}, {societe.capital_variable_formule_intro}, au capital minimum de {societe.capital_social} euros, divisé en {capital.nb_parts_total} parts de {capital.valeur_nominale_part} euro chacune, s’est réuni ce jour au siège de la société.
```

Règles :
- utiliser le singulier si `associes[].count == 1` ;
- utiliser le pluriel si `associes[].count >= 2` ;
- `societe.capital_variable_formule_intro` vaut `à capital variable` dans le cas source ;
- `société civile immobilière` ne doit pas être codé en dur : utiliser `societe.forme_sociale_libelle_long`.

### Bloc D — Associés présents ou représentés

Texte fixe d’ouverture :

```text
Associés présents ou représentés :
```

Bloc répétable par associé :

```text
{associe.civilite_affichage} {associe.prenom} {associe.nom}, représentant {associe.nb_parts} {parts_label}{ponctuation}
```

Règles de répétition :
- parcourir `associes[]` dans l’ordre fourni par le contexte ;
- ne jamais utiliser `personne_1` / `personne_2` comme structure d’entrée ;
- `parts_label` vaut `part` si `associe.nb_parts == 1`, sinon `parts` ;
- les lignes intermédiaires finissent par `,` ;
- la dernière ligne finit par `,` en stricte fidélité source si revue juridique le confirme ; sinon le générateur pourra utiliser `.` uniquement après décision explicite.

Phrase de synthèse pluriel :

```text
Les associés présents représentent {capital.nb_parts_representees} {parts_label}, soit la totalité du capital.
```

Phrase de synthèse singulier :

```text
L’associé présent représente {capital.nb_parts_representees} {parts_label}, soit la totalité du capital.
```

Règles :
- `capital.nb_parts_representees` est calculable comme somme des `associes[].nb_parts` présents ou représentés ;
- en V1, le texte source suppose la totalité du capital représentée ;
- si le total représenté diffère de `capital.nb_parts_total`, bloquer ou exiger une décision métier avant génération.

### Bloc E — Ordre du jour

Ouverture pluriel :

```text
A l’issue de la signature des statuts, les associés se sont réunis pour prendre les décisions suivantes :
```

Ouverture singulier :

```text
A l’issue de la signature des statuts, l’associé s’est réuni pour prendre les décisions suivantes :
```

Lignes fixes / conditionnelles :

```text
Nomination du {dirigeant_nomine.fonction_affichage} ;
{si emprunt.actif} Autorisation de  contracter un emprunt pour l’achat d’un bien immobilier sis {bien_immobilier.adresse.num_voie} {bien_immobilier.adresse.voie}, {bien_immobilier.adresse.cp} {bien_immobilier.adresse.ville} ;
Pouvoir.
```

Règles :
- conserver le double espace source dans `Autorisation de  contracter` tant qu’aucune correction juridique/typographique n’est validée ;
- générer la ligne emprunt uniquement si `emprunt.actif == true` ;
- si `emprunt.actif == false`, l’ordre du jour contient uniquement nomination et pouvoir ;
- la fonction affichée est pilotée par `dirigeant_nomine.fonction_affichage`.

### Bloc F — Première décision : nomination

Titre fixe :

```text
PREMIERE DECISION
```

Texte fixe :

```text
L’assemblée générale extraordinaire décide de désigner en qualité de {dirigeant_nomine.fonction_affichage} pour une durée indéterminée :
```

Identité du dirigeant nommé :

```text
{dirigeant_nomine.civilite_affichage} {dirigeant_nomine.prenom} {dirigeant_nomine.nom}, {ne_label} le {dirigeant_nomine.date_naissance} à {dirigeant_nomine.ville_naissance} ({dirigeant_nomine.departement_naissance}), de nationalité {dirigeant_nomine.nationalite}, demeurant {dirigeant_nomine.adresse_personnelle.num_voie} {dirigeant_nomine.adresse_personnelle.voie}, {dirigeant_nomine.adresse_personnelle.cp} {dirigeant_nomine.adresse_personnelle.ville}.
```

Formule de vote :

```text
Cette résolution, soumise au vote est adoptée à l’unanimité des voix présentes.
```

Règles :
- `ne_label` vaut `né` si `dirigeant_nomine.genre == masculin` ;
- `ne_label` vaut `née` si `dirigeant_nomine.genre == feminin` ;
- `dirigeant_nomine` peut référencer un associé, mais doit rester un rôle distinct dans l’entrée générateur ;
- ne pas déduire le dirigeant nommé de l’index `associes[1]`.

### Bloc G — Décision conditionnelle emprunt / bien immobilier

Condition :
- générer ce bloc uniquement si `emprunt.actif == true`.

Titre si le bloc est présent :

```text
DEUXIEME DECISION
```

Texte :

```text
L’assemblée générale extraordinaire, décide de contracter un emprunt d’un montant maximum de {emprunt.montant_max} euros pour l’acquisition d’un bien immobilier sis {bien_immobilier.adresse.num_voie} {bien_immobilier.adresse.voie}, {bien_immobilier.adresse.cp} {bien_immobilier.adresse.ville}.
Cette résolution, soumise au vote est adoptée à l’unanimité des voix présentes.
```

Règles :
- `emprunt.montant_max` est obligatoire si `emprunt.actif == true` ;
- les champs `bien_immobilier.adresse.*` sont obligatoires si `emprunt.actif == true` ;
- si `emprunt.actif == false`, ne pas générer ce bloc et renuméroter le bloc pouvoirs en `DEUXIEME DECISION`.

### Bloc H — Décision pouvoirs

Titre si `emprunt.actif == true` :

```text
TROISIEME DECISION
```

Titre si `emprunt.actif == false` :

```text
DEUXIEME DECISION
```

Texte fixe :

```text
L’assemblée générale extraordinaire confère tous les pouvoirs au porteur d’un original à l’effet de procéder aux formalités d’enregistrement au greffe du Tribunal de Commerce.
Cette résolution, soumise au vote est adoptée à l’unanimité des voix présentes.
```

Règles :
- le wording est conservé depuis la source ;
- seule la numérotation varie selon la présence du bloc emprunt.

### Bloc I — Clôture et signature

Texte canonique :

```text
De tout ce qui a été décidé, il a été dressé le présent procès-verbal qui a été signé après lecture par les associés.
L’ordre du jour étant épuisé et personne ne demandant plus la parole, la séance est levée.
Fait à {signature.lieu} en {signature.nombre_exemplaires} exemplaires
```

Bloc répétable signature associés :

```text
{associe.prenom} {associe.nom}
```

Mention d’acceptation :

```text
Faire précéder la signature de la mention « Bon pour acceptation des fonctions de {dirigeant_nomine.fonction_affichage} »
```

Règles :
- générer une ligne signature par item de `associes[]` ;
- ne pas limiter les signatures à deux associés ;
- si le dirigeant nommé n’est pas dans `associes[]`, ajouter une ligne de signature dirigeant uniquement après validation métier ;
- la mention d’acceptation est conservée comme texte source, en fin de document.

## 6. Variables canoniques attendues

### Société

- `societe.denomination`
- `societe.forme_sociale_affichage`
- `societe.forme_sociale_libelle_long`
- `societe.capital_social`
- `societe.capital_variable`
- `societe.capital_variable_mention`
- `societe.capital_variable_formule_intro`
- `societe.siege.num_voie`
- `societe.siege.voie`
- `societe.siege.cp`
- `societe.siege.ville`
- `societe.ville_rcs`

### Décision / réunion

- `decision.date`
- `reunion.date_lettres`
- `reunion.heure`

### Capital

- `capital.nb_parts_total`
- `capital.valeur_nominale_part`
- `capital.nb_parts_representees` calculable ou fourni

### Associés répétables

Pour chaque item `associes[]` :

- `civilite_affichage`
- `genre`
- `prenom`
- `nom`
- `nb_parts`
- `est_present_ou_represente`

### Dirigeant nommé

- `dirigeant_nomine.civilite_affichage`
- `dirigeant_nomine.genre`
- `dirigeant_nomine.prenom`
- `dirigeant_nomine.nom`
- `dirigeant_nomine.date_naissance`
- `dirigeant_nomine.ville_naissance`
- `dirigeant_nomine.departement_naissance`
- `dirigeant_nomine.nationalite`
- `dirigeant_nomine.adresse_personnelle.num_voie`
- `dirigeant_nomine.adresse_personnelle.voie`
- `dirigeant_nomine.adresse_personnelle.cp`
- `dirigeant_nomine.adresse_personnelle.ville`
- `dirigeant_nomine.fonction_affichage`
- `dirigeant_nomine.ref_associe_index` optionnel

### Emprunt / bien immobilier

- `emprunt.actif`
- `emprunt.montant_max`
- `bien_immobilier.adresse.num_voie`
- `bien_immobilier.adresse.voie`
- `bien_immobilier.adresse.cp`
- `bien_immobilier.adresse.ville`

### Signature

- `signature.lieu`
- `signature.nombre_exemplaires`

## 7. Variantes grammaticales

### Singulier / pluriel associés

| Condition | Forme |
|---|---|
| `associes[].count == 1` | `L’associé ... s’est réuni` |
| `associes[].count >= 2` | `Les associés ... se sont réunis` |
| `associes[].count == 1` | `L’associé présent représente ...` |
| `associes[].count >= 2` | `Les associés présents représentent ...` |
| `nb_parts == 1` | `part` |
| `nb_parts > 1` | `parts` |

### Masculin / féminin dirigeant nommé

| Variable | Masculin | Féminin |
|---|---|---|
| `dirigeant_nomine.genre` | `né` | `née` |
| `dirigeant_nomine.fonction_affichage` | `gérant` | `gérante`, si validation métier |

Décision V1 :
- le texte source affiche `gérant` au masculin ;
- le générateur doit techniquement accepter `dirigeant_nomine.fonction_affichage` ;
- la féminisation automatique `gérant/gérante` doit être testable, mais son activation documentaire reste un point de validation métier si la revue exige l’identité stricte avec la source.

## 8. Conditions et branches documentaires

### 8.1 Branche capital variable

V1 source :
- société à capital variable ;
- capital minimum et effectif ;
- introduction avec `à capital variable`.

Condition :
- `societe.capital_variable == true` ou champs d’affichage déjà fournis.

Hors V1 :
- wording non capital variable.

### 8.2 Branche emprunt

Condition :
- `emprunt.actif == true`

Effets :
- ajoute une ligne à l’ordre du jour ;
- ajoute la décision emprunt ;
- impose les champs `emprunt` et `bien_immobilier` ;
- le bloc pouvoirs devient `TROISIEME DECISION`.

Si `emprunt.actif == false` :
- la ligne d’ordre du jour emprunt est absente ;
- la décision emprunt est absente ;
- le bloc pouvoirs devient `DEUXIEME DECISION`.

### 8.3 Branche associés dynamiques

Condition :
- `len(associes[]) >= 1`

Effets :
- liste des associés générée par répétition ;
- signatures générées par répétition ;
- synthèse des parts recalculée ou validée ;
- variantes singulier/pluriel appliquées.

### 8.4 Branche dirigeant distinct des associés

V1 :
- le dirigeant nommé est un rôle distinct ;
- il peut être lié à un associé via `dirigeant_nomine.ref_associe_index`.

Si le dirigeant n’est pas associé :
- la nomination peut être générée ;
- la signature et la mention d’acceptation nécessitent une validation métier pour savoir si une signature dirigeant séparée est attendue.

## 9. Mapping source vers canonique pour le texte

| Placeholder source | Variable canonique texte |
|---|---|
| `[denomination_societe]` | `societe.denomination` |
| `[forme_sociale]` | `societe.forme_sociale_affichage` |
| `[capital_social]` | `societe.capital_social` |
| `[num_voie_siege]` | `societe.siege.num_voie` |
| `[voie_siege]` | `societe.siege.voie` |
| `[cp_siege]` | `societe.siege.cp` |
| `[ville_siege]` | `societe.siege.ville` |
| `[ville_rcs]` | `societe.ville_rcs` |
| `[date_decision]` | `decision.date` |
| `[date_reunion_lettres]` | `reunion.date_lettres` |
| `[heure_reunion]` | `reunion.heure` |
| `[nb_parts]` | `capital.nb_parts_total` ou `capital.nb_parts_representees` selon la phrase |
| `[valeur_nominale_part]` | `capital.valeur_nominale_part` |
| `[civilite_personne_1]` | `associes[0].civilite_affichage` uniquement comme remapping source |
| `[prenom_personne_1]` | `associes[0].prenom` uniquement comme remapping source |
| `[nom_personne_1]` | `associes[0].nom` uniquement comme remapping source |
| `[nb_parts_personne_1]` | `associes[0].nb_parts` uniquement comme remapping source |
| `[civilite_personne_2]` | `associes[1].civilite_affichage` pour la liste, `dirigeant_nomine.civilite_affichage` pour la nomination |
| `[prenom_personne_2]` | `associes[1].prenom` pour la liste/signature, `dirigeant_nomine.prenom` pour la nomination |
| `[nom_personne_2]` | `associes[1].nom` pour la liste/signature, `dirigeant_nomine.nom` pour la nomination |
| `[nb_parts_personne_2]` | `associes[1].nb_parts` uniquement comme remapping source |
| `[date_naissance_personne_2]` | `dirigeant_nomine.date_naissance` |
| `[ville_naissance_personne_2]` | `dirigeant_nomine.ville_naissance` |
| `[departement_naissance_personne_2]` | `dirigeant_nomine.departement_naissance` |
| `[nationalite_personne_2]` | `dirigeant_nomine.nationalite` |
| `[num_voie_perso_personne_2]` | `dirigeant_nomine.adresse_personnelle.num_voie` |
| `[voie_perso_personne_2]` | `dirigeant_nomine.adresse_personnelle.voie` |
| `[cp_perso_personne_2]` | `dirigeant_nomine.adresse_personnelle.cp` |
| `[ville_perso_personne_2]` | `dirigeant_nomine.adresse_personnelle.ville` |
| `[montant_emprunt]` | `emprunt.montant_max` |
| `[num_voie_bien]` | `bien_immobilier.adresse.num_voie` |
| `[voie_bien]` | `bien_immobilier.adresse.voie` |
| `[cp_bien]` | `bien_immobilier.adresse.cp` |
| `[ville_bien]` | `bien_immobilier.adresse.ville` |
| `[lieu_signature]` | `signature.lieu` |
| `[nombre_exemplaires]` | `signature.nombre_exemplaires` |
| `[fonction_dirigeant]` | `dirigeant_nomine.fonction_affichage` |

## 10. Critères avant implémentation

Le ticket de code pourra démarrer si :
- le générateur n’accepte pas `personne_1` / `personne_2` comme modèle d’entrée ;
- `associes[]` est répétable et testé avec 1, 2 et 3 associés ;
- `dirigeant_nomine` est distinct de `associes[]` ;
- les variantes `né` / `née` sont testées ;
- la branche `emprunt.actif == true` est testée ;
- la branche `emprunt.actif == false` est testée avec renumérotation du bloc pouvoirs ;
- aucune formulation juridique n’est modifiée hors templates ci-dessus ;
- les cas de total de parts incohérent bloquent la génération.

## 11. Points ouverts restants

Points ouverts non bloquants pour préparer le code, mais à garder visibles en revue :

1. SELAS : le référentiel rattache la famille à SELAS, mais la fonction `gérant` peut nécessiter validation métier selon la structure.
2. Capital non variable : aucun wording source reçu pour une société non capital variable.
3. Société déjà immatriculée : la source dit `En cours d’immatriculation`; aucun wording alternatif n’est validé.
4. Dirigeant non associé : la signature finale séparée du dirigeant n’est pas explicitement couverte par la source.
5. Ponctuation de la dernière ligne `associes[]` : la source termine chaque associé par une virgule ; ne pas corriger sans validation.
6. Féminisation `gérante` : techniquement prévue via `dirigeant_nomine.fonction_affichage`, mais à valider juridiquement si elle diffère du wording source.
7. `euro` / `euros` pour `capital.valeur_nominale_part` : la source utilise `euro chacune`; prévoir une règle seulement si une valeur différente de 1 est attendue.

## 12. Statut de la spec texte

`SPEC-TEXTE-PV-001` est complète pour ouvrir le ticket suivant :

- `CODE-PV-001 | Implémenter le générateur canonique PV nomination gérant`

Le ticket de code devra rester limité à cette famille documentaire et ne devra pas modifier les autres documents métier.
