# Protocole de construction d'un processus métier V1

Ticket source : `SELARL-PILOT-PROTOCOL-001`

## Objet

Ce protocole décrit la méthode à appliquer pour transformer une source de vérité métier en parcours de saisie exploitable par l'Assistant métier, sans repartir du moteur ni d'une liste brute de variables.

Il est volontairement opérationnel : il doit pouvoir être repris pour SELAS, SPFPL, SCI, SCM ou tout autre processus futur.

## Entrées obligatoires

Avant de commencer un processus :

1. Lire `AGENTS.md`, `docs/project/00_MASTER_PLAN.md`, `docs/project/01_EXECUTION_BOARD.md`, `docs/project/02_CODEX_WORKFLOW.md`, `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` et `docs/project/04_LAST_STATE.md`.
2. Identifier la source de vérité métier du processus.
3. Identifier les specs delivery existantes liées aux documents attendus.
4. Lire `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md` et `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.
5. Confirmer que le ticket ne demande pas de modifier le wording juridique.

Si une source manque ou contredit le ticket, bloquer la construction et documenter le point d'arbitrage.

## Méthode reproductible

### Addendum 2026-06-01 - méthode SELARL capitalisée

Pour tout nouveau processus/type d'entreprise, la méthode SELARL complète impose
désormais :

1. lire le document de référence qui dit quels documents produire ;
2. interroger la base de connaissance par prompts courts et journaliser chaque
   réponse ;
3. recouper avec les retours humains disponibles ;
4. éviter les questions humaines dont la réponse est déjà dans les sources ;
5. produire une matrice documentaire et une matrice de réutilisation avant code ;
6. générer un pack numéroté avec manifest après implémentation ;
7. vérifier la fidélité source des documents sensibles ;
8. faire relire l'associé uniquement sur des écarts concrets ;
9. régénérer un nouveau pack après correction ;
10. clore en `DONE`, `PARTIAL` ou `BLOCKED`.

Cette séquence complète le protocole ci-dessous. Elle prime si une ancienne
formulation semble autoriser un passage direct en implémentation.

### 1. Lire la source de vérité

- Extraire le texte du DOCX source sans le modifier.
- Relever les blocs visibles : cas principal, sous-cas, conditions, documents communs, documents conditionnels et documents manuels.
- Conserver les anomalies de libellé telles quelles dans les notes ; ne pas les corriger silencieusement.

Livrable attendu : liste brute des documents et des conditions.

### 2. Identifier les cas et sous-cas

Pour chaque branche :

- nommer le cas principal avec un libellé métier compréhensible ;
- lister les questions de qualification nécessaires ;
- distinguer les booléens simples, les choix exclusifs et les sous-choix dépendants.

Exemple SELARL : profession, site distinct, SCM cession, régime communautaire, dérogation, cession, type de cabinet si cession.

### 3. Identifier les documents attendus

Pour chaque document :

- relever son nom métier ;
- relever le fichier source ;
- rattacher le `DOC-XXX` si le moteur le connaît ;
- qualifier son statut : générable, manuel, non implémenté ou mapping à confirmer ;
- noter la condition de présence.

La sélection documentaire doit venir de la source vérité et du catalogue métier, pas du formulaire existant.

### 4. Extraire les variables

Pour chaque document :

- partir des specs delivery et de la table de mapping si elles existent ;
- sinon, extraire les placeholders source et les zones à remplir ;
- séparer les variables structurantes des champs ponctuels ;
- ne jamais créer une variable canonique à partir d'un nom local de modèle sans justification.

Sortie attendue : variables par document, avec le bloc métier cible.

### 5. Regrouper les variables par contexte métier

Transformer la liste brute en blocs compréhensibles :

- Qualification du dossier ;
- Société ;
- Siège social ;
- Fiche Client / Praticien ;
- Associés ;
- Mandataire / signataire ;
- Ordre professionnel ;
- Régime matrimonial / conjoint ;
- Cession de cabinet ;
- Bail ;
- SCM ;
- Banque / financement ;
- Signature.

Un bloc n'existe que s'il sert au processus. Ne pas afficher un bloc vide pour faire joli.

### 6. Dédupliquer les champs

Pour chaque champ répété :

- identifier la donnée source unique ;
- lister les variables moteur alimentées ;
- décider si la donnée est recopiée, dérivée ou référencée ;
- prévoir le mécanisme UI : case à cocher, bouton de copie, champ source unique ou lecture seule.

Règle : un utilisateur juriste ne doit pas ressaisir une même identité ou une même adresse sous deux libellés différents.

### 7. Nommer les champs pour l'utilisateur

Chaque label doit dire de quoi on parle :

- `Adresse personnelle du professionnel`, pas `Adresse` ;
- `Adresse du siège social`, pas `Adresse société` ;
- `Adresse du cabinet cédé`, pas `Adresse cabinet` si plusieurs cabinets peuvent exister ;
- `Adresse du service d'enregistrement`, pas `Adresse SDE`.

Règle : aucun champ UI ne doit s'appeler seulement `adresse`, `nom`, `date` ou `montant`.

### 8. Définir les dépendances conditionnelles

Pour chaque champ ou bloc :

- préciser la condition d'affichage ;
- préciser si le champ est obligatoire, optionnel ou obligatoire seulement si le bloc est actif ;
- préciser les documents impactés ;
- prévoir le comportement quand la condition repasse à `false`.

Les champs masqués ne doivent pas bloquer la progression.

### 9. Construire le parcours utilisateur

Ordre recommandé :

1. Qualification du dossier.
2. Données communes de société et de siège.
3. Personnes et rôles.
4. Conditions spécifiques.
5. Documents attendus et champs manquants.
6. Génération.

Le parcours doit suivre la logique métier, pas l'ordre des documents dans le moteur.

### 10. Mapper les champs UI vers les variables moteur

Pour chaque champ UI :

- donner le label utilisateur ;
- donner la ou les variables moteur alimentées ;
- indiquer le bloc UI ;
- indiquer les documents qui consomment cette donnée ;
- indiquer la règle de réutilisation.

Une donnée peut alimenter plusieurs variables moteur si le mapping est explicitement documenté.

### 11. Tester document par document

Avant implémentation :

- préparer un scénario minimal du processus ;
- lister les documents attendus ;
- lister les documents exclus ;
- vérifier les champs requis par document ;
- vérifier les documents manuels et non implémentés ;
- écrire les critères de smoke test.

Après implémentation :

- tester la sélection documentaire ;
- tester le formulaire avec les conditions `true` et `false` ;
- tester les documents générables un par un ;
- vérifier que les documents manuels ne sont pas envoyés à la génération ;
- lancer `ruff check .` et `pytest`.

### 12. Valider avec un juriste

La validation attendue porte sur :

- les questions de qualification ;
- les libellés utilisateurs ;
- les déductions métier ;
- les documents attendus et exclus ;
- les wording sensibles ;
- les champs manuels.

Aucune correction juridique ne doit être faite par l'agent sans validation tracée.

### 13. Répliquer au processus suivant

Pour répliquer :

1. Copier la structure de spec du processus pilote.
2. Remplacer uniquement les sources, cas, documents et conditions.
3. Réutiliser les blocs UI déjà validés quand les rôles métier sont identiques.
4. Créer un champ nouveau seulement si aucun champ existant ne couvre la donnée.
5. Produire un rapport de comparaison avec le processus précédent.

## Critères de sortie

Un processus est prêt pour implémentation UI seulement si :

- la source de vérité est versionnée ;
- les choix de qualification sont listés ;
- les documents attendus sont classés ;
- les variables sont regroupées par blocs métier ;
- les règles de réutilisation sont écrites ;
- les écarts avec l'UI actuelle sont connus ;
- un plan d'implémentation découpé existe ;
- les points d'ambiguïté sont documentés.
