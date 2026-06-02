# SELAS front contract 001

Date : 2026-06-01

Ticket : `SELAS-FRONT-CONTRACT-001`

Statut : `DONE - cadrage lecture seule`

Decision sprint : `NO-GO dev`

## Objet

Definir le contrat metier-front provisoire du sprint SELAS, a partir de :

- `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` ;
- `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md` ;
- `docs/sprints/SPRINT_SELAS_MATRIX_001.md` ;
- les registres globaux de roles, adresses et variables ;
- le contrat SELARL Track B, utilise comme methode seulement.

Ce contrat ne modifie pas l'UI, ne modifie aucun generateur, ne modifie aucune
source DOCX et ne valide aucun wording juridique.

## Promesse produit visible cible

Le futur front SELAS ne doit promettre que ceci :

> Preparer un dossier de creation de SELAS medecin simple, avec actionnaire
> unique et president unique, en affichant les documents candidats, les
> documents reserves et les cas complexes bloques, sans generer tant que les
> specs et le `GO dev` ne sont pas donnes.

Le front ne doit pas promettre :

- une SELAS chirurgien-dentiste tant que la source statuts dentiste SELAS n'est
  pas identifiee ;
- une SELAS multi-actionnaires ;
- une nomination de directeur general ;
- une micro-holding ou des actions de preference ;
- une cession de fonds ou de cabinet automatisee ;
- une cession SCM automatisee dans le premier parcours ;
- une derogation ou un site distinct automatise ;
- une generation juridique validee avant arbitrage Gad.

## Perimetre exact du parcours candidat

Inclus en cadrage :

- structure : `SELAS` ;
- profession : `medecin` uniquement pour le premier parcours candidat ;
- creation simple ;
- actionnaire unique ;
- president unique ;
- signataire principal rattache au president ;
- mandataire formalites distinct ;
- siege social ;
- lieu d'exercice principal ;
- capital divise en actions ;
- ordre professionnel ;
- regime communautaire comme option conditionnelle a arbitrer.

Exclus du parcours candidat :

- `chirurgien_dentiste` tant que la source de statuts SELAS dentiste manque ;
- plus d'un actionnaire ;
- personne morale associee ou micro-holding ;
- actions de preference ou droits financiers/votes derogatoires ;
- directeur general ;
- cession fonds/cabinet ;
- SCM ;
- derogation ;
- site distinct ;
- `DOC-006` en generation automatique.

## Documents candidats et decisions front

| Document | Code | Condition front | Statut front candidat | Blocage avant dev |
| --- | --- | --- | --- | --- |
| Declaration de non-condamnation du president | `DOC-001` | Toujours | Candidat `reuse-check` | Confirmer filiation et fonction president |
| Autorisation de domiciliation | `DOC-002` | Toujours | Candidat `reuse-check` | Confirmer neutralite SELAS |
| Procuration president | `DOC-003` | Toujours | Candidat `adapter` | Spec wording president obligatoire |
| Decision / PV nomination president | A definir, proche `DOC-004` | Toujours | Candidat `adapter` | Spec canonique SELAS president obligatoire |
| Demande d'inscription a l'Ordre | `DOC-034` | Toujours | Candidat `reuse-check` | Confirmer pieces ordinales et overlay SELAS |
| Statuts SELAS medecin | `DOC-018` | Profession = medecin | Candidat `adapter` | Lock source/spec SELAS associe unique |
| Lettre renonciation conjoint | `DOC-005` | Regime communautaire = oui | Candidat `reuse-check` | Arbitrer effet juridique SELAS |
| Lettre avertissement conjoint | `DOC-006` | Regime communautaire = oui | Reserve | Decision explicite requise |
| Statuts SELAS dentiste | A definir | Profession = chirurgien-dentiste | Bloque | Source DOCX manquante |
| Attestation depot capital / liste souscripteurs | A definir | Capital SELAS | Reserve | Document canonique exact a identifier |
| Plans locaux / devis materiel | Hors `DOC-XXX` | Selon Ordre | Piece attendue / reserve | Caractere bloquant UI a arbitrer |

## Parcours de saisie cible

### 1. Qualification

Champs :

- type de dossier : `SELAS` ;
- profession : `medecin` dans le premier parcours candidat ;
- actionnaire unique : oui obligatoire pour le parcours candidat ;
- president unique : oui obligatoire pour le parcours candidat ;
- regime communautaire : oui / non ;
- cession : oui / non ;
- SCM : oui / non ;
- derogation : oui / non ;
- site distinct : oui / non ;
- directeur general : non, bloque ;
- micro-holding / personne morale associee : non, bloque ;
- actions de preference : non, bloque.

Regles :

- si profession = chirurgien-dentiste, bloquer le pack candidat tant que la
  source statuts SELAS dentiste manque ;
- si actionnaire unique = non, bloquer le pack candidat ;
- si directeur general = oui, bloquer le pack candidat ;
- si micro-holding ou actions de preference = oui, bloquer le pack candidat ;
- si cession, SCM, derogation ou site distinct = oui, afficher les documents ou
  pieces attendues mais bloquer la generation automatique du premier parcours.

### 2. Fiche Client / Praticien

Champs :

- civilite d'affichage ;
- genre grammatical ;
- prenom ;
- nom ;
- date de naissance ;
- ville et departement de naissance ;
- nationalite ;
- adresse personnelle ;
- profession reglementee ;
- numero RPPS ;
- numero d'inscription a l'Ordre si disponible ;
- ordre departemental / ville d'ordre ;
- telephone portable pour signature ;
- email de signature.

Champs a confirmer avant dev :

- filiation complete pour `DOC-001` ;
- numero de securite sociale, cite NotebookLM mais pas rattache aux documents
  candidats dans cette matrice.

### 3. Roles personnes

Roles explicites :

- `personne.praticien` ;
- `personne.actionnaire_unique` ;
- `personne.president` ;
- `personne.signataire` ;
- `personne.mandataire` ;
- `personne.conjoint` si regime communautaire.

Regles de reutilisation :

- en dossier unipersonnel uniquement, le praticien peut alimenter actionnaire
  unique, president et signataire ;
- le role president reste distinct du role actionnaire, meme si la fiche cible
  est la meme ;
- le mandataire reste distinct du signataire ;
- le conjoint reste une fiche separee ;
- aucune fusion silencieuse n'est autorisee hors regle explicite.

### 4. Societe SELAS

Champs :

- denomination sociale ;
- forme sociale complete : SELAS a confirmer selon source statuts ;
- forme sociale abregee : SELAS ;
- objet / profession ;
- fiscalite si le futur parcours la conserve ;
- date de cloture d'exercice ;
- duree de la societe si consommee par les statuts ;
- ville RCS si consommee par les documents candidats.

Regles :

- le libelle juridique exact de la forme sociale doit venir des statuts/source,
  pas d'une transformation SELARL ;
- aucune mention SELARL ne doit apparaitre dans un parcours SELAS.

### 5. Adresses

Adresses a modeliser :

- domicile du praticien ;
- siege social de la SELAS ;
- lieu d'exercice principal ;
- adresse du conseil de l'Ordre ;
- adresse de banque de depot, si le document capital/statuts la consomme.

Regles :

- domiciliation = siege social seulement si cette regle est confirmee pour
  `DOC-002` SELAS ;
- siege social = lieu d'exercice seulement via option explicite ;
- lieu d'exercice principal ne doit pas creer automatiquement un site distinct ;
- adresse d'Ordre et adresse de banque restent des adresses de tiers.

### 6. Capital / actions

Champs :

- capital social en chiffres ;
- capital social en lettres ;
- nombre total d'actions ;
- valeur nominale d'une action ;
- apport en numeraire ;
- apport en lettres ;
- banque de depot : nom ;
- banque de depot : adresse si requise ;
- repartition des actions : actionnaire unique dans le premier parcours ;
- numerotation des actions : champ ou calcul a arbitrer.

Regles :

- le type de titre est `actions`, pas `parts sociales` ;
- controle : capital = nombre total d'actions x valeur nominale ;
- en V1 candidat, toutes les actions sont attribuees a l'actionnaire unique ;
- pas d'actions de preference ;
- pas de droits de vote ou droits financiers derogatoires ;
- pas de numerotation automatique tant que l'arbitrage n'est pas donne.

### 7. Ordre et pieces

Champs :

- profession ordinale affichee ;
- profession ordinale plurielle ;
- conseil departemental de l'Ordre ;
- adresse du conseil ;
- numero RPPS ;
- numero d'ordre ;
- mandataire formalites : civilite, prenom, nom, fonction, cabinet ;
- plans des locaux : piece attendue a qualifier ;
- devis materiel : piece attendue a qualifier.

Regles :

- le mandataire peut etre preconfigure mais doit rester modifiable ou explicite ;
- plans/devis doivent etre visibles comme pieces attendues si l'Ordre les exige ;
- le caractere bloquant des plans/devis reste une question ouverte.

### 8. Regime communautaire

Champs conditionnels :

- statut matrimonial ;
- regime matrimonial ;
- prenom/nom du conjoint ;
- adresse du conjoint si requise par source ;
- montant/apport commun si le document le consomme ;
- lieu/date de signature de la renonciation.

Regles :

- `DOC-005` est candidat `reuse-check` ;
- `DOC-006` reste reserve ;
- le front ne doit pas affirmer que le mecanisme conjoint SELARL s'applique
  juridiquement a la SELAS sans arbitrage.

### 9. Signature

Champs :

- lieu de signature ;
- date de signature ;
- email du signataire ;
- telephone portable du signataire ;
- prestataire de signature electronique si les statuts le consomment ;
- mandataire interne SYDEL si requis.

Regles :

- les donnees email/telephone servent au flux de signature, pas forcement au
  wording documentaire ;
- une date par defaut peut etre proposee, mais le document doit garder sa date
  explicite.

## Blocages visibles attendus

| Cas | Message fonctionnel cible |
| --- | --- |
| Profession chirurgien-dentiste | `Les statuts SELAS chirurgien-dentiste ne sont pas encore sources dans le sprint. Generation bloquee.` |
| Plusieurs actionnaires | `La SELAS multi-actionnaires exige des statuts, votes et accords non verrouilles. Hors V1 simple.` |
| Directeur general | `La nomination d'un Directeur General n'est pas sourcee pour la V1 SELAS. Hors perimetre.` |
| Micro-holding / personne morale | `Le cas micro-holding est distinct et requiert un ticket dedie. Hors V1 simple.` |
| Actions de preference | `Les actions de preference et droits derogatoires sont hors V1 simple.` |
| Cession fonds/cabinet | `La cession de fonds ou cabinet demande une redaction personnalisee. Preparation manuelle ou ticket dedie requis.` |
| SCM | `La cession SCM dispose de sources, mais demande un sous-parcours dedie. Hors V1 simple.` |
| Derogation/site distinct | `Le document est attendu ou conditionnel, mais reste manuel ou reserve dans le parcours SELAS simple.` |
| `DOC-006` | `La lettre d'avertissement conjoint reste reservee tant que la decision SELAS n'est pas explicite.` |
| Numerotation actions | `La numerotation des actions doit etre arbitree avant automatisation.` |

## Readiness par bloc

| Bloc | Statut | Raison |
| --- | --- | --- |
| Qualification | `READY cadrage` | Perimetre simple clair |
| Fiche praticien | `READY cadrage` | Champs proches SELARL/global |
| Roles president/actionnaire | `READY cadrage` | Role distinct documente, wording a specifier |
| Societe SELAS | `READY cadrage` | Forme SELAS connue, libelle exact a verrouiller |
| Capital/actions | `PARTIAL` | Numerotation actions et attestation capital ouvertes |
| Ordre | `PARTIAL` | `DOC-034` candidat, plans/devis et lock humain ouverts |
| Regime communautaire | `PARTIAL` | `DOC-005` candidat, `DOC-006` reserve |
| Documents complexes | `BLOCKED` | Cession, SCM, derogation, multi-actionnaires, DG, micro-holding |

## Questions ouvertes avant tickets

1. Gad valide-t-il le premier parcours candidat `SELAS medecin associe unique`
   seulement ?
2. Faut-il creer un ticket de spec dedie pour `Decision / PV nomination
   president SELAS` avant tout code ?
3. La procuration doit-elle etre adaptee par parametre de fonction ou par
   document SELAS separe ?
4. La DNC president doit-elle exiger la filiation complete ?
5. La numerotation des actions doit-elle etre calculee ou saisie ?
6. Les plans/devis Ordre sont-ils bloquants ?
7. `DOC-006` reste-t-il reserve ?

## Decision de sortie

`SELAS-FRONT-CONTRACT-001` est suffisant pour preparer les tickets de sprint en
lecture seule.

Prochaine etape recommandee : `SELAS-TICKETS-001`, sans `GO dev`.
