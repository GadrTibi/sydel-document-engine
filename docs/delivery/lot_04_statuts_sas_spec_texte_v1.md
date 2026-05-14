# DAAT x SYDEL - SPEC TEXTE V1
## Statuts SAS

## 1. Objet

Stabiliser le texte canonique et les variantes textuelles des statuts SAS avant tout codage.

Cette spec texte complete :
- `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md`

Elle couvre uniquement :
- `project/source_documents/lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx`

Elle ne modifie aucun wording juridique source. Les anomalies ou formulations sensibles sont documentees comme points ouverts, sans correction implicite.

## 2. Sources lues

Memoire projet et referentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_04_statuts_preparation_v1.md`
- `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md`
- `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`
- `docs/delivery/lot_05_spfpl_spec_texte_v1.md`
- `docs/delivery/lot_05_spfpl_arbitrages_v1.md`

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Source documentaire Lot 04 :
- `project/source_documents/lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0005 : mode Codex repo-first.

## 3. Perimetre texte V1

Chemin couvert :
- `SAS`, avec source de statuts dont le contenu est `SPFPL medecins par actions simplifiee`.

Hors perimetre :
- SAS generique ;
- SASU holding ;
- statuts SPFPL cession/apport deja traites comme famille distincte ;
- attestation sur le capital / liste des souscripteurs ;
- PV remuneration president ;
- toute transformation multi-actionnaires.

Decision texte V1 :
- conserver la lecture actionnaire unique ;
- documenter les blocs qui devraient devenir dynamiques avant tout passage multi-actionnaires ;
- ne pas corriger les formulations juridiquement sensibles sans validation.

## 4. Structure texte source

Structure visible du document :
- cartouche de tete avec denomination, forme, capital et siege ;
- titre `STATUTS` ;
- identification du soussigne ;
- clause de constitution sous condition suspensive d'inscription au Tableau de l'Ordre des Medecins ;
- articles 1 a 27 ;
- signature du president ;
- annexe des engagements pris avant constitution.

Footer visible :
- `[denomination_societe] - Statuts constitutifs`

## 5. Cartouche de tete

Texte source structurel :

```text
{societe.denomination}
Societe de Participations Financieres de Profession Liberale de Medecins par actions simplifiee
Au capital de {societe.capital_social}
Siege social : {societe.siege.adresse_affichee}

STATUTS
```

Variables :
- `societe.denomination`
- `societe.capital_social`
- `societe.siege.adresse_affichee`

Point de vigilance :
- la forme sociale est fixe dans la source sur une SPFPL de medecins ; elle ne doit pas devenir une SAS generique sans validation.

## 6. Bloc soussigne / actionnaire unique

Structure source :

```text
Le soussigne :
- {actionnaire_unique.civilite_affichage} {actionnaire_unique.prenom} {actionnaire_unique.nom}
{actionnaire_unique.qualification_principale} de profession
Ne le {actionnaire_unique.date_naissance} a {actionnaire_unique.ville_naissance} ({actionnaire_unique.departement_naissance})
Demeurant {actionnaire_unique.adresse_personnelle_affichee}
{actionnaire_unique.situation_maritale} sous le regime de {actionnaire_unique.regime_matrimonial} avec {actionnaire_unique.conjoint.civilite_affichage} {actionnaire_unique.conjoint.prenom} {actionnaire_unique.conjoint.nom}
De nationalite {actionnaire_unique.nationalite}
Inscrit au tableau de l'Ordre des Medecins de {actionnaire_unique.ordre.departemental} sous le numero national {actionnaire_unique.ordre.numero} et sous le numero RPPS {actionnaire_unique.ordre.numero_rpps}.
```

Le bloc enchaine ensuite sur les qualites :
- `Associe Unique` ;
- `Actionnaire Unique` ;
- ou, avec d'eventuels autres associes, `Associes`.

Decision texte V1 :
- le rendu automatique est limite a l'actionnaire unique ;
- les formules pluripersonnelles restent dans le texte fixe general, mais ne suffisent pas a generer des comparutions multiples.

Point bloquant :
- la phrase matrimoniale est unique et suppose conjoint/regime ; elle doit etre arbitree avant tout rendu pour une situation personnelle differente.

## 7. Articles fixes principaux

### 7.1 Article 1 - Forme

Texte fixe principal :
- constitution d'une SPFPL de medecins sous forme de societe par actions simplifiee unipersonnelle ;
- reference aux presents statuts ;
- references legales et deontologiques ;
- fonctionnement avec un ou plusieurs associes.

Variables :
- aucune variable source dans l'article.

Point ouvert :
- confirmer que les references a l'ordonnance du 8 fevrier 2023 et au Code de la Sante publique sont applicables au perimetre SAS cible.

### 7.2 Article 2 - Objet

Texte fixe principal :
- detention de parts ou actions de SEL ayant pour objet la profession de medecin ;
- activites accessoires en relation directe ;
- operations rattachees a l'objet.

Variables :
- aucune variable source dans l'article.

### 7.3 Article 3 - Denomination

Texte source structurel :

```text
La denomination de la Societe est : {societe.denomination}
```

Le reste de l'article fixe les mentions obligatoires dans les actes, lettres, factures et documents.

Variables :
- `societe.denomination`

### 7.4 Article 4 - Siege social

Texte source structurel :

```text
Le siege social est fixe au {societe.siege.adresse_affichee}.
```

Le reste de l'article traite le transfert du siege.

Point ouvert :
- la source mentionne une decision du `gerant seul` dans un document SAS ; aucune correction automatique n'est autorisee.

### 7.5 Article 5 - Duree

Texte fixe principal :
- duree de 99 ans a compter de l'immatriculation au RCS ;
- prorogation ou dissolution anticipee par decision de l'actionnaire unique ou des associes.

Variables :
- aucune variable source dans l'article.

### 7.6 Article 6 - Apports

Texte source structurel :

```text
Il a ete apporte en numeraire :
Par le Docteur {actionnaire_unique.prenom} {actionnaire_unique.nom} {societe.capital_social}
Soit au total la somme de {societe.capital_social}
Cette somme a ete des avant ce jour, deposee au credit d'un compte ouvert au nom de la Societe dans les livres de la Banque {depot_fonds.banque.nom}
```

Variables :
- `actionnaire_unique.prenom`
- `actionnaire_unique.nom`
- `societe.capital_social`
- `depot_fonds.banque.nom`

Point de rendu :
- la ligne source `Par le Docteur ... [capital_social]` devra etre relue avant code pour separer proprement identite et montant sans modifier le wording juridique.

### 7.7 Article 7 - Capital social

Texte source structurel :

```text
Le capital social est fixe a {societe.capital_social_lettres} ({societe.capital_social}) euros, divise en {societe.nb_actions_total_lettres} ({societe.nb_actions_total}) actions de {societe.valeur_nominale_action_lettres} ({societe.valeur_nominale_action}) chacune, entierement liberees et attribuees comme suit :
Le Docteur {actionnaire_unique.prenom} {actionnaire_unique.nom} {actionnaire_unique.nb_actions} actions
Soit un total de {societe.nb_actions_total} actions
```

Variables :
- `societe.capital_social_lettres`
- `societe.capital_social`
- `societe.nb_actions_total_lettres`
- `societe.nb_actions_total`
- `societe.valeur_nominale_action_lettres`
- `societe.valeur_nominale_action`
- `actionnaire_unique.prenom`
- `actionnaire_unique.nom`
- `actionnaire_unique.nb_actions`

Regle de coherence :
- en V1 actionnaire unique, `actionnaire_unique.nb_actions == societe.nb_actions_total`.

### 7.8 Article 8 - Qualite des associes

Texte fixe principal :
- detention du capital et des droits de vote par des personnes exercant la profession de medecin au sein des SEL dans lesquelles la societe detient des participations ;
- categories pouvant detenir le complement du capital.

Variables :
- aucune variable source dans l'article.

### 7.9 Article 9 - Augmentation et reduction du capital

Texte fixe principal :
- augmentation du capital par decision collective ou de l'associe unique ;
- creation d'actions nouvelles ;
- augmentation du nominal ;
- reduction du capital.

Variables :
- aucune variable source dans l'article.

Point de vigilance :
- la source contient des accords et formulations a relire juridiquement avant toute correction.

### 7.10 Article 10 - Cession et transmission des actions

Texte fixe principal :
- restriction de transmission au profit de personnes remplissant les qualites de l'article 8 ;
- clause d'agrement ;
- formalites ;
- transmission par deces ;
- nullite des cessions.

Variables :
- aucune variable source dans l'article.

Point de vigilance :
- l'article alterne `actions`, `parts` et certaines formulations heritees ; ne pas harmoniser sans validation.

### 7.11 Articles 11 a 16

Blocs fixes :
- Article 11 : comptes courants ;
- Article 12 : president, nomination, pouvoirs, remuneration ;
- Article 13 : directeurs generaux ;
- Article 14 : conventions entre la societe et ses dirigeants ;
- Article 15 : decisions d'actionnaires ;
- Article 16 : commissaires aux comptes.

Variables :
- Article 12 seulement :
  - `president.prenom`
  - `president.nom`
  - `president.adresse_personnelle_affichee`

Texte source structurel Article 12 :

```text
L'Associe Unique, Monsieur {president.prenom} {president.nom},
Demeurant {president.adresse_personnelle_affichee}
est nomme president de la Societe et ce pour une duree illimitee.
```

Point ouvert :
- la source fixe `Monsieur` dans la nomination du president, alors que le bloc soussigne utilise `[civilite]`. Une variante feminine ne doit pas etre inventee sans validation.

### 7.12 Article 17 - Exercice social - comptes sociaux

Texte source structurel :

```text
Chaque exercice social a une duree d'une annee, qui commence le {exercice_social.debut} et finit le {exercice_social.fin}.
Par exception, le premier exercice commencera le jour de l'immatriculation de la Societe au Registre du Commerce et des Societes et se terminera le {exercice_social.date_cloture_premier_exercice}.
```

Variables :
- `exercice_social.debut`
- `exercice_social.fin`
- `exercice_social.date_cloture_premier_exercice`

### 7.13 Articles 18 a 23

Blocs fixes :
- Article 18 : affectation et repartition des benefices ;
- Article 19 : capitaux propres inferieurs a la moitie du capital social ;
- Article 20 : exclusion ;
- Article 21 : dissolution - liquidation ;
- Article 22 : transformation de la societe ;
- Article 23 : contestations.

Variables :
- aucune variable source dans ces articles.

Points de vigilance :
- Article 20 contient des cas d'exclusion lies a la SEL ;
- Article 23 prevoit une conciliation confiee au Conseil Departemental de l'Ordre des Medecins.

### 7.14 Article 24 - Condition suspensive

Texte fixe principal :
- constitution realisee sous condition suspensive d'inscription au Tableau de l'Ordre des Medecins ;
- inscription emportant levee automatique de la condition.

Variables :
- aucune variable source dans l'article.

Point ouvert :
- confirmer que la condition suspensive Ordre doit figurer dans tous les statuts SAS cibles.

### 7.15 Article 25 - Ordre professionnel

Texte fixe principal :
- inscription de la SPFPL au Tableau ou sur la liste de l'Ordre professionnel ;
- information annuelle sur la composition du capital social ;
- declaration de changement dans la situation declaree.

Variables :
- aucune variable source dans l'article.

### 7.16 Articles 26 et 27

Blocs fixes :
- Article 26 : frais ;
- Article 27 : jouissance de la personnalite morale et pouvoirs.

Article 27 prevoit :
- annexe des actes accomplis avant signature ;
- reprise des actes a l'immatriculation ;
- pouvoirs du president pour formalites de publicite.

Variables :
- aucune variable source dans ces articles.

## 8. Signature et annexe

Texte source structurel :

```text
Fait a {signature.lieu}
Le

{president.prenom} {president.nom}

Faire preceder de la mention
"Bon pour acceptation des fonctions de President"

ANNEXE
ETAT DES ENGAGEMENTS PRIS AVANT
LA CONSTITUTION DE LA SOCIETE

Ouverture d'un compte bancaire aupres de la Banque.
```

Variables :
- `signature.lieu`
- `signature.date` si le futur rendu decide de renseigner la ligne `Le`
- `president.prenom`
- `president.nom`

Elements manuels :
- mention d'acceptation des fonctions de president ;
- etat des engagements si plus d'un engagement existe.

## 9. Variables texte V1

Variables obligatoires pour un rendu actionnaire unique :
- `societe.denomination`
- `societe.capital_social`
- `societe.capital_social_lettres`
- `societe.nb_actions_total`
- `societe.nb_actions_total_lettres`
- `societe.valeur_nominale_action`
- `societe.valeur_nominale_action_lettres`
- `societe.siege.adresse_affichee`
- `actionnaire_unique.civilite_affichage`
- `actionnaire_unique.prenom`
- `actionnaire_unique.nom`
- `actionnaire_unique.qualification_principale`
- `actionnaire_unique.date_naissance`
- `actionnaire_unique.ville_naissance`
- `actionnaire_unique.departement_naissance`
- `actionnaire_unique.adresse_personnelle_affichee`
- `actionnaire_unique.situation_maritale`
- `actionnaire_unique.regime_matrimonial`
- `actionnaire_unique.nationalite`
- `actionnaire_unique.ordre.departemental`
- `actionnaire_unique.ordre.numero`
- `actionnaire_unique.ordre.numero_rpps`
- `actionnaire_unique.nb_actions`
- `president.ref_associe_index`
- `depot_fonds.banque.nom`
- `exercice_social.debut`
- `exercice_social.fin`
- `exercice_social.date_cloture_premier_exercice`
- `signature.lieu`

Variables conditionnelles ou manuelles :
- `actionnaire_unique.conjoint.civilite_affichage`
- `actionnaire_unique.conjoint.prenom`
- `actionnaire_unique.conjoint.nom`
- `signature.date`
- `signature.mention_president`
- `engagements_preconstitution[]`

## 10. Blocs associes / souscripteurs

### 10.1 Actionnaire unique

La V1 texte ne stabilise qu'un actionnaire unique.

Blocs concernes :
- comparution initiale ;
- apport en numeraire ;
- attribution des actions ;
- nomination du president ;
- signature.

### 10.2 Multi-actionnaires

Non stabilise en V1.

Blocs qui devraient etre specifies avant extension :
- liste des soussignes ;
- apports par actionnaire ;
- repartition des actions ;
- decisions collectives initiales si elles remplacent l'actionnaire unique ;
- signatures multiples ;
- coherence avec la liste des souscripteurs.

### 10.3 Lien avec liste des souscripteurs

La source de verite relie le chemin SAS a l'attestation sur le capital / liste des souscripteurs.

Regle texte :
- le bloc Article 7 des statuts et la liste des souscripteurs doivent presenter les memes donnees de capital ;
- la V1 doit bloquer si les donnees divergent ;
- les plusieurs souscripteurs restent hors automatisation V1.

## 11. Lien avec attestation sur le capital

Document lie, hors presente spec :
- `Attestation sur le capital - apport - liste des souscripteurs.docx`

Champs a partager :
- denomination de la societe ;
- forme / qualite SPFPL si confirmee ;
- capital social ;
- nombre total d'actions ;
- valeur nominale ;
- identite du souscripteur/actionnaire unique ;
- adresse personnelle du souscripteur/actionnaire unique ;
- nombre d'actions souscrites ;
- signature du president ;
- lieu et date de signature.

Decision texte V1 :
- ne pas fusionner l'attestation dans les statuts ;
- ne pas deduire automatiquement une liste multi-souscripteurs depuis les clauses generales des statuts ;
- reutiliser la limite actionnaire unique posee dans les specs SPFPL existantes tant qu'aucun arbitrage SAS specifique n'etend ce point.

## 12. Elements manuels

Les elements suivants doivent rester fournis par saisie dossier controlee, bloc manuel ou arbitrage :
- banque de depot ;
- situation matrimoniale compatible avec la phrase source ;
- regime matrimonial ;
- donnees du conjoint ;
- donnees ordinales ;
- premier exercice social ;
- mention d'acceptation des fonctions de president ;
- engagements pris avant constitution au-dela de l'ouverture du compte bancaire ;
- toute correction ou harmonisation des termes `gerant`, `gerance`, `parts` ou `actions`.

## 13. Regles de blocage texte

Un futur generateur doit bloquer si :
- le dossier n'est pas une SAS / SPFPL medecins confirmee ;
- plusieurs actionnaires ou souscripteurs sont fournis ;
- le president n'est pas l'actionnaire unique ;
- la situation matrimoniale ne correspond pas a la phrase source disponible ;
- les champs ordre medecins sont absents ;
- le capital statuts diverge de l'attestation capital / liste des souscripteurs ;
- le rendu final conserverait un placeholder `[` ou `]` ;
- le rendu final impose une feminisation, une pluralisation ou une correction de vocabulaire non arbitree ;
- le rendu final corrigerait une anomalie source sans note de validation.

## 14. Points ouverts

1. **Validation SAS / SPFPL medecins** : confirmer que ce modele est bien la source SAS cible malgre son contenu SPFPL de medecins.
2. **Actionnaire unique** : confirmer que la V1 statuts SAS reste limitee a un actionnaire unique.
3. **Situation matrimoniale** : definir les variantes admises ou rendre la phrase manuelle.
4. **Civilite president** : la source emploie `Monsieur` dans la nomination du president ; la gestion d'une presidente n'est pas sourcee.
5. **Vocabulaire juridique heterogene** : ne pas corriger `gerant`, `gerance`, `parts sociales` ou autres termes voisins sans validation.
6. **Attestation / liste des souscripteurs** : confirmer que le document lie peut etre reutilise en actionnaire unique pour le chemin SAS.
7. **PV remuneration president** : document satellite du chemin SAS non analyse dans cette spec.
8. **Annexe engagements** : confirmer si l'ouverture de compte bancaire suffit en V1 ou si une liste dynamique est attendue.

## 15. Statut de la spec texte

`SPEC-STATUTS-SAS-001` est stabilise cote texte pour les statuts SAS source Lot 04, sans code Python.

Prochaine etape recommandee :
- revue juridique/metier des points ouverts avant tout ticket de code.
