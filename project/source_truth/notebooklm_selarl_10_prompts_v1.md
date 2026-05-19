Voici une analyse structurée du processus métier **SELARL** (souvent transcrit phonétiquement par « c'est l'art » ou « CELAR » dans les échanges), basée sur vos sources pour la conception de votre formulaire logiciel.

### 1. Ce que le client entend par SELARL/CELAR

La **SELARL** (Société d’Exercice Libéral à Responsabilité Limitée) est le véhicule juridique privilégié proposé par le cabinet pour permettre aux professionnels de santé (médecins, dentistes) de quitter l'exercice en nom propre (BNC) pour passer en société.

- **Objectif :** Simplifier l'organisation, optimiser la fiscalité et permettre une restructuration patrimoniale globale.
- **Variante :** Le cabinet traite aussi la **SELAS**, mais la SELARL reste le modèle standard pour les opérations d'exercice libéral.

### 2. Les sous-cas et variables rencontrés

Pour le formulaire, la complexité vient des variantes métier et de la situation personnelle du praticien :

- **Professions :** Le modèle de statuts change impérativement selon la profession (médecin, chirurgien-dentiste, ophtalmo, infirmier, kiné, sage-femme) car les contraintes ordinales diffèrent.
- **SCM (Société Civile de Moyens) :** Si le client est déjà membre d'une SCM pour partager ses frais, il doit céder ses parts de SCM à sa nouvelle SELARL.
- **Régime matrimonial :** Si le client est marié sous le régime de la communauté, un document de « renonciation à la qualité d'associé » du conjoint est nécessaire.
- **Dérogation de lieu :** Nécessaire si le praticien exerce sur deux sites différents.
- **Cession / Apport :** Le praticien peut soit **céder** son fonds libéral (fonds de commerce) à la société, soit l'**apporter**. Cela change la rédaction de l'acte (compromis de cession vs contrat d'apport).
- **Bail :** Le passage en société nécessite souvent un avenant au bail professionnel pour changer le titulaire.
- **Financement :** Le projet de statuts doit être envoyé à la banque pour le déblocage des fonds.

### 3. L’objectif final du dossier

L'objectif est d'aboutir à l'**immatriculation de la société** au Greffe et à son **inscription à l'Ordre professionnel**. À terme, cela permet de « faire basculer l'argent » de la structure professionnelle vers des projets personnels (via une holding SPFPL ou une SCI).

### 4. Qui utilise les documents

- **Les Juristes (Albane, Cassandra) :** Elles rédigent les actes (statuts, PV) à partir des données collectées.
- **Le Client :** Il valide les informations, signe les actes électroniquement et dépose le capital à la banque.
- **Le Back-office (Karen) :** Elle utilise l'envoi de la fiche de création comme déclencheur pour facturer l'acompte.
- **Les tiers :** La banque (pour l'attestation de dépôt), le Conseil de l'Ordre (pour agrément) et le Greffe (pour le Kbis).

### 5. Constitution d’un dossier complet (Champs du formulaire)

Pour automatiser la génération, les éléments suivants sont indispensables :

- **Identité de l'associé :** Nom, prénom, date/lieu de naissance, nationalité, adresse, n° de sécurité sociale, régime matrimonial (et identité du conjoint le cas échéant).
- **Informations professionnelles :** Profession exacte, n° RPPS, n° d'inscription à l'Ordre, lieu d'inscription, n° SIREN (si exercice déjà en cours), n° de téléphone professionnel.
- **Informations société future :** Dénomination sociale, montant du capital, répartition des parts entre associés (majoritaire/égalitaire), siège social, banque pour le dépôt du capital, date de clôture de l'exercice.
- **Éléments de contexte :** Membre d'une SCM ? Existence de salariés ? Crédits bancaires en cours ? Lieux d'exercice multiples ? Origine de propriété du fonds (créé ou acheté) ?.

### 6. Étapes réelles du dossier (Ordre logique)

1.  **Qualification (RDV 1) :** Appel de découverte pour comprendre le besoin (passage en société).
2.  **Collecte documentaire :** Récupération des avis d'impôt, déclarations 2035 et relevé de carrière.
3.  **Proposition et Validation (RDV 2) :** Présentation du montage et signature de la lettre de mission.
4.  **Ouverture de la mission juridique :** La « fiche de création » est complétée (souvent par le middle office à partir des notes de RDV) et considérée comme la **source de vérité**.
5.  **Rédaction des "Projets" :** Génération des brouillons de statuts, PV de nomination du gérant, et demandes d'agrément à l'Ordre.
6.  **Phase Bancaire :** Le client apporte le projet de statuts à sa banque pour ouvrir le compte temporaire et obtenir l'**attestation de dépôt de capital**.
7.  **Contrôle de l'Ordre :** Envoi des projets au Conseil de l'Ordre pour validation (étape critique : peut durer un mois selon les commissions).
8.  **Signatures et Formalités :** Signature électronique des actes définitifs et envoi au Greffe/INPI pour immatriculation.

**À confirmer :**

- L'utilisation du terme « CELAR » semble être une erreur de transcription récurrente des outils de dictée pour **SELARL**.
- Le besoin d'un « mode projet » (filigrane sur les documents) pour les échanges avec la banque et l'Ordre avant l'acte définitif.

Souhaitez-vous que je prépare un projet de structure de base de données pour les objets "Contact" et "Société" basés sur ces éléments ?

---

Voici l'analyse des rôles et entités liés au processus **SELARL** (souvent orthographié « CELAR » dans les transcriptions audio) basée sur les sources du notebook.

### 1. Analyse des rôles et entités

| Rôle / Entité                                 | Définition Métier                                                                                      | Documents associés                                          | Informations à saisir                                                                                   | Identité possible                                         | Réutilisation de données                                                               | Ambiguïtés à confirmer                                                                  |
| :-------------------------------------------- | :----------------------------------------------------------------------------------------------------- | :---------------------------------------------------------- | :------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------- | :------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| **Praticien / Médecin / Chirurgien-Dentiste** | Professionnel de santé passant d'un exercice individuel (BNC) à une société.                           | Fiche client, Statuts, Lettre de mission.                   | Nom, prénom, date/lieu de naissance, nationalité, adresse, profession, n° RPPS, n° d'ordre, n° de sécu. | Gérant, Associé, Cédant, Signataire.                      | Les données de la "Fiche Client" alimentent automatiquement tous les actes juridiques. | Les transcriptions "CELAR" sont des erreurs de l'IA pour **SELARL** [conversation, 31]. |
| **Gérant**                                    | Mandataire social assurant la gestion quotidienne de la SELARL.                                        | PV de nomination, Statuts, Kbis.                            | Identité, n° de téléphone.                                                                              | Praticien (cas de la SELARL unipersonnelle).              | Identité du praticien reprise pour le mandat social.                                   | Peut être nommé directement dans les statuts ou via un PV séparé.                       |
| **Associé**                                   | Détenteur de parts sociales dans le capital de la SELARL.                                              | Statuts, Fiche de création.                                 | Identité, nombre de parts, montant et type d'apport (numéraire ou nature).                              | Praticien, Cessionnaire (si holding), Conjoint (parfois). | Répartition du capital réutilisée dans les schémas de holding (SPFPL).                 | Distinction entre associé "exerçant" et associé "non-exerçant" (minoritaire).           |
| **Signataire**                                | Personne physique validant l'acte (souvent via signature électronique).                                | Tous les actes finaux.                                      | Adresse mail (pour l'envoi via Chronique), Nom.                                                         | Associé, Gérant, Cédant.                                  | Identité et mail issus de la fiche client.                                             | Un signataire peut signer plusieurs documents dans un même flux.                        |
| **Mandataire**                                | Personne recevant pouvoir pour effectuer les formalités (Greffe, Ordre).                               | Procuration.                                                | Identité complète.                                                                                      | Souvent un membre du cabinet Sydel (Albane ou Cassandra). | Données du collaborateur Sydel pré-remplies.                                           | À confirmer : si le client doit signer une procuration pour chaque acte ou une globale. |
| **Conjoint**                                  | Époux(se) du praticien, impliqué(e) selon le régime matrimonial.                                       | Acte de renonciation à la qualité d'associé.                | Nom, prénom.                                                                                            | Uniquement une tierce partie.                             | Identité issue de la section "Mariage" de la fiche client.                             | À confirmer : s'il faut saisir l'identité complète du conjoint ou juste son nom.        |
| **Cédant / Vendeur**                          | Le praticien (en tant qu'individu BNC) transférant son fonds libéral ou ses parts de SCM à la société. | Acte de cession de fonds libéral, Acte de cession de parts. | Identité complète, prix de cession, origine de propriété.                                               | Praticien (souvent cession à soi-même).                   | Données du praticien reprises en qualité de vendeur.                                   | Préciser si la cession se fait à des tiers ou à soi-même (modèles différents).          |
| **Cessionnaire / Acquéreur**                  | La société (SELARL) ou la holding (SPFPL) recevant les parts ou le fonds.                              | Acte de cession.                                            | Dénomination, siège, capital, SIREN.                                                                    | SELARL ou SPFPL.                                          | Données de la fiche société.                                                           | -                                                                                       |
| **Bailleur / Locataire**                      | Propriétaire des murs ou titulaire actuel du bail professionnel.                                       | Avenant au bail.                                            | Identité du bailleur.                                                                                   | Le praticien (via une SCI) ou un tiers.                   | Données de la SCI immobilière reliée au client.                                        | S'agit-il d'un bailleur physique ou d'une société civile immobilière ?.                 |
| **Conseil de l'Ordre**                        | Organisme de régulation (Médecins, Dentistes) validant l'exercice en société.                          | Demande d'inscription, Statuts (pour agrément).             | Adresse de l'Ordre départemental.                                                                       | Entité tierce (CDO).                                      | Adresse de l'Ordre réutilisée pour tous les courriers formels.                         | Les exigences varient selon les départements (ex: CDO 94).                              |
| **Banque**                                    | Établissement recevant le dépôt du capital social.                                                     | Attestation de dépôt de capital.                            | Nom et adresse de l'agence bancaire.                                                                    | Entité tierce.                                            | Coordonnées bancaires réutilisées dans les statuts (Art. 7).                           | Différent de la banque finale utilisée après immatriculation.                           |
| **SCM**                                       | Société Civile de Moyens préexistante dont le praticien est membre.                                    | Acte de cession de parts de SCM.                            | SIREN, capital, liste des associés, siège.                                                              | Entité reliée.                                            | Données récupérables via API Pappers.                                                  | À confirmer : si la SCM doit être totalement intégrée au SI ou juste citée.             |
| **SELARL**                                    | La société en cours de création.                                                                       | Tous les documents.                                         | Dénomination, capital, siège, objet social.                                                             | Cessionnaire / Acquéreur.                                 | Informations centrales du dossier.                                                     | Est-elle unipersonnelle (60% des cas) ou pluripersonnelle ?.                            |

### 2. Point sur le terme « professionnel principal »

Le terme **« professionnel principal » n'est pas utilisé dans les sources**.

Les documents utilisent majoritairement :

- **« Praticien »** : pour désigner le client dans son contexte médical.
- **« Client »** : dans le contexte commercial et de conseil patrimonial.
- **« Associé Unique »** : spécifiquement dans les fiches de création pour les SELARL à un seul membre.

**Proposition pour l'interface :**
Le libellé le plus pertinent et le plus utilisé dans vos sources est **« Praticien »**. Il permet de distinguer clairement le professionnel de santé de ses éventuels associés non-exerçants ou de son conjoint.

Souhaitez-vous que je développe la liste des informations spécifiques à collecter pour les "associés minoritaires" ou les "personnes morales" associées ?

---

Pour optimiser l'interface de votre logiciel SELARL (souvent transcrit **CELAR** ou **Sélart** par erreur dans les audios), voici une analyse terminologique basée sur les sources pour garantir l'adoption par les juristes.

### Tableau de recommandations terminologiques

| Terme recommandé | Emplacement Interface                       | Termes à éviter                 | Justification issue des sources                                                                            | Exemple d'aide contextuelle                                                |
| :--------------- | :------------------------------------------ | :------------------------------ | :--------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| **Praticien**    | En-tête global, Liste clients               | Professionnel principal, Client | C'est le terme utilisé par les conseillers pour désigner le médecin ou dentiste dans son exercice libéral. | "Le praticien est la personne physique exerçant l'activité médicale."      |
| **Fiche Client** | Titre de l'écran d'identité                 | Contact, Fiche individu         | Libellé utilisé explicitement dans les maquettes et croquis du processus.                                  | "Identité et situation personnelle du praticien (état civil, famille)."    |
| **Opération**    | Boutons d'action (ex: "Nouvelle Opération") | Transaction, Deal               | Le métier parle de "faire une opération juridique" (création, cession, transformation).                    | "Sélectionnez le type d'acte juridique à réaliser (ex: Création SELARL)."  |
| **Associé**      | Tableau du capital social                   | Actionnaire                     | Dans une SELARL, le capital est divisé en "parts sociales" détenues par des "associés".                    | "Détenteur de parts sociales. Précisez s'il est exerçant ou non."          |
| **Gérant**       | Section Gouvernance                         | Représentant légal, Président   | Terme juridique précis pour la SELARL, présent dans le document "PV de nomination de gérant".              | "Le gérant assure la direction de la société."                             |
| **Signataire**   | Configuration du workflow de signature      | Validateur                      | Désigne la personne qui recevra le mail pour la signature électronique (via Chronique).                    | "Personne physique qui apposera sa signature électronique sur les actes."  |
| **Mandataire**   | Section Formalités / Procuration            | Fondé de pouvoir                | Utilisé pour la "Procuration" permettant au juriste d'effectuer les démarches au Greffe/Ordre.             | "Personne recevant pouvoir pour effectuer les formalités administratives." |

---

### Réponses aux questions spécifiques

**1. Choix des termes (Praticien, Gérant, etc.) :**
Il ne faut pas choisir un seul terme, mais les utiliser selon le **contexte juridique**.

- Utilisez **Praticien** pour le dossier global.
- Utilisez **Associé** pour la détention du capital (ex: "Répartition entre les associés").
- Utilisez **Gérant** pour le mandat social (ex: "PV de nomination de gérant").
- Utilisez **Mandataire** spécifiquement pour les procurations de formalités.

**2. Le terme "Professionnel principal" :**
**Il doit être évité.** Ce terme n'apparaît nulle part dans les sources. Les sources utilisent soit "Praticien", soit "Associé Unique" dans le cas d'une structure unipersonnelle (60 % des cas). L'utilisation d'un libellé inconnu risquerait de créer une distance avec l'utilisateur final.

**3. Nom de l'écran d'identité :**
L'écran doit être nommé **"Fiche Client"**. C'est le nom qui apparaît sur tous les schémas de l'atelier audit et les croquis de l'interface cible.

**4. Distinction claire des rôles :**
Pour éviter la confusion entre des rôles souvent tenus par la même personne :

- **Gérant :** À placer dans une section "Organes de direction".
- **Associé 1 :** À placer dans un tableau "Répartition du Capital".
- **Signataire :** À définir lors de l'étape finale "Envoi en signature".
- **Mandataire :** À pré-remplir dans l'onglet "Formalités" (souvent Albane ou Cassandra par défaut).

**5. Mots risquant de perdre un juriste :**

- **CELAR / Sélart :** Erreurs de transcription à bannir absolument de l'interface au profit de **SELARL**.
- **Transaction / Deal :** Termes de CRM financier qui n'ont pas de sens juridique pour la rédaction d'actes. Préférez **"Dossier"** ou **"Opération"**.
- **Actionnaire :** À réserver aux SELAS. Pour une SELARL, un juriste s'attend à lire **"Associé"**.
- **BNC :** Bien que connu, il désigne le régime fiscal. Pour l'identité, préférez **"Exercice en nom propre"** ou **"Entreprise Individuelle"**.

Souhaitez-vous que je génère une liste de messages d'erreurs "métier" (ex: oubli du n° RPPS ou du régime matrimonial) basés sur les irritants mentionnés par les juristes ?

---

Cette analyse détaille les documents clés du processus **SELARL** (souvent transcrit **CELAR** dans les audios), en s'appuyant sur les besoins d'automatisation exprimés par le cabinet Sydel.

### 1. Documents de Structure et Gouvernance

| Document                               | Cas et Condition d'activation                                               | Type et Dépendances                                     | Infos et Vigilance                                                                                                                                                                   |
| :------------------------------------- | :-------------------------------------------------------------------------- | :------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Statuts (Médecin / Dentiste)**       | **Systématique** pour toute création. Sélection de la profession au départ. | **Générable (Word)**. Dépend du formulaire de création. | **Infos :** Dénomination, capital, siège, RPPS, n° d'ordre, répartition des parts. **Vigilance :** Clauses spécifiques par profession (Ordre) ; accord de genre (« ée ») et pluriel. |
| **PV de Nomination du Gérant**         | Si le gérant n'est pas nommé directement dans les statuts.                  | **Générable**. Dépend des Statuts.                      | **Infos :** Identité du gérant, durée du mandat. **Vigilance :** Souvent optionnel si intégré aux statuts.                                                                           |
| **DNC (Déclaration Non-Condamnation)** | **Systématique** pour chaque gérant lors d'une création.                    | **Générable**.                                          | **Infos :** Identité complète du gérant et filiation (noms des parents). **Vigilance :** Doit être signée par le gérant pour le Greffe.                                              |
| **Procuration**                        | **Systématique** pour permettre aux juristes d'agir.                        | **Générable**. Modèle commun à toutes les professions.  | **Infos :** Mandant (Praticien) et Mandataire (Juriste Sydel). **Vigilance :** Document administratif indispensable pour le Greffe/Ordre.                                            |
| **Autorisation de Domiciliation**      | Si le siège social est au domicile du gérant ou chez un tiers.              | **Générable** (parfois appelé "Courrier du siège").     | **Infos :** Adresse, nom du propriétaire, dénomination de la société. **Vigilance :** Document obligatoire pour l'immatriculation.                                                   |

### 2. Documents Réglementaires et Externes

| Document                                  | Cas et Condition d'activation                                    | Type et Dépendances                                          | Infos et Vigilance                                                                                                                     |
| :---------------------------------------- | :--------------------------------------------------------------- | :----------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| **Demande d’Inscription à l’Ordre**       | **Systématique** pour les professions libérales de santé.        | **Générable**. Dépend des statuts "en projet".               | **Infos :** RPPS, n° d'ordre, lieu d'exercice. **Vigilance :** Formulaires variables selon les départements (ex: CDO 94).              |
| **Demande de Dérogation (Site Distinct)** | Si le praticien exerce sur plus d'un lieu.                       | **Générable**. Dépend de la fiche client (lieux d'exercice). | **Infos :** Adresse du site secondaire et justification. **Vigilance :** Nécessite souvent des justificatifs de locaux/matériel.       |
| **Appel de fonds (Acompte)**              | **Déclenchement** dès l'envoi de la fiche de création au client. | **Générable** (via CRM/Compta).                              | **Infos :** Identité client, montant (généralement 50 % d'acompte). **Vigilance :** Conditionne le début réel de la mission juridique. |

### 3. Documents de Transfert et Patrimoine

| Document                               | Cas et Condition d'activation                                           | Type et Dépendances                                               | Infos et Vigilance                                                                                                                                            |
| :------------------------------------- | :---------------------------------------------------------------------- | :---------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Cession de Cabinet (Fonds Libéral)** | Transition d'un exercice BNC (nom propre) vers la SELARL.               | **Générable / Manuel**. Souvent appelé "Compromis de cession".    | **Infos :** Prix de cession, chiffre d'affaires, origine de propriété. **Vigilance :** Modèles distincts pour "cession à soi-même" ou à des tiers.            |
| **Cession de parts de SCM**            | Si le client est déjà membre d'une SCM existante.                       | **Générable**. Conditionnée par la question "Membre d'une SCM ?". | **Infos :** SIREN de la SCM, capital, identité du cédant/cessionnaire. **Vigilance :** Récupération conseillée via Pappers pour éviter les erreurs de saisie. |
| **Lettres Conjoint (Renonciation)**    | Praticien marié sous le régime de la **communauté**.                    | **Générable**. Dépend du statut matrimonial saisi.                | **Infos :** Identité du conjoint. **Vigilance :** Document crucial pour la sécurité juridique de la détention des parts.                                      |
| **Avenant au Bail**                    | Nécessaire pour transférer le bail professionnel à la nouvelle société. | **Manuel / Partiel**.                                             | **Infos :** Coordonnées du bailleur, date d'effet. **Vigilance :** Difficile à automatiser sans l'analyse du bail original.                                   |

### Points de Vigilance Globaux

- **Mode "Projet" :** Un filigrane "PROJET" doit pouvoir être appliqué sur tous les actes pour les échanges préalables avec la banque et l'Ordre.
- **Source de Vérité :** La fiche de création validée par le client est la donnée maîtresse qui alimente tous ces documents.
- **Rôle des Juristes :** Le système doit générer des **brouillons modifiables** pour permettre aux juristes d'ajuster les clauses spécifiques avant l'envoi en signature électronique.

Souhaitez-vous que je crée un rapport structuré détaillant le modèle de données (champs et types) nécessaire pour automatiser ces documents ?

---

Voici la transformation des informations extraites de vos sources en champs de formulaire utilisateur, structurés pour un usage par des juristes et adaptés à la création d'une **SELARL**.

### Bloc 1 : État civil et Identité (Fiche Client)

_Ce bloc constitue le référentiel de base du praticien._

| Label recommandé                   | Bloc d’écran | Aide contextuelle                                          | Exemple                            | Statut       | Condition d'affichage              | Documents impactés        | Données réutilisables   |
| :--------------------------------- | :----------- | :--------------------------------------------------------- | :--------------------------------- | :----------- | :--------------------------------- | :------------------------ | :---------------------- |
| **Nom et Prénom**                  | Identité     | Saisir tels qu'ils figurent sur la pièce d'identité.       | Patrick Lellouche                  | Obligatoire  | Toujours                           | Tous les actes            | Oui (Parties)           |
| **Sexe**                           | Identité     | Détermine l'accord de genre dans les actes (« ée »).       | Masculin                           | Obligatoire  | Toujours                           | Statuts, PV, DNC          | Accords grammaticaux    |
| **Nationalité**                    | Identité     | Indispensable pour les déclarations au Greffe.             | Française                          | Obligatoire  | Toujours                           | Statuts, DNC              | Fiche client            |
| **Date et Lieu de naissance**      | Identité     | Préciser la ville et le département (ou pays).             | 05/12/1967 à Paris (75)            | Obligatoire  | Toujours                           | Statuts, DNC              | Fiche client            |
| **Adresse personnelle (domicile)** | Coordonnées  | Adresse de résidence principale du praticien.              | 114 Ave Parmentier, 94120 Fontenay | Obligatoire  | Toujours                           | Statuts, DNC, Procuration | Identité associé/gérant |
| **Numéro de sécurité sociale**     | Identité     | Requis pour l'identification fiscale et sociale.           | 1 67 12 75...                      | Obligatoire  | Toujours                           | Fiche client              | Dossier social          |
| **Régime matrimonial**             | Famille      | Détermine la nécessité d'une renonciation du conjoint.     | Communauté réduite aux acquêts     | Obligatoire  | Toujours                           | Lettre conjoint           | Workflow signature      |
| **Nom du conjoint**                | Famille      | Requis pour l'acte de renonciation à la qualité d'associé. | Marie Lellouche                    | Conditionnel | Si marié sous régime de communauté | Lettre conjoint           | Signataire tiers        |

---

### Bloc 2 : Informations Professionnelles (Exercice)

_Données liées à l'activité réglementée du praticien._

| Label recommandé                            | Bloc d’écran | Aide contextuelle                                      | Exemple                        | Statut       | Condition d'affichage           | Documents impactés         | Données réutilisables      |
| :------------------------------------------ | :----------- | :----------------------------------------------------- | :----------------------------- | :----------- | :------------------------------ | :------------------------- | :------------------------- |
| **Profession**                              | Activité     | Détermine le modèle de statuts à utiliser.             | Chirurgien-dentiste            | Obligatoire  | Toujours                        | Statuts (Modèle)           | Objet social               |
| **Numéro RPPS**                             | Ordre        | Répertoire Partagé des Professionnels de Santé.        | 10006565446                    | Obligatoire  | Toujours                        | Statuts, Inscription Ordre | Fiche client               |
| **Numéro d'inscription à l'Ordre**          | Ordre        | Numéro interne au tableau départemental.               | 75/62492                       | Obligatoire  | Toujours                        | Statuts, Inscription Ordre | Fiche client               |
| **Lieu d'inscription (Conseil de l'Ordre)** | Ordre        | Département du conseil dont dépend le praticien.       | PARIS (75)                     | Obligatoire  | Toujours                        | Statuts, Inscription Ordre | Adresse Conseil de l'Ordre |
| **Adresse du Conseil de l'Ordre**           | Ordre        | Adresse postale pour l'envoi du dossier d'inscription. | 92 bd Haussmann, 75008 Paris   | Obligatoire  | Toujours                        | Demande d'inscription      | Courrier sortant           |
| **Adresse professionnelle actuelle**        | Activité     | Lieu d'exercice actuel (BNC) avant création.           | 6 Rue Pelleport, 75020 Paris   | Obligatoire  | Toujours                        | Cession de fonds, Bail     | Adresse vendeur            |
| **Adresse des locaux (Site distinct)**      | Dérogation   | Adresse du second lieu d'exercice souhaité.            | 12 rue de la Paix, 75002 Paris | Conditionnel | Si exercice sur sites multiples | Demande dérogation         | Fiche société              |

---

### Bloc 3 : Projet de Société (SELARL)

_Paramètres de la nouvelle structure juridique._

| Label recommandé                        | Bloc d’écran | Aide contextuelle                             | Exemple                               | Statut      | Condition d'affichage  | Documents impactés           | Données réutilisables |
| :-------------------------------------- | :----------- | :-------------------------------------------- | :------------------------------------ | :---------- | :--------------------- | :--------------------------- | :-------------------- |
| **Dénomination sociale**                | Société      | Nom de la future SELARL.                      | SELARL Patrick Lellouche              | Obligatoire | Toujours               | Tous les actes               | Fiche société         |
| **Adresse du siège social**             | Société      | Adresse où sera fixée la société.             | 6 Rue Pelleport, 75020 Paris          | Obligatoire | Toujours               | Statuts, DNC, Kbis           | Domiciliation         |
| **Montant du capital social**           | Capital      | Montant total des apports (numéraire/nature). | 1 000 €                               | Obligatoire | Toujours               | Statuts, Attestation capital | Fiche société         |
| **Valeur nominale des parts**           | Capital      | Valeur unitaire de chaque part sociale.       | 1 €                                   | Obligatoire | Toujours               | Statuts                      | Calcul capital        |
| **Date de clôture de l'exercice**       | Société      | Date de fin d'exercice comptable annuel.      | 31 décembre                           | Obligatoire | Toujours               | Statuts                      | Fiche société         |
| **Nom et adresse de la banque (Dépôt)** | Banque       | Établissement où les fonds seront bloqués.    | CIC, 9 rue du Potier, 94000 Vincennes | Obligatoire | Si apport en numéraire | Statuts (Art. 7)             | Courrier banque       |

---

### Bloc 4 : Opérations de Cession / Apport (Transition BNC vers SELARL)

_Gère le transfert d'activité._

| Label recommandé             | Bloc d’écran | Aide contextuelle                                      | Exemple                       | Statut       | Condition d'affichage       | Documents impactés     | Données réutilisables |
| :--------------------------- | :----------- | :----------------------------------------------------- | :---------------------------- | :----------- | :-------------------------- | :--------------------- | :-------------------- |
| **Type de transfert**        | Opération    | Choisir entre la vente (cession) ou l'apport pur.      | Cession de fonds libéral      | Obligatoire  | Toujours                    | Acte de cession/apport | Workflow juridique    |
| **Prix de cession du fonds** | Cession      | Montant de la vente du cabinet à la société.           | 150 000 €                     | Obligatoire  | Si Type = Cession           | Acte de cession        | Enregistrement fiscal |
| **Adresse de la SCM**        | SCM          | Adresse du siège de la SCM dont les parts sont cédées. | 10 rue des Arts, 75017 Paris  | Conditionnel | Si membre d'une SCM         | Cession parts SCM      | Fiche SCM             |
| **Adresse du bailleur**      | Bail         | Adresse pour l'envoi de l'avenant au bail.             | 45 rue du Louvre, 75001 Paris | Conditionnel | Si local loué               | Avenant bail           | Courrier bailleur     |
| **Adresse du bien financé**  | Crédit       | Adresse de l'immeuble objet du prêt professionnel.     | 6 Rue Pelleport, 75020 Paris  | Conditionnel | Si crédits bancaires actifs | Fiche client           | Dossier financier     |

### Récapitulatif des adresses spécifiques à collecter :

Conformément à votre demande, voici les adresses distinctes identifiées dans les sources :

1.  **Adresse personnelle (domicile)** : Pour l'état civil de l'associé/gérant.
2.  **Adresse du siège social** : Pour l'immatriculation de la SELARL.
3.  **Adresse de domiciliation** : Si différente du siège (ex: domicile du gérant).
4.  **Adresse du Conseil de l'Ordre** : Pour les formalités d'agrément.
5.  **Adresse professionnelle actuelle** : Lieu d'exercice actuel (vendeur/cédant).
6.  **Adresse du bailleur** : Pour l'avenant au contrat de location.
7.  **Adresse de la banque** : Pour le dépôt du capital social.
8.  **Adresse du siège de la SCM** : Pour la cession des parts de SCM.
9.  **Adresse des locaux (Site distinct)** : Pour les demandes de dérogation.
10. **Adresse du bien financé** : Pour le suivi des crédits et garanties.

---

Sur la base des sources analysées, le processus **SELARL/CELAR** repose massivement sur la réutilisation de données pivot pour éviter la ressaisie manuelle, tout en gérant une complexité liée au nombre d'associés et aux spécificités ordinales.

Voici la liste des règles de réutilisation identifiées :

### 1. Praticien = Associé unique = Gérant = Signataire

C'est la règle d'or pour **60 % des dossiers** traités par le cabinet.

- **Quand elle est vraie :** Dans les structures **unipersonnelles** (EURL/SELARL unipersonnelle) où le médecin ou dentiste exerce seul.
- **Quand elle est fausse :** Dès qu'il y a plusieurs associés (40 % des cas), des associés minoritaires (enfants, conjoint) ou une personne morale (holding SPFPL).
- **UI recommandée :** Case à cocher « Dossier unipersonnel » qui pré-remplit automatiquement les blocs Gérant, Associé 1 et Signataire à partir de la Fiche Client.
- **Risques :** Erreurs massives de **féminisation** (« ée ») et de **pluralisation** (« s ») dans les actes si le système ne bascule pas dynamiquement d'un modèle « associé unique » à « associés ».

### 2. Mandataire ≠ Signataire

- **Quand elle est vraie :** Le **Mandataire** est presque toujours un membre de l'équipe Sydel (Albane ou Cassandra) qui reçoit pouvoir pour effectuer les formalités. Le **Signataire** est le client (Praticien) qui valide l'acte.
- **Quand elle est fausse :** Rarement, sauf si le praticien donne mandat à un tiers (conjoint, associé) pour signer à sa place.
- **UI recommandée :** Menu déroulant pour le Mandataire (pré-rempli avec les initiales des juristes Sydel) et champ e-mail spécifique pour le Signataire (pour le flux de signature électronique).
- **Risques :** Confusion entre le pouvoir de signer l'acte (associé) et le pouvoir d'effectuer les formalités au Greffe (mandataire).

### 3. SELARL (en création) = Acquéreur / Cessionnaire

- **Quand elle est vraie :** Systématiquement lors d'un **transfert d'activité** (passage de BNC à société). La nouvelle SELARL achète le fonds libéral ou les parts de SCM du praticien.
- **Quand elle est fausse :** Lors d'une **première installation** (jeune diplômé sans patientèle préexistante).
- **UI recommandée :** Bouton de copie « Utiliser la société en cours de création » dans le bloc Acquéreur de l'acte de cession.
- **Risques :** Oubli de saisir les données de la SELARL (siège, capital) car elles sont "en cours", ce qui bloque la rédaction de l'acte de cession.

### 4. Vendeur (Cédant) = Locataire actuel

- **Quand elle est vraie :** Le praticien exerçant en nom propre (BNC) est titulaire du bail professionnel et le transfère à sa société.
- **Quand elle est fausse :** Si les murs appartiennent déjà au praticien via une **SCI** ou s'il est sous-locataire d'un tiers.
- **UI recommandée :** Case à cocher « Le vendeur est le titulaire actuel du bail ».
- **Risques :** Générer un avenant au bail inutile si le praticien est propriétaire en nom propre (dans ce cas, il faut un nouveau bail entre lui et sa SELARL).

### 5. Cabinet cédé = Siège social = Lieu d'exercice

- **Quand elle est vraie :** Cas standard où la société est domiciliée là où le médecin travaille.
- **Quand elle est fausse :** Si le gérant domicilie la société à son **domicile personnel** (nécessite une autorisation de domiciliation) ou en cas de **multi-sites** (dérogations ordinales nécessaires).
- **UI recommandée :** Bouton « Identique au lieu d'exercice » dans le bloc Siège Social.
- **Risques :** Incohérence entre l'adresse au Kbis et l'adresse connue par le Conseil de l'Ordre, ce qui peut bloquer l'inscription.

### 6. Cessionnaire des parts de SCM = SELARL

- **Quand elle est vraie :** Le praticien membre d'une SCM doit faire racheter ses parts par sa nouvelle structure d'exercice.
- **Quand elle est fausse :** Si les parts de SCM sont transférées à une holding (SPFPL), ce qui est plus rare pour une SCM de moyens.
- **UI recommandée :** Bouton de récupération des données de la SCM via **API Pappers/SIREN** pour éviter de ressaisir manuellement le capital et le siège de la SCM.
- **Risques :** Erreur sur le montant du capital ou le numéro SIREN de la SCM, ce qui rend l'acte de cession irrecevable au Greffe.

**Conseil pour l'interface :** Les juristes insistent sur le fait que la **Fiche de création** doit être la « source de vérité ». Toute donnée saisie une fois doit pouvoir être "propagée" dans tous les rôles (vendeur, acquéreur, associé, gérant) via des boutons de duplication pour gagner la « demi-seconde » qui, cumulée, fait gagner des heures.

Souhaitez-vous que je liste les **champs obligatoires à bloquer** (ex: n° RPPS ou régime matrimonial) pour éviter que les juristes ne génèrent des actes incomplets ?

---

Sur la base des sources analysées, voici l'inventaire des documents et sections du dossier SELARL/CELAR qui doivent rester **manuels** ou faire l'objet d'une vigilance particulière pour l'automatisation.

### 1. Documents et parties de documents à maintenir en manuel

| Nom du document                                         | Pourquoi est-il manuel ?                                                              | Statut (Définitif/Temp)         | Informations manquantes                                           | Affichage Interface                                                   | Risque si automatisé                                                  |
| :------------------------------------------------------ | :------------------------------------------------------------------------------------ | :------------------------------ | :---------------------------------------------------------------- | :-------------------------------------------------------------------- | :-------------------------------------------------------------------- |
| **Cession de fonds / Cabinet (Libéral)**                | Complexité de l'**origine de propriété** (achat vs création) et du prix.              | Temporaire (Semi-auto)          | Historique des actes d'achat précédents, détails du cédant tiers. | Brouillon Word modifiable après injection des identités.              | Erreur sur l'origine du fonds, rendant l'acte nul ou contestable.     |
| **Avenant au Bail**                                     | Nécessite l'analyse du contrat de bail original pour adapter les clauses.             | Temporaire                      | Identité du bailleur, clauses de transfert spécifiques.           | Bouton "Générer un masque" avec l'en-tête, mais corps de texte libre. | Incompatibilité avec les clauses du bailleur original.                |
| **Demande de dérogation (Site distinct / Multi-sites)** | Nécessite une **justification métier** précise et l'ajout de pièces annexes.          | Temporaire                      | Justification de l'activité, plans des locaux, devis de travaux.  | Formulaire de saisie de texte libre pour la justification.            | Rejet par le Conseil de l'Ordre si la motivation est trop générique.  |
| **Répartition complexe du capital**                     | Cas où il y a plus de 2-3 associés ou des pourcentages atypiques (ex: 100 000 parts). | Définitif (Besoin de souplesse) | Détails des droits de vote vs droits financiers spécifiques.      | Tableau dynamique avec saisie manuelle libre des pourcentages.        | Statuts incohérents mathématiquement si l'algorithme est trop rigide. |
| **Cession de parts de SCM**                             | Nécessite des données souvent non disponibles sans un accès API complet.              | Temporaire                      | Liste exacte des gérants et associés actuels de la SCM.           | Champ de recherche API (Pappers) avec bouton "Valider les infos".     | Saisie d'une SCM erronée ou obsolète si non vérifiée manuellement.    |

---

### 2. Focus sur les points de vigilance spécifiques

- **Dérogations (SEL BNC, Cumul) :** Les sources indiquent que ces cas sont des "variantes" qui s'ajoutent au dossier standard. Plutôt que de générer un document à part entière, il est recommandé d'injecter une **clause spécifique** dans la demande d'inscription à l'ordre (ex: mentionner qu'on exerce ailleurs ou nulle part ailleurs).
- **Lettre d’avertissement conjoint :** Ce document dépend strictement de l'**option mariage/communauté**. Si l'identité du conjoint est connue, elle est pré-remplissable, mais la signature doit être traitée comme un flux séparé.
- **Plans et devis de travaux :** Pour l'Ordre, l'automatisation ne peut pas fournir les plans des locaux ou les devis. L'interface doit comporter un **bloquant (checklist)** empêchant l'envoi du dossier tant que ces fichiers manuels ne sont pas téléchargés.
- **Le mode "Projet" :** Il est impératif de ne pas présenter les documents comme "Définitifs" au début. Les banques et l'Ordre exigent des versions **filigranées "PROJET"** pour étude avant signature.

### Recommandation pour l'interface

Pour éviter de perdre les juristes, le système ne doit pas viser le "100 % automatique" immédiatement. Il est préférable de présenter ces documents comme des **"Brouillons intelligents"** (Word) que l'expert peut ajuster, car 10 % des dossiers comportent des particularités imprévisibles pour un algorithme.

Voulez-vous que je liste les documents qui, à l'inverse, sont considérés comme "100 % automatisables" dès maintenant (type DNC ou Procuration) ?

---

L'analyse des sources et des transcriptions d'ateliers avec les juristes (Albane, Cassandra et Hugo) permet de dégager un ordre plus "naturel" que celui proposé. Le point critique soulevé par les juristes est que **le choix de la profession et du type d'opération doit impérativement intervenir en premier**, car cela conditionne l'intégralité des modèles de documents et des questionnaires suivants.

Voici la proposition d'ordre idéal pour le formulaire **SELARL** :

### 1. Qualification & Type d'Opération

- **Objectif :** Déterminer le "moteur" juridique et les modèles de documents à charger.
- **Champs à afficher :** Profession (Dentiste, Médecin, etc.), Type d'opération (Création, Cession de parts, Transformation), Forme juridique (SELARL, SELAS).
- **Champs à masquer :** Les formes juridiques non pertinentes (ex: masquer SCI/SPFPL si "Création SELARL" est choisi).
- **Conditions d’affichage :** Toujours visible en entrée.
- **Documents impactés :** Tous (Statuts, PV, Cession).
- **Erreurs à éviter :** Ne pas permettre la modification de la profession en cours de saisie, car les statuts varient trop entre un médecin et un dentiste.

### 2. Le Praticien (Fiche Client)

- **Objectif :** Établir la "source de vérité" sur l'identité de l'associé principal.
- **Champs à afficher :** Nom, prénom, sexe (pour le "ée"), date/lieu de naissance, nationalité, adresse personnelle, n° de sécu, n° RPPS, n° d'ordre.
- **Champs à masquer :** N° SIREN (si création pure).
- **Conditions d’affichage :** Toujours présent.
- **Documents impactés :** Statuts, DNC, Procuration, Inscription à l'ordre.
- **Erreurs à éviter :** Oublier le sexe, ce qui bloque la **féminisation automatique** des actes ("Monsieur né..." vs "Madame née...").

### 3. La Société (Fiche Société)

- **Objectif :** Définir les paramètres de la future entité juridique.
- **Champs à afficher :** Dénomination sociale, montant du capital, adresse du siège, date de clôture, banque de dépôt.
- **Champs à masquer :** Date d'immatriculation et SIREN (ces champs seront remplis après le processus par les juristes).
- **Conditions d’affichage :** Toujours présent.
- **Documents impactés :** Statuts, PV de nomination, Attestation de capital.
- **Erreurs à éviter :** Confondre la banque de dépôt (avant création) avec la banque d'exploitation (après création).

### 4. Capital & Associés

- **Objectif :** Gérer la répartition des parts et les droits spécifiques.
- **Champs à afficher :** Nombre de parts, valeur nominale, identité des autres associés, répartition (majoritaire/égalitaire), droits financiers vs droits de vote.
- **Champs à masquer :** Bloc "Associés" si la case "Associé unique" est cochée (60% des cas).
- **Conditions d’affichage :** Si plusieurs associés sont déclarés.
- **Documents impactés :** Statuts (Art. 7 et 8), Liste des associés.
- **Erreurs à éviter :** Ne pas prévoir de souplesse pour les dossiers avec plus de 2 associés (ex: cas à 100 000 parts).

### 5. Contexte & Scénarios (Variables métier)

- **Objectif :** Activer les documents optionnels selon la situation du client.
- **Champs à afficher :** Régime matrimonial (Communauté ?), Membre d'une SCM ?, Transfert de bail ?, Autre lieu d'exercice ?.
- **Champs à masquer :** Détails SCM si "Non".
- **Conditions d’affichage :** Toujours présent (sous forme de questions Oui/Non).
- **Documents impactés :** Lettre conjoint, Cession SCM, Avenant bail, Demande de dérogation.
- **Erreurs à éviter :** Oublier de demander s'il y a des salariés (BNC), ce qui impacte la reprise d'activité.

### 6. Documents & Génération

- **Objectif :** Visualiser et télécharger les actes avant envoi.
- **Champs à afficher :** Checklist des documents obligatoires vs facultatifs, Bouton "Générer en mode Projet" (filigrane).
- **Champs à masquer :** Les documents non activés à l'étape précédente.
- **Conditions d’affichage :** Étape finale.
- **Documents impactés :** Tous.
- **Erreurs à éviter :** Générer une version "Définitive" trop tôt ; le client a besoin du "Projet" pour la banque et l'Ordre.

---

### Comparaison avec votre structure initiale

| Votre structure  | Structure recommandée (Sydel)    | Justification des sources                                           |
| :--------------- | :------------------------------- | :------------------------------------------------------------------ |
| 1. Qualification | **1. Qualification & Opération** | Indispensable pour charger les 62 types de docs.                    |
| 2. Société       | **2. Personne (Praticien)**      | Le client est la source de vérité avant la société inexistante.     |
| 3. Personne      | **3. Société**                   | Les données de la personne pré-remplissent le gérant de la société. |
| 4. Associés      | **4. Capital & Associés**        | Centralise la logique mathématique (parts/actions).                 |
| 5. Conditions    | **5. Scénarios métier**          | Active les documents "satellites" (Bail, SCM, Conjoint).            |
| 6. Documents     | **6. Génération & Revue**        | Unifie la liste des docs obligatoires/facultatifs.                  |

**L'ordre "Sydel" est plus efficace** car il permet de récupérer les données du Praticien (écran 2) pour pré-remplir automatiquement la section Gérant/Associé 1 de l'écran Société (écran 3), évitant ainsi la "ressaisie" dénoncée par Hugo.

Souhaitez-vous que je rédige la liste des "Questions Bloquantes" à intégrer dans l'écran 5 pour éviter les retards au Conseil de l'Ordre ?

---

Sur la base des sept sources du notebook et des ateliers d'audit, voici les questions stratégiques et techniques qu'il reste à trancher avec la direction de Sydel (Denis et Hugo) avant de finaliser l'implémentation du système SELARL/CELAR.

### 1. Questions de niveau : BLOQUANT

_Ces questions touchent au cœur de la génération juridique et au moteur de l'application._

- **Comment gérer techniquement la féminisation et la pluralisation ("ée", "s") ?**
  - **Pourquoi :** C'est un irritant majeur et une source d'erreurs récurrente dans les statuts actuels.
  - **Impact :** Écran de saisie du praticien et tous les modèles de documents.
  - **Décision produit :** Faut-il une logique de code rigide (si "sexe" = F alors ajouter "e") ou un appel API à une IA (Mistral/GPT) pour reformuler le paragraphe entier ?
- **Quelle architecture pour les 62 variantes de templates SELARL ?**
  - **Pourquoi :** Sydel dispose de 62 modèles différents (selon la profession et le cas). Les maintenir tous individuellement est jugé "ingérable" à terme.
  - **Impact :** Administration du système et écran de génération.
  - **Décision produit :** Doit-on partir sur 62 fichiers Word distincts ou sur un "moteur de clauses" qui assemble un document unique à partir de briques stockées en base de données ?
- **Comment traiter les droits de vote vs droits financiers dérogatoires ?**
  - **Pourquoi :** Dans certains cas, 1 % du capital ne donne pas droit à 1 % du résultat.
  - **Impact :** Écran "Associés/Répartition du capital" et Article 8 des statuts.
  - **Décision produit :** Le formulaire doit-il permettre une saisie manuelle libre des droits financiers ou rester sur une règle de proportionnalité par défaut ?

### 2. Questions de niveau : IMPORTANT

_Ces questions impactent la fiabilité du dossier et la satisfaction du client final._

- **Faut-il bloquer la génération si les pièces jointes CDO (plans/devis) sont manquantes ?**
  - **Pourquoi :** L'absence de plans des locaux ou de devis de travaux bloque systématiquement le dossier au Conseil de l'Ordre, entraînant un mois de retard.
  - **Impact :** Écran "Documents attendus" et workflow de validation.
  - **Décision produit :** Le système doit-il être "bloquant" (interdire l'envoi) ou simplement "alertant" ?
- **Le mode "Projet" (filigrane) doit-il être automatisé ?**
  - **Pourquoi :** Les banques et l'Ordre exigent des versions non définitives pour étude.
  - **Impact :** Écran de génération finale.
  - **Décision produit :** Ajoute-t-on un bouton "Générer en mode Projet" qui applique un filigrane automatique sur le PDF ?
- **Comment automatiser l'origine de propriété du fonds libéral ?**
  - **Pourquoi :** C'est une partie complexe à rédiger si le fonds a été acheté plutôt que créé.
  - **Impact :** Acte de cession de fonds et écran "Opération".
  - **Décision produit :** Doit-on ajouter des champs ultra-détaillés (date d'achat, prix initial, vendeur précédent) ou laisser cette section en saisie libre dans le Word généré ?

### 3. Questions de niveau : CONFORT

_Ces questions visent à optimiser le temps de travail des juristes._

- **Quelle profondeur d'intégration pour l'API Pappers ?**
  - **Pourquoi :** Pour éviter de remplir les fiches de SCM ou de sociétés existantes à la main.
  - **Impact :** Écrans "Société" et "Cession de parts".
  - **Décision produit :** L'import doit-il se limiter au SIREN/Siège ou doit-il tenter de récupérer la liste des associés et gérants ?
- **Le portail client doit-il être ouvert dès la V1 ?**
  - **Pourquoi :** Pour que le client saisisse lui-même ses données d'état civil.
  - **Impact :** Architecture globale et sécurité des données.
  - **Décision produit :** Est-ce une priorité immédiate ou préfère-t-on que les juristes gardent la main sur la saisie pour l'instant ?

### 4. Questions de niveau : PLUS TARD

_Ces points sont mentionnés comme des objectifs à terme._

- **Comment archiver légalement les communications (10 ans) ?**
  - **Pourquoi :** C'est une obligation de conformité mentionnée par la direction.
  - **Impact :** Stockage Drive et base de données.
  - **Décision produit :** Intégration d'un outil d'archivage à valeur probante ou simple stockage structuré sur Google Drive ?
- **Liaison avec la facturation (Karen) ?**
  - **Pourquoi :** Pour déclencher automatiquement l'envoi de la facture d'acompte.
  - **Impact :** Interconnexion avec le logiciel de comptabilité.
  - **Décision produit :** Automatisation du mail de facturation ou simple notification interne pour le back-office.

Souhaitez-vous que je développe l'une de ces questions sous forme de **cas d'usage utilisateur** (User Story) pour faciliter la discussion avec votre équipe technique ?

---

Cette synthèse est structurée pour servir de base technique à un cahier des charges fonctionnel. Elle s'appuie sur les besoins d'automatisation du cabinet Sydel pour le processus **SELARL** (souvent transcrit **CELAR** ou **Sélart** dans les sources).

### Synthèse Exécutable du Processus SELARL

| Écran UI             | Bloc métier          | Champ utilisateur                      | Variable(s) / Infos           | Condition d’affichage | Document(s) impactés        | Règle de réutilisation                                | Statut          | Commentaire / Risque                                               |
| :------------------- | :------------------- | :------------------------------------- | :---------------------------- | :-------------------- | :-------------------------- | :---------------------------------------------------- | :-------------- | :----------------------------------------------------------------- |
| **0. Accueil**       | **Recherche & Init** | Recherche globale                      | Nom, SIREN, Dossier           | Toujours              | Aucun                       | Récupère l'historique client/société                  | **Générable**   | Éviter la double saisie si le client existe déjà.                  |
| **1. Qualification** | **Type de dossier**  | Profession                             | `profession_type`             | Toujours              | Statuts (Modèle spécifique) | Définit le "moteur" des statuts (Dentiste vs Médecin) | **Générable**   | **Bloquant** : Les statuts varient strictement selon l'Ordre.      |
|                      |                      | Type d'opération                       | `op_type`                     | Toujours              | Tous les actes              | Création, Cession, ou Transformation                  | **Générable**   | -                                                                  |
| **2. Fiche Client**  | **Identité**         | Sexe (H/F)                             | `genre_praticien`             | Toujours              | Statuts, PV, DNC            | Gère l'accord grammatical (« ée »)                    | **Générable**   | **Risque majeur** : Erreurs de genre très fréquentes manuellement. |
|                      |                      | Nom / Prénom                           | `client_nom`, `client_prenom` | Toujours              | Tous les actes              | Propagé vers "Associé 1", "Gérant" et "Vendeur"       | **Générable**   | Source de vérité pour tout le dossier.                             |
|                      |                      | Nationalité / Date & Lieu de Naissance | `birth_data`, `natio`         | Toujours              | Statuts, DNC                | Réutilisé pour le gérant                              | **Générable**   | -                                                                  |
|                      | **Réglementaire**    | N° RPPS / N° d'Ordre                   | `rpps_num`, `ordre_num`       | Toujours              | Statuts, Inscription Ordre  | Stocké dans le CRM client                             | **Générable**   | -                                                                  |
|                      | **Situation Perso**  | Régime Matrimonial                     | `regime_matri`                | Toujours              | Lettre conjoint             | Si "Communauté", active "Nom du conjoint"             | **Générable**   | -                                                                  |
| **3. Fiche Société** | **Structure**        | Dénomination                           | `ste_nom`                     | Toujours              | Tous les actes              | Devient le "Cessionnaire" dans les actes de cession   | **Générable**   | -                                                                  |
|                      |                      | Siège Social                           | `ste_siege_adr`               | Toujours              | Statuts, Kbis, DNC          | Peut être = "Adresse Pro" ou "Domicile"               | **Générable**   | Ne pas appeler seulement "Adresse".                                |
|                      |                      | Capital Social                         | `ste_capital_total`           | Toujours              | Statuts, Attestation        | Doit être écrit en lettres et chiffres                | **Générable**   | -                                                                  |
|                      |                      | Banque de dépôt                        | `banque_depot_nom`            | Toujours              | Statuts (Art. 7)            | Différent de la banque d'exploitation finale          | **Générable**   | -                                                                  |
| **4. Capital**       | **Répartition**      | Nombre de parts                        | `parts_nb`, `parts_val`       | Toujours              | Statuts (Art. 8)            | Gère le terme "Parts" ou "Actions"                    | **Générable**   | -                                                                  |
|                      |                      | Droits financiers / Droits de vote     | `droits_vote`, `droits_fin`   | Si > 1 associé        | Statuts                     | Parfois dérogatoire (1% parts ≠ 1% résultat)          | **À confirmer** | Risque de calculs complexes hors standard.                         |
| **5. Scénarios**     | **Spécificités**     | Membre d'une SCM ?                     | `scm_member_bool`             | Toujours              | Cession de parts SCM        | Si Oui, demande SIREN SCM (via Pappers)               | **Générable**   | Automatiser via API Pappers pour éviter la saisie.                 |
|                      |                      | Sites multiples ?                      | `site_distinct_bool`          | Toujours              | Demande dérogation CDO      | Si Oui, demande "Adresse site 2"                      | **Manuel**      | Nécessite souvent une justification libre.                         |
|                      |                      | Transfert de bail ?                    | `bail_transfert_bool`         | Toujours              | Avenant au bail             | Si Oui, demande "Nom du bailleur"                     | **Manuel**      | Souvent trop spécifique pour du 100% auto.                         |
| **6. Documents**     | **Génération**       | Mode Projet                            | `is_draft_mode`               | Toujours              | Filigrane "PROJET"          | Applique un "PROJET" en travers du PDF/Word           | **Générable**   | Indispensable pour la banque et l'Ordre.                           |
|                      |                      | Statut Signature                       | `sign_status`                 | Fin de flux           | Workflow signature          | Envoi automatique vers Chronique                      | **Générable**   | -                                                                  |

### Points de vigilance pour le développement :

1.  **Moteur de templates :** Le système doit gérer 62 variantes de statuts selon la profession. Une approche par "blocs de clauses" est préférable à 62 fichiers Word statiques.
2.  **Gestion des adresses :** Les sources distinguent l'adresse personnelle, le siège social, l'adresse professionnelle (BNC), l'adresse du bailleur, celle de la banque et celle de la SCM. Chaque champ doit être typé précisément.
3.  **Statut "Brouillon" :** Les juristes exigent que le logiciel génère un **brouillon modifiable (Word)** plutôt qu'un PDF final immédiat pour ajuster les 10% de cas particuliers.
4.  **Dépendance de l'Ordre :** Certains documents (plans, devis de travaux) sont manuels mais **bloquants** pour le dossier au Conseil de l'Ordre. Prévoir une checklist bloquante.
5.  **Réutilisation (Key Feature) :** Une donnée saisie dans la "Fiche de création" doit se propager instantanément dans tous les documents (Procuration, DNC, Statuts) sans aucune ressaisie.

Souhaitez-vous que je crée un rapport détaillé sur la structure de la base de données (entités et relations) pour l'objet "Société" et ses "Associés" ?
