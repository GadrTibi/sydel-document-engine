# Cadrage métier — Lot 2 — Batch régime communautaire V1

## Position dans le projet

Ticket : `ANALYSE-ORDRE-001`.

Ce document cadre le batch documentaire composé de deux lettres liées au régime communautaire :

1. lettre de renonciation à revendiquer la qualité d'associé ;
2. lettre d'avertissement au conjoint en cas d'apport d'un bien commun.

Ce cadrage ne vaut pas spec canonique codable et ne déclenche aucun développement Python.

## Sources lues

Le ticket mentionne les fichiers sources suivants :

- `project/source_documents/lot_02/Lettre de renonciation a revendiquer la qualite d'associe.docx`
- `project/source_documents/lot_02/Lettre d'avertissement au conjoint en cas d'apport d'un bien commun.docx`

Ces chemins n'existent pas littéralement dans le dépôt au moment de l'analyse. Les sources Lot 2 correspondantes réellement présentes et lues en lecture seule sont :

- `project/source_documents/lot_02/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx`
- `project/source_documents/lot_02/Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - transforme.docx`

Référentiels projet lus avant analyse :

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`

ADR applicables :

- `docs/adr/0001-source-of-truth.md`
- `docs/adr/0002-engine-per-document.md`
- `docs/adr/0003-lot-based-delivery.md`
- `docs/adr/0005-codex-working-mode.md`

## État du pipeline documentaire

| Étape | Statut | Note |
|---|---|---|
| Inventorié | Oui | Le bloc régime communautaire est visible dans l'arbre document-centré V1. |
| Validé | À confirmer | Le cadrage ne vaut pas validation métier finale. |
| Source reçue | Oui | Deux sources DOCX présentes dans `project/source_documents/lot_02/`. |
| Analysé | Oui | Présent cadrage. |
| Spécifié | Non | À formaliser dans `SPEC-RC-001`. |
| Codé | Non | Aucun code à ce stade. |
| Testé | Non | Non applicable avant spec/code. |
| Validé | Non | Validation humaine à obtenir après spec et rendu. |

## Analyse document 1 — Lettre de renonciation à revendiquer la qualité d'associé

### Structure observée

La lettre est rédigée par le conjoint qui renonce à revendiquer la qualité d'associé. Elle est adressée à la personne qui projette de constituer la société et d'apporter un bien ou une somme dépendant du régime matrimonial.

Structure :

1. lieu de signature ;
2. date de signature ;
3. objet ;
4. destinataire ;
5. rappel du courrier reçu et du projet de constitution ;
6. renonciation à la qualité d'associé ;
7. consentement à l'apport effectué par le conjoint ;
8. nombre d'exemplaires ;
9. signature du conjoint renonçant.

### Texte fixe

Blocs fixes observés, hors placeholders :

- `Objet : Lettre de renonciation à revendiquer la qualité d'associé`
- rappel d'un courrier reçu ;
- annonce du projet de constitution de société ;
- annonce d'un apport dépendant du régime matrimonial ;
- notification de l'intention de renoncer à la faculté de devenir personnellement associé de la société ;
- déclaration de consentement à l'apport effectué par le conjoint ;
- formule `En ... exemplaires`.

La lettre utilise le tutoiement : `tu m’as fait part`, `Je te notifie`.

### Variables / zones variables

| Placeholder source | Rôle canonique candidat | Type | Note de cadrage |
|---|---|---|---|
| `[lieu_signature]` | `signature.lieu` | existant | Lieu de signature de la lettre de renonciation. |
| `[date_signature]` | `signature.date` | existant | Date de signature de la lettre de renonciation. |
| `[civilite]` | `apporteur.civilite_affichage` ou rôle à nommer | nouveau rôle | Destinataire de la lettre, probablement conjoint apporteur / futur associé. |
| `[prenom]` | `apporteur.prenom` ou rôle à nommer | nouveau rôle | Destinataire. |
| `[nom]` | `apporteur.nom` ou rôle à nommer | nouveau rôle | Destinataire. |
| `[date_courrier]` | `regime_communautaire.date_courrier_avertissement` | nouveau | Date du courrier d'avertissement reçu ; relation à `signature.date` à préciser. |
| `[denomination_societe]` | `societe.denomination` | existant | Société en constitution. |
| `[forme_sociale_complete]` | `societe.forme_complete` | à confirmer | Forme longue de la société. |
| `[apport_personne_1]` | `apport.montant` | nouveau / commun | Montant de l'apport, affiché ici avant le montant en lettres. |
| `[apport_lettres_personne_1]` | `apport.montant_lettres` | nouveau / commun | Montant en lettres. |
| `[regime_matrimonial]` | `regime_communautaire.regime_matrimonial` | nouveau | Exemple attendu : communauté ; à valider. |
| `[qualite_associe]` | `regime_communautaire.qualite_renoncee` | nouveau | Doit gérer au moins associé/associée/actionnaire si applicable. |
| `[nombre_exemplaires_lettres]` | `document.nombre_exemplaires_lettres` | local | Nombre d'exemplaires en lettres. |
| `[prenom_conjoint]` | `conjoint.prenom` | nouveau rôle | Signataire de la renonciation. |
| `[nom_conjoint]` | `conjoint.nom` | nouveau rôle | Signataire de la renonciation. |

### Accords de genre / nombre

Accords ou variantes à arbitrer avant spec :

- `[qualite_associe]` doit porter la bonne qualité et, si nécessaire, le bon genre.
- `mon conjoint` est fixe dans `l'apport effectué par mon conjoint`; confirmer si une variante `ma conjointe` est nécessaire.
- `[nombre_exemplaires_lettres] exemplaires` doit rester cohérent avec le nombre.
- `euros` est fixe au pluriel après l'apport.
- La lettre utilise le tutoiement ; aucune variante vouvoiement n'est fournie.

### Blocs potentiellement mutualisables

Blocs ou données mutualisables avec la lettre d'avertissement :

- rôles `apporteur` et `conjoint` ;
- société en constitution ;
- montant d'apport en chiffres et en lettres ;
- régime matrimonial / communauté ;
- date de courrier si les deux lettres sont produites ensemble ;
- nombre d'exemplaires, si la spec décide de le paramétrer globalement ;
- rendu de signature simple.

### Anomalies / ambiguïtés source

Points à trancher avant spec/code :

1. Le nom du fichier source réel contient `- SELAS`, ce qui peut limiter son périmètre métier initial.
2. `[qualite_associe]` doit être validé pour SELAS et pour les autres formes sociales du bloc régime communautaire.
3. `[date_courrier]` n'est pas explicitement relié à la date de la lettre d'avertissement, alors que le contenu le suggère.
4. Les placeholders `[apport_personne_1]` et `[apport_lettres_personne_1]` semblent désigner la même donnée que `[montant_apport]` / `[montant_apport_lettres]` dans l'autre lettre, avec des noms divergents.
5. La source distingue `[forme_sociale_complete]` de `[forme_sociale]` et `[forme_sociale_abregee]` observés dans l'autre lettre.
6. Le tutoiement est fixe.

## Analyse document 2 — Lettre d'avertissement au conjoint en cas d'apport d'un bien commun

### Structure observée

La lettre est rédigée par la personne qui envisage d'apporter un bien commun. Elle avertit son conjoint de l'apport projeté à une société dont les caractéristiques sont rappelées.

Structure :

1. en-tête société ;
2. coordonnées du conjoint destinataire ;
3. date ;
4. objet ;
5. formule d'appel au conjoint ;
6. rappel de l'article 1832-2 alinéa 1er du Code civil ;
7. description de la société ;
8. description de l'apport numéraire dépendant de la communauté ;
9. nombre d'exemplaires ;
10. signature de l'apporteur / futur dirigeant ;
11. emplacement ou mention du conjoint ;
12. mention manuscrite à faire précéder.

### Texte fixe

Blocs fixes observés, hors placeholders :

- en-tête société avec forme, capital et siège ;
- objet : `Lettre d'avertissement au conjoint en cas d'apport d'un bien commun.`
- référence à l'article 1832-2 alinéa 1er du Code civil ;
- information de l'intention de faire apport à une société ;
- introduction des caractéristiques de la société ;
- apport d'une somme en numéraire dépendant de la communauté ;
- formule `Fait en trois exemplaires` ;
- formule `Agissant en qualité de futur ...` ;
- instruction de mention manuscrite : `j’atteste avoir été informé de l’apport de ...`.

### Variables / zones variables

| Placeholder source | Rôle canonique candidat | Type | Note de cadrage |
|---|---|---|---|
| `[denomination_societe]` | `societe.denomination` | existant | Utilisé dans l'en-tête, le corps et la mention. |
| `[forme_sociale]` | `societe.forme` | existant / à harmoniser | Forme affichée dans l'en-tête et le corps. |
| `[capital_social]` | `societe.capital_social` | existant | Capital de la société. |
| `[num_voie_siege]` | `societe.siege.num_voie` | existant | Siège social. |
| `[voie_siege]` | `societe.siege.voie` | existant | Siège social. |
| `[cp_siege]` | `societe.siege.cp` | existant | Siège social. |
| `[ville_siege]` | `societe.siege.ville` | existant | Siège social. |
| `[civilite_conjoint]` | `conjoint.civilite_affichage` | nouveau rôle | Destinataire et signataire de l'attestation. |
| `[nom_conjoint]` | `conjoint.nom` | nouveau rôle | Source sans prénom du conjoint. |
| `[num_voie_conjoint]` | `conjoint.adresse.num_voie` | nouveau rôle | Adresse du conjoint. |
| `[voie_conjoint]` | `conjoint.adresse.voie` | nouveau rôle | Adresse du conjoint. |
| `[cp_conjoint]` | `conjoint.adresse.cp` | nouveau rôle | Adresse du conjoint. |
| `[ville_conjoint]` | `conjoint.adresse.ville` | nouveau rôle | Adresse du conjoint. |
| `[date_signature]` | `signature.date` | existant | Date de la lettre ; pas de lieu source. |
| `[montant_apport_lettres]` | `apport.montant_lettres` | nouveau / commun | Montant de l'apport en lettres. |
| `[montant_apport]` | `apport.montant` | nouveau / commun | Montant de l'apport en chiffres. |
| `[civilite]` | `apporteur.civilite_affichage` ou rôle à nommer | nouveau rôle | Auteur de la lettre / futur dirigeant. |
| `[prenom]` | `apporteur.prenom` ou rôle à nommer | nouveau rôle | Auteur de la lettre / futur dirigeant. |
| `[nom]` | `apporteur.nom` ou rôle à nommer | nouveau rôle | Auteur de la lettre / futur dirigeant. |
| `[fonction_dirigeant]` | `apporteur.fonction_dirigeant` ou `dirigeant_nomine.fonction` | à arbitrer | Utilisé dans `futur [fonction_dirigeant]`. |
| `[forme_sociale_abregee]` | `societe.forme_abregee` | à confirmer | Utilisé dans la mention manuscrite. |

### Accords de genre / nombre

Accords ou variantes à arbitrer avant spec :

- `futur [fonction_dirigeant]` est au masculin dans la source ; variante `future` à confirmer.
- `[fonction_dirigeant]` peut elle-même porter un accord : gérant/gérante, président/présidente.
- `d'une somme en numéraire` semble figé pour un apport en numéraire ; aucune variante pour apport autre que somme n'est fournie.
- `euros` est fixe au pluriel.
- `Fait en trois exemplaires` est fixe, contrairement à la lettre de renonciation.
- `notre communauté` est fixe, alors que l'autre lettre utilise `[regime_matrimonial]`.

### Blocs potentiellement mutualisables

Blocs ou données mutualisables avec la lettre de renonciation :

- rôles `apporteur` et `conjoint` ;
- société en constitution ;
- montant d'apport en chiffres et en lettres ;
- régime communautaire / communauté ;
- signature de l'apporteur ;
- données de forme sociale complètes ou abrégées ;
- helper de rendu pour le montant `lettres (chiffres) euros` ou `chiffres (lettres) euros`.

Blocs propres à cette lettre :

- en-tête société complet ;
- adresse du conjoint destinataire ;
- référence à l'article 1832-2 du Code civil ;
- mention manuscrite d'information du conjoint.

### Anomalies / ambiguïtés source

Points à trancher avant spec/code :

1. Le fichier demandé dans le ticket n'existe pas littéralement ; le fichier lu est la version transformée présente dans le dépôt.
2. La source ne contient pas de prénom du conjoint dans le bloc destinataire ou la signature du conjoint.
3. La source ne contient pas de `[lieu_signature]`, contrairement à la lettre de renonciation.
4. La référence `alinéa 1 er` présente un espacement atypique ; ne pas corriger sans validation métier.
5. Le nombre d'exemplaires est fixe (`trois`) alors que l'autre lettre le paramètre.
6. La source fixe `notre communauté` alors que l'autre lettre utilise `[regime_matrimonial]`.
7. Le montant d'apport utilise des placeholders différents de la lettre de renonciation.
8. La mention manuscrite est une instruction à faire précéder ; la spec doit décider si elle est générée comme texte d'instruction, bloc signature ou zone à compléter.

## Analyse batch régime communautaire

### Ce qui est commun aux deux lettres

Les deux lettres appartiennent à un même événement métier : apport d'une somme ou d'un bien commun dans le cadre de la constitution d'une société.

Points communs structurants :

- même condition de déclenchement probable : `dossier.options.regime_communautaire = true` ;
- mêmes rôles métier :
  - apporteur / futur associé ou futur dirigeant ;
  - conjoint informé ou renonçant ;
  - société en constitution ;
- même donnée centrale d'apport :
  - montant en chiffres ;
  - montant en lettres ;
  - dépendance à la communauté ou au régime matrimonial ;
- même besoin de formes sociales :
  - forme complète ;
  - forme affichée ;
  - forme abrégée ;
- même style de lettre simple avec date, objet, corps, signature ;
- relation métier probable entre la date de la lettre d'avertissement et `[date_courrier]` de la lettre de renonciation.

### Ce qui diffère

Différences structurantes :

| Sujet | Lettre de renonciation | Lettre d'avertissement |
|---|---|---|
| Auteur | Conjoint renonçant | Apporteur / futur dirigeant |
| Destinataire | Apporteur / futur associé | Conjoint |
| Société | Mention courte dans le corps | En-tête complet + rappel dans le corps |
| Adresse du conjoint | Non présente | Présente |
| Lieu de signature | Présent | Non présent |
| Date spécifique | `date_signature` + `date_courrier` | `date_signature` |
| Nombre d'exemplaires | Variable en lettres | Fixe à trois |
| Qualité associée | `[qualite_associe]` | Non présente |
| Fonction dirigeant | Non présente | `futur [fonction_dirigeant]` |
| Forme sociale | `forme_sociale_complete` | `forme_sociale` + `forme_sociale_abregee` |
| Mention manuscrite | Non présente | Présente |
| Référence Code civil | Indirecte | Explicite article 1832-2 |

### Réalisme d'un batch de codage commun

Un batch de codage commun est réaliste, mais seulement sous forme de deux documents canoniques distincts dans un même ticket ou lot technique.

Recommandation :

- garder deux générateurs dédiés, un par document ;
- partager un pack de variables `regime_communautaire` ;
- partager les rôles `apporteur` et `conjoint` ;
- partager les helpers de montant en chiffres/lettres ;
- partager les helpers de rendu lettre simple, date, objet et signature ;
- ne pas chercher à créer un générateur unique, car les destinataires, auteurs, blocs fixes et validations diffèrent fortement.

Niveau de mutualisation attendu :

- variables : fort ;
- validations métier : fort à modéré ;
- rendu de base : modéré ;
- texte juridique : faible, car chaque lettre a son propre wording.

### Conditions avant spec/codage

Avant tout codage, `SPEC-RC-001` doit arbitrer :

1. les noms canoniques des rôles `apporteur` et `conjoint` ;
2. le mapping unique des montants d'apport malgré les placeholders divergents ;
3. la relation entre `date_courrier` et la date de la lettre d'avertissement ;
4. les variantes de forme sociale complète / affichée / abrégée ;
5. les accords `associé/associée/actionnaire`, `futur/future`, `gérant/gérante`, `président/présidente` ;
6. le traitement exact de la mention manuscrite ;
7. le périmètre des formes sociales concernées, car la source de renonciation est nommée `SELAS`.

## Suffisance du cadrage

Le cadrage est suffisant pour créer le ticket `SPEC-RC-001`.

Il n'est pas suffisant pour coder le batch, car les mappings canoniques et plusieurs arbitrages de wording restent à formaliser.

## Prochain livrable attendu

`SPEC-RC-001 | Formaliser la spec canonique batch régime communautaire`

La spec devra produire au minimum :

- périmètre exact des deux documents ;
- structure canonique de chaque lettre ;
- mapping source -> variables canoniques ;
- pack commun `regime_communautaire` ;
- règles de genre/nombre ;
- règles de génération conjointe ou indépendante ;
- critères de recette avant code ;
- points de wording à validation humaine.
