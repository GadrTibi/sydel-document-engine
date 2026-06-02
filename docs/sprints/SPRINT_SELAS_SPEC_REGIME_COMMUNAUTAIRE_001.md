# SELAS spec regime communautaire 001

Date : 2026-06-02

Ticket : `SELAS-SPEC-REGIME-COMMUNAUTAIRE-001`

Statut : `DONE - spec documentaire`

Decision sprint : `NO-GO pack`

## Objet

Verrouiller le bloc `regime communautaire` pour le parcours SELAS V1 avant tout
branchement documentaire dans le pack SELAS.

Ce livrable ne code rien, ne modifie aucun generateur, ne genere aucun
DOCX/PDF/ZIP, ne change aucune source DOCX et ne valide aucun wording juridique
nouveau. Il fixe seulement la decision documentaire pour `DOC-005` et `DOC-006`
dans le sprint SELAS.

## Sources et livrables lus

- `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`
- `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md`
- `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`
- `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md`
- `docs/sprints/SPRINT_SELAS_MATRIX_001.md`
- `docs/sprints/SPRINT_SELAS_FRONT_CONTRACT_001.md`
- `docs/sprints/SPRINT_SELAS_TICKETS_001.md`
- `docs/sprints/SPRINT_SELAS_SPEC_PRESIDENT_001.md`
- `docs/sprints/SPRINT_SELAS_SPEC_CAPITAL_ACTIONS_001.md`
- `docs/sprints/SPRINT_SELAS_SPEC_ORDRE_001.md`
- `src/sydel_doc_engine/front_data/selas_schema.py`
- `src/sydel_doc_engine/generators/lot_02/regime_communautaire_common.py`
- `src/sydel_doc_engine/generators/lot_02/lettre_renonciation_associe.py`
- `src/sydel_doc_engine/generators/lot_02/lettre_avertissement_conjoint.py`
- `tests/unit/test_regime_communautaire.py`
- `tests/unit/test_selas_front_schema.py`

Sources DOCX pertinentes deja referencees dans les specs Lot 2 :

- `project/source_documents/lot_02/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx`
- `project/source_documents/lot_02/Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - transforme.docx`

ADR applicables :

- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0005 : mode Codex repo-first.

## Perimetre V1

Inclus :

- structure : `SELAS` ;
- profession active du premier parcours : medecin ;
- creation simple ;
- actionnaire unique ;
- president unique ;
- apport en numeraire dependant de la communaute ;
- conjoint personne physique ;
- regime matrimonial communautaire ;
- documents conditionnels du batch regime communautaire.

Exclus :

- celibataire, PACS, separation de biens ou regime non communautaire ;
- apport en nature ou apport de bien autre qu'une somme en numeraire ;
- plusieurs actionnaires ;
- personne morale actionnaire ;
- micro-holding ;
- actions de preference ;
- droits financiers ou droits de vote derogatoires ;
- cession de fonds ou cabinet ;
- SCM ;
- site distinct ou derogation ;
- directeur general ;
- variation de wording non sourcee comme `ma conjointe`, `future`, ou
  feminisation automatique de la fonction.

## Condition d'apparition

Le bloc regime communautaire SELAS n'apparait que si :

```text
dossier.structure = SELAS
dossier.options.regime_communautaire = true
```

En parcours simple sans regime communautaire, aucun document du batch ne doit
etre attendu ni genere.

## Decision documentaire

Le batch regime communautaire SELAS couvre deux documents conditionnels :

| Code | Document | Decision SELAS V1 |
| --- | --- | --- |
| `DOC-005` | Lettre de renonciation a revendiquer la qualite d'associe | Candidat conditionnel SELAS si regime communautaire. |
| `DOC-006` | Lettre d'avertissement au conjoint en cas d'apport d'un bien commun | Candidat conditionnel SELAS si regime communautaire, a sortir de la reserve front apres GO borne. |

Decision :

- `DOC-005` et `DOC-006` sont un batch conditionnel pour SELAS ;
- la source Lot 2 / SELAS / SPFPL comparee dans les specs couvre les deux
  lettres ;
- le futur dev ne doit pas activer seulement `DOC-005` si le parcours produit
  un dossier regime communautaire complet ;
- la sortie de reserve de `DOC-006` est autorisee en spec, mais demande un futur
  `GO dev` borne et des tests front/schema ;
- aucun pack SELAS complet n'est active par cette decision.

## Roles et donnees obligatoires

### Roles

| Role | Statut V1 | Note |
| --- | --- | --- |
| `apporteur` | Obligatoire | En SELAS simple, pointe vers le praticien / actionnaire unique / President par reuse explicite. |
| `conjoint` | Obligatoire | Signataire de la renonciation et destinataire de l'avertissement. |
| `societe_principale` | Obligatoire | SELAS en constitution. |
| `president` | Contexte dossier | Porte la fonction dirigeante si elle est affichee dans l'avertissement. |
| `signataire` | Par document | Apporteur pour l'avertissement, conjoint pour la renonciation. |

### Donnees minimales

- `dossier.structure = SELAS`
- `dossier.options.regime_communautaire = true`
- `societe.denomination`
- `societe.forme_sociale`
- `societe.forme_sociale_complete`
- `societe.forme_sociale_abregee = SELAS`
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
- `apporteur.fonction_dirigeant`
- `conjoint.civilite_affichage`
- `conjoint.prenom`
- `conjoint.nom`
- `conjoint.adresse.num_voie`
- `conjoint.adresse.voie`
- `conjoint.adresse.cp`
- `conjoint.adresse.ville`
- `regime_communautaire.avertissement.date_signature`
- `regime_communautaire.renonciation.lieu_signature`
- `regime_communautaire.renonciation.date_signature`
- `regime_communautaire.date_courrier_avertissement`
- `regime_communautaire.regime_matrimonial`
- `regime_communautaire.qualite_renoncee`
- `regime_communautaire.renonciation.nombre_exemplaires_lettres`

## Valeurs SELAS attendues

Pour SELAS V1 simple :

- `societe.forme_sociale_abregee` : `SELAS` ;
- `societe.forme_sociale_complete` : valeur source/statuts SELAS, sans
  transformation SELARL automatique ;
- `apporteur.fonction_dirigeant` : `president` ou libelle source valide ;
- `regime_communautaire.qualite_renoncee` : `actionnaire`, sauf decision
  juridique contraire ;
- `regime_communautaire.regime_matrimonial` : valeur affichee du regime, par
  exemple `communaute` / `communauté` selon normalisation deja documentee.

Point sensible :

- la source conserve le titre objet `qualite d'associe` dans `DOC-005` ;
- le champ variable `qualite_renoncee` doit porter le terme documentaire adapte
  a la SELAS, donc `actionnaire` pour le parcours cible ;
- ne pas faire de remplacement global `associe -> actionnaire`.

## Regles de generation futures

Un futur ticket code devra :

1. garder `DOC-005` et `DOC-006` comme documents canoniques distincts ;
2. selectionner les deux documents seulement si l'option regime communautaire
   est vraie ;
3. passer `dossier.structure = SELAS` au batch ;
4. utiliser l'overlay SELAS / SPFPL pour la mention manuscrite de
   l'avertissement ;
5. exiger `societe.forme_sociale_abregee` pour SELAS ;
6. rendre la mention manuscrite comme instruction imprimee, sans la simuler ;
7. rendre `qualite_renoncee` tel que fourni, sans deduction silencieuse ;
8. bloquer si le conjoint est absent ;
9. bloquer si l'apport est absent ou non numerique/affichable ;
10. bloquer si `qualite_renoncee` est absente ;
11. bloquer si la date du courrier d'avertissement ne peut pas etre resolue ;
12. verifier l'absence de placeholders source `[` / `]`.

Le futur code ne doit pas :

- inventer une variante feminine non sourcee ;
- changer `mon conjoint` en `ma conjointe` ;
- changer `futur` en `future` ;
- modifier le texte source `alinea 1 er` ;
- automatiser un apport en nature ;
- activer le pack SELAS complet.

## Impact front/data

Le schema SELAS actuel :

- ajoute `DOC-005` comme candidat quand `regime_communautaire=True` ;
- garde `DOC-006` en reserve avec statut `NOT_IMPLEMENTED`.

Decision spec :

- `DOC-005` reste candidat conditionnel ;
- `DOC-006` doit passer de reserve a candidat conditionnel dans un futur ticket
  front/data ou document, car la source SELAS est qualifiee par les specs Lot 2 ;
- le statut de readiness du batch doit rester `context_incomplete` tant que les
  donnees conjoint/apport/regime ne sont pas completes ;
- le front doit afficher clairement que ces documents ne concernent que le cas
  marie sous regime communautaire.

## Cas bloques

Bloquer le batch SELAS regime communautaire si :

- `regime_communautaire` est faux ou absent ;
- le regime matrimonial n'est pas communautaire ;
- le conjoint est absent ;
- l'adresse du conjoint manque pour `DOC-006` ;
- le prenom du conjoint manque pour `DOC-005` ;
- l'apport commun manque ;
- la qualite renoncee manque ;
- la forme sociale abregee manque pour SELAS ;
- le dossier demande un apport en nature ;
- le dossier contient plusieurs actionnaires, micro-holding, actions de
  preference, SCM, cession ou site distinct.

## Criteres d'acceptation d'un futur ticket code

Un futur ticket `SELAS-DOC005-DOC006-REGIME-COMMUNAUTAIRE-001` sera acceptable
si :

- un contexte SELAS avec regime communautaire rend `DOC-005` et `DOC-006`
  candidats ;
- un contexte SELAS sans regime communautaire ne rend ni `DOC-005` ni
  `DOC-006` candidats ;
- `DOC-006` n'est plus reserve dans le schema SELAS lorsque l'option est vraie ;
- les documents generes ne contiennent pas de placeholder source ;
- `DOC-005` utilise `qualite_renoncee = actionnaire` pour le parcours SELAS ;
- `DOC-006` rend la mention manuscrite `a la SELAS {denomination}` ;
- les blocages sur conjoint, apport, qualite renoncee et forme abregee SELAS
  sont testes ;
- aucun autre document SELAS n'est active par accident.

## Decision de sortie

`SELAS-SPEC-REGIME-COMMUNAUTAIRE-001` est suffisant pour autoriser une demande
de `GO dev` borne sur :

```text
SELAS-DOC005-DOC006-REGIME-COMMUNAUTAIRE-001
```

Ce futur ticket devra rester limite au batch regime communautaire SELAS
conditionnel. Il ne devra pas activer le pack SELAS complet.

Prochaine action recommandee : demander a Gad un `GO dev` borne sur
`SELAS-DOC034-ORDRE-001` ou
`SELAS-DOC005-DOC006-REGIME-COMMUNAUTAIRE-001`, ou relancer les validations
outillees des tickets deja codes.
