# Registre canonique global V2.1

Statut : version gelee pour architecture front globale, sans modification de l'UI, des generateurs, du moteur DOCX/PDF/ZIP ni du wording juridique.

## Sources integrees

- `docs/project/GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv`
- `docs/project/GLOBAL_VARIABLE_IDENTITY_MATRIX_V1.csv`
- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2.md`
- `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V1.md`
- `docs/review/global_variable_identity_audit_001_report_v1.md`
- `project/source_truth/albane_reponse_mail_selarl_v1.md`
- `project/source_truth/modele Statuts SELAS avec MH.docx`
- `project/source_truth/notebooklm_selarl_10_prompts_v1.md`
- `project/source_truth/Documents_a_generer_par_cas_V3.docx`

Note source : le ticket mentionne `project/source_truth/modele_statuts_selas_medecin_micro_holding_v1.docx`, mais le fichier present dans le workspace est `project/source_truth/modele Statuts SELAS avec MH.docx`. Le contenu a ete lu comme modele SELAS medecin avec associe personne morale type societe civile micro-holding.

## Synthese V2.1

- Base conservee : registre V2, 49 champs canoniques proposes, 43 documents, 15 familles.
- Changement principal : integration des arbitrages humains sur les roles, les adresses, la cession SCM / fonds liberal et le cas SELAS + micro-holding.
- Regle de securite : aucune fusion silencieuse de roles, d'adresses ou de parties.
- Statut front : suffisamment stable pour lancer l'architecture du nouveau front global.
- Statut implementation : non suffisant pour modifier les generateurs ou le wording juridique sans ticket documentaire dedie.

## Principes obligatoires V2.1

### 1. Roles et personnes

Le futur modele doit distinguer les fiches personnes et les roles documentaires.

| Role canonique | Definition V2.1 | Fusion autorisee |
|---|---|---|
| `personne.praticien` | Personne physique cliente exercant ou ayant exerce en BNC. | Peut alimenter d'autres roles uniquement via option explicite ou contexte `Dossier unipersonnel`. |
| `personne.associe[]` | Detenteur de parts ou actions. | Peut etre le praticien, une autre personne physique ou une personne morale, sans fusion silencieuse. |
| `personne.gerant` / `personne.president` | Mandataire social selon la forme sociale. | Peut etre le praticien seulement si le dossier le confirme. |
| `personne.signataire` | Personne qui signe un document donne. | Role par document ou par lot, jamais mandataire par defaut. |
| `personne.mandataire` | Personne recevant pouvoir pour les formalites. | Distincte du signataire sauf option documentee. |
| `personne.vendeur` / `personne.cedant` | Partie personne physique qui vend ou cede un fonds, des parts ou actions. | Dans le parcours SELARL standard, reutilise le praticien BNC ; ailleurs, role distinct. |
| `societe.acquereur` / `societe.cessionnaire` | Societe qui acquiert le fonds ou les parts. | Dans le parcours SELARL standard, reutilise la SEL en constitution ; ailleurs, role distinct. |
| `personne.bailleur` / `personne.locataire` | Parties du bail ou de son avenant. | Distinctes des roles vendeur/acquereur, sauf branche documentee. |
| `personne.representant_personne_morale` | Representant d'une societe associee ou partie a l'acte. | Distinct de l'associe personne morale. |

Regles associees :

- `Dossier unipersonnel` autorise Praticien = associe unique = gerant = signataire.
- Si `Dossier unipersonnel` est inactif, aucune derivation Praticien / associe / gerant / signataire n'est imposee.
- Un associe personne morale doit avoir sa propre fiche societe et, si le document le requiert, un representant personne physique.
- Vendeur, cedant, acquereur, cessionnaire, bailleur et locataire sont des roles de parties, pas de simples alias.

### 2. Adresses

Albane confirme trois adresses pivots pour le parcours SEL :

| Adresse canonique | Definition V2.1 | Regle |
|---|---|---|
| `personne.praticien.adresse_domicile` | Adresse personnelle du praticien. | Distincte du siege et du lieu d'exercice par defaut. |
| `exercice.lieu_principal.adresse` | Adresse du lieu d'exercice / cabinet. | Base pour le cabinet, les locaux professionnels et l'adresse SCM standard. |
| `societe.{role}.siege.adresse` | Adresse du siege social de la societe rolee. | Peut etre domicile, lieu d'exercice ou adresse manuelle selon option explicite. |

Regles fortes :

- `domiciliation.adresse` = `societe.principale.siege.adresse`.
- `societe.principale.siege.adresse` = `exercice.lieu_principal.adresse` seulement via option explicite.
- `scm.adresse` = `exercice.lieu_principal.adresse` pour le cas standard documente par Albane.
- `scm_cedee.siege.adresse` n'est pas automatiquement egale a `scm_cession.cessionnaire.siege.adresse`.
- `personne.vendeur.adresse` est l'adresse de domicile du praticien dans la cession SELARL standard.
- L'adresse des locaux loues peut coincider avec le lieu d'exercice dans le cas standard, mais le bail reste une famille documentaire a arbitrer quand la SCM modifie le paragraphe locataire.

### 3. Parties de cession

| Operation | Partie cedante / vendeuse | Partie acquereuse / cessionnaire | Regle V2.1 |
|---|---|---|---|
| Cession de fonds liberal SELARL standard | `personne.praticien` en BNC | `societe.principale` SEL en constitution | Reutilisation documentee, sans fusion de roles. |
| Cession de parts SCM vers SEL | `personne.praticien` en BNC | `societe.principale` SEL en constitution | La SEL peut etre cessionnaire avant immatriculation ; ne pas ajouter de filigrane automatiquement. |
| Bail / avenant | `personne_ou_societe.bailleur` | `personne_ou_societe.locataire` | Locataire pas toujours SELARL en constitution ; branche ou champ libre a traiter dans ticket bail. |
| Cessionnaire de parts SCM | `societe.principale` ou autre societe rolee | N/A | Adresse et representant distincts si necessaire. |

### 4. Champs canoniques V2.1 par famille

Les champs V2 non contredits restent valides. Le statut V2.1 ci-dessous remplace les statuts prudents V2 pour les familles arbitrees.

| Famille | Champs V2.1 | Statut |
|---|---|---|
| Signature | `signature.lieu`, `signature.date`, `signature.nombre_exemplaires` | Stable, reuse possible par document ou lot. |
| Societe | `societe.{role}.denomination`, `forme_sociale`, `capital_social`, `rcs.numero`, `rcs.ville` | Stable avec role societe obligatoire. |
| Siege | `societe.{role}.siege.adresse_affichee`, `num_voie`, `voie`, `cp`, `ville` | Stable ; composants et affiche peuvent etre lies. |
| Personnes | `personne.{role}.civilite_affichage`, `genre`, `prenom`, `nom`, `date_naissance`, `ville_naissance`, `departement_naissance`, `nationalite`, `profession`, `fonction`, `adresse_personnelle`, `numero_rpps`, `numero_ordre` | Stable avec role obligatoire ; pas de fusion silencieuse. |
| Conjoint | `personne.conjoint.{attribut}` | Stable comme role distinct. |
| Capital et titres | `capital.titres.nombre_total`, `capital.titres.valeur_nominale`, `capital.repartition_associes` | Stable en structure ; calculs et overrides a arbitrer en interne. |
| Apports | `apport.numeraire.montant`, `apport.nature.montant` | Stable ; liens avec capital non automatiques. |
| Cession titres | `cession.parts.nombre`, `cession.parts.plage`, `cession.prix.total`, `cession.prix.unitaire` | Stable ; parts/actions et SCM/SPFPL/SAS a typer. |
| Cession cabinet | `cession.cabinet.adresse`, `cession.cabinet.prix_composantes` | Stable ; adresse reliee au lieu d'exercice seulement via regle documentee. |
| Bail | `bail.parties`, `bail.dates` | Stable mais paragraphe locataire a garder en arbitrage documentaire. |
| Ordre | `ordre.professionnel` | Ouvert interne : modele par inscrit a finaliser. |
| Derogations | `derogation.{type}` | Stable comme bloc optionnel ou manuel selon document. |
| Regime communautaire | `regime_communautaire.{document}` | Stable comme bloc conjoint/regime/date. |
| SPFPL | `spfpl.operation.type` | Stable hors confusion avec SELAS + micro-holding. |
| SCM cession | `scm_cession.{champ}` | Stable ; cessionnaire, SCM cedee et praticien cedant restent rolees. |
| Commissaire / evaluateur | `commissaire_aux_apports.{champ}` | Stable comme entite tierce. |
| Banque | `banque.{role}` | Ouvert interne : parametrage global ou champ dossier avec override. |
| Fiscalite | `administration_fiscale.{role}` | Ouvert interne : probablement parametrage local avec override. |
| Options dossier | `dossier.options.{option}` | Stable pour piloter conditions et champs visibles. |

## Cas hors perimetre immediat

### SELAS medecin avec associe personne morale micro-holding

Decision V2.1 :

- ce n'est pas un cas SELARL standard ;
- c'est une SELAS medecin ;
- l'associe personne morale n'est pas une SPFPL dans l'arbitrage Albane, mais une societe civile micro-holding ;
- le modele fourni montre une societe civile associee, representee par son gerant, avec apports, actions et actions de preference ;
- aucun generateur, aucune UI et aucun wording juridique ne doivent etre modifies dans ce ticket.

Champs candidats pour ticket futur uniquement :

- `societe.micro_holding.denomination`
- `societe.micro_holding.forme_sociale`
- `societe.micro_holding.capital_social`
- `societe.micro_holding.siege.adresse`
- `societe.micro_holding.rcs.numero`
- `societe.micro_holding.representant`
- `capital.actions.preference.categorie`
- `capital.actions.preference.droits_financiers`
- `capital.repartition_droits_vote`

## Contradictions connues entre pratique client et arbitrage produit interne

| Sujet | Pratique client documentee | Arbitrage produit interne actuel | Decision V2.1 |
|---|---|---|---|
| Filigrane PROJET | Albane applique un filigrane projet tant que la SEL n'est pas immatriculee, puis le retire apres integration du numero. | Pas de mode Projet / filigrane en V1. | Contradiction documentee, non implementee. Ticket produit separe requis. |
| Mode Projet NotebookLM | NotebookLM presente le mode Projet comme utile pour banque et Ordre. | La correction interne anterieure exclut mode Projet et filigrane V1. | Non implemente ; ne pas creer de regle automatique. |
| Adresses souvent identiques | Albane indique que domicile, lieu d'exercice, siege SEL/SCM et locaux loues sont souvent identiques dans le cas standard. | Le produit doit eviter toute copie implicite risquee. | Options explicites et roles conserves ; pas de fusion globale. |
| Locataire du bail | Albane indique que le paragraphe varie selon presence d'une SCM et peut rester plus simple en champ libre. | Le moteur existant ne doit pas etre modifie ici. | Backlog documentaire bail/cession. |

## Stabilite pour architecture front

Le registre V2.1 est stable pour lancer l'architecture du nouveau front :

- modele objet `Personne` + `RoleAssignment` ;
- modele objet `Societe` rolee ;
- modele `Adresse` rolee avec liens explicites ;
- blocs operationnels cession, bail, SCM, capital, ordre, banque et fiscalite ;
- options de reutilisation explicites et tracables.

Limite : le registre V2.1 ne vaut pas spec de generation documentaire. Toute implementation de document, de filigrane, de wording ou de calcul juridique reste soumise au pipeline documentaire complet.
