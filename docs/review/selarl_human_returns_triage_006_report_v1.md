# SELARL human returns triage 006 report V1

Date : 2026-06-02

Ticket : `SELARL-HUMAN-RETURNS-006-TRIAGE-001`

## Amendement 2026-06-03

Le ticket `SELARL-HUMAN-RETURNS-DEEP-AUDIT-006` etait trop confiant. L'audit
incident `SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001` a trouve puis
corrige un ecart restant sur `DOC-002` autorisation de domiciliation :
`pour une duree indeterminee` a ete remplace par `pour 99 ans`.

Source brute :

- `docs/review/selarl_human_returns_006_raw_v1.md`

## Objet

Classer les nouveaux retours humains SELARL recus le 2026-06-02, sans lancer
de developpement non borne.

Ces retours sont concrets. Ils doivent remplacer le mode `attente validation
finale simple` par une boucle de corrections documentaires, puis regeneration
d'un nouveau pack.

## Verdict produit

Verdict : `GO correction tickets bornes`.

Verdict : `NO-GO cloture SELARL simple/regime` tant que ces retours ne sont pas
traites, testes et regenes dans un nouveau pack.

Verdict : `NO-GO question abstraite associe`.

Le retour contient assez d'informations pour ouvrir des tickets de correction.
Il ne faut pas redemander a l'associe de confirmer les points explicitement
formules.

## Impact sur le pack actif

Le pack precedent etait :

- `artifacts/selarl_closing_pack_004/`

Il est remplace apres traitement des retours 006 par :

- `artifacts/selarl_closing_pack_005/`

`SELARL-CANONICAL-CLOSE-001` reste bloque jusqu'a validation finale associe.

## Triage par retour

| ID | Document / zone | Retour humain | Classification | Decision | Ticket recommande |
| --- | --- | --- | --- | --- | --- |
| R006-01 | `DOC-016` / `DOC-017` statuts | Ajouter la mention matrimoniale apres l'identite de l'associe : communaute ou separation de biens avec civilite/prenom/nom conjoint | Ecart concret | Corriger statuts et contexte matrimonial | `SELARL-RETURNS-006-STATUTS-001` |
| R006-02 | `DOC-016` / `DOC-017` article 8 | Accorder le mot `associe` au genre et au nombre des associes | Ecart concret | Ajouter accord genre/nombre teste | `SELARL-RETURNS-006-STATUTS-001` |
| R006-03 | `DOC-016` / `DOC-017` annexe | Placer l'annexe a la page suivante | Ecart layout | Corriger rendu DOCX des statuts | `SELARL-RETURNS-006-STATUTS-001` |
| R006-04 | `DOC-016` / `DOC-017` fin document | Mettre un `-` devant `Ouverture...` a la fin du document | Ecart concret | Corriger bloc final statuts | `SELARL-RETURNS-006-STATUTS-001` |
| R006-05 | `DOC-001` declaration non condamnation | Apres `Ne le {date}`, ajouter `a/au {ville naissance}` | Ecart concret | Ajouter preposition de lieu de naissance | `SELARL-RETURNS-006-DNC-001` |
| R006-06 | Front/moteur pour `DOC-001` | Ajouter une case `au` pour les villes comme `Le Bourget` | Donnee front + moteur | Ajouter champ/preference preposition, repercuter dans DNC | `SELARL-RETURNS-006-DNC-001` |
| R006-07 | `DOC-004` PV nomination gerant | Remplacer l'acronyme de forme juridique par la version redigee sous la denomination et au-dessus du capital | Ecart concret | Afficher forme juridique developpee selon profession | `SELARL-RETURNS-006-PV-001` |
| R006-08 | `DOC-004` PV nomination gerant | Remplacer `Au capital minimum et effectif de 5000 euros` par `Au capital de {capital social}` | Ecart concret | Corriger mention capital PV | `SELARL-RETURNS-006-PV-001` |
| R006-09 | Regle generale adresses | Le code postal doit toujours preceder la ville | Regle transversale | Auditer les formats d'adresse et corriger les sorties SELARL couvertes | `SELARL-RETURNS-006-ADDRESS-SIGNATURE-001` |
| R006-10 | Tous documents | Supprimer tous les encadres de signature | Regle transversale layout | Auditer et supprimer les encadres de signature dans le perimetre SELARL pack | `SELARL-RETURNS-006-ADDRESS-SIGNATURE-001` |
| R006-11 | `DOC-034` demande inscription ordre | Ne plus demander le libelle complet du conseil ; composer `Conseil departemental de l'Ordre des {Profession} de {departement}` | Ecart variable/front | Remplacer variable libelle complet par departement + profession | `SELARL-RETURNS-006-ORDRE-001` |
| R006-12 | `DOC-006` avertissement conjoint | Remplacer l'acronyme par la forme juridique redigee sous denomination et au-dessus du capital | Ecart concret | Corriger bloc societe `DOC-006` | `SELARL-RETURNS-006-CONJOINT-LETTERS-001` |
| R006-13 | `DOC-006` avertissement conjoint | Adresse conjoint identique a associe ; supprimer variable adresse conjoint | Regle front/moteur | Deriver adresse conjoint depuis associe pour `DOC-006` | `SELARL-RETURNS-006-CONJOINT-LETTERS-001` |
| R006-14 | `DOC-005` renonciation | Supprimer la date sous la ville, garder l'espace | Ecart concret | Corriger layout/texte `DOC-005` | `SELARL-RETURNS-006-CONJOINT-LETTERS-001` |
| R006-15 | Variables moteur/front | Supprimer duree sociale, toujours 99 ans | Simplification variable | Supprimer saisie, constante 99 ans | `SELARL-RETURNS-006-FRONT-VARIABLES-001` |
| R006-16 | Front SELARL | Ajouter case sous siege social `identique a l'adresse personnelle` | Reutilisation explicite | Ajouter option de copie adresse personnelle vers siege | `SELARL-RETURNS-006-FRONT-VARIABLES-001` |
| R006-17 | Front SELARL | Ajouter nationalite `portugaise` | Donnee front | Ajouter choix liste | `SELARL-RETURNS-006-FRONT-VARIABLES-001` |
| R006-18 | Variables moteur/front | Supprimer nombre d'exemplaires, mettre 4 par defaut | Simplification variable | Constante 4 exemplaires | `SELARL-RETURNS-006-FRONT-VARIABLES-001` |
| R006-19 | Variables moteur/front | Supprimer qualite renoncee, toujours qualite d'associe | Simplification variable | Constante `associe` | `SELARL-RETURNS-006-FRONT-VARIABLES-001` |
| R006-20 | Variables moteur/front | Supprimer date courrier, toujours date du jour | Simplification variable | Date courrier derivee du jour | `SELARL-RETURNS-006-FRONT-VARIABLES-001` |
| R006-21 | `DOC-003` procuration | Mettre `agissant` en minuscule sur la meme phrase apres l'adresse personnelle | Ecart concret | Corriger wording procuration | `SELARL-RETURNS-006-PROCURATION-001` |

## Tickets recommandes

| Ordre | Ticket | Statut | Perimetre | Critere de sortie |
| --- | --- | --- | --- | --- |
| 1 | `SELARL-RETURNS-006-TRIAGE-001` | DONE | Enregistrer et classer les retours | Fichier brut + rapport de triage + board/last state |
| 2 | `SELARL-RETURNS-006-STATUTS-001` | DONE | `DOC-016` / `DOC-017` statuts | Rapport `docs/review/selarl_returns_006_statuts_001_report_v1.md` ; tests statuts SEL OK |
| 3 | `SELARL-RETURNS-006-DNC-001` | DONE | `DOC-001` + champ front/moteur naissance | Rapport `docs/review/selarl_returns_006_dnc_001_report_v1.md` ; tests DNC/front OK |
| 4 | `SELARL-RETURNS-006-PV-001` | DONE | `DOC-004` PV nomination gerant | Rapport `docs/review/selarl_returns_006_pv_001_report_v1.md` ; tests PV/front OK |
| 5 | `SELARL-RETURNS-006-PROCURATION-001` | DONE | `DOC-003` procuration | Rapport `docs/review/selarl_returns_006_procuration_001_report_v1.md` ; phrase `demeurant..., agissant...` conforme, tests procuration OK |
| 6 | `SELARL-RETURNS-006-CONJOINT-LETTERS-001` | DONE | `DOC-005` / `DOC-006` | Rapport `docs/review/selarl_returns_006_conjoint_letters_001_report_v1.md` ; adresse conjoint derivee, forme juridique redigee, date renonciation retiree, tests regime/front OK |
| 7 | `SELARL-RETURNS-006-ORDRE-001` | DONE | `DOC-034` demande inscription ordre | Rapport `docs/review/selarl_returns_006_ordre_001_report_v1.md` ; tests ordre/front OK |
| 8 | `SELARL-RETURNS-006-FRONT-VARIABLES-001` | DONE | Variables/front SELARL | Rapport `docs/review/selarl_returns_006_front_variables_001_report_v1.md` ; constantes 99 ans / 4 exemplaires / associe / date du jour, nationalite portugaise, reuse siege=adresse perso |
| 9 | `SELARL-RETURNS-006-ADDRESS-SIGNATURE-001` | DONE | Regles transversales SELARL pack | Rapport `docs/review/selarl_returns_006_address_signature_001_report_v1.md` ; CP avant ville et suppression encadres signature controles par tests |
| 10 | `SELARL-CLOSING-PACK-005` | DONE | Pack corrige apres retours 006 | `artifacts/selarl_closing_pack_005/`, manifest 0 echec |
| 11 | `SELARL-HUMAN-RETURNS-DEEP-AUDIT-006` | DONE historique | Audit retours 006 sur pack 005 | Ancien audit amende par l'incident `DOC-002` du 2026-06-03 |

## Points a surveiller

### Forme juridique redigee

Le retour donne l'exemple :

```text
SELARL -> Societe d'exercice liberal a responsabilite limitee de medecin
```

Pour chirurgien-dentiste, la forme redigee devra etre adaptee a la profession
du scenario. Le ticket doit verifier les libelles existants avant modification.

### Adresse du conjoint

Le retour 006 dit explicitement que l'adresse du conjoint est identique a celle
de l'associe. Cette consigne remplace le comportement pack 004 qui demandait une
adresse de conjoint separee pour `DOC-006`.

### Separation de biens

Le retour 006 introduit une situation matrimoniale nouvelle pour les statuts :
marie sous separation de biens. Elle ne genere aucun document supplementaire,
mais elle doit apparaitre dans les statuts.

### Variables supprimees

Les variables suivantes ne doivent plus etre demandees a l'utilisateur dans le
parcours SELARL quand elles sont dans ce perimetre :

- duree sociale ;
- nombre d'exemplaires ;
- qualite renoncee ;
- date courrier ;
- adresse du conjoint pour `DOC-006`.

## Decision de suite

Prochaine action recommandee :

```text
Lancer `SELARL-FINAL-ASSOCIE-VALIDATION-001`.
```

Raison : tous les tickets `SELARL-RETURNS-006-*` issus des retours humains 006
sont maintenant corriges, testes, integres dans le pack 005 et audites cote
Codex. Le prochain risque borne est le retour final de l'associe.

Le developpement doit rester borne : ne pas rouvrir un nouveau sous-cas SELARL
complexe avant validation finale ou ecarts residuels classes.
