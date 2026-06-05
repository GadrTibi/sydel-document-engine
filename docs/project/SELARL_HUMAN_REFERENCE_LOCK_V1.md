# SELARL human reference lock V1

Ticket : `TRACK-B-SELARL-HUMAN-REFERENCE-LOCK-002`

Source humaine prioritaire : `C:\Users\Gad\Downloads\Retours humains .docx`, fourni par l'utilisateur le 31/05/2026.

Ce document verrouille les corrections humaines explicites à reprendre pour le premier pack SELARL de production. Quand le texte humain fournit une formulation exacte, le générateur doit s'en rapprocher au plus près et ne pas reformuler librement.

## Documents verrouillés

### Autorisation de domiciliation

Correction humaine :

> dans les locaux du cabinet au [num_voie_siege] [voie_siege], [cp_siege] [ville_siege] pour une durée indéterminée.

Correction 2026-06-05 (retour à la source primaire) :

- l'amendement du 2026-06-03 (`pour 99 ans`) était **ERRONÉ** : il contredisait la source humaine
  primaire `Retours humains .docx` (31/05), qui dit explicitement « …[ville_siege] **pour une durée
  indéterminée**. » pour l'autorisation de domiciliation.
- la domiciliation est donc rétablie à **« pour une durée indéterminée »** (`DOC-002`).
- ⚠️ Ne pas confondre : le « 99 ans » concerne la **DURÉE DE LA SOCIÉTÉ** (statuts art. 6, figée en dur
  d'après le retour 006), **pas** la domiciliation.

Mapping moteur :

- `[num_voie_siege]` : `societe.siege.num_voie`
- `[voie_siege]` : `societe.siege.voie`
- `[cp_siege]` : `societe.siege.cp`
- `[ville_siege]` : `societe.siege.ville`

Règle de dérivation :

- l'adresse libre de domiciliation ne pilote plus cette phrase ;
- l'adresse utilisée est celle du siège/cabinet de la société.

### Déclaration de non-condamnation

Correction humaine :

> demeurant au [num_voie_perso] [voie_perso], [cp_perso] [ville_perso]

Mapping moteur :

- `[num_voie_perso]` : `personne_signataire.adresse_perso.num_voie`
- `[voie_perso]` : `personne_signataire.adresse_perso.voie`
- `[cp_perso]` : `personne_signataire.adresse_perso.cp`
- `[ville_perso]` : `personne_signataire.adresse_perso.ville`

Règle de dérivation :

- l'adresse personnelle se compose toujours avec virgule avant le code postal : `num voie, cp ville`.

### Lettre de renonciation à revendiquer la qualité d'associé

Corrections humaines :

- remplacer `A {ville}` par `À {ville}` ;
- remplacer `euros dépendant de notre regime de communaute` par `euros dépendant de notre communauté` ;
- supprimer tout texte parasite `RCS PARIS 788 531 432 0153814303` ;
- ajouter `Fait pour servir et valoir ce que de droit.` avant le bloc de signature.

Mapping moteur :

- `regime_communautaire.regime_matrimonial` est normalisé en `communauté` dès qu'il contient une forme de `communaute` ;
- `regime_communautaire.renonciation.lieu_signature` pilote `À {ville}` ;
- `regime_communautaire.renonciation.date_signature` pilote la date ;
- `regime_communautaire.renonciation.nombre_exemplaires_lettres` pilote le nombre d'exemplaires.

Point de vigilance :

- le retour humain rattache aussi l'ajout après `L'exécution de ce mandat vaudra décharge au mandataire.` ; le ticket `TRACK-B-SELARL-DENTIST-LINE-BY-LINE-LOCK-003` a confirmé que ce point vise la procuration `DOC-003`, où la correction est désormais appliquée.

### Procuration

Corrections humaines confirmées par le ticket `TRACK-B-SELARL-DENTIST-LINE-BY-LINE-LOCK-003` :

- supprimer les lignes parasites `RCS PARIS 788 531 432` et `0153814303` du bloc mandataire ;
- ajouter `Fait pour servir et valoir ce que de droit.` juste après `L'exécution de ce mandat vaudra décharge au mandataire.` et avant le bloc de signature.

### PV de nomination de gérant

Corrections humaines intégrées :

- supprimer `RCS de Lyon` / `RCS de {ville}` dans l'en-tête ;
- supprimer `EXTRAORDINAIRE` dans le titre et les décisions ;
- supprimer l'heure de réunion dans ce document ;
- remplacer l'introduction par une formulation centrée sur la SELARL, le capital, le nombre de parts et la valeur nominale ;
- remplacer `Associés présents ou représentés :` par `Sont présents ou représentés :` ;
- remplacer `représentant` par `détenant` dans la liste des associés ;
- remplacer le bloc de quorum et d'ordre du jour par :
  `Les associés présents ou représentés disposent ensemble de la totalité des parts sociales. Cet ensemble est habilité à prendre des décisions.`
- ajouter le président de séance sous la forme :
  `[civilite_president_seance] [prenom_president_seance] [nom_personne_seance] préside la séance.`
- ajouter `Le président rappelle l'ordre du jour :` puis les lignes d'ordre du jour ;
- gérer `Nomination du gérant` si l'associé est unique, et `Nomination des premiers gérants` en pluralité ;
- ajouter `au` après `demeurant` ;
- remplacer la formule de vote par `Cette résolution est adoptée à l'unanimité` ;
- remplacer le bloc pouvoirs par :
  `L'assemblée générale confère tous les pouvoirs au porteur d'un original à l'effet de procéder aux formalités d'enregistrement au greffe du Tribunal de Commerce de la Société.`
- supprimer les deux phrases finales relatives au procès-verbal dressé et à la séance levée.

Variables nouvelles :

- `civilite_president_seance`
- `prenom_president_seance`
- `nom_personne_seance`

Mapping moteur :

- `DocumentGenerationContext.reunion.president.civilite_president_seance`
- `DocumentGenerationContext.reunion.president.prenom_president_seance`
- `DocumentGenerationContext.reunion.president.nom_personne_seance`

Règle de dérivation front/data :

- dans la slice clean Track B SELARL, le président de séance est prérempli à partir de l'associé unique/praticien déjà saisi ;
- aucune ressaisie n'est demandée dans le front V1 ;
- le moteur conserve la capacité d'utiliser un président explicitement fourni si le contexte le renseigne.

### Statuts SELARL chirurgien-dentiste

Corrections minimales verrouillées :

- afficher `Au capital de [capital_social] euros` ;
- rendre la situation maritale communautaire sous la forme `marié sous le régime de la communauté...` ou accord féminin équivalent ;
- corriger l'ARTICLE 5 avec le lieu d'exercice unique ;
- corriger les ARTICLES 7 et 8 sur apports et capital social ;
- conserver l'ARTICLE 34 de signature électronique avec la variable `[prestataire_signature_electronique]`.

Mappings principaux :

- `[denomination_societe]` : `societe.denomination`
- `[capital_social]` : `societe.capital_social` ou `capital.montant`
- `[capital_lettres]` : `societe.capital_social_lettres` ou `capital.montant_lettres`
- `[nb_parts_total]` : `capital.nombre_titres_total` ou `capital.nb_parts_total`
- `[nb_parts_total_lettres]` : `capital.nombre_titres_total_lettres`
- `[valeur_nominale_part]` : `capital.valeur_nominale_titre` ou `capital.valeur_nominale_part`
- `[montant_apport]` : `associes[0].apport_numeraire` ou `apport.montant`
- `[montant_apport_lettres]` : `associes[0].apport_numeraire_lettres` ou `apport.montant_lettres`
- `[adresse_lieu_exercice]` : `exercice_social.lieux[0].adresse_affichee`
- `[nom_banque]` : `depot_fonds.banque.nom`
- `[prestataire_signature_electronique]` : `signature.prestataire_signature_electronique`

Règles de dérivation :

- le bloc de capital humain fixe `Monsieur` et `mille / 1000` dans l'exemple ; le générateur mappe ces valeurs sur la civilité réelle et les variables de parts pour ne pas figer un dossier particulier ;
- la formulation `sous le régime de la communauté légale` est dérivée dès que le régime contient `communaute` et `legale`.

## Points ouverts

- Le retour `RCS PARIS 788 531 432 0153814303` et la phrase `L'exécution de ce mandat vaudra décharge au mandataire.` ne visaient pas la renonciation mais la procuration `DOC-003`; l'écart est fermé dans `TRACK-B-SELARL-DENTIST-LINE-BY-LINE-LOCK-003`.
- Les statuts SELARL chirurgien-dentiste multi-associés restent hors V1 moteur/front ; le pack actuel verrouille le cas associé unique.
- Le front Track B SELARL rattache automatiquement l'associé unique comme président de séance ; la sélection explicite d'un président parmi plusieurs associés n'est pas exposée tant que le front SELARL reste borné à l'unipersonnel.
