# TRACK-B-SELARL-DENTIST-LINE-BY-LINE-LOCK-003 - Rapport V1

## Amendement 2026-06-03

Ce rapport est historique. Le verrou `DOC-002` ci-dessous utilisait l'ancien
libelle `pour une duree indeterminee`. Le retour humain 006 a ensuite remplace
ce libelle par `pour 99 ans`. La source active pour `DOC-002` est maintenant :

- `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md`
- `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`

## Contexte prouvé

- `pwd` : `C:\Users\Gad\Desktop\Sydel\sydel-track-b`
- `git rev-parse --show-toplevel` : `C:/Users/Gad/Desktop/Sydel/sydel-track-b`
- `git branch --show-current` : `track-b/clean-rebuild`
- `git status --short --branch` : worktree déjà modifiée par les tickets Track B SELARL précédents, aucun reset effectué.

## Source de comparaison

Le message du ticket `003` annonce un bloc humain complet collé dans le ticket, mais aucun nouveau bloc texte n'est présent dans le message reçu. La référence opérationnelle utilisée est donc le fichier humain déjà fourni et disponible localement :

- `C:\Users\Gad\Downloads\Retours humains .docx`

Méthode de contrôle :

- génération d'un smoke SELARL chirurgien-dentiste avec `1000` parts pour correspondre à l'exemple humain `mille / 1000` ;
- extraction du bloc humain `ARTICLE 1` à `ARTICLE 34` depuis le DOCX humain ;
- substitution des variables humaines par les valeurs du smoke ;
- comparaison paragraphes à paragraphes après normalisation des espaces et espaces insécables ;
- contrôle complémentaire des documents courts sur les formulations humaines ciblées.

Smoke de comparaison :

- dossier : `artifacts/line_lock_003_compare`
- ZIP : `artifacts/line_lock_003_compare/dossier_generation.zip`
- DOCX produits : 7
- placeholders résiduels : aucun
- segments parasites `RCS PARIS 788 531 432` / `0153814303` : aucun dans le pack généré

## Synthèse

| Document | Statut | Décision |
|---|---|---|
| DOC-002 Autorisation de domiciliation | LOCKED | Formulation humaine exacte intégrée sur l'adresse siège/cabinet. |
| DOC-001 Déclaration de non-condamnation | LOCKED | Adresse personnelle au format humain `num voie, cp ville`. |
| DOC-005 Lettre de renonciation | LOCKED | `À {ville}`, `communauté`, absence de RCS parasite, clause finale présente. |
| DOC-003 Procuration | LOCKED | Point humain anciennement OPEN fermé : suppression RCS/téléphone SYDEL et ajout de la clause après le mandat. |
| DOC-004 PV nomination gérant | LOCKED | Corrections humaines fermées, y compris l'introduction `Les associés...` et le singulier `Nomination du gérant`. |
| DOC-016 Statuts SELARL chirurgien-dentiste | LOCKED sur articles 1 à 34 | 243 paragraphes humains comparés, 243 paragraphes générés, 0 écart article. |

## DOC-002 - Autorisation de domiciliation

Référence humaine attendue :

```text
dans les locaux du cabinet au [num_voie_siege] [voie_siege], [cp_siege] [ville_siege] pour une durée indéterminée.
```

Rendu généré actuel :

```text
Je soussigné Monsieur Jean Martin autorise la domiciliation de la Société SELARL MARTIN au capital de 1000 € en cours de formation, dans les locaux du cabinet au 20 avenue du Siege, 75002 Paris pour une durée indéterminée.
```

Écarts restants : aucun sur la formulation ciblée.

Décision prise : conserver le mapping sur `societe.siege`.

Statut : LOCKED.

## DOC-001 - Déclaration de non-condamnation

Référence humaine attendue :

```text
demeurant au [num_voie_perso] [voie_perso], [cp_perso] [ville_perso]
```

Rendu généré actuel :

```text
demeurant au 10 rue Test, 75001 Paris
```

Écarts restants : aucun sur la formulation ciblée.

Décision prise : conserver la virgule avant le code postal.

Statut : LOCKED.

## DOC-005 - Lettre de renonciation

Références humaines attendues :

```text
À {ville}
euros dépendant de notre communauté
Fait pour servir et valoir ce que de droit.
```

Rendu généré actuel :

```text
À Paris
Par courrier en date du 20/05/2026, tu m’as fait part du projet de constitution de la société SELARL MARTIN, societe d'exercice liberal a responsabilite limitee, à laquelle tu souhaites t'associer en apportant 1000 (mille) euros dépendant de notre communauté.
Fait pour servir et valoir ce que de droit.
```

Écarts restants : aucun sur les corrections humaines ciblées.

Décision prise : `regime_communautaire.regime_matrimonial` est normalisé en `communauté` quand la donnée contient une forme de `communaute`.

Statut : LOCKED.

## DOC-003 - Procuration

Références humaines attendues :

```text
Supprimer “RCS PARIS 788 531 432 0153814303”.
Rajoute : “Fait pour servir et valoir ce que de droit.”
Juste après “L’exécution de ce mandat vaudra décharge au mandataire.”
```

Rendu généré actuel :

```text
SYDEL
80 avenue Marceau, 75008 PARIS
L’exécution de ce mandat vaudra décharge au mandataire.
Fait pour servir et valoir ce que de droit.
```

Écarts restants : aucun pour le segment humain identifié.

Décision prise : ce point n'est plus classé hors scope ; il vise bien `DOC-003` car la phrase de mandat y existe. Les lignes RCS/téléphone ont été retirées du bloc mandataire.

Statut : LOCKED.

## DOC-004 - PV de nomination de gérant

Références humaines attendues :

```text
Les associés de la SELARL [denomination_societe], au capital de [capital_social], composé de [nb_parts] parts de [valeur_nominale_part] euro chacune, se sont réunis au siège social.
Sont présents ou représentés :
[civilite_president_seance] [prenom_president_seance] [nom_personne_seance] préside la séance.
Le président rappelle l’ordre du jour :
· Nomination du gérant
· Pouvoirs
Cette résolution est adoptée à l’unanimité
```

Rendu généré actuel :

```text
Les associés de la SELARL SELARL MARTIN, au capital de 1000, composé de 1000 parts de 1 euro chacune, se sont réunis au siège social.
Sont présents ou représentés :
- Monsieur Jean Martin, détenant 1000 parts,
Monsieur Jean Martin préside la séance.
Le président rappelle l’ordre du jour :
· Nomination du gérant
· Pouvoirs
Cette résolution est adoptée à l’unanimité
L’assemblée générale confère tous les pouvoirs au porteur d’un original à l’effet de procéder aux formalités d’enregistrement au greffe du Tribunal de Commerce de la Société.
```

Écarts restants : aucun sur les corrections humaines ciblées.

Décision prise :

- la phrase d'introduction reste au pluriel même pour l'associé unique, conformément au texte humain ;
- le singulier est conservé uniquement pour `Nomination du gérant` en dossier unipersonnel ;
- les variables de président de séance sont dérivées de l'associé unique dans le clean front.

Statut : LOCKED.

## DOC-016 - Statuts SELARL chirurgien-dentiste

Référence humaine attendue :

- bloc articles complet du DOCX humain, de `ARTICLE 1 – FORME` à `ARTICLE 34 - CONVENTION SUR LA PREUVE – SIGNATURE ELECTRONIQUE` ;
- variables entre crochets substituées par les valeurs du contexte smoke.

Rendu généré actuel :

- bloc généré depuis `statuts_selarl_chirurgien_dentiste.docx`, de `ARTICLE 1 – FORME` à la fin de l'article 34 ;
- comparaison paragraphes à paragraphes :
  - paragraphes humains attendus : 243 ;
  - paragraphes générés : 243 ;
  - écarts : 0.

Points spécifiquement vérifiés :

- `Au capital de 1000 euros` : conforme ;
- `marié sous le régime de la communauté avec` : conforme pour une donnée `regime de communaute` ;
- Article 5 lieu d'exercice unique : conforme ;
- Articles 7 / 8 apports et capital social : conformes ;
- Articles 9 / 10 qualité d'associé et capital : conformes ;
- Article 15 et suivants transmission / exclusion / sanctions / cessation : conformes au bloc humain ;
- Articles 19 à 34 gouvernance, assemblées, procès-verbaux, comptes, pouvoirs, signature électronique : conformes au bloc humain ;
- `[prestataire_signature_electronique]` rendu par `Yousign` : conforme.

Écarts restants :

- OPEN GAP de périmètre uniquement : le bloc humain fourni commence à l'article 1 et s'arrête à l'article 34. Le générateur conserve ensuite les blocs de signature et d'annexe hérités de la spec statuts existante. Ils ne sont ni confirmés ni interdits par le bloc humain d'articles.

Décision prise :

- verrouiller strictement les articles 1 à 34 ;
- conserver les signatures/annexes existantes faute de consigne humaine explicite de suppression.

Statut : LOCKED sur les articles 1 à 34 ; OPEN GAP limité au wrapper post-article.

## Variables / mappings

Variables nouvelles ajoutées dans les tickets SELARL précédents et vérifiées ici :

- `civilite_president_seance`
- `prenom_president_seance`
- `nom_personne_seance`
- `nb_parts_total_lettres`

Mapping confirmé :

- `[nb_parts]` humain du PV : `capital.nb_parts_total`
- `[nb_parts_total]` statuts : `capital.nombre_titres_total` ou `capital.nb_parts_total`
- `[nb_parts_total_lettres]` : `capital.nombre_titres_total_lettres`
- `[prestataire_signature_electronique]` : `signature.prestataire_signature_electronique`

## Contrôles exécutés

- Tests ciblés documents SELARL courts + statuts + clean front : OK, 63 tests passés.
- `ruff check .` : OK.
- Smoke DOCX/ZIP dentiste : OK dans `artifacts/line_lock_003_compare`.
- Contrôle texte smoke : aucun placeholder résiduel, aucun segment parasite RCS/téléphone SYDEL.
- Clean front Track B : HTTP 200 sur `http://localhost:8523`, PID `13164`, processus arrêté proprement.

## Statuts finaux

- LOCKED : DOC-001, DOC-002, DOC-003, DOC-004, DOC-005.
- LOCKED article par article : DOC-016 articles 1 à 34.
- OPEN GAP : wrapper post-article DOC-016, car non présent dans la référence humaine disponible.
