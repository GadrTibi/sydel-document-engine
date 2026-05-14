# DAAT x SYDEL - SPEC TEXTE V1
## Batch SPFPL specifique

## 1. Objet

Stabiliser le texte canonique et les variantes textuelles du batch SPFPL specifique, sans coder.

Cette spec texte complete :
- `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`

Elle vise a preparer de futurs generateurs deterministes pour :
- la note d'information ;
- les PV d'agrement de cession SPFPL, variante associe unique et variante plusieurs associes ;
- l'acte de cession de parts ;
- le contrat d'apport SEL vers SPFPL ;
- l'attestation sur le capital / liste des souscripteurs ;
- l'acte de designation d'un commissaire aux apports.

Cette spec ne modifie aucun wording juridique source. Les formulations ambigues sont conservees comme constats ou transformees en points ouverts bloquants avant code.

## 2. Sources lues

Memoire projet et referentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : generation DOCX propre from-scratch pour les futurs tickets code ;
- ADR-0005 : mode Codex repo-first.

Constat de placement :
- `project/source_documents/lot_05/` ne contient pas les sources DOCX attendues ;
- les sources SPFPL ci-dessous ont donc ete lues dans `project/source_import/raw_drive_dump/`.

Sources SPFPL lues :
- `project/source_import/raw_drive_dump/Creation SPFPL/NOTE D_INFORMATION.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession spfpl/PV agrement cession/PV SELARL agrement cession SPFPL - SELARL plusieurs associes - transforme.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession spfpl/PV agrement cession/PV SELARL agrement cession SPFPL - SELARL 1 associe.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/cession spfpl/Cession/Acte_cession_SPFPL_tiers_part_modele.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/apport/apport doc/Contrat d_apport SEL SPFPL.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/apport/apport doc/Attestation sur le capital - apport - liste des souscripteurs.docx`
- `project/source_import/raw_drive_dump/Creation SPFPL/apport/apport doc/attestation nomination commissaire aux apports - transforme.docx`

Notes de source :
- la source de verite mentionne `PV SELARL agrement cession SPFPL - SELARL 1 associe - transforme.docx`, mais le fichier disponible et lu ne porte pas le suffixe `- transforme` ;
- la source de verite mentionne `Attestation nomination comm. aux comptes`, mais la source disponible concerne un commissaire aux apports ;
- la note d'information contient une double formule cession/apport ;
- les PV classes cote cession emploient le vocabulaire de l'apport.

## 3. Perimetre texte V1

Chemins couverts :
- `SPFPL_CESSION` pour note d'information, PV d'agrement et acte de cession de parts ;
- `SPFPL_APPORT` pour note d'information, contrat d'apport, attestation capital / liste des souscripteurs et commissaire aux apports.

Hors perimetre de cette spec texte :
- documents universels deja couverts par les lots transverses ;
- statuts SPFPL ;
- PV nomination gerant ;
- demande d'inscription a l'ordre ;
- batch regime communautaire ;
- acte de cession d'actions, faute de source DOCX confirmee.

## 4. Note d'information

### 4.1 Structure texte source

Structure visible :
- titre `Note d'informations` ;
- bloc `Constitution de la Societe` ;
- denomination de la SPFPL ;
- paragraphe de presentation de la SPFPL en cours de constitution ;
- paragraphe sur l'acquisition ou l'apport des titres de la societe cible ;
- decomposition du capital apres operation ;
- signature du dirigeant de la SPFPL.

### 4.2 Texte canonique V1

Le texte V1 doit etre traite comme un tronc commun a deux variantes, mais le wording cession/apport n'est pas tranche.

Squelette commun :

```text
Note d'informations

Constitution de la Societe

{societe_spfpl.denomination}

La {societe_spfpl.denomination}, en cours de constitution, dont le siege est situe {societe_spfpl.siege.adresse_affichee}, au capital de {societe_spfpl.capital_social}, prevoit {note_information.operation_phrase}, des son immatriculation, {operation_titres.nb_titres} parts de la {societe_cible.denomination}, {societe_cible.forme_sociale} de {societe_cible.profession_reglementee} au capital de {societe_cible.capital_social} divise en {societe_cible.nb_parts_total} parts, dont le siege social est situe {societe_cible.siege.adresse_affichee}, immatriculee au RCS de {societe_cible.ville_rcs} sous le numero {societe_cible.numero_rcs}.

Apres ladite {note_information.operation_nom}, le capital de la {societe_cible.denomination} sera decompose comme suit :
{societe_cible.repartition_capital_apres_operation}

{apporteur_ou_cedant.prenom} {apporteur_ou_cedant.nom}
{societe_spfpl.dirigeant.fonction} de la {societe_spfpl.denomination}
```

Decision texte V1 :
- ne pas rendre automatiquement la double formule source `acquerir/de recevoir en apport en nature` ;
- `note_information.operation_phrase` et `note_information.operation_nom` doivent etre fournis par arbitrage ou configuration validee ;
- si l'arbitrage n'est pas disponible, le futur generateur doit bloquer.

### 4.3 Variables propres

- `note_information.operation_phrase`
- `note_information.operation_nom`
- `operation_titres.nb_titres`
- `societe_cible.repartition_capital_apres_operation`

## 5. Agrement cession

### 5.1 Variantes

Deux variantes sourcees :
- associe unique : `PROCES-VERBAL DE L'ASSOCIE UNIQUE` ;
- plusieurs associes : `PROCES-VERBAL DE L'ASSEMBLEE GENERALE EXTRAORDINAIRE`.

Regle de selection future :
- `dossier.options.associe_unique == true` : variante associe unique ;
- `dossier.options.associe_unique == false` : variante plusieurs associes.

### 5.2 Tronc commun d'en-tete

Squelette commun :

```text
{societe_cible.denomination}
{societe_cible.forme_sociale}
Au capital de {societe_cible.capital_social} euros
Siege social : {societe_cible.siege.num_voie} {societe_cible.siege.voie}, {societe_cible.siege.cp} {societe_cible.siege.ville}
Immatriculee au RCS de {societe_cible.ville_rcs} sous le n {societe_cible.numero_rcs}
```

### 5.3 Variante associe unique

Structure texte :
- en-tete societe cible ;
- titre `PROCES-VERBAL DE L'ASSOCIE UNIQUE` ;
- date de PV ;
- rappel de l'associe unique ;
- ordre du jour ;
- trois resolutions ;
- signature de l'associe unique.

Squelette :

```text
PROCES-VERBAL DE
L'ASSOCIE UNIQUE
DU {reunion.date_pv}

L'an {reunion.annee_pv_lettres},
Le {reunion.date_reunion_lettres}, a {reunion.heure_reunion},
{apporteur_ou_cedant.civilite_affichage} {apporteur_ou_cedant.prenom} {apporteur_ou_cedant.nom}, associe unique de la Societe {societe_cible.denomination}, au capital de {societe_cible.capital_social} euros, compose de {societe_cible.nb_parts_total} parts, a pris les decisions suivantes :

Agrement d'un nouvel associe, la {societe_spfpl.denomination} ;
Modification correlative des statuts ;
Pouvoirs pour l'accomplissement des formalites.

PREMIERE RESOLUTION
{pv_agrement.resolution_agrement}

DEUXIEME RESOLUTION
{pv_agrement.article_7_bis_apres_operation}

TROISIEME RESOLUTION
L'associe unique donne tous pouvoirs au porteur de copies ou d'extraits du present proces-verbal pour remplir toutes formalites de droit.

{apporteur_ou_cedant.prenom} {apporteur_ou_cedant.nom}
```

### 5.4 Variante plusieurs associes

Structure texte :
- en-tete societe cible ;
- titre AGE ;
- convocation et reunion ;
- liste des associes presents ou representes ;
- depot des documents ;
- ordre du jour ;
- trois resolutions ;
- signatures de tous les associes.

Squelette :

```text
PROCES-VERBAL DE
L'ASSEMBLEE GENERALE EXTRAORDINAIRE
DU {reunion.date_pv}

L'an {reunion.annee_pv_lettres},
Le {reunion.date_reunion_lettres}, a {reunion.heure_reunion},
Les associes de la Societe {societe_cible.denomination}, au capital de {societe_cible.capital_social} euros, compose de {societe_cible.nb_parts_total} parts, se sont reunis sur convocation reguliere de la gerance au siege de la Societe.

Sont presents ou representes :
{associes_cible.liste_presence}

Les associes presents ou representes disposent ensemble de la totalite des parts formant le capital de la societe. L'assemblee est habilitee a prendre les decisions extraordinaires.

{reunion.president.civilite_affichage} {reunion.president.prenom} {reunion.president.nom} preside la seance en qualite de {reunion.president.qualite}.

PREMIERE RESOLUTION
{pv_agrement.resolution_agrement}

DEUXIEME RESOLUTION
{pv_agrement.article_7_bis_apres_operation}

TROISIEME RESOLUTION
L'assemblee generale donne tous pouvoirs au porteur de copies ou d'extraits du present proces-verbal pour remplir toutes formalites de droit.

{associes_cible.signatures}
```

### 5.5 Wording bloque avant code

Les deux sources de PV emploient les formulations :
- `contrat d'apport` ;
- `autorise l'apport` ;
- `parts apportees`.

Ces formulations contredisent le classement `agrement cession` de la source de verite. La V1 ne corrige pas ce wording. Un futur ticket code doit bloquer tant que l'arbitrage `cession` versus `apport` n'est pas donne explicitement.

### 5.6 Variables propres

- `pv_agrement.resolution_agrement`
- `pv_agrement.article_7_bis_apres_operation`
- `associes_cible.liste_presence`
- `associes_cible.signatures`
- `reunion.president.*`

## 6. Acte de cession de parts

### 6.1 Structure texte source

Structure visible :
- titre `Cession de parts` ;
- comparution du cedant ;
- comparution de la SPFPL cessionnaire ;
- expose relatif a la societe cible ;
- repartition du capital actuel ;
- origine de propriete ;
- objet du contrat ;
- nantissement / pacte / agrement ;
- propriete et jouissance ;
- prix et modalites de paiement ;
- declarations des parties ;
- garantie d'actif et de passif ;
- clauses generales ;
- signification de la cession ;
- declaration pour l'enregistrement ;
- pouvoirs ;
- communication au Conseil de l'Ordre ;
- frais ;
- affirmation de sincerite ;
- loi applicable ;
- signature electronique ;
- signatures.

### 6.2 Texte canonique V1

L'acte de cession de parts est le document le plus directement exploitable du sous-batch cession, sous reserve de rendre dynamiques les listes de repartition.

Squelette de tete :

```text
Cession de parts

ENTRE
{cedant.civilite_affichage} {cedant.prenom} {cedant.nom}

ET
La Societe {societe_spfpl.denomination}

ENTRE LES SOUSSIGNES :
{cedant.identite_complete}
Inscrit au Tableau de l'ordre departemental des {cedant.profession_reglementee_pluriel} du {cedant.ordre.departemental} sous le numero RPPS {cedant.ordre.numero_rpps}.

Ci-apres denomme "LE CEDANT",

ET
La Societe {societe_spfpl.denomination}
{societe_spfpl.forme_sociale}
Au capital de {societe_spfpl.capital_social}
Immatriculee au RCS de {societe_spfpl.ville_rcs} sous le numero {societe_spfpl.numero_rcs}
Siege social : {societe_spfpl.siege.adresse_affichee}
Representee aux presentes par {societe_spfpl.representant.identite_qualite}.

Ci-apres denommee "LE CESSIONNAIRE",
```

Squelette operation :

```text
Le capital social est reparti a ce jour comme suit :
{societe_cible.repartition_capital_avant_operation}

Par les presentes, le Cedant cede ce jour, sous les garanties ordinaires de fait et de droit en la matiere, ainsi que celles consenties dans les presentes, a l'Acquereur, qui accepte, la pleine propriete de {cession_parts.nb_parts_lettres} ({cession_parts.nb_parts}) parts qu'il detient.

La cession a lieu moyennant le prix de {cession_parts.prix_unitaire_lettres} ({cession_parts.prix_unitaire}) euro par part cedee, soit un prix de {cession_parts.prix_total} euros ({cession_parts.prix_total_lettres}), a payer par la Societe {societe_spfpl.denomination}.
```

Squelette signature :

```text
Fait a {signature.lieu}
Le {signature.date}
En {cession_parts.nombre_exemplaires_lettres} exemplaires originaux,

Dr {cedant.prenom} {cedant.nom}
La societe {societe_spfpl.denomination}
Representee par {societe_spfpl.representant.civilite_courte} {societe_spfpl.representant.prenom} {societe_spfpl.representant.nom}
```

### 6.3 Points de fidelite

- le document source est un acte de cession de parts, pas un acte de cession d'actions ;
- la repartition du capital source est fixee sur trois personnes et doit devenir `associes_cible[]` avant code ;
- le bloc frais contient la formule `cession d'action` dans une source de cession de parts : aucune correction automatique n'est autorisee sans validation.

## 7. Apport

### 7.1 Structure texte source

Le contrat d'apport contient :
- titre `Contrat d'apport` ;
- identification de l'apporteur ;
- identification de la SPFPL beneficiaire ;
- expose de l'operation ;
- biens apportes ;
- evaluation de l'apport ;
- remuneration de l'apport ;
- option pour le report d'imposition ;
- conditions suspensives ;
- affirmation de sincerite ;
- frais ;
- election de domicile ;
- date d'effet ;
- convention sur la preuve / signature electronique ;
- signatures.

### 7.2 Texte canonique V1

Squelette de tete :

```text
Contrat d'apport

Entre les soussignes :
- {apporteur.civilite_affichage} {apporteur.prenom} {apporteur.nom}
{apporteur.profession_reglementee} de profession
Ne le {apporteur.date_naissance} a {apporteur.ville_naissance} ({apporteur.departement_naissance})
Demeurant {apporteur.adresse_personnelle_affichee}
{apporteur.situation_maritale} avec {apporteur.conjoint.nom}
De nationalite {apporteur.nationalite}
Inscrit au tableau de l'{apporteur.ordre.professionnel} de {apporteur.ordre.departement} sous le n {apporteur.ordre.numero} et sous le numero RPPS {apporteur.ordre.numero_rpps}

Ci-apres designe "l'apporteur" ou le soussigne de premiere part

{societe_spfpl.denomination}
{societe_spfpl.forme_sociale} au capital de {societe_spfpl.capital_social} euros
Societe de {societe_spfpl.activite}
Siege social : {societe_spfpl.siege.adresse_affichee}
En cours d'immatriculation au RCS de {societe_spfpl.ville_rcs}
Representee par son {societe_spfpl.dirigeant.fonction}, {apporteur.civilite_affichage} {apporteur.prenom} {apporteur.nom}, domicilie en cette qualite audit siege.

Ci-apres designee "la societe beneficiaire"
```

Squelette operation :

```text
Les Parties ont decide que {apporteur.civilite_affichage} {apporteur.prenom} {apporteur.nom} apporte a la {societe_spfpl.denomination} {apport_titres.nb_parts} {apport_titres.nature_titres} de la {societe_cible.denomination}, {societe_cible.forme_sociale}, au capital de {societe_cible.capital_social} euros dont le siege social est situe au {societe_cible.siege.adresse_affichee}, immatriculee au RCS de {societe_cible.ville_rcs} sous le n {societe_cible.numero_rcs}.

L'apport est indivisible et porte obligatoirement sur la pleine et entiere propriete de {apport_titres.nb_parts} parts sociales de la Societe Apportee numerotees de {apport_titres.plage_parts}.

Le montant de l'apport est estime a {apport_titres.valeur_par_titre_lettres} euros ({apport_titres.valeur_par_titre} euros) par part, soit le prix global de {apport_titres.valeur_globale_lettres} euros ({apport_titres.valeur_globale} euros).

En contrepartie de l'apport, il est attribue a l'apporteur {apport_titres.nb_actions_attribuees_lettres} ({apport_titres.nb_actions_attribuees}) actions nouvelles d'une valeur nominale de {apport_titres.valeur_nominale_action_lettres} euro chacune.
```

### 7.3 Evaluateur et commissaire

La source nommee contient des entites fixes pour :
- l'evaluation de l'apport ;
- le commissaire aux apports.

Decision texte V1 :
- ne pas hard-coder ces entites dans un futur generateur ;
- `evaluateur_apport.*` et `commissaire_aux_apports.*` doivent venir du contexte, d'un referentiel valide ou d'un arbitrage explicite ;
- si le ticket code choisit de reprendre les entites fixes de la source, ce choix doit etre documente comme validation metier.

## 8. Attestation capital / liste des souscripteurs

### 8.1 Structure texte source

Structure visible :
- en-tete SPFPL ;
- titre `ATTESTATION` ;
- sous-titre `Liste des souscripteurs` ;
- attestation du president ;
- capital social ;
- nombre d'actions et valeur nominale ;
- repartition ;
- apports en nature ;
- total des apports en nature ;
- apports en numeraire ;
- certification par le president ;
- signature.

### 8.2 Texte canonique V1

Squelette :

```text
{societe_spfpl.denomination}
Societe par actions simplifiee au capital de {societe_spfpl.capital_social} euros
Societe de Participations Financieres de Profession Liberale de {societe_spfpl.profession}
Siege social : {societe_spfpl.siege.adresse_affichee}

ATTESTATION

Liste des souscripteurs

{capital_souscription.president.identite_qualite}, demeurant {capital_souscription.president.adresse_personnelle_affichee}, atteste que le capital de la societe {societe_spfpl.denomination} est reparti de la maniere suivante :

Capital social : {societe_spfpl.capital_social} euros
Nombre d'actions : {capital_souscription.nb_actions_total} actions d'un montant d'{capital_souscription.valeur_nominale_action} euro chacune
Repartition :
{capital_souscription.repartition_actions}

Apports en nature :
{apporteur.identite_courte} fait apport de {apport_titres.nb_parts} parts de la {societe_cible.forme_sociale} denommee {societe_cible.denomination} ayant son siege {societe_cible.siege.adresse_affichee}, immatriculee au RCS de {societe_cible.ville_rcs} sous le numero {societe_cible.numero_rcs} pour une valeur de {capital_souscription.apports_nature_montant} euros.

Total des apports en nature {capital_souscription.apports_nature_montant} euros
Apports en numeraire : {capital_souscription.apports_numeraire_montant}

Le present etat est certifie exact, sincere et veritable par le President, {capital_souscription.president.identite_courte}.

Fait a {signature.lieu}
Le {signature.date}
{capital_souscription.president.identite_courte}
```

### 8.3 Point liste dynamique

La source V1 est centree sur un actionnaire unique :
- `actionnaire unique` ;
- `la totalite des apports en nature`.

Un futur generateur doit bloquer si plusieurs souscripteurs sont demandes sans arbitrage sur :
- la forme de `capital_souscription.repartition_actions` ;
- la certification finale ;
- les accords singulier/pluriel.

## 9. Commissaire aux apports

### 9.1 Structure texte source

Structure visible :
- adresse de la personne principale ;
- titre `Acte de designation d'un commissaire aux apports` ;
- identification du soussigne ;
- rappel de la constitution de la SPFPL ;
- description de l'apport en nature ;
- nomination du commissaire ;
- mission ;
- signature.

### 9.2 Texte canonique V1

Squelette :

```text
{apporteur.prenom} {apporteur.nom}
{apporteur.adresse_personnelle_affichee}

Acte de designation d'un commissaire aux apports

Le soussigne, {apporteur.civilite_affichage} {apporteur.prenom} {apporteur.nom}, ne le {apporteur.date_naissance} a {apporteur.ville_naissance} ({apporteur.departement_naissance}), {apporteur.profession_reglementee}, de nationalite {apporteur.nationalite}, demeurant {apporteur.adresse_personnelle_affichee}, {apporteur.situation_maritale} avec {apporteur.conjoint.nom}

seul futur associe de la societe {societe_spfpl.denomination} {societe_spfpl.forme_sociale} de {societe_spfpl.profession} en cours de formation,

a prealablement expose et rappele ce qui suit :

Le soussigne a decide de constituer une societe de {societe_spfpl.activite} moyennant l'apport suivant :
- {apport_titres.nb_parts} parts de la {societe_cible.forme_sociale} denommee "{societe_cible.denomination}", ayant son siege {societe_cible.siege.adresse_affichee}, immatriculee au RCS de {societe_cible.ville_rcs} sous le n {societe_cible.numero_rcs}.

Aux fins de realisation de cet apport en nature a ladite societe, le soussigne nomme :
{commissaire_aux_apports.presentation_complete}

A l'effet d'etablir sous sa responsabilite un rapport sur la valeur dudit apport en nature, lequel sera annexe aux statuts de la societe conformement a l'article L. 223-9 du Code de commerce.

Fait a {signature.lieu}
Le {signature.date}

{apporteur.prenom} {apporteur.nom}
```

### 9.3 Choix commissaire

La source contient deux options separees par `OU`.

Decision texte V1 :
- le futur rendu ne doit jamais conserver `OU` ni les deux commissaires en sortie ;
- `commissaire_aux_apports.presentation_complete` doit etre resolu depuis un commissaire selectionne ;
- si aucun commissaire n'est selectionne, le futur generateur doit bloquer.

## 10. Variables

### 10.1 Dossier et selection

- `dossier.structure`
- `dossier.options.cession`
- `dossier.options.apport`
- `dossier.options.associe_unique`
- `operation_spfpl.type`

Valeurs couvertes :
- `SPFPL_CESSION`
- `SPFPL_APPORT`

### 10.2 Societe SPFPL

- `societe_spfpl.denomination`
- `societe_spfpl.forme_sociale`
- `societe_spfpl.forme_sociale_abregee`
- `societe_spfpl.capital_social`
- `societe_spfpl.profession`
- `societe_spfpl.activite`
- `societe_spfpl.ville_rcs`
- `societe_spfpl.numero_rcs`
- `societe_spfpl.siege.adresse_affichee`
- `societe_spfpl.siege.num_voie`
- `societe_spfpl.siege.voie`
- `societe_spfpl.siege.cp`
- `societe_spfpl.siege.ville`
- `societe_spfpl.dirigeant.fonction`
- `societe_spfpl.representant.*`

### 10.3 Cedant / apporteur

- `cedant.*`
- `apporteur.*`
- `apporteur_ou_cedant.*`

Champs principaux :
- `civilite_affichage`
- `genre`
- `prenom`
- `nom`
- `profession`
- `profession_reglementee`
- `profession_reglementee_pluriel`
- `date_naissance`
- `ville_naissance`
- `departement_naissance`
- `nationalite`
- `situation_maritale`
- `conjoint.*`
- `adresse_personnelle_affichee`
- `ordre.*`

### 10.4 Societe cible

- `societe_cible.denomination`
- `societe_cible.forme_sociale`
- `societe_cible.forme_sociale_complete`
- `societe_cible.profession_reglementee`
- `societe_cible.profession_reglementee_pluriel`
- `societe_cible.capital_social`
- `societe_cible.capital_social_lettres`
- `societe_cible.nb_parts_total`
- `societe_cible.valeur_nominale_part`
- `societe_cible.valeur_nominale_part_lettres`
- `societe_cible.siege.adresse_affichee`
- `societe_cible.siege.num_voie`
- `societe_cible.siege.voie`
- `societe_cible.siege.cp`
- `societe_cible.siege.ville`
- `societe_cible.ville_rcs`
- `societe_cible.numero_rcs`
- `societe_cible.repartition_capital_avant_operation`
- `societe_cible.repartition_capital_apres_operation`

### 10.5 Associes et souscripteurs

- `associes_cible[]`
- `associes_cible.liste_presence`
- `associes_cible.signatures`
- `capital_souscription.souscripteurs[]`
- `capital_souscription.repartition_actions`

### 10.6 Operation de cession

- `cession_parts.nb_parts`
- `cession_parts.nb_parts_lettres`
- `cession_parts.plage_parts`
- `cession_parts.prix_unitaire`
- `cession_parts.prix_unitaire_lettres`
- `cession_parts.prix_total`
- `cession_parts.prix_total_lettres`
- `cession_parts.nombre_exemplaires_lettres`

### 10.7 Operation d'apport

- `apport_titres.nb_parts`
- `apport_titres.nb_parts_lettres`
- `apport_titres.nature_titres`
- `apport_titres.plage_parts`
- `apport_titres.valeur_par_titre`
- `apport_titres.valeur_par_titre_lettres`
- `apport_titres.valeur_globale`
- `apport_titres.valeur_globale_lettres`
- `apport_titres.nb_actions_attribuees`
- `apport_titres.nb_actions_attribuees_lettres`
- `apport_titres.valeur_nominale_action`
- `apport_titres.valeur_nominale_action_lettres`

### 10.8 Reunion, capital et commissaire

- `reunion.*`
- `pv_agrement.*`
- `capital_souscription.*`
- `evaluateur_apport.*`
- `commissaire_aux_apports.*`
- `signature.lieu`
- `signature.date`

## 11. Regles de blocage avant generation

Un futur generateur SPFPL doit bloquer si :
- la structure n'est pas `SPFPL_CESSION` ou `SPFPL_APPORT` ;
- le document demande ne correspond pas au chemin cession/apport du dossier ;
- une variable obligatoire du document manque ;
- la note d'information n'a pas d'arbitrage cession/apport ;
- un PV d'agrement est demande sans arbitrage sur le wording `cession` versus `apport` ;
- l'acte de cession d'actions est demande sans source DOCX confirmee ;
- la repartition dynamique du capital ne peut pas etre calculee ;
- plusieurs associes ou souscripteurs sont demandes sans donnees structurees ;
- un contrat d'apport est demande sans choix valide pour l'evaluateur et le commissaire aux apports ;
- l'acte de designation du commissaire aux apports est demande sans commissaire selectionne ;
- le rendu final conserverait un placeholder source `[` ou `]`, une double option non tranchee ou le litteral `OU`.

## 12. Criteres avant implementation

Un ticket de code pourra demarrer seulement si :
- le ticket cible une seule sous-famille documentaire ou un batch explicitement limite ;
- les arbitrages de wording requis pour cette sous-famille sont fournis ;
- les listes dynamiques necessaires sont structurees dans le contexte ;
- aucun DOCX source n'est utilise comme template d'execution ;
- les tests futurs couvrent les structures `SPFPL_CESSION` et/ou `SPFPL_APPORT` pertinentes ;
- les tests verifient l'absence de placeholders residuels ;
- aucun wording juridique n'est corrige silencieusement ;
- les points ouverts ci-dessous sont soit tranches, soit convertis en blocages explicites.

## 13. Points ouverts

1. **Note d'information** : choisir entre une variante cession, une variante apport ou une validation explicite de la double formule source.
2. **PV agrement cession** : arbitrer le conflit entre le classement cession et le wording source d'apport.
3. **PV associe unique** : confirmer que le fichier sans suffixe `- transforme` est la bonne source.
4. **Acte de cession d'actions** : source DOCX non confirmee ; rester hors automatisation.
5. **Acte de cession de parts** : relire la mention isolee `cession d'action` dans le bloc frais avant toute correction.
6. **Repartition du capital** : remplacer les lignes fixes `personne_1`, `personne_2`, `personne_3` et societe associee par `associes_cible[]`.
7. **Contrat d'apport** : choisir entre source nommee a entites fixes et variante parametree pour evaluateur / commissaire.
8. **Commissaire aux apports** : selectionner un commissaire unique ; ne jamais rendre les deux options separees par `OU`.
9. **Commissaire aux comptes / aux apports** : confirmer le libelle metier, la source disponible portant sur un commissaire aux apports.
10. **Liste des souscripteurs** : arbitrer la prise en charge d'une liste dynamique ou limiter la V1 a l'actionnaire unique.
11. **Genre et nombre** : aucune variation supplementaire ne doit etre inventee hors valeurs fournies ou wording valide.

## 14. Statut de la spec texte

`SPEC-TEXTE-SPFPL-001` stabilise la spec texte V1 du batch SPFPL specifique sans code Python.

La prochaine etape recommandee est un arbitrage metier sur les points ouverts 1, 2, 8 et 10 avant tout ticket de code SPFPL.
