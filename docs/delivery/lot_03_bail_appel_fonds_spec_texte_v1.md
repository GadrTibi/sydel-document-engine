# DAAT x SYDEL - SPEC TEXTE V1
## Mini-batch `bail / appel de fonds`

## 1. Objet

Stabiliser le texte V1 du mini-batch `bail / appel de fonds`, sans coder.

Cette spec texte complete :
- `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`

Elle couvre deux documents distincts :
- `LOT03-BAIL-AVENANT` : avenant au contrat de bail ;
- `LOT03-APPEL-FONDS-SEL` : appel de fonds SEL.

Objectif V1 :
- distinguer le texte fixe source ;
- isoler les variables ;
- identifier les blocs conditionnels ;
- lister les elements manuels ;
- garder les points ouverts visibles avant tout ticket de code.

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
- `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : generation DOCX propre from-scratch pour un futur ticket code ;
- ADR-0005 : mode Codex repo-first.

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Sources DOCX :
- `project/source_documents/lot_03/` ne contient pas les deux DOCX demandes ;
- les sources ont donc ete lues dans `project/source_import/raw_drive_dump/Creation SELARL/Cession/`.

Sources raw lues :
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/Avenant Contrat de bail.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/appel de fond sel.docx`

Note de fidelite :
- les formulations juridiques ci-dessous reprennent les sources lues ;
- les anomalies ou ambiguites source sont signalees en points ouverts, pas corrigees.

## 3. Perimetre V1

### 3.1 Avenant contrat de bail

Selection metier issue de la source de verite :
- SELARL : document rattache au bloc `Si cession` ;
- SELAS : document rattache au bloc `Si Cession`.

Decision texte V1 :
- document canonique distinct ;
- activable quand `dossier.options.cession == true` pour SELARL ou SELAS ;
- aucune variante textuelle SELAS specifique n'est stabilisee dans cette spec texte, faute de lecture demandee d'une source SELAS dediee.

### 3.2 Appel de fonds SEL

Selection metier issue de la source de verite :
- SELARL : document rattache au bloc `Si cession` ;
- SELAS : non liste dans le bloc cession.

Decision texte V1 :
- document canonique distinct ;
- activable en V1 uniquement pour SELARL avec `dossier.options.cession == true` ;
- usage limite au cabinet dentaire tant que le wording source `cabinet dentaire` n'est pas arbitre pour le medical.

## 4. Texte fixe source - Avenant contrat de bail

Le titre est porte par un tableau source :

```text
Avenant n°1 au bail du [date_du_jour]
```

Corps fixe avec placeholders source :

```text
Entre les soussignés :

[civilite_bailleur] [prenom_bailleur] [nom_bailleur], [profession_bailleur], né le [date_naissance_bailleur], à [ville_naissance_bailleur] de nationalité [nationalite_bailleur], demeurant [adresse_bailleur],

Ci-après désigné « le Bailleur »

ET :

[civilite_locataire] [prenom_locataire] [nom_locataire], [profession_locataire], né le [date_naissance_locataire], à [ville_naissance_locataire] de nationalité [nationalite_locataire], demeurant [adresse_locataire],

Ci-après désigné « le Locataire »

Les parties conviennent de ce qui suit :

ARTICLE 1 : changement de locataire

Le bail signé en date du [date_bail], a pour locataire [civilite_locataire] [prenom_locataire] [nom_locataire], ([profession_locataire]).

Le présent avenant donne bail à la société [denomination_societe] en cours d’immatriculation au RCS [ville_rcs], domiciliée au [adresse_siege].

ARTICLE 2 : Responsabilité pour une société en cours de formation

Le [civilite_courte_locataire] [prenom_locataire] [nom_locataire], domicilié [adresse_locataire], engage sa responsabilité pour tous les actes passés au nom de la société jusqu’à l’immatriculation au RCS.

[civilite_locataire] [prenom_locataire] [nom_locataire] s’engage à fournir au Bailleur un extrait KBIS une fois que les démarches seront finies.

ARTICLE 3 : Clauses du bail

Le présent avenant ne modifie pas les clauses du bail en cours.

Fait à [lieu_signature] en [nombre_exemplaires_lettres] exemplaires, le [date_signature]
```

Table de signatures source :

```text
Le Bailleur | L’ancien locataire
Le nouveau locataire | Le nouveau locataire
```

Regles de fidelite :
- `changement de locataire` conserve la casse source ;
- `en cours d’immatriculation au RCS` reste fixe en V1 ;
- `démarches seront finies` reste le wording source ;
- la table de signatures contient deux cellules `Le nouveau locataire`; cette duplication est conservee comme anomalie source a arbitrer.

## 5. Texte fixe source - Appel de fonds SEL

Texte fixe avec placeholders source :

```text
[nom_banque]

[lieu_signature], le [date_signature]

A l’attention de [civilite_destinataire] [prenom_destinataire] [nom_destinataire]

Objet : demande de déblocage des fonds

Cher Monsieur,

Nous vous remercions de bien vouloir procéder, ce jour, au déblocage des fonds d’un montant de :

Montant du fond
€

pour la cession du cabinet dentaire exploité au [denomination_societe] de [civilite_vendeur] [prenom_vendeur] [nom_vendeur] à la Société [denomination_societe_acquereur].

Nous vous prions d’agréer, Cher Monsieur, nos salutations distinguées.

[prenom_signataire] [nom_signataire]
```

Regles de fidelite :
- `A l’attention de` conserve l'absence d'accent sur `A` ;
- `Objet : demande de déblocage des fonds` conserve la casse source ;
- `Cher Monsieur` reste fixe en V1, aucune variante de civilite n'est sourcee ;
- `Montant du fond` est conserve comme libelle source de zone montant, mais ne peut pas rester un placeholder implicite en generation ;
- `cabinet dentaire` reste fixe et bloque l'usage medical sans wording valide.

## 6. Texte canonique V1 - Avenant contrat de bail

Forme cible avec variables canoniques :

```text
Avenant n°1 au bail du {bail.date_avenant}

Entre les soussignés :

{bail.bailleur.civilite_affichage} {bail.bailleur.prenom} {bail.bailleur.nom}, {bail.bailleur.profession}, né le {bail.bailleur.date_naissance}, à {bail.bailleur.ville_naissance} de nationalité {bail.bailleur.nationalite}, demeurant {bail.bailleur.adresse_affichee},

Ci-après désigné « le Bailleur »

ET :

{bail.locataire.civilite_affichage} {bail.locataire.prenom} {bail.locataire.nom}, {bail.locataire.profession}, né le {bail.locataire.date_naissance}, à {bail.locataire.ville_naissance} de nationalité {bail.locataire.nationalite}, demeurant {bail.locataire.adresse_affichee},

Ci-après désigné « le Locataire »

Les parties conviennent de ce qui suit :

ARTICLE 1 : changement de locataire

Le bail signé en date du {bail.date_signature_origine}, a pour locataire {bail.locataire.civilite_affichage} {bail.locataire.prenom} {bail.locataire.nom}, ({bail.locataire.profession}).

Le présent avenant donne bail à la société {societe.denomination} en cours d’immatriculation au RCS {societe.rcs_ville}, domiciliée au {societe.siege.adresse_affichee}.

ARTICLE 2 : Responsabilité pour une société en cours de formation

Le {bail.locataire.civilite_courte} {bail.locataire.prenom} {bail.locataire.nom}, domicilié {bail.locataire.adresse_affichee}, engage sa responsabilité pour tous les actes passés au nom de la société jusqu’à l’immatriculation au RCS.

{bail.locataire.civilite_affichage} {bail.locataire.prenom} {bail.locataire.nom} s’engage à fournir au Bailleur un extrait KBIS une fois que les démarches seront finies.

ARTICLE 3 : Clauses du bail

Le présent avenant ne modifie pas les clauses du bail en cours.

Fait à {signature.lieu} en {document.nombre_exemplaires_lettres} exemplaires, le {signature.date}
```

Signatures cible :
- `Le Bailleur`
- `L’ancien locataire`
- `Le nouveau locataire`

Point de prudence :
- la source contient quatre cellules de signature dont deux libelles identiques `Le nouveau locataire`; le futur rendu doit etre arbitre avant code entre reproduction stricte de la table et normalisation en trois emplacements.

## 7. Texte canonique V1 - Appel de fonds SEL

Forme cible avec variables canoniques :

```text
{cession.financement.banque.nom}

{signature.lieu}, le {signature.date}

A l’attention de {cession.financement.destinataire.civilite_affichage} {cession.financement.destinataire.prenom} {cession.financement.destinataire.nom}

Objet : demande de déblocage des fonds

Cher Monsieur,

Nous vous remercions de bien vouloir procéder, ce jour, au déblocage des fonds d’un montant de :

{cession.financement.montant_deblocage}
€

pour la cession du cabinet dentaire exploité au {cession.cabinet.denomination_ou_adresse_affichee} de {cession.vendeur.civilite_affichage} {cession.vendeur.prenom} {cession.vendeur.nom} à la Société {cession.acquereur.denomination_societe}.

Nous vous prions d’agréer, Cher Monsieur, nos salutations distinguées.

{document.signataire.prenom} {document.signataire.nom}
```

Point de prudence :
- la source ne fournit pas de montant en lettres ;
- la zone montant doit etre fournie manuellement sous une forme affichee valide, sans deduction juridique ou bancaire.

## 8. Variables

### 8.1 Variables de selection

| Variable | Usage |
|---|---|
| `dossier.structure` | selection SELARL / SELAS |
| `dossier.options.cession` | condition generale du mini-batch |
| `dossier.cession.type_cabinet` | condition medical / dentaire |

### 8.2 Variables - Avenant contrat de bail

| Placeholder source | Variable canonique V1 |
|---|---|
| `[date_du_jour]` | `bail.date_avenant` |
| `[civilite_bailleur]` | `bail.bailleur.civilite_affichage` |
| `[prenom_bailleur]` | `bail.bailleur.prenom` |
| `[nom_bailleur]` | `bail.bailleur.nom` |
| `[profession_bailleur]` | `bail.bailleur.profession` |
| `[date_naissance_bailleur]` | `bail.bailleur.date_naissance` |
| `[ville_naissance_bailleur]` | `bail.bailleur.ville_naissance` |
| `[nationalite_bailleur]` | `bail.bailleur.nationalite` |
| `[adresse_bailleur]` | `bail.bailleur.adresse_affichee` |
| `[civilite_locataire]` | `bail.locataire.civilite_affichage` |
| `[civilite_courte_locataire]` | `bail.locataire.civilite_courte` |
| `[prenom_locataire]` | `bail.locataire.prenom` |
| `[nom_locataire]` | `bail.locataire.nom` |
| `[profession_locataire]` | `bail.locataire.profession` |
| `[date_naissance_locataire]` | `bail.locataire.date_naissance` |
| `[ville_naissance_locataire]` | `bail.locataire.ville_naissance` |
| `[nationalite_locataire]` | `bail.locataire.nationalite` |
| `[adresse_locataire]` | `bail.locataire.adresse_affichee` |
| `[date_bail]` | `bail.date_signature_origine` |
| `[denomination_societe]` | `societe.denomination` |
| `[ville_rcs]` | `societe.rcs_ville` |
| `[adresse_siege]` | `societe.siege.adresse_affichee` |
| `[lieu_signature]` | `signature.lieu` |
| `[nombre_exemplaires_lettres]` | `document.nombre_exemplaires_lettres` |
| `[date_signature]` | `signature.date` |

### 8.3 Variables - Appel de fonds SEL

| Placeholder / zone source | Variable canonique V1 |
|---|---|
| `[nom_banque]` | `cession.financement.banque.nom` |
| `[lieu_signature]` | `signature.lieu` |
| `[date_signature]` | `signature.date` |
| `[civilite_destinataire]` | `cession.financement.destinataire.civilite_affichage` |
| `[prenom_destinataire]` | `cession.financement.destinataire.prenom` |
| `[nom_destinataire]` | `cession.financement.destinataire.nom` |
| `Montant du fond` | `cession.financement.montant_deblocage` |
| `[denomination_societe]` | `cession.cabinet.denomination_ou_adresse_affichee` |
| `[civilite_vendeur]` | `cession.vendeur.civilite_affichage` |
| `[prenom_vendeur]` | `cession.vendeur.prenom` |
| `[nom_vendeur]` | `cession.vendeur.nom` |
| `[denomination_societe_acquereur]` | `cession.acquereur.denomination_societe` |
| `[prenom_signataire]` | `document.signataire.prenom` |
| `[nom_signataire]` | `document.signataire.nom` |

## 9. Blocs conditionnels

### 9.1 Selection avenant contrat de bail

Regle V1 :
- rendre l'avenant si `dossier.options.cession == true` et `dossier.structure in {SELARL, SELAS}`.

Blocage :
- bloquer hors SELARL / SELAS tant qu'aucune decision metier ne rattache l'avenant a une autre structure.

### 9.2 Selection appel de fonds SEL

Regle V1 :
- rendre l'appel de fonds si `dossier.options.cession == true`, `dossier.structure == SELARL` et `dossier.cession.type_cabinet == dentaire`.

Blocage :
- bloquer l'appel de fonds pour SELAS, car la source de verite ne le liste pas dans le bloc cession SELAS ;
- bloquer l'appel de fonds pour cabinet medical, car la source dit `cabinet dentaire`.

### 9.3 Societe en cours d'immatriculation

Constat :
- l'avenant contient le texte fixe `en cours d’immatriculation au RCS`.

Regle V1 :
- ne pas produire l'avenant pour une societe deja immatriculee sans variante source ou validation metier.

### 9.4 Civilite courte du locataire

Constat :
- la source utilise `Le [civilite_courte_locataire]` dans l'article 2.

Regle V1 :
- `bail.locataire.civilite_courte` doit etre fournie explicitement ;
- ne pas la deduire automatiquement de `civilite_affichage` sans referentiel valide.

### 9.5 Signature avenant

Constat :
- la source contient une table de signatures avec `Le Bailleur`, `L’ancien locataire`, puis deux cellules `Le nouveau locataire`.

Regle V1 :
- le futur code doit soit reproduire strictement la table source, soit appliquer un arbitrage metier documente ;
- sans arbitrage, la duplication reste un point ouvert.

## 10. Elements manuels

### 10.1 Avenant contrat de bail

Doivent etre fournis par contexte dossier ou saisie humaine :
- identite complete du bailleur ;
- identite complete du locataire personne physique ;
- civilite courte du locataire ;
- date du bail initial ;
- date de l'avenant ;
- ville RCS ;
- adresse affichee du siege ;
- lieu et date de signature ;
- nombre d'exemplaires en lettres ;
- confirmation que la societe est bien en cours d'immatriculation ;
- confirmation que le bailleur accepte le changement de locataire.

### 10.2 Appel de fonds SEL

Doivent etre fournis par contexte dossier ou saisie humaine :
- banque ;
- destinataire bancaire ;
- montant affiche du deblocage ;
- identification du cabinet cede ;
- vendeur ;
- societe acquereur ;
- signataire effectif de la lettre ;
- lieu et date de signature ;
- confirmation que le dossier porte sur un cabinet dentaire.

Doivent rester hors automatisation V1 :
- adaptation medicale du wording `cabinet dentaire` ;
- variante de civilite pour `Cher Monsieur` ;
- correction silencieuse de `Montant du fond` ;
- deduction automatique que le locataire, le vendeur et le signataire sont la meme personne.

## 11. Regles de blocage avant generation

Un futur generateur doit bloquer si :
- `dossier.options.cession != true` ;
- une variable obligatoire du document demande est absente ;
- l'avenant est demande hors SELARL / SELAS ;
- l'avenant est demande pour une societe deja immatriculee sans wording valide ;
- `bail.locataire.civilite_courte` est absent ;
- `document.nombre_exemplaires_lettres` est absent pour l'avenant ;
- l'appel de fonds est demande hors SELARL ;
- l'appel de fonds est demande pour un cabinet medical ;
- le montant de deblocage est absent ;
- le lien entre `bail.locataire`, `cession.vendeur`, `cession.acquereur` et `societe` n'est pas explicite quand ces roles sont reutilises.

Le futur generateur ne doit pas :
- inventer une variante medicale ;
- feminiser ou varier `Cher Monsieur` ;
- corriger le texte juridique source sans note de validation ;
- lire les DOCX source comme templates d'execution.

## 12. Criteres avant implementation

Le ticket de code peut demarrer si :
- les identifiants catalogue definitifs sont confirmes ;
- le comportement de la table de signatures de l'avenant est arbitre ;
- le statut de l'appel de fonds hors SELARL est confirme ;
- l'appel de fonds medical reste bloque ou dispose d'un wording source valide ;
- les variables obligatoires ci-dessus sont modelisees ou fournies par contexte ;
- les tests prevus couvrent SELARL cession, SELAS cession, cabinet medical bloque et cabinet dentaire autorise ;
- les tests verifient l'absence de placeholders residuels `[` / `]` ;
- aucun autre document metier n'est modifie dans le meme ticket.

## 13. Points ouverts

1. Appel de fonds SELAS : non liste dans la source de verite pour SELAS ; ne pas activer sans arbitrage.
2. Appel de fonds medical : la source contient `cabinet dentaire`; aucune variante medicale n'est stabilisee.
3. Montant : la source contient `Montant du fond` puis `€`, sans placeholder propre ; le format affiche du montant doit etre valide avant code.
4. Cabinet exploite : `[denomination_societe]` dans l'appel de fonds designe le cabinet exploite, pas clairement la societe du dossier ; mapping a valider.
5. Avenant : la source vise une societe en cours d'immatriculation ; aucune variante pour societe deja immatriculee n'est lue.
6. Signature avenant : la table source contient deux cellules `Le nouveau locataire`; reproduction stricte ou normalisation en trois signatures a arbitrer.
7. Civilite courte : les valeurs autorisees pour `civilite_courte_locataire` doivent etre fournies explicitement.
8. Roles personne physique : ne pas supposer automatiquement que `bail.locataire`, `cession.vendeur` et `document.signataire` sont identiques.

## 14. Statut de la spec texte

`SPEC-TEXTE-BAIL-APP-001` est complete pour stabiliser le texte V1 du mini-batch `bail / appel de fonds`.

Aucun code Python n'est modifie par cette spec.
