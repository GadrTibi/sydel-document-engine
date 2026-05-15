# DAAT x SYDEL - SPEC TEXTE V1
## Batch satellites SAS

## 1. Objet

Stabiliser le texte canonique et les variantes textuelles des satellites SAS avant tout codage.

Cette spec texte complète :
- `docs/delivery/lot_05_sas_satellites_spec_canonique_v1.md`

Elle couvre uniquement :
- le PV rémunération président ;
- l'attestation sur le capital / liste des souscripteurs.

Elle ne modifie aucun wording juridique source. Les formulations ambiguës sont conservées comme constats ou transformées en points ouverts bloquants avant code.

## 2. Sources lues

Mémoire projet et référentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`
- `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`
- `docs/delivery/lot_05_spfpl_spec_texte_v1.md`
- `docs/delivery/lot_05_sas_satellites_spec_canonique_v1.md`

Source de vérité métier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Sources documentaires lues :
- `project/source_import/raw_drive_dump/Creation SAS/PV remuneration president - transforme.docx`
- `project/source_documents/lot_05/Attestation sur le capital - apport - liste des souscripteurs.docx`

ADR applicables :
- ADR-0001 : source de vérité documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : génération DOCX propre from-scratch pour les futurs tickets code ;
- ADR-0005 : mode Codex repo-first.

## 3. Périmètre texte V1

Chemin couvert :
- `SAS`, limité aux deux satellites inventoriés.

Hors périmètre :
- statuts SAS ;
- SAS générique non SPFPL ;
- PV nomination gérant ;
- documents universels ;
- plusieurs actionnaires ou souscripteurs ;
- rémunération positive, variable ou décidée selon un autre schéma.

Décision texte V1 :
- conserver la lecture actionnaire unique ;
- ne pas généraliser les formulations vers des associés multiples ;
- documenter les anomalies de placeholder ou de vocabulaire sans les corriger.

## 4. PV rémunération président

### 4.1 Structure texte source

Structure visible :
- en-tête société ;
- titre `PROCES-VERBAL DES DECISIONS DE L'ASSOCIE UNIQUE` ;
- date du PV ;
- identité de l'associé unique ;
- qualité d'associé et fonction dirigeante ;
- ordre du jour ;
- décision unique d'absence de rémunération ;
- remboursement des frais sur justificatif ;
- clôture et signature.

### 4.2 Squelette texte V1

Le squelette ci-dessous reprend la structure source en remplaçant les placeholders locaux par des rôles canoniques.

```text
{societe.denomination}
{societe.forme_juridique}
Au capital de {societe.capital_social} euros
Siège social : {societe.siege.num_voie} {societe.siege.voie}, {societe.siege.cp} {societe.siege.ville}
En cours d'immatriculation au RCS de {societe.ville_rcs}

PROCES-VERBAL DES DECISIONS
DE L'ASSOCIE UNIQUE
DU {signature.date}

{actionnaire_unique.civilite_affichage} {actionnaire_unique.prenom} {actionnaire_unique.nom}
Demeurant {actionnaire_unique.adresse_personnelle.num_voie} {actionnaire_unique.adresse_personnelle.voie}, {actionnaire_unique.adresse_personnelle.ville} {actionnaire_unique.adresse_personnelle.cp}.
{actionnaire_unique.qualite_associe} et {president.fonction} de la Société {societe.denomination} en cours de formation.

a pris la décision suivante :

Fixation de la rémunération du {president.fonction}

DECISION UNIQUE
{actionnaire_unique.civilite_affichage} {actionnaire_unique.prenom} {actionnaire_unique.nom}, {actionnaire_unique.qualite_associe}, décide qu'il ne percevra aucune rémunération au titre de son mandat de {president.fonction}, à compter de son immatriculation, et ce, jusqu'au {exercice_social.date_cloture_premier_exercice} inclus, date de la clôture du premier exercice social.

Il pourra donc prétendre au remboursement sur justification de ses frais de représentation et de déplacement.

De tout ce que dessus, l'associé unique a dressé et signé le présent procès-verbal.

Fait à {signature.lieu} en trois exemplaires

________________
{actionnaire_unique.prenom} {actionnaire_unique.nom}
```

### 4.3 Variables texte obligatoires

- `societe.denomination`
- `societe.forme_juridique`
- `societe.capital_social`
- `societe.siege.num_voie`
- `societe.siege.voie`
- `societe.siege.cp`
- `societe.siege.ville`
- `societe.ville_rcs`
- `signature.date`
- `actionnaire_unique.civilite_affichage`
- `actionnaire_unique.prenom`
- `actionnaire_unique.nom`
- `actionnaire_unique.adresse_personnelle.num_voie`
- `actionnaire_unique.adresse_personnelle.voie`
- `actionnaire_unique.adresse_personnelle.ville`
- `actionnaire_unique.adresse_personnelle.cp`
- `actionnaire_unique.qualite_associe`
- `president.fonction`
- `exercice_social.date_cloture_premier_exercice`
- `signature.lieu`

### 4.4 Blocs et limites

Blocs fixes :
- titre du PV ;
- ordre du jour unique ;
- décision unique ;
- remboursement des frais ;
- clôture.

Blocs conditionnels non automatisés en V1 :
- rémunération positive ;
- durée de non-rémunération autre que la clôture du premier exercice ;
- président non actionnaire unique ;
- plusieurs associés ;
- variation de genre autour de `qu'il`.

Règle texte :
- le futur rendu doit bloquer plutôt que corriger ou féminiser le texte sans validation.

## 5. Attestation sur le capital / liste des souscripteurs

### 5.1 Structure texte source

Structure visible :
- en-tête société ;
- titre `ATTESTATION` ;
- sous-titre `Liste des souscripteurs` ;
- attestation par le président ;
- capital social ;
- nombre d'actions et valeur nominale ;
- répartition à l'actionnaire unique ;
- apports en nature ;
- total des apports en nature ;
- apports en numéraire ;
- certification par le président ;
- lieu, date et signature.

### 5.2 Squelette texte V1

```text
{societe.denomination}
Société par actions simplifiée au capital de {societe.capital_social} euros
Société de Participations Financières de Profession Libérale de {societe.profession}
Siège social : {societe.siege.adresse_affichee}

ATTESTATION

Liste des souscripteurs

{president.civilite_affichage} {president.prenom} {president.nom} {actionnaire_unique.profession}, demeurant {actionnaire_unique.adresse_personnelle_affichee}, atteste que le capital de la société {societe.denomination} est réparti de la manière suivante :

Capital social : {societe.capital_social} euros

Nombre d'actions : {capital_souscription.nb_actions_total} actions d'un montant de {capital_souscription.valeur_nominale_action} euro chacune

Répartition : {capital_souscription.souscripteurs[0].nb_actions} actions attribuées au Dr {actionnaire_unique.prenom} {actionnaire_unique.nom}, actionnaire unique

Apports en nature :
{actionnaire_unique.civilite_affichage} {actionnaire_unique.prenom} {actionnaire_unique.nom} fait apport de {apport_titres.nb_parts} parts de la {societe_cible.forme_sociale} dénommée {societe_cible.denomination} ayant son siège {societe_cible.siege.adresse_affichee}, immatriculée au RCS de {societe_cible.ville_rcs} sous le numéro {societe_cible.numero_rcs} pour une valeur de {capital_souscription.apports_nature_montant} euros.

Total des apports en nature {capital_souscription.apports_nature_montant} euros

Apports en numéraire : {capital_souscription.apports_numeraire_montant}

Le Docteur {president.civilite_affichage} {president.prenom} {president.nom} a fait la totalité des apports en nature.

Le présent état qui constate la souscription d'actions de la société {societe.denomination}, ainsi que l'apport de la somme de {capital_souscription.apports_nature_montant} euros correspondant à la totalité du nominal desdites actions, est certifié exact, sincère et véritable par le Président, {president.civilite_affichage} {president.prenom} {president.nom}.

Fait à {signature.lieu}
Le {signature.date}

{president.civilite_affichage} {president.prenom} {president.nom}
```

### 5.3 Variables texte obligatoires

- `societe.denomination`
- `societe.capital_social`
- `societe.profession`
- `societe.siege.adresse_affichee`
- `president.civilite_affichage`
- `president.prenom`
- `president.nom`
- `actionnaire_unique.profession`
- `actionnaire_unique.adresse_personnelle_affichee`
- `capital_souscription.nb_actions_total`
- `capital_souscription.valeur_nominale_action`
- `capital_souscription.souscripteurs[0].nb_actions`
- `apport_titres.nb_parts`
- `societe_cible.forme_sociale`
- `societe_cible.denomination`
- `societe_cible.siege.adresse_affichee`
- `societe_cible.ville_rcs`
- `societe_cible.numero_rcs`
- `capital_souscription.apports_nature_montant`
- `capital_souscription.apports_numeraire_montant`
- `signature.lieu`
- `signature.date`

### 5.4 Blocs et limites

Blocs fixes :
- attestation du président ;
- liste des souscripteurs limitée à un souscripteur ;
- apports en nature ;
- apports en numéraire ;
- certification finale.

Blocs conditionnels non automatisés en V1 :
- plusieurs souscripteurs ;
- absence d'apports en nature ;
- apports uniquement en numéraire ;
- souscripteur distinct du président ;
- variation de la formule `Le Docteur`.

Règle texte :
- la future génération doit bloquer si une liste dynamique est requise ou si le dossier n'a pas d'apport en nature structuré.

## 6. Variables partagées entre les deux satellites

Variables communes :
- `societe.denomination`
- `societe.capital_social`
- `actionnaire_unique.civilite_affichage`
- `actionnaire_unique.prenom`
- `actionnaire_unique.nom`
- `president.civilite_affichage`
- `president.prenom`
- `president.nom`
- `president.fonction`
- `signature.lieu`
- `signature.date`

Variables à maintenir cohérentes avec les statuts SAS :
- `societe.forme_juridique`
- `societe.siege.*`
- `societe.ville_rcs`
- `exercice_social.date_cloture_premier_exercice`
- `capital_souscription.nb_actions_total`
- `capital_souscription.valeur_nominale_action`

## 7. Éléments manuels

Éléments qui doivent venir du contexte ou d'une saisie contrôlée :
- qualité de l'associé unique ;
- fonction dirigeante exacte ;
- date du PV ;
- lieu de signature ;
- date de clôture du premier exercice ;
- profession affichée dans l'attestation ;
- adresse personnelle complète ;
- détails de la société cible dont les parts sont apportées ;
- nombre de parts apportées ;
- montants des apports en nature et en numéraire ;
- éventuelle validation du lieu de signature issu de `[ville_siege]`.

Le moteur ne doit pas inventer ces valeurs.

## 8. Règles de blocage texte

Un futur générateur doit bloquer si :
- le dossier n'est pas `SAS` ;
- le périmètre `SAS / SPFPL medecins` n'est pas confirmé ;
- le dossier contient plusieurs actionnaires ou souscripteurs ;
- le président n'est pas l'actionnaire unique ;
- le PV doit prévoir une rémunération autre que l'absence de rémunération ;
- le PV doit gérer une présidente sans validation du wording autour de `il` et `président` ;
- l'attestation doit être produite sans apport en nature ;
- l'attestation doit produire une liste dynamique de souscripteurs ;
- les données de capital ou d'actions divergent des statuts SAS ;
- le rendu final conserverait un placeholder `[` ou `]` ;
- le rendu final corrigerait un alias ou une anomalie source sans note de validation.

## 9. Critères avant implémentation

Un ticket de code pourra démarrer seulement si :
- le ticket cible explicitement ces deux satellites ou l'un des deux ;
- les points ouverts du PV sur genre, fonction et absence de rémunération sont tranchés ou convertis en blocages explicites ;
- l'attestation est confirmée comme document unique malgré le double libellé de la source de vérité ;
- le cas `apports en nature` est confirmé pour le chemin SAS ;
- les tests futurs couvrent la cohérence capital/actions avec les statuts SAS ;
- les tests futurs vérifient l'absence de placeholders résiduels ;
- aucun wording juridique n'est modifié silencieusement.

## 10. Points ouverts

1. **Périmètre SAS / SPFPL medecins** : confirmer que les satellites suivent le même périmètre que les statuts SAS source.
2. **PV absence de rémunération** : confirmer que la V1 ne couvre que l'absence de rémunération jusqu'à la clôture du premier exercice.
3. **Genre et fonction du président** : aucune variante féminine n'est sourceée pour `qu'il` ni pour `Président`.
4. **Nombre d'exemplaires du PV** : la source fixe trois exemplaires ; confirmer que cette valeur reste fixe.
5. **Attestation en document unique** : confirmer que `Attestation sur le capital` et `liste des souscripteurs` désignent un seul fichier à générer.
6. **Apports en nature** : confirmer que le document SAS attendu contient toujours un apport de parts ; sinon une variante numéraire-only est à fournir.
7. **Liste dynamique des souscripteurs** : hors V1 tant qu'une structure textuelle multi-souscripteurs n'est pas validée.
8. **Alias valeur nominale** : la source utilise `[valeur_nominale_part]` alors que le texte parle d'actions ; aucune correction de wording sans validation.
9. **Lieu de signature de l'attestation** : confirmer si `[ville_siege]` doit être traité comme `signature.lieu`.

## 11. Statut de la spec texte

`SPEC-SAS-SATELLITES-001` stabilise la spec texte V1 des satellites SAS sans code Python.

La prochaine étape recommandée est un arbitrage métier sur les points ouverts 1, 2, 3, 5 et 6 avant tout ticket de code.
