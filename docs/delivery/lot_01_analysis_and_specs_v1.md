# DAAT x SYDEL — Lot 1
## Analyse source + specs de génération v1

Date : 2026-05-12

## Périmètre analysé
- DOC-001 — Déclaration sur l’honneur de non-condamnation
- DOC-002 — Autorisation de domiciliation
- DOC-003 — Procuration

## Constats communs Lot 1
1. Les trois documents sont courts, mono-page et fortement mutualisables.
2. Les trois modèles partagent une même logique visuelle :
   - page A4 portrait ;
   - marges standard (~2,5 cm) ;
   - titre dans un cartouche encadré en haut de page ;
   - corps en police 10 pt environ ;
   - bloc de signature en bas de page.
3. Les sources reçues sont des versions transformées. Elles contiennent des artefacts de transformation :
   - DOC-001 : commentaire source sur l’adaptation « fille » ;
   - DOC-002 : révisions / insertions ;
   - DOC-003 : placeholders colorés / surlignés.
4. Recommandation technique : pour le code V1, générer des DOCX propres à partir d’un gabarit reconstruit ou d’un build from-scratch, plutôt que de nettoyer à chaque fois les versions transformées.
5. Les accords de genre sont à gérer dès le Lot 1.

## Variables communes Lot 1
### Personne signataire
- personne_signataire.genre
- personne_signataire.civilite
- personne_signataire.prenom
- personne_signataire.nom
- personne_signataire.adresse_perso.num_voie
- personne_signataire.adresse_perso.voie
- personne_signataire.adresse_perso.cp
- personne_signataire.adresse_perso.ville

### Société
- societe.denomination
- societe.forme_sociale
- societe.capital
- societe.siege.num_voie
- societe.siege.voie
- societe.siege.cp
- societe.siege.ville

### Signature
- signature.lieu
- signature.date
- signature.image_optionnelle

### Variables documentaires spécifiques
- personne_signataire.date_naissance
- personne_signataire.nationalite
- personne_signataire.nom_pere
- personne_signataire.nom_mere
- personne_signataire.fonction_dirigeant
- domiciliation.adresse_domiciliation_affichee

---

## DOC-001 — Déclaration sur l’honneur de non-condamnation

### Métadonnées
- doc_id : DOC-001
- générateur cible : `generate_declaration_sur_l_honneur_de_non_condamnation(ctx)`
- condition : tous les dossiers
- associés dynamiques : non
- accords grammaticaux : oui (genre)

### Placeholders identifiés dans la source
- civilite
- prenom
- nom
- date_naissance
- num_voie_perso
- voie_perso
- ville_perso
- cp_perso
- nationalite
- nom_pere
- nom_mere
- lieu_signature
- date_signature
- signature

### Blocs documentaires
1. Cartouche titre sur 2 lignes :
   - DECLARATION DE NON CONDAMNATION
   - EN APPLICATION DE L’ARTICLE A.123-51 du Code de Commerce
2. Bloc identité signataire.
3. Bloc filiation.
4. Paragraphe de déclaration.
5. Bloc signature à droite.
6. Bloc de rappel légal en italique en bas de page.

### Règles de génération
- Générer le titre dans un cartouche encadré noir, centré.
- Générer le corps en 10 pt environ.
- Gérer les accords suivants :
  - « Je soussigné » / « Je soussignée »
  - « Né le » / « Née le »
  - « fils de Monsieur » / « fille de Monsieur »
- L’adresse personnelle doit être assemblée à partir des composants.
- Le bloc de signature doit rester visuellement décalé à droite.
- Le bloc « Rappel » doit rester en italique, avec « Rappel » souligné.

### Champs obligatoires
- genre
- civilite
- prenom
- nom
- date_naissance
- nationalite
- nom_pere
- nom_mere
- adresse personnelle
- lieu de signature
- date de signature

### Champ manuel / optionnel
- `signature.image_optionnelle`
  - si présent : insérer l’image/signature ;
  - sinon : laisser une zone de signature vide.

### Sortie attendue
- document propre, sans commentaire, sans placeholder coloré, sans artefact de transformation.

### Critères de recette
- accords de genre corrects ;
- bloc signature bien positionné ;
- rappel légal en italique ;
- document sur 1 page.

---

## DOC-002 — Autorisation de domiciliation

### Métadonnées
- doc_id : DOC-002
- générateur cible : `generate_autorisation_de_domiciliation(ctx)`
- condition : tous les dossiers
- associés dynamiques : non
- accords grammaticaux : oui (genre)

### Placeholders identifiés dans la source
- civilite
- prenom
- nom
- denomination_societe
- capital_social
- ville_siege
- cp_siege
- lieu_signature
- date_signature

### Texte de référence retenu
Le modèle transformé contient des révisions. Le texte cible à retenir pour la spec est celui avec les insertions acceptées :
- « de la Société »
- « situés au »

### Blocs documentaires
1. Cartouche titre :
   - AUTORISATION DE DOMICILIATION
2. Paragraphe unique d’autorisation.
3. Bloc lieu / date.
4. Nom du signataire en bas à droite.

### Règles de génération
- Générer le titre dans un cartouche encadré noir, centré.
- Gérer « Je soussigné » / « Je soussignée ».
- Utiliser un document très sobre, sur une seule page.
- Conserver la logique de signature avec nom affiché seul en bas à droite.

### Variables obligatoires
- genre
- civilite
- prenom
- nom
- societe.denomination
- societe.capital
- signature.lieu
- signature.date

### Point sensible sur l’adresse
Le modèle transformé n’expose pas une adresse complète des locaux : il montre une logique incomplète autour de `ville_siege / cp_siege / ville_siege`.

### Option de spec retenue en V1
- prévoir un champ `domiciliation.adresse_domiciliation_affichee` en champ libre ;
- ce champ pourra plus tard être mappé automatiquement au siège si SYDEL valide cette règle.

### Sortie attendue
- document propre, sans révisions visibles ;
- pas de duplication de ville ;
- pas de texte parasite issu de la transformation.

### Critères de recette
- texte révisé correctement retenu ;
- accord de genre correct ;
- adresse affichée conforme à la règle validée ;
- document sur 1 page.

---

## DOC-003 — Procuration

### Métadonnées
- doc_id : DOC-003
- générateur cible : `generate_procuration(ctx)`
- condition : tous les dossiers
- associés dynamiques : non
- accords grammaticaux : oui (genre)

### Placeholders identifiés dans la source
- civilite
- prenom
- nom
- num_voie_perso
- voie_perso
- ville_perso
- cp_perso
- fonction_dirigeant
- forme_sociale
- denomination_societe
- num_voie_siege
- voie_siege
- ville_siege
- cp_siege
- lieu_signature
- date_signature

### Blocs documentaires
1. Cartouche titre :
   - Procuration
2. Paragraphe d’identification du signataire et de la société.
3. Ligne d’introduction du pouvoir.
4. Bloc mandataire fixe centré :
   - SYDEL
   - 80 avenue Marceau, 75008 PARIS
   - RCS PARIS 788 531 432
   - 0153814303
5. Deux paragraphes de mandat.
6. Phrase de décharge au mandataire.
7. Bloc lieu / date.
8. Signature nominale en bas à droite.

### Règles de génération
- Gérer « Je soussigné » / « Je soussignée ».
- Conserver le bloc mandataire SYDEL en centré, avec :
  - nom en gras ;
  - adresse / RCS / téléphone en italique.
- Assembler les adresses personnelle et siège à partir des composants.
- Conserver la formulation source à l’identique sur le mandat, sauf validation juridique contraire.

### Variables obligatoires
- genre
- civilite
- prenom
- nom
- adresse personnelle
- fonction_dirigeant
- forme_sociale
- denomination sociale
- adresse du siège
- lieu de signature
- date de signature

### Constantes à externaliser en configuration
- mandataire.nom = SYDEL
- mandataire.adresse = 80 avenue Marceau, 75008 PARIS
- mandataire.rcs = RCS PARIS 788 531 432
- mandataire.telephone = 0153814303

### Sortie attendue
- document propre, sans placeholders colorés ;
- mandataire visuellement centré ;
- document sur 1 page.

### Critères de recette
- accord de genre correct ;
- bloc mandataire correctement stylé ;
- adresses correctement assemblées ;
- document sur 1 page.

---

## Recommandation pour le code Lot 1
Pour les trois générateurs du Lot 1 :
1. créer un helper de cartouche titre ;
2. créer un helper d’assemblage d’adresse ;
3. créer un helper d’accords de genre ;
4. créer un helper de bloc de signature ;
5. externaliser les constantes SYDEL pour la procuration.

## Questions restant ouvertes avant code
1. DOC-002 : adresse des locaux = champ libre ou mapping automatique du siège ?
2. Stratégie technique : gabarit propre from-scratch ou nettoyage des modèles transformés ?
